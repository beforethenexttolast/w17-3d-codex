#!/usr/bin/env python3
"""Automated validation for W17 P0 diagnostic CAD outputs."""
from __future__ import annotations

import contextlib
import hashlib
import io
import math
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from generate import (BUILD_PLATES, DEFAULT_OUTPUT, PARAMETERS, RENDER_TARGETS, REPO_ROOT,
                      generate, pack_plate)
from lib.meshkit import Mesh, Parameters, read_binary_stl
from parts import Part, build_parts


REPORT = REPO_ROOT / "10_assembly_architecture/cad/reports/generated_part_validation.md"
TASK_WHITELIST = {"CAD-01", "CAD-02", "CAD-04", "CAD-06", "CAD-08"}
BLOCKED_TOKENS = ("cad03", "cad05", "cad07", "camera", "gimbal", "duct",
                  "ps10", "ps11", "ps14", "ps17", "production")


@dataclass
class MeshAudit:
    triangles: int
    bbox: tuple[tuple[float, float, float], tuple[float, float, float]]
    size: tuple[float, float, float]
    min_area: float
    signed_volume: float
    closed_shells: int
    boundary_edges: int
    nonmanifold_edges: int
    orientation_mismatches: int


def _q(v: tuple[float, float, float]) -> tuple[int, int, int]:
    return tuple(round(coord * 100000) for coord in v)


