# W17 FPV RC F1 — BUILD SHEET (v2 · current)

*The tape-it-to-the-bench one-pager. Depth lives in `bill_of_materials_v2.md`, `print_spec_v2.md`, `esp32_control_firmware_brief.md`, and the wiring atlas — this is the at-a-glance.*
**Deadline: 21 Jul 2026 · Mercedes W17 · #63**

---

## Print order (what / material / selection)
| Group | Material | Notes |
|---|---|---|
| Body shell (generic 2024, painted W17) | **PLA**, 0.12–0.16 mm, **black** | `NEW BODY 2024 FRONT 1 + REAR + Mirror + halo 2.1 + camera top 1.1`. **Skip Ferrari SF24 / McLaren MCL38 + `New 1.1 Steering Upgrades`.** Silver-nose piece in white/grey. |
| Brake-light diffuser | **white/natural translucent** | `rearbacklightdiffuser`, 1–2 walls over lens, **lens unpainted** (mask it). Red comes from firmware. |
| Floor | **PETG** (Tough PLA if it stays cool) | Original floor — not the REVISION 1.1 front floor. |
| Wheels: rims / nuts / tyre-slot adapters | **PETG** | `Front/Rear_Rim_F1_2022`, `Front_Right_Wheel_Hub_2022_F104`(+mir), `Front/Rear_Locking_Nut`, `F104 tyreslot1/2 tighter`. 4–5 walls. |
| Rear hub | **ASA** | hot + torque-loaded. |
| Front suspension + steering (oil-shock) | **PETG** | original parts (`Suspension_Block_10`, `Arm4`, `Crossarm3_extended`, `GuideRod`, `Steering_Block4`, `servosaverv7`, upright `2023WheelHubsSuspension5`+mir). |
| Rear axle + drivetrain mounts | **ASA, 100% rectilinear** | `Leftrearaxle`, `Rightrearaxle`, `beltdrivemotorlock`, `newgearmotorlock`, rear spacers, 68 mm-shock mount. **No PLA here.** Enclosed + ventilated. |
| Camera cooling duct | **PETG** | `camera_blower_duct.scad` — print once measured. |

**Golden rule:** orient stressed parts so load runs *along* the layers.
⚠ **Before printing the rear:** confirm `Spring_mount_2_REVISION_1` rocker seats the **68 mm** shock in the slicer → if not, use the original rear mount (skip `RearSpringMountREV4`/`springblock`).

## Filament ladder (fast)
PLA = cosmetic/body · PETG = floor + wheels + front + duct · **ASA (100%) = rear/drivetrain (non-negotiable)** · white/natural = diffuser lens.

## Where it packs (2024 body)
- **Battery** → central floor tub (≤75×45×25 mm 2S; carry 2, swap for runtime).
- **ESP32 #1 + #2** → stacked in the rear engine cover / airbox spine.
- **Both UBECs + MAX98357A + RP1 RX** → sidepod pockets.
- **Camera + WiFi module + blower + duct** → nose / airbox (blower on Rail B, vents cut front-in / rear-out).
- **Speaker** → a sidepod.
- **Hall sensor** → at the rear axle; **magnet** on the axle.

## Power rails (all grounds common)
- **Rail A (clean, 5 A UBEC):** camera + WiFi module + both ESP32 + RX + LEDs.
- **Rail B (5 A UBEC):** steering servo + 3× MG90S + blower.
- **XT60** battery main → **Y-split** to ESC + both BECs.

## Bench fixes / must-dos
**Power**
- **Isolate the ESC's BEC +5 V (red) wire** — UBECs power the rails; ESP32 #1 drives only the ESC *signal* + shares ground.
- **Servo rail: 1000 µF** decoupling cap.
- **All grounds common.**

**Signal / sensors**
- **Battery divider 27 k / 10 k** → ESP32 #1 GPIO34 (ADC1, 11 dB); 8.4 V ≈ 2.27 V; calibrate with a meter.
- **Hall A3144 on 5 V**, 10 k pull-up to 3.3 V, out → ESP32 #1 GPIO35 (rising-edge ISR); 1 axle magnet.
- **WS2812:** 330 Ω series on data + **1000 µF** across 5 V/GND at the strip input; *optional* 1N5819 diode-drop on the LED 5 V for a cleaner 3.3 V logic-high.
- **Camera ↔ WiFi-module solder:** D+→DP, D−→DM, GND→GND, **5 V→VDD5.0 from clean Rail A** (never the camera USB rail); antennas on **before** power; heatsink first.

**Drivetrain / radio**
- **Pinion + spur both 48-pitch** (mesh-killer if mismatched).
- **14 mm metal sleeves on the rear axle** (protect printed spacers from motor heat).
- **ESC → sensored mode.**
- **ELRS: version-lock TX/RX** (same major.minor) + **same bind phrase** (TX16S backup matches).

## Build sequence (high level)
1. **Print** — test coupons → 1 rim + hub + **test-fit a tyre before the other three** → ASA rear/drivetrain → PETG front → floor → PLA shell → diffuser + duct.
2. **Paint** — prime (grey; white under silver/turquoise; **mask the diffuser lens**) → gloss clear → decals → final clear.
3. **Electronics on the bench first** — rails + BECs, ESP32 #1 firmware (failsafe + arm gate before anything), camera + WiFi link, sound/light board. Verify before it's buried in the shell.
4. **Install** into chassis/body → **tune** (steering endpoints/trim, ESC, gearbox feel, camera focus 3–5 m).

## Before-you-start checklist (open)
- [ ] Place the order (pull the ring; add 1000 µF cap + XT60 Y-split; optional 1N5819).
- [ ] Confirm XT60 variant at checkout; **TX16S internal module = ExpressLRS**.
- [ ] Shop stocks **ASA**.
- [ ] **Spring_mount rocker vs 68 mm shock** slicer check.
- [ ] King-pin bore = **3 mm** (slicer); spur ↔ belt-pulley bolt pattern (on arrival).
- [ ] Measure camera + blower → finalize the duct.

## Key numbers
Rims **Ø44 front / Ø47 rear** · Tyres **Tamiya 54198 (F, 30 mm) + 51400 (R, 35 mm)**, 64 mm OD · Gears **28T / 75T (48 P)** · Battery **≤75×45×25 mm 2S** · Divider **27 k/10 k** · Front brg **8×12×3.5 ×4** · Rear brg **6801 ×2** · Shocks **52 mm F / 68 mm R** · CRSF **420000 8N1**.
