# p0_07 / D-39 — whole-car planning mass and balance

Vehicle datum: DAT-F; X+ forward; front axle X=146.1; rear axle X=-90.9; wheelbase=237.0 mm (DERIVED from P0 shell arches).

Tuning target (not a donor specification): **36–40% front / 60–64% rear**, **|L-CG|≤2 mm**, and cross-weight within 3% (**ASSUMPTION**). Physical scales own the result.

| Group | Mass range g | X | L | Z | Confidence |
|---|---:|---:|---:|---:|---|
| BASE-PRINT — printed floor/body/aero/supports | 350.0–520.0 | +20.0 | +0.0 | 18.0 | ASSUMPTION |
| BASE-HW — fasteners, inserts, loom, glue | 100.0–150.0 | +0.0 | +0.0 | 10.0 | ASSUMPTION |
| DRV-MOT — motor | 145.0–165.0 | -100.0 | +0.0 | 27.0 | ASSUMPTION |
| DRV-ESC — ESC incl. wires | 101.5–101.5 | -70.0 | -35.0 | 20.0 | DOCUMENTED mass / ASSUMPTION position |
| DRV-TRAIN — belt/gears/shaft/rear bearings/spacers | 100.0–150.0 | -91.0 | +0.0 | 27.0 | ASSUMPTION |
| FRONT-SUSP — front printed suspension + shocks | 100.0–160.0 | +110.0 | +0.0 | 25.0 | ASSUMPTION |
| FRONT-WHEELS — two front wheel/tyre assemblies | 110.0–160.0 | +146.0 | +0.0 | 27.0 | ASSUMPTION |
| REAR-WHEELS — two rear wheel/tyre assemblies | 130.0–190.0 | -91.0 | +0.0 | 27.0 | ASSUMPTION |
| PWR-BAT-1 — one active pack | 80.0–120.0 | -44.0 | +32.0 | 15.5 | ASSUMPTION mass/position |
| PWR — UBECs, caps, junction, buzzer | 35.0–70.0 | -20.0 | -35.0 | 10.0 | ASSUMPTION |
| CONTROL — two ESP32, RX, Wi-Fi, heatsink | 50.0–95.0 | -10.0 | -35.0 | 30.0 | ASSUMPTION |
| CAM-GIMBAL — camera, blower, two MG90S, mount | 55.0–85.0 | +60.0 | +0.0 | 45.0 | ASSUMPTION Option A |
| SRV-DRS — DRS MG90S | 13.4–13.4 | -125.0 | +0.0 | 65.0 | DOCUMENTED mass / ASSUMPTION position |
| AUDIO-LIGHT — speaker, amp, installed LED segments | 25.0–55.0 | -20.0 | +43.0 | 12.0 | ASSUMPTION |
| SRV-STEER — completed steering servo/horn | 60.0–75.0 | -55.0 | +0.0 | 15.0 | ASSUMPTION mass |

## Calculated scenarios

| Scenario | Mass g | X-CG mm | L-CG mm | Z-CG mm | Front / rear | Verdict |
|---|---:|---:|---:|---:|---:|---|
| One active pack; cockpit camera (midpoint ledger) | 1782 | -7.9 | -1.7 | 22.2 | 35.0% / 65.0% | L/R near target; front is ~1 point below target |
| One active pack; high airbox pod | 1782 | -12.3 | -1.7 | 23.2 | 33.2% / 66.8% | worse fore/aft; assumed Z=70 group raises vertical CG; still physically gated |
| Hypothetical second 100 g pack in right mirror bay | 1882 | -9.8 | -3.3 | 21.9 | 34.2% / 65.8% | mechanically rejected; worsens modelled front and right bias |

Total planning range: **1455–2110 g**. Enumerating all min/max combinations gives a front-load range of **30.6–39.2%** and L-CG **-3.7…-0.2 mm**. This uncertainty is too large to claim that the target is met.

## Decision

- The **left active pack is useful lateral ballast** against the right ESC/power/deck. The speaker-left option also improves the midpoint ledger.
- The battery station alone cannot guarantee fore/aft target: ±10 mm pack motion moves whole-car X-CG by only about 0.6 mm at the midpoint mass.
- Option-A cockpit camera is preferable to the high airbox pod by roughly 1.9 percentage points of front load and 1.0 mm whole-car Z-CG in this model.
- Pack 2 remains an off-car swap. A two-onboard proposal is a new architecture and requires a fresh power/safety review; this mechanical study does not authorize parallel packs.
- Close D-39/ASM-58 with four corner scales before ballast or production tray position.
