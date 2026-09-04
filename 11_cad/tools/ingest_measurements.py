#!/usr/bin/env python3
"""ingest_measurements.py — turn a MEASUREMENT_RECORD_SHEET.csv into a
reviewable patch against w17_params.scad.

=======================================================================
 CONVENTION THIS TOOL DEPENDS ON (read this before filling in a sheet)
=======================================================================
w17_params.scad tags every shared dimension with a provenance comment.
This tool retires exactly one class of those tags: lines whose comment
is, verbatim, "ASSUMED (see §9)" — the ones §9 lists under the owner's
name and a measurement (M-nn) or coupon (C-1) that retires them. It
does NOT touch "ASSUMED-adjacent" (screw_m3_clear_d), ESTIMATED,
POLICY, DERIVED, DOCUMENTED lines, or the deliberately-undef
drs_arm_pivot_span — those are out of scope by construction, not by
guesswork: the regex only matches the literal "ASSUMED (see §9)" tag.

The CSV schema (agreed with B1's brief, B1.md / B1's
MEASUREMENT_SITTING_RUNBOOK.md — B1 may not have finished; this tool
was implemented against the schema stated in both briefs, and is
deliberately permissive about anything B1 adds *in addition* to it):

    id,quantity,unit,value,tolerance,photo_ref,notes

    id          the sheet's row id (e.g. M-03, M-03(f), C-1-step4).
                Carried into the patch as provenance; never parsed for
                meaning.
    quantity    MUST equal the exact w17_params.scad parameter name it
                measures (e.g. "esp_thk_headers"). This is the one
                convention this tool invents rather than reads off a
                shared doc, because it is the only mapping that needs
                no lookup table and stays correct if the file's own
                names ever change: one CSV row measures one named
                parameter. A quantity that measures TWO parameters
                (e.g. one caliper reading for a hole spacing that sets
                both esp_hole_dx and esp_hole_dy) needs two CSV rows,
                one per parameter — this mirrors w17_params.scad's own
                rule that every physical number is a named parameter.
                If B1's actual sheet uses a different convention for
                "quantity" (a free-text description rather than the
                bare parameter name), rows will simply not match and
                will be reported as unmatched CSV rows — nothing is
                silently applied on a guessed mapping.
    unit        mm (default assumed if blank) or g or deg. "enum" for
                the two string-valued params (esp_usb_type,
                esp_usb_edge) — value is then the literal string
                without quotes (e.g. usb_c).
    value       the measured number, or the literal for an enum row.
                A row with an empty value, or notes containing
                "could not" (per the measurement prompt's own
                convention for an untakeable measurement), is skipped
                and reported, never coerced into a number.
    tolerance   carried into the patch comment; not otherwise used.
    photo_ref   carried into the patch comment when present.
    notes       carried into the patch comment when present.

=======================================================================
 WHAT THE PATCH DOES AND DOES NOT TOUCH
=======================================================================
For every CSV row whose `quantity` matches a live "ASSUMED (see §9)"
parameter in w17_params.scad, this tool rewrites ONLY that parameter's
own definition line: the value, and the tag from "ASSUMED (see §9)" to
"MEASURED(<sheet>#<id>, <date>)", keeping whatever descriptive text
followed the old tag (e.g. "brand-dependent") so the rationale is not
lost, and appending tolerance/photo_ref/notes when the CSV supplied
them.

It deliberately does NOT touch section 9's own ASSUMED table, the AA
study's §12, or the measurement-session prompt — the repo's own
editing rule (11_cad/README.md "Editing rules") says a landed
measurement updates three places, and some §9 rows bundle several
parameters under one M-nn (e.g. M-03 lists six). Auto-editing a
bundled row on a partial match risks deleting the record of params
that are still ASSUMED. The patch report instead PRINTS which §9
rows are now fully retired (every parameter they list has a matching
MEASURED line) so a human can strike them in the same commit, and
which are partially retired.

=======================================================================
 USAGE
=======================================================================
    ingest_measurements.py --sheet MEASUREMENT_RECORD_SHEET.csv
        Dry run (the default). Prints a unified diff against
        w17_params.scad and a summary: matched / unmatched CSV rows,
        §9 rows fully vs. partially retired. Writes nothing.

    ingest_measurements.py --sheet SHEET.csv --apply
        Writes the patched w17_params.scad in place, then re-renders
        (./render.sh --stl by default; --skip-render to suppress) and
        reports PASS/FAIL. On any assert() failure or non-clean
        render, the tool still leaves the patched file in place (it is
        a normal, reviewable git diff at that point) but exits
        non-zero and says so plainly — it does not revert your worktree.

    ingest_measurements.py --sheet SHEET.csv --params /other/w17_params.scad
        Patch a different copy (mainly for the test suite).

Exit codes: 0 clean (dry run with no errors, or --apply that rendered
clean); 1 CSV or matching problem; 2 --apply rendered dirty.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import re
import subprocess
import sys
from pathlib import Path

REQUIRED_HEADERS = ["id", "quantity", "unit", "value", "tolerance", "photo_ref", "notes"]

# Matches exactly the "ASSUMED (see §9)" tag this tool is scoped to.
# Captures: name, the "name<ws>=<ws>" prefix, the current value token,
# the ";" plus trailing whitespace before the comment, and whatever
# descriptive text follows the tag on the same line.
ASSUMED_RE = re.compile(
    r"^(?P<prefix>(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?P<sp1>[ \t]+)=(?P<sp2>[ \t]+))"
    r"(?P<value>[^;]+?)"
    r"(?P<mid>;(?P<sp3>[ \t]+)//[ \t]*)"
    r"ASSUMED \(see §9\)"
    r"(?P<rest>.*)$"
)

# A §9 table row, e.g. "//  M-03  esp_thk_headers                                13.0"
# Params are whitespace/slash separated identifiers on the row.
SECTION9_ROW_RE = re.compile(r"^//\s+(?P<mid>[A-Za-z0-9\-\(\)]+)\s+(?P<rest>.*)$")
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


class Row:
    __slots__ = ("id", "quantity", "unit", "value", "tolerance", "photo_ref", "notes", "lineno")

    def __init__(self, d: dict, lineno: int):
        self.id = (d.get("id") or "").strip()
        self.quantity = (d.get("quantity") or "").strip()
        self.unit = (d.get("unit") or "").strip()
        self.value = (d.get("value") or "").strip()
        self.tolerance = (d.get("tolerance") or "").strip()
        self.photo_ref = (d.get("photo_ref") or "").strip()
        self.notes = (d.get("notes") or "").strip()
        self.lineno = lineno


def load_sheet(path: Path) -> list[Row]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"{path}: empty CSV (no header row)")
        missing = [h for h in REQUIRED_HEADERS if h not in reader.fieldnames]
        if missing:
            raise ValueError(
                f"{path}: missing required column(s) {missing}; "
                f"header row was {reader.fieldnames}"
            )
        rows = []
        for i, d in enumerate(reader, start=2):  # header is line 1
            rows.append(Row(d, i))
        return rows


def find_assumed_params(scad_lines: list[str]) -> dict[str, tuple[int, re.Match]]:
    """name -> (0-based line index, regex Match) for every live ASSUMED
    (see §9) definition line. Only matches definitions (before the §9
    table itself), never the §9 table's own commented rows, because
    ASSUMED_RE requires an executable "name = value;" prefix that a
    "//" comment line can never produce."""
    found: dict[str, tuple[int, re.Match]] = {}
    for i, line in enumerate(scad_lines):
        m = ASSUMED_RE.match(line)
        if m:
            found[m.group("name")] = (i, m)
    return found


def find_section9_rows(scad_lines: list[str]) -> list[tuple[int, str, list[str]]]:
    """Return [(line_index, m_id, [param_names_on_that_row]), ...] for
    section 9's table, i.e. every commented row of the form
    '//  M-03  esp_hole_dx / esp_hole_dy / esp_hole_d  33/25/3.2'."""
    out = []
    in_section9 = False
    seen_row = False
    for i, line in enumerate(scad_lines):
        if "===  ASSUMED" in line and "THE OWNER'S LIST" in line:
            in_section9 = True
            continue
        if not in_section9:
            continue
        # The banner's OWN "// ---" underline (right after "9. === ...")
        # must not end the table before it starts — only a divider seen
        # AFTER at least one real row closes the table.
        if seen_row and line.strip().startswith("// -----"):
            break
        m = SECTION9_ROW_RE.match(line)
        if not m:
            continue
        row_id = m.group("mid")
        rest = m.group("rest")
        # Parameter names are the identifiers before two-or-more spaces
        # (the value column), stripped of stray "<-" annotations.
        head = re.split(r"\s{2,}", rest, maxsplit=1)[0]
        params = [tok for tok in re.split(r"\s*/\s*", head) if IDENT_RE.fullmatch(tok)]
        if params:
            seen_row = True
            out.append((i, row_id, params))
    return out


def build_patch(scad_path: Path, rows: list[Row], sheet_name: str, date: str):
    """Returns (new_lines, report_lines, matched_names, errors)."""
    text = scad_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    assumed = find_assumed_params(lines)

    report: list[str] = []
    errors: list[str] = []
    matched_names: set[str] = set()
    skipped_rows: list[Row] = []
    unmatched_rows: list[Row] = []
    dup_targets: dict[str, list[Row]] = {}

    for row in rows:
        if not row.quantity:
            skipped_rows.append(row)
            continue
        if not row.value or "could not" in row.notes.lower() or "could not" in row.value.lower():
            skipped_rows.append(row)
            continue
        dup_targets.setdefault(row.quantity, []).append(row)

    for quantity, candidate_rows in dup_targets.items():
        if quantity not in assumed:
            unmatched_rows.extend(candidate_rows)
            continue
        if len(candidate_rows) > 1:
            ids = ", ".join(r.id or f"line {r.lineno}" for r in candidate_rows)
            errors.append(
                f"CONFLICT: {len(candidate_rows)} rows target '{quantity}' ({ids}); "
                f"skipping all of them — resolve to one row per parameter and re-run."
            )
            continue
        row = candidate_rows[0]
        idx, m = assumed[quantity]
        old_value = m.group("value").strip()

        is_string_param = old_value.startswith('"')
        if is_string_param or row.unit.lower() == "enum":
            new_value_token = f'"{row.value.strip().strip(chr(34))}"'
        else:
            try:
                float(row.value)
            except ValueError:
                errors.append(
                    f"BAD VALUE: row {row.id or row.lineno} quantity='{quantity}' "
                    f"value='{row.value}' is not numeric and unit is not 'enum'; skipped."
                )
                continue
            new_value_token = row.value.strip()

        provenance = f"MEASURED({sheet_name}#{row.id or ('line ' + str(row.lineno))}, {date})"
        extras = []
        if row.tolerance:
            extras.append(f"tol {row.tolerance}")
        if row.photo_ref:
            extras.append(f"photo {row.photo_ref}")
        if row.notes:
            extras.append(row.notes)
        extra_txt = f" [{'; '.join(extras)}]" if extras else ""
        old_rest = m.group("rest")  # keeps the pre-existing rationale text, if any

        new_line = (
            f"{m.group('prefix')}{new_value_token}{m.group('mid')}"
            f"{provenance}{extra_txt}{old_rest}\n"
        )
        lines[idx] = new_line
        matched_names.add(quantity)
        report.append(
            f"  MATCH  {quantity:<20} {old_value!s:>10}  ->  {new_value_token:<10}  "
            f"(row {row.id or row.lineno})"
        )

    for row in unmatched_rows:
        report.append(
            f"  MISS   quantity='{row.quantity}' (row {row.id or row.lineno}) — "
            f"no live 'ASSUMED (see §9)' parameter named '{row.quantity}' in {scad_path.name}"
        )
    for row in skipped_rows:
        why = "empty value" if not row.value else "marked 'could not' / no measurement taken"
        report.append(f"  SKIP   row {row.id or row.lineno} quantity='{row.quantity}': {why}")

    # section 9 bookkeeping report (informational only — never edited).
    # find_section9_rows uses a plain "/"-split, which mis-tokenizes the
    # handful of §9 rows that use elliptical shorthand instead of full
    # names (e.g. "ko01_x_lo/x_hi/l_half/z_lo/z_hi" -> a bogus "x_hi"
    # fragment; "gcs_tx_*, ..." wildcard/comma rows aren't tokenized at
    # all). Rather than guess at the abbreviation, every extracted token
    # is checked against the file's REAL parameter names (either still
    # ASSUMED, or matched by this run) before being reported — a bogus
    # fragment that is neither is silently dropped, never reported as
    # "retired" or "still ASSUMED". This means shorthand/wildcard §9
    # rows (currently M-02, M-13, M-17) may be under-reported here;
    # check those by hand.
    known_params = set(assumed.keys()) | matched_names
    sec9 = find_section9_rows(lines)
    for _idx, row_id, raw_params in sec9:
        params = [p for p in raw_params if p in known_params]
        if not params:
            continue
        retired = [p for p in params if p in matched_names]
        still_assumed = [p for p in params if p not in matched_names and p in assumed]
        if retired and not still_assumed:
            report.append(f"  SEC9   {row_id}: fully retired ({', '.join(params)}) — strike this row by hand")
        elif retired:
            report.append(
                f"  SEC9   {row_id}: partially retired — {', '.join(retired)} now MEASURED, "
                f"{', '.join(still_assumed) or '(none)'} still ASSUMED"
            )

    return lines, report, matched_names, errors


def unified_diff(old_text: str, new_text: str, path_label: str) -> str:
    import difflib

    return "".join(
        difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f"a/{path_label}",
            tofile=f"b/{path_label}",
        )
    )


def render_check(cad_dir: Path, openscad: str | None) -> tuple[bool, str]:
    import os

    cmd = ["./render.sh", "--stl"]
    env = None
    if openscad:
        env = {**os.environ, "OPENSCAD": openscad}
    proc = subprocess.run(
        cmd, cwd=str(cad_dir), capture_output=True, text=True, env=env
    )
    ok = proc.returncode == 0
    out = proc.stdout + proc.stderr
    return ok, out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", required=True, type=Path, help="MEASUREMENT_RECORD_SHEET.csv")
    ap.add_argument(
        "--params",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "w17_params.scad",
        help="w17_params.scad to patch (default: ../w17_params.scad next to this tool)",
    )
    ap.add_argument("--apply", action="store_true", help="write the patch (default: dry run, diff only)")
    ap.add_argument("--skip-render", action="store_true", help="with --apply, skip the post-apply re-render")
    ap.add_argument("--openscad", default=None, help="OpenSCAD binary (passed through as OPENSCAD=...)")
    ap.add_argument("--date", default=None, help="override the MEASURED(...) date, default today (YYYY-MM-DD)")
    args = ap.parse_args(argv)

    date = args.date or _dt.date.today().isoformat()

    if not args.sheet.exists():
        print(f"error: sheet not found: {args.sheet}", file=sys.stderr)
        return 1
    try:
        rows = load_sheet(args.sheet)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if not args.params.exists():
        print(f"error: params file not found: {args.params}", file=sys.stderr)
        return 1

    old_text = args.params.read_text(encoding="utf-8")
    new_lines, report, matched, errors = build_patch(args.params, rows, args.sheet.name, date)
    new_text = "".join(new_lines)

    print(f"ingest_measurements.py — {args.sheet}  ->  {args.params}")
    print(f"  {len(rows)} CSV row(s) read, {len(matched)} parameter(s) matched")
    print()
    for line in report:
        print(line)
    if errors:
        print()
        for e in errors:
            print(f"  ERROR  {e}")

    diff = unified_diff(old_text, new_text, args.params.name)
    print()
    if diff:
        print(diff)
    else:
        print("(no changes — nothing matched)")

    if errors:
        return 1

    if not args.apply:
        print()
        print("dry run only — nothing written. Re-run with --apply to write the patch.")
        return 0

    if not matched:
        print()
        print("nothing matched — not writing (no-op apply refused).")
        return 0

    args.params.write_text(new_text, encoding="utf-8")
    print()
    print(f"applied: wrote {args.params}")

    if args.skip_render:
        print("--skip-render given: not re-rendering.")
        return 0

    cad_dir = args.params.parent
    ok, out = render_check(cad_dir, args.openscad)
    print()
    print("post-apply render (./render.sh --stl):")
    print(out)
    if ok:
        print("RENDER PASS — geometry still clean after the patch.")
        return 0
    else:
        print("RENDER FAIL — the patched file is still on disk (this is now a normal git diff); "
              "fix the offending value/assert before committing.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
