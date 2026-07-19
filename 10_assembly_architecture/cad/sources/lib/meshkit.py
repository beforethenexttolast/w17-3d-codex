#!/usr/bin/env python3
"""Dependency-free parametric mesh helpers for W17 diagnostic CAD.

All coordinates are millimetres.  The library creates deterministic closed
triangle shells, writes binary STL, and can rasterize a local inspection PNG.
It deliberately provides only simple diagnostic primitives; it is not a
production solid modeller and never imports donor STL geometry.
"""
from __future__ import annotations

import csv
import math
import os
import struct
import zlib
from dataclasses import dataclass, field
from pathlib import Path


Vec3 = tuple[float, float, float]
Tri = tuple[Vec3, Vec3, Vec3]


@dataclass
class Mesh:
    triangles: list[Tri] = field(default_factory=list)

    def add(self, other: "Mesh") -> "Mesh":
        self.triangles.extend(other.triangles)
        return self

    def moved(self, dx: float, dy: float, dz: float) -> "Mesh":
        return Mesh([
            (tuple(a[i] + (dx, dy, dz)[i] for i in range(3)),
             tuple(b[i] + (dx, dy, dz)[i] for i in range(3)),
             tuple(c[i] + (dx, dy, dz)[i] for i in range(3)))
            for a, b, c in self.triangles
        ])

    def bbox(self) -> tuple[Vec3, Vec3]:
        if not self.triangles:
            raise ValueError("empty mesh has no bounding box")
        vertices = [v for tri in self.triangles for v in tri]
        return (tuple(min(v[i] for v in vertices) for i in range(3)),
                tuple(max(v[i] for v in vertices) for i in range(3)))


class Parameters:
    """Strict loader for the authoritative CAD parameter CSV."""

    REQUIRED_COLUMNS = {
        "parameter_id", "related_cad_task", "related_part", "value", "units",
        "status", "source_report_table", "uncertainty", "physical_dependency",
        "selected_diagnostic_variant",
    }

    def __init__(self, path: Path):
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            missing = self.REQUIRED_COLUMNS - set(reader.fieldnames or ())
            if missing:
                raise ValueError(f"parameter manifest missing columns: {sorted(missing)}")
            rows = list(reader)
        self.rows: dict[str, dict[str, str]] = {}
        for row in rows:
            pid = row["parameter_id"]
            if pid in self.rows:
                raise ValueError(f"duplicate parameter ID: {pid}")
            if not row["status"] or not row["source_report_table"]:
                raise ValueError(f"untraceable parameter row: {pid}")
            self.rows[pid] = row

    def f(self, parameter_id: str) -> float:
        try:
            return float(self.rows[parameter_id]["value"])
        except KeyError as exc:
            raise KeyError(f"undeclared CAD parameter: {parameter_id}") from exc

    def s(self, parameter_id: str) -> str:
        try:
            return self.rows[parameter_id]["value"]
        except KeyError as exc:
            raise KeyError(f"undeclared CAD parameter: {parameter_id}") from exc


def _quad(a: Vec3, b: Vec3, c: Vec3, d: Vec3) -> list[Tri]:
    return [(a, b, c), (a, c, d)]


def box(x: float, y: float, z: float, sx: float, sy: float, sz: float) -> Mesh:
    """Closed axis-aligned box with outward triangle winding."""
    if min(sx, sy, sz) <= 0:
        raise ValueError("box dimensions must be positive")
    x1, y1, z1 = x + sx, y + sy, z + sz
    v = [(x, y, z), (x1, y, z), (x1, y1, z), (x, y1, z),
         (x, y, z1), (x1, y, z1), (x1, y1, z1), (x, y1, z1)]
    faces = [
        (0, 3, 2, 1),  # bottom
        (4, 5, 6, 7),  # top
        (0, 1, 5, 4),  # -Y
        (1, 2, 6, 5),  # +X
        (2, 3, 7, 6),  # +Y
        (3, 0, 4, 7),  # -X
    ]
    return Mesh([tri for a, b, c, d in faces for tri in _quad(v[a], v[b], v[c], v[d])])


