# Coupon Print Plan — C-1 .. C-4

**Status: A2 is NOT-EXECUTED and Phase B is BLOCKED.** Nothing in this file
authorises a production print. All four coupons are TP-class: draft settings,
physically labelled `TP`, logged in [`../04_test_prints/`](../04_test_prints)
using the `TP-NNN-<short-name>.md` template from
[`../PRINT_LOG_TEMPLATE.md`](../PRINT_LOG_TEMPLATE.md), and **never installed on
the car** (risk **E-22**, [`fit_check_coupons.scad`](fit_check_coupons.scad):7-10).
No printer was used to produce this plan — printing is bench work for the owner.
`04_test_prints/` currently has zero entries (checked 2026-09-05: only its
`README.md`); the `TP-NNN` numbers below are **proposed**, not logged — log them
for real only after an actual print.

Source: [`fit_check_coupons.scad`](fit_check_coupons.scad) (all four modules),
[`w17_params.scad`](w17_params.scad) (provenance tags), and the study's §11
(cited in the coupon file's header). Print policy: [`../PRINT_SPEC.md`](../PRINT_SPEC.md)
§6 "Test / calibration prints" and [`../FIRST_PRINT_DECISION.md`](../FIRST_PRINT_DECISION.md)
"Diagnostic vs production prints".

All export commands below run from `11_cad/` with OpenSCAD 2026.09.01 (this
Mac's copy, confirmed identical at `/opt/homebrew/bin/openscad` and
`/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD` — both resolve to the same
44 290 208-byte binary):

```bash
cd 11_cad
openscad --backend=manifold -D 'coupon="cN"' -o out/C-N.stl fit_check_coupons.scad
```

(`render.sh` already exports the same four solids to `out/coupon_c1..c4.stl` as
part of its own naming scheme — this plan uses the bare `C-N.stl` name because
that is what a slicer import and a printed label should say.)

**Print settings baseline (all four coupons), per `PRINT_SPEC.md` §6:** 0.20 mm
layer height, 4 walls, 40% infill, no supports (every coupon is authored so its
tallest features are vertical-from-the-plate in the modelled orientation — pegs,
the register wall, the graduated steps — so slice as-is, do not rotate). Material:
PLA or PETG per the TP-class "any suitable filament" policy — **but if the
eventual cage/tray material has already been decided in
[`../MATERIAL_DECISION_MATRIX.md`](../MATERIAL_DECISION_MATRIX.md) (not read for
this plan), print C-1 and C-3 in THAT material specifically**, because their
whole purpose is calibrating this printer+filament combination's clearance and
confirming a fit — a different material can shift shrinkage and the measured
clearance. C-2 and C-4 are less sensitive to material (a height gauge and an S0
step gauge tolerate a substitute filament). Physically label every coupon `TP`
in permanent marker in addition to its embossed name — the raised/engraved text
identifies the coupon; the marker label is what stops it from being mistaken for
a production part on the bench (E-22).

Every coupon's read-out is designed to land directly in a
`MEASUREMENT_RECORD_SHEET.csv` row
(`id,param,quantity,unit,value,tolerance,photo_ref,notes` — the schema shared by
[`../tools/gen_measurement_sheet.py`](../tools/gen_measurement_sheet.py) and
[`tools/ingest_measurements.py`](tools/ingest_measurements.py)), so a coupon
result reaches `w17_params.scad` through the same reviewable dry-run/`--apply`
patch path as an owner caliper reading. **`param` is the mapping** — the exact
`w17_params.scad` parameter name, or empty for a register-only row; `quantity`
is prose and is never parsed for a parameter name (see the tool's docstring).

---

## C-1 — peg / hole tolerance ladder — **print this one first**

**Validates:** `fit_clearance` (§1 process constants) — the per-side print
clearance this printer and this filament need before a printed peg and a
printed hole of the same nominal size go together by hand. Every other
coupon, the cage's clip/peg fit, and the register wall's clearance all derive
from this one number ([`README.md`](README.md) "Order of operations").

**Params needed: none.** `clip_peg_d` (the peg diameter) and the seven ladder
steps `c1_steps` are `ESTIMATED` constants local to
[`fit_check_coupons.scad`](fit_check_coupons.scad):87,237 — not `ASSUMED (see
§9)` — so C-1 has no blocking dependency on anything the owner measurement
sitting produces. This is why it is the one coupon that can print today.

**Export (already run, OBSERVED 2026-09-05):**
```bash
cd 11_cad
openscad --backend=manifold -D 'coupon="c1"' -o out/C-1.stl fit_check_coupons.scad
```
Result: `Status: NoError` (manifold backend), **19 754 triangles**, bounding
box **106.0 × 28.0 × 12.0 mm**, file `out/C-1.stl` is **4 551 912 bytes**
(≈ 4.34 MiB). Matches the pre-existing `render.sh --table` entry for
`coupon_c1` exactly ([`README.md`](README.md) render table). `out/` is
gitignored and the repo's own `.gitignore` blocks `*.stl` everywhere, so this
file was not and will not be committed.

**Print settings:** as the baseline above. No supports — 7 pegs stand
vertical, 7 holes cut straight through a 4 mm plate.

**How to read it into a number:** try each of the 7 numbered peg/hole pairs by
hand, no tools, no force. Every peg is the same nominal `clip_peg_d` = 3 mm;
only the hole diameter varies, as `clip_peg_d + 2 × step`, for
`step ∈ {-0.15, -0.05, 0.05, 0.10, 0.15, 0.20, 0.30}` mm. The radial gap at
step *i* **is** `step_i` — no halving, no doubling, read the number straight
off. Record the **first** (smallest) step that assembles by hand and stays
put when shaken. Steps 1–2 are negative (hole smaller than peg); if either of
those goes together by hand, this printer/filament combo is running under
size — write that down as the result, do not force a larger step to "feel
right."

**Where this result goes.** `MEASUREMENT_RECORD_SHEET.csv` already holds a
**reserved row `C-1.1`** for it — the one row on the sheet that a printed part,
not a caliper, answers (`param = fit_clearance`, value blank until this coupon
is read). **Fill that row in; do not invent a new id.** Write the step number
into its `value` and name the coupon in its `notes`:

```
id,param,quantity,unit,value,tolerance,photo_ref,notes
C-1.1,fit_clearance,"RESERVED — per-side print clearance read off coupon C-1 …",mm,0.10,±0.05,,"TP-001 step 4: first step that fit by hand and stayed put when shaken; steps 1-2 (negative) did not fit"
```

(`0.10` above is a placeholder for whichever step the coupon actually reads —
fill in the real one.) Then run
`tools/ingest_measurements.py --sheet ../MEASUREMENT_RECORD_SHEET.csv` (dry run
first) to patch `fit_clearance` in `w17_params.scad`.

---

## C-2 — standoff height gauge

**Validates:** whether a printed standoff reaches its nominal height once the
first layer has squished and the part has shrunk — a process/consistency
check, not a single named design dimension.

**Params needed:** `screw_m3_clear_d` (§2 fastener family,
[`w17_params.scad`](w17_params.scad):71) — the standoff's bore diameter. Its
tag on that line reads `ASSUMED-adjacent`, not the literal `ASSUMED (see §9)`
this repo's tooling matches on — **but §9's own table lists it anyway**, grouped
with `insert_m3_d` / `insert_m3_h` under **C-1**
([`w17_params.scad`](w17_params.scad):370: `C-1 insert_m3_d / insert_m3_h /
screw_m3_clear_d`). That is an internal inconsistency worth knowing about (the
definition-line tag and the §9 table disagree on what retires it), not a
blocking one: either reading says the number is unconfirmed until a coupon
result is in. **Do not export C-2 as a production input yet** — it is not
technically gated by an `ASSUMED (see §9)` parameter the way C-3 is, but it
IS gated by the same clearance C-1 measures (a standoff bore is a peg/hole fit
in miniature), so reading it before C-1 risks reading squish/shrink error
confounded with an untuned clearance. Print it after C-1.

**Export (do not run yet — listed for when C-1's result is in hand):**
```bash
cd 11_cad
openscad --backend=manifold -D 'coupon="c2"' -o out/C-2.stl fit_check_coupons.scad
```
`render.sh --table` already confirms this renders clean today (11 500
triangles, 68.0×20.0×16.0 mm — see [`README.md`](README.md)); that is a
geometry check, not a print authorisation.

**Print settings:** baseline above. No supports — five standoffs on a flat
plate.

**How to read it into a number:** caliper each of the five pillar tops
(heights 4/6/8/10/12 mm) against the plate top. Pass is ±0.15 mm over all
five. If they are consistently short by the same amount, that offset is a
global correction applied to every standoff height in `w17_params.scad`
uniformly — **not** a fudge factor in one model. There is currently no single
named parameter this retires (no `standoff_height_offset` exists in
`w17_params.scad`); record it as a process-calibration row and decide with
the owner whether it becomes a new named `POLICY` constant.

**CSV row this produces** — a process check, not a §9 retirement, so `param` is
**empty** (register-only) and `ingest_measurements.py` will count it under `REG`
and patch nothing, which is correct and expected:
```
id,param,quantity,unit,value,tolerance,photo_ref,notes
TP-002-c2-offset,,"C-2 standoff height offset vs the plate top",mm,-0.10,±0.15,,"all five pillars ~0.10mm short; systematic, not per-height"
```

---

## C-3 — MH-ET hole pattern + edge slot

**Validates three things at once, with a real ESP32 board in hand:** (a) does
the board drop into the printed edge slot without bowing; (b) does the
assumed hole pattern actually line up; (c) do both clip stations land on bare
PCB or on a component. (c) is the one that decides whether the cage's
retention scheme survives — the board band is exactly one board thick
(AA §5.2), so the two clip stations necessarily stand in the outboard
component zone, and this coupon is where that gets confirmed or falsified.

**Params needed (all `ASSUMED (see §9)`):** `esp_hole_dx`, `esp_hole_dy`,
`esp_hole_d` (M-03, [`w17_params.scad`](w17_params.scad):152-154) and
`fit_clearance` (C-1, used at [`w17_params.scad`](w17_params.scad):59 and
consumed inside `coupon_c3()`'s hole-pattern cut,
[`fit_check_coupons.scad`](fit_check_coupons.scad):189). **Blocked** until
both M-03 (owner calipers the real board) and C-1 (this printer's
`fit_clearance`) have landed real numbers — printing C-3 against today's
placeholders would only test whether the placeholders happen to be right,
which is not what the coupon is for.

**Export (do not run yet):**
```bash
cd 11_cad
openscad --backend=manifold -D 'coupon="c3"' -o out/C-3.stl fit_check_coupons.scad
```
Renders clean today at 6 240 triangles, 59.0×48.6×17.0 mm
([`README.md`](README.md) table) — again a geometry check, not print
authorisation; re-render after `w17_params.scad` is patched with the real
M-03/C-1 values before printing.

**Print settings:** baseline above. No supports — the register wall, low
rail, and clip-station blocks are all extruded straight up from the plate.

**How to read it into a number:** with a real MH-ET board, (a) slide it into
the printed slot — pass/fail plus "how much it bowed" in mm if it did not sit
flat; (b) try to drop pins/pegs through the printed hole pattern onto the
board's actual holes — pass/fail plus the X/Y offset in mm if any hole
missed; (c) look at each clip-station block against the board's real
component layout — record "copper" or the name of whatever component it
lands on, at each of the two `clip_station_x` positions (10, 34 mm).

**CSV rows this produces.** `esp_hole_dx/dy/d` are already owned by sheet rows
**M-03d.1/.2/.3** — C-3 *confirms* them, it does not re-declare them. **One row
per parameter**: if you add a second row carrying the same `param`, the tool
reports `CONFLICT` and skips both. So a C-3 confirmation either goes into the
existing M-03d cell's `notes`, or is added register-only (`param` empty) as
below:
```
id,param,quantity,unit,value,tolerance,photo_ref,notes
TP-003-c3-holedx,,"C-3 cross-check of the hole pitch along the long edge",mm,33.2,±0.2,IMG_0xx,"confirms M-03d.1; if it disagrees, say which you trust"
TP-003-c3-holedy,,"C-3 cross-check of the hole pitch along the short edge",mm,24.8,±0.2,IMG_0xx,"confirms M-03d.2"
TP-003-c3-holed,,"C-3 cross-check of the hole diameter",mm,3.2,±0.1,,"pins dropped through cleanly at nominal; confirms M-03d.3"
TP-003-c3-slotfit,,"C-3 edge-slot fit (slot_w is ESTIMATED, not a §9 target)",mm,1.8,±0.2,,"board dropped in flat, no forcing"
TP-003-c3-clip1,,"C-3 clip station X10: what it lands on",note,copper,,IMG_0xx,"lands on bare PCB"
TP-003-c3-clip2,,"C-3 clip station X34: what it lands on",note,capacitor,,IMG_0xx,"lands on a component -- needs relocating"
```
(`clip_station_x_0/1` and `slot_w` are not `ASSUMED (see §9)` targets — they
will not be auto-patched by `ingest_measurements.py`; they are CAD decisions
for a human to act on directly in `w17_params.scad`, per this repo's "every
number is a named parameter" rule.)

---

## C-4 — S0 / deck-height stepped gauge

**Validates:** `s0_measured` — the height of the seated shell's bottom edge
above the floor top (DAT-F), the single measurement that decides whether the
second-floor cage can be built at all (README.md: "9.82 mm of an 11 mm
ceiling... a coin flip").

**Params needed: none, directly — this is worth flagging.** Reading
[`fit_check_coupons.scad`](fit_check_coupons.scad):232-254, `coupon_c4()`
only consumes the local constants `c4_steps` (a hardcoded `[2..11]` mm
array), `c4_step_l`, `c4_handle_l`, `c4_handle_t`, and the shared `label_h`
/ `label_size` / `label_font` constants — **none of which is an `ASSUMED
(see §9)` parameter**. `s0_measured` and `s0_upper_bound` are not referenced
by this module's geometry at all; the gauge's step range (2–11 mm) is an
independent literal chosen to span "the printable part of the 0..11 bound"
(the coupon's own comment), not computed from `s0_upper_bound`. So, strictly
by the "export only if inputs are non-ASSUMED" test, **C-4 could print
today** — unlike C-2 and C-3, its geometry does not depend on anything the
measurement sitting will change.

**This plan still does not export it as production, for a different reason:**
[`README.md`](README.md)'s stated order is C-1 → measurement session → C-2/C-3/C-4,
and using it at all requires the **real shell seated on the real floor**,
which is a bench-assembly step this session cannot perform or verify
(COMMON rule 1: no hardware). Printing it early costs nothing structurally,
but reading it needs the shell in hand regardless, so there is no gain to
jumping the queue — flagged here as an accurate finding, not acted on.

**Export (do not run yet, per the order above):**
```bash
cd 11_cad
openscad --backend=manifold -D 'coupon="c4"' -o out/C-4.stl fit_check_coupons.scad
```
Renders clean today at 10 616 triangles, 150.0×18.0×11.0 mm
([`README.md`](README.md) table); the model asserts its own correctness at
render time (digits engraved, not raised — see the file's C-4 header comment
for the bug this caught previously).

**Print settings:** baseline above. No supports — steps and handle are one
contiguous solid from the plate up; digits are engraved, not raised, so
nothing to support there either.

**How to read it into a number:** with the shell seated and only lightly
pressed (not clamped, not lifted), slide the gauge in from the side at **four
or more points** around the car. At each point, read the tallest step that
still slides under the shell edge. Record **all four (or more) readings**,
not just the smallest — the spread tells you whether the shell sits flat
(a shell that doesn't is a separate problem to solve before trusting any
single S0 number). The value that retires `s0_measured` is the **minimum**
across all points — the cage's clearance budget has to hold everywhere, so
the worst (tightest) point governs, matching this file's own convention for
`roof_z_worst` ("the worst finite shell roof sampled over BOTH board
seats").

**CSV rows this produces.** C-4 is the *instrument* for sheet rows **M-01.1–.5**;
the four point readings go into those existing cells (register-only), and the
governing minimum goes into **M-01.worst**, which is the single cell carrying
`param = s0_measured`. Do not create a second `s0_measured` row.
```
id,param,quantity,unit,value,tolerance,photo_ref,notes
M-01.1,,"S0 at forward, BELT side (L-) …",mm,7,±0.5,IMG_0xx,"read with C-4; gauge step resolution is 1mm"
M-01.2,,"S0 at forward, MIRROR side (L+) …",mm,8,±0.5,IMG_0xx,
M-01.3,,"S0 at rear, BELT side (L-) …",mm,6,±0.5,IMG_0xx,"tightest point -- governs"
M-01.4,,"S0 at rear, MIRROR side (L+) …",mm,8,±0.5,IMG_0xx,
M-01.worst,s0_measured,"S0 WORST (smallest) of the M-01 readings …",mm,6,±0.5,,"minimum of the four C-4 readings above; shell sits with ~2mm spread front-to-back"
```
(Only the final `s0_measured` row is an `ASSUMED (see §9)` target that
`ingest_measurements.py` will patch; the four `s0_point_*` rows are raw field
data, kept for the record per this repo's "write the datum down too" rule.)

---

## Summary — what actually happened in this session

| Coupon | Exported now? | Blocking `ASSUMED` inputs | Print order |
|---|---|---|---|
| C-1 | **yes** — `out/C-1.stl`, OBSERVED clean | none | 1st |
| C-2 | no | `screw_m3_clear_d` (tag says `ASSUMED-adjacent`; §9 table says C-1) | after C-1 |
| C-3 | no | `esp_hole_dx`, `esp_hole_dy`, `esp_hole_d` (M-03), `fit_clearance` (C-1) | after M-03 + C-1 |
| C-4 | no | **none directly** (flagged above); gated by needing the real shell, not by CAD params | after the measurement session, per README's stated order |
