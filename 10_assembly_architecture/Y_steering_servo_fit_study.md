# Y · DS3235SG steering-servo fit study — original oil-shock front

Date: 2026-07-22  
Scope: mechanical repository only; no firmware/electrical changes  
Locked build: original Ryan's Creations oil-shock front; the complete Rev-1.1
ball-joint steering set remains excluded.

Reproducible mesh evidence:
[`evidence/scripts/p0_05_steering_rod_line.py`](evidence/scripts/p0_05_steering_rod_line.py)
→ [`evidence/p0/tables/p0_d09_d26_steering_servo_fit.md`](evidence/p0/tables/p0_d09_d26_steering_servo_fit.md).

---

## 1. Recommendation

**Keep the DS3235SG as the primary fit candidate and retain the original steering
architecture. Test it in the original `Servoholder` on its side, as the holder
geometry and supplier floor drawing intend.** The 58 mm axis of the
holder is horizontal/longitudinal, its 22.89 mm axis is vertical, and its 10 mm
axis is lateral. The servo's 40 mm side-face length fits the holder's 42.0 mm
clear span, but its documented 20 mm case width is 1.5 mm larger than the
measured 18.5 mm clear height. Thus the geometry proves the intended orientation,
not the final physical fit. If the real rounded/chamfered case seats without
force, the output shaft is horizontal/lateral and the installed servo is about
20 mm high, not 40.4 mm high.

The horizontal shaft is compatible with the original steering chain:

1. a normal 25T servo horn is vertical at neutral;
2. the horn tip moves fore/aft and drives the long rod;
3. the rod drives `servosaverv7` at the front;
4. `servosaverv7` pivots around a vertical M3 and converts that motion into the
   local steering-link motion.

No bevel gear or other right-angle gearbox is needed. The prompt's “horizontal
shaft cannot drive horizontal steering” argument would apply only if the horn
were expected to rotate the wheel links directly in its own plane. Here the
system uses one tangent of the horn's circular motion to drive a linear rod.

**Do not install `servosaverv7` on the DS3235SG spline.** Its measured central
bore is 2.90 × 2.97 mm through the full 26.50 mm height: it is an M3-pivoted
front mechanism, not a 25T spline socket. The servo itself needs an ordinary
25T metal horn. Removing that mistaken 26.5 mm item from the servo stack is the
largest clearance correction.

No production STL is justified before that fit check. First perform the original
side-mount test in §8. If the real case will not enter the nominal 18.5 mm clear
height, the recommended change is a minimally relieved side-mount holder based
on the measured case; shaft-down and floor-well designs are not clean fallbacks.

---

## 2. Datums and confidence

Vehicle frame:

- **DAT-F / Z=0:** top surface of the assembled original floor.
- **X+:** forward; X=0 at the front/rear floor joint.
- **L:** lateral from vehicle centreline.
- **S0:** seated shell bottom above DAT-F. Digital sections use **S0=0**, so
  every shell ceiling below is a lower bound. The prior digital work bounds the
  unresolved real S0 at about 0…11 mm; body-on measurement still owns it.

Confidence language:

- **VERIFIED / DERIVED:** directly reproduced from STL sections, bores, or
  matched hole patterns.
- **DOCUMENTED:** supplier drawing/README value, not measured from an STL.
- **ASSUMPTION:** needed because the actual horn, rod ends, spacers, seated body,
  or servo placement are not represented by meshes.

Servo vertical datum for the recommended side mount:

- **ASSUMPTION:** DS3235SG 20 mm case side rests on DAT-F, so case top is about
  Z=20 and shaft centre is about Z=10.
- `Servoholder` outer top is **Z=22.89** if its feet rest on DAT-F.
- The physical fit check must record any pad, floor penetration, case chamfer,
  or preload that changes those values.

---

## 3. Verified original-holder and servo geometry

### 3.1 `Servoholder.stl`

| item | measured value |
|---|---:|
| raw bbox | 22.89 × 10.00 × 58.00 mm |
| assembled arch | 58.00 long × 22.89 high × 10.00 thick |
| clear arch | 42.00 long × 18.50 high |
| straight mounting bores | none |

