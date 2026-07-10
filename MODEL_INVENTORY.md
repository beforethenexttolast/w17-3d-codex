# Model Inventory — every raw file, classified

Human-readable authority for what each file in `unsorted_stl_raw/` is and what we do
with it. Machine-readable twin: `01_inventory/inventory.csv` (one row per file with
size, SHA-256, triangle count, authored-frame bounding box, and the same decisions —
regenerate it from `01_inventory/` script notes if this file changes).

**Corpus (2026-07-10):** 210 files — 152 STL, 25 JPEG photos, 17 PDF drawings, 8 TXT
READMEs, 6 Inventor `.ipt` sources, 1 OpenSCAD, 1 `.3mf`.

| Tier | Count | Meaning |
|---|---|---|
| REQUIRED | **37** | print for the locked build (grouped 02–07 below) |
| OPTIONAL | 5 | cosmetic/display extras, print if desired |
| UNCERTAIN | 16 (15 STL + 1 .scad) | blocked on a human gate — do NOT print yet |
| REJECTED_LIVERY | 42 | wrong team/era shells & aero (Ferrari, McLaren, SF23, RB19, 2021/2023) |
| REJECTED_WRONG_CHASSIS | 18 | Revision 1/1.1 front & floor parts — we run the original oil-shock config |
| REJECTED_SUPERSEDED | 13 | older versions of parts we print differently |
| DUPLICATE | 22 | identical file at a second path (canonical copy noted in CSV) |
| REFERENCE | 57 | PDFs, photos, READMEs, CAD sources — keep, never print |

**How to read the tables.** Dims are the authored-frame bounding box in mm (X×Y×Z) —
NOT print orientation; orientation is decided in the slicer per `PRINT_SPEC.md`.
Geometry has **not been visually inspected** — classification is from filenames, READMEs,
the v2 docs, measured bounding boxes, and a skeptical cross-check of the Codex print
repo's decision reports. Anything load-bearing gets a human check before printing.

---

## REQUIRED (37) — the locked build

### Group 02 — Rear axle + drivetrain · **ASA black, 100% rectilinear** (9)

Hot + torque-loaded; the documented failure point of this design (Ryan added metal
axle sleeves because printed parts melted). ASA kept after re-evaluation: 2 spools on
hand, X1C enclosed. Print slow, ventilate (styrene). Sources: `Ryans…/Rear Suspension/`
except Axle Main (nested Rev-1 tree).

| File | Dims (mm) | Confidence | Note / check |
|---|---|---|---|
| `Leftrearaxle.stl` | 81×25×10 | high | use the STL (a `.3mf` twin exists — ignore it) |
| `Rightrearaxle.stl` | 81×35×10 | high | |
| `beltdrivemotorlock.stl` | 32×3.5×32 | high | belt-drive motor lock |
| `newgearmotorlock.stl` | 38×3.5×38 | high | second motor lock — v2 lists both |
| `Axle Main no grubs.stl` | 11×115×15 | **medium** | ⚠ confirm role vs drawing `[7]` before printing |
| `Left/Right Spacer for long axle.stl` | 44/26×21×21 | **medium** | ⚠ verify spacer pairing at assembly |
| `NewSpacerleft/right.stl` | 30/18×21×21 | **medium** | ⚠ same — four spacer files, unclear which pair the long axle needs |

### Group 03 — Front suspension + steering · **PETG** (8)

