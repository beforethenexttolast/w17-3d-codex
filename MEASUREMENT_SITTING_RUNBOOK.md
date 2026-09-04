# The measurement sitting — runbook

**Date written:** 2026-09-05 · **No power. No battery. No USB into a live port. Nothing
flashed, nothing connected.** Calipers, a rule, a depth gauge, feeler gauges, a protractor,
a gram scale, and your eyes.

---

## What this file is, and what it is not

[`w17-mechanical-measurement-session-prompt.md`](w17-mechanical-measurement-session-prompt.md)
is the **record and the reasoning**: it says *why* each number matters and its tables are
where the values are finally committed. It is ordered by **what unblocks the most**.

This file is the **executable order**: the same measurements re-sorted by *what is in your
hand and where you are standing*, deduplicated against four other registers that ask for
the same physical quantities under different IDs, and split into what can be measured
**today** versus what is **BLOCKED** on a part that does not exist yet.

Capture goes on [`MEASUREMENT_RECORD_SHEET.md`](MEASUREMENT_RECORD_SHEET.md) (print it) or
[`MEASUREMENT_RECORD_SHEET.csv`](MEASUREMENT_RECORD_SHEET.csv) (type it). **One home per
number:** the sheet is the *capture* medium; afterwards the values are transcribed into the
session prompt's tables (the record), then into
[`11_cad/w17_params.scad`](11_cad/w17_params.scad) with the tag changed from `ASSUMED` to
`MEASURED(file:line)`, then the entry is deleted from that file's §9 and §12 of
[`AA_electronics_placement_study.md`](10_assembly_architecture/AA_electronics_placement_study.md)
is updated. Three places, always all three
([`w17-mechanical-measurement-session-prompt.md:61-64`](w17-mechanical-measurement-session-prompt.md)).

**Nothing here opens a gate.** A2 stays **NOT-EXECUTED** and Phase B stays **BLOCKED**
whatever the numbers say. No part is forced, cut, drilled, filed or glued in this sitting.

> **Naming collision, restated:** a bare **`S0`** anywhere in the mechanical package is the
> **shell-bottom clearance**. The A2 gate once called S0 was renamed **SF** on 2026-08-04
> ([`w17-socket-stack-caliper-prompt.md:19-21`](../w17-socket-stack-caliper-prompt.md)).
> There is no gate S0.

---

## Before you start (10 lines)

1. **No power at any point** — no battery, no USB into anything live, not "just to see the LED".
2. The **only** cable used is a **dead** one (M-03g), plugged in as a mechanical gauge with its
   far end connected to nothing.
3. Battery bay **empty**; the ZEEE 5200 pack stays bagged and **off the bench** except when it is
   on the scale (M-08j).
4. **Nothing is forced.** If a dry fit binds, stop and write down *where* it binds. The fix is a
   relieved part in CAD, never a knife on a servo.
5. Shell (if it exists) comes **off** and onto a soft cloth before anything else.
6. Print the record sheet; have a pen, a fine marker, masking tape, and a charged phone.
7. Zero the calipers on closed jaws before each block, and re-zero after any drop.
8. Fill the sheet header **once** (instrument, serial/model, date) — then value + unit per row.
9. **A measurement you could not take is a result:** write `could not — <why>`. Never estimate
   to fill a cell.
10. Do **M-00 first**. It decides whether Stations 3–5 exist at all.

**Have in hand on the bench before you sit down (Stations 1–2):** 3× MH-ET D1-Mini ESP32,
2× IP2326 charge module, 2× UBEC, the XT90-S pigtail pair, XT60/XT30 stock, the electrolytic
cap kit, 3× MG90S (+ their horns), DS3235SG + 25T horn, the QuicRun ESC, the OpenIPC camera,
the BL-M8812EU2 + its antennas, speaker + MAX98357A, RP1, A3144, the M3 insert + bolt kits,
cable ties, front + rear shocks, belt set + spur + pinion, ES24TX, FT232RL, RT5370.

---

## Tools

| Tool | Spec that matters | Rows |
|---|---|---|
| Digital calipers | 0–150 mm, 0.01 mm resolution, ≤0.03 mm accuracy; internal jaws + depth rod usable | almost every row |
| Depth gauge | the caliper's depth rod is enough **if** it reaches; otherwise a printed stepped gauge (coupon **C-4**, `fit_check_coupons.scad coupon="c4"`, steps 2…11 mm) or a feeler stack | M-01, M-07, M-12 |
| Feeler gauge set, **steel** | 0.05–1.00 mm blades | M-10, M-28, M-14h |
| Feeler/shim, **non-magnetic** | brass, plastic or paper shim stock, ±0.5 mm — **a steel gauge next to a Hall sensor and a magnet tells you about the gauge** | M-19b, M-19c |
| Steel rule | 150 mm **and** 300 mm, mm graduations | M-02, M-11e, M-14h |
| Protractor / angle gauge | 1° graduations (a digital angle gauge is fine) | M-14f, M-14i |
| Gram scale | ≥2 kg capacity, **1 g** resolution | M-08 (all) |
| Four scales | ≥1 kg each, 5 g — **only for M-09, which is BLOCKED this sitting** | M-09 |
| M3 screw + M3 bolt | the actual build fasteners, for the occupancy try-fit | M-20 |
| Fine marker + masking tape | rod marks, datum marks, part labels | M-02, M-14i |
| Phone camera | the 23 rows marked 📷 below | 23 rows |

**Not on the bench, and not permitted here:** power supply, battery leads, a live USB port,
a soldering iron, a knife, a file, a drill.

---

## The plan, in one screen

| Station | Where you are | Needs | Rows | Blocked |
|---|---|---|---|---|
| **0** | anywhere, 10 min | eyes | 1 | 0 |
| **1** | bench, loose parts, calipers | nothing printed | 40 | 5 |
| **2** | same bench, scale swap | nothing printed | 11 | 4 |
| **3** | car, shell off | printed floor/steering (M-00) | 9 | 0 |
| **4** | car, shell seated | printed shell + floor (M-00) | 6 | 1 |
| **5** | car, rear end | printed wing/rear stack (M-00) | 12 | 2 |

**Stations 1 and 2 do not depend on M-00 and can be done today.** They are 51 of the 79 rows
and they retire more `ASSUMED` parameters than the rest of the sitting combined.

**If you only have an hour** the session prompt's answer is M-00, M-01, M-02, M-03
([`w17-mechanical-measurement-session-prompt.md:32`](w17-mechanical-measurement-session-prompt.md)).
**If nothing is printed**, that hour becomes **M-00, M-03, M-04, M-05** — which is Station 1's
first two blocks, and is the highest-value hour available without a car.

**Rows vs values.** The 79 rows below are *measurements*; several read more than one number
(M-26 alone reads seventeen). The record sheet expands them into **231 numbered cells**, one per
value, so nothing is lost between "take this measurement" and "write this down".

**Reading the tables.** `mm` means millimetres to **0.1** unless the row says otherwise;
`g` means grams to **1**. `Tol.` is the precision the consumer actually needs — measuring
tighter is free, measuring looser invalidates the row. `Unlocks` names the
`w17_params.scad` parameter (and the §9 `ASSUMED` tag it retires) or the register row it
closes. `📷` means a photograph materially helps, and the cell says what it must show.

---

## Station 0 — What actually exists

| ID | What / where | Tool | Unit · Tol. | Unlocks | 📷 | Stop if |
|---|---|---|---|---|---|---|
| **M-00** | Tick each REQUIRED group from [`MODEL_INVENTORY.md:47-130`](MODEL_INVENTORY.md) — 02 rear axle (8) · 03 front susp/steering (8) · 04 wheels (7) · 05 floor (8) · 06 body shell (7) · 07 diffuser (1) — as `none / some / all`, name the actual parts, and give each a condition: `good / warped / layer split / supports on / TP / unknown material`. Then answer the six named parts by name: `Servoholder.stl`, `FloorBoard2.stl`, `2023NewFrontFloorLargerParts.stl`, `NEW BODY 2024 REAR.stl` (+ `FRONT 1`), `2023NEWSideVent1/2.stl`, `2021Rearwing with DRS.stl` + `DRS Arm…` | eyes + labels | — | [`05_printed_parts_log/PRINT_LOG.md`](05_printed_parts_log/PRINT_LOG.md) (which today records **nothing printed**); gates Stations 3–5 | ✅ one photo per group as laid out, plus a close-up of any warp or layer split | **If the shell does not exist, M-01 cannot be taken** and the cage stays a proposal — say so plainly rather than substituting a "close enough" body. A part whose **material or settings are unknown is a diagnostic part, not a build part**: a dry fit with it proves geometry, never durability |

