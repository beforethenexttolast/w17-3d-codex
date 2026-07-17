# First Print Decision — do this before anything touches the printer

Working checklist from the 2026-07-10 pre-print audit, revised twice the same day:
second pass (drawings read, BOM v2 + atlas, DRS reinstated, hardware ordered) and
**third pass (human answers: preferred rear wing, diagnostic-print policy, motor-lock
demotion, camera research task, dry-assembly allowance, battery probe)**. Sources of
truth stay where they are (`PRINT_SPEC.md`, `MODEL_INVENTORY.md`,
`MATERIAL_DECISION_MATRIX.md`, `BUILD_SHEET.md`) — this file is the execution order.
Check items off here; record outcomes in `GENERAL_PLAN.md` open questions and the logs.

## Status snapshot (2026-07-10, third pass)

- **Resolved:** Gate B front (nose + wing REQUIRED), Gate D (`Servoholder`), motor
  lock (belt-drive `beltdrivemotorlock` primary; `newgearmotorlock` demoted to
  diagnostic candidate). Required count **39**, staged and hash-verified.
- **Directional:** rear wing — **old `2021Rearwing with DRS` preferred** (user);
  DRS remains a goal. **Rear shocks confirmed 68 mm** (the 51/52 mm numbers are
  front-only). Gate stays open until wing + mount + DRS arm + diffuser/backplate +
  rear stack pass a **combined** check.
- **Open:** Gate A sub-questions (covers vs axle holders; "Light Cover" identity),
  Gate C (camera integration = research/design task), battery (approximate probe done,
  final blocked).
- **Hardware:** everything ordered, **in transit**. Calipers + camera (SSC338Q +
  IMX335) on hand. **New allowance:** diagnostic TP prints of uncertain small parts
  + printed-part-to-printed-part dry assembly may proceed before hardware arrives.

## Diagnostic vs production prints (the new policy, short form)

- **TP-NNN = diagnostic/test print.** Draft settings OK, any suitable filament,
  physically labelled TP, logged in `04_test_prints/`, **never installed on the
  final car**. Uncertain parts flagged "diagnostic candidate" may be TP-printed to
  resolve their gate — better a cheap print than a premature rejection (user
  decision 2026-07-10). Unstaged/uncertain parts may be sliced straight from the raw
  file (read-only; record source path in the TP entry).
- **P-NNN = production print.** Only for REQUIRED parts, only from staged copies in
  `02_ready_to_slice/`, only after the part's gate is closed.
- A diagnostic print never changes a tier by itself — the gate decision does.

**Approved diagnostic candidates (all small/cheap):** `newgearmotorlock` (compare
with belt lock) · Rev-1 rear-stack pieces (`Spring mount 2 REVISION 1`,
`Spring Block`, 3× Motor Covers, `Diffuser backplate`) and/or original pieces
(`RearSpringMountREV4`, `springblock`) · DRS interface parts (`DRS Arm for 2021`,
flap deco, `DRS Diffuser`) · the wing itself if a slicer check isn't conclusive.
Use PETG or PLA drafts for shape/fit diagnostics — save the ASA for production.

## The decision (TL;DR)

1. **Print now:** Bambu demo → **PLA coupon** → **PETG coupon** (dry the spool).
   Measure with calipers, log as TP.
2. **Slicer sitting (§1):** Gate A + rear wing combined check, centred on the
   preferred 2021 wing. Where the slicer can't settle it — **TP-print the small
   candidates and dry-fit them** (diagnostic wave).
3. **After coupons:** wheel fit set (print unblocked; FIT verdicts wait for tyres +
   bearings).
4. **Camera:** research/design task — start the §6 measurement checklist with the
   real camera now; duct/mount design waits for the blower.
5. **Battery:** approximate probe done (§7) — final choice stays blocked until a
   slicer-assembly measure / printed dry-fit.
6. **Still no production prints of:** ASA rear batch, floor batch (servo fit-check
   pending), body shells, wing.

---

## 1 · Slicer inspection checklist (no filament, ~1 evening)

Import from `02_ready_to_slice/` (production parts) or raw paths view-only (gated
candidates). Use **Measure**; write outcomes down.

**The coupled rear decision — Gate A + rear wing + DRS (one sitting).**
Gate A, precisely (user 2026-07-10): *check whether the selected rear rocker /
spring-mount / rear-stack configuration correctly seats **and articulates** with the
**68 mm rear shocks**.* Rear length is confirmed at 68 mm — the 51/52 mm figures are
front shocks only, never the rear.
- [ ] Open `Spring mount 2 REVISION 1.stl` (view-only). Does its rocker seat the
      **68 mm** coilover (ordered HSP shock, eye-to-eye) — and can it articulate
      through travel, not just fit statically?
