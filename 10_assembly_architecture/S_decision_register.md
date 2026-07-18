# S · Session-2 Decision Register (DN-xx) & Decision Audit

Session 2 · 2026-07-18. Companion to `D_measurement_plan.md` (measurements) — this file
holds **decisions**. Statuses: DECIDED (S2) · RECOMMENDED (needs owner confirm) ·
DECISION-NEEDED (owner) · GATED (waits on a measurement/gate). Nothing here alters a
pre-existing gate (RST-07).

## S.1 New decision entries

| ID | Decision | Options | Status | Recommendation | Gate / input | Where used |
|---|---|---|---|---|---|---|
| **DN-01** | Fuse / overcurrent protection | none · accessory-branch mini-blade · full main-line | **DECISION-NEEDED (owner)** | accessory-branch mini-blade; **rating only after D-24** (placeholder 7.5 A) | D-24 → Gate P9 | L.3, PS-15, ASM-18 |
| **DN-02** | Main disconnect | XT60 unplug (body-off) · **loop-key XT60 at PS-15, cockpit-reachable** · switch (rejected as sole) | **DECISION-NEEDED (owner)** | loop-key | — (seat printed either way) | L.3, O.4, Q emergency row |
| **DN-03** | ESC-BEC treatment | isolate red wire (BOM bench note) · use as Rail B (L.2 T2) | **DECIDED (S2, carries BOM plan-of-record)** | isolate; revisit only with T2 bench evidence | — | L.1, ASM-16, ASM-34 |
| **DN-04** | WS2812 current cap | firmware brightness/current limit vs full 1.8 A | **GATED** | cap so Rail A sustained ≤80% of rating; value from D-24 data | **D-24** | L.4, ASM-36/42 |
| **DN-05** | Camera placement Option A (cockpit) vs B (halo pod) | A · B | **DECISION-NEEDED (owner)** — pre-existing open decision, registered here; rule "A unless halo occlusion fails" per `CAMERA_GIMBAL_PLACEMENT.md` | — | D-06, D-07, halo-occlusion dry-fit | Z8, PS-10, ASM-26 |
| **DN-06** | Driver figure vs Option A camera | mutually exclusive occupants (R-14) | **DECISION-NEEDED (owner)** — couples to DN-05 | decide together with DN-05 | DN-05 | Z8 |
| **DN-07** | Speaker location | Z4L sidepod port · under-deck facing airbox | **GATED** | sidepod if D-03 clears it (audibility) | **D-03** | PS-14, J row AUD-SPK |
| **DN-08** | USB/programming access | body-off only · parked pigtails (PS-17) · body port (shell mod) | **DECISION-NEEDED (owner)** | parked pigtails (no shell modification) | D-11 dry-fit | PS-17, H-11, Q programming row |
| **DN-09** | Rail B voltage | 5 V · 6 V | **GATED** | 5 V until MG90S at 6 V is bench-verified | Gate P4 | L.1/L.4, ASM-21 |
| **DN-10** | Rear-shell exhaust vent (body modification) | none needed · add vent | **GATED** | decide from the D-01 slicer sitting (is the shell closed over the motor?) + D-19 | D-01 view + D-19 | O.1, ASM-43 |
| **DN-11** | Camera↔WiFi USB module-boundary treatment (added S3 — risk E-26: the BOM solder-only run crosses the MOD-CAM/MOD-DECK boundary and defeats one-piece module removal) | **CN-16** latched signal-grade connector at the deck edge · keep solder-only and accept deck+camera as one documented combined service unit | **DECISION-NEEDED (owner)** | CN-16; USB-2.0 integrity bench-verified at Gate P4 **before** the BOM solder note is amended | Gate P4 | M.1/M.2 (CN-16), N H-07, Q deck-out + camera rows, K PS-04 |

## S.2 Decision audit — Session-1/1.5 decisions carried unchanged

Per F §7 and RST-07, all remain as stated there: chassis/steering config, belt drive,
2024 body/W17, Gate B front files, Gate D `Servoholder`, battery envelope, 68 mm rear
shock, 2021 DRS wing preference (gated), rear-stack path (OPEN, Gate A), camera
integration (OPEN, Gate C + DN-05), DRS reinstated. **No gate opened or closed this
session.** New Session-2 selections that are *architecture* (not gate) decisions:
H.4 recommended + fallback architectures; zone allocations in I/J (each tagged with
its own confidence and blockers).

## S.3 Registry additions made by Session 2 to existing registers

- `D_measurement_plan.md`: **D-26** (steering-rod line height + sweep), **D-27**
  (floor M3 slot-map for support mounting) — added in place, tagged (S2).
- `E_constraint_risk_register.md`: **E-25** (rod-height uncertainty over the side
  bays) — added in place, tagged (S2).
- No Session-1 content was removed or reworded beyond these tagged additions.
- **Session 3 (2026-07-18 skeptical review)** added, all tagged "(S3)": **E-26** to E,
  **CN-16** to M, **DN-11** here; D-24 scope extended in place in D; corrections applied
  in I/J/K/L/M/N/O/P/Q/R/T (+ two tagged addenda in frozen H). Findings register:
  `U_session3_review_findings.md`.
- **Session 4A (2026-07-18, P0 measurement)** added, all tagged "(P0)": results table
  in D; measured notes in I/J/K/T; README updated; new report
  `V_P0_geometry_measurement_results.md` + `evidence/` (scripts p0_00…p0_06, tables,
  sections, diagrams). **No decision was taken or reopened**: DN-05/06/07/08/11 remain
  owner calls; no gate opened/closed; the H.4 fallback-A trigger is armed pending the
  S0 physical pin, not fired. No production CAD authorized.
