# Measurement record sheet — print this

**Sitting date: ____________  ·  Instrument (calipers, make/model): ____________________  ·  Scale: ____________________  ·  Recorded by: ____________**

**No power. No battery. No USB into a live port. Nothing forced, cut, drilled, filed or glued.**
**A2 stays NOT-EXECUTED and Phase B stays BLOCKED whatever the numbers say.**

Order and rationale: [`MEASUREMENT_SITTING_RUNBOOK.md`](MEASUREMENT_SITTING_RUNBOOK.md).
Machine-readable twin: [`MEASUREMENT_RECORD_SHEET.csv`](MEASUREMENT_RECORD_SHEET.csv) —
**both files are generated from one row list, so they cannot drift.**

**A measurement you could not take is a result:** write `could not — <why>` in the Value box.
Never estimate to fill a cell. Photo refs are filenames under
`08_reference_photos/YYYY-MM-DD_<what>.jpg`.


---

## Station 0 — What actually exists (M-00)

### M-00.g02 — Group 02 — Rear axle + drivetrain (ASA) (8 files): none / some / all, then WHICH parts

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the group as laid out.  **Photo ref:** `______________`
- Condition per part: good / warped / layer split / supports still on / TP / unknown material. Unknown material or settings = a DIAGNOSTIC part, not a build part.

### M-00.g03 — Group 03 — Front suspension + steering (PETG) (8 files): none / some / all, then WHICH parts

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the group as laid out.  **Photo ref:** `______________`
- Condition per part: good / warped / layer split / supports still on / TP / unknown material. Unknown material or settings = a DIAGNOSTIC part, not a build part.

### M-00.g04 — Group 04 — Wheels (PETG) (7 files): none / some / all, then WHICH parts

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the group as laid out.  **Photo ref:** `______________`
- Condition per part: good / warped / layer split / supports still on / TP / unknown material. Unknown material or settings = a DIAGNOSTIC part, not a build part.

### M-00.g05 — Group 05 — Floor (PETG) (8 files): none / some / all, then WHICH parts

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the group as laid out.  **Photo ref:** `______________`
- Condition per part: good / warped / layer split / supports still on / TP / unknown material. Unknown material or settings = a DIAGNOSTIC part, not a build part.

### M-00.g06 — Group 06 — Body shell (PLA matte black) (7 files): none / some / all, then WHICH parts

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the group as laid out.  **Photo ref:** `______________`
- Condition per part: good / warped / layer split / supports still on / TP / unknown material. Unknown material or settings = a DIAGNOSTIC part, not a build part.

### M-00.g07 — Group 07 — Brake-light diffuser (1 files): none / some / all, then WHICH parts

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the group as laid out.  **Photo ref:** `______________`
- Condition per part: good / warped / layer split / supports still on / TP / unknown material. Unknown material or settings = a DIAGNOSTIC part, not a build part.

### M-00.g99 — OPTIONAL / UNCERTAIN / anything else printed

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Name them; do not fold them into a REQUIRED group.

### M-00.p1 — Does `Servoholder.stl` exist? condition?

- **Unit:** yes/no + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Called out by name because it gates M-28, the ~1.7 mm steering-servo interference (OP-B).

### M-00.p2 — Does `FloorBoard2.stl` exist? condition?

- **Unit:** yes/no + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Called out by name because it gates M-20, the three centreline splice screws (OP-G).

### M-00.p3 — Does `2023NewFrontFloorLargerParts.stl` exist? condition?

- **Unit:** yes/no + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Called out by name because it gates M-20 and the floor datum DAT-F itself.

### M-00.p4 — Does `NEW BODY 2024 REAR.stl (+ FRONT 1)` exist? condition?

- **Unit:** yes/no + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Called out by name because it M-01 needs a shell to seat — no shell, no S0, cage stays a proposal.

### M-00.p5 — Does `2023NEWSideVent1/2.stl` exist? condition?

- **Unit:** yes/no + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Called out by name because it gates M-15, the charge-flap candidate CF-1.

### M-00.p6 — Does `2021Rearwing with DRS.stl + DRS Arm for 2021 Rear Wing.stl` exist? condition?

- **Unit:** yes/no + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Called out by name because it gates M-14, the DRS linkage.


---

## Station 1A — MH-ET D1-Mini ESP32 (bench, calipers)

### M-03a.1 — Bare PCB length (jaws on FR4 edges)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_len. STOP if outside 39 x 31 +/-1: not the planned SKU.

### M-03a.2 — Bare PCB width

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_wid.

### M-03b — PCB thickness on a bare edge

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_pcb_t; slot_w derives from it. Expect 1.6.

### M-03c — TOTAL thickness with headers fitted, at its thickest (incl. tallest underside tail)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_thk_headers. STOP if > 13.0 — the assert at w17_params.scad:391 fires and the cage design stops.

### M-03d.1 — Mounting-hole pitch, X (centre to centre)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_hole_dx.

### M-03d.2 — Mounting-hole pitch, Y

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_hole_dy.

### M-03d.3 — Mounting-hole diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_hole_d. If there are no holes at all, say so.

### M-03e — WHICH EDGE carries the service port: long or short, and which end

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the port edge with silkscreen legible.  **Photo ref:** `______________`
- esp_usb_edge; decides the clip notch. Port on a LONG edge changes the wall-seat service face.

