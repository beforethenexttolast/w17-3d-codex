#!/usr/bin/env python3
"""p0_07_zone_fit_rollup.py — remaining-component fit-study evidence.

Read-only inputs:
* SHA-256-manifested STLs in 02_ready_to_slice/
* selected gated raw STLs in unsorted_stl_raw/ (bbox inspection only)
* the P0 shell-section CSV produced by p0_03

Outputs:
* evidence/p0/tables/p0_d28_zone_component_envelopes.md
* evidence/p0/tables/p0_d29_zone_placements.csv
* evidence/p0/tables/p0_d30_mass_balance.md
* evidence/p0/tables/p0_d31_fit_gates.md

No STL is written or changed.  Hardware values that are not represented by a mesh
remain DOCUMENTED or ASSUMPTION; this script never promotes them to VERIFIED.
Run from the repository root:

    python3 10_assembly_architecture/evidence/scripts/p0_07_zone_fit_rollup.py
"""
from __future__ import annotations

import csv
import itertools
import math
import os
from pathlib import Path

import stlkit as K


REPO = Path(__file__).resolve().parents[3]
TABLES = REPO / "10_assembly_architecture/evidence/p0/tables"
FRONT_AXLE_X = 146.1
REAR_AXLE_X = -90.9
WHEELBASE = FRONT_AXLE_X - REAR_AXLE_X

ZONE_META = {
    "rear": {
        "title": "Rear drivetrain & thermal",
        "study": "ZR_rear_drivetrain_fit_study.md",
        "html": "rear_drivetrain.html",
        "summary": "ESC, motor, belt/gear train, output shaft, rear bearings and 68 mm shock.",
    },
    "power": {
        "title": "Power, twin-pack feasibility & balance",
        "study": "ZP_power_balance_fit_study.md",
        "html": "power_balance.html",
        "summary": "Two BOM packs, dual UBEC rails, capacitors, divider, connectors and buzzer.",
    },
    "control": {
        "title": "Control & RF",
        "study": "ZC_control_rf_fit_study.md",
        "html": "control_rf.html",
        "summary": "Two installed ESP32 boards, RP1, Wi-Fi module, heatsink and three RF systems.",
    },
    "camera": {
        "title": "Camera, pod/nose & cooling",
        "study": "ZV_camera_nose_fit_study.md",
        "html": "camera_nose.html",
        "summary": "SSC338Q camera identity, candidate prints, 20 mm blower and duct.",
    },
    "servos": {
        "title": "Accessory servos & DRS",
        "study": "ZA_accessory_servo_fit_study.md",
        "html": "accessory_servos.html",
        "summary": "MG90S pan, tilt and DRS installations and their moving envelopes.",
    },
    "audio": {
        "title": "Audio & lighting",
        "study": "ZL_audio_light_fit_study.md",
        "html": "audio_light.html",
        "summary": "MAX98357A, speaker, WS2812 segments, lenses and diffuser.",
    },
    "suspension": {
        "title": "Suspension & rolling",
        "study": "ZS_suspension_rolling_fit_study.md",
        "html": "suspension_rolling.html",
        "summary": "Original oil-shock front, uprights, king pins, F104 wheels, tyres and travel.",
    },
    "sensors": {
        "title": "Rear speed sensor",
        "study": "ZH_speed_sensor_fit_study.md",
        "html": "speed_sensor.html",
        "summary": "A3144 pickup, 3 × 1 mm magnet, gap and protected lead route.",
    },
}


# Raw bbox expectations are intentionally independent of inventory.csv parsing.  A
# mismatch means either a source file changed or a path now names a different mesh.
STL_SOURCES = {
    "DRV-LOCK": ("02_ready_to_slice/02_ASA_rear_drivetrain/beltdrivemotorlock.stl",
                 (32.0, 3.5, 32.0)),
    "DRV-AXLE-PRINT": ("02_ready_to_slice/02_ASA_rear_drivetrain/Axle Main no grubs.stl",
                       (11.25, 115.0, 14.99)),
    "DRV-REAR-L": ("02_ready_to_slice/02_ASA_rear_drivetrain/Leftrearaxle.stl",
                   (81.5, 25.0, 10.0)),
    "DRV-REAR-R": ("02_ready_to_slice/02_ASA_rear_drivetrain/Rightrearaxle.stl",
                   (81.5, 35.0, 10.0)),
    "UPRIGHT-L": ("02_ready_to_slice/03_PETG_front_suspension_steering/"
                  "2023WheelHubsSuspension5.stl", (56.86, 20.0, 49.99)),
    "UPRIGHT-R": ("02_ready_to_slice/03_PETG_front_suspension_steering/"
                  "2023WheelHubsSuspension5mir.stl", (56.86, 20.0, 49.99)),
    "STEER-BLOCK": ("02_ready_to_slice/03_PETG_front_suspension_steering/"
                    "Steering Block4.stl", (31.0, 17.0, 29.99)),
    "RIM-F": ("02_ready_to_slice/04_PETG_wheels/Front_Rim_F1_2022.stl",
              (44.0, 43.99, 30.0)),
    "RIM-R": ("02_ready_to_slice/04_PETG_wheels/Rear_Rim_F1_2022.stl",
              (47.01, 47.01, 35.55)),
    "HUB-F": ("02_ready_to_slice/04_PETG_wheels/Front_Right_Wheel_Hub_2022_F104.stl",
              (27.99, 63.96, 55.95)),
    "CAM-TOP": ("02_ready_to_slice/06_PLA_body_shell/camera top 1.1.stl",
                (16.75, 17.72, 6.92)),
    "HALO": ("02_ready_to_slice/06_PLA_body_shell/new halo 2.1.stl",
             (74.94, 38.75, 24.86)),
    "LGT-DIFF": ("02_ready_to_slice/07_translucent_diffuser/"
                 "rearbacklightdiffuser.stl", (9.5, 12.0, 14.5)),
    "DRS-WING": ("unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/"
                 "2021 Upgrades/2021Rearwing with DRS.stl", (105.1, 82.0, 60.0)),
    "DRS-ARM": ("unsorted_stl_raw/Ryans Creations Open RC F1 Car/Experimental Parts/"
                "DRS Arm for 2021 Rear Wing.stl", (58.0, 5.0, 10.0)),
    "CAM-NOSE": ("unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/"
                 "Decoration Parts/cameranose.stl", (5.8, 10.5, 9.8)),
    "CAM-2C": ("unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/"
               "Decoration Parts/camera 2 colour.stl", (26.3, 14.9, 12.6)),
    "CAM-F104": ("unsorted_stl_raw/Ryans Creations Open RC F1 Car/Car Body/"
                 "Decoration Parts/f104camera.stl", (26.3, 15.0, 10.8)),
}


def _fmt_dims(dims: tuple[float, float, float]) -> str:
    return " × ".join(f"{v:.2f}".rstrip("0").rstrip(".") for v in dims)


def measure_stls() -> dict[str, dict]:
    result = {}
    for component_id, (rel, expected) in STL_SOURCES.items():
        path = REPO / rel
        tris = K.load_stl(str(path))
        bb = K.bbox(tris)
        dims = tuple(bb[1][i] - bb[0][i] for i in range(3))
        error = max(abs(dims[i] - expected[i]) for i in range(3))
        if error > 0.12:
            raise AssertionError(
                f"{component_id}: bbox {_fmt_dims(dims)} != expected {_fmt_dims(expected)}"
            )
        result[component_id] = {
            "path": rel,
            "tris": len(tris),
            "bbox": bb,
            "dims": dims,
        }
    return result


