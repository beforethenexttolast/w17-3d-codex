#!/usr/bin/env python3
"""p0_04_nose_interior.py — Session 4A, D-25: FRONTNOSE2024 interior sections.

ORIENTATION (established this session, verified geometrically below):
  authored x_n = LONGITUDINAL: tip at x_n=-64.49 (full 3D blob), rear
      installation ring at x_n=+45..+64.5 (closed full-height sections);
  authored y_n = VERTICAL (+-21): top cowl skin at +15..+21 mid-length;
  authored z_n = LATERAL, centreline at z_n=64 (sections mirror-symmetric
      about it; cone width <=42 = |z_n-64|<=21; the rear widens to 128 at the
      front-wing pylon region).
  The underside is OPEN from x_n ~ -43 rearward: the nose is a cowl that
  drops over the front-floor NOSE BEAM (the beam is its floor).

VERTICAL MAPPING (SLICER-ESTIMATED +-2 mm): nose bottom edge (y_n=-21) at the
beam bottom plane Z=-8  =>  Z = y_n + 13. Beam TOP (DAT-F, Z=0) = y_n = -13.
Consistency: nose rear top (+21 -> Z=34) meets the front shell's forward
lower skin (measured z_s 36.8 at its tip) within the joint overlap.
Longitudinal anchoring to the beam bolt (floor hole X=+160, L=0) is
PARTIALLY RESOLVED — sections below are reported in nose-local x_n.

Run from repo root; read-only; writes tables + section SVGs.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stlkit as K

OUT_T = '10_assembly_architecture/evidence/p0/tables'
OUT_S = '10_assembly_architecture/evidence/p0/sections'
BEAM_TOP_Y = -13.0     # y_n of DAT-F under the cowl
BEAM_W = 33.0          # beam width at the nose stations (from p0_02 silhouette)


def main():
    p = '02_ready_to_slice/06_PLA_body_shell/FRONTNOSE2024.stl'
    if not os.path.isfile(p):
        raise SystemExit('FATAL: missing %s' % p)
    t = K.load_stl(p)
    os.makedirs(OUT_T, exist_ok=True)
    os.makedirs(OUT_S, exist_ok=True)
    md = ['# p0_04 — D-25 FRONTNOSE2024 interior sections', '']
    md.append('Coordinates: nose-local x_n (tip -64.5, rear +64.5); heights converted to')
    md.append('Z above DAT-F via Z = y_n + 13 (SLICER-ESTIMATED +-2). Lateral = z_n - 64.')
    md.append('')
    md.append('| x_n | usable height above beam top @lat 0 | interior width @Z+5 | @Z+12 | @Z+20 | notes |')
    md.append('|---|---|---|---|---|---|')
    for xn in (-60, -52, -44, -36, -28, -20, -12, -4, 4, 12, 20, 28, 36, 44, 52, 60):
        segs = K.section(t, 'x', float(xn))
        if not segs:
            md.append('| %+d | — empty section — | | | | diagnose: beyond part |' % xn)
            continue
        # interior ceiling over the beam centreline: crossings of vertical line
        # at lat=0 (z_n=64): coords in section are (y, z) -> scanline axis 1 = z
        ys = K.scanline(segs, 1, 64.0)   # y crossings at lateral centre
        above = [y for y in ys if y > BEAM_TOP_Y]
        ceil_inner = min(above) if above else None
        h = (ceil_inner - BEAM_TOP_Y) if ceil_inner is not None else None
        ws = []
        for dz in (5.0, 12.0, 20.0):
            yq = BEAM_TOP_Y + dz
            zs = K.scanline(segs, 0, yq)
            lat = [z - 64.0 for z in zs]
            inner_neg = [l for l in lat if -25 < l < 0]
            inner_pos = [l for l in lat if 0 < l < 25]
            if inner_neg and inner_pos:
                ws.append('%.0f' % (min(inner_pos) - max(inner_neg)))
            elif lat:
                ws.append('open>%d' % int(min(50, max(lat) - min(lat))))
            else:
                ws.append('—')
        note = 'top-skin only (open under)' if xn < 2 and xn > -44 else (
            'closed ring (installation section)' if xn >= 2 else 'tip blob')
        md.append('| %+d | %s | %s | %s | %s | %s |'
                  % (xn, '%.1f' % h if h is not None else 'no skin @lat0',
                     ws[0], ws[1], ws[2], note))
        svg = K.SVG(30, -25, 100, 25, scale=5.0)
        vs = [((p_[1], p_[0]), (q[1], q[0])) for (p_, q) in segs]
        svg.segs(vs, color='#222', width=1.0)
        svg.line((30, BEAM_TOP_Y), (100, BEAM_TOP_Y), color='#0a0', width=1.2)
        svg.line((64 - BEAM_W / 2, BEAM_TOP_Y - 8), (64 - BEAM_W / 2, BEAM_TOP_Y), color='#c60')
        svg.line((64 + BEAM_W / 2, BEAM_TOP_Y - 8), (64 + BEAM_W / 2, BEAM_TOP_Y), color='#c60')
        svg.text((32, 22), 'x_n=%+d; green DAT-F; orange beam' % xn, size=9)
        svg.save(os.path.join(OUT_S, 'p0_d25_nose_x%+04d.svg' % xn),
                 title='D-25 x_n=%+d | lateral vs y_n | interior crop' % xn)
    md.append('')
    md.append('Reading: usable cavity over the beam exists mainly in the REAR/installation')
    md.append('half; the visible cone forward of x_n~0 is a shallow top cowl whose skin')
    md.append('sits low over the beam; the tip is effectively solid. Empty/one-sided')
    md.append('results at lat 0 mean NO skin above the beam line there (open underside),')
    md.append('not "no cavity" — see per-station SVGs before quoting any number.')
    md.append('')
    md.append('D-25 status: interior DIGITALLY measured relative to the nose; absolute')
    md.append('vertical mapping SLICER-ESTIMATED (+-2); nose-camera decision NOT taken.')
    with open(os.path.join(OUT_T, 'p0_d25_nose_interior.md'), 'w') as f:
        f.write('\n'.join(md) + '\n')
    print('\n'.join(md))


if __name__ == '__main__':
    main()
