# p0_03 — D-02 body-to-floor clearance profile, D-04 airbox, D-03 sidepods

Frame: P0 vehicle (X fwd, L lateral, Z above DAT-F). Vertical registration
S0=0 (shell bottom edge = DAT-F) — every ceiling is a LOWER BOUND if the
real seat is higher. Raw ceilings; policy clearance 5 mm static (I.1) is
NOT subtracted in the "raw" column.

## D-02 — transverse clearance stations

| X | zone | ceil @L0 | @|L|=20 | @|L|=30 | @|L|=40 | @|L|=50 | width @Z15 | @Z25 | @Z35 | @Z45 |
|---|---|---|---|---|---|---|---|---|---|---|
| +150 | nose beam / front axle | 37 | — | — | — | — | — | — | — | — |
| +120 | nose beam, tower zone | 42 | 37/37 | — | — | — | — | — | — | — |
| +90 | front shell fwd taper | 42 | 42/42 | 3/3 | 29/29 | — | 52 | 52 | 88 | — |
| +60 | cockpit hump | 42 | 42/42 | 40/40 | 40/40 | 41/41 | 103 | 115 | 124 | 27 |
| +40 | front bay / shell joint zone | — | — | — | — | 7/7 | 109 | 122 | — | — |
| +20 | Z2 rear (front bay) | 53 | 41/41 | 33/33 | 32/32 | 9/9 | 110 | 122 | 59 | 34 |
| +0 | junction Z3 (joint plane) | 71 | 40/40 | 30/29 | 28/28 | 33/33 | 115 | 121 | 59 | 33 |
| -20 | Z3 core (battery/UBEC) | 68 | 39/39 | 26/26 | 25/24 | 2/2 | 115 | 60 | 59 | 28 |
| -40 | Z3/Z5 boundary | 65 | 38/38 | 23/22 | 22/21 | 6/6 | 109 | 59 | 59 | 17 |
| -60 | Z5 / airbox mid | 62 | 37/37 | 19/19 | 19/19 | 12/12 | 72 | 49 | 48 | 17 |
| -80 | ESC bay Z5R | 58 | — | — | — | — | — | — | 33 | 15 |
| -100 | motor / rear axle | 55 | — | — | — | — | — | — | 26 | 11 |
| -120 | tail | 52 | — | — | — | — | — | — | — | 10 |

Ceiling cells "a/b": +L side / -L side. "-1" = no roof at that L (open
cockpit / arch / beyond wall). Width = interior span across L=0 at height Z.

## D-04 — airbox / tall-channel width by station

Channel = lateral span where the ceiling is >= the given height.

| X | span ceil>=45 | span ceil>=50 | span ceil>=60 | max ceil (L of max) |
|---|---|---|---|---|
| +30 | -19..19 (38) | -15..15 (30) | -8..8 (16) | 72.6 (L=+4) |
| +20 | -17..17 (34) | -13..13 (26) | — | 53.4 (L=+6) |
| +10 | -16..16 (32) | -12..12 (24) | -2..2 (4) | 70.1 (L=+2) |
| +0 | -16..16 (32) | -11..10 (21) | -2..2 (4) | 71.2 (L=-1) |
| -10 | -14..14 (28) | -6..6 (12) | -3..3 (6) | 69.5 (L=-1) |
| -20 | -13..13 (26) | -6..6 (12) | -3..3 (6) | 68.0 (L=+0) |
| -30 | -11..11 (22) | -7..7 (14) | -4..4 (8) | 66.4 (L=+0) |
| -40 | -8..8 (16) | -6..6 (12) | -5..5 (10) | 64.9 (L=+0) |
| -50 | -8..8 (16) | -6..6 (12) | -5..4 (9) | 63.3 (L=+0) |
| -60 | -8..8 (16) | -6..6 (12) | -4..2 (6) | 61.7 (L=+0) |
| -70 | -7..7 (14) | -6..6 (12) | 0..0 (0) | 60.1 (L=+0) |
| -80 | -7..7 (14) | -5..6 (11) | — | 58.3 (L=-1) |

## D-03 — sidepod pocket survey (|L| 35..62, low heights)

| X | side | wall inner |L| at Z10 | at Z20 | ceil at |L|=45 | ceil at |L|=55 |
|---|---|---|---|---|---|
| +20 | +L | 47 | 59 | 34 | 9 |
| +20 | -L | 47 | 59 | 34 | 9 |
| +0 | +L | 54 | 60 | 30 | 7 |
| +0 | -L | 54 | 60 | 30 | 7 |
| -20 | +L | 55 | 59 | 27 | 6 |
| -20 | -L | 55 | 59 | 27 | 6 |
| -40 | +L | 53 | 55 | 24 | 8 |
| -40 | -L | 53 | 55 | 25 | 8 |
| -60 | +L | 49 | 27 | 22 | — |
| -60 | -L | 49 | 27 | 22 | — |
| -80 | +L | — | — | — | — |
| -80 | -L | — | — | — | — |

Outputs: per-station SVGs in `evidence/p0/sections/` (p0_d02_X*.svg,
p0_d02_long_L*.svg); CSV `p0_d02_stations.csv`.