def build_components(stls: dict[str, dict]) -> list[dict]:
    def mesh(cid: str, zone: str, name: str, qty: str, install: str,
             mass: str = "not weighed") -> dict:
        row = stls[cid]
        return {
            "id": cid, "zone": zone, "name": name, "qty": qty,
            "body": _fmt_dims(row["dims"]) + " mm raw bbox",
            "confidence": "VERIFIED",
            "install": install, "mass": mass,
            "source": f"`{row['path']}`; p0_07 live bbox ({row['tris']} triangles)",
        }

    spur_pd = 75 * 25.4 / 48
    spur_od = 77 * 25.4 / 48
    pinion_pd = 28 * 25.4 / 48
    pinion_od = 30 * 25.4 / 48
    centre = (75 + 28) * 25.4 / (2 * 48)

    rows = [
        {"id": "DRV-ESC", "zone": "rear", "name": "Hobbywing QuicRun 10BL120 Sensored G2",
         "qty": "1", "body": "43 × 36.8 × 32.3 mm; fan 25 × 25 × 10 mm",
         "confidence": "DOCUMENTED", "install": "body + ≥10 mm clear above fan + 12 AWG exits",
         "mass": "101.5 g incl. wires (DOCUMENTED)",
         "source": "Hobbywing official QuicRun 10BL120 Sensored G2 product page; exact on-hand label still a gate"},
        {"id": "DRV-MOT", "zone": "rear", "name": "Rocket 540 V3 17.5T sensored motor",
         "qty": "1", "body": "Ø36 × 54 mm can; Ø3.175 × 14.5 mm shaft",
         "confidence": "DOCUMENTED", "install": "can + solder tabs/sensor lead + pinion + axial service pull",
         "mass": "145–165 g (ASSUMPTION until weighed)",
         "source": "BOM/Rocket 540 family listing; user-specified Ø≈36; verify the real can"},
        {"id": "DRV-BELT", "zone": "rear", "name": "belt-drive set",
         "qty": "1", "body": "140 mm belt length; pulley diameters TO MEASURE",
         "confidence": "DOCUMENTED", "install": "two pulley discs + two moving tangent runs + guard clearance",
         "mass": "30–60 g (ASSUMPTION)", "source": "BOM v2 §8 and on-hand inventory"},
        {"id": "DRV-SHAFT", "zone": "rear", "name": "belt-set metal rear output shaft",
         "qty": "1", "body": "diameter/shoulders/usable span TO MEASURE",
         "confidence": "ASSUMPTION", "install": "bearing seats + spacers + wheel/gear retention",
         "mass": "20–45 g (ASSUMPTION)", "source": "BOM v2 §8; physical set required"},
        {"id": "DRV-SPUR", "zone": "rear", "name": "HPI/3Racing 48P 75T spur",
         "qty": "1", "body": f"pitch Ø{spur_pd:.2f}; theoretical outside Ø{spur_od:.2f} mm",
         "confidence": "DERIVED", "install": "gear disc + unknown hub/bolt pattern + ≥2 mm radial guard",
         "mass": "8–15 g (ASSUMPTION)", "source": "75T/48P BOM; standard diametral-pitch arithmetic"},
        {"id": "DRV-PINION", "zone": "rear", "name": "48P 28T pinion",
         "qty": "1", "body": f"pitch Ø{pinion_pd:.2f}; theoretical outside Ø{pinion_od:.2f} mm",
         "confidence": "DERIVED", "install": f"gear disc; theoretical centre distance {centre:.2f} mm",
         "mass": "5–10 g (ASSUMPTION)", "source": "28T/48P BOM; standard diametral-pitch arithmetic"},
        {"id": "BRG-REAR", "zone": "rear", "name": "6801 rear bearing",
         "qty": "2", "body": "12 ID × 21 OD × 5 mm",
         "confidence": "DOCUMENTED", "install": "two coaxial carrier seats; no printed preload",
         "mass": "≈11 g pair (ASSUMPTION)", "source": "BOM v2 §9 / Ryan Parts List"},
        {"id": "SHK-REAR", "zone": "rear", "name": "rear oil shock",
         "qty": "1", "body": "68 mm eye-to-eye; body Ø/stroke TO MEASURE",
         "confidence": "DOCUMENTED", "install": "full compressed↔extended swept cylinder",
         "mass": "15–30 g (ASSUMPTION)", "source": "BOM v2 §10 / Ryan Parts List"},
        mesh("DRV-LOCK", "rear", "belt-drive motor lock", "1",
             "32 mm disc/lock at motor interface; orientation and screw stack gate"),
        mesh("DRV-REAR-L", "rear", "original left rear bearing carrier", "1",
             "Gate A decides whether this or Rev-1 motor covers carry the 6801"),
        mesh("DRV-REAR-R", "rear", "original right rear bearing carrier", "1",
             "Gate A decides whether this or Rev-1 motor covers carry the 6801"),
        {"id": "PWR-BAT-1", "zone": "power", "name": "2S LiPo active pack",
         "qty": "1", "body": "≤75 × 45 × 25 mm",
         "confidence": "DOCUMENTED", "install": "95 × 50 × 30 mm allocation incl. XT60/strap",
         "mass": "80–120 g (ASSUMPTION)", "source": "BOM v2 §D / 2024-body limit"},
        {"id": "PWR-BAT-2", "zone": "power", "name": "2S LiPo swap pack",
         "qty": "1", "body": "≤75 × 45 × 25 mm",
         "confidence": "DOCUMENTED", "install": "OFF-CAR storage/charge envelope on selected architecture",
         "mass": "80–120 g off-car (ASSUMPTION)", "source": "BOM v2 §D; dual-onboard fit rejected provisionally"},
        {"id": "PWR-UBEC-A", "zone": "power", "name": "UBEC 5 A — Rail A clean",
         "qty": "1", "body": "TO MEASURE; 30 × 14 × 10 mm planning block",
         "confidence": "ASSUMPTION", "install": "body + both lead exits + ≥5 mm convection",
         "mass": "10–20 g (ASSUMPTION)", "source": "B register planning block; on-hand part not measured"},
        {"id": "PWR-UBEC-B", "zone": "power", "name": "UBEC 5 A — Rail B servos",
         "qty": "1", "body": "TO MEASURE; 30 × 14 × 10 mm planning block",
         "confidence": "ASSUMPTION", "install": "body + both lead exits + ≥5 mm convection",
         "mass": "10–20 g (ASSUMPTION)", "source": "B register planning block; on-hand part not measured"},
        {"id": "PWR-CAP-B", "zone": "power", "name": "servo-rail electrolytic",
         "qty": "1", "body": "1000 µF / 16 V; Ø10 × 20 mm planning body",
         "confidence": "ASSUMPTION", "install": "upright/sideways body + insulated leads and zip restraint",
         "mass": "2–5 g (ASSUMPTION)", "source": "BOM value; physical capacitor can size unknown"},
        {"id": "PWR-CAP-LED", "zone": "power", "name": "LED-input electrolytic",
         "qty": "1 if stock permits", "body": "1000 µF / 16 V; Ø10 × 20 mm planning body",
         "confidence": "ASSUMPTION", "install": "within 50 mm electrical lead length of strip input",
         "mass": "2–5 g (ASSUMPTION)", "source": "BOM recommends 1–2; physical capacitor unknown"},
        {"id": "SNS-DIV", "zone": "power", "name": "battery divider 27 kΩ / 10 kΩ",
         "qty": "1", "body": "two axial resistors; assembled body TO MEASURE",
         "confidence": "DOCUMENTED", "install": "heatshrunk branch, ADC tap, common-star ground",
         "mass": "<1 g (ASSUMPTION)", "source": "BOM v2 §D/key reminders"},
        {"id": "PWR-XT60", "zone": "power", "name": "XT60 main junction / loop",
         "qty": "as built", "body": "connector/lead geometry TO MEASURE",
         "confidence": "ASSUMPTION", "install": "finger access + wire bend + recessed live side",
         "mass": "10–25 g junction (ASSUMPTION)", "source": "BOM; local connector variant unknown"},
        {"id": "PWR-XT30", "zone": "power", "name": "XT30 accessory taps",
         "qty": "few", "body": "connector/lead geometry TO MEASURE",
         "confidence": "ASSUMPTION", "install": "tap row + caps/strain relief",
         "mass": "5–15 g set (ASSUMPTION)", "source": "BOM; local connector variant unknown"},
        {"id": "PWR-BUZZ", "zone": "power", "name": "BX100 low-voltage buzzer",
         "qty": "0–1", "body": "TO MEASURE; 30 × 12 × 8 mm planning block",
         "confidence": "ASSUMPTION", "install": "speaker apertures unobstructed + balance-lead access",
         "mass": "5–10 g (ASSUMPTION)", "source": "B register planning block"},
        {"id": "CTL-E1", "zone": "control", "name": "ESP32-WROOM-32 DevKit V1 — control",
         "qty": "1", "body": "TO MEASURE clone; 55 × 28 × 13 mm planning block",
         "confidence": "ASSUMPTION", "install": "55 × 44 × 23 mm incl. side headers and USB bend",
         "mass": "8–15 g (ASSUMPTION)", "source": "BOM identifies clone family, not a controlled PCB drawing"},
        {"id": "CTL-E2", "zone": "control", "name": "ESP32-WROOM-32 DevKit V1 — sound/light",
         "qty": "1", "body": "TO MEASURE clone; 55 × 28 × 13 mm planning block",
         "confidence": "ASSUMPTION", "install": "55 × 44 × 23 mm incl. side headers and USB bend",
         "mass": "8–15 g (ASSUMPTION)", "source": "BOM identifies clone family, not a controlled PCB drawing"},
        {"id": "CTL-E3", "zone": "control", "name": "ESP32-WROOM-32 spare",
         "qty": "1", "body": "same family as CTL-E1/E2",
         "confidence": "ASSUMPTION", "install": "OFF-CAR bench stock",
         "mass": "off-car", "source": "BOM explicitly assigns one of three as spare"},
        {"id": "RX-ELRS", "zone": "control", "name": "RadioMaster RP1 V2 ELRS receiver",
         "qty": "1", "body": "13 × 11 × 3 mm; 65 mm T antenna",
         "confidence": "DOCUMENTED", "install": "receiver pad + 65 mm antenna + service loop",
         "mass": "2.2 g incl. antenna (DOCUMENTED)", "source": "RadioMaster official RP1 V2 page"},
        {"id": "VID-WIFI", "zone": "control", "name": "BL-M8812EU2 USB Wi-Fi module",
         "qty": "1", "body": "TO MEASURE; allocated maximum 60 × 32 × 12 mm",
         "confidence": "ASSUMPTION", "install": "module + 28 × 28 × 3 heatsink + USB/U.FL exits + airflow",
         "mass": "15–35 g (ASSUMPTION)", "source": "H P9 allocation; on-hand module not measured"},
        {"id": "VID-HS", "zone": "control", "name": "Wi-Fi heatsink",
         "qty": "1", "body": "28 × 28 × 3 mm",
         "confidence": "DOCUMENTED", "install": "bond layer + module stack",
         "mass": "5–12 g (ASSUMPTION)", "source": "BOM v2 §1"},
        {"id": "VID-ANT", "zone": "control", "name": "5.8 GHz U.FL linear omni",
         "qty": "2", "body": "70 mm whip each",
         "confidence": "DOCUMENTED", "install": "two 70 mm routes + U.FL service loop; no sharp fold",
         "mass": "2–6 g pair (ASSUMPTION)", "source": "BOM v2 §1 / on-hand mapping"},
        {"id": "VID-CAM", "zone": "camera", "name": "OpenIPC SSC338Q camera assembly",
         "qty": "1", "body": "TO MEASURE: PCB, heatsink, lens and cable exits",
         "confidence": "ASSUMPTION", "install": "measured body + FOV cone + cooling + gimbal sweep",
         "mass": "20–45 g (ASSUMPTION)", "source": "Gate C; user says IMX415, repo says IMX335"},
        mesh("CAM-TOP", "camera", "`camera top 1.1`", "1 candidate",
             "tiny exterior pod cover; does not establish camera-board capacity"),
        mesh("CAM-NOSE", "camera", "`cameranose`", "1 candidate",
             "gated decorative/legacy candidate; no measured hardware interface"),
        mesh("CAM-2C", "camera", "`camera 2 colour`", "1 candidate",
             "gated legacy candidate; no measured hardware interface"),
        mesh("CAM-F104", "camera", "`f104camera`", "1 candidate",
             "gated legacy candidate; no measured hardware interface"),
        {"id": "COOL-BLOW", "zone": "camera", "name": "5 V 20 mm blower",
         "qty": "1", "body": "20 × 20 face; thickness/outlet TO MEASURE",
         "confidence": "DOCUMENTED", "install": "body + inlet hemisphere + outlet collar + lead",
         "mass": "3–8 g (ASSUMPTION)", "source": "BOM v2 §13; actual blower calipers pending"},
        {"id": "COOL-DUCT", "zone": "camera", "name": "camera blower duct",
         "qty": "1", "body": "placeholder defaults: 20 × 8 collar; 18 mm transition",
         "confidence": "ASSUMPTION", "install": "nine measured dimensions + 1.4 mm wall + 0.25 mm nominal slip",
         "mass": "2–8 g (ASSUMPTION)", "source": "`unsorted_stl_raw/camera_blower_duct.scad`; defaults explicitly non-production"},
        {"id": "SRV-PAN", "zone": "servos", "name": "MG90S pan servo",
         "qty": "1", "body": "22.8 × 12.2 × 28.5 mm",
         "confidence": "DOCUMENTED", "install": "body + ears + horn sweep + 250 mm lead",
         "mass": "13.4 g (DOCUMENTED)", "source": "TowerPro official MG90S page; clone must be measured"},
        {"id": "SRV-TILT", "zone": "servos", "name": "MG90S tilt servo",
         "qty": "1", "body": "22.8 × 12.2 × 28.5 mm",
         "confidence": "DOCUMENTED", "install": "body + ears + horn sweep + 250 mm lead",
         "mass": "13.4 g (DOCUMENTED)", "source": "TowerPro official MG90S page; clone must be measured"},
        {"id": "SRV-DRS", "zone": "servos", "name": "MG90S DRS servo",
         "qty": "1", "body": "22.8 × 12.2 × 28.5 mm",
         "confidence": "DOCUMENTED", "install": "body + ears + horn/rod swept volume",
         "mass": "13.4 g (DOCUMENTED)", "source": "TowerPro official MG90S page; clone must be measured"},
        mesh("DRS-WING", "servos", "preferred 2021 rear wing with DRS", "1 candidate",
             "full wing + servo pocket; mounting to chosen rear stack remains Gate A/B"),
        mesh("DRS-ARM", "servos", "2021 DRS arm", "1 candidate",
             "58 mm linkage arm swept through measured flap travel"),
        {"id": "AUD-AMP", "zone": "audio", "name": "MAX98357A breakout",
         "qty": "1", "body": "TO MEASURE; 19.4 × 17.8 × 3 mm reference board",
         "confidence": "ASSUMPTION", "install": "board + terminals/pins + wire bends",
         "mass": "1–5 g (ASSUMPTION)", "source": "Adafruit reference board only; BOM clone can differ"},
        {"id": "AUD-SPK", "zone": "audio", "name": "4 Ω 3 W speaker",
         "qty": "1", "body": "TO MEASURE; Ø28–40 × 6–12 mm planning range",
         "confidence": "ASSUMPTION", "install": "basket + cone excursion + baffle/port + two wires",
         "mass": "20–40 g (ASSUMPTION)", "source": "B register planning range; actual speaker unmeasured"},
        {"id": "LGT-LED", "zone": "audio", "name": "WS2812B 30 LED/m strip",
         "qty": "1 m stock", "body": "10 mm wide; 33.33 mm pixel pitch",
         "confidence": "DOCUMENTED", "install": "cut segments + 3-wire tails + 330 Ω data resistor",
         "mass": "5–20 g installed segments (ASSUMPTION)", "source": "BOM v2 §4 (30 LED / 1 m)"},
        mesh("LGT-DIFF", "audio", "`rearbacklightdiffuser`", "1",
             "one-pixel translucent lens; keep paint out of optical faces"),
        mesh("HALO", "audio", "`new halo 2.1`", "1",
             "halo structure; LED carrier/adhesive path remains physical"),
        {"id": "SHK-FRONT", "zone": "suspension", "name": "front oil shock",
         "qty": "2", "body": "51 mm requirement / 52 mm stock label; exact eye-to-eye, stroke and body Ø TO MEASURE",
         "confidence": "DOCUMENTED conflict / ASSUMPTION physical", "install": "full bump↔droop swept cylinder each side",
         "mass": "20–40 g pair (ASSUMPTION)", "source": "user requirement; HARDWARE_INVENTORY §10 explicitly flags 51-vs-52 residual"},
        mesh("UPRIGHT-L", "suspension", "original oil-shock upright left", "1",
             "assembled orientation/king-pin/wheel-axis envelope, not raw bbox"),
        mesh("UPRIGHT-R", "suspension", "original oil-shock upright right", "1",
             "assembled orientation/king-pin/wheel-axis envelope, not raw bbox"),
        mesh("STEER-BLOCK", "suspension", "`Steering Block4` knuckle", "2",
             "M3 king-pin bore and two MR128 bearing seats require physical coupons"),
        {"id": "KINGPIN", "zone": "suspension", "name": "M3 × 30 king pin",
         "qty": "2", "body": "Ø3 × 30 mm",
         "confidence": "DOCUMENTED", "install": "pin + circlip access + free pivot",
         "mass": "≈3 g pair (ASSUMPTION)", "source": "BOM v2 §11 / on-hand inventory"},
        mesh("RIM-F", "suspension", "printed F104 front rim", "2",
             "Ø44 bead family ×30 wide; tyre/bearing coupon gates production"),
        mesh("RIM-R", "suspension", "printed F104 rear rim", "2",
             "Ø47 bead family ×35.55 wide; tyre/adapter coupon gates production"),
        mesh("HUB-F", "suspension", "front-right F104 hub source", "1 + mirrored 1",
             "raw multi-axis bbox; installed bearing seats and mirrored left gate"),
        {"id": "TYRE-F", "zone": "suspension", "name": "Tamiya 54198 front tyre",
         "qty": "2", "body": "Ø64 × 30 mm",
         "confidence": "DOCUMENTED", "install": "steer + bump moving envelope",
         "mass": "40–70 g pair (ASSUMPTION)", "source": "Tamiya F104 official chassis specification / BOM"},
        {"id": "TYRE-R", "zone": "suspension", "name": "Tamiya 51400 rear tyre",
         "qty": "2", "body": "Ø64 × 35 mm",
         "confidence": "DOCUMENTED", "install": "bump/axle moving envelope",
         "mass": "50–90 g pair (ASSUMPTION)", "source": "Tamiya F104 official chassis specification / BOM"},
        {"id": "BRG-FRONT", "zone": "suspension", "name": "MR128ZZ front bearing",
         "qty": "4", "body": "8 ID × 12 OD × 3.5 mm",
         "confidence": "DOCUMENTED", "install": "two coaxial seats per front hub",
         "mass": "≈10 g set (ASSUMPTION)", "source": "BOM v2 §9 / Ryan Parts List"},
        {"id": "SNS-HALL", "zone": "sensors", "name": "A3144 Hall switch",
         "qty": "1", "body": "4.04–4.17 × 2.97–3.10 × 1.47–1.57 mm package body",
         "confidence": "DOCUMENTED", "install": "body + leads + 1–3 mm adjustable gap bracket",
         "mass": "<1 g", "source": "Allegro A3141–A3144 datasheet, UA package"},
        {"id": "SNS-MAG", "zone": "sensors", "name": "rear-axle magnet",
         "qty": "1", "body": "Ø3 × 1 mm",
         "confidence": "DOCUMENTED", "install": "recess/bond + retention witness mark",
         "mass": "<1 g", "source": "BOM v2 §7"},
    ]
    return rows