- [ ] Open the **preferred wing `2021Rearwing with DRS.stl`** next to the chosen
      stack (drawing `[2]` shows it on the original spring-mount tower with the DRS
      pocket): do the mount interfaces mate? Where does the MG90S sit; where does the
      metal rod run (drawing `[2]`)?
- [ ] Combined check before anything is final: **wing + mount + `DRS Arm for 2021` +
      diffuser/backplate + selected rear stack together.** Fallbacks if the 2021 wing
      disappoints: MCL60-style (Rev-1 stack, drawing `[7]`) or PIP DRSv2 (undocumented).
- [ ] Rev-1 sub-questions (user-confirmed open): do the Motor Covers replace
      `Left/Rightrearaxle` (bearings seat in the covers in `[7]`)? Which small STL is
      `[7]`'s "Light Cover" vs "Diffuser"?
- [ ] **Where the slicer can't settle any of the above → TP-print the small
      candidates** (see diagnostic list) and dry-fit. Log TP + ASM-diagnostic entries.
- [ ] **Closure check — the rear gates close only when ALL of:** 68 mm shock path
      checked (slicer or diagnostic dry assembly) ✓ · rear stack confirmed ✓ · wing
      mount confirmed ✓ · 2021 wing checked with mount + DRS arm +
      diffuser/backplate ✓ · remaining doubts settled by diagnostic TPs ✓.
- [ ] Motor lock: `beltdrivemotorlock` is the build's lock (original belt-drive
      solution). Optionally TP-print `newgearmotorlock` alongside for comparison —
      neither this nor any rear question blocks coupons or wheel-fit prints.
- [ ] `Axle Main no grubs` role vs `[7]` — the belt set includes a metal output
      shaft (BOM v2 §8), so a printed axle part may be redundant.

**Body group confirms (fast — decisions already made):**
- [ ] Shell + `FRONTNOSE2024` + `2024 Revised Front Wing` together: no duplicated
      geometry; nose bolts to the front floor (body READ ME).
- [ ] `camera top 1.1` mates with the 2024 shell (Rev-1-era part).
- [ ] `pin.stl`: no pin holes anywhere → formally reject it.
- [ ] Mirror `Front_Right_Wheel_Hub_2022_F104`; measure the mirrored bearing seat
      (Ø12 pocket for 8×12×3.5).
- [ ] Floor: all 8 group-05 files (incl. `Servoholder`) against drawing `[2]`.
- [ ] King-pin knuckle bore ≈ 3 mm (M3×30 dowel pins ordered).
- [ ] Battery bay: assemble floor + FRONT/REAR shells visually (bolt holes align) and
      measure the clear pocket — this supersedes the §7 single-shell probe.
- [ ] Slicer error check on every staged file; note anything red in the inventory.

Gate outcomes → update `MODEL_INVENTORY.md` + CSV (via `build_inventory.py`) +
`REVIEW.md` together; stage newly-required files with MANIFEST rows.

## 2 · Hardware — ordered, in transit, on hand

Everything from BOM v2 is **ordered**. Nothing left to buy except the **battery**
(deliberately last) and paint/decal consumables (Phase 8–9).

| Arrives → unblocks | Items |
|---|---|
| Wheel FIT verdicts | Tamiya 54198 + 51400 tyres, MR128ZZ front bearings, 6801 rear bearings |
| Gate A physical confirm + rear assembly | 68 mm HSP rear shock, 52 mm front shocks, belt set (incl. metal output shaft), pinion + spur, aluminium tube (cut 4× 14 mm spacers) |
| Servo fit-checks (floor batch + DRS pocket) | DS3235SG steering servo, 3× MG90S (pan/tilt/DRS) |
| Steering assembly | king pins, ball studs, rod ends, turnbuckles, M4 rods, M3 kit, inserts, sleeves |
| Camera duct render (Gate C, other half) | ACP2006-class 5 V blower (camera on hand — measure it now, §6) |

**On hand:** digital calipers ✓ · camera (flashed) ✓ · filament ✓ · printer ✓.
**On arrival:** measure front shocks (51 vs 52 mm), spur ↔ belt-pulley bolt pattern,
both servo fit-checks. **Until then:** hardware-dependent fitment is blocked, but
printed-part-to-printed-part **diagnostic dry assembly may proceed**
(`ASSEMBLY_NOTES.md`).

