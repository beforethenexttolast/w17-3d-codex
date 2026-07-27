# ZK · Lift-out electronics cassette physical fit study

Date: 2026-07-24  
Revision: batch-1 measured-envelope, selected-hardware and connector-route recomputation  
Scope: physical packaging only. The supplied PDB contents, controller identity
and connector map are accepted inputs; this study does not design their
circuits. No production STL, shell relief or donor-floor drilling is authorized.

## 1. Recommendation

**FIT GATE: CONDITIONAL-GO TO A FULL-SCALE REPACK DUMMY, NOT TO
PRODUCTION CAD. THE EVERYTHING-INSIDE CLAIM IS NOT YET CLOSED.**

The two changes remove the two independent failures that made the preceding
reference attempt a categorical NO-GO:

- a single wall-mounted mini-board row is 39 mm long instead of a 110 mm
  two-DevKit row. It fits the registered 97.36 mm clean longitudinal interval
  with **58.36 mm** left before wall, plug and harness allowances;
- the camera/gimbal is no longer added above the cassette's Z38 top. The old
  arithmetic `Z38 + 60 = Z98` is retired; the hollow pedestal and gimbal are now
  independently floor/front-structure referenced.

Batch-1 measurements move three gates and regress one:

- **CAS-04 / ASM-22 moves from height-deficit HOLD to dimensional PASS-GAUGE.**
  A 10 mm laid-flat capacitor over a 1.6 mm PCB gives an 11.6 mm electrical
  stack. From the existing Z1 seat the component top is Z12.6; this study carries
  a conservative Z14 installed audit top including the insulated pad/retention
  allowance. `Z22 − Z14 = 8 mm`: the former 5 mm deficit is removed, with zero
  policy reserve at the conservative audit top. ASM-08 still owns closure.
- **D-06b component identity/envelope closes.** The measured BL-M8812EU2 is
  32.4×32.0×7.0 mm and 11.2 g including antennas. It receives a rear-stem
  heatsink-up trial seat and two explicit U.FL root reserves. That station still
  depends on the measured steering sweep.
- **CAS-11 / ASM-58 narrows.** The provisional control/RF group is 30.8–32.8 g
  (31.8 g midpoint), not 72.5 g.
- **CAS-06 / ASM-49 regresses to FAIL-STATION.** The measured ESC is
  44.2×33.7×34.0 mm. Its floor body reaches Z35.5 and its required 10 mm
  intake-air plane reaches Z45.5. The current side station conflicts with both
  KO-01 policy and the registered shell shoulder; it must be relocated.

The worst shell shoulder over the two controller wall seats still requires
**S0≥9.82 mm**. The straight dock face remains rejected and becomes more crowded
after adding the USB-C charge link. The verdict therefore stays CONDITIONAL-GO
to a full-scale dummy only.

## 2. Datums, inputs and confidence

- **VERIFIED:** raw floor, shell, halo, `Suspension_Block_10`, motor-lock and
  drivetrain silhouettes embedded in the generated visualization. A raw
  silhouette does not verify its assembly transform.
- **FIRM selected controller:** both installed controllers are ordered USB-C
  MH-ET D1-Mini ESP32 boards, 39×31 mm procurement class. The required control
  and sound/light pins are exposed and the firmware pin map is unchanged. An
  ESP32-C3/S2/S3 “SuperMini” is not an allowed substitute. Board thickness,
  headers, holes, installed height and live USB-C plug projection await arrival.
- **FIRM electrical content/map:** the PDB contains XT60 input, two measured
  44.3×22.1×9.1 mm UBECs, laid-flat 1000 µF Rail-B capacitor, 27k/10k divider
  and common-ground star. The XT90-S master switch and IP2326 charger are
  separate inline/cell occupants, not PDB height contributors.