### M-03f.1 — WHICH CONNECTOR it actually is: USB-C / micro-USB B / other

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the connector, shell shape readable.  **Photo ref:** `______________`
- esp_usb_type. CLOSES OP-I. micro-USB rewrites AA 4.7 service story and 5.6 clip-notch rule, not just a hole size.

### M-03f.2 — Connector shell width

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_usb_w.

### M-03f.3 — Connector shell height

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_usb_h.

### M-03f.4 — Connector protrusion past the PCB edge

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- service opening depth.

### M-03f.5 — Connector offset from that edge's centreline

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_usb_offset.

### M-03g.1 — With a DEAD cable fitted: plug-body projection past the PCB edge

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Service access; KO-34. The cable's far end connects to NOTHING.

### M-03g.2 — Cable minimum bend radius before the plug is levered

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Service access at the X+42..+46 tongue.

### M-03h.1 — Component-free margin from the FORWARD short edge (outboard face)

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- OP-H / clip stations.

### M-03h.2 — Component-free margin from the AFT short edge (outboard face)

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- OP-H.

### M-03h.3 — Component-free margin from the INBOARD long edge (outboard face)

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- OP-H.

### M-03h.4 — Component-free margin from the OUTBOARD long edge (outboard face)

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the outboard face flat-on with a rule alongside.  **Photo ref:** `______________`
- OP-H. STOP if no bare land at X+10 or X+34 — clip_station_x [10,34] stands on components.

### M-03x.1 — Board #2: length and thickness-with-headers (cross-check)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- If any board differs by more than the tolerance they are not one SKU: take every M-03 row per board.

### M-03x.2 — Board #3: length and thickness-with-headers (cross-check)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Same.

### M-03i — OPTIONAL: adjacent header pin pairs read off the silkscreen

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: both silkscreen edges, every label readable.  **Photo ref:** `______________`
- A2 review F12 + open finding F20. Do NOT let this delay the M-04 verdict.

### M-04 — Female header + MH-ET male pins, SEATED: total stack height

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esp_socket_stack. GO/NO-GO on socketing vs S0 >= 9.82. NO-GO = STOP, do not solder; F12 reopens. Marginal is a report, not a judgement. Needs a female header from stock.


---

## Station 1B — PDB components and connector bodies (bench, calipers)

### M-05a.1 — 1000 uF electrolytic: body diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- pdb_stack_h candidate.

### M-05a.2 — 1000 uF: height above the SEATING PLANE (not lead tips)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- pdb_stack_h candidate.

### M-05a.3 — 1000 uF: lead length below the body

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Board planning.

### M-05b.1 — XT60 body L x W x H, as it will lie on the board (male)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- pdb_stack_h candidate; KO-33 dock body.

### M-05b.2 — XT60 body L x W x H (female)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-33 dock body.

### M-05c.1 — XT90-S anti-spark FEMALE half: body L x W x H

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- pdb_stack_h candidate; the half that faces the live pack.

### M-05c.2 — XT90H-M male half: body L x W x H

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-05c.3 — Mated overall length of the pigtail pair

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Finger access body-on.

### M-05c.4 — PULL AXIS: which way the finger pulls

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the mated pair with an arrow on tape along the pull axis.  **Photo ref:** `______________`
- Charge/run interlock ritual (F9a/F9b).

### M-05d — TALLEST PDB PART = max(M-05a.2, M-05b, M-05c, 9.1 UBEC MEASURED). Write the arithmetic

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- pdb_stack_h. STOP if > 13: PDB audit top Z14 vs KO-01 bottom Z22 is the 8 mm policy with nothing spare. Report; do not re-plan the cage at the bench.

### M-06 — PDB finished outline, mounting holes, connector exits

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — the PDB does not exist; no substrate bought. Built at A2 build week, and its outline is a DESIGN OUTPUT, not a measurement. pdb_len/pdb_wid stay ASSUMED. Do not cut a pocket to 55 x 45.

### M-21.a — XT30: body L x W x H, and MATED depth (pair plugged together)

- **Unit:** mm (LxWxH; mated)  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-33 dock bodies; M connector matrix; Z wire schedule. Sanity-checks pass_slot_w/h (10 x 6).

### M-21.b — 3-pin servo (JR): body L x W x H, and MATED depth (pair plugged together)

- **Unit:** mm (LxWxH; mated)  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-33 dock bodies; M connector matrix; Z wire schedule. Sanity-checks pass_slot_w/h (10 x 6).

### M-21.c — JST-XH 3-pin: body L x W x H, and MATED depth (pair plugged together)

- **Unit:** mm (LxWxH; mated)  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-33 dock bodies; M connector matrix; Z wire schedule. Sanity-checks pass_slot_w/h (10 x 6).

### M-21.d — JST-XH 4-pin: body L x W x H, and MATED depth (pair plugged together)

- **Unit:** mm (LxWxH; mated)  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-33 dock bodies; M connector matrix; Z wire schedule. Sanity-checks pass_slot_w/h (10 x 6).

### M-21.e — JST-XH 5-pin: body L x W x H, and MATED depth (pair plugged together)

- **Unit:** mm (LxWxH; mated)  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-33 dock bodies; M connector matrix; Z wire schedule. Sanity-checks pass_slot_w/h (10 x 6).

### M-21.f — JST-PH 2-pin: body L x W x H, and MATED depth (pair plugged together)

- **Unit:** mm (LxWxH; mated)  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-33 dock bodies; M connector matrix; Z wire schedule. Sanity-checks pass_slot_w/h (10 x 6).

