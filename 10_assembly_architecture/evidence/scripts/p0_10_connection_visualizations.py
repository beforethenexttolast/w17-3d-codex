#!/usr/bin/env python3
"""Generate the W17 mechanical connection register, build sequence and diagrams.

This is an execution layer over the existing assembly evidence.  It does not
change a source STL, fit result, placement, gate, or conclusion.  Exact
interfaces come only from the existing STL evidence or controlled documents;
otherwise the row is explicitly ASSUMPTION and carries an ASM physical check.

Outputs:
  10_assembly_architecture/Z_connection_joint_register.{md,csv}
  generated joint block in P_assembly_master_manual.md
  10_assembly_architecture/viz/connections/*.html
  a generated link block in 10_assembly_architecture/viz/index.html

Run from the repository root:

    python3 10_assembly_architecture/evidence/scripts/p0_10_connection_visualizations.py
"""
from __future__ import annotations

import base64
import csv
from dataclasses import dataclass, asdict
import hashlib
import html
import io
import math
from pathlib import Path
import re
import struct
import zlib

import numpy as np
import trimesh


REPO = Path(__file__).resolve().parents[3]
ARCH = REPO / "10_assembly_architecture"
VIZ = ARCH / "viz"
OUT = VIZ / "connections"
REGISTER_MD = ARCH / "Z_connection_joint_register.md"
REGISTER_CSV = ARCH / "Z_connection_joint_register.csv"
MANUAL = ARCH / "P_assembly_master_manual.md"
MASTER_INDEX = VIZ / "index.html"

MANUAL_START = "<!-- BEGIN GENERATED JOINT BUILD SEQUENCE · p0_10 -->"
MANUAL_END = "<!-- END GENERATED JOINT BUILD SEQUENCE · p0_10 -->"
INDEX_START = "<!-- BEGIN GENERATED CONNECTION LINKS · p0_10 -->"
INDEX_END = "<!-- END GENERATED CONNECTION LINKS · p0_10 -->"


@dataclass(frozen=True)
class Part:
    name: str
    mesh: str = ""
    shape: str = "box"
    dims: tuple[float, float] | None = None
    confidence: str = "ASSUMPTION"


@dataclass(frozen=True)
class Joint:
    joint_id: str
    zone: str
    assembly: str
    order: float
    asm_step: str
    part_a: str
    part_b: str
    hardware: str
    interface: str
    fastening_retention: str
    dependency: str
    instruction: str
    tool: str
    torque_threadlock: str
    confidence: str
    asm_check: str
    disposition: str
    evidence: str


ASSEMBLIES = {
    "floor": ("01", "Floor datum & chassis structure", "floor_structure.html"),
    "servo": ("02", "Steering servo & holder", "servo_holder.html"),
    "steering": ("03", "Steering output chain", "steering.html"),
    "front": ("04", "Front suspension & rolling", "front_suspension.html"),
    "rear": ("05", "Rear suspension & drivetrain", "rear_drivetrain.html"),
    "power": ("06", "Battery, power & onboard charging", "power_charge.html"),
    "electronics": ("07", "Electronics trays & RF hardware", "electronics_trays.html"),
    "camera": ("08", "Camera pod, gimbal & blower", "camera_blower.html"),
    "audio": ("09", "Audio assembly", "audio.html"),
    "lighting": ("10", "Lighting segments & lenses", "lighting.html"),
    "sensor": ("11", "Hall speed sensor", "speed_sensor.html"),
    "body": ("12", "Body, shell & aero fasteners", "body_shell.html"),
}


def p(group: str, name: str) -> str:
    return f"02_ready_to_slice/{group}/{name}"


PARTS = {
    # Floor / donor structure
    "front_floor": Part("2023 front floor", p("05_PETG_floor", "2023NewFrontFloorLargerParts.stl"), confidence="VERIFIED"),
    "rear_floor": Part("2023 rear floor", p("05_PETG_floor", "2023NewBackFloorLargerParts.stl"), confidence="VERIFIED"),
    "rear_floor_2": Part("rear floor 2", p("05_PETG_floor", "2023NewBackFloorLargerPart2.stl"), confidence="VERIFIED"),
    "floorboard": Part("FloorBoard2", p("05_PETG_floor", "FloorBoard2.stl"), confidence="VERIFIED"),
    "vent_l": Part("side vent L", p("05_PETG_floor", "2023NEWSideVent1.stl"), confidence="VERIFIED"),
    "vent_r": Part("side vent R", p("05_PETG_floor", "2023NEWSideVent2.stl"), confidence="VERIFIED"),
    "diffuser": Part("floor diffuser", p("05_PETG_floor", "Diffuser.stl"), confidence="VERIFIED"),
    "servo_holder": Part("Servoholder", p("05_PETG_floor", "Servoholder.stl"), confidence="VERIFIED"),
    # Steering / front
    "steer_servo": Part("DS3235SG servo", shape="servo", dims=(40.0, 40.5), confidence="DOCUMENTED"),
    "horn": Part("25T metal horn", shape="horn", dims=(47.0, 8.0), confidence="DOCUMENTED"),
    "ball_stud": Part("M3 ball stud", shape="ball", dims=(10.0, 6.0), confidence="DOCUMENTED"),
    "rod_end_m4": Part("M4 rod-end", shape="rodend", dims=(24.0, 10.0), confidence="DOCUMENTED"),
    "tie_end_m3": Part("3Racing M3 tie-rod end", shape="rodend", dims=None, confidence="DOCUMENTED"),
    "tie_rod_m4": Part("M4 threaded rod cut ≈22 mm", shape="rod", dims=(22.0, 4.0), confidence="DOCUMENTED"),
    "turnbuckle": Part("3×32 turnbuckle", shape="rod", dims=(32.0, 3.0), confidence="DOCUMENTED"),
    "servo_saver": Part("servosaverv7", p("03_PETG_front_suspension_steering", "servosaverv7.stl"), confidence="VERIFIED"),
    "susp_block": Part("Suspension Block_10", p("03_PETG_front_suspension_steering", "Suspension Block_10.stl"), confidence="VERIFIED"),
    "crossarm": Part("Crossarm3_extended", p("03_PETG_front_suspension_steering", "Crossarm3_extended.stl"), confidence="VERIFIED"),
    "arm": Part("Arm4", p("03_PETG_front_suspension_steering", "Arm4.stl"), confidence="VERIFIED"),
    "guide_rod": Part("GuideRod / D5×M3 sleeve", p("03_PETG_front_suspension_steering", "GuideRod.stl"), confidence="VERIFIED"),
    "upright_l": Part("front upright L", p("03_PETG_front_suspension_steering", "2023WheelHubsSuspension5mir.stl"), confidence="VERIFIED"),
    "upright_r": Part("front upright R", p("03_PETG_front_suspension_steering", "2023WheelHubsSuspension5.stl"), confidence="VERIFIED"),
    "steering_block": Part("Steering Block4", p("03_PETG_front_suspension_steering", "Steering Block4.stl"), confidence="VERIFIED"),
    "kingpin": Part("M3×30 king pin", shape="pin", dims=(30.0, 3.0), confidence="DOCUMENTED"),
    "front_shock": Part("52 mm front shock", shape="shock", dims=(52.0, 12.0), confidence="DOCUMENTED"),
    "front_bearing": Part("8×12×3.5 bearing", shape="bearing", dims=(12.0, 12.0), confidence="DOCUMENTED"),
    "front_hub": Part("front rotating hub", p("04_PETG_wheels", "Front_Right_Wheel_Hub_2022_F104.stl"), confidence="VERIFIED"),
    "front_rim": Part("front F104 rim", p("04_PETG_wheels", "Front_Rim_F1_2022.stl"), confidence="VERIFIED"),
    "front_locknut": Part("front locking nut", p("04_PETG_wheels", "Front_Locking_Nut_F1_2022.stl"), confidence="VERIFIED"),
    "front_tyre": Part("Tamiya F104 front tyre", shape="tyre", dims=(64.0, 30.0), confidence="DOCUMENTED"),
    # Rear
    "rear_carrier_l": Part("rear axle carrier L", p("02_ASA_rear_drivetrain", "Leftrearaxle.stl"), confidence="VERIFIED"),
    "rear_carrier_r": Part("rear axle carrier R", p("02_ASA_rear_drivetrain", "Rightrearaxle.stl"), confidence="VERIFIED"),
    "rear_bearing": Part("12×21×5 rear bearing", shape="bearing", dims=(21.0, 21.0), confidence="DOCUMENTED"),
    "output_shaft": Part("belt-set output shaft", shape="shaft", dims=(115.0, 12.0), confidence="DOCUMENTED"),
    "metal_spacer": Part("14 mm-ID metal spacer", shape="sleeve", dims=(18.0, 18.0), confidence="DOCUMENTED"),
    "spacer_l": Part("left printed spacer", p("02_ASA_rear_drivetrain", "Left Spacer for long axle.stl"), confidence="VERIFIED"),
    "spacer_r": Part("right printed spacer", p("02_ASA_rear_drivetrain", "Right Spacer for long axle.stl"), confidence="VERIFIED"),
    "spacer_new_l": Part("NewSpacerleft", p("02_ASA_rear_drivetrain", "NewSpacerleft.stl"), confidence="VERIFIED"),
    "spacer_new_r": Part("NewSpacerright", p("02_ASA_rear_drivetrain", "NewSpacerright.stl"), confidence="VERIFIED"),
    "pulley": Part("belt-set axle pulley", shape="pulley", dims=(36.0, 10.0), confidence="ASSUMPTION"),
    "spur": Part("75T 48P spur", shape="gear", dims=(40.75, 5.0), confidence="DOCUMENTED"),
    "pinion": Part("28T 48P pinion", shape="gear", dims=(15.88, 8.0), confidence="DOCUMENTED"),
    "motor": Part("Rocket 540 V3 motor", shape="motor", dims=(54.0, 36.0), confidence="DOCUMENTED"),
    "motor_lock": Part("beltdrivemotorlock", p("02_ASA_rear_drivetrain", "beltdrivemotorlock.stl"), confidence="VERIFIED"),
    "belt": Part("140 mm belt", shape="belt", dims=(70.0, 35.0), confidence="DOCUMENTED"),
    "rear_rim": Part("rear F104 rim", p("04_PETG_wheels", "Rear_Rim_F1_2022.stl"), confidence="VERIFIED"),
    "tyreslot_1": Part("F104 tyreslot1 tighter", p("04_PETG_wheels", "F104 tyreslot1 no grubs tighter.stl"), confidence="VERIFIED"),
    "tyreslot_2": Part("F104 tyreslot2 tighter", p("04_PETG_wheels", "F104 tyreslot2 no grubs tighter.stl"), confidence="VERIFIED"),
    "rear_locknut": Part("rear locking nut", p("04_PETG_wheels", "Rear_Locking_Nut_F1_2022.stl"), confidence="VERIFIED"),
    "rear_tyre": Part("Tamiya F104 rear tyre", shape="tyre", dims=(64.0, 35.0), confidence="DOCUMENTED"),
    "rear_shock": Part("68 mm rear shock", shape="shock", dims=(68.0, 14.0), confidence="DOCUMENTED"),
    "rear_spring_mount": Part("rear spring mount / rocker", "unsorted_stl_raw/Ryans Creations Open RC F1 Car/Rear Suspension/RearSpringMountREV4.stl", confidence="VERIFIED"),
    "spring_block": Part("spring block", "unsorted_stl_raw/Ryans Creations Open RC F1 Car/Rear Suspension/springblock.stl", confidence="VERIFIED"),
    "rear_wing": Part("preferred 2021 DRS rear wing", "unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/2021 Upgrades/2021Rearwing with DRS.stl", confidence="VERIFIED"),
    "drs_servo": Part("MG90S DRS servo", shape="servo", dims=(22.8, 28.5), confidence="DOCUMENTED"),
    "drs_arm": Part("DRS Arm for 2021 wing", "unsorted_stl_raw/Ryans Creations Open RC F1 Car/Experimental Parts/DRS Arm for 2021 Rear Wing.stl", confidence="VERIFIED"),
    # Supports / power
    "ps01": Part("PS-01 battery tray (DIAG-CAD)", "10_assembly_architecture/cad/generated/stl/cad02_ps01_battery_tray.stl", confidence="ASSUMPTION"),
    "battery": Part("2S pack ≤75×45×25", shape="battery", dims=(75.0, 45.0), confidence="DOCUMENTED"),
    "ps03": Part("PS-03 UBEC shelf (DIAG-CAD)", "10_assembly_architecture/cad/generated/stl/cad04_ps03_ubec_shelf.stl", confidence="ASSUMPTION"),
    "ubec": Part("5 A UBEC", shape="inline", dims=(30.0, 14.0), confidence="ASSUMPTION"),
    "cap": Part("rail capacitor", shape="cap", dims=(20.0, 10.0), confidence="ASSUMPTION"),
    "ps15": Part("PS-15 junction support (DIAG-CAD)", "10_assembly_architecture/cad/generated/stl/cad08_ps15_junction_support.stl", confidence="ASSUMPTION"),
    "charge_module": Part("USB-C 2S balancing charge module · 30×25×10 TARGET · SKU TBD", shape="board", dims=(30.0, 25.0), confidence="ASSUMPTION"),
    "charge_pocket": Part("parametric charge-module pocket", shape="bracket", dims=None, confidence="ASSUMPTION"),
    "charge_port": Part("hidden USB-C charge port", shape="port", dims=None, confidence="ASSUMPTION"),
    "charge_interlock": Part("charge/run interlock", shape="switch", dims=None, confidence="ASSUMPTION"),
    # New lift-out cassette architecture.  These are interface envelopes only;
    # p0_12 owns the physical fit audit and no production mesh exists.
    "cassette_fixed_frame": Part("cassette external four-point saddle / clamp · topology TBD", shape="plate", dims=None, confidence="ASSUMPTION"),
    "cassette_box": Part("lift-out electronics cassette stepped-T gauge", shape="box", dims=(77.0, 86.0), confidence="ASSUMPTION"),
    "cassette_deck": Part("cassette insulated rear service deck", shape="plate", dims=(32.0, 36.0), confidence="ASSUMPTION"),
    "cassette_wall_l": Part("cassette left interior mini-board wall seat", shape="bracket", dims=(39.0, 31.0), confidence="ASSUMPTION"),
    "cassette_wall_r": Part("cassette right interior mini-board wall seat", shape="bracket", dims=(39.0, 31.0), confidence="ASSUMPTION"),
    "pdb": Part("power-distribution board · 55×45×18 TARGET", shape="board", dims=(55.0, 45.0), confidence="ASSUMPTION"),
    "cockpit_pedestal": Part("hollow cut-through cockpit pedestal", shape="post", dims=None, confidence="ASSUMPTION"),
    "pedestal_conduit": Part("pedestal shielded-USB4 / 2×3-pin conduit · 10×18 clear TARGET", shape="inline", dims=(18.0, 10.0), confidence="ASSUMPTION"),
    "cassette_dock": Part("ganged cassette umbilical dock", shape="port", dims=None, confidence="ASSUMPTION"),
    "xt_seat": Part("cassette XT60 / XT30 power-seat bank", shape="port", dims=(60.0, 12.0), confidence="ASSUMPTION"),
    "servo_seat": Part("cassette 5× 3-pin servo-seat bank", shape="port", dims=(58.0, 10.0), confidence="ASSUMPTION"),
    "signal_seat": Part("cassette JST-XH / shielded-USB4 signal-seat bank", shape="port", dims=(64.0, 10.0), confidence="ASSUMPTION"),
    # Electronics
    "ps04": Part("PS-04 electronics deck", shape="plate", dims=(130.0, 55.0), confidence="ASSUMPTION"),
    "ps05": Part("PS-05 deck post (DIAG-CAD)", "10_assembly_architecture/cad/generated/stl/cad06_ps05_post_h20.stl", confidence="ASSUMPTION"),
    "esp32": Part("dual-core ESP32-WROOM-32 D1-Mini-ESP32 / MH-ET Live MiniKit", shape="board", dims=(39.0, 31.0), confidence="DOCUMENTED"),
    "rp1": Part("RadioMaster RP1", shape="board", dims=(13.0, 11.0), confidence="ASSUMPTION"),
    "ps06": Part("PS-06 RX carrier", shape="bracket", dims=(30.0, 20.0), confidence="ASSUMPTION"),
    "wifi": Part("BL-M8812EU2 WiFi module", shape="board", dims=(60.0, 32.0), confidence="ASSUMPTION"),
    "heatsink": Part("28×28×3 heatsink", shape="fins", dims=(28.0, 28.0), confidence="DOCUMENTED"),
    "antenna_post": Part("PS-12 antenna post", shape="post", dims=(35.0, 8.0), confidence="ASSUMPTION"),
    "antenna": Part("5.8 GHz U.FL whip", shape="antenna", dims=(70.0, 6.0), confidence="DOCUMENTED"),
    "cable_comb": Part("PS-08 cable comb", shape="clip", dims=(18.0, 12.0), confidence="ASSUMPTION"),
    # Camera
    "camera_top": Part("camera top 1.1 pod", p("06_PLA_body_shell", "camera top 1.1.stl"), confidence="VERIFIED"),
    "ps10": Part("PS-10 gimbal base", shape="bracket", dims=(55.0, 45.0), confidence="ASSUMPTION"),
    "ps11": Part("PS-11 blower/duct interface", shape="bracket", dims=None, confidence="ASSUMPTION"),
    "pan_servo": Part("MG90S pan servo", shape="servo", dims=(22.8, 28.5), confidence="DOCUMENTED"),
    "tilt_servo": Part("MG90S tilt servo", shape="servo", dims=(22.8, 28.5), confidence="DOCUMENTED"),
    "camera": Part("SSC338Q + IMX335 camera", shape="camera", dims=None, confidence="ASSUMPTION"),
    "blower": Part("5 V blower", shape="blower", dims=None, confidence="ASSUMPTION"),
    "duct": Part("camera blower duct", shape="duct", dims=None, confidence="ASSUMPTION"),
    # Audio / light / sensor
    "amp": Part("MAX98357A amplifier", shape="board", dims=(19.4, 17.8), confidence="ASSUMPTION"),
    "ps14": Part("PS-14 speaker carrier", shape="ring", dims=None, confidence="ASSUMPTION"),
    "speaker": Part("4 Ω 3 W speaker", shape="speaker", dims=(40.0, 40.0), confidence="ASSUMPTION"),
    "led": Part("WS2812B segment", shape="led", dims=(33.3, 10.0), confidence="DOCUMENTED"),
    "rear_lens": Part("rearbacklightdiffuser", p("07_translucent_diffuser", "rearbacklightdiffuser.stl"), confidence="VERIFIED"),
    "ps18": Part("PS-18 light anchor / lens", shape="bracket", dims=None, confidence="ASSUMPTION"),
    "halo": Part("new halo 2.1", p("06_PLA_body_shell", "new halo 2.1.stl"), confidence="VERIFIED"),
    "hall": Part("A3144 Hall sensor", shape="hall", dims=(4.17, 3.1), confidence="DOCUMENTED"),
    "magnet": Part("Ø3×1 magnet", shape="magnet", dims=(3.0, 3.0), confidence="DOCUMENTED"),
    "ps16": Part("PS-16 Hall bracket", shape="bracket", dims=(15.0, 12.0), confidence="ASSUMPTION"),
    # Body
    "body_front": Part("NEW BODY 2024 FRONT", p("06_PLA_body_shell", "NEW BODY 2024 FRONT 1.stl"), confidence="VERIFIED"),
    "body_rear": Part("NEW BODY 2024 REAR", p("06_PLA_body_shell", "NEW BODY 2024 REAR.stl"), confidence="VERIFIED"),
    "nose": Part("FRONTNOSE2024", p("06_PLA_body_shell", "FRONTNOSE2024.stl"), confidence="VERIFIED"),
    "front_wing": Part("2024 revised front wing", p("06_PLA_body_shell", "2024 Revised Front Wing.stl"), confidence="VERIFIED"),
    "mirror": Part("2024 mirror", p("06_PLA_body_shell", "NEW BODY 2024 Mirror.stl"), confidence="VERIFIED"),
    "insert": Part("M3×5 heat-set insert", shape="insert", dims=(5.0, 5.0), confidence="DOCUMENTED"),
}