def frame_rect(x: float, y: float, z: float, sx: float, sy: float, sz: float,
               rail: float) -> Mesh:
    """Four closed rails forming a rectangular frame in the XY plane."""
    if rail * 2 >= min(sx, sy):
        raise ValueError("frame rail too large")
    mesh = Mesh()
    mesh.add(box(x, y, z, sx, rail, sz))
    mesh.add(box(x, y + sy - rail, z, sx, rail, sz))
    mesh.add(box(x, y + rail, z, rail, sy - 2 * rail, sz))
    mesh.add(box(x + sx - rail, y + rail, z, rail, sy - 2 * rail, sz))
    return mesh


def open_shell(x: float, y: float, z: float, sx: float, sy: float, sz: float,
               wall: float, base: float | None = None) -> Mesh:
    """Open-top lightweight shell: bottom plus four vertical walls."""
    base = wall if base is None else base
    if wall * 2 >= min(sx, sy) or base >= sz:
        raise ValueError("open shell wall/base incompatible with dimensions")
    mesh = Mesh()
    mesh.add(box(x, y, z, sx, sy, base))
    mesh.add(box(x, y, z + base, sx, wall, sz - base))
    mesh.add(box(x, y + sy - wall, z + base, sx, wall, sz - base))
    mesh.add(box(x, y + wall, z + base, wall, sy - 2 * wall, sz - base))
    mesh.add(box(x + sx - wall, y + wall, z + base, wall, sy - 2 * wall, sz - base))
    return mesh


def wireframe_box(x: float, y: float, z: float, sx: float, sy: float, sz: float,
                  rail: float) -> Mesh:
    """Twelve-beam open cage used only to make a clearance volume tangible."""
    if rail * 2 >= min(sx, sy, sz):
        raise ValueError("wireframe rail too large")
    mesh = Mesh()
    for zz in (z, z + sz - rail):
        mesh.add(frame_rect(x, y, zz, sx, sy, rail, rail))
    for xx in (x, x + sx - rail):
        for yy in (y, y + sy - rail):
            mesh.add(box(xx, yy, z + rail, rail, rail, sz - 2 * rail))
    return mesh


def cylinder(cx: float, cy: float, cz: float, diameter: float, length: float,
             facets: int, axis: str = "z") -> Mesh:
    """Closed regular-prism cylinder along X, Y, or Z."""
    if diameter <= 0 or length <= 0 or facets < 8:
        raise ValueError("invalid cylinder")
    r = diameter / 2

    def point(t: float, at_end: bool) -> Vec3:
        a, b = r * math.cos(t), r * math.sin(t)
        q = length if at_end else 0.0
        if axis == "x":
            return (cx + q, cy + a, cz + b)
        if axis == "y":
            return (cx + a, cy + q, cz + b)
        if axis == "z":
            return (cx + a, cy + b, cz + q)
        raise ValueError(f"invalid cylinder axis {axis}")

    start_center = (cx, cy, cz)
    end_center = ({"x": (cx + length, cy, cz),
                   "y": (cx, cy + length, cz),
                   "z": (cx, cy, cz + length)})[axis]
    tris: list[Tri] = []
    for i in range(facets):
        a0 = 2 * math.pi * i / facets
        a1 = 2 * math.pi * (i + 1) / facets
        p0, p1 = point(a0, False), point(a1, False)
        q0, q1 = point(a0, True), point(a1, True)
        if axis in ("x", "z"):
            tris.extend([(p0, p1, q1), (p0, q1, q0)])
        else:
            tris.extend([(p0, q0, q1), (p0, q1, p1)])
        if axis in ("x", "z"):
            tris.extend([(start_center, p1, p0), (end_center, q0, q1)])
        else:
            tris.extend([(start_center, p0, p1), (end_center, q1, q0)])
    return Mesh(tris)