---

## Station 1 — Bench, calipers, loose parts

Nothing here needs a printed part. Everything listed as on hand is on hand per
[`../HARDWARE_INVENTORY.md`](../HARDWARE_INVENTORY.md).

### Block A — the two controllers (MH-ET Live D1-Mini ESP32, 3 on hand)

Measure **one** board fully, then check the other two on M-03a/c only; if any of the three
disagrees by more than the tolerance, they are not the same SKU and every row here must be
taken per board.

| ID | What / datum & landmarks | Tool | Unit · Tol. | Unlocks | 📷 | Stop if |
|---|---|---|---|---|---|---|
| **M-03a** | Bare PCB **length × width**, jaws on the FR4 edges, not on a header or a shield lip | calipers | mm ±0.2 | `esp_len` / `esp_wid` — upgrades `DOCUMENTED(SKU class)` → MEASURED ([`11_cad/w17_params.scad:138-139`](11_cad/w17_params.scad)); ZK CAS-03 | — | outside **39 × 31 ±1** → this is not the SKU the whole cassette was planned on; stop and report before any other board row is trusted |
| **M-03b** | PCB **thickness**, on a bare edge away from a pad | calipers | mm ±0.1 | `esp_pcb_t` ([`:140`](11_cad/w17_params.scad)); `slot_w` = pcb_t + hand-fit | — | ≠ 1.6 ±0.2 → `slot_w` (1.8) is wrong; re-derive before coupon C-3 |
| **M-03c** | **Total thickness with headers fitted, at its thickest** — jaws across the board's two faces at the worst station, including the tallest through-hole tail on the underside | calipers | mm ±0.2 | `esp_thk_headers` (retires §9 `M-03`); AA §5.2 "the 13 mm band is exactly one board thick"; the assert at [`11_cad/w17_params.scad:391`](11_cad/w17_params.scad) | — | **> 13.0 → the assert fires and the design stops.** The band `board_l_out − board_l_in` is 13.0 mm exactly. Thinner is harmless (slack in the band); fatter ends the cage as drawn |
| **M-03d** | Mounting-hole **pitch X and pitch Y** (centre-to-centre, opposite corners) and **hole Ø** | calipers (internal jaws for Ø) | mm ±0.2 | `esp_hole_dx` / `esp_hole_dy` / `esp_hole_d` (retires §9 `M-03`); coupon **C-3** | — | no mounting holes at all → say so; the cage's retention is a clip and does not use them ([`11_cad/w17_params.scad:220-229`](11_cad/w17_params.scad)), but C-3's hole-pattern half becomes void |
| **M-03e** | **Which edge carries the service port** — long or short edge, and which end of it | eyes + calipers | — | `esp_usb_edge` (retires §9 `M-03`); decides the clip notch, AA §5.6 | ✅ the port edge with the silkscreen legible | port on a **long** edge → the on-edge wall seat presents a different face to X+42; AA §4.7's single service opening has to be re-planned |
| **M-03f** | **Which connector it actually is** — USB-C, micro-USB B, or something else — then its shell **width × height**, how far it **protrudes past the PCB edge**, and its **offset from that edge's centreline** | calipers | mm ±0.2 | `esp_usb_type`, `esp_usb_w`, `esp_usb_h`, `esp_usb_offset` (retires §9 `M-03`); **closes OP-I** and the AA §1 / [`w17-electrical-inputs-for-codex.md:8,10`](../w17-electrical-inputs-for-codex.md) vs [`ZK:102`](10_assembly_architecture/fit_studies/ZK_electronics_cassette_fit_study.md) conflict | ✅ the connector itself, close enough to read the shell shape | **micro-USB** → this is not just a smaller hole: AA §4.7's service story and §5.6's clip-notch rule were both written for USB-C. Record it and stop treating the USB-C wording anywhere as fact |
| **M-03g** | With a **dead** cable plugged in: how far the **plug body** projects past the PCB edge, and the cable's **minimum bend radius** before the plug is levered | calipers + rule | mm ±0.5 | service access; KO-34 (lift envelope); AA §4.7 | — | plug + bend exceeds the X+42…+46 tongue → the service opening cannot be at the tongue; report the number, do not cut anything |
| **M-03h** | **Component-free zones:** how far in from **each** of the four edges the **outboard** face is bare. Four numbers, one per edge | calipers + rule | mm ±0.5 | **OP-H**; `clip_station_x` (currently `[10, 34]` ESTIMATED) and `board_seat_x0` (retires §9 `M-03`); coupon **C-3**'s "both clip stations land on bare PCB" criterion | ✅ the outboard face flat-on with a rule alongside, so the bare margins are readable | no bare band at either **X+10** or **X+34** → the two clip stations as drawn stand on components. Report where the bare land actually is; the clips move, the board does not |
| **M-03i** | *Optional, do not let it delay anything:* read the **adjacent header pin pairs** off the silkscreen (which signal sits next to which) | eyes | — | A2 review **F12** (the MH-ET adjacency list, an explicit OWED placeholder) and open finding **F20** ([`../w17-pdb-build-and-connector-guide.md:141-144,184`](../w17-pdb-build-and-connector-guide.md)) | ✅ both silkscreen edges, sharp enough to read every label | — (its fallback, "beeper-check every joint", stays valid and slower) |
| **M-04** | The **female header** intended for the PDB, stacked with an MH-ET's **pre-soldered male pins**, seated as it would be in the cassette: **total stack height** | calipers | mm **±0.1** | `esp_socket_stack` (retires §9 `M-04`); the socketing **GO/NO-GO** ([`../w17-socket-stack-caliper-prompt.md`](../w17-socket-stack-caliper-prompt.md)); owner decision **F12** | — | Run the verdict from the socket prompt, not from here. **NO-GO → stop, do not solder**: F12 reopens, the boards go hard-wired, and §3 rule 2's unseat-for-isolation method has to be rewritten before anyone touches the harness. **Marginal is a report, not a judgement call.** ⚠ needs a female header from stock — if none is on hand, this row is `could not — no female header` and the socketing decision stays owed |

### Block B — PDB components and the connector bodies

The PDB **does not exist yet**: it is built at A2 build week from the parts below
([`../w17-pdb-build-and-connector-guide.md:130-141`](../w17-pdb-build-and-connector-guide.md)).
So its *outline* cannot be measured — but the parts that **set its height** can, and that is
the number the whole cage turns on.