The supplier floor drawing shows the part standing as an arch. Its 42 × 18.5
opening corresponds to a standard servo's 40 × 20 side face; its 58 mm outer
span corresponds to the standard mounting-ear family. The nominal 1.5 mm
vertical interference means the real rounded/chamfered DS case must be test-fit
without force. It is not permission to grind the metal servo case.

### 3.2 DS3235SG supplier drawing

The DS-branded drawing documents:

| item | documented value |
|---|---:|
| case footprint | 40 × 20 mm |
| drawing height envelope | 40.4 mm |
| mounting-ear span | 54.5 mm |
| mounting-hole pitch | 49.5 mm longitudinal × 10 mm transverse |
| bottom-to-ear datum | 27.7 mm |
| output spline | 25T |
| optional horn hole radii | 19.5 and 23.5 mm |

Source: [DS3235/DS3235-180/270 datasheet](https://hajim.rochester.edu/me/sites/kelley/me240/DS3235-270_datasheet.pdf),
pp. 2 and 5. The mechanical-spec table says 40 × 20 × 38.5 mm while its drawing
shows 40.4 mm to the upper output envelope; this study conservatively uses
40.4 mm for clearance.

Ryan's original local parts list explicitly names a “DSServo 35KG” and says a
20 kg unit also works, which independently supports a standard-size servo in
the original build rather than the three MG90S accessory servos:
`unsorted_stl_raw/Ryans Creations Open RC F1 Car/Parts List.txt`.

---

## 4. Floor-to-shell clearance at the servo station

The likely 58 mm holder station is X≈−85.76…−27.76; its centre is X≈−56.76.
A centred 40 mm servo body occupies X≈−76.76…−36.76. With the body end carrying
the output boss toward the front, the lateral shaft's centre station is
X≈−46.76. This station registration is **ASSUMED**
from the repeated 58 mm floor feature pitch and supplier drawing; ASM-08 must
pin the real position.

S0=0 mesh ceilings (mm above DAT-F):

| X | L=0 | L=+10/−10 | L=+20/−20 | L=+26/−26 | L=+30/−30 |
|---:|---:|---:|---:|---:|---:|
| −57, holder centre | 62.3 | 41.1 / 41.2 | 37.6 / 37.6 | 22.2 / 22.3 | 19.2 / 19.1 |
| −47, forward shaft | 63.9 | 43.1 / 43.1 | 38.1 / 38.1 | 37.6 / 37.6 | 21.1 / 20.7 |

**Finding:** the interior is a narrow, high centre spine with low shoulders. A
single “≈45 mm crown” is not a valid envelope, although ≈41–43 mm at |L|=10
does explain the physical observation.

- **Shaft-up:** 40.4 mm already has only about 0.7–2.7 mm at |L|=10 before an
  actual horn, screw, vibration allowance, or 5 mm static policy. At |L|=20 it
  intrudes into the shell. Adding the 26.5 mm `servosaverv7` would make a
  66.9 mm printed/servo stack and is categorically impossible there.
- **Correct side mount:** servo case top is about Z=20 and holder top Z=22.89.
  It has comfortable clearance inside |L|≈20; the low shoulder near |L|≈26–30
  makes the servo's exact lateral seating the remaining physical check.

The same OpenRC family has long-standing reports of steering parts rubbing the
inside shell, but those reports are context rather than dimensions for W17; our
mesh sections above are the governing evidence. See, for example,
[Maker Forums' archived OpenRC fit discussion](https://forum.makerforums.info/t/having-some-problems-hooking-up-the-steering-for-the-f1/68632).

---

## 5. Corrected front-saver and linkage heights

The earlier D-26 result was wrong because it treated `Suspension Block_10` raw
Z (70.79 mm) as vertical. Four M3 centres match the original front-floor holes
within 0.025 mm and prove:

```text
X = 109.389 + block_raw_z
L =  -0.002 + block_raw_x
Z = block_raw_y - 4.000
```

Therefore the block's assembled height is Z=−14…+23; its 70.79 mm axis is
longitudinal.

| front datum | derived value |
|---|---:|
| saver pivot boss plan centre | X=78.09, L≈0 |
| boss printed top / saver base assumption | Z=10.50 |
| saver paired-forward-link clear-gap centre | Z=25.33 |
| saver side-input hole plan centre | X=78.01, L=−13.30 |
| paired forward-hole plan centres | X=95.10, L=−5.83 / +6.15 |
| saver printed top | Z=37.00 |

The STL does **not** contain the servo horn, long rod, ball ends, bolts, spacers,
or their installed centre planes. The side input hole has printed material from
local Z≈13.1…21.9; an external ball joint can sit above or below it depending on
hardware. It would be false precision to quote one final long-rod height from
the STLs alone.

For planning only:

- side-mounted servo shaft centre ≈Z10 (**ASSUMPTION**);
- vertical neutral horn joint ≈Z29.5 or 33.5 using the documented 19.5/23.5 mm
  holes (**ASSUMPTION**);
- front paired-link gap centre Z25.33 (**DERIVED**).

Until ASM-08 supplies the real linkage, use conservative KO-01:
**X −80…+100, Z 22…38, |L|≤22**. This supersedes the erroneous Z35…62 band.

---

## 6. Option evaluation

### A. Vertical shaft-down DS3235SG — reject

If mounted by its ears near DAT-F, inversion can leave roughly the documented
27.7 mm body datum above the mount, but the spline, horn, screw, and horn sweep
then sit below the floor. The original floor has no servo opening at this
station; its centre band is continuous and is generally 4 mm plate with deeper
underside features. The above-floor long rod also has no route to a below-floor
horn.

This option needs a floor cutout, a sealed bearing/guarded transfer, new linkage,
and lost ground clearance. That is a different steering architecture, not a
holder change.

### B. Shaft-up servo in a floor well — reject

At X≈−47, |L|≈10, 40.4 mm + the 5 mm static policy requires at least about
2.3 mm of lowering before the real horn/screw is counted; at the lower shoulder
near |L|≈20 it needs at least about 7.3 mm. A practical well would therefore
breach the 4 mm plate and extend beneath the chassis. It also leaves the rod
higher than the corrected front linkage. There is no benefit once the intended
side orientation is used.

### C. Rev-1.1 `New Steering Servo Holder` — reject for this build

Verified mesh delta:

| item | original | Rev-1.1 |
|---|---:|---:|
| front-floor opening | 12.1 × 12.1 at X=78.1 | 40.5 × 20.0 at X=70.8 |
| servo holder | original remote holder | 37.9 × 38.0 × 32.9 box |

The original `Suspension Block_10` spans X=70.6…141.4 and therefore overlaps
the Rev-1.1 servo opening. The Rev-1.1 README additionally requires cutting the
servo tabs and four M3×20 screws through its changed floor. Its local photos
show the servo lying horizontally in the front box and feeding the new direct
ball-joint steering. It is a coordinated floor + holder + arm + hub system, not
a drop-in fitment fix for the original oil-shock module.

### D. New shaft-down holder — do not design

A new holder cannot solve the missing floor opening, below-floor horn sweep,
ground-clearance loss, and linkage-plane transfer. Designing it would merely
encode an architecture rejected above.

### E. Minimally relieved original side holder — conditional only

If the real DS3235SG will not enter the 18.5 mm arch without force, make a
holder that preserves the 58 × 10 footprint and 42 mm longitudinal clear span,
but raises the bridge just enough for the caliper-measured side width +0.4 mm.
Preserve the current 8 mm end legs and approximately 4.39 mm bridge depth; set
the new outer height to `measured_case_width + 0.40 + 4.39 mm`. For a measured
20.00 mm case this would mean a 20.40 mm clear height and approximately 24.79 mm
outer height, 1.90 mm taller than stock. Recheck ≥5 mm shell clearance at the
actual lateral seat before printing it as production geometry.

Do not change the floor or front steering parts. No STL is emitted now because
the required relief depends on the real case/chamfer and PETG print tolerance;
encoding a nominal 20.00 mm value before measuring the on-hand servo would defeat
the fit-check.

---

## 7. Low-profile fallback if the DS3235SG itself must be replaced

A conventional “low-profile” servo does **not** solve the holder's 18.5-versus-20
mm nominal fit by itself. In the correct side mount, conventional servo **width**
is vertical, while conventional servo **height** runs laterally along the shaft.
Therefore an unchanged-holder replacement needs a case width ≤18.5 mm; otherwise
it needs the same measured bridge relief described in §6E.

Target the following, measured in the same standard-servo axes:

- case length ≤41 mm;
- case width ≤18.5 mm for the stock holder, or measured width plus a relieved holder;
- shaft-axis depth/conventional “height” ≤30 mm to improve shell-shoulder margin;
- 25T, Ø≈5.92 mm output;
- ≥20 kg·cm at the actual 6.0 V Rail-B setting;
- standard PWM; mounting ears physically checked against the holder before
  purchase/installation.

Closest documented electrical/mechanical candidate: **AGFRC SA33** —
40.8 × 20.2 × 29.5 mm, 25T
Ø5.92 mm, 25 kg·cm at 6.0 V, 4.8–8.4 V, standard 1520 µs/333 Hz PWM.
Source: [AGFRC SA33 official product page](https://www.agfrc.com/index.php?id=2522).

Why it is conditional, not a drop-in recommendation:

- the DS3235SG is already on hand and the intended side orientation removes
  the height problem;
- its 20.2 mm case width is 1.7 mm larger than the stock 18.5 mm arch, so it also
  needs a measured relieved holder unless a physical sample proves otherwise;
- AGFRC does not publish the ear span/hole pitch in the text specification, so
  “fits `Servoholder`” remains a purchase gate despite the compatible case;
- its Rail-B stall current is not documented on that page and must pass the
  existing D-24 bench-current test.

No low-profile servo is verified as an unchanged-`Servoholder` drop-in. The 25T
requirement applies to the **servo horn**, not to `servosaverv7`.

---

## 8. Printed parts and assembly order

Printed steering set: **unchanged**.

- Keep original `Servoholder`, `Suspension Block_10`, `servosaverv7`,
  `Crossarm3_extended`, `Arm4`, `Steering Block4`, `GuideRod`, and both original
  `2023WheelHubsSuspension5` handed parts.
- Continue to exclude every file in `New 1.1 Steering Upgrades`.
- Add no floor well, cutout, transfer box, or shaft-down holder.
- Use an ordinary metal 25T servo horn on the DS3235SG; do not put the printed
  saver on the servo.

Mechanical sequence:

1. Print/test-fit `Servoholder` alone. Stand the 58 mm span longitudinally and
   its 22.89 mm axis vertically.
2. With power disconnected, slide the DS3235SG side face into the arch; shaft
   horizontal/lateral. Put the output-boss end fore/aft and the spline face on
   the lateral side shown by the physical drawing/rod route. Do not force or
   grind the case. Record case/holder contact and lateral shell clearance.
3. Power and centre the servo using the already-planned control/servo-test
   procedure; this study makes no firmware change.
4. Fit the ordinary 25T horn vertical at neutral. Start at the 19.5 mm hole if
   available; it is closest to the corrected front linkage height.
5. Assemble the original oil-shock front and mount `servosaverv7` on its M3
   pivot boss.
6. Connect the long rod; add only the spacers needed for a free, nearly level
   run. Do not pull it into plane by bending the rod.
7. Sweep neutral/left/right with the car at ride height, then with relevant
   suspension bump. Record shaft centre, rod Z/L at rear/mid/front, minimum
   shell gap, and all rub points; this closes the physical half of D-26.
8. Seat the shell before installing nearby electronics. Require ≥5 mm static
   shell clearance and ≥8 mm to moving rod/joint envelopes, or revise only the
   holder/rod spacer identified by the measurement.

---

## 9. Remaining assumptions / stop conditions

- Real S0 is not yet pinned.
- The exact original holder X/L registration and servo output-facing direction
  are inferred from the drawing/floor pitch, not assembly-mated STL transforms.
- The actual DS3235SG case chamfer and holder PETG compliance determine whether
  the 18.5 mm nominal clear height is an intentional snap fit.
- Long-rod and side-input ball-centre heights depend on hardware absent from the
  meshes.

Stop and measure rather than modify if any of these occur: metal case must be
forced into the holder; servo top/corner touches the shell in the correct side
orientation; horn cannot be vertical at neutral; rod must bend to meet the
saver; or the saver binds before steering lock.
