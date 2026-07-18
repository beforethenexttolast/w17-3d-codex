#!/usr/bin/env python3
"""p0_06_deckside_slot_map.py — Session 4A, D-27: deck-side (architecture
RIGHT = belt side = L<0 in the P0 frame) mounting-feature map.

Side-naming resolution (P0): the architecture's "right" is DEFINED by the
drivetrain: J places ESC/deck on the motor/belt side. The floor's belt/spur
cutout sits at L<0 (X -98..-117), so architecture-RIGHT = L<0 throughout the
P0 evidence. Whether that side is the driver's right when standing behind
the car is the residual naming check at Gate P1 (p0_02 caveat) — it cannot
change any relative placement.

Consumes p0_d01_feature_map.csv (p0_02 must run first). Adds keep-out
overlays measured this session and emits the D-27 anchor-candidate table.
Run from repo root.
"""
import csv
import os
import sys

OUT_T = '10_assembly_architecture/evidence/p0/tables'
SRC = os.path.join(OUT_T, 'p0_d01_feature_map.csv')

# keep-outs in the P0 frame (this session's measurements)
KO = [
    ('KO-01 rod band', 'X -50..+135, |L|<=18 (rear)..12 (fwd), Z 35..62'),
    ('KO-19 servo+holder', 'X -25..-52 (bracket stations), |L|<=12, Z 0..58'),
    ('belt/spur cutout', 'X -98..-117, L -34..-60 — NO plate (through)'),
    ('joint window', 'X -14..-4 centre |L|<14 OPEN; splice screws to +24'),
    ('motor/axle bay', 'X <= -94 centre — open + rotating (KO-08/09)'),
    ('ESC bay allocation', 'X -60..-90, L -10..-52 (P11) — PS-02 territory'),
    ('vent + shell-lip zone', 'X +27..+62, |L| 41..62 — vent screws + body seat'),
]


def main():
    if not os.path.isfile(SRC):
        raise SystemExit('FATAL: %s missing — run p0_02 first' % SRC)
    rows = list(csv.DictReader(open(SRC)))
    md = ['# p0_06 — D-27 deck-side mounting map (architecture RIGHT = belt side = L<0)', '']
    md.append('Frame: P0 vehicle. Sources: p0_02 feature map + this session\'s keep-outs.')
    md.append('')
    md.append('## Keep-out overlays')
    md.append('')
    for name, desc in KO:
        md.append('- **%s** — %s' % (name, desc))
    md.append('')
    md.append('## Fastener features, deck-relevant band (L +5 .. -60, X +30 .. -100)')
    md.append('')
    md.append('| X | L | feature | usable as | blockers |')
    md.append('|---|---|---|---|---|')
    sel = []
    for r in rows:
        X, L = float(r['X']), float(r['L'])
        if not (-100 <= X <= 30 and -60 <= L <= 5):
            continue
        sel.append((X, L, r))
    sel.sort(key=lambda t: (-t[0], t[1]))
    notes = {
        (7.5, 0.0): ('FloorBoard2 splice screw', 'occupied (splice); centre band'),
        (14.26, 0.0): ('FloorBoard2 splice screw', 'occupied; centre band'),
        (22.69, 0.0): ('FloorBoard2 splice screw', 'occupied; centre band'),
        (-27.76, -13.5): ('rear-floor bracket station (fwd pair)', 'KO-19 candidate seat — VERIFY at dry-fit'),
        (-39.94, -32.86 if False else 17.14): (None, None),
        (-39.99, -32.86): ('single, mid-bay', 'FREE candidate: PS-03 shelf / PS-04 post'),
        (-70.64, -40.25): ('axle-holder row 1', 'occupied (axle holder, 3-position row)'),
        (-70.64, -45.25): ('axle-holder row 2', 'occupied'),
        (-70.64, -50.38): ('axle-holder row 3', 'occupied'),
        (-85.76, -13.5): ('rear bracket station (rear pair)', 'spring-mount territory (Gate A)'),
        (-85.93, -5.0): ('splice/b2 stack bolt', 'occupied (3-layer joint)'),
    }

    def near(d, X, L):
        for (x, l), v in d.items():
            if v[0] and abs(x - X) < 0.6 and abs(l - L) < 0.6:
                return v
        return None

    for X, L, r in sel:
        n = near(notes, X, L)
        use, blk = (n if n else ('unassigned M3-class feature' if r['shape'] == 'M3-sq'
                                 else r['kind'], 'assign at P1 dry-fit'))
        md.append('| %+8.2f | %+7.2f | %s %s %s | %s | %s |'
                  % (X, L, r['part'], r['shape'], r['kind'], use, blk))
    md.append('')
    md.append('## D-27 anchor answers for the T CAD tasks (P0)')
    md.append('')
    md.append('- **PS-03/PS-04/PS-05 (UBEC shelf + deck posts):** the deck-side bay')
    md.append('  X 0..-60, L -15..-50 contains only ONE free fastener feature')
    md.append('  ((-40.0, -32.9)); the bay is otherwise plain 4 mm plate. Supports')
    md.append('  spanning to the centre-band splice screws or clamping the plate edge')
    md.append('  will be needed — the "12-slot" reuse assumption does NOT hold on this')
    md.append('  side: most M3 features are occupied by the donor build or sit in the')
    md.append('  centre band under KO-01/KO-19.')
    md.append('- **PS-15 junction block (Z2R, X +10..+40, L -15..-50):** NO existing')
    md.append('  fastener feature in that patch (plain plate + vent zone outboard).')
    md.append('- **PS-01 battery tray (mirror side, L>0):** same picture mirrored —')
    md.append('  one free single at (-39.9, +17.1); bay otherwise plain.')
    md.append('- Consequence recorded for K/T: the floor M3 slot-nut pattern is NOT a')
    md.append('  12-position free grid; new supports must either share donor screws,')
    md.append('  use the few free singles, or add plate-clamp feet (no new holes in')
    md.append('  donor parts — rule unchanged).')
    md.append('')
    md.append('Status: feature positions DIGITALLY CONFIRMED (mesh-measured, +-0.2);')
    md.append('occupancy hypotheses PARTIALLY RESOLVED (drawing [2] consumers not all')
    md.append('mesh-verified); side naming per header; final free-slot availability =')
    md.append('PHYSICAL CONFIRMATION at the P1 dry-fit (D-27 stays two-stage).')
    with open(os.path.join(OUT_T, 'p0_d27_deckside_map.md'), 'w') as f:
        f.write('\n'.join(md) + '\n')
    print('\n'.join(md))


if __name__ == '__main__':
    main()