| ID | What / datum & landmarks | Tool | Unit · Tol. | Unlocks | 📷 | Stop if |
|---|---|---|---|---|---|---|
| **M-05a** | **1000 µF electrolytic**: body **Ø × height**, and lead length below the body. Height is from the *seating plane* (where it sits on the board), not from the lead tips | calipers | mm ±0.2 | `pdb_stack_h` candidate (retires §9 `M-05`); [`../w17-batch1-measurements-for-codex.md:63-72`](../w17-batch1-measurements-for-codex.md) §2a's re-derivation | — | see M-05d |
| **M-05b** | **XT60** body **L × W × H**, male and female as actually used, measured lying as it will lie on the board | calipers | mm ±0.2 | `pdb_stack_h` candidate; **KO-33** dock body allocation | — | see M-05d |
| **M-05c** | **XT90-S loop key / master pigtail**: body **L × W × H** of each half, **mated overall length**, and the **pull axis** (which way the finger pulls) | calipers + rule | mm ±0.5 | `pdb_stack_h` candidate; finger access at the body ([`../w17-pdb-build-and-connector-guide.md:36-57`](../w17-pdb-build-and-connector-guide.md), owner decisions F9a/F9b); M-08d | ✅ the mated pair with an arrow drawn on tape along the pull axis | see M-05d |
| **M-05d** | **The tallest thing on the board, whatever it turns out to be** = `max(M-05a, M-05b, M-05c, 9.1)` — the 9.1 is the **already-MEASURED** UBEC height ([`../w17-batch1-measurements-for-codex.md:45`](../w17-batch1-measurements-for-codex.md)). Write the arithmetic on the sheet, not just the answer | derived at the bench | mm ±0.2 | `pdb_stack_h` (retires §9 `M-05`) | — | **> 13 mm → the cage's constraint arithmetic changes.** The PDB's audit top is `Z14` and KO-01's bottom is `Z22`: exactly the 8 mm moving-clearance policy with nothing spare ([`11_cad/w17_params.scad:128,395`](11_cad/w17_params.scad)). Report the number and stop; do not re-plan the cage at the bench |
| **M-06** | PDB finished outline L × W, mounting-hole positions, connector exit faces and directions | — | — | `pdb_len` / `pdb_wid` (§9 `M-06`) | — | **BLOCKED — the board does not exist.** No substrate has been chosen or bought (nothing in [`../HARDWARE_INVENTORY.md`](../HARDWARE_INVENTORY.md) is a perfboard). `pdb_len`/`pdb_wid` stay `ASSUMED` until the board is planned flat and built at A2 build week. **Do not cut a pocket to 55 × 45.** Owner action below |
| **M-21** | **Dock connector bodies**, one row per type: **XT30**, 3-pin servo (JR), **JST-XH 3 / 4 / 5**, JST-PH 2, **U.FL** head + pigtail Ø, and the camera↔Wi-Fi shielded 4-pin / micro-USB. For each: body **L × W × H** and **mated depth** (the pair plugged together) | calipers | mm ±0.2 | **KO-33** ("caliper XT60/XT30/3-pin/XH3/4/5/USB/U.FL", [`C_clearance_keepout_register.md:104`](10_assembly_architecture/C_clearance_keepout_register.md)); [`M_connector_harness_matrix.md`](10_assembly_architecture/M_connector_harness_matrix.md); [`Z_wire_schedule.md`](10_assembly_architecture/Z_wire_schedule.md); sanity-checks `pass_slot_w/h` (10 × 6 ESTIMATED) | — | any mated body deeper than the X+42…+58 dock projection → the dock is stepped or wrapped, not straight; record and report |

### Block C — process and fastener stock

These four rows are listed in [`11_cad/w17_params.scad:370-372`](11_cad/w17_params.scad) §9
against coupon **C-1**. That is right for `fit_clearance` — which only a printed ladder can
answer — but **wrong for the rest**: the inserts, the screws and the ties are on hand and
are caliper rows, today. See *Reconciliation findings* below.

| ID | What / datum & landmarks | Tool | Unit · Tol. | Unlocks | 📷 | Stop if |
|---|---|---|---|---|---|---|
| **M-22a** | **Heat-set insert M3×5** from the on-hand pack: **outside Ø** at its widest knurl, and **overall length** | calipers | mm ±0.1 | `insert_m3_d` (4.0 ASSUMED) / `insert_m3_h` (5.7 ASSUMED) ([`11_cad/w17_params.scad:73-74`](11_cad/w17_params.scad)); every `insert_boss` in [`11_cad/lib/w17_lib.scad`](11_cad/lib/w17_lib.scad); the GCS box lid | — | OD outside **4.0 ±0.2** → every boss Ø in the library changes; do not print a GCS lid until it is re-rendered |
| **M-22b** | **M3 screw** from the on-hand kit: thread **OD**, **button-head Ø**, head **height** | calipers | mm ±0.1 | `screw_m3_clear_d` (3.4) / `screw_m3_head_d` (6.0) ([`:71-72`](11_cad/w17_params.scad)) | — | head Ø > 6.0 → counterbores in the GCS box and the sleds are undersized |
| **M-22c** | **Cable-tie stock**: strap **width × thickness**, and head thickness | calipers | mm ±0.1 | `zip_slot_w` (4.0) / `zip_slot_l` (2.5) (retires §9 `C-1` rows) ([`:243-244`](11_cad/w17_params.scad)) | — | strap wider than 3.5 mm → the 4.0 slot has under 0.5 mm of dressing room; report |
| **M-22d** | *Optional, needs wire stock:* dress a representative **4-way silicone bundle** as it would run and measure its **OD** | calipers + tape | mm ±0.5 | sanity for `pass_slot_w/h` (10 × 6) and `tail_hole_d` (8.0), all ESTIMATED ([`:247-248,263`](11_cad/w17_params.scad)) | — | bundle OD > 8 mm → the tail hole is undersized; a hole in free plate is cheap to grow, so report rather than redesign |

### Block D — the rest of the on-hand parts