PLACEMENTS = [
    # Coordinate strings intentionally preserve mixed confidence by axis.
    {"id": "DRV-ESC", "zone": "rear", "x": "−60", "l": "−25", "z": "+3",
     "orientation": "fan up; 43 mm X; 36.8 mm L", "confidence": "ASSUMPTION",
     "note": "Current Z5R candidate FAILS S0=0 side-envelope check; freeze PS-02/CAD-03."},
    {"id": "DRV-MOT", "zone": "rear", "x": "−105", "l": "0", "z": "+27 axis",
     "orientation": "shaft lateral; can transverse", "confidence": "ASSUMPTION",
     "note": "Donor drivetrain fixes the family of location, not a datum-clean transform."},
    {"id": "DRV-BELT", "zone": "rear", "x": "−118…−82", "l": "belt side", "z": "+10…+45",
     "orientation": "two pulley planes and moving tangent runs", "confidence": "ASSUMPTION",
     "note": "Pulley teeth/diameters/plane offsets require the physical set."},
    {"id": "DRV-SHAFT", "zone": "rear", "x": "−90.9", "l": "transverse", "z": "+26…+27 axis",
     "orientation": "coaxial with rear wheels", "confidence": "X DERIVED; L/Z ASSUMPTION",
     "note": "Rear shell arch establishes X; ride height establishes Z."},
    {"id": "DRV-SPUR", "zone": "rear", "x": "−90.9", "l": "belt-side offset TBD", "z": "+26…+27 axis",
     "orientation": "vertical gear plane", "confidence": "X DERIVED; L/Z ASSUMPTION",
     "note": "Bolt pattern and lateral stack are physical gates."},
    {"id": "DRV-PINION", "zone": "rear", "x": "motor axis ±27.25", "l": "motor shaft", "z": "TBD",
     "orientation": "parallel gear plane to spur", "confidence": "DERIVED centre distance; placement ASSUMPTION",
     "note": "27.25 mm is 48P pitch-centre arithmetic, not a mounted measurement."},
    {"id": "BRG-REAR", "zone": "rear", "x": "−90.9", "l": "carrier centres TBD", "z": "+26…+27",
     "orientation": "axes lateral", "confidence": "X DERIVED; L/Z ASSUMPTION",
     "note": "Gate A decides original carriers versus motor covers."},
    {"id": "SHK-REAR", "zone": "rear", "x": "−60…−25", "l": "0", "z": "+10…+45",
     "orientation": "longitudinal/central, exact eyes TBD", "confidence": "ASSUMPTION",
     "note": "Full articulation owns the envelope; 68 mm is only free eye distance."},
    {"id": "PWR-BAT-1", "zone": "power", "x": "−44", "l": "+25", "z": "+3",
     "orientation": "75 X ×45 L ×25 Z, XT60 forward", "confidence": "ASSUMPTION",
     "note": "Candidate crosses provisional steering corridor and shell shoulder; fit gate open."},
    {"id": "PWR-BAT-2", "zone": "power", "x": "OFF-CAR", "l": "OFF-CAR", "z": "OFF-CAR",
     "orientation": "charged swap/storage pack", "confidence": "DERIVED architecture decision",
     "note": "Two onboard packs do not fit the selected architecture without relocating electronics."},
    {"id": "PWR-UBEC-A", "zone": "power", "x": "−15", "l": "−38", "z": "+3",
     "orientation": "flat, leads fore/aft", "confidence": "ASSUMPTION",
     "note": "Rail A route stays forward/upper and away from motor phase wires."},
    {"id": "PWR-UBEC-B", "zone": "power", "x": "−48", "l": "−38", "z": "+3",
     "orientation": "flat, leads fore/aft", "confidence": "ASSUMPTION",
     "note": "Rail B remains low/right; capacitor adjacent."},
    {"id": "PWR-CAP-B", "zone": "power", "x": "−48", "l": "−48", "z": "+3",
     "orientation": "sideways/upright after real can measure", "confidence": "ASSUMPTION",
     "note": "Shortest practical Rail-B leads."},
    {"id": "PWR-CAP-LED", "zone": "power", "x": "+20", "l": "−40", "z": "+3",
     "orientation": "at lighting harness origin", "confidence": "ASSUMPTION",
     "note": "Final position follows first strip segment and stock count."},
    {"id": "SNS-DIV", "zone": "power", "x": "−5", "l": "−35", "z": "+3",
     "orientation": "heatshrunk inline branch", "confidence": "ASSUMPTION",
     "note": "Battery sense branch; ground returns to star."},
    {"id": "PWR-XT60", "zone": "power", "x": "+20", "l": "−40", "z": "+3",
     "orientation": "contacts recessed; disconnect upward", "confidence": "ASSUMPTION",
     "note": "Body-on reach remains a gate."},
    {"id": "PWR-XT30", "zone": "power", "x": "+10", "l": "−42", "z": "+3",
     "orientation": "tap row upward", "confidence": "ASSUMPTION",
     "note": "No final seat before connector calipers."},
    {"id": "PWR-BUZZ", "zone": "power", "x": "+25", "l": "−50", "z": "+3",
     "orientation": "apertures unobstructed", "confidence": "ASSUMPTION",
     "note": "Optional; no priority over main disconnect access."},
    {"id": "CTL-E1", "zone": "control", "x": "+10", "l": "−32", "z": "+20 deck",
     "orientation": "flat, USB outboard", "confidence": "ASSUMPTION",
     "note": "Conditional on S0 and physical steering sweep."},
    {"id": "CTL-E2", "zone": "control", "x": "−45", "l": "−32", "z": "+20 deck",
     "orientation": "flat, USB outboard", "confidence": "ASSUMPTION",
     "note": "Conditional on S0; outer header field is the shell limiter."},
    {"id": "CTL-E3", "zone": "control", "x": "OFF-CAR", "l": "OFF-CAR", "z": "OFF-CAR",
     "orientation": "bench spare", "confidence": "DOCUMENTED",
     "note": "BOM explicitly assigns the third board as spare."},
    {"id": "RX-ELRS", "zone": "control", "x": "+20 receiver / +120 antenna", "l": "+38 / +15", "z": "+3 / +30",
     "orientation": "receiver flat; T antenna transverse/clear", "confidence": "ASSUMPTION",
     "note": "Forward antenna route targets separation from video antennas."},
    {"id": "VID-WIFI", "zone": "control", "x": "−45", "l": "−18", "z": "+20 deck",
     "orientation": "flat, heatsink up, U.FL aft", "confidence": "ASSUMPTION",
     "note": "P9 hard cap only; real module and shell fit are open."},
    {"id": "VID-ANT", "zone": "control", "x": "−45 roots", "l": "±18", "z": "+35",
     "orientation": "70 mm longitudinal routes; shallow opposing V", "confidence": "ASSUMPTION",
     "note": "Chassis-mounted; ≥150 mm design target from 2.4 GHz antenna, validate D-20."},
    {"id": "VID-CAM", "zone": "camera", "x": "+60 Option A / −53 Option B", "l": "0", "z": "+20 / +73+S0",
     "orientation": "boresight X+; adjustable roll", "confidence": "ASSUMPTION",
     "note": "Option A preferred for CG/POV; identity and calipers still block geometry."},
    {"id": "CAM-TOP", "zone": "camera", "x": "−61.6…−44.8", "l": "−8.8…+8.9", "z": "+73.35…+80.27 + S0",
     "orientation": "same authored shell frame", "confidence": "DERIVED",
     "note": "Transform X=146.6−raw_x, L=−(raw_y−1.855), Z=raw_z+S0."},
    {"id": "COOL-BLOW", "zone": "camera", "x": "camera-module local", "l": "offset from lens", "z": "TBD",
     "orientation": "inlet open; outlet to hot side", "confidence": "ASSUMPTION",
     "note": "No fixed coordinate before camera/placement decision."},
    {"id": "COOL-DUCT", "zone": "camera", "x": "camera-module local", "l": "local", "z": "local",
     "orientation": "blower outlet → camera heatsink", "confidence": "ASSUMPTION",
     "note": "Nine SCAD inputs must be measured."},
    {"id": "SRV-PAN", "zone": "servos", "x": "+60 / −53", "l": "0", "z": "camera-module base",
     "orientation": "output axis Z", "confidence": "ASSUMPTION",
     "note": "Option A/B coordinate follows VID-CAM."},
    {"id": "SRV-TILT", "zone": "servos", "x": "+60 / −53", "l": "0", "z": "above pan",
     "orientation": "output axis L", "confidence": "ASSUMPTION",
     "note": "Reserve board, lens and horn sweep; no gimbal mesh exists."},
    {"id": "SRV-DRS", "zone": "servos", "x": "−125", "l": "0", "z": "+55…+80",
     "orientation": "per 2021 wing pocket", "confidence": "ASSUMPTION",
     "note": "Raw wing proves a pocket exists, not that the actual clone fits."},
    {"id": "DRS-ARM", "zone": "servos", "x": "rear-wing local", "l": "0", "z": "flap linkage",
     "orientation": "58 mm arm swept", "confidence": "ASSUMPTION",
     "note": "Gate A/B combined dry-fit fixes pivots and travel."},
    {"id": "AUD-AMP", "zone": "audio", "x": "−5", "l": "−40", "z": "+15 deck",
     "orientation": "flat; speaker terminals outboard", "confidence": "ASSUMPTION",
     "note": "Actual clone size and connector height pending."},
    {"id": "AUD-SPK", "zone": "audio", "x": "−30", "l": "+43", "z": "+3",
     "orientation": "flat, cone/port outboard", "confidence": "ASSUMPTION",
     "note": "S0=0 shell gives 6–9 mm policy margin for a 12 mm-tall speaker."},
    {"id": "LGT-DIFF", "zone": "audio", "x": "−125", "l": "0", "z": "+35",
     "orientation": "lens aft", "confidence": "ASSUMPTION",
     "note": "BBox verified; rear-stack transform is not."},
    {"id": "LGT-LED", "zone": "audio", "x": "tail / wing ends / halo", "l": "0 / ±40 / halo", "z": "TBD",
     "orientation": "1 centre + 2 per indicator + 2 halo planning segments", "confidence": "ASSUMPTION",
     "note": "Seven installed pixels proposed; remaining strip is spare until lens checks."},
    {"id": "SHK-FRONT", "zone": "suspension", "x": "+120…+150", "l": "±55…±75", "z": "+10…+45",
     "orientation": "eye axes per original oil-shock front", "confidence": "ASSUMPTION",
     "note": "51 mm requirement conflicts with 52 mm stock label; D-12/D-37 measures the real free/compressed length."},
    {"id": "UPRIGHT-L", "zone": "suspension", "x": "+146.1", "l": "+75", "z": "+26…+27 axle",
     "orientation": "original oil-shock assembly", "confidence": "X DERIVED; L/Z ASSUMPTION",
     "note": "Do not substitute Rev-1/1.1 steering parts."},
    {"id": "UPRIGHT-R", "zone": "suspension", "x": "+146.1", "l": "−75", "z": "+26…+27 axle",
     "orientation": "original oil-shock assembly", "confidence": "X DERIVED; L/Z ASSUMPTION",
     "note": "Do not substitute Rev-1/1.1 steering parts."},
    {"id": "TYRE-F", "zone": "suspension", "x": "+146.1", "l": "±75", "z": "+26…+27",
     "orientation": "wheel axes lateral", "confidence": "X DERIVED; L/Z ASSUMPTION",
     "note": "At ±25° assumed steer, plan half-envelope is 35.3 X ×27.1 L mm."},
    {"id": "TYRE-R", "zone": "suspension", "x": "−90.9", "l": "±72.5", "z": "+26…+27",
     "orientation": "wheel axes lateral", "confidence": "X DERIVED; L/Z ASSUMPTION",
     "note": "No steering; vertical bump remains unmeasured."},
    {"id": "SNS-HALL", "zone": "sensors", "x": "−90.9", "l": "belt-side collar TBD", "z": "+26…+27",
     "orientation": "sensitive face toward magnet", "confidence": "X DERIVED; L/Z ASSUMPTION",
     "note": "Bracket requires 0.5 mm adjustment steps and a service loop."},
    {"id": "SNS-MAG", "zone": "sensors", "x": "−90.9", "l": "shaft collar TBD", "z": "+26…+27",
     "orientation": "radial face; one pulse/rev", "confidence": "X DERIVED; L/Z ASSUMPTION",
     "note": "Target 1.5 mm cold gap, validate reliable range 1–3 mm."},
]