- **DERIVED:** DAT-F floor top Z=0; X+ forward; L from centreline; shell sections
  in
  [`p0_d02_d03_d04_clearance.md`](../evidence/p0/tables/p0_d02_d03_d04_clearance.md);
  corrected steering evidence in
  [`p0_d09_d26_steering_servo_fit.md`](../evidence/p0/tables/p0_d09_d26_steering_servo_fit.md).
- **MEASURED owner ground truth:** QuicRun 10BL120 G2
  44.2×33.7×34.0 mm and 100 g; BL-M8812EU2 32.4×32.0×7.0 mm and
  11.2 g with antennas; UBEC 44.3×22.1×9.1 mm and 10 g each; selected pack
  69×35×18 mm and 88 g.
- **TARGET / ASSUMPTION:** final PDB geometry is not a measured board:
  its plan remains 55×45 mm and mass remains ~50 g provisional, but its installed
  height audit is now Z1…14. The selected IP2326 footprint is 18.3×31 mm in its
  own ≤10 mm target-height cell. The stepped-T cassette, connector-body
  allocations, 10×18 conduit and pedestal remain audit gauges.
- **ASSUMPTION install:** mini-board holes, component-side projection, live
  USB-C plug, wire bends and retention are not calipered even though the
  identity/envelope input is firm.
- **SELECTED / physical-fit pending:** all electrical items are chosen/ordered.
  The ZEEE 2S pack, IP2326, XT90-S, MH-ET boards and accessory servos still have
  missing arrived-part/install evidence; no pocket, port, strap, plug-bend or
  retention geometry may be inferred from procurement alone.

The general 5 mm static and 8 mm moving policies remain. KO-01 remains the
conservative X−80…+100, |L|≤22, Z22…38 band until ASM-08.

## 3. Revised everything-inside reference gauge

The shape is intentionally not a rectangular production box. The former
T-gauge is re-tightened into a stepped rear stem, forward wall wing and tapered
PDB tongue. Coordinates and every structural thickness are ASSUMPTION gauges.