## 3 · First prints, in order (what to open in Bambu Studio)

Workflow per step: `PRINT_SPEC.md`. Log every one: TP-NNN in `04_test_prints/`.

0. **Bambu demo print** (pre-sliced). Proves the machine. **Today.**
1. **TP: PLA coupon** — 25×25×10 mm cube + Ø12 negative cylinder 4 mm deep (bearing
   seat) + Ø3 through-hole (M3). 0.20 mm, 4 walls, 40% gyroid. Measure, log.
2. **TP: PETG coupon** — same model; **dry the spool first** (60–65 °C, 6–8 h), cap
   outer walls ~150 mm/s. Calibrates the wheel prints.
3. **TP: diagnostic wave (optional, as needed from §1)** — small rear-stack / DRS /
   motor-lock candidates in PETG/PLA draft; dry-fit; record TP + ASM-diagnostic
   entries. This is how the rear gate closes if the slicer alone can't.
4. **TP: wheel fit set (PETG)** — 1× front rim + hub + locking nut (thread axis
   vertical) + 1× rear rim + 1× of each tyreslot adapter. Print after the PETG
   coupon measures sane; **FIT verdicts wait for tyres + bearings** (adapters were
   designed against Tamiya F104 rim geometry per `[7]` — exactly what the test checks).
5. **TP: body wall slice** (2–3 cm slicer-cut, 0.12 mm PLA matte) — look test +
   primer/paint card. Any time; needed before Phase 8.
6. **TP: ASA coupon** — immediately before the group-02 *production* batch (which
   waits on the resolved rear gate). Ventilation drill applies. Fallback if ASA
   fights you twice: PETG + metal sleeves + heat check, logged as an MD deviation.

## 4 · Blocked / unblocked map

**Print now:** demo · PLA coupon · PETG coupon · body wall slice.
**Diagnostic prints now (TP, draft, labelled):** rear-stack candidates · DRS
interface parts · `newgearmotorlock` comparison · preferred wing if slicer is
inconclusive.
**Design validation now (no printing):** default-render `camera_blower_duct.scad`
to a temp STL and inspect it in Bambu Studio (§6 — visual only).
**Print after coupons:** wheel fit set (verdicts wait on parts).
**Dry assembly now (diagnostic):** printed↔printed fits only; nothing final.

**Blocked until the slicer sitting + diagnostic dry-fits:** the ASA rear
*production* batch (Gate A decides which files — possibly not the staged axle
holders) · rear wing + DRS arm *production* print · `Diffuser backplate` ·
formal rejection of `pin.stl`.
**Blocked until parts arrive:** all FIT entries with real hardware · floor batch
(DS3235SG fit-check into `Servoholder`) · DRS pocket check (MG90S) · Gate A physical
confirm (68 mm shock) · spacer cutting.
**Blocked until measured:** camera mount/duct design (§6 — camera measurable now,
blower in transit) · battery purchase (§7 → slicer-assembly measure → physical fit).
**Not yet, regardless:** body shells / halo / nose / front wing production prints
(after wall-slice + paint plan) · remaining rims + mirrored hub (after fit set
passes) · optionals.

## 5 · Top open risks

1. **Rear stack ambiguity includes required files** — don't production-print any
   group-02 part before the combined rear check; use diagnostic TPs to de-risk.
2. **Wing choice is aesthetic + mechanical at once** — the 2021 wing is preferred
   but unverified against the stack; the combined check (slicer + TP dry-fit) is
   the gate, not preference.
3. **Servo fitment is assumed, not confirmed** — measure DS3235SG + MG90S on arrival
   before the floor batch and the wing production print.
4. **HF PETG at speed is weaker** — the ~150 mm/s wall cap (`PRINT_SPEC.md` §2) is
   mandatory for suspension parts.
5. **Atlas staleness** — `docs/w17_wiring_assembly_atlas.html` predates BOM v2
   ("12 mm hex" wheels, "51 mm" shocks, IMX415 sensor are stale). Trust BOM v2 +
   this repo for mechanics; the atlas for wiring topology.
6. **Diagnostic prints masquerading as production** — every TP part gets a physical
   TP label; nothing labelled TP goes on the final car.

## 6 · Camera integration — research/design checklist (Gate C)

Camera on hand: OpenIPC-style **SSC338Q + IMX335 5 MP** (similar to
hobbyt.com.ua "OpenIPC mapping mini" — **reference only; take zero dimensions from
product pages or similar cameras**). The mount/duct is designed exclusively from
calipers measurements of **your** board. Blower (ACP2006-class) in transit.
This is a design task, not a ready-to-print task.

