#!/usr/bin/env python3
"""p0_00_validate_frames.py — Session 4A step 0.

(1) Tool validation: reproduce the bounding boxes recorded in
    01_inventory/inventory.csv (already independently confirmed twice, Sessions
    1 and 1.5) for every model used in P0. Any mismatch > 0.1 mm fails loudly.
(2) Authored-frame inspection: print raw min/max extents to establish each
    model's authored orientation and whether models share an assembly frame.

Run from the repo root. Read-only.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stlkit as K

ROOT = '02_ready_to_slice'

# (path, expected bbox sizes from inventory.csv: x, y, z)
MODELS = [
    ('05_PETG_floor/2023NewFrontFloorLargerParts.stl', (182.0, 8.0, 137.0)),
    ('05_PETG_floor/2023NewBackFloorLargerParts.stl', (116.8, 8.0, 137.0)),
    ('05_PETG_floor/2023NewBackFloorLargerPart2.stl', (74.5, 8.0, 68.0)),
    ('05_PETG_floor/FloorBoard2.stl', (112.6, 2.0, 19.0)),
    ('05_PETG_floor/2023NEWSideVent1.stl', (35.0, 37.3, 19.6)),
    ('05_PETG_floor/2023NEWSideVent2.stl', (35.1, 37.5, 19.6)),
    ('05_PETG_floor/Servoholder.stl', (22.9, 10.0, 58.0)),
    ('06_PLA_body_shell/NEW BODY 2024 FRONT 1.stl', (161.4, 129.2, 54.3)),
    ('06_PLA_body_shell/NEW BODY 2024 REAR.stl', (156.3, 127.3, 73.4)),
    ('06_PLA_body_shell/FRONTNOSE2024.stl', (129.0, 42.0, 127.9)),
    ('06_PLA_body_shell/new halo 2.1.stl', (74.9, 38.8, 24.9)),
    ('03_PETG_front_suspension_steering/Suspension Block_10.stl', (37.0, 37.0, 70.8)),
    ('03_PETG_front_suspension_steering/servosaverv7.stl', (25.3, 26.7, 26.5)),
    ('03_PETG_front_suspension_steering/Steering Block4.stl', (31.0, 17.0, 30.0)),
    ('03_PETG_front_suspension_steering/GuideRod.stl', (6.2, 6.8, 6.2)),
]

TOL = 0.11  # mm — inventory values are rounded to 0.1

ok = True
for rel, exp in MODELS:
    path = os.path.join(ROOT, rel)
    tris = K.load_stl(path)
    bb = K.bbox(tris)
    sizes = tuple(bb[1][i] - bb[0][i] for i in range(3))
    status = ''
    if exp[0] is not None:
        bad = [abs(sizes[i] - exp[i]) > TOL for i in range(3)]
        status = 'OK' if not any(bad) else 'MISMATCH exp=%s' % (exp,)
        ok = ok and not any(bad)
    print('%-55s tris=%6d  %s  %s' % (rel, len(tris), K.fmt_bbox(bb), status))

print()
print('VALIDATION:', 'PASS — all inventory bboxes reproduced' if ok else 'FAIL')
sys.exit(0 if ok else 1)
