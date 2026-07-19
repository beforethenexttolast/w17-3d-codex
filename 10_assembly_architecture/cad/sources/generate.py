#!/usr/bin/env python3
"""Generate only the P0-authorized W17 diagnostic STL set.

Run from the repository root.  Donor STLs are never read or copied.  Existing
generated STL files in the fixed diagnostic output folder are removed first so
the output set cannot retain stale parts.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from lib.meshkit import Mesh, Parameters, render_png, write_binary_stl
from parts import Part, build_parts


SOURCE = Path(__file__).resolve()
REPO_ROOT = SOURCE.parents[3]
PARAMETERS = REPO_ROOT / "10_assembly_architecture/cad/parameters/cad_parameters.csv"
DEFAULT_OUTPUT = REPO_ROOT / "10_assembly_architecture/cad/generated"


BUILD_PLATES: tuple[tuple[str, tuple[tuple[str, int], ...]], ...] = (
    ("plate_01_core_power_dummies.stl", (
        ("cad01_pwr_bat_max.stl", 1), ("cad01_drv_esc.stl", 1),
        ("cad01_pwr_ubec_a.stl", 1), ("cad01_pwr_ubec_b.stl", 1))),
    ("plate_02_controller_communication_dummies.stl", (
        ("cad01_ctl_e1.stl", 1), ("cad01_ctl_e2.stl", 1),
        ("cad01_vid_wifi_max.stl", 1), ("cad01_aud_amp.stl", 1))),
    ("plate_03_connector_bank_access_dummies.stl", (
        ("cad01_srv_steer.stl", 1), ("cad01_ps15_connector_bank.stl", 1))),
    ("plate_04_battery_tray_test.stl", (
        ("cad02_ps01_battery_tray.stl", 1), ("cad02_ps01_plate_clamp_foot.stl", 2))),
    ("plate_05_ubec_shelf_junction_support.stl", (
        ("cad04_ps03_ubec_shelf.stl", 1), ("cad04_ps03_plate_clamp_foot.stl", 2),
        ("cad08_ps15_junction_support.stl", 1), ("cad08_ps15_dn_open_blanks.stl", 1),
        ("cad08_ps15_plate_clamp_foot.stl", 2))),
    ("plate_06_post_height_set.stl", (
        ("cad06_ps05_post_h20.stl", 1), ("cad06_ps05_post_h26.stl", 1),
        ("cad06_ps05_post_h32.stl", 1))),
)

RENDER_TARGETS: tuple[tuple[str, str, str], ...] = (
    ("render_cad01_core_power.png", "plate", "plate_01_core_power_dummies.stl"),
    ("render_cad01_controllers.png", "plate", "plate_02_controller_communication_dummies.stl"),
    ("render_cad01_access.png", "plate", "plate_03_connector_bank_access_dummies.stl"),
    ("render_cad01_battery.png", "part", "cad01_pwr_bat_max.stl"),
    ("render_cad01_esc.png", "part", "cad01_drv_esc.stl"),
    ("render_cad01_ubec_a.png", "part", "cad01_pwr_ubec_a.stl"),
    ("render_cad01_ubec_b.png", "part", "cad01_pwr_ubec_b.stl"),
    ("render_cad01_ctl_e1.png", "part", "cad01_ctl_e1.stl"),
    ("render_cad01_ctl_e2.png", "part", "cad01_ctl_e2.stl"),
    ("render_cad01_wifi.png", "part", "cad01_vid_wifi_max.stl"),
    ("render_cad01_amp.png", "part", "cad01_aud_amp.stl"),
    ("render_cad01_servo.png", "part", "cad01_srv_steer.stl"),
    ("render_cad01_connector_bank.png", "part", "cad01_ps15_connector_bank.stl"),
    ("render_cad02_battery_tray.png", "part", "cad02_ps01_battery_tray.stl"),
    ("render_cad02_plate_clamp.png", "part", "cad02_ps01_plate_clamp_foot.stl"),
    ("render_cad04_ubec_shelf.png", "part", "cad04_ps03_ubec_shelf.stl"),
    ("render_cad06_post_family.png", "plate", "plate_06_post_height_set.stl"),
    ("render_cad08_junction_support.png", "part", "cad08_ps15_junction_support.stl"),
    ("render_cad08_decision_blanks.png", "part", "cad08_ps15_dn_open_blanks.stl"),
)

TOP_DOWN_RENDERS = {
    "render_cad01_battery.png", "render_cad01_esc.png",
    "render_cad01_ubec_a.png", "render_cad01_ubec_b.png",
    "render_cad01_ctl_e1.png", "render_cad01_ctl_e2.png",
    "render_cad01_wifi.png", "render_cad01_amp.png",
    "render_cad01_servo.png", "render_cad01_connector_bank.png",
    "render_cad08_decision_blanks.png",
}


def _sizes(mesh: Mesh) -> tuple[float, float, float]:
    lo, hi = mesh.bbox()
    return tuple(hi[i] - lo[i] for i in range(3))


def pack_plate(entries: tuple[tuple[str, int], ...], parts: dict[str, Part],
               p: Parameters) -> Mesh:
    """Deterministic row packer; no rotations hide a source part's print orientation."""
    plate = p.f("SH-BUILD-PLATE-SIZE")
    gap = p.f("SH-BUILD-PLATE-GAP")
    result = Mesh()
    cursor_x = gap
    cursor_y = gap
    row_depth = 0.0
    for filename, count in entries:
        for _ in range(count):
            source = parts[filename].mesh
            lo, hi = source.bbox()
            sx, sy, _ = (hi[i] - lo[i] for i in range(3))
            if cursor_x + sx + gap > plate:
                cursor_x = gap
                cursor_y += row_depth + gap
                row_depth = 0.0
            if cursor_y + sy + gap > plate:
                raise ValueError(f"build plate overflow while placing {filename}")
            result.add(source.moved(cursor_x - lo[0], cursor_y - lo[1], -lo[2]))
            cursor_x += sx + gap
            row_depth = max(row_depth, sy)
    return result


