# P · Assembly Master Manual (dependency-aware)

Session 2 · 2026-07-18; connection execution layer added 2026-07-23. Steps
ASM-01…ASM-60 (ASM-49…ASM-60 are appended closures that execute before the
ASM-48 authorization decision). Format per step: **Purpose · Prereq ·
Needs** (parts/tools/fasteners) · **CN/H** (connectors/harnesses touched) · **Do**
(orientation, tightening, routing) · **Test → pass** · **⚠ / STOP** · **Evidence** ·
**📷** (diagram/photo still needed). "Snug" = plastic-thread rule (ASSEMBLY_NOTES);
"final" torque only where stated. Gates P0–P10 per `R_validation_gates.md`; nothing
proceeds past a STOP. Sequencing notes vs the generic order: UBEC bodies go in at
ASM-17 (they live **under** the deck), ASM-21 is their rail configuration/verification;
the rear LED tail (ASM-13) precedes rear-stack closure (R-09).

**Phase I — Verification (Gate P0 territory)**

- **ASM-01 Inventory verification.** Purpose: every part/fastener present vs BOM v2 +
  `MODEL_INVENTORY.md`. Prereq: —. Needs: BOM, calipers. Do: tick lists; **physically
  confirm the WiFi module (RST-06)** — if absent it stays a dummy through ASM-25.
  Test → pass: no missing mandatory row (F §2). STOP: missing structural hardware.
  Evidence: checked list in `07_assembly_notes/`. 📷 no.
- **ASM-02 Measurement-gate verification.** Purpose: confirm Gate P0 state. Prereq:
  ASM-01. Do: check D-01/D-02/D-04/D-25/D-26 (**slicer stage** — the physical confirm
  lands at ASM-08, S3)/D-27 done; D-06 done; Gate A/B state.
  STOP: any P0 measurement missing → run it before continuing. Evidence: updated
  `D_measurement_plan.md`. 📷 no.
- **ASM-03 Printed-part inspection.** Purpose: no diagnostic (TP) part enters the
  build (E-22). Do: verify P-NNN labels, inspect seats/bores, deburr. Test: inserts'
  bosses undamaged. Evidence: PRINT_LOG refs. 📷 no.
- **ASM-04 Heat-set inserts + captive hardware.** Purpose: metal threads at service
  bosses. Prereq: ASM-03. Needs: iron ~200 °C, M3×5 inserts. Do: PS-04 front bosses,
  PS-15 bosses, 3 body bosses (E-08); floor slot nuts seated (drawing `[2]`).
  ⚠ hot iron, fumes (CLAUDE.md safety). Test: M3 threads by hand. 📷 yes (insert seats).

**Phase II — Mechanical core (Gates A/B rules apply, RST-07)**

- **ASM-05 Chassis dry assembly (floor).** Purpose: floor = datum. Do: front + rear +
  rear-2 + floorboard + vents + diffuser per drawing `[2]`, 12× M3 snug. Test: flat,
  no rock. Evidence: ASM note + photo. 📷 yes.
- **ASM-06 Steering-servo installation (KO-19).** Purpose: the central occupant goes
  in **first**, while access is open (RST-03). Prereq: ASM-05, D-09 fit-check done.
  Needs: DS3235SG, `Servoholder`. CN-08. Do: test/fit servo **side-on** per drawing
  `[2]`, 58 mm holder span longitudinal, shaft horizontal/lateral; do not force the
  documented 20 mm case through the measured 18.5 mm arch. Confirm lead exit and
  shell-shoulder clearance. ⚠ do not attach horn yet. Evidence: photo + caliper note. 📷 yes.
- **ASM-07 Servo power-up + firmware centring.** Purpose: centre **before** linkage
  (A §3 dependency). Prereq: ASM-06; bench Rail B source (current-limited). Do: power
  via CN-08 from bench, command centre with the existing control/test setup, fit an
  ordinary metal 25T horn **vertical at neutral**, final-tighten horn screw. This is
  a mechanical procedure and requires no firmware change. Test → pass: horn repeats
  centre ±1° after power cycle. STOP: servo
  doesn't fit holder or won't centre → Gate D residual reopens. Evidence: ASM note.
- **ASM-08 Steering linkage closure.** Prereq: ASM-07. Needs: rod, tie rods,
  turnbuckles, ball studs. Do: place `servosaverv7` on the front M3 boss (never on
  the servo spline), then link horn → saver per drawing `[3]`; equal-length links;
  toe ≈0. **Record shaft/horn hole, spacer stack, three rod heights + sweep → closes
  D-26.** Test:
  full lock-to-lock by firmware, no bind, no contact with PS-01 volume mock.
  📷 yes (rod line photo with rule).
- **ASM-09 Front suspension.** Do: per drawing `[3]`: tower, arms, uprights, king-pins
  (tap-in — ⚠ not serviceable later, KO-18), 52 mm shocks. Test: compress/return free;
  steer sweep at full bump. Evidence: FIT entries. 📷 yes.
- **ASM-10 Rear suspension (part 1).** Prereq: **Gate A resolved** (D-14/D-15 — else
  STOP). Do: chosen stack's spring mount + rocker, dry. 📷 yes.
- **ASM-11 Rear rocker/spring-lock + 68 mm shock validation.** Purpose: Gate A
  physical confirm. Do: seat 68 mm shock, articulate full travel next to KO-06 band
  mock. Test → pass: seats AND articulates, no bind (BUILD_SHEET gate 1 wording).
  STOP: binding → back to Gate A options; **do not shim silently**. Evidence: video +
  ASM note (feeds Gate P3). 📷 yes.
- **ASM-12 Motor + drivetrain.** Prereq: ASM-11. Do: axle, bearings (per resolved
  stack), 14 mm metal sleeves **on before printed spacers** (E-05, mandatory), belt,
  spur/pinion 48P mesh with slight backlash, `beltdrivemotorlock`, motor transverse.
  Test: axle spins free; mesh check; D-16 bolt pattern confirmed. ⚠ hot zone parts =
  ASA only. 📷 yes.
- **ASM-13 Rear LED-tail pre-routing (before the stack closes).** Purpose: R-09.
  Needs: PS-09, H-08 tail with CN-13/15/11 ends + 80 mm loop. Do: lay H-08 into the
  drawing-`[7]` channel path / PS-09; leave pull-through loop accessible. STOP: if the
  chosen stack has no channel (original path) → route the PS-09 alternative **now**,
  never after. Evidence: photo before closure. 📷 yes (critical).

**Phase III — Lower electrical layer**

- **ASM-14 Lower support structure.** Prereq: ASM-05…13; D-27 slot map. Do: PS-01
  (battery tray), PS-02 (ESC mount), PS-03 (UBEC shelf), PS-15 (junction block),
  PS-08 combs — all snug to slot nuts; PS-15 bosses use inserts. Test: KO-01/KO-11
  sweeps re-run (ASM-08 rig) with structure in — no contact. 📷 yes.
- **ASM-15 Battery + main-power mock-up.** Purpose: prove the swap path before wiring.
  Needs: PS-13 battery dummy (or real pack if bought post-D-01). CN-01. Do: dummy into
  PS-01, strap, H-01 reach to PS-15. Test: swap in <60 s body-off; strap holds a shake
  test. Evidence: ASM note. 📷 no.
- **ASM-16 ESC installation.** Prereq: D-08 (real ESC measured), ASM-14. CN-04/22,
  H-03. Do: ESC on PS-02 fan-up, strap; bullets aft to motor (phase order noted);
  sensor lead; signal lead CN-22 dressed up-forward — **verify the BEC red wire is
  lifted + insulated (DN-03) before it ever meets the deck.** Test: fan gap gauge
  10 mm. 📷 yes.
- **ASM-17 Lower power harness.** Do: H-02 (Y, CN-05/06 UBEC feeds), UBEC-A/B into
  PS-03 pockets, CN-23A/B loops bridged, H-04/H-05 trunks laid on R1/R2 with combs —
  **long, uncut** (final length only at Gate P9). Test: continuity map (no meter
  surprises); no centreline crossing outside X1/X2. 📷 yes.
- **ASM-18 Main disconnect + protection.** Per DN-01/DN-02 decisions: fuse into PS-15
  seat (or blank), loop-key CN-02 fitted. Test: key reachable through cockpit opening
  body-on (mock shell hold). STOP: unreachable → PS-15 reposition before P3. 📷 yes.
- **ASM-19 Lower-layer bench test in chassis.** Purpose: Gate P5 entry. Do: bench
  supply (current-limited) → PS-15; verify UBEC outputs at CN-23 (voltage, no load);
  ESC beep-check via CN-22 (motor pinion OFF). Test → pass: rails in spec, no warm
  smell, grounds star-verified. STOP on any anomaly. Evidence: measurement note.

**Phase IV — Upper layer + periphery**

- **ASM-20 Upper deck structure.** Prereq: Gate P5 passed for the lower layer.
  Do: PS-05 posts (height = D-02 value), PS-04 deck trial-fit empty, remove. Test:
  deck plane level ±1 mm; posts don't foul UBEC leads. 📷 yes.
- **ASM-21 Regulator rail configuration + verification.** Do: set/verify UBEC output
  selects (Rail B per DN-09), re-measure at CN-23 under a 1 A dummy load each. Pass:
  ±5% at load. Evidence: noted values (pre-D-24 baseline).
- **ASM-22 ESP/controller installation (deck bench-build).** Do: on the bench: CTL-E1,
  CTL-E2 on standoffs+pads, AUD-AMP, deck-internal H-06 (UART, I2S, LED data pigtails,
  divider, CN-21), CN-07 anchor; then deck onto posts, CN-07 mated. ⚠ no Dupont
  remains at flight config (M rule — bench-only). Test: deck removal drill <60 s. 📷 yes.
- **ASM-23 RC receiver.** Do: RX onto PS-06, antenna into guide, CN-19 to deck with
  loop. Test: bind + LQ sanity at bench power. 📷 no.
- **ASM-24 Sensors.** Do: SNS-MAG glued to axle (CA), SNS-HALL on PS-16 at 1–3 mm
  (gauge), divider verified inline in H-06; CN-15 mated at X1. Test: wheel spin by
  hand → pulses seen at CTL-E1 (bench). 📷 yes (gap).
- **ASM-25 Communications / video transmitter.** **RST-06:** if the real module is
  unconfirmed, install the PS-13 **dummy** in the deck slot and continue — the real
  install requires: possession confirmed → D-06b measured → heatsink bonded →
  **antennas on U.FL before any power**. CN in H-07. Test (real only): enumerates on
  camera USB at bench power. STOP: never power the module without antennas.
- **ASM-26 Camera + gimbal.** Prereq: **Gate C set complete (D-06/D-07), owner A-vs-B
  decision, halo-occlusion check** — else install the mount-station blank and defer.
  Do: MOD-CAM (PS-10/11 build) onto its station; CN-09/10/12/24 + CN-16 at the deck
  edge (S3/DN-11); H-07 with 60 mm loops. Test: boresight straight-ahead at commanded centre; roll level by bubble/
  reference (VR §3 requirement); FOV clear of body at centre. 📷 yes.
- **ASM-27 LEDs + body-shell harness.** Do: brake strip into `rearbacklightdiffuser`
  (lens unpainted rule) terminating H-08 at CN-13; halo strip onto shell + H-09 to
  CN-14 at PS-07. Test: data-order sanity (firmware test pattern at low brightness).
  📷 yes.
- **ASM-28 Optional DRS.** Prereq: Gate B closed (RST-07). Do: MG90S into wing pocket,
  rod to horn per drawing `[2]`, CN-11 from H-08 with loop. Test: full flap travel by
  firmware, no fouling of KO-12 volume. 📷 yes.
- **ASM-29 Fan / blower / ducts.** Prereq: Gate C. Do: blower onto PS-11, duct
  (from measured `.scad`) blower→camera; CN-12. Test: airflow felt at camera; duct
  de-mates for camera service. 📷 yes.
- **ASM-30 Antennas + coax.** Do: VID-ANT whips onto PS-12 posts (V geometry), U.FL
  seated with guides; RX antenna final position check (≥150 mm to posts, ≥40 mm to
  metal). Test: tug-test guides (not the U.FL), spacing measured. 📷 yes.
- **ASM-31 Cable restraint + inspection.** Do: dress everything into PS-08 combs;
  loops verified at all M.1 stations; grommets seated; H-11 pigtails parked (if
  DN-08); labels per M.3 complete. Test: full-motion sweep (steering, suspension,
  gimbal, DRS) with fingers on the loom — nothing tugs. Evidence: photo set. 📷 yes.

**Phase V — Verification before burial (Gate P6/P7/P8 territory)**

- **ASM-32 Full electronics bench verification (before shell burial).** Purpose: the
  R-09 "verify before it's buried" dependency. Do: body OFF, bench power then battery:
  every subsystem exercised once (steer, ESC beep/no-pinion spin, gimbal, DRS, LEDs,
  audio, Hall telemetry, video link if real module). Pass: all nominal. STOP on any
  fail — fix with full access now.
- **ASM-33 Body-shell trial fit.** Do: lower shell over dressed car (KO-14), CN-14
  mate, 3× M3 into inserts. Test: nothing fouls; 5 mm gauge over tallest deck item
  (D-04 confirm); body-off drill ≤30 s + one unplug. 📷 yes.
- **ASM-34 Polarity + continuity checks.** Do: cold meter pass: battery → PS-15 →
  every CN power pin map per M.2; ESC red-wire isolation re-verified; no rail-to-rail
  short; grounds star. Evidence: signed checklist.
- **ASM-35 Current-limited power-up.** Do: bench supply at PS-15: 0.5 A limit →
  logic only; 2 A → rails sequentially via CN-23; watch for current anomalies.
  Pass: idle currents match L.4 typ column ±30%. STOP: any rail over budget → debug
  before battery. Evidence: noted values.
- **ASM-36 Rail-current measurement (D-24).** Prereq (S3): **real VID-WIFI installed
  (RST-06)** — with the dummy this step is only a partial D-24 and does not unlock P9
  Rail A sizing. Do: ammeter in CN-23A then CN-23B **plus the PS-15 input-side loop
  (the DN-01 fuse rates on the input side — S3)**; drive the D-24 state matrix
  deliberately (cold boot, LED full-white burst, servo stall bump at reduced dwell,
  WiFi max bitrate, audio peak, combined plausible peak); scope Rail A through WiFi
  bursts and Rail B at the servo connector under stall. Record peaks + 5-min sustained.
  **This closes D-24 → unlocks DN-01 rating, DN-04 cap value, Gate P9 sizing.**
  Evidence: table in `07_assembly_notes/` + update L.4.
- **ASM-37 Steering test.** Full lock-to-lock under battery power, wheels loaded on
  bench blocks; centre repeatability; no rail-B brownout of Rail A (scope/LED flicker
  watch). Pass: no resets, no bind.
