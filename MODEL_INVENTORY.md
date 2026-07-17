# Model Inventory — every raw file, classified

Human-readable authority for what each file in `unsorted_stl_raw/` is and what we do
with it. Machine-readable twin: `01_inventory/inventory.csv` (one row per file with
size, SHA-256, triangle count, authored-frame bounding box, and the same decisions —
regenerate it from `01_inventory/` script notes if this file changes).

**Corpus (2026-07-10):** 210 files — 152 STL, 25 JPEG photos, 17 PDF drawings, 8 TXT
READMEs, 6 Inventor `.ipt` sources, 1 OpenSCAD, 1 `.3mf`.

| Tier | Count | Meaning |
|---|---|---|
| REQUIRED | **39** | print for the locked build (grouped 02–07 below) |
| OPTIONAL | 5 | cosmetic/display extras, print if desired |
| UNCERTAIN | 21 (20 STL + 1 .scad) | blocked on a human gate — no *production* print yet (diagnostic TP prints allowed where flagged) |
| REJECTED_LIVERY | 39 | wrong team/era shells & aero (Ferrari, McLaren, SF23, RB19, 2021/2023) |
| REJECTED_WRONG_CHASSIS | 18 | Revision 1/1.1 front & floor parts — we run the original oil-shock config |
| REJECTED_SUPERSEDED | 9 | older versions of parts we print differently |
| DUPLICATE | 22 | identical file at a second path (canonical copy noted in CSV) |
| REFERENCE | 57 | PDFs, photos, READMEs, CAD sources — keep, never print |

*(Counts revised 2026-07-10: second pass +3 required — FRONTNOSE2024, 2024 Revised
Front Wing, Servoholder — resolved via drawings [2]/[3]/[5]; 7 rear-wing/DRS files
un-rejected to UNCERTAIN. Third pass: `newgearmotorlock` demoted REQUIRED→UNCERTAIN
(belt-drive lock is primary). See the change notes at the bottom.)*

**Diagnostic vs production prints (policy, user decision 2026-07-10).** UNCERTAIN
parts flagged "diagnostic print candidate" *may* be printed early as **TP-NNN test
prints** (draft settings, any suitable material, physically labelled TP, never
installed on the final car) to resolve fit/assembly questions — preferring a cheap
diagnostic print over rejecting a part too early. This does **not** change the tier:
a part becomes REQUIRED (and gets a production **P-NNN** print from a staged copy)
only when its gate is resolved. Diagnostic prints of unstaged parts may be sliced
directly from the raw file (read-only — never modify raw); record the source path in
the TP entry.

**How to read the tables.** Dims are the authored-frame bounding box in mm (X×Y×Z) —
NOT print orientation; orientation is decided in the slicer per `PRINT_SPEC.md`.
STL geometry has **not been visually inspected** — classification is from filenames,
READMEs, the v2 docs, measured bounding boxes, and a skeptical cross-check of the Codex
print repo's decision reports. Six supplier drawings ([0][1][2][3][5][7]) **were
visually reviewed 2026-07-10** (findings in `ASSEMBLY_NOTES.md`). Anything load-bearing
still gets a human slicer check before printing.

---

## REQUIRED (39) — the locked build

### Group 02 — Rear axle + drivetrain · **ASA black, 100% rectilinear** (8)

Hot + torque-loaded; the documented failure point of this design (Ryan added metal
axle sleeves because printed parts melted). ASA kept after re-evaluation: 2 spools on
hand, X1C enclosed. Print slow, ventilate (styrene). Sources: `Ryans…/Rear Suspension/`
except Axle Main (nested Rev-1 tree).

| File | Dims (mm) | Confidence | Note / check |
|---|---|---|---|
| `Leftrearaxle.stl` | 81×25×10 | **medium** | use the STL (a `.3mf` twin exists — ignore it). ⚠ **do NOT print before Gate A**: drawing `[7]` shows the Rev-1 rear seating the bearings in the Motor Covers instead — these holders may be replaced on that path |
| `Rightrearaxle.stl` | 81×35×10 | **medium** | ⚠ same Gate A caveat |
| `beltdrivemotorlock.stl` | 32×3.5×32 | high | **primary motor lock** — the build uses the original belt-drive solution (user 2026-07-10). `newgearmotorlock` demoted to UNCERTAIN (diagnostic candidate) |
| `Axle Main no grubs.stl` | 11×115×15 | **medium** | ⚠ confirm role vs drawing `[7]` before printing (note: BOM v2 says the belt set *includes* the metal rear output shaft) |
| `Left/Right Spacer for long axle.stl` | 44/26×21×21 | **medium** | ⚠ verify spacer pairing at assembly |
| `NewSpacerleft/right.stl` | 30/18×21×21 | **medium** | ⚠ same — four spacer files, unclear which pair the long axle needs |

