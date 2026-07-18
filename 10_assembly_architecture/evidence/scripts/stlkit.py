#!/usr/bin/env python3
"""stlkit.py — pure-Python (no numpy) STL inspection toolkit for P0 (Session 4A).

Read-only with respect to source models: loads binary/ASCII STL, never writes one.
All measurement scripts in this directory import from here so every number in
`V_P0_geometry_measurement_results.md` is reproducible with:

    python3 10_assembly_architecture/evidence/scripts/<script>.py
    (run from the repo root)

Conventions
-----------
* Triangles are tuples (v0, v1, v2), each vertex an (x, y, z) float tuple.
* Transforms are axis permutations/sign flips + translations only — no arbitrary
  rotations are ever applied, and every transform is recorded by the calling
  script in its printed output and in the results report.
* The W17-P0 vehicle frame used by the measurement scripts:
      X+ = forward (nose direction), L = lateral offset from centreline, Z+ = up,
      Z = 0 at DAT-F (chassis floor TOP plane),
      X = 0 at the front-floor <-> rear-floor mating joint (junction line).
  The physical driver-left/right name for the sign of L remains open until the
  Gate-P1 dry-fit; measurement scripts document the sign caveat explicitly.

Known limitations (recorded per the tool-validation rule):
* Section/scanline logic assumes locally 2-manifold geometry; open edges produce
  unpaired crossings. Scripts must sanity-check crossing counts (even parity)
  and MUST NOT interpret an empty section as an empty cavity — assert non-empty
  segment lists before deriving any dimension.
* Ray casting reports every surface crossing; callers decide which pair is the
  cavity of interest (single-shell walls give two crossings per skin).
* A section plane exactly coincident with a flat face skips the in-plane
  triangles but still collects the touching edges of adjacent walls, so it
  returns the face's closed BOUNDARY loop with no material-thickness info.
  Measurement scripts must offset section planes off exact faces by >=0.05 mm
  (validated by p0_01_stlkit_selftest.py).
"""
import struct
import math
import os

# ---------------------------------------------------------------- loading


def load_stl(path):
    """Load a binary or ASCII STL. Returns list of ((x,y,z),(x,y,z),(x,y,z))."""
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        head = f.read(84)
        if len(head) >= 84:
            (n,) = struct.unpack('<I', head[80:84])
            if 84 + 50 * n == size:
                return _load_binary(path, n)
    return _load_ascii(path)


def _load_binary(path, n):
    tris = []
    with open(path, 'rb') as f:
        f.seek(84)
        data = f.read()
    unpack = struct.Struct('<12fH').unpack_from
    for i in range(n):
        rec = unpack(data, i * 50)
        tris.append(((rec[3], rec[4], rec[5]),
                     (rec[6], rec[7], rec[8]),
                     (rec[9], rec[10], rec[11])))
    return tris


def _load_ascii(path):
    tris, cur = [], []
    with open(path, 'r', errors='replace') as f:
        for line in f:
            parts = line.split()
            if parts and parts[0] == 'vertex':
                cur.append((float(parts[1]), float(parts[2]), float(parts[3])))
                if len(cur) == 3:
                    tris.append(tuple(cur))
                    cur = []
    return tris


# ---------------------------------------------------------------- transforms


def apply(tris, fn):
    """Apply vertex function fn((x,y,z)) -> (x,y,z) to every vertex."""
    return [(fn(a), fn(b), fn(c)) for a, b, c in tris]


def translate(tris, dx, dy, dz):
    return apply(tris, lambda v: (v[0] + dx, v[1] + dy, v[2] + dz))


def bbox(tris):
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def fmt_bbox(bb):
    (x0, y0, z0), (x1, y1, z1) = bb
    return ("x[%8.2f..%8.2f] (%7.2f)  y[%8.2f..%8.2f] (%7.2f)  z[%8.2f..%8.2f] (%7.2f)"
            % (x0, x1, x1 - x0, y0, y1, y1 - y0, z0, z1, z1 - z0))


# ---------------------------------------------------------------- sections

AX = {'x': 0, 'y': 1, 'z': 2}