### M-21.g — U.FL head + pigtail diameter: body L x W x H, and MATED depth (pair plugged together)

- **Unit:** mm (LxWxH; mated)  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-33 dock bodies; M connector matrix; Z wire schedule. Sanity-checks pass_slot_w/h (10 x 6).

### M-21.h — camera<->WiFi shielded 4-pin / micro-USB: body L x W x H, and MATED depth (pair plugged together)

- **Unit:** mm (LxWxH; mated)  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-33 dock bodies; M connector matrix; Z wire schedule. Sanity-checks pass_slot_w/h (10 x 6).


---

## Station 1C — Process and fastener stock (bench, calipers)

### M-22a.1 — Heat-set insert M3x5: outside diameter at the widest knurl

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- insert_m3_d (4.0 ASSUMED). STOP if outside 4.0 +/-0.2 — every insert boss in lib/w17_lib.scad changes.

### M-22a.2 — Heat-set insert M3x5: overall length

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- insert_m3_h (5.7 ASSUMED).

### M-22b.1 — M3 screw: thread outside diameter

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- screw_m3_clear_d (3.4).

### M-22b.2 — M3 screw: button-head diameter

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- screw_m3_head_d (6.0). > 6.0 undersizes every counterbore.

### M-22b.3 — M3 screw: head height

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Counterbore depth.

### M-22c.1 — Cable tie: strap width

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- zip_slot_w (4.0). > 3.5 leaves under 0.5 mm dressing room.

### M-22c.2 — Cable tie: strap thickness

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- zip_slot_l (2.5).

### M-22c.3 — Cable tie: head thickness

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Clearance under the base plate.

### M-22d — OPTIONAL (needs wire stock): OD of a dressed 4-way silicone bundle

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Sanity for pass_slot_w/h (10 x 6) and tail_hole_d (8.0), all ESTIMATED.


---

## Station 1D — Other on-hand parts (bench, calipers)

### M-16.1 — IP2326 charge module: body length

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- chg_l. STOP if any axis exceeds the 30 x 25 x 10 cell.

### M-16.2 — IP2326: body width

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- chg_w.

### M-16.3 — IP2326: body height

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- chg_h.

### M-16.4 — IP2326: mounting-hole positions and diameter (if any)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- ASM-59 seat.

### M-16.5 — IP2326: which edge carries the onboard Type-C, and its protrusion

- **Unit:** mm + text  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- CF-1/CF-6 flap decision.

### M-16.6 — IP2326: which face gets hot

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Thermal face; no pocket may be cut before this row.

### M-16.7 — IP2326: where the leads exit

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-16.8 — IP2326: is the state LED on the board (light-pipe) or can it fly on two wires?

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: both faces, silkscreen legible.  **Photo ref:** `______________`
- CLOSES OP-C. The photo is also the evidence this is a genuine BALANCING charger, not boost+CV. Two sources conflict (29x26x6 vs 18.3x31 in a <=10 mm cell) and NEITHER is a caliper record.

### M-11a — ESC: full label text / variant, transcribed exactly

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the label, sharp, all of it.  **Photo ref:** `______________`
- Retires the on-hand identity ASSUMPTION. STOP if it is not QuicRun 10BL120 G2 Sensored — the measured 44.2x33.7x34.0 body belongs to another part.

### M-11c — ESC: foot / mounting-tab centres and tab hole diameter

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- esc_* install envelope; the OP-A relocation search. Record 'no tabs' if tape-mounted.

### M-11d — ESC: which face each lead exits (battery in, 3 phase, signal) and each free length

- **Unit:** mm + text  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the ESC with all leads laid out flat.  **Photo ref:** `______________`
- KO-20 install envelope; N cable routing.

### M-14b.1 — MG90S: body L x W x H

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- STOP if it differs from documented TowerPro 22.8 x 12.2 x 28.5 by > 0.5 — these are clones and every pocket is sized wrong.

### M-14b.2 — MG90S: mounting-ear pitch

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Pocket geometry.

### M-14b.3 — MG90S: ear hole diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-14b.4 — MG90S: boss height above the case

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-14b.5 — MG90S: spline height and tooth COUNT

- **Unit:** mm + count  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Horn compatibility.

### M-14b.6 — MG90S: lead exit face

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Pocket orientation; DRS lead route.

### M-14c — MG90S horn radii actually supplied, per hole, from the spline centre; and how many horns per servo

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- DRS throw arithmetic with M-14d. If no horns came, M-14d/e/f cannot close.

### M-14g1.1 — Rod-end (M4 ball joint): ball diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- DRS + steering linkage.

### M-14g1.2 — Rod-end: thread size / pitch

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-14g1.3 — Rod-end: ball-centre to thread-end distance

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Sets usable rod length with M-14g2.

### M-18a.1 — Speaker: cone diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- spk_* residual. NOTE: outline is already MEASURED 35.3 x 25.1 x 6.1 — the part is RECTANGULAR, not a round basket. Record the shape as found.

### M-18a.2 — Speaker: mounting-hole pattern and diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- PS-14 / KO-28 baffle.

### M-18a.3 — Speaker: total depth including the magnet

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Sidepod pocket depth.

### M-23.1 — Camera: PCB length

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Gate C / D-06 / D-34. No camera mount CAD until every M-23 row exists.

### M-23.2 — Camera: PCB width

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-23.3 — Camera: PCB thickness

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-23.4 — Camera: heatsink envelope L x W x H

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-23.5 — Camera: lens outside diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Duct interface; FOV opening.

