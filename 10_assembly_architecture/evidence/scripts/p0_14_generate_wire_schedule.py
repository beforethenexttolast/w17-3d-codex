#!/usr/bin/env python3
"""Generate the W17 physical wire schedule (Markdown + CSV).

Electrical nets and GPIOs are transcribed from the supplied connector map and
the two firmware PinMap.hpp files.  This script adds only physical segmentation,
route estimates, gauges, terminations and dry-fit gates.  It emits no STL.
"""
from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from collections import Counter
import math


REPO = Path(__file__).resolve().parents[3]
ARCH = REPO / "10_assembly_architecture"
CSV_OUT = ARCH / "Z_wire_schedule.csv"
MD_OUT = ARCH / "Z_wire_schedule.md"

ELECTRICAL_SOURCE_SHA256 = "e7b96a8fdbaeeed47352c208777743f70e0b4f60b252527eff12d9fb43d6fd51"
CONTROL_PINMAP_SHA256 = "6afca81526092adfabb8dd65484867cef40a1c9d625d8997692437b18f8dbcd2"
SOUNDLIGHT_PINMAP_SHA256 = "71e0a93a63f1c899717454ebcbe55ae37e5bb6122d63f15d5b69b1ad90510f5d"

BUNDLES = ("on-PDB", "on-cassette", "pedestal-conduit", "umbilical")

# DAT-F coordinates/ranges.  These are module envelopes or routing datums, not
# claims of measured pad-centre locations.
XYZ = {
    "PDB": "X +1…+46, L −27.5…+27.5, Z +1…+19",
    "CHARGE": "X −31…−1, L −13…+12, Z +1…+11",
    "PACK": "X −80…−5, L +22.5…+67.5, Z +1.5…+26.5",
    "PORT": "UNPLACED hidden shell opening; X/L/Z TBD",
    "ESP1": "X +3…+42, L −43…−30, Z +1…+32",
    "ESP2": "X +3…+42, L +30…+43, Z +1…+32",
    "RP1": "X −12.2…+0.8, L −6…+5, Z +13…+16",
    "AMP": "X −31…−13.2, L −10.2…+9.2, Z +13…+16",
    "WIFI": "UNPLACED in cassette; X/L/Z TBD",
    "ANT_L": "root ≈X −45, L −18, Z +35; route conditional",
    "ANT_R": "root ≈X −45, L +18, Z +35; route conditional",
    "DOCK_PWR": "X +42…+58, L near −32, Z local TBD",
    "DOCK_SIG": "X +42…+58, L near +32, Z local TBD",
    "DOCK_PED": "X +42…+58, L near 0, Z local TBD",
    "STEER": "X −84…−16 station, L ≈0, Z 0…+22.9",
    "ESC": "X −49.2…−5, L −60.5…−23.5, Z +1.5…+25.7",
    "DRS": "X ≈−125, L ≈0, Z +55…+80",
    "LED": "tail input ≈X −125, L 0, Z +35",
    "HALL": "X −90.9, L collar TBD, Z +26…+27",
    "SPEAKER": "X ≈−30, L ≈+43, Z ≈+3",
    "PED": "pedestal X +51…+65, L −11…+11; gimbal Z datum TBD",
    "BLOWER": "camera-module local on pedestal; X/L/Z TBD",
}


@dataclass(frozen=True)
class Wire:
    wire_id: str
    bundle: str
    circuit: str
    signal: str
    rail: str
    endpoint_a: str
    endpoint_b: str
    connector_a: str
    termination_a: str
    connector_b: str
    termination_b: str
    from_xyz: str
    to_xyz: str
    route: str
    gauge: str
    routed_mm_est: int
    service_slack_mm: int
    strain_relief_mm: int
    cut_length_mm: int
    confidence: str
    disposition: str
    cut_to_fit_at_dry_fit: str
    color_label: str
    joint_ids: str
    electrical_basis: str
    ordering_class: str = "BASE"


WIRES: list[Wire] = []
COUNTERS: Counter[str] = Counter()


def add(
    bundle: str,
    circuit: str,
    signal: str,
    rail: str,
    endpoint_a: str,
    endpoint_b: str,
    connector_a: str,
    termination_a: str,
    connector_b: str,
    termination_b: str,
    from_xyz: str,
    to_xyz: str,
    route: str,
    gauge: str,
    routed: int,
    slack: int,
    relief: int,
    disposition: str,
    color_label: str,
    joint_ids: str,
    electrical_basis: str,
    *,
    confidence: str = "FIRM electrical / ASSUMPTION physical",
    cut_to_fit: str = "YES",
    ordering_class: str = "BASE",
) -> None:
    prefixes = {
        "on-PDB": "PDB",
        "on-cassette": "CAS",
        "pedestal-conduit": "PED",
        "umbilical": "UMB",
    }
    COUNTERS[bundle] += 1
    wire_id = f"W-{prefixes[bundle]}-{COUNTERS[bundle]:03d}"
    WIRES.append(
        Wire(
            wire_id=wire_id,
            bundle=bundle,
            circuit=circuit,
            signal=signal,
            rail=rail,
            endpoint_a=endpoint_a,
            endpoint_b=endpoint_b,
            connector_a=connector_a,
            termination_a=termination_a,
            connector_b=connector_b,
            termination_b=termination_b,
            from_xyz=from_xyz,
            to_xyz=to_xyz,
            route=route,
            gauge=gauge,
            routed_mm_est=routed,
            service_slack_mm=slack,
            strain_relief_mm=relief,
            cut_length_mm=routed + slack + relief,
            confidence=confidence,
            disposition=disposition,
            cut_to_fit_at_dry_fit=cut_to_fit,
            color_label=color_label,
            joint_ids=joint_ids,
            electrical_basis=electrical_basis,
            ordering_class=ordering_class,
        )
    )


def add_pair(
    bundle: str,
    circuit: str,
    rail: str,
    endpoint_a_prefix: str,
    endpoint_b_prefix: str,
    connector_a: str,
    termination_a: str,
    connector_b: str,
    termination_b: str,
    from_xyz: str,
    to_xyz: str,
    route: str,
    gauge: str,
    routed: int,
    slack: int,
    relief: int,
    disposition: str,
    joint_ids: str,
    electrical_basis: str,
    *,
    positive_signal: str = "+5 V",
    negative_signal: str = "GND",
    positive_suffix: str = "+5V",
    negative_suffix: str = "GND",
    positive_color: str | None = None,
    negative_color: str | None = None,
    negative_endpoint_a: str | None = None,
    negative_endpoint_b: str | None = None,
) -> None:
    band = "blue band" if rail == "A clean" else "yellow band" if rail == "B servos" else "battery label"
    add(
        bundle, circuit, positive_signal, rail,
        f"{endpoint_a_prefix}.{positive_suffix}", f"{endpoint_b_prefix}.{positive_suffix}",
        connector_a, termination_a, connector_b, termination_b,
        from_xyz, to_xyz, route, gauge, routed, slack, relief, disposition,
        positive_color or f"red · {band} · {circuit} +", joint_ids, electrical_basis,
    )
    add(
        bundle, circuit, negative_signal, rail,
        negative_endpoint_a or f"{endpoint_a_prefix}.{negative_suffix}",
        negative_endpoint_b or f"{endpoint_b_prefix}.{negative_suffix}",
        connector_a, termination_a, connector_b, termination_b,
        from_xyz, to_xyz, route, gauge, routed, slack, relief, disposition,
        negative_color or f"black · {band} · {circuit} GND", joint_ids, electrical_basis,
    )


