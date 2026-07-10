# First Print Decision — do this before anything touches the printer

Working checklist from the 2026-07-10 pre-print audit, **revised the same day after
the gate-review pass** (drawings `[0][1][2][3][5][7]` read, `docs/bill_of_materials_v2.md`
+ wiring atlas added, DRS reinstated, hardware ordered). Sources of truth stay where
they are (`PRINT_SPEC.md`, `MODEL_INVENTORY.md`, `MATERIAL_DECISION_MATRIX.md`,
`BUILD_SHEET.md`) — this file is the execution order. Check items off here; record
outcomes in `GENERAL_PLAN.md` open questions and the logs.

## Status snapshot (2026-07-10, second pass)

- **Resolved on paper:** Gate B *front* (nose + front wing are separate REQUIRED
  parts), Gate D (`Servoholder` is the floor-mounted steering-servo holder).
  Required count now **40**, all staged with manifest rows.
- **Open:** Gate A (rear stack) ⟷ rear-wing/DRS gate — one coupled slicer decision;
  Gate C (camera on hand, blower in transit); final battery choice.
- **Hardware:** tyres, bearings, shocks, servos, king pins, sleeves, inserts, belt set
  **ordered — in transit**. Calipers **on hand**. Camera **on hand** (flashed).
  Battery **not selected** (envelope ≤75×45×25 mm holds until geometry says otherwise).

## The decision (TL;DR)

1. **Print now (nothing blocks these):** Bambu demo → **PLA coupon** → **PETG coupon**
   (dry the spool first). Calipers are here — measure and log both as TP entries.
2. **Do the coupled rear decision in Bambu Studio** (§1) — Gate A + rear wing + DRS in
   one sitting. Zero filament, unblocks the whole ASA batch plan.
3. **Print after coupons measure OK:** the wheel fit set (§3) — the *print* isn't
   blocked, but its verdict (FIT entries) **waits for tyres + bearings to arrive**.
4. **Everything ASA, the floor batch, and the wing wait** — on the rear gate, the
   servo fit-check, and the wing choice respectively.
5. **Battery:** decide only after the floor tub + body interior can be measured
   (slicer measure now, printed parts later). Keep ≤75×45×25 mm as the constraint.

---

## 1 · Slicer inspection checklist (no filament, ~1 evening)

Import from `02_ready_to_slice/` (never from `unsorted_stl_raw/`, except view-only
peeks at gated candidates). Use **Measure** or the size panel; write outcomes down.