def annulus(cx: float, cy: float, z: float, outer_d: float, inner_d: float,
            height: float, facets: int) -> Mesh:
    """Closed Z-axis annular prism."""
    if not 0 < inner_d < outer_d:
        raise ValueError("invalid annulus diameters")
    ro, ri = outer_d / 2, inner_d / 2
    tris: list[Tri] = []
    for i in range(facets):
        a0, a1 = 2 * math.pi * i / facets, 2 * math.pi * (i + 1) / facets
        o0 = (cx + ro * math.cos(a0), cy + ro * math.sin(a0), z)
        o1 = (cx + ro * math.cos(a1), cy + ro * math.sin(a1), z)
        O0, O1 = (o0[0], o0[1], z + height), (o1[0], o1[1], z + height)
        i0 = (cx + ri * math.cos(a0), cy + ri * math.sin(a0), z)
        i1 = (cx + ri * math.cos(a1), cy + ri * math.sin(a1), z)
        I0, I1 = (i0[0], i0[1], z + height), (i1[0], i1[1], z + height)
        tris.extend([(o0, O0, O1), (o0, O1, o1),
                     (i0, I1, I0), (i0, i1, I1),
                     (O0, I0, I1), (O0, I1, O1),
                     (o0, i1, i0), (o0, o1, i1)])
    # The loop above is edge-consistent but inward-wound as a complete shell.
    return Mesh([(a, c, b) for a, b, c in tris])


def extrude_polygon(points: list[tuple[float, float]], z: float, height: float) -> Mesh:
    """Extrude a convex or star-shaped XY polygon using a centroid fan."""
    if len(points) < 3 or height <= 0:
        raise ValueError("invalid polygon extrusion")
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    cb, ct = (cx, cy, z), (cx, cy, z + height)
    tris: list[Tri] = []
    for i, p in enumerate(points):
        q = points[(i + 1) % len(points)]
        pb, qb = (p[0], p[1], z), (q[0], q[1], z)
        pt, qt = (p[0], p[1], z + height), (q[0], q[1], z + height)
        tris.extend([(cb, qb, pb), (ct, pt, qt), (pb, qb, qt), (pb, qt, pt)])
    return Mesh(tris)


def arrow(x: float, y: float, z: float, length: float, width: float,
          height: float, direction: str = "+x") -> Mesh:
    """Raised, filled diagnostic orientation arrow."""
    head = min(length * 0.42, width * 1.8)
    shaft = width * 0.35
    pts = [(0, -shaft / 2), (length - head, -shaft / 2),
           (length - head, -width / 2), (length, 0),
           (length - head, width / 2), (length - head, shaft / 2),
           (0, shaft / 2)]
    if direction == "-x":
        pts = [(-px, py) for px, py in pts]
    elif direction == "+y":
        pts = [(-py, px) for px, py in pts]
    elif direction == "-y":
        pts = [(py, -px) for px, py in pts]
    elif direction != "+x":
        raise ValueError(f"invalid arrow direction {direction}")
    return extrude_polygon([(x + px, y + py) for px, py in pts], z, height)


