# W17 Gate P1 diagnostic print preflight and print plan

Date: 2026-07-19  
Scope: diagnostic prints and physical evidence only  
Status: **PREFLIGHT INCOMPLETE — NO PRINT AUTHORIZATION — GATE P1 NOT PASSED**

This document selects the smallest useful diagnostic print sequence for Gate P1. It
does not redesign a part, authorize production CAD, close P1/P2, select the narrow
right deck, or activate fallback A. Physical acceptance remains controlled by
[`P1_dry_fit_checklist.md`](P1_dry_fit_checklist.md); authoritative datum and
measurement definitions remain in [`V_P0_geometry_measurement_results.md`](../../V_P0_geometry_measurement_results.md)
and [`D_measurement_plan.md`](../../D_measurement_plan.md).

## 1. Preflight verdict

**Do not send any diagnostic STL to the printer yet.** The deterministic CAD validator
passes, and Bambu Studio's CLI calls every individual input manifold, but the slicer
also reports floating-region/cantilever warnings on 15 of 20 individual STLs. Those
warnings must be located in layer Preview and either accepted as a controlled bridge,
supported without changing a measurement surface, or corrected at the source.

The minimum P1 evidence set ultimately needs all ten distinct CAD-01 dummies. The two
apparently duplicated pairs are not redundant: CTL-E1/E2 and UBEC-A/B must be present
simultaneously to prove neighbour clearance and independent removal. The support parts
should not all be printed up front; print them only after their matching dummies pass
the first bare-floor fit.

## 2. Bambu Studio and tool availability

| Tool/workflow | Result | What it proves / does not prove |
|---|---|---|
| Bambu Studio | Installed at `/Applications/BambuStudio.app`, version **02.07.01.62** | Correct local slicer is available for the documented X1 Carbon |
| Printer context | Bambu Lab **X1 Carbon**, 0.4 mm nozzle, 256 mm square bed, Textured PEI default | Confirmed by `CLAUDE.md` and `PRINT_SPEC.md`; no printer was invented |
| Bambu CLI | Installed binary documents `--info`, `--export-stl`, `--export-3mf`, `--export-settings`, `--slice`, profile loading and related options | Usable for import facts, screening slices and estimates; not a substitute for GUI layer inspection |
| Repository validator | `python3 10_assembly_architecture/cad/sources/validate.py` | Re-run: **PASS**, 20 individual STLs, 6 grouped layouts, deterministic regeneration |
| Boolean union | No separate Boolean engine found; Bambu export round-trip did not union a test file | One global Boolean-unioned solid is **not** established |
| Existing diagnostic project | No P1 `.3mf` project exists | Manual Bambu projects must be saved after the checks below |

### 2.1 Programmatic slicer facts completed

- `BambuStudio --info` reports `manifold = yes` for all 20 individual STLs.
- Each input is supplied as one STL file, but Bambu reports **61–775 internal parts**
  per individual file. These are disconnected/intersecting diagnostic primitives and
  text pixels, not permission to add that many copies. The GUI object-list count still
  requires a screenshot because the CLI does not expose the Prepare-pane hierarchy.
- The dependency-free validator found no boundary or orientation-mismatch edge, but it
  still exposes strict `>2` edge incidence at touching/intersecting primitives.
- A Bambu import/export round-trip of `cad01_ctl_e1.stl` preserved its 3,940 facets,
  327 Bambu-reported parts and 80 × 44 × 13 mm bounds. Therefore the round-trip did
  **not** repair/union the file into one connected volume.
- All 20 individual STLs completed a headless screening slice. Fifteen reported a
  floating-region or floating-cantilever warning; five did not: `cad01_aud_amp`,
  `cad01_pwr_bat_max`, and the H20/H26/H32 posts.
- Grouped plates 02, 03, 04 and 06 completed a screening slice. Plates 02–04 retain
  floating warnings; plate 06 does not.
- Grouped plates 01 and 05 failed at the CLI's default placement with “no object fully
  inside the print volume.” Their raw 228 × 74 and 227 × 73 mm bounds fit the nominal
  256 mm bed, but the monolithic grouped object cannot be trusted to auto-place around
  the X1C exclusion/placement constraints. Manually centre and preview it, or—preferred
  here—import its individual members.
- The six generated layouts remain free of XY bounding-box overlap according to the
  repository validator. This is geometric spacing evidence only, not a slicer collision,
  brim, calibration-zone or travel-path clearance result.
- The CLI result has no authoritative thin-wall/readability verdict. Thin walls and
  omitted text paths remain manual line-by-line Preview checks for every selected part.