# ---------------------------------------------------------------------------
# Bundle 1 — on-PDB.  The PDB and dock-side pieces are cut/terminated before
# the cassette-local signal looms.  Pack/charger circuits remain DEFERRED.
# ---------------------------------------------------------------------------

for signal, suffix, color in (
    ("BAT+", "BAT+", "red · POWER · BAT+"),
    ("BAT−", "BAT−", "black · POWER · BAT−"),
):
    add(
        "on-PDB", "BATTERY_MAIN", signal, "power",
        f"CAS-DOCK.XT60_LOAD.{suffix}", f"PDB.{suffix}",
        "XT60 recessed load half", "SOLDERED cup",
        "PDB pad", "SOLDERED",
        XYZ["DOCK_PWR"], XYZ["PDB"],
        "on-PDB: ganged-dock XT60 seat → BAT pad; shortest protected run",
        "16 AWG", 50, 30, 20, "DEFER — 2S pack in transit",
        color, "J-CAS-012; J-CAS-017; J-PWR-002",
        "Connector map: Battery main · Pack → PDB · +, − · XT60",
    )

usb_rows = (
    ("5 V", "VBUS", "USB_5V", "22 AWG", "red · POWER · USB 5V"),
    ("GND", "GND", "USB_GND", "22 AWG", "black · POWER · USB GND"),
    ("D+", "D+", "USB_D+", "28 AWG", "green · USB D+"),
    ("D−", "D−", "USB_D−", "28 AWG", "white · USB D−"),
    ("CC", "CC", "USB_CC", "28 AWG", "blue · USB CC"),
)
for signal, a_pad, b_pad, gauge, color in usb_rows:
    add(
        "on-PDB", "USB_C_CHARGE", signal, "power",
        f"HIDDEN_USB_C.{a_pad}", f"PDB/IP2326_INTERFACE.{b_pad}",
        "USB-C receptacle pad", "SOLDERED",
        "PDB/IP2326 interface pad", "SOLDERED",
        XYZ["PORT"], XYZ["CHARGE"],
        "on-PDB/charge bay; hidden-port path TBD; keep D+/D− together",
        gauge, 40, 70, 30, "DEFER — IP2326 charge hardware not sourced",
        color, "J-CHG-001; J-CHG-003; J-CAS-005",
        "Connector map: USB-C charge · port → PDB · 5 V, D±/CC; common-ground rule supplies GND",
    )

for pin in (1, 2, 3):
    add(
        "on-PDB", "PACK_BALANCE", f"2S balance contact {pin}", "power",
        f"CAS-DOCK.BALANCE_LOAD.pin{pin}", f"IP2326.JST-XH_3.pin{pin}",
        "JST-XH 3-pin load half", "CRIMPED contact",
        "JST-XH 3-pin charge-module half", "CRIMPED contact",
        XYZ["DOCK_SIG"], XYZ["CHARGE"],
        "on-PDB: balance dock seat → charge bay; pin order witness pending",
        "22 AWG", 50, 40, 20, "DEFER — 2S pack and IP2326 not sourced",
        f"white flag · BAL-{pin} · polarity TBD", "J-CAS-005; J-CAS-014; J-CHG-001",
        "Connector map: Pack balance · Pack → charge module · 2S balance · JST-XH 3-pin",
    )

add_pair(
    "on-PDB", "RAIL_A_DOCK_FEED", "A clean",
    "PDB.RAIL_A", "CAS-DOCK.RAIL_A_INPUT",
    "PDB rail pad", "SOLDERED", "XT30 shrouded/socket source half", "SOLDERED cup",
    XYZ["PDB"], XYZ["DOCK_PWR"],
    "on-PDB: Rail-A pad → visually blue-banded XT30 dock feed",
    "20 AWG", 50, 30, 20, "HOLD — cassette/dock dry-fit",
    "J-CAS-004; J-CAS-012; J-CAS-017",
    "Connector map: Rail A bus · PDB → clean loads · 5 V, GND · XT30",
    negative_endpoint_a="PDB.GND_STAR",
)
add_pair(
    "on-PDB", "RAIL_B_DOCK_FEED", "B servos",
    "PDB.RAIL_B", "CAS-DOCK.RAIL_B_INPUT",
    "PDB rail pad", "SOLDERED", "XT30 shrouded/socket source half", "SOLDERED cup",
    XYZ["PDB"], XYZ["DOCK_PWR"],
    "on-PDB: Rail-B pad → visually yellow-banded XT30 dock feed",
    "20 AWG", 50, 30, 20, "HOLD — cassette/dock dry-fit",
    "J-CAS-004; J-CAS-012; J-CAS-017",
    "Connector map: Rail B bus · PDB → servo loads · 5 V, GND · XT30",
    negative_endpoint_a="PDB.GND_STAR",
)

add(
    "on-PDB", "BATTERY_ADC", "battery divider tap", "A clean",
    "PDB.27k/10k_DIV_TAP", "ESP32#1.GPIO34",
    "PDB divider pad", "SOLDERED",
    "ESP32#1 pad; no connector specified", "SOLDERED",
    XYZ["PDB"], XYZ["ESP1"],
    "on-PDB → cassette wall; short quiet run, twisted beside its star-ground return",
    "28 AWG", 70, 40, 20, "HOLD — cassette/ESP32 dry-fit",
    "white · blue band · ADC34", "J-CAS-004; J-CAS-007",
    "PDB contents: 27 k / 10 k divider tap → ESP32 #1 GPIO34",
)


# ---------------------------------------------------------------------------
# Bundle 2 — on-cassette.  Includes local modules and the cassette-side pigtails
# and rail fan-out that terminate in the ganged dock.
# ---------------------------------------------------------------------------

