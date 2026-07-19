# W17 P0 diagnostic-CAD implementation manifest

`(CAD-01/P0-CAD)` · diagnostic fit and access gauges only · **not production geometry**.

## Repository and method

The implementation was made at checkpoint
`794bcf7 docs: establish W17 assembly architecture and P0 geometry evidence` after the
required clean-tree gate passed. The repository had no tracked CAD source and no locally
installed OpenSCAD, FreeCAD, Blender, mesh Boolean engine, NumPy or trimesh. It did have
a reviewed dependency-free Python STL/evidence convention under `evidence/scripts/`.
The selected method is therefore deterministic, dependency-free Python geometry in
millimetres, controlled by one CSV parameter manifest.

## Authority and scope

Implemented:

- CAD-01 / PS-13 diagnostic installation-envelope dummy set;
- CAD-02 / PS-01 diagnostic battery tray and reversible plate-clamp coupon;
- CAD-04 / PS-03 diagnostic UBEC shelf and reversible plate-clamp coupon;
- CAD-06 / PS-05 replaceable 20/26/32 mm post family;
- CAD-08 / PS-15 diagnostic junction support, open-decision blanks and plate-clamp coupon.

Intentionally absent: CAD-03, CAD-05, CAD-07, camera/gimbal geometry, blower duct,
antenna mount, PS-10, PS-11, PS-14, PS-17, production cable guides, body modifications,
production harness retention, physical-S0-dependent geometry and D-06-dependent geometry.
No camera dummy was made. The ESP32 airbox fallback was not made. No right deck was made.

## Parameter authority

[`cad_parameters.csv`](../parameters/cad_parameters.csv) contains 148 rows with the
required task, part, value, unit, status, source, uncertainty, physical dependency and
selected diagnostic variant fields. It directly cross-references:

- DAT-F at Z=0;
- D-26 at Z 35–62 mm and its rear/forward lateral bands;
- the one right-side free feature at X -39.99, L -32.86;
- the mirror battery-side free feature at X -39.94, L +17.14;
- the approximately 78 mm battery span;
- the ±68.5 mm wide-floor edges;
- every component body, connector, bend, cooling and access parameter used by CAD-01;
- all diagnostic support dimensions and every unresolved physical dependency.

The battery-side free feature is recorded but not consumed by a tray ear: its L=+17.14
centre is too close to the KO-19 policy boundary for a useful diagnostic pad. CAD-02
instead tests two reversible outboard plate clamps. CAD-04 uses the verified right-side
single plus one reversible clamp. CAD-08 uses reversible clamps because the Z2R patch
contains no free M3 feature.

## CAD-01 dummy set

| Dummy | Variant/status | Installation-envelope content |
|---|---|---|
| PWR-BAT | 75 × 45 × 25 maximum body inside the registered 95 × 50 × 30 installation envelope; no invented min/expected pack | open body shell, 50 × 30 restraint/strap cage, forward XT60 inside the documented 20 mm allowance, cable/bend cage, orientation arrow and labelled balance-test mass pocket |
| DRV-ESC | expected/unmeasured body | body, mounting flange, forward XT60, three aft phase exits, bend allowance, Ø30 × 8 fan, 10 mm cooling cage, airflow and forward arrows |
| PWR-UBEC-A | expected/unmeasured | separate Rail A label, body, input/output leads and bends, mounting allowance, cooling cage and orientation arrow |
| PWR-UBEC-B | expected/unmeasured | separate Rail B label, body, input/output leads and bends, mounting allowance, cooling cage and orientation arrow |
| CTL-E1 | expected/unmeasured | body, 44 mm pin-header envelope, permanently occupied USB plug, 15 mm bend cage, USB access marking, standoff allowance and arrow |
| CTL-E2 | expected/unmeasured | same service envelope, separately identified |
| VID-WIFI | only the authorized P9 maximum 60 × 32 × 12 | explicitly embossed `UNCONFIRMED ENVELOPE`, two aft pigtails, power exit, CN-16 boundary, cable bends, confirmed 28 × 28 × 3 heatsink and 5 mm cooling cage |
| AUD-AMP | expected/unmeasured | body, I2S and speaker exits, bends, mount allowance, adjustment/tool-access cage and arrow |
| SRV-STEER | expected/unmeasured KO-19 stand-in | body, lead/bend and maximum horn-sweep disc; never a mount |
| PS-15 connector bank | expected diagnostic allocation | body, XT60 and three XT30 allowances, mating-hand cage, extraction/wire-bend cage, tool access and mating/removal arrows |