| ID | What / datum & landmarks | Tool | Unit · Tol. | Unlocks | 📷 | Stop if |
|---|---|---|---|---|---|---|
| **M-16** | **IP2326 charge module** (2 on hand): body **L × W × H**; hole positions if any; the **onboard Type-C** connector's edge and protrusion; **which face gets hot**; where the leads exit; and whether the **state LED is on the board** (light-pipe needed) or can be flown on two wires | calipers | mm ±0.2 | `chg_l` / `chg_w` / `chg_h` (retires §9 `M-16`); **closes OP-C**; ASM-59; the CF-1 state-LED decision (AA §7) | ✅ both faces, silkscreen legible — the same photo is the evidence the board is a genuine **balancing** charger, not a boost+CV board | any axis over the **30 × 25 × 10** cell → the charge cell must be re-planned. **No pocket may be cut to either published figure** — the two sources disagree (`~29×26×~6` [`../w17-electrical-inputs-for-codex.md:38`](../w17-electrical-inputs-for-codex.md) vs `18.3×31` in a ≤10 mm cell [`ZK:73`](10_assembly_architecture/fit_studies/ZK_electronics_cassette_fit_study.md)) and neither is a caliper record |
| **M-11a** | **ESC identity:** transcribe the **full label text / variant** exactly as printed | eyes | — | retires the "on-hand identity ASSUMPTION" in [`B_component_envelope_register.md:143`](10_assembly_architecture/B_component_envelope_register.md); D-28 | ✅ the label, sharp, all of it | label is **not** QuicRun 10BL120 G2 Sensored → the 44.2 × 33.7 × 34.0 body already measured belongs to a different part; stop and report |
| **M-11c** | ESC **foot / mounting-tab positions**: tab centres relative to the body's near face and to each other, and tab hole Ø | calipers | mm ±0.5 | `esc_*` install envelope; the OP-A relocation search | — | no tabs at all (tape-mounted) → record it; the relocation study loses its only fixings |
| **M-11d** | ESC **wire exit faces and directions** — which face each of battery-in, 3 phase and signal leaves, and the free length of each | rule | mm ±2 | KO-20 install envelope; N cable routing | ✅ the ESC with all leads laid out flat | — |
| **M-14b** | **MG90S** (3 on hand): body **L × W × H**, **ear pitch**, **ear hole Ø**, **boss height**, **spline height + tooth count**, lead exit face | calipers | mm ±0.2 | `drs_*` / gimbal pockets; **D-35**; the "clone fit ASSUMPTION" in [`B_component_envelope_register.md:148`](10_assembly_architecture/B_component_envelope_register.md) | — | body differs from the documented genuine TowerPro **22.8 × 12.2 × 28.5** by more than 0.5 mm → these are clones and every pocket is sized to the wrong body |
| **M-14c** | **Horn radii actually supplied**, per hole, from the **spline centre**; and how many horns came with each servo | calipers | mm ±0.2 | DRS throw arithmetic (with M-14d); gimbal | — | no horns supplied → M-14d/e/f cannot close; report |
| **M-14g1** | **Rod-end (M4 ball joint) stock:** ball Ø, thread size/pitch, and **ball-centre to thread-end** distance | calipers (+ thread gauge if available) | mm ±0.2 | the geometry half of `drs_*` (with M-14g2, Station 5); the steering rod build | — | — |
| **M-18a** | **Speaker:** record its **shape as found** (the outline is already MEASURED **35.3 × 25.1 × 6.1**, i.e. rectangular, not a round basket), then **cone Ø**, **mounting-hole pattern**, and **total depth including the magnet** | calipers | mm ±0.2 | `spk_*` residual; **D-36**; PS-14; KO-28 | — | ⚠ the session prompt asks for "basket Ø" (M-18a) — the batch-1 caliper record says the part is rectangular. Record what is in your hand and note the discrepancy |
| **M-23** | **Camera (OpenIPC SSC338Q + IMX335):** PCB **L × W × thickness**; heatsink envelope; **lens Ø**, axial length and its offset from the PCB centre; mounting-hole pattern + Ø; **cable-exit face**; total axial depth lens-tip to heatsink-back | calipers | mm ±0.2 | **Gate C** / **D-06** / **D-34**; the nine "MEASURE THESE" dims of the cooling duct ([`FIRST_PRINT_DECISION.md`](FIRST_PRINT_DECISION.md) §6); KO-24 | ✅ camera identity photo (D-34) plus one square-on shot of the lens face | disagrees with the owner ground truth **19.2 × 19.2 transverse × 30.7 axial** by more than 1 mm → the "documented body reference" in [`B_component_envelope_register.md:151`](10_assembly_architecture/B_component_envelope_register.md) is the wrong unit; stop and report. **No camera mount CAD until this row exists** |
| **M-24** | **Wi-Fi antennas + pigtails:** whip **length**, U.FL head body, pigtail **Ø** and its **minimum bend radius** before the coax kinks | calipers + rule | mm ±1 | **KO-26** (≥10 mm coax bend, ≥150 mm inter-system target); **D-33**; closes "antenna length not yet measured" ([`../w17-batch1-measurements-for-codex.md:40`](../w17-batch1-measurements-for-codex.md)) | — | whip ≠ ~70 mm → the routing reserve in KO-26 is wrong |
| **M-25** | **Shocks:** front **eye-to-eye** (the 51 vs 52 mm conflict), rear 68 mm eye-to-eye, body **Ø**, **fully-compressed length**, spring OD and free length — front and rear | calipers | mm ±0.5 | **D-12** (resolves the "51 mm requirement / 52 mm received-stock label" conflict, [`B_component_envelope_register.md:154`](10_assembly_architecture/B_component_envelope_register.md)); **D-37**; KO-04 / **KO-06** swept cylinder | — | front is neither 51 nor 52 → the front shock-mount fit is unproven either way; report both |
| **M-26** | **Drivetrain metrology:** spur teeth / OD / bore + **bolt PCD and hole Ø**; belt-set pulley teeth / OD / **width** / bore + bolt PCD; **belt width** and measured length; pinion teeth / OD / bore; rear output shaft Ø and shoulder positions | calipers | mm ±0.1 (bores, PCD) / ±0.2 (rest) | **D-16** (spur ↔ pulley bolt pattern — a BOM open confirm); **D-30**; **KO-21** guard geometry | ✅ spur and pulley faces side by side, bolt holes visible | spur and pulley bolt patterns do **not** match → the drivetrain as bought cannot be assembled; **stop and report before any rear print** |
| **M-27a** | **A3144 Hall sensor**: TO-92 body **L × W × thickness**, lead pitch, lead length | calipers | mm ±0.2 | SNS-HALL install envelope; PS-16 bracket; **D-38** | — | — |
| **M-27b** | Magnet **Ø × thickness** | — | — | KO-27; `hall_gap` context | — | **BLOCKED — magnets ⏳ ordered / in transit** ([`../HARDWARE_INVENTORY.md`](../HARDWARE_INVENTORY.md) §7, "chase next" item 2). The Ø3 × 1 spec is CONFIRMED on paper only |
| **M-13** | SP3T boot-mode selector: body L × W × H, throw, panel cut-out, terminal projection behind the panel | — | — | `sp3t_body_l/w/h`, `sp3t_cutout_l/w` (§9 `M-13`) | — | **BLOCKED — no switch has been selected or bought** ([`CURRENT_STATUS.md`](../CURRENT_STATUS.md) owner shopping residue). The placement question it also asks — *where can a hand reach a switch under the engine cover, with the cassette's forward face below Z14 entirely PDB* — is answerable at Station 4 once a shell exists |
| **M-17a** | **ES24TX**: confirm the **variant** (is it the Pro?), then body **L × W × H**, the JR hook, and which faces carry connectors | calipers | mm ±0.5 | `gcs_tx_l/w/h` (retires §9 `M-17`); the vendor 70 × 49 × 32.5 figure is valid **only if** the unit is the Pro ([`../w17-gcs-box-guide.md`](../w17-gcs-box-guide.md) §6) | ✅ the module's label / model marking | not a Pro → the envelope shrinks and is **re-measured, not scaled**; `gcs_sled_tx` is re-rendered |
| **M-17b** | **FT232RL USB-UART board**: body **L × W × H** and connector faces | calipers | mm ±0.5 | `gcs_ftdi_l/w/h` (retires §9 `M-17`) — *"no measurement exists anywhere in the workspace"* | — | — |
| **M-17c** | **RT5370 dongle**: body **L × W × H** with the USB shell | calipers | mm ±0.5 | `gcs_wifi_*` **as the spare/2.4 GHz fallback only** | — | ⚠ this is **not** the primary hotspot adapter — the approved dual-band one is (Addendum 2026-08-17). Measuring the RT5370 does **not** retire §9 `gcs_wifi_*` for the primary |
| **M-17d** | Approved dual-band 5 GHz-AP-capable Wi-Fi adapter | — | — | `gcs_wifi_l/w/h` (§9 `M-17`) | — | **BLOCKED — not procured.** Top of the owner shopping residue; it also gates the hotspot half of the Windows validation suite |
| **M-17e** | USB hub | — | — | `gcs_hub_l/w/h` (§9 `M-17`) | — | **BLOCKED — not procured** ("hub NOT PROCURED", [`11_cad/w17_params.scad:332`](11_cad/w17_params.scad)) |

---

## Station 2 — The scale

Same bench, one tool swap. **No power, no battery connected** — the pack is weighed on its
own, off the car.

| ID | What | Tool | Unit · Tol. | Unlocks | 📷 | Stop if |
|---|---|---|---|---|---|---|
| **M-08a** | ESP32 #1 **with headers** | scale | g ±1 | CG ledger; replaces the DevKit-class ~9–10 g estimate ([`../w17-batch1-measurements-for-codex.md:106-108`](../w17-batch1-measurements-for-codex.md)) | — | — |
| **M-08b** | ESP32 #2 **with headers** | scale | g ±1 | same | — | — |
| **M-08c** | IP2326 charge module | scale | g ±1 | CG ledger; ASM-59 | — | — |
| **M-08d** | XT90-S loop key + leads (the mated pigtail pair) | scale | g ±1 | CG ledger | — | — |
| **M-08e** | MG90S, **each of the three** | scale | g ±1 | CG ledger; the documented 13.4 g is a genuine-TowerPro figure | — | — |
| **M-08f** | Camera assembly as it will install | scale | g ±1 | CG ledger; KO-24 / gimbal load | — | — |
| **M-08g** | PDB, assembled | — | — | `~50 g` TARGET; **CAS-11** | — | **BLOCKED — not built** (see M-06) |
| **M-08h** | Cassette assembly | — | — | CAS-11 | — | **BLOCKED — does not exist**; nothing in `11_cad/` has been printed |
| **M-08i** | Pedestal | — | — | CAS-11 | — | **BLOCKED — does not exist** |
| **M-08j** | The **bench-only ZEEE 5200 pack**, in its bag, on the scale | scale | g ±1 | retires an explicit ASSUMED: *"a 2S 5200 typically weighs ~250–300 g — weigh it before any CG argument cites a number"* ([`../HARDWARE_INVENTORY.md`](../HARDWARE_INVENTORY.md) §E) | — | this pack is **not** a car pack (138 × 47 × 37 vs the ≤75 × 45 × 25 envelope). Its mass informs bench handling only — **do not put it in any car CG ledger** |
| **M-09** | Four-corner weights, rolling assembly | — | — | **D-39** / ASM-58; the 36.50 / 63.50 % planning split at 1717.6 g is bookkeeping, not a measurement | — | **BLOCKED twice over** — there is no rolling assembly, and the tyres are ⏳ in transit. **No balance claim may be made and no ballast cut until this table exists** |