### 2.2 Screening-slice settings and estimate limitation

The CLI estimates below used the installed X1 Carbon 0.4 mm machine definition,
Generic PLA or Generic PETG material basis, and an effective process recorded by the
result as **0.20 mm, 2 walls, 4 top / 3 bottom, 20% infill, supports off**. Bambu's
standalone CLI does not fully resolve every inherited preset field from the named JSON;
the effective values, not the preset filename, are the evidence.

Times and grams are therefore **screening estimates**, normally low for the recommended
3/4-wall profiles below. Re-slice and record the GUI estimate after the final profile,
support painting, brim and actual spool preset are applied.

## 3. Per-part slicer screening and disposition

`Bridge` means bridge toolpaths were generated. `WARN` is a Bambu floating-region or
cantilever warning. Time/grams use the screening profile in §2.2.

| STL | Bambu internal parts | Time | g | Screening result | P1 disposition |
|---|---:|---:|---:|---|---|
| `cad01_aud_amp.stl` | 264 | 3.3 min | 0.78 | bridge 0 s; no warning; smallest scaled label stroke is about 0.21 mm | **PRINT NOW**, first PLA text/access coupon |
| `cad01_pwr_ubec_a.stl` | 201 | 8.7 min | 2.85 | WARN floating region; cooling-cage top bridges | **PRINT NOW**, first PLA cage/stub coupon |
| `cad02_ps01_plate_clamp_foot.stl` | 63 | 5.5 min | 0.97 | WARN floating cantilever; jaw roof is an ~11.8 mm cantilever above the 4.4 mm gap | **PRINT NOW**, first PETG clamp/plate coupon; supports off initially |
| `cad06_ps05_post_h20.stl` | 123 | 10.1 min | 1.85 | bridge 11 s; no warning; 3.4 mm M3 passage | **PRINT NOW**, PETG M3/text/shoulder/height coupon |
| `cad08_ps15_dn_open_blanks.stl` | 266 | 2.0 min | 0.79 | WARN floating regions; label paths require preview | **PRINT NOW**, PETG text/thin blank/handling coupon |
| `cad01_pwr_bat_max.stl` | 352 | 35.4 min | 17.74 | bridge 33 s; no warning | **PRINT NOW after coupons pass** |
| `cad01_drv_esc.stl` | 297 | 25.1 min | 10.00 | WARN floating regions; 30 mm fan/cooling cage is bridge-critical | **PRINT NOW after coupons pass** |
| `cad01_pwr_ubec_b.stl` | 203 | 8.7 min | 2.85 | WARN floating region; same process risk as A | **PRINT NOW after UBEC-A coupon passes** |
| `cad01_ctl_e1.stl` | 327 | 18.0 min | 8.71 | WARN floating regions; USB bend cage | **PRINT NOW after coupons pass** |
| `cad01_ctl_e2.stl` | 331 | 18.0 min | 8.71 | WARN floating regions; USB bend cage | **PRINT NOW after coupons pass** |
| `cad01_vid_wifi_max.stl` | 775 | 21.7 min | 9.56 | WARN floating regions; heatsink/cooling cage; some connector text is sub-line-width | **PRINT NOW after coupons pass** |
| `cad01_srv_steer.stl` | 302 | 23.6 min | 10.37 | WARN floating cantilever; 116 s bridge time at horn disc | **PRINT NOW only after servo-disc Preview is cleared** |
| `cad01_ps15_connector_bank.stl` | 481 | 32.3 min | 12.47 | WARN floating cantilever; hand/wire/tool cage top rails | **PRINT NOW only after cage Preview is cleared** |
| `cad02_ps01_battery_tray.stl` | 357 | 13.7 min | 5.02 | WARN floating regions; strap walls/receiver/ballast detail need layer check | **PRINT AFTER FIRST BATTERY FIT** |
| `cad04_ps03_ubec_shelf.stl` | 289 | 16.0 min | 5.23 | WARN floating regions; open frame, M3 ear, receivers and labels need layer check | **PRINT AFTER UBEC DUMMY FIT** |
| `cad08_ps15_junction_support.stl` | 421 | 18.9 min | 6.16 | WARN floating cantilever; connector seats/receivers need layer check | **PRINT AFTER CONNECTOR-BANK DUMMY FIT** |
| `cad06_ps05_post_h26.stl` | 120 | 12.8 min | 2.24 | bridge 11 s; no warning | **PRINT AFTER FIRST FIT only if H20 is too low** |
| `cad06_ps05_post_h32.stl` | 119 | 15.5 min | 2.63 | bridge 12 s; no warning; closest to D-26 policy limit | **DO NOT PRINT YET**; only if H20 and H26 fail for low-layer access and H32 still has ≥8 mm moving clearance |
| `cad04_ps03_plate_clamp_foot.stl` | 68 | 5.5 min | 0.97 | same jaw/key geometry as PS-01; label differs; WARN | **DO NOT PRINT YET**; reuse first generic key test, then print required quantity |
| `cad08_ps15_plate_clamp_foot.stl` | 61 | 5.5 min | 0.97 | same jaw/key geometry as PS-01; label differs; WARN | **DO NOT PRINT YET**; reuse first generic key test, then print required quantity |

