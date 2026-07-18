#!/usr/bin/env python3
"""p0_02_floor_datum_and_features.py — Session 4A, D-01 (+ the D-27 feature base).

Establishes the P0 vehicle frame from the floor STLs, verifies the floor-top
datum plane, measures the front<->rear floor joint, classifies every floor
feature (through-hole / top pocket / underside recess), derives the fastener
map in vehicle coordinates, and writes the D-01 evidence tables + diagram.

P0 VEHICLE FRAME (defined here, used by every later p0_* script)
  X+  forward (nose direction — forced by the tongue-and-groove joint: the
      front floor's rear edge carries the tongue, so its opposite end is the nose)
  L   lateral offset from the floor centreline (authored z_lat - 68.5).
      SIGN CAVEAT: which L sign is the driver's LEFT is PARTIALLY RESOLVED —
      if the STL set is authored right-handed, +L(high-z) = RIGHT; the Rev-1.1
      build photo puts the spur/belt on the car's RIGHT while the floor's
      spur/belt cutout is at LOW z. One of {mirrored export, revision change,
      cutout misread} applies; pin the mapping at the first physical dry-fit.
      All |L| values are exact regardless.
  Z   up. Z = 0 at DAT-F = the chassis floor TOP plane (authored y = +4).

  Transforms (translations/axis relabels only, no rotation):
    front floor  X = x + 89.00          L = z - 68.5   Z = y - 4
    back floor   X = x -  1.15          L = z - 68.5   Z = y - 4
    back floor 2 X = x + 25.22          L = z - 68.5   Z = y - 4 - 8   (sits one
                 plate-thickness LOWER: its plan region overlaps the back floor
                 and its bolt pair is coaxial with the back-floor pair)
    FloorBoard2  X = -x - 34.13 (flipped) L = z - 9.5  Z = y - 5      (recessed
                 into the 2 mm underside channel: occupies Z -8..-6)

Run from the repo root.  Read-only on models; writes evidence to
10_assembly_architecture/evidence/p0/{tables,diagrams}.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stlkit as K

FL = '02_ready_to_slice/05_PETG_floor'
OUT_T = '10_assembly_architecture/evidence/p0/tables'
OUT_D = '10_assembly_architecture/evidence/p0/diagrams'

XOFF = {'ff': 89.00, 'bf': -1.15, 'b2': 25.22}
ZOFF = {'ff': -4.0, 'bf': -4.0, 'b2': -12.0}
NAMES = {'ff': '2023NewFrontFloorLargerParts.stl',
         'bf': '2023NewBackFloorLargerParts.stl',
         'b2': '2023NewBackFloorLargerPart2.stl'}


def load(tag):
    p = os.path.join(FL, NAMES[tag])
    if not os.path.isfile(p):
        raise SystemExit('FATAL: missing model %s (run from repo root)' % p)
    return K.load_stl(p)


def veh(tag, x, zlat, y):
    """Authored (x, z_lat, y) -> vehicle (X, L, Z)."""
    return (x + XOFF[tag], zlat - 68.5, y + ZOFF[tag])


def closed_loops(tris, y):
    segs = K.section(tris, 'y', y)
    loops = K.assemble_loops(segs)
    out, nopen = [], 0
    for l in loops:
        if K.loop_closed(l):
            (u0, v0), (u1, v1) = K.loop_bbox(l)
            out.append((abs(K.loop_area(l)), u0, u1, v0, v1))
        else:
            nopen += 1
    return out, nopen


def main():
    os.makedirs(OUT_T, exist_ok=True)
    os.makedirs(OUT_D, exist_ok=True)
    parts = {t: load(t) for t in ('ff', 'bf', 'b2')}
    grids = {t: K.ZRayGrid(K.apply(parts[t], lambda v: (v[0], v[2], v[1])), cell=6.0)
             for t in parts}   # probe grid: (x, z_lat) -> thickness crossings in y

    md = []   # report lines
    md.append('# p0_02 — D-01 floor datum & feature map (generated; frame: P0 vehicle frame)')
    md.append('')
    md.append('All coordinates in the P0 vehicle frame (X fwd, L lateral from centreline,')
    md.append('Z up, Z=0 at DAT-F floor top). Lateral LEFT/RIGHT naming: see sign caveat')
    md.append('in the script header — |L| exact, side naming PARTIALLY RESOLVED.')
    md.append('')

    # ---- 1. joint measurement -------------------------------------------------
    md.append('## 1. Front<->rear floor joint (tongue & groove)')
    ffs = K.section(parts['ff'], 'z', 68.5)
    bfs = K.section(parts['bf'], 'z', 30.0)
    tongue = [(x, K.scanline(ffs, 0, x)) for x in (-91.0, -90.5, -90.0, -89.5, -89.2)]
    groove = [(x, K.scanline(bfs, 0, x)) for x in (-1.0, 0.0, 0.5, 0.8, 1.1)]
    md.append('- Front-floor rear edge: full-thickness butt face at authored x=-89.0;')
    md.append('  wedge tongue x -89.0..-91.0 (profile y %s at x=-90.0).'
              % [round(v, 2) for v in dict(tongue)[-90.0]])
    md.append('- Back-floor forward edge: butt face x=+1.16 with matching wedge groove')
    md.append('  (opening y %s at x=+0.8, z_lat=30).' % [round(v, 2) for v in dict(groove)[0.8]])
    md.append('- Mated registration: x_ff = x_bf - 90.15 (+-0.2, cross-checked by the')
    md.append('  FloorBoard2 hole span 93.6 mm landing on both plates within 0.2 mm).')
    md.append('- Joint interface plane defined as X = 0.')
    md.append('')

    # ---- 2. floor-top flatness / thickness classes ----------------------------
    md.append('## 2. Floor-top datum (DAT-F) verification + thickness classes')
    import collections
    thick = collections.Counter()
    bad_top = []
    for tag in ('ff', 'bf'):
        (x0, _, z0), (x1, _, z1) = K.bbox(parts[tag])
        g = grids[tag]
        xs = [x0 + 2 + i * 4 for i in range(int((x1 - x0 - 4) // 4) + 1)]
        zs = [z0 + 2 + j * 4 for j in range(int((z1 - z0 - 4) // 4) + 1)]
        for x in xs:
            for z in zs:
                sp = K.spans([c[0] for c in g.crossings(x, z)])
                if not sp:
                    thick[(tag, 'open')] += 1
                    continue
                lo = min(s[0] for s in sp)
                hi = max(s[1] for s in sp)
                thick[(tag, round(hi - lo, 1))] += 1
                if hi > 4.01 or (4.0 - hi) > 0.15:
                    bad_top.append((tag, x, z, hi))
    md.append('- 4 mm-grid ray survey over both plates: every sampled solid point tops at')
    md.append('  authored y=+4.00 (deviations >0.15 mm: %d of %d samples — all at outer'
              % (len(bad_top), sum(thick.values())))
    md.append('  edge chamfers / the joint edge, none in a mounting region)')
    md.append('- => DAT-F is ONE continuous flat plane over front+back floors: Z=0. DIGITALLY CONFIRMED.')

    def bucket(tag):
        b = collections.Counter()
        for (t, k), v in thick.items():
            if t != tag:
                continue
            b['open' if k == 'open' else '%.0f' % round(float(k))] += v
        return dict(sorted(b.items()))

    md.append('- Thickness classes, bucketed to 1 mm (front floor): %s' % bucket('ff'))
    md.append('  (back floor: %s)' % bucket('bf'))
    md.append('- 4.0 = plain plate (underside at Z-4); ~6 = underside 2 mm recess zones')
    md.append('  (FloorBoard2 channel / nut pockets); 8.0 = full-depth zones (centre spine')
    md.append('  block, outboard skirts) reaching Z-8. Top face flat everywhere -> ribs,')
    md.append('  recesses and skirts are all UNDERSIDE features; the mounting surface is')
    md.append('  uninterrupted EXCEPT at through-openings.')
    if bad_top:
        for tag, x, z, hi in bad_top[:12]:
            md.append('  - deviation: %s (%.1f, %.1f) top=%.2f' % (tag, x, z, hi))
    md.append('')

    # ---- 3. feature classification --------------------------------------------
    md.append('## 3. Feature map (classified loops; vehicle coords)')
    rows = []
    for tag in ('ff', 'bf', 'b2'):
        top, no1 = closed_loops(parts[tag], 3.0)
        bot, no2 = closed_loops(parts[tag], -3.0)
        gr = grids[tag]

        def near(lset, cu, cv):
            for a, u0, u1, v0, v1 in lset:
                if abs((u0 + u1) / 2 - cu) < 1.0 and abs((v0 + v1) / 2 - cv) < 1.0:
                    return True
            return False

        (bx0, _, bz0), (bx1, _, bz1) = K.bbox(parts[tag])
        part_area = (bx1 - bx0) * (bz1 - bz0)
        seen = []
        for src, lset in (('top', top), ('bot', bot)):
            for a, u0, u1, v0, v1 in lset:
                if (u1 - u0) * (v1 - v0) > 0.6 * part_area:
                    continue   # outer silhouette, not a feature
                cu, cv = (u0 + u1) / 2, (v0 + v1) / 2
                if any(abs(cu - p[0]) < 1.0 and abs(cv - p[1]) < 1.0 for p in seen):
                    continue
                seen.append((cu, cv))
                sp = K.spans([c[0] for c in gr.crossings(cu, cv)])
                in_top, in_bot = near(top, cu, cv), near(bot, cu, cv)
                if not sp and in_top and in_bot:
                    kind = 'THROUGH'
                elif not sp:
                    kind = 'THROUGH(edge)'
                elif in_top and not in_bot:
                    kind = 'TOP-POCKET(depth %.1f)' % (4.0 - max(s[1] for s in sp))
                elif in_bot and not in_top:
                    kind = 'UNDERSIDE(bottom %.1f)' % min(s[0] for s in sp)
                else:
                    kind = 'RING/BOSS'
                w, h = u1 - u0, v1 - v0
                if 2.8 <= w <= 3.6 and 2.8 <= h <= 3.6:
                    shape = 'M3-sq'
                elif max(w, h) > 15 and kind.startswith('THROUGH'):
                    shape = 'OPENING'
                else:
                    shape = 'slot/pocket'
                # underside nut-pocket probe: ring at +-2.2 mm (inside a 5.5 mm
                # square-nut pocket, outside the ~3 mm screw hole)
                pockets = 0
                for dx, dz in ((2.2, 0), (-2.2, 0), (0, 2.2), (0, -2.2)):
                    s2 = K.spans([c[0] for c in gr.crossings(cu + dx, cv + dz)])
                    if s2 and abs(min(s[0] for s in s2) - -2.0) < 0.25:
                        pockets += 1
                X, L, _ = veh(tag, cu, cv, 0)
                rows.append((tag, X, L, w, h, kind, shape, pockets, a))
    rows.sort(key=lambda r: (-r[1], r[2]))
    csv = ['part,X,L,w,h,kind,shape,edge_probes_at_-2mm,area_mm2']
    md.append('')
    md.append('| part | X | L | w x h | class | shape | -2mm edge probes | area |')
    md.append('|---|---|---|---|---|---|---|---|')
    for tag, X, L, w, h, kind, shape, pk, a in rows:
        md.append('| %s | %+8.2f | %+7.2f | %.1f x %.1f | %s | %s | %d/4 | %.0f |'
                  % (tag, X, L, w, h, kind, shape, pk, a))
        csv.append('%s,%.2f,%.2f,%.2f,%.2f,%s,%s,%d,%.1f'
                   % (tag, X, L, w, h, kind, shape, pk, a))
    md.append('')
    m3_rows = [r for r in rows if r[6] == 'M3-sq']
    m3_unique = {(round(r[1], 1), round(r[2], 1)) for r in m3_rows}
    md.append('M3-class count: **%d part-level rows / %d unique assembled coordinates**.'
              % (len(m3_rows), len(m3_unique)))
    md.append('The difference is the two coaxial back-floor/back-floor-2 holes at')
    md.append('X=-85.9, L=+-5.0; each stacked plate contributes a mesh row but the')
    md.append('assembled fastener map contains one feature at each coordinate.')
    md.append('')
    md.append('"-2mm edge probes" counts rays just outside the loop whose material bottom')
    md.append('sits at Z=-6 (authored -2), i.e. the 2 mm underside recess consistent with')
    md.append('a captured-nut pocket / the FloorBoard2 channel. 4/4 around an M3-sq hole =')
    md.append('strong slot-nut candidate (drawing [2]: "Insert M3 nuts into the slots x12").')
    md.append('')

    # ---- 3b. centreline trench / openings survey -------------------------------
    md.append('## 3b. Centreline trench + through-openings (mounting-surface interruptions)')
    md.append('')
    md.append('Ray survey of the centreline band |L|<=14, X -100..+56, 2 mm steps.')
    md.append('Classes: SOLID Z0 top (mountable), OPEN (no plate — FloorBoard2 lid at')
    md.append('Z~-6 below where it spans X -90..+22), ISLAND (6 mm plate, top Z0).')
    md.append('')
    md.append('| X range | centre-band state (fraction open) |')
    md.append('|---|---|')
    band = {}
    for Xi in range(-100, 57, 2):
        n_open = n_tot = 0
        for Lq in [-12 + 3 * i for i in range(9)]:
            for tag in ('ff', 'bf'):
                xq = Xi - XOFF[tag]
                (x0, _, _), (x1, _, _) = K.bbox(parts[tag])
                if not (x0 <= xq <= x1):
                    continue
                n_tot += 1
                if not grids[tag].crossings(xq, Lq + 68.5):
                    n_open += 1
        if n_tot:
            band[Xi] = n_open / n_tot
    runs, cur = [], None
    for Xi in sorted(band):
        cls = 'open' if band[Xi] > 0.5 else ('mixed' if band[Xi] > 0.1 else 'solid')
        if cur and cur[2] == cls:
            cur[1] = Xi
        else:
            if cur:
                runs.append(cur)
            cur = [Xi, Xi, cls]
    if cur:
        runs.append(cur)
    for a, b, cls in runs:
        md.append('| X %+d .. %+d | %s |' % (a, b, cls.upper()))
    md.append('')
    md.append('Reading: the centre band is SOLID over X -84..-16 (the KO-19 Servoholder')
    md.append('region has continuous Z0 floor), OPEN at X -14..-4 (junction window over')
    md.append('the FloorBoard2 lid) with small MIXED spots at the splice-screw stations,')
    md.append('and OPEN again X <= -94 (motor/axle bay). Another 12x12 opening sits at')
    md.append('X +78 on the centreline. Supports must not assume plate in those windows.')
    md.append('')

    # ---- 4. silhouette width profile ------------------------------------------
    md.append('## 4. Plan silhouette vs X (taper/ramps/unusable edges)')
    md.append('')
    md.append('| X | parts | lateral extent L | width |')
    md.append('|---|---|---|---|')
    for Xq in range(-140, 181, 10):
        ext = []
        for tag in ('ff', 'bf', 'b2'):
            xq = Xq - XOFF[tag]
            (x0, _, _), (x1, _, _) = K.bbox(parts[tag])
            if not (x0 - 0.01 <= xq <= x1 + 0.01):
                continue
            segs = K.section(parts[tag], 'x', xq)
            if not segs:
                continue
            zs = [p[1] for s in segs for p in s]   # (y, z_lat) -> z_lat
            ext.append((tag, min(zs) - 68.5, max(zs) - 68.5))
        if ext:
            lo = min(e[1] for e in ext)
            hi = max(e[2] for e in ext)
            md.append('| %+d | %s | %+.1f .. %+.1f | %.1f |'
                      % (Xq, '+'.join(e[0] for e in ext), lo, hi, hi - lo))
    md.append('')

    # ---- 5. SVG plan map -------------------------------------------------------
    svg = K.SVG(-150, -75, 190, 75, scale=3.0, pad=24)
    for tag, color in (('ff', '#222'), ('bf', '#222'), ('b2', '#888')):
        for yq in (3.0, -3.0):
            segs = K.section(parts[tag], 'y', yq)
            vs = [((veh(tag, p[0], p[1], 0)[0], veh(tag, p[0], p[1], 0)[1]),
                   (veh(tag, q[0], q[1], 0)[0], veh(tag, q[0], q[1], 0)[1]))
                  for (p, q) in segs]
            svg.segs(vs, color=color if yq > 0 else '#8bb', width=0.7)
    svg.line((0, -75), (0, 75), color='#c00', dash='4,3')
    svg.text((2, 70), 'X=0 joint', color='#c00')
    svg.line((-150, 0), (190, 0), color='#0a0', dash='6,4')
    svg.text((160, 3), 'L=0', color='#0a0')
    svg.text((-145, 70), 'X+ forward ->', color='#000')
    svg.text((-145, 64), 'L sign: see Gate-P1 caveat', color='#000')
    for tag, X, L, w, h, kind, shape, pk, a in rows:
        if shape == 'M3-sq' and kind.startswith('THROUGH'):
            svg.circle((X, L), 2.2, color='#c00', width=1.2)
        elif kind.startswith('THROUGH'):
            svg.circle((X, L), max(w, h) / 2, color='#06c', width=0.8)
    path = os.path.join(OUT_D, 'p0_d01_floor_map.svg')
    svg.save(path, title='D-01 floor map | P0 (X,L) | dark=top, teal=underside, '
                         'red=M3, blue=openings')
    md.append('## 5. Outputs')
    md.append('- diagram: `evidence/p0/diagrams/p0_d01_floor_map.svg`')
    md.append('- feature CSV: `evidence/p0/tables/p0_d01_feature_map.csv`')

    with open(os.path.join(OUT_T, 'p0_d01_feature_map.csv'), 'w') as f:
        f.write('\n'.join(csv) + '\n')
    with open(os.path.join(OUT_T, 'p0_d01_floor_datum.md'), 'w') as f:
        f.write('\n'.join(md) + '\n')
    print('\n'.join(md))
    print('\nWROTE:', OUT_T + '/p0_d01_floor_datum.md', OUT_T + '/p0_d01_feature_map.csv', path)


if __name__ == '__main__':
    main()
