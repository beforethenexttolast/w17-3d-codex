#!/usr/bin/env python3
"""Validate p0_12 cassette evidence, separate HTML set and register integration."""
from __future__ import annotations

import csv
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


REPO = Path(__file__).resolve().parents[3]
ARCH = REPO / "10_assembly_architecture"
VIZ = ARCH / "viz/cassette"
OUT = ARCH / "evidence/p0/tables/p0_d35_cassette_output_validation.md"


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs: list[str] = []
        self.svg_count = 0
        self.external: list[tuple[str, str]] = []
        self.data_images = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and "href" in values:
            self.hrefs.append(values["href"])
        if tag == "svg":
            self.svg_count += 1
        if tag == "img":
            src = values.get("src", "")
            if src.startswith("data:image/png;base64,"):
                self.data_images += 1
            elif src:
                self.external.append((tag, src))
        if tag in {"script", "link", "source"}:
            attr = "href" if tag == "link" else "src"
            value = values.get(attr, "")
            if value:
                self.external.append((tag, value))


def check(name: str, passed: bool, detail: str, rows: list[tuple[str, str, str]]) -> bool:
    rows.append((name, "PASS" if passed else "FAIL", detail))
    return passed


def main() -> int:
    rows: list[tuple[str, str, str]] = []
    ok = True
    expected = ["index.html", "layout.html", "exploded.html", "pedestal.html", "umbilical.html"]
    scans: dict[str, Scan] = {}
    texts: dict[str, str] = {}
    for name in expected:
        path = VIZ / name
        ok &= check(f"HTML exists: cassette/{name}", path.is_file(),
                    str(path.relative_to(REPO)), rows)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        scan = Scan()
        scan.feed(text)
        texts[name], scans[name] = text, scan
        ok &= check(f"{name}: CSP",
                    "default-src 'none'" in text and "img-src data:" in text,
                    "inline-only CSP present", rows)
        ok &= check(f"{name}: theme",
                    "prefers-color-scheme" in text
                    and ':root[data-theme="dark"]' in text
                    and ':root[data-theme="light"]' in text,
                    "media preference + explicit overrides", rows)
        ok &= check(f"{name}: overflow",
                    "body { overflow-x:hidden" in text
                    and ".drawing { width:100%; overflow-x:auto" in text,
                    "body fixed; drawings scroll", rows)
        ok &= check(f"{name}: no external assets", not scan.external,
                    str(scan.external) if scan.external else "none", rows)
        ok &= check(f"{name}: local links",
                    all((path.parent / href.split("#", 1)[0]).resolve().exists()
                        for href in scan.hrefs
                        if href and not href.startswith(("#", "http:", "https:", "mailto:"))
                        and href.split("#", 1)[0]),
                    f"{len(scan.hrefs)} links checked", rows)
        ok &= check(f"{name}: confidence vocabulary",
                    all(term in text for term in
                        ("VERIFIED", "DERIVED", "DOCUMENTED", "ASSUMPTION")),
                    "four-state vocabulary present", rows)

    layout = texts.get("layout.html", "")
    ok &= check("layout: three scaled views",
                scans.get("layout.html", Scan()).svg_count >= 3
                and all(term in layout for term in
                        ("50 mm ruler", "S0=0", "SECTION X=+20")),
                f"{scans.get('layout.html', Scan()).svg_count} SVG views", rows)
    ok &= check("layout: explicit conditional verdict and keep-outs",
                all(term in layout for term in
                    ("EVERYTHING-INSIDE DOES NOT YET CLOSE", "55×45×18",
                     "30×25×10", "KO-01", "Suspension_Block_10", "battery",
                     "ESC", "motor", "belt")),
                "governors visibly named", rows)
    ok &= check("layout: embedded real STL assets",
                scans.get("layout.html", Scan()).data_images >= 6,
                f"{scans.get('layout.html', Scan()).data_images} data-URI mesh silhouettes", rows)

    exploded = texts.get("exploded.html", "")
    ok &= check("exploded: order and balloons",
                "Assembly-order strip" in exploded and "callout balloons" in exploded
                and "2.0 px/mm" in exploded and "50 mm ruler" in exploded,
                "order strip + scaled exploded SVG", rows)
    ok &= check("exploded: deferral discipline",
                all(term in exploded for term in
                    ("PDB TARGET", "55×45×18", "30×25×10", "Wi-Fi",
                     "MG90S", "DEFER", "MH-ET Live")),
                "target/assumption/deferred items visible", rows)

    pedestal = texts.get("pedestal.html", "")
    ok &= check("pedestal: fixed cut-through architecture",
                all(term in pedestal for term in
                    ("floor/front structure", "hollow", "shielded 4-pin USB",
                     "MG90S", "R1/R2", "Z98")),
                "fixed joint, conduit and retired additive stack visible", rows)
    ok &= check("pedestal: scale and gate discipline",
                "50 mm ruler" in pedestal and "3.0 px/mm" in pedestal
                and "10×18" in pedestal and "14×22" in pedestal
                and "DEFER" in pedestal and "ASSUMPTION" in pedestal,
                "to-scale gauge + physical stop states", rows)

    umbilical = texts.get("umbilical.html", "")
    ok &= check("umbilical: seats and route",
                all(term in umbilical for term in
                    ("XT60", "XT30", "5× positive-lock 3-pin",
                     "JST-XH 3-pin", "JST-XH 4-pin", "JST-XH 5-pin",
                     "U.FL", "10×18", "R1/R2", "A0", "A3", "body-off")),
                "connector seats, anchors and access present", rows)
    ok &= check("umbilical: firm map / assumed bodies",
                "CONNECTOR MAP FIRM" in umbilical
                and "body allocation" in umbilical
                and "ASSUMPTION" in umbilical
                and "straight 16×64 mm body projection" in umbilical,
                "fixed family/count separated from physical-seat assumptions", rows)

    evidence = ARCH / "evidence/p0/tables/p0_d34_cassette_fit_audit.md"
    study = ARCH / "fit_studies/ZK_electronics_cassette_fit_study.md"
    ok &= check("evidence table exists", evidence.is_file(),
                str(evidence.relative_to(REPO)), rows)
    ok &= check("fit study exists", study.is_file(), str(study.relative_to(REPO)), rows)
    if evidence.is_file():
        e = evidence.read_text(encoding="utf-8")
        ok &= check("evidence: arithmetic + CG + no-STL",
                    all(term in e for term in
                        ("58.36", "9.82", "55×45×18", "30×25×10",
                         "3 mm", "5 mm short", "C=25", "CONDITIONAL-GO",
                         "No STL")),
                    "target repack, KO deficit, sensitivity and production stop present", rows)
    if study.is_file():
        s = study.read_text(encoding="utf-8")
        headings = len(re.findall(r"^## [1-9]\.", s, re.M))
        ok &= check("study: Y-like sections", headings == 9,
                    f"{headings}/9 numbered sections", rows)

    required_joint_ids = {f"J-CAS-{number:03d}" for number in range(1, 19)}
    csv_path = ARCH / "Z_connection_joint_register.csv"
    csv_ids: set[str] = set()
    if csv_path.is_file():
        with csv_path.open(newline="", encoding="utf-8") as handle:
            csv_ids = {row["joint_id"] for row in csv.DictReader(handle)}
    ok &= check("Z register cassette joints",
                required_joint_ids <= csv_ids,
                f"{len(required_joint_ids & csv_ids)}/{len(required_joint_ids)} IDs", rows)

    register_tokens = {
        "B": (ARCH / "B_component_envelope_register.md", "B.6 Cassette"),
        "C": (ARCH / "C_clearance_keepout_register.md", "KO-30"),
        "E": (ARCH / "E_constraint_risk_register.md", "E-35"),
        "I": (ARCH / "I_zone_layer_plan.md", "I.7 Cassette"),
        "J": (ARCH / "J_component_placement_matrix.md", "J.4 Cassette"),
    }
    for label, (path, token) in register_tokens.items():
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        ok &= check(f"{label} register cassette block", token in text, token, rows)

    master = ARCH / "viz/index.html"
    master_text = master.read_text(encoding="utf-8") if master.is_file() else ""
    ok &= check("viz master cassette link",
                "BEGIN GENERATED CASSETTE LINKS" in master_text
                and 'href="cassette/index.html"' in master_text,
                "bounded link block present", rows)
    ok &= check("no cassette STL output",
                not any(VIZ.rglob("*.stl")),
                "visualization directory contains no STL", rows)

    lines = [
        "# p0_13 — cassette output validation",
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