for circuit, endpoint, xyz, routed in (
    ("ESP32_1_POWER", "ESP32#1", XYZ["ESP1"], 60),
    ("ESP32_2_POWER", "ESP32#2", XYZ["ESP2"], 70),
    ("WIFI_POWER", "BL-M8812EU2", XYZ["WIFI"], 90),
):
    add_pair(
        "on-cassette", circuit, "A clean",
        "PDB.RAIL_A", endpoint,
        "XT30 load half (mates shrouded/socket PDB source)", "SOLDERED cup",
        f"{endpoint} power pad/header", "SOLDERED",
        XYZ["PDB"], xyz,
        "on-cassette; separate clean-rail branch; WiFi route waits on placement",
        "20 AWG" if circuit == "WIFI_POWER" else "22 AWG",
        routed, 40, 20, "HOLD — cassette physical dry-fit",
        "J-CAS-004; J-CAS-007; J-CAS-008; J-CAS-010",
        "Connector map: Rail A bus · PDB → clean loads · 5 V, GND · XT30 per branch",
        negative_endpoint_a="PDB.GND_STAR",
    )

crsf_rows = (
    ("RP1_TX", "RP1.RP1_TX", "ESP32#1.GPIO16", "28 AWG", "white · CRSF RX16", XYZ["RP1"], XYZ["ESP1"]),
    ("CRSF telemetry", "ESP32#1.GPIO17", "RP1.RP1_RX", "28 AWG", "white · CRSF TX17", XYZ["ESP1"], XYZ["RP1"]),
    ("+5 V", "PDB.RAIL_A.+5V", "RP1.+5V", "22 AWG", "red · blue band · CRSF 5V", XYZ["PDB"], XYZ["RP1"]),
    ("GND", "PDB.GND_STAR", "RP1.GND", "22 AWG", "black · blue band · CRSF GND", XYZ["PDB"], XYZ["RP1"]),
)
for signal, ep_a, ep_b, gauge, color, xyz_a, xyz_b in crsf_rows:
    add(
        "on-cassette", "CRSF", signal, "A clean",
        ep_a, ep_b,
        "JST-XH 4-pin source pigtail", "CRIMPED contact; module end SOLDERED",
        "JST-XH 4-pin RP1 pigtail", "CRIMPED contact; RP1 end SOLDERED",
        xyz_a, xyz_b,
        "on-cassette rear service deck; twist TX/RX and keep off switching nodes",
        gauge, 60, 40, 20, "HOLD — cassette physical dry-fit",
        color, "J-CAS-007; J-CAS-009; J-CAS-014",
        "Connector map: CRSF · RP1 ↔ ESP32 #1 · RP1_TX→GPIO16, GPIO17→RP1_RX, 5 V, GND · JST-XH 4-pin",
    )

link2_rows = (
    ("link2 TX", "ESP32#1.GPIO25", "ESP32#2.GPIO16", "white · LINK2 25→16", "BASE", "HOLD — cassette physical dry-fit", XYZ["ESP1"], XYZ["ESP2"]),
    ("optional ack", "ESP32#2.GPIO17", "ESP32#1.GPIO26", "violet · OPT ACK 17→26", "OPTIONAL", "OPTIONAL — not opened in firmware; do not populate", XYZ["ESP2"], XYZ["ESP1"]),
    ("GND", "ESP32#1.GND", "ESP32#2.GND", "black · LINK2 GND", "BASE", "HOLD — cassette physical dry-fit", XYZ["ESP1"], XYZ["ESP2"]),
)
for signal, ep_a, ep_b, color, ordering_class, disposition, xyz_a, xyz_b in link2_rows:
    add(
        "on-cassette", "LINK2", signal, "A clean",
        ep_a, ep_b,
        "JST-XH 3-pin board-#1 half", "CRIMPED contact; module end SOLDERED",
        "JST-XH 3-pin board-#2 half", "CRIMPED contact; module end SOLDERED",
        xyz_a, xyz_b,
        "on-cassette between opposed mini-board wall seats",
        "28 AWG", 70, 40, 20, disposition,
        color, "J-CAS-007; J-CAS-008; J-CAS-014",
        "Connector map: link2 · GPIO25→GPIO16(#2), (opt) GPIO26←GPIO17(#2), GND · JST-XH 3-pin",
        ordering_class=ordering_class,
    )

i2s_rows = (
    ("BCLK", "ESP32#2.GPIO26", "MAX98357A.BCLK", "28 AWG", "white · I2S BCLK26"),
    ("LRCLK", "ESP32#2.GPIO25", "MAX98357A.LRCLK", "28 AWG", "white · I2S LRCLK25"),
    ("DIN", "ESP32#2.GPIO22", "MAX98357A.DIN", "28 AWG", "white · I2S DIN22"),
    ("+5 V", "PDB.RAIL_A.+5V", "MAX98357A.+5V", "22 AWG", "red · blue band · AMP 5V"),
    ("GND", "PDB.GND_STAR", "MAX98357A.GND", "22 AWG", "black · blue band · AMP GND"),
)
for signal, ep_a, ep_b, gauge, color in i2s_rows:
    add(
        "on-cassette", "I2S_AUDIO", signal, "A clean",
        ep_a, ep_b,
        "JST-XH 5-pin source pigtail", "CRIMPED contact; source end SOLDERED",
        "JST-XH 5-pin amp pigtail", "CRIMPED contact; amp end SOLDERED",
        XYZ["PDB"] if ep_a.startswith("PDB.") else XYZ["ESP2"], XYZ["AMP"],
        "on-cassette rear service deck; clocks/data grouped, speaker pair separated",
        gauge, 60, 40, 20, "HOLD — cassette physical dry-fit",
        color, "J-CAS-008; J-CAS-018; J-CAS-014",
        "Connector map: I2S audio · BCLK26, LRCLK25, DIN22, +5 V(A), GND · JST-XH 5-pin",
    )

# Cassette-side source pigtails into the ganged dock.
servo_signal_sources = (
    ("STEERING", "ESP32#1.GPIO13", "CAS-DOCK.STEERING_SOURCE.SIG", "W-STEER SIG13", "HOLD — cassette/dock dry-fit"),
    ("ESC_SIGNAL", "ESP32#1.GPIO14", "CAS-DOCK.ESC_SOURCE.SIG", "W-ESC SIG14", "HOLD — cassette/dock dry-fit"),
    ("DRS", "ESP32#1.GPIO18", "CAS-DOCK.DRS_SOURCE.SIG", "W-DRS SIG18", "DEFER — MG90S in transit"),
    ("PAN", "ESP32#1.GPIO19", "CAS-DOCK.PAN_SOURCE.SIG", "W-PAN SIG19", "DEFER — MG90S in transit"),
    ("TILT", "ESP32#1.GPIO23", "CAS-DOCK.TILT_SOURCE.SIG", "W-TILT SIG23", "DEFER — MG90S in transit"),
)
for circuit, ep_a, ep_b, label, disposition in servo_signal_sources:
    add(
        "on-cassette", circuit, "sig", "B servos",
        ep_a, ep_b,
        "ESP32#1 pad", "SOLDERED",
        "positive-lock 3-pin servo dock source contact", "CRIMPED contact",
        XYZ["ESP1"], XYZ["DOCK_PED"] if circuit in {"PAN", "TILT"} else XYZ["DOCK_SIG"],
        "on-cassette → stepped/wrapped servo bank; no centre-spine run",
        "28 AWG", 80, 50, 20, disposition,
        f"white · yellow band · {label}", "J-CAS-007; J-CAS-013; J-CAS-017",
        {
            "STEERING": "Connector map: Steering servo · ESP32 #1 GPIO13 · 3-pin servo",
            "ESC_SIGNAL": "Connector map: ESC signal · ESP32 #1 GPIO14 → ESC · 3-pin servo, +5 V pin removed",
            "DRS": "Connector map: DRS servo · ESP32 #1 GPIO18 · 3-pin servo",
            "PAN": "Connector map: Gimbal pan · ESP32 #1 GPIO19 · 3-pin servo",
            "TILT": "Connector map: Gimbal tilt · ESP32 #1 GPIO23 · 3-pin servo",
        }[circuit],
    )