**Measure (calipers, record in a Gate C note under `07_assembly_notes/`):**
- [ ] Board width / height / thickness
- [ ] Heatsink width / height / thickness (is one fitted at all?)
- [ ] Total depth including lens
- [ ] Lens barrel diameter
- [ ] Lens center offset from each board edge
- [ ] Mounting holes: present? positions/diameters
- [ ] Cable/connector exit direction + required wire clearance

**Thermal:**
- [ ] Does it need forced airflow (run it on the bench, feel/measure temperature)?
- [ ] Is the existing heatsink adequate, or is the ducted blower load-bearing?
- [ ] Blower placement + duct path (never trap heat in a closed pocket; inlet/outlet
      per `BUILD_SHEET.md` packing note: vents front-in / rear-out)

**Design constraints (all mandatory):**
- [ ] Lens fully unobstructed (FOV check against the body opening)
- [ ] No clamping stress on the lens barrel — grip the board/heatsink, never the lens
- [ ] Service access: camera removable without destroying the mount
- [ ] No paint near lens, heatsink, connectors, or airflow openings (mask them)

**Decisions to make (write them down as an MD/Gate note):**
- [ ] Fixed, adjustable-tilt, or servo pan/tilt mount? (pan/tilt servos are ordered;
      the *firmware* side of gimbal control lives in the firmware repos with its own
      safety gates — this repo only decides the mechanical mount)
- [ ] Placement: behind a body opening, above the body (camera top 1.1 pod), or
      inside a protective duct? → requirements + the driver-seat vs halo-height
      trade study live in `CAMERA_GIMBAL_PLACEMENT.md` (source of truth; includes
      the VR/head-tracking requirements and the hard-stop geometry the firmware
      safety gate needs)
- [ ] Does `camera top 1.1` still fit the chosen scheme, or does the duct/mount
      replace it? (then cameranose/f104camera/camera 2 colour get their verdicts)

**Duct source (inspected 2026-07-10):** `camera_blower_duct.scad` is the current
duct design candidate and it is **fully parameterized, not hard-coded** — 9 labelled
"MEASURE THESE" dimensions (blower outlet w/h, blower face w/h, collar depth, camera
mouth w/h, duct length) plus `wall`/`clearance` fit params and an optional M3
mounting tab. The shipped values are **placeholder defaults** — the file itself says
"a sane STARTING geometry, not a guaranteed fit". Its header print spec (PETG,
0.2 mm, 3 walls, 20%) matches our material matrix.

**Diagnostic step (allowed now, no printing):** open the `.scad` in OpenSCAD, render
the defaults (F6), export a temporary STL (keep it out of `02_ready_to_slice/`;
`*.stl` is gitignored anyway), and inspect it in Bambu Studio — purely
**visual/design validation** of the duct concept, never a production print. Record
observations in a Gate C note.

**Gate C stays blocked for production printing until ALL of:** real camera measured
with calipers ✓ · blower arrived + measured ✓ · camera placement decided ✓ · airflow
path checked ✓ · lens clearance checked ✓ · service/removal access checked ✓ → then
set the `.scad` parameters from the real measurements, render, **TP-print and verify
fit**, and only then production print.

## 7 · Battery-fit estimate (approximate — 2026-07-10 mesh probe)

Method: ray-cast probe of the two body-shell STLs alone (authored frames, no floor
offset, no assembly transform, no internal bosses). **Approximate only — a slicer
mesh measure is NOT battery compatibility.**

- `NEW BODY 2024 REAR` (forward half): interior clear width ≈ **99–120 mm**,
  centerline ceiling ≈ **61–70 mm** above the shell's bottom edge.
- `NEW BODY 2024 FRONT 1` (cockpit region, rear 40%): interior clear width ≈
  **50–105 mm**, ceiling ≈ **42 mm**.
- The floor is flat (8 mm bbox) — there is no deep printed "tub"; the bay is the
  shell interior above the floor.

**Reading:** the required **≤75×45×25 mm** pack clears width and height with margin
near the shells' junction (the "central floor tub" of the v2 packing plan). What the
probe **cannot** tell: usable bay **length** (bulkheads/bosses), wiring + XT60
connector clearance, retention (strap/velcro), and body install/removal path.
**Final battery choice stays blocked** until: (a) the §1 slicer assembly measure of
the actual pocket, then (b) physical confirmation on the printed floor + body.
Envelope ≤75×45×25 mm stands (designer's own limit in the body READ ME) unless the
assembled measure proves more room.
