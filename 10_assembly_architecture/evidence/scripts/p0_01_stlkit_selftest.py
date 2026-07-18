#!/usr/bin/env python3
"""p0_01_stlkit_selftest.py — Session 4A tool validation for stlkit.py.

Exercises every stlkit primitive against synthetic geometry with known answers
before any authoritative P0 number is derived from it. Covers the mandated
edge cases: units passthrough, section semantics, scanline parity, even-odd
spans, loop closure/area, ray misses, multiple intersections, non-watertight
meshes, plane-coincident faces, and binary/ASCII STL parsing round-trip.

Run from the repo root. Writes two throwaway STLs to the OS temp dir only.
Exit 0 = all checks pass; any failure raises AssertionError loudly.
"""
import os
import struct
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stlkit as K

FAILS = []


def check(name, cond, detail=''):
    print('%-58s %s %s' % (name, 'PASS' if cond else 'FAIL', detail))
    if not cond:
        FAILS.append(name)


def box_tris(x0, y0, z0, x1, y1, z1):
    """12-triangle closed axis-aligned box (outward CCW normals)."""
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    quads = [(0, 3, 2, 1),   # bottom (z0), normal -Z
             (4, 5, 6, 7),   # top (z1), normal +Z
             (0, 1, 5, 4),   # front (y0), normal -Y
             (2, 3, 7, 6),   # back (y1), normal +Y
             (0, 4, 7, 3),   # left (x0), normal -X
             (1, 2, 6, 5)]   # right (x1), normal +X
    tris = []
    for (a, b, c, d) in quads:
        tris.append((v[a], v[b], v[c]))
        tris.append((v[a], v[c], v[d]))
    return tris


# ---- 1. bbox + translate (mm passthrough: coordinates are never scaled) ----
cube = box_tris(0, 0, 0, 10, 20, 30)
bb = K.bbox(cube)
check('bbox of 10x20x30 box', bb == ((0, 0, 0), (10, 20, 30)), str(bb))
bb2 = K.bbox(K.translate(cube, 1, -2, 3))
check('translate then bbox', bb2 == ((1, -2, 3), (11, 18, 33)), str(bb2))

# ---- 2. section semantics: axis plane, remaining axes in x,y,z order ------
segs = K.section(cube, 'x', 5.0)          # plane x=5 -> coords are (y, z)
check('section x=5 non-empty', len(segs) > 0, '%d segs' % len(segs))
loops = [l for l in K.assemble_loops(segs) if K.loop_closed(l)]
check('section x=5 closes into 1 loop', len(loops) == 1, '%d loops' % len(loops))
if loops:
    (u0, v0), (u1, v1) = K.loop_bbox(loops[0])
    check('section rect is y[0..20] z[0..30]',
          abs(u0) < 1e-6 and abs(u1 - 20) < 1e-6 and abs(v0) < 1e-6 and abs(v1 - 30) < 1e-6,
          'u[%.2f..%.2f] v[%.2f..%.2f]' % (u0, u1, v0, v1))
    check('loop area == 600 mm^2', abs(abs(K.loop_area(loops[0])) - 600.0) < 1e-6,
          '%.3f' % K.loop_area(loops[0]))

# ---- 3. plane-coincident face: characterized DEGENERATE semantics ---------
# In-plane triangles are skipped; adjacent walls contribute their touching
# edges, so the result is the face's closed BOUNDARY loop carrying no
# material-thickness info. Rule: offset section planes off exact faces.
segs_face = K.section(cube, 'z', 30.0)
loops_face = [l for l in K.assemble_loops(segs_face) if K.loop_closed(l)]
face_ok = (len(loops_face) == 1)
if face_ok:
    (fu0, fv0), (fu1, fv1) = K.loop_bbox(loops_face[0])
    face_ok = (abs(fu0) < 1e-6 and abs(fu1 - 10) < 1e-6
               and abs(fv0) < 1e-6 and abs(fv1 - 20) < 1e-6)
check('coincident-face section = boundary loop only (offset planes!)',
      face_ok, '%d segs -> face outline, no thickness data' % len(segs_face))

# ---- 4. section plane that misses the solid entirely ----------------------
check('section beyond bbox is empty (NOT an empty cavity!)',
      K.section(cube, 'z', 99.0) == [], '')

# ---- 5. scanline parity + even-odd spans ----------------------------------
segs_z15 = K.section(cube, 'z', 15.0)     # coords (x, y)
xs = K.scanline(segs_z15, 1, 10.0)        # cut section at y=10 -> x crossings
check('scanline crossing count is even', len(xs) % 2 == 0, str(xs))
sp = K.spans(xs)
check('scanline span is x[0..10]',
      len(sp) == 1 and abs(sp[0][0]) < 1e-6 and abs(sp[0][1] - 10) < 1e-6, str(sp))
