#!/usr/bin/env python3
"""Generate the detailed, self-contained W17 zone engineering drawings.

The evidence and conclusions remain owned by p0_07_zone_fit_rollup.py.  This
script only visualises them.  It reads the same 18 component STLs plus the two
registered 2024 shell meshes.  Mesh gallery images are deterministic
point-sampled, flat-shaded, depth-sorted PNGs written with numpy + stdlib and
embedded as data URIs.  A per-run render cache avoids rendering a mesh twice.

No production mesh is created or modified.  Hardware without a controlled mesh
is deliberately drawn as a labelled technical outline and retains its source
confidence.

Run from the repository root:

    python3 10_assembly_architecture/evidence/scripts/p0_08_zone_visualizations.py
"""
from __future__ import annotations

import base64
from collections import deque
import hashlib
import html
import math
import os
from pathlib import Path
import struct
import zlib

import numpy as np
import trimesh

import p0_07_zone_fit_rollup as D
import stlkit as K


REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "10_assembly_architecture/viz"
PX = 4.0
DETAIL_PX = 6.0
RENDER_CACHE: dict[str, str] = {}

FLOOR_PLAN = [
    (-141, -34), (-110, -56), (-30, -68.5), (30, -68.5), (55, -26.5),
    (180, -15), (180, 15), (55, 26.5), (30, 68.5), (-30, 68.5),
    (-110, 56), (-141, 34),
]

ZONE = {
    "rear": {
        "code": "ZR", "station": -60.0, "xr": (-145, -15), "lr": (-82, 82),
        "status": "FAIL — current side ESC intersects the S0=0 shell envelope.",
        "tone": "fail", "gate": "D-28 / ASM-49 + D-16 / ASM-51",
        "governor": "43×36.8×32.3 ESC + 10 mm fan plane; belt/gear axes remain open.",
    },
    "power": {
        "code": "ZP", "station": -20.0, "xr": (-95, 45), "lr": (-75, 75),
        "status": "FAIL / PROVISIONAL — one active pack selected; present candidate does not clear S0=0 + KO-01.",
        "tone": "fail", "gate": "D-31 / ASM-50 + D-39 / ASM-58",
        "governor": "75×45×25 pack at X−44/L+25/Z+3; second pack stays off-car.",
    },
    "control": {
        "code": "ZC", "station": -20.0, "xr": (-90, 145), "lr": (-75, 75),
        "status": "PROVISIONAL — inboard deck edge is plausible; outboard board edge fails S0=0.",
        "tone": "warn", "gate": "D-32/33 / ASM-52",
        "governor": "ESP32 top Z≈33 against 39 mm at |L|20 and 26 mm at |L|30.",
    },
    "camera": {
        "code": "ZV", "station": 60.0, "xr": (-85, 105), "lr": (-68, 68),
        "status": "UNRESOLVED — camera identity and physical module dimensions block geometry.",
        "tone": "warn", "gate": "D-34 / ASM-53",
        "governor": "IMX415-vs-IMX335 identity, FOV, airflow, service pull and full gimbal sweep.",
    },
    "servos": {
        "code": "ZA", "station": 60.0, "xr": (-150, 105), "lr": (-78, 78),
        "status": "UNRESOLVED — MG90S clone bodies, horns, endpoints and DRS pocket are unmeasured.",
        "tone": "warn", "gate": "D-35 / ASM-54",
        "governor": "15 mm assumed horn reserve, gimbal sweep and 58 mm DRS-arm envelope.",
    },
    "audio": {
        "code": "ZL", "station": -30.0, "xr": (-150, 90), "lr": (-78, 78),
        "status": "PROVISIONAL — speaker shell margin is plausible; ports and seven-pixel lens mapping remain open.",
        "tone": "warn", "gate": "D-36 / ASM-55",
        "governor": "Speaker ≤12 mm tall; 3 mm vent; 33.33 mm WS2812 pixel pitch.",
    },
    "suspension": {
        "code": "ZS", "station": 146.1, "xr": (-135, 190), "lr": (-102, 102),
        "status": "HIGH RISK — ≈3.5/4 mm tyre-arch gaps are below moving policy; shock length conflicts.",
        "tone": "fail", "gate": "D-37 / ASM-56",
        "governor": "Ø64 F104 tyres through steer+bump; 51 mm requirement vs 52 mm stock label.",
    },
    "sensors": {
        "code": "ZH", "station": -90.9, "xr": (-122, -60), "lr": (-68, 10),
        "status": "UNRESOLVED — Hall gap and switching repeatability require the assembled rotating axle.",
        "tone": "warn", "gate": "D-38 / ASM-57",
        "governor": "1.5 mm cold target inside a 1–3 mm test band; collar/runout unknown.",
    },
}

# Candidate installation envelopes.  Component dimensions retain their evidence
# confidence; all coordinates here are exactly the p0_07 planning placements and
# therefore use ASSUMPTION styling unless noted.
ITEMS = {
    "rear": [
        ("DRV-ESC", -60, -25, 3, 43, 36.8, 32.3, "box", "ESC · fan up"),
        ("DRV-MOT", -105, 0, 9, 36, 54, 36, "motor", "Ø36 motor"),
        ("DRV-SPUR", -90.9, -25, 6.6, 40.75, 4, 40.75, "gear", "75T Ø40.75"),
        ("DRV-PINION", -63.65, -25, 19, 15.88, 4, 15.88, "gear", "28T Ø15.88"),
        ("SHK-REAR", -43, 0, 10, 68, 18, 35, "shock", "68 mm shock"),
        ("DRV-BELT", -100, -39, 10, 36, 6, 35, "belt", "140 mm belt loop"),
    ],
    "power": [
        ("PWR-BAT-1", -44, 25, 3, 75, 45, 25, "battery", "ACTIVE pack"),
        ("PWR-UBEC-A", -15, -38, 3, 30, 14, 10, "inline", "UBEC A"),
        ("PWR-UBEC-B", -48, -38, 3, 30, 14, 10, "inline", "UBEC B"),
        ("PWR-CAP-B", -48, -48, 3, 10, 10, 20, "cap", "1000 µF"),
        ("PWR-XT60", 20, -40, 3, 20, 18, 15, "connector", "XT60 junction"),
        ("PWR-BUZZ", 25, -50, 3, 30, 12, 8, "board", "BX100"),
    ],
    "control": [
        ("CTL-E1", 10, -32, 20, 55, 28, 13, "board", "ESP32 #1"),
        ("CTL-E2", -45, -32, 20, 55, 28, 13, "board", "ESP32 #2"),
        ("VID-WIFI", -45, -18, 20, 60, 32, 12, "board", "Wi-Fi P9 max"),
        ("RX-ELRS", 20, 38, 3, 13, 11, 3, "board", "RP1"),
        ("VID-HS", -45, -18, 32, 28, 28, 3, "fins", "28×28 heatsink"),
    ],
    "camera": [
        ("VID-CAM", 60, 0, 20, 55, 45, 60, "camera", "Option A reserve"),
        ("CAM-TOP", -53.2, 0, 73.35, 16.75, 17.72, 6.92, "mesh", "camera top 1.1"),
        ("COOL-BLOW", 42, -25, 35, 20, 20, 10, "blower", "20 mm blower"),
        ("COOL-DUCT", 50, -14, 38, 18, 20, 8, "duct", "duct defaults"),
    ],
    "servos": [
        ("SRV-PAN", 60, 0, 20, 22.8, 12.2, 28.5, "servo", "pan MG90S"),
        ("SRV-TILT", 60, 0, 45, 22.8, 28.5, 12.2, "servo", "tilt MG90S"),
        ("SRV-DRS", -125, 0, 55, 22.8, 12.2, 28.5, "servo", "DRS MG90S"),
        ("DRS-ARM", -112, 0, 72, 58, 5, 10, "arm", "58 mm DRS arm"),
    ],
    "audio": [
        ("AUD-SPK", -30, 43, 3, 40, 40, 12, "speaker", "speaker Ø28–40"),
        ("AUD-AMP", -5, -40, 15, 19.4, 17.8, 3, "board", "MAX98357A ref."),
        ("LGT-DIFF", -125, 0, 35, 9.5, 12, 14.5, "mesh", "rear diffuser"),
        ("LGT-LED", -120, 40, 42, 66.7, 10, 3, "led", "indicator pair"),
        ("HALO", 60, 0, 48, 74.94, 38.75, 24.86, "mesh", "halo"),
    ],
    "suspension": [
        ("TYRE-F", 146.1, 75, -5, 64, 30, 64, "tyre", "front tyre L"),
        ("TYRE-F", 146.1, -75, -5, 64, 30, 64, "tyre", "front tyre R"),
        ("TYRE-R", -90.9, 72.5, -5, 64, 35, 64, "tyre", "rear tyre L"),
        ("TYRE-R", -90.9, -72.5, -5, 64, 35, 64, "tyre", "rear tyre R"),
        ("SHK-FRONT", 132, 60, 10, 52, 10, 35, "shock", "front shock"),
        ("UPRIGHT-L", 146.1, 58, 2, 56.86, 20, 49.99, "mesh", "upright L"),
    ],
    "sensors": [
        ("SNS-MAG", -90.9, -25, 25.5, 3, 1, 3, "magnet", "Ø3×1 magnet"),
        ("SNS-HALL", -90.9, -29, 23, 4.17, 3.1, 1.57, "hall", "A3144"),
        ("BRACKET", -90.9, -33, 18, 12, 8, 12, "bracket", "adjustable bracket"),
    ],
}

ITEM_DIM_CONF = {
    "rear": ("DOCUMENTED", "documented"),
    "power": ("DOCUMENTED", "documented"),
    "control": ("ASSUMPTION", "assumption"),
    "camera": ("ASSUMPTION", "assumption"),
    "servos": ("DOCUMENTED", "documented"),
    "audio": ("ASSUMPTION", "assumption"),
    "suspension": ("DOCUMENTED", "documented"),
    "sensors": ("DOCUMENTED", "documented"),
}

CLEARANCES = {
    "rear": [
        ("C1", "ESC @ X−60/L−25", "body top Z35.3", "shell ≈19 mm at |L|30–40", "FAIL · interference", "DERIVED"),
        ("C2", "ESC fan plane", "Z45.3", "shell width 17 mm @Z45", "FAIL · <25 mm fan", "DERIVED"),
        ("C3", "belt/shock/static", "≥8 mm", "nearest distance TO MEASURE", "OPEN", "ASSUMPTION"),
        ("C4", "gear guard", "≥2 mm radial", "hub/backlash UNKNOWN", "OPEN", "ASSUMPTION"),
    ],
    "power": [
        ("C1", "pack @ L≈45", "top Z28", "ceiling Z27→24", "FAIL · −1…−4 mm raw", "DERIVED"),
        ("C2", "pack vs KO-01", "pack Z3…28", "KO Z22…38, |L|≤22", "FAIL · overlap", "DERIVED"),
        ("C3", "static shell policy", "≥5 mm", "current raw margin negative", "FAIL", "DOCUMENTED"),
        ("C4", "battery X adjustment", "±10 mm", "whole-car X-CG ≈0.6 mm", "LOW SENSITIVITY", "DERIVED"),
    ],
    "control": [
        ("C1", "board top @ |L|20", "Z≈33", "ceiling 39", "PASS RAW · +6 mm", "DERIVED"),
        ("C2", "board top @ |L|30", "Z≈33", "ceiling 26", "FAIL · −7 mm", "DERIVED"),
        ("C3", "U.FL bend", "≥10 mm radius", "route TO PROVE", "OPEN", "DOCUMENTED"),
        ("C4", "RF separation target", "≥150 mm systems", "route ASSUMPTION", "OPEN", "ASSUMPTION"),
    ],
    "camera": [
        ("C1", "lens to fixed structure", "≥5 mm", "camera body/FOV UNKNOWN", "OPEN", "DOCUMENTED"),
        ("C2", "horn/link to fixed", "≥8 mm", "full sweep UNKNOWN", "OPEN", "DOCUMENTED"),
        ("C3", "blower inlet/outlet", "unobstructed", "thickness/outlet TO MEASURE", "OPEN", "ASSUMPTION"),
        ("C4", "Option A vs B Z-CG", "22.2→23.2 mm", "midpoint model", "B raises CG", "DERIVED"),
    ],
    "servos": [
        ("C1", "pan/tilt horn reserve", "r=15 mm", "real horns TO MEASURE", "OPEN", "ASSUMPTION"),
        ("C2", "gimbal moving clearance", "≥8 mm", "endpoints UNKNOWN", "OPEN", "DOCUMENTED"),
        ("C3", "DRS arm/static", "≥8 mm", "58 mm arm, angle UNKNOWN", "OPEN", "ASSUMPTION"),
        ("C4", "MG90S body", "22.8×12.2×28.5", "clone TO MEASURE", "OPEN", "DOCUMENTED"),
    ],
    "audio": [
        ("C1", "speaker top", "≤Z15", "raw shell +9…12 mm", "PASS RAW", "DERIVED"),
        ("C2", "after static policy", "≥5 mm", "remaining +4…7 mm", "PROVISIONAL PASS", "DERIVED"),
        ("C3", "cone/port free space", "≥3 mm", "speaker TO MEASURE", "OPEN", "ASSUMPTION"),
        ("C4", "rear LEDs vs motion", "≥8 mm", "DRS/shock sweep UNKNOWN", "OPEN", "DOCUMENTED"),
    ],
    "suspension": [
        ("C1", "front tyre arch", "Ø64", "≈3.5 mm registered gap", "HIGH RISK", "DERIVED"),
        ("C2", "rear tyre arch", "Ø64", "≈4 mm registered gap", "HIGH RISK", "DERIVED"),
        ("C3", "front sweep envelope", "X±35.3 / L±27.1", "±25° steer ASSUMPTION", "OPEN", "DERIVED"),
        ("C4", "wheel-centre bump", "Z22…34", "stroke/ratio TO MEASURE", "OPEN", "ASSUMPTION"),
        ("C5", "shock/body", "≥3 mm", "51 vs 52 mm conflict", "OPEN", "ASSUMPTION"),
    ],
    "sensors": [
        ("C1", "cold Hall face gap", "1.5 mm target", "shaft/collar runout UNKNOWN", "OPEN", "ASSUMPTION"),
        ("C2", "switching test band", "1–3 mm", "hand-spin validation pending", "OPEN", "ASSUMPTION"),
        ("C3", "bracket to collar", "≥2 mm except face", "bracket geometry UNKNOWN", "OPEN", "ASSUMPTION"),
        ("C4", "Hall to belt/gear", "≥8 mm", "rear stack transform UNKNOWN", "OPEN", "DOCUMENTED"),
    ],
}


