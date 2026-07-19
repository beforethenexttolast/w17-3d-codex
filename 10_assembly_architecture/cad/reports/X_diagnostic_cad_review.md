# X · W17 diagnostic-CAD recovery and final review

**Review date:** 2026-07-19
**Repository checkpoint:** `794bcf7 docs: establish W17 assembly architecture and P0 geometry evidence`
**Scope:** recovered CAD-01, CAD-02, CAD-04, CAD-06 and CAD-08 diagnostic work only
**Verdict:** **DIAGNOSTIC CAD VERIFIED WITH MINOR CORRECTIONS**

The lost session had substantially completed the requested diagnostic CAD, but it was
not ready to close unchanged. Independent geometry and visual review found five
fit-invalidating defects and several evidence/reporting gaps. The defects were corrected
in the recovered parametric sources, all outputs were regenerated, and no unresolved
`CRITICAL` or `HIGH` finding remains. This verdict releases the outputs to the mandatory
Bambu Studio pre-print inspection and then the P1 diagnostic-print/dry-fit process; it
does not authorize production geometry or skip the physical gates.

## 1. Recovery state and method

The repository gate matched the required repository and checkpoint. The recovered tree
contained the full source/configuration set, 20 individual STLs, six plate STLs, seven
initial renders and three implementation reports. No temporary output, cache or
unexplained file was present. The missing independent `X` report and insufficient visual
coverage showed that the previous session had completed implementation but not its final
skeptical review/handoff.

The review read the architecture authority set and every file under `cad/`, audited all
parameter consumers and output declarations, reproduced generation, parsed every mesh,
checked each grouped plate against its declared source meshes, and visually inspected all
original and added renders. It did not repeat the P0 chassis investigation.

OpenSCAD, FreeCAD, Bambu Studio, Blender, MeshLab/admesh, Manifold, NumPy and trimesh were
not available locally. Consequently the review used the repository's dependency-free
Python mesh convention and records the slicer/Boolean limitation explicitly.

## 2. Complete final inventory

The final `cad/` tree contains **55 files** in the following explained categories:

| Classification | Count | Files |
|---|---:|---|
| Source | 4 | `sources/generate.py`; `sources/parts.py`; `sources/validate.py`; `sources/lib/meshkit.py` |
| Parameter data | 1 | `parameters/cad_parameters.csv` |
| Individual STL | 20 | `generated/stl/cad01_aud_amp.stl`; `cad01_ctl_e1.stl`; `cad01_ctl_e2.stl`; `cad01_drv_esc.stl`; `cad01_ps15_connector_bank.stl`; `cad01_pwr_bat_max.stl`; `cad01_pwr_ubec_a.stl`; `cad01_pwr_ubec_b.stl`; `cad01_srv_steer.stl`; `cad01_vid_wifi_max.stl`; `cad02_ps01_battery_tray.stl`; `cad02_ps01_plate_clamp_foot.stl`; `cad04_ps03_plate_clamp_foot.stl`; `cad04_ps03_ubec_shelf.stl`; `cad06_ps05_post_h20.stl`; `cad06_ps05_post_h26.stl`; `cad06_ps05_post_h32.stl`; `cad08_ps15_dn_open_blanks.stl`; `cad08_ps15_junction_support.stl`; `cad08_ps15_plate_clamp_foot.stl` |
| Grouped plate STL | 6 | `generated/stl/plate_01_core_power_dummies.stl`; `plate_02_controller_communication_dummies.stl`; `plate_03_connector_bank_access_dummies.stl`; `plate_04_battery_tray_test.stl`; `plate_05_ubec_shelf_junction_support.stl`; `plate_06_post_height_set.stl` |
| Render | 19 | `generated/renders/render_cad01_access.png`; `render_cad01_amp.png`; `render_cad01_battery.png`; `render_cad01_connector_bank.png`; `render_cad01_controllers.png`; `render_cad01_core_power.png`; `render_cad01_ctl_e1.png`; `render_cad01_ctl_e2.png`; `render_cad01_esc.png`; `render_cad01_servo.png`; `render_cad01_ubec_a.png`; `render_cad01_ubec_b.png`; `render_cad01_wifi.png`; `render_cad02_battery_tray.png`; `render_cad02_plate_clamp.png`; `render_cad04_ubec_shelf.png`; `render_cad06_post_family.png`; `render_cad08_decision_blanks.png`; `render_cad08_junction_support.png` |
| Report/document | 5 | `README.md`; `reports/diagnostic_cad_manifest.md`; `reports/generated_part_validation.md`; `reports/P1_dry_fit_checklist.md`; `reports/X_diagnostic_cad_review.md` |
| Temporary output | 0 | None |
| Cache | 0 | None |
| Unexplained | 0 | None |

