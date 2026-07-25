# ZS · Original suspension and F104 rolling fit study

Date: 2026-07-23  
Locked front: Ryan's original oil-shock assembly. Rev-1 and Rev-1.1 front
steering/suspension parts remain excluded.

---

## 1. Recommendation

Use the original front uprights/knuckles with the received shock set, but do
not production-print the wheel/suspension batch until one front wheel coupon
closes the tyre bead, both MR128 bearing seats, mirrored hub and M3 king-pin
interfaces. Then perform a body-on full steer+bump test.

The requested front length is 51 mm while `HARDWARE_INVENTORY` calls the
received set “52 mm” and explicitly leaves 51-vs-52 as a fit item. Both are
**DOCUMENTED** statements; neither verifies the physical eye-to-eye length.
D-12/D-37 must resolve it with calipers.

The shell registration gives only ≈3.5 mm around a Ø64 front tyre and ≈4 mm
around a Ø64 rear tyre (**DERIVED**). Both are below the general 8 mm moving
policy, so motion—not static appearance—owns acceptance.

## 2. Datums and confidence

- Front and rear axle X=+146.1 / −90.9, wheelbase 237 mm are **DERIVED**.
- Tamiya tyre Ø64×30 front and Ø64×35 rear are **DOCUMENTED** by the
  [official F104 specification](https://www.tamiya.com/english/products/58652/index.html).
- Ride height 5–6 mm is an **ASSUMPTION** tuning start. With 32 mm tyre radius,
  axle Z=26…27 is **DERIVED from that ASSUMPTION**.
- L=±75 front and ±72.5 rear, ±25° steer and Z22…34 wheel-centre travel reserve
  are **ASSUMPTION** pending dry assembly.
- Raw printed bboxes are **VERIFIED**; installed transforms/bore fits are not.

## 3. Component envelopes

| Item | Envelope | Confidence |
|---|---:|---|
| front shocks ×2 | 51 mm requirement / 52 mm stock label; eye-to-eye/body Ø/stroke unknown | DOCUMENTED conflict / ASSUMPTION physical |
| original uprights L/R | each 56.86×20×49.99 raw bbox | VERIFIED |
| `Steering Block4` knuckles | 31×17×29.99 raw bbox | VERIFIED |
| M3 king pins ×2 | Ø3×30 mm | DOCUMENTED |
| front rims | Ø44 bead family×30 wide raw bbox | VERIFIED |
| rear rims | Ø47.01×35.55 raw bbox | VERIFIED |
| front-right hub source | 27.99×63.96×55.95 raw bbox | VERIFIED; multi-axis raw |
| front tyres | Ø64×30 | DOCUMENTED |
| rear tyres | Ø64×35 | DOCUMENTED |
| front MR128 bearings ×4 | 8 ID×12 OD×3.5 | DOCUMENTED |
| rear 6801 bearings ×2 | 12 ID×21 OD×5 | DOCUMENTED; rear study |

The raw hub/upright bboxes are not installed envelopes; they include authored
orientation and possibly separated geometry.

## 4. Ride height, travel and moving envelopes

At 5–6 mm assumed floor ground clearance, wheel axes sit Z=26…27. Reserve wheel
centre Z22…34 until real shock stroke/ratio is measured (**ASSUMPTION**). That
produces a conservative tyre vertical envelope from Z=−10 to +66 at maximum
bump centre, referenced to DAT-F.

For a Ø64×30 front tyre at ±25° assumed steer, rotating the 32 mm radius/15 mm
half-width rectangle gives plan half-extents:

- X half-envelope = 32 cos25° + 15 sin25° = **35.3 mm**;
- L half-envelope = 32 sin25° + 15 cos25° = **27.1 mm**.

Both are **DERIVED from ASSUMPTION steer angle**. Physical lock may be different.
Thus the provisional front wheel keep-out at each centre is X±35.3,
L±27.1, plus the Z travel above. Tie rods, arms, shock bodies and the steering
envelope from Y must be swept simultaneously.

## 5. Shell, neighbour and ground clearances

- Front shell arch: ≈3.5 mm around the registered Ø64 tyre (**DERIVED lower
  bound/context**, not a full 3D bump clearance).
- Rear arch: ≈4 mm around Ø64 (**DERIVED**).
- Ground: target floor 5–6 mm, but front wing/diffuser may be lower; measure the
  lowest printed point separately (**ASSUMPTION target**).
- Require no tyre rub at full steer+bump and ≥2 mm practical wheel-to-static
  clearance after flex (**ASSUMPTION exception to the general 8 mm corridor,
  because the donor arch is already tighter**). Any rub is a fail, not permission
  to sand a tyre.
- Shock spring/body, arms and tie rods need ≥3 mm to shell at all motion
  (**ASSUMPTION minimum**) and no binding at full droop.

## 6. Mounting and interfaces

- Press two MR128 bearings coaxially in each front hub/knuckle stack; load only
  the bearing outer race during insertion. No adhesive before coupon verdict.
- Mirror the right hub in the slicer for the left, then remeasure both Ø12 seats.
- King pin must enter the printed 3 mm bore without splitting and rotate freely
  after circlip installation. Ream only under a logged tolerance correction.
- Shocks mount through their real eye bushings with M3 hardware/spacers that do
  not side-load the eye. Do not pull an eye into alignment by tightening.
- Tyres are glued only after one complete dry bead fit and wheel runout check.
- Rear adapters and sleeves are assembled under the rear drivetrain gate.

## 7. Mass and balance

D-30 reserves 110–160 g for two front wheel/tyre assemblies, 130–190 g for two
rear assemblies and 100–160 g for front printed suspension/shocks
(all **ASSUMPTION**). Unsprung mass differences affect response and cross-weight;
weigh each completed corner. Match left/right front assemblies and left/right
rear assemblies within 2 g (**ASSUMPTION target**) before adding chassis ballast.

## 8. Assembly and fit gates

1. Caliper shock free eye-to-eye, fully compressed length, body/spring OD,
   bushing width and usable stroke.
2. Slicer-measure king-pin bore and mirrored hub seats; print the one-wheel coupon.
3. Record bearing insertion force/fit, tyre bead fit and wheel radial/lateral runout.
4. Assemble both original front corners at 5–6 mm starting ride height.
5. Body on: sweep left/right through bump/droop, record tyre/body, shock/body and
   arm/body minimums; repeat rear bump.
6. Set final ride height and corner weights only with full running mass.

## 9. Remaining assumptions / stop conditions

Stop for cracked bearing seats, bearing preload, king-pin bind, circlip interference,
tyre bead mismatch, >1 mm visible wheel runout (**ASSUMPTION threshold**), shock
side-load, spring/body rub, tyre/body contact or any ground contact at static
ride height. Do not substitute Rev-1/1.1 front files to cure a local fit.