CSS = r"""
:root {
  color-scheme:light dark;
  --bg:#edf1f0; --paper:#fff; --ink:#15201f; --muted:#596866;
  --line:#bdc9c7; --grid:#dce3e2; --ground:#d8dfde; --accent:#00857c;
  --accent2:#00aa9c; --soft:#e7f4f2; --good:#1f8f5f; --warn:#b05b22;
  --bad:#bf3f35; --assume:#687573; --scan:#111918;
  --shadow:0 1px 2px rgba(20,32,31,.08),0 9px 25px rgba(20,32,31,.06);
}
@media (prefers-color-scheme: dark) {
  :root { --bg:#0c1211; --paper:#121b1a; --ink:#e7eeed; --muted:#9aa9a6;
    --line:#2a3a38; --grid:#263230; --ground:#1d2927; --accent:#27c9b9;
    --accent2:#56e0d2; --soft:#163330; --good:#3bbd7f; --warn:#e08a4f;
    --bad:#e06758; --assume:#9ba8a6; --scan:#0a0f0e;
    --shadow:0 1px 2px rgba(0,0,0,.42),0 10px 30px rgba(0,0,0,.35); }
}
:root[data-theme="light"] {
  --bg:#edf1f0; --paper:#fff; --ink:#15201f; --muted:#596866;
  --line:#bdc9c7; --grid:#dce3e2; --ground:#d8dfde; --accent:#00857c;
  --accent2:#00aa9c; --soft:#e7f4f2; --good:#1f8f5f; --warn:#b05b22;
  --bad:#bf3f35; --assume:#687573; --scan:#111918;
  --shadow:0 1px 2px rgba(20,32,31,.08),0 9px 25px rgba(20,32,31,.06);
}
:root[data-theme="dark"] {
  --bg:#0c1211; --paper:#121b1a; --ink:#e7eeed; --muted:#9aa9a6;
  --line:#2a3a38; --grid:#263230; --ground:#1d2927; --accent:#27c9b9;
  --accent2:#56e0d2; --soft:#163330; --good:#3bbd7f; --warn:#e08a4f;
  --bad:#e06758; --assume:#9ba8a6; --scan:#0a0f0e;
  --shadow:0 1px 2px rgba(0,0,0,.42),0 10px 30px rgba(0,0,0,.35);
}
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
p { max-width:92ch; }
.lede { font-size:clamp(15px,1.6vw,18px); color:var(--muted); margin-top:0; }
.board { background:var(--paper); border:1px solid var(--line); border-radius:13px;
  box-shadow:var(--shadow); padding:clamp(14px,2.4vw,26px); margin-top:24px; }
.sub { color:var(--muted); margin:2px 0 14px; font-size:13.5px; }
.status { display:flex; gap:12px; align-items:flex-start; border-radius:10px;
  padding:12px 14px; margin:18px 0; border:1px solid var(--line); }
.status.fail { background:color-mix(in srgb,var(--bad) 10%,var(--paper)); }
.status.warn { background:color-mix(in srgb,var(--warn) 9%,var(--paper)); }
.status .flag { flex:0 0 auto; font:800 12px/1.4 ui-monospace,monospace; letter-spacing:.06em; }
.status.fail .flag { color:var(--bad); } .status.warn .flag { color:var(--warn); }
.meta,.legend,.parts,.gategrid,.summary { display:grid; gap:12px; }
.meta { grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); margin:20px 0 0; }
.chip { border:1px solid var(--line); border-radius:9px; padding:11px 13px; background:var(--paper); }
.chip b { display:block; color:var(--muted); font:700 10px/1.4 ui-monospace,monospace;
  letter-spacing:.1em; text-transform:uppercase; margin-bottom:2px; }
.drawing { width:100%; overflow-x:auto; overscroll-behavior-inline:contain;
  border:1px solid var(--line); border-radius:9px; background:var(--paper); }
.drawing svg { display:block; width:max(100%,var(--drawing-w,900px)); height:auto; }
.views { display:grid; grid-template-columns:1fr; gap:20px; }
@media(min-width:1080px) { .views.two { grid-template-columns:1fr 1fr; } }
.legend { grid-template-columns:repeat(auto-fit,minmax(215px,1fr)); margin:13px 0 0; }
.legend span { display:flex; align-items:center; gap:9px; color:var(--muted); font-size:12px; }
.swatch { width:40px; height:16px; background:var(--soft); border:2px solid var(--accent); }
.swatch.derived { border-width:1px; }
.swatch.documented { border-style:dotted; }
.swatch.assumption { border-color:var(--assume); border-style:dashed;
  background:repeating-linear-gradient(135deg,transparent 0 5px,color-mix(in srgb,var(--assume) 20%,transparent) 5px 7px); }
.parts { grid-template-columns:repeat(auto-fit,minmax(285px,1fr)); }
.part { border:1px solid var(--line); border-radius:11px; overflow:hidden; background:var(--paper); }
.partviz { position:relative; min-height:145px; display:grid; place-items:center;
  background:var(--scan); border-bottom:1px solid var(--line); overflow:hidden; }
.partviz img,.partviz svg { display:block; width:100%; height:auto; }
.partviz .viewlabel { position:absolute; left:9px; bottom:7px; color:#91aaa6;
  font:10px/1.3 ui-monospace,monospace; letter-spacing:.04em; }
.partbody { padding:13px 14px 15px; }
.partbody h3 { margin-bottom:4px; }
.tag { display:inline-block; border:1px solid currentColor; border-radius:4px;
  padding:2px 6px; font-size:10px; font-weight:800; letter-spacing:.05em; color:var(--accent); }
.tag.derived { border-width:1px; }
.tag.documented { border-style:dotted; }
.tag.assumption { color:var(--assume); border-style:dashed; }
.kv { display:grid; grid-template-columns:86px 1fr; gap:4px 9px; margin-top:10px; font-size:12.5px; }
.kv b { color:var(--muted); font-weight:650; }
.evidence { border-top:1px solid var(--grid); padding-top:9px; margin-top:10px;
  color:var(--muted); font-size:11.5px; overflow-wrap:anywhere; }
.tablewrap { width:100%; overflow-x:auto; border:1px solid var(--line); border-radius:9px; }
table { border-collapse:collapse; width:100%; min-width:880px; background:var(--paper); }
th,td { padding:9px 10px; text-align:left; vertical-align:top; border-bottom:1px solid var(--grid); }
th { color:var(--muted); font-size:10px; letter-spacing:.06em; text-transform:uppercase; }
tr:last-child td { border-bottom:0; }
.result-fail { color:var(--bad); font-weight:750; } .result-pass { color:var(--good); font-weight:750; }
.note { border-left:3px solid var(--accent); background:var(--soft); padding:12px 15px;
  border-radius:0 9px 9px 0; margin:16px 0 0; color:var(--muted); font-size:13px; }
.summary { grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); margin:20px 0 0; }
.summary>div { background:var(--paper); border:1px solid var(--line); border-radius:9px; padding:14px; }
.summary strong { display:block; color:var(--accent); font-size:1.35rem; }
.summary span { color:var(--muted); font-size:11.5px; }
.gategrid { grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); }
.gate { display:block; color:var(--ink); text-decoration:none; border:1px solid var(--line);
  border-left:5px solid var(--warn); border-radius:9px; padding:14px; background:var(--paper); }
.gate.rank-high { border-left-color:var(--bad); }
.gate.rank-watch { border-left-color:var(--accent); }
.gate p { margin:4px 0 0; color:var(--muted); font-size:12.5px; }
footer { border-top:1px solid var(--line); color:var(--muted); padding:22px 0 34px; font-size:12.5px; }
svg .gridline { stroke:var(--grid); stroke-width:.7; }
svg .axis { stroke:var(--ink); stroke-width:1.5; fill:none; }
svg .floor { stroke:var(--ink); stroke-width:2; fill:none; }
svg .shell { stroke:var(--muted); stroke-width:1.4; fill:color-mix(in srgb,var(--muted) 13%,transparent); }
svg .shellmat { stroke:var(--muted); stroke-width:1.1; fill:color-mix(in srgb,var(--muted) 20%,transparent); fill-rule:evenodd; }
svg .conf-verified { stroke:var(--accent); stroke-width:2.2; fill:color-mix(in srgb,var(--accent) 16%,transparent); }
svg .conf-derived { stroke:var(--accent); stroke-width:1.2; fill:color-mix(in srgb,var(--accent) 9%,transparent); }
svg .conf-documented { stroke:var(--accent); stroke-width:1.7; stroke-dasharray:2 4; fill:color-mix(in srgb,var(--accent) 8%,transparent); }
svg .conf-assumption { stroke:var(--assume); stroke-width:1.7; stroke-dasharray:7 5; fill:url(#hatch); }
svg .moving { stroke:var(--warn); stroke-width:1.6; stroke-dasharray:7 4; fill:url(#moveHatch); }
svg .failure { stroke:var(--bad); stroke-width:1.7; fill:url(#failHatch); }
svg .pass { stroke:var(--good); stroke-width:1.5; fill:color-mix(in srgb,var(--good) 13%,transparent); }
svg .dim { stroke:var(--muted); stroke-width:1; fill:none; marker-start:url(#arrow); marker-end:url(#arrow); }
svg .dim.conf-documented { stroke-dasharray:2 4; } svg .dim.conf-assumption { stroke-dasharray:7 5; }
svg .tick { stroke:var(--muted); stroke-width:1; }
svg .leader { stroke:var(--muted); stroke-width:1; fill:none; }
svg .label { fill:var(--ink); font-size:11px; } svg .small { fill:var(--muted); font-size:9.5px; }
svg .tiny { fill:var(--muted); font-size:8px; } svg .accent { fill:var(--accent); }
svg .badtext { fill:var(--bad); font-weight:800; } svg .goodtext { fill:var(--good); font-weight:800; }
@media(max-width:640px) { .bar,.page { width:min(100% - 20px,1420px); }
  main { padding-top:20px; } .brand span { display:none; } .kv { grid-template-columns:74px 1fr; } }
"""

SCRIPT = r"""
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


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def conf_class(confidence: str) -> str:
    c = confidence.upper()
    if "ASSUMPTION" in c:
        return "assumption"
    if "DOCUMENTED" in c:
        return "documented"
    if "DERIVED" in c:
        return "derived"
    return "verified"


def defs() -> str:
    return """<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
 <path d="M40 0H0V40" class="gridline" fill="none"/>
</pattern>
<pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
 <line x1="0" y1="0" x2="0" y2="9" stroke="var(--assume)" stroke-width="1" opacity=".38"/>
</pattern>
<pattern id="moveHatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
 <line x1="0" y1="0" x2="0" y2="10" stroke="var(--warn)" stroke-width="2" opacity=".42"/>