MODE = {
    "M3": (
        "M3 bolt from 8/10/12/20/30 mm BOM kit + M3 nut where through; exact length ASSUMPTION",
        "screw; captive/standard nut where the drawing shows a slot; no insert unless this row names one",
        "matching 1.5/2/2.5 mm hex driver + nut driver; confirm supplied head",
        "Plastic: snug only. Metal–metal: low-strength threadlock after dry fit. No numeric torque is documented.",
    ),
    "M3X8": (
        "M3×8 bolt from BOM kit + mapped floor slot nut",
        "screw into captive floor nut; reversible",
        "matching hex driver + nut driver if the captive nut is not yet seated",
        "Snug only against printed support. Threadlock only if both engaged threads are metal.",
    ),
    "INSERT": (
        "heat-set M3×5 brass insert + M3 bolt from BOM kit; exact bolt length ASSUMPTION",
        "insert heat-set square to boss; service screw retained by metal thread",
        "temperature-controlled soldering iron + insert tip; matching hex driver after cool-down",
        "Insert with heat only; never torque while hot. Service screw snug; low-strength threadlock only metal–metal.",
    ),
    "PRESS": (
        "specified BOM bearing / press-fit part; no added fastener",
        "square press fit against the correct race/shoulder",
        "arbor press or smooth-jaw vice + square drift; calipers",
        "No screw torque or threadlock. Press on the race supported by the receiving feature.",
    ),
    "PIN": (
        "M3×30 dowel king pin + supplied circlip; no substitute screw unless the physical check selects it",
        "dowel through aligned bores; circlip in the supplied groove",
        "smooth-jaw pliers / light press + circlip pliers; calipers",
        "No threadlock. Do not hammer through a tight printed bore; rework only from a recorded FIT result.",
    ),
    "ROD": (
        "M3 ball stud + M4 rod-end + M4 threaded rod cut to ≈22 mm, all from supplied BOM",
        "rod-end clips on ball; M4 thread carries axial adjustment; ball stud retained by its M3 thread/nut",
        "calipers, fine saw/cutoff tool, file, two small spanners, ball-end pliers if available",
        "Deburr cut rod. Equal thread engagement both ends. Low-strength threadlock only at final metal–metal threads.",
    ),
    "TURNBUCKLE": (
        "M3 ball studs + 3Racing M3 tie-rod ends + 3×32 turnbuckle, all from supplied BOM",
        "tie-rod ends clip to M3 balls; opposite-hand turnbuckle threads provide toe adjustment; ball studs use measured M3 nut/thread retention",
        "calipers, two small spanners and ball-end pliers if available",
        "Equal thread engagement left/right. Low-strength threadlock only at final metal–metal ball-stud threads; keep turnbuckle adjustable.",
    ),
    "HORN": (
        "DS3235SG 25T metal horn + servo's own horn screw",
        "press horn onto 25T spline at neutral; centre screw retains it",
        "servo tester/control setup + matching driver for the supplied horn screw",
        "Seat fully without rocking; final-tighten only after centring. Threadlock only if servo maker permits it.",
    ),
    "BELT": (
        "belt-drive set + 140 mm belt; included pulley hardware only",
        "belt captured by pulley flanges and installed tension; no added keeper invented",
        "hex drivers matching included hardware + straightedge; turn shaft by hand",
        "No numeric tension is documented. Set by the ASM-51 free-rotation check; threadlock only metal–metal screws.",
    ),
    "M4": (
        "M4 bolt / M4 threaded element from listed steering or belt-drive hardware; exact form noted in interface",
        "threaded retention; nut/axle internal thread only if physically present",
        "matching hex driver/spanner; calipers",
        "Do not force printed threads. Low-strength threadlock only metal–metal after free-motion check.",
    ),
    "BOND": (
        "no connector fastener in the supplied joint BOM; bond/adhesive remains ASSUMPTION unless BOM v2 names it",
        "bonded retention after dry fit; no hidden substitute hardware",
        "surface-prep tools + clamp appropriate to the selected, documented adhesive",
        "No torque/threadlock. Do not bond until the named ASM dry-fit and service check pass.",
    ),
    "CLIP": (
        "no added BOM fastener; printed clip/pocket/strap feature only",
        "clip, pocket or strap retention; exact secondary restraint remains ASSUMPTION",
        "hands + calipers; trim tool only after a recorded fit check",
        "No torque/threadlock. Tug-test without loading wires, U.FL, PCB, or component leads.",
    ),
    "TBD_RETENTION": (
        "reversible external four-point retention hardware/topology not selected; no substitute authorized",
        "external saddle/clamp retention; exact tabs, screws/inserts and release method remain ASSUMPTION",
        "transparent full-stack dummy + calipers first; installation tool follows the selected closure",
        "No torque, drilling, bonding or threadlock until CAS-07 selects and records the retention.",
    ),
    "DEFER": (
        "hardware not selected / still in transit; no substitute authorized",
        "DEFER — retention cannot be chosen before the named real part is measured",
        "calipers first; installation tool is selected only after hardware identity closes",
        "No torque, bonding, drilling or threadlock while DEFERRED.",
    ),
    "LAND": (
        "no fastener; designed shell/floor landing contact",
        "gravity/contact landing with nearby registered fasteners carrying retention",
        "feeler gauges + inspection light",
        "No torque/threadlock at the landing itself; do not shim unless a later decision authorizes it.",
    ),
}


JOINTS: list[Joint] = []


def add(
    joint_id: str,
    zone: str,
    assembly: str,
    order: float,
    asm_step: str,
    part_a: str,
    part_b: str,
    mode: str,
    interface: str,
    dependency: str,
    instruction: str,
    confidence: str,
    asm_check: str,
    disposition: str = "READY",
    evidence: str = "",
    hardware: str = "",
    retention: str = "",
    tool: str = "",
    torque: str = "",
) -> None:
    default_hw, default_ret, default_tool, default_torque = MODE[mode]
    JOINTS.append(Joint(
        joint_id, zone, assembly, order, asm_step,
        PARTS[part_a].name, PARTS[part_b].name,
        hardware or default_hw, interface,
        retention or default_ret, dependency, instruction,
        tool or default_tool, torque or default_torque,
        confidence, asm_check, disposition, evidence,
    ))
    PART_KEY_BY_NAME.setdefault(PARTS[part_a].name, part_a)
    PART_KEY_BY_NAME.setdefault(PARTS[part_b].name, part_b)


PART_KEY_BY_NAME: dict[str, str] = {}


# ---- Floor datum and chassis structure ---------------------------------------
add("J-FLR-001", "Z0 floor", "floor", 5.01, "ASM-05", "front_floor", "rear_floor", "M3",
    "Matched tongue/groove at X=0; adjacent STL M3-class features 3.00–3.36 mm [VERIFIED]",
    "ASM-04 inserts/nuts seated", "Slide tongue into groove on DAT-F, clamp flat, then fit the drawing-[2] M3 stack without lifting the seam.",
    "VERIFIED", "ASM-05: straightedge across DAT-F; record any step/rock before tightening.",
    evidence="p0_02 §1 + p0_d01_feature_map.csv; drawing [2]")
add("J-FLR-002", "Z0 floor", "floor", 5.02, "ASM-05", "floorboard", "front_floor", "M3",
    "FloorBoard2 registered underside channel and front-floor M3 features [VERIFIED geometry]; exact bolt length ASSUMPTION",
    "J-FLR-001 loosely assembled", "Offer FloorBoard2 from below, align its forward hole(s), start fasteners two turns, leave loose.",
    "VERIFIED", "ASM-05: confirm FloorBoard2 stays in the recessed underside channel and does not bow DAT-F.",
    evidence="p0_02 FloorBoard2 transform and matched-hole span")
add("J-FLR-003", "Z0 floor", "floor", 5.03, "ASM-05", "floorboard", "rear_floor", "M3",
    "FloorBoard2 rear hole span matches rear-floor features within 0.2 mm [VERIFIED]; exact bolt length ASSUMPTION",
    "J-FLR-002 started loose", "Start rear FloorBoard2 fastener(s), square the floor, then snug front/rear in an alternating pattern.",
    "VERIFIED", "ASM-05: flat-plate rock test after all FloorBoard2 screws are snug.",
    evidence="p0_02 §1")
add("J-FLR-004", "Z0 floor", "floor", 5.04, "ASM-05", "rear_floor", "rear_floor_2", "M3",
    "Two coaxial pairs at X−85.93/L±5.00, 3.00 mm STL features [VERIFIED]",
    "J-FLR-001…003 complete", "Stack rear-floor-2 on the documented lower plane, align both coaxial holes and start both M3 fasteners before snugging.",
    "VERIFIED", "ASM-05: confirm both plates remain coaxial and the bendable tail is free.",
    evidence="p0_d01_feature_map.csv; drawing [2]")
add("J-FLR-005", "Z0 floor", "floor", 5.05, "ASM-05", "vent_l", "front_floor", "M3",
    "Donor M3 mounting topology DOCUMENTED; exact local hole Ø and bolt length unmeasured",
    "Datum floor flat", "Seat left vent on its keyed floor edge; install the shortest BOM M3 bolt that fully engages without protruding into the shell.",
    "DOCUMENTED", "ASM-05: caliper hole and underfloor protrusion; log chosen BOM length.")
add("J-FLR-006", "Z0 floor", "floor", 5.06, "ASM-05", "vent_r", "front_floor", "M3",
    "Donor M3 mounting topology DOCUMENTED; exact local hole Ø and bolt length unmeasured",
    "J-FLR-005 orientation established", "Mirror the left-side sequence; start all vent fasteners before snugging.",
    "DOCUMENTED", "ASM-05: caliper hole and underfloor protrusion; log chosen BOM length.")
add("J-FLR-007", "Z0 floor", "floor", 5.07, "ASM-05", "diffuser", "rear_floor_2", "M3",
    "Diffuser-to-floor screw topology DOCUMENTED; exact feature Ø/count on selected tail ASSUMPTION",
    "J-FLR-004 complete; rear LED pull-through route still open", "Offer diffuser from the rear, align without flex preload, start M3 hardware, and keep the LED channel accessible.",
    "ASSUMPTION", "ASM-05/13: measure feature Ø/count and prove the diffuser can be removed without cutting H-08.",
    disposition="HOLD", evidence="drawing [2]; ASSEMBLY_NOTES Stage 4")

# ---- Steering servo and holder ------------------------------------------------
add("J-SRV-001", "ZS steering", "servo", 6.01, "ASM-06", "servo_holder", "rear_floor", "M3",
    "Floor/holder M3 feature topology DOCUMENTED; holder has no verified insert seat",
    "J-FLR-001…007 complete", "Install the 58 mm holder longitudinally on the rear floor; start both ends before snugging and keep the arch square.",
    "DOCUMENTED", "ASM-06: record floor holes, chosen BOM bolt lengths and whether nuts or plastic threads retain them.")
add("J-SRV-002", "ZS steering", "servo", 6.02, "ASM-06", "steer_servo", "servo_holder", "M3",
    "42×18.5 mm holder arch VERIFIED; servo side face 40×20 mm DOCUMENTED; ear holes/stack ASSUMPTION",
    "J-SRV-001 snug; DS3235SG unpowered", "No-force side-on fit with shaft horizontal/lateral; align both ear pairs and fit BOM M3 hardware only if the ears land without case preload.",
    "ASSUMPTION", "ASM-06: record ear-hole Ø/pitch, spacer stack and the selected 8/10/12/20/30 mm bolt length.",
    disposition="HOLD", evidence="Y steering study §3–4")
add("J-SRV-003", "ZS steering", "servo", 6.03, "ASM-06", "steer_servo", "rear_floor", "LAND",
    "Servo case-to-floor/holder clearance is a physical landing; no direct fastener [ASSUMPTION]",
    "J-SRV-002 dry-fitted", "Confirm the servo body is supported by the holder rather than wedged between floor and arch; retain a lead exit with no pinch.",
    "ASSUMPTION", "ASM-06: 0.1 mm feeler/no-force test around case and lead; STOP if the documented 20 mm face will not pass.")
add("J-SRV-004", "ZS steering", "servo", 7.01, "ASM-07", "steer_servo", "horn", "HORN",
    "25T spline and horn radii 19.5/23.5 mm DOCUMENTED; supplied horn-screw thread not independently measured",
    "J-SRV-002 accepted; servo powered and centred", "At commanded neutral, press the ordinary metal horn onto the 25T spline vertically; install the servo's own horn screw.",
    "DOCUMENTED", "ASM-07: power-cycle centre repeatability ±1° and photograph selected horn-hole radius.",
    evidence="Y steering study §4/§9; user target chain")

# ---- Complete steering output chain ------------------------------------------
add("J-STR-001", "ZS steering", "steering", 8.01, "ASM-08", "horn", "ball_stud", "ROD",
    "Horn outer hole at 19.5 or 23.5 mm radius DOCUMENTED; hole Ø/thread for M3 ball stud ASSUMPTION",
    "J-SRV-004 centred", "Select the least aggressive usable horn radius, fit the M3 ball stud with its supplied nut/thread, and orient the ball toward the rod line.",
    "ASSUMPTION", "ASM-08: gauge horn hole Ø, record 19.5/23.5 selection and retention side.")
