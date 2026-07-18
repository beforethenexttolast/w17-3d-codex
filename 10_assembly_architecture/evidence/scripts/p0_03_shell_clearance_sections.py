#!/usr/bin/env python3
"""p0_03_shell_clearance_sections.py — Session 4A: D-02 clearance profile,
D-04 airbox channel, D-03 sidepod pockets (+ the shell<->floor registration
they all depend on).

SHELL REGISTRATION (derived this session; see V report §D-01/D-02):
  * The two 2024 shells are authored in one frame; they BUTT edge-to-edge:
    the rear shell translates by -67.47 so its forward edge (x=181.96) meets
    the front shell's rear edge (x=114.49).
  * Longitudinal: vehicle X = 146.6 - x_front_shell_frame  (front-arch gap
    then brackets a D64 front tyre at X=+146.1 with ~3.5 mm margins, the
    rear-arch gap brackets a D64 tyre at X=-90.9 with ~4 mm margins, and the
    wheelbase lands at 237 mm — three independent consistency checks).
  * Lateral: L = -(y_shell - 1.855)  (shell centreline y=1.855; the sign
    choice matches the floor's L convention — |L| exact, side naming per the
    p0_02 caveat).
  * Vertical: WORKING REGISTRATION S0 = 0: shell bottom-edge plane (both
    shells z=0) = DAT-F. The flanks rest on the floor plate; if the real seat
    is higher every ceiling below only grows. GEOMETRICALLY DERIVED /
    PARTIALLY RESOLVED — confirm at first body-on dry-fit (Gate P1/P3).

All outputs in the P0 vehicle frame (X fwd, L lateral, Z above DAT-F).
Run from repo root. Read-only on models.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stlkit as K

SH = '02_ready_to_slice/06_PLA_body_shell'
OUT_T = '10_assembly_architecture/evidence/p0/tables'
OUT_S = '10_assembly_architecture/evidence/p0/sections'

C = 146.6          # X = C - x_shell (front-shell frame)
REAR_SHIFT = -67.47
YC = 1.855         # shell lateral centre


def load_assembled():
    f = os.path.join(SH, 'NEW BODY 2024 FRONT 1.stl')
    r = os.path.join(SH, 'NEW BODY 2024 REAR.stl')
    for p in (f, r):
        if not os.path.isfile(p):
            raise SystemExit('FATAL: missing %s (run from repo root)' % p)
    tris = K.load_stl(f) + K.translate(K.load_stl(r), REAR_SHIFT, 0, 0)
    # to vehicle frame: X = C - x ; L = -(y - YC) ; Z = z
    return K.apply(tris, lambda v: (C - v[0], -(v[1] - YC), v[2]))


def ceil_profile(section_segs, L, zmin=2.0):
    """Lowest material crossing above zmin on the vertical line at L
    (transverse section coords are (L, Z)). None = no roof over this L."""
    zs = [z for z in K.scanline(section_segs, 0, L) if z > zmin]
    return min(zs) if zs else None


def width_at(section_segs, Z):
    """Interior width at height Z: innermost crossings either side of L=0."""
    ls = K.scanline(section_segs, 1, Z)
    neg = [l for l in ls if l < 0]
    pos = [l for l in ls if l > 0]
    if not neg or not pos:
        return None, None, None
    return max(neg), min(pos), min(pos) - max(neg)


def main():
    os.makedirs(OUT_T, exist_ok=True)
    os.makedirs(OUT_S, exist_ok=True)
    tris = load_assembled()
    md = []
    md.append('# p0_03 — D-02 body-to-floor clearance profile, D-04 airbox, D-03 sidepods')
    md.append('')
    md.append('Frame: P0 vehicle (X fwd, L lateral, Z above DAT-F). Vertical registration')
    md.append('S0=0 (shell bottom edge = DAT-F) — every ceiling is a LOWER BOUND if the')
    md.append('real seat is higher. Raw ceilings; policy clearance 5 mm static (I.1) is')
    md.append('NOT subtracted in the "raw" column.')
    md.append('')

    # ---------------- D-02 transverse stations --------------------------------
    stations = [
        (150, 'nose beam / front axle'), (120, 'nose beam, tower zone'),
        (90, 'front shell fwd taper'), (60, 'cockpit hump'),
        (40, 'front bay / shell joint zone'), (20, 'Z2 rear (front bay)'),
        (0, 'junction Z3 (joint plane)'), (-20, 'Z3 core (battery/UBEC)'),
        (-40, 'Z3/Z5 boundary'), (-60, 'Z5 / airbox mid'),
        (-80, 'ESC bay Z5R'), (-100, 'motor / rear axle'), (-120, 'tail'),
    ]
    md.append('## D-02 — transverse clearance stations')
    md.append('')
    md.append('| X | zone | ceil @L0 | @|L|=20 | @|L|=30 | @|L|=40 | @|L|=50 | width @Z15 | @Z25 | @Z35 | @Z45 |')
    md.append('|---|---|---|---|---|---|---|---|---|---|---|')
    rows_csv = [['X', 'zone', 'ceil_L0', 'ceil_L20', 'ceil_L30', 'ceil_L40',
                 'ceil_L50', 'w_Z15', 'w_Z25', 'w_Z35', 'w_Z45']]
    for X, zone in stations:
        segs = K.section(tris, 'x', float(X))
        if not segs:
            md.append('| %+d | %s | — no shell — | | | | | | | | |' % (X, zone))
            rows_csv.append([X, zone] + [''] * 9)
            continue
        cs = []
        for Lq in (0.0, 20.0, 30.0, 40.0, 50.0):
            a = ceil_profile(segs, +Lq)
            b = ceil_profile(segs, -Lq) if Lq else a
            both = [v for v in (a, b) if v is not None]
            cs.append('%.0f/%.0f' % (a if a else -1, b if b else -1) if Lq and (a or b)
                      else ('%.0f' % both[0] if both else '—'))
        ws = []
        for Zq in (15.0, 25.0, 35.0, 45.0):
            _, _, w = width_at(segs, Zq)
            ws.append('%.0f' % w if w else '—')
        md.append('| %+d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |'
                  % tuple([X, zone] + cs + ws))
        rows_csv.append([X, zone] + [v.replace('—', '') for v in cs + ws])
        # per-station SVG
        (u0, v0), (u1, v1) = ((-70, -5), (70, 80))
        svg = K.SVG(u0, v0, u1, v1, scale=4.0)
        svg.segs(segs, color='#222', width=1.0)
        svg.line((-70, 0), (70, 0), color='#0a0', width=1.2)
        svg.text((-68, 76), 'X=%+d %s (L right-to-left per sign caveat)' % (X, zone), size=9)
        for Zq in (25, 45):
            svg.line((-70, Zq), (70, Zq), color='#ccc', dash='2,3')
        svg.save(os.path.join(OUT_S, 'p0_d02_X%+04d.svg' % X),
                 title='D-02 transverse section X=%+d — %s (Z above DAT-F, S0=0)' % (X, zone))
    md.append('')
    md.append('Ceiling cells "a/b": +L side / -L side. "-1" = no roof at that L (open')
    md.append('cockpit / arch / beyond wall). Width = interior span across L=0 at height Z.')
    md.append('')

    # ---------------- longitudinal sections -----------------------------------
    for Lq in (0.0, 25.0, -25.0, 45.0, -45.0):
        segs = K.section(tris, 'y', Lq)
        svg = K.SVG(-140, -5, 200, 85, scale=2.6)
        svg.segs(segs, color='#222', width=0.9)
        svg.line((-140, 0), (200, 0), color='#0a0', width=1.2)
        svg.text((-135, 80), 'longitudinal L=%+.0f (X fwd right; Z above DAT-F)' % Lq, size=9)
        svg.save(os.path.join(OUT_S, 'p0_d02_long_L%+03d.svg' % int(Lq)),
                 title='D-02 longitudinal section L=%+.0f' % Lq)

    # ---------------- D-04 airbox channel -------------------------------------
    md.append('## D-04 — airbox / tall-channel width by station')
    md.append('')
    md.append('Channel = lateral span where the ceiling is >= the given height.')
    md.append('')
    md.append('| X | span ceil>=45 | span ceil>=50 | span ceil>=60 | max ceil (L of max) |')
    md.append('|---|---|---|---|---|')
    for X in (30, 20, 10, 0, -10, -20, -30, -40, -50, -60, -70, -80):
        segs = K.section(tris, 'x', float(X))
        if not segs:
            continue
        prof = []
        for i in range(-60, 61):
            c = ceil_profile(segs, float(i))
            prof.append((float(i), c))
        cells = []
        for h in (45.0, 50.0, 60.0):
            ls = [l for l, c in prof if c is not None and c >= h]
            cells.append('%.0f..%.0f (%.0f)' % (min(ls), max(ls), max(ls) - min(ls)) if ls else '—')
        vals = [(c, l) for l, c in prof if c is not None]
        mx = max(vals) if vals else (None, None)
        md.append('| %+d | %s | %s | %s | %.1f (L=%+.0f) |'
                  % (X, cells[0], cells[1], cells[2], mx[0], mx[1]))
    md.append('')

    # ---------------- D-03 sidepod pockets ------------------------------------
    md.append('## D-03 — sidepod pocket survey (|L| 35..62, low heights)')
    md.append('')
    md.append('| X | side | wall inner |L| at Z10 | at Z20 | ceil at |L|=45 | ceil at |L|=55 |')
    md.append('|---|---|---|---|---|---|')
    for X in (20, 0, -20, -40, -60, -80):
        segs = K.section(tris, 'x', float(X))
        if not segs:
            continue
        for sgn, name in ((1, '+L'), (-1, '-L')):
            walls = []
            for Zq in (10.0, 20.0):
                ls = [l * sgn for l in K.scanline(segs, 1, Zq)]
                inner = min([l for l in ls if l > 15], default=None)
                walls.append('%.0f' % inner if inner else '—')
            c45 = ceil_profile(segs, sgn * 45.0)
            c55 = ceil_profile(segs, sgn * 55.0)
            md.append('| %+d | %s | %s | %s | %s | %s |'
                      % (X, name, walls[0], walls[1],
                         '%.0f' % c45 if c45 else '—', '%.0f' % c55 if c55 else '—'))
    md.append('')
    md.append('Outputs: per-station SVGs in `evidence/p0/sections/` (p0_d02_X*.svg,')
    md.append('p0_d02_long_L*.svg); CSV `p0_d02_stations.csv`.')

    with open(os.path.join(OUT_T, 'p0_d02_stations.csv'), 'w', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows(rows_csv)
    with open(os.path.join(OUT_T, 'p0_d02_d03_d04_clearance.md'), 'w') as f:
        f.write('\n'.join(md) + '\n')
    print('\n'.join(md))


if __name__ == '__main__':
    main()