SHELL_CHECKS = [
    ("DRV-ESC", "X−60, L≈−25", "body top Z35.3; airflow plane Z45.3",
     "S0=0 width near Z35 is 48 mm only about centre; width at Z45 is 17 mm",
     "FAIL at side placement; S0 + exact fan footprint/label required", "DERIVED"),
    ("PWR-BAT-1", "X−20…−40, L shoulder", "pack body top Z28; strap stack ≈Z31",
     "ceil @L45 is 27→24 mm; provisional KO-01 is Z22…38, |L|≤22",
     "FAIL at S0=0 / moving corridor unresolved; S0 and dummy sweep required", "DERIVED"),
    ("CTL-E1/E2", "X−20, L20/L30", "planning top ≈Z33 on DAT-D20",
     "ceil 39 mm @L20, 26 mm @L30",
     "only narrow inboard edge is plausible; no production deck", "DERIVED"),
    ("AUD-SPK", "X−20…−40, L45", "planning top ≤Z15",
     "ceil 27→24 mm at S0=0",
     "raw 9–12 mm / policy 4–7 mm; candidate is plausible, physical port gate stays", "DERIVED"),
    ("TYRE-F", "front arch X+146.1", "Ø64 moving wheel", "about 3.5 mm arch margin",
     "below 8 mm moving policy; full steer+bump/body-on test mandatory", "DERIVED"),
    ("TYRE-R", "rear arch X−90.9", "Ø64 moving wheel", "about 4 mm arch margin",
     "below 8 mm moving policy; full bump/body-on test mandatory", "DERIVED"),
]