add("J-STR-002", "ZS steering", "steering", 8.02, "ASM-08", "ball_stud", "rod_end_m4", "ROD",
    "M3 ball / M4 rod-end pairing is BOM-listed topology; actual ball cup fit ASSUMPTION",
    "J-STR-001 complete", "Press the near M4 rod-end squarely over the horn ball by hand/ball-end pliers; do not lever on the servo shaft.",
    "ASSUMPTION", "ASM-08: snap/tug test and articulation through the horn sweep.")
add("J-STR-003", "ZS steering", "steering", 8.03, "ASM-08", "rod_end_m4", "tie_rod_m4", "ROD",
    "M4 female rod-end thread + ≈22 mm M4 threaded rod DOCUMENTED; engagement depth ASSUMPTION",
    "Rod cut, ends deburred", "Thread the near rod-end halfway onto the cut M4 rod and count turns.",
    "DOCUMENTED", "ASM-08: record cut length, thread engagement and exposed thread.")
add("J-STR-004", "ZS steering", "steering", 8.04, "ASM-08", "tie_rod_m4", "rod_end_m4", "ROD",
    "Second M4 rod-end on the same ≈22 mm threaded rod DOCUMENTED; finished centre distance ASSUMPTION",
    "J-STR-003", "Thread the far rod-end by the same turn count; orient both cups without twisting the rod.",
    "DOCUMENTED", "ASM-08: caliper finished ball-centre distance and confirm equal engagement.")
add("J-STR-005", "ZS steering", "steering", 8.05, "ASM-08", "rod_end_m4", "ball_stud", "ROD",
    "Far rod-end clips to M3 ball stud on saver side-input arm; fit ASSUMPTION",
    "Servo saver not yet pivot-clamped", "Snap the far rod-end onto the saver-side ball stud while the saver can still be lifted for access.",
    "ASSUMPTION", "ASM-08: articulation/tug check at both lock limits.")
add("J-STR-006", "ZS steering", "steering", 8.06, "ASM-08", "ball_stud", "servo_saver", "ROD",
    "Saver side-input feature location VERIFIED; printed hole is not proven M3 threaded and requires drilling/retention decision",
    "J-STR-005", "Trial the M3 ball stud in the saver side-input feature; use a nut only if the feature is through and accessible—do not cut an assumed thread.",
    "ASSUMPTION", "ASM-08: measure hole Ø/depth and record nut vs thread retention before final assembly.",
    evidence="Y steering study §5")
add("J-STR-007", "ZS steering", "steering", 8.07, "ASM-08", "servo_saver", "susp_block", "PIN",
    "Saver pivot bore 2.90×2.97 mm through 26.50 mm [VERIFIED]; vertical M3 boss [VERIFIED topology]",
    "Front suspension block fixed but linkage loose", "Lower saver onto the vertical M3 boss; retain with the actual dowel+circlip or M3 screw stack selected by the physical boss check.",
    "VERIFIED", "ASM-08: record boss Ø/height, selected pin/screw, washer/spacer stack and free axial play.",
    evidence="Y steering study §2/§5")
for side, upright, suffix, base in (("left", "upright_l", "L", 8.10), ("right", "upright_r", "R", 8.20)):
    add(f"J-STR-{8 if side == 'left' else 12:03d}", "ZS steering", "steering", base, "ASM-08",
        "servo_saver", "ball_stud", "TURNBUCKLE",
        f"Saver {side} forward-link hole location VERIFIED; M3 thread/retention ASSUMPTION",
        "J-STR-007", f"Fit the {side} M3 ball stud to the corresponding saver output hole; keep ball height matched to the opposite side.",
        "ASSUMPTION", f"ASM-08: measure {side} hole Ø/depth, retention and ball-centre height.")
    add(f"J-STR-{9 if side == 'left' else 13:03d}", "ZS steering", "steering", base + .01, "ASM-08",
        "ball_stud", "tie_end_m3", "TURNBUCKLE",
        "M3 ball stud to 3Racing tie-rod end / 3×32 turnbuckle topology DOCUMENTED; cup fit ASSUMPTION",
        f"J-STR-{8 if side == 'left' else 12:03d}", f"Clip the {side} inner 3Racing M3 tie-rod end squarely over the saver ball.",
        "ASSUMPTION", f"ASM-08: record {side} inner cup fit and initial ball-centre length.")
    inner_thread_id = 16 if side == "left" else 18
    add(f"J-STR-{inner_thread_id:03d}", "ZS steering", "steering", base + .015, "ASM-08",
        "tie_end_m3", "turnbuckle", "TURNBUCKLE",
        "3Racing M3 tie-rod end threads onto one end of the 3×32 turnbuckle; handedness and engagement are physical",
        f"J-STR-{9 if side == 'left' else 13:03d}", f"Identify the {side} inner turnbuckle thread direction, then install the tie-rod end to a counted starting engagement.",
        "ASSUMPTION", f"ASM-08: mark {side} inner thread handedness and record engaged length.")
    add(f"J-STR-{10 if side == 'left' else 14:03d}", "ZS steering", "steering", base + .02, "ASM-08",
        "turnbuckle", "tie_end_m3", "TURNBUCKLE",
        "Second 3Racing M3 tie-rod end threads onto the opposite 3×32 turnbuckle end; handedness/engagement physical",
        f"J-STR-{inner_thread_id:03d}", f"Install the {side} far tie-rod end with equal engagement and orient its cup toward the upright ball.",
        "ASSUMPTION", f"ASM-08: mark {side} far thread handedness and match inner engagement.")
    outer_cup_id = 17 if side == "left" else 19
    add(f"J-STR-{outer_cup_id:03d}", "ZS steering", "steering", base + .025, "ASM-08",
        "tie_end_m3", "ball_stud", "TURNBUCKLE",
        "Far 3Racing M3 tie-rod end clips to upright M3 ball stud; cup/ball fit ASSUMPTION",
        f"J-STR-{10 if side == 'left' else 14:03d}", f"Clip the {side} far tie-rod end over the upright ball without side-loading the cup.",
        "ASSUMPTION", f"ASM-08: snap/tug test and full bump/lock articulation.")
    add(f"J-STR-{11 if side == 'left' else 15:03d}", "ZS steering", "steering", base + .03, "ASM-08",
        "ball_stud", upright, "TURNBUCKLE",
        f"{side.title()} upright steering-arm M3 interface topology DOCUMENTED; hole Ø/thread ASSUMPTION",
        f"J-STR-{outer_cup_id:03d}", f"Fit the {side} upright ball stud only after its hole/retention is identified; match ball height left/right.",
        "ASSUMPTION", f"ASM-08: measure {side} upright feature and record nut/thread plus spacer stack.")

# ---- Front suspension and rolling --------------------------------------------
add("J-FRT-001", "ZF front", "front", 9.01, "ASM-09", "susp_block", "front_floor", "M3",
    "Four matched M3 centres in block/floor [VERIFIED]; exact bolt length ASSUMPTION",
    "J-FLR-001…007 and J-STR-007 access plan", "Place the complete front block on the front-floor datum, start all four M3 fasteners, square it, then snug diagonally.",
    "VERIFIED", "ASM-09: log selected bolt lengths/nut seats and verify block cannot rock.",
    evidence="Y steering study §5")
for idx, side in enumerate(("left", "right"), start=2):
    add(f"J-FRT-{idx:03d}", "ZF front", "front", 9.02 + idx / 100, "ASM-09",
        "crossarm", "susp_block", "PRESS",
        f"{side.title()} crossarm pivot uses GuideRod or optional D5×M3×5 sleeve [DOCUMENTED]; bore fit unmeasured",
        "J-FRT-001 loose", f"Align the {side} crossarm pivot, press/tap the selected GuideRod/sleeve squarely, and stop if plastic whitens.",
        "DOCUMENTED", f"ASM-09: caliper {side} bore/pin and record press force/free pivot.")
for idx, side in enumerate(("left", "right"), start=4):
    add(f"J-FRT-{idx:03d}", "ZF front", "front", 9.04 + idx / 100, "ASM-09",
        "arm", "susp_block", "PRESS",
        f"{side.title()} lower-arm pivot uses GuideRod or optional D5×M3×5 sleeve [DOCUMENTED]; bore fit unmeasured",
        "J-FRT-001 loose", f"Align the {side} lower arm, insert the guide/sleeve without mushrooming the printed end, and confirm gravity-free pivot.",
        "DOCUMENTED", f"ASM-09: measure {side} pivot and record sleeve vs printed GuideRod.")
for idx, (side, upright) in enumerate((("left", "upright_l"), ("right", "upright_r")), start=6):
    add(f"J-FRT-{idx:03d}", "ZF front", "front", 9.06 + idx / 100, "ASM-09",
        upright, "arm", "PIN",
        f"{side.title()} king-pin path nominal Ø3 mm; exact printed bore remains D-05 [ASSUMPTION]",
        f"J-FRT-{idx-2:03d}", f"Align upright and arm bores, insert the M3×30 dowel from the serviceable side, then fit its circlip.",
        "ASSUMPTION", f"ASM-09/D-05: measure {side} bore and king pin; prove free steer with circlip seated.",
        disposition="HOLD")
for num, side, target, dep in (
    (8, "left upper", "susp_block", "J-FRT-002"),
    (9, "left lower", "arm", "J-FRT-006"),
    (10, "right upper", "susp_block", "J-FRT-003"),
    (11, "right lower", "arm", "J-FRT-007"),
):
    add(f"J-FRT-{num:03d}", "ZF front", "front", 9.20 + num / 100, "ASM-09",
        "front_shock", target, "M3",
        f"52 mm shock eye to {side} M3 mount DOCUMENTED; eye bushing width/hole Ø and spacer stack ASSUMPTION",
        dep, f"Fit the {side} shock eye with no side preload; choose a BOM M3 bolt only after the eye and boss stack are measured.",
        "ASSUMPTION", f"ASM-09/56: record {side} eye Ø/width, bolt length and free articulation.",
        disposition="HOLD")
for num, side, upright in ((12, "left outer", "upright_l"), (13, "left inner", "upright_l"),
                           (14, "right outer", "upright_r"), (15, "right inner", "upright_r")):
    add(f"J-FRT-{num:03d}", "ZF front", "front", 9.40 + num / 100, "ASM-09",
        "front_bearing", "front_hub", "PRESS",
        "8 mm ID ×12 mm OD ×3.5 mm bearing DOCUMENTED; hub seat Ø12 requires D-22 physical confirm",
        "Wheel hub deburred and clean", f"Press the {side} bearing squarely into the rotating front hub, supporting the outer race.",
        "DOCUMENTED", f"ASM-09/D-22: caliper seat and verify {side} bearing is fully shoulder-seated.",
        disposition="HOLD")
for num, side, upright in ((16, "left", "upright_l"), (17, "right", "upright_r")):
    add(f"J-FRT-{num:03d}", "ZF front", "front", 9.60 + num / 100, "ASM-09",
        "front_hub", upright, "M4",
        f"{side.title()} rotating-hub spindle/retention thread is mesh-present but unmeasured; bearing ID is Ø8 DOCUMENTED",
        f"Both {side} bearings seated", f"Insert the rotating hub through the {side} upright/bearing stack and hand-check axial play before any locking nut.",
        "ASSUMPTION", f"ASM-09: record spindle Ø/thread and any washer/spacer stack.")
    add(f"J-FRT-{num+2:03d}", "ZF front", "front", 9.70 + num / 100, "ASM-09",
        "front_rim", "front_hub", "CLIP",
        f"Printed rim-to-hub keyed interface exists [VERIFIED silhouette]; exact locking feature/quantity ASSUMPTION",
        f"J-FRT-{num:03d}", f"Seat the {side} front rim fully on the rotating hub without forcing the bead seat.",
        "ASSUMPTION", f"ASM-09: mark orientation and verify zero rocking before retention.")
    add(f"J-FRT-{num+4:03d}", "ZF front", "front", 9.80 + num / 100, "ASM-09",
        "front_locknut", "front_hub", "M4",
        f"Printed locking-nut thread exists; diameter/pitch and mating spindle thread unmeasured [ASSUMPTION]",
        f"J-FRT-{num+2:03d}", f"Start the {side} printed locknut by hand only and stop at first resistance; retain only after free wheel rotation is proven.",
        "ASSUMPTION", f"ASM-09: identify thread and record hand-tight position; no threadlock in plastic.")
    add(f"J-FRT-{num+6:03d}", "ZF front", "front", 9.90 + num / 100, "ASM-09",
        "front_tyre", "front_rim", "DEFER",
        "Tamiya F104 tyre/rim bead DOCUMENTED; actual bead fit and bond gap unmeasured",
        "Tyres physically present and one wheel coupon accepted", f"DEFER {side} tyre installation; dry-seat first, then use only the BOM-v2 tyre-bond system after bead fit passes.",
        "ASSUMPTION", f"ASM-09/56: record bead fit/runout and selected documented tyre adhesive.",
        disposition="DEFER")

# ---- Rear suspension / drivetrain --------------------------------------------
for num, side, carrier in ((1, "left", "rear_carrier_l"), (2, "right", "rear_carrier_r")):
    add(f"J-REA-{num:03d}", "ZR rear", "rear", 10.00 + num / 100, "ASM-10",
        carrier, "rear_floor", "M3",
        f"{side.title()} carrier-to-floor M3 topology DOCUMENTED; selected original-vs-Rev-1 stack unresolved",
        "Gate A stack selection", f"Dry-place the {side} carrier on its floor seats; start all M3 screws but do not final-tighten until both bearings share one shaft axis.",
        "ASSUMPTION", f"ASM-10/51: identify selected carrier path, hole Ø/count, bolt lengths and retention.",
        disposition="HOLD")
    add(f"J-REA-{num+2:03d}", "ZR rear", "rear", 12.00 + num / 100, "ASM-12",
        "rear_bearing", carrier, "PRESS",
        "Rear bearing 12×21×5 DOCUMENTED; Ø21 carrier seat is path-dependent and unverified",
        f"J-REA-{num:03d} dry located", f"Press the {side} rear bearing squarely into the selected carrier/motor cover, supporting the outer race.",
        "DOCUMENTED", f"ASM-12/51: caliper Ø21 seat, confirm shoulder depth and retention against axle walk.",
        disposition="HOLD")
add("J-REA-005", "ZR rear", "rear", 12.05, "ASM-12", "output_shaft", "rear_bearing", "PRESS",
    "Output shaft Ø/shoulders TBD; bearing ID Ø12 DOCUMENTED",
    "J-REA-003/004 seated and coaxial", "Pass the output shaft through both bearings without using the thread/end as a drift; hand-rotate before adding spacers.",
    "ASSUMPTION", "ASM-51: record shaft journals/shoulders/span and free-rotation baseline.",
    disposition="HOLD")
for num, side, spacer in ((6, "left inboard", "spacer_l"), (7, "left outboard", "spacer_new_l"),
                          (8, "right inboard", "spacer_r"), (9, "right outboard", "spacer_new_r")):
    add(f"J-REA-{num:03d}", "ZR rear", "rear", 12.10 + num / 100, "ASM-12",
        "metal_spacer", spacer, "PRESS",
        f"{side.title()} stack uses 14 mm-ID metal sleeve before printed spacer [DOCUMENTED]; cut length TBD",
        "J-REA-005 rotates freely", f"Slide/cut the {side} metal sleeve first, then the printed spacer; do not omit or swap order.",
        "DOCUMENTED", f"ASM-12/51: record sleeve cut length, printed-spacer identity and axial endplay.",
        disposition="HOLD", evidence="ASSEMBLY_NOTES hardware list; E-05")
add("J-REA-010", "ZR rear", "rear", 12.20, "ASM-12", "pulley", "output_shaft", "BELT",
    "Belt-set pulley bore/retention and shaft flat/key are unmeasured [ASSUMPTION]",
    "J-REA-005…009 dry stack", "Install the axle pulley using only its included hardware; align its belt plane before retention.",
    "ASSUMPTION", "ASM-51: measure pulley bore/width/retainer and shaft feature; photograph retention.",
    disposition="HOLD")
add("J-REA-011", "ZR rear", "rear", 12.21, "ASM-12", "spur", "pulley", "M3",
    "75T spur ↔ belt-pulley bolt PCD/count/Ø is D-16 UNKNOWN; 48P/75T is DOCUMENTED",
    "J-REA-010 located", "Offer the 75T spur to the pulley without drilling or slotting; install BOM M3 screws only if every hole registers.",
    "ASSUMPTION", "ASM-51/D-16: caliper both PCDs, hole Ø/count and screw engagement; STOP on mismatch.",
    disposition="HOLD")