The ten CAD-01 dummies total about **84 g and 3 h 15 min** when their individual
screening estimates are summed. A final arranged plate can be faster, but that saving
does not justify combining high-risk bridges before the coupons have passed.

## 4. Minimum print set and why each item remains

### PRINT NOW — conditional on manual Bambu clearance

1. Process coupons: AUD-AMP, UBEC-A, one PS-01 clamp foot, H20 post and DN-open blanks.
2. After those pass, complete the ten-dummy set with battery, ESC, UBEC-B, CTL-E1,
   CTL-E2, Wi-Fi maximum, servo/KO-19 and connector-bank dummy.

No dummy in the resulting ten-part set is a spare:

| Evidence question | Minimum physical representative |
|---|---|
| Battery envelope, installation path, XT60 and 20 mm bend | battery maximum dummy |
| ESC allocation, fan gap and forward/aft exits | ESC dummy |
| Two UBEC lanes and independent lift/lead paths | UBEC-A **and** UBEC-B simultaneously |
| Two controllers, occupied USB plugs and neighbour access | CTL-E1 **and** CTL-E2 simultaneously |
| Right-deck heat/height maximum and CN-16/coax routes | Wi-Fi maximum dummy |
| Amplifier neighbour/tool/access assumption | amplifier dummy |
| Steering/D-26/KO-19 stand-in | servo dummy; physical D-26 measurement remains authoritative |
| Junction allocation and mating-hand/tool/extraction clearance | connector-bank dummy |

### PRINT AFTER FIRST FIT

- Battery dummy passes bare-floor fit → battery tray plus **one additional** PS-01
  clamp foot; reuse the first coupon so the tray has two feet without printing three.
- UBEC pair passes bare-floor/lane study → UBEC shelf. Use the first clamp coupon to
  test its identical key sequentially; print a shelf-labelled foot only when the final
  diagnostic attachment quantity is known.
- Connector-bank dummy passes Z2R access study → junction support. Reuse the first
  clamp coupon sequentially and the already printed DN blanks.
- H20 fails because the mock plane is too low for lower-layer leads/service, while
  shell and D-26 margin permit a rise → H26. Print H32 only after the H26 result proves
  why it is needed.

### DO NOT PRINT YET

- The full generated plate 05: it duplicates four clamp feet and the DN blanks, and
  failed headless default placement.
- The full generated plate 06: H20 is the lowest credible plane and decides whether a
  higher gauge is necessary.
- Extra PS-03/PS-15 clamp feet before the generic 4.4 mm jaw/key coupon passes.
- Any CAD-03/05/07 or production geometry; it is absent/gated for good reason.
- ASA versions of diagnostic dummies/supports. No P1 evidence justifies the added time,
  warp and fume burden.

### OPTIONAL

- A second generic clamp coupon only if a simultaneous two-edge unloaded pull-off test
  is desired before the tray print.
- A second H20 post if a physical mock deck cannot otherwise be held level; a rigid
  straightedge or temporary flat card at the measured plane is preferred.
- A re-sliced individual dummy as a process retest after a bridge/profile change. Do
  not print an entire grouped plate merely to retest one bridge.

## 5. Staged build-plate plan

Do not mix PLA and PETG on one run. “Plate A” is intentionally two material-specific
subplates.