add(
    "on-cassette", "LED", "data", "A clean",
    "ESP32#2.GPIO4", "CAS-DOCK.LED_SOURCE.DATA",
    "ESP32#2 pad", "SOLDERED",
    "JST-XH 3-pin dock source contact", "CRIMPED contact",
    XYZ["ESP2"], XYZ["DOCK_SIG"],
    "on-cassette → signal bank; keep with its ground branch",
    "28 AWG", 90, 50, 20, "HOLD — cassette/dock dry-fit",
    "white · blue band · LED DATA4", "J-CAS-008; J-CAS-014; J-CAS-017",
    "Connector map: LEDs · ESP32 #2 GPIO4 → WS2812B · data, +5 V(A), GND · JST-XH 3-pin",
)
add(
    "on-cassette", "HALL", "sig", "A clean",
    "CAS-DOCK.HALL_SOURCE.SIG", "ESP32#1.GPIO35",
    "JST-XH 3-pin dock source contact", "CRIMPED contact",
    "ESP32#1 pad", "SOLDERED",
    XYZ["DOCK_SIG"], XYZ["ESP1"],
    "signal bank → ESP32#1; twist beside Hall ground; 10 k pull-up stays on board",
    "28 AWG", 80, 50, 20, "HOLD — cassette/dock dry-fit",
    "white · blue band · HALL GPIO35", "J-CAS-007; J-CAS-014; J-CAS-017",
    "Connector map: Hall · sensor → ESP32 #1 GPIO35 · sig, +5 V(A), GND",
)

for signal, wifi_pad, dock_pad, color in (
    ("D+", "DP", "D+", "green · USB D+"),
    ("D−", "DM", "D−", "white · USB D−"),
):
    add(
        "on-cassette", "CAMERA_USB", signal, "A clean",
        f"CAS-DOCK.USB4_SOURCE.{dock_pad}", f"BL-M8812EU2.{wifi_pad}",
        "shielded USB 4-pin dock source contact", "CRIMPED or SOLDERED per selected USB4",
        "BL-M8812EU2 USB pad", "SOLDERED",
        XYZ["DOCK_PED"], XYZ["WIFI"],
        "on-cassette from shielded USB4 dock seat → unplaced WiFi seat",
        "28 AWG", 90, 60, 20, "HOLD — WiFi placement and USB4 body dry-fit",
        color, "J-CAS-010; J-CAS-014; J-CAS-017",
        f"Connector map: Camera ↔ WiFi · {signal}→{'DP' if signal == 'D+' else 'DM'} · shielded 4-pin / micro-USB",
    )

for signal, amp_pad, dock_pad, color in (
    ("speaker +", "SPK+", "+", "white · SPK+"),
    ("speaker −", "SPK−", "−", "black · SPK−"),
):
    add(
        "on-cassette", "SPEAKER", signal, "A clean",
        f"MAX98357A.{amp_pad}", f"CAS-DOCK.SPEAKER_SOURCE.{dock_pad}",
        "MAX98357A speaker pad", "SOLDERED",
        "JST-PH 2-pin dock source contact", "CRIMPED contact",
        XYZ["AMP"], XYZ["DOCK_SIG"],
        "on-cassette amp → U-AUX speaker seat; keep away from ADC/Hall",
        "24 AWG", 70, 40, 20, "HOLD — cassette/dock dry-fit",
        color, "J-CAS-018; J-CAS-017; J-AUD-002",
        "Connector map: Speaker · amp → speaker · +, − · JST-PH 2-pin",
    )

# Power/ground fan-out inside the dock.  These do not assign new nets; they
# carry the authoritative A/B rail to the named contacts in the firm connector bank.
dock_fanouts = (
    ("CAMERA_USB", "A clean", "USB4_SOURCE", "24 AWG", "HOLD — dock/pedestal dry-fit"),
    ("LED", "A clean", "LED_SOURCE", "20 AWG", "HOLD — dock/umbilical dry-fit"),
    ("HALL", "A clean", "HALL_SOURCE", "28 AWG", "HOLD — dock/umbilical dry-fit"),
    ("STEERING", "B servos", "STEERING_SOURCE", "22 AWG", "HOLD — dock/steering dry-fit"),
    ("DRS", "B servos", "DRS_SOURCE", "24 AWG", "DEFER — MG90S in transit"),
    ("PAN", "B servos", "PAN_SOURCE", "24 AWG", "DEFER — MG90S in transit"),
    ("TILT", "B servos", "TILT_SOURCE", "24 AWG", "DEFER — MG90S in transit"),
    ("BLOWER", "B servos", "BLOWER_SOURCE", "24 AWG", "HOLD — auxiliary seat/conduit route open"),
)
for circuit, rail, dock_group, gauge, disposition in dock_fanouts:
    source = "CAS-DOCK.RAIL_A_INPUT" if rail == "A clean" else "CAS-DOCK.RAIL_B_INPUT"
    family = {
        "CAMERA_USB": "shielded USB 4-pin",
        "LED": "JST-XH 3-pin",
        "HALL": "JST-XH 3-pin",
        "STEERING": "positive-lock 3-pin servo",
        "DRS": "positive-lock 3-pin servo",
        "PAN": "positive-lock 3-pin servo",
        "TILT": "positive-lock 3-pin servo",
        "BLOWER": "2-pin JST",
    }[circuit]
    add_pair(
        "on-cassette", f"{circuit}_DOCK_POWER", rail,
        source, f"CAS-DOCK.{dock_group}",
        f"XT30 {rail} load/bus contact", "SOLDERED bus joint",
        f"{family} dock source contact", "CRIMPED contact",
        XYZ["DOCK_PWR"], XYZ["DOCK_PED"] if circuit in {"CAMERA_USB", "PAN", "TILT", "BLOWER"} else XYZ["DOCK_SIG"],
        "on-cassette dock internal fan-out; A0 strain relief before first bend",
        gauge, 30, 30, 20, disposition,
        "J-CAS-012; J-CAS-013; J-CAS-014; J-CAS-017",
        f"Connector map: {circuit} power is {rail}; all grounds common",
    )

