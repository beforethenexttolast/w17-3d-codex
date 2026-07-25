# p0_07 / D-28…D-38 — remaining-component envelope roll-up

Datum: component-local dimensions unless a vehicle coordinate is stated. Confidence vocabulary is exactly **VERIFIED / DERIVED / DOCUMENTED / ASSUMPTION**.

48P arithmetic: 75T pitch Ø **39.69 mm**, 28T pitch Ø **14.82 mm**, pitch-centre distance **27.25 mm** (DERIVED; hub/bolt/backlash excluded).

| ID | Zone | Component | Qty | Body envelope | Confidence | Installation envelope | Mass | Evidence |
|---|---|---|---:|---|---|---|---|---|
| DRV-ESC | rear | Hobbywing QuicRun 10BL120 Sensored G2 | 1 | 43 × 36.8 × 32.3 mm; fan 25 × 25 × 10 mm | **DOCUMENTED** | body + ≥10 mm clear above fan + 12 AWG exits | 101.5 g incl. wires (DOCUMENTED) | Hobbywing official QuicRun 10BL120 Sensored G2 product page; exact on-hand label still a gate |
| DRV-MOT | rear | Rocket 540 V3 17.5T sensored motor | 1 | Ø36 × 54 mm can; Ø3.175 × 14.5 mm shaft | **DOCUMENTED** | can + solder tabs/sensor lead + pinion + axial service pull | 145–165 g (ASSUMPTION until weighed) | BOM/Rocket 540 family listing; user-specified Ø≈36; verify the real can |
| DRV-BELT | rear | belt-drive set | 1 | 140 mm belt length; pulley diameters TO MEASURE | **DOCUMENTED** | two pulley discs + two moving tangent runs + guard clearance | 30–60 g (ASSUMPTION) | BOM v2 §8 and on-hand inventory |
| DRV-SHAFT | rear | belt-set metal rear output shaft | 1 | diameter/shoulders/usable span TO MEASURE | **ASSUMPTION** | bearing seats + spacers + wheel/gear retention | 20–45 g (ASSUMPTION) | BOM v2 §8; physical set required |
| DRV-SPUR | rear | HPI/3Racing 48P 75T spur | 1 | pitch Ø39.69; theoretical outside Ø40.75 mm | **DERIVED** | gear disc + unknown hub/bolt pattern + ≥2 mm radial guard | 8–15 g (ASSUMPTION) | 75T/48P BOM; standard diametral-pitch arithmetic |
| DRV-PINION | rear | 48P 28T pinion | 1 | pitch Ø14.82; theoretical outside Ø15.88 mm | **DERIVED** | gear disc; theoretical centre distance 27.25 mm | 5–10 g (ASSUMPTION) | 28T/48P BOM; standard diametral-pitch arithmetic |
| BRG-REAR | rear | 6801 rear bearing | 2 | 12 ID × 21 OD × 5 mm | **DOCUMENTED** | two coaxial carrier seats; no printed preload | ≈11 g pair (ASSUMPTION) | BOM v2 §9 / Ryan Parts List |
| SHK-REAR | rear | rear oil shock | 1 | 68 mm eye-to-eye; body Ø/stroke TO MEASURE | **DOCUMENTED** | full compressed↔extended swept cylinder | 15–30 g (ASSUMPTION) | BOM v2 §10 / Ryan Parts List |
| DRV-LOCK | rear | belt-drive motor lock | 1 | 31.99 × 3.5 × 32 mm raw bbox | **VERIFIED** | 32 mm disc/lock at motor interface; orientation and screw stack gate | not weighed | `02_ready_to_slice/02_ASA_rear_drivetrain/beltdrivemotorlock.stl`; p0_07 live bbox (1440 triangles) |
| DRV-REAR-L | rear | original left rear bearing carrier | 1 | 81.5 × 25 × 10 mm raw bbox | **VERIFIED** | Gate A decides whether this or Rev-1 motor covers carry the 6801 | not weighed | `02_ready_to_slice/02_ASA_rear_drivetrain/Leftrearaxle.stl`; p0_07 live bbox (11596 triangles) |
| DRV-REAR-R | rear | original right rear bearing carrier | 1 | 81.5 × 35 × 10 mm raw bbox | **VERIFIED** | Gate A decides whether this or Rev-1 motor covers carry the 6801 | not weighed | `02_ready_to_slice/02_ASA_rear_drivetrain/Rightrearaxle.stl`; p0_07 live bbox (6332 triangles) |
| PWR-BAT-1 | power | 2S LiPo active pack | 1 | ≤75 × 45 × 25 mm | **DOCUMENTED** | 95 × 50 × 30 mm allocation incl. XT60/strap | 80–120 g (ASSUMPTION) | BOM v2 §D / 2024-body limit |
| PWR-BAT-2 | power | 2S LiPo swap pack | 1 | ≤75 × 45 × 25 mm | **DOCUMENTED** | OFF-CAR storage/charge envelope on selected architecture | 80–120 g off-car (ASSUMPTION) | BOM v2 §D; dual-onboard fit rejected provisionally |
| PWR-UBEC-A | power | UBEC 5 A — Rail A clean | 1 | TO MEASURE; 30 × 14 × 10 mm planning block | **ASSUMPTION** | body + both lead exits + ≥5 mm convection | 10–20 g (ASSUMPTION) | B register planning block; on-hand part not measured |
| PWR-UBEC-B | power | UBEC 5 A — Rail B servos | 1 | TO MEASURE; 30 × 14 × 10 mm planning block | **ASSUMPTION** | body + both lead exits + ≥5 mm convection | 10–20 g (ASSUMPTION) | B register planning block; on-hand part not measured |
| PWR-CAP-B | power | servo-rail electrolytic | 1 | 1000 µF / 16 V; Ø10 × 20 mm planning body | **ASSUMPTION** | upright/sideways body + insulated leads and zip restraint | 2–5 g (ASSUMPTION) | BOM value; physical capacitor can size unknown |
| PWR-CAP-LED | power | LED-input electrolytic | 1 if stock permits | 1000 µF / 16 V; Ø10 × 20 mm planning body | **ASSUMPTION** | within 50 mm electrical lead length of strip input | 2–5 g (ASSUMPTION) | BOM recommends 1–2; physical capacitor unknown |
| SNS-DIV | power | battery divider 27 kΩ / 10 kΩ | 1 | two axial resistors; assembled body TO MEASURE | **DOCUMENTED** | heatshrunk branch, ADC tap, common-star ground | <1 g (ASSUMPTION) | BOM v2 §D/key reminders |
| PWR-XT60 | power | XT60 main junction / loop | as built | connector/lead geometry TO MEASURE | **ASSUMPTION** | finger access + wire bend + recessed live side | 10–25 g junction (ASSUMPTION) | BOM; local connector variant unknown |
| PWR-XT30 | power | XT30 accessory taps | few | connector/lead geometry TO MEASURE | **ASSUMPTION** | tap row + caps/strain relief | 5–15 g set (ASSUMPTION) | BOM; local connector variant unknown |
| PWR-BUZZ | power | BX100 low-voltage buzzer | 0–1 | TO MEASURE; 30 × 12 × 8 mm planning block | **ASSUMPTION** | speaker apertures unobstructed + balance-lead access | 5–10 g (ASSUMPTION) | B register planning block |
| CTL-E1 | control | ESP32-WROOM-32 DevKit V1 — control | 1 | TO MEASURE clone; 55 × 28 × 13 mm planning block | **ASSUMPTION** | 55 × 44 × 23 mm incl. side headers and USB bend | 8–15 g (ASSUMPTION) | BOM identifies clone family, not a controlled PCB drawing |
| CTL-E2 | control | ESP32-WROOM-32 DevKit V1 — sound/light | 1 | TO MEASURE clone; 55 × 28 × 13 mm planning block | **ASSUMPTION** | 55 × 44 × 23 mm incl. side headers and USB bend | 8–15 g (ASSUMPTION) | BOM identifies clone family, not a controlled PCB drawing |
| CTL-E3 | control | ESP32-WROOM-32 spare | 1 | same family as CTL-E1/E2 | **ASSUMPTION** | OFF-CAR bench stock | off-car | BOM explicitly assigns one of three as spare |
| RX-ELRS | control | RadioMaster RP1 V2 ELRS receiver | 1 | 13 × 11 × 3 mm; 65 mm T antenna | **DOCUMENTED** | receiver pad + 65 mm antenna + service loop | 2.2 g incl. antenna (DOCUMENTED) | RadioMaster official RP1 V2 page |
| VID-WIFI | control | BL-M8812EU2 USB Wi-Fi module | 1 | TO MEASURE; allocated maximum 60 × 32 × 12 mm | **ASSUMPTION** | module + 28 × 28 × 3 heatsink + USB/U.FL exits + airflow | 15–35 g (ASSUMPTION) | H P9 allocation; on-hand module not measured |
| VID-HS | control | Wi-Fi heatsink | 1 | 28 × 28 × 3 mm | **DOCUMENTED** | bond layer + module stack | 5–12 g (ASSUMPTION) | BOM v2 §1 |
| VID-ANT | control | 5.8 GHz U.FL linear omni | 2 | 70 mm whip each | **DOCUMENTED** | two 70 mm routes + U.FL service loop; no sharp fold | 2–6 g pair (ASSUMPTION) | BOM v2 §1 / on-hand mapping |
| VID-CAM | camera | OpenIPC SSC338Q camera assembly | 1 | TO MEASURE: PCB, heatsink, lens and cable exits | **ASSUMPTION** | measured body + FOV cone + cooling + gimbal sweep | 20–45 g (ASSUMPTION) | Gate C; user says IMX415, repo says IMX335 |
| CAM-TOP | camera | `camera top 1.1` | 1 candidate | 16.75 × 17.71 × 6.92 mm raw bbox | **VERIFIED** | tiny exterior pod cover; does not establish camera-board capacity | not weighed | `02_ready_to_slice/06_PLA_body_shell/camera top 1.1.stl`; p0_07 live bbox (9668 triangles) |
| CAM-NOSE | camera | `cameranose` | 1 candidate | 5.84 × 10.5 × 9.81 mm raw bbox | **VERIFIED** | gated decorative/legacy candidate; no measured hardware interface | not weighed | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts/cameranose.stl`; p0_07 live bbox (832 triangles) |
| CAM-2C | camera | `camera 2 colour` | 1 candidate | 26.25 × 14.94 × 12.58 mm raw bbox | **VERIFIED** | gated legacy candidate; no measured hardware interface | not weighed | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts/camera 2 colour.stl`; p0_07 live bbox (8900 triangles) |
| CAM-F104 | camera | `f104camera` | 1 candidate | 26.25 × 15 × 10.85 mm raw bbox | **VERIFIED** | gated legacy candidate; no measured hardware interface | not weighed | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts/f104camera.stl`; p0_07 live bbox (7550 triangles) |
| COOL-BLOW | camera | 5 V 20 mm blower | 1 | 20 × 20 face; thickness/outlet TO MEASURE | **DOCUMENTED** | body + inlet hemisphere + outlet collar + lead | 3–8 g (ASSUMPTION) | BOM v2 §13; actual blower calipers pending |
| COOL-DUCT | camera | camera blower duct | 1 | placeholder defaults: 20 × 8 collar; 18 mm transition | **ASSUMPTION** | nine measured dimensions + 1.4 mm wall + 0.25 mm nominal slip | 2–8 g (ASSUMPTION) | `unsorted_stl_raw/camera_blower_duct.scad`; defaults explicitly non-production |
| SRV-PAN | servos | MG90S pan servo | 1 | 22.8 × 12.2 × 28.5 mm | **DOCUMENTED** | body + ears + horn sweep + 250 mm lead | 13.4 g (DOCUMENTED) | TowerPro official MG90S page; clone must be measured |
| SRV-TILT | servos | MG90S tilt servo | 1 | 22.8 × 12.2 × 28.5 mm | **DOCUMENTED** | body + ears + horn sweep + 250 mm lead | 13.4 g (DOCUMENTED) | TowerPro official MG90S page; clone must be measured |
| SRV-DRS | servos | MG90S DRS servo | 1 | 22.8 × 12.2 × 28.5 mm | **DOCUMENTED** | body + ears + horn/rod swept volume | 13.4 g (DOCUMENTED) | TowerPro official MG90S page; clone must be measured |
| DRS-WING | servos | preferred 2021 rear wing with DRS | 1 candidate | 105.11 × 82.05 × 60 mm raw bbox | **VERIFIED** | full wing + servo pocket; mounting to chosen rear stack remains Gate A/B | not weighed | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2021 Upgrades/2021Rearwing with DRS.stl`; p0_07 live bbox (5664 triangles) |
| DRS-ARM | servos | 2021 DRS arm | 1 candidate | 58 × 5 × 10 mm raw bbox | **VERIFIED** | 58 mm linkage arm swept through measured flap travel | not weighed | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Experimental Parts/DRS Arm for 2021 Rear Wing.stl`; p0_07 live bbox (1324 triangles) |
| AUD-AMP | audio | MAX98357A breakout | 1 | TO MEASURE; 19.4 × 17.8 × 3 mm reference board | **ASSUMPTION** | board + terminals/pins + wire bends | 1–5 g (ASSUMPTION) | Adafruit reference board only; BOM clone can differ |
| AUD-SPK | audio | 4 Ω 3 W speaker | 1 | TO MEASURE; Ø28–40 × 6–12 mm planning range | **ASSUMPTION** | basket + cone excursion + baffle/port + two wires | 20–40 g (ASSUMPTION) | B register planning range; actual speaker unmeasured |
| LGT-LED | audio | WS2812B 30 LED/m strip | 1 m stock | 10 mm wide; 33.33 mm pixel pitch | **DOCUMENTED** | cut segments + 3-wire tails + 330 Ω data resistor | 5–20 g installed segments (ASSUMPTION) | BOM v2 §4 (30 LED / 1 m) |
| LGT-DIFF | audio | `rearbacklightdiffuser` | 1 | 9.5 × 12 × 14.5 mm raw bbox | **VERIFIED** | one-pixel translucent lens; keep paint out of optical faces | not weighed | `02_ready_to_slice/07_translucent_diffuser/rearbacklightdiffuser.stl`; p0_07 live bbox (3298 triangles) |
| HALO | audio | `new halo 2.1` | 1 | 74.94 × 38.75 × 24.86 mm raw bbox | **VERIFIED** | halo structure; LED carrier/adhesive path remains physical | not weighed | `02_ready_to_slice/06_PLA_body_shell/new halo 2.1.stl`; p0_07 live bbox (96250 triangles) |
| SHK-FRONT | suspension | front oil shock | 2 | 51 mm requirement / 52 mm stock label; exact eye-to-eye, stroke and body Ø TO MEASURE | **DOCUMENTED conflict / ASSUMPTION physical** | full bump↔droop swept cylinder each side | 20–40 g pair (ASSUMPTION) | user requirement; HARDWARE_INVENTORY §10 explicitly flags 51-vs-52 residual |
| UPRIGHT-L | suspension | original oil-shock upright left | 1 | 56.86 × 20 × 49.99 mm raw bbox | **VERIFIED** | assembled orientation/king-pin/wheel-axis envelope, not raw bbox | not weighed | `02_ready_to_slice/03_PETG_front_suspension_steering/2023WheelHubsSuspension5.stl`; p0_07 live bbox (1864 triangles) |
| UPRIGHT-R | suspension | original oil-shock upright right | 1 | 56.86 × 20 × 49.99 mm raw bbox | **VERIFIED** | assembled orientation/king-pin/wheel-axis envelope, not raw bbox | not weighed | `02_ready_to_slice/03_PETG_front_suspension_steering/2023WheelHubsSuspension5mir.stl`; p0_07 live bbox (1864 triangles) |
| STEER-BLOCK | suspension | `Steering Block4` knuckle | 2 | 31 × 17 × 29.99 mm raw bbox | **VERIFIED** | M3 king-pin bore and two MR128 bearing seats require physical coupons | not weighed | `02_ready_to_slice/03_PETG_front_suspension_steering/Steering Block4.stl`; p0_07 live bbox (3158 triangles) |
| KINGPIN | suspension | M3 × 30 king pin | 2 | Ø3 × 30 mm | **DOCUMENTED** | pin + circlip access + free pivot | ≈3 g pair (ASSUMPTION) | BOM v2 §11 / on-hand inventory |
| RIM-F | suspension | printed F104 front rim | 2 | 44 × 43.99 × 30 mm raw bbox | **VERIFIED** | Ø44 bead family ×30 wide; tyre/bearing coupon gates production | not weighed | `02_ready_to_slice/04_PETG_wheels/Front_Rim_F1_2022.stl`; p0_07 live bbox (40136 triangles) |
| RIM-R | suspension | printed F104 rear rim | 2 | 47.01 × 47.01 × 35.55 mm raw bbox | **VERIFIED** | Ø47 bead family ×35.55 wide; tyre/adapter coupon gates production | not weighed | `02_ready_to_slice/04_PETG_wheels/Rear_Rim_F1_2022.stl`; p0_07 live bbox (25994 triangles) |
| HUB-F | suspension | front-right F104 hub source | 1 + mirrored 1 | 27.99 × 63.96 × 55.95 mm raw bbox | **VERIFIED** | raw multi-axis bbox; installed bearing seats and mirrored left gate | not weighed | `02_ready_to_slice/04_PETG_wheels/Front_Right_Wheel_Hub_2022_F104.stl`; p0_07 live bbox (13126 triangles) |
| TYRE-F | suspension | Tamiya 54198 front tyre | 2 | Ø64 × 30 mm | **DOCUMENTED** | steer + bump moving envelope | 40–70 g pair (ASSUMPTION) | Tamiya F104 official chassis specification / BOM |
| TYRE-R | suspension | Tamiya 51400 rear tyre | 2 | Ø64 × 35 mm | **DOCUMENTED** | bump/axle moving envelope | 50–90 g pair (ASSUMPTION) | Tamiya F104 official chassis specification / BOM |
| BRG-FRONT | suspension | MR128ZZ front bearing | 4 | 8 ID × 12 OD × 3.5 mm | **DOCUMENTED** | two coaxial seats per front hub | ≈10 g set (ASSUMPTION) | BOM v2 §9 / Ryan Parts List |
| SNS-HALL | sensors | A3144 Hall switch | 1 | 4.04–4.17 × 2.97–3.10 × 1.47–1.57 mm package body | **DOCUMENTED** | body + leads + 1–3 mm adjustable gap bracket | <1 g | Allegro A3141–A3144 datasheet, UA package |
| SNS-MAG | sensors | rear-axle magnet | 1 | Ø3 × 1 mm | **DOCUMENTED** | recess/bond + retention witness mark | <1 g | BOM v2 §7 |

## Lower-bound shell / moving-envelope checks

Shell values use **DAT-F Z=0 and S0=0**. Add the physically measured S0 to the ceiling; the 5 mm static / 8 mm moving policies are not waived.

| ID | Datum station | Occupant | Evidence profile | Result | Confidence |
|---|---|---|---|---|---|
| DRV-ESC | X−60, L≈−25 | body top Z35.3; airflow plane Z45.3 | S0=0 width near Z35 is 48 mm only about centre; width at Z45 is 17 mm | FAIL at side placement; S0 + exact fan footprint/label required | DERIVED |
| PWR-BAT-1 | X−20…−40, L shoulder | pack body top Z28; strap stack ≈Z31 | ceil @L45 is 27→24 mm; provisional KO-01 is Z22…38, |L|≤22 | FAIL at S0=0 / moving corridor unresolved; S0 and dummy sweep required | DERIVED |
| CTL-E1/E2 | X−20, L20/L30 | planning top ≈Z33 on DAT-D20 | ceil 39 mm @L20, 26 mm @L30 | only narrow inboard edge is plausible; no production deck | DERIVED |
| AUD-SPK | X−20…−40, L45 | planning top ≤Z15 | ceil 27→24 mm at S0=0 | raw 9–12 mm / policy 4–7 mm; candidate is plausible, physical port gate stays | DERIVED |
| TYRE-F | front arch X+146.1 | Ø64 moving wheel | about 3.5 mm arch margin | below 8 mm moving policy; full steer+bump/body-on test mandatory | DERIVED |
| TYRE-R | rear arch X−90.9 | Ø64 moving wheel | about 4 mm arch margin | below 8 mm moving policy; full bump/body-on test mandatory | DERIVED |

## Reproducibility

- 18 STL bboxes loaded directly; every bbox matched its independent expected value within 0.12 mm.
- Raw/historical STLs were read only. No mesh was transformed, repaired or written.
- Hardware without a controlled drawing remains ASSUMPTION even when a planning block exists elsewhere in the repo.
