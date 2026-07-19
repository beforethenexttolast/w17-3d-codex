# 10 · Assembly Architecture — evidence package (Session 1/1.5) + architecture set (Session 2)

**Purpose.** Establish, from evidence, **whether the planned W17 vehicle can physically
and electrically be assembled** on the OpenRC RC-01 chassis with our FPV/dual-ESP32/
audio/lighting/gimbal electronics package — *before* anyone commits to a final assembly
architecture or production CAD. This is a **constraint-definition** package, not a
manual and not a design.

**Scope of this session (Session 1).** Evidence collection, dimensional investigation,
and constraint definition only. **No architecture decisions are made here.** Decisions
belong to Session 2, which must be able to rely on this package instead of repeating the
investigation.

**Status:** DRAFT / provisional evidence model, **reviewed and corrected by Session 1.5
(2026-07-17, independent skeptical pass — see `G_session1_5_review_findings.md`;
corrections are tagged "(1.5)" in place)**. **Session 2 (2026-07-18) added the
architecture set H–T under the 1.5 restrictions** — all placements remain PROVISIONAL
until their listed measurements (see `R_validation_gates.md` P0); Session-2 additions
to D/E are tagged "(S2)". **Session 3 (2026-07-18, independent skeptical review — see
`U_session3_review_findings.md`) verified the H comparison arithmetic and the L budget
independently, corrected the reports in place (tagged "(S3)": new CN-16/DN-11/E-26,
D-24 scope extension, gate-prerequisite fixes in R, dummy-stub rule in K/T, balance
ledger in I), and issued the verdict **APPROVED FOR P0 + CAD-01**.** **Session 4A (2026-07-18)
executed the P0 digital/slicer-stage measurements — results in
`V_P0_geometry_measurement_results.md`, deltas tagged "(P0)" in D/I/J/K/S/T,
reproducible evidence under `evidence/`; the S0 shell-seat pin at Gate P1 is the
decisive physical residual.** **The independent Session 4A checkpoint review (`W`)
reproduced the evidence, corrected findings F4A-01…05, and issued `P0 VERIFIED WITH
MINOR CORRECTIONS — READY FOR CHECKPOINT`.** **The recovered diagnostic-CAD final review
(`cad/reports/X_diagnostic_cad_review.md`, 2026-07-19) corrected fit/evidence defects,
reproduced all authorized CAD-01/02/04/06/08 outputs and issued `DIAGNOSTIC CAD VERIFIED
WITH MINOR CORRECTIONS`; mandatory slicer preflight and physical P1 remain open.** Nothing here
supersedes the authoritative print-side docs (`../BUILD_SHEET.md`,
`../MODEL_INVENTORY.md`, `../MATERIAL_DECISION_MATRIX.md`, `../FIRST_PRINT_DECISION.md`,
`../CAMERA_GIMBAL_PLACEMENT.md`) — it *consumes* them and adds the mechanical-integration
lens they do not carry.

## Files