| Plate | Included individual STLs | Material | Diagnostic value | Dependency and next check |
|---|---|---|---|---|
| **P1-A-PLA** | AUD-AMP + UBEC-A | regular/matte PLA | Worst scaled ID text; small stubs; open access cage; UBEC 30 mm cooling-cage bridge | Manual Preview first. Require readable IDs, intact stubs and bridge with no detached strand before any larger PLA plate |
| **P1-A-PETG** | one PS-01 clamp + H20 + DN blanks | PETG HF | 4.4 mm jaw/4 mm plate, clamp bridge/flex, M3 passage, shoulder key, H20, PETG text and thin blank robustness | Dry PETG if needed. Measure before deburring. Fail stops all support printing |
| **P1-B1 power** | battery + ESC + UBEC-B; reuse UBEC-A | PLA | Battery/XT60/bend, ESC/fan/exits, simultaneous UBEC pair | P1-A pass. Before B2: bare-floor battery/ESC/UBEC fit and first S0/D-26 observations |
| **P1-B2 deck cluster** | CTL-E1 + CTL-E2 + Wi-Fi maximum; reuse AUD-AMP | PLA | Complete minimum right-deck/fallback-A dummy cluster | S0 measured; Preview clears USB/cooling cages. Check H20 mock plane before B3/supports |
| **P1-B3 access** | servo + connector-bank | PLA | Steering conflict aid and junction mating-hand/tool/extraction allocation | Servo disc and connector cage require critical-layer screenshots before print |
| **P1-C1 tray** | tray + one new PS-01 clamp; reuse first clamp | PETG | Tray station, strap slot, balance park, two-foot attachment | Battery dummy bare-floor fit and first clamp coupon pass |
| **P1-C2 lower supports** | UBEC shelf + junction support; reuse coupon/blanks sequentially | PETG | Lanes/free feature/airflow/post shoulders plus vent-safe junction seats/access | Corresponding dummies pass; final D-27 occupancy photographed |
| **P1-C3 height escalation** | H26 only, then H32 only if required | PETG | Lowest passing post-height search | H20/H26 recorded failure reason; physical D-26 and shell gaps available |

Generated plate 02 is useful only if AUD-AMP has not already been coupon-printed;
generated plate 03 is a rational B3 group after both warning regions pass Preview.
Generated plates 01/04/05/06 are less efficient than the staged individual imports
because they force duplicates, premature variants, or default-placement correction.

## 6. Material and profile recommendations

These are starting values for diagnostic evidence, not new repository-wide defaults.
Use the actual installed-spool preset for temperature. Save the exact `.3mf` and record
the final settings in the TP record when printing begins.

| Group | Material | Orientation | Nozzle / layer | Walls; top/bottom; infill | Supports / brim | Dimensional controls | Speed, seam and priority |
|---|---|---|---|---|---|---|---|
| P1-A-PLA | ordinary PLA, not specialty/silk | Amp mount allowance flat; UBEC mount allowance flat with cooling cage up | 0.4 / 0.20 mm | 3; 4/4; 15% gyroid | Support off for first comparison; 3 mm brim only if UBEC cage footprint lifts | Elephant-foot 0.15 mm; XY-hole N/A; minimum feature generator **on only if Preview proves it preserves rather than invents text** | Standard speeds; bridge ≤25 mm/s; seam on non-access outside wall; text/bridge quality over speed |
| P1-B dummies | ordinary PLA | Keep manifest source orientation: DAT-F/base/board/flange faces down; cages, cooling volumes and servo disc up | 0.4 / 0.20 mm | 3; 4/4; 10–15% gyroid | No global support. Paint only beneath accepted cage roofs/disc areas; 3 mm brim on servo/tall narrow cages, otherwise off | Elephant-foot 0.15 mm; hole compensation 0.00; preserve registered outer envelope | Outer wall ≤100 mm/s and bridge ≤25 mm/s for first set; align seam away from connector stubs and measured faces |
| P1-A-PETG | PETG HF, dry if spool sat out/stringing | Clamp bottom jaw face down; post DAT-F end/flag down; DN blanks flat | 0.4 / 0.20 mm | 4; 5/5; 40% gyroid, matching `PRINT_SPEC.md` coupon rule | Clamp: **support off** so jaw sag is measured; 3 mm outer brim, no brim inside jaw/hole. H20/blanks: support off | Elephant-foot 0.15 mm; M3/hole compensation **0.00 first pass**; record actual 3.4 mm passage and 4.4 mm jaw before tuning | Strength/quality; outer/inner ≤150 mm/s, bridge 20–25 mm/s; clamp seam on closed back, never jaw/key face |
| P1-C supports | PETG HF | Tray/shelf/junction DAT-F open frame down; posts DAT-F end down; do not auto-orient away from gauge datum | 0.4 / 0.20 mm | 3 walls for tray/open frames; 4 at clamp/load coupons; 5/5; 25–40% gyroid | Support only where Preview shows a true island and removal leaves the gauge surface intact. 3 mm brim for clamp/post; large tray/shelf/support off unless corners lift | Elephant-foot 0.15 mm; hole compensation starts 0.00 and changes only from H20 coupon; record value. No scaling | Strength-oriented, ≤150 mm/s walls; slow small perimeters; seam outside pockets, M3 ear, strap slot, clamp receiver and lead combs |