The STL and PNG files are repository-ignored generated evidence; their absence from an
ordinary Git diff is expected.

## 3. Completion audit

| Deliverable | Recovered state | Final state |
|---|---|---|
| CAD-01 dummies | Implemented, with envelope/floating-feature defects | Complete for authorized diagnostic scope; ten installation-envelope dummies corrected and validated |
| CAD-02 / PS-01 | Implemented, balance-lead provision absent | Complete; 78 mm open tray, strap/XT60/balance/ballast provisions and reversible clamp coupon |
| CAD-04 / PS-03 | Implemented, two 18 mm dummies could not fit its 12 mm-clear lanes | Complete; two separate 18 mm-clear Rail A/B lanes, open airflow/removal, verified feature plus clamp |
| CAD-06 / PS-05 | Implemented | Complete; independent H20/H26/H32 gauges, DAT-F reference, no CAD-05 surface or selected height |
| CAD-08 / PS-15 | Implemented, but test seats/vent rail/shoulders conflicted | Complete for diagnostic scope; non-overlapping seats, open access, vent-safe frame, clamps and open-decision blanks; shoulder position explicitly deferred |
| Parameter manifest | Present | Complete; 148 populated, unique and traceable rows |
| Validation report | Present, weaker plate/render assertions | Complete; exact output/render sets, exact plate membership/count, overlap and deterministic regeneration checks |
| Build-plate groups | Six present | Complete; exact declared membership and no XY bbox overlap; all fit 256 × 256 mm |
| P1 checklist | Present | Complete; corrected envelope/features and shoulder deferral reflected |
| K/R/T/README handoff | Present | Cross-checked and corrected to match generated outputs and limitations |
| Independent final report | Missing | This report completes it |

## 4. Reproduction and source-integrity evidence

Generation was run twice from the repository root with the documented command. Both
runs replaced the fixed `*.stl` and `*.png` output sets. The validator then performed
two additional isolated temporary-directory regenerations.

| Evidence | Result |
|---|---|
| Generated STL set | 26 files on each run; aggregate SHA-256 `022a25008ada9c120ec0633a78756be82395e19d7cc51a6372895d4c8a9edbbf` on both runs |
| Generated render set | 19 files on each run; aggregate SHA-256 `8b6b5505e71e568c95249a44e7f1bcaac12b7a695f2e8a8912f30eebd22d04ca` on both runs |
| Validator isolated regeneration | Two byte-identical STL maps; PASS |
| Python syntax | All four source modules compile; PASS |
| Paths | Repository-root-relative; running from `cad/` exits 2 with `FATAL: run from repository root ...` |
| Cleanup | Fixed output directories; stale STL and PNG suffixes are removed before exact-set write/check |
| External/ignored state | No source imports donor STLs, temporary files or generated local state |
| Donor integrity | No changes under `02_ready_to_slice/`; every generated SHA-256 differs from every donor STL hash |

The implementation reads only the CSV and its own Python modules. It never rewrites or
derives geometry by loading a donor STL.

## 5. Mesh and plate validation

[`generated_part_validation.md`](generated_part_validation.md) is the detailed machine
report. All 20 individual and six grouped files exist, are non-empty binary STLs marked
in millimetres, start at Z=0, match their parameter-derived expected bboxes, contain only
non-zero-area triangles, and have zero boundary and orientation-mismatch edges. Support
geometry remains below the D-26 Z=35 mm lower boundary. Individual bbox results are:

