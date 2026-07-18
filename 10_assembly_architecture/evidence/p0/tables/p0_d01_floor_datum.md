# p0_02 — D-01 floor datum & feature map (generated; frame: P0 vehicle frame)

All coordinates in the P0 vehicle frame (X fwd, L lateral from centreline,
Z up, Z=0 at DAT-F floor top). Lateral LEFT/RIGHT naming: see sign caveat
in the script header — |L| exact, side naming PARTIALLY RESOLVED.

## 1. Front<->rear floor joint (tongue & groove)
- Front-floor rear edge: full-thickness butt face at authored x=-89.0;
  wedge tongue x -89.0..-91.0 (profile y [1.0, 3.0] at x=-90.0).
- Back-floor forward edge: butt face x=+1.16 with matching wedge groove
  (opening y [0.0, 0.36, 3.65, 4.0] at x=+0.8, z_lat=30).
- Mated registration: x_ff = x_bf - 90.15 (+-0.2, cross-checked by the
  FloorBoard2 hole span 93.6 mm landing on both plates within 0.2 mm).
- Joint interface plane defined as X = 0.

## 2. Floor-top datum (DAT-F) verification + thickness classes
- 4 mm-grid ray survey over both plates: every sampled solid point tops at
  authored y=+4.00 (deviations >0.15 mm: 68 of 2516 samples — all at outer
  edge chamfers / the joint edge, none in a mounting region)
- => DAT-F is ONE continuous flat plane over front+back floors: Z=0. DIGITALLY CONFIRMED.
- Thickness classes, bucketed to 1 mm (front floor): {'0': 1, '1': 2, '2': 38, '3': 3, '4': 469, '5': 15, '6': 59, '7': 22, '8': 98, 'open': 823}
  (back floor: {'4': 349, '5': 24, '6': 122, '7': 23, '8': 245, 'open': 223})
- 4.0 = plain plate (underside at Z-4); ~6 = underside 2 mm recess zones
  (FloorBoard2 channel / nut pockets); 8.0 = full-depth zones (centre spine
  block, outboard skirts) reaching Z-8. Top face flat everywhere -> ribs,
  recesses and skirts are all UNDERSIDE features; the mounting surface is
  uninterrupted EXCEPT at through-openings.
  - deviation: ff (-89.0, 2.0) top=0.00
  - deviation: ff (-89.0, 6.0) top=0.00
  - deviation: ff (-89.0, 14.0) top=2.58
  - deviation: ff (-89.0, 58.0) top=0.00
  - deviation: ff (-89.0, 62.0) top=0.00
  - deviation: ff (-89.0, 66.0) top=0.00
  - deviation: ff (-89.0, 70.0) top=0.00
  - deviation: ff (-89.0, 74.0) top=0.00
  - deviation: ff (-89.0, 78.0) top=0.00
  - deviation: ff (-89.0, 86.0) top=2.58
  - deviation: ff (-89.0, 134.0) top=0.00
  - deviation: ff (-53.0, 10.0) top=2.54

## 3. Feature map (classified loops; vehicle coords)

