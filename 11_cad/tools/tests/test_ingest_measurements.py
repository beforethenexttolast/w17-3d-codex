#!/usr/bin/env python3
"""Unit tests for ingest_measurements.py.

No pytest dependency (none is installed in this environment) — plain
unittest, runnable as:

    python3 -m unittest discover -s 11_cad/tools/tests -v

or directly:

    python3 11_cad/tools/tests/test_ingest_measurements.py

These tests never touch the real w17_params.scad or the real
MEASUREMENT_RECORD_SHEET.csv — everything runs against the small
fixtures in tests/fixtures/, and --apply is exercised only against a
tempfile copy.
"""
from __future__ import annotations

import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(TOOLS_DIR))

import ingest_measurements as im  # noqa: E402


class TestLoadSheet(unittest.TestCase):
    def test_reads_all_rows(self):
        rows = im.load_sheet(FIXTURES / "sample_measurements.csv")
        self.assertEqual(len(rows), 7)
        self.assertEqual(rows[0].id, "M-03")
        self.assertEqual(rows[0].quantity, "esp_thk_headers")
        self.assertEqual(rows[0].value, "12.4")

    def test_missing_header_raises(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.csv"
            bad.write_text("id,quantity,unit,value\nM-01,x,mm,1\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                im.load_sheet(bad)

    def test_missing_file_is_caller_responsibility(self):
        with self.assertRaises(FileNotFoundError):
            im.load_sheet(FIXTURES / "does_not_exist.csv")


class TestFindAssumedParams(unittest.TestCase):
    def setUp(self):
        self.lines = (FIXTURES / "sample_params.scad").read_text(encoding="utf-8").splitlines(keepends=True)

    def test_finds_only_true_assumed_tags(self):
        found = im.find_assumed_params(self.lines)
        names = set(found.keys())
        self.assertEqual(
            names,
            {"esp_thk_headers", "board_seat_x0", "esp_usb_type", "guide_top_z", "pdb_len", "pdb_wid"},
        )
        # ASSUMED-adjacent must never be matched
        self.assertNotIn("screw_m3_clear_d", names)

    def test_captures_current_value(self):
        found = im.find_assumed_params(self.lines)
        _, m = found["esp_thk_headers"]
        self.assertEqual(m.group("value").strip(), "13.0")
        _, m2 = found["esp_usb_type"]
        self.assertEqual(m2.group("value").strip(), '"usb_c"')


class TestFindSection9Rows(unittest.TestCase):
    def test_bundled_rows_list_every_param(self):
        # Real w17_params.scad §9 reuses the same M-nn id across several
        # TABLE ROWS (e.g. "M-03  esp_thk_headers", "M-03  esp_usb_type"
        # are two separate rows), so find_section9_rows must return a
        # LIST, not a dict keyed by id — this fixture mirrors that.
        lines = (FIXTURES / "sample_params.scad").read_text(encoding="utf-8").splitlines(keepends=True)
        rows = im.find_section9_rows(lines)
        m03_params = [p for _idx, row_id, params in rows if row_id == "M-03" for p in params]
        self.assertIn("esp_thk_headers", m03_params)
        self.assertIn("board_seat_x0", m03_params)
        self.assertIn("esp_usb_type", m03_params)
        m06_rows = [params for _idx, row_id, params in rows if row_id == "M-06"]
        self.assertEqual(m06_rows, [["pdb_len", "pdb_wid"]])
        m07_rows = [params for _idx, row_id, params in rows if row_id == "M-07"]
        self.assertEqual(m07_rows, [["guide_top_z"]])


class TestBuildPatch(unittest.TestCase):
    def setUp(self):
        self.params_path = FIXTURES / "sample_params.scad"
        self.rows = im.load_sheet(FIXTURES / "sample_measurements.csv")

    def test_matches_expected_params_only(self):
        _lines, _report, matched, errors = im.build_patch(
            self.params_path, self.rows, "sample_measurements.csv", "2026-09-05"
        )
        # guide_top_z is excluded: it has a CONFLICT (two rows target it)
        self.assertEqual(matched, {"esp_thk_headers", "board_seat_x0", "esp_usb_type"})
        self.assertTrue(any("CONFLICT" in e for e in errors))

    def test_numeric_value_is_written_literally(self):
        lines, _report, _matched, _errors = im.build_patch(
            self.params_path, self.rows, "sample_measurements.csv", "2026-09-05"
        )
        joined = "".join(lines)
        self.assertIn("esp_thk_headers   = 12.4;", joined)
        self.assertIn("MEASURED(sample_measurements.csv#M-03, 2026-09-05)", joined)

    def test_enum_value_is_quoted(self):
        lines, _report, _matched, _errors = im.build_patch(
            self.params_path, self.rows, "sample_measurements.csv", "2026-09-05"
        )
        joined = "".join(lines)
        self.assertIn('esp_usb_type      = "usb_c";', joined)

    def test_unmatched_and_could_not_rows_are_reported_not_applied(self):
        lines, report, matched, _errors = im.build_patch(
            self.params_path, self.rows, "sample_measurements.csv", "2026-09-05"
        )
        joined_report = "\n".join(report)
        self.assertIn("not_a_real_param", joined_report)
        self.assertIn("MISS", joined_report)
        self.assertTrue(any("SKIP" in r and "M-06a" in r for r in report))
        # pdb_len must be untouched: its only CSV row was "could not"
        self.assertNotIn("pdb_len", matched)
        joined = "".join(lines)
        self.assertIn('pdb_len           = 55;     // ASSUMED (see §9)', joined)

    def test_conflicting_rows_leave_target_untouched(self):
        lines, _report, matched, errors = im.build_patch(
            self.params_path, self.rows, "sample_measurements.csv", "2026-09-05"
        )
        self.assertNotIn("guide_top_z", matched)
        joined = "".join(lines)
        self.assertIn("guide_top_z       = 30.0;   // ASSUMED (see §9)", joined)
        self.assertTrue(any("guide_top_z" in e for e in errors))

    def test_never_touches_unrelated_lines(self):
        old_text = self.params_path.read_text(encoding="utf-8")
        lines, _report, _matched, _errors = im.build_patch(
            self.params_path, self.rows, "sample_measurements.csv", "2026-09-05"
        )
        new_text = "".join(lines)
        old_lines = old_text.splitlines()
        new_lines = new_text.splitlines()
        self.assertEqual(len(old_lines), len(new_lines))
        changed = [i for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
        # Only the 3 matched definition lines change; §9 table, the
        # ASSUMED-adjacent line, and everything else stay byte-identical.
        self.assertEqual(len(changed), 3)
        self.assertNotIn(
            "screw_m3_clear_d  = 3.4;    // ASSUMED-adjacent: typical M3 clearance; confirmed by coupon C-1",
            [old_lines[i] for i in changed],
        )

    def test_section9_reports_partial_vs_full_retirement(self):
        _lines, report, _matched, _errors = im.build_patch(
            self.params_path, self.rows, "sample_measurements.csv", "2026-09-05"
        )
        joined_report = "\n".join(report)
        # M-03 bundles 3 params, all matched here -> fully retired
        self.assertRegex(joined_report, r"SEC9\s+M-03: fully retired")
        # M-06 bundles pdb_len/pdb_wid; pdb_len was "could not" so neither
        # is matched -> M-06 must not be reported at all (nothing retired)
        self.assertNotIn("SEC9   M-06", joined_report)


class TestApplyWritesAndIsIdempotentOnDryRun(unittest.TestCase):
    def test_dry_run_never_writes(self):
        with tempfile.TemporaryDirectory() as d:
            params_copy = Path(d) / "w17_params.scad"
            shutil.copy(FIXTURES / "sample_params.scad", params_copy)
            before = params_copy.read_text(encoding="utf-8")
            rc = im.main(
                [
                    "--sheet",
                    str(FIXTURES / "sample_measurements.csv"),
                    "--params",
                    str(params_copy),
                ]
            )
            after = params_copy.read_text(encoding="utf-8")
            self.assertEqual(before, after)
            # errors (CONFLICT) exist in this fixture, so exit code is 1
            self.assertEqual(rc, 1)

    def test_apply_writes_only_matched_lines(self):
        with tempfile.TemporaryDirectory() as d:
            params_copy = Path(d) / "w17_params.scad"
            shutil.copy(FIXTURES / "sample_params.scad", params_copy)
            # Use only the clean, unambiguous rows for this test so --apply
            # can succeed (the full fixture sheet has a deliberate CONFLICT
            # row that makes build_patch report an error and main() exit 1).
            clean_csv = Path(d) / "clean.csv"
            with (FIXTURES / "sample_measurements.csv").open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = [r for r in reader if r["id"] in ("M-03", "M-03h", "M-03f")]
            with clean_csv.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=im.REQUIRED_HEADERS)
                writer.writeheader()
                writer.writerows(rows)

            rc = im.main(
                [
                    "--sheet",
                    str(clean_csv),
                    "--params",
                    str(params_copy),
                    "--apply",
                    "--skip-render",
                ]
            )
            self.assertEqual(rc, 0)
            new_text = params_copy.read_text(encoding="utf-8")
            self.assertIn("esp_thk_headers   = 12.4;", new_text)
            self.assertIn("board_seat_x0     = 3.0;    // MEASURED(clean.csv#M-03h", new_text)
            self.assertIn("guide_top_z       = 30.0;   // ASSUMED (see §9)", new_text)  # untouched


if __name__ == "__main__":
    unittest.main()