# ESC uses signal + ground only.  The +5 V position is intentionally absent.
add(
    "on-cassette", "ESC_SIGNAL", "GND", "power",
    "PDB.GND_STAR", "CAS-DOCK.ESC_SOURCE.GND",
    "PDB star pad", "SOLDERED",
    "positive-lock 3-pin servo dock source contact", "CRIMPED contact",
    XYZ["PDB"], XYZ["DOCK_SIG"],
    "on-cassette → ESC dock position; +5 contact cavity left empty and witnessed",
    "28 AWG", 80, 50, 20, "HOLD — cassette/dock dry-fit",
    "black · ESC GND · RED/+5 CAVITY EMPTY", "J-CAS-004; J-CAS-013; J-CAS-017",
    "Connector map: ESC signal · sig, GND only · ESC BEC +5 V isolated; +5 V pin removed",
)

for side, endpoint, xyz in (
    ("J0", "VID-ANT#1.U_FL", XYZ["ANT_L"]),
    ("J1", "VID-ANT#2.U_FL", XYZ["ANT_R"]),
):
    add(
        "on-cassette", f"RF_{side}", "5.8 GHz RF", "RF",
        f"BL-M8812EU2.{side}", endpoint,
        "U.FL plug/jack", "FACTORY-TERMINATED — DO NOT SOLDER",
        "U.FL whip assembly", "FACTORY-TERMINATED — DO NOT CUT",
        XYZ["WIFI"], xyz,
        "on-cassette H-10 to antenna root; ≥10 mm bend; no service pull on jack",
        "50 Ω micro-coax", 70, 0, 10, "HOLD — WiFi/antenna placement dry-fit",
        f"black coax · RF-{side}", f"J-CAS-010; J-ELC-0{13 if side == 'J0' else 14}",
        "Connector map: Antennas · WiFi module → antennas · RF · U.FL ×J0/J1",
        confidence="FIRM electrical / ASSUMPTION placement",
        cut_to_fit="NO — purchase 80 mm factory lead; never field-cut coax",
    )


# ---------------------------------------------------------------------------
# Bundle 3 — pedestal conduit.  These are the chassis-side cuts from the dock
# through the fixed hollow pedestal.  MG90S circuits are explicitly DEFERRED.
# ---------------------------------------------------------------------------

for circuit, signal_ep, servo_ep, routed, slack in (
    ("PAN", "CAS-DOCK.PAN_LOAD.SIG", "MG90S_PAN.SIG", 140, 90),
    ("TILT", "CAS-DOCK.TILT_LOAD.SIG", "MG90S_TILT.SIG", 150, 100),
):
    add(
        "pedestal-conduit", circuit, "sig", "B servos",
        signal_ep, servo_ep,
        "positive-lock 3-pin servo dock load contact", "CRIMPED contact",
        "3-pin servo connector", "CRIMPED/factory contact",
        XYZ["DOCK_PED"], XYZ["PED"],
        "dock → ≥25 mm lower loop → R1/R2 turn → 10×18 pedestal conduit → gimbal loop",
        "28 AWG", routed, slack, 30, "DEFER — MG90S in transit",
        f"white · yellow band · {circuit} SIG", "J-CAS-011; J-CAS-013; J-CAS-016; J-CAS-017",
        f"Connector map: Gimbal {circuit.lower()} · ESP32 #1 GPIO{'19' if circuit == 'PAN' else '23'} · sig, +5 V(B), GND",
    )
    for signal, suffix, gauge, color in (
        ("+5 V", "+5V", "24 AWG", f"red · yellow band · {circuit} 5V"),
        ("GND", "GND", "24 AWG", f"black · yellow band · {circuit} GND"),
    ):
        add(
            "pedestal-conduit", circuit, signal, "B servos",
            f"CAS-DOCK.{circuit}_LOAD.{suffix}", f"MG90S_{circuit}.{suffix}",
            "positive-lock 3-pin servo dock load contact", "CRIMPED contact",
            "3-pin servo connector", "CRIMPED/factory contact",
            XYZ["DOCK_PED"], XYZ["PED"],
            "dock → ≥25 mm lower loop → R1/R2 turn → 10×18 pedestal conduit → gimbal loop",
            gauge, routed, slack, 30, "DEFER — MG90S in transit",
            color, "J-CAS-011; J-CAS-013; J-CAS-016; J-CAS-017",
            f"Connector map: Gimbal {circuit.lower()} · sig, +5 V(B), GND · 3-pin servo",
        )

camera_remote = (
    ("D+", "D+", "DP", "28 AWG", "green · USB D+"),
    ("D−", "D−", "DM", "28 AWG", "white · USB D−"),
    ("+5 V", "+5V", "+5V", "24 AWG", "red · blue band · CAMERA 5V"),
    ("GND", "GND", "GND", "24 AWG", "black · blue band · CAMERA GND"),
)
for signal, dock_pad, cam_pad, gauge, color in camera_remote:
    is_data = signal in {"D+", "D−"}
    add(
        "pedestal-conduit", "CAMERA_USB", signal, "A clean",
        f"VID-CAM.{signal}" if is_data else f"CAS-DOCK.USB4_LOAD.{dock_pad}",
        f"CAS-DOCK.USB4_LOAD.{dock_pad}" if is_data else f"VID-CAM.{cam_pad}",
        "shielded micro-USB/camera pad" if is_data else "shielded USB 4-pin dock load contact",
        "SOLDERED or factory micro-USB" if is_data else "CRIMPED or SOLDERED per selected USB4",
        "shielded USB 4-pin dock load contact" if is_data else "shielded micro-USB/camera pad",
        "CRIMPED or SOLDERED per selected USB4" if is_data else "SOLDERED or factory micro-USB",
        XYZ["PED"] if is_data else XYZ["DOCK_PED"],
        XYZ["DOCK_PED"] if is_data else XYZ["PED"],
        "camera ↔ 10×18 pedestal conduit ↔ ≥20 mm USB bend / ≥25 mm lower loop ↔ dock",
        gauge, 160, 90, 30, "HOLD — camera/USB4/pedestal dry-fit",
        color, "J-CAS-011; J-CAS-014; J-CAS-016; J-CAS-017",
        "Connector map: Camera ↔ WiFi · D+→DP, D−→DM, +5 V(A), GND · shielded 4-pin / micro-USB",
    )