check('scanline missing the section is empty',
      K.scanline(segs_z15, 1, 999.0) == [], '')

# ---- 6. two disjoint boxes: multiple intersections, two spans -------------
two = box_tris(0, 0, 0, 10, 10, 10) + box_tris(30, 0, 0, 40, 10, 10)
segs2 = K.section(two, 'z', 5.0)
xs2 = K.scanline(segs2, 1, 5.0)
sp2 = K.spans(xs2)
check('two solids -> 4 crossings, 2 spans',
      len(xs2) == 4 and len(sp2) == 2
      and abs(sp2[0][0] - 0) < 1e-6 and abs(sp2[0][1] - 10) < 1e-6
      and abs(sp2[1][0] - 30) < 1e-6 and abs(sp2[1][1] - 40) < 1e-6, str(sp2))

# ---- 7. non-watertight mesh: open loop must be detectable -----------------
open_box = [t for t in box_tris(0, 0, 0, 10, 10, 10)
            if not all(v[0] == 10 for v in t)]        # remove +X face
segs_open = K.section(open_box, 'z', 5.0)
loops_open = K.assemble_loops(segs_open)
check('open mesh -> section loop reported NOT closed',
      len(loops_open) >= 1 and not any(K.loop_closed(l) for l in loops_open),
      '%d loops' % len(loops_open))
xs_open = K.scanline(segs_open, 1, 5.0)
check('open mesh -> odd/short crossings detectable',
      len(xs_open) != 2, 'crossings=%s (parity check catches the hole)' % xs_open)

# ---- 8. ZRayGrid: hits, miss, multiple, orientation sign ------------------
grid = K.ZRayGrid(cube, cell=8.0)
c = grid.crossings(5.0, 10.0)
check('Z-ray through box -> 2 crossings z=0,30',
      len(c) == 2 and abs(c[0][0]) < 1e-6 and abs(c[1][0] - 30) < 1e-6, str(c))
check('Z-ray bottom faces down / top faces up',
      len(c) == 2 and c[0][1] < 0 and c[1][1] > 0, str(c))
check('Z-ray outside footprint -> MISS is empty list, not error',
      grid.crossings(50.0, 50.0) == [], '')
grid2 = K.ZRayGrid(box_tris(0, 0, 0, 10, 10, 10)
                   + box_tris(0, 0, 20, 10, 10, 30), cell=8.0)
c2 = grid2.crossings(5.0, 5.0)
check('Z-ray through stacked solids -> 4 crossings',
      len(c2) == 4, str([round(z, 3) for z, s in c2]))
sp_z = K.spans([z for z, s in c2])
check('Z spans are [0..10],[20..30]',
      len(sp_z) == 2 and abs(sp_z[0][1] - 10) < 1e-6 and abs(sp_z[1][0] - 20) < 1e-6,
      str(sp_z))

# ---- 9. degenerate triangle: zero-area must not crash the ray caster ------
degen = [((0, 0, 0), (10, 0, 0), (20, 0, 0))]
check('degenerate (zero-area) triangle -> ray returns None path',
      K.ZRayGrid(degen, cell=8.0).crossings(5.0, 0.0) == [], '')

# ---- 10. binary/ASCII STL round-trip: same mesh from both encodings -------
tmpdir = tempfile.mkdtemp(prefix='stlkit_selftest_')
bin_path = os.path.join(tmpdir, 'cube_bin.stl')
asc_path = os.path.join(tmpdir, 'cube_asc.stl')
with open(bin_path, 'wb') as f:
    f.write(b'\0' * 80)
    f.write(struct.pack('<I', len(cube)))
    for (a, b, cc) in cube:
        f.write(struct.pack('<12fH', 0, 0, 0, *(a + b + cc), 0))
with open(asc_path, 'w') as f:
    f.write('solid cube\n')
    for t in cube:
        f.write(' facet normal 0 0 0\n  outer loop\n')
        for v in t:
            f.write('   vertex %r %r %r\n' % v)
        f.write('  endloop\n endfacet\n')
    f.write('endsolid cube\n')
tb = K.load_stl(bin_path)
ta = K.load_stl(asc_path)
check('binary STL loads 12 tris, bbox exact',
      len(tb) == 12 and K.bbox(tb) == ((0, 0, 0), (10, 20, 30)), '')
check('ASCII STL loads 12 tris, bbox exact',
      len(ta) == 12 and K.bbox(ta) == ((0, 0, 0), (10, 20, 30)), '')
for p in (bin_path, asc_path):
    os.remove(p)
os.rmdir(tmpdir)

print()
if FAILS:
    print('SELFTEST: FAIL —', len(FAILS), 'checks failed:', FAILS)
    sys.exit(1)
print('SELFTEST: PASS — stlkit primitives validated for P0 use')