| part | X | L | w x h | class | shape | -2mm edge probes | area |
|---|---|---|---|---|---|---|---|
| ff |  +159.99 |   +0.02 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| ff |  +134.40 |   +7.79 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| ff |  +134.39 |   -7.80 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| ff |  +129.39 |   +0.00 | 3.2 x 3.2 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| ff |  +119.39 |   +0.00 | 3.3 x 3.2 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| ff |   +78.11 |   +0.00 | 12.1 x 12.1 | THROUGH(edge) | slot/pocket | 4/4 | 114 |
| ff |   +64.24 |   +0.00 | 3.0 x 3.1 | THROUGH | M3-sq | 0/4 | 7 |
| ff |   +57.50 |   +0.00 | 3.0 x 3.0 | THROUGH | M3-sq | 0/4 | 7 |
| ff |   +43.55 |  -41.51 | 3.2 x 3.2 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| ff |   +43.55 |  +41.40 | 3.2 x 3.2 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| ff |   +39.18 |  -55.71 | 13.1 x 10.3 | THROUGH(edge) | slot/pocket | 0/4 | 50 |
| ff |   +39.18 |  +55.71 | 13.1 x 10.3 | THROUGH(edge) | slot/pocket | 0/4 | 50 |
| ff |   +37.15 |  -41.51 | 3.4 x 3.4 | THROUGH(edge) | M3-sq | 0/4 | 9 |
| ff |   +37.12 |  +41.50 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| ff |   +34.36 |   -0.00 | 68.7 x 44.4 | UNDERSIDE(bottom -2.0) | slot/pocket | 4/4 | 1469 |
| ff |   +28.71 |  -63.67 | 57.4 x 9.7 | UNDERSIDE(bottom -0.7) | slot/pocket | 0/4 | 199 |
| ff |   +28.71 |  +63.67 | 57.4 x 9.7 | UNDERSIDE(bottom -0.7) | slot/pocket | 0/4 | 199 |
| ff |   +22.69 |   +0.00 | 3.0 x 3.0 | THROUGH(edge) | M3-sq | 4/4 | 7 |
| ff |   +14.26 |   +0.00 | 3.1 x 3.1 | THROUGH(edge) | M3-sq | 4/4 | 7 |
| ff |    +7.50 |   +0.00 | 3.0 x 3.0 | THROUGH(edge) | M3-sq | 4/4 | 7 |
| bf |   -27.76 |  -13.50 | 3.0 x 3.0 | THROUGH | M3-sq | 0/4 | 7 |
| bf |   -27.76 |  +16.50 | 3.0 x 3.0 | THROUGH | M3-sq | 0/4 | 7 |
| bf |   -39.94 |  +17.14 | 3.1 x 3.1 | THROUGH | M3-sq | 0/4 | 8 |
| bf |   -39.99 |  -32.86 | 3.0 x 3.0 | THROUGH(edge) | M3-sq | 0/4 | 7 |
| bf |   -46.55 |   +0.00 | 92.8 x 66.3 | UNDERSIDE(bottom -2.0) | slot/pocket | 4/4 | 3703 |
| bf |   -51.53 |  -63.23 | 73.1 x 10.5 | UNDERSIDE(bottom -1.5) | slot/pocket | 1/4 | 282 |
| bf |   -51.57 |  +63.20 | 73.2 x 10.6 | UNDERSIDE(bottom -1.5) | slot/pocket | 1/4 | 282 |
| bf |   -70.64 |  -50.38 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 9 |
| bf |   -70.64 |  -45.25 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 9 |
| bf |   -70.64 |  +45.25 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 9 |
| bf |   -70.64 |  +50.37 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 9 |
| bf |   -70.65 |  +40.25 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| bf |   -70.65 |  -40.25 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| b2 |   -80.18 |  -30.75 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| b2 |   -80.18 |  +30.75 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| bf |   -85.76 |  -13.50 | 3.0 x 3.0 | THROUGH | M3-sq | 0/4 | 7 |
| bf |   -85.76 |  +16.50 | 3.0 x 3.0 | THROUGH | M3-sq | 0/4 | 7 |
| bf |   -85.93 |   -5.00 | 3.0 x 3.0 | THROUGH(edge) | M3-sq | 4/4 | 7 |
| bf |   -85.93 |   +5.00 | 3.0 x 3.0 | THROUGH(edge) | M3-sq | 4/4 | 7 |
| b2 |   -85.93 |   -5.00 | 3.0 x 3.0 | THROUGH | M3-sq | 0/4 | 7 |
| b2 |   -85.93 |   +5.00 | 3.0 x 3.0 | THROUGH | M3-sq | 0/4 | 7 |
| b2 |  -129.43 |  -29.00 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| b2 |  -129.43 |  +29.00 | 3.3 x 3.3 | THROUGH(edge) | M3-sq | 0/4 | 8 |
| b2 |  -136.68 |   -0.00 | 3.3 x 3.3 | THROUGH | M3-sq | 0/4 | 8 |

M3-class count: **35 part-level rows / 33 unique assembled coordinates**.
The difference is the two coaxial back-floor/back-floor-2 holes at
X=-85.9, L=+-5.0; each stacked plate contributes a mesh row but the
assembled fastener map contains one feature at each coordinate.

