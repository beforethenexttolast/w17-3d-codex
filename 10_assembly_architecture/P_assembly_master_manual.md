# P · Assembly Master Manual (dependency-aware)

Session 2 · 2026-07-18. Steps ASM-01…ASM-48. Format per step: **Purpose · Prereq ·
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
  Needs: DS3235SG, `Servoholder`. CN-08. Do: servo into holder per drawing `[2]`,
  lead exits aft-right to X1, snug. ⚠ do not attach horn yet. Evidence: photo. 📷 yes.
- **ASM-07 Servo power-up + firmware centring.** Purpose: centre **before** linkage
  (A §3 dependency). Prereq: ASM-06; bench Rail B source (current-limited). Do: power
  via CN-08 from bench, command centre from firmware, fit horn at centre, final-tighten
  horn screw. Test → pass: horn repeats centre ±1° after power cycle. STOP: servo
  doesn't fit holder or won't centre → Gate D residual reopens. Evidence: ASM note.
- **ASM-08 Steering linkage closure.** Prereq: ASM-07. Needs: rod, tie rods,
  turnbuckles, ball studs. Do: link horn → servo-saver per drawing `[3]`; equal-length
  links; toe ≈ 0. **Record the real rod line height + sweep → closes D-26.** Test:
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