- **ASM-38 Suspension test.** Full compress/rebound all corners + rear central; loom
  motion re-check. Pass: free, no contact.
- **ASM-39 Gimbal test.** Stick-driven CRSF ch9/10 sweep (firmware boundaries per
  workspace rules — **no head-tracking, no iPhone path**); hard-stop geometry recorded
  for the D-18 gate (measurement itself stays behind firmware A2/Phase B). Pass: no
  stall buzz at endpoints in the usable range.
- **ASM-40 Camera/video test.** Real module only: latency/quality at bench range,
  boresight/roll verified on-screen against a level reference. Pass: level horizon.
- **ASM-41 RF coexistence test (D-20).** ELRS LQ/RSSI logged while WiFi streams at
  max; walk-test attenuation body-on vs body-off (paint effect check, O.2). Pass: LQ
  stable at intended range envelope.
- **ASM-42 LED load test.** Full-white worst case at the DN-04 cap; measure Rail A
  during it (repeat of the D-24 state); check 1000 µF holds the strip stable.
- **ASM-43 Thermal test (D-19).** O.1 procedure: bench → body-on static → 5-min
  drive → IR sweep of all named points. Pass: O.1 limits. STOP: any PETG structural
  part over limit → duct/vent fix (DN-10 path) before continuing.
- **ASM-44 Full-power test.** First wheels-down drive: short low-speed run, then
  progressive. Watch: ESC temp, steering authority, video (if fitted), failsafe
  behaviour (kill via CN-02 loop-key once, deliberately). Pass: controlled stop on
  disconnect; no resets.
- **ASM-45 Weight + balance (D-21).** Corner scales / axle scales; record F/R + L/R;
  trim battery station in PS-01 slots (±10 mm) if needed. Evidence: numbers vs I.4
  ledger.
- **ASM-46 Fastener + connector inspection.** Torque/seat re-check after first runs;
  thread-lock metal-metal only; connector flags all present (M.3).
- **ASM-47 Serviceability demonstration.** Run the Q drills with a timer: battery
  swap, deck-out, module-out each within their stated times; no desoldering needed
  anywhere. Evidence: timed list (feeds Gate P10).
- **ASM-48 Production-CAD authorization decision.** Inputs: Gates P0–P9 all green,
  D-register current, DN register decided or explicitly deferred. Output: Gate P10
  verdict — which PS parts are authorized for production print CAD (T spec), which
  iterate. **Owner sign-off required.**

## P.7 Remaining-component physical closures (ASM-49…ASM-58)

These steps are inserted before ASM-48 authorization; numbering is appended to
preserve existing references.

- **ASM-49 ESC identity and fit (D-28).** Power disconnected. Photograph exact
  label/variant; caliper body/fan/feet/wire exits and weigh. Use the exact gauge
  with shell/S0 and rear shock installed. Pass: ≥10 mm fan-air space, ≥5 mm
  shell/static, ≥8 mm shock/belt, natural wire bends. Fail: PS-02/CAD-03 remains frozen.
- **ASM-50 battery architecture (D-31).** Install the completed steering and two
  labelled 75×45×25 dummies. Sweep steering/bump, seat shell, prove pack-1
  removal and document pack-2 interference. Pass: one active onboard, one
  off-car swap, ≥5/8 mm policies. This step does not authorize parallel packs.
- **ASM-51 rear drive metrology (D-30/D-16).** Record pulleys, belt, shaft
  shoulders, spacers and spur PCD; assemble dry, blue-check mesh and hand-rotate.
  Pass: free rotation, retained bearings, no walk/rub and serviceable pinion.
- **ASM-52 electronics/RF dress (D-32/33).** Caliper/weigh boards and power
  hardware; dress real-length 65/70 mm antennas/coax; lower/remove shell ten
  times. Pass: no tug, ≥10 mm coax bends, deck/USB service and separated rail/RF lanes.
- **ASM-53 camera/cooling gate (D-34).** Photograph camera identity, record all
  camera/blower/SCAD fields, compare A/B with halo/FOV/roll, then prove airflow
  and module removal. Pass before PS-10/11; nose remains rejected for primary.
- **ASM-54 MG90S physical fit (D-35).** Power disconnected: measure each clone,
  no-force fit pan/tilt/DRS, install horns/links and hand-sweep. Pass: ≥8 mm,
  no preload/pinch. Powered endpoints remain under the wider safety gate.
- **ASM-55 audio/light fit (D-36).** Fit speaker/amp and actual strip offcuts:
  one centre, 2+2 indicators, 2 halo. Pass: speaker port/cone clear, optical
  faces unpainted, DRS/shock/belt clear, body disconnect snag-free.
- **ASM-56 suspension/rolling travel (D-37).** Measure shock free/compressed
  geometry; close one front wheel coupon; set 5–6 mm starting ride height; body-on
  full steer+bump/droop and rear bump. Pass: no rub/bind/ground contact.
- **ASM-57 Hall gap/retention (D-38).** On final rear carrier, set 1.5 mm cold,
  hand-rotate through play and verify reliable 1–3 mm range; inspect keyed/bonded
  magnet and service loop. Pass: one clean event/rev, no contact/movement.
- **ASM-58 final mass/balance (D-39).** Weigh every module and all four corners,
  body on, running configuration. Record total, X/L axle loads, diagonals and
  ride height. Compare with the ASSUMPTION target 36–40% front, |L-CG|≤2 mm,
  cross ≤3%; tune without unsafe rear/belt ballast, then repeat.

Every failed step returns only the named support/placement to design. It does
not authorize shell relief, donor drilling or production STL by implication.

<!-- BEGIN GENERATED JOINT BUILD SEQUENCE · p0_10 -->

## P.8 Joint-controlled build sequence (generated; project-wide standard)

This appendix is the build-floor expansion of the existing ASM steps. Every
mechanical neighbour pair has one Joint ID in
[`Z_connection_joint_register.md`](Z_connection_joint_register.md); the
[sortable CSV](Z_connection_joint_register.csv) is the machine-readable twin.
It adds connection execution detail only: no fit result, value, gate, placement
or STL is changed. A checked box requires the row's physical closure to be
recorded in the ASM note. **DEFER means stop at that row.**

### Charge-module stop rule for ASM-59

Prereq: OP-49 module selection and separate charge-safety authorization. The
5 V USB-C → 2S balancing module, hidden port and charge/run interlock remain
SKU/interface TBD; 30×25×10 is a TARGET envelope only. Execute
`J-CHG-001…004` only after the real hardware is measured; no circuit,
pocket, fastener or shell cut is inferred.

### ASM-04 joint closure · Battery, power & onboard charging

- [ ] **J-PWR-008 — M3×5 heat-set insert → PS-15 junction support (DIAG-CAD).** **ASSUMPTION / HOLD**
  **First:** PS-15 production boss authorized and printed. **Hardware/interface:** heat-set M3×5 brass insert + M3 bolt from BOM kit; exact bolt length ASSUMPTION;
  M3×5 insert DOCUMENTED; PS-15 repeated-service boss exists in spec but DIAG-CAD seat is not production-authorized. **Do:** Heat-set each service insert square and flush; let cool fully before chasing with an M3 screw.
  **Retention:** insert heat-set square to boss; service screw retained by metal thread. **Tool:** temperature-controlled soldering iron + insert tip; matching hex driver after cool-down.
  **Torque/threadlock:** Insert with heat only; never torque while hot. Service screw snug; low-strength threadlock only metal–metal.
  **Close only when:** ASM-04: boss wall/depth, insertion temperature/result and hand-thread check.
- [ ] **J-BDY-001 — M3×5 heat-set insert → NEW BODY 2024 FRONT.** **ASSUMPTION / HOLD**
  **First:** Printed shell inspected and insert policy accepted. **Hardware/interface:** heat-set M3×5 brass insert + M3 bolt from BOM kit; exact bolt length ASSUMPTION;
  Three body service bosses documented for M3 mounting; actual insert OD boss wall/depth unmeasured. **Do:** Heat-set inserts only where the boss has enough wall/depth; keep each square to its mating screw axis.
  **Retention:** insert heat-set square to boss; service screw retained by metal thread. **Tool:** temperature-controlled soldering iron + insert tip; matching hex driver after cool-down.
  **Torque/threadlock:** Insert with heat only; never torque while hot. Service screw snug; low-strength threadlock only metal–metal.
  **Close only when:** ASM-04: record boss ID/wall/depth and which of three positions receives inserts.

### ASM-05 joint closure · Floor datum & chassis structure

- [ ] **J-FLR-001 — 2023 front floor → 2023 rear floor.** **VERIFIED / READY**
  **First:** ASM-04 inserts/nuts seated. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Matched tongue/groove at X=0; adjacent STL M3-class features 3.00–3.36 mm [VERIFIED]. **Do:** Slide tongue into groove on DAT-F, clamp flat, then fit the drawing-[2] M3 stack without lifting the seam.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-05: straightedge across DAT-F; record any step/rock before tightening.
- [ ] **J-FLR-002 — FloorBoard2 → 2023 front floor.** **VERIFIED / READY**
  **First:** J-FLR-001 loosely assembled. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  FloorBoard2 registered underside channel and front-floor M3 features [VERIFIED geometry]; exact bolt length ASSUMPTION. **Do:** Offer FloorBoard2 from below, align its forward hole(s), start fasteners two turns, leave loose.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-05: confirm FloorBoard2 stays in the recessed underside channel and does not bow DAT-F.
- [ ] **J-FLR-003 — FloorBoard2 → 2023 rear floor.** **VERIFIED / READY**
  **First:** J-FLR-002 started loose. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  FloorBoard2 rear hole span matches rear-floor features within 0.2 mm [VERIFIED]; exact bolt length ASSUMPTION. **Do:** Start rear FloorBoard2 fastener(s), square the floor, then snug front/rear in an alternating pattern.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-05: flat-plate rock test after all FloorBoard2 screws are snug.
- [ ] **J-FLR-004 — 2023 rear floor → rear floor 2.** **VERIFIED / READY**
  **First:** J-FLR-001…003 complete. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Two coaxial pairs at X−85.93/L±5.00, 3.00 mm STL features [VERIFIED]. **Do:** Stack rear-floor-2 on the documented lower plane, align both coaxial holes and start both M3 fasteners before snugging.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-05: confirm both plates remain coaxial and the bendable tail is free.
- [ ] **J-FLR-005 — side vent L → 2023 front floor.** **DOCUMENTED / READY**
  **First:** Datum floor flat. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Donor M3 mounting topology DOCUMENTED; exact local hole Ø and bolt length unmeasured. **Do:** Seat left vent on its keyed floor edge; install the shortest BOM M3 bolt that fully engages without protruding into the shell.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-05: caliper hole and underfloor protrusion; log chosen BOM length.
- [ ] **J-FLR-006 — side vent R → 2023 front floor.** **DOCUMENTED / READY**
  **First:** J-FLR-005 orientation established. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Donor M3 mounting topology DOCUMENTED; exact local hole Ø and bolt length unmeasured. **Do:** Mirror the left-side sequence; start all vent fasteners before snugging.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-05: caliper hole and underfloor protrusion; log chosen BOM length.
- [ ] **J-FLR-007 — floor diffuser → rear floor 2.** **ASSUMPTION / HOLD**
  **First:** J-FLR-004 complete; rear LED pull-through route still open. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Diffuser-to-floor screw topology DOCUMENTED; exact feature Ø/count on selected tail ASSUMPTION. **Do:** Offer diffuser from the rear, align without flex preload, start M3 hardware, and keep the LED channel accessible.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-05/13: measure feature Ø/count and prove the diffuser can be removed without cutting H-08.

### ASM-06 joint closure · Steering servo & holder

- [ ] **J-SRV-001 — Servoholder → 2023 rear floor.** **DOCUMENTED / READY**
  **First:** J-FLR-001…007 complete. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Floor/holder M3 feature topology DOCUMENTED; holder has no verified insert seat. **Do:** Install the 58 mm holder longitudinally on the rear floor; start both ends before snugging and keep the arch square.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-06: record floor holes, chosen BOM bolt lengths and whether nuts or plastic threads retain them.
- [ ] **J-SRV-002 — DS3235SG servo → Servoholder.** **ASSUMPTION / HOLD**
  **First:** J-SRV-001 snug; DS3235SG unpowered. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  42×18.5 mm holder arch VERIFIED; servo side face 40×20 mm DOCUMENTED; ear holes/stack ASSUMPTION. **Do:** No-force side-on fit with shaft horizontal/lateral; align both ear pairs and fit BOM M3 hardware only if the ears land without case preload.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-06: record ear-hole Ø/pitch, spacer stack and the selected 8/10/12/20/30 mm bolt length.
- [ ] **J-SRV-003 — DS3235SG servo → 2023 rear floor.** **ASSUMPTION / READY**
  **First:** J-SRV-002 dry-fitted. **Hardware/interface:** no fastener; designed shell/floor landing contact;
  Servo case-to-floor/holder clearance is a physical landing; no direct fastener [ASSUMPTION]. **Do:** Confirm the servo body is supported by the holder rather than wedged between floor and arch; retain a lead exit with no pinch.
  **Retention:** gravity/contact landing with nearby registered fasteners carrying retention. **Tool:** feeler gauges + inspection light.
  **Torque/threadlock:** No torque/threadlock at the landing itself; do not shim unless a later decision authorizes it.
  **Close only when:** ASM-06: 0.1 mm feeler/no-force test around case and lead; STOP if the documented 20 mm face will not pass.

### ASM-07 joint closure · Steering servo & holder

- [ ] **J-SRV-004 — DS3235SG servo → 25T metal horn.** **DOCUMENTED / READY**
  **First:** J-SRV-002 accepted; servo powered and centred. **Hardware/interface:** DS3235SG 25T metal horn + servo's own horn screw;
  25T spline and horn radii 19.5/23.5 mm DOCUMENTED; supplied horn-screw thread not independently measured. **Do:** At commanded neutral, press the ordinary metal horn onto the 25T spline vertically; install the servo's own horn screw.
  **Retention:** press horn onto 25T spline at neutral; centre screw retains it. **Tool:** servo tester/control setup + matching driver for the supplied horn screw.
  **Torque/threadlock:** Seat fully without rocking; final-tighten only after centring. Threadlock only if servo maker permits it.
  **Close only when:** ASM-07: power-cycle centre repeatability ±1° and photograph selected horn-hole radius.

### ASM-08 joint closure · Steering output chain

