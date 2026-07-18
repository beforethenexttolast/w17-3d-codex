# J · Component Placement Matrix

Session 2 · 2026-07-18. Component IDs from `B_component_envelope_register.md` (LGT-LED
split into its two physical segments); zones from `I_zone_layer_plan.md`; mounts
(PS-xx) from `K_printable_support_spec.md`; connectors/harnesses (CN/H-xx) from
`M_connector_harness_matrix.md`; steps (ASM-xx) from `P_assembly_master_manual.md`.
Confidence: **C** confirmed placement · **R** recommended · **P** provisional ·
**G** gated/open decision. No component from Report B is omitted (B.4 rule).

## J.1 Placement & physical integration

| ID | Zone (alt) | Orientation | Mount | Connector exit | Cable run | Conf | Blocking measurements |
|---|---|---|---|---|---|---|---|
| PWR-BAT | Z3L-L0 (Z2L if D-01 shortens Z3L) | flat, XT60 fwd | PS-01 + strap | forward | fwd to PS-15 | R | D-01, D-02, D-26 |
| DRV-MOT | Z6 (fixed by donor design) | transverse | `beltdrivemotorlock` | phase wires inboard-right | short to ESC | C | Gate A residuals only |
| DRV-ESC | Z5R (Z3R-L0 if D-08 shows oversize) | fan up | PS-02 | XT60 fwd, bullets aft | R2 right edge | R | D-08, Gate A edge |
| SRV-STEER | **Z3C — KO-19, occupies by design** | per drawing `[2]` | `Servoholder` (donor) | lead aft-right | to CN-08 at R2 | C | D-09 fit (Gate D residual) |
| SRV-PAN | Z8 gimbal module | per PS-10 design | PS-10 (gated) | per module | H-07 | G | D-06/D-07, owner A-vs-B |
| SRV-TILT | Z8 gimbal module | per PS-10 design | PS-10 (gated) | per module | H-07 | G | D-06/D-07, owner A-vs-B |
| SRV-DRS | Z7 wing pocket (donor design) | per drawing `[2]` | wing pocket | lead down | H-08 via PS-09 | C(loc)/G(wing) | Gate A/B, D-09 |
| CTL-E1 | Z3R-L1 deck, fwd position | flat, USB outboard-right | PS-04 standoffs | USB right; pins low-profile | on-deck + CN-07 | R | D-02, D-04, D-26 |
| CTL-E2 | Z3R-L1 deck, mid position | flat, USB outboard-right | PS-04 standoffs | USB right | on-deck + CN-07 | R | D-02, D-04, D-26 |
| CTL-E3 (spare) | **not installed** (bench stock) | — | — | — | — | C | — |
| RX-ELRS | Z2L (deck fwd edge if D-26 conflicts) | flat, antenna fwd | PS-06 | CRSF aft | CN-19→H-06 | R | D-26, D-20 |
| VID-CAM | Z8 gimbal module (nose **REJECTED-for-primary**, E-24; revisit only after D-25+D-06, owner) | boresight fwd, roll-trimmed | PS-10 (gated) | soldered leads aft | H-07 (**CN-16 at deck edge, S3/DN-11**) | G | **D-06, D-07, halo check** |
| VID-WIFI | Z3R-L1 deck rear slot (airbox draft) | flat, pigtails aft | PS-04 pocket (P9 **dummy**, RST-06) | USB pad fwd, U.FL aft | H-07/H-10 | P | **possession + D-06b**, D-02 |
| VID-HS | bonded to VID-WIFI | — | thermal bond | — | — | C(spec) | D-06b |
| VID-ANT ×2 | PS-12 posts at deck rear (fallback: **standalone chassis posts** — ZB shell mount rejected S3: shell-mounted whips would tether the body through the ~30-mate U.FL at every body-off) | shallow V, tips up | PS-04/PS-12 | U.FL to module | H-10 ≤80 mm | P | D-06b, D-20 |
| AUD-AMP | Z3R-L1 deck beside CTL-E2 | flat | PS-04 pad | spk lead outboard | on-deck + CN-21 | R | D-02 |
| AUD-SPK | Z4L sidepod (fallback under-deck facing airbox) | port outward | PS-14 (gated) | 2-wire inboard | CN-21→H-06 | G | **D-03**, DN-07 |
| LGT-LED-BRK | Z7 tail via drawing-`[7]` channel | strip in `rearbacklightdiffuser` | LGT-DIFF + PS-09 | 3-wire fwd | H-08 (**pre-routed ASM-13**) | C(loc)/G(stack) | Gate A path |
| LGT-LED-HALO | ZB shell (halo base) | strip under halo | adhesive + anchors | 3-wire to CN-14 | H-09 | R | shell fit check |
| LGT-DIFF | Z7 tail (donor part) | lens aft, unpainted | rear stack | houses LED | — | C | Gate A |
| PWR-UBEC-A | Z3R-L0 shelf, fwd pocket | flat | PS-03 | in fwd / out up | H-02 in, H-04 out | R | D-02, **D-24 (upsize risk)** |
| PWR-UBEC-B | Z3R-L0 shelf, aft pocket | flat | PS-03 | in fwd / out aft | H-02 in, H-05 out | R | D-02, **D-24** |
| PWR-Y | inside PS-15 | cradled | PS-15 | — | H-02 | R | DN-01/02 seats |
| PWR-XT30 taps | PS-15 tap row (+1 spare = FUT-EXP) | up | PS-15 | up | H-04/H-05 taps | R | D-24 |
| PWR-CAP ×1–2 | strip input (LED) + PS-03 (servo rail) | upright, zip-tied | PS-03 / at strip | leads short | in H-04/H-05 | R | D-24 |
| PWR-PROT (fuse) | PS-15 fuse seat | mini-blade up | PS-15 | — | in H-02 | **G — DN-01** | **D-24 rating** |
| SW-PWR / disconnect | PS-15 loop-key seat, cockpit-reachable | loop up | PS-15 | — | in H-02 | **G — DN-02** | — |
| SNS-HALL | rear axle at PS-16 | gap 1–3 mm to magnet | PS-16 (ASA) | 3-wire fwd | H-08→CN-15 | R | Gate A stack, D-15 |
| SNS-MAG | rear axle (glued) | radial | CA bond | — | — | C | Gate A |
| SNS-DIV | PS-03 edge (solder joint on battery-sense line) | inline | heatshrunk, zip | — | in H-06 | R | — |
| COOL-BLOW | Z8 at gimbal module | duct outlet to camera | PS-11 (gated) | XH lead down | CN-12→H-05 | G | Gate C set |
| COOL-DUCT | Z8 (from `camera_blower_duct.scad`) | per Gate C | PS-11 | — | — | G | **Gate C: D-06 + blower** |
| PWR-BUZZ (opt) | PS-15 side, if fitted | opening down | zip point | leads to tap | H-04 tap | P | owner opt-in |
| USB-PORT (service) | cockpit rim via PS-17 | pigtails parked | PS-17 (gated) | — | H-11 | G | **D-11, DN-08** |
| HW-INSERT | PS-04/PS-15 bosses + 3 body bosses | — | heat-set | — | — | R | — |
| HARNESS | R1/R2 edge routes + crossings X1/X2 | — | PS-08 combs | — | N plan | R | **D-10, D-26** |
| FUT-EXP | deck fwd blank + CN-20 spare tap + CN-07 spares | — | PS-04 grid | — | — | R | — |