### M-23.6 — Camera: lens axial length

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-23.7 — Camera: lens axis offset from the PCB centre (both axes)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Boresight; KO-24.

### M-23.8 — Camera: mounting-hole pattern and diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-23.9 — Camera: cable-exit face and direction

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Service pull.

### M-23.10 — Camera: total axial depth, lens tip to heatsink back

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: camera identity photo + one square-on shot of the lens face.  **Photo ref:** `______________`
- STOP if it disagrees with the owner ground truth 19.2 x 19.2 transverse x 30.7 axial by > 1 mm — the documented body reference is then the wrong unit.

### M-24.1 — Wi-Fi antenna: whip length

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-26 routing reserve. Expect ~70 mm.

### M-24.2 — Wi-Fi antenna: U.FL head body dimensions

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-24.3 — Wi-Fi antenna: pigtail coax diameter

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-24.4 — Wi-Fi antenna: minimum bend radius before the coax kinks

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-26 wants >= 10 mm coax bend.

### M-25.1 — FRONT shock: eye-to-eye length

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- D-12 — resolves the 51 mm requirement vs 52 mm received-stock-label conflict. If it is neither, report both.

### M-25.2 — FRONT shock: body diameter

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-04 swept cylinder.

### M-25.3 — FRONT shock: fully compressed length

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Stroke = eye-to-eye minus this.

### M-25.4 — FRONT shock: spring OD and free length

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-25.5 — REAR 68 mm shock: eye-to-eye length

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-06 — the central shock in the electronics spine.

### M-25.6 — REAR shock: body diameter

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-25.7 — REAR shock: fully compressed length

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Feeds M-14h (swept arm vs shock at full compression).

### M-25.8 — REAR shock: spring OD and free length

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-26.1 — Spur: tooth count

- **Unit:** count  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- D-16 / D-30.

### M-26.2 — Spur: outside diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-08 / KO-21 guard.

### M-26.3 — Spur: bore diameter

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-26.4 — Spur: bolt-hole PCD

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- D-16 — must match the belt-set pulley.

### M-26.5 — Spur: bolt-hole diameter and count

- **Unit:** mm + count  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: spur and pulley faces side by side, bolt holes visible.  **Photo ref:** `______________`
- STOP if the spur and pulley bolt patterns do not match: the drivetrain as bought cannot be assembled. Report before any rear print.

### M-26.6 — Belt-set pulley: tooth count

- **Unit:** count  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-26.7 — Belt-set pulley: outside diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-26.8 — Belt-set pulley: width

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Belt guard width.

### M-26.9 — Belt-set pulley: bore diameter

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-26.10 — Belt-set pulley: bolt-hole PCD, diameter and count

- **Unit:** mm + count  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- D-16 pair with M-26.4/.5.

### M-26.11 — Belt: width

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-21.

### M-26.12 — Belt: measured length (laid flat, pitch line)

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BOM says 140 mm — a length alone cannot establish the axes.

### M-26.13 — Pinion: tooth count

- **Unit:** count  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-26.14 — Pinion: outside diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Mesh centre with the spur.

### M-26.15 — Pinion: bore diameter

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Motor shaft is 3.3 measured.

### M-26.16 — Rear output shaft: diameter

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-26.17 — Rear output shaft: shoulder positions along its length

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Spacer stack.

### M-27a.1 — A3144 Hall: TO-92 body L x W x thickness

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- SNS-HALL envelope; PS-16 bracket.

### M-27a.2 — A3144: lead pitch

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-27a.3 — A3144: lead length

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-27b — Neodymium magnet: diameter x thickness

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — magnets ordered / in transit. The 3 x 1 spec is CONFIRMED on paper only.

### M-13 — SP3T boot-mode selector: body, throw, panel cut-out, terminal projection

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — no switch selected or bought (owner shopping residue). sp3t_* stay ASSUMED.

### M-17a.1 — ES24TX: variant — IS IT THE PRO?

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the module's model marking.  **Photo ref:** `______________`
- gcs_tx_*. The vendor 70 x 49 x 32.5 figure is valid ONLY if it is the Pro. A nano/Slim is RE-MEASURED, not scaled.

### M-17a.2 — ES24TX: body L x W x H (without antenna)

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- gcs_tx_l/w/h.

### M-17a.3 — ES24TX: JR hook dimensions and which faces carry connectors

- **Unit:** mm + text  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Bulkhead panel is laid out from connector faces, not bodies.

### M-17b.1 — FT232RL board: body L x W x H

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- gcs_ftdi_l/w/h — no measurement exists anywhere in the workspace.

### M-17b.2 — FT232RL: connector faces

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Bulkhead layout.

### M-17c.1 — RT5370 dongle: body L x W x H with the USB shell

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- SPARE / 2.4 GHz fallback only. This does NOT retire gcs_wifi_* for the primary adapter.

### M-17d — Approved dual-band 5 GHz-AP-capable Wi-Fi adapter: body + connector faces

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — not procured. Top of the owner shopping residue; also gates the hotspot half of the Windows validation suite.

### M-17e — USB hub: body + connector faces, cables seated

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — not procured.


---

## Station 2 — The scale (no power, no battery connected)

### M-08a — ESP32 #1 with headers

- **Unit:** g  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- CG ledger; replaces the DevKit-class ~9-10 g estimate.

### M-08b — ESP32 #2 with headers

- **Unit:** g  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- CG ledger.

### M-08c — IP2326 charge module