MASS_ITEMS = [
    # id, description, min g, max g, X, L, Z, confidence
    ("BASE-PRINT", "printed floor/body/aero/supports", 350.0, 520.0, 20.0, 0.0, 18.0, "ASSUMPTION"),
    ("BASE-HW", "fasteners, inserts, loom, glue", 100.0, 150.0, 0.0, 0.0, 10.0, "ASSUMPTION"),
    ("DRV-MOT", "motor", 145.0, 165.0, -100.0, 0.0, 27.0, "ASSUMPTION"),
    ("DRV-ESC", "ESC incl. wires", 101.5, 101.5, -70.0, -35.0, 20.0, "DOCUMENTED mass / ASSUMPTION position"),
    ("DRV-TRAIN", "belt/gears/shaft/rear bearings/spacers", 100.0, 150.0, -91.0, 0.0, 27.0, "ASSUMPTION"),
    ("FRONT-SUSP", "front printed suspension + shocks", 100.0, 160.0, 110.0, 0.0, 25.0, "ASSUMPTION"),
    ("FRONT-WHEELS", "two front wheel/tyre assemblies", 110.0, 160.0, 146.0, 0.0, 27.0, "ASSUMPTION"),
    ("REAR-WHEELS", "two rear wheel/tyre assemblies", 130.0, 190.0, -91.0, 0.0, 27.0, "ASSUMPTION"),
    ("PWR-BAT-1", "one active pack", 80.0, 120.0, -44.0, 32.0, 15.5, "ASSUMPTION mass/position"),
    ("PWR", "UBECs, caps, junction, buzzer", 35.0, 70.0, -20.0, -35.0, 10.0, "ASSUMPTION"),
    ("CONTROL", "two ESP32, RX, Wi-Fi, heatsink", 50.0, 95.0, -10.0, -35.0, 30.0, "ASSUMPTION"),
    ("CAM-GIMBAL", "camera, blower, two MG90S, mount", 55.0, 85.0, 60.0, 0.0, 45.0, "ASSUMPTION Option A"),
    ("SRV-DRS", "DRS MG90S", 13.4, 13.4, -125.0, 0.0, 65.0, "DOCUMENTED mass / ASSUMPTION position"),
    ("AUDIO-LIGHT", "speaker, amp, installed LED segments", 25.0, 55.0, -20.0, 43.0, 12.0, "ASSUMPTION"),
    ("SRV-STEER", "completed steering servo/horn", 60.0, 75.0, -55.0, 0.0, 15.0, "ASSUMPTION mass"),
]


