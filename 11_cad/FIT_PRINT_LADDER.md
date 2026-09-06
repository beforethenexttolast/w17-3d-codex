# Fit-Print Ladder — the order of low-cost validation prints

**A2 stays NOT-EXECUTED and Phase B stays BLOCKED at every rung of this
ladder.** Nothing below authorises a production print, a shell cut, a hole in
a donor part, or any powered work — every part in this file is TP-class:
draft settings, physically labelled `TP`, logged in
[`../04_test_prints/`](../04_test_prints), never installed on the car
(risk **E-22**). The point of the ladder is the opposite of skipping steps:
each rung is small, cheap, and fails loudly enough on its own that a bad
number never survives to reach the next, more expensive print.

**Stop-rule discipline, stated once so every rung below can be short:** a
"STOP" at any rung means exactly that — do not print the next rung on
schedule while the failure is unresolved, do not substitute a "close enough"
number, and do not proceed to any second_floor_cage.scad print (`cage_body`,
`cage_all`, `cage_clip_print`) while a STOP is open anywhere above it in the
ladder. A rung that only partially fails still stops it — "the peg fits but
the wrong step" is a STOP on rung 1, not a partial pass.

---

## Rung 0 — C-1 peg/hole ladder

**What it's for:** calibrate `fit_clearance`, the one number every other rung
below depends on. Detailed in [`COUPON_PRINT_PLAN.md`](COUPON_PRINT_PLAN.md).

**Cost:** one small plate, ~2 g, no supports, prints in minutes.

**STOP if:** no step in the 7-step ladder assembles by hand and stays put
when shaken (reprint with a wider step range — the printer/filament is
outside the ladder's -0.15..+0.30 mm span), OR either of the two negative
steps (undersized holes) fits (this printer is running under size — report
it, do not silently pick a bigger step to "feel right"). Either way: do not
print rungs 1-5 below until a real `fit_clearance` is in hand, because the
cage's clip/peg fit and the register wall's clearance both derive from it.

---

## Rung 1 — the owner measurement sitting

**What it's for:** M-00 through M-20 (at minimum M-00, M-01 S0, M-02 steering
sweep, M-03 the board) — the caliper/scale/protractor session, no power, that
retires most of `w17_params.scad` §9's `ASSUMED` list. Full runbook: B1's
`MEASUREMENT_SITTING_RUNBOOK.md` (a sibling worker's deliverable, not this
one — see `w17-mechanical-measurement-session-prompt.md` for the underlying
21-row session this repo already has).

**Cost:** no printing, no filament — calipers, a rule, a depth gauge, a
protractor, kitchen scales.

**STOP if:** M-00 finds the shell does not physically exist (M-01, the S0
reading, cannot be taken at all — the cage stays a proposal, full stop, do
not print rungs 2-5), or M-02's steering sweep cannot be run (KO-01 stays
provisional — do not trust any cage clearance number that assumes a fixed
KO-01 band). A partial sitting (some M-rows measured, others not) is not a
STOP by itself — only the specific downstream rung that needed the unmeasured
row is blocked; see each rung's own gate below.

---

## Rung 2 — C-2 standoff height gauge

**What it's for:** confirm the printer's shrink/squish offset on standoff
heights before trusting any standoff dimension elsewhere. Detailed in
[`COUPON_PRINT_PLAN.md`](COUPON_PRINT_PLAN.md).

**Gate:** rung 0 (C-1) done. Not gated by rung 1 — `screw_m3_clear_d` is not
one of the M-nn caliper rows — but printed after rung 1 anyway, per
[`README.md`](README.md)'s stated order, since it uses the same
process-clearance reasoning as C-1 and there is no benefit to rushing it.

**Cost:** one small plate, five standoffs, ~3 g.

**STOP if:** any standoff reads outside ±0.15 mm of nominal in a way that
is NOT uniform across all five heights (a uniform offset is a correctable
process constant; a non-uniform one means something is wrong with cooling or
support-free bridging on this geometry, not just shrinkage — investigate
before trusting any standoff height in the tray or cage models).