- [ ] **J-STR-001 — 25T metal horn → M3 ball stud.** **ASSUMPTION / READY**
  **First:** J-SRV-004 centred. **Hardware/interface:** M3 ball stud + M4 rod-end + M4 threaded rod cut to ≈22 mm, all from supplied BOM;
  Horn outer hole at 19.5 or 23.5 mm radius DOCUMENTED; hole Ø/thread for M3 ball stud ASSUMPTION. **Do:** Select the least aggressive usable horn radius, fit the M3 ball stud with its supplied nut/thread, and orient the ball toward the rod line.
  **Retention:** rod-end clips on ball; M4 thread carries axial adjustment; ball stud retained by its M3 thread/nut. **Tool:** calipers, fine saw/cutoff tool, file, two small spanners, ball-end pliers if available.
  **Torque/threadlock:** Deburr cut rod. Equal thread engagement both ends. Low-strength threadlock only at final metal–metal threads.
  **Close only when:** ASM-08: gauge horn hole Ø, record 19.5/23.5 selection and retention side.
- [ ] **J-STR-002 — M3 ball stud → M4 rod-end.** **ASSUMPTION / READY**
  **First:** J-STR-001 complete. **Hardware/interface:** M3 ball stud + M4 rod-end + M4 threaded rod cut to ≈22 mm, all from supplied BOM;
  M3 ball / M4 rod-end pairing is BOM-listed topology; actual ball cup fit ASSUMPTION. **Do:** Press the near M4 rod-end squarely over the horn ball by hand/ball-end pliers; do not lever on the servo shaft.
  **Retention:** rod-end clips on ball; M4 thread carries axial adjustment; ball stud retained by its M3 thread/nut. **Tool:** calipers, fine saw/cutoff tool, file, two small spanners, ball-end pliers if available.
  **Torque/threadlock:** Deburr cut rod. Equal thread engagement both ends. Low-strength threadlock only at final metal–metal threads.
  **Close only when:** ASM-08: snap/tug test and articulation through the horn sweep.
- [ ] **J-STR-003 — M4 rod-end → M4 threaded rod cut ≈22 mm.** **DOCUMENTED / READY**
  **First:** Rod cut, ends deburred. **Hardware/interface:** M3 ball stud + M4 rod-end + M4 threaded rod cut to ≈22 mm, all from supplied BOM;
  M4 female rod-end thread + ≈22 mm M4 threaded rod DOCUMENTED; engagement depth ASSUMPTION. **Do:** Thread the near rod-end halfway onto the cut M4 rod and count turns.
  **Retention:** rod-end clips on ball; M4 thread carries axial adjustment; ball stud retained by its M3 thread/nut. **Tool:** calipers, fine saw/cutoff tool, file, two small spanners, ball-end pliers if available.
  **Torque/threadlock:** Deburr cut rod. Equal thread engagement both ends. Low-strength threadlock only at final metal–metal threads.
  **Close only when:** ASM-08: record cut length, thread engagement and exposed thread.
- [ ] **J-STR-004 — M4 threaded rod cut ≈22 mm → M4 rod-end.** **DOCUMENTED / READY**
  **First:** J-STR-003. **Hardware/interface:** M3 ball stud + M4 rod-end + M4 threaded rod cut to ≈22 mm, all from supplied BOM;
  Second M4 rod-end on the same ≈22 mm threaded rod DOCUMENTED; finished centre distance ASSUMPTION. **Do:** Thread the far rod-end by the same turn count; orient both cups without twisting the rod.
  **Retention:** rod-end clips on ball; M4 thread carries axial adjustment; ball stud retained by its M3 thread/nut. **Tool:** calipers, fine saw/cutoff tool, file, two small spanners, ball-end pliers if available.
  **Torque/threadlock:** Deburr cut rod. Equal thread engagement both ends. Low-strength threadlock only at final metal–metal threads.
  **Close only when:** ASM-08: caliper finished ball-centre distance and confirm equal engagement.
- [ ] **J-STR-005 — M4 rod-end → M3 ball stud.** **ASSUMPTION / READY**
  **First:** Servo saver not yet pivot-clamped. **Hardware/interface:** M3 ball stud + M4 rod-end + M4 threaded rod cut to ≈22 mm, all from supplied BOM;
  Far rod-end clips to M3 ball stud on saver side-input arm; fit ASSUMPTION. **Do:** Snap the far rod-end onto the saver-side ball stud while the saver can still be lifted for access.
  **Retention:** rod-end clips on ball; M4 thread carries axial adjustment; ball stud retained by its M3 thread/nut. **Tool:** calipers, fine saw/cutoff tool, file, two small spanners, ball-end pliers if available.
  **Torque/threadlock:** Deburr cut rod. Equal thread engagement both ends. Low-strength threadlock only at final metal–metal threads.
  **Close only when:** ASM-08: articulation/tug check at both lock limits.
- [ ] **J-STR-006 — M3 ball stud → servosaverv7.** **ASSUMPTION / READY**
  **First:** J-STR-005. **Hardware/interface:** M3 ball stud + M4 rod-end + M4 threaded rod cut to ≈22 mm, all from supplied BOM;
  Saver side-input feature location VERIFIED; printed hole is not proven M3 threaded and requires drilling/retention decision. **Do:** Trial the M3 ball stud in the saver side-input feature; use a nut only if the feature is through and accessible—do not cut an assumed thread.
  **Retention:** rod-end clips on ball; M4 thread carries axial adjustment; ball stud retained by its M3 thread/nut. **Tool:** calipers, fine saw/cutoff tool, file, two small spanners, ball-end pliers if available.
  **Torque/threadlock:** Deburr cut rod. Equal thread engagement both ends. Low-strength threadlock only at final metal–metal threads.
  **Close only when:** ASM-08: measure hole Ø/depth and record nut vs thread retention before final assembly.
- [ ] **J-STR-007 — servosaverv7 → Suspension Block_10.** **VERIFIED / READY**
  **First:** Front suspension block fixed but linkage loose. **Hardware/interface:** M3×30 dowel king pin + supplied circlip; no substitute screw unless the physical check selects it;
  Saver pivot bore 2.90×2.97 mm through 26.50 mm [VERIFIED]; vertical M3 boss [VERIFIED topology]. **Do:** Lower saver onto the vertical M3 boss; retain with the actual dowel+circlip or M3 screw stack selected by the physical boss check.
  **Retention:** dowel through aligned bores; circlip in the supplied groove. **Tool:** smooth-jaw pliers / light press + circlip pliers; calipers.
  **Torque/threadlock:** No threadlock. Do not hammer through a tight printed bore; rework only from a recorded FIT result.
  **Close only when:** ASM-08: record boss Ø/height, selected pin/screw, washer/spacer stack and free axial play.
- [ ] **J-STR-008 — servosaverv7 → M3 ball stud.** **ASSUMPTION / READY**
  **First:** J-STR-007. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  Saver left forward-link hole location VERIFIED; M3 thread/retention ASSUMPTION. **Do:** Fit the left M3 ball stud to the corresponding saver output hole; keep ball height matched to the opposite side.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: measure left hole Ø/depth, retention and ball-centre height.
- [ ] **J-STR-009 — M3 ball stud → 3Racing M3 tie-rod end.** **ASSUMPTION / READY**
  **First:** J-STR-008. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  M3 ball stud to 3Racing tie-rod end / 3×32 turnbuckle topology DOCUMENTED; cup fit ASSUMPTION. **Do:** Clip the left inner 3Racing M3 tie-rod end squarely over the saver ball.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: record left inner cup fit and initial ball-centre length.
- [ ] **J-STR-016 — 3Racing M3 tie-rod end → 3×32 turnbuckle.** **ASSUMPTION / READY**
  **First:** J-STR-009. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  3Racing M3 tie-rod end threads onto one end of the 3×32 turnbuckle; handedness and engagement are physical. **Do:** Identify the left inner turnbuckle thread direction, then install the tie-rod end to a counted starting engagement.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: mark left inner thread handedness and record engaged length.
- [ ] **J-STR-010 — 3×32 turnbuckle → 3Racing M3 tie-rod end.** **ASSUMPTION / READY**
  **First:** J-STR-016. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  Second 3Racing M3 tie-rod end threads onto the opposite 3×32 turnbuckle end; handedness/engagement physical. **Do:** Install the left far tie-rod end with equal engagement and orient its cup toward the upright ball.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: mark left far thread handedness and match inner engagement.
- [ ] **J-STR-017 — 3Racing M3 tie-rod end → M3 ball stud.** **ASSUMPTION / READY**
  **First:** J-STR-010. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  Far 3Racing M3 tie-rod end clips to upright M3 ball stud; cup/ball fit ASSUMPTION. **Do:** Clip the left far tie-rod end over the upright ball without side-loading the cup.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: snap/tug test and full bump/lock articulation.
- [ ] **J-STR-011 — M3 ball stud → front upright L.** **ASSUMPTION / READY**
  **First:** J-STR-017. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  Left upright steering-arm M3 interface topology DOCUMENTED; hole Ø/thread ASSUMPTION. **Do:** Fit the left upright ball stud only after its hole/retention is identified; match ball height left/right.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: measure left upright feature and record nut/thread plus spacer stack.
- [ ] **J-STR-012 — servosaverv7 → M3 ball stud.** **ASSUMPTION / READY**
  **First:** J-STR-007. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  Saver right forward-link hole location VERIFIED; M3 thread/retention ASSUMPTION. **Do:** Fit the right M3 ball stud to the corresponding saver output hole; keep ball height matched to the opposite side.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: measure right hole Ø/depth, retention and ball-centre height.
- [ ] **J-STR-013 — M3 ball stud → 3Racing M3 tie-rod end.** **ASSUMPTION / READY**
  **First:** J-STR-012. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  M3 ball stud to 3Racing tie-rod end / 3×32 turnbuckle topology DOCUMENTED; cup fit ASSUMPTION. **Do:** Clip the right inner 3Racing M3 tie-rod end squarely over the saver ball.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: record right inner cup fit and initial ball-centre length.
- [ ] **J-STR-018 — 3Racing M3 tie-rod end → 3×32 turnbuckle.** **ASSUMPTION / READY**
  **First:** J-STR-013. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  3Racing M3 tie-rod end threads onto one end of the 3×32 turnbuckle; handedness and engagement are physical. **Do:** Identify the right inner turnbuckle thread direction, then install the tie-rod end to a counted starting engagement.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: mark right inner thread handedness and record engaged length.
- [ ] **J-STR-014 — 3×32 turnbuckle → 3Racing M3 tie-rod end.** **ASSUMPTION / READY**
  **First:** J-STR-018. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  Second 3Racing M3 tie-rod end threads onto the opposite 3×32 turnbuckle end; handedness/engagement physical. **Do:** Install the right far tie-rod end with equal engagement and orient its cup toward the upright ball.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: mark right far thread handedness and match inner engagement.
- [ ] **J-STR-019 — 3Racing M3 tie-rod end → M3 ball stud.** **ASSUMPTION / READY**
  **First:** J-STR-014. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  Far 3Racing M3 tie-rod end clips to upright M3 ball stud; cup/ball fit ASSUMPTION. **Do:** Clip the right far tie-rod end over the upright ball without side-loading the cup.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: snap/tug test and full bump/lock articulation.
- [ ] **J-STR-015 — M3 ball stud → front upright R.** **ASSUMPTION / READY**
  **First:** J-STR-019. **Hardware/interface:** M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM;
  Right upright steering-arm M3 interface topology DOCUMENTED; hole Ø/thread ASSUMPTION. **Do:** Fit the right upright ball stud only after its hole/retention is identified; match ball height left/right.
  **Retention:** tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention. **Tool:** calipers, two small spanners and ball-end pliers if available.
  **Torque/threadlock:** Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.
  **Close only when:** ASM-08: measure right upright feature and record nut/thread plus spacer stack.

### ASM-09 joint closure · Front suspension & rolling

- [ ] **J-FRT-001 — Suspension Block_10 → 2023 front floor.** **VERIFIED / READY**
  **First:** J-FLR-001…007 and J-STR-007 access plan. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Four matched M3 centres in block/floor [VERIFIED]; exact bolt length ASSUMPTION. **Do:** Place the complete front block on the front-floor datum, start all four M3 fasteners, square it, then snug diagonally.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-09: log selected bolt lengths/nut seats and verify block cannot rock.
- [ ] **J-FRT-002 — Crossarm3_extended → Suspension Block_10.** **DOCUMENTED / READY**
  **First:** J-FRT-001 loose. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Left crossarm pivot uses GuideRod or optional D5×M3×5 sleeve [DOCUMENTED]; bore fit unmeasured. **Do:** Align the left crossarm pivot, press/tap the selected GuideRod/sleeve squarely, and stop if plastic whitens.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-09: caliper left bore/pin and record press force/free pivot.
- [ ] **J-FRT-003 — Crossarm3_extended → Suspension Block_10.** **DOCUMENTED / READY**
  **First:** J-FRT-001 loose. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Right crossarm pivot uses GuideRod or optional D5×M3×5 sleeve [DOCUMENTED]; bore fit unmeasured. **Do:** Align the right crossarm pivot, press/tap the selected GuideRod/sleeve squarely, and stop if plastic whitens.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-09: caliper right bore/pin and record press force/free pivot.
- [ ] **J-FRT-004 — Arm4 → Suspension Block_10.** **DOCUMENTED / READY**
  **First:** J-FRT-001 loose. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Left lower-arm pivot uses GuideRod or optional D5×M3×5 sleeve [DOCUMENTED]; bore fit unmeasured. **Do:** Align the left lower arm, insert the guide/sleeve without mushrooming the printed end, and confirm gravity-free pivot.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-09: measure left pivot and record sleeve vs printed GuideRod.
- [ ] **J-FRT-005 — Arm4 → Suspension Block_10.** **DOCUMENTED / READY**
  **First:** J-FRT-001 loose. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Right lower-arm pivot uses GuideRod or optional D5×M3×5 sleeve [DOCUMENTED]; bore fit unmeasured. **Do:** Align the right lower arm, insert the guide/sleeve without mushrooming the printed end, and confirm gravity-free pivot.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-09: measure right pivot and record sleeve vs printed GuideRod.
- [ ] **J-FRT-006 — front upright L → Arm4.** **ASSUMPTION / HOLD**
  **First:** J-FRT-004. **Hardware/interface:** M3×30 dowel king pin + supplied circlip; no substitute screw unless the physical check selects it;
  Left king-pin path nominal Ø3 mm; exact printed bore remains D-05 [ASSUMPTION]. **Do:** Align upright and arm bores, insert the M3×30 dowel from the serviceable side, then fit its circlip.
  **Retention:** dowel through aligned bores; circlip in the supplied groove. **Tool:** smooth-jaw pliers / light press + circlip pliers; calipers.
  **Torque/threadlock:** No threadlock. Do not hammer through a tight printed bore; rework only from a recorded FIT result.
  **Close only when:** ASM-09/D-05: measure left bore and king pin; prove free steer with circlip seated.
