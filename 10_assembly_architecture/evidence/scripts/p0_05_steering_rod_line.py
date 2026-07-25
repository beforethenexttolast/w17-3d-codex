#!/usr/bin/env python3
"""p0_05_steering_rod_line.py — D-09/D-26 steering-servo fit and rod datum.

This supersedes the Session-4A interpretation that treated the 70.8 mm raw-Z
extent of `Suspension Block_10` as vertical.  The floor and block hole patterns
show that the block's raw Y axis is vertical and raw Z is longitudinal.

The script measures only mesh geometry.  Servo dimensions and horn-hole radii
are recorded in the generated report as supplier-drawing inputs, never as STL
measurements.  The real shell seat S0 and installed linkage hardware remain
physical dry-fit measurements at ASM-08.

Run from the repository root.  Source STLs are read-only.  Generated tables are
written under `10_assembly_architecture/evidence/p0/tables/`.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stlkit as K
import p0_03_shell_clearance_sections as shell_sections

OUT_T = '10_assembly_architecture/evidence/p0/tables'
SU = '02_ready_to_slice/03_PETG_front_suspension_steering'
FL = '02_ready_to_slice/05_PETG_floor'
REV = 'unsorted_stl_raw/RC-01 Revision 1.1/New 1.1 Steering Upgrades'


def loop_rows(tris, axis, value, lo=2.8, hi=3.7):
    """Closed near-M3 loops as (centre_u, centre_v, width, height)."""
    rows = []
    for loop in K.assemble_loops(K.section(tris, axis, value)):
        if not K.loop_closed(loop):
            continue
        (u0, v0), (u1, v1) = K.loop_bbox(loop)
        w, h = u1 - u0, v1 - v0
        if lo <= w <= hi and lo <= h <= hi:
            rows.append(((u0 + u1) / 2, (v0 + v1) / 2, w, h))
    return rows


def nearest(rows, u, v):
    return min(rows, key=lambda r: math.hypot(r[0] - u, r[1] - v))


def fmt_spans(spans):
    return ', '.join('%.2f..%.2f' % (a, b) for a, b in spans)


def main():
    os.makedirs(OUT_T, exist_ok=True)

    floor = K.load_stl(os.path.join(FL, '2023NewFrontFloorLargerParts.stl'))
    holder = K.load_stl(os.path.join(FL, 'Servoholder.stl'))
    tower = K.load_stl(os.path.join(SU, 'Suspension Block_10.stl'))
    saver = K.load_stl(os.path.join(SU, 'servosaverv7.stl'))
    rev_floor = K.load_stl(os.path.join(
        REV, 'NewFrontFloorSuspensionUpgrade REVISION_1.1.stl'))
    rev_holder = K.load_stl(os.path.join(REV, 'New Steering Servo Holder.stl'))

    # ---- Original Servoholder: supplier drawing installs raw X vertically,
    # raw Z longitudinally and raw Y as its 10 mm thickness.
    hbb = K.bbox(holder)
    hp = K.section(holder, 'y', 0.0)
    leg_spans = K.spans(K.scanline(hp, 0, -10.0))  # z material at raw x=-10
    inner_w = leg_spans[1][0] - leg_spans[0][1]
    inner_h = 1.0 - hbb[0][0]  # bridge begins at raw x=+1.0
    outer_h = hbb[1][0] - hbb[0][0]
    outer_w = hbb[1][2] - hbb[0][2]
    thickness = hbb[1][1] - hbb[0][1]

    # The 58 mm holder span matches the two repeated rear-floor stations.
    # This fixes a useful station estimate but not the unmeshed clamp/servo
    # seating tolerance; the supplier drawing remains the orientation source.
    holder_x0, holder_x1 = -85.76, -27.76
    holder_xc = (holder_x0 + holder_x1) / 2
    servo_body_x0, servo_body_x1 = holder_xc - 20.0, holder_xc + 20.0
    # Output shaft is 10 mm from either end of a standard 40 mm case.  The
    # body end carrying the output boss is expected forward, but the physical
    # dry-fit pins that fore/aft choice. The shaft axis itself is lateral.
    servo_shaft_x_fwd = servo_body_x1 - 10.0
    servo_shaft_x_rev = servo_body_x0 + 10.0

    # ---- Tower registration: match its four raw-(x,z) vertical holes to the
    # original front floor's four raw-(x,z) holes.  Floor vehicle transform is
    # X=raw_x+89, L=raw_z-68.5, Z=raw_y-4.
    floor_holes = loop_rows(floor, 'y', 3.9)
    tower_holes = loop_rows(tower, 'y', -9.0)
    matches = []
    for tx, tz in ((0.0, 10.0), (0.0, 20.0), (-7.8, 25.0), (7.8, 25.0)):
        th = nearest(tower_holes, tx, tz)
        target_floor_raw_x = 109.39 + tz - 89.0
        target_floor_raw_z = 68.5 + tx
        fh = nearest(floor_holes, target_floor_raw_x, target_floor_raw_z)
        floor_X, floor_L = fh[0] + 89.0, fh[1] - 68.5
        matches.append((th[0], th[1], floor_X, floor_L,
                        floor_X - th[1], floor_L - th[0]))
    x_offsets = [r[4] for r in matches]
    l_offsets = [r[5] for r in matches]
    tower_xoff = sum(x_offsets) / len(x_offsets)
    tower_loff = sum(l_offsets) / len(l_offsets)
    registration_residual = max(
        max(x_offsets) - min(x_offsets), max(l_offsets) - min(l_offsets))

    # Saver pivot boss is the annulus at tower raw (x=0,z=-31.3).  Probe its
    # top surface at x=+2, clear of the D3 bore.
    tower_side = K.section(tower, 'x', 2.0)
    boss_spans_y = K.spans(K.scanline(tower_side, 1, -31.3))
    boss_top_raw_y = max(b for a, b in boss_spans_y)
    boss_X = tower_xoff - 31.3
    boss_L = tower_loff
    boss_top_Z = boss_top_raw_y - 4.0

    # ---- Saver bores and printed plate levels.
    saver_holes = loop_rows(saver, 'z', 19.0)
    pivot_samples = [nearest(loop_rows(saver, 'z', z), -0.35, -43.80)
                     for z in (0.1, 1.0, 5.0, 10.0, 15.0, 20.0, 25.0, 26.4)]
    pivot = pivot_samples[4]
    pivot_dim_spread = max(
        max(row[i] for row in pivot_samples) - min(row[i] for row in pivot_samples)
        for i in (2, 3))
    forward_l = nearest(saver_holes, -6.18, -26.79)
    forward_r = nearest(saver_holes, 5.80, -26.79)
    side = nearest(saver_holes, -13.65, -43.89)
    sg = K.ZRayGrid(saver, cell=4.0)
    front_plate_spans = [(a[0], b[0]) for a, b in
                         K.spans(sg.crossings(forward_l[0] + 2.0, forward_l[1]))]
    side_plate_spans = [(a[0], b[0]) for a, b in
                        K.spans(sg.crossings(side[0] + 2.0, side[1]))]
    front_gap_centre_local = (front_plate_spans[0][1] + front_plate_spans[1][0]) / 2
    front_gap_centre_Z = boss_top_Z + front_gap_centre_local
    saver_top_Z = boss_top_Z + K.bbox(saver)[1][2]

    # Translate saver plan using its pivot.  The side input arm points laterally;
    # the paired forward holes point toward the front of the car.
    def saver_vehicle(raw_x, raw_y):
        return (boss_X + (raw_y - pivot[1]), boss_L + (raw_x - pivot[0]))

    side_X, side_L = saver_vehicle(side[0], side[1])
    fwd_l_X, fwd_l_L = saver_vehicle(forward_l[0], forward_l[1])
    fwd_r_X, fwd_r_L = saver_vehicle(forward_r[0], forward_r[1])

    # ---- Shell lower-bound ceilings at the likely holder/shaft stations.
    shell = shell_sections.load_assembled()
    sample_xs = (round(holder_xc), round(servo_shaft_x_fwd))
    sample_ls = (0, 10, 20, 26, 30)
    ceilings = []
    for x in sample_xs:
        segs = K.section(shell, 'x', float(x))
        row = []
        for lat in sample_ls:
            pos = shell_sections.ceil_profile(segs, float(lat))
            neg = shell_sections.ceil_profile(segs, float(-lat)) if lat else pos
            row.append((pos, neg))
        ceilings.append((x, row))

    # ---- Rev-1.1 floor/holder delta.
    def large_opening(tris, target_w, target_h):
        best = None
        for loop in K.assemble_loops(K.section(tris, 'y', 3.9)):
            if not K.loop_closed(loop):
                continue
            (a, b), (c, d) = K.loop_bbox(loop)
            w, h = c - a, d - b
            score = abs(w - target_w) + abs(h - target_h)
            if best is None or score < best[0]:
                best = (score, w, h, (a + c) / 2, (b + d) / 2)
        return best[1:]

    orig_open = large_opening(floor, 12.1, 12.1)
    rev_open = large_opening(rev_floor, 40.5, 20.0)
    rev_bb = K.bbox(rev_holder)

    md = [
        '# p0_05 — D-09/D-26 steering-servo fit + linkage datum (corrected)',
        '',
        'All Z values are above DAT-F (floor top). Shell ceilings use S0=0 and are',
        'therefore lower bounds until the real body-seat offset S0 is measured.',
        '',
        '## 1. Verified mesh facts',
        '',
        '### Original `Servoholder`',
        '',
        '- mesh bbox: %.2f x %.2f x %.2f mm (raw x/y/z)' % (
            outer_h, thickness, outer_w),
        '- supplier-drawing assembly orientation: raw x = vertical, raw z =',
        '  longitudinal, raw y = 10 mm lateral thickness',
        '- assembled outer arch: %.2f long x %.2f high x %.2f thick; clear arch' % (
            outer_w, outer_h, thickness),
        '  opening: %.2f long x %.2f high' % (inner_w, inner_h),
        '- this is intended around the 40 x 20 mm *side-face* envelope of a',
        '  standard servo: the intended shaft is horizontal, not vertical;',
        '  40 mm fits the 42 mm span, but 20 mm has 1.5 mm nominal interference',
        '  with the 18.5 mm arch, so the real case requires a no-force fit check',
        '',
        '### `Suspension Block_10` registration',
        '',
        '- four tower/floor M3 centres reproduce one transform with max spread',
        '  %.3f mm: X = %.3f + tower_raw_z; L = %.3f + tower_raw_x;' % (
            registration_residual, tower_xoff, tower_loff),
        '  Z = tower_raw_y - 4.000',
        '- block assembly height is raw-y -10..27 => Z -14..23; its 70.79 mm',
        '  raw-z extent is LONGITUDINAL, not vertical',
        '- saver pivot boss: X %.2f, L %.2f; printed top surface Z %.2f' % (
            boss_X, boss_L, boss_top_Z),
        '',
        '### `servosaverv7`',
        '',
        '- central bore: %.2f x %.2f mm at eight sections from Z 0.1..26.4' % (
            pivot[2], pivot[3]),
        '  (dimension spread <%.6f mm), through the full 26.50 mm height; this is' % (
            pivot_dim_spread),
        '  an M3 pivot bore, not a 25T spline socket',
        '- paired forward-hole printed plate spans (local Z): %s; clear-gap' % (
            fmt_spans(front_plate_spans)),
        '  centre: local Z %.2f => vehicle Z %.2f' % (
            front_gap_centre_local, front_gap_centre_Z),
        '- side input-hole material spans (local Z): %s; external ball-joint' % (
            fmt_spans(side_plate_spans)),
        '  centre height depends on the unmeshed bolt/spacer/rod end',
        '- saver printed top: Z %.2f' % saver_top_Z,
        '- input side hole plan centre: X %.2f, L %.2f' % (side_X, side_L),
        '- paired forward holes: X %.2f, L %.2f / %.2f' % (
            (fwd_l_X + fwd_r_X) / 2, fwd_l_L, fwd_r_L),
        '',
        '## 2. Body-to-floor clearance at the original holder station',
        '',
        '| X | ceil L0 | ceil +L10/-L10 | +L20/-L20 | +L26/-L26 | +L30/-L30 |',
        '|---:|---:|---:|---:|---:|---:|',
    ]
    for x, row in ceilings:
        cells = []
        for pos, neg in row:
            if pos is None and neg is None:
                cells.append('open/open')
            elif pos == neg:
                cells.append('%.1f' % pos)
            else:
                cells.append('%s/%s' % (
                    'open' if pos is None else '%.1f' % pos,
                    'open' if neg is None else '%.1f' % neg))
        md.append('| %+.0f | %s | %s | %s | %s | %s |' % tuple([x] + cells))
    md += [
        '',
        'The shell is a narrow high spine over low shoulders: a single "45 mm',
        'crown" number is not a valid servo envelope. The shaft-up DS3235SG',
        '40.4 mm drawing height has little/no margin at |L| about 10 and cannot',
        'carry another 26.5 mm printed part. In the intended side mount, the',
        'servo is about 20 mm high and the holder top is Z 22.89.',
        '',
        '## 3. Servo/horn/rod assumptions still requiring the physical dry-fit',
        '',
        '- likely holder span: X %.2f..%.2f (58 mm repeated floor-station pitch);' % (
            holder_x0, holder_x1),
        '  DS body centred in the 42 mm opening: X %.2f..%.2f' % (
            servo_body_x0, servo_body_x1),
        '- shaft-centre X is %.2f if the output-boss end of the body is forward,' % (
            servo_shaft_x_fwd),
        '  or %.2f if the body is reversed end-for-end;' % (
            servo_shaft_x_rev),
        '  supplier drawing + physical placement must pin the choice',
        '- floor-seated side mount gives shaft centre Z about 10.0; the DS3235',
        '  optional horn drawing has holes at radius 19.5/23.5 mm. A vertical',
        '  neutral horn therefore puts the long-rod joint near Z 29.5 or 33.5.',
        '- the saver paired-link gap centre is verified at Z %.2f; the input' % (
            front_gap_centre_Z),
        '  rod-end centre is not present in the STL. Conservative provisional',
        '  KO-01 pending ASM-08: **X -80..+100, Z 22..38, |L| <= 22**.',
        '- ASM-08 must record shaft centre, selected horn hole, rod-end spacers,',
        '  neutral/left/right Z and L, and minimum shell/neighbour gap.',
        '',
        '## 4. Rev-1.1 incompatibility with the locked oil-shock front',
        '',
        '- original front-floor opening: %.1f x %.1f at vehicle X %.1f, L %.1f' % (
            orig_open[0], orig_open[1], orig_open[2] + 89.0, orig_open[3] - 68.5),
        '- Rev-1.1 opening: %.1f x %.1f at vehicle X %.1f, L %.1f' % (
            rev_open[0], rev_open[1], rev_open[2] + 89.0, rev_open[3] - 68.5),
        '- Rev-1.1 holder bbox: %.1f x %.1f x %.1f' % (
            rev_bb[1][0] - rev_bb[0][0], rev_bb[1][1] - rev_bb[0][1],
            rev_bb[1][2] - rev_bb[0][2]),
        '- original block longitudinal range after registration: X %.1f..%.1f;' % (
            tower_xoff + K.bbox(tower)[0][2], tower_xoff + K.bbox(tower)[1][2]),
        '  it overlaps the Rev-1.1 servo opening. The holder is not a drop-in',
        '  adapter; it requires the Rev-1.1 floor and steering architecture.',
        '',
        '## Status',
        '',
        '- holder/tower/saver/floor relative geometry: GEOMETRICALLY DERIVED',
        '- shell ceilings at S0=0: DIGITALLY CONFIRMED lower bounds',
        '- supplier servo/horn dimensions: DOCUMENTED, not mesh-derived',
        '- installed servo/rod absolute line and sweep: PHYSICAL CONFIRMATION',
        '  REQUIRED at ASM-08',
    ]

    full_path = os.path.join(OUT_T, 'p0_d09_d26_steering_servo_fit.md')
    with open(full_path, 'w') as f:
        f.write('\n'.join(md) + '\n')

    summary = [
        '# p0_05 — D-26 steering-rod datum (corrected summary)', '',
        '> Supersedes the earlier Z 35..62 result. Full evidence:',
        '> `p0_d09_d26_steering_servo_fit.md`.', '',
        '- `Suspension Block_10` raw Y is vertical; raw Z is longitudinal.',
        '- Saver boss top: X %.2f, L %.2f, Z %.2f.' % (boss_X, boss_L, boss_top_Z),
        '- Saver paired-link gap centre: Z %.2f; printed top: Z %.2f.' % (
            front_gap_centre_Z, saver_top_Z),
        '- Original holder is a %.2f x %.2f mm upright arch around the servo' % (
            outer_w, outer_h),
        '  side face; shaft is horizontal. A floor-seated DS3235SG shaft is',
        '  about Z 10; its vertical horn puts the rod joint around Z 29.5/33.5',
        '  for the documented 19.5/23.5 mm horn holes.',
        '- Provisional KO-01 until ASM-08: **X -80..+100, Z 22..38, |L| <= 22**.',
        '- Absolute rod centre/sweep remains PHYSICAL CONFIRMATION REQUIRED.',
    ]
    with open(os.path.join(OUT_T, 'p0_d26_rod_line.md'), 'w') as f:
        f.write('\n'.join(summary) + '\n')
    print('\n'.join(md))


if __name__ == '__main__':
    main()