add("J-REA-012", "ZR rear", "rear", 12.22, "ASM-12", "pinion", "motor", "BELT",
    "28T pinion, 48P and 3.175 mm motor shaft DOCUMENTED; included set-screw thread/flat ASSUMPTION",
    "Motor out of mount", "Slide pinion onto the motor shaft, align its tooth plane to the spur and retain with the pinion's included set screw only.",
    "DOCUMENTED", "ASM-12/51: measure bore/shaft, confirm set-screw lands on a flat or document round-shaft retention.")
add("J-REA-013", "ZR rear", "rear", 12.23, "ASM-12", "motor", "motor_lock", "M3",
    "Motor face/lock M3 topology DOCUMENTED; Rocket 540 face pattern and bolt depth must be measured",
    "J-REA-012 pinion loosely located", "Bolt motor to beltdrivemotorlock with the shortest BOM M3 screws that fully engage without touching windings.",
    "ASSUMPTION", "ASM-12/51: measure face PCD/thread depth and record bolt length.")
add("J-REA-014", "ZR rear", "rear", 12.24, "ASM-12", "motor_lock", "rear_floor", "M3",
    "Donor motor-lock mounting topology DOCUMENTED; selected rear-stack receiver/bolt length ASSUMPTION",
    "J-REA-013", "Install motor/lock as one serviceable unit; leave mesh adjustment loose.",
    "ASSUMPTION", "ASM-12/51: record receiver holes, adjustment travel and service access.")
add("J-REA-015", "ZR rear", "rear", 12.25, "ASM-12", "belt", "pulley", "BELT",
    "140 mm belt DOCUMENTED; pulley teeth/centres/tension unmeasured",
    "J-REA-010/014", "Loop belt over both pulleys without prying across flange teeth; set alignment and tension by hand rotation.",
    "ASSUMPTION", "ASM-51: record tooth counts, belt width, centre distance and free rotation.",
    disposition="HOLD")
add("J-REA-016", "ZR rear", "rear", 12.26, "ASM-12", "pinion", "spur", "BELT",
    "28T↔75T 48P mesh DOCUMENTED; backlash and installed centre distance physical",
    "J-REA-011…015", "Use a paper/blue-check mesh setup, tighten the motor lock gradually, and rotate through a full spur revolution.",
    "DOCUMENTED", "ASM-12/51: record backlash/blue pattern and any tight spot; no powered test.")
for num, side in ((17, "left"), (18, "right")):
    add(f"J-REA-{num:03d}", "ZR rear", "rear", 12.30 + num / 100, "ASM-12",
        "tyreslot_1", "rear_rim", "CLIP",
        f"{side.title()} tighter tyreslot1/2 keyed rim interface VERIFIED as mesh; required quantity 1-vs-2 per side unresolved",
        "D-23 quantity check", f"Dry-seat both candidate tyreslot pieces in the {side} rear rim and retain only the confirmed required set.",
        "ASSUMPTION", f"ASM-12/D-23: record {side} adapter quantity/orientation and play.",
        disposition="HOLD")
    add(f"J-REA-{num+2:03d}", "ZR rear", "rear", 12.40 + num / 100, "ASM-12",
        "tyreslot_2", "output_shaft", "M4",
        "Drawing [7] specifies M4 bolt through tyreslot into axle; axle internal thread/depth unmeasured",
        f"J-REA-{num:03d}; shaft end present", f"Insert the {side} rear wheel/adapter stack and hand-start its M4 retention only after axle thread is identified.",
        "DOCUMENTED", f"ASM-12/51: measure {side} axle thread/depth and select exact M4 bolt without bottoming.")
    add(f"J-REA-{num+4:03d}", "ZR rear", "rear", 12.50 + num / 100, "ASM-12",
        "rear_locknut", "rear_rim", "M4",
        "Printed rear locking nut is present but its role/thread relative to drawing-[7] M4 axle bolt is unresolved",
        f"J-REA-{num+2:03d}", f"Do not install the {side} printed locknut until ASM-51 proves whether it is required in the selected wheel stack.",
        "ASSUMPTION", f"ASM-51: identify {side} locknut role; mark OMIT if the M4 axle bolt supersedes it.",
        disposition="HOLD")
    add(f"J-REA-{num+6:03d}", "ZR rear", "rear", 12.60 + num / 100, "ASM-12",
        "rear_tyre", "rear_rim", "DEFER",
        "Tamiya F104 rear bead DOCUMENTED; actual fit/bond interface unmeasured",
        "Tyres physically present and adapter quantity closed", f"DEFER the {side} tyre bond; dry-seat, measure runout, then use only the documented BOM-v2 tyre bond.",
        "ASSUMPTION", f"ASM-12/56: record {side} bead/runout and bond method.",
        disposition="DEFER")
add("J-REA-025", "ZR rear", "rear", 10.25, "ASM-10", "rear_spring_mount", "rear_floor", "M3",
    "Original/Rev-1 rear spring-mount M3 topology DOCUMENTED; selected stack unresolved",
    "Gate A selection", "Dry-fit only the selected spring mount to the floor/rear stack; start all screws and leave loose for rocker alignment.",
    "ASSUMPTION", "ASM-10: identify selected STL, hole Ø/count, bolt lengths and nut/insert retention.",
    disposition="HOLD")
add("J-REA-026", "ZR rear", "rear", 10.26, "ASM-10", "spring_block", "rear_spring_mount", "M3",
    "Spring-block-to-mount topology DOCUMENTED; pivot/fastener stack unmeasured",
    "J-REA-025", "Assemble the spring block/rocker dry with the selected M3 stack; preserve free articulation.",
    "ASSUMPTION", "ASM-10: record pivot Ø, spacer stack, retention and free travel.",
    disposition="HOLD")
add("J-REA-027", "ZR rear", "rear", 11.01, "ASM-11", "rear_shock", "spring_block", "DEFER",
    "68 mm eye-to-eye DOCUMENTED; eye Ø/width/bushing and lower mount ASSUMPTION",
    "Rear 68 mm shock arrival + J-REA-025/026", "DEFER lower shock eye connection until the real shock is measured; do not shim or drill the selected rocker.",
    "ASSUMPTION", "ASM-11: caliper eye/bushing and record BOM M3 bolt/spacer stack through full travel.",
    disposition="DEFER")
add("J-REA-028", "ZR rear", "rear", 11.02, "ASM-11", "rear_shock", "rear_floor", "DEFER",
    "68 mm upper-eye station DOCUMENTED topology; exact receiver and M3 stack ASSUMPTION",
    "Rear 68 mm shock arrival + J-REA-027", "DEFER upper eye; install only after the selected stack seats the lower eye without side load.",
    "ASSUMPTION", "ASM-11: record upper boss/hole Ø, bolt length, spacer stack and articulation.",
    disposition="DEFER")
add("J-REA-029", "ZR rear", "rear", 10.29, "ASM-10", "rear_wing", "rear_spring_mount", "M3",
    "Preferred 2021 wing-to-original rear-stack topology DOCUMENTED; hole/count/stack still Gate A/B",
    "Selected stack and wing accepted together", "Dry-offer wing to the spring-mount/backplate interface; start M3s only when all holes register without bending the wing.",
    "ASSUMPTION", "ASM-10: record wing holes, exact BOM bolt lengths and nut/insert retention.",
    disposition="HOLD")
add("J-REA-030", "ZR rear", "rear", 28.01, "ASM-28", "drs_servo", "rear_wing", "DEFER",
    "MG90S wing pocket DOCUMENTED topology; clone body/ears/hole pitch unmeasured",
    "MG90S arrival + Gate A/B wing selection", "DEFER servo-to-pocket mount; do not resize the wing pocket from nominal clone dimensions.",
    "ASSUMPTION", "ASM-54: measure MG90S body/ears/hole pitch and select BOM M3 hardware only if holes permit.",
    disposition="DEFER")
add("J-REA-031", "ZR rear", "rear", 28.02, "ASM-28", "drs_servo", "horn", "DEFER",
    "MG90S spline/horn/horn screw unmeasured; 25T DS3235SG horn is NOT transferable",
    "MG90S arrival and centring", "DEFER horn fit; use only the horn and horn screw supplied/verified for the MG90S clone.",
    "ASSUMPTION", "ASM-54: identify spline, horn holes/radii and retaining screw.",
    disposition="DEFER")
add("J-REA-032", "ZR rear", "rear", 28.03, "ASM-28", "horn", "drs_arm", "DEFER",
    "Drawing [2] documents metal-rod linkage; rod diameter, ends and horn/arm holes are UNKNOWN and not in supplied joint BOM",
    "J-REA-030/031 and real MG90S", "DEFER DRS link hardware; do not repurpose steering M4 rod or M3 ball studs without a measured match.",
    "ASSUMPTION", "ASM-54: measure horn/arm hole Ø, centre distance and specify only BOM-compatible hardware or leave open.",
    disposition="DEFER")
add("J-REA-033", "ZR rear", "rear", 28.04, "ASM-28", "drs_arm", "rear_wing", "DEFER",
    "DRS arm/flap pivot exists in mesh/drawing; pin/retention specification UNKNOWN",
    "Gate B and J-REA-032", "DEFER arm-to-flap/pivot closure until the wing dry assembly identifies the actual pin and retention.",
    "ASSUMPTION", "ASM-54: record pivot Ø, hardware, end retention and free flap travel.",
    disposition="DEFER")

# ---- Battery, power and onboard charge hardware -------------------------------
add("J-PWR-001", "ZP power", "power", 14.01, "ASM-14", "ps01", "front_floor", "M3X8",
    "PS-01 DIAG-CAD feet + mapped floor M3 feature/clamp; final station ASSUMPTION",
    "J-FLR complete; D-27 occupancy checked", "Install the diagnostic tray with M3×8 at the mapped shared/free feature and its reversible clamp foot; do not drill donor floor.",
    "ASSUMPTION", "ASM-14/50: record exact floor feature(s), clamp engagement and pull-off test.",
    disposition="HOLD", evidence="K PS-01/K.3")
add("J-PWR-002", "ZP power", "power", 15.01, "ASM-15", "battery", "ps01", "DEFER",
    "Pack ≤75×45×25 DOCUMENTED; exact SKU, case, leads, strap path and tray fit UNKNOWN",
    "Exact 2S pack arrival + J-PWR-001", "DEFER pack retention. Fit the exact pack/dummy and prove open-top removal before selecting the restraint.",
    "ASSUMPTION", "ASM-50: measure pack/lead exit, strap land, shake retention and body-off service.",
    disposition="DEFER")
add("J-PWR-003", "ZP power", "power", 14.02, "ASM-14", "ps03", "rear_floor", "M3X8",
    "PS-03 DIAG-CAD uses one verified right-side M3 feature plus reversible clamp [ASSUMPTION final]",
    "D-27 occupancy", "Install shelf low on DAT-F with M3×8 at the verified feature and the reversible clamp; keep both rail lanes separate.",
    "ASSUMPTION", "ASM-14: identify donor/shared screw and perform pull-off/flatness check.",
    disposition="HOLD", evidence="K PS-03/K.3")
for num, label in ((4, "A"), (5, "B")):
    add(f"J-PWR-{num:03d}", "ZP power", "power", 17.00 + num / 100, "ASM-17",
        "ubec", "ps03", "CLIP",
        f"UBEC-{label} pocket nominal 30×14×10 ASSUMPTION; real body/lead exits unmeasured",
        "J-PWR-003 + real UBEC measured", f"Seat UBEC-{label} in its own pocket with leads unloaded; use only pocket/declared restraint, no screw through its case.",
        "ASSUMPTION", f"ASM-17/52: caliper UBEC-{label}, tug-test body not leads, confirm ventilation.",
        disposition="HOLD")
add("J-PWR-006", "ZP power", "power", 17.06, "ASM-17", "cap", "ps03", "CLIP",
    "Cap can Ø/height and shelf retainer ASSUMPTION; value remains governed by D-24",
    "Real capacitor selected after D-24", "Seat capacitor adjacent to its rail using the designed pocket/tie point; no lead carries mechanical load.",
    "ASSUMPTION", "ASM-17/36: measure can, retention and lead strain relief.",
    disposition="HOLD")
add("J-PWR-007", "ZP power", "power", 14.03, "ASM-14", "ps15", "rear_floor", "M3X8",
    "PS-15 DIAG-CAD uses reversible plate clamps because no free Z2R feature exists [ASSUMPTION final]",
    "D-27 occupancy and disconnect reach", "Clamp PS-15 to the donor plate without new holes; align connector access upward/inward.",
    "ASSUMPTION", "ASM-14/18: pull-off test and body-on disconnect finger reach.",
    disposition="HOLD", evidence="K PS-15/K.3")
add("J-PWR-008", "ZP power", "power", 4.01, "ASM-04", "insert", "ps15", "INSERT",
    "M3×5 insert DOCUMENTED; PS-15 repeated-service boss exists in spec but DIAG-CAD seat is not production-authorized",
    "PS-15 production boss authorized and printed", "Heat-set each service insert square and flush; let cool fully before chasing with an M3 screw.",
    "ASSUMPTION", "ASM-04: boss wall/depth, insertion temperature/result and hand-thread check.",
    disposition="HOLD")
add("J-CHG-001", "ZP power", "power", 59.01, "ASM-59", "charge_module", "charge_pocket", "DEFER",
    "30×25×10 mm is the supplied TARGET envelope; module SKU, final dimensions, hole pattern, thermal face and connector exits remain TBD",
    "Owner selects compliant 5 V-input 2S balancing-charge module with safety evidence", "DEFER module mount; after selection, caliper every body/hole/connector against the TARGET and generate a parametric pocket—no photo-derived dimensions.",
    "ASSUMPTION", "ASM-59/OP-49: record SKU/datasheet, mass, envelope, hole Ø/pitch, cell ports and thermal faces.",
    disposition="DEFER", evidence="OPEN_PROBLEMS OP-49")
add("J-CHG-002", "ZP power", "power", 59.02, "ASM-59", "charge_pocket", "rear_floor", "DEFER",
    "Pocket station/feet/fastener count UNKNOWN until full inside-shell cluster fit",
    "J-CHG-001 measured + P1 full cluster", "DEFER pocket-to-floor joint; prefer mapped shared M3 stack or reversible clamp and never add donor holes.",
    "ASSUMPTION", "ASM-59/P1: record station, M3 feature, exact BOM bolt length and shell/service clearance.",
    disposition="DEFER")
add("J-CHG-003", "ZP power", "power", 59.03, "ASM-59", "charge_port", "body_rear", "DEFER",
    "Existing opening/reversible hidden insert required; receptacle geometry and panel thickness UNKNOWN",
    "Selected charge module/receptacle measured", "DEFER port mount; use an existing opening or reversible insert, with no shell drilling or guessed clip geometry.",
    "ASSUMPTION", "ASM-59/OP-49: identify opening, panel thickness, receptacle flange/hole pattern, plug insertion force and weather/strain relief.",
    disposition="DEFER")
add("J-CHG-004", "ZP power", "power", 59.04, "ASM-59", "charge_interlock", "ps15", "DEFER",
    "Charge/run interlock type, body, terminals and mounting thread UNKNOWN",
    "Electrical safety architecture separately authorized", "DEFER interlock mount; provide mechanical keying so charge and run states cannot be selected together, without inferring circuit topology.",
    "ASSUMPTION", "ASM-59/OP-49: record switch/interlock SKU, mounting feature, positive detent and finger access.",
    disposition="DEFER")

# ---- Electronics trays and RF hardware ---------------------------------------
add("J-ELC-001", "ZC control", "electronics", 20.01, "ASM-20", "ps05", "ps03", "INSERT",
    "PS-05 rear post landing on PS-03 documented in spec; exact station and production boss ASSUMPTION",
    "J-PWR-003", "Install rear deck post(s) on the PS-03 shoulder/receiver and keep their axes square to DAT-F.",
    "ASSUMPTION", "ASM-20: record count/stations, insert engagement and post height.",
    disposition="HOLD")
add("J-ELC-002", "ZC control", "electronics", 20.02, "ASM-20", "ps05", "ps15", "INSERT",
    "PS-05 front post landing on PS-15 shoulders is concept-only; recovered DIAG-CAD omits fixed shoulders",
    "J-PWR-007 and physical P1", "HOLD front post connection until a non-overlapping shoulder station is proven; then use M3×5 insert service threads.",
    "ASSUMPTION", "ASM-20/P1: record station, boss geometry, post height and connector hand clearance.",
    disposition="HOLD")