PLA is appropriate for rigid envelopes that will not live in the car. PETG is required
for clamp feet and support/interface tests where limited flex and plate contact matter.
ASA adds no useful P1 evidence; reserve it for later heat/exposure-driven production
decisions. PETG can bond aggressively to smooth plates, so use the documented Textured
PEI default or the correct release layer for the selected plate.

### 6.1 Minimum line width and text

The source uses a 0.65 mm bitmap cell with a nominal pixel stroke of about 0.56 mm,
but labels are scaled to fit small faces. The narrowest identified scaled stroke is
about **0.21 mm** on `AUD-AMP TP`; several access labels are also below a normal 0.4 mm
nozzle line. Therefore:

1. Preview the top label layers in line-type view at maximum zoom.
2. Pass only if the complete mandatory part ID and critical `UNCONFIRMED`/height/rail
   text have continuous extrusion paths. Connector captions may be secondary only when
   their arrow/stub remains unambiguous in the P1 photo.
3. If a mandatory ID is missing, **stop and revise the label geometry only**; do not
   claim the part is evidence-identifiable and do not compensate by handwriting before
   the original slicer failure is recorded.

## 7. Exact Bambu Studio import and Preview checklist

Perform this for every staged plate and save the project as
`P1_<plate>_X1C_0p4_<material>.3mf`.

- [ ] Select Bambu Lab X1 Carbon, 0.4 mm nozzle and the actual plate type.
- [ ] Import the listed **individual** STL once each; record the object-list count. Do
  not split to objects or auto-arrange until the original import state is screenshotted.
- [ ] Record any repair banner/icon and the before/after object name, bounds and volume.
  A repair is not accepted merely because the dialog says success.
- [ ] Confirm the expected bounds from `generated_part_validation.md`; fail if repair
  changes any registered outer dimension by more than 0.2 mm or deletes a stub/label.
- [ ] Confirm every intended object is on the bed, outside the 18 × 28 mm X1C exclusion
  area, outside calibration/prime regions, and wholly inside the printable boundary.
- [ ] Confirm objects and their brim/skirt do not overlap; retain at least the generated
  6 mm part gap unless the final brim needs more.
- [ ] Keep source orientation initially. Inspect first-layer coverage, bed contact and
  whether elephant-foot compensation changes a gauge edge.
- [ ] Scrub every layer. Search for first appearance of a disconnected island, not only
  red overhang colour. Any extrusion that begins in air is a stop.
- [ ] In line-type view, inspect Bridge and Overhang on: UBEC/ESC/Wi-Fi cooling-cage
  roofs, CTL USB bend cages, servo horn disc, connector-bank cages, clamp jaw roof,
  tray receivers/ballast land, support connector seats and DN labels.
- [ ] Use paint-on support only after identifying the exact region. Confirm support is
  removable without cutting a registered envelope, jaw, M3 passage, strap slot,
  connector stub, hand cage or mating surface.
- [ ] Inspect wall paths: 1.2 mm shell walls should resolve as approximately three
  nominal 0.4 mm lines; 1.8/2.0/2.2 mm ribs and walls must not collapse to one line.
- [ ] Inspect all mandatory IDs and arrows. Confirm no text is replaced by isolated
  dots that will detach.
- [ ] Check seam placement away from holes, clamp/key faces, strap slots, lead combs,
  connector stubs and measured exterior corners.
- [ ] Record final time and grams using the actual spool preset, wall count, supports
  and brim. The §3 estimates are not the final TP record.
- [ ] Save screenshots listed in §10 before printing. Watch the entire first layer.

## 8. Coupon plan and reprint logic

