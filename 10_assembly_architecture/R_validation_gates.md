# R · Validation Gates P0–P10

Session 2 · 2026-07-18. These gates sequence the *architecture* build. They do **not**
replace, reopen, or close the pre-existing gates (Gate A, Gate B, Gate C, D-09, D-18 —
RST-07); where a P-gate needs one of those, it lists it as a prerequisite. Fail
responses name the redesign path — a failed gate is a loop, not a dead end.

| Gate | Prerequisites | Procedure | Pass | Fail | Evidence | Unlocks | Redesign response |
|---|---|---|---|---|---|---|---|
| **P0 Required measurements** | slicer + calipers available | run D-01 (floor↔shell datum, bay length), D-02 (net spine volume), D-04 (roof clearance method ready), D-25 (nose sections), **D-26 (rod line)**, **D-27 (slot map)**, D-06 (camera calipers); D-03 sidepods | every P0 measurement has a number ± stated accuracy in Report D | any unmeasurable → escalate method (print a gauge, dry-fit earlier) | updated `D_measurement_plan.md` rows | real values for P1…P3; battery purchase path (D-01) | if D-01/D-02 contradict H.1 ranges → re-run H.3 scoring with real numbers (fallback A trigger) |
| **P1 Dummy-envelope dry-fit** | P0; PS-13 dummy set TP-printed | place all dummies (battery, ESC, ESP32 ×2, UBEC ×2, servo/KO-19 stand-in, **WiFi P9 dummy**) on the bare floor per J; sweep steering/suspension mocks | all dummies fit with I.1 clearance policy; KO sweeps clear | any overlap → record which | photos + marked floor | diagnostic **printing** (P2) of PS-01…PS-06/PS-15; their parametric CAD modelling may already begin at P0 (T order — S3 harmonization) | move the offending allocation per J's alt-zone column; if Z3R fails wholesale → fallback A |
| **P2 Diagnostic support print** | P1; T specs frozen for the affected parts | TP-print minimum geometry: PS-01, PS-02, PS-03+PS-05, PS-04 blank, PS-15 shell, PS-08 samples | each TP part seats on the real floor; dummies seat in them | print/fit error | TP entries in `04_test_prints/` | P3 | parametric dims adjusted, reprint (cheap by design) |
| **P3 Mechanical dry assembly** | P2; mechanicals through ASM-12 state (needs **Gate A** for the rear) | ASM-05…14 with TP supports + dummies; full motion sweeps; body trial-lower (KO-14) | insertion, motion, removal, tool access all demonstrated | any clash/inaccessible fastener | ASM notes + photos | P4; freezes support geometry for production CAD candidates | geometry rev of the clashing part; re-run P2 for it |
| **P4 Electrical bench integration** | components on hand (per row); **D-09** for servos | outside the chassis: rails from bench supply, each subsystem smoke-tested per ASM-19/21/22 patterns; **(S3) plus: camera→WiFi USB link integrity through CN-16 (DN-11), ESC signal-loss = motor-stop behaviour (fuse-blow safety basis, L.3.1), dev-board USB-isolation check (back-power rule, O.4)** | every subsystem runs on its intended rail; voltages in spec | any brown-out/fault | measurement notes | P5 | topology fix (L.2 alternatives) before anything is installed |
| **P5 Lower-layer integration** | P3+P4 | ASM-14…19 in the chassis; lower harness live on bench power | lower layer fully functional **before** the deck goes on | fault under deck footprint | ASM-19 note | P6 | fix now — this gate exists so faults are found with full access |
| **P6 Full dry assembly** | P5 | ASM-20…31 with provisional (uncut) harnesses; **WiFi dummy allowed (RST-06)** | all modules in, all motion sweeps clean, deck drill <60 s | congestion/loop failures | photos, timed drills | P7 | re-dress or re-route per N; comb additions |
| **P7 Rail-current validation (D-24)** | P6; battery on hand; **real VID-WIFI installed (possession + D-06b, RST-06) — a dummy-module run is a *partial* D-24 and cannot unlock Gate P9 Rail A sizing (S3)** | ASM-34…36: polarity, current-limited power-up, ammeter at CN-23 through worst-case states **+ accessory-branch input current at PS-15 (the DN-01 fuse rates on the input side — S3)** | peaks + sustained recorded; both rails ≤100% transient / ≤80% sustained **or** a decided mitigation (DN-04 cap, upsize) | over budget with no mitigation | D-24 table | **DN-01 rating, DN-04 value, Gate P9 sizing**; closes E-23 | LED cap / load stagger / UBEC upsize (PS-03 parametric), re-measure |
| **P8 Thermal + RF validation** | P7; **real WiFi module** (possession + D-06b) for the RF half **and for the WiFi-related D-19 thermal points — it is the top deck heat source; a dummy cannot pass them (S3)** | ASM-41 (D-20) + ASM-43 (D-19) body-on | O.1 temp limits; stable LQ at range; paint A/B check done | overheat / link degradation | D-19/D-20 tables | P9; closes KO-16/KO-17 validations | vent path fix (DN-10), antenna reposition (PS-12 alt), duct rev |
| **P9 Final harness authorization** | P7+P8 | cut harnesses to measured lengths, final gauges/ratings per D-24, labels per M.3, restraint per ASM-31 | M.2 matrix updated from PROVISIONAL to final; ASM-31 inspection passes | — | updated M | P10 | — |
| **P10 Production CAD + print authorization** | P0…P9; **Gate C** for camera parts; DN register decided/deferred explicitly; ASM-47 drills passed | ASM-48 review with owner | owner signs; T spec rows flip to production-authorized per part | any part not demonstrated | signed ASM-48 note | production CAD session | iterate the specific part; P10 is per-part, not all-or-nothing |

**Standing-gate cross-map (unchanged, RST-07):** Gate A/B → prerequisite of P3 (rear);
Gate C (D-06/D-07 + blower) → prerequisite of MOD-CAM steps in P6 and of PS-10/11 CAD;
Gate D residual (D-09) → prerequisite of P4 servo rows and ASM-06; D-18 gimbal
endpoints → stays behind firmware A2 + Phase B (ASM-39 only *records geometry*);
battery purchase → after D-01 (P0), per F §6.

## P0-CAD evidence available `(CAD-01/P0-CAD)`

The reproducible diagnostic sources and ignored STL set for CAD-01/02/04/06/08 are now
available under [`cad/`](cad/); this is modelling/output evidence, not a TP print and
does not skip P1. Execute P1 with the exact item-by-item form in
[`cad/reports/P1_dry_fit_checklist.md`](cad/reports/P1_dry_fit_checklist.md). The form
requires body/connector/bend/hand/insertion/removal/shell/floor/D-26/neighbour/route/
service/balance/photo observations and explicitly maps the observations controlling the
narrow-deck continuation, fallback-A trigger, tray/shelf/junction revisions and post
height. P2 remains locked until that physical evidence exists.

Local automated validation passes deterministic regeneration, non-empty mm meshes,
parameter-derived bboxes, bed orientation, closed/oriented primitive shells, D-26
height and 256 mm plate fit. Because no Boolean mesh engine or Bambu Studio CLI is
installed, strict global manifold union and slicer/layer checks are an explicit
pre-print requirement; they are not silently counted as passed.