---

## Rung 3 — C-3 board hole pattern + edge slot

**What it's for:** with a real MH-ET ESP32 board in hand, confirm the
assumed hole pattern lines up, the board drops into the edge slot without
bowing, and — the one that decides the cage's retention scheme — whether
both clip stations land on bare copper or on a component. Detailed in
[`COUPON_PRINT_PLAN.md`](COUPON_PRINT_PLAN.md).

**Gate:** rung 0 (`fit_clearance`) AND rung 1's M-03 (the real board's hole
pattern, thickness, USB connector type/edge) both landed real numbers in
`w17_params.scad` (via `tools/ingest_measurements.py`) and the file
re-rendered clean. Printing C-3 against today's placeholder values only
tests whether the placeholders happen to be right, which defeats the point.

**Cost:** one plate with a wall + rail + two clip-station blocks, ~5-8 g.

**STOP if:** the board does not drop in flat without bowing (the slot's
`slot_w`/`slot_lead_in` need revising before anything downstream trusts that
geometry), OR any hole in the pattern misses the board's real hole by more
than a hand-fit tolerance (re-caliper M-03 and re-patch, then re-print C-3 —
do not proceed on a "probably close enough" hole pattern), OR **either**
clip station lands on a component rather than bare PCB (this is the
retention-scheme gate: `clip_station_x` must move, and every downstream cage
print that includes a clip is blocked until it does).

---

## Rung 4 — C-4 S0 / deck-height gauge

**What it's for:** the single measurement that decides whether the
second-floor cage can be built at all — does the seated shell's real
clearance above the floor (S0) clear the 9.82 mm the cage's roof geometry
needs, out of an 11 mm hard ceiling. Detailed in
[`COUPON_PRINT_PLAN.md`](COUPON_PRINT_PLAN.md) (including the finding that
this coupon's own geometry has no blocking `ASSUMED` input — it is sequenced
here for the physical prerequisite, not a CAD one: reading it needs the real
shell seated on the real floor).

**Gate:** the real shell physically exists (checked at rung 1 / M-00) and is
available to seat on the floor. Not gated by C-1/C-2/C-3's results.

**Cost:** one stepped gauge with a handle, ~4-6 g.

**STOP if:** the minimum of four-or-more readings around the car comes back
**above 11.0 mm** (`s0_upper_bound` in `w17_params.scad`) — the cage as
currently designed cannot be built; this is a terminal gate for
`second_floor_cage.scad`, not a "print it anyway and see" situation. STOP
also if the four readings spread by more than a couple of millimetres — a
shell that does not sit flat is a separate problem (a warped shell, a floor
that is not flat, or a seating obstruction) that has to be solved before any
single S0 number can be trusted at all.

---

## Rung 5 — single tray fit slice (`esp_tray.scad`, `variant="shoe"`)

**What it's for:** the on-edge board carrier that goes in the car — a
sacrificial U-channel around the bare PCB edge, so service cycles abrade the
shoe rather than the ESP32
([`esp_tray.scad`](esp_tray.scad):21-29). Its own header states the gate
plainly: *"Coupon C-3 with a real board decides whether the shoe is
affordable at all — if it is not, the cage grips the bare PCB and this file
stays a bench tray."* This is the first rung that prints a real vehicle-part
candidate rather than a test coupon, but it is still TP-class until a
production gate formally clears it.

**Gate:** rung 3 (C-3) passed clean with no STOP — meaning the board fits
the slot AND both clip stations are confirmed on bare copper — because the
shoe's wall thickness eats further into the same 13 mm board band C-3 just
confirmed has nothing spare
([`esp_tray.scad`](esp_tray.scad):27-29). Also needs `esp_len` / `esp_wid` /
`esp_pcb_t` to be more than `DOCUMENTED`-for-the-SKU-class if any doubt
remains from M-03 (they are currently accepted as documented, not flagged
`ASSUMED`, but M-03's real board measurement is the check that would catch a
SKU mismatch).