- **Unit:** g  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- CG ledger; ASM-59.

### M-08d — XT90-S loop key + leads (mated pigtail pair)

- **Unit:** g  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- CG ledger.

### M-08e.1 — MG90S #1

- **Unit:** g  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Documented 13.4 g is a genuine-TowerPro figure.

### M-08e.2 — MG90S #2

- **Unit:** g  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-08e.3 — MG90S #3

- **Unit:** g  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-08f — Camera assembly as it will install

- **Unit:** g  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-24 / gimbal load.

### M-08g — PDB, assembled

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — not built (see M-06). The ~50 g is a TARGET.

### M-08h — Cassette assembly

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — does not exist; nothing in 11_cad/ has been printed.

### M-08i — Pedestal

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — does not exist.

### M-08j — ZEEE 5200 bench-only pack, bagged, on the scale

- **Unit:** g  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Retires an explicit ASSUMED (~250-300 g). NOT a car pack (138x47x37 vs <=75x45x25) — bench handling only, keep it out of any car CG ledger.

### M-09 — Four-corner weights, rolling assembly

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED TWICE — no rolling assembly, and tyres are in transit. NO balance claim and NO ballast cut until this table exists.


---

## Station 3 — Car, shell off (gated by M-00)

### M-20.1 — splice screw at X +7.50, L 0: FREE or OCCUPIED — try an actual M3 screw, do not judge by eye; if occupied, by what

- **Unit:** free/occupied + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: one photo per OCCUPIED feature showing what occupies it.  **Photo ref:** `______________`
- D-27 stage 2. Splice screws are OP-G's only anchors inside the cassette footprint; X+57.50/+64.24 are the pedestal's only anchors. Occupied = those ideas die here, which is cheaper than finding out with a printed part in hand. NO new holes in donor parts.

### M-20.2 — splice screw at X +14.26, L 0: FREE or OCCUPIED — try an actual M3 screw, do not judge by eye; if occupied, by what

- **Unit:** free/occupied + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: one photo per OCCUPIED feature showing what occupies it.  **Photo ref:** `______________`
- D-27 stage 2. Splice screws are OP-G's only anchors inside the cassette footprint; X+57.50/+64.24 are the pedestal's only anchors. Occupied = those ideas die here, which is cheaper than finding out with a printed part in hand. NO new holes in donor parts.

### M-20.3 — splice screw at X +22.69, L 0: FREE or OCCUPIED — try an actual M3 screw, do not judge by eye; if occupied, by what

- **Unit:** free/occupied + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: one photo per OCCUPIED feature showing what occupies it.  **Photo ref:** `______________`
- D-27 stage 2. Splice screws are OP-G's only anchors inside the cassette footprint; X+57.50/+64.24 are the pedestal's only anchors. Occupied = those ideas die here, which is cheaper than finding out with a printed part in hand. NO new holes in donor parts.

### M-20.4 — rear bracket at X -27.76, L -13.50: FREE or OCCUPIED — try an actual M3 screw, do not judge by eye; if occupied, by what

- **Unit:** free/occupied + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: one photo per OCCUPIED feature showing what occupies it.  **Photo ref:** `______________`
- D-27 stage 2. Splice screws are OP-G's only anchors inside the cassette footprint; X+57.50/+64.24 are the pedestal's only anchors. Occupied = those ideas die here, which is cheaper than finding out with a printed part in hand. NO new holes in donor parts.

### M-20.5 — rear bracket at X -27.76, L +16.50: FREE or OCCUPIED — try an actual M3 screw, do not judge by eye; if occupied, by what

- **Unit:** free/occupied + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: one photo per OCCUPIED feature showing what occupies it.  **Photo ref:** `______________`
- D-27 stage 2. Splice screws are OP-G's only anchors inside the cassette footprint; X+57.50/+64.24 are the pedestal's only anchors. Occupied = those ideas die here, which is cheaper than finding out with a printed part in hand. NO new holes in donor parts.

### M-20.6 — free single (belt side) at X -39.99, L -32.86: FREE or OCCUPIED — try an actual M3 screw, do not judge by eye; if occupied, by what

- **Unit:** free/occupied + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: one photo per OCCUPIED feature showing what occupies it.  **Photo ref:** `______________`
- D-27 stage 2. Splice screws are OP-G's only anchors inside the cassette footprint; X+57.50/+64.24 are the pedestal's only anchors. Occupied = those ideas die here, which is cheaper than finding out with a printed part in hand. NO new holes in donor parts.

### M-20.7 — free single (mirror side) at X -39.94, L +17.14: FREE or OCCUPIED — try an actual M3 screw, do not judge by eye; if occupied, by what

- **Unit:** free/occupied + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: one photo per OCCUPIED feature showing what occupies it.  **Photo ref:** `______________`
- D-27 stage 2. Splice screws are OP-G's only anchors inside the cassette footprint; X+57.50/+64.24 are the pedestal's only anchors. Occupied = those ideas die here, which is cheaper than finding out with a printed part in hand. NO new holes in donor parts.

### M-20.8 — centreline pedestal candidate at X +57.50, L 0: FREE or OCCUPIED — try an actual M3 screw, do not judge by eye; if occupied, by what

- **Unit:** free/occupied + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: one photo per OCCUPIED feature showing what occupies it.  **Photo ref:** `______________`
- D-27 stage 2. Splice screws are OP-G's only anchors inside the cassette footprint; X+57.50/+64.24 are the pedestal's only anchors. Occupied = those ideas die here, which is cheaper than finding out with a printed part in hand. NO new holes in donor parts.