</pattern>
<pattern id="failHatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
 <rect width="8" height="8" fill="color-mix(in srgb,var(--bad) 12%,transparent)"/>
 <line x1="0" y1="0" x2="0" y2="8" stroke="var(--bad)" stroke-width="2" opacity=".62"/>
</pattern>
<marker id="arrow" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
 <path d="M0 0L8 4L0 8Z" fill="context-stroke"/>
</marker>
</defs>"""


def page_start(title: str, subtitle: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'">
<title>{esc(title)} · W17 assembly architecture</title>
<style>{CSS}</style></head><body>
<header><div class="bar">
 <div class="brand"><b>W17 / RC-01</b><span>{esc(subtitle)}</span></div>
 <div><a href="index.html">Overview</a> · <button data-theme-toggle type="button">Theme</button></div>
</div></header><main><div class="page">"""


def page_end() -> str:
    return f"""</div></main><footer><div class="page">
Generated by <code>10_assembly_architecture/evidence/scripts/p0_08_zone_visualizations.py</code>.
Evidence: <code>p0_07</code> / D-28…D-39 plus the measured D-02 S0=0 shell sections.
No production STL, hardware identity, or unresolved coordinate is authorized by these drawings.
</div></footer><script>{SCRIPT}</script></body></html>"""


def _png_bytes(rgb: np.ndarray) -> bytes:
    h, w, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[y].tobytes() for y in range(h))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(
            ">I", zlib.crc32(kind + data) & 0xFFFFFFFF
        )

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def mesh_data_uri(component_id: str) -> str:
    """Return deterministic, cached isometric + orthographic mesh render."""
    if component_id in RENDER_CACHE:
        return RENDER_CACHE[component_id]
    rel = D.STL_SOURCES[component_id][0]
    path = REPO / rel
    loaded = trimesh.load_mesh(path, process=False)
    if isinstance(loaded, trimesh.Scene):
        mesh = trimesh.util.concatenate(tuple(loaded.geometry.values()))
    else:
        mesh = loaded
    seed = int(hashlib.sha256(rel.encode("utf-8")).hexdigest()[:8], 16)
    count = min(70000, max(22000, len(mesh.faces) * 6))
    points, faces = trimesh.sample.sample_surface(mesh, count, seed=seed)
    points = np.array(points, dtype=np.float64, copy=True)
    normals = np.array(np.asarray(mesh.face_normals)[faces], dtype=np.float64, copy=True)
    centre = (points.min(axis=0) + points.max(axis=0)) / 2.0
    points = points - centre
    canvas = np.zeros((250, 640, 3), dtype=np.uint8)
    canvas[:] = np.array([13, 22, 21], dtype=np.uint8)
    views = [
        (
            np.array([0.707, -0.707, 0.0]),
            np.array([-0.408, -0.408, 0.816]),
            np.array([0.577, 0.577, 0.577]),
        ),
        (
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 0.0, 1.0]),
            np.array([0.0, -1.0, 0.0]),
        ),
    ]
    light = np.array([0.28, -0.38, 0.88])
    light /= np.linalg.norm(light)
    for panel, (u, v, depth_axis) in enumerate(views):
        # Elementwise reductions avoid platform BLAS alignment quirks while
        # retaining the exact deterministic projection.
        uu = np.sum(points * u[None, :], axis=1)
        vv = np.sum(points * v[None, :], axis=1)
        dd = np.sum(points * depth_axis[None, :], axis=1)
        span_u = max(float(np.ptp(uu)), 1e-6)
        span_v = max(float(np.ptp(vv)), 1e-6)
        scale = min(278 / span_u, 202 / span_v)
        x = (uu - (uu.min() + uu.max()) / 2) * scale + panel * 320 + 160
        y = -(vv - (vv.min() + vv.max()) / 2) * scale + 118
        shade = np.clip(0.32 + 0.68 * np.abs(np.sum(normals * light[None, :], axis=1)), 0, 1)
        order = np.argsort(dd)
        xi = np.clip(x[order].astype(int), panel * 320 + 8, panel * 320 + 311)
        yi = np.clip(y[order].astype(int), 7, 226)
        sh = shade[order]
        colors = np.column_stack(
            (24 + 18 * sh, 96 + 112 * sh, 91 + 101 * sh)
        ).astype(np.uint8)
        for ox, oy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            canvas[np.clip(yi + oy, 0, 249), np.clip(xi + ox, 0, 639)] = colors
    canvas[:, 319:321] = np.array([48, 66, 63], dtype=np.uint8)
    canvas[232:234, 12:112] = np.array([51, 204, 189], dtype=np.uint8)
    data = base64.b64encode(_png_bytes(canvas)).decode("ascii")
    uri = "data:image/png;base64," + data
    RENDER_CACHE[component_id] = uri
    return uri


def technical_icon(component_id: str) -> str:
    """Recognisable technical outline for hardware that has no controlled mesh."""
    cid = component_id
    base = ['<svg viewBox="0 0 320 150" role="img" aria-label="Technical outline; no controlled mesh">', defs(),
            '<rect width="320" height="150" fill="var(--scan)"/>']
    line = 'stroke="#34c9b9" fill="none" stroke-width="3"'
    fill = 'fill="#1b4b47" stroke="#34c9b9" stroke-width="2"'
    if cid == "DRV-ESC":
        base += [f'<rect x="72" y="38" width="160" height="82" rx="8" {fill}/>',
                 f'<circle cx="152" cy="79" r="29" {line}/>',
                 f'<path d="M152 50v58M123 79h58M132 59l40 40M172 59l-40 40" {line}/>',
                 f'<path d="M232 52c30-18 35-12 56-25M232 78c33-8 39 0 56-8M232 104c31 7 36 14 55 21" {line}/>']
    elif cid == "DRV-MOT":
        base += [f'<path d="M79 42h134a38 38 0 010 76H79a38 38 0 010-76Z" {fill}/>',
                 f'<ellipse cx="79" cy="80" rx="38" ry="38" {line}/>',
                 f'<circle cx="79" cy="80" r="9" {line}/>', f'<path d="M213 80h64" {line}/>']
    elif cid in {"DRV-SPUR", "DRV-PINION"}:
        teeth = 20 if cid == "DRV-SPUR" else 14
        pts = []
        for i in range(teeth * 2):
            a = i * math.pi / teeth
            r = 55 if i % 2 == 0 else 48
            pts.append(f"{160+r*math.cos(a):.1f},{75+r*math.sin(a):.1f}")
        base += [f'<polygon points="{" ".join(pts)}" {fill}/>', f'<circle cx="160" cy="75" r="13" {line}/>']
    elif cid in {"DRV-BELT"}:
        base += [f'<circle cx="95" cy="76" r="38" {line}/>', f'<circle cx="230" cy="76" r="23" {line}/>',
                 f'<path d="M95 38L230 53M95 114L230 99" {line}/>',
                 '<text x="160" y="142" text-anchor="middle" fill="#91aaa6" font-size="11">pulley Ø / centres UNKNOWN</text>']
    elif cid in {"BRG-REAR", "BRG-FRONT"}:
        base += [f'<circle cx="160" cy="75" r="54" {fill}/>', f'<circle cx="160" cy="75" r="29" fill="var(--scan)" stroke="#34c9b9" stroke-width="3"/>']
    elif cid.startswith("SHK"):
        base += [f'<circle cx="69" cy="75" r="18" {line}/>', f'<circle cx="250" cy="75" r="18" {line}/>',
                 f'<rect x="88" y="58" width="82" height="34" rx="12" {fill}/>',
                 f'<path d="M170 75h61M102 51l12-13M122 51l12-13M142 51l12-13" {line}/>']
    elif cid.startswith("PWR-BAT"):
        base += [f'<rect x="65" y="35" width="175" height="88" rx="9" {fill}/>',
                 f'<path d="M240 55c27-8 25-25 48-24M240 78c25 0 27 11 48 11" {line}/>',
                 f'<rect x="280" y="22" width="23" height="20" {line}/>',
                 '<text x="152" y="84" text-anchor="middle" fill="#8fe0d7" font-size="16">2S LiPo</text>']
    elif cid.startswith("PWR-UBEC"):
        base += [f'<path d="M25 75h55M240 75h55" {line}/>', f'<rect x="80" y="49" width="160" height="52" rx="20" {fill}/>',
                 '<text x="160" y="80" text-anchor="middle" fill="#8fe0d7" font-size="14">UBEC 5 A</text>']
    elif cid.startswith("PWR-CAP"):
        base += [f'<ellipse cx="160" cy="35" rx="42" ry="17" {fill}/>', f'<path d="M118 35v68c0 23 84 23 84 0V35" {fill}/>',
                 f'<path d="M145 119v23M175 119v23" {line}/>']
    elif cid in {"PWR-XT60", "PWR-XT30"}:
        base += [f'<path d="M92 45h136l24 25-24 35H92L68 70Z" {fill}/>',
                 f'<circle cx="132" cy="75" r="13" {line}/>', f'<circle cx="188" cy="75" r="13" {line}/>']
    elif cid == "SNS-DIV":
        base += [f'<path d="M25 75h55l10-15 16 30 16-30 16 30 16-15h25l10-15 16 30 16-30 16 30 16-15h42" {line}/>']
    elif cid.startswith("CTL-E") or cid in {"VID-WIFI", "VID-HS", "AUD-AMP", "RX-ELRS", "PWR-BUZZ"}:
        base += [f'<rect x="55" y="28" width="210" height="95" rx="5" {fill}/>',
                 f'<rect x="105" y="51" width="72" height="50" {line}/>',
                 f'<rect x="221" y="59" width="44" height="35" {line}/>',
                 f'<path d="M69 38v74M84 38v74M191 38v74M206 38v74" stroke="#34c9b9" stroke-width="2" stroke-dasharray="3 4"/>']
    elif cid == "VID-ANT":
        base += [f'<path d="M45 106C95 106 92 45 142 45H275" {line}/>', f'<path d="M142 45v-24" {line}/>',
                 '<text x="185" y="132" text-anchor="middle" fill="#91aaa6" font-size="11">70 mm whip</text>']
    elif cid == "VID-CAM":
        base += [f'<rect x="58" y="37" width="150" height="85" rx="5" {fill}/>',
                 f'<circle cx="208" cy="79" r="45" {fill}/>', f'<circle cx="208" cy="79" r="24" {line}/>',
                 f'<circle cx="208" cy="79" r="8" fill="#34c9b9"/>']
    elif cid == "COOL-BLOW":
        base += [f'<rect x="91" y="22" width="138" height="110" rx="12" {fill}/>',
                 f'<circle cx="154" cy="77" r="44" {line}/>', f'<path d="M154 77c35-20 48 11 18 24-20 8-36-4-18-24Z" {fill}/>',
                 f'<path d="M229 83h60v37h-60" {line}/>']
    elif cid == "COOL-DUCT":
        base += [f'<path d="M45 44h75l105 24h50v45h-50L120 105H45Z" {fill}/>']
    elif cid.startswith("SRV-"):
        base += [f'<rect x="91" y="40" width="138" height="80" rx="6" {fill}/>',
                 f'<path d="M68 52h184v18H68ZM68 103h184v17H68Z" {fill}/>',
                 f'<circle cx="195" cy="40" r="25" {fill}/>', f'<circle cx="195" cy="40" r="9" {line}/>']
    elif cid == "AUD-SPK":
        base += [f'<circle cx="160" cy="75" r="61" {fill}/>', f'<circle cx="160" cy="75" r="42" {line}/>',
                 f'<circle cx="160" cy="75" r="13" {line}/>']
    elif cid == "LGT-LED":
        base += [f'<rect x="32" y="54" width="256" height="42" {fill}/>']
        for x in (66, 160, 254):
            base += [f'<rect x="{x-15}" y="60" width="30" height="30" {line}/>']
    elif cid.startswith("TYRE"):
        base += [f'<circle cx="160" cy="75" r="65" {fill}/>', f'<circle cx="160" cy="75" r="39" fill="var(--scan)" stroke="#34c9b9" stroke-width="3"/>',
                 f'<path d="M115 27l90 96M96 48l126 60M96 102l126-60" stroke="#34c9b9" opacity=".5"/>']
    elif cid == "KINGPIN":
        base += [f'<path d="M55 75h210" stroke="#34c9b9" stroke-width="16" stroke-linecap="round"/>']
    elif cid == "SNS-HALL":
        base += [f'<rect x="111" y="36" width="98" height="65" rx="5" {fill}/>',
                 f'<path d="M128 101v42M160 101v42M192 101v42" {line}/>']
    elif cid == "SNS-MAG":
        base += [f'<ellipse cx="160" cy="48" rx="61" ry="22" {fill}/>', f'<path d="M99 48v48c0 29 122 29 122 0V48" {fill}/>']
    else:
        base += [f'<path d="M62 111V52l42-24h155v58l-42 35H62Z" {fill}/>',
                 f'<path d="M62 52h155l42-24M217 52v69" {line}/>']
    base += [f'<text x="12" y="139" fill="#91aaa6" font-size="11">{esc(cid)} · TECHNICAL OUTLINE · NO STL</text>', "</svg>"]
    return "".join(base)


