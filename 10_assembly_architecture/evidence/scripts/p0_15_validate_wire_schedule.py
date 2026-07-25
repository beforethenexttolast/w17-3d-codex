#!/usr/bin/env python3
"""Validate the generated W17 wire schedule and its electrical/physical discipline."""
from __future__ import annotations

import csv
from collections import Counter
from dataclasses import asdict
import hashlib
import importlib.util
from pathlib import Path
import re
import sys


REPO = Path(__file__).resolve().parents[3]
ARCH = REPO / "10_assembly_architecture"
GENERATOR = Path(__file__).with_name("p0_14_generate_wire_schedule.py")
CSV_PATH = ARCH / "Z_wire_schedule.csv"
MD_PATH = ARCH / "Z_wire_schedule.md"
OUT = ARCH / "evidence/p0/tables/p0_d36_wire_schedule_validation.md"


def load_generator():
    spec = importlib.util.spec_from_file_location("p0_14_wire_schedule", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, passed: bool, detail: str, rows: list[tuple[str, str, str]]) -> bool:
    rows.append((name, "PASS" if passed else "FAIL", detail))
    return passed


def main() -> int:
    data = load_generator()
    checks: list[tuple[str, str, str]] = []
    ok = True

    expected = data.WIRES
    expected_dicts = [{key: str(value) for key, value in asdict(w).items()} for w in expected]
    expected_ids = [w.wire_id for w in expected]

    # Authoritative inputs must be the exact reviewed versions.
    source_paths = {
        "connector map": (REPO.parent / "w17-electrical-inputs-for-codex.md", data.ELECTRICAL_SOURCE_SHA256),
        "control PinMap": (REPO.parent / "w17-control-fw/lib/config/include/config/PinMap.hpp", data.CONTROL_PINMAP_SHA256),
        "sound/light PinMap": (REPO.parent / "w17-soundlight-fw/lib/config/include/config/PinMap.hpp", data.SOUNDLIGHT_PINMAP_SHA256),
    }
    for label, (path, expected_sha) in source_paths.items():
        exists = path.is_file()
        ok &= check(f"authoritative {label} exists", exists, str(path), checks)
        if exists:
            actual = sha256(path)
            ok &= check(f"authoritative {label} hash", actual == expected_sha, actual, checks)

    # Pin-map content is checked independently of the hashes for readable failure evidence.
    control_text = source_paths["control PinMap"][0].read_text(encoding="utf-8")
    sound_text = source_paths["sound/light PinMap"][0].read_text(encoding="utf-8")
    control_pin_tokens = {
        "kCrsfUartRxPin = 16", "kCrsfUartTxPin = 17",
        "kBoard2UartTxPin = 25", "kBoard2UartRxPin = 26",
        "kSteeringServoPin = 13", "kEscThrottlePin = 14",
        "kDrsServoPin = 18", "kGimbalPanPin = 19", "kGimbalTiltPin = 23",
        "kBatterySenseAdcPin = 34", "kWheelSpeedHallPin = 35",
    }
    sound_pin_tokens = {
        "kLink2UartRxPin = 16", "kLink2UartTxPinReserved = 17",
        "kI2sBclkPin = 26", "kI2sLrclkPin = 25",
        "kI2sDataPin = 22", "kLedStripPin = 4",
    }
    ok &= check("control firmware pin tokens",
                all(token in control_text for token in control_pin_tokens),
                f"{len(control_pin_tokens)} exact assignments", checks)
    ok &= check("sound/light firmware pin tokens",
                all(token in sound_text for token in sound_pin_tokens),
                f"{len(sound_pin_tokens)} exact assignments", checks)

    # Generated output parity and field completeness.
    csv_rows: list[dict[str, str]] = []
    if CSV_PATH.is_file():
        with CSV_PATH.open(newline="", encoding="utf-8") as handle:
            csv_rows = list(csv.DictReader(handle))
    ok &= check("CSV exists", CSV_PATH.is_file(), str(CSV_PATH.relative_to(REPO)), checks)
    ok &= check("CSV exact generator parity", csv_rows == expected_dicts,
                f"{len(csv_rows)}/{len(expected_dicts)} rows", checks)
    ok &= check("wire IDs unique", len(expected_ids) == len(set(expected_ids)),
                f"{len(expected_ids)} unique IDs", checks)
    ok &= check("per-row fields complete",
                all(all(value not in ("", None) for value in asdict(w).values()) for w in expected),
                f"{len(expected)} complete physical cuts", checks)
    ok &= check("bundle build order",
                [w.bundle for w in expected] == sorted(
                    [w.bundle for w in expected], key=lambda bundle: data.BUNDLES.index(bundle)
                ),
                "on-PDB → on-cassette → pedestal-conduit → umbilical", checks)
    bundle_counts = Counter(w.bundle for w in expected)
    ok &= check("four-bundle coverage", set(bundle_counts) == set(data.BUNDLES),
                ", ".join(f"{name}={bundle_counts[name]}" for name in data.BUNDLES), checks)

    md_text = MD_PATH.read_text(encoding="utf-8") if MD_PATH.is_file() else ""
    ok &= check("Markdown exists", MD_PATH.is_file(), str(MD_PATH.relative_to(REPO)), checks)
    missing_md_ids = [wire_id for wire_id in expected_ids if wire_id not in md_text]
    ok &= check("Markdown wire-ID coverage", not missing_md_ids,
                "all IDs present" if not missing_md_ids else "missing " + ", ".join(missing_md_ids), checks)
    ok &= check("Markdown Joint-ID links",
                md_text.count("(Z_connection_joint_register.md)") >= len(expected),
                "every row has one or more clickable Joint Register links", checks)
    ok &= check("Markdown sources and totals",
                all(value in md_text for value in (
                    data.ELECTRICAL_SOURCE_SHA256,
                    data.CONTROL_PINMAP_SHA256,
                    data.SOUNDLIGHT_PINMAP_SHA256,
                    "## Wire totals for ordering",
                    "## Connector and contact totals",
                    "## Prioritized open ASM checks",
                )),
                "source hashes + wire/connector totals + ASM checks", checks)
    connector_families = [row[0] for row in data.CONNECTORS]
    connector_totals_ok = (
        len(connector_families) == len(set(connector_families))
        and all(row[2] > 0 and row[3] > 0 and row[4] >= 0 for row in data.CONNECTORS)
        and all(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |" in md_text
                for row in data.CONNECTORS)
    )
    ok &= check("connector-count manifest", connector_totals_ok,
                f"{sum(row[2] for row in data.CONNECTORS)} mating pairs/receptacles; "
                f"{sum(row[3] for row in data.CONNECTORS)} housings/halves; "
                f"{sum(row[4] for row in data.CONNECTORS)} loaded contacts/mapped pads", checks)

    # Arithmetic, no-false-precision and gauge rules.
    arithmetic_ok = all(
        w.cut_length_mm == w.routed_mm_est + w.service_slack_mm + w.strain_relief_mm
        for w in expected
    )
    ok &= check("cut arithmetic", arithmetic_ok, "route + slack + relief = cut for every row", checks)
    rounded_ok = all(
        value % 10 == 0
        for w in expected
        for value in (w.routed_mm_est, w.service_slack_mm, w.strain_relief_mm, w.cut_length_mm)
    )
    ok &= check("rounded estimate discipline", rounded_ok,
                "all route/slack/relief/cut values are 10 mm increments", checks)
    allowed_gauges = {"16 AWG", "20 AWG", "22 AWG", "24 AWG", "28 AWG", "50 Ω micro-coax"}
    ok &= check("gauge vocabulary", {w.gauge for w in expected} <= allowed_gauges,
                ", ".join(sorted({w.gauge for w in expected})), checks)
    ok &= check("battery-main gauge",
                all(w.gauge == "16 AWG" for w in expected if w.circuit == "BATTERY_MAIN"),
                "all battery-main cuts are 16 AWG", checks)
    ok &= check("RF no-field-cut rule",
                all(
                    w.gauge != "50 Ω micro-coax"
                    or (w.cut_to_fit_at_dry_fit.startswith("NO") and "FACTORY" in w.termination_b)
                    for w in expected
                ),
                "U.FL rows are factory-terminated 80 mm leads", checks)
    ok &= check("dry-fit flags",
                all(
                    w.cut_to_fit_at_dry_fit == "YES" or w.gauge == "50 Ω micro-coax"
                    for w in expected
                ),
                "all field wire waits for dry-fit; coax is buy-to-length", checks)

    # Electrical pin authority: exact required pairs and no extra ESP GPIO numbers.
    endpoint_pairs = {(w.endpoint_a, w.endpoint_b) for w in expected}
    required_pairs = {
        ("RP1.RP1_TX", "ESP32#1.GPIO16"),
        ("ESP32#1.GPIO17", "RP1.RP1_RX"),
        ("ESP32#1.GPIO25", "ESP32#2.GPIO16"),
        ("ESP32#2.GPIO17", "ESP32#1.GPIO26"),
        ("PDB.27k/10k_DIV_TAP", "ESP32#1.GPIO34"),
        ("CAS-DOCK.HALL_SOURCE.SIG", "ESP32#1.GPIO35"),
        ("ESP32#1.GPIO13", "CAS-DOCK.STEERING_SOURCE.SIG"),
        ("ESP32#1.GPIO14", "CAS-DOCK.ESC_SOURCE.SIG"),
        ("ESP32#1.GPIO18", "CAS-DOCK.DRS_SOURCE.SIG"),
        ("ESP32#1.GPIO19", "CAS-DOCK.PAN_SOURCE.SIG"),
        ("ESP32#1.GPIO23", "CAS-DOCK.TILT_SOURCE.SIG"),
        ("ESP32#2.GPIO26", "MAX98357A.BCLK"),
        ("ESP32#2.GPIO25", "MAX98357A.LRCLK"),
        ("ESP32#2.GPIO22", "MAX98357A.DIN"),
        ("ESP32#2.GPIO4", "CAS-DOCK.LED_SOURCE.DATA"),
        ("VID-CAM.D+", "CAS-DOCK.USB4_LOAD.D+"),
        ("VID-CAM.D−", "CAS-DOCK.USB4_LOAD.D−"),
        ("CAS-DOCK.USB4_SOURCE.D+", "BL-M8812EU2.DP"),
        ("CAS-DOCK.USB4_SOURCE.D−", "BL-M8812EU2.DM"),
        ("A3144.OUT", "CAS-DOCK.HALL_LOAD.SIG"),
    }
    missing_pairs = sorted(required_pairs - endpoint_pairs)
    ok &= check("authoritative endpoint-pair coverage", not missing_pairs,
                f"{len(required_pairs)} exact pairs" if not missing_pairs else str(missing_pairs), checks)
    gpio_matches: set[tuple[int, int]] = set()
    for wire in expected:
        for endpoint in (wire.endpoint_a, wire.endpoint_b):
            for board, gpio in re.findall(r"ESP32#([12])\.GPIO(\d+)", endpoint):
                gpio_matches.add((int(board), int(gpio)))
    allowed_gpio = {
        (1, 13), (1, 14), (1, 16), (1, 17), (1, 18), (1, 19),
        (1, 23), (1, 25), (1, 26), (1, 34), (1, 35),
        (2, 4), (2, 16), (2, 17), (2, 22), (2, 25), (2, 26),
    }
    ok &= check("no invented GPIO", gpio_matches <= allowed_gpio,
                ", ".join(f"ESP32#{board}.GPIO{gpio}" for board, gpio in sorted(gpio_matches)), checks)

    # Exact per-circuit physical segmentation.  Remote power fan-out is a
    # separate on-cassette circuit and is intentionally counted separately.
    expected_circuit_counts = {
        "BATTERY_MAIN": 4, "USB_C_CHARGE": 5, "PACK_BALANCE": 6,
        "RAIL_A_DOCK_FEED": 2, "RAIL_B_DOCK_FEED": 2, "BATTERY_ADC": 1,
        "ESP32_1_POWER": 2, "ESP32_2_POWER": 2, "WIFI_POWER": 2,
        "CRSF": 4, "LINK2": 3, "I2S_AUDIO": 5,
        "STEERING": 4, "ESC_SIGNAL": 4, "DRS": 4, "PAN": 4, "TILT": 4,
        "LED": 4, "HALL": 4, "CAMERA_USB": 6, "BLOWER": 2, "SPEAKER": 4,
        "CAMERA_USB_DOCK_POWER": 2, "LED_DOCK_POWER": 2, "HALL_DOCK_POWER": 2,
        "STEERING_DOCK_POWER": 2, "DRS_DOCK_POWER": 2, "PAN_DOCK_POWER": 2,
        "TILT_DOCK_POWER": 2, "BLOWER_DOCK_POWER": 2, "RF_J0": 1, "RF_J1": 1,
    }
    circuit_counts = Counter(w.circuit for w in expected)
    ok &= check("per-circuit cut coverage", circuit_counts == expected_circuit_counts,
                f"{sum(circuit_counts.values())} physical pieces across {len(circuit_counts)} circuits", checks)

    remote_circuits = ("STEERING", "ESC_SIGNAL", "DRS", "PAN", "TILT", "LED", "HALL", "CAMERA_USB", "BLOWER", "SPEAKER")
    segmentation_ok = True
    for circuit in remote_circuits:
        circuit_rows = [
            w for w in expected
            if w.circuit in {circuit, f"{circuit}_DOCK_POWER"}
        ]
        has_source = any(
            "CAS-DOCK." in endpoint and "_SOURCE." in endpoint
            for w in circuit_rows
            for endpoint in (w.endpoint_a, w.endpoint_b)
        )
        has_load = any(
            "CAS-DOCK." in endpoint and "_LOAD." in endpoint
            for w in circuit_rows
            for endpoint in (w.endpoint_a, w.endpoint_b)
        )
        segmentation_ok &= has_source and has_load
    ok &= check("ganged-dock two-sided segmentation", segmentation_ok,
                f"{len(remote_circuits)} remote circuits have SOURCE and LOAD cuts", checks)

    # Deferral and safety policy.
    defer_circuits = {
        "BATTERY_MAIN", "PACK_BALANCE", "USB_C_CHARGE",
        "DRS", "DRS_DOCK_POWER", "PAN", "PAN_DOCK_POWER", "TILT", "TILT_DOCK_POWER",
    }
    deferral_ok = all(
        w.disposition.startswith("DEFER")
        for w in expected
        if w.circuit in defer_circuits
    )
    ok &= check("in-transit DEFER discipline", deferral_ok,
                f"{sum(w.disposition.startswith('DEFER') for w in expected)} cuts deferred", checks)
    optional_rows = [w for w in expected if w.ordering_class == "OPTIONAL"]
    ok &= check("optional ACK not populated",
                len(optional_rows) == 1
                and optional_rows[0].endpoint_a == "ESP32#2.GPIO17"
                and optional_rows[0].endpoint_b == "ESP32#1.GPIO26"
                and "do not populate" in optional_rows[0].disposition,
                "one GPIO17(#2)→GPIO26(#1) reserve", checks)
    esc_signals = {w.signal for w in expected if w.circuit == "ESC_SIGNAL"}
    ok &= check("ESC BEC isolation", esc_signals == {"sig", "GND"}
                and all("+5" not in w.endpoint_a + w.endpoint_b for w in expected if w.circuit == "ESC_SIGNAL"),
                "signal + GND only; no +5 conductor", checks)
    source_shrouding_ok = (
        any("shrouded/socket source half" in w.connector_b for w in expected if w.circuit == "RAIL_A_DOCK_FEED")
        and any("shrouded/socket source half" in w.connector_b for w in expected if w.circuit == "RAIL_B_DOCK_FEED")
        and any("shrouded/socket source half" in w.connector_b for w in expected if w.circuit == "BATTERY_MAIN" and w.bundle == "umbilical")
        and "source-side shrouding" in md_text
    )
    ok &= check("source-side power shrouding", source_shrouding_ok,
                "XT60 + both dock XT30 source halves explicitly shrouded/socketed", checks)

    # All Joint IDs must resolve in the generated physical Joint Register.
    joint_path = ARCH / "Z_connection_joint_register.csv"
    with joint_path.open(newline="", encoding="utf-8") as handle:
        known_joint_ids = {row["joint_id"] for row in csv.DictReader(handle)}
    used_joint_ids = {
        joint_id.strip()
        for wire in expected
        for joint_id in wire.joint_ids.split(";")
        if joint_id.strip()
    }
    missing_joints = sorted(used_joint_ids - known_joint_ids)
    ok &= check("Joint-ID cross-links resolve", not missing_joints,
                f"{len(used_joint_ids)} unique Joint IDs" if not missing_joints else str(missing_joints), checks)

    # Known electrical-map omissions must stay explicit instead of being invented.
    ok &= check("traction-power omission disclosed",
                "does not state the PDB→ESC battery connector" in md_text
                and not any("MOTOR_PHASE" in w.circuit or "ESC_POWER" in w.circuit for w in expected),
                "PDB→ESC and ESC→motor await authoritative map update", checks)
    ok &= check("blower conduit conflict disclosed",
                "firm conduit bundle does not currently include it" in md_text
                and all("conduit inclusion is OPEN" in w.route for w in expected if w.circuit == "BLOWER"),
                "blower route remains HOLD, not silently added to firm conduit", checks)

    lines = [
        "# p0_d36 — wire-schedule validation",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    lines.extend(f"| {name} | **{result}** | {detail} |" for name, result, detail in checks)
    lines += [
        "",
        f"**Verdict: {'PASS' if ok else 'FAIL'} — "
        f"{sum(result == 'PASS' for _, result, _ in checks)}/{len(checks)} checks passed.**",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(lines[-2])
    print("WROTE", OUT.relative_to(REPO))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