add("J-ELC-003", "ZC control", "electronics", 20.03, "ASM-20", "ps04", "ps05", "INSERT",
    "Two front M3 service fasteners into post inserts DOCUMENTED; rear hook count/plane ASSUMPTION",
    "J-ELC-001/002 and S0/KO-01 gates", "Lower PS-04 onto rear hooks, align front post holes, then install the two service screws.",
    "ASSUMPTION", "ASM-20: record hole Ø/pitch, exact bolt lengths, level ±1 mm and <60 s removal.",
    disposition="HOLD")
add("J-ELC-004", "ZC control", "electronics", 20.04, "ASM-20", "ps04", "ps03", "CLIP",
    "Tool-free rear deck hook into PS-03 documented in spec; geometry not production-authorized",
    "J-ELC-003", "Engage rear hooks before front screws; lift only after front screws and CN-DECK are removed.",
    "ASSUMPTION", "ASM-20: hook engagement/tug test and removal path.",
    disposition="HOLD")
for num, label in ((5, "#1"), (6, "#2")):
    add(f"J-ELC-{num:03d}", "ZC control", "electronics", 22.00 + num / 100, "ASM-22",
        "esp32", "ps04", "M3",
        f"ESP32 {label} mounting holes may be M2.5/M3 by board variant; supplied BOM has M3 only [ASSUMPTION]",
        "Real board calipered + J-ELC-003", f"Bench-fit ESP32 {label}; use BOM M3 only if holes clear without touching pads/traces, otherwise DEFER rather than invent M2.5 hardware.",
        "ASSUMPTION", f"ASM-22/52: record ESP32 {label} hole Ø/pitch, standoff height, insulation and exact BOM fastener.",
        disposition="HOLD")
add("J-ELC-007", "ZC control", "electronics", 23.01, "ASM-23", "rp1", "ps06", "CLIP",
    "RP1 body/pad retention documented as carrier+adhesive option; board holes/fastener absent from supplied BOM",
    "Real RP1 measured", "Seat RP1 on PS-06 without loading antenna/coax; do not run an M3 screw through the board unless a measured mounting hole exists.",
    "ASSUMPTION", "ASM-23/52: record body/hole geometry and carrier tug test.",
    disposition="HOLD")
add("J-ELC-008", "ZC control", "electronics", 14.08, "ASM-14", "ps06", "front_floor", "M3",
    "One floor M3 feature + carrier option documented; D-27/rod-sweep station physical",
    "ASM-08 steering sweep recorded", "Install PS-06 at the accepted quiet-side floor feature with the shortest matching BOM M3 screw.",
    "ASSUMPTION", "ASM-14/23: record station, bolt/nut, antenna clearance and no KO-01 contact.",
    disposition="HOLD")
add("J-ELC-009", "ZC control", "electronics", 25.01, "ASM-25", "wifi", "ps04", "CLIP",
    "WiFi max pocket 60×32×12 is diagnostic ASSUMPTION; real module possession/dimensions unconfirmed",
    "Possession + D-06b", "Use PS-13 dummy only until the real WiFi module is measured; then seat with U.FL exits unloaded and service pull open.",
    "ASSUMPTION", "ASM-25/52: record module envelope, pocket retention and removal path.",
    disposition="HOLD")
add("J-ELC-010", "ZC control", "electronics", 25.02, "ASM-25", "heatsink", "wifi", "BOND",
    "28×28×3 heatsink DOCUMENTED; WiFi thermal face, bond line and keepouts unmeasured",
    "D-06b + thermal material selected", "Dry-align heatsink to the identified hot package/plane, preserve U.FL/USB access, then make the documented thermal bond.",
    "ASSUMPTION", "ASM-25: record thermal face, bond material/thickness, cure and pull test.",
    disposition="HOLD")
for num, side in ((11, "left"), (12, "right")):
    add(f"J-ELC-{num:03d}", "ZC control", "electronics", 30.00 + num / 100, "ASM-30",
        "antenna_post", "ps04", "M3",
        f"{side.title()} PS-12 post is intended integral-to-deck or standalone; exact joint path ASSUMPTION",
        "D-33 route + D-20 separation", f"If not integral, fasten the {side} post to PS-04/standalone foot with a measured BOM M3 stack; never shell-mount it.",
        "ASSUMPTION", f"ASM-30/52: record {side} post joint, bolt length and body-cycle stability.",
        disposition="HOLD")
    add(f"J-ELC-{num+2:03d}", "ZC control", "electronics", 30.20 + num / 100, "ASM-30",
        "antenna", "antenna_post", "CLIP",
        f"{side.title()} 70 mm whip DOCUMENTED; post tie/clip geometry and coax strain relief ASSUMPTION",
        f"J-ELC-{num:03d}; antenna attached to module before power", f"Seat the {side} whip on the post in the shallow V; restrain the cable jacket, never the U.FL plug.",
        "ASSUMPTION", f"ASM-30/52: jacket tug test, ≥10 mm bend and body-off cycle proof.",
        disposition="HOLD")
add("J-ELC-015", "ZC control", "electronics", 31.01, "ASM-31", "cable_comb", "front_floor", "M3",
    "PS-08 push-fit + optional M3 documented; exact floor stations and comb geometry depend on D-10/D-27",
    "All harnesses routed and motion sweep available", "Clip/bolt each comb only at a mapped donor/shared feature; load cable jackets, not solder joints.",
    "ASSUMPTION", "ASM-31: record every comb station/fastener and full-motion tug test.",
    disposition="HOLD")

# ---- Lift-out electronics cassette (new architecture; p0_12 audit) -----------
add("J-CAS-001", "ZK cassette", "electronics", 20.10, "ASM-20",
    "cassette_fixed_frame", "front_floor", "TBD_RETENTION",
    "Former X+35/L±12 bosses are REJECTED inside the 55×45 PDB target; no replacement forward stations are registered",
    "p0_12 full-stack dummy + external four-point clamp coupon",
    "HOLD the forward saddle. Find reversible external tabs/clamps clear of the PDB, wall boards, floor edge and shell; do not hide screws under modules or drill the donor floor.",
    "ASSUMPTION",
    "ASM-20/CAS-04: record both forward attachment stations, clamp pull-off, shell-lip clearance and zero donor damage.",
    disposition="HOLD", evidence="p0_d01 feature map; p0_12 cassette fit audit")
add("J-CAS-002", "ZK cassette", "electronics", 20.11, "ASM-20",
    "cassette_fixed_frame", "rear_floor", "TBD_RETENTION",
    "Former X−15/L±12 bosses are REJECTED inside the 30×25 charge target; nearby M3 rows remain occupied/servo-contested",
    "p0_12 full-stack dummy + ASM-08 steering installation",
    "HOLD the rear saddle. Find reversible external tabs/clamps clear of the charge cell, servo and side bodies; no hidden module-first screw or donor hole is authorized.",
    "ASSUMPTION",
    "ASM-20/CAS-04: feeler-map the rear carrier against servo/rod, record clamp stations and repeat the unloaded pull-off test.",
    disposition="HOLD", evidence="p0_d01 feature map; D-27; KO-01/19")
add("J-CAS-003", "ZK cassette", "electronics", 20.12, "ASM-20",
    "cassette_box", "cassette_fixed_frame", "TBD_RETENTION",
    "Four-point lift-out remains required, but the former X−15/+35/L±12 pattern is rejected by PDB/charge overlap; new pattern and retention are TBD",
    "J-CAS-001/002 + S0/KO-01/full-cluster fit gate + new external pattern",
    "Lower the cassette onto four external datums and engage the selected reversible retention only after its insert/clamp coupon; never remove an electrical module to reach a cassette service joint.",
    "ASSUMPTION",
    "ASM-20/CAS-04: record four coordinates, insert/boss dimensions, bolt lengths, rocking, driver reach and body-off removal time.",
    disposition="HOLD")
add("J-CAS-004", "ZK cassette", "electronics", 22.10, "ASM-22",
    "pdb", "cassette_box", "M3",
    "PDB contents are FIRM; 55×45×18 mm and ~50 g are TARGET/ASSUMPTION; target placement X+1…+46/L±27.5/Z1…19 has only 3 mm to KO-01",
    "final PDB component placement + ASM-08 measured sweep + full connector dummy",
    "HOLD the four-M3 lower-bay PDB seat. Refine and caliper the final board, tall UBEC/cap side, holes, loop-key access and every connector/bend before selecting the exact BOM M3 lengths/standoffs.",
    "ASSUMPTION",
    "ASM-22/CAS-05: record PDB L/W/H/mass, holes, live-side insulation, connector exits, creepage lands and service pull.",
    disposition="HOLD")
add("J-CAS-005", "ZK cassette", "electronics", 59.05, "ASM-59",
    "charge_module", "cassette_box", "DEFER",
    "Charge module uses a 30×25×10 TARGET cell at X−31…−1/L−13…+12/Z1…11; SKU, holes, exits, thermal face and electrical authorization remain open",
    "OP-49 + J-CHG-001 and full cassette fit gate",
    "DEFER the charge-module seat. Select and caliper the actual 5 V USB-C to 2S balancing SKU; do not treat the target cell as a pocket or infer a circuit.",
    "ASSUMPTION",
    "ASM-59/CAS-05: record selected module dimensions/mass/thermal face and prove isolated charge/run access.",
    disposition="DEFER")
add("J-CAS-006", "ZK cassette", "electronics", 20.13, "ASM-20",
    "cassette_deck", "cassette_box", "INSERT",
    "Insulated rear service deck Z13…16 carries amp + RP1 above the charge TARGET; 6 mm to KO-01 is 2 mm short of moving policy",
    "J-CAS-004/005 + J-CAS-018 + ASM-08 measured sweep",
    "HOLD the rear service deck. Prove insulation, charge thermal clearance, amp/RP1 exits and measured steering gap before selecting its supports.",
    "ASSUMPTION",
    "ASM-20/CAS-02: record deck Z, four supports, flatness, lower-module clearance and no rod contact.",
    disposition="HOLD")
for num, label, wall, lateral in (
    (7, "#1 control", "cassette_wall_l", "L−43…−30"),
    (8, "#2 sound/light", "cassette_wall_r", "L+30…+43"),
):
    add(f"J-CAS-{num:03d}", "ZK cassette", "electronics",
        22.10 + num / 100, "ASM-22", "esp32", wall, "M3",
        f"Mini board {label} identity/envelope is FIRM at 39 X ×31 Z ×~13 L at {lateral}; holes, headers, retention and live micro-USB plug bends are unmeasured",
        "real MH-ET Live board calipers + S0≥9.82 + p0_12 fit gate",
        f"HOLD mini-board {label} wall retention; orient the micro-USB end toward X+42 and do not force M3 through an unverified PCB hole.",
        "ASSUMPTION",
        f"ASM-22/CAS-03: record mini-board {label} SKU/chip, body/headers/live USB plug, holes, wall gap, insulation and body-off hand clearance.",
        disposition="HOLD")
add("J-CAS-009", "ZK cassette", "electronics", 23.09, "ASM-23",
    "rp1", "cassette_deck", "CLIP",
    "RP1 body is DOCUMENTED 13×11×3; cassette pad, antenna root and lead exit are unmeasured",
    "J-CAS-006 + firm connector map + full body/bend dummy",
    "HOLD the RP1 seat; restrain the body/pad and cable jacket without clamping the antenna root.",
    "ASSUMPTION",
    "ASM-23/CAS-05: record pad size, pull direction, antenna service loop and separation from WiFi/XT seats.",
    disposition="HOLD")
add("J-CAS-010", "ZK cassette", "electronics", 25.10, "ASM-25",
    "wifi", "cassette_deck", "CLIP",
    "WiFi allocation remains ≤60×32×12 with 28×28×3 heatsink, but the target-cell repack has no accepted WiFi station",
    "Real BL-M8812EU2 calipers + full PDB/charge/amp/RP1/dock dummy",
    "HOLD the WiFi seat as UNPLACED; find a shell/KO-safe vented station with USB, both U.FL service directions and ≥10 mm coax bends unobstructed.",
    "ASSUMPTION",
    "ASM-25/CAS-05: record complete module/heatsink envelope, vent free area, cable bends, retention and body-on temperature.",
    disposition="HOLD")
add("J-CAS-011", "ZK cassette", "electronics", 26.10, "ASM-26",
    "ps10", "cockpit_pedestal", "DEFER",
    "PS-10 gimbal-to-pedestal face, holes, gimbal datum and swept envelope are unmeasured; both MG90S units remain in transit",
    "J-CAS-015 + D-34/35 + real MG90S units + p0_12 pedestal/halo gate",
    "DEFER the gimbal-to-pedestal joint; the gimbal is never supported by the cassette, and no nominal MG90S pocket or horn interface is authorized.",
    "ASSUMPTION",
    "ASM-26/CAS-08: record pedestal face, hardware, roll datum, FOV, halo/airbox gap, full no-power sweep and independent cassette lift.",
    disposition="DEFER")
add("J-CAS-012", "ZK cassette", "electronics", 31.12, "ASM-31",
    "xt_seat", "cassette_box", "CLIP",
    "Firm dock minimum is 1×XT60 pack inlet + 2×XT30 Rail-A/B branches; target allocations XT60 20×20×12 and XT30 16×16×10 are ASSUMPTION",
    "selected terminated XT60/XT30 calipers + D-10 full harness/dock dummy",
    "HOLD the ~60 mm power bank; recess the potentially live/source half as shrouded/socket, separate it visibly from signal and load jackets rather than PDB solder joints.",
    "ASSUMPTION",
    "ASM-31/CAS-07: record connector SKU/polarity, seat outline, mating hand, bend radius, extraction force and strain relief.",
    disposition="HOLD")
add("J-CAS-013", "ZK cassette", "electronics", 31.13, "ASM-31",
    "servo_seat", "cassette_box", "CLIP",
    "Firm bank count is 5×3-pin: steering, ESC signal (+5 removed), DRS, pan and tilt; 16 mate-depth ×10 pitch ×8 high each is ASSUMPTION",
    "selected positive-lock 3-pin housing calipers + D-10 servo-lead dress",
    "HOLD the ~58 mm servo bank; positively retain and label all five positions, witness the ESC missing +5 contact and preserve body-off finger release.",
    "ASSUMPTION",
    "ASM-31/CAS-07: record count, pin order, clip retention, finger clearance and full-motion tug test.",
    disposition="HOLD")
add("J-CAS-014", "ZK cassette", "electronics", 31.14, "ASM-31",
    "signal_seat", "cassette_box", "CLIP",
    "Firm external signal bank is 3×JST-XH 3-pin (balance/LED/Hall) + 1×shielded USB4; internal bodies include XH4 CRSF, XH3 link2, XH5 I2S and 2×U.FL; all body allocations ASSUMPTION",
    "selected terminated XH3/4/5, USB4 and U.FL calipers + D-10 full chassis umbilical",
    "HOLD the ~64 mm external signal bank and internal seats; key/label every mate, separate them from XT power, reserve U.FL bend relief and anchor jackets before first bends.",
    "ASSUMPTION",
    "ASM-31/CAS-07: record pin map, seat spacing, plug extraction, bundle OD, first anchor and ten body-off mate cycles.",
    disposition="HOLD")
add("J-CAS-015", "ZK cassette", "electronics", 20.14, "ASM-20",
    "cockpit_pedestal", "front_floor", "M3",
    "Trial pedestal outer core is X+51…+65/L±11 to carry the 14×22 outer conduit gauge; floor feature, hole count and gimbal datum remain TBD",
    "ASM-08 measured steering + D-04 body/halo registration + transparent pedestal template",
    "HOLD the fixed pedestal floor joint. Use only a physically free/shared feature or reversible clamp; do not drill the donor floor and do not attach it to the cassette.",
    "ASSUMPTION",
    "ASM-20/CAS-08: record foot contacts, existing/shared fastener or clamp, 14×22 core section, 5 mm PDB/5.6 mm front-block gaps, pull-off and zero donor damage.",
    disposition="HOLD")
add("J-CAS-016", "ZK cassette", "electronics", 31.15, "ASM-31",
    "pedestal_conduit", "cockpit_pedestal", "DEFER",
    "Firm bundle is shielded USB4 + 2×3-pin servo; target clear section 10×18 with 2 mm trial wall gives 14×22 outer, ≥25 mm lower slack and ≥20 mm provisional USB bend",
    "J-CAS-015 + terminated USB4/two servo plugs + real MG90S leads + 2 mm-wall coupon",
    "DEFER the conduit interface; pull full connectors sequentially without removing terminals, then prove slack, bend and jacket anchor before the R1/R2 turn.",
    "ASSUMPTION",
    "ASM-31/CAS-09: record clear section, wall, plug pull-through, bend radius, strain relief, steering gap and cassette-lift clearance.",
    disposition="DEFER")