- [ ] **J-FRT-007 — front upright R → Arm4.** **ASSUMPTION / HOLD**
  **First:** J-FRT-005. **Hardware/interface:** M3×30 dowel king pin + supplied circlip; no substitute screw unless the physical check selects it;
  Right king-pin path nominal Ø3 mm; exact printed bore remains D-05 [ASSUMPTION]. **Do:** Align upright and arm bores, insert the M3×30 dowel from the serviceable side, then fit its circlip.
  **Retention:** dowel through aligned bores; circlip in the supplied groove. **Tool:** smooth-jaw pliers / light press + circlip pliers; calipers.
  **Torque/threadlock:** No threadlock. Do not hammer through a tight printed bore; rework only from a recorded FIT result.
  **Close only when:** ASM-09/D-05: measure right bore and king pin; prove free steer with circlip seated.
- [ ] **J-FRT-008 — 52 mm front shock → Suspension Block_10.** **ASSUMPTION / HOLD**
  **First:** J-FRT-002. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  52 mm shock eye to left upper M3 mount DOCUMENTED; eye bushing width/hole Ø and spacer stack ASSUMPTION. **Do:** Fit the left upper shock eye with no side preload; choose a BOM M3 bolt only after the eye and boss stack are measured.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-09/56: record left upper eye Ø/width, bolt length and free articulation.
- [ ] **J-FRT-009 — 52 mm front shock → Arm4.** **ASSUMPTION / HOLD**
  **First:** J-FRT-006. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  52 mm shock eye to left lower M3 mount DOCUMENTED; eye bushing width/hole Ø and spacer stack ASSUMPTION. **Do:** Fit the left lower shock eye with no side preload; choose a BOM M3 bolt only after the eye and boss stack are measured.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-09/56: record left lower eye Ø/width, bolt length and free articulation.
- [ ] **J-FRT-010 — 52 mm front shock → Suspension Block_10.** **ASSUMPTION / HOLD**
  **First:** J-FRT-003. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  52 mm shock eye to right upper M3 mount DOCUMENTED; eye bushing width/hole Ø and spacer stack ASSUMPTION. **Do:** Fit the right upper shock eye with no side preload; choose a BOM M3 bolt only after the eye and boss stack are measured.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-09/56: record right upper eye Ø/width, bolt length and free articulation.
- [ ] **J-FRT-011 — 52 mm front shock → Arm4.** **ASSUMPTION / HOLD**
  **First:** J-FRT-007. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  52 mm shock eye to right lower M3 mount DOCUMENTED; eye bushing width/hole Ø and spacer stack ASSUMPTION. **Do:** Fit the right lower shock eye with no side preload; choose a BOM M3 bolt only after the eye and boss stack are measured.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-09/56: record right lower eye Ø/width, bolt length and free articulation.
- [ ] **J-FRT-012 — 8×12×3.5 bearing → front rotating hub.** **DOCUMENTED / HOLD**
  **First:** Wheel hub deburred and clean. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  8 mm ID ×12 mm OD ×3.5 mm bearing DOCUMENTED; hub seat Ø12 requires D-22 physical confirm. **Do:** Press the left outer bearing squarely into the rotating front hub, supporting the outer race.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-09/D-22: caliper seat and verify left outer bearing is fully shoulder-seated.
- [ ] **J-FRT-013 — 8×12×3.5 bearing → front rotating hub.** **DOCUMENTED / HOLD**
  **First:** Wheel hub deburred and clean. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  8 mm ID ×12 mm OD ×3.5 mm bearing DOCUMENTED; hub seat Ø12 requires D-22 physical confirm. **Do:** Press the left inner bearing squarely into the rotating front hub, supporting the outer race.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-09/D-22: caliper seat and verify left inner bearing is fully shoulder-seated.
- [ ] **J-FRT-014 — 8×12×3.5 bearing → front rotating hub.** **DOCUMENTED / HOLD**
  **First:** Wheel hub deburred and clean. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  8 mm ID ×12 mm OD ×3.5 mm bearing DOCUMENTED; hub seat Ø12 requires D-22 physical confirm. **Do:** Press the right outer bearing squarely into the rotating front hub, supporting the outer race.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-09/D-22: caliper seat and verify right outer bearing is fully shoulder-seated.
- [ ] **J-FRT-015 — 8×12×3.5 bearing → front rotating hub.** **DOCUMENTED / HOLD**
  **First:** Wheel hub deburred and clean. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  8 mm ID ×12 mm OD ×3.5 mm bearing DOCUMENTED; hub seat Ø12 requires D-22 physical confirm. **Do:** Press the right inner bearing squarely into the rotating front hub, supporting the outer race.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-09/D-22: caliper seat and verify right inner bearing is fully shoulder-seated.
- [ ] **J-FRT-016 — front rotating hub → front upright L.** **ASSUMPTION / READY**
  **First:** Both left bearings seated. **Hardware/interface:** M4 bolt / M4 threaded element from listed steering or belt-drive hardware; exact form noted in interface;
  Left rotating-hub spindle/retention thread is mesh-present but unmeasured; bearing ID is Ø8 DOCUMENTED. **Do:** Insert the rotating hub through the left upright/bearing stack and hand-check axial play before any locking nut.
  **Retention:** threaded retention; nut/axle internal thread only if physically present. **Tool:** matching hex driver/spanner; calipers.
  **Torque/threadlock:** Do not force printed threads. Low-strength threadlock only metal–metal after free-motion check.
  **Close only when:** ASM-09: record spindle Ø/thread and any washer/spacer stack.
- [ ] **J-FRT-017 — front rotating hub → front upright R.** **ASSUMPTION / READY**
  **First:** Both right bearings seated. **Hardware/interface:** M4 bolt / M4 threaded element from listed steering or belt-drive hardware; exact form noted in interface;
  Right rotating-hub spindle/retention thread is mesh-present but unmeasured; bearing ID is Ø8 DOCUMENTED. **Do:** Insert the rotating hub through the right upright/bearing stack and hand-check axial play before any locking nut.
  **Retention:** threaded retention; nut/axle internal thread only if physically present. **Tool:** matching hex driver/spanner; calipers.
  **Torque/threadlock:** Do not force printed threads. Low-strength threadlock only metal–metal after free-motion check.
  **Close only when:** ASM-09: record spindle Ø/thread and any washer/spacer stack.
- [ ] **J-FRT-018 — front F104 rim → front rotating hub.** **ASSUMPTION / READY**
  **First:** J-FRT-016. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Printed rim-to-hub keyed interface exists [VERIFIED silhouette]; exact locking feature/quantity ASSUMPTION. **Do:** Seat the left front rim fully on the rotating hub without forcing the bead seat.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-09: mark orientation and verify zero rocking before retention.
- [ ] **J-FRT-019 — front F104 rim → front rotating hub.** **ASSUMPTION / READY**
  **First:** J-FRT-017. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Printed rim-to-hub keyed interface exists [VERIFIED silhouette]; exact locking feature/quantity ASSUMPTION. **Do:** Seat the right front rim fully on the rotating hub without forcing the bead seat.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-09: mark orientation and verify zero rocking before retention.
- [ ] **J-FRT-020 — front locking nut → front rotating hub.** **ASSUMPTION / READY**
  **First:** J-FRT-018. **Hardware/interface:** M4 bolt / M4 threaded element from listed steering or belt-drive hardware; exact form noted in interface;
  Printed locking-nut thread exists; diameter/pitch and mating spindle thread unmeasured [ASSUMPTION]. **Do:** Start the left printed locknut by hand only and stop at first resistance; retain only after free wheel rotation is proven.
  **Retention:** threaded retention; nut/axle internal thread only if physically present. **Tool:** matching hex driver/spanner; calipers.
  **Torque/threadlock:** Do not force printed threads. Low-strength threadlock only metal–metal after free-motion check.
  **Close only when:** ASM-09: identify thread and record hand-tight position; no threadlock in plastic.
- [ ] **J-FRT-021 — front locking nut → front rotating hub.** **ASSUMPTION / READY**
  **First:** J-FRT-019. **Hardware/interface:** M4 bolt / M4 threaded element from listed steering or belt-drive hardware; exact form noted in interface;
  Printed locking-nut thread exists; diameter/pitch and mating spindle thread unmeasured [ASSUMPTION]. **Do:** Start the right printed locknut by hand only and stop at first resistance; retain only after free wheel rotation is proven.
  **Retention:** threaded retention; nut/axle internal thread only if physically present. **Tool:** matching hex driver/spanner; calipers.
  **Torque/threadlock:** Do not force printed threads. Low-strength threadlock only metal–metal after free-motion check.
  **Close only when:** ASM-09: identify thread and record hand-tight position; no threadlock in plastic.
- [ ] **J-FRT-022 — Tamiya F104 front tyre → front F104 rim.** **ASSUMPTION / DEFER**
  **First:** Tyres physically present and one wheel coupon accepted. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Tamiya F104 tyre/rim bead DOCUMENTED; actual bead fit and bond gap unmeasured. **Do:** DEFER left tyre installation; dry-seat first, then use only the BOM-v2 tyre-bond system after bead fit passes.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-09/56: record bead fit/runout and selected documented tyre adhesive.
- [ ] **J-FRT-023 — Tamiya F104 front tyre → front F104 rim.** **ASSUMPTION / DEFER**
  **First:** Tyres physically present and one wheel coupon accepted. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Tamiya F104 tyre/rim bead DOCUMENTED; actual bead fit and bond gap unmeasured. **Do:** DEFER right tyre installation; dry-seat first, then use only the BOM-v2 tyre-bond system after bead fit passes.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-09/56: record bead fit/runout and selected documented tyre adhesive.

### ASM-10 joint closure · Rear suspension & drivetrain

- [ ] **J-REA-001 — rear axle carrier L → 2023 rear floor.** **ASSUMPTION / HOLD**
  **First:** Gate A stack selection. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Left carrier-to-floor M3 topology DOCUMENTED; selected original-vs-Rev-1 stack unresolved. **Do:** Dry-place the left carrier on its floor seats; start all M3 screws but do not final-tighten until both bearings share one shaft axis.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-10/51: identify selected carrier path, hole Ø/count, bolt lengths and retention.
- [ ] **J-REA-002 — rear axle carrier R → 2023 rear floor.** **ASSUMPTION / HOLD**
  **First:** Gate A stack selection. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Right carrier-to-floor M3 topology DOCUMENTED; selected original-vs-Rev-1 stack unresolved. **Do:** Dry-place the right carrier on its floor seats; start all M3 screws but do not final-tighten until both bearings share one shaft axis.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-10/51: identify selected carrier path, hole Ø/count, bolt lengths and retention.
- [ ] **J-REA-025 — rear spring mount / rocker → 2023 rear floor.** **ASSUMPTION / HOLD**
  **First:** Gate A selection. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Original/Rev-1 rear spring-mount M3 topology DOCUMENTED; selected stack unresolved. **Do:** Dry-fit only the selected spring mount to the floor/rear stack; start all screws and leave loose for rocker alignment.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-10: identify selected STL, hole Ø/count, bolt lengths and nut/insert retention.
- [ ] **J-REA-026 — spring block → rear spring mount / rocker.** **ASSUMPTION / HOLD**
  **First:** J-REA-025. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Spring-block-to-mount topology DOCUMENTED; pivot/fastener stack unmeasured. **Do:** Assemble the spring block/rocker dry with the selected M3 stack; preserve free articulation.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-10: record pivot Ø, spacer stack, retention and free travel.
- [ ] **J-REA-029 — preferred 2021 DRS rear wing → rear spring mount / rocker.** **ASSUMPTION / HOLD**
  **First:** Selected stack and wing accepted together. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Preferred 2021 wing-to-original rear-stack topology DOCUMENTED; hole/count/stack still Gate A/B. **Do:** Dry-offer wing to the spring-mount/backplate interface; start M3s only when all holes register without bending the wing.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-10: record wing holes, exact BOM bolt lengths and nut/insert retention.

### ASM-11 joint closure · Rear suspension & drivetrain

- [ ] **J-REA-027 — 68 mm rear shock → spring block.** **ASSUMPTION / DEFER**
  **First:** Rear 68 mm shock arrival + J-REA-025/026. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  68 mm eye-to-eye DOCUMENTED; eye Ø/width/bushing and lower mount ASSUMPTION. **Do:** DEFER lower shock eye connection until the real shock is measured; do not shim or drill the selected rocker.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-11: caliper eye/bushing and record BOM M3 bolt/spacer stack through full travel.
- [ ] **J-REA-028 — 68 mm rear shock → 2023 rear floor.** **ASSUMPTION / DEFER**
  **First:** Rear 68 mm shock arrival + J-REA-027. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  68 mm upper-eye station DOCUMENTED topology; exact receiver and M3 stack ASSUMPTION. **Do:** DEFER upper eye; install only after the selected stack seats the lower eye without side load.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-11: record upper boss/hole Ø, bolt length, spacer stack and articulation.

### ASM-12 joint closure · Rear suspension & drivetrain

- [ ] **J-REA-003 — 12×21×5 rear bearing → rear axle carrier L.** **DOCUMENTED / HOLD**
  **First:** J-REA-001 dry located. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Rear bearing 12×21×5 DOCUMENTED; Ø21 carrier seat is path-dependent and unverified. **Do:** Press the left rear bearing squarely into the selected carrier/motor cover, supporting the outer race.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-12/51: caliper Ø21 seat, confirm shoulder depth and retention against axle walk.
- [ ] **J-REA-004 — 12×21×5 rear bearing → rear axle carrier R.** **DOCUMENTED / HOLD**
  **First:** J-REA-002 dry located. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Rear bearing 12×21×5 DOCUMENTED; Ø21 carrier seat is path-dependent and unverified. **Do:** Press the right rear bearing squarely into the selected carrier/motor cover, supporting the outer race.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-12/51: caliper Ø21 seat, confirm shoulder depth and retention against axle walk.
- [ ] **J-REA-005 — belt-set output shaft → 12×21×5 rear bearing.** **ASSUMPTION / HOLD**
  **First:** J-REA-003/004 seated and coaxial. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Output shaft Ø/shoulders TBD; bearing ID Ø12 DOCUMENTED. **Do:** Pass the output shaft through both bearings without using the thread/end as a drift; hand-rotate before adding spacers.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-51: record shaft journals/shoulders/span and free-rotation baseline.
- [ ] **J-REA-006 — 14 mm-ID metal spacer → left printed spacer.** **DOCUMENTED / HOLD**
  **First:** J-REA-005 rotates freely. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Left Inboard stack uses 14 mm-ID metal sleeve before printed spacer [DOCUMENTED]; cut length TBD. **Do:** Slide/cut the left inboard metal sleeve first, then the printed spacer; do not omit or swap order.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-12/51: record sleeve cut length, printed-spacer identity and axial endplay.
- [ ] **J-REA-007 — 14 mm-ID metal spacer → NewSpacerleft.** **DOCUMENTED / HOLD**
  **First:** J-REA-005 rotates freely. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Left Outboard stack uses 14 mm-ID metal sleeve before printed spacer [DOCUMENTED]; cut length TBD. **Do:** Slide/cut the left outboard metal sleeve first, then the printed spacer; do not omit or swap order.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-12/51: record sleeve cut length, printed-spacer identity and axial endplay.