FIT_GATES = [
    (1, "rear", "D-28 / ASM-49", "Read exact ESC label; caliper body/fan/wire exits; body-on dummy at X−60 and alternatives.",
     "Current ESC envelope and PS-02/CAD-03 are stale.", "all ESC support geometry"),
    (2, "power", "D-31 / ASM-50", "Pin S0; fit one 75×45×25 dummy with the real steering sweep; explicitly reject/approve dual-onboard.",
     "Pack 1 fails the S0=0 shoulder/rod model and pack 2 displaces the electronics bay.",
     "battery purchase/tray and any dual-pack wiring"),
    (3, "rear", "D-14/15/17", "Dry-assemble the selected rear stack, 68 mm shock, preferred wing and DRS parts through travel.",
     "Carrier identity, shock articulation and wing mounting are coupled.", "rear ASA and wing production"),
    (4, "rear", "D-16 / ASM-51", "Measure pulley teeth/OD/bores/planes, output shaft shoulders, spur bolt PCD and gear backlash.",
     "140 mm belt length and 48P gear arithmetic do not establish the mounted axes.", "drivetrain production/assembly"),
    (5, "suspension", "D-37 / ASM-56", "Measure front shock free/compressed length and body-on steer+bump; set ride height on scales.",
     "Front/rear arch margins are only 3.5/4 mm and shock stroke is unknown.", "full suspension and body sign-off"),
    (6, "camera", "D-34 / ASM-53", "Resolve IMX415-vs-IMX335 identity; caliper camera/blower; choose A/B; prove airflow/FOV/service.",
     "No camera body dimension exists and the visible nose has no protected cavity.", "PS-10/11 and camera prints"),
    (7, "servos", "D-35 / ASM-54", "Caliper all three MG90S clones; no-power pocket/horn sweep; later record powered endpoints under project safety gate.",
     "Official TowerPro dimensions do not prove the purchased clones or pockets.", "gimbal/DRS production"),
    (8, "control", "D-32/33 / ASM-52", "Caliper boards/module/heatsink and trial the complete RF/coax routes with shell seated.",
     "ESP32 and Wi-Fi envelopes are planning blocks; antenna clearances are inferred.", "deck/RX/antenna supports"),
    (9, "audio", "D-36 / ASM-55", "Measure speaker/amp; prove port and seven-pixel proposed segment/lens layout.",
     "Actual boards and speaker are unmeasured; only one-pixel diffuser is verified.", "speaker and LED supports"),
    (10, "sensors", "D-38 / ASM-57", "Set 1.5 mm cold gap; spin by hand through axle play; verify 1–3 mm reliable range.",
     "Magnetic field, collar runout and hot rear geometry are unknown.", "PS-16 Hall bracket"),
    (11, "power", "D-24 / ASM-36", "Measure rail currents, hold-up and common-star continuity before final harness.",
     "Both nominal 5 A rails have plausible overload cases.", "final harness/fuse/cap decisions"),
    (12, "power", "D-39 / ASM-58", "Weigh every module and all four corners with body on; compute X/L CG and axle percentages.",
     "Planning mass range is too wide for a production balance decision.", "ballast and final battery station"),
]