| Item | Reference envelope in vehicle coordinates | Confidence | Result |
|---|---|---|---|
| cassette rear stem | X−31…+1, L−18.5…+17.5; lower charger/RP1 layer Z1…11 and Wi-Fi deck Z12…19 | ASSUMPTION | Wi-Fi now consumes the old amp/RP1 upper deck; amp returns to the speaker/audio cell |
| cassette forward wing / tongue | wing X+1…+42, L±43; tapered tongue X+42…+46, L±29.5; conservative structure/audit top Z14 | ASSUMPTION | side-seat floor margin retained at X+42; tongue fits the narrowing floor |
| PDB revised height gauge | body X+1…+46, L±27.5; component stack top Z12.6 nominal, installed audit top Z14; ~50 g provisional | FIRM contents / measured UBEC / TARGET plan and mass | 16.86 mm static-policy shell surplus at Z14; exactly 8 mm to KO-01 |
| IP2326 charge cell | X−31…−12.7, L−15.5…+15.5, Z1…11 (18.3 X ×31 L ×≤10 Z target) | selected footprint / installed height ASSUMPTION | rotated footprint packs; onboard Type-C/thermal face/height remain ASM-59 |
| RP1 lower seat | X−11.4…0, L−6.7…+6.7, Z1…5.05 | MEASURED body / retention ASSUMPTION | fits beside the rotated IP2326 cell with 1.3 mm X separation |
| BL-M8812EU2 seat | X−31…+1, L−16.2…+16.2, Z12…19; heatsink up; clear-air reserve Z19…29 | MEASURED body / seat and airflow ASSUMPTION | D-06b body placement closes; physical gap to provisional KO-01 is only 3 mm, 5 mm short of moving policy pending ASM-08 |
| ESP32 #1 wall seat | X+3…+42, L−43…−30, Z1…32 | identity/envelope FIRM; install ASSUMPTION | clears KO-01 lateral boundary by 8 mm; shell needs S0≥9.82 |
| ESP32 #2 wall seat | X+3…+42, L+30…+43, Z1…32 | same | same; both USB-C service ends face X+42 |
| Wi-Fi U.FL roots | two 12×12×6 bend/strain-relief reserves at the X+1 module edge, separated to L−8/+8 routes | U.FL family FIRM / pigtail lengths ASSUMPTION | both coax runs turn outward with ≥10 mm bend; never clamp a plug; antenna lengths/routes remain physical |
| ganged dock | existing banks plus one added USB-C charge link; straight trial projection X+42…+58 remains rejected | connector map FIRM; bodies/topology ASSUMPTION | U-SIG body-width sum rises to at least 68 mm before separators; stepped/wrapped dummy required |
| ZEEE pack on floor | body X−77…−8, trial shift L+30…+65, Z1.5…19.5 (69×35×18), within station X−80…−5/L+22.5…+67.5/Z1.5…26.5 | MEASURED body/mass / service placement ASSUMPTION | body margins: 6 X, 10 L and 7 Z total; trial L shift gives 8 mm to KO-01, but strap/lead/shell/removal remain CAS-05 |
| ESC broken floor station | X−49.2…−5, L−60.5…−26.8, Z1.5…35.5; intake-air plane Z45.5 | MEASURED body / outboard-anchored station ASSUMPTION | **FAIL-STATION:** only 4.8 mm to KO-01 and body/air conflict with shell shoulder |
| XT90-S master access | fixed pack-side main-lead pocket at the body-accessible battery edge; pack → XT90-S → dock/PDB | selected family / exact body and pull axis pending | off PDB; body-on pull is the run/charge-safe action; no pocket CAD before caliper/body-opening proof |
| motor + belt | registered rear group near X−90.9 | VERIFIED silhouettes / transform and sweep partly ASSUMPTION | retained; no cassette entry into the rear rotation zone |
| hollow cockpit pedestal | trial outer core X+51…+65, L±11; conduit clear 10×18 with 2 mm wall →14×22 outer | architecture split VERIFIED; geometry ASSUMPTION; MG90S physical fit pending | 5 mm from PDB tongue and 5.6 mm from front block; opening/halo/FOV/sweep/conduit gate open |

The plan/side/section sheet shows this one reference, including the unresolved
conditions. It is not a choice among hidden arrangements.

## 4. Shell, steering, pedestal and drivetrain audit

The old board-length result is reversed:

`97.36 − 39 = 58.36 mm`

The assumed board seats use X+3…+42 and put their inner faces at |L|=30.
Against the provisional |L|≤22 steering band this is exactly 8 mm. Their
Z1…32 envelopes no longer enter KO-01. The limiting shell point sampled over
both seats is Z27.18 at approximately X+3/L−37, so:

`required S0 = board top 32 + static 5 − roof 27.18 = 9.82 mm`

That is a conditional closure inside the existing 0…+11 S0 range, not a verified
body-on margin. Calipered headers, USB plug bodies or a lower real S0 can reject
it.

The target PDB is rotated so its 45 mm side runs X+1…+46 and its 55 mm side
runs L±27.5. The high electrical stack is:

`max(cap 10, XT60 8, UBEC 9.1) + PCB 1.6 = 11.6 mm`

From the existing Z1 seat, the nominal component top is Z12.6. The audit rounds
up to **Z14** to carry the insulated pad/retention tolerance without pretending
those details are designed. The worst finite roof sampled over that footprint is
Z35.86, so `35.86 − (14+5) = 16.86 mm` static-policy surplus at S0=0. Plan gaps
are also positive: 6 mm to
the battery/ESC X−5 front edge, 5 mm from its tapered tongue to the shifted
pedestal X+51, and ≥14.1 mm raw from the PDB body to the floor edge at X+46.
The board-to-mini inner-face gap is only 2.5 mm, so wall/rib/connector
protrusions remain a real dummy check.