| Family | Validated bboxes in mm |
|---|---|
| CAD-01 | amp 37×19×8; E1/E2 80×44×13 each; ESC 67×40×36; connector bank 105×40×28; battery 95×50×30; UBEC A/B 54×18×15 each; servo 52×40×42.9; Wi-Fi 90×32×20 |
| CAD-02 | tray 78×50×12; clamp 14×12×10.8 |
| CAD-04 | shelf 70×42×12; clamp 14×12×10.8 |
| CAD-06 | H20/H26/H32 27.3×12×20/26/32 |
| CAD-08 | blanks 45×12×2.1; support 40×55×12; clamp 14×12×10.8 |

The six plate bboxes are 228×74×36, 166×82×20, 163×40×42.9, 118×50×12,
227×73×12 and 93.9×12×32 mm. Validation now reconstructs each plate from its declared
part/count layout and compares its quantized triangle multiset to the on-disk plate. It
also independently rejects XY bbox overlap. Exact membership, counts, non-overlap and
256 mm bed fit all pass.

The edge-incidence check finds closed, consistently oriented component shells, but some
STLs have `>2` incidence at intersections/touching labels. Without a Boolean engine this
is not proof of one globally unioned 2-manifold. That is a documented pre-print check,
not a hidden pass.

## 6. Part-family review

### CAD-01 installation-envelope dummies

- **Battery:** the confirmed 75×45×25 maximum body is now inside the registered
  95×50×30 restraint/strap installation cage. The forward XT60, explicit forward cable,
  initial bend cage, orientation and maximum-only status are present.
- **ESC:** body/mount allowance, forward XT60, three distinct aft phase exits and bends,
  Ø30 fan, heatsink/cooling volume and airflow direction are present.
- **UBEC A/B:** distinct geometric Rail A/B IDs, leads and bend zones at both ends,
  mount allowance, open cooling cage and direction arrow are present.
- **CTL-E1/E2:** body, connected header envelope, occupied USB stub, 15 mm cable-bend and
  access side, mount/standoff allowance, arrow and distinct IDs are present.
- **Wi-Fi:** only the authorized P9 maximum is represented. `UNCONFIRMED ENVELOPE`, two
  aft pigtails, power exit, CN-16 boundary, bends, confirmed heatsink and cooling cage are
  present; it makes no actual-module claim.
- **Amplifier:** body/mount, I2S and speaker exits/bends, orientation and bed-connected
  adjustment/tool-access volume are present.
- **Steering-servo stand-in:** body/lead/bend, maximum horn-sweep disc, direction and a
  top-visible ID are present; it is explicitly not a new mount.
- **Connector bank:** body, XT60/three-XT30 allowances, wire/bend and extraction volume,
  mating-hand volume, tool access and support/reference region are present.

None is a body-only plain block where a connector, bend, access or cooling envelope
controls fit. No donor/chassis shape appears in any dummy.

### CAD-02 / PS-01 battery tray

The source parameterizes the recovered 78 mm bay and battery dependency. The DAT-F-open
frame exposes floor interruptions; the forward face supports top insertion/removal and
XT60/cable-bend clearance. Two 20 mm strap interruptions, side restraint, an open-top
balance-lead park and an outboard 5 g ballast land are present. Attachment uses two
reversible plate-edge clamp receivers/coupons and invents no chassis hole.

### CAD-04 / PS-03 UBEC shelf

The corrected 70×42×12 shelf has two separate 18 mm-clear lanes for the full diagnostic
UBEC widths. Both ends remain open for leads and upward service removal, and the frame is
open for airflow. It uses only the verified X=-39.99/L=-32.86 feature plus one reversible
clamp. All support geometry is below D-26; no mounting grid is assumed. D-24 may still
resize the physical pockets after the actual parts arrive.

### CAD-06 / PS-05 post family

H20, H26 and H32 start at DAT-F/seat Z=0, contain M3 passages and connected readable
height/PS flags, and remain separately replaceable. There is no deck surface and no
selected production height. PS-03 provides the diagnostic shoulder-fit interface;
PS-15 shoulder position is correctly left for physical S0/P1.

### CAD-08 / PS-15 junction support

