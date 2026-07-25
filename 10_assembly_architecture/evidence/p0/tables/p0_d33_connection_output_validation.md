# p0_11 — connection output validation

| Check | Result | Detail |
|---|---|---|
| source joint IDs unique | **PASS** | 160 unique rows |
| source assembly coverage | **PASS** | 12 assemblies |
| per-joint field completeness | **PASS** | parts, BOM hardware, interface, retention, order, dependency, tool, torque, confidence and ASM check |
| DEFER discipline: MG90S | **PASS** | 5 row(s): J-CAM-002, J-CAM-003, J-CAM-004, J-REA-030, J-REA-031 |
| DEFER discipline: rear 68 mm shock | **PASS** | 2 row(s): J-REA-027, J-REA-028 |
| DEFER discipline: magnet-dependent | **PASS** | 3 row(s): J-SNS-001, J-SNS-002, J-SNS-003 |
| DEFER discipline: 2S pack | **PASS** | 1 row(s): J-PWR-002 |
| DEFER discipline: charge module/port/interlock | **PASS** | 5 row(s): J-CHG-001, J-CHG-002, J-CHG-003, J-CHG-004, J-CAS-005 |
| DEFER discipline: in-transit tyres | **PASS** | 4 row(s): J-FRT-022, J-FRT-023, J-REA-023, J-REA-024 |
| CSV register exists | **PASS** | 10_assembly_architecture/Z_connection_joint_register.csv |
| CSV row/ID parity | **PASS** | 160/160 rows in canonical order |
| CSV sortable columns | **PASS** | zone/order/ASM/confidence/disposition present |
| Markdown register exists | **PASS** | 10_assembly_architecture/Z_connection_joint_register.md |
| Markdown register Joint-ID coverage | **PASS** | all IDs present |
| Markdown zone-sort view | **PASS** | assembly-order table + zone index + sortable CSV declaration |
| manual generated block | **PASS** | bounded p0_10 block present |
| manual Joint-ID coverage | **PASS** | all IDs present |
| manual charge + closure steps | **PASS** | deferred charge integration + connection closure audit |
| HTML exists: connections/index.html | **PASS** | 10_assembly_architecture/viz/connections/index.html |
| index.html: CSP | **PASS** | inline-only CSP present |
| index.html: theme | **PASS** | media preference + explicit overrides |
| index.html: overflow | **PASS** | body fixed; drawings scroll |
| index.html: no external assets | **PASS** | none |
| index.html: local links | **PASS** | 13 links checked |
| HTML exists: connections/floor_structure.html | **PASS** | 10_assembly_architecture/viz/connections/floor_structure.html |
| floor_structure.html: CSP | **PASS** | inline-only CSP present |
| floor_structure.html: theme | **PASS** | media preference + explicit overrides |
| floor_structure.html: overflow | **PASS** | body fixed; drawings scroll |
| floor_structure.html: no external assets | **PASS** | none |
| floor_structure.html: local links | **PASS** | 8 links checked |
| floor_structure.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| floor_structure.html: scale/ruler | **PASS** | declared per exploded strip |
| floor_structure.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| floor_structure.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| floor_structure.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/servo_holder.html | **PASS** | 10_assembly_architecture/viz/connections/servo_holder.html |
| servo_holder.html: CSP | **PASS** | inline-only CSP present |
| servo_holder.html: theme | **PASS** | media preference + explicit overrides |
| servo_holder.html: overflow | **PASS** | body fixed; drawings scroll |
| servo_holder.html: no external assets | **PASS** | none |
| servo_holder.html: local links | **PASS** | 5 links checked |
| servo_holder.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| servo_holder.html: scale/ruler | **PASS** | declared per exploded strip |
| servo_holder.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| servo_holder.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| servo_holder.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/steering.html | **PASS** | 10_assembly_architecture/viz/connections/steering.html |
| steering.html: CSP | **PASS** | inline-only CSP present |
| steering.html: theme | **PASS** | media preference + explicit overrides |
| steering.html: overflow | **PASS** | body fixed; drawings scroll |
| steering.html: no external assets | **PASS** | none |
| steering.html: local links | **PASS** | 20 links checked |
| steering.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| steering.html: scale/ruler | **PASS** | declared per exploded strip |
| steering.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| steering.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| steering.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/front_suspension.html | **PASS** | 10_assembly_architecture/viz/connections/front_suspension.html |
| front_suspension.html: CSP | **PASS** | inline-only CSP present |
| front_suspension.html: theme | **PASS** | media preference + explicit overrides |
| front_suspension.html: overflow | **PASS** | body fixed; drawings scroll |
| front_suspension.html: no external assets | **PASS** | none |
| front_suspension.html: local links | **PASS** | 24 links checked |
| front_suspension.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| front_suspension.html: scale/ruler | **PASS** | declared per exploded strip |
| front_suspension.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| front_suspension.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| front_suspension.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/rear_drivetrain.html | **PASS** | 10_assembly_architecture/viz/connections/rear_drivetrain.html |
| rear_drivetrain.html: CSP | **PASS** | inline-only CSP present |
| rear_drivetrain.html: theme | **PASS** | media preference + explicit overrides |
| rear_drivetrain.html: overflow | **PASS** | body fixed; drawings scroll |
| rear_drivetrain.html: no external assets | **PASS** | none |
| rear_drivetrain.html: local links | **PASS** | 34 links checked |
| rear_drivetrain.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| rear_drivetrain.html: scale/ruler | **PASS** | declared per exploded strip |
| rear_drivetrain.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| rear_drivetrain.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| rear_drivetrain.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/power_charge.html | **PASS** | 10_assembly_architecture/viz/connections/power_charge.html |
| power_charge.html: CSP | **PASS** | inline-only CSP present |
| power_charge.html: theme | **PASS** | media preference + explicit overrides |
| power_charge.html: overflow | **PASS** | body fixed; drawings scroll |
| power_charge.html: no external assets | **PASS** | none |
| power_charge.html: local links | **PASS** | 13 links checked |
| power_charge.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| power_charge.html: scale/ruler | **PASS** | declared per exploded strip |
| power_charge.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| power_charge.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| power_charge.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/electronics_trays.html | **PASS** | 10_assembly_architecture/viz/connections/electronics_trays.html |
| electronics_trays.html: CSP | **PASS** | inline-only CSP present |
| electronics_trays.html: theme | **PASS** | media preference + explicit overrides |
| electronics_trays.html: overflow | **PASS** | body fixed; drawings scroll |
| electronics_trays.html: no external assets | **PASS** | none |
| electronics_trays.html: local links | **PASS** | 34 links checked |
| electronics_trays.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| electronics_trays.html: scale/ruler | **PASS** | declared per exploded strip |
| electronics_trays.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| electronics_trays.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| electronics_trays.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/camera_blower.html | **PASS** | 10_assembly_architecture/viz/connections/camera_blower.html |
| camera_blower.html: CSP | **PASS** | inline-only CSP present |
| camera_blower.html: theme | **PASS** | media preference + explicit overrides |
| camera_blower.html: overflow | **PASS** | body fixed; drawings scroll |
| camera_blower.html: no external assets | **PASS** | none |
| camera_blower.html: local links | **PASS** | 9 links checked |
| camera_blower.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| camera_blower.html: scale/ruler | **PASS** | declared per exploded strip |
| camera_blower.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| camera_blower.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| camera_blower.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/audio.html | **PASS** | 10_assembly_architecture/viz/connections/audio.html |
| audio.html: CSP | **PASS** | inline-only CSP present |
| audio.html: theme | **PASS** | media preference + explicit overrides |
| audio.html: overflow | **PASS** | body fixed; drawings scroll |
| audio.html: no external assets | **PASS** | none |
| audio.html: local links | **PASS** | 4 links checked |
| audio.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| audio.html: scale/ruler | **PASS** | declared per exploded strip |
| audio.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| audio.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| audio.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/lighting.html | **PASS** | 10_assembly_architecture/viz/connections/lighting.html |
| lighting.html: CSP | **PASS** | inline-only CSP present |
| lighting.html: theme | **PASS** | media preference + explicit overrides |
| lighting.html: overflow | **PASS** | body fixed; drawings scroll |
| lighting.html: no external assets | **PASS** | none |
| lighting.html: local links | **PASS** | 7 links checked |
| lighting.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| lighting.html: scale/ruler | **PASS** | declared per exploded strip |
| lighting.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| lighting.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| lighting.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/speed_sensor.html | **PASS** | 10_assembly_architecture/viz/connections/speed_sensor.html |
| speed_sensor.html: CSP | **PASS** | inline-only CSP present |
| speed_sensor.html: theme | **PASS** | media preference + explicit overrides |
| speed_sensor.html: overflow | **PASS** | body fixed; drawings scroll |
| speed_sensor.html: no external assets | **PASS** | none |
| speed_sensor.html: local links | **PASS** | 4 links checked |
| speed_sensor.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| speed_sensor.html: scale/ruler | **PASS** | declared per exploded strip |
| speed_sensor.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| speed_sensor.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| speed_sensor.html: order strip | **PASS** | short linked sequence present |
| HTML exists: connections/body_shell.html | **PASS** | 10_assembly_architecture/viz/connections/body_shell.html |
| body_shell.html: CSP | **PASS** | inline-only CSP present |
| body_shell.html: theme | **PASS** | media preference + explicit overrides |
| body_shell.html: overflow | **PASS** | body fixed; drawings scroll |
| body_shell.html: no external assets | **PASS** | none |
| body_shell.html: local links | **PASS** | 10 links checked |
| body_shell.html: exploded SVG | **PASS** | 1 inline SVG(s) |
| body_shell.html: scale/ruler | **PASS** | declared per exploded strip |
| body_shell.html: confidence style | **PASS** | solid/dotted/dashed-hatched legend |
| body_shell.html: real mesh silhouette | **PASS** | embedded data-URI mesh silhouette(s) |
| body_shell.html: order strip | **PASS** | short linked sequence present |
| HTML Joint-ID coverage | **PASS** | 160/160 unique IDs |
| zone master links connection atlas | **PASS** | generated connection block present |
| zone master links all assemblies | **PASS** | 12 direct assembly links |
| requested joint-family coverage | **PASS** | all requested families found |

**Verdict: PASS — 160/160 checks passed.**
