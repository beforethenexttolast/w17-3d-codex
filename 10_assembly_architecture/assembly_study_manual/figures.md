# Figure index

This index separates newly authored schematic views from existing diagnostic-CAD
renders. Every schematic is approximate and inherits the confidence of its cited
evidence; none creates a new dimension authority.

| Fig. | Asset | View / purpose | Evidence basis | Key status boundary |
|---:|---|---|---|---|
| 01 | [`assets/fig01_system_layers.svg`](assets/fig01_system_layers.svg) | System/layer overview | `I` §§1–3; `V` §§4–7, 13; `M` §1 | Narrow deck conditional on physical S0/P1; camera optional/gated. |
| 02 | [`assets/fig02_top_layout.svg`](assets/fig02_top_layout.svg) | Approximate top packaging | `I` zone register; `J`; `V` §§4, 9–13 | Allocations, not part outlines; architecture-right = `L<0`. |
| 03 | [`assets/fig03_side_section.svg`](assets/fig03_side_section.svg) | Longitudinal height logic | `V` §§5–7, 9; `I` §1 | DAT-F confirmed; S0 and physical D-26 open. |
| 04 | [`assets/fig04_front_section.svg`](assets/fig04_front_section.svg) | Transverse left/right stack | `V` §§6, 9, 11; `I` §§1, 3 | Shell profile schematic; H20 is a gauge plane only. |
| 05 | [`assets/fig05_exploded_modules.svg`](assets/fig05_exploded_modules.svg) | Semi-exploded module stack | `M` §1; `K`; `Q` | CN-16 recommended/owner decision; no normal vehicle-level desolder. |
| 06 | [`assets/fig06_architecture_options.svg`](assets/fig06_architecture_options.svg) | Single-level / two-level / bridge / skeleton comparison | `H` §§3–4; `I`; `V` §13 | `B+D` recommended conditionally; A remains fallback; bridge rejected. |
| 07 | [`assets/fig07_connectorization.svg`](assets/fig07_connectorization.svg) | Connector/service boundary map | `L` §§1–3; `M` §§1–3; `Q` | Families/ratings/lengths provisional to D-24/D-10/P9. |
| 08 | [`assets/fig08_harness_routes.svg`](assets/fig08_harness_routes.svg) | R1/R2, X1/X2 and H-08 routes | `N` §§1–5; `V` §9 | Corridors only; real bend/loop/bulk check required. |
| 09 | [`assets/fig09_assembly_sequence.svg`](assets/fig09_assembly_sequence.svg) | Ten-stage assembly logic | `P` ASM-01…48; `R` P0…P10 | Summary only; named gate failures stop downstream work. |
| 10 | [`assets/fig10_service_paths.svg`](assets/fig10_service_paths.svg) | Removal dependency map | `Q`; `M` §1 | U.FL handling and recalibration steps remain load-bearing. |
| 11 | [`assets/fig11_conflicts_decisions.svg`](assets/fig11_conflicts_decisions.svg) | Decision-driving physical checks | `V` §13; `R`; `S`; P1 checklist | Branches are inputs, not decisions or production authorization. |

## Existing diagnostic-CAD render set used by the manual

These PNGs are generated locally and ignored by Git. If missing, regenerate them per
[`../cad/README.md`](../cad/README.md). They illustrate diagnostic envelopes and
support concepts only.

| Render | Manual use | Diagnostic meaning |
|---|---|---|
| [`render_cad01_core_power.png`](../cad/generated/renders/render_cad01_core_power.png) | Battery/ESC/UBEC installation-envelope family | Includes connector, bend, fan, cooling, and restraint gauges; hardware sizes remain as registered. |
| [`render_cad01_controllers.png`](../cad/generated/renders/render_cad01_controllers.png) | Controller/Wi-Fi/amplifier envelope family | Wi-Fi is explicitly the unconfirmed P9 maximum. |
| [`render_cad01_access.png`](../cad/generated/renders/render_cad01_access.png) | Steering and connector-bank access study | Servo is a KO-19 stand-in; connector bank is an allocation gauge. |
| [`render_cad02_battery_tray.png`](../cad/generated/renders/render_cad02_battery_tray.png) | PS-01 open tray concept | DIAG-CAD only; clamp and physical floor fit remain open. |
| [`render_cad04_ubec_shelf.png`](../cad/generated/renders/render_cad04_ubec_shelf.png) | PS-03 two-lane shelf concept | Real UBECs and D-24 can still resize it. |
| [`render_cad06_post_family.png`](../cad/generated/renders/render_cad06_post_family.png) | H20/H26/H32 height gauges | No deck geometry and no selected production height. |
| [`render_cad08_junction_support.png`](../cad/generated/renders/render_cad08_junction_support.png) | PS-15 open connector support | DN-01/DN-02 and post shoulders intentionally remain open. |
| [`render_cad08_decision_blanks.png`](../cad/generated/renders/render_cad08_decision_blanks.png) | Visible open-decision gauges | Blanks prevent diagnostic CAD from silently selecting fuse/disconnect choices. |

## Coordinate and visual conventions

- Top views put **front at left** for page readability.
- Architecture-right/belt side remains P0 `L<0`; architecture-left is `L>0`.
- `DAT-F` is the floor top (`Z=0`). `DAT-S = DAT-F + S0`.
- Green = confirmed, blue = recommended, amber = provisional/conditional,
  red = physical check/blocker, purple = optional.
- Dashed shells, envelopes, and corridors are schematic or reserved volumes.
- Component rectangles do not imply mounting-hole locations, production shape, or
  exact installed orientation beyond the labels in `J`.