| Risk | Cheapest valid coupon | Measure | Pass | Failure response |
|---|---|---|---|---|
| PLA text/minimum line | AUD-AMP | mandatory ID continuity and naked-eye/photo readability | ID unambiguous; no loose text pixels | Revise label scale/placement or validated slicer feature mode; revalidate/reprint amp only |
| PLA bridge/stub | UBEC-A | cooling-cage roof sag; lead stub survival | cage retains registered max envelope; stubs survive 3 handling cycles | Tune bridge/reorient/support only if removal preserves envelope; do not print UBEC-B/ESC/Wi-Fi yet |
| M3 clearance | H20 3.4 mm through passage with the actual intended M3 screw and driver | entry/exit diameter, insertion and driver access | screw passes without cracking/forced threading; original hole recorded | Keep source nominal; adjust documented slicer hole compensation from measured result and reprint H20 before supports |
| Clamp flex/plate thickness | one PS-01 foot on each candidate 4 mm plate edge/chamfer | plate thickness, jaw gap, three cycles, unloaded pull-off, whitening/set/marring | installs/removes three times; stays seated under hand handling; no crack, permanent set, gouge or delamination | Stop all clamp-supported parts; record bridge sag and edge geometry; reorient/process-revise or parameter-revise coupon only |
| Strap slot | full tray after battery fit; a separate source coupon is not justified for this small 5 g part | actual strap width/thickness, as-printed 22 mm opening, edge condition | 20 mm strap passes freely without abrasion or pinching | Record before trimming; revise slot/process only, reprint tray before load |
| DN text/thin blank | DN-open blanks | both labels, flatness and three insert/remove handling cycles | both `OPEN` decisions remain legible; no curl/crack | Keep decisions open; reprint blank/profile before junction-support evidence |
| Connector-stub robustness | UBEC-A first; then each unique dummy | three normal handling cycles, no deliberate abuse | stub remains attached and dimensionally useful | Revise only failed stub attachment/process before printing the matching group |

Do not drill, sand, heat-form or trim a failed coupon until its original dimensions and
photos are recorded. Such cleanup may make a later assembly aid, but it cannot convert
the original diagnostic result to PASS.

## 9. Physical measurement sequence to combine with P1

This sequence cross-references Report V; it does not redefine it. Record millimetres
unless the authoritative row says otherwise.

| Seq. | Measurement and exact setup | Reference/tool | Required result and photos | Decision affected |
|---:|---|---|---|---|
| 1 | **D-06 camera calipers**, unpowered on an ESD-safe bench before chassis work | Real SSC338Q+IMX335; calipers ±0.2 mm. Measure PCB W/H/thickness, heatsink, lens Ø/protrusion, total depth, lens X/Y offset, hole Ø/centre spacing, connector/cable exit and service pull | One labelled table plus front/back/each edge and caliper-on-feature photos. D-06b only after Wi-Fi possession is confirmed | Gate C inputs; camera mount/duct/placement. No camera dummy is authorized before this |
| 2 | Assemble floor to **ASM-05** without forcing it flat | DAT-F top; verified flat glass/reference surface, straightedge and feeler gauges | Longitudinal centre/both outboard and transverse front/joint/rear gaps; top and low side-light photos. Report range, do not average a twisted floor | DAT-F physical confirmation and all support seating |
| 3 | Measure **screw-head protrusion** before adding dummies | Straightedge on clean DAT-F + feeler/depth gauge, ±0.1 mm; every head inside PS-01/03/15 footprints and splice | Coordinate/owner/head type/protrusion table; macro at maximum and each support footprint | Tray ribs, shelf/support seating, reprint/fastener response |
| 4 | Resolve **driver-side physical naming** with car pointing +X and observer behind it | Belt/spur side versus physical driver-left/right; architecture-RIGHT remains L<0 regardless | One annotated top photo with +X arrow, belt, physical left/right and `architecture RIGHT = L<0`; one-line mapping | Prevents mirrored placement/report errors only; does not alter coordinates |
| 5 | Complete **D-27 final fastener occupancy** at the assembled mechanical state | Report V 35 part rows/33 unique coordinates; 2 mm driver, inspection light/mirror | Mark every position `donor-occupied`, `free`, `shareable only with approval`, or `prohibited`; photograph four floor quadrants with IDs | Clamp/shared-screw/free-single attachment strategy |
| 6 | Dry-seat the complete body normally and locate its **three body screw landing points** without forcing a screw | One nose→front-floor and two front-floor→front-body interfaces from Report A; ruler/calipers | Coordinate/landing boss/head/driver-path/engagement notes; underside, top and side photos | Shell registration, access and S0 confidence |
| 7 | Pin **S0** with the body fully seated by its real landing geometry, not held by hand | DAT-F top to DAT-S shell bottom edge; depth gauge/feeler/calipers at front/rear on both sides | Four or more readings and range, side photos with scale. If readings differ >1 mm, record non-planarity; do not average it away | Highest-value right-deck versus fallback-A input; absolute D-02 clearances |
| 8 | Perform **nose vertical dry-fit** in the same registered shell/floor state | Nose rear ring, beam top and DAT-F; caliper/depth gauge at three Report-V stations | Actual vertical offsets versus V's ±2 mm slicer estimate; side/profile and rear-ring photos | Confirms D-25 vertical map; does not reopen the protected-volume finding by itself |
| 9 | Complete **ASM-08 / D-26** after steering servo centring and linkage closure; chassis at ride height, then relevant bump state | DAT-F to rod/joint lower and upper bounds at S1 X≈−30, S2 X≈+45, S3 X≈+125; rule/calipers ±2 mm | Centre/left-lock/right-lock readings, lateral sweep, minimum neighbour gaps, three rule-in-frame photos plus lock-to-lock video | KO-01 physical band, battery overhead, X1 route, post/deck boundary and H32 rejection |
| 10 | Execute dummy and support rows in `P1_dry_fit_checklist.md` in plate order | 5 mm static, 8 mm moving, 10 mm ESC-fan gauges; calipers/ruler/stopwatch | PASS/FAIL/N/A, measured gap, removal time where requested and exact photo names for every applicable cell | Named tray/shelf/junction/post revisions and later architecture review |