for signal, suffix, color in (
    ("+5 V", "+5V", "red · yellow band · BLOWER 5V"),
    ("GND", "GND", "black · yellow band · BLOWER GND"),
):
    add(
        "pedestal-conduit", "BLOWER", signal, "B servos",
        f"CAS-DOCK.BLOWER_LOAD.{suffix}", f"COOL-BLOW.{suffix}",
        "2-pin JST dock load contact", "CRIMPED contact",
        "2-pin JST blower connector", "CRIMPED/factory contact",
        XYZ["DOCK_PED"], XYZ["BLOWER"],
        "dock → R1/pedestal-adjacent route; conduit inclusion is OPEN (firm conduit bundle excludes blower)",
        "24 AWG", 160, 90, 30, "HOLD — auxiliary seat and camera-module route open",
        color, "J-CAS-016; J-CAS-017",
        "Connector map: Blower · Rail B · +5 V, GND (always-on) · 2-pin JST",
    )


# ---------------------------------------------------------------------------
# Bundle 4 — chassis umbilical.  Fixed-consumer loom from the parked dock half
# into R1/R2; pack leads and MG90S DRS lead remain DEFERRED.
# ---------------------------------------------------------------------------

for signal, suffix, color in (
    ("BAT+", "BAT+", "red · POWER · BAT+"),
    ("BAT−", "BAT−", "black · POWER · BAT−"),
):
    add(
        "umbilical", "BATTERY_MAIN", signal, "power",
        f"2S_PACK.{suffix}", f"CAS-DOCK.XT60_SOURCE.{suffix}",
        "pack tab/lead", "FACTORY-SOLDERED",
        "XT60 shrouded/socket source half", "SOLDERED cup",
        XYZ["PACK"], XYZ["DOCK_PWR"],
        "pack lead → strain anchor → ganged dock; no exposed live contact",
        "16 AWG", 100, 70, 30, "DEFER — 2S pack in transit",
        color, "J-PWR-002; J-CAS-012; J-CAS-017",
        "Connector map: Battery main · Pack → PDB · +, − · XT60",
    )

for pin in (1, 2, 3):
    add(
        "umbilical", "PACK_BALANCE", f"2S balance contact {pin}", "power",
        f"2S_PACK.JST-XH_3.pin{pin}", f"CAS-DOCK.BALANCE_SOURCE.pin{pin}",
        "pack JST-XH 3-pin contact", "FACTORY-CRIMPED",
        "JST-XH 3-pin dock source contact", "CRIMPED contact",
        XYZ["PACK"], XYZ["DOCK_SIG"],
        "pack balance lead → protected parallel path to signal bank; no pin-order inference",
        "22 AWG", 110, 80, 30, "DEFER — 2S pack and IP2326 not sourced",
        f"white flag · BAL-{pin} · polarity TBD", "J-PWR-002; J-CAS-005; J-CAS-014; J-CAS-017",
        "Connector map: Pack balance · Pack → charge module · 2S balance · JST-XH 3-pin",
    )

fixed_remote = {
    "STEERING": {
        "xyz": XYZ["STEER"], "route": "dock → immediate R2 turn → A1 → A2/X1 lateral exit → steering lead",
        "routed": 190, "slack": 60, "disposition": "HOLD — steering/dock dry-fit",
        "joint": "J-SRV-002; J-CAS-013; J-CAS-017",
        "basis": "Connector map: Steering servo · ESP32 #1 GPIO13 · sig, +5 V(B), GND · 3-pin servo",
        "gauge_power": "22 AWG",
    },
    "DRS": {
        "xyz": XYZ["DRS"], "route": "dock → R2 first bend → X1 90° cross → R1/A3 rear tail → wing loop",
        "routed": 260, "slack": 90, "disposition": "DEFER — MG90S in transit",
        "joint": "J-CAS-013; J-CAS-017",
        "basis": "Connector map: DRS servo · ESP32 #1 GPIO18 · sig, +5 V(B), GND · 3-pin servo",
        "gauge_power": "24 AWG",
    },
}
for circuit, meta in fixed_remote.items():
    for signal, suffix, gauge, color in (
        ("sig", "SIG", "28 AWG", f"white · yellow band · {circuit} SIG"),
        ("+5 V", "+5V", meta["gauge_power"], f"red · yellow band · {circuit} 5V"),
        ("GND", "GND", meta["gauge_power"], f"black · yellow band · {circuit} GND"),
    ):
        add(
            "umbilical", circuit, signal, "B servos",
            f"CAS-DOCK.{circuit}_LOAD.{suffix}", f"{'DS3235SG' if circuit == 'STEERING' else 'MG90S_DRS'}.{suffix}",
            "positive-lock 3-pin servo dock load contact", "CRIMPED contact",
            "3-pin servo connector", "CRIMPED/factory contact",
            XYZ["DOCK_SIG"], meta["xyz"],
            meta["route"], gauge, meta["routed"], meta["slack"], 30, meta["disposition"],
            color, meta["joint"], meta["basis"],
        )

for signal, suffix, endpoint, color in (
    ("sig", "SIG", "ESC.SIG", "white · ESC SIG14"),
    ("GND", "GND", "ESC.GND", "black · ESC GND · +5 CAVITY EMPTY"),
):
    add(
        "umbilical", "ESC_SIGNAL", signal, "power",
        f"CAS-DOCK.ESC_LOAD.{suffix}", endpoint,
        "positive-lock 3-pin servo dock load contact", "CRIMPED contact",
        "3-pin servo connector with +5 contact removed", "CRIMPED contact",
        XYZ["DOCK_SIG"], XYZ["ESC"],
        "dock → immediate R2 turn → A1 → ESC signal exit; stay ≥20 mm from motor phase run",
        "28 AWG", 180, 50, 30, "HOLD — ESC/dock dry-fit",
        color, "J-CAS-013; J-CAS-017",
        "Connector map: ESC signal · ESP32 #1 GPIO14 → ESC · sig, GND only · 3-pin servo, +5 V pin removed",
    )

for signal, suffix, gauge, color in (
    ("data", "DATA", "28 AWG", "white · blue band · LED DATA4"),
    ("+5 V", "+5V", "20 AWG", "red · blue band · LED 5V"),
    ("GND", "GND", "20 AWG", "black · blue band · LED GND"),
):
    add(
        "umbilical", "LED", signal, "A clean",
        f"CAS-DOCK.LED_LOAD.{suffix}", f"WS2812B.{suffix if signal != 'data' else 'DIN'}",
        "JST-XH 3-pin dock load contact", "CRIMPED contact",
        "JST-XH 3-pin strip connector",
        "CRIMPED contact; strip pigtail SOLDERED"
        + (" through documented 330 Ω series resistor" if signal == "data" else ""),
        XYZ["DOCK_SIG"], XYZ["LED"],
        "dock → immediate R1 turn → A1/A2 → A3 rear tail → strip input service loop",
        gauge, 260, 90, 30, "HOLD — LED segment/topology dry-fit",
        color, "J-LGT-001; J-CAS-014; J-CAS-017",
        "Connector map: LEDs · ESP32 #2 GPIO4 → WS2812B · data, +5 V(A), GND · JST-XH 3-pin",
    )