The corrected open L-frame uses no new chassis hole and preserves the X≥27/|L|≥41
vent/body-seat exclusion. XT60, three non-overlapping XT30 and two decision-seat gauges
are bed-connected and reachable; the mating, cable/R2, tool and removal sides remain
open. Attachment is by reversible clamp receivers/coupons. `DN01 OPEN` and `DN02 OPEN`
blanks remain removable gauges and choose neither fuse nor disconnect. Fixed post
shoulders were removed because the recovered coordinates overlapped connector gauges;
choosing replacements before S0/P1 would improperly freeze CAD-05-dependent geometry.

## 7. Visual review

All 19 final PNGs were inspected, including a grouped view for each CAD-01 cluster,
close-ups for every CAD-01 dummy, and every support/blank/clamp family. Render filenames
match their represented geometry. The inspection confirms:

- diagnostic IDs/arrows exist geometrically and the close-up views expose their faces;
- connector faces, cable exits, cooling/access cages and open removal sides are visible;
- corrected shelf lanes and junction seats do not overlap;
- ESP header rails, amp/tool cages, connector-bank access cages and junction seats are
  tied to their owner geometry rather than floating;
- no accidental donor, camera, deck, duct, antenna or production feature is visible;
- print orientation does not hide the intended fit evidence.

Some same-colour shaded text is faint in the raster renderer. Its mesh presence is
confirmed, but real legibility depends on nozzle/layer width and therefore remains a
mandatory slicer-preview check. The servo horn disc and clamp jaw/bridge also require an
unsupported-bridge/support decision in the slicer.

## 8. Parameter-manifest review

All 148 CSV rows have a unique ID and populated task, owner, value, unit, status, source,
uncertainty, physical-dependency and variant fields. Units are constrained to millimetres,
pixels or counts. Statuses distinguish confirmed/derived/expected/provisional/limits and
open dependencies rather than converting unknowns into facts.

Geometry directly references 140 row IDs. The eight deliberate context/policy/deferred
rows are `SH-STATIC-CLEARANCE`, `SH-MOVING-CLEARANCE`, `SH-D26-L-REAR`,
`SH-D26-L-FWD`, `SH-FLOOR-EDGE-L`, `SH-BAT-FREE-X`, `SH-BAT-FREE-L` and
`JUNC-POST-SHOULDER-D`; each remains traceable because it records a governing clearance,
measured but rejected feature, or intentionally deferred interface. There are no orphaned
blank/unknown rows.

## 9. P1 checklist and document review

The checklist covers each dummy and support for body/floor alignment, connectors,
cable bends/routes, mating-hand/tool access, insertion, removal, shell fit, D-26,
neighbours, serviceability, balance where applicable, and required photographs. Its
decision map explicitly handles narrow deck versus fallback A, battery-tray revision,
UBEC-shelf revision, junction-support revision and selection of the physical post height.
The corrected 95×50×30 battery cage, balance park and PS-15 shoulder deferral are present.

The implementation manifest now supplies every requested per-output field: part ID,
CAD task, related PS/component, dimensions, parameter source, status, output filename,
quantity, material, orientation, validation purpose and limitations. K, R, T, the
architecture README and `cad/README.md` agree with the generated set and explicitly state
that no TP, CAD-05 decision or production authorization has occurred.

## 10. Prohibited-scope audit

Source declarations, output names, feature metadata, manifests and renders contain no
CAD-03 production ESC mount, CAD-05 right deck, CAD-07 rod-sensitive final geometry,
camera/gimbal part, blower duct, production antenna mount, PS-10/11/14/17, production
body modification, production cable guide, physical-S0-dependent final geometry or
invented D-06 camera geometry. CAD-06 is post gauges only. CAD-08 decision blanks keep
DN-01/DN-02 open. No prohibited output required removal.

## 11. Findings and corrections