For the H20/H26/H32 study, place a rigid temporary flat card/straightedge on the post
top as a mock plane; verify its height from DAT-F with calipers. It is a gauge, not a
CAD-05 deck. Select the lowest height that passes shell, D-26 and lower-layer service
checks; a higher post is not “better.”

## 10. Required slicer screenshots and physical photo evidence

### 10.1 For each Bambu project

1. Prepare view: object list, printer/nozzle, plate, actual filament and process visible.
2. Imported-model status: any repair warning/icon and the unmodified bounds.
3. First-layer Preview: every object's contact patch, brim/skirt and exclusion areas.
4. Critical bridge/island layer in line-type view, with the affected object named.
5. Highest text layer close-up showing mandatory IDs/arrows as extrusion paths.
6. Final whole-plate Preview showing no overlap/collision and the final time/grams.
7. For P1-B3, separate close-ups of the first servo-disc layer and connector-cage roofs.
8. For P1-A-PETG, separate close-up of the clamp jaw bridge and H20 M3 opening.

Save the `.3mf` plus screenshots using `P1_<plate>_<view>_<pass-or-fail>` stems. If the
user cannot supply the project, also export the final settings JSON and record every
manual override. A G-code file alone is insufficient because it hides object/repair
history.

### 10.2 Physical evidence minimum

- Coupon: top, side, underside/first layer, scale, label close-up and failure close-up.
- Clamp: actual plate cross-section, key/receiver engagement, pull direction, edge
  before/after and three-cycle result.
- Every dummy/support: top, side, connector/access, removal direction and shell-seated
  view, with a ruler and visible part ID/arrow.
- Battery: XT60, bend, strap, balance park, four-corner scale and top-only removal.
- UBEC pair/shelf: both lanes, both lead ends, independent lift, cooling gap, free M3
  feature and clamp.
- Deck cluster: each controller USB, Wi-Fi `UNCONFIRMED` label/pigtails/cooling, amp
  tool access, neighbour gaps and each tested mock-plane height.
- Junction: all connector faces, fingers, driver, R2, extraction/removal, vent notch,
  DN blanks seated/removed and body-on reach gauge.
- Steering: centre and both locks, real rod rule, servo dummy/battery gap and shell view.

Physical photo names follow the authoritative checklist pattern
`P1_<item>_<view>_<pass-or-fail>.jpg`.

## 11. Pass/fail criteria

### 11.1 Slicer pass

- Expected one imported object per selected STL and expected plate membership.
- Bambu manifold status has no unresolved repair; any repair preserves registered
  dimensions within 0.2 mm and all diagnostic features.
- No extrusion starts unsupported. Every flagged bridge either previews as a continuous
  bridge within the profile's capability or has removable, explicitly inspected support.
- Mandatory IDs/arrows/`UNCONFIRMED`/rail/height labels have continuous printable paths.
- No thin wall collapses below two continuous paths where geometry requires a wall;
  the 1.2 mm dummy shell resolves consistently.
- No object, skirt, brim or calibration path overlaps another object or leaves the
  printable area.
- Final time/grams, material, orientation, support, brim, seam, elephant-foot and hole
  compensation are recorded in the saved project/TP record.

### 11.2 Printed coupon/part pass

- Outer diagnostic dimensions meet the manifest's ±0.5 mm part tolerance unless an
  authoritative feature has a tighter stated criterion.
- M3: the intended screw passes the original 3.4 mm coupon without crack or forced
  thread; driver access remains usable.
- Clamp: fits the actual measured plate/chamfer three times, remains seated for unloaded
  hand handling, releases intentionally and causes no whitening, permanent set, gouge
  or delamination. No dynamic-retention claim is made.