# Complete 5x7 uppercase bitmap font.  Markings are geometry, not annotations.
FONT = {
    "A":["01110","10001","10001","11111","10001","10001","10001"],
    "B":["11110","10001","10001","11110","10001","10001","11110"],
    "C":["01111","10000","10000","10000","10000","10000","01111"],
    "D":["11110","10001","10001","10001","10001","10001","11110"],
    "E":["11111","10000","10000","11110","10000","10000","11111"],
    "F":["11111","10000","10000","11110","10000","10000","10000"],
    "G":["01111","10000","10000","10111","10001","10001","01111"],
    "H":["10001","10001","10001","11111","10001","10001","10001"],
    "I":["11111","00100","00100","00100","00100","00100","11111"],
    "J":["00111","00010","00010","00010","10010","10010","01100"],
    "K":["10001","10010","10100","11000","10100","10010","10001"],
    "L":["10000","10000","10000","10000","10000","10000","11111"],
    "M":["10001","11011","10101","10101","10001","10001","10001"],
    "N":["10001","11001","10101","10011","10001","10001","10001"],
    "O":["01110","10001","10001","10001","10001","10001","01110"],
    "P":["11110","10001","10001","11110","10000","10000","10000"],
    "Q":["01110","10001","10001","10001","10101","10010","01101"],
    "R":["11110","10001","10001","11110","10100","10010","10001"],
    "S":["01111","10000","10000","01110","00001","00001","11110"],
    "T":["11111","00100","00100","00100","00100","00100","00100"],
    "U":["10001","10001","10001","10001","10001","10001","01110"],
    "V":["10001","10001","10001","10001","10001","01010","00100"],
    "W":["10001","10001","10001","10101","10101","11011","10001"],
    "X":["10001","10001","01010","00100","01010","10001","10001"],
    "Y":["10001","10001","01010","00100","00100","00100","00100"],
    "Z":["11111","00001","00010","00100","01000","10000","11111"],
    "0":["01110","10001","10011","10101","11001","10001","01110"],
    "1":["00100","01100","00100","00100","00100","00100","01110"],
    "2":["01110","10001","00001","00010","00100","01000","11111"],
    "3":["11110","00001","00001","01110","00001","00001","11110"],
    "4":["00010","00110","01010","10010","11111","00010","00010"],
    "5":["11111","10000","10000","11110","00001","00001","11110"],
    "6":["01110","10000","10000","11110","10001","10001","01110"],
    "7":["11111","00001","00010","00100","01000","01000","01000"],
    "8":["01110","10001","10001","01110","10001","10001","01110"],
    "9":["01110","10001","10001","01111","00001","00001","01110"],
    "-":["00000","00000","00000","11111","00000","00000","00000"],
    "+":["00000","00100","00100","11111","00100","00100","00000"],
    "/":["00001","00010","00010","00100","01000","01000","10000"],
    " ":["00000"] * 7,
}


def text_size(text: str, cell: float) -> tuple[float, float]:
    return ((len(text) * 6 - 1) * cell if text else 0.0, 7 * cell)


def text_mesh(text: str, x: float, y: float, z: float, cell: float,
              height: float) -> Mesh:
    """Raised XY text constructed from closed pixel cuboids."""
    mesh = Mesh()
    cursor = x
    for char in text.upper():
        if char not in FONT:
            raise ValueError(f"unsupported label character: {char!r}")
        rows = FONT[char]
        for row, bits in enumerate(rows):
            for col, bit in enumerate(bits):
                if bit == "1":
                    mesh.add(box(cursor + col * cell, y + (6 - row) * cell, z,
                                 cell * 0.86, cell * 0.86, height))
        cursor += 6 * cell
    return mesh


def write_binary_stl(path: Path, mesh: Mesh, label: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (f"W17 DIAGNOSTIC {label} MM").encode("ascii", errors="replace")[:80]
    with path.open("wb") as handle:
        handle.write(header.ljust(80, b"\0"))
        handle.write(struct.pack("<I", len(mesh.triangles)))
        for a, b, c in mesh.triangles:
            ux, uy, uz = (b[i] - a[i] for i in range(3))
            vx, vy, vz = (c[i] - a[i] for i in range(3))
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            mag = math.sqrt(nx * nx + ny * ny + nz * nz)
            normal = (0.0, 0.0, 0.0) if mag == 0 else (nx / mag, ny / mag, nz / mag)
            handle.write(struct.pack("<12fH", *(normal + a + b + c), 0))


def read_binary_stl(path: Path) -> Mesh:
    data = path.read_bytes()
    if len(data) < 84:
        raise ValueError(f"not a binary STL: {path}")
    count = struct.unpack_from("<I", data, 80)[0]
    if len(data) != 84 + count * 50:
        raise ValueError(f"binary STL size/count mismatch: {path}")
    triangles = []
    for index in range(count):
        record = struct.unpack_from("<12fH", data, 84 + index * 50)
        triangles.append(((record[3], record[4], record[5]),
                          (record[6], record[7], record[8]),
                          (record[9], record[10], record[11])))
    return Mesh(triangles)


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    return (struct.pack(">I", len(payload)) + kind + payload
            + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff))