add("J-CAS-017", "ZK cassette", "electronics", 31.16, "ASM-31",
    "cassette_dock", "cassette_box", "CLIP",
    "Map/count is firm, but the straight X+42…+58/L±32 body projection overlaps pedestal X+51…+65/L±11; stepped/wrapped topology, auxiliary 2-pin seats and mating pull remain ASSUMPTION",
    "J-CAS-012/013/014/016 + selected body calipers + D-10 full harness dummy",
    "HOLD the dock-to-cassette joint; reject the straight face, prove a notched/wrapped body-off-accessible frame, recess live power, separate families and turn the chassis loom into R1/R2.",
    "ASSUMPTION",
    "ASM-31/CAS-10: record dock station, seat spacing, latch access, mating force, jacket anchor, ten cycles and parked chassis-half retention.",
    disposition="HOLD")
add("J-CAS-018", "ZK cassette", "electronics", 22.19, "ASM-22",
    "amp", "cassette_deck", "CLIP",
    "MAX98357A uses a 17.8 X ×19.4 L ×3 reference body on the insulated Z13…16 rear service deck; purchased-board holes/exits are ASSUMPTION",
    "J-CAS-005/006 + real amp calipers + ASM-08 measured sweep",
    "HOLD the amp seat; support and insulate the PCB, leave I2S XH5/speaker exits accessible and prove the deck stays clear of the charge thermal face and steering.",
    "ASSUMPTION",
    "ASM-22/55/CAS-05: record amp L/W/H, holes, insulation, XH5/PH2 exits, charge gap and measured moving clearance.",
    disposition="HOLD")

# ---- Camera, gimbal and blower -------------------------------------------------
add("J-CAM-001", "ZV camera", "camera", 26.01, "ASM-26", "ps10", "front_floor", "M3",
    "PS-10 common station envelope documented; actual base holes/station blocked by D-34/35",
    "Gate C and A-vs-B choice", "HOLD chassis-side gimbal base; when authorized, use only existing mapped M3 features/shared stack.",
    "ASSUMPTION", "ASM-26/53: record station, hole Ø/count, bolt lengths and roll datum.",
    disposition="HOLD")
add("J-CAM-002", "ZV camera", "camera", 26.02, "ASM-26", "pan_servo", "ps10", "DEFER",
    "MG90S clone body/ears/pitch/spline unmeasured",
    "MG90S arrival + J-CAM-001", "DEFER pan-servo mount; no nominal-clone pocket edits before calipers/no-force fit.",
    "ASSUMPTION", "ASM-54: record pan servo body/ears/hole Ø/pitch and exact BOM-compatible fastener.",
    disposition="DEFER")
add("J-CAM-003", "ZV camera", "camera", 26.03, "ASM-26", "tilt_servo", "pan_servo", "DEFER",
    "Orthogonal MG90S gimbal interface, horn and link geometry UNKNOWN",
    "Both MG90S arrived/centred", "DEFER tilt-to-pan connection; use only measured servo horns/screws and prove hand sweep before power.",
    "ASSUMPTION", "ASM-54: record axes, horn radius/hole Ø, retention and hard-stop clearance.",
    disposition="DEFER")
add("J-CAM-004", "ZV camera", "camera", 26.04, "ASM-26", "camera", "tilt_servo", "DEFER",
    "Camera board/heatsink/lens holes and cradle interface D-34 UNKNOWN",
    "D-34 camera measurements + J-CAM-003", "HOLD/DEFER camera cradle until the real board, lens and cable exits are measured; clamp no lens barrel.",
    "ASSUMPTION", "ASM-53: record camera holes, safe clamp lands, roll reference and service pull.",
    disposition="DEFER")
add("J-CAM-005", "ZV camera", "camera", 29.01, "ASM-29", "blower", "ps11", "DEFER",
    "Blower face/depth/outlet/hole pattern are D-34 UNKNOWN",
    "Real blower measured + PS-11 authorized", "HOLD blower mount; orient outlet toward duct and leave inlet fully open.",
    "ASSUMPTION", "ASM-53: record blower holes, fastener/clip, inlet plane and vibration isolation.",
    disposition="HOLD")
add("J-CAM-006", "ZV camera", "camera", 29.02, "ASM-29", "duct", "blower", "DEFER",
    "Nine SCAD inputs, collar and blower outlet are UNKNOWN until D-34",
    "J-CAM-005 + measured duct render", "HOLD duct collar; it must demate for camera service without prying on blower housing.",
    "ASSUMPTION", "ASM-53: record outlet/collar dimensions, retention and air-leak check.",
    disposition="HOLD")
add("J-CAM-007", "ZV camera", "camera", 29.03, "ASM-29", "duct", "camera", "DEFER",
    "Duct mouth/camera thermal face and stand-off are UNKNOWN",
    "J-CAM-004/006", "HOLD duct-to-camera interface; preserve lens/FOV and avoid contact with components not identified as thermal surfaces.",
    "ASSUMPTION", "ASM-53: airflow proof, lens clearance, temperature and independent removal.",
    disposition="HOLD")
add("J-CAM-008", "ZV camera", "camera", 33.08, "ASM-33", "camera_top", "body_rear", "M3",
    "Camera-top STL silhouette VERIFIED; attachment feature/hardware to 2024 rear shell unmeasured",
    "Body shell dry-assembled; camera Option B only if selected", "Dry-seat camera top on its authored shell station; use BOM M3 only if matching features are physically present—otherwise leave joint open.",
    "ASSUMPTION", "ASM-33/53: measure holes/contact land and record screw/nut/insert or approved bond.",
    disposition="HOLD")

# ---- Audio --------------------------------------------------------------------
add("J-AUD-001", "ZL audio", "audio", 22.30, "ASM-22", "amp", "ps04", "M3",
    "MAX98357A reference 19.4×17.8×3 ASSUMPTION for purchased board; two-screw pad unspecified",
    "Real amp measured + J-ELC-003", "Bench-fit amp; use BOM M3 only if board holes clear pads/traces and the deck pad supports the PCB.",
    "ASSUMPTION", "ASM-22/55: record board/hole pitch, standoff/insulation and fastener.",
    disposition="HOLD")
add("J-AUD-002", "ZL audio", "audio", 55.01, "ASM-55", "speaker", "ps14", "CLIP",
    "Speaker basket/hole/cone/port all D-36 UNKNOWN; compliant ring concept only",
    "D-36 real speaker measurements", "HOLD speaker-to-carrier joint; support basket rim only, never cone/surround, and keep ≥3 mm port/cone clearance.",
    "ASSUMPTION", "ASM-55: record basket holes/rim, isolation, retention and cone/port clearance.",
    disposition="HOLD")
add("J-AUD-003", "ZL audio", "audio", 55.02, "ASM-55", "ps14", "front_floor", "M3",
    "Left sidepod/fallback station documented; PS-14 floor/body interface un designed",
    "J-AUD-002 + D-03/DN-07", "HOLD carrier mount; use mapped existing M3/shared stack only and preserve body removal.",
    "ASSUMPTION", "ASM-55: record station, floor feature, bolt length, port direction and shell clearance.",
    disposition="HOLD")

# ---- Lighting -----------------------------------------------------------------
add("J-LGT-001", "ZL light", "lighting", 27.01, "ASM-27", "led", "rear_lens", "CLIP",
    "WS2812 strip and diffuser location DOCUMENTED; strip thickness/adhesive/channel fit D-36 UNKNOWN",
    "ASM-13 H-08 pre-route and actual strip offcut", "Seat the brake segment behind the unpainted lens without covering pads; provide pull-through strain relief.",
    "ASSUMPTION", "ASM-55: record pixel count/segment length, channel fit, retention and optical test.",
    disposition="HOLD")
add("J-LGT-002", "ZL light", "lighting", 13.01, "ASM-13", "rear_lens", "rear_wing", "M3",
    "Rear light diffuser sits in selected rear stack [DOCUMENTED]; mounting hole/clip and stack path unresolved",
    "Gate A/B rear stack chosen; H-08 laid first", "Install diffuser/lens only after the tail harness is in its channel; keep lens unpainted and removable.",
    "ASSUMPTION", "ASM-13/55: record receiver feature, hardware/clip and pull-through service.",
    disposition="HOLD")
for num, label in ((3, "left indicator"), (4, "right indicator")):
    add(f"J-LGT-{num:03d}", "ZL light", "lighting", 27.00 + num / 100, "ASM-27",
        "led", "ps18", "CLIP",
        f"{label.title()} segment/lens anchor is new concept; segment cut and retention D-36 UNKNOWN",
        "Actual strip offcut + PS-18 authorized", f"HOLD {label} segment in its unpainted lens/anchor without loading solder pads.",
        "ASSUMPTION", f"ASM-55: record {label} pixel count, cut line, anchor retention and shell/DRS clearance.",
        disposition="HOLD")
add("J-LGT-005", "ZL light", "lighting", 27.05, "ASM-27", "led", "halo", "CLIP",
    "Halo strip location DOCUMENTED; 2+2 pixel proposal/anchor/adhesive D-36 ASSUMPTION",
    "Actual strip + halo dry fit", "Dry-route halo segments on the underside/declared optical land; keep data direction and body disconnect lead serviceable.",
    "ASSUMPTION", "ASM-55: record pixel layout, cut points, retention and light bleed.",
    disposition="HOLD")
add("J-LGT-006", "ZL light", "lighting", 33.06, "ASM-33", "halo", "body_front", "M3",
    "Halo and front-shell meshes VERIFIED; attachment features/hardware unmeasured",
    "J-LGT-005 and painted shell cured", "Dry-seat halo on the front body; use BOM M3 only where matching features exist, otherwise await an approved bond method.",
    "ASSUMPTION", "ASM-33/55: record holes/contact lands, retention and body-off harness path.",
    disposition="HOLD")

# ---- Hall sensor ---------------------------------------------------------------
add("J-SNS-001", "ZH sensor", "sensor", 24.01, "ASM-24", "magnet", "output_shaft", "DEFER",
    "Magnet Ø3×1 DOCUMENTED; final shaft carrier, keyed recess/bond land and runout UNKNOWN",
    "Magnets arrive + final rear carrier/shaft assembled", "DEFER magnet bond; select a radial station with no belt/bearing conflict and key/bond only after dry-run gap proof.",
    "ASSUMPTION", "ASM-57: record shaft land, keyed feature/bond, runout and retention after hand spin.",
    disposition="DEFER")
add("J-SNS-002", "ZH sensor", "sensor", 24.02, "ASM-24", "hall", "ps16", "DEFER",
    "A3144 body max 4.17×3.10×1.57 DOCUMENTED; clip/fastener and sensitive face orientation physical",
    "J-SNS-001 + PS-16 authorized", "DEFER sensor retention; place the active face toward the magnet and strain-relieve leads outside the 1–3 mm adjustment.",
    "ASSUMPTION", "ASM-57: identify active face, clip/fastener, lead strain relief and repeatable 1.5 mm cold setting.",
    disposition="DEFER")
add("J-SNS-003", "ZH sensor", "sensor", 24.03, "ASM-24", "ps16", "rear_carrier_l", "DEFER",
    "PS-16 clips to selected bearing-carrier region; mount geometry depends on Gate A and magnet station",
    "J-SNS-001/002 + final rear carrier", "DEFER bracket joint; use a reversible M3/shared feature only after full axle play is known.",
    "ASSUMPTION", "ASM-57: record carrier feature, exact BOM fastener, adjustment range and ≥8 mm belt/gear clearance.",
    disposition="DEFER")

# ---- Body and shell ------------------------------------------------------------
add("J-BDY-001", "ZB body", "body", 4.02, "ASM-04", "insert", "body_front", "INSERT",
    "Three body service bosses documented for M3 mounting; actual insert OD boss wall/depth unmeasured",
    "Printed shell inspected and insert policy accepted", "Heat-set inserts only where the boss has enough wall/depth; keep each square to its mating screw axis.",
    "ASSUMPTION", "ASM-04: record boss ID/wall/depth and which of three positions receives inserts.",
    disposition="HOLD")
add("J-BDY-002", "ZB body", "body", 33.01, "ASM-33", "body_front", "body_rear", "M3",
    "Clamshell panel joint DOCUMENTED; 2023 drawing's 12×M3 count does not verify 2024 panel count",
    "Paint cured; internal modules tested", "Join front and rear shell panels at their matching lands; start every present M3 feature before snugging.",
    "ASSUMPTION", "ASM-33: count/measure 2024 panel holes, record exact BOM lengths and nut/insert/self-thread retention.",
    disposition="HOLD")
add("J-BDY-003", "ZB body", "body", 33.02, "ASM-33", "body_front", "front_floor", "M3",
    "2024 README documents two M3 screws front-floor→front body; holes intentionally tight/self-threading",
    "J-BDY-002 + shell landing check", "Lower shell without dragging harnesses, start both floor-to-body M3 screws by hand, and snug once.",
    "DOCUMENTED", "ASM-33: record hole Ø, chosen bolt lengths and insert vs self-thread decision.",
    evidence="2024 body READ ME")
add("J-BDY-004", "ZB body", "body", 33.03, "ASM-33", "nose", "front_floor", "M3",
    "2024 README documents one M3 nose→front-floor screw; hole intentionally tight/self-threading",
    "J-BDY-003", "Seat nose on its landing, hand-start the single M3 from nose to floor and stop as soon as the shell is retained.",
    "DOCUMENTED", "ASM-33: record hole Ø, bolt length and insert vs self-thread decision.",
    evidence="2024 body READ ME")
add("J-BDY-005", "ZB body", "body", 33.04, "ASM-33", "front_wing", "nose", "M3",
    "Separate revised front wing/nose installation DOCUMENTED; exact 2024 hole count/Ø/bolt length unverified",
    "J-BDY-004", "Offer wing to nose/front-floor interface without flexing; start all matching M3 fasteners before snugging.",
    "ASSUMPTION", "ASM-33: count/measure holes, record bolt lengths/retention and sacrificial service behavior.",
    disposition="HOLD")
for num, side in ((6, "left"), (7, "right")):
    add(f"J-BDY-{num:03d}", "ZB body", "body", 33.10 + num / 100, "ASM-33",
        "mirror", "body_front", "BOND",
        f"{side.title()} mirror mesh exists; shell landing and fastener/bond are unmeasured",
        "Paint cured; mirror orientation confirmed", f"Dry-seat the {side} mirror; do not drill the shell or choose adhesive until contact area and service intent are recorded.",
        "ASSUMPTION", f"ASM-33: photograph {side} landing, measure contact/holes and record approved retention.",
        disposition="HOLD")
add("J-BDY-008", "ZB body", "body", 33.20, "ASM-33", "body_front", "front_floor", "LAND",
    "Shell landing points derive from registered meshes; exact physical contact and S0 remain P1",
    "All internal harnesses dressed", "Lower shell vertically and verify every intended landing contacts without resting on electronics or steering.",
    "ASSUMPTION", "ASM-33/P1: feeler-map landing points, S0 and any unintended contact; no shim/relief by implication.",
    disposition="HOLD")
add("J-BDY-009", "ZB body", "body", 33.21, "ASM-33", "body_rear", "rear_floor", "LAND",
    "Rear shell landing is mesh-derived but physical stack/wing/harness state remains open",
    "Rear stack and H-08 closed", "Seat rear shell onto donor landing points while watching tail harness, shock and antenna routes.",
    "ASSUMPTION", "ASM-33: feeler-map rear landings and prove no harness or moving part carries shell load.",
    disposition="HOLD")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def confidence_class(value: str) -> str:
    return value.lower()