def section(tris, axis, value):
    """Intersect mesh with plane axis=value.

    Returns list of 2D segments ((a0,b0),(a1,b1)) in the two remaining axes,
    kept in x,y,z order (e.g. axis='x' -> coordinates are (y, z)).
    """
    ai = AX[axis]
    oi = [i for i in range(3) if i != ai]
    segs = []
    for t in tris:
        d = [v[ai] - value for v in t]
        pts = []
        for i in range(3):
            j = (i + 1) % 3
            di, dj = d[i], d[j]
            if di == dj:
                continue
            if (di > 0) != (dj > 0) or di == 0 or dj == 0:
                f = di / (di - dj)
                if 0.0 <= f <= 1.0:
                    vi, vj = t[i], t[j]
                    p = (vi[oi[0]] + f * (vj[oi[0]] - vi[oi[0]]),
                         vi[oi[1]] + f * (vj[oi[1]] - vi[oi[1]]))
                    pts.append(p)
        uniq = []
        for p in pts:
            if not any(abs(p[0] - q[0]) < 1e-7 and abs(p[1] - q[1]) < 1e-7 for q in uniq):
                uniq.append(p)
        if len(uniq) == 2:
            segs.append((uniq[0], uniq[1]))
    return segs


def scanline(segs, axis_idx, value):
    """Cut 2D section segments with line coord[axis_idx]=value; return sorted
    crossing coordinates in the other axis (even-odd material spans)."""
    other = 1 - axis_idx
    xs = []
    for (p, q) in segs:
        a, b = p[axis_idx], q[axis_idx]
        if (a > value) != (b > value):
            f = (value - a) / (b - a)
            xs.append(p[other] + f * (q[other] - p[other]))
    xs.sort()
    return xs


def spans(crossings):
    """Even-odd pairing of sorted crossings -> [(lo, hi), ...]."""
    return [(crossings[i], crossings[i + 1]) for i in range(0, len(crossings) - 1, 2)]


# ---------------------------------------------------------------- loops


def assemble_loops(segs, tol=1e-3):
    """Chain section segments into loops (lists of 2D points). Loops whose ends
    meet within tol are closed; callers should check closure themselves."""
    def key(p):
        return (round(p[0] / tol), round(p[1] / tol))

    adj = {}
    for i, (p, q) in enumerate(segs):
        adj.setdefault(key(p), []).append((i, p, q))
        adj.setdefault(key(q), []).append((i, q, p))
    used = [False] * len(segs)
    loops = []
    for i, (p, q) in enumerate(segs):
        if used[i]:
            continue
        used[i] = True
        loop = [p, q]
        while True:
            k = key(loop[-1])
            nxt = None
            for (j, a, b) in adj.get(k, []):
                if not used[j]:
                    nxt = (j, b)
                    break
            if nxt is None:
                break
            used[nxt[0]] = True
            loop.append(nxt[1])
            if key(loop[-1]) == key(loop[0]):
                break
        loops.append(loop)
    return loops


def loop_closed(loop, tol=1e-2):
    return (abs(loop[0][0] - loop[-1][0]) < tol and abs(loop[0][1] - loop[-1][1]) < tol
            and len(loop) > 3)


def loop_area(loop):
    a = 0.0
    for i in range(len(loop) - 1):
        a += loop[i][0] * loop[i + 1][1] - loop[i + 1][0] * loop[i][1]
    return a / 2.0


def loop_bbox(loop):
    us = [p[0] for p in loop]
    vs = [p[1] for p in loop]
    return (min(us), min(vs)), (max(us), max(vs))


def loop_centroid(loop):
    us = [p[0] for p in loop]
    vs = [p[1] for p in loop]
    return (sum(us) / len(us), sum(vs) / len(vs))


# ---------------------------------------------------------------- ray casting


