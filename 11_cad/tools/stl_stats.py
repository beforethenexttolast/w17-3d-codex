#!/usr/bin/env python3
"""stl_stats.py — triangle count and bounding box of an STL, as one line.

Used by render.sh to fill the render table in 11_cad/README.md. Handles both
binary and ASCII STL, because OpenSCAD's default export format has changed
between releases and we would rather not care.

Output (tab separated), so it can be pasted straight into a Markdown table:

    <name>  <tris>  <dx>x<dy>x<dz>  <x0>..<x1>  <y0>..<y1>  <z0>..<z1>

The axes are the W17 vehicle frame, because that is what the models are
authored in: x = vehicle X (forward), y = vehicle L (lateral), z = vehicle Z
(up from the floor datum DAT-F).
"""

import struct
import sys
from pathlib import Path


def read_stl(path: Path):
    """Return (triangle_count, [(minx,miny,minz),(maxx,maxy,maxz)])."""
    data = path.read_bytes()
    if not data:
        return 0, None

    # A binary STL is 84 bytes of header + 50 bytes per triangle, exactly.
    tris = 0
    verts = []
    if len(data) >= 84:
        (count,) = struct.unpack_from("<I", data, 80)
        if len(data) == 84 + count * 50:
            tris = count
            for i in range(count):
                off = 84 + i * 50 + 12  # skip the facet normal
                verts.extend(struct.unpack_from("<9f", data, off))
            xs = verts[0::3]
            ys = verts[1::3]
            zs = verts[2::3]
            if not xs:
                return 0, None
            return tris, [(min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))]

    # Otherwise assume ASCII.
    xs, ys, zs = [], [], []
    for line in data.decode("utf-8", "replace").splitlines():
        s = line.strip()
        if s.startswith("vertex "):
            _, x, y, z = s.split()
            xs.append(float(x))
            ys.append(float(y))
            zs.append(float(z))
        elif s.startswith("facet "):
            tris += 1
    if not xs:
        return tris, None
    return tris, [(min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))]


def main(argv):
    if len(argv) < 2:
        print("usage: stl_stats.py <file.stl> [...]", file=sys.stderr)
        return 2
    rc = 0
    for arg in argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"{p.name}\tMISSING", file=sys.stderr)
            rc = 1
            continue
        tris, bb = read_stl(p)
        if bb is None:
            # An empty STL is a real failure mode: the model rendered but
            # produced no solid. Say so loudly rather than printing zeros.
            print(f"{p.stem}\t{tris}\tEMPTY — the model produced no geometry")
            rc = 1
            continue
        (x0, y0, z0), (x1, y1, z1) = bb
        print(
            "{}\t{}\t{:.1f}x{:.1f}x{:.1f}\t{:.1f}..{:.1f}\t{:.1f}..{:.1f}\t{:.1f}..{:.1f}".format(
                p.stem, tris, x1 - x0, y1 - y0, z1 - z0, x0, x1, y0, y1, z0, z1
            )
        )
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