def gallery(components: list[dict]) -> str:
    cards = []
    for c in components:
        cc = conf_class(c["confidence"])
        if c["id"] in D.STL_SOURCES:
            visual = (
                f'<img src="{mesh_data_uri(c["id"])}" alt="{esc(c["name"])} real STL render">'
                '<span class="viewlabel">REAL STL · ISOMETRIC + ORTHOGRAPHIC · DEPTH-SORTED SAMPLE</span>'
            )
            visual_note = "Mesh silhouette VERIFIED; installed transform may remain ASSUMPTION."
        else:
            visual = technical_icon(c["id"]) + '<span class="viewlabel">NO CONTROLLED MESH · OUTLINE ONLY</span>'
            visual_note = "No STL exists for this hardware; outline is illustrative, not evidence."
        cards.append(f"""<article class="part">
<div class="partviz">{visual}</div><div class="partbody">
 <h3>{esc(c['name'])}</h3><span class="tag {cc}">{esc(c['confidence'])}</span>
 <div class="kv">
  <b>ID / qty</b><span>{esc(c['id'])} / {esc(c['qty'])}</span>
  <b>Measured dims</b><span>{esc(c['body'])}</span>
  <b>Installed</b><span>{esc(c['install'])}</span>
  <b>Mass</b><span>{esc(c['mass'])}</span>
 </div>
 <div class="evidence"><b>Visual:</b> {esc(visual_note)}<br>
 <b>Evidence:</b> <code>p0_d28_zone_component_envelopes.md</code>, row
 <code>{esc(c['id'])}</code> — {esc(c['source'])}</div>
</div></article>""")
    return '<div class="parts">' + "".join(cards) + "</div>"


def ruler(x: float, y: float, scale: float, length: int = 50) -> str:
    out = [f'<line class="tick" x1="{x}" y1="{y}" x2="{x+length*scale}" y2="{y}"/>']
    for mm in range(0, length + 1, 10):
        h = 9 if mm % 50 == 0 else 6
        out.append(f'<line class="tick" x1="{x+mm*scale}" y1="{y}" x2="{x+mm*scale}" y2="{y+h}"/>')
        out.append(f'<text class="tiny" x="{x+mm*scale}" y="{y+20}">{mm}</text>')
    out.append(f'<text class="small" x="{x}" y="{y-6}">{length} mm ruler · {scale:.1f} px/mm</text>')
    return "".join(out)


def dimline(x1: float, y1: float, x2: float, y2: float, label: str, conf: str = "documented") -> str:
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return (
        f'<line class="dim conf-{conf}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>'
        f'<rect x="{mx-4.2*len(label):.1f}" y="{my-16:.1f}" width="{8.4*len(label):.1f}" height="15" '
        f'fill="var(--paper)" opacity=".92"/><text class="small" text-anchor="middle" x="{mx:.1f}" y="{my-5:.1f}">{esc(label)}</text>'
    )


def _item_outline(kind: str, x: float, y: float, w: float, h: float, label: str) -> str:
    """SVG symbol in a projected bounding envelope."""
    cl = "conf-assumption"
    if kind in {"gear", "tyre", "magnet"}:
        r = min(w, h) / 2
        body = f'<circle class="{cl}" cx="{x+w/2:.1f}" cy="{y+h/2:.1f}" r="{r:.1f}"/>'
        if kind in {"gear", "tyre"}:
            body += f'<circle class="{cl}" cx="{x+w/2:.1f}" cy="{y+h/2:.1f}" r="{r*.58:.1f}"/>'
    elif kind == "shock":
        body = (f'<line class="{cl}" x1="{x:.1f}" y1="{y+h/2:.1f}" x2="{x+w:.1f}" y2="{y+h/2:.1f}"/>'
                f'<circle class="{cl}" cx="{x:.1f}" cy="{y+h/2:.1f}" r="{max(3,h*.25):.1f}"/>'
                f'<circle class="{cl}" cx="{x+w:.1f}" cy="{y+h/2:.1f}" r="{max(3,h*.25):.1f}"/>')
    elif kind == "belt":
        body = (f'<rect class="moving" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{min(w,h)*.35:.1f}"/>'
                f'<circle class="{cl}" cx="{x+w*.2:.1f}" cy="{y+h/2:.1f}" r="{min(w,h)*.22:.1f}"/>'
                f'<circle class="{cl}" cx="{x+w*.8:.1f}" cy="{y+h/2:.1f}" r="{min(w,h)*.16:.1f}"/>')
    elif kind in {"motor", "speaker", "blower"}:
        body = (f'<rect class="{cl}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{min(w,h)*.18:.1f}"/>'
                f'<circle class="{cl}" cx="{x+w/2:.1f}" cy="{y+h/2:.1f}" r="{min(w,h)*.34:.1f}"/>')
    elif kind == "led":
        body = f'<rect class="{cl}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/>'
        for q in (0.25, 0.75):
            body += f'<rect class="conf-documented" x="{x+w*q-5:.1f}" y="{y+h/2-5:.1f}" width="10" height="10"/>'
    else:
        body = f'<rect class="{cl}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3"/>'
        if kind in {"board", "servo", "camera", "battery"}:
            body += f'<rect class="conf-assumption" x="{x+w*.18:.1f}" y="{y+h*.2:.1f}" width="{w*.36:.1f}" height="{h*.38:.1f}"/>'
    return body + f'<text class="label" x="{x+3:.1f}" y="{max(12,y-5):.1f}">{esc(label)}</text>'


def plan_svg(zone: str) -> str:
    cfg = ZONE[zone]
    x0, x1 = cfg["xr"]
    l0, l1 = cfg["lr"]
    s, pad = PX, 52
    w, h = (x1 - x0) * s + 2 * pad, (l1 - l0) * s + 2 * pad + 42
    X = lambda x: pad + (x - x0) * s
    L = lambda l: pad + (l1 - l) * s
    floor = " ".join(f"{X(x):.1f},{L(l):.1f}" for x, l in FLOOR_PLAN)
    out = [f'<svg style="--drawing-w:{w:.0f}px" viewBox="0 0 {w:.1f} {h:.1f}" role="img" aria-label="{esc(cfg["code"])} plan view at 4 px per mm">',
           defs(), f'<rect width="{w:.1f}" height="{h:.1f}" fill="url(#grid)"/>',
           f'<polygon class="shell conf-derived" points="{floor}"/>',
           f'<line class="axis" x1="{X(x0):.1f}" y1="{L(0):.1f}" x2="{X(x1):.1f}" y2="{L(0):.1f}"/>',
           f'<text class="small" x="{X(x0)+5:.1f}" y="{L(0)-6:.1f}">L=0 · X+ → NOSE</text>']
    # Moving zones.
    if zone in {"power", "control"}:
        out += [f'<rect class="moving" x="{X(-80):.1f}" y="{L(22):.1f}" width="{180*s:.1f}" height="{44*s:.1f}"/>',
                f'<text class="badtext label" x="{X(-77):.1f}" y="{L(22)+16:.1f}">KO-01 STEERING · X−80…+100 · |L|≤22</text>']
    if zone == "suspension":
        for cx, cl in ((146.1, 75), (146.1, -75)):
            out += [f'<ellipse class="moving" cx="{X(cx):.1f}" cy="{L(cl):.1f}" rx="{35.3*s:.1f}" ry="{27.1*s:.1f}"/>',
                    f'<line class="conf-assumption" x1="{X(cx-32):.1f}" y1="{L(cl-15):.1f}" x2="{X(cx+32):.1f}" y2="{L(cl+15):.1f}"/>',
                    f'<line class="conf-assumption" x1="{X(cx-32):.1f}" y1="{L(cl+15):.1f}" x2="{X(cx+32):.1f}" y2="{L(cl-15):.1f}"/>']
    if zone in {"camera", "servos"}:
        out += [f'<ellipse class="moving" cx="{X(60):.1f}" cy="{L(0):.1f}" rx="{28*s:.1f}" ry="{30*s:.1f}"/>',
                f'<text class="small badtext" x="{X(63):.1f}" y="{L(0)-8:.1f}">GIMBAL SWEEP · ENDPOINTS UNKNOWN</text>']
    if zone == "servos":
        out += [f'<path class="moving" d="M{X(-125):.1f},{L(0):.1f} A{58*s:.1f},{58*s:.1f} 0 0 1 {X(-85):.1f},{L(40):.1f}"/>',
                f'<text class="small badtext" x="{X(-140):.1f}" y="{L(50):.1f}">DRS ARM SWEEP · 58 mm · ANGLE UNKNOWN</text>']
    if zone == "rear":
        out += [f'<rect class="moving" x="{X(-118):.1f}" y="{L(-36):.1f}" width="{36*s:.1f}" height="{12*s:.1f}" rx="12"/>',
                f'<text class="small badtext" x="{X(-118):.1f}" y="{L(-38):.1f}">BELT MOVING LOOP · PULLEY Ø UNKNOWN</text>']
    for cid, x, l, z, dx, dl, dz, kind, label in ITEMS[zone]:
        rx, ry, rw, rh = X(x - dx / 2), L(l + dl / 2), dx * s, dl * s
        out.append(_item_outline(kind, rx, ry, rw, rh, label))
    # Governing component dimensions: every orthographic view carries numeric
    # dimensions and an explicit confidence tag in addition to line styling.
    cid, x, l, z, dx, dl, dz, kind, label = ITEMS[zone][0]
    tag, line_conf = ITEM_DIM_CONF[zone]
    rx, ry, rw, rh = X(x - dx / 2), L(l + dl / 2), dx * s, dl * s
    ydim = min(h - 68, max(pad + 28, ry + rh + 19))
    xdim = min(w - 25, max(25, rx + rw + 17))
    out += [
        dimline(rx, ydim, rx + rw, ydim, f"{cid} X {dx:g} mm [{tag}]", line_conf),
        dimline(xdim, ry, xdim, ry + rh, f"L {dl:g} mm [{tag}]", line_conf),
    ]
    station = cfg["station"]
    out += [f'<line class="conf-derived" x1="{X(station):.1f}" y1="{L(l1):.1f}" x2="{X(station):.1f}" y2="{L(l0):.1f}"/>',
            f'<text class="accent label" x="{X(station)+5:.1f}" y="{L(l1)+15:.1f}">SECTION X={station:+.1f}</text>',
            ruler(pad, h-31, s, 50), "</svg>"]
    return "".join(out)


