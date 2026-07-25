# p0_05 — D-09/D-26 steering-servo fit + linkage datum (corrected)

All Z values are above DAT-F (floor top). Shell ceilings use S0=0 and are
therefore lower bounds until the real body-seat offset S0 is measured.

## 1. Verified mesh facts

### Original `Servoholder`

- mesh bbox: 22.89 x 10.00 x 58.00 mm (raw x/y/z)
- supplier-drawing assembly orientation: raw x = vertical, raw z =
  longitudinal, raw y = 10 mm lateral thickness
- assembled outer arch: 58.00 long x 22.89 high x 10.00 thick; clear arch
  opening: 42.00 long x 18.50 high
- this is intended around the 40 x 20 mm *side-face* envelope of a
  standard servo: the intended shaft is horizontal, not vertical;
  40 mm fits the 42 mm span, but 20 mm has 1.5 mm nominal interference
  with the 18.5 mm arch, so the real case requires a no-force fit check

### `Suspension Block_10` registration

- four tower/floor M3 centres reproduce one transform with max spread
  0.025 mm: X = 109.389 + tower_raw_z; L = -0.002 + tower_raw_x;
  Z = tower_raw_y - 4.000
- block assembly height is raw-y -10..27 => Z -14..23; its 70.79 mm
  raw-z extent is LONGITUDINAL, not vertical
- saver pivot boss: X 78.09, L -0.00; printed top surface Z 10.50

### `servosaverv7`

- central bore: 2.90 x 2.97 mm at eight sections from Z 0.1..26.4
  (dimension spread <0.000001 mm), through the full 26.50 mm height; this is
  an M3 pivot bore, not a 25T spline socket
- paired forward-hole printed plate spans (local Z): 9.44..10.94, 18.72..20.22; clear-gap
  centre: local Z 14.83 => vehicle Z 25.33
- side input-hole material spans (local Z): 13.12..16.00, 16.12..18.87, 19.00..21.87; external ball-joint
  centre height depends on the unmeshed bolt/spacer/rod end
- saver printed top: Z 37.00
- input side hole plan centre: X 78.01, L -13.30
- paired forward holes: X 95.10, L -5.83 / 6.15

## 2. Body-to-floor clearance at the original holder station

| X | ceil L0 | ceil +L10/-L10 | +L20/-L20 | +L26/-L26 | +L30/-L30 |
|---:|---:|---:|---:|---:|---:|
| -57 | 62.3 | 41.1/41.2 | 37.6 | 22.2/22.3 | 19.2/19.1 |
| -47 | 63.9 | 43.1 | 38.1 | 37.6 | 21.1/20.7 |

The shell is a narrow high spine over low shoulders: a single "45 mm
crown" number is not a valid servo envelope. The shaft-up DS3235SG
40.4 mm drawing height has little/no margin at |L| about 10 and cannot
carry another 26.5 mm printed part. In the intended side mount, the
servo is about 20 mm high and the holder top is Z 22.89.

## 3. Servo/horn/rod assumptions still requiring the physical dry-fit

- likely holder span: X -85.76..-27.76 (58 mm repeated floor-station pitch);
  DS body centred in the 42 mm opening: X -76.76..-36.76
- shaft-centre X is -46.76 if the output-boss end of the body is forward,
  or -66.76 if the body is reversed end-for-end;
  supplier drawing + physical placement must pin the choice
- floor-seated side mount gives shaft centre Z about 10.0; the DS3235
  optional horn drawing has holes at radius 19.5/23.5 mm. A vertical
  neutral horn therefore puts the long-rod joint near Z 29.5 or 33.5.
- the saver paired-link gap centre is verified at Z 25.33; the input
  rod-end centre is not present in the STL. Conservative provisional
  KO-01 pending ASM-08: **X -80..+100, Z 22..38, |L| <= 22**.
- ASM-08 must record shaft centre, selected horn hole, rod-end spacers,
  neutral/left/right Z and L, and minimum shell/neighbour gap.

## 4. Rev-1.1 incompatibility with the locked oil-shock front

- original front-floor opening: 12.1 x 12.1 at vehicle X 78.1, L 0.0
- Rev-1.1 opening: 40.5 x 20.0 at vehicle X 70.8, L 0.0
- Rev-1.1 holder bbox: 37.9 x 38.0 x 32.9
- original block longitudinal range after registration: X 70.6..141.4;
  it overlaps the Rev-1.1 servo opening. The holder is not a drop-in
  adapter; it requires the Rev-1.1 floor and steering architecture.

## Status

- holder/tower/saver/floor relative geometry: GEOMETRICALLY DERIVED
- shell ceilings at S0=0: DIGITALLY CONFIRMED lower bounds
- supplier servo/horn dimensions: DOCUMENTED, not mesh-derived
- installed servo/rod absolute line and sweep: PHYSICAL CONFIRMATION
  REQUIRED at ASM-08