---

## Station 3 — Car, shell off

**Gated by M-00.** Every row here needs printed parts to exist and be assembled far enough
to hold their relationship. If a group came back `none`, write `could not — not printed` and
move on; that is a result.

| ID | What / datum & landmarks | Tool | Unit · Tol. | Unlocks | 📷 | Stop if |
|---|---|---|---|---|---|---|
| **M-20** | **Free-feature occupancy.** Walk the nine registered M3 features and **try an actual M3 screw** in each — do not judge by eye. Splice screws at **X +7.50 / +14.26 / +22.69, L 0**; rear brackets at **X −27.76, L −13.50 / +16.50**; free singles at **X −39.99, L −32.86** and **X −39.94, L +17.14**; centreline pedestal candidates at **X +57.50** and **X +64.24, L 0**. For each: free / occupied, and by what | eyes + an M3 screw | — | **D-27** stage 2; **OP-G** (the three splice screws are the only existing-hole anchors inside the cassette footprint); **OP-D** (the cassette has no retention); PS-01…PS-15 mounting | ✅ one photo per **occupied** feature, showing what occupies it | the three splice screws occupied → **OP-G dies here**; both centreline features occupied → the pedestal's only anchors die. Both are good outcomes — cheaper than finding out with a printed part in hand. **No new holes in donor parts**, whatever the result |
| **M-28** | **`Servoholder` arch vs DS3235SG.** Measure the **printed** arch's real clear opening (length × height) — the mesh figure is 42.0 × 18.5 — then offer the servo **side-on** and record whether it enters **without force** and, if not, exactly **where it binds** | calipers + feeler | mm ±0.2 | **OP-B**; **D-09** Gate D residual; gates the whole floor print batch. Context: the measured servo face is **40.25 × 20.2** → ~1.75 mm clearance in length and **~1.7 mm interference** in height ([`../w17-batch1-measurements-for-codex.md:85-97`](../w17-batch1-measurements-for-codex.md)) | ✅ the servo offered to the arch, and a close-up of the binding point | **it binds → stop.** Do not file, do not force, do not heat. A test-grade print can bind from layer swell alone; the fix is production tolerance or a measured relief in CAD. Also record the shaft-centre orientation you used (boss-forward X−46.76 vs reversed X−66.76) — it is still unpinned |
| **M-29** | **`Steering Block4` king-pin bore Ø**, both sides, with the caliper's internal jaws | calipers | mm **±0.1** | **D-05**; the M3 × 30 dowel fit; steering geometry | — | outside 3.0 +0.15 / −0.05 → the king pin will not press or will be sloppy; a reprint tolerance change, decided in CAD |
| **M-30** | **Mirrored front hub** bearing seat Ø (for the 8 × 12 × 3.5 bearing), both hubs | calipers | mm **±0.1** | **D-22** — the left hub exists only as a Bambu mirror | — | seat Ø off by more than 0.1 → the mirrored hub needs a tolerance pass before the wheel print |
| **M-02a** | Steering **rod lowest Z** at three stations (**X ≈ +40 / 0 / −40**), swept lock to lock and through bump travel. Datum **DAT-F** (floor top) | rule + a marker on the rod | mm ±2 | `ko01_z_lo` (retires §9 `M-02`); **replaces provisional KO-01**; ASM-08 / CAS-01 | ✅ **both locks**, photographed from the same place | see M-02e |
| **M-02b** | Rod **highest Z** at the same three stations | rule + marker | mm ±2 | `ko01_z_hi` (retires §9 `M-02`) | — | see M-02e |
| **M-02c** | Max **\|L\|** the rod reaches at each station | rule | mm ±2 | `ko01_l_half` (retires §9 `M-02`) | — | see M-02e |
| **M-02d** | **Fore/aft extent of the swept rod: X of the most forward and most rearward swept point.** *(New row — see Reconciliation findings: §9 lists `ko01_x_lo` / `ko01_x_hi` under M-02 but the prompt's M-02 table has no cell for them)* | rule | mm ±2 | `ko01_x_lo` / `ko01_x_hi` (retires the last two §9 `M-02` entries) | — | see M-02e |
| **M-02e** | **Does anything already fitted enter that envelope?** List every item and where | eyes + rule | mm ±2 | KO-01 / KO-11 / **KO-36**; the cage's whole guard arithmetic (`ko01_z_guard` = 14, `ko01_l_guard` = 30, [`11_cad/w17_params.scad:107-108`](11_cad/w17_params.scad)) | ✅ anything found inside the envelope | measured **`z_lo` < 22** or **`l_half` > 22** → the guard band shrinks: the PDB's 3 mm gap to KO-01 (already 5 mm short of the 8 mm moving policy) goes further negative, and `wall_top_z` / `wall_l_out` both move. **Report; do not re-derive the cage at the bench** |

---

## Station 4 — Car, shell seated

**Gated by M-00, and specifically on the shell existing.**

| ID | What / datum & landmarks | Tool | Unit · Tol. | Unlocks | 📷 | Stop if |
|---|---|---|---|---|---|---|
| **M-01** | **S0** — height of the seated shell's bottom edge above the floor top, at **four or more points**: forward belt-side, forward mirror-side, rear belt-side, rear mirror-side, and optionally over the cassette. Shell **seated and only lightly pressed** — not clamped, not lifted. Datum **DAT-F ↔ shell bottom edge**. **Record all readings, not the smallest** — the *spread* is a second result | depth gauge, feeler stack, or coupon **C-4** (steps 2…11 mm; read the tallest step that still passes) | mm **±0.5** | `s0_measured` (retires §9 `M-01`); **D-04** / CAS-02; **the whole second-floor cage** | ✅ the gauge in place at one point, showing the seating | **< 9.82 → stop, and do not shave the cage.** Reopen the board orientation with a real number in hand — a production stop already demanded by [`ZK:363-364`](10_assembly_architecture/fit_studies/ZK_electronics_cassette_fit_study.md). **> 11 → the derived 0…11 bound is wrong**; re-check the datum before believing it. **Below the 2 mm step → "below the lowest step"**, a real answer and a serious one. **Spread > 1.0 mm → the shell does not sit flat**, which is a different problem from sitting low, and the cage cares about both |
| **M-07** | **Cassette deck clear height** above the floor with the shell seated, at **X +3, +20, +42**, across **\|L\| 27…46**, **both sides** — six cells | depth gauge | mm ±1 | `guide_top_z` (retires §9 `M-07`); AA §5.4 | — | the worst value must agree with **M-01 + the modelled roof (27.18 at X+3 / L−37)**. **If it does not, one of the two is wrong — say which you trust and why**, on the sheet, at the bench |
| **M-11e** | **ESC candidate stations:** at each of three stations you would consider, record where it is (X, L) and **how much open air is above** the fan intake with the body seated | rule + depth gauge | mm ±0.5 | **OP-A** — the largest unsolved packaging problem; **KO-20**; CAS-06 / ASM-49 | ✅ each candidate with the ESC dry-placed (not fixed) | policy wants **10 mm of open air** above the fan, i.e. a plane at **Z 45.5** with the measured 34.0 mm body. **No registered shell station supplies it, even at S0 = 11.** This row is looking for a home, not confirming one — if none of the three works, say so; the decision (relocate / accept a documented lower gap with a measured thermal run / change the ESC) is the owner's |
| **M-12** | **Shell interior at the charge-flap candidates.** **CF-1** (side vent) and **CF-2** (floor opening at X +39.18, \|L\| 55.71): **wall thickness**, **local depth behind**, and **what is behind it**. Datum: shell inner face | calipers | mm ±0.5 | `flap_open_w` / `flap_open_h` / `flap_wall` (retires §9 `M-12`); **OP-F** | ✅ behind each candidate | **No cut is authorised by this row.** It exists so the CF-1 / CF-2 decision is made against numbers instead of preference. The shell stays unmodified — the flap must use an existing opening or a reversible insert |
| **M-15** | **Side-vent parts** `2023NEWSideVent1/2.stl`: internal geometry, how they mount to the shell, and the **visible face dimensions** | calipers | mm ±0.2 | `vent_w` / `vent_h` (retires §9 `M-15`) | — | ⚠ the `13.1 × 10.3` currently in `w17_params.scad` is the **floor slot, not the shell vent**. Nobody has measured the vent. Do not carry the floor number forward |
| **M-10** | Tyre arch clearance at full steer, full bump, and both together, four corners, body on | — | — | **D-37** / risk **E-30** | — | **BLOCKED — Tamiya tyres ⏳ in transit** ([`../HARDWARE_INVENTORY.md`](../HARDWARE_INVENTORY.md) §B). The registered margins are **3.5 mm and 4 mm**, already below policy, so this row is looking for a problem that is probably there |

---

## Station 5 — Car, rear end

**Gated by M-00** (wing, DRS arm, rear stack). **Rule: never test the pocket alone** — the
DRS check runs with the real rear shock / stack / wing / LED harness present.

| ID | What / datum & landmarks | Tool | Unit · Tol. | Unlocks | 📷 | Stop if |
|---|---|---|---|---|---|---|
| **M-14a** | Wing **pocket internal L × W × H** and its **wall thickness**. Datum: pocket floor | calipers | mm ±0.2 | `drs_*` pocket; KO-12 / KO-25 | — | the MG90S (M-14b) does not enter without distorting the pocket → **stop** |
| **M-14d** | **Arm pivot-to-pivot spacing**, and **both hole Ø**. Datum: hole centres | calipers | mm ±0.2 | `drs_arm_pivot_span` — **deliberately `undef`**, with an `assert()` that fires if anyone gives it a value ([`11_cad/w17_params.scad:310,405-406`](11_cad/w17_params.scad)). **This row is the only thing that may set it** | ✅ the arm with the caliper across the two pivots | the **58 mm** in the inventory is a **raw bounding box, not a pivot span**. If the arm's real span makes the linkage unable to close, that is the result — do not adjust the number to make it work |
| **M-14e** | **Flap hinge axis** position, and its **perpendicular distance to the arm's driven pivot**. Datum: hinge line | calipers | mm ±0.5 | DRS four-bar geometry | — | — |
| **M-14f** | Flap **closed and open angles wanted**. Datum: chord vs wing datum | protractor | ° ±2 | DRS throw; firmware DRS endpoints (mechanical side only) | — | — |
| **M-14g2** | **Rod length between rod-end centres** as the assembly actually needs it (with M-14g1's rod-end geometry) | calipers | mm ±0.2 | `drs_*` linkage | — | the linkage **preloads the flap** at either end → **stop** |
| **M-14h** | **Nearest approach of the swept arm** to: the **68 mm shock at full compression**, the **LED tail**, and the **body inner**. Datum: swept envelope | feeler / rule | mm ±1 | **KO-25** (≥8 mm policy); Gate A / Gate B coupling | — | any gap **< 8 mm** → the 8 mm moving policy is broken by the wing that sits directly above the shock's territory; report the number |
| **M-14i** | **Servo neutral orientation** that puts the rod straight at flap-closed: mark the horn and the case | marker | — | DRS assembly repeatability | ✅ the horn at neutral, mark visible | a **wire becomes the hard stop**, or an ear needs drilling, or the horn hits the wing → **stop** |
| **M-18b** | The **sidepod port aperture you actually want**. Datum: vent face | calipers | mm ±0.2 | `spk_port_d` (22.0, retires §9 `M-18`) — *"a design choice with no acoustic evidence"* | — | this is a **decision recorded as a number**, not a discovered measurement; write down what you chose and why |
| **M-19a** | **Hall carrier surface:** what the sensor can actually be mounted to at the rear axle — the surface, its extent, and its distance to the axle centreline. Datum: axle face | calipers | mm ±0.5 | PS-16 bracket; **D-38**; KO-27 | ✅ the candidate surface with the sensor offered to it | no carrier surface exists → the bracket becomes a new part; report |
| **M-19b** | **Collar runout** — how much the magnet face moves per revolution | — | — | KO-27 | — | **BLOCKED — magnets ⏳ in transit** (M-27b) |
| **M-19c** | **Sensor-to-magnet gap actually achievable**, target 1.5 mm inside a 1–3 mm band | — | — | `hall_gap` (§9 `M-19`) | — | **BLOCKED — magnets ⏳ in transit.** When it runs, use a **non-magnetic** gauge |
| **M-19d** | **Hall lead route check** (no dimension, a pass/fail): can the lead be routed **away from the ESC and motor phase leads** — no parallel run, crossing at 90° if it must cross — and kept short with its pull-up near the board? | eyes + rule | pass / fail | AA §4.5; the control firmware's GPIO35 interrupt has **no rate bound** and GPIO34–39 have **no internal pull-ups** — a noisy Hall line **cannot be rescued in software** | ✅ the intended route | FAIL → the route is a design problem, not a wiring-day problem; report it now |

---

## What to do with the results

1. Fill [`MEASUREMENT_RECORD_SHEET.md`](MEASUREMENT_RECORD_SHEET.md) at the bench.
2. Transcribe into the tables in
   [`w17-mechanical-measurement-session-prompt.md`](w17-mechanical-measurement-session-prompt.md)
   and commit it in `w17-3d-codex` — **it is the record**.
3. For each row, update [`11_cad/w17_params.scad`](11_cad/w17_params.scad): the value, **and**
   the tag (`ASSUMED` → `MEASURED(<file>:<line>)`), **and** delete its entry from §9.
4. Update §12 of
   [`AA_electronics_placement_study.md`](10_assembly_architecture/AA_electronics_placement_study.md)
   to match.
5. Run `11_cad/render.sh`. **If an `assert()` now fires, that is the sitting's most valuable
   output** — the geometry has moved outside what the study's arithmetic allows, and the
   design needs revisiting before anything is printed.
6. If **M-00** found printed parts, add them to
   [`05_printed_parts_log/PRINT_LOG.md`](05_printed_parts_log/PRINT_LOG.md) with what is
   genuinely known (source, date, shop, material if known) and mark every unknown as unknown.
   They get **no retroactive `P-NNN`**; a fit check with one is a `TP-NNN` naming the part's
   unknown provenance.

---

## Cross-check A — every `ASSUMED` parameter maps to a row

Source: [`11_cad/w17_params.scad:343-373`](11_cad/w17_params.scad) §9, the mirror of AA §12.

| §9 parameter(s) | §9 says | Row here | Runnable this sitting? |
|---|---|---|---|
| `s0_measured` | M-01 | **M-01** | M-00-gated (needs the shell) |
| `ko01_z_lo`, `ko01_z_hi`, `ko01_l_half` | M-02 | **M-02a / M-02b / M-02c** | M-00-gated |
| `ko01_x_lo`, `ko01_x_hi` | M-02 | **M-02d** ← *new row; the prompt's M-02 table has no cell for these* | M-00-gated |
| `esp_thk_headers` | M-03 | **M-03c** | ✅ today |
| `esp_hole_dx` / `dy` / `d` | M-03 | **M-03d** | ✅ today |
| `esp_usb_w` / `h` / `offset` | M-03 | **M-03f** | ✅ today |
| `esp_usb_type` | M-03(f) | **M-03f** | ✅ today |
| `esp_usb_edge` | M-03(e) | **M-03e** | ✅ today |
| `board_seat_x0` | M-03 (OP-H) | **M-03h** (a decision the row unlocks, not a value it reads) | ✅ today |
| `esp_socket_stack` | M-04 | **M-04** | ✅ today, **if a female header is in stock** |
| `pdb_stack_h` | M-05 | **M-05a–d** | ✅ today |
| `pdb_len`, `pdb_wid` | M-06 | **M-06** | ❌ **BLOCKED** — the PDB does not exist |
| `guide_top_z` | M-07 | **M-07** | M-00-gated |
| `flap_open_w` / `h`, `flap_wall` | M-12 | **M-12** | M-00-gated |
| `sp3t_body_l/w/h`, `sp3t_cutout_l/w` | M-13 | **M-13** | ❌ **BLOCKED** — no switch selected |
| `drs_arm_pivot_span` | M-14d | **M-14d** | M-00-gated |
| `vent_w`, `vent_h` | M-15 | **M-15** | M-00-gated |
| `chg_l` / `w` / `h` | M-16 | **M-16** | ✅ today |
| `gcs_tx_l/w/h` | M-17 | **M-17a** | ✅ today (variant confirm included) |
| `gcs_ftdi_l/w/h` | M-17 | **M-17b** | ✅ today |
| `gcs_wifi_l/w/h` | M-17 | **M-17d** (primary) · M-17c measures only the **spare** | ❌ **BLOCKED** — adapter not procured |
| `gcs_hub_l/w/h` | M-17 | **M-17e** | ❌ **BLOCKED** — hub not procured |
| `spk_port_d` | M-18 | **M-18b** | M-00-gated; it is a **decision**, not a discovery |
| `hall_gap` | M-19 | **M-19c** | ❌ **BLOCKED** — magnets in transit |
| `insert_m3_d`, `insert_m3_h` | C-1 | **M-22a** ← *reassigned: a caliper row, not a coupon row* | ✅ today |
| `screw_m3_clear_d` (+ `screw_m3_head_d`) | C-1 | **M-22b** ← *reassigned* | ✅ today |
| `zip_slot_w`, `zip_slot_l` | C-1 | **M-22c** ← *reassigned* | ✅ today |
| `fit_clearance` | C-1 | **none — correctly so.** Only a printed peg/hole ladder can answer it | ❌ needs coupon C-1 printed |

**No §9 entry is unmapped.** Four are BLOCKED on a part that does not exist, one
(`fit_clearance`) is correctly a coupon rather than a caliper, and three were filed under
C-1 that are really caliper rows.

## Cross-check B — every row maps to a consumer

Each row's `Unlocks` cell names a `w17_params.scad` parameter, a register row (D-nn / KO-nn /
OP-nn / CAS-nn / ASM-nn / PS-nn / E-nn), or a named gate. **There are no rows without a
consumer.**

**Rows whose consumer is *not* a `w17_params.scad` parameter** — these are not orphans, they
close register rows instead, and they are why this runbook is longer than §9:

| Row | Consumer |
|---|---|
| M-00 | `PRINT_LOG.md`; gates Stations 3–5 |
| M-03a / M-03b | upgrade `esp_len`/`esp_wid`/`esp_pcb_t` from `DOCUMENTED` to `MEASURED`; ZK CAS-03 |
| M-03g | AA §4.7 service access; KO-34 |
| M-03i | A2 review **F12**, open finding **F20** |
| M-05a–c | feed M-05d; KO-33 (XT60 body) |
| M-08a–j | CG ledger / **D-39** / CAS-11 |
| M-11a / c / d | D-28; KO-20 install envelope; N cable routing |
| M-14a / b / c / e / f / g1 / g2 / h / i | KO-12, KO-25, D-35, Gate A / Gate B |
| M-18a | D-36, PS-14, KO-28 |
| M-19a / d | PS-16, D-38, AA §4.5 |
| M-20 | D-27 stage 2, **OP-G**, **OP-D** |
| M-21 | **KO-33**, M connector matrix, Z wire schedule |
| M-22d | sanity for `pass_slot_*` / `tail_hole_d` (ESTIMATED, not ASSUMED) |
| M-23 | **Gate C**, D-06 / D-34, the duct's nine dims, KO-24 |
| M-24 | KO-26, D-33 |
| M-25 | **D-12** (the 51/52 conflict), D-37, KO-04 / KO-06 |
| M-26 | **D-16**, D-30, KO-21 |
| M-27a | SNS-HALL envelope, PS-16 |
| M-28 | **OP-B**, D-09 / Gate D residual |
| M-29 | **D-05** |
| M-30 | **D-22** |

**Orphans in the other direction — asks in the registers that this sitting deliberately does
not carry** (27 of them), because they are powered, gated behind A2 / Phase B, or need a part
or an assembly that does not exist even on paper:

D-07 (camera boresight — no mount exists) · D-10 (harness bulk on a placed chassis) ·
D-11 (USB service access — needs shell + boards placed) · D-14 (Gate A articulation) ·
D-15 (rear-stack identity — a drawing question) · D-17 (Gate B combined fit) ·
**D-18 (gimbal hard-stops — A2 + Phase-B gated)** · D-19 (thermal run — powered) ·
D-20 (RF / RSSI — powered) · D-23 (adapter qty + heat soak — after drives) ·
D-24 (rail currents — powered) · D-33 (video route dress + ten body cycles) ·
KO-13 (gimbal sweep — gated) · KO-14 (clamshell path) · KO-15 (fastener reach) ·
KO-16 (airflow verify) · KO-17 (antenna RF — powered) · KO-21 (belt guard, needs the
assembled drivetrain; M-26 measures its inputs) · KO-23 (battery body/strap — **no
in-envelope pack exists**) · KO-31 (pedestal sweep — not printed) · KO-34 (cassette lift —
does not exist) · KO-35 (pedestal conduit pull-through — does not exist) ·
B: USB-PORT (a port to design, not a part) · B: COOL-DUCT (to design) · B: FUT-EXP
(placeholder) · B: HARNESS loom bulk · B: LGT-LED segmentation (a design decision).

---

## Dedupe ledger

**Method (DERIVED, and checkable):** every source was read at the granularity of its own
enumerated rows; each enumerated request for a physical quantity counted as one "ask".

| Source | Asks |
|---|---:|
| [`w17-mechanical-measurement-session-prompt.md`](w17-mechanical-measurement-session-prompt.md) M-00…M-20, sub-rows counted | 63 |
| [`D_measurement_plan.md`](10_assembly_architecture/D_measurement_plan.md) D-01…D-39, excluding digitally-closed and document-review rows | 33 |
| [`B_component_envelope_register.md`](10_assembly_architecture/B_component_envelope_register.md) B.1 `TO MEASURE` + B.4 | 23 |
| [`C_clearance_keepout_register.md`](10_assembly_architecture/C_clearance_keepout_register.md) "required physical test" cells that ask for a dimension or a gap | 21 |
| [`11_cad/w17_params.scad`](11_cad/w17_params.scad) §9, counted per named parameter | 35 |
| [`../w17-socket-stack-caliper-prompt.md`](../w17-socket-stack-caliper-prompt.md) | 2 |
| [`../w17-batch1-measurements-for-codex.md`](../w17-batch1-measurements-for-codex.md) §6 "still open" | 6 |
| [`../HARDWARE_INVENTORY.md`](../HARDWARE_INVENTORY.md) (weigh the 5200 pack) | 1 |
| **Harvested total** | **184** |
| − already retired by the 2026-07-24 caliper session (ESC body, Wi-Fi body, UBEC, amp, speaker outline, RP1, motor, DS3235SG face, BX100, LED strip width) | −10 |
| − out of scope for a no-power, no-assembly sitting (the 27 listed above) | −27 |
| **In-scope asks** | **147** |
| **After dedupe → rows in this runbook** | **79** |

**The merges that did the work** (same physical quantity, asked under different IDs):

| One row | Absorbs |
|---|---|
| **M-01** | prompt M-01 · D-01 residual (S0 pin at first body-on) · D-04 · D-31 (S0 half) · CAS-02 · KO-30 (S0 half) · `s0_measured` |
| **M-02a–e** | prompt M-02 · D-26 residual · KO-01 · KO-11 · KO-36 · ASM-08 / CAS-01 · five `ko01_*` params |
| **M-03a–h** | prompt M-03(a–h) · D-32 (both ESP32 rows) · B CTL-E1/E2 "holes and installed service volume TO CALIPER" · CAS-03 · OP-H · OP-I · nine `esp_*` params · batch-1 §6 "real MH-ET caliper" |
| **M-05a–d** | prompt M-05(a–d) · D-32 (caps, XT parts) · B PWR-CAP · batch-1 §2a action + §6 "1000 µF / XT60 / loop-key heights" · `pdb_stack_h` |
| **M-11a/c/d/e** | prompt M-11(a,c,d,e–g) · D-08 · D-28 · KO-20 · OP-A · CAS-06 / ASM-49 · batch-1 §6 "ESC fan intake-air" |
| **M-14a–i** | prompt M-14(a–i) · D-09 (MG90S half) · D-35 · KO-12 · KO-25 · B SRV-DRS / SRV-PAN / SRV-TILT · Gate B |
| **M-16** | prompt M-16 · B PWR-CHG · OP-C · ASM-59 · batch-1 §6 "charge-module height" · three `chg_*` params |
| **M-21** | KO-33 · B PWR-Y / PWR-XT30 · the M connector matrix · the Z wire schedule (all previously asking for the same connector bodies) |
| **M-23** | D-06 · D-34 · B VID-CAM · B COOL-DUCT inputs · Gate C · KO-24 |
| **M-25** | D-12 · D-37 (shock half) · B SHK-FRONT/REAR · KO-04 · KO-06 |
| **M-26** | D-16 · D-30 · B DRV-SPUR/PINION · KO-08 · KO-21 inputs |
| **M-28** | prompt M-00's `Servoholder` call-out · D-09 (steering half) · OP-B · KO-19 · Gate D residual · batch-1 §3 + §6 "Track D" |
| **M-08a–j** | prompt M-08 (7 items) · D-21 partial · D-39 · CAS-11 · the HARDWARE_INVENTORY 5200 mass assumption |

---

## Reconciliation findings

Where the prompt and the registers disagree, both are listed and the row that resolves it is
named. **None of these is a baseline contradiction** — they are bookkeeping collisions inside
the mechanical package.

1. **`M-06b` is used for two different things.** The prompt's M-00 table says
   *"`Servoholder.stl` — M-06b: the ~1.7 mm steering-servo interference (OP-B)"*
   ([`:98`](w17-mechanical-measurement-session-prompt.md)), while the M-05/M-06 table's
   **M-06b** is *"mounting-hole positions, if any"* for the **PDB**
   ([`:223`](w17-mechanical-measurement-session-prompt.md)). Two unrelated quantities under
   one ID. **Resolved here:** the servo/arch fit is **M-28**; the PDB holes stay under
   **M-06** (and are BLOCKED anyway).
2. **`ko01_x_lo` / `ko01_x_hi` have no measurement cell.** §9 lists all five `ko01_*`
   parameters under M-02 ([`11_cad/w17_params.scad:351`](11_cad/w17_params.scad)), and AA §12
   lists only `ko01_z_lo/hi` and `ko01_l_half`; the prompt's M-02 table records Z and \|L\|
   only. **Resolved here:** new row **M-02d** takes the fore/aft extent.
3. **Three §9 rows are filed under coupon C-1 that are caliper rows.**
   `insert_m3_d` / `insert_m3_h`, `screw_m3_clear_d`, `zip_slot_w` / `zip_slot_l` are
   properties of **purchased stock that is on hand**, not of this printer. Only
   `fit_clearance` genuinely needs the printed ladder. **Resolved here:** M-22a / M-22b /
   M-22c, runnable today; C-1 keeps `fit_clearance` alone.
4. **The speaker is rectangular, and the prompt asks for a basket Ø.** M-18a says *"speaker
   basket Ø, cone Ø"*; the batch-1 caliper record has **35.3 × 25.1 × 6.1**
   ([`../w17-batch1-measurements-for-codex.md:47`](../w17-batch1-measurements-for-codex.md)).
   **Resolved here:** M-18a records the shape as found; the outline is already MEASURED and
   only the cone Ø, hole pattern and depth are owed.
5. **The camera is missing from the prompt entirely.** It is on hand, it is `TO MEASURE` in
   two registers (B VID-CAM, D-06/D-34), it gates **Gate C** and *"no camera mount CAD until
   board/heatsink/lens/exits are calipered"*
   ([`B_component_envelope_register.md:151`](10_assembly_architecture/B_component_envelope_register.md)),
   and it needs nothing but calipers. **Resolved here:** **M-23**, Station 1.
6. **`gcs_wifi_*` points at the wrong adapter.** §9 and AA §8 size it from a generic figure,
   the box guide's §2 row 3 names the **RT5370**, and the 2026-08-17 addendum demotes the
   RT5370 to spare in favour of an approved dual-band adapter that **has not been bought**.
   **Resolved here:** M-17c measures the spare and explicitly does **not** retire the tag;
   **M-17d** is BLOCKED on procurement.
7. **`pdb_len` / `pdb_wid` cannot be measured by anyone, yet.** The prompt's M-06a asks for
   the *"finished board outline"*, but the PDB is built at A2 build week and its first step
   is *"plan the board flat"*
   ([`../w17-pdb-build-and-connector-guide.md:139`](../w17-pdb-build-and-connector-guide.md)) —
   the outline is a **design output**, not a measurement. **Resolved here:** M-06 is BLOCKED
   and says so; M-05a–d still deliver the height, which is the number the cage actually needs.

---

## BLOCKED rows, and what would unblock them

Each is phrased as **device / where-how / what it unlocks / what would then be measured**.

| Row | Device | Where / how | Unlocks | Would then measure |
|---|---|---|---|---|
| **M-06**, **M-08g** | a PDB substrate (perfboard) + the A2 build | it is built, not bought-and-measured; the build is A2 build week | `pdb_len`, `pdb_wid`; CAS-04 / ASM-22; the ~50 g TARGET | finished outline, holes, connector exits, assembled mass |
| **M-13** | an SP3T boot-mode switch | owner shopping residue ([`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)) — none selected | `sp3t_body_l/w/h`, `sp3t_cutout_l/w`; the under-engine-cover reach question | body, throw, panel cut-out, terminal projection |
| **M-17d** | approved dual-band 5 GHz-AP-capable USB Wi-Fi adapter | owner shopping residue; also gates the hotspot half of the Windows validation suite | `gcs_wifi_l/w/h`; the GCS bulkhead layout | body + connector faces |
| **M-17e** | a powered USB hub | owner shopping residue; *"hub NOT PROCURED"* | `gcs_hub_l/w/h`; the sled grid layout | body + connector faces, with cables seated |
| **M-27b**, **M-19b**, **M-19c** | neodymium magnets 3 × 1 mm | ⏳ ordered / in transit ([`../HARDWARE_INVENTORY.md`](../HARDWARE_INVENTORY.md) §7) | `hall_gap`; KO-27; PS-16 | magnet body, collar runout, achievable gap (non-magnetic gauge) |
| **M-10** | Tamiya 54198 / 51400 tyres | ⏳ ordered / on the way (rcMart) | D-37 / E-30 — arch margins are 3.5 / 4 mm, already below policy | arch clearance at full steer, full bump, and both |
| **M-09**, **M-08h**, **M-08i** | a rolling assembly (printed parts + tyres + cassette + pedestal) | needs M-00's parts **and** printing the cassette/pedestal, which is itself gated on M-01/M-02 | D-39 / ASM-58; **no balance claim and no ballast until it exists** | four-corner weights; cassette and pedestal masses |
| **M-04** *(conditional)* | one female header of the type intended for the PDB | office stock — [`../HARDWARE_INVENTORY.md`](../HARDWARE_INVENTORY.md) §D lists the interconnect as owned but **not delivery-verified** | `esp_socket_stack`; owner decision **F12** GO/NO-GO | seated stack height |
| **Stations 3–5** *(24 rows)* | printed donor parts | **M-00 decides.** If the shell does not exist, M-01 cannot be taken and the cage stays a proposal | `s0_measured`, all `ko01_*`, `guide_top_z`, `flap_*`, `vent_*`, `drs_arm_pivot_span` | everything in Stations 3, 4 and 5 |

---

## Safety, restated because it is easy to drift

No power, no battery, no USB into a live port, nothing flashed or connected — calipers, a
rule, a scale and your eyes. No part is forced, cut, drilled, filed or glued in this sitting.
**A2 stays NOT-EXECUTED and Phase B stays BLOCKED whatever the numbers say.** Measuring is
not building. Show diffs before committing.