- [ ] **J-REA-008 — 14 mm-ID metal spacer → right printed spacer.** **DOCUMENTED / HOLD**
  **First:** J-REA-005 rotates freely. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Right Inboard stack uses 14 mm-ID metal sleeve before printed spacer [DOCUMENTED]; cut length TBD. **Do:** Slide/cut the right inboard metal sleeve first, then the printed spacer; do not omit or swap order.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-12/51: record sleeve cut length, printed-spacer identity and axial endplay.
- [ ] **J-REA-009 — 14 mm-ID metal spacer → NewSpacerright.** **DOCUMENTED / HOLD**
  **First:** J-REA-005 rotates freely. **Hardware/interface:** specified BOM bearing / press-fit part; no added fastener;
  Right Outboard stack uses 14 mm-ID metal sleeve before printed spacer [DOCUMENTED]; cut length TBD. **Do:** Slide/cut the right outboard metal sleeve first, then the printed spacer; do not omit or swap order.
  **Retention:** square press fit against the correct race/shoulder. **Tool:** arbor press or smooth-jaw vice + square drift; calipers.
  **Torque/threadlock:** No screw torque or threadlock. Press on the race supported by the receiving feature.
  **Close only when:** ASM-12/51: record sleeve cut length, printed-spacer identity and axial endplay.
- [ ] **J-REA-010 — belt-set axle pulley → belt-set output shaft.** **ASSUMPTION / HOLD**
  **First:** J-REA-005…009 dry stack. **Hardware/interface:** belt-drive set + 140 mm belt; included pulley hardware only;
  Belt-set pulley bore/retention and shaft flat/key are unmeasured [ASSUMPTION]. **Do:** Install the axle pulley using only its included hardware; align its belt plane before retention.
  **Retention:** belt captured by pulley flanges and installed tension; no added keeper invented. **Tool:** hex drivers matching included hardware + straightedge; turn shaft by hand.
  **Torque/threadlock:** No numeric tension is documented. Set by the ASM-51 free-rotation check; threadlock only metal–metal screws.
  **Close only when:** ASM-51: measure pulley bore/width/retainer and shaft feature; photograph retention.
- [ ] **J-REA-011 — 75T 48P spur → belt-set axle pulley.** **ASSUMPTION / HOLD**
  **First:** J-REA-010 located. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  75T spur ↔ belt-pulley bolt PCD/count/Ø is D-16 UNKNOWN; 48P/75T is DOCUMENTED. **Do:** Offer the 75T spur to the pulley without drilling or slotting; install BOM M3 screws only if every hole registers.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-51/D-16: caliper both PCDs, hole Ø/count and screw engagement; STOP on mismatch.
- [ ] **J-REA-012 — 28T 48P pinion → Rocket 540 V3 motor.** **DOCUMENTED / READY**
  **First:** Motor out of mount. **Hardware/interface:** belt-drive set + 140 mm belt; included pulley hardware only;
  28T pinion, 48P and 3.175 mm motor shaft DOCUMENTED; included set-screw thread/flat ASSUMPTION. **Do:** Slide pinion onto the motor shaft, align its tooth plane to the spur and retain with the pinion's included set screw only.
  **Retention:** belt captured by pulley flanges and installed tension; no added keeper invented. **Tool:** hex drivers matching included hardware + straightedge; turn shaft by hand.
  **Torque/threadlock:** No numeric tension is documented. Set by the ASM-51 free-rotation check; threadlock only metal–metal screws.
  **Close only when:** ASM-12/51: measure bore/shaft, confirm set-screw lands on a flat or document round-shaft retention.
- [ ] **J-REA-013 — Rocket 540 V3 motor → beltdrivemotorlock.** **ASSUMPTION / READY**
  **First:** J-REA-012 pinion loosely located. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Motor face/lock M3 topology DOCUMENTED; Rocket 540 face pattern and bolt depth must be measured. **Do:** Bolt motor to beltdrivemotorlock with the shortest BOM M3 screws that fully engage without touching windings.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-12/51: measure face PCD/thread depth and record bolt length.
- [ ] **J-REA-014 — beltdrivemotorlock → 2023 rear floor.** **ASSUMPTION / READY**
  **First:** J-REA-013. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Donor motor-lock mounting topology DOCUMENTED; selected rear-stack receiver/bolt length ASSUMPTION. **Do:** Install motor/lock as one serviceable unit; leave mesh adjustment loose.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-12/51: record receiver holes, adjustment travel and service access.
- [ ] **J-REA-015 — 140 mm belt → belt-set axle pulley.** **ASSUMPTION / HOLD**
  **First:** J-REA-010/014. **Hardware/interface:** belt-drive set + 140 mm belt; included pulley hardware only;
  140 mm belt DOCUMENTED; pulley teeth/centres/tension unmeasured. **Do:** Loop belt over both pulleys without prying across flange teeth; set alignment and tension by hand rotation.
  **Retention:** belt captured by pulley flanges and installed tension; no added keeper invented. **Tool:** hex drivers matching included hardware + straightedge; turn shaft by hand.
  **Torque/threadlock:** No numeric tension is documented. Set by the ASM-51 free-rotation check; threadlock only metal–metal screws.
  **Close only when:** ASM-51: record tooth counts, belt width, centre distance and free rotation.
- [ ] **J-REA-016 — 28T 48P pinion → 75T 48P spur.** **DOCUMENTED / READY**
  **First:** J-REA-011…015. **Hardware/interface:** belt-drive set + 140 mm belt; included pulley hardware only;
  28T↔75T 48P mesh DOCUMENTED; backlash and installed centre distance physical. **Do:** Use a paper/blue-check mesh setup, tighten the motor lock gradually, and rotate through a full spur revolution.
  **Retention:** belt captured by pulley flanges and installed tension; no added keeper invented. **Tool:** hex drivers matching included hardware + straightedge; turn shaft by hand.
  **Torque/threadlock:** No numeric tension is documented. Set by the ASM-51 free-rotation check; threadlock only metal–metal screws.
  **Close only when:** ASM-12/51: record backlash/blue pattern and any tight spot; no powered test.
- [ ] **J-REA-017 — F104 tyreslot1 tighter → rear F104 rim.** **ASSUMPTION / HOLD**
  **First:** D-23 quantity check. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Left tighter tyreslot1/2 keyed rim interface VERIFIED as mesh; required quantity 1-vs-2 per side unresolved. **Do:** Dry-seat both candidate tyreslot pieces in the left rear rim and retain only the confirmed required set.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-12/D-23: record left adapter quantity/orientation and play.
- [ ] **J-REA-018 — F104 tyreslot1 tighter → rear F104 rim.** **ASSUMPTION / HOLD**
  **First:** D-23 quantity check. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Right tighter tyreslot1/2 keyed rim interface VERIFIED as mesh; required quantity 1-vs-2 per side unresolved. **Do:** Dry-seat both candidate tyreslot pieces in the right rear rim and retain only the confirmed required set.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-12/D-23: record right adapter quantity/orientation and play.
- [ ] **J-REA-019 — F104 tyreslot2 tighter → belt-set output shaft.** **DOCUMENTED / READY**
  **First:** J-REA-017; shaft end present. **Hardware/interface:** M4 bolt / M4 threaded element from listed steering or belt-drive hardware; exact form noted in interface;
  Drawing [7] specifies M4 bolt through tyreslot into axle; axle internal thread/depth unmeasured. **Do:** Insert the left rear wheel/adapter stack and hand-start its M4 retention only after axle thread is identified.
  **Retention:** threaded retention; nut/axle internal thread only if physically present. **Tool:** matching hex driver/spanner; calipers.
  **Torque/threadlock:** Do not force printed threads. Low-strength threadlock only metal–metal after free-motion check.
  **Close only when:** ASM-12/51: measure left axle thread/depth and select exact M4 bolt without bottoming.
- [ ] **J-REA-020 — F104 tyreslot2 tighter → belt-set output shaft.** **DOCUMENTED / READY**
  **First:** J-REA-018; shaft end present. **Hardware/interface:** M4 bolt / M4 threaded element from listed steering or belt-drive hardware; exact form noted in interface;
  Drawing [7] specifies M4 bolt through tyreslot into axle; axle internal thread/depth unmeasured. **Do:** Insert the right rear wheel/adapter stack and hand-start its M4 retention only after axle thread is identified.
  **Retention:** threaded retention; nut/axle internal thread only if physically present. **Tool:** matching hex driver/spanner; calipers.
  **Torque/threadlock:** Do not force printed threads. Low-strength threadlock only metal–metal after free-motion check.
  **Close only when:** ASM-12/51: measure right axle thread/depth and select exact M4 bolt without bottoming.
- [ ] **J-REA-021 — rear locking nut → rear F104 rim.** **ASSUMPTION / HOLD**
  **First:** J-REA-019. **Hardware/interface:** M4 bolt / M4 threaded element from listed steering or belt-drive hardware; exact form noted in interface;
  Printed rear locking nut is present but its role/thread relative to drawing-[7] M4 axle bolt is unresolved. **Do:** Do not install the left printed locknut until ASM-51 proves whether it is required in the selected wheel stack.
  **Retention:** threaded retention; nut/axle internal thread only if physically present. **Tool:** matching hex driver/spanner; calipers.
  **Torque/threadlock:** Do not force printed threads. Low-strength threadlock only metal–metal after free-motion check.
  **Close only when:** ASM-51: identify left locknut role; mark OMIT if the M4 axle bolt supersedes it.
- [ ] **J-REA-022 — rear locking nut → rear F104 rim.** **ASSUMPTION / HOLD**
  **First:** J-REA-020. **Hardware/interface:** M4 bolt / M4 threaded element from listed steering or belt-drive hardware; exact form noted in interface;
  Printed rear locking nut is present but its role/thread relative to drawing-[7] M4 axle bolt is unresolved. **Do:** Do not install the right printed locknut until ASM-51 proves whether it is required in the selected wheel stack.
  **Retention:** threaded retention; nut/axle internal thread only if physically present. **Tool:** matching hex driver/spanner; calipers.
  **Torque/threadlock:** Do not force printed threads. Low-strength threadlock only metal–metal after free-motion check.
  **Close only when:** ASM-51: identify right locknut role; mark OMIT if the M4 axle bolt supersedes it.
- [ ] **J-REA-023 — Tamiya F104 rear tyre → rear F104 rim.** **ASSUMPTION / DEFER**
  **First:** Tyres physically present and adapter quantity closed. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Tamiya F104 rear bead DOCUMENTED; actual fit/bond interface unmeasured. **Do:** DEFER the left tyre bond; dry-seat, measure runout, then use only the documented BOM-v2 tyre bond.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-12/56: record left bead/runout and bond method.
- [ ] **J-REA-024 — Tamiya F104 rear tyre → rear F104 rim.** **ASSUMPTION / DEFER**
  **First:** Tyres physically present and adapter quantity closed. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Tamiya F104 rear bead DOCUMENTED; actual fit/bond interface unmeasured. **Do:** DEFER the right tyre bond; dry-seat, measure runout, then use only the documented BOM-v2 tyre bond.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-12/56: record right bead/runout and bond method.

### ASM-13 joint closure · Lighting segments & lenses

- [ ] **J-LGT-002 — rearbacklightdiffuser → preferred 2021 DRS rear wing.** **ASSUMPTION / HOLD**
  **First:** Gate A/B rear stack chosen; H-08 laid first. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Rear light diffuser sits in selected rear stack [DOCUMENTED]; mounting hole/clip and stack path unresolved. **Do:** Install diffuser/lens only after the tail harness is in its channel; keep lens unpainted and removable.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-13/55: record receiver feature, hardware/clip and pull-through service.

### ASM-14 joint closure · Battery, power & onboard charging

- [ ] **J-PWR-001 — PS-01 battery tray (DIAG-CAD) → 2023 front floor.** **ASSUMPTION / HOLD**
  **First:** J-FLR complete; D-27 occupancy checked. **Hardware/interface:** M3×8 bolt from BOM kit + mapped floor slot nut;
  PS-01 DIAG-CAD feet + mapped floor M3 feature/clamp; final station ASSUMPTION. **Do:** Install the diagnostic tray with M3×8 at the mapped shared/free feature and its reversible clamp foot; do not drill donor floor.
  **Retention:** screw into captive floor nut; reversible. **Tool:** matching hex driver + nut driver if the captive nut is not yet seated.
  **Torque/threadlock:** Snug only against printed support. Threadlock only if both engaged threads are metal.
  **Close only when:** ASM-14/50: record exact floor feature(s), clamp engagement and pull-off test.
- [ ] **J-PWR-003 — PS-03 UBEC shelf (DIAG-CAD) → 2023 rear floor.** **ASSUMPTION / HOLD**
  **First:** D-27 occupancy. **Hardware/interface:** M3×8 bolt from BOM kit + mapped floor slot nut;
  PS-03 DIAG-CAD uses one verified right-side M3 feature plus reversible clamp [ASSUMPTION final]. **Do:** Install shelf low on DAT-F with M3×8 at the verified feature and the reversible clamp; keep both rail lanes separate.
  **Retention:** screw into captive floor nut; reversible. **Tool:** matching hex driver + nut driver if the captive nut is not yet seated.
  **Torque/threadlock:** Snug only against printed support. Threadlock only if both engaged threads are metal.
  **Close only when:** ASM-14: identify donor/shared screw and perform pull-off/flatness check.
- [ ] **J-PWR-007 — PS-15 junction support (DIAG-CAD) → 2023 rear floor.** **ASSUMPTION / HOLD**
  **First:** D-27 occupancy and disconnect reach. **Hardware/interface:** M3×8 bolt from BOM kit + mapped floor slot nut;
  PS-15 DIAG-CAD uses reversible plate clamps because no free Z2R feature exists [ASSUMPTION final]. **Do:** Clamp PS-15 to the donor plate without new holes; align connector access upward/inward.
  **Retention:** screw into captive floor nut; reversible. **Tool:** matching hex driver + nut driver if the captive nut is not yet seated.
  **Torque/threadlock:** Snug only against printed support. Threadlock only if both engaged threads are metal.
  **Close only when:** ASM-14/18: pull-off test and body-on disconnect finger reach.
- [ ] **J-ELC-008 — PS-06 RX carrier → 2023 front floor.** **ASSUMPTION / HOLD**
  **First:** ASM-08 steering sweep recorded. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  One floor M3 feature + carrier option documented; D-27/rod-sweep station physical. **Do:** Install PS-06 at the accepted quiet-side floor feature with the shortest matching BOM M3 screw.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-14/23: record station, bolt/nut, antenna clearance and no KO-01 contact.

### ASM-15 joint closure · Battery, power & onboard charging