def side_svg(zone: str) -> str:
    cfg = ZONE[zone]
    x0, x1 = cfg["xr"]
    z0, z1 = -8, 88
    s, pad = PX, 52
    w, h = (x1 - x0) * s + 2 * pad, (z1 - z0) * s + 2 * pad + 42
    X = lambda x: pad + (x - x0) * s
    Z = lambda z: pad + (z1 - z) * s
    out = [f'<svg style="--drawing-w:{w:.0f}px" viewBox="0 0 {w:.1f} {h:.1f}" role="img" aria-label="{esc(cfg["code"])} side elevation at 4 px per mm">',
           defs(), f'<rect width="{w:.1f}" height="{h:.1f}" fill="url(#grid)"/>',
           f'<line class="floor" x1="{X(x0):.1f}" y1="{Z(0):.1f}" x2="{X(x1):.1f}" y2="{Z(0):.1f}"/>',
           f'<text class="small" x="{X(x0)+5:.1f}" y="{Z(0)+17:.1f}">DAT-F · Z=0</text>']
    # True longitudinal shell sections are handled in cross view; side keeps
    # the measured S0=0 centreline envelope visible as a derived reference.
    shell_a = [(-120, 52), (-100, 55), (-80, 58), (-60, 62), (-40, 65), (-20, 68), (0, 71), (20, 53)]
    shell_b = [(90, 42), (120, 42), (150, 37), (180, 20)]
    for pts in (shell_a, shell_b):
        out.append('<polyline class="shell conf-derived" points="' +
                   " ".join(f"{X(x):.1f},{Z(z):.1f}" for x, z in pts) + '"/>')
    if zone == "suspension":
        for cx in (D.REAR_AXLE_X, D.FRONT_AXLE_X):
            out += [f'<rect class="moving" x="{X(cx-32):.1f}" y="{Z(66):.1f}" width="{64*s:.1f}" height="{76*s:.1f}" rx="{32*s:.1f}"/>',
                    f'<circle class="conf-documented" cx="{X(cx):.1f}" cy="{Z(27):.1f}" r="{32*s:.1f}"/>',
                    f'<line class="dim conf-assumption" x1="{X(cx)+38:.1f}" y1="{Z(22):.1f}" x2="{X(cx)+38:.1f}" y2="{Z(34):.1f}"/>',
                    f'<text class="small" x="{X(cx)+45:.1f}" y="{Z(28):.1f}">centre Z22…34</text>']
    if zone in {"power", "control"}:
        out += [f'<rect class="moving" x="{X(-80):.1f}" y="{Z(38):.1f}" width="{180*s:.1f}" height="{16*s:.1f}"/>',
                f'<text class="badtext small" x="{X(-77):.1f}" y="{Z(35):.1f}">KO-01 · Z22…38</text>']
    if zone == "rear":
        out += [f'<rect class="moving" x="{X(-118):.1f}" y="{Z(45):.1f}" width="{36*s:.1f}" height="{35*s:.1f}" rx="24"/>']
    for cid, x, l, z, dx, dl, dz, kind, label in ITEMS[zone]:
        rx, ry, rw, rh = X(x - dx / 2), Z(z + dz), dx * s, dz * s
        side_kind = "tyre" if kind == "tyre" else ("gear" if kind == "gear" else kind)
        out.append(_item_outline(side_kind, rx, ry, rw, rh, label))
    cid, x, l, z, dx, dl, dz, kind, label = ITEMS[zone][0]
    tag, line_conf = ITEM_DIM_CONF[zone]
    rx, ry, rw, rh = X(x - dx / 2), Z(z + dz), dx * s, dz * s
    ydim = min(h - 68, max(pad + 28, ry + rh + 19))
    xdim = min(w - 25, max(25, rx + rw + 17))
    out += [
        dimline(rx, ydim, rx + rw, ydim, f"{cid} X {dx:g} mm [{tag}]", line_conf),
        dimline(xdim, ry, xdim, ry + rh, f"Z {dz:g} mm [{tag}]", line_conf),
    ]
    if zone == "rear":
        # ESC fan service plane.
        out += [f'<rect class="failure" x="{X(-81.5):.1f}" y="{Z(45.3):.1f}" width="{43*s:.1f}" height="{10*s:.1f}"/>',
                f'<text class="badtext label" x="{X(-80):.1f}" y="{Z(46):.1f}">C1/C2 · CURRENT ESC FAIL</text>']
    out += [ruler(pad, h-31, s, 50), "</svg>"]
    return "".join(out)


def load_shell() -> list:
    sh = REPO / "02_ready_to_slice/06_PLA_body_shell"
    front = K.load_stl(str(sh / "NEW BODY 2024 FRONT 1.stl"))
    rear = K.translate(K.load_stl(str(sh / "NEW BODY 2024 REAR.stl")), -67.47, 0, 0)
    return K.apply(front + rear, lambda v: (146.6 - v[0], -(v[1] - 1.855), v[2]))


class RayParity:
    """Chunked numpy Möller–Trumbore occupancy audit for transverse cuts.

    Projected L/Z bins keep each ray's triangle candidate list small.  Exterior
    empty cells are flood-filled from the grid boundary; remaining empty cells
    are enclosed holes/cavities.  The exact SVG boundary still comes from the
    triangle/plane intersection, while this independent parity audit verifies
    material-versus-void classification.
    """

    def __init__(self, triangles: list, cell: float = 2.0):
        self.triangles = np.asarray(triangles, dtype=np.float64)
        self.cell = cell
        self.bins: dict[tuple[int, int], list[int]] = {}
        t = self.triangles
        l0 = np.floor(t[:, :, 1].min(axis=1) / cell).astype(int)
        l1 = np.floor(t[:, :, 1].max(axis=1) / cell).astype(int)
        z0 = np.floor(t[:, :, 2].min(axis=1) / cell).astype(int)
        z1 = np.floor(t[:, :, 2].max(axis=1) / cell).astype(int)
        for i in range(len(t)):
            for li in range(l0[i], l1[i] + 1):
                for zi in range(z0[i], z1[i] + 1):
                    self.bins.setdefault((li, zi), []).append(i)
        self.cache: dict[float, dict] = {}

    def _inside(self, x: float, lateral: float, z: float) -> bool:
        ids = self.bins.get(
            (math.floor(lateral / self.cell), math.floor(z / self.cell)), ()
        )
        if not ids:
            return False
        tri = self.triangles[ids]
        v0 = tri[:, 0]
        edge1 = tri[:, 1] - v0
        edge2 = tri[:, 2] - v0
        # Möller–Trumbore with ray direction d=(1,0,0).
        h = np.column_stack(
            (np.zeros(len(ids), dtype=np.float64), -edge2[:, 2], edge2[:, 1])
        )
        a = np.sum(edge1 * h, axis=1)
        valid = np.abs(a) > 1e-10
        f = np.zeros_like(a)
        f[valid] = 1.0 / a[valid]
        offset = np.array([x, lateral, z]) - v0
        u = f * np.sum(offset * h, axis=1)
        q = np.cross(offset, edge1)
        v = f * q[:, 0]
        distance = f * np.sum(edge2 * q, axis=1)
        hits = distance[
            valid
            & (u >= 0.0)
            & (u <= 1.0)
            & (v >= 0.0)
            & ((u + v) <= 1.0)
            & (distance > 1e-7)
        ]
        if not len(hits):
            return False
        hits.sort()
        unique = int(np.count_nonzero(np.r_[True, np.diff(hits) > 1e-5]))
        return bool(unique % 2)

    def section(self, station: float) -> dict:
        key = round(station, 3)
        if key in self.cache:
            return self.cache[key]
        laterals = np.arange(-81.0, 82.0, self.cell)
        zs = np.arange(-4.0, 86.0, self.cell)
        occupied = np.zeros((len(zs), len(laterals)), dtype=bool)
        # Offset cell centres slightly to avoid shared mesh edges/vertices.
        for iz, z in enumerate(zs):
            for il, lateral in enumerate(laterals):
                occupied[iz, il] = self._inside(
                    station, lateral + 0.37, z + 0.41
                )
        exterior = np.zeros_like(occupied)
        queue: deque[tuple[int, int]] = deque()
        rows, cols = occupied.shape
        for r in range(rows):
            for c in (0, cols - 1):
                if not occupied[r, c] and not exterior[r, c]:
                    exterior[r, c] = True
                    queue.append((r, c))
        for c in range(cols):
            for r in (0, rows - 1):
                if not occupied[r, c] and not exterior[r, c]:
                    exterior[r, c] = True
                    queue.append((r, c))
        while queue:
            r, c = queue.popleft()
            for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if (
                    0 <= rr < rows
                    and 0 <= cc < cols
                    and not occupied[rr, cc]
                    and not exterior[rr, cc]
                ):
                    exterior[rr, cc] = True
                    queue.append((rr, cc))
        enclosed = (~occupied) & (~exterior)
        result = {
            "occupied": int(occupied.sum()),
            "enclosed": int(enclosed.sum()),
            "shape": occupied.shape,
        }
        self.cache[key] = result
        return result


