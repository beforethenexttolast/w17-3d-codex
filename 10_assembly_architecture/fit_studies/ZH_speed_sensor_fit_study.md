# ZH · Rear-axle Hall speed-sensor fit study

Date: 2026-07-23  
Scope: A3144 pickup and one Ø3×1 mm magnet, one pulse per rear-axle revolution.

---

## 1. Recommendation

Use an adjustable ASA bracket on the selected rear bearing carrier, with the
A3144 sensitive face aimed at a mechanically pocketed/bonded Ø3×1 mm magnet on
a shaft collar. Start at 1.5 mm cold face gap and verify reliable switching
through 1–3 mm by hand rotation (**ASSUMPTION test range**). Do not glue the
magnet directly to a smooth high-speed shaft without a pocket or collar.

PS-16 remains blocked until Gate A fixes the carrier, the physical magnet
arrives, the shaft/collar runout is known and D-38 passes.

## 2. Datums and confidence

- Rear axle station X=−90.9 is **DERIVED**.
- Axle Z=26…27 follows the assumed 5–6 mm ride height and is **DERIVED from
  ASSUMPTION**.
- Sensor/magnet L coordinate and bracket transform are **ASSUMPTION**.
- A3144 UA body 4.04–4.17×2.97–3.10×1.47–1.57 mm is **DOCUMENTED** by the
  [Allegro A3141–A3144 datasheet](https://www.allegromicro.com/~/media/Files/Datasheets/A3141-2-3-4-Datasheet.ashx?la=en).
- Magnet Ø3×1 is **DOCUMENTED** by BOM; its actual field/grade is unknown.
- No Hall-bracket, collar or magnet-retention geometry is **VERIFIED** from a
  physical article or mesh; Gate A and D-38 must create that evidence.

## 3. Envelopes

| Item | Body | Installed envelope | Confidence |
|---|---:|---|---|
| A3144 | max 4.17×3.10×1.57 mm body | leads, heatshrink, bracket and 0.5 mm adjustment steps | DOCUMENTED body / ASSUMPTION bracket |
| magnet | Ø3×1 mm | pocket/collar, adhesive fillet and rotational sweep | DOCUMENTED body / ASSUMPTION retention |
| gap | target 1.5 mm; test 1–3 mm | includes axle play, bracket flex and thermal change | ASSUMPTION |

The Hall package's 15+ mm leads are not part of its body bbox and require
strain relief; do not bend them at the epoxy body.

## 4. Placement and moving clearance

Candidate sensor coordinate: X=−90.9, belt-side collar L TBD, sensitive face
near Z=26…27 (**X DERIVED; L/Z ASSUMPTION**). The magnet rotates at the same
station. Its complete swept volume is the collar OD plus adhesive/pocket, not
only Ø3 mm.

Require ≥2 mm from the bracket to the rotating collar/magnet everywhere except
the controlled sensor face gap (**ASSUMPTION**), and ≥8 mm to belt, spur, wheel
adapter, shock and their moving envelopes. The lead exits forward along H-08,
never across the belt or axle.

## 5. Mounting and fasteners

- Bracket material ASA due to motor/axle heat.
- Attach to the finally selected carrier with a clip/shared M3 screw; no new
  hole in a donor carrier. Add 0.5 mm shim/slot adjustment and a positive lock.
- Hold the flat Hall body without crushing it; pot/heatshrink the leads and add
  a service loop.
- Magnet sits in a keyed pocket or bonded collar with a mechanical lip where
  possible. Degrease, use compatible adhesive and add a witness mark.
- Balance/runout check follows magnet installation; do not place the magnet on
  a bearing race or gear tooth.

## 6. Rail and cable assignment

A3144 uses Rail A 5 V; its output has a 10 kΩ pull-up to 3.3 V and returns to
the all-common-ground star (**DOCUMENTED topology**). Use a three-wire twisted/
bundled run with strain relief. Keep it away from phase wires and cross the
motor bundle only at 90°. The bracket connector must let the rear carrier come
out without cutting the harness.

## 7. Mass and CG

Sensor+magnet+bracket are expected below 5 g (**ASSUMPTION**) at X=−90.9; CG
effect is negligible. Reliability and retention dominate weight.

## 8. Assembly and fit gates

1. Confirm magnet quantity, grade/marking if present and physical Ø/thickness.
2. Select final rear carrier via Gate A and record its mounting surface.
3. Build a diagnostic adjustable bracket; set 1.5 mm with a non-magnetic gauge.
4. Hand-rotate slowly and at increasing drill-free wheel speed; verify one clean
   event/rev throughout 1–3 mm and through axial/radial play.
5. Inspect magnet retention/runout, heat the rear zone only under the governed
   drivetrain test, then recheck gap.
6. Freeze PS-16 only after repeatability and carrier service removal pass.

## 9. Remaining assumptions / stop conditions

Stop for multiple/missed pulses, magnet movement, adhesive-only exposed retention,
sensor/bracket contact, gap change outside the reliable band, lead flex at the
package, belt/gear proximity under 8 mm, or loss of rear-carrier serviceability.
No production Hall bracket is emitted before Gate A and D-38 close.