**The coupled rear decision — Gate A + rear wing + DRS (one sitting):**
- [ ] Open `Spring mount 2 REVISION 1.stl` (view-only from raw). Does its rocker seat
      the **68 mm** coilover (compare the ordered HSP shock's eye-to-eye)?
- [ ] **If yes (Rev-1 stack, drawing `[7]`):** plan = `Spring mount 2` + `Spring
      Block` + 3× `Motor Cover REVISION 1` + `Diffuser backplate`. ⚠ Check whether
      the Motor Covers **replace** `Left/Rightrearaxle` (the bearings seat in the
      covers in `[7]` — don't print the holders if so). Identify which small STL is
      `[7]`'s "Light Cover" vs "Diffuser" (we have `rearbacklightdiffuser`, the floor
      `Diffuser`, `Diffuser backplate`). Wing candidate: **`MCL60 2023 Rear Wing`**
      (+ `DRS Arm for 2023`).
- [ ] **If no (original stack, drawing `[2]`):** plan = `RearSpringMountREV4` +
      `springblock` + `Left/Rightrearaxle` as staged. Wing candidate:
      **`2021Rearwing with DRS`** (+ `DRS Arm for 2021`, optional flap deco), which
      `[2]` shows with its DRS-servo pocket and metal-rod linkage.
- [ ] **Wing beauty contest:** also open `Print_In_Place DRSv2` (newest DRS design,
      but undocumented + print-in-place hinge risk). Pick by W17 realism + mount
      compatibility with your chosen stack. Check `DRS Diffuser` vs the required
      `Diffuser` once the wing is picked. **Escalation rule: the wing file only moves
      to REQUIRED after you've eyeballed the mount interfaces mate.**
- [ ] While there: confirm from `[7]`/photos whether both motor locks
      (`beltdrivemotorlock` + `newgearmotorlock`) are used — BOM v2 names only the
      belt one. And `Axle Main no grubs` role — note the belt set already **includes
      a metal rear output shaft** (BOM v2 §8), so a printed axle part may be redundant.

**Body group confirms (fast — the decisions are already made):**
- [ ] Shell + `FRONTNOSE2024` + `2024 Revised Front Wing` together in the slicer: no
      duplicated geometry, mounting holes line up (nose bolts to the front floor per
      the body READ ME).
- [ ] `camera top 1.1` mates with the 2024 shell (it's a Rev-1-era part).
- [ ] `pin.stl`: confirm no pin holes remain anywhere (M3-bolted body) → then it can
      be formally rejected.
- [ ] Mirror `Front_Right_Wheel_Hub_2022_F104`, measure the mirrored bearing seat
      (Ø12 pocket for 8×12×3.5).
- [ ] Floor: all 8 group-05 files (incl. `Servoholder`) against drawing `[2]` — the
      drawing shows Front Floor, Rear Floor, Rear Floor 2, Floorboard, 2 Side Vents,
      Diffuser, Servo Holder. Anything unmatched?
- [ ] King-pin knuckle bore ≈ 3 mm (M3×30 dowel pins ordered).
- [ ] Battery tub: measure the floor's battery bay in the slicer — does ≤75×45×25 mm
      hold? Record the real numbers for the battery purchase.
- [ ] Slicer error check on every staged file; note anything red in the inventory.

Gate outcomes → update `MODEL_INVENTORY.md` + `inventory.csv` (via
`01_inventory/build_inventory.py`) + `REVIEW.md` together; stage newly-required files
with MANIFEST rows.

## 2 · Hardware — ordered, in transit, on hand

Everything from BOM v2 is **ordered** (AliExpress ~40 lines + rcMart tyres). Nothing
left to buy except the **battery** (deliberately last — see §1 battery-tub measure)
and paint/decal consumables (Phase 8-9, not urgent).

| Arrives → unblocks | Items |
|---|---|
| Wheel FIT verdicts | Tamiya 54198 + 51400 tyres, MR128ZZ front bearings, 6801 rear bearings |
| Gate A physical confirm + rear assembly | 68 mm HSP rear shock, 52 mm front shocks, belt set (incl. metal output shaft), pinion + spur, aluminium tube (cut 4× 14 mm spacers) |
| Servo fit-checks (floor batch + DRS pocket) | DS3235SG steering servo, 3× MG90S (pan/tilt/DRS) |
| Steering assembly | king pins, ball studs, rod ends, turnbuckles, M4 rods, M3 kit, inserts, sleeves |
| Camera duct render (Gate C, other half) | ACP2006-class 5 V blower (camera itself is on hand — measure it now) |

**On hand already:** digital calipers ✓ · camera (flashed) ✓ · all filament ✓ ·
printer ✓. **On arrival:** measure front shocks (51 vs 52 mm question), verify
spur ↔ belt-pulley bolt pattern (BOM v2 open confirmation #1).

## 3 · First prints, in order (what to open in Bambu Studio)

Workflow details per step: `PRINT_SPEC.md`. Log every one: TP-NNN in `04_test_prints/`.

0. **Bambu demo print** (pre-sliced, from the printer's own menu/SD). Proves the
   machine itself. **Nothing blocks this — today.**
1. **TP: PLA coupon** — 25×25×10 mm cube + Ø12 negative cylinder 4 mm deep (bearing
   seat) + Ø3 negative through-hole (M3). 0.20 mm, 4 walls, 40% gyroid. Measure with
   the calipers, write numbers down. **Nothing blocks this.**
2. **TP: PETG coupon** — same model, PETG HF spool: **dry first** (60–65 °C, 6–8 h),
   cap outer walls ~150 mm/s. This one calibrates the wheel prints. **Nothing blocks
   this.**
3. **TP: wheel fit set (PETG)** — 1× front rim + 1× front hub + 1× front locking nut
   (thread axis vertical) + 1× rear rim + 1× of each tyreslot adapter. Print once the
   PETG coupon measures sane; the **FIT verdicts wait for tyres + bearings to arrive**
   (note: per drawing `[7]` the adapters were designed against Tamiya F104 rim
   geometry — the printed rims emulate it; that's exactly what the fit test checks).
4. **TP: body wall slice** (2–3 cm slicer-cut of a shell, 0.12 mm PLA matte) — the
   look test + later the primer/paint test card. Printable any time; needed before
   Phase 8.
5. **TP: ASA coupon** — immediately before the group-02 batch (which itself waits on
   the resolved rear gate). Ventilation drill: enclosed, room door closed, ventilate
   during + after, parts cool in the chamber. Fallback if ASA fights you twice: PETG
   + metal sleeves + heat check, logged as an MD deviation.

## 4 · Blocked / unblocked map

**Print now:** demo print · PLA coupon · PETG coupon · body wall slice.

**Print after coupons only:** wheel fit set (its *verdict* still waits on parts).

**Blocked until the slicer sitting (§1):** the whole ASA rear batch (Gate A decides
*which files* — possibly not the staged axle holders!) · rear wing + DRS arm (file
choice) · `Diffuser backplate` · formal rejection of `pin.stl`.

**Blocked until parts arrive:** wheel/bearing/tyre FIT entries · floor batch
(DS3235SG fit-check into `Servoholder` pocket) · DRS pocket check (MG90S) ·
Gate A physical confirmation (68 mm shock in hand) · spacer cutting (aluminium tube).

**Blocked until measured:** camera duct render (camera measurable **now**, blower in
transit) · battery purchase (slicer-measure the tub in §1, confirm with printed floor).

**Not yet, regardless:** body shells / halo / nose / front wing (after wall-slice test
+ paint plan, watched first hour) · remaining 3 rims + mirrored hub (after fit set
passes) · optionals (driver figure etc. — after the car).

## 5 · Top open risks

1. **The rear stack ambiguity now includes required files:** if Gate A lands on the
   Rev-1 path, the staged `Left/Rightrearaxle` may be replaced by the Motor Covers
   (drawing `[7]`) — don't print any group-02 part before the §1 sitting.
2. **Wing choice is aesthetic + mechanical at once** — a wrong pick costs a reprint
   and possibly a DRS re-rig; do the beauty contest with the mount interfaces visible.
3. **Servo fitment is assumed, not confirmed** (DS3235SG is the same size class as
   Ryan's DSServo 35KG; MG90S is the classic micro) — measure both on arrival before
   the floor batch and the wing print.
4. **HF PETG at speed is weaker** — the ~150 mm/s wall cap in `PRINT_SPEC.md` §2 is
   mandatory for suspension parts.
5. **Atlas caveats:** `docs/w17_wiring_assembly_atlas.html` predates BOM v2 — its
   "12 mm hex" wheel note and "51 mm" front shocks are stale (printed rims use
   tyreslot adapters + M4 bolt; 52 mm shocks ordered). Trust BOM v2 + this repo's
   docs for mechanics; the atlas for wiring.