def _write_envelopes(components: list[dict], stls: dict[str, dict]) -> None:
    spur_pd = 75 * 25.4 / 48
    pinion_pd = 28 * 25.4 / 48
    centre = (75 + 28) * 25.4 / (2 * 48)
    path = TABLES / "p0_d28_zone_component_envelopes.md"
    lines = [
        "# p0_07 / D-28…D-38 — remaining-component envelope roll-up",
        "",
        "Datum: component-local dimensions unless a vehicle coordinate is stated. "
        "Confidence vocabulary is exactly **VERIFIED / DERIVED / DOCUMENTED / ASSUMPTION**.",
        "",
        f"48P arithmetic: 75T pitch Ø **{spur_pd:.2f} mm**, 28T pitch Ø "
        f"**{pinion_pd:.2f} mm**, pitch-centre distance **{centre:.2f} mm** "
        "(DERIVED; hub/bolt/backlash excluded).",
        "",
        "| ID | Zone | Component | Qty | Body envelope | Confidence | Installation envelope | Mass | Evidence |",
        "|---|---|---|---:|---|---|---|---|---|",
    ]
    for c in components:
        lines.append(
            f"| {c['id']} | {c['zone']} | {c['name']} | {c['qty']} | {c['body']} | "
            f"**{c['confidence']}** | {c['install']} | {c['mass']} | {c['source']} |"
        )
    lines += [
        "",
        "## Lower-bound shell / moving-envelope checks",
        "",
        "Shell values use **DAT-F Z=0 and S0=0**. Add the physically measured S0 to "
        "the ceiling; the 5 mm static / 8 mm moving policies are not waived.",
        "",
        "| ID | Datum station | Occupant | Evidence profile | Result | Confidence |",
        "|---|---|---|---|---|---|",
    ]
    for row in SHELL_CHECKS:
        lines.append("| " + " | ".join(row) + " |")
    lines += [
        "",
        "## Reproducibility",
        "",
        f"- {len(stls)} STL bboxes loaded directly; every bbox matched its independent "
        "expected value within 0.12 mm.",
        "- Raw/historical STLs were read only. No mesh was transformed, repaired or written.",
        "- Hardware without a controlled drawing remains ASSUMPTION even when a planning "
        "block exists elsewhere in the repo.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_placements() -> None:
    path = TABLES / "p0_d29_zone_placements.csv"
    fields = ["id", "zone", "x", "l", "z", "orientation", "confidence", "note"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(PLACEMENTS)


def _state(masses: list[float], items=MASS_ITEMS) -> tuple[float, float, float, float, float]:
    total = sum(masses)
    x = sum(m * item[4] for m, item in zip(masses, items)) / total
    lateral = sum(m * item[5] for m, item in zip(masses, items)) / total
    z = sum(m * item[6] for m, item in zip(masses, items)) / total
    front_pct = 100.0 * (x - REAR_AXLE_X) / WHEELBASE
    return total, x, lateral, z, front_pct


def mass_summary() -> dict:
    lows = [item[2] for item in MASS_ITEMS]
    highs = [item[3] for item in MASS_ITEMS]
    mids = [(lo + hi) / 2 for lo, hi in zip(lows, highs)]
    midpoint = _state(mids)
    states = []
    for bits in itertools.product((0, 1), repeat=len(MASS_ITEMS)):
        masses = [MASS_ITEMS[i][2 + bit] for i, bit in enumerate(bits)]
        states.append(_state(masses))
    front_min = min(states, key=lambda s: s[4])
    front_max = max(states, key=lambda s: s[4])
    l_min = min(s[2] for s in states)
    l_max = max(s[2] for s in states)

    # High-pod sensitivity: replace Option A's X=+60/Z=45 group point with
    # camera-top X≈−53.2 and an assumed group CG at Z=70 (S0=0).  The cover
    # itself spans Z73.35..80.27+S0, but the servos/mount sit below it; D-39
    # must replace this deliberately coarse vertical coordinate.
    high_items = [list(i) for i in MASS_ITEMS]
    cam_i = next(i for i, item in enumerate(high_items) if item[0] == "CAM-GIMBAL")
    high_items[cam_i][4] = -53.2
    high_items[cam_i][6] = 70.0
    high_tuple = [tuple(i) for i in high_items]
    high = _state(mids, high_tuple)

    # Mechanically rejected but useful sensitivity: a nominal second 100 g pack
    # in the right mirror bay, without pretending the displaced electronics vanish.
    dual_mass = midpoint[0] + 100.0
    dual_x = (midpoint[0] * midpoint[1] + 100.0 * -44.0) / dual_mass
    dual_l = (midpoint[0] * midpoint[2] + 100.0 * -32.0) / dual_mass
    dual_z = (midpoint[0] * midpoint[3] + 100.0 * 15.5) / dual_mass
    dual_front = 100.0 * (dual_x - REAR_AXLE_X) / WHEELBASE
    dual = (dual_mass, dual_x, dual_l, dual_z, dual_front)
    return {
        "low_total": sum(lows), "high_total": sum(highs), "mid": midpoint,
        "front_min": front_min, "front_max": front_max,
        "l_min": l_min, "l_max": l_max, "high_pod": high, "dual": dual,
    }


def _write_mass() -> None:
    summary = mass_summary()
    path = TABLES / "p0_d30_mass_balance.md"
    lines = [
        "# p0_07 / D-39 — whole-car planning mass and balance",
        "",
        f"Vehicle datum: DAT-F; X+ forward; front axle X={FRONT_AXLE_X:.1f}; "
        f"rear axle X={REAR_AXLE_X:.1f}; wheelbase={WHEELBASE:.1f} mm (DERIVED from P0 shell arches).",
        "",
        "Tuning target (not a donor specification): **36–40% front / 60–64% rear**, "
        "**|L-CG|≤2 mm**, and cross-weight within 3% (**ASSUMPTION**). Physical scales own the result.",
        "",
        "| Group | Mass range g | X | L | Z | Confidence |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for item in MASS_ITEMS:
        lines.append(
            f"| {item[0]} — {item[1]} | {item[2]:.1f}–{item[3]:.1f} | "
            f"{item[4]:+.1f} | {item[5]:+.1f} | {item[6]:.1f} | {item[7]} |"
        )
    mid = summary["mid"]
    high = summary["high_pod"]
    dual = summary["dual"]
    lines += [
        "",
        "## Calculated scenarios",
        "",
        "| Scenario | Mass g | X-CG mm | L-CG mm | Z-CG mm | Front / rear | Verdict |",
        "|---|---:|---:|---:|---:|---:|---|",
        f"| One active pack; cockpit camera (midpoint ledger) | {mid[0]:.0f} | "
        f"{mid[1]:+.1f} | {mid[2]:+.1f} | {mid[3]:.1f} | {mid[4]:.1f}% / "
        f"{100-mid[4]:.1f}% | L/R near target; front is ~1 point below target |",
        f"| One active pack; high airbox pod | {high[0]:.0f} | {high[1]:+.1f} | "
        f"{high[2]:+.1f} | {high[3]:.1f} | {high[4]:.1f}% / {100-high[4]:.1f}% | "
        "worse fore/aft; assumed Z=70 group raises vertical CG; still physically gated |",
        f"| Hypothetical second 100 g pack in right mirror bay | {dual[0]:.0f} | "
        f"{dual[1]:+.1f} | {dual[2]:+.1f} | {dual[3]:.1f} | {dual[4]:.1f}% / "
        f"{100-dual[4]:.1f}% | mechanically rejected; worsens modelled front and right bias |",
        "",
        f"Total planning range: **{summary['low_total']:.0f}–{summary['high_total']:.0f} g**. "
        f"Enumerating all min/max combinations gives a front-load range of "
        f"**{summary['front_min'][4]:.1f}–{summary['front_max'][4]:.1f}%** and L-CG "
        f"**{summary['l_min']:+.1f}…{summary['l_max']:+.1f} mm**. This uncertainty is "
        "too large to claim that the target is met.",
        "",
        "## Decision",
        "",
        "- The **left active pack is useful lateral ballast** against the right ESC/power/deck. "
        "The speaker-left option also improves the midpoint ledger.",
        "- The battery station alone cannot guarantee fore/aft target: ±10 mm pack motion "
        "moves whole-car X-CG by only about 0.6 mm at the midpoint mass.",
        "- Option-A cockpit camera is preferable to the high airbox pod by roughly "
        f"{mid[4]-high[4]:.1f} percentage points of front load and "
        f"{high[3]-mid[3]:.1f} mm whole-car Z-CG in this model.",
        "- Pack 2 remains an off-car swap. A two-onboard proposal is a new architecture and "
        "requires a fresh power/safety review; this mechanical study does not authorize parallel packs.",
        "- Close D-39/ASM-58 with four corner scales before ballast or production tray position.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_gates() -> None:
    path = TABLES / "p0_d31_fit_gates.md"
    lines = [
        "# p0_07 — prioritized remaining-component fit gates",
        "",
        "Every row is a stop condition for the named production geometry. "
        "Diagnostic gauges are allowed only where T/K explicitly say so.",
        "",
        "| Rank | Zone | Gate | Physical closure | Why open | Blocks |",
        "|---:|---|---|---|---|---|",
    ]
    for rank, zone, gate, closure, why, blocks in FIT_GATES:
        lines.append(f"| {rank} | {zone} | {gate} | {closure} | {why} | {blocks} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    os.makedirs(TABLES, exist_ok=True)
    stls = measure_stls()
    components = build_components(stls)
    _write_envelopes(components, stls)
    _write_placements()
    _write_mass()
    _write_gates()
    summary = mass_summary()
    print(f"STL bbox validation: PASS ({len(stls)} models)")
    print(f"Envelope rows: {len(components)}")
    print(f"Placement rows: {len(PLACEMENTS)}")
    print(f"Planning mass: {summary['low_total']:.0f}..{summary['high_total']:.0f} g")
    print("WROTE:")
    for name in (
        "p0_d28_zone_component_envelopes.md",
        "p0_d29_zone_placements.csv",
        "p0_d30_mass_balance.md",
        "p0_d31_fit_gates.md",
    ):
        print(" ", TABLES / name)


if __name__ == "__main__":
    main()