## J.2 Access, environment & sequence

| ID | Access requirement | Cooling | Vibration | RF concern | Install | Removal dependency |
|---|---|---|---|---|---|---|
| PWR-BAT | **top, every session** (swap) | none | strap, 20 g fwd | none | ASM-15 | body off only — nothing above it |
| DRV-MOT | mesh/pinion reach | rear exhaust path | source | noise source | ASM-12 | drivetrain partial teardown |
| DRV-ESC | top reach, fan gap check | **fan + ≥10 mm**, rear-out | strap | noise source | ASM-16 | connectors off → strap → out |
| SRV-STEER | horn + screws reach until ASM-08 | convection | rigid in holder | — | **ASM-06 (early: powered+centred ASM-07 before linkage ASM-08)** | linkage open → holder |
| SRV-PAN/TILT | at module bench | convection | module stiffness (VR) | — | ASM-26 | module off (CN-09/10) |
| SRV-DRS | wing pocket reach | convection | wing loads | — | ASM-28 | CN-11 → wing off |
| CTL-E1/E2 | **USB right side; boards swappable on deck** | deck airflow | foam pad + standoffs | keep sense wires short | ASM-22 | CN-07 → deck out → board off |
| RX-ELRS | antenna untouched during service | cool | pad | **2.4 GHz — quiet corner** | ASM-23 | CN-19, peel from PS-06 |
| VID-CAM | removable w/o destroying mount | **ducted blower** | soft-mount board | — | ASM-26 | module out via CN-09/10 + feeds |
| VID-WIFI | heatsink first; antennas **before power** | **airbox draft mandatory** | pocket + zip | **5.8 GHz TX** | ASM-25 (**dummy until confirmed**) | CN-07 + CN-16 (S3) → deck out |
| VID-ANT | replaceable at posts | — | zip anchors | keep ≥150 mm from RX ant | ASM-30 | unzip, U.FL off |
| AUD-AMP | on-deck | deck airflow | pad | keep spk wires off sense | ASM-22 | with deck |
| AUD-SPK | port clear | — | isolation ring | — | ASM-22/after DN-07 | CN-21 |
| LGT-LED-BRK | pull-through replaceable (PS-09 loop) | — | channel-guided | — | **ASM-13 pre-route** | tail pull-through |
| LGT-LED-HALO | with shell | — | adhesive + anchors | — | ASM-27 | CN-14, shell off |
| PWR-UBEC-A/B | under deck | pocket vented (D-19) | ribs + zip | switching noise — keep from Z2L | ASM-17 (+verify ASM-21) | deck out → lift |
| PWR-Y / taps / fuse / disconnect | **disconnect reachable body-on** | — | rigid in PS-15 | — | ASM-17/ASM-18 | at PS-15, fingers |
| PWR-CAP | at rails | — | zip | — | ASM-17 | with rail leads |
| SNS-HALL | gap gauge access at build | hot pocket (ASA mount) | rigid | pull-up line quiet | ASM-24 | service loop pull |
| SNS-DIV | none (inline) | — | heatshrunk | ADC line short | ASM-24 | with H-06 |
| COOL-BLOW/DUCT | duct de-mate for camera service | is the cooling | isolate from camera board | — | ASM-29 | CN-12, duct off |
| USB-PORT | body-on programming (if DN-08 yes) | — | parked | — | ASM-31 | — |
| HARNESS | every connector reachable per Q | — | combs ≤60 mm at motion | rail separation (N) | ASM-17/31 | per module |