### Group 03 — Front suspension + steering · **PETG** (8)

Original oil-shock set (locked config). Source: `Ryans…/Front Suspension/`.
`2023WheelHubsSuspension5.stl` + `…mir.stl` (57×20×50), `Arm4.stl`, `Crossarm3_extended.stl`,
`GuideRod.stl`, `Steering Block4.stl`, `Suspension Block_10.stl` (37×37×71),
`servosaverv7.stl` (⚠ multi-body STL — import once, don't duplicate). All high confidence.
Orient so cornering/steering loads run along layers. Optional: 4× metal sleeves
(5 mm OD × M3, 5 mm long) can replace printed `GuideRod` (Ryan's parts list).

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

### Group 05 — Floor · **PETG** (8)

Original floor (NOT the Rev-1.1 front floor). Source: `Ryans…/Floor/`. Medium
confidence as a set — ⚠ cross-check against drawing `[2] FLOOR ASSEMBLY.pdf` that
nothing is missing before printing all eight.
`2023NewFrontFloorLargerParts.stl` (182×8×137 — largest part, fits X1C bed),
`2023NewBackFloorLargerParts.stl` (117×8×137), `2023NewBackFloorLargerPart2.stl`,
`FloorBoard2.stl`, `Diffuser.stl` (the floor aero diffuser — not the brake light),
`2023NEWSideVent1.stl` (⚠ multi-body), `2023NEWSideVent2.stl`,
`Servoholder.stl` (23×10×58 — **Gate D resolved 2026-07-10**: drawing `[2]` labels it
"Servo Holder" on the rear floor; drawing `[3]` shows the servo driving the servo-saver
via a long rod. ⚠ confirm the ordered DS3235SG fits it when the servo arrives, before
printing the floor batch).

### Group 06 — Body shell · **PLA matte black, 0.12–0.16 mm** (7)

Generic 2024 body painted as W17. Source: `RC-01 Revision 1.1/New 2024 Body/` (+ nested
Body Parts for the camera pod, + Rev-1 Body Upgrades for nose/wing).
`NEW BODY 2024 FRONT 1.stl` (161×129×54), `NEW BODY 2024 REAR.stl` (156×127×73),
`NEW BODY 2024 Mirror.stl`, `new halo 2.1.stl`, `camera top 1.1.stl` (FPV camera pod),
plus — **Gate B front resolved 2026-07-10** —
`FRONTNOSE2024.stl` (129×42×128, **PLA white/grey**, painted silver; drawing `[5]`
"Revised Front Nose"; the 2024-body READ ME bolts the nose to the front floor) and
`2024 Revised Front Wing.stl` (72×181×28; drawing `[5]` "Revised Front Wing"; its
181 mm span exceeds the FRONT shell bbox — cannot be integrated. ⚠ crash-prone:
treat as consumable; consider PETG via an MD entry if it keeps breaking).
Shell mounts with 3× M3 into tight self-threading holes (per its READ ME).
⚠ Final slicer visual confirm of shell+nose+wing together before printing (no
duplicated geometry).

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

## UNCERTAIN (21) — blocked on human gates (production prints; diagnostic TPs allowed where flagged)

**Gate A — rear stack vs 68 mm rear shocks** (decides 9 files incl.
`newgearmotorlock`, coupled to the rear-wing gate). **Precise statement (user
2026-07-10): check whether the selected rear rocker / spring-mount / rear-stack
configuration correctly seats AND articulates with 68 mm rear shocks.** The rear
shock length is **confirmed: 68 mm** — the 51/52 mm figures are the *front* shocks
only; they play no role at the rear. Open `Spring mount 2 REVISION 1.stl` in Bambu
Studio next to the 68 mm coilover dimensions.
- Fits → Rev-1/hybrid rear stack per drawing `[7]`: print `Spring mount 2 REVISION 1`
  + `Spring Block` + the 3× `Rear * Motor Cover REVISION 1` + `Diffuser backplate`
  (all ASA); skip `RearSpringMountREV4` + `springblock`. ⚠ On this path drawing `[7]`
  seats the **bearings in the Motor Covers** and bolts the **rear wing to the
  Diffuser backplate** — verify whether `Left/Rightrearaxle` are then replaced, and
  identify which small STL is `[7]`'s "Light Cover" vs "Diffuser" (we only have
  `rearbacklightdiffuser`, `Diffuser backplate`, and the floor `Diffuser`).
- Doesn't fit → original rear stack per drawing `[2]` (axle holders on the rear floor,
  original spring mounts); skip the Rev-1 pieces above.