def generate(output_root: Path, with_renders: bool = True) -> tuple[dict[str, Part], dict[str, Mesh]]:
    p = Parameters(PARAMETERS)
    parts = build_parts(p)
    stl_dir = output_root / "stl"
    render_dir = output_root / "renders"
    stl_dir.mkdir(parents=True, exist_ok=True)
    render_dir.mkdir(parents=True, exist_ok=True)

    # Exact fixed folder and exact extension: this is a stale-output cleanup only.
    for stale in sorted(stl_dir.glob("*.stl")):
        stale.unlink()

    for filename in sorted(parts):
        part = parts[filename]
        write_binary_stl(stl_dir / filename, part.mesh, f"{part.cad_task} {part.support_id}")

    plates: dict[str, Mesh] = {}
    for filename, entries in BUILD_PLATES:
        plate_mesh = pack_plate(entries, parts, p)
        plates[filename] = plate_mesh
        write_binary_stl(stl_dir / filename, plate_mesh, "BUILD PLATE DIAGNOSTIC")

    if with_renders:
        representative = {
            filename: (parts[source].mesh if source_kind == "part" else plates[source])
            for filename, source_kind, source in RENDER_TARGETS
        }
        for stale in sorted(render_dir.glob("*.png")):
            stale.unlink()
        for filename, mesh in representative.items():
            render_png(render_dir / filename, mesh, int(p.f("RENDER-WIDTH")),
                       int(p.f("RENDER-HEIGHT")),
                       (0.12, -0.12, 0.985) if filename in TOP_DOWN_RENDERS
                       else (0.64, -0.60, 0.48))

    for path in sorted(stl_dir.glob("*.stl")):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        # Read from the in-memory source so generation itself has no STL dependency.
        source_mesh = parts[path.name].mesh if path.name in parts else plates[path.name]
        sx, sy, sz = _sizes(source_mesh)
        print(f"WROTE {path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path} "
              f"bbox={sx:.2f}x{sy:.2f}x{sz:.2f} mm sha256={digest}")
    return parts, plates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--no-renders", action="store_true")
    args = parser.parse_args()
    if Path.cwd().resolve() != REPO_ROOT:
        print(f"FATAL: run from repository root {REPO_ROOT}", file=sys.stderr)
        return 2
    generate(args.output_root.resolve(), not args.no_renders)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