- Strap: actual 20 mm strap passes the as-printed 22 mm opening without pinch/abrasion.
- Text is unambiguous in the required evidence photo without a handwritten substitute.
- Connector/cable stubs and cages survive three normal handling cycles and remain true
  enough to represent their registered envelope.
- Part-specific physical clearance: ≥5 mm static, ≥8 mm moving, ≥10 mm over ESC fan;
  insertion/removal/tool paths meet the exact P1 checklist.
- Supports seat without rocking on screw heads/interruptions, do not consume prohibited
  D-27 occupancy and stay clear of the physical D-26 band.

P1 closes only when every applicable checklist cell has PASS/FAIL/N/A, measured gaps
and named photos. A successful print is not a Gate P1 pass.

## 12. Stop, revision and reprint conditions

Stop before printing when any of the following occurs:

- Bambu shows a floating region/cantilever and its first layer in air has not been
  identified and resolved.
- A repair changes a registered bound >0.2 mm, deletes text/stubs, changes intended
  membership, or produces an unexplained extra object.
- A mandatory ID or arrow has no continuous toolpath, or a 1.2/1.8/2.0/2.2 mm wall/rib
  disappears in Preview.
- Servo disc, cooling cage or connector cage begins as an unsupported island. Global
  support is not an automatic cure if removal would damage the diagnostic envelope.
- Clamp bridge droops into the 4.4 mm jaw or support fills/scars the gauge gap.
- Grouped plate 01 or 05 remains outside the printable area after manual placement,
  including brim/skirt/calibration exclusion. Use individual imports; do not scale.
- Objects/brims overlap or the first layer has inadequate contact.

Stop the physical sequence and revise/reprint only the affected parameterized part when:

- a coupon fails M3, jaw/key, text, bridge, plate-thickness or stub handling;
- a part is >0.5 mm from its diagnostic bounds before cleanup;
- elephant foot closes a hole, key or slot; first reprint with the measured compensation,
  not a source-scale change;
- battery/XT60/strap/bend, shelf lane/lead, junction hand/tool/extraction or post-height
  evidence fails;
- support removal alters a measurement surface;
- actual hardware measurement exceeds or contradicts an expected/provisional dummy.

Keep the failed part and original photos. Regenerate with the named parameter/feature,
run `validate.py`, repeat Bambu Preview, then reprint only that item. Do not trim a
failure into a PASS and do not reprint unaffected duplicates.

## 13. Architecture decisions unlocked by evidence

| Result | Decision input unlocked | What it does **not** unlock |
|---|---|---|
| S0 + H20 complete CTL-E1/E2/amp/Wi-Fi cluster, with shell/D-26/service gaps | Evidence to continue the narrow inboard right-deck review when S0 is about ≥6 mm and all policy clearances pass | CAD-05 or production authorization |
| S0/cluster below Report V trigger or H20 cluster cannot install/remove with policy clearance | Evidence to return to the architecture decision process for fallback A | Automatic fallback-A declaration or ESP32 airbox fallback (already geometrically dead) |
| Battery dummy + tray + two clamps + balance observation | Battery envelope/purchase input, PS-01 station/strap/attachment parameter decision | Final battery retention or D-21 balance closure |
| UBEC pair + shelf + free-feature/clamp evidence | PS-03 lane/origin/attachment decision; later D-24 may still resize | Production UBEC shelf before P7 |
| Generic clamp coupon | Whether plate-clamp feet remain a credible no-new-hole diagnostic strategy | Dynamic retention/load rating |
| Connector-bank dummy + junction support + DN blanks | PS-15 seat/access/notch/attachment revision inputs and future post-shoulder candidate region | DN-01/DN-02 owner decisions or final fuse rating |
| H20, then only necessary higher gauges | Lowest passing diagnostic post height for later review | Deck outline or production post |
| Servo dummy + physical ASM-08 D-26 | Battery overhead, KO-01, X1 crossing and right-deck inboard boundary | Replacement for the real powered lock-to-lock measurement |
| ESC dummy | Provisional Z5R packaging/fan/exits evidence | CAD-03 before D-08 and Gate A |
| D-06 camera calipers | Gate C dimensional input | Camera CAD, FOV/boresight or duct authorization by itself |

## 14. Session close-out state

- Bambu Studio is available and a documented CLI workflow is usable.
- Geometry/import/screening slices were completed programmatically; GUI Preview and
  screenshots remain mandatory.
- The minimum staged set avoids duplicate controllers/UBECs only where simultaneous
  evidence would be lost; it avoids duplicate clamps, premature post heights and the
  oversized all-support grouped plate.
- No part has been printed, no physical measurement has been claimed, no gate has been
  passed and no production CAD has been authorized.