The revised PDB steering result is:

`KO-01 bottom Z22 − conservative PDB audit top Z14 = 8 mm`

The height deficit is removed: nominal component geometry gives 9.4 mm and the
rounded installed audit gives exactly 8 mm. This is a dimensional policy pass,
not final closure. A PDB over Z14 or any measured sweep below Z22 reopens it;
ASM-08 remains mandatory. The stacked Wi-Fi body ends at Z19 and has only 3 mm
to provisional KO-01. D-06b closes its measured envelope/seat assignment, while
CAS-01 owns acceptance of that station.

The gimbal is no longer a cassette roof load or a cassette lift obstruction.
Its floor/front-structure pedestal remains installed when the cassette lifts,
and the camera USB plus two MG90S leads descend through the hollow path. This
**does resolve the old additive Z98-vs-~Z42 failure mechanism**. It does not
claim that an unmeasured gimbal sweep fits the cockpit: the pedestal datum,
existing cockpit opening, halo transform, airbox clearance, FOV and endpoints
remain CAS-08/09.

The exact 69×35×18 pack fits the ≤75×45×25 body station with 6×10×7 mm total
body margin. A trial outboard shift to L+30…+65 leaves 8 mm from its inner face
to KO-01 at |L|=22. Reserve the central strap over the body, take the XT60 main
and JST-XH balance leads from the X+ end into the +L edge route, and keep the
body-off vertical removal path free after the strap and both leads release.
Those assignments are not a retention claim: strap thickness, natural wire
bends, shell shoulder and removal sweep remain CAS-05/D-31 measurements.

The measured ESC **breaks its station**. Retaining X−49.2…−5 and anchoring the
narrower 33.7 mm width at the old outboard edge gives:

- body `L−60.5…−26.8, Z1.5…35.5`;
- nearest lateral separation to KO-01: `26.8 − 22 = 4.8 mm`, **3.2 mm short**;
- 10 mm fan-intake plane: `Z35.5 + 10 = Z45.5`;
- registered S0=0 shoulder over the ESC centre L−43.65: approximately
  Z22.4…28.5 across its X band, so the 34 mm body penetrates the gauge by about
  **7.0…13.1 mm** before static clearance;
- even at the inboard face L−26.8, roof Z36.7…39.5 cannot supply the Z45.5
  air plane.

CAS-06/ASM-49 therefore returns **FAIL-STATION / RELOCATE**. S0+11 does not
recover the required air plane over the outboard body footprint. Natural
12-AWG bends only enlarge the failed volume. Motor/belt/wheel/suspension
conclusions are unchanged.

## 5. Mounting and four-point lift-out

The smaller/T-shaped gauge does **not** create a clean existing-hole rectangle:

- X+37/+43, L±41 rows remain vent/body-seat features and have only ~6 mm
  longitudinal separation;
- the rear X−27.76 pair remains asymmetric and servo-contested;
- centreline holes are occupied by the floor splice; rear rows remain
  drivetrain/axle territory.

Use no donor hole as a cassette attachment until a physical occupancy check
changes that evidence. The former reversible-saddle centres were:

`(X,L)=(-15,±12),(+35,±12)`

They no longer survive the supplied target cells:

| Four-point re-check | Derived result | Disposition |
|---|---:|---|
| rear pair X−15/L±12 | inside rotated IP2326 cell X−31…−12.7/L±15.5 | **REJECT** |
| front pair X+35/L±12 | inside PDB target X+1…+46/L±27.5 | **REJECT** |
| hidden service screw below a module | module removal would precede cassette removal | **REJECT**; defeats lift-out intent |
| existing donor holes | still vent/body-seat, seam, servo or drivetrain contested | no clean four-point pattern |

The earlier **boss OD≤11 mm** result is retained only as historical evidence
for those rejected coordinates; it is not a current design target. CAS-07 must
use a transparent full-stack dummy to establish a new reversible external
saddle/clamp pattern, insert coupon, driver axes and four-point stability.
No replacement coordinate, donor drilling or STL is inferred here.