- [ ] **J-PWR-002 — 2S pack ≤75×45×25 → PS-01 battery tray (DIAG-CAD).** **ASSUMPTION / DEFER**
  **First:** Exact 2S pack arrival + J-PWR-001. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Pack ≤75×45×25 DOCUMENTED; exact SKU, case, leads, strap path and tray fit UNKNOWN. **Do:** DEFER pack retention. Fit the exact pack/dummy and prove open-top removal before selecting the restraint.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-50: measure pack/lead exit, strap land, shake retention and body-off service.

### ASM-17 joint closure · Battery, power & onboard charging

- [ ] **J-PWR-004 — 5 A UBEC → PS-03 UBEC shelf (DIAG-CAD).** **ASSUMPTION / HOLD**
  **First:** J-PWR-003 + real UBEC measured. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  UBEC-A pocket nominal 30×14×10 ASSUMPTION; real body/lead exits unmeasured. **Do:** Seat UBEC-A in its own pocket with leads unloaded; use only pocket/declared restraint, no screw through its case.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-17/52: caliper UBEC-A, tug-test body not leads, confirm ventilation.
- [ ] **J-PWR-005 — 5 A UBEC → PS-03 UBEC shelf (DIAG-CAD).** **ASSUMPTION / HOLD**
  **First:** J-PWR-003 + real UBEC measured. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  UBEC-B pocket nominal 30×14×10 ASSUMPTION; real body/lead exits unmeasured. **Do:** Seat UBEC-B in its own pocket with leads unloaded; use only pocket/declared restraint, no screw through its case.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-17/52: caliper UBEC-B, tug-test body not leads, confirm ventilation.
- [ ] **J-PWR-006 — rail capacitor → PS-03 UBEC shelf (DIAG-CAD).** **ASSUMPTION / HOLD**
  **First:** Real capacitor selected after D-24. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Cap can Ø/height and shelf retainer ASSUMPTION; value remains governed by D-24. **Do:** Seat capacitor adjacent to its rail using the designed pocket/tie point; no lead carries mechanical load.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-17/36: measure can, retention and lead strain relief.

### ASM-20 joint closure · Electronics trays & RF hardware

- [ ] **J-ELC-001 — PS-05 deck post (DIAG-CAD) → PS-03 UBEC shelf (DIAG-CAD).** **ASSUMPTION / HOLD**
  **First:** J-PWR-003. **Hardware/interface:** heat-set M3×5 brass insert + M3 bolt from BOM kit; exact bolt length ASSUMPTION;
  PS-05 rear post landing on PS-03 documented in spec; exact station and production boss ASSUMPTION. **Do:** Install rear deck post(s) on the PS-03 shoulder/receiver and keep their axes square to DAT-F.
  **Retention:** insert heat-set square to boss; service screw retained by metal thread. **Tool:** temperature-controlled soldering iron + insert tip; matching hex driver after cool-down.
  **Torque/threadlock:** Insert with heat only; never torque while hot. Service screw snug; low-strength threadlock only metal–metal.
  **Close only when:** ASM-20: record count/stations, insert engagement and post height.
- [ ] **J-ELC-002 — PS-05 deck post (DIAG-CAD) → PS-15 junction support (DIAG-CAD).** **ASSUMPTION / HOLD**
  **First:** J-PWR-007 and physical P1. **Hardware/interface:** heat-set M3×5 brass insert + M3 bolt from BOM kit; exact bolt length ASSUMPTION;
  PS-05 front post landing on PS-15 shoulders is concept-only; recovered DIAG-CAD omits fixed shoulders. **Do:** HOLD front post connection until a non-overlapping shoulder station is proven; then use M3×5 insert service threads.
  **Retention:** insert heat-set square to boss; service screw retained by metal thread. **Tool:** temperature-controlled soldering iron + insert tip; matching hex driver after cool-down.
  **Torque/threadlock:** Insert with heat only; never torque while hot. Service screw snug; low-strength threadlock only metal–metal.
  **Close only when:** ASM-20/P1: record station, boss geometry, post height and connector hand clearance.
- [ ] **J-ELC-003 — PS-04 electronics deck → PS-05 deck post (DIAG-CAD).** **ASSUMPTION / HOLD**
  **First:** J-ELC-001/002 and S0/KO-01 gates. **Hardware/interface:** heat-set M3×5 brass insert + M3 bolt from BOM kit; exact bolt length ASSUMPTION;
  Two front M3 service fasteners into post inserts DOCUMENTED; rear hook count/plane ASSUMPTION. **Do:** Lower PS-04 onto rear hooks, align front post holes, then install the two service screws.
  **Retention:** insert heat-set square to boss; service screw retained by metal thread. **Tool:** temperature-controlled soldering iron + insert tip; matching hex driver after cool-down.
  **Torque/threadlock:** Insert with heat only; never torque while hot. Service screw snug; low-strength threadlock only metal–metal.
  **Close only when:** ASM-20: record hole Ø/pitch, exact bolt lengths, level ±1 mm and <60 s removal.
- [ ] **J-ELC-004 — PS-04 electronics deck → PS-03 UBEC shelf (DIAG-CAD).** **ASSUMPTION / HOLD**
  **First:** J-ELC-003. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Tool-free rear deck hook into PS-03 documented in spec; geometry not production-authorized. **Do:** Engage rear hooks before front screws; lift only after front screws and CN-DECK are removed.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-20: hook engagement/tug test and removal path.
- [ ] **J-CAS-001 — cassette external four-point saddle / clamp · topology TBD → 2023 front floor.** **ASSUMPTION / HOLD**
  **First:** p0_12 full-stack dummy + external four-point clamp coupon. **Hardware/interface:** reversible external four-point retention hardware/topology not selected; no substitute authorized;
  Former X+35/L±12 bosses are REJECTED inside the 55×45 PDB target; no replacement forward stations are registered. **Do:** HOLD the forward saddle. Find reversible external tabs/clamps clear of the PDB, wall boards, floor edge and shell; do not hide screws under modules or drill the donor floor.
  **Retention:** external saddle/clamp retention; exact tabs, screws/inserts and release method remain ASSUMPTION. **Tool:** transparent full-stack dummy + calipers first; installation tool follows the selected closure.
  **Torque/threadlock:** No torque, drilling, bonding or threadlock until CAS-07 selects and records the retention.
  **Close only when:** ASM-20/CAS-04: record both forward attachment stations, clamp pull-off, shell-lip clearance and zero donor damage.
- [ ] **J-CAS-002 — cassette external four-point saddle / clamp · topology TBD → 2023 rear floor.** **ASSUMPTION / HOLD**
  **First:** p0_12 full-stack dummy + ASM-08 steering installation. **Hardware/interface:** reversible external four-point retention hardware/topology not selected; no substitute authorized;
  Former X−15/L±12 bosses are REJECTED inside the 30×25 charge target; nearby M3 rows remain occupied/servo-contested. **Do:** HOLD the rear saddle. Find reversible external tabs/clamps clear of the charge cell, servo and side bodies; no hidden module-first screw or donor hole is authorized.
  **Retention:** external saddle/clamp retention; exact tabs, screws/inserts and release method remain ASSUMPTION. **Tool:** transparent full-stack dummy + calipers first; installation tool follows the selected closure.
  **Torque/threadlock:** No torque, drilling, bonding or threadlock until CAS-07 selects and records the retention.
  **Close only when:** ASM-20/CAS-04: feeler-map the rear carrier against servo/rod, record clamp stations and repeat the unloaded pull-off test.
- [ ] **J-CAS-003 — lift-out electronics cassette stepped-T gauge → cassette external four-point saddle / clamp · topology TBD.** **ASSUMPTION / HOLD**
  **First:** J-CAS-001/002 + S0/KO-01/full-cluster fit gate + new external pattern. **Hardware/interface:** reversible external four-point retention hardware/topology not selected; no substitute authorized;
  Four-point lift-out remains required, but the former X−15/+35/L±12 pattern is rejected by PDB/charge overlap; new pattern and retention are TBD. **Do:** Lower the cassette onto four external datums and engage the selected reversible retention only after its insert/clamp coupon; never remove an electrical module to reach a cassette service joint.
  **Retention:** external saddle/clamp retention; exact tabs, screws/inserts and release method remain ASSUMPTION. **Tool:** transparent full-stack dummy + calipers first; installation tool follows the selected closure.
  **Torque/threadlock:** No torque, drilling, bonding or threadlock until CAS-07 selects and records the retention.
  **Close only when:** ASM-20/CAS-04: record four coordinates, insert/boss dimensions, bolt lengths, rocking, driver reach and body-off removal time.
- [ ] **J-CAS-006 — cassette insulated rear service deck → lift-out electronics cassette stepped-T gauge.** **ASSUMPTION / HOLD**
  **First:** J-CAS-004/005 + J-CAS-018 + ASM-08 measured sweep. **Hardware/interface:** heat-set M3×5 brass insert + M3 bolt from BOM kit; exact bolt length ASSUMPTION;
  Insulated rear service deck Z13…16 carries amp + RP1 above the charge TARGET; 6 mm to KO-01 is 2 mm short of moving policy. **Do:** HOLD the rear service deck. Prove insulation, charge thermal clearance, amp/RP1 exits and measured steering gap before selecting its supports.
  **Retention:** insert heat-set square to boss; service screw retained by metal thread. **Tool:** temperature-controlled soldering iron + insert tip; matching hex driver after cool-down.
  **Torque/threadlock:** Insert with heat only; never torque while hot. Service screw snug; low-strength threadlock only metal–metal.
  **Close only when:** ASM-20/CAS-02: record deck Z, four supports, flatness, lower-module clearance and no rod contact.
- [ ] **J-CAS-015 — hollow cut-through cockpit pedestal → 2023 front floor.** **ASSUMPTION / HOLD**
  **First:** ASM-08 measured steering + D-04 body/halo registration + transparent pedestal template. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Trial pedestal outer core is X+51…+65/L±11 to carry the 14×22 outer conduit gauge; floor feature, hole count and gimbal datum remain TBD. **Do:** HOLD the fixed pedestal floor joint. Use only a physically free/shared feature or reversible clamp; do not drill the donor floor and do not attach it to the cassette.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-20/CAS-08: record foot contacts, existing/shared fastener or clamp, 14×22 core section, 5 mm PDB/5.6 mm front-block gaps, pull-off and zero donor damage.

### ASM-22 joint closure · Electronics trays & RF hardware

- [ ] **J-ELC-005 — dual-core ESP32-WROOM-32 D1-Mini-ESP32 / MH-ET Live MiniKit → PS-04 electronics deck.** **ASSUMPTION / HOLD**
  **First:** Real board calipered + J-ELC-003. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  ESP32 #1 mounting holes may be M2.5/M3 by board variant; supplied BOM has M3 only [ASSUMPTION]. **Do:** Bench-fit ESP32 #1; use BOM M3 only if holes clear without touching pads/traces, otherwise DEFER rather than invent M2.5 hardware.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-22/52: record ESP32 #1 hole Ø/pitch, standoff height, insulation and exact BOM fastener.
- [ ] **J-ELC-006 — dual-core ESP32-WROOM-32 D1-Mini-ESP32 / MH-ET Live MiniKit → PS-04 electronics deck.** **ASSUMPTION / HOLD**
  **First:** Real board calipered + J-ELC-003. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  ESP32 #2 mounting holes may be M2.5/M3 by board variant; supplied BOM has M3 only [ASSUMPTION]. **Do:** Bench-fit ESP32 #2; use BOM M3 only if holes clear without touching pads/traces, otherwise DEFER rather than invent M2.5 hardware.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-22/52: record ESP32 #2 hole Ø/pitch, standoff height, insulation and exact BOM fastener.
- [ ] **J-CAS-004 — power-distribution board · 55×45×18 TARGET → lift-out electronics cassette stepped-T gauge.** **ASSUMPTION / HOLD**
  **First:** final PDB component placement + ASM-08 measured sweep + full connector dummy. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  PDB contents are FIRM; 55×45×18 mm and ~50 g are TARGET/ASSUMPTION; target placement X+1…+46/L±27.5/Z1…19 has only 3 mm to KO-01. **Do:** HOLD the four-M3 lower-bay PDB seat. Refine and caliper the final board, tall UBEC/cap side, holes, loop-key access and every connector/bend before selecting the exact BOM M3 lengths/standoffs.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-22/CAS-05: record PDB L/W/H/mass, holes, live-side insulation, connector exits, creepage lands and service pull.
- [ ] **J-CAS-007 — dual-core ESP32-WROOM-32 D1-Mini-ESP32 / MH-ET Live MiniKit → cassette left interior mini-board wall seat.** **ASSUMPTION / HOLD**
  **First:** real MH-ET Live board calipers + S0≥9.82 + p0_12 fit gate. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Mini board #1 control identity/envelope is FIRM at 39 X ×31 Z ×~13 L at L−43…−30; holes, headers, retention and live micro-USB plug bends are unmeasured. **Do:** HOLD mini-board #1 control wall retention; orient the micro-USB end toward X+42 and do not force M3 through an unverified PCB hole.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-22/CAS-03: record mini-board #1 control SKU/chip, body/headers/live USB plug, holes, wall gap, insulation and body-off hand clearance.
- [ ] **J-CAS-008 — dual-core ESP32-WROOM-32 D1-Mini-ESP32 / MH-ET Live MiniKit → cassette right interior mini-board wall seat.** **ASSUMPTION / HOLD**
  **First:** real MH-ET Live board calipers + S0≥9.82 + p0_12 fit gate. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Mini board #2 sound/light identity/envelope is FIRM at 39 X ×31 Z ×~13 L at L+30…+43; holes, headers, retention and live micro-USB plug bends are unmeasured. **Do:** HOLD mini-board #2 sound/light wall retention; orient the micro-USB end toward X+42 and do not force M3 through an unverified PCB hole.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-22/CAS-03: record mini-board #2 sound/light SKU/chip, body/headers/live USB plug, holes, wall gap, insulation and body-off hand clearance.
- [ ] **J-CAS-018 — MAX98357A amplifier → cassette insulated rear service deck.** **ASSUMPTION / HOLD**
  **First:** J-CAS-005/006 + real amp calipers + ASM-08 measured sweep. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  MAX98357A uses a 17.8 X ×19.4 L ×3 reference body on the insulated Z13…16 rear service deck; purchased-board holes/exits are ASSUMPTION. **Do:** HOLD the amp seat; support and insulate the PCB, leave I2S XH5/speaker exits accessible and prove the deck stays clear of the charge thermal face and steering.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-22/55/CAS-05: record amp L/W/H, holes, insulation, XH5/PH2 exits, charge gap and measured moving clearance.
- [ ] **J-AUD-001 — MAX98357A amplifier → PS-04 electronics deck.** **ASSUMPTION / HOLD**
  **First:** Real amp measured + J-ELC-003. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  MAX98357A reference 19.4×17.8×3 ASSUMPTION for purchased board; two-screw pad unspecified. **Do:** Bench-fit amp; use BOM M3 only if board holes clear pads/traces and the deck pad supports the PCB.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-22/55: record board/hole pitch, standoff/insulation and fastener.