for signal, suffix, endpoint, color in (
    ("sig", "SIG", "A3144.OUT", "white · blue band · HALL GPIO35"),
    ("+5 V", "+5V", "A3144.+5V", "red · blue band · HALL 5V"),
    ("GND", "GND", "A3144.GND", "black · blue band · HALL GND"),
):
    add(
        "umbilical", "HALL", signal, "A clean",
        endpoint if signal == "sig" else f"CAS-DOCK.HALL_LOAD.{suffix}",
        f"CAS-DOCK.HALL_LOAD.{suffix}" if signal == "sig" else endpoint,
        "JST-XH 3-pin Hall connector" if signal == "sig" else "JST-XH 3-pin dock load contact",
        "CRIMPED contact; sensor pigtail SOLDERED" if signal == "sig" else "CRIMPED contact",
        "JST-XH 3-pin dock load contact" if signal == "sig" else "JST-XH 3-pin Hall connector",
        "CRIMPED contact" if signal == "sig" else "CRIMPED contact; sensor pigtail SOLDERED",
        XYZ["HALL"] if signal == "sig" else XYZ["DOCK_SIG"],
        XYZ["DOCK_SIG"] if signal == "sig" else XYZ["HALL"],
        "axle service loop ↔ A3 rear edge ↔ A2/R1 ↔ dock; twist sig/GND",
        "28 AWG", 220, 70, 30, "HOLD — Hall bracket/dock dry-fit",
        color, "J-SNS-002; J-SNS-003; J-CAS-014; J-CAS-017",
        "Connector map: Hall · sensor → ESP32 #1 GPIO35 · sig, +5 V(A), GND · JST-XH 3-pin",
    )

for signal, suffix, endpoint, color in (
    ("speaker +", "+", "SPEAKER.+", "white · SPK+"),
    ("speaker −", "−", "SPEAKER.−", "black · SPK−"),
):
    add(
        "umbilical", "SPEAKER", signal, "A clean",
        f"CAS-DOCK.SPEAKER_LOAD.{suffix}", endpoint,
        "JST-PH 2-pin dock load contact", "CRIMPED contact",
        "JST-PH 2-pin speaker connector", "CRIMPED/factory contact",
        XYZ["DOCK_SIG"], XYZ["SPEAKER"],
        "dock → R1/A1 → X2 if required → left sidepod speaker; twist pair",
        "24 AWG", 180, 50, 30, "HOLD — speaker/dock dry-fit",
        color, "J-AUD-002; J-AUD-003; J-CAS-017",
        "Connector map: Speaker · amp → speaker · +, − · JST-PH 2-pin",
    )


# Connector/pin count is by distinct mating interface, not by occurrences in
# conductor rows.  Contacts count both halves of a pair.
CONNECTORS = [
    ("XT60", "ganged battery-main pair", 1, 2, 4, "SOLDERED cups", "DEFER"),
    ("XT30", "Rail-A/Rail-B dock feeds + 3 local clean branches", 5, 10, 20, "SOLDERED cups", "BASE"),
    ("USB-C", "hidden charge receptacle (external cable excluded)", 1, 1, 5, "SOLDERED pads mapped", "DEFER"),
    ("JST-XH 3-pin", "balance dock+charger, link2, LED dock+strip, Hall dock+sensor", 7, 14, 40, "CRIMPED; +2 optional ACK contacts", "BASE + DEFER"),
    ("JST-XH 4-pin", "CRSF", 1, 2, 8, "CRIMPED contacts; module pigtails soldered", "BASE"),
    ("JST-XH 5-pin", "I2S audio", 1, 2, 10, "CRIMPED contacts; module pigtails soldered", "BASE"),
    ("3-pin servo", "dock + endpoint pairs for steering/ESC/DRS/pan/tilt", 10, 20, 56, "CRIMPED; ESC +5 cavity empty at both interfaces", "BASE + DEFER"),
    ("2-pin JST", "blower dock + endpoint", 2, 4, 8, "CRIMPED", "BASE"),
    ("JST-PH 2-pin", "speaker dock + endpoint", 2, 4, 8, "CRIMPED", "BASE"),
    ("shielded USB 4-pin / micro-USB", "camera dock + camera endpoint", 2, 4, 16, "selected shielded termination; four mapped conductors", "BASE"),
    ("U.FL", "J0/J1 RF links", 2, 4, 0, "factory-terminated coax; no loose pins", "BASE"),
]


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def joint_links(value: str) -> str:
    return "; ".join(
        f"[`{joint_id.strip()}`](Z_connection_joint_register.md)"
        for joint_id in value.split(";")
        if joint_id.strip()
    )


def write_csv() -> None:
    fields = list(asdict(WIRES[0]))
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(asdict(w) for w in WIRES)


def totals_by_gauge(*, include_optional: bool) -> Counter[str]:
    result: Counter[str] = Counter()
    for wire in WIRES:
        if not include_optional and wire.ordering_class == "OPTIONAL":
            continue
        result[wire.gauge] += wire.cut_length_mm
    return result


def rounded_order_mm(total_mm: int) -> int:
    return int(math.ceil((total_mm * 1.15) / 500.0) * 500)