def audit_mesh(mesh: Mesh) -> MeshAudit:
    if not mesh.triangles:
        raise AssertionError("empty mesh")
    edge_count: Counter[tuple[tuple[int, int, int], tuple[int, int, int]]] = Counter()
    directed: Counter[tuple[tuple[int, int, int], tuple[int, int, int]]] = Counter()
    adjacency: dict[tuple[int, int, int], set[tuple[int, int, int]]] = defaultdict(set)
    min_area = float("inf")
    volume = 0.0
    for a, b, c in mesh.triangles:
        ux, uy, uz = (b[i] - a[i] for i in range(3))
        vx, vy, vz = (c[i] - a[i] for i in range(3))
        cross = (uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)
        area = math.sqrt(sum(value * value for value in cross)) / 2
        min_area = min(min_area, area)
        volume += (a[0] * (b[1] * c[2] - b[2] * c[1])
                   - a[1] * (b[0] * c[2] - b[2] * c[0])
                   + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6
        vertices = [_q(a), _q(b), _q(c)]
        for u, v in ((vertices[0], vertices[1]), (vertices[1], vertices[2]),
                     (vertices[2], vertices[0])):
            key = tuple(sorted((u, v)))
            edge_count[key] += 1
            directed[(u, v)] += 1
            adjacency[u].add(v)
            adjacency[v].add(u)
    if min_area <= 1e-8:
        raise AssertionError(f"degenerate triangle area {min_area}")
    boundary = sum(count == 1 for count in edge_count.values())
    nonmanifold = sum(count > 2 for count in edge_count.values())
    orientation = 0
    for edge, count in edge_count.items():
        u, v = edge
        # Separate closed primitives may intentionally share a coincident edge.
        # A balanced even count remains closed/oriented but is not a strict
        # single-manifold edge; it is reported separately as nonmanifold.
        if count % 2 or directed[(u, v)] != count / 2 or directed[(v, u)] != count / 2:
            orientation += 1
    unseen = set(adjacency)
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            node = stack.pop()
            neighbors = adjacency[node] & unseen
            unseen.difference_update(neighbors)
            stack.extend(neighbors)
    lo, hi = mesh.bbox()
    size = tuple(hi[i] - lo[i] for i in range(3))
    return MeshAudit(len(mesh.triangles), (lo, hi), size, min_area, volume,
                     components, boundary, nonmanifold, orientation)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare_size(actual: tuple[float, float, float], expected: tuple[float, float, float],
                 tolerance: float, label: str) -> None:
    for axis, (got, wanted) in enumerate(zip(actual, expected)):
        if abs(got - wanted) > tolerance:
            raise AssertionError(
                f"{label} bbox axis {axis}: {got:.3f} vs expected {wanted:.3f} +/- {tolerance}")


def compare_meshes(actual: Mesh, expected: Mesh, tolerance: float, label: str) -> None:
    """Require a grouped STL to contain exactly its declared, placed source meshes."""
    if len(actual.triangles) != len(expected.triangles):
        raise AssertionError(
            f"{label} triangle membership: {len(actual.triangles)} vs {len(expected.triangles)}")
    for index, (got, wanted) in enumerate(zip(actual.triangles, expected.triangles)):
        if any(abs(got[corner][axis] - wanted[corner][axis]) > tolerance
               for corner in range(3) for axis in range(3)):
            raise AssertionError(f"{label} triangle membership differs at triangle {index}")


def plate_rectangles(entries: tuple[tuple[str, int], ...], parts: dict[str, Part],
                     p: Parameters) -> list[tuple[str, tuple[float, float, float, float]]]:
    """Independent XY rectangle audit for the deterministic row packer."""
    plate = p.f("SH-BUILD-PLATE-SIZE")
    gap = p.f("SH-BUILD-PLATE-GAP")
    cursor_x = gap
    cursor_y = gap
    row_depth = 0.0
    rectangles: list[tuple[str, tuple[float, float, float, float]]] = []
    for filename, count in entries:
        for copy_index in range(count):
            lo, hi = parts[filename].mesh.bbox()
            sx, sy = hi[0] - lo[0], hi[1] - lo[1]
            if cursor_x + sx + gap > plate:
                cursor_x = gap
                cursor_y += row_depth + gap
                row_depth = 0.0
            if cursor_y + sy + gap > plate:
                raise AssertionError(f"independent plate overflow while placing {filename}")
            rectangles.append((f"{filename}#{copy_index + 1}",
                               (cursor_x, cursor_y, cursor_x + sx, cursor_y + sy)))
            cursor_x += sx + gap
            row_depth = max(row_depth, sy)
    return rectangles


def validate() -> str:
    if Path.cwd().resolve() != REPO_ROOT:
        raise AssertionError(f"run from repository root {REPO_ROOT}")
    p = Parameters(PARAMETERS)
    parts = build_parts(p)
    output_dir = DEFAULT_OUTPUT / "stl"
    expected_files = set(parts) | {name for name, _ in BUILD_PLATES}
    actual_files = {path.name for path in output_dir.glob("*.stl")}
    if actual_files != expected_files:
        raise AssertionError(
            f"stale/missing output set: extra={sorted(actual_files - expected_files)} "
            f"missing={sorted(expected_files - actual_files)}")
    render_dir = DEFAULT_OUTPUT / "renders"
    expected_renders = {filename for filename, _, _ in RENDER_TARGETS}
    actual_renders = {path.name for path in render_dir.glob("*.png")}
    if actual_renders != expected_renders:
        raise AssertionError(
            f"stale/missing render set: extra={sorted(actual_renders - expected_renders)} "
            f"missing={sorted(expected_renders - actual_renders)}")

    # Manifest discipline and explicit policy scope.
    for row in p.rows.values():
        for column in ("value", "units", "status", "source_report_table", "uncertainty",
                       "physical_dependency", "selected_diagnostic_variant"):
            if not row[column].strip():
                raise AssertionError(f"parameter {row['parameter_id']} has empty {column}")
    for part in parts.values():
        if part.cad_task not in TASK_WHITELIST or not part.diagnostic_only:
            raise AssertionError(f"unauthorized task/output: {part.filename}")
        lowered = part.filename.lower()
        if any(token in lowered for token in BLOCKED_TOKENS):
            raise AssertionError(f"blocked geometry token in {part.filename}")
        for parameter_id in part.parameter_ids:
            if parameter_id not in p.rows:
                raise AssertionError(f"{part.filename} uses undeclared {parameter_id}")
        if part.cad_task == "CAD-01":
            if not any("component ID" == feature for feature in part.features):
                raise AssertionError(f"{part.filename} lacks component ID feature")
            if not any("arrow" in feature for feature in part.features):
                raise AssertionError(f"{part.filename} lacks orientation/direction arrow")

    audits: dict[str, MeshAudit] = {}
    donor_hashes = {sha256(path) for path in REPO_ROOT.glob("02_ready_to_slice/**/*.stl")}
    for filename, part in sorted(parts.items()):
        path = output_dir / filename
        header = path.read_bytes()[:80]
        if b"MM" not in header:
            raise AssertionError(f"{filename} does not declare MM in its STL header")
        if sha256(path) in donor_hashes:
            raise AssertionError(f"{filename} is a copied donor STL")
        mesh = read_binary_stl(path)
        audit = audit_mesh(mesh)
        compare_size(audit.size, part.expected_size, part.bbox_tolerance, filename)
        if abs(audit.bbox[0][2]) > 0.01:
            raise AssertionError(f"{filename} is not bed-oriented at Z=0")
        if audit.boundary_edges or audit.orientation_mismatches:
            raise AssertionError(
                f"{filename} topology boundary={audit.boundary_edges} "
                f"nonmanifold={audit.nonmanifold_edges} orientation={audit.orientation_mismatches}")
        audits[filename] = audit

    plate_audits: dict[str, MeshAudit] = {}
    plate_limit = p.f("SH-BUILD-PLATE-SIZE")
    for filename, entries in BUILD_PLATES:
        expected_mesh = pack_plate(entries, parts, p)
        disk_mesh = read_binary_stl(output_dir / filename)
        compare_meshes(disk_mesh, expected_mesh, 0.0001, filename)
        expected_triangles = sum(count * len(parts[source].mesh.triangles)
                                 for source, count in entries)
        if len(disk_mesh.triangles) != expected_triangles:
            raise AssertionError(f"{filename} does not contain its declared part/count set")
        rectangles = plate_rectangles(entries, parts, p)
        for index, (name_a, a) in enumerate(rectangles):
            for name_b, b in rectangles[index + 1:]:
                overlap_x = min(a[2], b[2]) - max(a[0], b[0])
                overlap_y = min(a[3], b[3]) - max(a[1], b[1])
                if overlap_x > 1e-6 and overlap_y > 1e-6:
                    raise AssertionError(
                        f"{filename} XY overlap: {name_a} vs {name_b} "
                        f"({overlap_x:.3f} x {overlap_y:.3f} mm)")
        audit = audit_mesh(disk_mesh)
        compare_size(audit.size, audit_mesh(expected_mesh).size, 0.02, filename)
        if audit.size[0] > plate_limit or audit.size[1] > plate_limit:
            raise AssertionError(f"{filename} exceeds {plate_limit} mm plate")
        if abs(audit.bbox[0][2]) > 0.01:
            raise AssertionError(f"{filename} does not sit at Z=0")
        if audit.boundary_edges or audit.orientation_mismatches:
            raise AssertionError(f"{filename} has an open or inconsistently oriented shell")
        plate_audits[filename] = audit

    # D-26 policy checks in DAT-F coordinates.
    d26_min = p.f("SH-D26-Z-MIN")
    for filename in ("cad02_ps01_battery_tray.stl", "cad04_ps03_ubec_shelf.stl",
                     "cad08_ps15_junction_support.stl", "cad06_ps05_post_h20.stl",
                     "cad06_ps05_post_h26.stl", "cad06_ps05_post_h32.stl"):
        if audits[filename].bbox[1][2] >= d26_min:
            raise AssertionError(f"{filename} enters D-26 at Z={d26_min}")

    # Rebuild twice in isolated temp folders and require byte-for-byte identity.
    with tempfile.TemporaryDirectory(prefix="w17_p0cad_determinism_") as temp:
        root = Path(temp)
        first, second = root / "a", root / "b"
        with contextlib.redirect_stdout(io.StringIO()):
            generate(first, with_renders=False)
            generate(second, with_renders=False)
        hashes_a = {path.name: sha256(path) for path in (first / "stl").glob("*.stl")}
        hashes_b = {path.name: sha256(path) for path in (second / "stl").glob("*.stl")}
        if hashes_a != hashes_b or set(hashes_a) != expected_files:
            raise AssertionError("deterministic regeneration mismatch")

    lines = [
        "# W17 diagnostic CAD — automated generated-part validation",
        "",
        "Generated by `python3 10_assembly_architecture/cad/sources/validate.py` from the repository root.",
        "",
        "Status: **PASS**. Scope is diagnostic CAD only: CAD-01, CAD-02, CAD-04, CAD-06 and CAD-08.",
        "",
        "## Automated checks",
        "",
        f"- Authoritative parameter rows: **{len(p.rows)}**; all required traceability/status fields populated.",
        f"- Individual diagnostic STLs: **{len(parts)}**; build-plate STLs: **{len(BUILD_PLATES)}**.",
        f"- Deterministic visual-review renders: **{len(RENDER_TARGETS)}**; exact render set present.",
        "- Binary STL headers declare millimetres; every mesh is non-empty and bed-oriented at Z=0.",
        "- Bounding boxes reproduce the parameter-derived expected envelope within each part's diagnostic tolerance.",
        "- Every triangle has non-zero area; no boundary edge or edge-orientation mismatch was found.",
        "- Strict >2-incidence edge counts are reported per STL. They occur where diagnostic primitives/labels "
        "share geometry; this local tool proves closed, consistently oriented shells but does not Boolean-union them.",
        "- Generated SHA-256 values do not equal any donor STL under `02_ready_to_slice/`.",
        "- Output filenames and task metadata contain no blocked CAD/PS/production geometry.",
        f"- CAD-02/CAD-04/CAD-06/CAD-08 geometry stays below D-26's Z={d26_min:g} mm lower boundary.",
        f"- All six grouped layouts contain the exact declared part/count membership, have no XY bounding-box "
        f"overlap and fit the confirmed {plate_limit:g} x {plate_limit:g} mm build plate.",
        "- Two isolated regenerations produced byte-identical STL sets; no stale file survived the exact-set check.",
        "",
        "## Individual STL results",
        "",
        "| Output | Task / ID | Triangles | Bounding box mm | Closed shells | Boundary / nonmanifold / orientation edges | SHA-256 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for filename, part in sorted(parts.items()):
        audit = audits[filename]
        size = " x ".join(f"{value:.2f}" for value in audit.size)
        lines.append(
            f"| `{filename}` | {part.cad_task} / {part.support_id} | {audit.triangles} | {size} | "
            f"{audit.closed_shells} | {audit.boundary_edges} / {audit.nonmanifold_edges} / "
            f"{audit.orientation_mismatches} | `{sha256(output_dir / filename)[:16]}...` |")
    lines.extend([
        "",
        "## Build-plate group results",
        "",
        "| Output | Triangles | Bounding box mm | Closed shells | Topology |",
        "|---|---:|---:|---:|---|",
    ])
    for filename, _ in BUILD_PLATES:
        audit = plate_audits[filename]
        size = " x ".join(f"{value:.2f}" for value in audit.size)
        lines.append(f"| `{filename}` | {audit.triangles} | {size} | {audit.closed_shells} | "
                     f"closed/oriented; strict >2 edges={audit.nonmanifold_edges} |")
    lines.extend([
        "",
        "## Feature and print-orientation audit",
        "",
        "| Output | Represented diagnostic features | Print orientation | Assembly reference |",
        "|---|---|---|---|",
    ])
    for filename, part in sorted(parts.items()):
        lines.append(f"| `{filename}` | {'; '.join(part.features)} | {part.print_orientation} | {part.assembly_reference} |")
    lines.extend([
        "",
        "## Manifold-check limitation",
        "",
        "The dependency-free check proves closed, consistently oriented primitive shells by edge incidence. "
        "A strict global 2-manifold claim is not made: diagnostic labels and intersecting/touching primitives remain "
        "separate or coincident closed shells because no Boolean mesh engine is installed. The table exposes every "
        ">2-incidence edge count; self-intersection/Boolean-union analysis must be confirmed in Bambu Studio before printing.",
        "",
        "## Visual inspection inputs",
        "",
        "The generator also creates the exact 19-file ignored PNG set: grouped CAD-01 views, close-ups for every "
        "CAD-01 dummy, and views for every support family. Human inspection results are recorded in "
        "`diagnostic_cad_manifest.md`; renders are not "
        "a substitute for slicer preview or the P1 physical dry-fit.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    try:
        report = validate()
    except Exception as exc:
        print(f"VALIDATION: FAIL — {exc}", file=sys.stderr)
        return 1
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