## 6. CG sensitivity

The prior one-pack/cockpit-camera midpoint was **1782 g, 35.0/65.0%
front/rear and Z-CG 22.2 mm**. The batch-1 substitution uses measured mass where
available and retains the unchanged midpoint assumptions for printed structure,
hardware, drivetrain, suspension/wheels and camera/gimbal.

| Refreshed group | Mass used | Reference group station / note |
|---|---:|---|
| motor | 156.7 g MEASURED | X−100, Z27 |
| ESC | 100.0 g MEASURED | X−27.1, Z18.5 at the now-failed station |
| steering servo | 70.3 g MEASURED | X−55, Z15 |
| battery | 88.0 g MEASURED | X−42.5, Z10.5 |
| control/RF | 31.8 g provisional midpoint | Wi-Fi+ant 11.2 + RP1 1.6 + 2× MH-ET 9.5; range 30.8–32.8 g until board arrival; composite X+7.87/Z15.47 |
| PDB | 50.0 g provisional target | includes the 20 g measured UBEC subset; cap/PCB/XT60/headers/wiring still unweighed; X+23.5/Z7.3 |
| audio/light | `10.4 + 17ℓ` g | amp+speaker measured 10.4; `ℓ` is installed LED-strip length in metres; X−20/Z12 planning station |

For the deliberately conservative `ℓ=1.00 m` bookkeeping case, with no
unweighed IP2326, XT90-S, cassette/dock or pedestal increment added:

`mass = 1717.6 g`

`X moment = −7559.23 g·mm`

`Z moment = 36936.15 g·mm`

`front% = 100 × (X-CG + 90.9) / 237`

| Scenario | Total | X-CG | Z-CG | Front/rear |
|---|---:|---:|---:|---:|
| measured/provisional substitution, 1.00 m LED | 1717.6 g | −4.40 mm | 21.50 mm | 36.50/63.50% |
| same, current seven-pixel planning segment (`ℓ=7/30 m`) | 1704.6 g | −4.28 mm | 21.58 mm | 36.55/63.45% |

For every later weighed item `i`, use
`M=1717.6+Σmᵢ`, `Mx=−7559.23+Σ(mᵢxᵢ)` and
`Mz=36936.15+Σ(mᵢzᵢ)`; an actual PDB mass replaces, rather than adds to, the
50 g target. The displayed result is about **60.8 g lighter** than the previous
ZK substituted ledger, principally because control/RF drops by 40.7 g and the
pack by 12 g. It remains inside the 36–40% front planning band, but D-39/ASM-58
still requires the arrived MH-ET/IP2326/XT90-S masses, completed cassette and
four-corner scales before ballast.

## 7. Pedestal conduit, umbilical and service

The delivered map fixes the families and links; it does not verify housing
dimensions. The retained topology is one **ganged service dock**, not one
literal centre-spine cable:

1. the pedestal's shielded 4-pin camera USB and two 3-pin MG90S leads descend
   through a **10×18 mm clear** rounded-rectangle target; a 2 mm trial wall gives
   a 14×22 mm outer core. Pull connectors sequentially, reserve ≥25 mm lower
   service loop and use ≥20 mm provisional USB bend radius before R1/R2;
2. the fixed-consumer dock minimum is 1× XT60 pack inlet, 2× XT30 Rail-A/B
   branches, 5× positive-lock 3-pin positions (steering, ESC with +5 absent,
   DRS, pan, tilt), 3× JST-XH 3-pin links (pack balance, LED, Hall), 1×
   shielded USB4 camera link, **1× USB-C charge-extension link**, plus 2-pin
   blower and speaker auxiliaries. The U-SIG assumed-body sum is now at least
   `3×12 + 16 + 16 = 68 mm` before dividers, labels or finger gaps;