### ASM-23 joint closure · Electronics trays & RF hardware

- [ ] **J-ELC-007 — RadioMaster RP1 → PS-06 RX carrier.** **ASSUMPTION / HOLD**
  **First:** Real RP1 measured. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  RP1 body/pad retention documented as carrier+adhesive option; board holes/fastener absent from supplied BOM. **Do:** Seat RP1 on PS-06 without loading antenna/coax; do not run an M3 screw through the board unless a measured mounting hole exists.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-23/52: record body/hole geometry and carrier tug test.
- [ ] **J-CAS-009 — RadioMaster RP1 → cassette insulated rear service deck.** **ASSUMPTION / HOLD**
  **First:** J-CAS-006 + firm connector map + full body/bend dummy. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  RP1 body is DOCUMENTED 13×11×3; cassette pad, antenna root and lead exit are unmeasured. **Do:** HOLD the RP1 seat; restrain the body/pad and cable jacket without clamping the antenna root.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-23/CAS-05: record pad size, pull direction, antenna service loop and separation from WiFi/XT seats.

### ASM-24 joint closure · Hall speed sensor

- [ ] **J-SNS-001 — Ø3×1 magnet → belt-set output shaft.** **ASSUMPTION / DEFER**
  **First:** Magnets arrive + final rear carrier/shaft assembled. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Magnet Ø3×1 DOCUMENTED; final shaft carrier, keyed recess/bond land and runout UNKNOWN. **Do:** DEFER magnet bond; select a radial station with no belt/bearing conflict and key/bond only after dry-run gap proof.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-57: record shaft land, keyed feature/bond, runout and retention after hand spin.
- [ ] **J-SNS-002 — A3144 Hall sensor → PS-16 Hall bracket.** **ASSUMPTION / DEFER**
  **First:** J-SNS-001 + PS-16 authorized. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  A3144 body max 4.17×3.10×1.57 DOCUMENTED; clip/fastener and sensitive face orientation physical. **Do:** DEFER sensor retention; place the active face toward the magnet and strain-relieve leads outside the 1–3 mm adjustment.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-57: identify active face, clip/fastener, lead strain relief and repeatable 1.5 mm cold setting.
- [ ] **J-SNS-003 — PS-16 Hall bracket → rear axle carrier L.** **ASSUMPTION / DEFER**
  **First:** J-SNS-001/002 + final rear carrier. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  PS-16 clips to selected bearing-carrier region; mount geometry depends on Gate A and magnet station. **Do:** DEFER bracket joint; use a reversible M3/shared feature only after full axle play is known.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-57: record carrier feature, exact BOM fastener, adjustment range and ≥8 mm belt/gear clearance.

### ASM-25 joint closure · Electronics trays & RF hardware

- [ ] **J-ELC-009 — BL-M8812EU2 WiFi module → PS-04 electronics deck.** **ASSUMPTION / HOLD**
  **First:** Possession + D-06b. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  WiFi max pocket 60×32×12 is diagnostic ASSUMPTION; real module possession/dimensions unconfirmed. **Do:** Use PS-13 dummy only until the real WiFi module is measured; then seat with U.FL exits unloaded and service pull open.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-25/52: record module envelope, pocket retention and removal path.
- [ ] **J-ELC-010 — 28×28×3 heatsink → BL-M8812EU2 WiFi module.** **ASSUMPTION / HOLD**
  **First:** D-06b + thermal material selected. **Hardware/interface:** no connector fastener in the supplied joint BOM; bond/adhesive remains ASSUMPTION unless BOM v2 names it;
  28×28×3 heatsink DOCUMENTED; WiFi thermal face, bond line and keepouts unmeasured. **Do:** Dry-align heatsink to the identified hot package/plane, preserve U.FL/USB access, then make the documented thermal bond.
  **Retention:** bonded retention after dry fit; no hidden substitute hardware. **Tool:** surface-prep tools + clamp appropriate to the selected, documented adhesive.
  **Torque/threadlock:** No torque/threadlock. Do not bond until the named ASM dry-fit and service check pass.
  **Close only when:** ASM-25: record thermal face, bond material/thickness, cure and pull test.
- [ ] **J-CAS-010 — BL-M8812EU2 WiFi module → cassette insulated rear service deck.** **ASSUMPTION / HOLD**
  **First:** Real BL-M8812EU2 calipers + full PDB/charge/amp/RP1/dock dummy. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  WiFi allocation remains ≤60×32×12 with 28×28×3 heatsink, but the target-cell repack has no accepted WiFi station. **Do:** HOLD the WiFi seat as UNPLACED; find a shell/KO-safe vented station with USB, both U.FL service directions and ≥10 mm coax bends unobstructed.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-25/CAS-05: record complete module/heatsink envelope, vent free area, cable bends, retention and body-on temperature.

### ASM-26 joint closure · Camera pod, gimbal & blower

- [ ] **J-CAM-001 — PS-10 gimbal base → 2023 front floor.** **ASSUMPTION / HOLD**
  **First:** Gate C and A-vs-B choice. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  PS-10 common station envelope documented; actual base holes/station blocked by D-34/35. **Do:** HOLD chassis-side gimbal base; when authorized, use only existing mapped M3 features/shared stack.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-26/53: record station, hole Ø/count, bolt lengths and roll datum.
- [ ] **J-CAM-002 — MG90S pan servo → PS-10 gimbal base.** **ASSUMPTION / DEFER**
  **First:** MG90S arrival + J-CAM-001. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  MG90S clone body/ears/pitch/spline unmeasured. **Do:** DEFER pan-servo mount; no nominal-clone pocket edits before calipers/no-force fit.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-54: record pan servo body/ears/hole Ø/pitch and exact BOM-compatible fastener.
- [ ] **J-CAM-003 — MG90S tilt servo → MG90S pan servo.** **ASSUMPTION / DEFER**
  **First:** Both MG90S arrived/centred. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Orthogonal MG90S gimbal interface, horn and link geometry UNKNOWN. **Do:** DEFER tilt-to-pan connection; use only measured servo horns/screws and prove hand sweep before power.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-54: record axes, horn radius/hole Ø, retention and hard-stop clearance.
- [ ] **J-CAM-004 — SSC338Q + IMX335 camera → MG90S tilt servo.** **ASSUMPTION / DEFER**
  **First:** D-34 camera measurements + J-CAM-003. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Camera board/heatsink/lens holes and cradle interface D-34 UNKNOWN. **Do:** HOLD/DEFER camera cradle until the real board, lens and cable exits are measured; clamp no lens barrel.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-53: record camera holes, safe clamp lands, roll reference and service pull.
- [ ] **J-CAS-011 — PS-10 gimbal base → hollow cut-through cockpit pedestal.** **ASSUMPTION / DEFER**
  **First:** J-CAS-015 + D-34/35 + real MG90S units + p0_12 pedestal/halo gate. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  PS-10 gimbal-to-pedestal face, holes, gimbal datum and swept envelope are unmeasured; both MG90S units remain in transit. **Do:** DEFER the gimbal-to-pedestal joint; the gimbal is never supported by the cassette, and no nominal MG90S pocket or horn interface is authorized.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-26/CAS-08: record pedestal face, hardware, roll datum, FOV, halo/airbox gap, full no-power sweep and independent cassette lift.

### ASM-27 joint closure · Lighting segments & lenses

- [ ] **J-LGT-001 — WS2812B segment → rearbacklightdiffuser.** **ASSUMPTION / HOLD**
  **First:** ASM-13 H-08 pre-route and actual strip offcut. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  WS2812 strip and diffuser location DOCUMENTED; strip thickness/adhesive/channel fit D-36 UNKNOWN. **Do:** Seat the brake segment behind the unpainted lens without covering pads; provide pull-through strain relief.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-55: record pixel count/segment length, channel fit, retention and optical test.
- [ ] **J-LGT-003 — WS2812B segment → PS-18 light anchor / lens.** **ASSUMPTION / HOLD**
  **First:** Actual strip offcut + PS-18 authorized. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Left Indicator segment/lens anchor is new concept; segment cut and retention D-36 UNKNOWN. **Do:** HOLD left indicator segment in its unpainted lens/anchor without loading solder pads.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-55: record left indicator pixel count, cut line, anchor retention and shell/DRS clearance.
- [ ] **J-LGT-004 — WS2812B segment → PS-18 light anchor / lens.** **ASSUMPTION / HOLD**
  **First:** Actual strip offcut + PS-18 authorized. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Right Indicator segment/lens anchor is new concept; segment cut and retention D-36 UNKNOWN. **Do:** HOLD right indicator segment in its unpainted lens/anchor without loading solder pads.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-55: record right indicator pixel count, cut line, anchor retention and shell/DRS clearance.
- [ ] **J-LGT-005 — WS2812B segment → new halo 2.1.** **ASSUMPTION / HOLD**
  **First:** Actual strip + halo dry fit. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Halo strip location DOCUMENTED; 2+2 pixel proposal/anchor/adhesive D-36 ASSUMPTION. **Do:** Dry-route halo segments on the underside/declared optical land; keep data direction and body disconnect lead serviceable.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-55: record pixel layout, cut points, retention and light bleed.

### ASM-28 joint closure · Rear suspension & drivetrain

- [ ] **J-REA-030 — MG90S DRS servo → preferred 2021 DRS rear wing.** **ASSUMPTION / DEFER**
  **First:** MG90S arrival + Gate A/B wing selection. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  MG90S wing pocket DOCUMENTED topology; clone body/ears/hole pitch unmeasured. **Do:** DEFER servo-to-pocket mount; do not resize the wing pocket from nominal clone dimensions.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-54: measure MG90S body/ears/hole pitch and select BOM M3 hardware only if holes permit.
- [ ] **J-REA-031 — MG90S DRS servo → 25T metal horn.** **ASSUMPTION / DEFER**
  **First:** MG90S arrival and centring. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  MG90S spline/horn/horn screw unmeasured; 25T DS3235SG horn is NOT transferable. **Do:** DEFER horn fit; use only the horn and horn screw supplied/verified for the MG90S clone.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-54: identify spline, horn holes/radii and retaining screw.
- [ ] **J-REA-032 — 25T metal horn → DRS Arm for 2021 wing.** **ASSUMPTION / DEFER**
  **First:** J-REA-030/031 and real MG90S. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Drawing [2] documents metal-rod linkage; rod diameter, ends and horn/arm holes are UNKNOWN and not in supplied joint BOM. **Do:** DEFER DRS link hardware; do not repurpose steering M4 rod or M3 ball studs without a measured match.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-54: measure horn/arm hole Ø, centre distance and specify only BOM-compatible hardware or leave open.
- [ ] **J-REA-033 — DRS Arm for 2021 wing → preferred 2021 DRS rear wing.** **ASSUMPTION / DEFER**
  **First:** Gate B and J-REA-032. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  DRS arm/flap pivot exists in mesh/drawing; pin/retention specification UNKNOWN. **Do:** DEFER arm-to-flap/pivot closure until the wing dry assembly identifies the actual pin and retention.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-54: record pivot Ø, hardware, end retention and free flap travel.

### ASM-29 joint closure · Camera pod, gimbal & blower

- [ ] **J-CAM-005 — 5 V blower → PS-11 blower/duct interface.** **ASSUMPTION / HOLD**
  **First:** Real blower measured + PS-11 authorized. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Blower face/depth/outlet/hole pattern are D-34 UNKNOWN. **Do:** HOLD blower mount; orient outlet toward duct and leave inlet fully open.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-53: record blower holes, fastener/clip, inlet plane and vibration isolation.
- [ ] **J-CAM-006 — camera blower duct → 5 V blower.** **ASSUMPTION / HOLD**
  **First:** J-CAM-005 + measured duct render. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Nine SCAD inputs, collar and blower outlet are UNKNOWN until D-34. **Do:** HOLD duct collar; it must demate for camera service without prying on blower housing.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-53: record outlet/collar dimensions, retention and air-leak check.
- [ ] **J-CAM-007 — camera blower duct → SSC338Q + IMX335 camera.** **ASSUMPTION / HOLD**
  **First:** J-CAM-004/006. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Duct mouth/camera thermal face and stand-off are UNKNOWN. **Do:** HOLD duct-to-camera interface; preserve lens/FOV and avoid contact with components not identified as thermal surfaces.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-53: airflow proof, lens clearance, temperature and independent removal.

### ASM-30 joint closure · Electronics trays & RF hardware

- [ ] **J-ELC-011 — PS-12 antenna post → PS-04 electronics deck.** **ASSUMPTION / HOLD**
  **First:** D-33 route + D-20 separation. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Left PS-12 post is intended integral-to-deck or standalone; exact joint path ASSUMPTION. **Do:** If not integral, fasten the left post to PS-04/standalone foot with a measured BOM M3 stack; never shell-mount it.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-30/52: record left post joint, bolt length and body-cycle stability.
- [ ] **J-ELC-012 — PS-12 antenna post → PS-04 electronics deck.** **ASSUMPTION / HOLD**
  **First:** D-33 route + D-20 separation. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Right PS-12 post is intended integral-to-deck or standalone; exact joint path ASSUMPTION. **Do:** If not integral, fasten the right post to PS-04/standalone foot with a measured BOM M3 stack; never shell-mount it.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-30/52: record right post joint, bolt length and body-cycle stability.
- [ ] **J-ELC-013 — 5.8 GHz U.FL whip → PS-12 antenna post.** **ASSUMPTION / HOLD**
  **First:** J-ELC-011; antenna attached to module before power. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Left 70 mm whip DOCUMENTED; post tie/clip geometry and coax strain relief ASSUMPTION. **Do:** Seat the left whip on the post in the shallow V; restrain the cable jacket, never the U.FL plug.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-30/52: jacket tug test, ≥10 mm bend and body-off cycle proof.
- [ ] **J-ELC-014 — 5.8 GHz U.FL whip → PS-12 antenna post.** **ASSUMPTION / HOLD**
  **First:** J-ELC-012; antenna attached to module before power. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Right 70 mm whip DOCUMENTED; post tie/clip geometry and coax strain relief ASSUMPTION. **Do:** Seat the right whip on the post in the shallow V; restrain the cable jacket, never the U.FL plug.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-30/52: jacket tug test, ≥10 mm bend and body-off cycle proof.

### ASM-31 joint closure · Electronics trays & RF hardware

- [ ] **J-ELC-015 — PS-08 cable comb → 2023 front floor.** **ASSUMPTION / HOLD**
  **First:** All harnesses routed and motion sweep available. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  PS-08 push-fit + optional M3 documented; exact floor stations and comb geometry depend on D-10/D-27. **Do:** Clip/bolt each comb only at a mapped donor/shared feature; load cable jackets, not solder joints.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-31: record every comb station/fastener and full-motion tug test.
