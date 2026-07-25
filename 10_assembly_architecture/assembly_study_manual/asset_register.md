# View and asset register

## A. Manual-authored assets

| Asset ID | File | Type | Traceability | Confidence carried | Known limitation |
|---|---|---|---|---|---|
| ASM-STUDY-V01 | `assets/fig01_system_layers.svg` | Exploded layer schematic | I/V/M | Mixed confirmed/recommended/provisional | Vertical spacing not dimensional. |
| ASM-STUDY-V02 | `assets/fig02_top_layout.svg` | Top layout schematic | I/J/V/N | Zone allocations | Shell/floor silhouette simplified; no mounting points. |
| ASM-STUDY-V03 | `assets/fig03_side_section.svg` | Longitudinal section | V/I | DAT-F and P0 bands traceable | Shell profile and module stations schematic. |
| ASM-STUDY-V04 | `assets/fig04_front_section.svg` | Transverse section | V/I | Height/side logic traceable | Not taken from one exact section station. |
| ASM-STUDY-V05 | `assets/fig05_exploded_modules.svg` | Module exploded view | M/K/Q | Module boundaries recommended | No fastener geometry or cable lengths. |
| ASM-STUDY-V06 | `assets/fig06_architecture_options.svg` | Architecture comparison | H/I/V | Current selection logic | Qualitative summary; H retains scoring authority. |
| ASM-STUDY-V07 | `assets/fig07_connectorization.svg` | Electrical module diagram | L/M/Q | Topology recommended | Connector sizing/gauge/length provisional. |
| ASM-STUDY-V08 | `assets/fig08_harness_routes.svg` | Route diagram | N/V | Corridors recommended | Harness bulk/bends physically unresolved. |
| ASM-STUDY-V09 | `assets/fig09_assembly_sequence.svg` | Sequence flow | P/R | Dependency order traceable | Condenses ASM-01…48; does not replace them. |
| ASM-STUDY-V10 | `assets/fig10_service_paths.svg` | Removal tree | Q/M | Service intent recommended | Timed drills not yet demonstrated. |
| ASM-STUDY-V11 | `assets/fig11_conflicts_decisions.svg` | Decision tree | V/R/S/P1 | Open-state faithful | Does not take owner decisions. |

All eleven SVGs are tracked text assets with no external fonts, scripts, raster links,
or hidden geometry. They are designed to render in Markdown viewers and directly in
the local HTML edition.

## B. Existing engineering evidence referenced

| Asset/evidence | Location | Status | What it supports | What it cannot prove |
|---|---|---|---|---|
| P0 floor map | `../evidence/p0/diagrams/p0_d01_floor_map.svg` | **CONFIRMED digital evidence** | DAT-F, floor silhouette, features, battery span, D-27 geometry | Assembled flatness, screw protrusion, physical occupancy. |
| P0 transverse/longitudinal sections | `../evidence/p0/sections/` | **CONFIRMED lower-bound digital evidence** | Shell ceilings at `S0=0`, airbox width, nose sections | Absolute clearance until S0 is measured. |
| P0 evidence tables | `../evidence/p0/tables/` | **CONFIRMED/DERIVED** | Stations, floor features, D-26 arithmetic, deck-side map | Powered motion or real assembled seating. |
| CAD parameter authority | `../cad/parameters/cad_parameters.csv` | **TRACEABLE mixed status** | All implemented diagnostic dimensions/status/source links | Production dimensions. |
| CAD source | `../cad/sources/` | **REPRODUCIBLE DIAG-CAD** | Authorized CAD-01/02/04/06/08 geometry | CAD-03/05/07, blocked supports, donor assembly. |
| Generated validation | `../cad/reports/generated_part_validation.md` | **PASS within stated validator scope** | Output set, bounds, deterministic generation, primitive-shell incidence | Global Boolean manifold, final slicer quality, physical fit. |
| Diagnostic manifest | `../cad/reports/diagnostic_cad_manifest.md` | **REVIEWED** | Per-output purpose, orientation, limitation | TP print/P1 pass or production authorization. |
| P1 dry-fit checklist | `../cad/reports/P1_dry_fit_checklist.md` | **OPEN physical form** | Required body/connector/bend/hand/removal evidence | Nothing until completed with measurements/photos. |
| P1 print preflight | `../cad/reports/P1_print_preflight.md` | **Working preflight** | Minimum staged print/slicer workflow | Physical gate closure. |

## C. Generated local render register

Source: `../cad/generated/renders/`. Policy: PNGs are ignored by `.gitignore`; tracked
CAD sources and reports are the reproducible record.

| Family | Files | Status/use |
|---|---|---|
| CAD-01 grouped | `render_cad01_core_power.png`, `render_cad01_controllers.png`, `render_cad01_access.png` | Visual QA of diagnostic envelope clusters. |
| CAD-01 close-ups | battery, ESC, UBEC A/B, CTL E1/E2, Wi-Fi, amp, servo, connector-bank renders | Per-dummy inspection; expected/provisional sizes remain labelled in CSV/manifest. |
| CAD-02 | battery-tray and plate-clamp renders | PS-01/reversible-clamp concept; physical coupon still required. |
| CAD-04 | UBEC-shelf render | Separate rail pockets and open service/airflow. |
| CAD-06 | post-family render | H20/H26/H32 gauges only. |
| CAD-08 | junction-support and decision-blank renders | Open frame and explicit DN-01/DN-02 non-selection. |

## D. Regeneration and review

From repository root:

```bash
python3 10_assembly_architecture/cad/sources/generate.py
python3 10_assembly_architecture/cad/sources/validate.py
```

Then inspect the exact 19 PNG set and use Bambu Studio for the pre-print layer/repair/
bridge/text checks. A regenerated render or passing local validator is not permission to
print or promote a part to production.