3. internal seats reserve JST-XH 4-pin CRSF, 3-pin link2, 5-pin I2S and 2× U.FL
   coax roots. The pack JST-XH balance lead crosses the dock to the IP2326; the
   hidden USB-C port/extension crosses the added charge seat to the IP2326;
4. A0 supports dock bodies, A1 arrests the first bend, A2 supports the
   steering/ESC fan-out and A3 fixes the rear tail before LED/Hall/DRS branches;
5. the main path is pack → body-accessible XT90-S → XT60 dock inlet → PDB.
   Pulling the XT90-S is the required run-off/safe-to-charge action. The switch
   remains fixed with the pack-side loom and is not counted in PDB height;
6. both mini-board USB-C connectors face the X+42 cassette access edge;
7. body off → pull the master, unplug the ganged dock → release the
   still-unresolved four-point
   external saddle/clamp → lift the
   cassette while the pedestal remains fixed.

Target body allocations are ASSUMPTION: XT60 20×20×12; XT30 16×16×10; servo
16 mate-depth ×10 pitch ×8 high; JST-XH 3/4/5-pin 12/15/18 square ×9 high;
USB4 and provisional USB-C 16×16×10; U.FL bend/strain-relief reserve 12×12×6
each. The camera USB allocation presents a 16×10 cross-section to the 18×10
conduit, leaving 2 mm on the long axis and **zero nominal short-axis surplus**.
Each servo body presents 10×8, leaving 8×2 mm surplus when oriented for the
gauge. Therefore the USB and two servo plugs still pass **sequentially**, not
abreast, on allocation arithmetic; real terminated plugs still own CAS-09.

The USB-C charge extension and pack-balance lead use the stepped/wrapped dock
and R1/R2 edge route; neither is added to the pedestal conduit. The straight
front-face projection X+42…+58/L±32 still overlaps the pedestal and is rejected.
A stepped/wrapped full-size dummy must establish the final dock. Real XT90-S and
USB-C bodies, terminated housings, wire gauges, mating hands, bends, latch
access and strain relief remain D-10/CAS-09/10 measurements.

## 8. Prioritized ASM fit-gate checks and electrical-input closures

1. **CAS-01 / ASM-08:** powered steering neutral/lock-to-lock plus bump sweep;
   replace KO-01 with measured X/L/Z points and record the conservative PDB Z14,
   Wi-Fi Z19, pack, relocated ESC, board-seat and conduit gaps. PDB height now
   passes the provisional 8 mm gauge, but neither that nor the Wi-Fi station is
   physically closed without this sweep.
2. **CAS-02 / D-04:** seat the real body, measure S0, and map the two board
   shoulders. Pass requires S0≥9.82 mm **and** ≥5 mm to the actual plugs/headers.
3. **CAS-03:** MH-ET D1-Mini 39×31 USB-C procurement premise is confirmed.
   Caliper both arrived boards, headers, holes, installed height, USB-C edge and
   live plug bend; verify the retained X+3…+42 seats and service hand. Reject
   C3/S2/S3 SuperMini substitutions.
4. **CAS-04 / ASM-22:** height moves to PASS-GAUGE at conservative Z14. Place
   the two 44.3×22.1×9.1 UBECs, laid-flat capacitor and XT60 on the 55×45 plan;
   record finished L/W/H/mass, holes, exits and insulation. Any installed top
   above Z14 reopens the steering-height deficit.
5. **CAS-05 / D-31:** exact 69×35×18 pack body is measured and plan-fits.
   Dummy the proposed L+30…+65 shift, central strap, X+ XT60/JST-XH exits and
   body-off removal sweep with natural leads and shell seated.
6. **CAS-06 / ASM-49:** current station is **failed**. Find a new station for
   the measured Z35.5 body, Z45.5 air plane, feet and natural 12-AWG bends with
   motor/belt installed and the body seated; no shell relief is authorized.