Original oil-shock set (locked config). Source: `Ryans…/Front Suspension/`.
`2023WheelHubsSuspension5.stl` + `…mir.stl` (57×20×50), `Arm4.stl`, `Crossarm3_extended.stl`,
`GuideRod.stl`, `Steering Block4.stl`, `Suspension Block_10.stl` (37×37×71),
`servosaverv7.stl` (⚠ multi-body STL — import once, don't duplicate). All high confidence.
Orient so cornering/steering loads run along layers. Optional: 5×M3 metal sleeves can
replace printed `GuideRod` (Ryan's parts list).

### Group 04 — Wheels · **PETG** (7)

Loaded parts, not cosmetic. Rims hidden under tyres → color irrelevant (high-speed
PETG blue is fine).

| File | Dims | Note / check |
|---|---|---|
| `Front_Rim_F1_2022.stl` | Ø44×30 | qty 2 final; **test-fit 1 rim + 1 tyre + 1 bearing first** |
| `Rear_Rim_F1_2022.stl` | Ø47×35.5 | qty 2 final |
| `Front_Right_Wheel_Hub_2022_F104.stl` | 28×64×56 | ⚠ **only a RIGHT hub exists — mirror in Bambu Studio for the left**; verify mirrored bearing seat 8×12×3.5 |
| `Front/Rear_Locking_Nut_F1_2022.stl` | Ø11.5 | qty 2 each; printed threads — thread gently |
| `F104 tyreslot1/2 no grubs tighter.stl` | ~16×33/19×14 | Rev-1.1 "tighter" versions (wanted). ⚠ final qty unproven (1 or 2 each); ⚠ near-axle heat — if they soften in use, reprint in ASA |

**Note:** the spec's "ASA for the rear hub" rule has **no matching file** — no rear-hub
STL exists (rear wheels mount via the tyre-slot adapters). Flagged instead as the heat
watch on the adapters above. The folder name mentions a "Wheelfin" that isn't present —
presumed not needed.

### Group 05 — Floor · **PETG** (7)

Original floor (NOT the Rev-1.1 front floor). Source: `Ryans…/Floor/`. Medium
confidence as a set — ⚠ cross-check against drawing `[2] FLOOR ASSEMBLY.pdf` that
nothing is missing before printing all seven.
`2023NewFrontFloorLargerParts.stl` (182×8×137 — largest part, fits X1C bed),
`2023NewBackFloorLargerParts.stl` (117×8×137), `2023NewBackFloorLargerPart2.stl`,
`FloorBoard2.stl`, `Diffuser.stl` (the floor aero diffuser — not the brake light),
`2023NEWSideVent1.stl` (⚠ multi-body), `2023NEWSideVent2.stl`.

### Group 06 — Body shell · **PLA matte black, 0.12–0.16 mm** (5)

Generic 2024 body painted as W17. Source: `RC-01 Revision 1.1/New 2024 Body/` (+ nested
Body Parts for the camera pod). `NEW BODY 2024 FRONT 1.stl` (161×129×54),
`NEW BODY 2024 REAR.stl` (156×127×73), `NEW BODY 2024 Mirror.stl`, `new halo 2.1.stl`,
`camera top 1.1.stl` (FPV camera pod). Mounts with 3× M3 into tight self-threading
holes (per its READ ME). See the FRONTNOSE2024 gate under UNCERTAIN.

### Group 07 — Brake-light diffuser · **PLA white-transparent** (1)

`rearbacklightdiffuser.stl` (9.5×12×14.5, nested Rev-1 tree) — the revised part with
the WS2812 hole. 1–2 walls over the lens, 15–20% infill, **lens never painted** (red
comes from firmware). Your PLA white-transparent spool matches the spec exactly.

---

## OPTIONAL (5)

`fulldrivercut2.stl` (driver figure — 50 MB/1M triangles, long print, display only),
`Fullhelm2.stl` (helmet), `wall mount.stl` (75×62×15 wall display), `sharkfinnew2.stl`
(⚠ 1.9 mm thin — fragile; confirm the 2024 body even wants one), `sidewingdeco.stl`
(⚠ 1 mm thin; confirm fitment). All PLA, any color under paint.

## UNCERTAIN (16) — blocked on human gates, do NOT print

**Gate A — rear rocker vs 68 mm shock** (decides 8 files): open
`Spring mount 2 REVISION 1.stl` in Bambu Studio next to the 68 mm coilover dimensions.
- Fits → hybrid rocker path: print `Spring mount 2 REVISION 1` + `Spring Block` + the
  3× `Rear * Motor Cover REVISION 1` (all ASA); skip `RearSpringMountREV4` + `springblock`.
- Doesn't fit → original rear mount; skip all of the above.
- `Diffuser backplate.stl` — verify against drawing `[7]` whether the chosen rear
  assembly needs it at all (ASA or PETG if yes).

**Gate B — body completeness** (3 files): open `NEW BODY 2024 FRONT 1` in the slicer
and check whether nose + front wing are integrated. If not: `FRONTNOSE2024.stl` is
almost certainly the separate **silver-nose piece** (print PLA white/grey per spec) and
`2024 Revised Front Wing.stl` is needed. `pin.stl` — check whether the M3-bolted 2024
body still uses body pins anywhere.

**Gate C — camera measurement** (4 files): `camera_blower_duct.scad` is parametric
SOURCE (not printable) — measure the real OpenIPC camera + ACP2006 blower, set the 9
parameters, render an STL, then it joins group 08. `cameranose.stl`,
`camera 2 colour.stl`, `f104camera.stl` are probably unneeded (camera top 1.1 selected)
— confirm after the camera is in hand.

**Gate D:** `Servoholder.stl` — check drawing `[3]` whether the oil-shock front uses it.

## REJECTED (73) — keep on disk, never print

- **Livery/era (42):** Ferrari SF24 shells, all 14 McLaren MCL38 files, MCL60 wing,
  SF23 set (top body, horn, sharkfin, camera top, pin), RB19 + 2023 top bodies,
  sidepods, 2021/2023 wings, noses, decos, turning vanes, 2021 side vent. We paint W17
  on the generic 2024 shell.
- **Wrong chassis (18):** the entire `New 1.1 Steering Upgrades` ball-joint set, all
  Revision-1 `Front Axle Upgrades` (ARM1 variants, Armblock, servomounts, steering
  arms/blocks), the three Revision-1 suspension floors + Rev-1.1 front floor.
- **Superseded (13):** non-"tighter" tyre-slot adapters, both old rear covers,
  `2024 halo` (→ new halo 2.1), `cameratop` (→ camera top 1.1), `Mirrors 2024`
  (→ NEW BODY Mirror), old invert-axle parts, and the whole DRS system (Print_In_Place
  DRSv2, DRS diffuser, both DRS arms — DRS was dropped from the v2 build).

Full per-file list with reasons: `09_rejected_or_uncertain/REVIEW.md` and the CSV.

## DUPLICATE (22) + REFERENCE (57)

The RC-01 Revision 1 tree exists twice; where both copies are byte-identical by name
the **nested** copy (under `RC-01 Revision 1.1/Original + Revision 1 Files…`) is
canonical and the top-level copy is marked DUPLICATE (and vice versa for Ryan's floor
parts — Ryan's copies are canonical). The two trees are NOT fully identical — each has
unique files; those got their own rows. Reference tier: 17 PDF drawings (mapped to
assembly stages in `ASSEMBLY_NOTES.md`), 25 install photos, 8 supplier READMEs, 6 `.ipt`
CAD sources, `Leftrearaxle.3mf` (alternate format of a selected STL — use the STL).

---

## Cross-check against the Codex print repo (skeptical intake, 2026-07-10)

The Codex-owned `w17-rc-print-codex` classified the same corpus. Where we agree and
where this inventory deliberately differs or adds:

- **Agree** on all 37 required files, the 5 optionals, the 16 uncertain, and the
  reject set — independent re-derivation from `docs/print_spec_v2.md` landed on the
  same selection.
- **Their queue has two orphan files** (`GuideRod.3mf`, `NEW BODY 2024 REAR.3mf`)
  absent from their own manifests — we copy from `unsorted_stl_raw/` originals only,
  never from their queue, so this can't leak into our build.
- **"ASA rear hub" spec rule is unappliable** (no rear-hub file exists); they noted it
  in a side report, we surface it as the heat-watch on the tyre-slot adapters (group 04).
- **They rate several "required" parts only medium-confidence** (Axle Main, all four
  spacers, the floor set) with boilerplate reasoning — we keep those parts required but
  attach explicit pre-print human checks (drawings `[2]`/`[7]`, assembly verification).
- **Their diffuser material** is "white/natural translucent PLA/PETG"; ours is pinned
  to the PLA white-transparent spool on hand.
- **Quantities:** their guide guesses tyre-slot adapter counts ("possibly 2") — carried
  here as an explicit check, not a fact.