- **Resolve together with the rear-wing gate below** — the wing mounts to whichever
  rear stack is chosen, not to the body shell.
- **Unresolved as of 2026-07-10 (user confirmed):** whether the Motor Covers replace
  `Left/Rightrearaxle`, and which STL is `[7]`'s "Light Cover". Per the diagnostic
  policy above, the small candidates (motor covers, spring mounts, backplate,
  `newgearmotorlock` — all ≲40 g) **may be TP-printed for a diagnostic dry-fit**
  rather than rejected early; production rear-stack prints stay blocked until the
  stack is confirmed as a whole.
- **The gate (with the rear-wing gate) closes only when ALL of:** ① the 68 mm shock
  path is checked in the slicer or a diagnostic dry assembly, ② the selected rear
  stack is confirmed, ③ the wing mount is confirmed, ④ `2021Rearwing with DRS` is
  checked together with mount + DRS arm + diffuser/backplate, ⑤ any remaining
  questionable small parts are diagnostic-TP printed where the slicer wasn't enough.
- `newgearmotorlock.stl` (38×3.5×38) — demoted from REQUIRED (belt-drive
  `beltdrivemotorlock` is the primary; BOM v2 lists only it). Diagnostic print
  candidate for comparison; REQUIRED again only if `[7]`/photos/assembly show it used.
  Does **not** block coupons or wheel-fit prints.