CSS = r"""
:root {
  color-scheme:light dark;
  --bg:#edf1f0; --paper:#fff; --ink:#15201f; --muted:#596866;
  --line:#bdc9c7; --grid:#dce3e2; --ground:#d8dfde; --accent:#00857c;
  --soft:#e7f4f2; --warn:#b05b22; --bad:#bf3f35; --assume:#687573;
  --shadow:0 1px 2px rgba(20,32,31,.08),0 9px 25px rgba(20,32,31,.06);
}
@media (prefers-color-scheme: dark) {
  :root { --bg:#0c1211; --paper:#121b1a; --ink:#e7eeed; --muted:#9aa9a6;
    --line:#2a3a38; --grid:#263230; --ground:#1d2927; --accent:#27c9b9;
    --soft:#163330; --warn:#e08a4f; --bad:#e06758; --assume:#9ba8a6;
    --shadow:0 1px 2px rgba(0,0,0,.42),0 10px 30px rgba(0,0,0,.35); }
}
:root[data-theme="light"] { --bg:#edf1f0; --paper:#fff; --ink:#15201f; --muted:#596866;
  --line:#bdc9c7; --grid:#dce3e2; --ground:#d8dfde; --accent:#00857c;
  --soft:#e7f4f2; --warn:#b05b22; --bad:#bf3f35; --assume:#687573;
  --shadow:0 1px 2px rgba(20,32,31,.08),0 9px 25px rgba(20,32,31,.06); }
:root[data-theme="dark"] { --bg:#0c1211; --paper:#121b1a; --ink:#e7eeed; --muted:#9aa9a6;
  --line:#2a3a38; --grid:#263230; --ground:#1d2927; --accent:#27c9b9;
  --soft:#163330; --warn:#e08a4f; --bad:#e06758; --assume:#9ba8a6;
  --shadow:0 1px 2px rgba(0,0,0,.42),0 10px 30px rgba(0,0,0,.35); }
* { box-sizing:border-box; }
html,body { margin:0; min-height:100%; }
body { overflow-x:hidden; background:var(--bg); color:var(--ink);
  font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }
a { color:var(--accent); text-underline-offset:.18em; }
code,.mono,.tag,th,svg text { font-family:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace; }
header { background:var(--paper); border-bottom:1px solid var(--line); }
.bar,.page { width:min(1420px,calc(100% - 32px)); margin:auto; }
.bar { min-height:62px; display:flex; justify-content:space-between; align-items:center; gap:16px; }
.brand { min-width:0; display:flex; gap:12px; align-items:baseline; }
.brand b,.eyebrow { color:var(--accent); letter-spacing:.13em; text-transform:uppercase; }
.brand span { color:var(--muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
button { border:1px solid var(--line); color:var(--ink); background:var(--paper);
  border-radius:7px; padding:7px 10px; cursor:pointer; }
main { padding:30px 0 58px; }
h1 { font-size:clamp(1.8rem,4vw,3rem); line-height:1.07; margin:.15em 0 .3em; text-wrap:balance; }
h2 { font:700 13px/1.4 ui-monospace,monospace; letter-spacing:.13em;
  text-transform:uppercase; color:var(--muted); margin:0 0 5px; }
h3 { margin:0 0 7px; font-size:1rem; }
p { max-width:100ch; }
.lede { font-size:clamp(15px,1.6vw,18px); color:var(--muted); margin-top:0; }
.board { background:var(--paper); border:1px solid var(--line); border-radius:13px;
  box-shadow:var(--shadow); padding:clamp(14px,2.4vw,26px); margin-top:24px; }
.sub { color:var(--muted); margin:2px 0 14px; font-size:13.5px; }
.drawing { width:100%; overflow-x:auto; overscroll-behavior-inline:contain;
  border:1px solid var(--line); border-radius:9px; background:var(--paper); }
.drawing svg { display:block; width:max(100%,var(--drawing-w,1200px)); height:auto; }
.legend,.cards,.summary { display:grid; gap:12px; }
.legend { grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); margin-top:13px; }
.legend span { display:flex; align-items:center; gap:9px; color:var(--muted); font-size:12px; }
.swatch { width:40px; height:16px; background:var(--soft); border:2px solid var(--accent); }
.swatch.documented { border-style:dotted; }
.swatch.assumption { border-color:var(--assume); border-style:dashed;
  background:repeating-linear-gradient(135deg,transparent 0 5px,color-mix(in srgb,var(--assume) 20%,transparent) 5px 7px); }
.cards,.summary { grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); }
.card { display:block; color:var(--ink); text-decoration:none; border:1px solid var(--line);
  border-left:5px solid var(--accent); border-radius:10px; padding:14px; background:var(--paper); }
.card p { margin:5px 0 0; color:var(--muted); font-size:12.5px; }
.tag { display:inline-block; border:1px solid currentColor; border-radius:4px;
  padding:2px 6px; font-size:10px; font-weight:800; letter-spacing:.05em; color:var(--accent); }
.tag.documented { border-style:dotted; }
.tag.assumption { color:var(--assume); border-style:dashed; }
.tag.defer { color:var(--bad); }
.orderstrip { display:flex; gap:7px; overflow-x:auto; padding:10px 0 2px; }
.orderstrip a { flex:0 0 auto; border:1px solid var(--line); border-radius:6px;
  padding:6px 8px; text-decoration:none; font:700 10px/1.2 ui-monospace,monospace; }
.tablewrap { width:100%; overflow-x:auto; border:1px solid var(--line); border-radius:9px; }
table { border-collapse:collapse; width:100%; min-width:1120px; background:var(--paper); }
th,td { padding:9px 10px; text-align:left; vertical-align:top; border-bottom:1px solid var(--grid); }
th { color:var(--muted); font-size:10px; letter-spacing:.06em; text-transform:uppercase; }
tr:last-child td { border-bottom:0; }
.note { border-left:3px solid var(--accent); background:var(--soft); padding:12px 15px;
  border-radius:0 9px 9px 0; margin:16px 0 0; color:var(--muted); font-size:13px; }
footer { border-top:1px solid var(--line); color:var(--muted); padding:22px 0 34px; font-size:12.5px; }
svg .gridline { stroke:var(--grid); stroke-width:.7; }
svg .axis { stroke:var(--ink); stroke-width:1.5; fill:none; }
svg .leader { stroke:var(--muted); stroke-width:1; fill:none; }
svg .arrow { stroke:var(--accent); stroke-width:1.5; fill:none; marker-end:url(#arr); }
svg .conf-verified { stroke:var(--accent); stroke-width:2; fill:color-mix(in srgb,var(--accent) 13%,transparent); }
svg .conf-documented { stroke:var(--accent); stroke-width:1.6; stroke-dasharray:2 4; fill:color-mix(in srgb,var(--accent) 8%,transparent); }
svg .conf-assumption { stroke:var(--assume); stroke-width:1.6; stroke-dasharray:7 5; fill:url(#hatch); }
svg .defer { stroke:var(--bad); stroke-width:1.8; stroke-dasharray:7 5; fill:url(#deferHatch); }
svg .balloon { fill:var(--paper); stroke:var(--line); stroke-width:1; }
svg .label { fill:var(--ink); font-size:11px; }
svg .small { fill:var(--muted); font-size:9.5px; }
svg .tiny { fill:var(--muted); font-size:8px; }
svg .accent { fill:var(--accent); }
svg .badtext { fill:var(--bad); font-weight:800; }
@media(max-width:640px) { .bar,.page { width:min(100% - 20px,1420px); }
  main { padding-top:20px; } .brand span { display:none; } }
"""


JS = r"""
(() => {
  const root=document.documentElement, btn=document.querySelector("[data-theme-toggle]");
  if(!btn) return;
  btn.addEventListener("click",()=>{
    const current=root.dataset.theme;
    root.dataset.theme=current==="dark"?"light":current==="light"?"dark":
      matchMedia("(prefers-color-scheme: dark)").matches?"light":"dark";
    btn.textContent=root.dataset.theme==="dark"?"Light":"Dark";
  });
})();
"""


def page_start(title: str, subtitle: str, up: str = "../index.html") -> str:
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; font-src data:">
<title>{esc(title)} · W17 connections</title><style>{CSS}</style></head><body>
<header><div class="bar"><div class="brand"><b>W17 / RC-01</b><span>{esc(subtitle)}</span></div>
<div><a href="{esc(up)}">Overview</a> · <button data-theme-toggle type="button">Theme</button></div>
</div></header><main><div class="page">"""


def page_end() -> str:
    return f"""</div></main><footer><div class="page">Generated by
<code>10_assembly_architecture/evidence/scripts/p0_10_connection_visualizations.py</code>.
Source STLs remain read-only. Dashed/hatched geometry is not production authority.</div></footer>
<script>{JS}</script></body></html>"""


def _png_rgba(canvas: np.ndarray) -> bytes:
    h, w, channels = canvas.shape
    assert channels == 4
    raw = b"".join(b"\x00" + canvas[y].tobytes() for y in range(h))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(
            ">I", zlib.crc32(kind + data) & 0xFFFFFFFF
        )

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


MESH_CACHE: dict[str, tuple[str, float, float]] = {}


def mesh_silhouette(key: str) -> tuple[str, float, float]:
    """Return transparent orthographic STL silhouette URI and projected mm span."""
    if key in MESH_CACHE:
        return MESH_CACHE[key]
    part = PARTS[key]
    path = REPO / part.mesh
    loaded = trimesh.load_mesh(path, process=False)
    mesh = trimesh.util.concatenate(tuple(loaded.geometry.values())) if isinstance(loaded, trimesh.Scene) else loaded
    bounds = np.asarray(mesh.bounds, dtype=float)
    spans = bounds[1] - bounds[0]
    axes = list(np.argsort(spans)[::-1][:2])
    width_mm, height_mm = float(spans[axes[0]]), float(spans[axes[1]])
    px_per_mm = min(4.0, 720.0 / max(width_mm, height_mm, 1.0))
    width = max(8, int(math.ceil(width_mm * px_per_mm)) + 6)
    height = max(8, int(math.ceil(height_mm * px_per_mm)) + 6)
    seed = int(hashlib.sha256(part.mesh.encode()).hexdigest()[:8], 16)
    count = min(110000, max(28000, len(mesh.faces) * 8))
    points, _ = trimesh.sample.sample_surface(mesh, count, seed=seed)
    uv = points[:, axes]
    uv -= uv.min(axis=0)
    x = np.clip((uv[:, 0] * px_per_mm + 3).astype(int), 1, width - 2)
    y = np.clip((height - 4 - uv[:, 1] * px_per_mm).astype(int), 1, height - 2)
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    color = np.array([24, 154, 143, 224], dtype=np.uint8)
    for ox, oy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1)):
        canvas[np.clip(y + oy, 0, height - 1), np.clip(x + ox, 0, width - 1)] = color
    uri = "data:image/png;base64," + base64.b64encode(_png_rgba(canvas)).decode("ascii")
    MESH_CACHE[key] = (uri, width_mm, height_mm)
    return MESH_CACHE[key]


def svg_defs() -> str:
    return """<defs>
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" class="gridline" fill="none"/></pattern>
<pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="9" stroke="var(--assume)" opacity=".45"/></pattern>
<pattern id="deferHatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="9" stroke="var(--bad)" stroke-width="2" opacity=".45"/></pattern>
<marker id="arr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8Z" fill="context-stroke"/></marker>
</defs>"""


def part_visual(key: str, cx: float, cy: float, scale: float, disposition: str) -> str:
    part = PARTS[key]
    cls = "defer" if disposition == "DEFER" else f"conf-{part.confidence.lower()}"
    if part.mesh:
        uri, wmm, hmm = mesh_silhouette(key)
        w, h = wmm * scale, hmm * scale
        # Mesh silhouette is VERIFIED geometry; the dashed box carries any
        # weaker installation confidence without falsifying the mesh itself.
        box = ""
        if part.confidence == "ASSUMPTION" or disposition == "DEFER":
            box = f'<rect class="{cls}" x="{cx-w/2-4:.1f}" y="{cy-h/2-4:.1f}" width="{w+8:.1f}" height="{h+8:.1f}" rx="5"/>'
        return box + f'<image href="{uri}" x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="xMidYMid meet"/>'
    if part.dims is None:
        wmm, hmm = 42.0, 24.0
        cls = "defer" if disposition == "DEFER" else "conf-assumption"
    else:
        wmm, hmm = part.dims
    w, h = max(8.0, wmm * scale), max(6.0, hmm * scale)
    x, y = cx - w / 2, cy - h / 2
    if part.shape in {"bearing", "ring", "tyre", "pulley", "gear", "magnet"}:
        r = min(w, h) / 2
        inner = r * (0.56 if part.shape in {"bearing", "tyre", "ring"} else 0.28)
        return f'<circle class="{cls}" cx="{cx}" cy="{cy}" r="{r:.1f}"/><circle cx="{cx}" cy="{cy}" r="{inner:.1f}" fill="var(--paper)" stroke="var(--accent)"/>'
    if part.shape in {"rod", "pin", "shaft", "sleeve", "antenna"}:
        return f'<rect class="{cls}" x="{x:.1f}" y="{cy-max(2,h/2):.1f}" width="{w:.1f}" height="{max(4,h):.1f}" rx="{max(2,h/2):.1f}"/>'
    if part.shape == "horn":
        return f'<path class="{cls}" d="M{x:.1f} {cy:.1f}H{x+w:.1f}M{cx:.1f} {cy-h/2:.1f}V{cy+h/2:.1f}"/><circle class="{cls}" cx="{cx}" cy="{cy}" r="8"/>'
    if part.shape == "shock":
        return f'<circle class="{cls}" cx="{x+7:.1f}" cy="{cy}" r="7"/><rect class="{cls}" x="{x+14:.1f}" y="{cy-h/3:.1f}" width="{max(10,w-28):.1f}" height="{max(8,2*h/3):.1f}" rx="5"/><circle class="{cls}" cx="{x+w-7:.1f}" cy="{cy}" r="7"/>'
    if part.shape == "belt":
        return f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}"/><rect x="{x+5:.1f}" y="{y+5:.1f}" width="{max(1,w-10):.1f}" height="{max(1,h-10):.1f}" rx="{max(1,h/2-5):.1f}" fill="var(--paper)" stroke="var(--line)"/>'
    return f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="5"/>'


def hardware_visual(joint: Joint, cx: float, cy: float) -> str:
    cls = "defer" if joint.disposition == "DEFER" else f"conf-{joint.confidence.lower()}"
    text = joint.hardware.lower()
    if "bearing" in text:
        return f'<circle class="{cls}" cx="{cx}" cy="{cy}" r="22"/><circle cx="{cx}" cy="{cy}" r="11" fill="var(--paper)" stroke="var(--accent)"/>'
    if "rod" in text or "turnbuckle" in text:
        return f'<line class="{cls}" x1="{cx-40}" y1="{cy}" x2="{cx+40}" y2="{cy}"/><circle class="{cls}" cx="{cx-40}" cy="{cy}" r="8"/><circle class="{cls}" cx="{cx+40}" cy="{cy}" r="8"/>'
    if "insert" in text:
        return f'<path class="{cls}" d="M{cx-14} {cy-18}H{cx+14}V{cy+18}H{cx-14}Z M{cx-8} {cy-18}V{cy+18}M{cx} {cy-18}V{cy+18}M{cx+8} {cy-18}V{cy+18}"/>'
    if "m3" in text or "m4" in text or "screw" in text or "bolt" in text:
        return f'<path class="{cls}" d="M{cx-10} {cy-14}H{cx+10}V{cy-7}H{cx+4}V{cy+28}H{cx-4}V{cy-7}H{cx-10}Z"/><path class="{cls}" d="M{cx-4} {cy+4}l8 5-8 5 8 5-8 5"/>'
    return f'<rect class="{cls}" x="{cx-34}" y="{cy-18}" width="68" height="36" rx="6"/>'


def wrap_svg_text(text: str, x: float, y: float, width: int = 46, cls: str = "small") -> str:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        if len(line) + len(word) + 1 > width and line:
            lines.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        lines.append(line)
    return "".join(
        f'<text class="{cls}" x="{x}" y="{y+i*12}">{esc(line)}</text>'
        for i, line in enumerate(lines[:3])
    )


def exploded_svg(rows: list[Joint]) -> str:
    width, card_h, scale = 1200, 250, 1.5
    height = 25 + card_h * len(rows)
    out = [f'<svg style="--drawing-w:{width}px" viewBox="0 0 {width} {height}" role="img" aria-label="Exploded connection sequence at 1.5 px/mm">',
           svg_defs(), f'<rect width="{width}" height="{height}" fill="url(#grid)"/>']
    for i, joint in enumerate(rows):
        y0, cy = 20 + i * card_h, 20 + i * card_h + 144
        akey, bkey = PART_KEY_BY_NAME[joint.part_a], PART_KEY_BY_NAME[joint.part_b]
        out += [
            f'<g id="{joint.joint_id}">',
            f'<rect class="balloon" x="15" y="{y0}" width="1170" height="230" rx="10"/>',
            f'<text class="accent label" x="30" y="{y0+22}">{joint.joint_id} · {joint.asm_step} · {esc(joint.disposition)} · {esc(joint.confidence)}</text>',
            f'<line class="arrow" x1="410" y1="{cy}" x2="555" y2="{cy}"/>',
            f'<line class="arrow" x1="645" y1="{cy}" x2="790" y2="{cy}"/>',
            part_visual(akey, 310, cy, scale, joint.disposition),
            hardware_visual(joint, 600, cy),
            part_visual(bkey, 890, cy, scale, joint.disposition),
            f'<rect class="balloon" x="35" y="{y0+34}" width="315" height="72" rx="5"/>',
            f'<text class="label" x="48" y="{y0+52}">A · {esc(joint.part_a)}</text>',
            wrap_svg_text(joint.interface, 48, y0 + 67, 52, "tiny"),
            f'<rect class="balloon" x="405" y="{y0+34}" width="390" height="72" rx="5"/>',
            f'<text class="label" x="418" y="{y0+52}">HARDWARE + SIZE</text>',
            wrap_svg_text(joint.hardware, 418, y0 + 67, 62, "tiny"),
            f'<rect class="balloon" x="850" y="{y0+34}" width="315" height="72" rx="5"/>',
            f'<text class="label" x="863" y="{y0+52}">B · {esc(joint.part_b)}</text>',
            wrap_svg_text("dependency: " + joint.dependency, 863, y0 + 67, 50, "tiny"),
            f'<line class="axis" x1="32" y1="{y0+211}" x2="107" y2="{y0+211}"/>',
        ]
        for tick in range(6):
            x = 32 + tick * 15
            out.append(f'<line class="leader" x1="{x}" y1="{y0+207}" x2="{x}" y2="{y0+216}"/>')
        out += [
            f'<text class="tiny" x="32" y="{y0+226}">50 mm ruler · 1.5 px/mm</text>',
            f'<text class="small" x="200" y="{y0+222}">assembly axis → · silhouette geometry stays to scale; unknown hardware remains dashed/hatched</text>',
            "</g>",
        ]
    out.append("</svg>")
    return "".join(out)


def confidence_legend() -> str:
    return """<div class="legend">