### M-20.9 — centreline pedestal candidate at X +64.24, L 0: FREE or OCCUPIED — try an actual M3 screw, do not judge by eye; if occupied, by what

- **Unit:** free/occupied + text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: one photo per OCCUPIED feature showing what occupies it.  **Photo ref:** `______________`
- D-27 stage 2. Splice screws are OP-G's only anchors inside the cassette footprint; X+57.50/+64.24 are the pedestal's only anchors. Occupied = those ideas die here, which is cheaper than finding out with a printed part in hand. NO new holes in donor parts.

### M-28.1 — Servoholder PRINTED arch: clear opening length

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Mesh figure is 42.0. Servo face measured 40.25 -> ~1.75 mm clearance.

### M-28.2 — Servoholder PRINTED arch: clear opening height

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Mesh figure is 18.5. Servo face measured 20.2 -> ~1.7 mm INTERFERENCE, as predicted.

### M-28.3 — Does the DS3235SG enter side-on WITHOUT FORCE?

- **Unit:** pass/fail  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the servo offered to the arch, plus a close-up of the binding point.  **Photo ref:** `______________`
- STOP if it binds. Do not file, force or heat. A test-grade print can bind from layer swell alone; the fix is production tolerance or a measured CAD relief. OP-B / Gate D residual — this gates the whole floor print batch.

### M-28.4 — If it binds: exactly WHERE

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- The location is the CAD input.

### M-28.5 — Shaft-centre orientation used (boss-forward X-46.76 vs reversed X-66.76)

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Still unpinned; record which you used.

### M-29.1 — Steering Block4 king-pin bore diameter, side 1

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- D-05; M3x30 dowel fit. Outside 3.0 +0.15/-0.05 = a reprint tolerance change, decided in CAD.

### M-29.2 — Steering Block4 king-pin bore diameter, side 2

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- D-05.

### M-30.1 — Front hub (original RIGHT): bearing seat diameter for 8x12x3.5

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- D-22 baseline.

### M-30.2 — Front hub (Bambu-MIRRORED left): bearing seat diameter

- **Unit:** mm  ·  **Tolerance:** ±0.1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- D-22 — the left hub exists only as a mirror. Off by > 0.1 = tolerance pass before the wheel print.

### M-02a.1 — Steering rod LOWEST Z at forward, X ~ +40, swept lock-to-lock and through bump (datum DAT-F)

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: both locks, photographed from the same place.  **Photo ref:** `______________`
- ko01_z_lo. Provisional band is Z 22..38 at |L| <= 22, with the PDB 8.00 mm below it and ZERO reserve.

### M-02a.2 — Steering rod LOWEST Z at middle, X ~ 0, swept lock-to-lock and through bump (datum DAT-F)

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: both locks, photographed from the same place.  **Photo ref:** `______________`
- ko01_z_lo. Provisional band is Z 22..38 at |L| <= 22, with the PDB 8.00 mm below it and ZERO reserve.

### M-02a.3 — Steering rod LOWEST Z at rear, X ~ -40, swept lock-to-lock and through bump (datum DAT-F)

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: both locks, photographed from the same place.  **Photo ref:** `______________`
- ko01_z_lo. Provisional band is Z 22..38 at |L| <= 22, with the PDB 8.00 mm below it and ZERO reserve.

### M-02b.1 — Steering rod HIGHEST Z at forward, X ~ +40

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- ko01_z_hi.

### M-02b.2 — Steering rod HIGHEST Z at middle, X ~ 0

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- ko01_z_hi.

### M-02b.3 — Steering rod HIGHEST Z at rear, X ~ -40

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- ko01_z_hi.

### M-02c.1 — Max |L| the rod reaches at forward, X ~ +40

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- ko01_l_half.

### M-02c.2 — Max |L| the rod reaches at middle, X ~ 0

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- ko01_l_half.

### M-02c.3 — Max |L| the rod reaches at rear, X ~ -40

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- ko01_l_half.

### M-02d.1 — Most FORWARD X reached by any swept point of the rod

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- ko01_x_hi. NEW ROW: section 9 lists ko01_x_lo/x_hi under M-02 but the prompt's M-02 table has no cell for them.

### M-02d.2 — Most REARWARD X reached by any swept point of the rod

- **Unit:** mm  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- ko01_x_lo. Same note.

### M-02e — Does anything ALREADY FITTED enter that envelope? List every item and where

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: anything found inside the envelope.  **Photo ref:** `______________`
- KO-01 / KO-11 / KO-36. STOP-READ: measured z_lo < 22 or l_half > 22 shrinks the guard band (ko01_z_guard 14, ko01_l_guard 30) and drives the PDB's already-negative-by-5mm gap further negative. Report; do not re-derive the cage at the bench.


---

## Station 4 — Car, shell seated (gated by M-00; needs the shell)

### M-01.1 — S0 — shell bottom edge above floor top (DAT-F) at: forward, belt side. Shell seated and only LIGHTLY pressed

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the gauge in place at one point, showing the seating.  **Photo ref:** `______________`
- s0_measured. Coupon C-4 steps run 2..11 mm: read the tallest step that still passes; below the 2 mm step, write 'below the lowest step' — a real and serious answer. Record ALL readings, not the smallest.