- [ ] **J-CAS-012 — cassette XT60 / XT30 power-seat bank → lift-out electronics cassette stepped-T gauge.** **ASSUMPTION / HOLD**
  **First:** selected terminated XT60/XT30 calipers + D-10 full harness/dock dummy. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Firm dock minimum is 1×XT60 pack inlet + 2×XT30 Rail-A/B branches; target allocations XT60 20×20×12 and XT30 16×16×10 are ASSUMPTION. **Do:** HOLD the ~60 mm power bank; recess the potentially live/source half as shrouded/socket, separate it visibly from signal and load jackets rather than PDB solder joints.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-31/CAS-07: record connector SKU/polarity, seat outline, mating hand, bend radius, extraction force and strain relief.
- [ ] **J-CAS-013 — cassette 5× 3-pin servo-seat bank → lift-out electronics cassette stepped-T gauge.** **ASSUMPTION / HOLD**
  **First:** selected positive-lock 3-pin housing calipers + D-10 servo-lead dress. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Firm bank count is 5×3-pin: steering, ESC signal (+5 removed), DRS, pan and tilt; 16 mate-depth ×10 pitch ×8 high each is ASSUMPTION. **Do:** HOLD the ~58 mm servo bank; positively retain and label all five positions, witness the ESC missing +5 contact and preserve body-off finger release.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-31/CAS-07: record count, pin order, clip retention, finger clearance and full-motion tug test.
- [ ] **J-CAS-014 — cassette JST-XH / shielded-USB4 signal-seat bank → lift-out electronics cassette stepped-T gauge.** **ASSUMPTION / HOLD**
  **First:** selected terminated XH3/4/5, USB4 and U.FL calipers + D-10 full chassis umbilical. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Firm external signal bank is 3×JST-XH 3-pin (balance/LED/Hall) + 1×shielded USB4; internal bodies include XH4 CRSF, XH3 link2, XH5 I2S and 2×U.FL; all body allocations ASSUMPTION. **Do:** HOLD the ~64 mm external signal bank and internal seats; key/label every mate, separate them from XT power, reserve U.FL bend relief and anchor jackets before first bends.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-31/CAS-07: record pin map, seat spacing, plug extraction, bundle OD, first anchor and ten body-off mate cycles.
- [ ] **J-CAS-016 — pedestal shielded-USB4 / 2×3-pin conduit · 10×18 clear TARGET → hollow cut-through cockpit pedestal.** **ASSUMPTION / DEFER**
  **First:** J-CAS-015 + terminated USB4/two servo plugs + real MG90S leads + 2 mm-wall coupon. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Firm bundle is shielded USB4 + 2×3-pin servo; target clear section 10×18 with 2 mm trial wall gives 14×22 outer, ≥25 mm lower slack and ≥20 mm provisional USB bend. **Do:** DEFER the conduit interface; pull full connectors sequentially without removing terminals, then prove slack, bend and jacket anchor before the R1/R2 turn.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-31/CAS-09: record clear section, wall, plug pull-through, bend radius, strain relief, steering gap and cassette-lift clearance.
- [ ] **J-CAS-017 — ganged cassette umbilical dock → lift-out electronics cassette stepped-T gauge.** **ASSUMPTION / HOLD**
  **First:** J-CAS-012/013/014/016 + selected body calipers + D-10 full harness dummy. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Map/count is firm, but the straight X+42…+58/L±32 body projection overlaps pedestal X+51…+65/L±11; stepped/wrapped topology, auxiliary 2-pin seats and mating pull remain ASSUMPTION. **Do:** HOLD the dock-to-cassette joint; reject the straight face, prove a notched/wrapped body-off-accessible frame, recess live power, separate families and turn the chassis loom into R1/R2.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-31/CAS-10: record dock station, seat spacing, latch access, mating force, jacket anchor, ten cycles and parked chassis-half retention.

### ASM-33 joint closure · Body, shell & aero fasteners

- [ ] **J-BDY-002 — NEW BODY 2024 FRONT → NEW BODY 2024 REAR.** **ASSUMPTION / HOLD**
  **First:** Paint cured; internal modules tested. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Clamshell panel joint DOCUMENTED; 2023 drawing's 12×M3 count does not verify 2024 panel count. **Do:** Join front and rear shell panels at their matching lands; start every present M3 feature before snugging.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-33: count/measure 2024 panel holes, record exact BOM lengths and nut/insert/self-thread retention.
- [ ] **J-BDY-003 — NEW BODY 2024 FRONT → 2023 front floor.** **DOCUMENTED / READY**
  **First:** J-BDY-002 + shell landing check. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  2024 README documents two M3 screws front-floor→front body; holes intentionally tight/self-threading. **Do:** Lower shell without dragging harnesses, start both floor-to-body M3 screws by hand, and snug once.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-33: record hole Ø, chosen bolt lengths and insert vs self-thread decision.
- [ ] **J-BDY-004 — FRONTNOSE2024 → 2023 front floor.** **DOCUMENTED / READY**
  **First:** J-BDY-003. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  2024 README documents one M3 nose→front-floor screw; hole intentionally tight/self-threading. **Do:** Seat nose on its landing, hand-start the single M3 from nose to floor and stop as soon as the shell is retained.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-33: record hole Ø, bolt length and insert vs self-thread decision.
- [ ] **J-BDY-005 — 2024 revised front wing → FRONTNOSE2024.** **ASSUMPTION / HOLD**
  **First:** J-BDY-004. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Separate revised front wing/nose installation DOCUMENTED; exact 2024 hole count/Ø/bolt length unverified. **Do:** Offer wing to nose/front-floor interface without flexing; start all matching M3 fasteners before snugging.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-33: count/measure holes, record bolt lengths/retention and sacrificial service behavior.
- [ ] **J-LGT-006 — new halo 2.1 → NEW BODY 2024 FRONT.** **ASSUMPTION / HOLD**
  **First:** J-LGT-005 and painted shell cured. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Halo and front-shell meshes VERIFIED; attachment features/hardware unmeasured. **Do:** Dry-seat halo on the front body; use BOM M3 only where matching features exist, otherwise await an approved bond method.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-33/55: record holes/contact lands, retention and body-off harness path.
- [ ] **J-CAM-008 — camera top 1.1 pod → NEW BODY 2024 REAR.** **ASSUMPTION / HOLD**
  **First:** Body shell dry-assembled; camera Option B only if selected. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Camera-top STL silhouette VERIFIED; attachment feature/hardware to 2024 rear shell unmeasured. **Do:** Dry-seat camera top on its authored shell station; use BOM M3 only if matching features are physically present—otherwise leave joint open.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-33/53: measure holes/contact land and record screw/nut/insert or approved bond.
- [ ] **J-BDY-006 — 2024 mirror → NEW BODY 2024 FRONT.** **ASSUMPTION / HOLD**
  **First:** Paint cured; mirror orientation confirmed. **Hardware/interface:** no connector fastener in the supplied joint BOM; bond/adhesive remains ASSUMPTION unless BOM v2 names it;
  Left mirror mesh exists; shell landing and fastener/bond are unmeasured. **Do:** Dry-seat the left mirror; do not drill the shell or choose adhesive until contact area and service intent are recorded.
  **Retention:** bonded retention after dry fit; no hidden substitute hardware. **Tool:** surface-prep tools + clamp appropriate to the selected, documented adhesive.
  **Torque/threadlock:** No torque/threadlock. Do not bond until the named ASM dry-fit and service check pass.
  **Close only when:** ASM-33: photograph left landing, measure contact/holes and record approved retention.
- [ ] **J-BDY-007 — 2024 mirror → NEW BODY 2024 FRONT.** **ASSUMPTION / HOLD**
  **First:** Paint cured; mirror orientation confirmed. **Hardware/interface:** no connector fastener in the supplied joint BOM; bond/adhesive remains ASSUMPTION unless BOM v2 names it;
  Right mirror mesh exists; shell landing and fastener/bond are unmeasured. **Do:** Dry-seat the right mirror; do not drill the shell or choose adhesive until contact area and service intent are recorded.
  **Retention:** bonded retention after dry fit; no hidden substitute hardware. **Tool:** surface-prep tools + clamp appropriate to the selected, documented adhesive.
  **Torque/threadlock:** No torque/threadlock. Do not bond until the named ASM dry-fit and service check pass.
  **Close only when:** ASM-33: photograph right landing, measure contact/holes and record approved retention.
- [ ] **J-BDY-008 — NEW BODY 2024 FRONT → 2023 front floor.** **ASSUMPTION / HOLD**
  **First:** All internal harnesses dressed. **Hardware/interface:** no fastener; designed shell/floor landing contact;
  Shell landing points derive from registered meshes; exact physical contact and S0 remain P1. **Do:** Lower shell vertically and verify every intended landing contacts without resting on electronics or steering.
  **Retention:** gravity/contact landing with nearby registered fasteners carrying retention. **Tool:** feeler gauges + inspection light.
  **Torque/threadlock:** No torque/threadlock at the landing itself; do not shim unless a later decision authorizes it.
  **Close only when:** ASM-33/P1: feeler-map landing points, S0 and any unintended contact; no shim/relief by implication.
- [ ] **J-BDY-009 — NEW BODY 2024 REAR → 2023 rear floor.** **ASSUMPTION / HOLD**
  **First:** Rear stack and H-08 closed. **Hardware/interface:** no fastener; designed shell/floor landing contact;
  Rear shell landing is mesh-derived but physical stack/wing/harness state remains open. **Do:** Seat rear shell onto donor landing points while watching tail harness, shock and antenna routes.
  **Retention:** gravity/contact landing with nearby registered fasteners carrying retention. **Tool:** feeler gauges + inspection light.
  **Torque/threadlock:** No torque/threadlock at the landing itself; do not shim unless a later decision authorizes it.
  **Close only when:** ASM-33: feeler-map rear landings and prove no harness or moving part carries shell load.

### ASM-55 joint closure · Audio assembly

- [ ] **J-AUD-002 — 4 Ω 3 W speaker → PS-14 speaker carrier.** **ASSUMPTION / HOLD**
  **First:** D-36 real speaker measurements. **Hardware/interface:** no added BOM fastener; printed clip/pocket/strap feature only;
  Speaker basket/hole/cone/port all D-36 UNKNOWN; compliant ring concept only. **Do:** HOLD speaker-to-carrier joint; support basket rim only, never cone/surround, and keep ≥3 mm port/cone clearance.
  **Retention:** clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION. **Tool:** hands + calipers; trim tool only after a recorded fit check.
  **Torque/threadlock:** No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.
  **Close only when:** ASM-55: record basket holes/rim, isolation, retention and cone/port clearance.
- [ ] **J-AUD-003 — PS-14 speaker carrier → 2023 front floor.** **ASSUMPTION / HOLD**
  **First:** J-AUD-002 + D-03/DN-07. **Hardware/interface:** M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION;
  Left sidepod/fallback station documented; PS-14 floor/body interface un designed. **Do:** HOLD carrier mount; use mapped existing M3/shared stack only and preserve body removal.
  **Retention:** screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one. **Tool:** matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head.
  **Torque/threadlock:** Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.
  **Close only when:** ASM-55: record station, floor feature, bolt length, port direction and shell clearance.

### ASM-59 joint closure · Battery, power & onboard charging

- [ ] **J-CHG-001 — USB-C 2S balancing charge module · 30×25×10 TARGET · SKU TBD → parametric charge-module pocket.** **ASSUMPTION / DEFER**
  **First:** Owner selects compliant 5 V-input 2S balancing-charge module with safety evidence. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  30×25×10 mm is the supplied TARGET envelope; module SKU, final dimensions, hole pattern, thermal face and connector exits remain TBD. **Do:** DEFER module mount; after selection, caliper every body/hole/connector against the TARGET and generate a parametric pocket—no photo-derived dimensions.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-59/OP-49: record SKU/datasheet, mass, envelope, hole Ø/pitch, cell ports and thermal faces.
- [ ] **J-CHG-002 — parametric charge-module pocket → 2023 rear floor.** **ASSUMPTION / DEFER**
  **First:** J-CHG-001 measured + P1 full cluster. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Pocket station/feet/fastener count UNKNOWN until full inside-shell cluster fit. **Do:** DEFER pocket-to-floor joint; prefer mapped shared M3 stack or reversible clamp and never add donor holes.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-59/P1: record station, M3 feature, exact BOM bolt length and shell/service clearance.
- [ ] **J-CHG-003 — hidden USB-C charge port → NEW BODY 2024 REAR.** **ASSUMPTION / DEFER**
  **First:** Selected charge module/receptacle measured. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Existing opening/reversible hidden insert required; receptacle geometry and panel thickness UNKNOWN. **Do:** DEFER port mount; use an existing opening or reversible insert, with no shell drilling or guessed clip geometry.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-59/OP-49: identify opening, panel thickness, receptacle flange/hole pattern, plug insertion force and weather/strain relief.
- [ ] **J-CHG-004 — charge/run interlock → PS-15 junction support (DIAG-CAD).** **ASSUMPTION / DEFER**
  **First:** Electrical safety architecture separately authorized. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Charge/run interlock type, body, terminals and mounting thread UNKNOWN. **Do:** DEFER interlock mount; provide mechanical keying so charge and run states cannot be selected together, without inferring circuit topology.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-59/OP-49: record switch/interlock SKU, mounting feature, positive detent and finger access.
- [ ] **J-CAS-005 — USB-C 2S balancing charge module · 30×25×10 TARGET · SKU TBD → lift-out electronics cassette stepped-T gauge.** **ASSUMPTION / DEFER**
  **First:** OP-49 + J-CHG-001 and full cassette fit gate. **Hardware/interface:** hardware not selected / still in transit; no substitute authorized;
  Charge module uses a 30×25×10 TARGET cell at X−31…−1/L−13…+12/Z1…11; SKU, holes, exits, thermal face and electrical authorization remain open. **Do:** DEFER the charge-module seat. Select and caliper the actual 5 V USB-C to 2S balancing SKU; do not treat the target cell as a pocket or infer a circuit.
  **Retention:** DEFER — retention cannot be chosen before the named real part is measured. **Tool:** calipers first; installation tool is selected only after hardware identity closes.
  **Torque/threadlock:** No torque, bonding, drilling or threadlock while DEFERRED.
  **Close only when:** ASM-59/CAS-05: record selected module dimensions/mass/thermal face and prove isolated charge/run access.

### ASM-60 · Connection closure audit

Prereq: all applicable ASM steps complete. Sort the CSV by `disposition`,
confirm every installed joint is recorded READY with its physical check, and
confirm every HOLD/DEFER row is still visibly open—never silently treated as
installed. Re-run `p0_11_validate_connection_outputs.py`; archive the signed
CSV/filter result with the ASM session note.

<!-- END GENERATED JOINT BUILD SEQUENCE · p0_10 -->