**Export:**
```bash
cd 11_cad
openscad --backend=manifold -D 'variant="shoe"' -o out/esp_shoe.stl esp_tray.scad
```
Renders clean today at 200 triangles, 39.4×5.2×6.6 mm
([`README.md`](README.md) table) — small enough that "print it and see" is
cheap, but the gate above still has to hold first, because a shoe printed
against an unconfirmed board band just wastes the print confirming what C-3
already would have told you for less filament.

**Cost:** ~1 g, single small part.

**STOP if:** the shoe does not slide onto the real board's edge with the
`fit_clearance` from rung 0, or the shoe's own wall thickness measured on
the print pushes the total (board + shoe) band width past the 13 mm the
cage's register wall was designed around — that is a direct conflict with
`board_l_out - board_l_in >= esp_thk_headers` (`w17_params.scad`'s own
`assert()` at §10), and the shoe becomes a bench-only tray, not a vehicle
part, per its own header.

---

## Rung 6 — cage section (`second_floor_cage.scad`, one clip or `cage_body`)

**What it's for:** the first print of the actual cage geometry — not the
full `cage_all`, but the smallest committing slice: either a single printed
clip (`part="clip_print"`, the print-orientation plate, **not**
`part="clip"` which is the installed-view orientation and would print four
towers with their layer lines across the crash load —
[`README.md`](README.md) "second_floor_cage.scad" row) or the bare
`cage_body` (the register wall + rails + guide, without the clips), to
confirm the register-wall clearance and the PDB drop-in fit before
committing filament to the full assembly.

**Gate:** every STOP above is clear — rung 0 (`fit_clearance`), rung 1's
M-01/M-02/M-03, rung 3 (C-3, clip stations confirmed on copper), and rung 4
(C-4, S0 ≤ 11 mm, so `s0_required` from AA §5.3 actually holds) all resolved
with real numbers patched into `w17_params.scad` via
`tools/ingest_measurements.py` and the file **re-rendered clean** (all eight
`assert()`s in `w17_params.scad` §10 still pass, plus `render.sh`'s own
`check_max_z` reading the exported `cage_all` solid). This is the rung where
a still-open STOP anywhere above actually bites: printing a cage section
against an unresolved S0 or an unconfirmed clip station is exactly the
mistake this ladder exists to prevent.

**Export (clip, print orientation):**
```bash
cd 11_cad
openscad --backend=manifold -D 'part="clip_print"' -o out/cage_clip_print.stl second_floor_cage.scad
```
**Export (bare cage body, no clips):**
```bash
cd 11_cad
openscad --backend=manifold -D 'part="cage"' -o out/cage_body.stl second_floor_cage.scad
```
Both render clean today (`cage_clip_print` 960 triangles, 32.0×44.8×6.0 mm;
`cage_body` 2182 triangles, 45.0×86.0×30.0 mm — [`README.md`](README.md)
table) — again a geometry check against today's placeholder numbers, not a
print authorisation; re-render after every gate above is patched with real
values before printing.

**Cost:** `cage_clip_print` is a few grams; `cage_body` is the first
print in this ladder with real material cost (tens of grams) — the last one
to spend filament on before the whole cage is on the table.

**STOP if:** the PDB does not drop into the register wall by hand (the
cassette is a lift-out assembly — an interference fit here is a design
failure, not a "tap it in" situation), the clip does not seat flush at
`board_top_z` (anything proud of the board top reopens the 9.82→12.82 mm
failure mode `w17_params.scad`'s own comments describe), or any `assert()`
in `w17_params.scad` fired during the pre-print re-render (should never
reach the printer — the render would have already failed loudly).

**After rung 6 passes clean:** this ladder ends here. `cage_all` (the full
assembly, all four clips) and anything beyond it is a production-print
decision for the owner, gated by A2 and Phase B exactly as before — no rung
in this file, including a clean rung 6, changes that gate.
