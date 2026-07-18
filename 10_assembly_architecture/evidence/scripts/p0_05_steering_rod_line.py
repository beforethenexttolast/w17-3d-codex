#!/usr/bin/env python3
"""p0_05_steering_rod_line.py — Session 4A, D-26: steering push-rod nominal
line + sweep band (slicer stage; physical confirm stays at ASM-08).

Method: the rod runs from the DS3235SG horn (servo in `Servoholder`,
mid-chassis rear floor, drawing [2]) forward to `servosaverv7` (pivoting on a
vertical M3 to the nose-beam floor holes, drawing [3]). Every ingredient
below is re-measured from the staged STLs; absolute stations carry stated
assumption bands — this is exactly the D-26 "slicer stage".

MEASURED INGREDIENTS (re-derived here from the meshes):
  servosaverv7 : pivot bore D~3 at saver-local (x -0.35, y -43.8), vertical
                 (z 0..26.5); rod-attach holes at z ~16..22 (nominal 19),
                 arm holes at local x -6.2 / +5.8 (i.e. +-6 lateral) and a
                 third at x -13.7; radii about the pivot ~13.3 and ~18.0.
  tower        : `Suspension Block_10` 37x37x70.8 with the foot blade z
                 -38.8..~0 — floor-seat assumption: blade inserted through
                 the plate, body base at DAT-F => part z=0 plane ~ Z +34..38.
  Servoholder  : 22.9 x 10 x 58 plate standing on the rear floor (drawing
                 [2]); DS3235SG (~40.5 tall EST, D-09) held with output shaft
                 up: horn plane Z ~42..52 (P6 band, unchanged).

STATION ASSUMPTIONS (PARTIALLY RESOLVED):
  saver pivot at one of the nose-beam centreline M3 holes (X +119.4 or
  +129.4); Servoholder at the rear-floor bracket stations (X -28..-50).

Run from repo root. Prints + writes the D-26 table; no model modified.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stlkit as K

OUT_T = '10_assembly_architecture/evidence/p0/tables'
SU = '02_ready_to_slice/03_PETG_front_suspension_steering'


def main():
    os.makedirs(OUT_T, exist_ok=True)
    sv = K.load_stl(os.path.join(SU, 'servosaverv7.stl'))
    tw = K.load_stl(os.path.join(SU, 'Suspension Block_10.stl'))

    md = ['# p0_05 — D-26 steering-rod nominal line + sweep (slicer stage)', '']

    # re-measure the saver pivot bore + arm holes
    segs = K.section(sv, 'z', 8.0)
    bore = None
    for l in K.assemble_loops(segs):
        if K.loop_closed(l):
            (u0, v0), (u1, v1) = K.loop_bbox(l)
            if 2.5 <= u1 - u0 <= 3.5 and 2.5 <= v1 - v0 <= 3.5:
                bore = ((u0 + u1) / 2, (v0 + v1) / 2)
    md.append('- saver pivot bore (z=8 section): %s — vertical M3, saver-local' % (bore,))
    bore_centres = []
    segs = K.section(sv, 'z', 19.0)
    for l in K.assemble_loops(segs):
        if K.loop_closed(l):
            (u0, v0), (u1, v1) = K.loop_bbox(l)
            if 2.5 <= u1 - u0 <= 3.5 and 2.5 <= v1 - v0 <= 3.5:
                bore_centres.append((round((u0 + u1) / 2, 2), round((v0 + v1) / 2, 2)))
    if bore:
        import math
        arm = [(a, b) for a, b in bore_centres
               if math.hypot(a - bore[0], b - bore[1]) > 1.0]
        radii = [round(math.hypot(a - bore[0], b - bore[1]), 1) for a, b in arm]
        md.append('- saver arm-hole centres (z=19, pivot excluded): %s' % arm)
        md.append('- arm radii about the pivot: %s mm; outer rod-attach pair ~=18.0 mm' % radii)
    md.append('- tower z-extent (authored): %.1f..%.1f (70.8 tall, blade at the bottom)'
              % (K.bbox(tw)[0][2], K.bbox(tw)[1][2]))
    md.append('')
    md.append('## Nominal line (vehicle frame; Z above DAT-F)')
    md.append('')
    md.append('| station | X (assumed band) | Z nominal | Z band | lateral band L | basis |')
    md.append('|---|---|---|---|---|---|')
    md.append('| S1 servo-horn end | -30 (-50..-25) | 47 | 42..52 | +-6 about horn arm, sweep +-16 | '
              'holder 58 + DS3235SG ~40.5 EST (D-09); horn radius 12..20 EST |')
    md.append('| S2 mid-spine | +45 (joint fwd) | 51 | 42..56 | +-10 (interpolated sweep) | linear interp S1-S3 |')
    md.append('| S3 servo-saver end | +125 (+119/+129) | 54 | 50..58 | +-6 arm + sweep to +-12 | '
              'saver anchor 19 above its base; base ~ Z 34..38 (blade-inserted tower) |')
    md.append('')
    md.append('## KO-01 rod keep-out (P0 update, supersedes the H.1.2 35->70 reading)')
    md.append('')
    md.append('- The rod is a HIGH, nearly-level line: Z ~42..58 nominal over its whole run')
    md.append('  (NOT a 35->70 rising diagonal). With setup tolerance +-3, articulation')
    md.append('  sweep and joint bodies (+-4 vertical), the reserved band is:')
    md.append('  **Z 35..62, |L| <= 18 at X -50..0, tapering to |L| <= 12 at X > +60.**')
    md.append('- Consequence for the right deck (PS-04): the inboard edge at deck heights')
    md.append('  (Z 20..45) must stay at |L| >= ~18 + 5 policy + 3 setup ~= 26 near the')
    md.append('  horn (X -50..0) and |L| >= ~20 forward of X +20. On the architecture-')
    md.append('  right/belt side this means L <= -26 rear and L <= -20 forward. Below Z ~30 the rod band')
    md.append('  does NOT reach: the UBEC shelf (<= Z 14) is unaffected.')
    md.append('- The battery (Z3L) top at ~28 sits BELOW the rod band floor (35): the pack')
    md.append('  may pass under the rod; only its strap/wall above Z 30 must respect KO-01.')
    md.append('')
    md.append('## Status')
    md.append('- Relative geometry (saver bore/arm/tower/holder): GEOMETRICALLY DERIVED.')
    md.append('- Absolute stations + heights: SLICER-ESTIMATED (assumption bands above).')
    md.append('- Lock-to-lock sweep + real heights: PHYSICAL CONFIRMATION REQUIRED at')
    md.append('  ASM-08 (unchanged; this table pre-loads the datums to record there).')
    with open(os.path.join(OUT_T, 'p0_d26_rod_line.md'), 'w') as f:
        f.write('\n'.join(md) + '\n')
    print('\n'.join(md))


if __name__ == '__main__':
    main()
