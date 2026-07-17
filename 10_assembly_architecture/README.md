# 10 · Assembly Architecture — Session 1 evidence package

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
corrections are tagged "(1.5)" in place)**. Uncommitted by design. Nothing here
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
