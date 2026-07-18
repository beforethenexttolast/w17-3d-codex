# p0_05 — D-26 steering-rod nominal line + sweep (slicer stage)

- saver pivot bore (z=8 section): (-0.35097581148147583, -43.80256271362305) — vertical M3, saver-local
- saver arm-hole centres (z=19, pivot excluded): [(-6.18, -26.79), (5.8, -26.79), (-13.65, -43.89)]
- arm radii about the pivot: [18.0, 18.1, 13.3] mm; outer rod-attach pair ~=18.0 mm
- tower z-extent (authored): -38.8..32.0 (70.8 tall, blade at the bottom)

## Nominal line (vehicle frame; Z above DAT-F)

| station | X (assumed band) | Z nominal | Z band | lateral band L | basis |
|---|---|---|---|---|---|
| S1 servo-horn end | -30 (-50..-25) | 47 | 42..52 | +-6 about horn arm, sweep +-16 | holder 58 + DS3235SG ~40.5 EST (D-09); horn radius 12..20 EST |
| S2 mid-spine | +45 (joint fwd) | 51 | 42..56 | +-10 (interpolated sweep) | linear interp S1-S3 |
| S3 servo-saver end | +125 (+119/+129) | 54 | 50..58 | +-6 arm + sweep to +-12 | saver anchor 19 above its base; base ~ Z 34..38 (blade-inserted tower) |

## KO-01 rod keep-out (P0 update, supersedes the H.1.2 35->70 reading)

- The rod is a HIGH, nearly-level line: Z ~42..58 nominal over its whole run
  (NOT a 35->70 rising diagonal). With setup tolerance +-3, articulation
  sweep and joint bodies (+-4 vertical), the reserved band is:
  **Z 35..62, |L| <= 18 at X -50..0, tapering to |L| <= 12 at X > +60.**
- Consequence for the right deck (PS-04): the inboard edge at deck heights
  (Z 20..45) must stay at |L| >= ~18 + 5 policy + 3 setup ~= 26 near the
  horn (X -50..0) and |L| >= ~20 forward of X +20. On the architecture-
  right/belt side this means L <= -26 rear and L <= -20 forward. Below Z ~30 the rod band
  does NOT reach: the UBEC shelf (<= Z 14) is unaffected.
- The battery (Z3L) top at ~28 sits BELOW the rod band floor (35): the pack
  may pass under the rod; only its strap/wall above Z 30 must respect KO-01.

## Status
- Relative geometry (saver bore/arm/tower/holder): GEOMETRICALLY DERIVED.
- Absolute stations + heights: SLICER-ESTIMATED (assumption bands above).
- Lock-to-lock sweep + real heights: PHYSICAL CONFIRMATION REQUIRED at
  ASM-08 (unchanged; this table pre-loads the datums to record there).