### M-01.2 — S0 — shell bottom edge above floor top (DAT-F) at: forward, mirror side. Shell seated and only LIGHTLY pressed

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the gauge in place at one point, showing the seating.  **Photo ref:** `______________`
- s0_measured. Coupon C-4 steps run 2..11 mm: read the tallest step that still passes; below the 2 mm step, write 'below the lowest step' — a real and serious answer. Record ALL readings, not the smallest.

### M-01.3 — S0 — shell bottom edge above floor top (DAT-F) at: rear, belt side. Shell seated and only LIGHTLY pressed

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the gauge in place at one point, showing the seating.  **Photo ref:** `______________`
- s0_measured. Coupon C-4 steps run 2..11 mm: read the tallest step that still passes; below the 2 mm step, write 'below the lowest step' — a real and serious answer. Record ALL readings, not the smallest.

### M-01.4 — S0 — shell bottom edge above floor top (DAT-F) at: rear, mirror side. Shell seated and only LIGHTLY pressed

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the gauge in place at one point, showing the seating.  **Photo ref:** `______________`
- s0_measured. Coupon C-4 steps run 2..11 mm: read the tallest step that still passes; below the 2 mm step, write 'below the lowest step' — a real and serious answer. Record ALL readings, not the smallest.

### M-01.5 — S0 — shell bottom edge above floor top (DAT-F) at: OPTIONAL: over the cassette, either side. Shell seated and only LIGHTLY pressed

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the gauge in place at one point, showing the seating.  **Photo ref:** `______________`
- s0_measured. Coupon C-4 steps run 2..11 mm: read the tallest step that still passes; below the 2 mm step, write 'below the lowest step' — a real and serious answer. Record ALL readings, not the smallest.

### M-01.6 — S0 SPREAD = max reading minus min reading (derived at the bench)

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- STOP-READ: cage needs S0 >= 9.82 and S0 is bounded 0..~11. < 9.82 = STOP, do NOT shave the cage — reopen board orientation (a production stop ZK already demands). > 11 = re-check the datum. Spread > 1.0 = the shell does not sit flat, a DIFFERENT problem from sitting low, and the cage cares about both.

### M-07.1b — Clear height above DAT-F at X +3, BELT side (L-), across |L| 27..46, shell seated

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- guide_top_z.

### M-07.2b — Clear height above DAT-F at X +20, BELT side (L-), across |L| 27..46, shell seated

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- guide_top_z.

### M-07.3b — Clear height above DAT-F at X +42, BELT side (L-), across |L| 27..46, shell seated

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- guide_top_z.

### M-07.1m — Clear height above DAT-F at X +3, MIRROR side (L+), across |L| 27..46

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- guide_top_z. The WORST value must agree with M-01 plus the modelled roof (27.18 at X+3 / L-37). If it does not, ONE OF THE TWO IS WRONG — say which you trust and why, at the bench.

### M-07.2m — Clear height above DAT-F at X +20, MIRROR side (L+), across |L| 27..46

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- guide_top_z. The WORST value must agree with M-01 plus the modelled roof (27.18 at X+3 / L-37). If it does not, ONE OF THE TWO IS WRONG — say which you trust and why, at the bench.

### M-07.3m — Clear height above DAT-F at X +42, MIRROR side (L+), across |L| 27..46

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- guide_top_z. The WORST value must agree with M-01 plus the modelled roof (27.18 at X+3 / L-37). If it does not, ONE OF THE TWO IS WRONG — say which you trust and why, at the bench.

### M-11e.1 — ESC candidate station 1: where it is (X, L) and how much OPEN AIR is above the fan intake, body seated

- **Unit:** mm + coords  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the candidate with the ESC dry-placed (not fixed).  **Photo ref:** `______________`
- OP-A / KO-20 / CAS-06. Policy wants 10 mm above the fan = a plane at Z 45.5 with the measured 34.0 body, and NO registered shell station supplies it even at S0 = 11. This row is looking for a home, not confirming one. If none of the three works, say so; the decision is the owner's.

### M-11e.2 — ESC candidate station 2: where it is (X, L) and how much OPEN AIR is above the fan intake, body seated

- **Unit:** mm + coords  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the candidate with the ESC dry-placed (not fixed).  **Photo ref:** `______________`
- OP-A / KO-20 / CAS-06. Policy wants 10 mm above the fan = a plane at Z 45.5 with the measured 34.0 body, and NO registered shell station supplies it even at S0 = 11. This row is looking for a home, not confirming one. If none of the three works, say so; the decision is the owner's.

### M-11e.3 — ESC candidate station 3: where it is (X, L) and how much OPEN AIR is above the fan intake, body seated

- **Unit:** mm + coords  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the candidate with the ESC dry-placed (not fixed).  **Photo ref:** `______________`
- OP-A / KO-20 / CAS-06. Policy wants 10 mm above the fan = a plane at Z 45.5 with the measured 34.0 body, and NO registered shell station supplies it even at S0 = 11. This row is looking for a home, not confirming one. If none of the three works, say so; the decision is the owner's.

### M-12.1 — CF-1 (side vent): shell wall thickness

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- flap_wall.

### M-12.2 — CF-1: local depth behind the shell inner face

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- flap_open_w / flap_open_h.

### M-12.3 — CF-1: what is behind it

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: behind the candidate.  **Photo ref:** `______________`
- OP-F.

### M-12.4 — CF-2 (floor opening at X +39.18, |L| 55.71): wall thickness

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-12.5 — CF-2: local depth behind

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-12.6 — CF-2: what is behind it

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: behind the candidate.  **Photo ref:** `______________`
- NO CUT IS AUTHORISED BY THIS ROW. It exists so the CF-1/CF-2 decision is made against numbers instead of preference; the shell stays unmodified.

