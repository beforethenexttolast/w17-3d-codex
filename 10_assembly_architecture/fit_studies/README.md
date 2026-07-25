# Remaining-component fit studies

Date: 2026-07-23  
Scope: W17 mechanical/print repository only; original Ryan's Creations oil-shock
front. Steering remains governed by
[`../Y_steering_servo_fit_study.md`](../Y_steering_servo_fit_study.md) and is not
repeated here.

## Authority and evidence

All studies reuse the P0 vehicle frame:

- **DAT-F / Z=0:** assembled original-floor top.
- **X+:** forward; X=0 at the front/rear floor joint.
- **L:** lateral from vehicle centreline; the belt/architecture-right side is L<0.
- **S0:** shell-bottom height above DAT-F, still physically unresolved. All
  mesh-section ceilings use S0=0 and are lower bounds.

Confidence vocabulary is exactly **VERIFIED / DERIVED / DOCUMENTED /
ASSUMPTION**. A verified raw STL bbox does not verify its assembly transform.

Reproduce the common tables:

```text
python3 10_assembly_architecture/evidence/scripts/p0_07_zone_fit_rollup.py
python3 10_assembly_architecture/evidence/scripts/p0_08_zone_visualizations.py
python3 10_assembly_architecture/evidence/scripts/p0_09_validate_zone_outputs.py
python3 10_assembly_architecture/evidence/scripts/p0_12_cassette_fit_visualizations.py
python3 10_assembly_architecture/evidence/scripts/p0_13_validate_cassette_outputs.py
```

Outputs:

- [`../evidence/p0/tables/p0_d28_zone_component_envelopes.md`](../evidence/p0/tables/p0_d28_zone_component_envelopes.md)
- [`../evidence/p0/tables/p0_d29_zone_placements.csv`](../evidence/p0/tables/p0_d29_zone_placements.csv)
- [`../evidence/p0/tables/p0_d30_mass_balance.md`](../evidence/p0/tables/p0_d30_mass_balance.md)
- [`../evidence/p0/tables/p0_d31_fit_gates.md`](../evidence/p0/tables/p0_d31_fit_gates.md)
- [`../evidence/p0/tables/p0_d32_zone_output_validation.md`](../evidence/p0/tables/p0_d32_zone_output_validation.md)
- [`../evidence/p0/tables/p0_d34_cassette_fit_audit.md`](../evidence/p0/tables/p0_d34_cassette_fit_audit.md)
- [`../viz/index.html`](../viz/index.html)

## Study set

| Study | Components |
|---|---|
| [`ZR_rear_drivetrain_fit_study.md`](ZR_rear_drivetrain_fit_study.md) | ESC, motor, belt/pulleys/output shaft, spur/pinion, rear bearings and 68 mm shock |
| [`ZP_power_balance_fit_study.md`](ZP_power_balance_fit_study.md) | two BOM packs, dual UBEC rails, capacitors, divider, XT connectors and BX100 |
| [`ZC_control_rf_fit_study.md`](ZC_control_rf_fit_study.md) | two installed ESP32s + spare, RP1, Wi-Fi module/heatsink and 5.8 GHz antennas |
| [`ZV_camera_nose_fit_study.md`](ZV_camera_nose_fit_study.md) | SSC338Q camera, nose/top candidates, blower and duct |
| [`ZA_accessory_servo_fit_study.md`](ZA_accessory_servo_fit_study.md) | MG90S pan, tilt and DRS |
| [`ZL_audio_light_fit_study.md`](ZL_audio_light_fit_study.md) | MAX98357A, speaker, WS2812 strip, halo/tail lenses |
| [`ZS_suspension_rolling_fit_study.md`](ZS_suspension_rolling_fit_study.md) | original front shocks/uprights/king pins and F104 rolling set |
| [`ZH_speed_sensor_fit_study.md`](ZH_speed_sensor_fit_study.md) | A3144 and one-pulse/rev axle magnet |
| [`ZK_electronics_cassette_fit_study.md`](ZK_electronics_cassette_fit_study.md) | physical NO-GO audit of the forward two-level lift-out cassette, floor-mounted pack/ESC, cockpit gimbal and ganged umbilical |

No study authorizes production STL. Each ends with the physical gate that must
close first.
