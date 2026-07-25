#!/usr/bin/env python3
"""Audit and visualise the proposed lift-out electronics cassette.

Read-only geometry:
* registered 2024 front/rear body shell used by p0_03;
* verified floor, Suspension_Block_10, halo and drivetrain STL silhouettes;
* D-28 hardware installation envelopes and the corrected KO-01 envelope.

Outputs:
* evidence/p0/tables/p0_d34_cassette_fit_audit.md
* viz/cassette/{index,layout,exploded,pedestal,umbilical}.html
* one bounded link block in viz/index.html

This is a fit audit, not production CAD.  It writes no STL.  The electrical
content/map inputs are fixed, while TARGET envelopes, uncalipered connector
bodies, charge SKU and cassette structure remain explicit assumptions.
Run from the repository root after p0_08 and p0_10.
"""
from __future__ import annotations

import html
import math
from pathlib import Path
import re
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import p0_03_shell_clearance_sections as SHELL
import p0_07_zone_fit_rollup as ZONES
import p0_10_connection_visualizations as CONNECTIONS
import stlkit as K


REPO = Path(__file__).resolve().parents[3]
ARCH = REPO / "10_assembly_architecture"
OUT = ARCH / "viz/cassette"
MASTER = ARCH / "viz/index.html"
EVIDENCE = ARCH / "evidence/p0/tables/p0_d34_cassette_fit_audit.md"
INDEX_START = "<!-- BEGIN GENERATED CASSETTE LINKS · p0_12 -->"
INDEX_END = "<!-- END GENERATED CASSETTE LINKS · p0_12 -->"

# Candidate geometry is an ASSUMPTION gauge, not a production part.
S0_LOW = 0.0
S0_OPTIMISTIC = 11.0
STATIC_CLEARANCE = 5.0
MOVING_CLEARANCE = 8.0
# Re-tightened stepped-T gauge.  The rear stem stays between the floor-mounted
# battery/ESC; the forward bay carries the rotated PDB target.  These are audit
# coordinates, not a production shell.
CORE_X = (-31.0, 1.0)
CORE_L = (-18.5, 17.5)
WING_X = (1.0, 42.0)
WING_L = (-43.0, 43.0)
TONGUE_X = (42.0, 46.0)
TONGUE_L = (-29.5, 29.5)
LOWER_Z = (1.0, 19.0)
PDB_X = (1.0, 46.0)       # 55 L ×45 X board orientation
PDB_L = (-27.5, 27.5)
PDB_Z = (1.0, 19.0)
CHARGE_X = (-31.0, -1.0)
CHARGE_L = (-13.0, 12.0)
CHARGE_Z = (1.0, 11.0)
AMP_X = (-31.0, -13.2)    # 17.8 X ×19.4 L ×3 reference breakout
AMP_L = (-10.2, 9.2)
AMP_Z = (13.0, 16.0)
RP1_X = (-12.2, 0.8)
RP1_L = (-6.0, 5.0)
RP1_Z = (13.0, 16.0)
MINI_X = (3.0, 42.0)
MINI_Z = (1.0, 32.0)
MINI_L_NEG = (-43.0, -30.0)
MINI_L_POS = (30.0, 43.0)
KO_X = (-80.0, 100.0)
KO_L = (-22.0, 22.0)
KO_Z = (22.0, 38.0)
SERVO_X = (-76.76, -36.76)
SUSP_X = (70.60, 141.40)
PEDESTAL_X = (51.0, 65.0)
PEDESTAL_L = (-11.0, 11.0)
PEDESTAL_Z = (1.0, 42.0)
GIMBAL_X = (27.5, 82.5)  # old 55 mm audit reserve, now floor referenced
GIMBAL_Z = (1.0, 61.0)
BAT_X = (-80.0, -5.0)
BAT_L = (22.5, 67.5)
BAT_Z = (1.5, 26.5)
ESC_X = (-49.2, -5.0)
ESC_L = (-60.5, -23.5)
ESC_Z = (1.5, 25.7)
BOSS_POINTS = [(-15.0, -12.0), (-15.0, 12.0), (35.0, -12.0), (35.0, 12.0)]

# Connector family/count is FIRM.  Body allocations remain ASSUMPTION until
# the selected housings and terminated leads are calipered.  Dimensions are
# mating-axis depth × face pitch × height (mm).
SEAT_ALLOCATIONS = {
    "XT60": (20.0, 20.0, 12.0),
    "XT30": (16.0, 16.0, 10.0),
    "SERVO3": (16.0, 10.0, 8.0),
    "XH3": (12.0, 12.0, 9.0),
    "XH4": (15.0, 15.0, 9.0),
    "XH5": (18.0, 18.0, 9.0),
    "USB4": (16.0, 16.0, 10.0),
    "UFL": (12.0, 12.0, 6.0),
}
DOCK_X = (42.0, 58.0)     # straight-front-face body projection, not accepted
DOCK_L = (-32.0, 32.0)
CONDUIT_CLEAR = (10.0, 18.0)
CONDUIT_WALL = 2.0