**KO-19 statement (RST-03):** SRV-STEER + `Servoholder` are listed above as *occupants*,
not as items to place — the placement matrix allocates **around** them, and ASM-06/07/08
put the servo in, powered and centred, **before** the linkage closes and before Z3
electronics restrict access.

**(P0 — Session 4A measurement notes, tagged; details in `V_P0_geometry_measurement_results.md`):**
CTL-E1/E2 + AUD-AMP + VID-WIFI deck rows are now **conditional on the S0 pin**
(P2s measured 26–41 at S0=0 — deck viable only inboard-hugged at P4≈20 in the
S0 ≥ ~6 world; fallback-A trigger armed, not fired). PWR-BAT: bay **length 78 ✔**;
pack body passes under the measured rod band (Z 35–62). RX-ELRS Z2L and PS-15 Z2R:
validated with the best side-bay heights (33–41 at |L| 20–40, X +10…+55). The
ESP32 **airbox fallback F-2 is geometrically dead** (D-04); the nose remains
unallocated with **no protected camera volume found** (D-25). D-27: the free
slot-nut grid does not exist — mounts per K's (P0) rule update.

**Unknown-envelope components are present, not hidden:** VID-CAM (D-06), VID-WIFI
(D-06b + possession), AUD-SPK (model dims), DRV-ESC (D-08), servos (D-09), UBEC/caps/
blower (on-arrival), HARNESS bulk (D-10) — each row carries its blocker and its
dummy-envelope stand-in lives in PS-13 (except the camera, which is **not** dry-fitted
from a guessed block; D-06 first).
