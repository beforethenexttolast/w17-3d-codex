#!/usr/bin/env python3
"""Validate the remaining-component studies, evidence and self-contained HTML.

Run after p0_07 and p0_08.  Writes one Markdown validation table and exits
non-zero on any failed invariant.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys

import p0_07_zone_fit_rollup as D


REPO = Path(__file__).resolve().parents[3]
ARCH = REPO / "10_assembly_architecture"
VIZ = ARCH / "viz"
OUT = ARCH / "evidence/p0/tables/p0_d32_zone_output_validation.md"


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.svg_count = 0
        self.external_assets = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if tag == "svg":
            self.svg_count += 1
        if tag in {"img", "script", "link", "source"}:
            attr = "href" if tag == "link" else "src"
            value = a.get(attr, "")
            if value and not value.startswith("data:"):
                self.external_assets.append((tag, value))


def check(name, ok, detail, rows):
    rows.append((name, "PASS" if ok else "FAIL", detail))
    return ok


def main() -> int:
    rows = []
    ok = True
    expected_html = ["index.html"] + [m["html"] for m in D.ZONE_META.values()]
    expected_studies = ["README.md"] + [m["study"] for m in D.ZONE_META.values()]
    expected_tables = [
        "p0_d28_zone_component_envelopes.md",
        "p0_d29_zone_placements.csv",
        "p0_d30_mass_balance.md",
        "p0_d31_fit_gates.md",
    ]

    for name in expected_html:
        path = VIZ / name
        ok &= check(f"HTML exists: {name}", path.is_file(), str(path.relative_to(REPO)), rows)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        scan = Scan()
        scan.feed(text)
        zone_page = name != "index.html"
        ok &= check(f"{name}: CSP", "default-src 'none'" in text and
                    "style-src 'unsafe-inline'" in text and "img-src data:" in text,
                    "inline-only CSP present", rows)
        ok &= check(f"{name}: theme", "prefers-color-scheme" in text and
                    ':root[data-theme="dark"]' in text and ':root[data-theme="light"]' in text,
                    "media preference + explicit overrides", rows)
        ok &= check(f"{name}: overflow", "body { overflow-x:hidden" in text and
                    ".drawing { width:100%; overflow-x:auto" in text,
                    "body fixed; drawing scrolls", rows)
        minimum_svg = 2 if zone_page else 1
        ok &= check(f"{name}: SVG count", scan.svg_count >= minimum_svg,
                    f"{scan.svg_count} inline SVG(s)", rows)
        ok &= check(f"{name}: no external assets", not scan.external_assets,
                    str(scan.external_assets) if scan.external_assets else "none", rows)
        if zone_page:
            ok &= check(f"{name}: scale", "1.6 px/mm" in text,
                        "declared and ruler-labelled", rows)
            ok &= check(f"{name}: confidence legend",
                        "VERIFIED / DERIVED / DOCUMENTED" in text and "ASSUMPTION" in text,
                        "solid/dashed legend present", rows)
        for href in scan.hrefs:
            if href.startswith(("http:", "https:", "#", "mailto:")):
                continue
            target = (path.parent / href).resolve()
            ok &= check(f"{name}: link {href}", target.exists(),
                        str(target.relative_to(REPO)) if target.exists() else "MISSING", rows)

    for name in expected_studies:
        path = ARCH / "fit_studies" / name
        ok &= check(f"study exists: {name}", path.is_file(),
                    str(path.relative_to(REPO)), rows)
        if path.is_file() and name != "README.md":
            text = path.read_text(encoding="utf-8")
            headings = len(re.findall(r"^## [1-9]\.", text, re.M))
            ok &= check(f"{name}: Y-like sections", headings == 9,
                        f"{headings}/9 numbered sections", rows)
            ok &= check(f"{name}: confidence vocabulary",
                        all(word in text for word in
                            ("VERIFIED", "DERIVED", "DOCUMENTED", "ASSUMPTION")),
                        "all four tags present", rows)
            ok &= check(f"{name}: production gate",
                        "production" in text.lower() and
                        ("stop" in text.lower() or "gate" in text.lower()),
                        "explicit production stop/gate", rows)

    table_dir = ARCH / "evidence/p0/tables"
    for name in expected_tables:
        path = table_dir / name
        ok &= check(f"table exists: {name}", path.is_file(),
                    str(path.relative_to(REPO)), rows)

    # Coverage terms: each requested hardware family must occur in at least one
    # study.  These are intentionally coarse words, not a count of duplicate mentions.
    corpus = "\n".join(
        p.read_text(encoding="utf-8")
        for p in (ARCH / "fit_studies").glob("*.md")
    ).lower()
    required_terms = [
        "10bl120", "rocket 540", "140 mm belt", "75t", "28t", "6801",
        "51 mm", "52 mm", "68 mm", "2s", "ubec", "1000", "27 kω", "xt30", "xt60",
        "bx100", "esp32", "rp1", "bl-m8812eu2", "5.8 ghz", "ssc338q",
        "imx415", "blower", "mg90s", "max98357a", "4 ω 3 w", "ws2812b",
        "king pin", "f104", "a3144", "one pulse",
    ]
    missing = [term for term in required_terms if term not in corpus]
    ok &= check("requested component coverage", not missing,
                "all families found" if not missing else "missing: " + ", ".join(missing), rows)

    # Re-run live bbox validation as the final evidence integrity check.
    try:
        stls = D.measure_stls()
        live_ok = len(stls) == 18
        detail = f"{len(stls)} bboxes within 0.12 mm"
    except Exception as exc:  # pragma: no cover - diagnostic output
        live_ok = False
        detail = repr(exc)
    ok &= check("live STL bbox reproduction", live_ok, detail, rows)

    lines = [
        "# p0_09 — remaining-component output validation",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    lines.extend(f"| {a} | **{b}** | {c} |" for a, b, c in rows)
    lines += [
        "",
        f"**Verdict: {'PASS' if ok else 'FAIL'} — {sum(r[1]=='PASS' for r in rows)}/"
        f"{len(rows)} checks passed.**",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(lines[-2])
    print("WROTE", OUT)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