| File | What it is |
|---|---|
| [`A_assembly_evidence_report.md`](A_assembly_evidence_report.md) | Sources inspected, visual/dimensional findings, original assembly dependencies, inaccessible areas, usable-space observations, confidence of each conclusion |
| [`B_component_envelope_register.md`](B_component_envelope_register.md) | Every onboard item + its *installation envelope* (body + connectors + cable + mounting), status, evidence source |
| [`C_clearance_keepout_register.md`](C_clearance_keepout_register.md) | Chassis zones + movement/access keep-outs, affected components, evidence level, required physical test |
| [`D_measurement_plan.md`](D_measurement_plan.md) | Every unresolved measurement: what, reference points, tool, accuracy, why, what it blocks |
| [`E_constraint_risk_register.md`](E_constraint_risk_register.md) | Packaging/thermal/RF/service risks: likelihood, consequence, mitigation, validation, blocker status |
| [`F_session2_input_brief.md`](F_session2_input_brief.md) | The engineering brief for Session 2: confirmed/provisional/prohibited zones, mandatory vs optional components, critical measurements, what Session 2 may and may not decide |
| [`G_session1_5_review_findings.md`](G_session1_5_review_findings.md) | **Session 1.5 skeptical review**: findings register (R-01…R-14), what re-verified clean, in-place corrections applied to A–F (tagged "1.5"), and the Session-2 readiness verdict — **READY WITH RESTRICTIONS** |
| [`H_packaging_architecture_comparison.md`](H_packaging_architecture_comparison.md) | **Session 2**: virtual dry-fit (parameters P1–P11, datums), four candidate architectures, weighted comparison, **selected + fallback architecture** |
| [`I_zone_layer_plan.md`](I_zone_layer_plan.md) | Session 2: zone/layer plan, vertical stack with explicit datums, per-zone register, balance ledger — **authoritative for zone IDs** |
| [`J_component_placement_matrix.md`](J_component_placement_matrix.md) | Session 2: complete component-placement matrix (every Report-B item), access/environment/sequence attributes |
| [`K_printable_support_spec.md`](K_printable_support_spec.md) | Session 2: printable support parts PS-01…PS-17 (+ rejected structure) — **authoritative for PS IDs** |
| [`L_power_architecture.md`](L_power_architecture.md) | Session 2: power topologies T1/T2, protection/disconnect options, **provisional per-rail current budget (gated D-24)** |
| [`M_connector_harness_matrix.md`](M_connector_harness_matrix.md) | Session 2: modules, connector/harness matrix, labeling — **authoritative for CN-xx / H-xx / MOD-xx IDs** |
| [`N_cable_routing_plan.md`](N_cable_routing_plan.md) | Session 2: physical routes R1/R2 + crossings X1/X2, per-harness routing, logical / physical / module-disconnect diagrams |
| [`O_thermal_rf_vibration_safety.md`](O_thermal_rf_vibration_safety.md) | Session 2: thermal paths (named inlets/exhausts), RF/EMI plan, vibration/crash, safety review |
| [`P_assembly_master_manual.md`](P_assembly_master_manual.md) | Session 2: dependency-aware assembly manual **ASM-01…ASM-48** — authoritative for assembly order |
| [`Q_service_disassembly_guide.md`](Q_service_disassembly_guide.md) | Session 2: service/disassembly procedures (no-desolder rule, timed drills) |
| [`R_validation_gates.md`](R_validation_gates.md) | Session 2: validation gates **P0–P10** + cross-map to the unchanged Session-1 gates |
| [`S_decision_register.md`](S_decision_register.md) | Session 2: decision register **DN-01…DN-10**, decision audit, registry-addition log |
| [`T_cad_task_spec.md`](T_cad_task_spec.md) | Session 2: CAD-task spec (diagnostic only — **no production STL authorized**) |
| [`U_session3_review_findings.md`](U_session3_review_findings.md) | **Session 3 skeptical review**: findings register F3-01…F3-18, corrections applied in place (tagged "(S3)"), subsystem readiness matrix, verdict **APPROVED FOR P0 + CAD-01** |
| [`V_P0_geometry_measurement_results.md`](V_P0_geometry_measurement_results.md) | **Session 4A P0 measurements**: P0 vehicle frame + datums (DAT-F verified; S0 residual), D-01/02/03/04/25/26/27 digital results, ten P0 conclusions, physical hand-off list — registers carry the deltas tagged "(P0)"; reproducible via `evidence/scripts/p0_0N_*.py` (evidence in `evidence/p0/`) |
| [`W_session4A_P0_verification.md`](W_session4A_P0_verification.md) | **Independent Session 4A checkpoint review**: scripts/determinism/STL-integrity checks, high-impact measurement reproductions, evidence-asset inspection, findings F4A-01…05 corrected in place; verdict **P0 VERIFIED WITH MINOR CORRECTIONS — READY FOR CHECKPOINT** |
| [`cad/`](cad/) | **(CAD-01/P0-CAD)** reproducible diagnostic CAD for authorized CAD-01/02/04/06/08 only: authoritative parameter CSV, dependency-free Python sources, ignored STL/render outputs, automated validation report and exact P1 dry-fit checklist; no production or blocked geometry |
| [`cad/reports/X_diagnostic_cad_review.md`](cad/reports/X_diagnostic_cad_review.md) | **Independent recovered-CAD final review**: inventory, deterministic reproduction, mesh/plate/visual/scope audit, findings XCAD-01…10 corrected; verdict **DIAGNOSTIC CAD VERIFIED WITH MINOR CORRECTIONS** |

**Authority map (one home per subject):** measurements → `D` (updated in place, S2 adds
D-26/D-27) · risks → `E` (S2 adds E-25) · decisions → `S` · zones → `I` · placements →
`J` · printed parts → `K` · power/rails → `L` · connectors/harnesses → `M` · routing →
`N` · thermal/RF/safety → `O` · assembly order → `P` · service → `Q` · session gates →
`R` (pre-existing Gates A–D live in `BUILD_SHEET.md`/`GENERAL_PLAN.md`, unchanged) ·
CAD hand-off → `T`. Reports A–C and F–H are frozen evidence/selection records.

## Confidence vocabulary (used throughout)

- **CONFIRMED** — measured on real hardware, or read directly off a supplier drawing/README, or reproduced by independent computation.
- **DERIVED** — computed from a trustworthy source (e.g. STL vertex bounding box, arithmetic on confirmed numbers).
- **ESTIMATED** — typical datasheet/typical-part value, or read approximately from a photo; plausible but unverified for *our* specific hardware.
- **TO MEASURE** — not yet known; a physical or slicer measurement is required.
- **BLOCKER** — an open question that stops a downstream step (CAD / print / wiring / final assembly) until resolved.

## One-line finding

The **mechanics** of the RC-01 are a known, buildable quantity; the **open risk is
electronics packaging** — we are placing ~3–4× the component count of the original design
into the same (or a smaller) open centre-spine volume that is already occupied by the
central rear shock, the drivetrain, and the steering linkage, **with no printed
mounts/trays for any of it in the current file set.** Details in E and F.