The envelope register does not authorize numeric minimum/expected Wi-Fi variants beyond
the P9 maximum, so only that maximum is generated. Likewise, only the confirmed battery
maximum is generated. This avoids inventing ranges and avoids printing redundant sizes.

## CAD-02 battery tray

The tray is an open 78 mm longitudinal gauge with a 50 mm lateral allocation, DAT-F
open ribs, 12 mm diagnostic side restraint, an open forward insertion/XT60 face, 20 mm
strap passages, an open-top balance-lead park and a labelled outboard 5 g ballast land. The open floor exposes screw
heads and interruptions during P1. It uses two removable clamp-foot receivers at the
outboard ±68.5 mm plate edge and adds no chassis hole. Its 12 mm maximum geometry stays
below D-26 Z=35 mm; the 25 mm battery dummy separately tests the real pack height.

## CAD-04 UBEC shelf

The 70 × 42 mm open shelf is placed from assembly origin X=-57.5, L=-68.0, Z=DAT-F.
Two laterally separated 18 mm-clear, open-ended Rail A/B lanes accept the full
54 × 18 × 15 installation dummies while locating their 30 × 14 × 10 bodies;
lead combs exist at both ends, the floor is open for airflow, and all parts lift upward.
It combines the verified X=-39.99/L=-32.86 M3 candidate with one reversible outboard
clamp receiver and includes two replaceable-post shoulders. Solid geometry reaches only
Z=12 mm against the Z=14 diagnostic cap, wholly below D-26.

## CAD-06 post family