class ZRayGrid:
    """Vertical (Z) ray caster with (x,y) uniform-grid triangle binning."""

    def __init__(self, tris, cell=8.0):
        self.tris = tris
        self.cell = cell
        self.bins = {}
        for idx, t in enumerate(tris):
            xs = [v[0] for v in t]
            ys = [v[1] for v in t]
            i0, i1 = int(min(xs) // cell), int(max(xs) // cell)
            j0, j1 = int(min(ys) // cell), int(max(ys) // cell)
            for i in range(i0, i1 + 1):
                for j in range(j0, j1 + 1):
                    self.bins.setdefault((i, j), []).append(idx)

    def crossings(self, x, y):
        """All (z, nz_sign) crossings of the vertical line at (x, y), sorted by z.
        nz_sign > 0 = surface faces up at that crossing. Deduped on z."""
        out = []
        cellkey = (int(x // self.cell), int(y // self.cell))
        for idx in self.bins.get(cellkey, ()):
            c = _tri_z_at(self.tris[idx], x, y)
            if c is not None:
                out.append(c)
        out.sort(key=lambda c: c[0])
        ded = []
        for c in out:
            if not ded or abs(c[0] - ded[-1][0]) > 1e-6:
                ded.append(c)
        return ded


def _tri_z_at(t, x, y):
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = t
    d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if abs(d) < 1e-12:
        return None
    l0 = ((y1 - y2) * (x - x2) + (x2 - x1) * (y - y2)) / d
    l1 = ((y2 - y0) * (x - x2) + (x0 - x2) * (y - y2)) / d
    l2 = 1.0 - l0 - l1
    eps = -1e-9
    if l0 < eps or l1 < eps or l2 < eps:
        return None
    z = l0 * z0 + l1 * z1 + l2 * z2
    ux, uy, uz = x1 - x0, y1 - y0, z1 - z0
    vx, vy, vz = x2 - x0, y2 - y0, z2 - z0
    nz = ux * vy - uy * vx
    return (z, 1 if nz > 0 else (-1 if nz < 0 else 0))


# ---------------------------------------------------------------- SVG output


class SVG:
    """Minimal SVG writer for section diagrams (text-only asset, commit-safe)."""

    def __init__(self, u0, v0, u1, v1, scale=4.0, pad=16.0, flip_v=True):
        self.u0, self.v0, self.u1, self.v1 = u0, v0, u1, v1
        self.s = scale
        self.pad = pad
        self.flip = flip_v
        self.body = []
        self.w = (u1 - u0) * scale + 2 * pad
        self.h = (v1 - v0) * scale + 2 * pad

    def pt(self, u, v):
        px = (u - self.u0) * self.s + self.pad
        if self.flip:
            py = (self.v1 - v) * self.s + self.pad
        else:
            py = (v - self.v0) * self.s + self.pad
        return px, py

    def segs(self, segs, color='#222', width=1.0):
        for (p, q) in segs:
            (x1, y1), (x2, y2) = self.pt(*p), self.pt(*q)
            self.body.append(
                '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"/>'
                % (x1, y1, x2, y2, color, width))

    def line(self, p, q, color='#c00', width=1.0, dash=None):
        (x1, y1), (x2, y2) = self.pt(*p), self.pt(*q)
        d = ' stroke-dasharray="%s"' % dash if dash else ''
        self.body.append(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"%s/>'
            % (x1, y1, x2, y2, color, width, d))

    def circle(self, p, r_mm, color='#06c', width=1.0, fill='none'):
        (x, y) = self.pt(*p)
        self.body.append(
            '<circle cx="%.1f" cy="%.1f" r="%.1f" stroke="%s" stroke-width="%.1f" fill="%s"/>'
            % (x, y, r_mm * self.s, color, width, fill))

    def text(self, p, s, size=10, color='#000', anchor='start'):
        (x, y) = self.pt(*p)
        self.body.append(
            '<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" '
            'font-family="monospace">%s</text>' % (x, y, size, color, anchor, s))

    def save(self, path, title=''):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
                    'viewBox="0 0 %.0f %.0f">\n' % (self.w, self.h, self.w, self.h))
            f.write('<rect width="100%" height="100%" fill="white"/>\n')
            if title:
                f.write('<text x="8" y="12" font-size="11" font-family="monospace" '
                        'fill="#000">%s</text>\n' % title)
            for b in self.body:
                f.write(b + '\n')
            f.write('</svg>\n')