### M-15.1 — Side-vent parts: internal geometry (clear opening L x H, depth)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- vent_w / vent_h. WARNING: the 13.1 x 10.3 currently in w17_params.scad is the FLOOR SLOT, not the shell vent. Nobody has measured the vent.

### M-15.2 — Side-vent parts: how they mount to the shell

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- CF-1 reversibility.

### M-15.3 — Side-vent parts: visible face dimensions

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Cosmetic cost of an integrated flap.

### M-10 — Tyre arch clearance at full steer / full bump / both, four corners, body on

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — Tamiya tyres in transit. Registered margins are 3.5 and 4 mm, ALREADY below policy (E-30): this row is looking for a problem that is probably there.


---

## Station 5 — Car, rear end (gated by M-00). Never test the pocket alone

### M-14a.1 — Wing DRS pocket: internal length (datum: pocket floor)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- STOP if the MG90S will not enter without distorting the pocket.

### M-14a.2 — Wing DRS pocket: internal width

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-14a.3 — Wing DRS pocket: internal height

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-14a.4 — Wing DRS pocket: wall thickness

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-14d.1 — DRS arm: PIVOT-TO-PIVOT spacing (hole centre to hole centre)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the arm with the caliper across the two pivots.  **Photo ref:** `______________`
- drs_arm_pivot_span, which is deliberately undef with an assert() that fires if anyone gives it a value. THIS ROW IS THE ONLY THING THAT MAY SET IT. The 58 mm in the inventory is a RAW BOUNDING BOX, not a pivot span.

### M-14d.2 — DRS arm: driving hole diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-14d.3 — DRS arm: driven hole diameter

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-14e.1 — Flap hinge axis position (datum: hinge line, referenced to the wing datum)

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Four-bar geometry.

### M-14e.2 — Perpendicular distance, hinge axis to the arm's driven pivot

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- Four-bar geometry.

### M-14f.1 — Flap CLOSED angle wanted (chord vs wing datum)

- **Unit:** deg  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- DRS throw.

### M-14f.2 — Flap OPEN angle wanted

- **Unit:** deg  ·  **Tolerance:** ±2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- DRS throw.

### M-14g2 — Rod length required between rod-end centres

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- STOP if the linkage PRELOADS the flap at either end.

### M-14h.1 — Nearest approach of the swept arm to the 68 mm shock AT FULL COMPRESSION

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-25 wants >= 8 mm. The wing sits directly above the shock's territory.

### M-14h.2 — Nearest approach of the swept arm to the LED tail

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-25 / KO-29.

### M-14h.3 — Nearest approach of the swept arm to the body inner

- **Unit:** mm  ·  **Tolerance:** ±1
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- KO-25.

### M-14i — Servo neutral orientation that puts the rod straight at flap-closed: mark horn and case

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the horn at neutral, mark visible.  **Photo ref:** `______________`
- STOP if a WIRE becomes the hard stop, an ear needs drilling, or the horn hits the wing.

### M-18b — Sidepod port aperture you actually want (datum: vent face)

- **Unit:** mm  ·  **Tolerance:** ±0.2
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- spk_port_d (22.0 ASSUMED). This is a DECISION recorded as a number, not a discovered measurement — write down what you chose and why.

### M-19a.1 — Hall carrier surface at the rear axle: what the sensor can be mounted to

- **Unit:** text  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the candidate surface with the sensor offered to it.  **Photo ref:** `______________`
- PS-16 / D-38. If no carrier surface exists, the bracket becomes a new part.

### M-19a.2 — Hall carrier surface: its extent (L x W)

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-19a.3 — Hall carrier surface: distance to the axle centreline

- **Unit:** mm  ·  **Tolerance:** ±0.5
- **Value:** `______________________`
- **Photo ref (optional):** `______________`

### M-19b — Collar runout — how much the magnet face moves per revolution

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — magnets in transit. Use a NON-MAGNETIC gauge when it runs.

### M-19c — Sensor-to-magnet gap actually achievable (target 1.5 inside a 1-3 mm band)

- **Unit:** -  ·  **Tolerance:** -
- **Value:** `______________________`
- **Photo ref (optional):** `______________`
- BLOCKED — magnets in transit. hall_gap stays ASSUMED. NON-MAGNETIC gauge only: a steel gauge next to a Hall sensor and a magnet tells you about the gauge.

### M-19d — Can the Hall lead be routed AWAY from the ESC and motor phase leads (no parallel run, 90 deg crossing if it must cross) and kept short with its pull-up near the board?

- **Unit:** pass/fail  ·  **Tolerance:** -
- **Value:** `______________________`
- **PHOTO REQUIRED** — must show: the intended route.  **Photo ref:** `______________`
- GPIO35's interrupt has NO RATE BOUND and GPIO34-39 have NO internal pull-ups: a noisy Hall line CANNOT be rescued in software. FAIL = a design problem to report now, not a wiring-day problem.


---

**231 rows.** Transcribe into `w17-mechanical-measurement-session-prompt.md` (the record), then `11_cad/w17_params.scad` (value **and** tag **and** delete the §9 entry), then §12 of `10_assembly_architecture/AA_electronics_placement_study.md`. Then run `11_cad/render.sh` — **if an `assert()` fires, that is the sitting's most valuable output.**