<span><i class="swatch"></i>VERIFIED · solid · measured STL/interface evidence</span>
<span><i class="swatch documented"></i>DOCUMENTED · dotted · drawing/BOM/supplier specification</span>
<span><i class="swatch assumption"></i>ASSUMPTION · dashed + hatched · physical ASM check required</span>
<span><i class="swatch assumption" style="border-color:var(--bad)"></i>DEFER · in transit/unselected · no substitute authorized</span>
</div>"""


def joint_table(rows: list[Joint]) -> str:
    body = []
    for j in rows:
        body.append(f"""<tr id="row-{j.joint_id}"><td><code>{j.joint_id}</code><br><span class="tag {confidence_class(j.confidence)}">{j.confidence}</span> <span class="tag {'defer' if j.disposition == 'DEFER' else 'assumption'}">{j.disposition}</span></td>
<td>{esc(j.part_a)}<br>→ {esc(j.part_b)}</td><td>{esc(j.interface)}</td><td>{esc(j.hardware)}<br><b>Retention:</b> {esc(j.fastening_retention)}</td>
<td><b>{esc(j.asm_step)}</b> · {esc(j.instruction)}<br><b>First:</b> {esc(j.dependency)}</td>
<td>{esc(j.tool)}<br><b>Torque:</b> {esc(j.torque_threadlock)}</td><td>{esc(j.asm_check)}</td></tr>""")
    return """<div class="tablewrap"><table><thead><tr><th>Joint / state</th><th>Parts</th><th>Interface</th><th>BOM hardware / retention</th><th>Assembly instruction / dependency</th><th>Tool / torque</th><th>Physical closure</th></tr></thead><tbody>""" + "".join(body) + "</tbody></table></div>"


def assembly_page(key: str, rows: list[Joint]) -> str:
    seq, title, _ = ASSEMBLIES[key]
    deferred = sum(j.disposition == "DEFER" for j in rows)
    page = page_start(title, "exploded connection atlas")
    page += f"""<p class="eyebrow">connection atlas / assembly {seq}</p><h1>{esc(title)}</h1>
<p class="lede">{len(rows)} physical joints, ordered by the existing ASM sequence. Each strip separates the two neighbours along the assembly axis, names the only authorized BOM family, and carries the weakest confidence. {deferred} joint(s) are DEFERRED.</p>
<div class="board"><h2>Assembles in this order</h2><div class="orderstrip">"""
    page += "".join(f'<a href="#row-{j.joint_id}">{j.joint_id}<br>{j.asm_step}</a>' for j in rows)
    page += f"""</div></div><div class="board"><h2>Exploded connection diagram</h2>
<p class="sub">1.5 px/mm orthographic silhouettes and a 50 mm ruler. Mesh-backed parts are real STL silhouettes; hardware without a controlled mesh is a technical outline. Installation uncertainty is overlaid dashed/hatched.</p>
<div class="drawing">{exploded_svg(rows)}</div></div>
<div class="board"><h2>Confidence & deferral legend</h2>{confidence_legend()}</div>
<div class="board"><h2>Joint-level work instructions</h2>{joint_table(rows)}</div>
<div class="note"><b>Scope discipline:</b> this page specifies how neighbours connect. It does not revise fit/clearance results, placement coordinates, gates, component values, or any STL. “Snug” remains the plastic-thread rule; a row without a measured length does not authorize choosing one silently.</div>"""
    return page + page_end()


def connection_index() -> str:
    cards = []
    total = 0
    for key, (seq, title, filename) in ASSEMBLIES.items():
        rows = sorted((j for j in JOINTS if j.assembly == key), key=lambda j: j.order)
        total += len(rows)
        deferred = sum(j.disposition == "DEFER" for j in rows)
        cards.append(f'<a class="card" href="{filename}"><span class="tag">ASSEMBLY {seq}</span> <b>{esc(title)}</b><p>{len(rows)} joints · {deferred} DEFER · {rows[0].asm_step}→{rows[-1].asm_step}</p></a>')
    page = page_start("Mechanical connection atlas", "joint-by-joint build drawings")
    page += f"""<p class="eyebrow">10_assembly_architecture / viz / connections</p>
<h1>Mechanical connection atlas</h1><p class="lede">{total} registered physical joints across twelve assemblies. Every page uses the same evidence discipline: solid VERIFIED mesh/interface, dotted DOCUMENTED hardware, dashed/hatched ASSUMPTION, and explicit DEFER for unselected or in-transit hardware.</p>
<div class="summary"><div class="card"><b>{total}</b><p>joint rows</p></div><div class="card"><b>{len(ASSEMBLIES)}</b><p>exploded assembly sheets</p></div><div class="card"><b>{sum(j.disposition == 'DEFER' for j in JOINTS)}</b><p>deferred connections</p></div></div>
<div class="board"><h2>Exploded assembly sheets</h2><div class="cards">{''.join(cards)}</div></div>
<div class="board"><h2>Evidence convention</h2>{confidence_legend()}<p class="sub mono">Register: ../../Z_connection_joint_register.md + .csv · build order: ../../P_assembly_master_manual.md</p></div>"""
    return page + page_end()


def csv_text() -> str:
    fields = list(asdict(JOINTS[0]).keys())
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for joint in sorted(JOINTS, key=lambda j: (j.order, j.joint_id)):
        writer.writerow(asdict(joint))
    return stream.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def register_markdown() -> str:
    ordered = sorted(JOINTS, key=lambda j: (j.order, j.joint_id))
    lines = [
        "# Z · Mechanical Connection / Joint Register",
        "",
        "Generated by `evidence/scripts/p0_10_connection_visualizations.py`. This is the",
        "project-wide physical-connection execution layer. It does **not** revise fit",
        "analysis, placements, gates, component values, conclusions, or source STLs.",
        "",
        f"**Coverage:** {len(JOINTS)} joint rows · {len(ASSEMBLIES)} assemblies · "
        f"{sum(j.disposition == 'DEFER' for j in JOINTS)} DEFER rows.",
        "",
        "The CSV twin is the sortable authority: sort `zone`, `order`, `asm_step`,",
        "`confidence`, or `disposition`. `READY` means the documented sequence may be",
        "attempted at its gate; `HOLD` means a named physical/design closure remains;",
        "`DEFER` means hardware is in transit or unselected and **no substitute is",
        "authorized**. Exact unmeasured lengths/threads remain ASSUMPTION.",
        "",
        "Confidence: **VERIFIED** = reproduced STL/interface evidence; **DOCUMENTED** =",
        "controlled drawing/BOM/supplier statement; **ASSUMPTION** = physical closure",
        "still required. The joint confidence is the weakest fact needed to close it.",
        "",
        "## Z.1 Assembly-order register",
        "",
        "| Order | Joint | Zone | ASM | Parts joined | Interface feature | BOM hardware + retention | Dependency / do | Tool + torque/threadlock | Confidence / state | ASM physical check |",
        "|---:|---|---|---|---|---|---|---|---|---|---|",
    ]
    for j in ordered:
        lines.append(
            f"| {j.order:.2f} | `{j.joint_id}` | {md_cell(j.zone)} | {j.asm_step} | "
            f"{md_cell(j.part_a)} → {md_cell(j.part_b)} | {md_cell(j.interface)} | "
            f"{md_cell(j.hardware)}; **retention:** {md_cell(j.fastening_retention)} | "
            f"**First:** {md_cell(j.dependency)}; **Do:** {md_cell(j.instruction)} | "
            f"{md_cell(j.tool)}; **torque:** {md_cell(j.torque_threadlock)} | "
            f"**{j.confidence} / {j.disposition}** | {md_cell(j.asm_check)} |"
        )
    lines += ["", "## Z.2 Zone-sort index", "",
              "Use this compact view for zone ownership; follow the linked Joint IDs in",
              "Z.1 or sort the CSV for the complete row.", "",
              "| Zone | Joint IDs in assembly order |", "|---|---|"]
    for zone in sorted({j.zone for j in JOINTS}):
        ids = [f"`{j.joint_id}`" for j in ordered if j.zone == zone]
        lines.append(f"| {zone} | {' · '.join(ids)} |")
    lines += ["", "## Z.3 Mandatory deferred-hardware rule", "",
              "The following stay open until the real item is present and measured:",
              "",
              "- MG90S pan/tilt/DRS joints (`J-CAM-*`, `J-REA-030…033`).",
              "- Cassette-pedestal gimbal and conduit joints while the two MG90S units",
              "  and their real leads remain unavailable (`J-CAS-011/016`).",
              "- 68 mm rear-shock eyes (`J-REA-027/028`).",
              "- Hall magnet and dependent bracket stack (`J-SNS-001…003`).",
              "- Exact 2S pack retention (`J-PWR-002`).",
              "- USB-C 2S balancing charge module, hidden port and charge/run interlock",
              "  (`J-CHG-001…004`, SKU TBD).",
              "- Tyre bead/bond rows while the actual Tamiya tyres are not physically",
              "  available (`J-FRT-022/023`, `J-REA-023/024`).",
              "",
              "A DEFER row is not permission to buy, drill, glue, resize a pocket, or",
              "substitute a plausible fastener. Close its named ASM check first.",
              ""]
    return "\n".join(lines)


def manual_block() -> str:
    lines = [
        MANUAL_START,
        "",
        "## P.8 Joint-controlled build sequence (generated; project-wide standard)",
        "",
        "This appendix is the build-floor expansion of the existing ASM steps. Every",
        "mechanical neighbour pair has one Joint ID in",
        "[`Z_connection_joint_register.md`](Z_connection_joint_register.md); the",
        "[sortable CSV](Z_connection_joint_register.csv) is the machine-readable twin.",
        "It adds connection execution detail only: no fit result, value, gate, placement",
        "or STL is changed. A checked box requires the row's physical closure to be",
        "recorded in the ASM note. **DEFER means stop at that row.**",
        "",
        "### Charge-module stop rule for ASM-59",
        "",
        "Prereq: OP-49 module selection and separate charge-safety authorization. The",
        "5 V USB-C → 2S balancing module, hidden port and charge/run interlock remain",
        "SKU/interface TBD; 30×25×10 is a TARGET envelope only. Execute",
        "`J-CHG-001…004` only after the real hardware is measured; no circuit,",
        "pocket, fastener or shell cut is inferred.",
        "",
    ]
    grouped: dict[str, list[Joint]] = {}
    for joint in sorted(JOINTS, key=lambda j: (j.order, j.joint_id)):
        grouped.setdefault(joint.asm_step, []).append(joint)
    for step in sorted(grouped, key=lambda s: (int(re.search(r"\d+", s).group()), s)):
        rows = grouped[step]
        title = ASSEMBLIES[rows[0].assembly][1]
        lines += [f"### {step} joint closure · {title}", ""]
        for j in rows:
            state = f"**{j.confidence} / {j.disposition}**"
            lines += [
                f"- [ ] **{j.joint_id} — {j.part_a} → {j.part_b}.** {state}",
                f"  **First:** {j.dependency}. **Hardware/interface:** {j.hardware};",
                f"  {j.interface}. **Do:** {j.instruction}",
                f"  **Retention:** {j.fastening_retention}. **Tool:** {j.tool}.",
                f"  **Torque/threadlock:** {j.torque_threadlock}",
                f"  **Close only when:** {j.asm_check}",
            ]
        lines.append("")
    lines += [
        "### ASM-60 · Connection closure audit",
        "",
        "Prereq: all applicable ASM steps complete. Sort the CSV by `disposition`,",
        "confirm every installed joint is recorded READY with its physical check, and",
        "confirm every HOLD/DEFER row is still visibly open—never silently treated as",
        "installed. Re-run `p0_11_validate_connection_outputs.py`; archive the signed",
        "CSV/filter result with the ASM session note.",
        "",
        MANUAL_END,
    ]
    return "\n".join(lines)


def replace_generated(path: Path, start: str, end: str, block: str, anchor: str | None = None) -> None:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        text = pattern.sub(block, text)
    elif anchor and anchor in text:
        text = text.replace(anchor, block + "\n" + anchor, 1)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def master_index_block() -> str:
    cards = []
    for key, (seq, title, filename) in ASSEMBLIES.items():
        rows = [j for j in JOINTS if j.assembly == key]
        cards.append(
            f'<a class="gate rank-watch" href="connections/{filename}">'
            f'<span class="tag documented">CONNECTION {seq}</span> <b>{esc(title)}</b>'
            f'<p>{len(rows)} joints · {sum(j.disposition == "DEFER" for j in rows)} DEFER · exploded + joint work instructions</p></a>'
        )
    return f"""{INDEX_START}
<div class="board"><h2>Exploded mechanical connections</h2>
<p class="sub">Project-wide build-level atlas: every neighbour joint, BOM hardware, interface confidence, retention, dependency, tool and ASM closure. These sheets add connection execution detail; they do not revise the fit pages above.</p>
<div class="gategrid"><a class="gate rank-watch" href="connections/index.html"><span class="tag">MASTER</span> <b>Mechanical connection atlas</b><p>{len(JOINTS)} joints · {len(ASSEMBLIES)} assemblies · sortable register + manual sequence</p></a>{''.join(cards)}</div></div>
{INDEX_END}
"""


def validate_source_data() -> None:
    ids = [j.joint_id for j in JOINTS]
    if len(ids) != len(set(ids)):
        dupes = sorted({value for value in ids if ids.count(value) > 1})
        raise RuntimeError(f"duplicate Joint IDs: {dupes}")
    if set(j.assembly for j in JOINTS) != set(ASSEMBLIES):
        raise RuntimeError("assembly coverage mismatch")
    for j in JOINTS:
        if j.part_a not in PART_KEY_BY_NAME or j.part_b not in PART_KEY_BY_NAME:
            raise RuntimeError(f"missing part key: {j.joint_id}")
        if j.confidence not in {"VERIFIED", "DOCUMENTED", "ASSUMPTION"}:
            raise RuntimeError(f"bad confidence: {j.joint_id}")
        if j.disposition not in {"READY", "HOLD", "DEFER"}:
            raise RuntimeError(f"bad disposition: {j.joint_id}")
    for key, part in PARTS.items():
        if part.mesh and not (REPO / part.mesh).is_file():
            raise RuntimeError(f"missing mesh for {key}: {part.mesh}")


def main() -> None:
    validate_source_data()
    OUT.mkdir(parents=True, exist_ok=True)
    REGISTER_CSV.write_text(csv_text(), encoding="utf-8")
    REGISTER_MD.write_text(register_markdown(), encoding="utf-8")
    replace_generated(MANUAL, MANUAL_START, MANUAL_END, manual_block())
    for key, (_, _, filename) in ASSEMBLIES.items():
        rows = sorted((j for j in JOINTS if j.assembly == key), key=lambda j: (j.order, j.joint_id))
        (OUT / filename).write_text(assembly_page(key, rows), encoding="utf-8")
    (OUT / "index.html").write_text(connection_index(), encoding="utf-8")
    replace_generated(
        MASTER_INDEX, INDEX_START, INDEX_END, master_index_block(),
        anchor='<div class="board"><h2>Evidence chain</h2>',
    )
    print(f"WROTE {len(JOINTS)} rows to {REGISTER_MD.name} + {REGISTER_CSV.name}")
    print(f"UPDATED generated joint sequence in {MANUAL.name}")
    print(f"WROTE {len(ASSEMBLIES)+1} self-contained connection HTML files to {OUT}")
    print(f"EMBEDDED {len(MESH_CACHE)} distinct read-only STL silhouettes")
    print(f"UPDATED connection links in {MASTER_INDEX}")


if __name__ == "__main__":
    main()
