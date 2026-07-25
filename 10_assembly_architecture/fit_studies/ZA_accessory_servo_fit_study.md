# ZA · MG90S pan, tilt and DRS servo fit study

Date: 2026-07-23  
Steering is excluded; see `Y_steering_servo_fit_study.md`.

---

## 1. Recommendation

Use the three MG90S units only after each purchased servo is calipered. TowerPro
documents a genuine MG90S body as 22.8×12.2×28.5 mm and 13.4 g
([official product page](https://towerpro.com.tw/product/mg90s-3/)), but clone
ears, bosses, spline height and horn sets vary. That makes the values
**DOCUMENTED**, not a verified fit to the ordered units.

The pan/tilt pair remains part of the gated camera module. The DRS servo remains
in the preferred 2021 wing's existing pocket, but raw wing geometry proves only
that a pocket exists. It does not prove this servo, horn, rod or selected rear
stack fits. No gimbal or DRS production geometry before D-35/ASM-54.

## 2. Datums and confidence

- Vehicle coordinates use DAT-F; gimbal local axes inherit X+ boresight.
- MG90S body/mass/250 mm lead are **DOCUMENTED** for the genuine TowerPro part.
- Purchased-unit geometry, horn radius and screw lengths are **ASSUMPTION**.
- Preferred `2021Rearwing with DRS` raw bbox 105.1×82×60 mm and `DRS Arm for
  2021 Rear Wing` 58×5×10 mm are **VERIFIED** from STL.
- Wing, pocket, hinge and arm assembly transforms are **ASSUMPTION**.
- No installed accessory-servo position is **DERIVED** from donor registration;
  the candidate coordinates remain assumptions until the module transforms close.

## 3. Envelopes

| Item | Body | Installed/moving envelope | Confidence |
|---|---:|---|---|
| pan MG90S | 22.8×12.2×28.5 mm | ears, spline/horn, lead and full yaw sweep | DOCUMENTED body / ASSUMPTION sweep |
| tilt MG90S | same | ears, horn/link, camera body and pitch sweep | DOCUMENTED body / ASSUMPTION sweep |
| DRS MG90S | same | wing pocket, horn/rod and flap sweep | DOCUMENTED body / ASSUMPTION pocket |
| 2021 DRS wing | 105.1×82×60 raw | chosen stack + hinge + fasteners | VERIFIED raw / ASSUMPTION transform |
| 2021 DRS arm | 58×5×10 raw | entire swept arm | VERIFIED raw / ASSUMPTION pivots |

Until the real horns are measured, reserve a 15 mm horn radius around each spline
(**ASSUMPTION**). The common camera-module reserve remains 55×45×60 mm
(**ASSUMPTION**), not a gimbal design.

## 4. Placement and moving keep-outs

| Servo | Candidate datum | Axis/orientation | Confidence |
|---|---|---|---|
| pan | Option A X≈+60 or B X≈−53, L=0, module base | output axis Z | ASSUMPTION |
| tilt | same X/L, above pan | output axis L; lens points X+ at centre | ASSUMPTION |
| DRS | X≈−125, L≈0, Z≈55…80 | per wing pocket | ASSUMPTION |

Pan and tilt moving envelopes include horn, camera, blower duct and service
loops. Require ≥8 mm to fixed halo/body/mount through full allowed travel.
DRS KO-12 includes the 58 mm arm, metal rod, flap and servo horn; require ≥8 mm
to shock, LED harness and body. Hard stops must be visible/measurable and must
not use the servo case or camera PCB as the stop.

## 5. Mounting and fasteners

- Use the servo's ear holes with through screws and captive nut/insert where
  service repeats. Do not self-tap repeatedly into a thin printed wall.
- Use M2-class servo hardware if supplied; the M3 kit is for the module/wing
  support, not permission to enlarge MG90S ears.
- Pan base must be torsionally stiff; tilt side plates support both sides of the
  camera where possible. No single-wall cantilever.
- DRS pocket retains the servo body without clamping the gear case. Rod must run
  straight at neutral with no flap preload.
- Mark every horn/spline neutral position before removal.

## 6. Rail and cable assignment

All three MG90S units use **Rail B** and all grounds join the common star. The
camera and Wi-Fi remain Rail A; do not power the camera from a servo lead.

Gimbal leads get separate flexible loops at pan and tilt. The DRS lead descends
the left rear guide before the rear stack closes and stays ≥8 mm from shock,
belt and arm sweep. The blower also uses Rail B but gets its own decoupled
branch; servo and blower leads may share the Rail-B trunk, not a moving loop.

## 7. Mass and CG

Three documented servo bodies total 40.2 g. Pan+tilt add 26.8 g plus camera/mount
at either X≈+60 or −53; DRS adds 13.4 g at X≈−125 and high Z
(positions **ASSUMPTION**). The high DRS mass is fixed by the feature. The
camera pair should remain in lower/forward Option A if FOV permits because
Option B worsens fore/aft and vertical CG.

## 8. Assembly and fit gates

1. Record each servo's body, ears, hole pitch, spline/boss, lead exit, horn radii
   and mass; label pan/tilt/DRS.
2. No-power fit each body into its candidate holder/pocket without force.
3. Fit horns/links and hand-sweep all mechanical travel; record nearest clearance.
4. Combine DRS with the actual rear shock/stack/wing/LED harness—never test the
   pocket alone.
5. Camera hard-stop measurement and any powered sweep remain behind the wider
   project safety gate; this repo only supplies the measurable geometry.
6. Production requires repeatable neutral, ≥8 mm clearance and no case/pocket bind.

## 9. Remaining assumptions / stop conditions

Stop if a servo must distort its pocket, an ear needs drilling, the horn hits
the shell/halo/wing, the linkage preloads a flap, a wire becomes the hard stop,
or any moving axis can pinch a lead. Clone dimensions supersede the TowerPro
drawing only after a dated physical record.
