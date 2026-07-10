# Review list — rejected & uncertain models

Per-file reasons for everything NOT staged for printing. Originals stay untouched in
`unsorted_stl_raw/`. Decision context and gates: `MODEL_INVENTORY.md`. If a decision
changes: update the inventory (MD + CSV), stage the file with a MANIFEST row, and move
its entry out of here.

## UNCERTAIN — parked behind human gates (do not print yet)

*(2026-07-10 second pass: `FRONTNOSE2024`, `2024 Revised Front Wing`, `Servoholder`
moved OUT to REQUIRED — Gate B front / Gate D resolved via drawings [5], [2], [3] and
the 2024-body README. Seven rear-wing/DRS files moved IN from the rejected tiers —
the user reinstated DRS (BOM v2 orders an MG90S for it). Gate A text expanded after
reading drawing [7].)*

| File | Location | Material if selected | Uncertainty | Gate / required check |
|---|---|---|---|---|
| `Diffuser backplate.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Rear Axle Upgrades` | ASA or PETG | medium | needed iff Gate A resolves to the Rev-1 stack — drawing [7] bolts diffuser + rear wing + backplate together |
| `Rear Back Motor Cover REVISION 1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Rear Axle Upgrades` | ASA if selected | medium | GATE A: confirm Spring mount 2 REVISION 1 seats the 68mm coilover in slicer; fits -> Rev-1 stack (bearings seat in these covers per [7] — check whether Left/Rightrearaxle are replaced), else original stack; resolve together with the rear-wing gate |
| `Rear Left Motor Cover REVISION 1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Rear Axle Upgrades` | ASA if selected | medium | GATE A (same as above) |
| `Rear Right Motor Cover REVISION 1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Rear Axle Upgrades` | ASA if selected | medium | GATE A (same as above) |
| `RearSpringMountREV4.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Rear Suspension` | ASA if selected | high | GATE A (same as above) — only if the rocker does NOT fit |
| `Spring Block.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Rear Axle Upgrades` | ASA if selected | high | GATE A (same as above) |
| `Spring mount 2 REVISION 1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Rear Axle Upgrades` | ASA if selected | high | GATE A (same as above) |
| `springblock.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Rear Suspension` | ASA if selected | high | GATE A (same as above) — only if the rocker does NOT fit |
| `2021Rearwing with DRS.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2021 Upgrades` | PLA or PETG | medium | REAR-WING/DRS GATE: pairs with the ORIGINAL rear stack — drawings [0]/[2] show it mounted with a DRS-servo pocket + metal-rod linkage; pick wing together with Gate A in Bambu Studio |
| `2021Rearwingflapdeco.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2021 Upgrades/DECO Painting Parts` | PLA | medium | REAR-WING/DRS GATE: colour-split flap deco — only if the 2021 wing is chosen |
| `MCL60 2023 Rear Wing.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Body Parts` | PLA or PETG | medium | REAR-WING/DRS GATE: very likely drawing [7]'s "Revised rear wing" (only rear-wing STL in the Rev-1 release); pairs with the Rev-1 stack + DRS Arm for 2023; McLaren-shaped but painted black anyway |
| `DRS Arm for 2021 Rear Wing.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Experimental Parts` | PETG | medium | REAR-WING/DRS GATE: 58mm actuation arm for the 2021 wing |
| `DRS Arm for 2023 Rear Wing.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Experimental Parts` | PETG | medium | REAR-WING/DRS GATE: 63.8mm actuation arm for the 2023-style wing |
| `Print_In_Place DRSv2.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2023 Upgrades` | PLA or PETG | high | REAR-WING/DRS GATE: newest DRS design by name, but no drawing covers it; PIP hinge = printability risk; mounting unverified |
| `DRS Diffuser.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Floor` | PETG | high | REAR-WING/DRS GATE: floor-diffuser variant for a DRS install — compare against required Diffuser.stl once the wing is chosen |
| `camera 2 colour.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts` | PETG or PLA | low | GATE C: camera on hand (owned+flashed); measure it now, blower in transit — probably unneeded (camera top 1.1 selected) |
| `camera_blower_duct.scad` | `unsorted_stl_raw` | PETG | high | GATE C: measure camera (on hand) + ACP2006-class blower (in transit), set the 9 params, render STL |
| `cameranose.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts` | PETG or PLA | low | GATE C (same as camera 2 colour) |
| `f104camera.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts` | PETG or PLA | low | GATE C (same as camera 2 colour) |
| `pin.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | PLA or PETG | low | 2024 body mounts with 3x M3 bolts (README) — pins probably unneeded; confirm no pin holes remain when shells are in the slicer |

## REJECTED — Wrong livery / era (39)

Team- or era-specific shells and aero. We paint W17 on the generic 2024 shell.
*(2026-07-10: `2021Rearwing with DRS`, `2021Rearwingflapdeco`, `MCL60 2023 Rear Wing`
moved to UNCERTAIN — rear-wing/DRS gate.)*

| File | Location | Reason |
|---|---|---|
| `2021 front wing sides.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2021 Upgrades/DECO Painting Parts` | 2021-era body/aero |
| `2021 front wing wing.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2021 Upgrades` | 2021-era body/aero |
| `2021deco.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2021 Upgrades/DECO Painting Parts` | 2021-era body/aero |
| `2021sidevent2.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Floor` | 2021-era body/aero |
| `2023 Front Wingsplit.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2023 Upgrades` | 2023-era body/aero (2023 top-body chassis line, not our 2024 shell) |
| `2023 Top Body RB19.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | 2023-era body/aero (2023 top-body chassis line, not our 2024 shell) |
| `2023 Top Body2.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | 2023-era body/aero (2023 top-body chassis line, not our 2024 shell) |
| `2023NewSidepodsopen.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | 2023-era body/aero (2023 top-body chassis line, not our 2024 shell) |
| `2023WINGDECO.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2023 Upgrades/colour decoration` | 2023-era body/aero (2023 top-body chassis line, not our 2024 shell) |
| `2023WINGDECO2.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2023 Upgrades/colour decoration` | 2023-era body/aero (2023 top-body chassis line, not our 2024 shell) |
| `2023WINGDECO3.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2023 Upgrades/colour decoration` | 2023-era body/aero (2023 top-body chassis line, not our 2024 shell) |
| `FRONT BODY BLACK.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `FRONT BODY MULTICOLOUR.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `FRONT BODY ORANGE 1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `FRONT BODY ORANGE 2.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `FRONT BODY ORANGE 3.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `FRONT WING MCL38 ORANGE 1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `FRONTNOSE BLACK.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `FRONTNOSE MULTICOLOUR.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `FRONTNOSE ORANGE.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `FRONTNOSE2021.stl` | `unsorted_stl_raw/RC-01 Revision 1 Files/Body Upgrades` | 2021-era body/aero |
| `FRONTNOSE2023tighterpins.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | 2023-era body/aero (2023 top-body chassis line, not our 2024 shell) |
| `LargerturningvaneLeft.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | 2023-era body/aero (2023 top-body chassis line, not our 2024 shell) |
| `LargerturningvaneRight.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | 2023-era body/aero (2023 top-body chassis line, not our 2024 shell) |
| `NEW BODY 2024 FRONT 1 SF24.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Ferrari SF 24` | Ferrari SF24 shell - we paint W17 on generic 2024 |
| `NEW BODY 2024 REAR BLACK.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `NEW BODY 2024 REAR ORANGE 1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `NEW BODY 2024 REAR ORANGE 2.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `NEW BODY 2024 REAR ORANGE 3.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `NEW BODY 2024 REAR ORANGE 4.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Mclaren mcl38` | McLaren MCL38 colour-split shell |
| `NEW BODY 2024 REAR SF24.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 2024 Body/Ferrari SF 24` | Ferrari SF24 shell - we paint W17 on generic 2024 |
| `NewFrontNose SF24.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Body Parts` | Ferrari SF24 shell - we paint W17 on generic 2024 |
| `NewFrontNose2021_3.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | 2021-era body/aero |
| `cameratopsf23.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts` | Ferrari SF23 variant |
| `pinsf23.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | Ferrari SF23 variant |
| `sf23horn.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts` | Ferrari SF23 variant |
| `sf23sharkfin.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts` | Ferrari SF23 variant |
| `sf23topbody.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | Ferrari SF23 variant |
| `sharkfinnew2021.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts` | 2021-era body/aero |

## REJECTED — Wrong chassis revision (18)

Revision 1/1.1 ball-joint front + revision floors. Locked config = original oil-shock.

| File | Location | Reason |
|---|---|---|
| `ARM1 extended bottom Left.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Front Axle Upgrades` | Revision-1 front axle upgrade set - locked config uses original front |
| `ARM1 extended bottom Right.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Front Axle Upgrades` | Revision-1 front axle upgrade set - locked config uses original front |
| `ARM1 extended bottom.stl` | `unsorted_stl_raw/RC-01 Revision 1 Files/Front Axle Upgrades` | Revision-1 front axle upgrade set - locked config uses original front |
| `ARM1 extended.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Front Axle Upgrades` | Revision-1 front axle upgrade set - locked config uses original front |
| `Armblock.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Front Axle Upgrades` | Revision-1 front axle upgrade set - locked config uses original front |
| `New Left Wheel Hub.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 1.1 Steering Upgrades` | Rev 1.1 ball-joint steering - incompatible with locked oil-shock front |
| `New Right Wheel Hub.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 1.1 Steering Upgrades` | Rev 1.1 ball-joint steering - incompatible with locked oil-shock front |
| `New Steering Arm with Ball Joint Left.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 1.1 Steering Upgrades` | Rev 1.1 ball-joint steering - incompatible with locked oil-shock front |
| `New Steering Arm with Ball Joint Right.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 1.1 Steering Upgrades` | Rev 1.1 ball-joint steering - incompatible with locked oil-shock front |
| `New Steering Servo Holder.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 1.1 Steering Upgrades` | Rev 1.1 ball-joint steering - incompatible with locked oil-shock front |
| `NewBackFloorSuspension UpgradeBack REVISION 1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Floor Upgrades` | Revision-1 suspension floor - locked config uses original floor |
| `NewBackFloorSuspension UpgradeFront3 REVISION 1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Floor Upgrades` | Revision-1 suspension floor - locked config uses original floor |
| `NewFrontFloorSuspensionUpgrade REVISION 1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Floor Upgrades` | Revision-1 suspension floor - locked config uses original floor |
| `NewFrontFloorSuspensionUpgrade REVISION_1.1.stl` | `unsorted_stl_raw/RC-01 Revision 1.1/New 1.1 Steering Upgrades` | Rev 1.1 ball-joint steering - incompatible with locked oil-shock front |
| `Servomount for steering bottom.stl` | `unsorted_stl_raw/RC-01 Revision 1 Files/Front Axle Upgrades` | Revision-1 front axle upgrade set - locked config uses original front |
| `Servomount for steering.stl` | `unsorted_stl_raw/RC-01 Revision 1 Files/Front Axle Upgrades` | Revision-1 front axle upgrade set - locked config uses original front |
| `Steering Arm 1.stl` | `unsorted_stl_raw/RC-01 Revision 1 Files/Front Axle Upgrades` | Revision-1 front axle upgrade set - locked config uses original front |
| `Steering Block 12x5x3 Bearings .stl` | `unsorted_stl_raw/RC-01 Revision 1 Files/Front Axle Upgrades` | Revision-1 front axle upgrade set - locked config uses original front |

## REJECTED — Superseded versions (9)

An explicitly newer/other part replaces each of these.
*(2026-07-10: both `DRS Arm`s, `DRS Diffuser`, `Print_In_Place DRSv2` moved to
UNCERTAIN — DRS is back in the build.)*

| File | Location | Reason |
|---|---|---|
| `2024 halo.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts` | Superseded by new halo 2.1 |
| `F104 tyreslot1 no grubs.stl` | `unsorted_stl_raw/RC-01 Revision 1 Files/Rear Axle Upgrades` | Superseded by the 'tighter' Rev1.1 adapters |
| `F104 tyreslot2 no grubs.stl` | `unsorted_stl_raw/RC-01 Revision 1 Files/Rear Axle Upgrades` | Superseded by the 'tighter' Rev1.1 adapters |
| `Mirrors 2024.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts` | Superseded by NEW BODY 2024 Mirror |
| `NewRearCovertighterholes.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/General Parts` | Old rear covers - 2024 REAR shell replaces them |
| `Newinvaxle2full.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Mechanical Parts` | Old invert-axle parts - belt-drive rear uses Left/Rightrearaxle |
| `RCRNewRearCover rev1.stl` | `unsorted_stl_raw/RC-01 Revision 1 Files/Body Upgrades` | Old rear covers - 2024 REAR shell replaces them |
| `cameratop.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Decoration Parts` | Superseded by camera top 1.1 |
| `newinvaxleextended.stl` | `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/Mechanical Parts` | Old invert-axle parts - belt-drive rear uses Left/Rightrearaxle |

## DUPLICATES (22)

Identical-name second copies; the canonical path is recorded in the CSV. Never printed from.

- `unsorted_stl_raw/RC-01 Revision 1 Files/Body Upgrades/2024 Revised Front Wing.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Body Upgrades/MCL60 2023 Rear Wing.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Extra Parts/fulldrivercut2.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Extra Parts/wall mount.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Floor Upgrades/NewBackFloorSuspension UpgradeBack REVISION 1.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Floor Upgrades/NewBackFloorSuspension UpgradeFront3 REVISION 1.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Floor Upgrades/NewFrontFloorSuspensionUpgrade REVISION 1.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Front Axle Upgrades/ARM1 extended.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Front Axle Upgrades/Armblock.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Rear Axle Upgrades/Axle Main no grubs.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Rear Axle Upgrades/Diffuser backplate.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Rear Axle Upgrades/Rear Back Motor Cover REVISION 1.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Rear Axle Upgrades/Rear Left Motor Cover REVISION 1.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Rear Axle Upgrades/Rear Right Motor Cover REVISION 1.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Rear Axle Upgrades/Spring Block.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Rear Axle Upgrades/Spring mount 2 REVISION 1.stl`
- `unsorted_stl_raw/RC-01 Revision 1 Files/Rear Axle Upgrades/rearbacklightdiffuser.stl`
- `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Body Parts/NewFrontNose2021_3.stl`
- `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Body Parts/cameranose.stl`
- `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Floor Upgrades/2023NEWSideVent1.stl`
- `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Floor Upgrades/2023NEWSideVent2.stl`
- `unsorted_stl_raw/RC-01 Revision 1.1/Original + Revision 1 Files pre-released to fully build the car/RC-01 Revision 1 Files/Floor Upgrades/FloorBoard2.stl`
