#!/usr/bin/env python3
"""Validate the generated W17 connection register, manual block and HTML atlas.

Run after p0_10. Writes a Markdown evidence table and exits non-zero on failure.
"""
from __future__ import annotations

import csv
from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import re
import sys


REPO = Path(__file__).resolve().parents[3]
ARCH = REPO / "10_assembly_architecture"
VIZ = ARCH / "viz"
CONNECTIONS = VIZ / "connections"
OUT = ARCH / "evidence/p0/tables/p0_d33_connection_output_validation.md"
GENERATOR = Path(__file__).with_name("p0_10_connection_visualizations.py")


def load_generator():
    spec = importlib.util.spec_from_file_location("p0_10_connections", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs: list[str] = []
        self.svg_count = 0
        self.external_assets: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and "href" in values:
            self.hrefs.append(values["href"])
        if tag == "svg":
            self.svg_count += 1
        if tag in {"img", "script", "link", "source"}:
            attr = "href" if tag == "link" else "src"
            value = values.get(attr, "")
            if value and not value.startswith("data:"):
                self.external_assets.append((tag, value))


def check(name: str, passed: bool, detail: str, rows: list[tuple[str, str, str]]) -> bool:
    rows.append((name, "PASS" if passed else "FAIL", detail))
    return passed


def main() -> int:
    data = load_generator()
    expected = sorted(data.JOINTS, key=lambda j: (j.order, j.joint_id))
    expected_ids = [j.joint_id for j in expected]
    expected_pages = ["index.html"] + [meta[2] for meta in data.ASSEMBLIES.values()]
    rows: list[tuple[str, str, str]] = []
    ok = True

    # Source-data invariants.
    ok &= check("source joint IDs unique", len(expected_ids) == len(set(expected_ids)),
                f"{len(expected_ids)} unique rows", rows)
    ok &= check("source assembly coverage",
                {j.assembly for j in expected} == set(data.ASSEMBLIES),
                f"{len(data.ASSEMBLIES)} assemblies", rows)
    full_fields = all(
        all(getattr(j, field) not in ("", None) for field in (
            "joint_id", "zone", "assembly", "asm_step", "part_a", "part_b",
            "hardware", "interface", "fastening_retention", "dependency",
            "instruction", "tool", "torque_threadlock", "confidence",
            "asm_check", "disposition",
        ))
        for j in expected
    )
    ok &= check("per-joint field completeness", full_fields,
                "parts, BOM hardware, interface, retention, order, dependency, tool, torque, confidence and ASM check", rows)

    # Explicit in-transit/unselected deferral discipline.
    deferral_groups = {
        "MG90S": lambda j: "MG90S" in (j.part_a + j.part_b),
        "rear 68 mm shock": lambda j: "68 mm rear shock" in (j.part_a + j.part_b),
        "magnet-dependent": lambda j: j.joint_id.startswith("J-SNS-"),
        "2S pack": lambda j: j.joint_id == "J-PWR-002",
        "charge module/port/interlock": lambda j: (
            j.joint_id.startswith("J-CHG-") or j.joint_id == "J-CAS-005"
        ),
        "in-transit tyres": lambda j: j.joint_id in {
            "J-FRT-022", "J-FRT-023", "J-REA-023", "J-REA-024"
        },
    }
    for label, predicate in deferral_groups.items():
        selected = [j for j in expected if predicate(j)]
        good = bool(selected) and all(j.disposition == "DEFER" for j in selected)
        ok &= check(f"DEFER discipline: {label}", good,
                    f"{len(selected)} row(s): " + ", ".join(j.joint_id for j in selected), rows)

    # CSV register is complete, unique and sorted by assembly order.
    csv_path = ARCH / "Z_connection_joint_register.csv"
    ok &= check("CSV register exists", csv_path.is_file(), str(csv_path.relative_to(REPO)), rows)
    csv_rows = []
    if csv_path.is_file():
        with csv_path.open(newline="", encoding="utf-8") as handle:
            csv_rows = list(csv.DictReader(handle))
    csv_ids = [row.get("joint_id", "") for row in csv_rows]
    ok &= check("CSV row/ID parity", csv_ids == expected_ids,
                f"{len(csv_ids)}/{len(expected_ids)} rows in canonical order", rows)
    ok &= check("CSV sortable columns",
                bool(csv_rows) and all(name in csv_rows[0] for name in
                    ("zone", "order", "asm_step", "confidence", "disposition")),
                "zone/order/ASM/confidence/disposition present", rows)

    # Markdown register and manual must cite every Joint ID.
    register = ARCH / "Z_connection_joint_register.md"
    register_text = register.read_text(encoding="utf-8") if register.is_file() else ""
    ok &= check("Markdown register exists", register.is_file(), str(register.relative_to(REPO)), rows)
    missing_register = [jid for jid in expected_ids if jid not in register_text]
    ok &= check("Markdown register Joint-ID coverage", not missing_register,
                "all IDs present" if not missing_register else "missing: " + ", ".join(missing_register), rows)
    ok &= check("Markdown zone-sort view",
                "## Z.2 Zone-sort index" in register_text and "sortable authority" in register_text,
                "assembly-order table + zone index + sortable CSV declaration", rows)

    manual = ARCH / "P_assembly_master_manual.md"
    manual_text = manual.read_text(encoding="utf-8") if manual.is_file() else ""
    ok &= check("manual generated block",
                data.MANUAL_START in manual_text and data.MANUAL_END in manual_text,
                "bounded p0_10 block present", rows)
    missing_manual = [jid for jid in expected_ids if jid not in manual_text]
    ok &= check("manual Joint-ID coverage", not missing_manual,
                "all IDs present" if not missing_manual else "missing: " + ", ".join(missing_manual), rows)
    ok &= check("manual charge + closure steps",
                "### ASM-59" in manual_text and "### ASM-60" in manual_text,
                "deferred charge integration + connection closure audit", rows)

    # HTML connection pages: self-contained, theme-aware, scaled and complete.
    page_joint_ids: set[str] = set()
    for name in expected_pages:
        path = CONNECTIONS / name
        ok &= check(f"HTML exists: connections/{name}", path.is_file(),
                    str(path.relative_to(REPO)), rows)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        scan = Scan()
        scan.feed(text)
        ok &= check(f"{name}: CSP",
                    "default-src 'none'" in text and "img-src data:" in text,
                    "inline-only CSP present", rows)
        ok &= check(f"{name}: theme",
                    "prefers-color-scheme" in text and ':root[data-theme="dark"]' in text
                    and ':root[data-theme="light"]' in text,
                    "media preference + explicit overrides", rows)
        ok &= check(f"{name}: overflow",
                    "body { overflow-x:hidden" in text
                    and ".drawing { width:100%; overflow-x:auto" in text,
                    "body fixed; drawings scroll", rows)
        ok &= check(f"{name}: no external assets", not scan.external_assets,
                    str(scan.external_assets) if scan.external_assets else "none", rows)
        ok &= check(f"{name}: local links",
                    all((path.parent / href.split("#", 1)[0]).resolve().exists()
                        for href in scan.hrefs
                        if href and not href.startswith(("#", "http:", "https:", "mailto:"))
                        and href.split("#", 1)[0]),
                    f"{len(scan.hrefs)} links checked", rows)
        if name == "index.html":
            continue
        ok &= check(f"{name}: exploded SVG", scan.svg_count >= 1 and "assembly axis" in text,
                    f"{scan.svg_count} inline SVG(s)", rows)
        ok &= check(f"{name}: scale/ruler", "1.5 px/mm" in text and "50 mm ruler" in text,
                    "declared per exploded strip", rows)
        ok &= check(f"{name}: confidence style",
                    "VERIFIED" in text and "DOCUMENTED" in text and "ASSUMPTION" in text
                    and "dashed + hatched" in text,
                    "solid/dotted/dashed-hatched legend", rows)
        ok &= check(f"{name}: real mesh silhouette",
                    "data:image/png;base64," in text and "real STL silhouettes" in text,
                    "embedded data-URI mesh silhouette(s)", rows)
        ok &= check(f"{name}: order strip", "Assembles in this order" in text,
                    "short linked sequence present", rows)
        page_joint_ids.update(re.findall(r"J-[A-Z]{3}-\d{3}", text))

    missing_pages = [jid for jid in expected_ids if jid not in page_joint_ids]
    ok &= check("HTML Joint-ID coverage", not missing_pages,
                f"{len(page_joint_ids)}/{len(expected_ids)} unique IDs"
                if not missing_pages else "missing: " + ", ".join(missing_pages), rows)

    master = VIZ / "index.html"
    master_text = master.read_text(encoding="utf-8") if master.is_file() else ""
    ok &= check("zone master links connection atlas",
                data.INDEX_START in master_text and 'href="connections/index.html"' in master_text,
                "generated connection block present", rows)
    ok &= check("zone master links all assemblies",
                all(f'href="connections/{meta[2]}"' in master_text
                    for meta in data.ASSEMBLIES.values()),
                f"{len(data.ASSEMBLIES)} direct assembly links", rows)

    # Requested physical-family coverage.
    corpus = (register_text + "\n" + manual_text).lower()
    required_terms = [
        "25t", "m3 ball stud", "m4 rod-end", "turnbuckle", "king pin",
        "8×12×3.5", "12×21×5", "d5×m3", "75t", "28t", "140 mm belt",
        "68 mm rear shock", "battery tray", "usb-c 2s balancing", "charge/run",
        "esp32", "rp1", "wifi", "ubec", "capacitor", "camera", "blower",
        "max98357a", "speaker", "ws2812b", "hall", "magnet", "heat-set",
        "shell landing", "front wing",
    ]
    missing_terms = [term for term in required_terms if term not in corpus]
    ok &= check("requested joint-family coverage", not missing_terms,
                "all requested families found" if not missing_terms else "missing: " + ", ".join(missing_terms), rows)

    lines = [
        "# p0_11 — connection output validation",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    lines.extend(f"| {a} | **{b}** | {c} |" for a, b, c in rows)
    lines += [
        "",
        f"**Verdict: {'PASS' if ok else 'FAIL'} — "
        f"{sum(result == 'PASS' for _, result, _ in rows)}/{len(rows)} checks passed.**",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(lines[-2])
    print("WROTE", OUT)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