def shell_path(tris: list, station: float, L, Z) -> str:
    segs = K.section(tris, "x", station)
    loops = [loop for loop in K.assemble_loops(segs, tol=.01) if K.loop_closed(loop, tol=.12)]
    paths = []
    for loop in loops:
        stride = max(1, len(loop) // 520)
        pts = loop[::stride]
        if pts[-1] != loop[-1]:
            pts.append(loop[-1])
        paths.append("M" + "L".join(f"{L(l):.1f},{Z(z):.1f}" for l, z in pts) + "Z")
    if paths:
        return '<path class="shellmat conf-verified" d="' + " ".join(paths) + '"/>'
    # Diagnostic fallback for a non-closed station; still uses real section segments.
    return "".join(
        f'<line class="shell conf-verified" x1="{L(a[0]):.1f}" y1="{Z(a[1]):.1f}" '
        f'x2="{L(b[0]):.1f}" y2="{Z(b[1]):.1f}"/>'
        for a, b in segs[::max(1, len(segs)//900)]
    )


def cross_svg(zone: str, shell_tris: list, parity: RayParity) -> str:
    cfg = ZONE[zone]
    l0, l1, z0, z1 = -82, 82, -5, 85
    s, pad = 5.0, 48
    w, h = (l1-l0)*s+2*pad, (z1-z0)*s+2*pad+42
    L = lambda l: pad + (l-l0)*s
    Z = lambda z: pad + (z1-z)*s
    station = cfg["station"]
    audit = parity.section(station)
    out = [f'<svg style="--drawing-w:{w:.0f}px" viewBox="0 0 {w:.1f} {h:.1f}" role="img" aria-label="True STL shell cross-section at X {station:+.1f}">',
           defs(), f'<rect width="{w:.1f}" height="{h:.1f}" fill="url(#grid)"/>',
           f'<desc>Chunked Möller–Trumbore 2 mm ray-parity audit: {audit["occupied"]} material cells; '
           f'{audit["enclosed"]} enclosed void cells after exterior flood fill.</desc>',
           shell_path(shell_tris, station, L, Z),
           f'<line class="floor" x1="{L(l0):.1f}" y1="{Z(0):.1f}" x2="{L(l1):.1f}" y2="{Z(0):.1f}"/>',
           f'<line class="conf-derived" x1="{L(0):.1f}" y1="{Z(z0):.1f}" x2="{L(0):.1f}" y2="{Z(z1):.1f}"/>',
           f'<text class="label accent" x="{L(l0)+5:.1f}" y="{Z(z1)+16:.1f}">REAL SHELL STL SECTION · X={station:+.1f} · S0=0 LOWER BOUND</text>',
           f'<text class="tiny" x="{L(32):.1f}" y="{Z(z1)+16:.1f}">MT PARITY 2 mm · {audit["occupied"]} material / {audit["enclosed"]} enclosed-void cells</text>',
           f'<text class="small" x="{L(1):.1f}" y="{Z(2):.1f}">L=0</text>']
    if zone == "rear":
        x, y, ww, hh = L(-43.4), Z(35.3), 36.8*s, 32.3*s
        out += [f'<rect class="conf-assumption" x="{x:.1f}" y="{y:.1f}" width="{ww:.1f}" height="{hh:.1f}"/>',
                f'<rect class="failure" x="{L(-43.4):.1f}" y="{Z(45.3):.1f}" width="{23.4*s:.1f}" height="{26.3*s:.1f}"/>',
                f'<line class="dim conf-documented" x1="{L(-47):.1f}" y1="{Z(3):.1f}" x2="{L(-47):.1f}" y2="{Z(35.3):.1f}"/>',
                f'<text class="badtext label" x="{L(-80):.1f}" y="{Z(48):.1f}">C1/C2 FAIL · body Z35.3 · fan plane Z45.3</text>',
                f'<text class="small" x="{L(-80):.1f}" y="{Z(43):.1f}">shell ≈19 @|L|30–40; width 17 @Z45</text>']
    elif zone == "power":
        out += [f'<rect class="conf-assumption" x="{L(2.5):.1f}" y="{Z(28):.1f}" width="{45*s:.1f}" height="{25*s:.1f}"/>',
                f'<rect class="moving" x="{L(-22):.1f}" y="{Z(38):.1f}" width="{44*s:.1f}" height="{16*s:.1f}"/>',
                f'<rect class="failure" x="{L(2.5):.1f}" y="{Z(28):.1f}" width="{19.5*s:.1f}" height="{6*s:.1f}"/>',
                f'<rect class="failure" x="{L(40):.1f}" y="{Z(28):.1f}" width="{7.5*s:.1f}" height="{4*s:.1f}"/>',
                f'<text class="badtext label" x="{L(-78):.1f}" y="{Z(45):.1f}">C1 −1…−4 mm SHELL · C2 KO-01 OVERLAP Z22…28</text>']
    elif zone == "control":
        out += [f'<rect class="conf-assumption" x="{L(-46):.1f}" y="{Z(33):.1f}" width="{28*s:.1f}" height="{13*s:.1f}"/>',
                f'<path class="failure" d="M{L(-46):.1f},{Z(33):.1f}H{L(-30):.1f}V{Z(26):.1f}H{L(-46):.1f}Z"/>',
                dimline(L(-20), Z(33), L(-20), Z(39), "C1 +6 raw", "derived"),
                dimline(L(-30), Z(33), L(-30), Z(26), "C2 −7 fail", "derived")]
    elif zone in {"camera", "servos"}:
        out += [f'<rect class="conf-assumption" x="{L(-22.5):.1f}" y="{Z(80):.1f}" width="{45*s:.1f}" height="{60*s:.1f}"/>',
                f'<rect class="moving" x="{L(-30):.1f}" y="{Z(85):.1f}" width="{60*s:.1f}" height="{70*s:.1f}" rx="18"/>',
                f'<text class="badtext label" x="{L(-75):.1f}" y="{Z(78):.1f}">C1/C2 · FOV + GIMBAL SWEEP · CAMERA BODY / ENDPOINTS UNKNOWN</text>']
    elif zone == "audio":
        out += [f'<circle class="conf-assumption" cx="{L(43):.1f}" cy="{Z(9):.1f}" r="{20*s:.1f}"/>',
                dimline(L(43), Z(15), L(43), Z(25.5), "C1 raw +9…12", "derived"),
                f'<text class="goodtext label" x="{L(-74):.1f}" y="{Z(42):.1f}">C2 PROVISIONAL · +4…7 mm AFTER 5 mm POLICY</text>']
    elif zone == "suspension":
        for lateral in (-75, 75):
            out += [f'<circle class="conf-documented" cx="{L(lateral):.1f}" cy="{Z(27):.1f}" r="{32*s:.1f}"/>',
                    f'<circle class="moving" cx="{L(lateral):.1f}" cy="{Z(27):.1f}" r="{35.5*s:.1f}"/>']
        out += [f'<text class="badtext label" x="{L(-78):.1f}" y="{Z(80):.1f}">C1 FRONT ARCH ≈3.5 mm · BELOW 8 mm GENERAL MOVING POLICY</text>']
    elif zone == "sensors":
        out += [f'<line class="axis" x1="{L(-58):.1f}" y1="{Z(27):.1f}" x2="{L(10):.1f}" y2="{Z(27):.1f}"/>',
                f'<circle class="moving" cx="{L(-25):.1f}" cy="{Z(27):.1f}" r="{3*s:.1f}"/>',
                f'<rect class="conf-assumption" x="{L(-31):.1f}" y="{Z(28.6):.1f}" width="{4.17*s:.1f}" height="{1.57*s:.1f}"/>',
                f'<text class="badtext label" x="{L(-78):.1f}" y="{Z(45):.1f}">C1/C2 · 1.5 TARGET · 1–3 mm SWITCH BAND</text>']
    cid, x, l, z, dx, dl, dz, kind, label = ITEMS[zone][0]
    tag, line_conf = ITEM_DIM_CONF[zone]
    out += [
        dimline(
            L(l - dl / 2), h - 70, L(l + dl / 2), h - 70,
            f"{cid} L {dl:g} mm [{tag}]", line_conf,
        ),
        dimline(
            min(w - 34, L(l + dl / 2) + 20), Z(z),
            min(w - 34, L(l + dl / 2) + 20), Z(z + dz),
            f"Z {dz:g} mm [{tag}]", line_conf,
        ),
    ]
    out += [ruler(pad, h-31, s, 50), "</svg>"]
    return "".join(out)


def callout_table(zone: str) -> str:
    rows = []
    for cid, interface, demand, evidence, verdict, conf in CLEARANCES[zone]:
        result_class = "result-fail" if any(k in verdict for k in ("FAIL", "RISK")) else (
            "result-pass" if "PASS" in verdict else ""
        )
        rows.append(
            f"<tr><td><code>{cid}</code></td><td>{esc(interface)}</td><td>{esc(demand)}</td>"
            f"<td>{esc(evidence)}</td><td class=\"{result_class}\">{esc(verdict)}</td>"
            f"<td><span class=\"tag {conf_class(conf)}\">{esc(conf)}</span></td></tr>"
        )
    return """<div class="tablewrap"><table><thead><tr><th>Callout</th><th>Interface</th>
<th>Required / occupant</th><th>Measured evidence</th><th>Verdict</th><th>Confidence</th>
</tr></thead><tbody>""" + "".join(rows) + "</tbody></table></div>"


def detail_frame(width: int, height: int, title: str) -> list[str]:
    return [f'<svg style="--drawing-w:{width}px" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">',
            defs(), f'<rect width="{width}" height="{height}" fill="url(#grid)"/>']


def rear_detail() -> str:
    s = 7.0
    out = detail_frame(1220, 500, "48 pitch gear mesh, belt loop and motor interface")
    cx, cy = 230, 250
    r1, r2, centre = 39.69/2*s, 14.82/2*s, 27.25*s
    out += [
        '<text class="accent label" x="25" y="28">ZR HARD INTERFACE · 48P GEAR MESH · 7 px/mm</text>',
        f'<circle class="conf-derived" cx="{cx}" cy="{cy}" r="{r1}"/>',
        f'<circle class="conf-derived" cx="{cx+centre}" cy="{cy}" r="{r2}"/>',
        f'<circle class="conf-documented" cx="{cx}" cy="{cy}" r="{40.75/2*s}"/>',
        f'<circle class="conf-documented" cx="{cx+centre}" cy="{cy}" r="{15.88/2*s}"/>',
        f'<circle class="conf-assumption" cx="{cx}" cy="{cy}" r="20"/>',
        f'<circle class="conf-assumption" cx="{cx+centre}" cy="{cy}" r="14"/>',
        dimline(cx, 430, cx+centre, 430, "27.25 mm pitch centres", "derived"),
        '<text class="label" x="65" y="92">75T · pitch Ø39.69 · outside Ø40.75</text>',
        '<text class="label" x="350" y="167">28T · pitch Ø14.82 · outside Ø15.88</text>',
        '<text class="badtext label" x="52" y="468">BACKLASH / SHAFT / HUB / BOLT PCD = UNKNOWN</text>',
        '<line class="axis" x1="555" y1="70" x2="555" y2="450"/>',
        '<text class="accent label" x="585" y="28">BELT LOOP · INSTALLATION ENVELOPE</text>',
        '<circle class="conf-assumption" cx="700" cy="230" r="70"/>',
        '<circle class="conf-assumption" cx="970" cy="270" r="45"/>',
        '<path class="moving" d="M700 160L970 225A45 45 0 010 90L700 300A70 70 0 010-140Z"/>',
        '<text class="label" x="635" y="105">140 mm belt length · DOCUMENTED</text>',
        '<text class="badtext label" x="835" y="370">pulley teeth / OD / bores / planes = UNKNOWN</text>',
        f'<circle class="conf-documented" cx="1110" cy="205" r="{36/2*5}"/>',
        f'<rect class="conf-assumption" x="{1110-18*5-8}" y="112" width="{36*5+16}" height="{36*5+16}" rx="55"/>',
        '<text class="label" x="1030" y="335">motor Ø36</text>',
        '<text class="badtext small" x="1012" y="353">slot coordinate / fasteners UNKNOWN</text>',
        ruler(610, 455, 5, 50), "</svg>",
    ]
    return "".join(out)


def power_detail(summary: dict) -> str:
    mid, high = summary["mid"], summary["high_pod"]
    out = detail_frame(1260, 650, "ESC failure, battery architecture and CG balance")
    out += [
        '<text class="accent label" x="24" y="28">ZP HARD INTERFACE · ESC SEARCH + SINGLE PACK + MASS/BALANCE</text>',
        '<text class="label" x="30" y="62">CURRENT ESC SIDE PLACEMENT · X−60/L−25 · ASSUMPTION transform</text>',
        '<path class="shell conf-verified" d="M45 222L110 132L190 88L270 132L345 222"/>',
        '<line class="floor" x1="35" y1="300" x2="355" y2="300"/>',
        '<rect class="conf-assumption" x="54" y="138" width="184" height="162"/>',
        '<rect class="failure" x="54" y="73" width="125" height="129"/>',
        '<text class="badtext label" x="45" y="330">FAIL · 43×36.8×32.3 + 10 fan plane</text>',
        '<text class="small" x="45" y="350">body top Z35.3; fan plane Z45.3; shell ≈19 outboard</text>',
        '<g transform="translate(410,50)"><rect class="conf-assumption" x="0" y="50" width="215" height="184"/>'
        '<text class="label" x="0" y="22">ALT A · CENTRELINE SEARCH</text><text class="badtext small" x="0" y="252">COORDINATE / WIRE EXITS / FAN GAP UNSET</text></g>',
        '<g transform="translate(680,50)"><rect class="conf-assumption" x="0" y="68" width="162" height="215"/>'
        '<text class="label" x="0" y="22">ALT B · ROTATION SEARCH</text><text class="badtext small" x="0" y="302">ORIENTATION + COORDINATE UNSET</text></g>',
        '<line class="axis" x1="885" y1="50" x2="885" y2="365"/>',
        '<rect class="conf-documented" x="925" y="86" width="225" height="135" rx="8"/>',
        '<rect class="conf-assumption" x="895" y="65" width="285" height="180" rx="10"/>',
        '<text class="label" x="945" y="146">ONE ACTIVE PACK</text>',
        '<text class="small" x="945" y="166">body ≤75×45×25</text>',
        '<text class="small" x="915" y="272">allocation 95×50×30 incl. XT60/strap</text>',
        '<path class="failure" d="M925 221h135v44H925Z"/>',
        '<text class="badtext small" x="925" y="288">current shoulder / KO-01 fails</text>',
        '<text class="label" x="925" y="325">PACK 2 = OFF-CAR SWAP</text>',
        '<text class="small" x="925" y="345">dual-onboard rejected provisionally</text>',
        '<line class="axis" x1="25" y1="390" x2="1235" y2="390"/>',
        '<text class="accent label" x="28" y="420">WHOLE-CAR BALANCE · p0_d30 midpoint ledger · ASSUMPTION masses/positions</text>',
        '<rect x="90" y="470" width="385" height="42" fill="var(--accent)" opacity=".75"/>',
        '<rect x="475" y="470" width="715" height="42" fill="var(--ground)" stroke="var(--line)"/>',
        f'<text class="label" x="235" y="497">FRONT {mid[4]:.1f}%</text>',
        f'<text class="label" x="760" y="497">REAR {100-mid[4]:.1f}%</text>',
        f'<text class="label" x="90" y="545">cockpit midpoint: X-CG {mid[1]:+.1f} · L-CG {mid[2]:+.1f} · Z-CG {mid[3]:.1f} mm</text>',
        f'<text class="label" x="90" y="570">camera-pod case: {high[4]:.1f}% front · Z-CG {high[3]:.1f} mm</text>',
        '<text class="badtext label" x="90" y="600">battery ±10 mm → whole-car X-CG only ≈0.6 mm</text>',
        '<text class="small" x="90" y="623">Target 36–40% front is ASSUMPTION; D-39/ASM-58 corner scales own the result.</text>',
        ruler(930, 600, 4, 50), "</svg>",
    ]
    return "".join(out)


def control_detail() -> str:
    out = detail_frame(1160, 500, "Control deck shell limiter and RF routing")
    out += [
        '<text class="accent label" x="24" y="28">ZC HARD INTERFACE · DECK SHOULDER + RF ROUTES</text>',
        '<line class="floor" x1="45" y1="390" x2="500" y2="390"/>',
        '<path class="shell conf-verified" d="M50 295L165 115L275 50L385 115L495 295"/>',
        '<rect class="conf-assumption" x="115" y="225" width="280" height="65"/>',
        '<line class="dim conf-derived" x1="205" y1="225" x2="205" y2="195"/>',
        '<text class="goodtext label" x="130" y="180">C1 · +6 mm RAW @|L|20</text>',
        '<path class="failure" d="M350 225h45v70h-45Z"/>',
        '<text class="badtext label" x="300" y="325">C2 · −7 mm @|L|30</text>',
        '<text class="small" x="95" y="420">board top Z≈33 · S0=0 shell 39 @20 / 26 @30</text>',
        '<line class="axis" x1="540" y1="45" x2="540" y2="455"/>',
        '<circle class="conf-documented" cx="650" cy="310" r="26"/>',
        '<path class="conf-assumption" d="M650 310C700 230 748 190 805 170"/>',
        '<line class="conf-documented" x1="805" y1="170" x2="805" y2="105"/>',
        '<text class="label" x="590" y="352">RP1 · 13×11×3</text>',
        '<text class="label" x="785" y="92">65 mm T antenna</text>',
        '<rect class="conf-assumption" x="880" y="248" width="180" height="96"/>',
        '<path class="conf-assumption" d="M970 248C1030 172 1060 118 1080 55"/>',
        '<path class="conf-assumption" d="M970 248C920 170 900 112 890 55"/>',
        '<text class="label" x="880" y="370">Wi-Fi ≤60×32×12 + HS</text>',
        '<text class="label" x="850" y="42">70 mm video whips ×2</text>',
        dimline(805, 440, 970, 440, "≥150 mm inter-system target", "assumption"),
        '<text class="small" x="620" y="472">U.FL bend ≥10 mm · conductive-mass target ≥20 mm · both routes physically gated</text>',
        ruler(565, 52, 5, 50), "</svg>",
    ]
    return "".join(out)


def camera_detail() -> str:
    out = detail_frame(1160, 520, "Camera FOV, airflow, service and identity conflict")
    out += [
        '<text class="accent label" x="24" y="28">ZV HARD INTERFACE · OPTICS / AIRFLOW / SERVICE</text>',
        '<rect class="conf-assumption" x="105" y="205" width="165" height="115"/>',
        '<circle class="conf-assumption" cx="270" cy="260" r="52"/>',
        '<path class="conf-assumption" d="M322 240L610 105V415L322 280Z"/>',
        '<path class="moving" d="M275 260A95 95 0 010 190A95 95 0 010 140"/>',
        '<text class="badtext label" x="365" y="95">FOV ANGLE = UNKNOWN · SENSOR/LENS TO MEASURE</text>',
        '<text class="label" x="115" y="345">SSC338Q board/heatsink/lens</text>',
        '<text class="small" x="115" y="365">body / holes / cable exits TO MEASURE</text>',
        '<path class="conf-documented" d="M320 205h25M320 315h25"/>',
        '<text class="label" x="348" y="214">C1 ≥5 mm fixed</text>',
        '<text class="label" x="348" y="322">C2 ≥8 mm horn/link</text>',
        '<rect class="conf-documented" x="690" y="125" width="120" height="120" rx="12"/>',
        '<circle class="conf-documented" cx="750" cy="185" r="42"/>',
        '<path class="conf-assumption" d="M810 175h150v60H810Z"/>',
        '<path d="M655 185h35M960 205h120" stroke="var(--accent2)" stroke-width="5" marker-end="url(#arrow)"/>',
        '<text class="label" x="682" y="105">20 mm face blower</text>',
        '<text class="small" x="675" y="275">thickness/outlet TO MEASURE</text>',
        '<text class="label" x="842" y="160">duct defaults 20×8 / 18 transition</text>',
        '<text class="badtext small" x="842" y="255">recirculation / blocked inlet = FAIL</text>',
        '<rect class="failure" x="690" y="340" width="405" height="105" rx="10"/>',
        '<text class="badtext" x="715" y="375" font-size="18">UNRESOLVED IDENTITY</text>',
        '<text class="label" x="715" y="405">user / frozen BOM: IMX415</text>',
        '<text class="label" x="715" y="428">repo camera stack: IMX335</text>',
        '<text class="badtext label" x="65" y="475">NO AUTHORIZED CAMERA PRINT · D-34/ASM-53 MUST CLOSE FIRST</text>',
        ruler(85, 410, 5, 50), "</svg>",
    ]
    return "".join(out)


def servo_detail() -> str:
    out = detail_frame(1180, 520, "Gimbal and DRS moving envelopes")
    out += [
        '<text class="accent label" x="24" y="28">ZA HARD INTERFACE · THREE MG90S + MOVING ENVELOPES</text>',
        '<rect class="conf-documented" x="95" y="210" width="137" height="73" rx="7"/>',
        '<circle class="conf-assumption" cx="205" cy="210" r="20"/>',
        '<line class="conf-assumption" x1="205" y1="210" x2="295" y2="210"/>',
        '<path class="moving" d="M205 120A90 90 0 010 180A90 90 0 010 300"/>',
        '<text class="label" x="70" y="318">pan MG90S · 22.8×12.2×28.5</text>',
        '<text class="badtext label" x="75" y="345">C1 horn reserve r=15 mm · ASSUMPTION</text>',
        '<rect class="conf-assumption" x="340" y="120" width="270" height="225"/>',
        '<path class="moving" d="M475 145A95 95 0 010 205A95 95 0 010 320"/>',
        '<path class="moving" d="M380 235A95 70 0 010 570 235"/>',
        '<text class="label" x="360" y="105">gimbal reserve 55×45×60</text>',
        '<text class="badtext small" x="360" y="370">pan/tilt endpoints + camera body UNKNOWN · C2 ≥8 mm</text>',
        '<line class="axis" x1="650" y1="45" x2="650" y2="455"/>',
        '<rect class="conf-documented" x="705" y="235" width="137" height="73" rx="7"/>',
        '<circle class="conf-assumption" cx="815" cy="235" r="20"/>',
        '<line class="conf-assumption" x1="815" y1="235" x2="1105" y2="235"/>',
        '<line class="conf-assumption" x1="815" y1="235" x2="1015" y2="90"/>',
        '<line class="conf-assumption" x1="815" y1="235" x2="1015" y2="380"/>',
        '<path class="moving" d="M1015 90A250 250 0 010 1015 380"/>',
        dimline(815, 430, 1105, 430, "58 mm DRS arm", "verified"),
        '<text class="badtext label" x="700" y="472">C3 sweep angle / linkage / pocket UNKNOWN · ≥8 mm static</text>',
        ruler(70, 455, 6, 50), "</svg>",
    ]
    return "".join(out)


def audio_detail() -> str:
    out = detail_frame(1160, 500, "Speaker clearance and LED lens segmentation")
    out += [
        '<text class="accent label" x="24" y="28">ZL HARD INTERFACE · SPEAKER PORT + PIXEL/LENS SEGMENTATION</text>',
        '<path class="shell conf-verified" d="M60 120L210 65L370 115L480 245"/>',
        '<line class="floor" x1="50" y1="355" x2="500" y2="355"/>',
        '<ellipse class="conf-assumption" cx="330" cy="295" rx="100" ry="60"/>',
        '<line class="dim conf-derived" x1="330" y1="235" x2="330" y2="185"/>',
        '<text class="goodtext label" x="150" y="175">C1 RAW +9…12 mm</text>',
        '<text class="goodtext label" x="150" y="198">C2 +4…7 mm after 5 mm static policy</text>',
        '<path class="moving" d="M235 275h190v35H235Z"/>',
        '<text class="badtext small" x="245" y="326">C3 cone/port ≥3 mm · speaker TO MEASURE</text>',
        '<line class="axis" x1="540" y1="45" x2="540" y2="455"/>',
        '<rect class="conf-assumption" x="600" y="120" width="480" height="80"/>',
        '<rect class="conf-documented" x="650" y="135" width="50" height="50"/>',
        '<rect class="conf-documented" x="850" y="135" width="50" height="50"/>',
        '<rect class="conf-documented" x="1050" y="135" width="50" height="50"/>',
        dimline(675, 230, 875, 230, "33.33 mm pixel pitch", "documented"),
        dimline(675, 275, 1075, 275, "≈66.7 mm two-pixel run", "assumption"),
        '<text class="label" x="600" y="320">proposed: centre brake/rain ×1 · indicators ×2/side · halo ×2</text>',
        '<text class="badtext label" x="600" y="350">lens optical coverage / cut pads / wire exits = UNKNOWN</text>',
        '<text class="small" x="600" y="378">Only rear diffuser bbox is VERIFIED; transform and every LED segment remain ASSUMPTION.</text>',
        '<path class="moving" d="M850 395h235v48H850Z"/>',
        '<text class="badtext small" x="870" y="425">C4 ≥8 mm from DRS / shock / belt</text>',
        ruler(595, 455, 6, 50), "</svg>",
    ]
    return "".join(out)


def suspension_detail() -> str:
    out = detail_frame(1260, 540, "Tyre arch, steer bump and shock conflict")
    out += [
        '<text class="accent label" x="24" y="28">ZS HARD INTERFACE · Ø64 F104 TYRES THROUGH BODY-ON MOTION</text>',
        '<circle class="conf-documented" cx="190" cy="265" r="160"/>',
        '<circle class="shell conf-derived" cx="190" cy="265" r="177.5"/>',
        dimline(190, 80, 190, 97.5, "≈3.5 mm FRONT", "derived"),
        '<text class="badtext label" x="75" y="470">C1 HIGH RISK · below 8 mm general moving policy</text>',
        '<circle class="conf-documented" cx="535" cy="265" r="160"/>',
        '<circle class="shell conf-derived" cx="535" cy="265" r="180"/>',
        dimline(535, 77, 535, 97, "≈4 mm REAR", "derived"),
        '<text class="badtext label" x="430" y="470">C2 HIGH RISK · full rear bump required</text>',
        '<line class="axis" x1="730" y1="45" x2="730" y2="500"/>',
        '<ellipse class="moving" cx="870" cy="235" rx="176.5" ry="135.5"/>',
        '<rect class="conf-documented" x="710" y="160" width="320" height="150" transform="rotate(25 870 235)"/>',
        dimline(693.5, 390, 1046.5, 390, "X half-envelope 35.3 mm", "derived"),
        dimline(1100, 99.5, 1100, 370.5, "L half-envelope 27.1 mm", "derived"),
        '<text class="small" x="770" y="430">±25° steer is ASSUMPTION · tyre body Ø64×30 DOCUMENTED</text>',
        '<line class="dim conf-assumption" x1="1170" y1="195" x2="1170" y2="315"/>',
        '<text class="badtext small" x="1120" y="345">C4 centre Z22…34</text>',
        '<rect class="failure" x="760" y="465" width="420" height="50" rx="8"/>',
        '<text class="badtext label" x="785" y="496">C5 SHOCK CONFLICT · 51 mm requirement / 52 mm stock label</text>',
        ruler(755, 60, 5, 50), "</svg>",
    ]
    return "".join(out)


def sensor_detail() -> str:
    s = 40.0
    out = detail_frame(1080, 500, "A3144 Hall switching gap band")
    out += [
        '<text class="accent label" x="24" y="28">ZH HARD INTERFACE · 40 px/mm LOCAL GAP DETAIL</text>',
        '<circle class="moving" cx="185" cy="250" r="120"/>',
        '<rect class="conf-documented" x="165" y="205" width="40" height="120"/>',
        '<text class="label" x="100" y="390">Ø3×1 magnet · one pulse/rev</text>',
        f'<rect class="conf-documented" x="{205+1.5*s}" y="{250-1.57/2*s}" width="{4.17*s}" height="{1.57*s}"/>',
        f'<rect class="moving" x="{205+1*s}" y="{250-1.57/2*s-20}" width="{2*s}" height="{1.57*s+40}"/>',
        dimline(205, 145, 205+1.5*s, 145, "1.5 mm TARGET", "assumption"),
        dimline(205+1*s, 365, 205+3*s, 365, "1–3 mm SWITCH BAND", "assumption"),
        '<text class="badtext label" x="475" y="205">C1/C2 · PHYSICAL SPIN TEST REQUIRED</text>',
        '<text class="small" x="475" y="232">A3144 max body 4.17×3.10×1.57 · DOCUMENTED</text>',
        '<text class="small" x="475" y="255">shaft/collar runout, magnetic polarity/field and hot geometry UNKNOWN</text>',
        '<rect class="conf-assumption" x="660" y="285" width="260" height="70" rx="7"/>',
        '<line class="dim conf-assumption" x1="620" y1="320" x2="660" y2="320"/>',
        '<text class="label" x="585" y="305">C3 ≥2 mm bracket/collar</text>',
        '<path class="moving" d="M660 405h260v50H660Z"/>',
        '<text class="badtext label" x="690" y="436">C4 ≥8 mm to belt / spur / wheel</text>',
        ruler(475, 420, 10, 20), "</svg>",
    ]
    return "".join(out)


def detail_svg(zone: str, summary: dict) -> str:
    return {
        "rear": rear_detail,
        "power": lambda: power_detail(summary),
        "control": control_detail,
        "camera": camera_detail,
        "servos": servo_detail,
        "audio": audio_detail,
        "suspension": suspension_detail,
        "sensors": sensor_detail,
    }[zone]()


def placement_table(zone: str) -> str:
    rows = []
    for p in D.PLACEMENTS:
        if p["zone"] != zone:
            continue
        cc = conf_class(p["confidence"])
        rows.append(
            f"<tr><td><code>{esc(p['id'])}</code></td><td>{esc(p['x'])}</td>"
            f"<td>{esc(p['l'])}</td><td>{esc(p['z'])}</td><td>{esc(p['orientation'])}</td>"
            f"<td><span class=\"tag {cc}\">{esc(p['confidence'])}</span></td><td>{esc(p['note'])}</td></tr>"
        )
    return """<div class="tablewrap"><table><thead><tr><th>ID</th><th>X mm</th><th>L mm</th>
<th>Z mm</th><th>Orientation</th><th>Confidence</th><th>Gate note</th></tr></thead>
<tbody>""" + "".join(rows) + "</tbody></table></div>"


def confidence_legend() -> str:
    return """<div class="legend">
 <span><i class="swatch"></i>VERIFIED · solid · measured mesh/physical evidence</span>
 <span><i class="swatch derived"></i>DERIVED · thin · arithmetic/registration</span>
 <span><i class="swatch documented"></i>DOCUMENTED · dotted · controlled reference</span>
 <span><i class="swatch assumption"></i>ASSUMPTION · dashed + hatched · physically open</span>
</div><p class="sub mono">VERIFIED / DERIVED / DOCUMENTED / ASSUMPTION — line style follows the weakest fact being shown.</p>"""


def zone_page(
    zone: str,
    components: list[dict],
    shell_tris: list,
    parity: RayParity,
    summary: dict,
) -> str:
    meta, cfg = D.ZONE_META[zone], ZONE[zone]
    page = page_start(f"{cfg['code']} · {meta['title']}", meta["summary"])
    page += f"""
<p class="eyebrow">{esc(cfg['code'])} · assembly zone · datum X+ forward / L lateral / Z+ up</p>
<h1>{esc(meta['title'])}</h1>
<p class="lede">{esc(cfg['status'])} Governing fit gate: <b>{esc(cfg['governor'])}</b></p>
<div class="status {esc(cfg['tone'])}"><span class="flag">{'✕ BUILD RISK' if cfg['tone']=='fail' else '⚠ OPEN GATE'}</span>
 <span><b>{esc(cfg['gate'])}</b> — production geometry remains stopped. S0=0 sections are measured lower bounds; add only a physically measured S0.</span></div>
<div class="meta">
 <div class="chip"><b>Governing station</b>X={cfg['station']:+.1f} mm · true shell STL section</div>
 <div class="chip"><b>Drawing scale</b>plan/side 4.0 px/mm · section 5.0 px/mm · details ≥5 px/mm</div>
 <div class="chip"><b>Evidence cells</b>D-28 rows + D-29 coordinates + D-02 station + D-31 gate</div>
 <div class="chip"><b>Legacy note</b>supersedes the old 1.6 px/mm schematic pages</div>
</div>
<div class="board"><h2>Orthographic plan</h2><p class="sub">Candidate installation envelopes and moving keep-outs; scroll horizontally without shrinking below 4 px/mm.</p>
 <div class="drawing">{plan_svg(zone)}</div></div>
<div class="board"><h2>Orthographic side elevation</h2><p class="sub">DAT-F floor, S0=0 shell reference and Z-direction motion/service envelopes.</p>
 <div class="drawing">{side_svg(zone)}</div></div>
<div class="board"><h2>Governing transverse cross-section</h2><p class="sub">Actual registered shell triangle section — curved shoulders/spine and holes preserved; occupant transforms remain visibly dashed.</p>
 <div class="drawing">{cross_svg(zone, shell_tris, parity)}</div></div>
<div class="board"><h2>Confidence legend</h2>{confidence_legend()}</div>
<div class="board"><h2>Hard-interface detail inset</h2><p class="sub">Numeric interface detail at enlarged scale. UNKNOWN remains UNKNOWN; hatched regions are moving, unresolved or failing.</p>
 <div class="drawing">{detail_svg(zone, summary)}</div></div>
<div class="board"><h2>Clearance callouts</h2><p class="sub">The C1…C5 identifiers mirror the labels drawn above.</p>{callout_table(zone)}</div>
<div class="board"><h2>Datum placement register</h2><p class="sub">Exact D-29 rows; OFF-CAR and TBD values are intentionally not converted into coordinates.</p>{placement_table(zone)}</div>
<div class="board"><h2>Per-part evidence gallery</h2><p class="sub">Every component is visually distinct. STL-backed parts use real dual-view silhouettes; non-mesh hardware uses labelled technical outlines only.</p>
 {gallery(components)}</div>
<div class="note"><b>Source chain:</b> <a href="../fit_studies/{esc(meta['study'])}">{esc(meta['study'])}</a> →
 <code>p0_d28_zone_component_envelopes.md</code> / <code>p0_d29_zone_placements.csv</code> /
 <code>p0_d31_fit_gates.md</code>. Shell geometry: <code>p0_d02_d03_d04_clearance.md</code>,
 station X={cfg['station']:+.1f}; body meshes remain read-only.</div>
"""
    return page + page_end()


def overview_svg(summary: dict) -> str:
    s, x0, x1, l0, l1, pad = 4.0, -145, 185, -105, 105, 55
    w, h = (x1-x0)*s+2*pad, (l1-l0)*s+2*pad+70
    X = lambda x: pad+(x-x0)*s
    L = lambda l: pad+(l1-l)*s
    floor = " ".join(f"{X(x):.1f},{L(l):.1f}" for x,l in FLOOR_PLAN)
    mid = summary["mid"]
    zones = [
        ("rear", -105, 0, 78, 112), ("power", -40, 32, 78, 54),
        ("control", -10, -34, 100, 42), ("camera", 60, 0, 70, 55),
        ("servos", -125, 0, 38, 78), ("audio", -25, 45, 78, 34),
        ("suspension", 146.1, 0, 72, 190), ("sensors", -90.9, -32, 24, 34),
    ]
    out = [f'<svg style="--drawing-w:{w:.0f}px" viewBox="0 0 {w:.1f} {h:.1f}" role="img" aria-label="Master W17 chassis plan with all assembly zones">',
           defs(), f'<rect width="{w}" height="{h}" fill="url(#grid)"/>',
           f'<polygon class="shell conf-derived" points="{floor}"/>',
           f'<line class="axis" x1="{X(x0)}" y1="{L(0)}" x2="{X(x1)}" y2="{L(0)}"/>']
    for zone,x,l,dx,dl in zones:
        cfg, meta = ZONE[zone], D.ZONE_META[zone]
        tone = "failure" if cfg["tone"]=="fail" else "conf-assumption"
        out += [f'<a href="{esc(meta["html"])}"><rect class="{tone}" x="{X(x-dx/2):.1f}" y="{L(l+dl/2):.1f}" width="{dx*s:.1f}" height="{dl*s:.1f}" rx="10"/>',
                f'<text class="label" x="{X(x-dx/2)+8:.1f}" y="{L(l+dl/2)+18:.1f}">{cfg["code"]} · {esc(meta["title"])}</text></a>']
    out += [f'<circle cx="{X(mid[1]):.1f}" cy="{L(mid[2]):.1f}" r="14" fill="var(--accent)" stroke="var(--paper)" stroke-width="4"/>',
            f'<line class="conf-assumption" x1="{X(mid[1])-25:.1f}" y1="{L(mid[2]):.1f}" x2="{X(mid[1])+25:.1f}" y2="{L(mid[2]):.1f}"/>',
            f'<line class="conf-assumption" x1="{X(mid[1]):.1f}" y1="{L(mid[2])-25:.1f}" x2="{X(mid[1]):.1f}" y2="{L(mid[2])+25:.1f}"/>',
            f'<text class="accent label" x="{X(mid[1])+20:.1f}" y="{L(mid[2])-18:.1f}">CG {mid[1]:+.1f} X / {mid[2]:+.1f} L</text>',
            f'<line class="conf-derived" x1="{X(D.REAR_AXLE_X):.1f}" y1="{L(l1):.1f}" x2="{X(D.REAR_AXLE_X):.1f}" y2="{L(l0):.1f}"/>',
            f'<line class="conf-derived" x1="{X(D.FRONT_AXLE_X):.1f}" y1="{L(l1):.1f}" x2="{X(D.FRONT_AXLE_X):.1f}" y2="{L(l0):.1f}"/>',
            dimline(X(D.REAR_AXLE_X), h-55, X(D.FRONT_AXLE_X), h-55, "237 mm wheelbase", "derived"),
            ruler(pad, h-30, s, 50), "</svg>"]
    return "".join(out)


def balance_svg(summary: dict) -> str:
    mid, high = summary["mid"], summary["high_pod"]
    return f"""<svg style="--drawing-w:940px" viewBox="0 0 940 230" role="img" aria-label="Whole car front rear balance">
{defs()}<rect width="940" height="230" fill="url(#grid)"/>
<text class="accent label" x="25" y="28">WHOLE-CAR CG · p0_d30 MIDPOINT LEDGER</text>
<rect x="50" y="75" width="{820*mid[4]/100:.1f}" height="60" fill="var(--accent)" opacity=".78"/>
<rect x="{50+820*mid[4]/100:.1f}" y="75" width="{820*(100-mid[4])/100:.1f}" height="60" fill="var(--ground)" stroke="var(--line)"/>
<text class="label" x="155" y="111">FRONT {mid[4]:.1f}%</text>
<text class="label" x="610" y="111">REAR {100-mid[4]:.1f}%</text>
<text class="small" x="50" y="160">cockpit case · X-CG {mid[1]:+.1f} · L-CG {mid[2]:+.1f} · Z-CG {mid[3]:.1f} mm</text>
<text class="small" x="50" y="182">high camera-pod case · {high[4]:.1f}% front · Z-CG {high[3]:.1f} mm</text>
<text class="badtext small" x="50" y="205">36–40% front target = ASSUMPTION · physical four-corner scales own D-39</text>
</svg>"""


def overview(components: list[dict], summary: dict) -> str:
    mid = summary["mid"]
    gates = []
    for rank, zone, gate, closure, why, blocks in D.FIT_GATES:
        risk = "rank-high" if rank <= 6 else ("rank-watch" if rank >= 11 else "")
        meta = D.ZONE_META[zone]
        gates.append(f"""<a class="gate {risk}" href="{esc(meta['html'])}">
<span class="tag assumption">OPEN · RANK {rank}</span> <b>{esc(gate)}</b> · {esc(ZONE[zone]['code'])}
<p>{esc(closure)}</p><p><b>Blocks:</b> {esc(blocks)}</p></a>""")
    page = page_start("Assembly-zone master overview", "eight-zone mechanical fit map")
    page += f"""
<p class="eyebrow">10_assembly_architecture / viz · master overview</p>
<h1>Whole-car assembly-zone map</h1>
<p class="lede">Eight linked engineering sheets locate every remaining component, preserve the real
S0=0 shell geometry, show moving envelopes, and mirror each clearance verdict back to its evidence row.
All gates below are still open; no production geometry is released.</p>
<div class="summary">
 <div><strong>{summary['low_total']:.0f}–{summary['high_total']:.0f} g</strong><span>planning range · ASSUMPTION</span></div>
 <div><strong>{mid[4]:.1f}% / {100-mid[4]:.1f}%</strong><span>front / rear midpoint balance</span></div>
 <div><strong>{mid[1]:+.1f}, {mid[2]:+.1f}</strong><span>X/L CG mm · midpoint</span></div>
 <div><strong>1 active + 1 swap</strong><span>single onboard pack architecture</span></div>
</div>
<div class="board"><h2>Chassis plan + linked zones</h2><p class="sub">4 px/mm master plan; click a coloured zone. Red denotes a directly failing/high-risk fit, orange an unresolved physical gate.</p>
 <div class="drawing">{overview_svg(summary)}</div></div>
<div class="board"><h2>Whole-car fore/aft balance</h2><div class="drawing">{balance_svg(summary)}</div></div>
<div class="board"><h2>Confidence legend</h2>{confidence_legend()}</div>
<div class="board"><h2>Fit-gate status board</h2><p class="sub">D-28…D-39 / ASM gates in the p0_07 priority order; each card links to its owning zone drawing.</p>
 <div class="gategrid">{''.join(gates)}</div></div>
<div class="board"><h2>Evidence chain</h2>
 <p><code>p0_07_zone_fit_rollup.py</code> owns 18 STL bboxes, component facts, placements,
 mass scenarios and open gates. This generator reads those structures without changing them,
 adds deterministic embedded STL renders, and sections the real registered 2024 shell meshes.
 The resulting nine pages use inline CSS/JS/SVG and data-URI PNG only.</p>
</div>
"""
    return page + page_end()


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    stls = D.measure_stls()
    components = D.build_components(stls)
    # Warm/cache every real component render once; pages then reuse the exact URI.
    for component_id in D.STL_SOURCES:
        mesh_data_uri(component_id)
    shell_tris = load_shell()
    parity = RayParity(shell_tris)
    summary = D.mass_summary()
    for zone, meta in D.ZONE_META.items():
        page = zone_page(
            zone,
            [c for c in components if c["zone"] == zone],
            shell_tris,
            parity,
            summary,
        )
        (OUT / meta["html"]).write_text(page, encoding="utf-8")
    (OUT / "index.html").write_text(overview(components, summary), encoding="utf-8")
    print(f"STL point renders: {len(RENDER_CACHE)} deterministic cached data URIs")
    print(f"Shell section source: {len(shell_tris)} triangles (front + registered rear)")
    print(f"Ray-parity audits: {len(parity.cache)} unique governing stations")
    print(f"WROTE {len(D.ZONE_META)+1} self-contained HTML files to {OUT}")
    for name in ["index.html"] + [m["html"] for m in D.ZONE_META.values()]:
        print(" ", OUT / name)


if __name__ == "__main__":
    main()