| ID | Severity | Affected part/file | Issue and evidence | Consequence | Correction | Final status |
|---|---|---|---|---|---|---|
| XCAD-01 | HIGH | CAD-04 shelf; `parts.py`, CSV | Recovered 40 mm shelf allowed only about 12 mm clear per lane while each dummy is 18 mm wide | P1 UBEC fit evidence would be invalid | Increased `SHELF-Y` to 42 mm and rebuilt two bed-connected 18 mm-clear lanes | **CLOSED**; bbox/visual/plate checks pass |
| XCAD-02 | HIGH | E1/E2, amp, connector bank, CAD-08; `parts.py` | Several header/access/seat fragments began above Z=0 or lacked owner ties in the recovered render/source | Slicer could produce loose fragments and access evidence could move independently | Added header ties, bed-connected access columns and bed-grounded junction frames | **CLOSED**; final visual and edge checks pass within documented Boolean limit |
| XCAD-03 | HIGH | Battery dummy; `parts.py` | Recovered bbox represented only a 95×45×25 arrangement instead of registered 95×50×30 installation envelope | Shell/restraint/strap fit could be falsely accepted | Added 50×30 restraint/strap cage and explicit `BAT-CABLE-D` cable path | **CLOSED**; final bbox 95×50×30 |
| XCAD-04 | HIGH | CAD-08 support; `parts.py` | Recovered XT30 gauges overlapped; cross rail entered the vent boundary; clamp/seat placement competed for space | Connector, vent and attachment validation was not trustworthy | Repositioned seats into a non-overlapping column, terminated rail at vent boundary, moved receivers and grounded seats | **CLOSED**; exact bbox/visual/plate checks pass |
| XCAD-05 | HIGH | CAD-08/CAD-06 interface; source, CSV, K/T/checklist/manifest | Fixed PS-15 shoulders overlapped diagnostic seats and prematurely selected an S0-dependent interface | Would hard-code blocked CAD-05/post geometry | Removed fixed shoulders, retained deferred parameter trace and moved placement check to P1; CAD-06 fit remains on PS-03 | **CLOSED**; no blocked geometry remains |
| XCAD-06 | MEDIUM | CAD-02 tray; source/CSV/checklist | Balance-lead park requested by K/checklist was absent; label extended bbox beyond nominal 50 mm | Incomplete cable-service test and bbox drift | Added open-top 4 mm park and label height constraint | **CLOSED**; final bbox 78×50×12 |
| XCAD-07 | MEDIUM | Manifest | Recovered narrative lacked one consolidated row per output with all required fields | Print quantities/material/status/limitations were not auditable output-by-output | Added 20-row per-output manifest and reconciled corrected bboxes/features | **CLOSED** |
| XCAD-08 | LOW | Validator | Plate validation checked size but not exact declared membership/count or overlap; render set was not exact-checked | A missing/duplicated/overlapping packed part could pass | Added triangle-multiset membership, count, XY overlap and exact 19-render-set checks | **CLOSED**; six plates pass |
| XCAD-09 | LOW | Render coverage; generator/renderer | Seven recovered renders did not show every CAD-01 dummy closely enough for label/feature review | Visual review was incomplete | Expanded deterministic set to 19 and added near-top camera support | **CLOSED**; all 19 inspected |
| XCAD-10 | EDITORIAL | Servo and reports | Servo top ID was hidden by horn disc; report prose still described representative renders/old shoulder state | Evidence could be misidentified or documentation could drift | Added `SRV TP` to disc and synchronized README, manifest, validator report, K/T and checklist language | **CLOSED** |

## 12. Print readiness and residual limitations

All 20 individual parts and six grouped layouts are source-complete and ready for
**Bambu Studio preflight**. Print only the P1-relevant diagnostic parts/plate after:

1. repair/union and global manifold inspection;
2. layer preview for minimum text/stroke width;
3. bridge/support inspection for the servo disc and clamp coupon;
4. confirmation that the selected material/profile is suitable; and
5. confirmation that the plate contains only the intended P1 subset.

No part requires another parametric source correction from this review. Physical S0,
D-06, D-08, D-09, D-10, D-24, DN-01, DN-02 and measured D-26 evidence can still require
the parameterized P1 revisions already identified in the checklist. Clamp coupons remain
unloaded diagnostic fit samples until physical plate-edge/pull-off evidence exists.

## 13. Final file effects

Created during this finalization: this report. The pre-existing recovered `cad/`
implementation remains an untracked review set relative to the checkpoint. Updated
during this skeptical pass: CSV parameters,
`parts.py`, `generate.py`, `validate.py`, `meshkit.py`, all three recovered reports,
`cad/README.md`, K, R, T and the architecture README handoff language. Generated STL/PNG files were
replaced deterministically and 12 additional render views were added. Removed from the
final tree: none. No donor STL or production file was modified, and no commit was made.