**Gate B — rear wing + DRS** (7 files; **user decisions 2026-07-10: DRS wing planned;
the OLD 2021 wing is the preferred candidate** — "as far as I can see, only the old
rear wing fits"). BOM v2 orders an MG90S for DRS, wiring atlas drives it on CH6. The
*front* half of Gate B is **resolved** — nose + front wing moved to REQUIRED group 06;
only `pin.stl` remains (M3-bolted 2024 body probably needs no pins — confirm in
slicer). The rear wing is chassis-mounted (drawings `[2]`/`[7]`), so pick it with
Gate A. **The gate stays open until the old wing + mount + DRS arm +
diffuser/backplate + selected rear stack are checked together**; questionable small
interface parts (arms, flap deco, DRS diffuser) are diagnostic-TP candidates, not
production parts, until that combined check passes:

| Candidate | Pairs with | Evidence | Risk |
|---|---|---|---|
| **PREFERRED:** `2021Rearwing with DRS.stl` (105×82×60) + `DRS Arm for 2021 Rear Wing.stl` (58 mm) + optional `2021Rearwingflapdeco.stl` | **original** rear stack | fully documented: drawings `[0]`/`[2]` show it mounted with a DRS-servo pocket + metal-rod linkage; user judged it the only wing that visibly fits | 2021-era tall-wing styling — least W17-like |
| fallback: `MCL60 2023 Rear Wing.stl` (108×41×75) + `DRS Arm for 2023 Rear Wing.stl` (64 mm) | **Rev-1** rear stack | very likely `[7]`'s "Revised rear wing" (the only rear-wing STL in the Rev-1 release); bolts to the Diffuser backplate | McLaren-shaped (painted black anyway); DRS-servo placement not drawn |
| fallback: `Print_In_Place DRSv2.stl` (120×50×83) | unknown | newest DRS design by name ("v2") | no drawing covers it; print-in-place hinge is a beginner printability risk; mounting unverified |

`DRS Diffuser.stl` (68×50×45) — floor-diffuser variant for a DRS install; compare
against the required `Diffuser.stl` once the wing is chosen (diagnostic-TP candidate).

**Gate C — camera integration** (4 files; **reframed 2026-07-10 as a research/design
task, not a ready-to-print task**). Camera on hand: OpenIPC-style **SSC338Q + IMX335
5 MP** (user 2026-07-10; note the frozen BOM/atlas say IMX415 — sensor is irrelevant
to the mount, board/heatsink/lens dims are what matter). **Never assume dimensions
from product links or similar cameras — the mount is designed only from the real
camera measured with calipers.** Full measurement + design checklist:
`FIRST_PRINT_DECISION.md` §6.

`camera_blower_duct.scad` is the **current duct source/design candidate** (source
inspected 2026-07-10): fully **parameterized**, not hard-coded — 9 labelled
"MEASURE THESE" dimensions (blower outlet w/h, blower face w/h, collar depth, mouth
w/h, duct length) plus wall/clearance and an optional M3 tab; the shipped values are
**placeholder defaults** ("a sane STARTING geometry, not a guaranteed fit" — its own
words), and its header carries a print spec (PETG, 0.2 mm, 3 walls, 20%) matching our
matrix. **Diagnostic step allowed:** render the defaults to a temporary STL and
inspect in Bambu Studio — visual/design validation only, never a production print.
**Production duct/mount stays blocked** until: camera measured with calipers ✓,
blower arrived + measured ✓, placement decided ✓, airflow path checked ✓, lens
clearance checked ✓, service/removal access checked ✓.
`cameranose.stl`, `camera 2 colour.stl`, `f104camera.stl` are probably unneeded
(camera top 1.1 selected) — confirm during the mount design.

**Gate D — RESOLVED 2026-07-10:** `Servoholder.stl` moved to REQUIRED group 05.
Drawing `[2]` labels it "Servo Holder" on the rear floor; drawing `[3]`'s note "mount
this hole with a rod to the steering servo motor" confirms the servo sits mid-chassis
driving the servo-saver through a long rod (the Rev-1.1 "direct front facing servo"
README corroborates: the *original* method was different, i.e. this rod layout).
Residual check: DS3235SG fitment when the servo arrives — do **not** print the floor
batch before that.

## REJECTED (66) — keep on disk, never print

- **Livery/era (39):** Ferrari SF24 shells, all 14 McLaren MCL38 files, SF23 set
  (top body, horn, sharkfin, camera top, pin), RB19 + 2023 top bodies, sidepods,
  2021/2023 front wings, noses, decos, turning vanes, 2021 side vent. We paint W17
  on the generic 2024 shell. *(MCL60 wing + the two 2021 rear-wing files moved to
  UNCERTAIN 2026-07-10 — rear-wing/DRS gate.)*
- **Wrong chassis (18):** the entire `New 1.1 Steering Upgrades` ball-joint set, all
  Revision-1 `Front Axle Upgrades` (ARM1 variants, Armblock, servomounts, steering
  arms/blocks), the three Revision-1 suspension floors + Rev-1.1 front floor.
- **Superseded (9):** non-"tighter" tyre-slot adapters, both old rear covers,
  `2024 halo` (→ new halo 2.1), `cameratop` (→ camera top 1.1), `Mirrors 2024`
  (→ NEW BODY Mirror), old invert-axle parts. *(The four DRS files moved to UNCERTAIN
  2026-07-10 — DRS is back in the build.)*

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

---

## Change note — 2026-07-10 second pass (gate review)

Evidence: supplier drawings `[0][1][2][3][5][7]` visually reviewed (Claude can read
the PDFs; findings mapped in `ASSEMBLY_NOTES.md`), `docs/bill_of_materials_v2.md` +
`docs/w17_wiring_assembly_atlas.html` added, user decisions of 2026-07-10.

- **+3 REQUIRED (37→40):** `FRONTNOSE2024` + `2024 Revised Front Wing` (Gate B front —
  drawing `[5]`, body README, bbox math) and `Servoholder` (Gate D — drawing `[2]`).
  Staged with MANIFEST rows.
- **7 files rejected→UNCERTAIN:** rear-wing/DRS candidates (`2021Rearwing with DRS`,
  `2021Rearwingflapdeco`, `MCL60 2023 Rear Wing`, both `DRS Arm`s, `Print_In_Place
  DRSv2`, `DRS Diffuser`) — the user reinstated DRS; BOM v2 orders an MG90S for it.
- **Gate A expanded:** drawing `[7]` shows the Rev-1 rear seating bearings in the
  Motor Covers and bolting the rear wing to the Diffuser backplate — the axle-holder
  files may be path-dependent; Gate A and the rear-wing gate resolve together.
- CSV regenerated via `01_inventory/build_inventory.py` (210 files, tiers sum checked).

## Change note — 2026-07-10 third pass (human answers)

- **Rear wing:** the 2021 wing marked **preferred** (user: only one that visibly
  fits); MCL60 + PIP DRSv2 kept as fallbacks; gate stays open until wing + mount +
  DRS arm + diffuser/backplate + rear stack are checked together.
- **Diagnostic-print policy added** (top of this file): uncertain small parts may be
  TP-printed to resolve gates instead of being rejected early; tiers unchanged by
  diagnostics; production prints still gate-blocked.
- **`newgearmotorlock` demoted REQUIRED→UNCERTAIN** (39 required): build uses the
  original belt-drive solution; `beltdrivemotorlock` is primary. Staged copy removed
  from `02_ready_to_slice/` (manifest updated); raw original untouched.
- **Gate C reframed** as a research/design task (camera = SSC338Q + IMX335; measure
  the real hardware only); checklist added to `FIRST_PRINT_DECISION.md`.
- **Dry printed-part assembly allowed as diagnostic** before hardware arrives;
  hardware-dependent fitment stays blocked (see `ASSEMBLY_NOTES.md`).
- CSV regenerated; 39 staged copies re-verified.