def write_md() -> None:
    base_totals = totals_by_gauge(include_optional=False)
    all_totals = totals_by_gauge(include_optional=True)
    defer_totals: Counter[str] = Counter()
    for wire in WIRES:
        if wire.ordering_class != "OPTIONAL" and wire.disposition.startswith("DEFER"):
            defer_totals[wire.gauge] += wire.cut_length_mm

    lines = [
        "# Z · W17 wire schedule",
        "",
        "Generated by `evidence/scripts/p0_14_generate_wire_schedule.py`. Electrical nets, GPIOs, rails and",
        "connector families are transcribed from the supplied `w17-electrical-inputs-for-codex.md`",
        f"(SHA-256 `{ELECTRICAL_SOURCE_SHA256}`) and the firmware pin maps it cites",
        f"(control `{CONTROL_PINMAP_SHA256}`; sound/light `{SOUNDLIGHT_PINMAP_SHA256}`).",
        "This file adds physical cuts/routes only; it does not revise the existing analysis, component",
        "values, placements, Joint Register or any STL.",
        "",
        f"**Coverage:** {len(WIRES)} physical cut pieces · {sum(w.disposition.startswith('DEFER') for w in WIRES)} DEFER · "
        f"{sum(w.ordering_class == 'OPTIONAL' for w in WIRES)} optional/not-populated.",
        "",
        "## Use and limits",
        "",
        "- `from_xyz` / `to_xyz` are DAT-F module envelopes or routing datums from J.3/J.4 and the",
        "  cassette audit—not measured pad centres. `UNPLACED` is intentional.",
        "- Every remote circuit is split at `CAS-DOCK`: cassette-side source/fan-out and chassis-side",
        "  loom cuts are separate rows. No hidden continuous wire crosses the lift-out boundary.",
        "- Every listed cut is a rounded routed estimate with explicit service and strain-relief",
        "  allowances. A `YES` cut-to-fit flag means **do not final-cut now**; loop the estimate at",
        "  full size, record the dry-fit route, then trim once.",
        "- The 2S pack, IP2326 path and every MG90S-dependent cut are `DEFER`. U.FL coax is purchased",
        "  factory-terminated and is never field-cut.",
        "- Source-side XT60/XT30 power contacts are shrouded/socketed and recessed. Rail A is blue-",
        "  banded, Rail B yellow-banded, battery power red-labelled; grounds are black.",
        "- A link-specific housing carries its listed power contacts (CRSF XH4, I2S XH5, servo,",
        "  LED/Hall XH3 and camera USB4). XT30 is used for standalone clean-load branches and the",
        "  two Rail-A/Rail-B dock feeds; no duplicate parallel power connector is inferred.",
        "- No numbered JST/dock pin order is invented. Balance contacts remain `pin1…3` pending a",
        "  polarity witness against the actual pack and charger.",
        "",
        "## Conductor schedule",
        "",
    ]
    for bundle in BUNDLES:
        rows = [w for w in WIRES if w.bundle == bundle]
        lines += [
            f"### {bundle}",
            "",
            "| Wire / Joint | Signal · rail | Endpoint A → endpoint B | Connector / termination A → B | "
            "From → to (DAT-F) | Route | Gauge | Length: route + slack + relief = cut | Confidence / state | CTF | Colour / label |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        for w in rows:
            lines.append(
                "| "
                + " | ".join(
                    md_escape(value)
                    for value in (
                        f"`{w.wire_id}`<br>{joint_links(w.joint_ids)}",
                        f"{w.signal} · {w.rail}",
                        f"`{w.endpoint_a}` → `{w.endpoint_b}`",
                        f"{w.connector_a}; **{w.termination_a}** → {w.connector_b}; **{w.termination_b}**",
                        f"{w.from_xyz} → {w.to_xyz}",
                        w.route,
                        w.gauge,
                        f"≈{w.routed_mm_est} + {w.service_slack_mm} + {w.strain_relief_mm} = **{w.cut_length_mm} mm**",
                        f"{w.confidence}<br>**{w.disposition}**",
                        w.cut_to_fit_at_dry_fit,
                        w.color_label,
                    )
                )
                + " |"
            )
        lines.append("")

    lines += [
        "## Wire totals for ordering",
        "",
        "Totals sum the rounded per-piece CUT estimates. `Planned base` includes deferred pack/charger/",
        "MG90S material so it can be ordered, but excludes the optional link2 ACK. `Cut-now ceiling`",
        "subtracts DEFER material; it is still not permission to final-cut before dry-fit. Suggested",
        "order adds 15% handling/waste and rounds up to the next 0.5 m.",
        "",
        "| Gauge / cable | Planned base | Of which DEFER | Cut-now ceiling | Optional reserve | Suggested order |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for gauge in sorted(all_totals):
        base = base_totals[gauge]
        deferred = defer_totals[gauge]
        optional = all_totals[gauge] - base
        lines.append(
            f"| {gauge} | {base / 1000:.2f} m | {deferred / 1000:.2f} m | "
            f"{(base - deferred) / 1000:.2f} m | {optional / 1000:.2f} m | "
            f"{rounded_order_mm(base + optional) / 1000:.1f} m |"
        )
    lines += [
        "",
        "## Connector and contact totals",
        "",
        "Counts are distinct mating interfaces. A pair has two housings/halves; loaded-contact totals",
        "count both halves. Module PCB pads and solder-only joins are not connector housings.",
        "",
        "| Family | Use | Mating pairs / receptacles | Housings / halves | Loaded contacts / mapped pads | Termination note | State |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for family, use, pairs, housings, contacts, note, state in CONNECTORS:
        lines.append(f"| {family} | {use} | {pairs} | {housings} | {contacts} | {note} | {state} |")

    lines += [
        "",
        "## Prioritized open ASM checks",
        "",
        "1. **ASM-31 / CAS-10 — full terminated dock dummy:** select actual XT60/XT30/JST/servo/",
        "   USB4/auxiliary housings; assign and witness numbered pin order; prove source-side shrouding,",
        "   stepped/wrapped placement, A0/A1 anchors, latch hand, ten mate cycles and cassette lift.",
        "2. **ASM-08 / CAS-01 — powered steering sweep:** record the real steering lead exit and X1/A2",
        "   route at neutral and lock-to-lock with bump; this firms steering, ESC and rear-fan-out lengths.",
        "3. **D-04 / CAS-02 — seat the body and pin S0:** record shell-to-board/header/loop clearance and",
        "   the final R1/R2 vertical routing plane before any local cassette cut is trimmed.",
        "4. **ASM-22 / CAS-04 — populate the 55×45×18 PDB target:** record actual pad/connector exits,",
        "   XT30 branch positions, tall-component side, divider-tap exit and loop-key hand clearance.",
        "5. **CAS-09 — conduit pull coupon:** sequentially pull the actual shielded USB4 and both servo",
        "   connectors through 10×18 clear, then record the lower loop, ≥20 mm USB bend and A1/P1 anchors.",
        "   Also decide a separate blower path: the firm conduit bundle does not currently include it.",
        "6. **ASM-53 / CAS-08 — camera/gimbal dry-fit:** with the real camera, halo/body and arrived",
        "   MG90S units, record gimbal datum, motion loops, blower exit and no-power endpoint sweeps.",
        "7. **ASM-50 / CAS-05 — actual 2S pack:** witness XT60 polarity, JST-XH numbered balance order,",
        "   factory lead lengths, strap/removal path and strain anchors; only then release pack rows.",
        "8. **ASM-59 — actual IP2326 module:** record SKU, pad labels, USB-C receptacle scheme, thermal",
        "   face and charge/run interlock. The source map says `5 V, D±/CC`; it does not authorize a",
        "   guessed IP2326 pad layout.",
        "9. **ASM-55 — speaker/LED/Hall endpoints:** seat the speaker and rear sensor/light parts,",
        "   record A3 branches and service loops, and define the physical WS2812 segment chain without",
        "   assigning any additional GPIO.",
        "10. **Electrical-owner closure before traction harness cutting:** the supplied connector map",
        "    does not state the PDB→ESC battery connector or ESC→motor phase/sensor conductors. They are",
        "    deliberately not invented in this schedule; add them only through an authoritative map update.",
        "",
        "## Regeneration",
        "",
        "```text",
        "python3 10_assembly_architecture/evidence/scripts/p0_14_generate_wire_schedule.py",
        "python3 10_assembly_architecture/evidence/scripts/p0_15_validate_wire_schedule.py",
        "```",
        "",
    ]
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    write_csv()
    write_md()
    print(f"WROTE {CSV_OUT.relative_to(REPO)} ({len(WIRES)} rows)")
    print(f"WROTE {MD_OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