Three rational P4 samples are generated: 20 mm (V's narrow-deck credible value), 26 mm
(mid-range diagnostic sample) and 32 mm (T/K maximum). Each starts at DAT-F/seat Z=0,
has a 12 mm outside diameter, a 3.4 mm M3 through passage and a connected flag embossed
with PS-05 plus H20/H26/H32. All variants stop below D-26's Z=35 mm lower boundary and
test the outboard shoulders on PS-03; PS-15 shoulder placement remains deferred and no
CAD-05 deck surface is implied.

## CAD-08 junction support

The support is an open L-frame at assembly origin X=0, L=-68.5, Z=DAT-F. Its omitted
outboard-rear quadrant respects the measured X≥27, |L|≥41 vent/body-seat zone. It carries
open diagnostic seats for XT60, three XT30 bodies and removable `DN01 OPEN` / `DN02 OPEN`
blanks, so neither owner decision is baked in. Mating/removal arrows, R2 marking, open
finger/tool access and two reversible clamp receivers test attachment and service access.
Fixed PS-15 post shoulders are deliberately absent: their recovered positions overlapped
the connector gauges and would prematurely fix the S0-dependent post interface. CAD-06
shoulder fit is tested on PS-03; PS-15 shoulder placement remains a P1 input. Geometry
reaches Z=12 mm against the Z=14 cap, below D-26.

## Generated individual outputs

All paths below are ignored binaries under `cad/generated/stl/`:

1. `cad01_pwr_bat_max.stl`
2. `cad01_drv_esc.stl`
3. `cad01_pwr_ubec_a.stl`
4. `cad01_pwr_ubec_b.stl`
5. `cad01_ctl_e1.stl`
6. `cad01_ctl_e2.stl`
7. `cad01_vid_wifi_max.stl`
8. `cad01_aud_amp.stl`
9. `cad01_srv_steer.stl`
10. `cad01_ps15_connector_bank.stl`
11. `cad02_ps01_battery_tray.stl`
12. `cad02_ps01_plate_clamp_foot.stl`
13. `cad04_ps03_ubec_shelf.stl`
14. `cad04_ps03_plate_clamp_foot.stl`
15. `cad06_ps05_post_h20.stl`
16. `cad06_ps05_post_h26.stl`
17. `cad06_ps05_post_h32.stl`
18. `cad08_ps15_junction_support.stl`
19. `cad08_ps15_dn_open_blanks.stl`
20. `cad08_ps15_plate_clamp_foot.stl`

Exact bboxes, triangle counts, topology counts, features, orientation and SHA-256
prefixes are in [`generated_part_validation.md`](generated_part_validation.md).

### Required per-output manifest fields

All dimensions below are regenerated bounding boxes in millimetres. `CSV` references
mean the named parameter families in `../parameters/cad_parameters.csv`; every row in
that file carries source, status, uncertainty and physical dependency.

| Output filename | Part ID | CAD task | Related PS/component | Dimensions | Parameter source | Status | Print qty | Material | Print orientation | Validation purpose | Limitation |
|---|---|---|---|---:|---|---|---:|---|---|---|---|
| `cad01_pwr_bat_max.stl` | PWR-BAT max dummy | CAD-01 | PS-13 / PWR-BAT | 95 × 50 × 30 | CSV `BAT-*` | DIAG-CAD | 1 | draft PLA/PETG | DAT-F base on bed; open cage up | pack/XT60/bend/restraint/balance envelope | maximum envelope; actual pack and S0 open |
| `cad01_drv_esc.stl` | DRV-ESC dummy | CAD-01 | PS-13 / DRV-ESC | 67 × 40 × 36 | CSV `ESC-*` | DIAG-CAD | 1 | draft PLA/PETG | flange on bed; fan/cooling cage up | body, exits, fan and 10 mm airflow | D-08 and rear Gate A open |
| `cad01_pwr_ubec_a.stl` | PWR-UBEC-A dummy | CAD-01 | PS-13 / Rail A | 54 × 18 × 15 | CSV `UBEC-*` | DIAG-CAD | 1 | draft PLA/PETG | mount allowance on bed | distinct rail, both leads, bend/air allowance | body/leads expected until arrival |
| `cad01_pwr_ubec_b.stl` | PWR-UBEC-B dummy | CAD-01 | PS-13 / Rail B | 54 × 18 × 15 | CSV `UBEC-*` | DIAG-CAD | 1 | draft PLA/PETG | mount allowance on bed | distinct rail, both leads, bend/air allowance | body/leads expected until arrival |
| `cad01_ctl_e1.stl` | CTL-E1 dummy | CAD-01 | PS-13 / CTL-E1 | 80 × 44 × 13 | CSV `ESP-*` | DIAG-CAD | 1 | draft PLA/PETG | board plane on bed | header, USB plug/bend and service access | board remains expected/unmeasured |
| `cad01_ctl_e2.stl` | CTL-E2 dummy | CAD-01 | PS-13 / CTL-E2 | 80 × 44 × 13 | CSV `ESP-*` | DIAG-CAD | 1 | draft PLA/PETG | board plane on bed | distinct ID, header, USB plug/bend/access | board remains expected/unmeasured |
| `cad01_vid_wifi_max.stl` | VID-WIFI max dummy | CAD-01 | PS-13 / VID-WIFI | 90 × 32 × 20 | CSV `WIFI-*` | DIAG-CAD / UNCONFIRMED | 1 | draft PLA/PETG | body base on bed; heatsink up | P9 max, coax/power/CN-16/cooling | no actual module claim; D-06b open |
| `cad01_aud_amp.stl` | AUD-AMP dummy | CAD-01 | PS-13 / AUD-AMP | 37 × 19 × 8 | CSV `AMP-*` | DIAG-CAD | 1 | draft PLA/PETG | mount allowance on bed | I2S/speaker bends and tool access | expected body; adjustment location provisional |
| `cad01_srv_steer.stl` | SRV-STEER dummy | CAD-01 | PS-13 / KO-19 | 52 × 40 × 42.9 | CSV `SERVO-*` | DIAG-CAD | 1 | draft PLA/PETG | body base on bed; horn disc up | body/lead/horn sweep and visible top ID | D-09/physical sweep open; disc support check in slicer |
| `cad01_ps15_connector_bank.stl` | connector-bank dummy | CAD-01 | PS-13 / PS-15 allocation | 105 × 40 × 28 | CSV `JUNC-DUMMY-*`, `JUNC-HAND-*` | DIAG-CAD | 1 | draft PLA/PETG | body/access columns on bed | mating hand, wire/extraction, tool paths | allocation gauge, not PS-15 production packing |
| `cad02_ps01_battery_tray.stl` | PS-01 tray | CAD-02 | PS-01 / PWR-BAT | 78 × 50 × 12 | CSV `TRAY-*`, `CLAMP-*` | DIAG-CAD | 1 | PETG | DAT-F ribs on bed | bay, insertion, strap, balance park/ballast | S0, floor and clamp fit remain P1 |
| `cad02_ps01_plate_clamp_foot.stl` | PS-01 clamp coupon | CAD-02 | PS-01 / floor edge | 14 × 12 × 10.8 | CSV `CLAMP-*` | DIAG-CAD | 2 | PETG | flat jaw face on bed | reversible no-hole attachment coupon | unloaded until plate fit/pull-off test |
| `cad04_ps03_ubec_shelf.stl` | PS-03 shelf | CAD-04 | PS-03 / UBEC A+B | 70 × 42 × 12 | CSV `SHELF-*`, `UBEC-*` | DIAG-CAD | 1 | PETG | DAT-F open frame on bed | two full-width lanes, leads, airflow, removal | D-24 may resize pockets; free M3 physical occupancy open |
| `cad04_ps03_plate_clamp_foot.stl` | PS-03 clamp coupon | CAD-04 | PS-03 / floor edge | 14 × 12 × 10.8 | CSV `CLAMP-*` | DIAG-CAD | 2 | PETG | flat jaw face on bed | reversible shared/free-feature strategy | unloaded until plate fit/pull-off test |
| `cad06_ps05_post_h20.stl` | PS-05 H20 | CAD-06 | PS-05 / DAT-F | 27.3 × 12 × 20 | CSV `POST-*` H20 | DIAG-CAD | 1 | PETG | post end/flag on bed | lowest height and shoulder/M3 fit | not a deck or selected production height |
| `cad06_ps05_post_h26.stl` | PS-05 H26 | CAD-06 | PS-05 / DAT-F | 27.3 × 12 × 26 | CSV `POST-*` H26 | DIAG-CAD | 1 | PETG | post end/flag on bed | midpoint height and shoulder/M3 fit | not a deck or selected production height |
| `cad06_ps05_post_h32.stl` | PS-05 H32 | CAD-06 | PS-05 / DAT-F | 27.3 × 12 × 32 | CSV `POST-*` H32 | DIAG-CAD | 1 | PETG | post end/flag on bed | high gauge; compare with shell/D-26 | 3 mm below raw D-26 band; must pass 8 mm physical policy |
| `cad08_ps15_junction_support.stl` | PS-15 support | CAD-08 | PS-15 / power junction | 40 × 55 × 12 | CSV `JUNC-SUPPORT-*`, seat families | DIAG-CAD | 1 | PETG | DAT-F open frame on bed | vent-safe seats, mating/removal/tool/R2 access | DN-01/02 and PS-15 post placement remain open |
| `cad08_ps15_dn_open_blanks.stl` | DN open blanks | CAD-08 | PS-15 / DN-01+DN-02 | 45 × 12 × 2.1 | CSV `JUNC-FUSE-*`, `JUNC-KEY-*` | DIAG-CAD | 1 set | PETG | flat on bed | preserve and photograph open decisions | gauges only; no fuse/key choice |
| `cad08_ps15_plate_clamp_foot.stl` | PS-15 clamp coupon | CAD-08 | PS-15 / floor edge | 14 × 12 × 10.8 | CSV `CLAMP-*` | DIAG-CAD | 2 | PETG | flat jaw face on bed | no-hole Z2R attachment coupon | unloaded until plate fit/pull-off test |

## Build-plate groups

| Group | Contents | Bounding box mm |
|---|---|---:|
| `plate_01_core_power_dummies.stl` | battery, ESC, UBEC A, UBEC B | 228.00 × 74.00 × 36.00 |
| `plate_02_controller_communication_dummies.stl` | ESP32 E1/E2, Wi-Fi maximum, amp | 166.00 × 82.00 × 20.00 |
| `plate_03_connector_bank_access_dummies.stl` | steering-servo/KO-19 and connector-bank access dummies | 163.00 × 40.00 × 42.90 |
| `plate_04_battery_tray_test.stl` | tray and two clamp coupons | 118.00 × 50.00 × 12.00 |
| `plate_05_ubec_shelf_junction_support.stl` | UBEC shelf, junction support, decision blanks and clamp coupons | 227.00 × 73.00 × 12.00 |
| `plate_06_post_height_set.stl` | H20, H26, H32 posts | 93.90 × 12.00 × 32.00 |

All groups fit the confirmed 256 × 256 mm X1 Carbon bed. A grouped STL is a practical
layout, not an instruction to print every group before P1; select only the gate-relevant
group and inspect it in Bambu Studio first.

Ignored visual-validation outputs under `cad/generated/renders/` are the exact 19-file
set declared by `sources/generate.py`: three CAD-01 grouped views; ten CAD-01 close-up
views (battery, ESC, UBEC A/B, CTL E1/E2, Wi-Fi, amp, servo and connector bank); CAD-02
tray and clamp views; CAD-04 shelf; CAD-06 post family; and CAD-08 support and decision
blank views. Selected close-ups use a near-top camera so IDs can be reviewed without
losing the isometric connector/access evidence in the grouped views.

## Automated and visual validation

The automated report passes non-empty mesh, mm header, parameter-derived bbox, Z=0 bed
orientation, non-degenerate triangles, closed/oriented shell incidence, D-26 height,
build-plate size, donor-hash inequality, exact output whitelist, stale-output removal and
two-run deterministic identity.

All 19 ignored PNG renders were visually inspected after final regeneration:

- CAD-01 core power: open bodies and connector/cooling cages are distinct; ESC fan/air
  volume and battery/UBEC exits are visible; no donor or production shape appears.
- CAD-01 controllers/communication: both separate ESP32 USB/pin envelopes, the Wi-Fi
  heatsink/cooling cage and aft/forward exits, and the amplifier access cage are visible.
- CAD-01 access: the steering-body/horn-sweep gauge and connector-bank body, mating-hand,
  extraction/wire and tool cages remain open and directionally distinct.
- CAD-02: the 78 mm open tray, forward-open removal path, strap interruptions, balance
  park, side restraints, ballast land and clamp receivers are visible; no roof hides fit evidence.
- CAD-04: separate Rail A/B lanes, open lead ends, airflow floor, free-feature ear,
  post shoulders and clamp receiver are visible and accessible from above.
- CAD-06: three visibly different heights, through passages and height/PS flags are
  present; no deck plate exists.
- CAD-08: the L-frame/vent exclusion, non-overlapping connector/decision seats, route
  arrows and open service side are visible; no fixed post shoulder, enclosure or final
  harness retainer exists.

## Known limitations and pre-print gate

- The local dependency-free validator proves closed and consistently oriented primitive
  shells. It reports strict >2-incidence edges where labels and primitives touch/overlap;
  without a Boolean engine it cannot claim one globally unioned manifold per STL.
- Bambu Studio is not installed in this environment, so slicer repair, layer preview,
  minimum-line-width and unsupported-bridge checks remain mandatory before any TP print.
- Text is geometric and present, but final legibility is slicer/nozzle dependent.
- Clamp feet are diagnostic 4 mm coupons. Do not load them dynamically before a physical
  plate-edge fit and pull-off test; they are not production retention.
- S0, D-06, D-08, D-09, D-10, D-24, DN-01, DN-02 and the physical D-26 sweep remain open
  exactly as their source reports state.
- No diagnostic output selects the narrow right deck or activates fallback A. Those
  outcomes are controlled only by the P1 observations in the checklist.

Generated STL/PNG files are ignored and absent from normal `git diff --stat`; do not
force-add them. The tracked text sources and reports are the reviewable implementation.