"-2mm edge probes" counts rays just outside the loop whose material bottom
sits at Z=-6 (authored -2), i.e. the 2 mm underside recess consistent with
a captured-nut pocket / the FloorBoard2 channel. 4/4 around an M3-sq hole =
strong slot-nut candidate (drawing [2]: "Insert M3 nuts into the slots x12").

## 3b. Centreline trench + through-openings (mounting-surface interruptions)

Ray survey of the centreline band |L|<=14, X -100..+56, 2 mm steps.
Classes: SOLID Z0 top (mountable), OPEN (no plate — FloorBoard2 lid at
Z~-6 below where it spans X -90..+22), ISLAND (6 mm plate, top Z0).

| X range | centre-band state (fraction open) |
|---|---|
| X -100 .. -94 | OPEN |
| X -92 .. -88 | SOLID |
| X -86 .. -86 | MIXED |
| X -84 .. -16 | SOLID |
| X -14 .. -4 | OPEN |
| X -2 .. +0 | MIXED |
| X +2 .. +6 | SOLID |
| X +8 .. +8 | MIXED |
| X +10 .. +12 | SOLID |
| X +14 .. +14 | MIXED |
| X +16 .. +20 | SOLID |
| X +22 .. +24 | MIXED |
| X +26 .. +56 | SOLID |

Reading: the centre band is SOLID over X -84..-16 (the KO-19 Servoholder
region has continuous Z0 floor), OPEN at X -14..-4 (junction window over
the FloorBoard2 lid) with small MIXED spots at the splice-screw stations,
and OPEN again X <= -94 (motor/axle bay). Another 12x12 opening sits at
X +78 on the centreline. Supports must not assume plate in those windows.

## 4. Plan silhouette vs X (taper/ramps/unusable edges)

| X | parts | lateral extent L | width |
|---|---|---|---|
| -140 | b2 | -34.0 .. +34.0 | 68.0 |
| -130 | b2 | -34.0 .. +34.0 | 68.0 |
| -120 | b2 | -34.0 .. +34.0 | 68.0 |
| -110 | bf+b2 | -56.1 .. +56.0 | 112.1 |
| -100 | bf+b2 | -59.4 .. +59.4 | 118.8 |
| -90 | bf+b2 | -62.0 .. +62.0 | 124.0 |
| -80 | bf+b2 | -64.1 .. +64.1 | 128.2 |
| -70 | bf+b2 | -65.9 .. +65.9 | 131.8 |
| -60 | bf | -67.2 .. +67.2 | 134.3 |
| -50 | bf | -68.0 .. +68.0 | 135.9 |
| -40 | bf | -68.4 .. +68.4 | 136.8 |
| -30 | bf | -68.5 .. +68.5 | 137.0 |
| -20 | bf | -68.5 .. +68.5 | 137.0 |
| -10 | bf | -53.5 .. +53.5 | 107.0 |
| +0 | ff+bf | -68.5 .. +68.5 | 137.0 |
| +10 | ff | -68.5 .. +68.5 | 137.0 |
| +20 | ff | -68.5 .. +68.5 | 137.0 |
| +30 | ff | -68.5 .. +68.5 | 137.0 |
| +40 | ff | -67.7 .. +67.7 | 135.4 |
| +50 | ff | -65.4 .. +65.4 | 130.9 |
| +60 | ff | -26.4 .. +26.4 | 52.9 |
| +70 | ff | -24.7 .. +24.7 | 49.3 |
| +80 | ff | -23.0 .. +23.0 | 46.1 |
| +90 | ff | -21.5 .. +21.5 | 43.0 |
| +100 | ff | -20.1 .. +20.1 | 40.2 |
| +110 | ff | -18.8 .. +18.8 | 37.6 |
| +120 | ff | -17.6 .. +17.6 | 35.2 |
| +130 | ff | -16.6 .. +16.6 | 33.1 |
| +140 | ff | -15.6 .. +15.6 | 31.3 |
| +150 | ff | -14.8 .. +14.8 | 29.6 |
| +160 | ff | -14.1 .. +14.1 | 28.2 |
| +170 | ff | -13.5 .. +13.5 | 27.0 |
| +180 | ff | -13.0 .. +13.0 | 26.0 |

## 5. Outputs
- diagram: `evidence/p0/diagrams/p0_d01_floor_map.svg`
- feature CSV: `evidence/p0/tables/p0_d01_feature_map.csv`