7. **CAS-07:** reject the former (−15,±12)/(+35,±12) boss pattern because it
   lies inside the charge/PDB targets. A transparent full-stack dummy must prove
   a new external four-point saddle/clamp, insert depth, driver reach and
   lift-out access; no drilling or hidden screws.
8. **CAS-08 / ASM-53:** fixed pedestal plus real halo/body, camera and the two
   selected MG90S units after arrival; verify FOV, airbox clearance, no-power
   pan/tilt endpoints and cassette lift.
9. **CAS-09:** 10×18 clear / 14×22 outer conduit coupon plus terminated-plug
   dummy; pull USB4 and both servo plugs sequentially, retain ≥25 mm lower slack,
   prove bend/strain relief and turn into R1/R2 without steering contact. Do not
   add the USB-C charge or JST-XH balance leads to this conduit.
10. **CAS-10 / D-10:** connector map is firm; caliper every selected XT60/XT30,
    servo, JST-XH 3/4/5, USB4, USB-C charge extension, XT90-S, auxiliary and U.FL
    body. Build the stepped/wrapped dock plus master-access dummy; prove
    source-side shrouding, labels, body-on master pull, latch access, mating pull,
    jacket anchors and ten body-off cycles. The straight front face is rejected.
11. **CAS-11 / ASM-58:** measured substitutions give 1717.6 g,
    36.50/63.50% and Z-CG 21.50 mm in the full-metre LED bookkeeping case.
    Weigh the two MH-ET boards, PDB, IP2326, XT90-S, completed cassette/dock,
    pedestal and camera group; then four-corner scale before ballast.

The selected 18.3×31 mm IP2326 remains under **ASM-59 / J-CHG-001**: caliper
installed height, holes, onboard Type-C edge, thermal face and connector exits.
Its rotated X−31…−12.7/L±15.5/Z1…11 cell is an ASSUMPTION, not a pocket. The
hidden port must use an existing opening or reversible insert; this study
authorizes no shell cut.

## 9. Open conditions and production stop

The re-audit verdict remains conditional until CAS-01…11 and ASM-59 are
recorded. The supplied lower cells do **not** close the complete
everything-inside layout today. Stop production CAD/STL or relief if S0 is below
9.82 mm at the real wall seats; if either mini installed envelope differs; if
the PDB exceeds Z14 or cannot clear the measured steering sweep; if the Wi-Fi
Z19 seat cannot clear that sweep or keep its heatsink/U.FL roots serviceable; if
the failed ESC station has no shell/KO-safe replacement with a Z45.5 air plane;
if the IP2326 cell, battery strap/leads/removal, or XT90-S body-on pull cannot be
proved; if the new four-point saddle requires hidden module removal or donor
drilling; if the stepped/wrapped dock including the added USB-C charge seat
cannot clear the pedestal and release body-off; if any terminated camera/servo
plug fails the 10×18 conduit dummy; or if the pedestal cannot complete FOV and
pan/tilt sweep with the halo and shell installed.

No prior owner-side gate is retired: S0/body seating, powered steering sweep and
real weights/four-corner scales remain owner measurements. CAS-04 moves only
from a known height deficit to an 8 mm dimensional gauge. D-06b closes the
measured Wi-Fi envelope/seat assignment, not the sweep. CAS-06 regresses to a
failed station. The old 110 mm board-row and Z98 additive-gimbal failure
mechanisms stay retired; the former four-boss coordinates and straight dock face
remain rejected implementations inside open mounting/service gates.

The generated `p0_d34`/cassette visualization set still encodes the preceding
Z19/unplaced-Wi-Fi cassette cells and must not be used as evidence for the full
batch-1 recomputation. Its ESC overlay is synchronized to the measured body and
failed station; that synchronization emits no STL or relief and authorizes no
print. A2 remains NOT-EXECUTED and Phase B remains BLOCKED; nothing is to be
powered.