def render_png(path: Path, mesh: Mesh, width: int, height: int,
               camera_view: Vec3 = (0.64, -0.60, 0.48)) -> None:
    """Small deterministic isometric z-buffer renderer for visual QA."""
    # View coordinates: by default the camera looks from (+X,-Y,+Z).  A near-top
    # view is used by selected label-review renders.
    view = camera_view
    vm = math.sqrt(sum(q * q for q in view))
    wv = tuple(q / vm for q in view)
    up0 = (0.0, 1.0, 0.0) if abs(wv[2]) > 0.9 else (0.0, 0.0, 1.0)
    uv = (up0[1] * wv[2] - up0[2] * wv[1],
          up0[2] * wv[0] - up0[0] * wv[2],
          up0[0] * wv[1] - up0[1] * wv[0])
    um = math.sqrt(sum(q * q for q in uv))
    uv = tuple(q / um for q in uv)
    vv = (wv[1] * uv[2] - wv[2] * uv[1],
          wv[2] * uv[0] - wv[0] * uv[2],
          wv[0] * uv[1] - wv[1] * uv[0])

    def project(p: Vec3) -> tuple[float, float, float]:
        return (sum(p[i] * uv[i] for i in range(3)),
                sum(p[i] * vv[i] for i in range(3)),
                sum(p[i] * wv[i] for i in range(3)))

    projected = [[project(v) for v in tri] for tri in mesh.triangles]
    us = [v[0] for tri in projected for v in tri]
    vs = [v[1] for tri in projected for v in tri]
    margin = 28.0
    scale = min((width - 2 * margin) / max(max(us) - min(us), 1e-6),
                (height - 2 * margin) / max(max(vs) - min(vs), 1e-6))
    u_mid, v_mid = (min(us) + max(us)) / 2, (min(vs) + max(vs)) / 2

    def screen(q: tuple[float, float, float]) -> tuple[float, float, float]:
        return ((q[0] - u_mid) * scale + width / 2,
                height / 2 - (q[1] - v_mid) * scale, q[2])

    background = (247, 248, 250)
    pixels = bytearray(background * (width * height))
    depth = [-float("inf")] * (width * height)
    light = (0.3, -0.2, 0.93)
    lm = math.sqrt(sum(q * q for q in light))
    light = tuple(q / lm for q in light)

    for tri, tri_world in zip(projected, mesh.triangles):
        p = [screen(q) for q in tri]
        x0 = max(0, int(math.floor(min(q[0] for q in p))))
        x1 = min(width - 1, int(math.ceil(max(q[0] for q in p))))
        y0 = max(0, int(math.floor(min(q[1] for q in p))))
        y1 = min(height - 1, int(math.ceil(max(q[1] for q in p))))
        ax, ay, _ = p[0]
        bx, by, _ = p[1]
        cx, cy, _ = p[2]
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-9:
            continue
        a, b, c = tri_world
        e1 = tuple(b[i] - a[i] for i in range(3))
        e2 = tuple(c[i] - a[i] for i in range(3))
        normal = (e1[1] * e2[2] - e1[2] * e2[1],
                  e1[2] * e2[0] - e1[0] * e2[2],
                  e1[0] * e2[1] - e1[1] * e2[0])
        nm = math.sqrt(sum(q * q for q in normal)) or 1.0
        normal = tuple(q / nm for q in normal)
        shade = 0.56 + 0.34 * abs(sum(normal[i] * light[i] for i in range(3)))
        color = (int(53 * shade), int(130 * shade), int(170 * shade))
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                px, py = xx + 0.5, yy + 0.5
                wa = ((by - cy) * (px - cx) + (cx - bx) * (py - cy)) / den
                wb = ((cy - ay) * (px - cx) + (ax - cx) * (py - cy)) / den
                wc = 1.0 - wa - wb
                if wa < -1e-7 or wb < -1e-7 or wc < -1e-7:
                    continue
                zz = wa * p[0][2] + wb * p[1][2] + wc * p[2][2]
                idx = yy * width + xx
                if zz > depth[idx]:
                    depth[idx] = zz
                    off = idx * 3
                    pixels[off:off + 3] = bytes(color)

    raw = b"".join(b"\x00" + bytes(pixels[row * width * 3:(row + 1) * width * 3])
                   for row in range(height))
    png = (b"\x89PNG\r\n\x1a\n"
           + _png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
           + _png_chunk(b"IDAT", zlib.compress(raw, 9))
           + _png_chunk(b"IEND", b""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)