FLOOR_PLAN = [
    (-141, -34), (-110, -56), (-30, -68.5), (30, -68.5), (55, -26.5),
    (180, -15), (180, 15), (55, 26.5), (30, 68.5), (-30, 68.5),
    (-110, 56), (-141, 34),
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


CSS = r"""
:root {
  color-scheme:light dark;
  --bg:#edf1f0; --paper:#fff; --ink:#15201f; --muted:#596866;
  --line:#bdc9c7; --grid:#dce3e2; --accent:#00857c; --soft:#e7f4f2;
  --good:#1f8f5f; --warn:#b05b22; --bad:#bf3f35; --assume:#687573;
  --shadow:0 1px 2px rgba(20,32,31,.08),0 9px 25px rgba(20,32,31,.06);
}
@media (prefers-color-scheme: dark) {
  :root { --bg:#0c1211; --paper:#121b1a; --ink:#e7eeed; --muted:#9aa9a6;
    --line:#2a3a38; --grid:#263230; --accent:#27c9b9; --soft:#163330;
    --good:#3bbd7f; --warn:#e08a4f; --bad:#e06758; --assume:#9ba8a6;
    --shadow:0 1px 2px rgba(0,0,0,.42),0 10px 30px rgba(0,0,0,.35); }
}
:root[data-theme="light"] { --bg:#edf1f0; --paper:#fff; --ink:#15201f; --muted:#596866;
  --line:#bdc9c7; --grid:#dce3e2; --accent:#00857c; --soft:#e7f4f2;
  --good:#1f8f5f; --warn:#b05b22; --bad:#bf3f35; --assume:#687573;
  --shadow:0 1px 2px rgba(20,32,31,.08),0 9px 25px rgba(20,32,31,.06); }
:root[data-theme="dark"] { --bg:#0c1211; --paper:#121b1a; --ink:#e7eeed; --muted:#9aa9a6;
  --line:#2a3a38; --grid:#263230; --accent:#27c9b9; --soft:#163330;
  --good:#3bbd7f; --warn:#e08a4f; --bad:#e06758; --assume:#9ba8a6;
  --shadow:0 1px 2px rgba(0,0,0,.42),0 10px 30px rgba(0,0,0,.35); }
* { box-sizing:border-box; }
html,body { margin:0; min-height:100%; }
body { overflow-x:hidden; background:var(--bg); color:var(--ink);
  font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }
a { color:var(--accent); text-underline-offset:.18em; }
code,.mono,.tag,th,svg text { font-family:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace; }
header { background:var(--paper); border-bottom:1px solid var(--line); }
.bar,.page { width:min(1420px,calc(100% - 32px)); margin:auto; }
.bar { min-height:62px; display:flex; justify-content:space-between; align-items:center; gap:16px; }
.brand { min-width:0; display:flex; gap:12px; align-items:baseline; }
.brand b,.eyebrow { color:var(--accent); letter-spacing:.13em; text-transform:uppercase; }
.brand span { color:var(--muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
button { border:1px solid var(--line); color:var(--ink); background:var(--paper);
  border-radius:7px; padding:7px 10px; cursor:pointer; }
main { padding:30px 0 58px; }
h1 { font-size:clamp(1.8rem,4vw,3rem); line-height:1.07; margin:.15em 0 .3em; text-wrap:balance; }
h2 { font:700 13px/1.4 ui-monospace,monospace; letter-spacing:.13em;
  text-transform:uppercase; color:var(--muted); margin:0 0 5px; }
h3 { margin:0 0 7px; font-size:1rem; }
p { max-width:100ch; }
.lede { font-size:clamp(15px,1.6vw,18px); color:var(--muted); margin-top:0; }
.board { background:var(--paper); border:1px solid var(--line); border-radius:13px;
  box-shadow:var(--shadow); padding:clamp(14px,2.4vw,26px); margin-top:24px; }
.sub { color:var(--muted); margin:2px 0 14px; font-size:13.5px; }
.drawing { width:100%; overflow-x:auto; overscroll-behavior-inline:contain;
  border:1px solid var(--line); border-radius:9px; background:var(--paper); }
.drawing svg { display:block; width:max(100%,var(--drawing-w,1100px)); height:auto; }
.cards,.summary,.legend,.assets { display:grid; gap:12px; }
.cards,.summary { grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); }
.legend { grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); margin-top:13px; }
.legend span { display:flex; align-items:center; gap:9px; color:var(--muted); font-size:12px; }
.assets { grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); }
.asset { border:1px solid var(--line); border-radius:9px; overflow:hidden; background:var(--paper); }
.asset img { width:100%; height:130px; object-fit:contain; background:#0b1312; display:block; }
.asset div { padding:9px 11px; font-size:11px; color:var(--muted); }
.card { display:block; color:var(--ink); text-decoration:none; border:1px solid var(--line);
  border-left:5px solid var(--accent); border-radius:10px; padding:14px; background:var(--paper); }
.card.fail { border-left-color:var(--bad); }
.card p { margin:5px 0 0; color:var(--muted); font-size:12.5px; }
.summary strong { display:block; color:var(--accent); font-size:1.3rem; }
.summary span { color:var(--muted); font-size:11.5px; }
.status { border:1px solid var(--bad); border-left-width:6px; border-radius:10px;
  padding:13px 15px; background:color-mix(in srgb,var(--bad) 9%,var(--paper)); }
.status b { color:var(--bad); }
.tag { display:inline-block; border:1px solid currentColor; border-radius:4px;
  padding:2px 6px; font-size:10px; font-weight:800; letter-spacing:.05em; color:var(--accent); }
.tag.documented { border-style:dotted; }
.tag.assumption { color:var(--assume); border-style:dashed; }
.tag.defer { color:var(--bad); border-style:dashed; }
.swatch { width:40px; height:16px; background:var(--soft); border:2px solid var(--accent); }
.swatch.derived { border-width:1px; }
.swatch.documented { border-style:dotted; }
.swatch.assumption { border-color:var(--assume); border-style:dashed;
  background:repeating-linear-gradient(135deg,transparent 0 5px,color-mix(in srgb,var(--assume) 20%,transparent) 5px 7px); }
.orderstrip { display:flex; gap:7px; overflow-x:auto; padding:10px 0 2px; }
.orderstrip span { flex:0 0 auto; border:1px solid var(--line); border-radius:6px;
  padding:7px 9px; font:700 10px/1.2 ui-monospace,monospace; }
.tablewrap { width:100%; overflow-x:auto; border:1px solid var(--line); border-radius:9px; }
table { border-collapse:collapse; width:100%; min-width:980px; background:var(--paper); }
th,td { padding:9px 10px; text-align:left; vertical-align:top; border-bottom:1px solid var(--grid); }
th { color:var(--muted); font-size:10px; letter-spacing:.06em; text-transform:uppercase; }
tr:last-child td { border-bottom:0; }
.note { border-left:3px solid var(--accent); background:var(--soft); padding:12px 15px;
  border-radius:0 9px 9px 0; margin:16px 0 0; color:var(--muted); font-size:13px; }
footer { border-top:1px solid var(--line); color:var(--muted); padding:22px 0 34px; font-size:12.5px; }
svg .gridline { stroke:var(--grid); stroke-width:.7; }
svg .axis { stroke:var(--ink); stroke-width:1.4; fill:none; }
svg .floor { stroke:var(--ink); stroke-width:1.5; fill:none; }
svg .shell { stroke:var(--accent); stroke-width:1.4; fill:none; }
svg .optimistic { stroke:var(--warn); stroke-width:1.1; stroke-dasharray:8 5; fill:none; }
svg .conf-verified { stroke:var(--accent); stroke-width:2.1; fill:color-mix(in srgb,var(--accent) 14%,transparent); }
svg .conf-derived { stroke:var(--accent); stroke-width:1.2; fill:color-mix(in srgb,var(--accent) 8%,transparent); }
svg .conf-documented { stroke:var(--accent); stroke-width:1.6; stroke-dasharray:2 4; fill:color-mix(in srgb,var(--accent) 8%,transparent); }
svg .conf-assumption { stroke:var(--assume); stroke-width:1.6; stroke-dasharray:7 5; fill:url(#hatch); }
svg .moving { stroke:var(--warn); stroke-width:1.7; stroke-dasharray:7 4; fill:url(#moveHatch); }
svg .failure,.defer { stroke:var(--bad); stroke-width:1.8; stroke-dasharray:7 5; fill:url(#failHatch); }
svg .leader { stroke:var(--muted); stroke-width:1; fill:none; marker-end:url(#arr); }
svg .route-a { stroke:#2086c9; stroke-width:5; fill:none; }
svg .route-b { stroke:#d68b25; stroke-width:5; fill:none; }
svg .trunk { stroke:var(--ink); stroke-width:8; fill:none; }
svg .anchor { fill:var(--paper); stroke:var(--ink); stroke-width:2; }
svg .label { fill:var(--ink); font-size:11px; }
svg .small { fill:var(--muted); font-size:9px; }
svg .tiny { fill:var(--muted); font-size:7.5px; }
svg .accent { fill:var(--accent); }
svg .badtext { fill:var(--bad); font-weight:800; }
@media(max-width:640px) { .bar,.page { width:min(100% - 20px,1420px); } main { padding-top:20px; } }
"""

JS = r"""
(() => {
  const root=document.documentElement, btn=document.querySelector("[data-theme-toggle]");
  if(!btn) return;
  btn.addEventListener("click",()=>{
    const current=root.dataset.theme;
    root.dataset.theme=current==="dark"?"light":current==="light"?"dark":
      matchMedia("(prefers-color-scheme: dark)").matches?"light":"dark";
    btn.textContent=root.dataset.theme==="dark"?"Light":"Dark";
  });
})();
"""


def defs() -> str:
    return """<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" class="gridline" fill="none"/></pattern>
<pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="9" stroke="var(--assume)" opacity=".4"/></pattern>
<pattern id="moveHatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="10" stroke="var(--warn)" stroke-width="2" opacity=".45"/></pattern>
<pattern id="failHatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect width="8" height="8" fill="color-mix(in srgb,var(--bad) 10%,transparent)"/><line x1="0" y1="0" x2="0" y2="8" stroke="var(--bad)" stroke-width="2" opacity=".6"/></pattern>
<marker id="arr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8Z" fill="context-stroke"/></marker>
</defs>"""


def page_start(title: str, subtitle: str) -> str:
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; font-src data:">
<title>{esc(title)} · W17 cassette audit</title><style>{CSS}</style></head><body>
<header><div class="bar"><div class="brand"><b>W17 / RC-01</b><span>{esc(subtitle)}</span></div>
<div><a href="index.html">Cassette index</a> · <a href="../index.html">All viz</a> · <button data-theme-toggle type="button">Theme</button></div>
</div></header><main><div class="page">"""


def page_end() -> str:
    return f"""</div></main><footer><div class="page">Generated by
<code>evidence/scripts/p0_12_cassette_fit_visualizations.py</code>. Real STLs are read-only;
ASSUMPTION is dashed/hatched. This audit emits no production STL.</div></footer>
<script>{JS}</script></body></html>"""


def legend() -> str:
    return """<div class="legend">
<span><i class="swatch"></i>VERIFIED · real STL/interface evidence</span>
<span><i class="swatch derived"></i>DERIVED · registered section/arithmetic</span>
<span><i class="swatch documented"></i>DOCUMENTED · owner/supplier value</span>
<span><i class="swatch assumption"></i>ASSUMPTION · dashed/hatched · ASM gate open</span>
</div>"""


def asset_cards() -> str:
    assets = [
        ("front_floor", "Front floor", "VERIFIED STL"),
        ("rear_floor", "Rear floor", "VERIFIED STL"),
        ("susp_block", "Suspension_Block_10", "VERIFIED STL"),
        ("motor_lock", "Belt motor lock", "VERIFIED STL"),
        ("body_front", "2024 front shell", "VERIFIED STL"),
        ("body_rear", "2024 rear shell", "VERIFIED STL"),
        ("halo", "new halo 2.1", "VERIFIED raw silhouette / transform open"),
    ]
    rows = []
    for key, title, note in assets:
        uri, width, height = CONNECTIONS.mesh_silhouette(key)
        rows.append(
            f'<div class="asset"><img src="{uri}" alt="{esc(title)} real STL silhouette">'
            f'<div><b>{esc(title)}</b><br>{esc(note)} · projected {width:.1f}×{height:.1f} mm</div></div>'
        )
    return '<div class="assets">' + "".join(rows) + "</div>"


def rect_svg(x0: float, x1: float, y0: float, y1: float, mapper, cls: str, label: str) -> str:
    ax, ay = mapper(x0, y1)
    bx, by = mapper(x1, y0)
    return (
        f'<rect class="{cls}" x="{min(ax,bx):.1f}" y="{min(ay,by):.1f}" '
        f'width="{abs(bx-ax):.1f}" height="{abs(by-ay):.1f}" rx="4"/>'
        f'<text class="tiny" x="{min(ax,bx)+4:.1f}" y="{min(ay,by)+12:.1f}">{esc(label)}</text>'
    )


def layout_plan_svg() -> str:
    scale, ox, oy = 2.4, 390.0, 245.0

    def mp(x: float, lateral: float) -> tuple[float, float]:
        return ox + scale * x, oy - scale * lateral

    floor = " ".join(f"{mp(x,l)[0]:.1f},{mp(x,l)[1]:.1f}" for x, l in FLOOR_PLAN)
    out = [
        '<svg style="--drawing-w:1260px" viewBox="0 0 1260 520" role="img" aria-label="Cassette everything-inside reference attempt plan at 2.4 px/mm">',
        defs(), '<rect width="1260" height="520" fill="url(#grid)"/>',
        f'<polygon class="floor" points="{floor}"/>',
        rect_svg(*KO_X, *KO_L, mp, "moving", "KO-01 · Z22…38"),
        rect_svg(*SERVO_X, -20, 20, mp, "conf-documented", "steering servo"),
        rect_svg(*SUSP_X, -18.5, 18.5, mp, "conf-derived", "Suspension_Block_10"),
        rect_svg(*CORE_X, *CORE_L, mp, "conf-assumption", "rear stem"),
        rect_svg(*WING_X, *WING_L, mp, "conf-assumption", "forward wall wing"),
        rect_svg(*TONGUE_X, *TONGUE_L, mp, "conf-assumption", "tapered PDB tongue"),
        rect_svg(*PDB_X, *PDB_L, mp, "failure", "PDB TARGET 45 X ×55 L ×18 Z"),
        rect_svg(*CHARGE_X, *CHARGE_L, mp, "defer", "charge TARGET 30×25×10"),
        rect_svg(*AMP_X, *AMP_L, mp, "conf-assumption", "amp deck 17.8×19.4"),
        rect_svg(*RP1_X, *RP1_L, mp, "conf-documented", "RP1 13×11"),
        rect_svg(*MINI_X, *MINI_L_NEG, mp, "conf-documented", "ESP #1 39×13 plan"),
        rect_svg(*MINI_X, *MINI_L_POS, mp, "conf-documented", "ESP #2 39×13 plan"),
        rect_svg(*PEDESTAL_X, *PEDESTAL_L, mp, "conf-assumption", "fixed hollow pedestal foot"),
        rect_svg(*DOCK_X, *DOCK_L, mp, "failure", "straight dock body projection · REJECT"),
        rect_svg(*BAT_X, *BAT_L, mp, "defer", "2S pack ≤75×45 · DEFER"),
        rect_svg(*ESC_X, *ESC_L, mp, "conf-documented", "ESC 44.2×37"),
        rect_svg(-132, -78, -18, 18, mp, "conf-documented", "motor Ø36×54"),
        rect_svg(-125, -82, -61, -24, mp, "moving", "belt/pulley sweep"),
    ]
    for x, l in BOSS_POINTS:
        px, py = mp(x, l)
        out.append(f'<circle class="failure" cx="{px:.1f}" cy="{py:.1f}" r="7"/>')
    # Wheel envelopes (schematic documented tyres at derived X stations).
    for x, l, label in ((146.1, 75, "F"), (146.1, -75, "F"), (-90.9, 72.5, "R"), (-90.9, -72.5, "R")):
        px, py = mp(x, l)
        out += [f'<circle class="moving" cx="{px:.1f}" cy="{py:.1f}" r="{32*scale:.1f}"/>',
                f'<text class="small" x="{px-5:.1f}" y="{py+4:.1f}">{label}</text>']
    x0, y0 = mp(-140, -92)
    out += [
        f'<line class="axis" x1="{mp(-145,0)[0]:.1f}" y1="{mp(-145,0)[1]:.1f}" x2="{mp(185,0)[0]:.1f}" y2="{mp(185,0)[1]:.1f}"/>',
        f'<line class="axis" x1="{mp(0,-90)[0]:.1f}" y1="{mp(0,-90)[1]:.1f}" x2="{mp(0,90)[0]:.1f}" y2="{mp(0,90)[1]:.1f}"/>',
        '<text class="accent label" x="28" y="28">RE-TIGHTENED TARGET-ENVELOPE GAUGE · LOWER PACK REPACKS / FULL CLOSURE OPEN</text>',
        '<text class="small" x="28" y="48">PDB includes both UBECs + capacitor. Red straight dock overlaps the fixed pedestal; a stepped/wrapped full-size dock dummy is required.</text>',
        f'<line class="axis" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0+120:.1f}" y2="{y0:.1f}"/>',
        f'<text class="small" x="{x0:.1f}" y="{y0-9:.1f}">50 mm ruler · 2.4 px/mm</text>',
        "</svg>",
    ]
    return "".join(out)


def segment_lines(segments, mapper, cls: str, dz: float = 0.0) -> str:
    rows = []
    for (a, b) in segments:
        x1, y1 = mapper(a[0], a[1] + dz)
        x2, y2 = mapper(b[0], b[1] + dz)
        rows.append(f'<line class="{cls}" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/>')
    return "".join(rows)


def layout_side_svg(shell_tris) -> str:
    scale, ox, oy = 2.6, 410.0, 300.0

    def mp(x: float, z: float) -> tuple[float, float]:
        return ox + scale * x, oy - scale * z

    segs = K.section(shell_tris, "y", 0.0)
    out = [
        '<svg style="--drawing-w:1260px" viewBox="0 0 1260 380" role="img" aria-label="Longitudinal cassette side fit under registered shell at 2.6 px/mm">',
        defs(), '<rect width="1260" height="380" fill="url(#grid)"/>',
        segment_lines(segs, mp, "shell"),
        segment_lines(segs, mp, "optimistic", S0_OPTIMISTIC),
        f'<line class="floor" x1="{mp(-145,0)[0]:.1f}" y1="{mp(-145,0)[1]:.1f}" x2="{mp(180,0)[0]:.1f}" y2="{mp(180,0)[1]:.1f}"/>',
        rect_svg(*CORE_X, *LOWER_Z, mp, "conf-assumption", "rear stem / target cells"),
        rect_svg(*PDB_X, *PDB_Z, mp, "failure", "PDB TARGET 18 high"),
        rect_svg(*CHARGE_X, *CHARGE_Z, mp, "defer", "charge TARGET 10 high"),
        rect_svg(*AMP_X, *AMP_Z, mp, "conf-assumption", "amp/RP1 service deck"),
        rect_svg(*MINI_X, *MINI_Z, mp, "conf-documented", "two wall mini profiles"),
        rect_svg(*KO_X, *KO_Z, mp, "moving", "KO-01"),
        rect_svg(*SERVO_X, 0, 20, mp, "conf-documented", "servo body"),
        rect_svg(*SUSP_X, -14, 23, mp, "conf-derived", "front block"),
        rect_svg(*PEDESTAL_X, *PEDESTAL_Z, mp, "conf-assumption", "fixed hollow pedestal"),
        rect_svg(*GIMBAL_X, *GIMBAL_Z, mp, "defer", "floor-ref gimbal reserve"),
        rect_svg(*BAT_X, *BAT_Z, mp, "defer", "battery"),
        rect_svg(*ESC_X, *ESC_Z, mp, "conf-documented", "ESC"),
        rect_svg(-132, -78, 9, 45, mp, "conf-documented", "motor"),
        '<text class="accent label" x="25" y="26">SIDE · REGISTERED L=0 SHELL · S0=0 SOLID / S0+11 DASHED</text>',
        '<text class="small" x="25" y="46">PDB top Z19 is shell-safe but only 3 mm below KO-01 Z22: 5 mm short of the 8 mm moving policy until ASM-08.</text>',
        f'<line class="axis" x1="{mp(-140,-10)[0]:.1f}" y1="{mp(-140,-10)[1]:.1f}" x2="{mp(-90,-10)[0]:.1f}" y2="{mp(-90,-10)[1]:.1f}"/>',
        f'<text class="small" x="{mp(-140,-10)[0]:.1f}" y="{mp(-140,-10)[1]-8:.1f}">50 mm ruler · 2.6 px/mm</text>',
        "</svg>",
    ]
    return "".join(out)


def layout_section_svg(shell_tris) -> str:
    scale, ox, oy = 4.0, 360.0, 360.0

    def mp(lateral: float, z: float) -> tuple[float, float]:
        return ox + scale * lateral, oy - scale * z

    segs = K.section(shell_tris, "x", 20.0)
    out = [
        '<svg style="--drawing-w:920px" viewBox="0 0 920 410" role="img" aria-label="Transverse X plus 20 cassette section at 4 px/mm">',
        defs(), '<rect width="920" height="410" fill="url(#grid)"/>',
        segment_lines(segs, mp, "shell"),
        segment_lines(segs, mp, "optimistic", S0_OPTIMISTIC),
        f'<line class="floor" x1="{mp(-70,0)[0]:.1f}" y1="{mp(-70,0)[1]:.1f}" x2="{mp(70,0)[0]:.1f}" y2="{mp(70,0)[1]:.1f}"/>',
        rect_svg(*WING_L, *LOWER_Z, mp, "conf-assumption", "forward wing / target bay"),
        rect_svg(*PDB_L, *PDB_Z, mp, "failure", "PDB TARGET"),
        rect_svg(*MINI_L_NEG, *MINI_Z, mp, "conf-documented", "ESP #1"),
        rect_svg(*MINI_L_POS, *MINI_Z, mp, "conf-documented", "ESP #2"),
        rect_svg(*KO_L, *KO_Z, mp, "moving", "KO-01"),
        rect_svg(*BAT_L, *BAT_Z, mp, "failure", "battery"),
        rect_svg(*ESC_L, *ESC_Z, mp, "failure", "ESC"),
        '<text class="accent label" x="24" y="25">SECTION X=+20 · REAL REGISTERED SHELL</text>',
        '<text class="small" x="24" y="44">Wall seats retain 8 mm lateral separation; central PDB top Z19 has only 3 mm vertical separation to KO-01.</text>',
        f'<line class="axis" x1="{mp(-65,-7)[0]:.1f}" y1="{mp(-65,-7)[1]:.1f}" x2="{mp(-15,-7)[0]:.1f}" y2="{mp(-15,-7)[1]:.1f}"/>',
        f'<text class="small" x="{mp(-65,-7)[0]:.1f}" y="{mp(-65,-7)[1]-8:.1f}">50 mm ruler · 4.0 px/mm</text>',
        "</svg>",
    ]
    return "".join(out)


def layout_page(shell_tris) -> str:
    page = page_start("Everything-inside re-audit", "plan + side + real shell section")
    page += """<p class="eyebrow">cassette audit / sheet A</p><h1>Everything-inside revised reference gauge</h1>
<div class="status"><b>LOWER TARGET PACK REPACKS; EVERYTHING-INSIDE DOES NOT YET CLOSE.</b> The 55×45×18 PDB target (including 2× UBEC + capacitor), 30×25×10 charge target, amp and RP1 fit a re-tightened stepped-T gauge. The PDB top is only 3 mm below provisional KO-01, the Wi-Fi body is still uncalipered/unplaced, and the straight three-bank dock projection collides with the fixed pedestal. A full-scale dummy remains allowed; production does not.</div>
<div class="board"><h2>Plan</h2><p class="sub">Real P0 floor outline, derived fixed occupancies and documented/assumed hardware at one common scale.</p><div class="drawing">"""
    page += layout_plan_svg()
    page += """</div></div><div class="board"><h2>Longitudinal side</h2><p class="sub">Registered shell section at L=0. Solid is the S0=0 lower bound; the dashed copy shows the optimistic, still-unverified +11 mm seat bound.</p><div class="drawing">"""
    page += layout_side_svg(shell_tris)
    page += """</div></div><div class="board"><h2>Transverse section X=+20</h2><p class="sub">Real shell mesh section. The section exposes the controlling stack/rod/shoulder conflict.</p><div class="drawing">"""
    page += layout_section_svg(shell_tris)
    roof, sx, sl = mini_shoulder_min(shell_tris)
    pdb_roof, px, pl = cell_shoulder_min(shell_tris, PDB_X, PDB_L)
    page += f"""</div></div><div class="board"><h2>Numerical closure checks</h2><div class="tablewrap"><table><thead><tr><th>Check</th><th>Required</th><th>Available / result</th><th>State</th></tr></thead><tbody>
<tr><td>Mini-board row</td><td>39 mm X</td><td>{clean_longitudinal_gap():.1f} mm clean interval; {clean_longitudinal_gap()-39:.1f} mm residual before plug/wall allowances</td><td><b>PASS GAUGE</b></td></tr>
<tr><td>Mini seats vs KO-01</td><td>8 mm moving policy</td><td>inner faces |L|=30 vs provisional boundary |L|=22</td><td><b>PASS GAUGE / ASM-08</b></td></tr>
<tr><td>Mini seats vs shell</td><td>Z32 + 5 mm</td><td>worst roof {roof:.2f} at X{sx:+.0f}/L{sl:+.0f}; S0≥{37-roof:.2f} mm</td><td><b>CONDITIONAL</b></td></tr>
<tr><td>PDB TARGET vs shell</td><td>Z19 + 5 mm</td><td>worst finite roof {pdb_roof:.2f} at X{px:+.0f}/L{pl:+.1f}; {pdb_roof-24:.2f} mm surplus at S0=0</td><td><b>PASS TARGET GAUGE</b></td></tr>
<tr><td>PDB TARGET vs KO-01</td><td>8 mm moving policy</td><td>KO starts Z22; PDB top Z19 leaves 3 mm</td><td><b>HOLD · 5 mm DEFICIT / ASM-08</b></td></tr>
<tr><td>Lower named stuffing</td><td>PDB 55×45×18 + charge 30×25×10 + amp + RP1</td><td>rotated PDB X+1…+46; rear charge X−31…−1; amp/RP1 deck Z13…16</td><td><b>PACKS AS ASSUMPTION</b></td></tr>
<tr><td>Gimbal stack</td><td>not carried above cassette</td><td>old Z38+60=Z98 retired; floor-referenced pedestal remains fixed</td><td><b>PASS ARCHITECTURE / SWEEP DEFER</b></td></tr>
<tr><td>Battery + ESC</td><td>5 mm static, 8 mm moving</td><td>no cassette plan overlap; shell, real leads/air and measured KO-01 remain open</td><td><b>CONDITIONAL / DEFER PACK</b></td></tr>
<tr><td>Wi-Fi + connector dock</td><td>complete body/bends + service pull</td><td>Wi-Fi ≤60×32×12 allocation remains uncalipered; straight 16×64 dock projection overlaps pedestal X51…58/L±11</td><td><b>HOLD · FULL LAYOUT OPEN</b></td></tr>
</tbody></table></div></div>
<div class="board"><h2>Real mesh silhouettes used</h2><p class="sub">These are directly loaded STL silhouettes. Hardware without a mesh remains a technical outline.</p>{asset_cards()}</div>
<div class="board"><h2>Confidence</h2>{legend()}</div>"""
    return page + page_end()


def exploded_svg() -> str:
    floor_uri, floor_w, floor_h = CONNECTIONS.mesh_silhouette("front_floor")
    halo_uri, halo_w, halo_h = CONNECTIONS.mesh_silhouette("halo")
    scale = 2.0
    rows = [
        (1, 690, "DAT-F floor", "VERIFIED STL", "verified"),
        (2, 600, "former 4-boss saddle pattern", "X−15/+35, L±12 · REJECT: target-cell overlap", "defer"),
        (3, 505, "stepped-T cassette + tapered tongue", "ASSUMPTION fit gauge", "assumption"),
        (4, 410, "PDB TARGET + rear charge cell", "55×45×18 incl. UBEC×2/cap; charge 30×25×10", "defer"),
        (5, 320, "insulated service deck: amp + RP1", "Wi-Fi still unplaced / D-06b", "defer"),
        (6, 225, "2× MH-ET Live wall seats", "39×31×~13 · micro-USB to edge", "assumption"),
        (7, 125, "fixed cockpit pedestal / gimbal", "separate floor joint · MG90S DEFER", "defer"),
    ]
    out = [
        '<svg style="--drawing-w:1200px" viewBox="0 0 1200 790" role="img" aria-label="Exploded cassette assembly at 2.0 px/mm">',
        defs(), '<rect width="1200" height="790" fill="url(#grid)"/>',
        '<text class="accent label" x="25" y="25">EXPLODED CASSETTE · INDIVIDUAL SILHOUETTES 2.0 px/mm · EXPLOSION GAPS SCHEMATIC</text>',
    ]
    # Real floor silhouette.
    iw, ih = floor_w * scale, floor_h * scale
    out += [
        f'<image href="{floor_uri}" x="{600-iw/2:.1f}" y="{690-ih/2:.1f}" width="{iw:.1f}" height="{ih:.1f}"/>',
        f'<rect class="conf-verified" x="{600-iw/2:.1f}" y="{690-ih/2:.1f}" width="{iw:.1f}" height="{ih:.1f}"/>',
    ]
    # Fixed frame, box, lower cells, deck and upper cells.
    out += [
        '<rect class="conf-assumption" x="550" y="580" width="100" height="44" rx="5"/>',
        '<circle class="conf-assumption" cx="535" cy="602" r="7"/><circle class="conf-assumption" cx="570" cy="602" r="7"/><circle class="conf-assumption" cx="630" cy="602" r="7"/><circle class="conf-assumption" cx="665" cy="602" r="7"/>',
        '<path class="conf-assumption" d="M538 475H662V486H686V532H514V486H538Z"/>',
        '<rect class="failure" x="520" y="374" width="110" height="90"/><text class="tiny" x="526" y="395">PDB TARGET 55×45×18</text><text class="tiny" x="526" y="410">includes UBEC×2 + cap</text>',
        '<rect class="defer" x="650" y="394" width="60" height="50"/><text class="tiny" x="655" y="414">CHARGE TARGET</text><text class="tiny" x="655" y="428">30×25×10</text>',
        '<rect class="conf-assumption" x="520" y="305" width="39" height="36"/><text class="tiny" x="524" y="325">AMP</text>',
        '<rect class="conf-documented" x="570" y="312" width="26" height="22"/><text class="tiny" x="573" y="327">RP1</text>',
        '<rect class="failure" x="720" y="295" width="120" height="64"/><text class="tiny" x="726" y="318">WI-FI ≤60×32×12</text><text class="tiny" x="726" y="334">UNCALIPERED / UNPLACED</text>',
        '<rect class="conf-assumption" x="540" y="305" width="120" height="8"/>',
        '<rect class="conf-documented" x="500" y="194" width="78" height="62"/><rect class="conf-documented" x="622" y="194" width="78" height="62"/>',
        '<text class="tiny" x="505" y="220">MINI #1 · WALL</text><text class="tiny" x="627" y="220">MINI #2 · WALL</text>',
        '<rect class="failure" x="720" y="194" width="128" height="48"/><text class="tiny" x="726" y="213">DOCK BANKS ~60 FACE SPAN</text><text class="tiny" x="726" y="228">STRAIGHT FACE NOT CLOSED</text>',
        '<rect class="defer" x="570" y="87" width="60" height="55" rx="5"/><circle class="defer" cx="600" cy="75" r="24"/>',
    ]
    # Halo is a real but unregistered raw silhouette beside the gimbal.
    hw, hh = halo_w * 1.2, halo_h * 1.2
    out += [
        f'<image href="{halo_uri}" x="{830:.1f}" y="{85:.1f}" width="{hw:.1f}" height="{hh:.1f}"/>',
        f'<rect class="conf-verified" x="830" y="85" width="{hw:.1f}" height="{hh:.1f}"/>',
        '<text class="tiny" x="830" y="78">REAL HALO STL · ASSEMBLY TRANSFORM OPEN</text>',
    ]
    for number, y, title, note, state in rows:
        out += [
            f'<circle class="{"failure" if state=="defer" else "conf-assumption" if state=="assumption" else "conf-verified"}" cx="92" cy="{y}" r="18"/>',
            f'<text class="label" text-anchor="middle" x="92" y="{y+4}">{number}</text>',
            f'<path class="leader" d="M112 {y}H470"/>',
            f'<rect x="125" y="{y-28}" width="330" height="55" rx="6" fill="var(--paper)" stroke="var(--line)"/>',
            f'<text class="label" x="138" y="{y-7}">{esc(title)}</text>',
            f'<text class="small" x="138" y="{y+13}">{esc(note)}</text>',
        ]
    for y1, y2 in ((660, 625), (570, 535), (465, 425), (380, 315), (285, 240), (180, 140)):
        out.append(f'<path class="leader" d="M600 {y1}V{y2}"/>')
    out += [
        '<line class="axis" x1="950" y1="730" x2="1050" y2="730"/>',
        '<text class="small" x="950" y="720">50 mm ruler · 2.0 px/mm</text>',
        "</svg>",
    ]
    return "".join(out)


def exploded_page() -> str:
    page = page_start("Exploded cassette", "floor → cassette → lower pack → wall minis")
    page += """<p class="eyebrow">cassette audit / sheet B</p><h1>Exploded cassette and assembly order</h1>
<div class="status"><b>FIT-GATED ASSEMBLY ONLY.</b> The PDB contents and connector map are fixed inputs, but the 55×45×18 PDB and 30×25×10 charge values are TARGET envelopes—not calipered production pockets. Wi-Fi, dock topology, cassette walls, bosses and every MG90S interface remain open.</div>
<div class="board"><h2>Assembly-order strip</h2><div class="orderstrip">
<span>1 · verify DAT-F</span><span>2 · fit fixed saddle</span><span>3 · fixed pedestal template</span><span>4 · four-point cassette</span><span>5 · lower/RF pack</span><span>6 · wall minis</span><span>7 · dock</span><span>8 · lift around pedestal</span>
</div></div><div class="board"><h2>Exploded sheet with callout balloons</h2><p class="sub">Each part silhouette uses 2.0 px/mm. Vertical explosion gaps communicate order only.</p><div class="drawing">"""
    page += exploded_svg()
    page += """</div></div><div class="board"><h2>Four-point lift-out rule</h2>
<p>The former four M3×5-insert centres at X−15/+35, L±12 are now rejected: both rear points fall inside the charge target and both front points inside the PDB target. A hidden screw under either module is not a lift-out service joint. CAS-07 must find a reversible external saddle/clamp pattern from a transparent full-stack dummy; no donor-floor hole is authorized.</p>
<p>The lower repack is PDB X+1…+46/L±27.5/Z1…19; charge X−31…−1/L−13…+12/Z1…11; an insulated Z13…16 deck carries the amp and RP1. That proves neighbour order only. D-06b must place the real Wi-Fi/heatsink, and a connector-board dummy must replace the rejected straight dock projection.</p>
<p>Removal order: battery disconnect → one ganged cassette dock → release the new external four-point saddle/clamp → vertical lift around the fixed pedestal. The fixed carrier and pedestal stay with the floor. The cassette must not touch the steering linkage, pedestal, shell lip, battery or ESC.</p></div>
<div class="board"><h2>Confidence</h2>""" + legend() + "</div>"
    return page + page_end()


def pedestal_svg(shell_tris) -> str:
    scale, ox, oy = 3.0, 420.0, 310.0

    def mp(x: float, z: float) -> tuple[float, float]:
        return ox + scale * x, oy - scale * z

    segs = K.section(shell_tris, "y", 0.0)
    out = [
        '<svg style="--drawing-w:1260px" viewBox="0 0 1260 410" role="img" aria-label="Cockpit pedestal and cut-through wiring path at 3 px/mm">',
        defs(), '<rect width="1260" height="410" fill="url(#grid)"/>',
        segment_lines(segs, mp, "shell"),
        segment_lines(segs, mp, "optimistic", S0_OPTIMISTIC),
        f'<line class="floor" x1="{mp(-30,0)[0]:.1f}" y1="{mp(-30,0)[1]:.1f}" x2="{mp(105,0)[0]:.1f}" y2="{mp(105,0)[1]:.1f}"/>',
        rect_svg(*WING_X, *LOWER_Z, mp, "conf-assumption", "cassette wing lifts"),
        rect_svg(*PEDESTAL_X, *PEDESTAL_Z, mp, "conf-assumption", "hollow fixed pedestal"),
        rect_svg(*GIMBAL_X, *GIMBAL_Z, mp, "defer", "55×60 prior sweep reserve · floor ref"),
        rect_svg(*SUSP_X, -14, 23, mp, "conf-derived", "Suspension_Block_10"),
        rect_svg(*KO_X, *KO_Z, mp, "moving", "KO-01"),
    ]
    cx = (PEDESTAL_X[0] + PEDESTAL_X[1]) / 2
    a, b, c = mp(cx, 56), mp(cx, 12), mp(38, 12)
    out += [
        f'<path class="route-a" stroke-dasharray="8 5" d="M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}L{c[0]:.1f} {c[1]:.1f}"/>',
        '<text class="accent label" x="25" y="25">FIXED HOLLOW COCKPIT PEDESTAL · FLOOR/FRONT STRUCTURE, NEVER CASSETTE</text>',
        '<text class="small" x="25" y="44">Dashed blue: shielded 4-pin USB + two 3-pin servo leads; target clear section 10×18, sequential plug pull-through.</text>',
        '<text class="small" x="25" y="63">2 mm trial wall gives 14×22 outer core. Keep ≥25 mm lower service loop and ≥20 mm provisional USB bend radius; all remain ASM assumptions.</text>',
        f'<line class="axis" x1="{mp(-20,-8)[0]:.1f}" y1="{mp(-20,-8)[1]:.1f}" x2="{mp(30,-8)[0]:.1f}" y2="{mp(30,-8)[1]:.1f}"/>',
        f'<text class="small" x="{mp(-20,-8)[0]:.1f}" y="{mp(-20,-8)[1]-8:.1f}">50 mm ruler · 3.0 px/mm</text>',
        "</svg>",
    ]
    return "".join(out)


def pedestal_page(shell_tris) -> str:
    page = page_start("Cockpit pedestal", "fixed support + hollow camera/servo conduit")
    page += """<p class="eyebrow">cassette audit / sheet C</p><h1>Decoupled cockpit pedestal</h1>
<div class="status"><b>OLD ADDITIVE ROOF FAILURE REMOVED; CONDUIT TARGET NOW DIMENSIONED.</b> The old cassette Z38 + 60 mm gimbal = Z98 stack is retired. A 10×18 mm clear rounded-rectangle trial path (2 mm wall, 14×22 outer) is reserved for one shielded 4-pin USB lead plus two 3-pin servo leads, with sequential connector pull-through and lower service slack. Real terminated bodies still own the gate.</div>
<div class="board"><h2>Side section and cut-through path</h2><p class="sub">Registered L=0 shell, S0=0 solid and optimistic S0+11 dashed. The previous 55×45×60 reserve is shown floor-referenced only to expose what the body/halo dummy must replace.</p><div class="drawing">"""
    page += pedestal_svg(shell_tris)
    page += """</div></div><div class="board"><h2>Interface rules</h2><div class="tablewrap"><table><thead><tr><th>Interface</th><th>Rule</th><th>Closure</th></tr></thead><tbody>
<tr><td>pedestal ↔ floor/front structure</td><td>Mapped existing/shared feature or reversible clamp only; never cassette-supported; no donor drilling</td><td>CAS-08 template/pull-off/body-on gate</td></tr>
<tr><td>gimbal ↔ pedestal</td><td>Real camera and two arrived MG90S units; hand sweep before any powered endpoint check</td><td>DEFER / ASM-53</td></tr>
<tr><td>hollow conduit</td><td>10×18 clear target, 2 mm trial wall; pass each full USB/servo connector sequentially; ≥25 mm lower service loop; exit to R1/R2 below Z22 and anchor jackets</td><td>ASSUMPTION / CAS-09; resize if any plug exceeds the gauge</td></tr>
<tr><td>cassette service</td><td>Pedestal and its loom remain fixed while the cassette releases from a new external four-point saddle/clamp</td><td>CAS-07 + timed body-off lift test</td></tr>
</tbody></table></div></div><div class="board"><h2>Confidence</h2>""" + legend() + "</div>"
    return page + page_end()


def umbilical_svg() -> str:
    scale, ox, oy = 2.5, 400.0, 280.0

    def mp(x: float, lateral: float) -> tuple[float, float]:
        return ox + scale * x, oy - scale * lateral

    floor = " ".join(f"{mp(x,l)[0]:.1f},{mp(x,l)[1]:.1f}" for x, l in FLOOR_PLAN)
    dock = mp(42, 0)
    pedestal = mp(54, 0)
    ped_exit = mp(47, -30)
    servo = mp(-55, 0)
    esc_point = mp(25, -42)
    tail = mp(-125, 45)
    out = [
        '<svg style="--drawing-w:1260px" viewBox="0 0 1260 575" role="img" aria-label="Cassette umbilical and connector-seat route at 2.5 px/mm">',
        defs(), '<rect width="1260" height="575" fill="url(#grid)"/>',
        f'<polygon class="floor" points="{floor}"/>',
        rect_svg(*KO_X, *KO_L, mp, "moving", "OPEN SPINE · KO-01"),
        rect_svg(*CORE_X, *CORE_L, mp, "conf-assumption", "rear stem"),
        rect_svg(*WING_X, *WING_L, mp, "conf-assumption", "forward wing"),
        rect_svg(*PEDESTAL_X, *PEDESTAL_L, mp, "conf-assumption", "fixed pedestal"),
        rect_svg(*DOCK_X, *DOCK_L, mp, "failure", "straight dock projection"),
        f'<text class="tiny" x="{dock[0]+7:.1f}" y="{dock[1]-55:.1f}">U-PWR · XT60×1 + XT30×2 MIN</text>',
        f'<text class="tiny" x="{dock[0]+7:.1f}" y="{dock[1]-35:.1f}">U-SRV · 3-PIN×5</text>',
        f'<text class="tiny" x="{dock[0]+7:.1f}" y="{dock[1]-15:.1f}">U-SIG · XH3×3 + USB4×1</text>',
        f'<text class="tiny badtext" x="{dock[0]+7:.1f}" y="{dock[1]+12:.1f}">OVERLAPS PEDESTAL · WRAP/NOTCH DUMMY</text>',
    ]
    # One ganged umbilical exits, then turns to the existing edge highways.
    p1, p2, p3 = mp(25, -42), mp(-55, -52), mp(-90, -52)
    out += [
        f'<path class="trunk" d="M{dock[0]:.1f} {dock[1]:.1f}L{p1[0]:.1f} {p1[1]:.1f}L{p2[0]:.1f} {p2[1]:.1f}"/>',
        f'<path class="route-a" stroke-dasharray="7 5" d="M{pedestal[0]:.1f} {pedestal[1]:.1f}L{ped_exit[0]:.1f} {ped_exit[1]:.1f}L{p1[0]:.1f} {p1[1]:.1f}"/>',
        f'<path class="route-b" d="M{p2[0]:.1f} {p2[1]:.1f}L{esc_point[0]:.1f} {esc_point[1]:.1f}"/>',
        f'<path class="route-a" d="M{p2[0]:.1f} {p2[1]:.1f}L{servo[0]:.1f} {servo[1]:.1f}"/>',
        f'<path class="route-a" d="M{p2[0]:.1f} {p2[1]:.1f}L{p3[0]:.1f} {p3[1]:.1f}L{tail[0]:.1f} {tail[1]:.1f}"/>',
    ]
    for x, y, name in ((dock[0], dock[1], "A0 dock"), (p1[0], p1[1], "A1 first bend"),
                       (p2[0], p2[1], "A2 fan-out/X1"), (p3[0], p3[1], "A3 rear trunk"),
                       (ped_exit[0], ped_exit[1], "P1 pedestal exit")):
        out += [f'<circle class="anchor" cx="{x:.1f}" cy="{y:.1f}" r="7"/>',
                f'<text class="small" x="{x+10:.1f}" y="{y-8:.1f}">{esc(name)}</text>']
    for point, label in ((servo, "fixed steering servo"), (esc_point, "relocated ESC candidate"),
                         (tail, "rear fan-out: LED / Hall / DRS")):
        out += [f'<circle class="conf-assumption" cx="{point[0]:.1f}" cy="{point[1]:.1f}" r="12"/>',
                f'<text class="label" x="{point[0]+16:.1f}" y="{point[1]+4:.1f}">{esc(label)}</text>']
    out += [
        '<text class="accent label" x="25" y="25">ONE UMBILICAL = ONE GANGED CASSETTE DOCK + ONE CHASSIS LOOM</text>',
        '<text class="small" x="25" y="44">A literal centre-spine trunk is rejected: it would occupy KO-01/KO-06. The dock turns immediately into R1/R2 edge highways.</text>',
        '<text class="small" x="25" y="64">Dashed blue = shielded USB4 + 2×3-pin servo leads in a 10×18 clear target conduit; straight-front dock projection is rejected.</text>',
        f'<line class="axis" x1="{mp(-140,-90)[0]:.1f}" y1="{mp(-140,-90)[1]:.1f}" x2="{mp(-90,-90)[0]:.1f}" y2="{mp(-90,-90)[1]:.1f}"/>',
        f'<text class="small" x="{mp(-140,-90)[0]:.1f}" y="{mp(-140,-90)[1]-8:.1f}">50 mm ruler · 2.5 px/mm</text>',
        "</svg>",
    ]
    return "".join(out)


def umbilical_page() -> str:
    page = page_start("Cassette umbilical", "connector seats + strain relief + fixed branches")
    page += """<p class="eyebrow">cassette audit / sheet D</p><h1>Umbilical route and connector seats</h1>
<div class="status"><b>CONNECTOR MAP FIRM; BODY SEATS ARE TARGET ALLOCATIONS.</b> The fixed-consumer dock must carry at least one XT60 pack inlet, two XT30 rail branches, five 3-pin servo positions, three JST-XH 3-pin links and one shielded USB4 link. A straight 16×64 mm body projection at the access edge overlaps the fixed pedestal, so a notched/wrapped full-size dummy is mandatory before any seat CAD.</div>
<div class="board"><h2>Physical route</h2><p class="sub">The route and family/count map are fixed. Dashed/hatched connector bodies, bank spans, bend radii and the dock station remain ASSUMPTION until terminated parts are measured.</p><div class="drawing">"""
    page += umbilical_svg()
    page += """</div></div><div class="board"><h2>Connector-seat rules</h2><div class="tablewrap"><table><thead><tr><th>Seat</th><th>Physical family</th><th>Location / access</th><th>Retention / strain relief</th><th>Open evidence</th></tr></thead><tbody>
<tr><td>U-PWR</td><td>1× XT60 pack inlet + minimum 2× XT30 Rail-A/Rail-B branches</td><td>~60 mm target face span; power physically distinct; source side shrouded/socket</td><td>XT60 20×20×12 and XT30 16×16×10 seat allocations</td><td>ASSUMPTION bodies: caliper housings, mating hand, wire gauge, bend and extraction</td></tr>
<tr><td>U-SRV</td><td>5× positive-lock 3-pin: steering, ESC (+5 absent), DRS, pan, tilt</td><td>~58 mm target face span; labelled; separate from power bank</td><td>16 mate-depth ×10 pitch ×8 high per position; anchor jackets</td><td>ASSUMPTION bodies: caliper shrouds/clips and prove finger release</td></tr>
<tr><td>U-SIG</td><td>3× JST-XH 3-pin: pack balance, LED, Hall; 1× shielded USB4 camera link</td><td>~64 mm target face span; keyed/labelled</td><td>XH3 12×12×9 each; USB4 16×16×10 allocation</td><td>ASSUMPTION bodies: pin-order witness, shell outline, shield termination and bends</td></tr>
<tr><td>U-AUX</td><td>blower 2-pin JST + speaker 2-pin JST-PH</td><td>adjacent auxiliary strip, visually distinct from signal/power</td><td>body seats remain unsized pending selected housings</td><td>ASM-31 full dock dummy; omission is not allowed</td></tr>
</tbody></table></div></div>
<div class="board"><h2>Internal connector-body allocations</h2><div class="tablewrap"><table><thead><tr><th>Link</th><th>Firm family</th><th>Target seat allocation</th><th>ASM closure</th></tr></thead><tbody>
<tr><td>CRSF</td><td>JST-XH 4-pin</td><td>15 mate-depth ×15 pitch ×9 high</td><td>caliper terminated housing, latch, conductor exit and RP1 service loop</td></tr>
<tr><td>link2</td><td>JST-XH 3-pin</td><td>12×12×9</td><td>caliper and label both ESP ends</td></tr>
<tr><td>I2S audio</td><td>JST-XH 5-pin</td><td>18×18×9</td><td>caliper, verify amp exit and speaker-wire separation</td></tr>
<tr><td>Wi-Fi RF</td><td>2× U.FL</td><td>12×12×6 bend/strain-relief reserve each; never clamp plug</td><td>real module + ≥10 mm coax bend + antenna-before-power tug check</td></tr>
</tbody></table></div></div>
<div class="board"><h2>Pedestal conduit target</h2><p><b>10×18 mm clear rounded rectangle, 2 mm trial wall → 14×22 mm outer.</b> Pull the shielded USB4 connector and two servo connectors through sequentially, not abreast. Reserve ≥25 mm of service loop below the pedestal and a provisional ≥20 mm USB bend radius before the R1/R2 turn. These are ASSUMPTION gauges: any terminated body over the pass gauge, cable bend that kinks, or wall coupon failure restarts the section.</p></div>
<div class="board"><h2>Strain-relief and service checks</h2><p>A0 supports the cassette-side connector bodies; A1 arrests the ganged bundle before its first direction change; A2 supports both fan-out branches at X1; A3 supports the rear tail before belt/shock/DRS approach. P1 anchors the pedestal leads after their lower turn. Add an anchor at every later branch and motion boundary. The body-off sequence must expose the entire dock, allow one-hand latch release, leave the chassis half parked, and let the cassette lift without pulling the fixed pedestal loom.</p></div>
<div class="board"><h2>Confidence</h2>""" + legend() + "</div>"
    return page + page_end()


def clean_longitudinal_gap() -> float:
    return (SUSP_X[0] - STATIC_CLEARANCE) - (SERVO_X[1] + STATIC_CLEARANCE)


def mini_shoulder_min(shell_tris) -> tuple[float, float, float]:
    """Minimum finite registered ceiling sampled over both assumed wall seats."""
    best = (math.inf, 0.0, 0.0)
    for x in range(int(MINI_X[0]), int(MINI_X[1]) + 1):
        station = K.section(shell_tris, "x", float(x))
        for sign in (-1.0, 1.0):
            for lateral in range(30, 44):
                roof = SHELL.ceil_profile(station, sign * lateral)
                if roof is not None and roof < best[0]:
                    best = (roof, float(x), sign * lateral)
    return best


def cell_shoulder_min(shell_tris, xr: tuple[float, float],
                      lr: tuple[float, float]) -> tuple[float, float, float]:
    """Minimum finite registered ceiling over a rectangular audit cell."""
    best = (math.inf, 0.0, 0.0)
    x = xr[0]
    while x <= xr[1] + 1e-9:
        station = K.section(shell_tris, "x", x)
        lateral = lr[0]
        while lateral <= lr[1] + 1e-9:
            roof = SHELL.ceil_profile(station, lateral)
            if roof is not None and roof < best[0]:
                best = (roof, x, lateral)
            lateral += 1.0
        x += 1.0
    return best


def mass_scenario(cassette_mass: float, pedestal_mass: float = 0.0) -> tuple[float, float, float, float, float]:
    """Target-input midpoint sensitivity; added masses remain parametric.

    PWR is replaced by the ~50 g PDB TARGET mass, which already contains both
    UBECs and the capacitor.  `cassette_mass` therefore means charge module +
    printed cassette/dock mass only; it must not count the PDB a second time.
    """
    items = [list(item) for item in ZONES.MASS_ITEMS]
    mids = [(item[2] + item[3]) / 2.0 for item in items]
    changes = {
        "DRV-ESC": (100.0, -27.1, -42.0, 13.6),
        "PWR-BAT-1": (100.0, -42.5, 45.0, 14.0),
        "PWR": (50.0, 23.5, 0.0, 10.0),
        "CONTROL": (72.5, 12.5, 0.0, 18.0),
        "CAM-GIMBAL": (70.0, 35.0, 0.0, 45.0),
    }
    for index, item in enumerate(items):
        if item[0] in changes:
            mass, x, lateral, z = changes[item[0]]
            mids[index] = mass
            item[4], item[5], item[6] = x, lateral, z
    base = ZONES._state(mids, [tuple(item) for item in items])
    total = base[0] + cassette_mass + pedestal_mass
    x = (base[0] * base[1] + cassette_mass * 10.0 + pedestal_mass * 35.0) / total
    lateral = (base[0] * base[2]) / total
    z = (base[0] * base[3] + cassette_mass * 10.0 + pedestal_mass * 25.0) / total
    front = 100.0 * (x - ZONES.REAR_AXLE_X) / ZONES.WHEELBASE
    return total, x, lateral, z, front


def evidence_markdown(shell_tris) -> str:
    roof, station_x, station_l = mini_shoulder_min(shell_tris)
    pdb_roof, pdb_x, pdb_l = cell_shoulder_min(shell_tris, PDB_X, PDB_L)
    base = mass_scenario(0.0, 0.0)
    illustrative = mass_scenario(25.0, 20.0)
    lines = [
        "# p0_d34 — lift-out electronics cassette physical audit",
        "",
        "This table is additive evidence. It does not revise D-28, prior placements,",
        "conclusions, source STLs or production-CAD authorization.",
        "",
        "## Fit result",
        "",
        "**CONDITIONAL-GO to a full-scale repack dummy; NO production CAD/STL.**",
        "The named lower target cells pack in plan and under the shell, but the",
        "everything-inside claim is not closed: PDB-to-KO clearance, Wi-Fi placement",
        "and a non-conflicting ganged dock remain open.",
        "",
        "| Check | Arithmetic / mesh result | Confidence | Disposition |",
        "|---|---|---|---|",
        f"| Mini-board X row | {clean_longitudinal_gap():.2f} mm clean interval; one 39 mm wall row leaves {clean_longitudinal_gap()-39:.2f} mm before plug/wall allowance | DERIVED + ASSUMPTION install | PASS gauge |",
        "| Mini-board steering separation | inner wall-seat faces at \\|L\\|=30 versus KO-01 boundary \\|L\\|=22 | DERIVED | 8 mm gauge; ASM-08 remains |",
        f"| Mini-board shell shoulder | worst finite S0=0 roof {roof:.2f} mm at X{station_x:+.0f}/L{station_l:+.0f}; Z32 top +5 requires S0≥{37-roof:.2f} mm | DERIVED shell + ASSUMPTION cell | CONDITIONAL; only {roof+11-37:.2f} mm surplus at S0+11 |",
        f"| PDB target vs shell | 45 X ×55 L footprint at X+1…+46/L±27.5, Z1…19; worst finite roof {pdb_roof:.2f} at X{pdb_x:+.0f}/L{pdb_l:+.1f} | DERIVED shell + TARGET envelope | PASS target gauge; {pdb_roof-24:.2f} mm static-policy surplus at S0=0 |",
        "| PDB target vs KO-01 | PDB top Z19 to provisional moving envelope start Z22 = 3 mm | DERIVED from TARGET placement | HOLD: 5 mm short of 8 mm moving policy until ASM-08 replaces KO-01 |",
        "| Lower named stuffing | PDB target + rear charge target + insulated amp/RP1 deck | TARGET/ASSUMPTION | packs in the stepped-T gauge; real holes/exits/thermal faces remain |",
        "| Decoupled pedestal | gimbal is floor/front-structure referenced; old cassette Z38 + 60 = Z98 arithmetic retired | architecture VERIFIED / geometry ASSUMPTION | old roof failure removed; halo/FOV/sweep/conduit open |",
        "| Battery/ESC side bodies | no cassette plan overlap; inner faces are only 0.5/1.5 mm outside raw KO-01, not 8 mm | DERIVED plan + DOCUMENTED ESC | CONDITIONAL on measured steering, shell, pack and ESC service volumes |",
        "| Wi-Fi + straight dock | Wi-Fi ≤60×32×12 remains uncalipered/unplaced; straight dock body projection X+42…+58/L±32 overlaps pedestal X+51…+65/L±11 | ASSUMPTION | full layout OPEN; D-06b + wrapped/notched connector dummy |",
        "| Existing floor holes | front candidates are vent/body-seat territory; rear candidates are single/asymmetric or servo/axle contested | VERIFIED feature map / ASSUMPTION occupancy | no clean four-point pattern |",
        "",
        "## Supplied target cells and remaining assumptions",
        "",
        "| Cell | Audit allocation | Confidence / rule |",
        "|---|---:|---|",
        "| PDB-CELL | 55×45×18 mm, ~50 g; includes 2× UBEC, 1000 µF cap, divider, USB-C charge input and star ground | FIRM contents / TARGET envelope and mass; final board L/W/H/holes/exits remain ASSUMPTION and ASM-22 |",
        "| CHG-CELL | 30×25×10 mm | TARGET envelope / SKU TBD; ASSUMPTION until selected and calipered at ASM-59 |",
        "| AMP-CELL | 17.8×19.4×3 mm reference | purchased-board geometry ASSUMPTION; insulated Z13…16 deck and exits to ASM-22/55 |",
        "| CASSETTE STRUCTURE | rear stem X−31…+1/L−18.5…+17.5; forward wing X+1…+42/L±43; tapered tongue X+42…+46/L±29.5; top Z19 | stepped-T ASSUMPTION gauge only |",
        "| MINI WALL SEATS | each 39 X ×31 Z ×~13 L; X+3…+42, L±30…43, Z1…32 | MH-ET identity/envelope FIRM input; holes, live plugs and wall retention ASSUMPTION |",
        "| DOCK BODY SEATS | XT60 20×20×12; XT30 16×16×10; 3-pin 16×10×8; XH3/4/5 12/15/18 square ×9; USB4 16×16×10; U.FL 12×12×6 | family/count FIRM; every body allocation ASSUMPTION pending terminated-part calipers |",
        "| PEDESTAL / CONDUIT | foot/core X+51…+65/L±11; 10×18 clear, 2 mm trial wall →14×22 outer; ≥25 mm lower slack | ASSUMPTION; sequential USB4/servo plug pull-through, bend and wall coupon at CAS-09 |",
        "",
        "## Mass / balance sensitivity",
        "",
        "The prior midpoint remains 1782 g, 35.0% front / 65.0% rear and Z-CG 22.2 mm.",
        "The updated ledger replaces the old 52.5 g PWR midpoint with the supplied",
        "~50 g PDB TARGET mass at X+23.5/Z10; it does not double-count the UBECs/cap.",
        "Let C be charge-module + printed cassette/dock mass not otherwise in the",
        "ledger at X+10/Z10, and P be added pedestal mass at X+35/Z25:",
        "",
        f"- before C/P: {base[0]:.1f} g, {base[4]:.2f}% front / {100-base[4]:.2f}% rear, Z-CG {base[3]:.2f} mm;",
        f"- illustrative C=25 g and P=20 g (**ASSUMPTION, not mass claims**): {illustrative[0]:.1f} g, {illustrative[4]:.2f}% front / {100-illustrative[4]:.2f}% rear, Z-CG {illustrative[3]:.2f} mm;",
        "- exact formula: total=1778.4+C+P; X moment=−7341.25+10C+35P;",
        "  Z moment=37933.5+10C+25P (g·mm); front%=100·(X-CG+90.9)/237.",
        "",
        "The illustration remains within the planning uncertainty and does not approve",
        "balance. Physical PDB/charge/cassette/pedestal weights and four-corner scales",
        "own the final result.",
        "",
        "## Mounting and umbilical",
        "",
        "- Existing holes alone do not make a clean, stable, serviceable four-point pattern.",
        "- The former X−15/+35, L±12 service-boss pattern is now REJECTED: its rear",
        "  pair lies inside the charge target and its front pair inside the PDB target.",
        "  Hiding service screws below modules would defeat lift-out access.",
        "- CAS-07 must establish a new reversible external saddle/clamp pattern with a",
        "  transparent full-stack dummy. M3×5 inserts remain coupon-gated; donor drilling",
        "  remains prohibited. No replacement coordinates are inferred here.",
        "- The fixed hollow pedestal carries one shielded USB4 + two 3-pin servo leads",
        "  through a 10×18 clear target section to an R1/R2 exit below Z22.",
        "- Firm dock minimum: XT60×1, XT30×2, 3-pin servo×5, XH3×3 and shielded USB4×1;",
        "  plus auxiliary blower/speaker seats. Internal seats reserve XH4, XH3, XH5",
        "  and 2×U.FL bodies. A straight access-edge dock overlaps the pedestal;",
        "  only a full-size stepped/wrapped dummy may select the final topology.",
        "",
        "## Reproducibility",
        "",
        "- Registered 2024 shell loaded through p0_03; S0=0 is the lower bound.",
        "- No STL was written, transformed in place, relieved or declared production-ready.",
        "- PDB contents, mini identity/envelope and connector map are supplied inputs.",
        "  PDB/charge final geometry, connector bodies, install retention, pedestal",
        "  and cassette structure remain ASSUMPTION/DEFER with named ASM checks.",
        "",
    ]
    return "\n".join(lines)


def index_page() -> str:
    illustrative = mass_scenario(25.0, 20.0)
    page = page_start("Electronics cassette audit", "separate physical-feasibility visualization set")
    page += f"""<p class="eyebrow">10_assembly_architecture / viz / cassette</p>
<h1>Lift-out electronics cassette audit</h1>
<div class="status"><b>CONDITIONAL-GO TO A FULL-SCALE REPACK DUMMY; EVERYTHING-INSIDE NOT CLOSED.</b> The supplied PDB/charge targets repack under the shell, but the PDB leaves only 3 mm to provisional KO-01, the Wi-Fi body is still unplaced, and a straight ganged dock overlaps the fixed pedestal. The old 110 mm board-row and Z98 gimbal failures remain removed. No production STL or relief.</div>
<div class="summary">
<div class="card"><strong>+58.4 mm</strong><span>39 mm mini row residual in the clean X interval</span></div>
<div class="card fail"><strong>S0≥9.82</strong><span>wall-seat shoulder condition with 5 mm static policy</span></div>
<div class="card fail"><strong>3 / 8 mm</strong><span>PDB-to-KO-01 vertical gap / moving policy</span></div>
<div class="card"><strong>{illustrative[4]:.1f}/{100-illustrative[4]:.1f}</strong><span>illustrative front/rear at C25 + P20 · ASSUMPTION</span></div>
</div>
<div class="board"><h2>Sheets</h2><div class="cards">
<a class="card fail" href="layout.html"><span class="tag assumption">SHEET A</span><b> Plan + side + shell section</b><p>Stepped-T target repack, wall minis, unresolved Wi-Fi/dock, battery, ESC, motor, belt and pedestal.</p></a>
<a class="card fail" href="exploded.html"><span class="tag assumption">SHEET B</span><b> Exploded cassette</b><p>Floor → saddle → PDB/charge → amp/RP1 deck → wall minis; Wi-Fi and dock visibly open.</p></a>
<a class="card fail" href="pedestal.html"><span class="tag defer">SHEET C</span><b> Cockpit pedestal</b><p>Floor/front joint, floor-referenced gimbal reserve and hollow USB/2×MG90S path.</p></a>
<a class="card fail" href="umbilical.html"><span class="tag assumption">SHEET D</span><b> Umbilical route</b><p>Firm XT60/XT30/3-pin/XH/U.FL map, assumed body seats, 10×18 conduit and rejected straight dock.</p></a>
</div></div>
<div class="board"><h2>Audit boundary</h2><p>The PDB contents and connector map are accepted as supplied electrical inputs; this set does not design their circuit. TARGET/TBD geometry remains ASSUMPTION until the named ASM checks. The source study is <a href="../../fit_studies/ZK_electronics_cassette_fit_study.md">ZK electronics cassette fit study</a>; machine evidence is <a href="../../evidence/p0/tables/p0_d34_cassette_fit_audit.md">p0_d34</a>.</p></div>
<div class="board"><h2>Confidence</h2>{legend()}</div>"""
    return page + page_end()


def master_block() -> str:
    return f"""{INDEX_START}
<div class="board"><h2>Lift-out cassette physical audit</h2>
<p class="sub">Separate, fit-gated visualization set for the owner/Claude cassette architecture. It preserves the prior eight-zone and connection sets.</p>
<div class="gategrid"><a class="gate rank-high" href="cassette/index.html"><span class="tag assumption">CASSETTE · REPACK DUMMY ONLY</span> <b>Electronics cassette audit</b><p>55×45×18 PDB target repack · 3/8 mm KO gap · unplaced Wi-Fi · firm connector map / assumed bodies · no production STL</p></a></div></div>
{INDEX_END}"""


def replace_master_block() -> None:
    text = MASTER.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(INDEX_START) + r".*?" + re.escape(INDEX_END), re.S)
    block = master_block()
    if pattern.search(text):
        text = pattern.sub(block, text)
    else:
        anchor = '<div class="board"><h2>Evidence chain</h2>'
        if anchor not in text:
            raise RuntimeError("viz/index.html anchor missing")
        text = text.replace(anchor, block + "\n" + anchor, 1)
    MASTER.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    shell_tris = SHELL.load_assembled()
    EVIDENCE.write_text(evidence_markdown(shell_tris), encoding="utf-8")
    (OUT / "index.html").write_text(index_page(), encoding="utf-8")
    (OUT / "layout.html").write_text(layout_page(shell_tris), encoding="utf-8")
    (OUT / "exploded.html").write_text(exploded_page(), encoding="utf-8")
    (OUT / "pedestal.html").write_text(pedestal_page(shell_tris), encoding="utf-8")
    (OUT / "umbilical.html").write_text(umbilical_page(), encoding="utf-8")
    replace_master_block()
    print(f"WROTE cassette evidence: {EVIDENCE.relative_to(REPO)}")
    print(f"WROTE 5 self-contained cassette HTML files to {OUT.relative_to(REPO)}")
    print(f"EMBEDDED {len(CONNECTIONS.MESH_CACHE)} read-only STL silhouettes")
    print(f"UPDATED cassette link block in {MASTER.relative_to(REPO)}")
    print("VERDICT REPACK DUMMY ONLY / EVERYTHING-INSIDE OPEN — no production STL emitted")


if __name__ == "__main__":
    main()
