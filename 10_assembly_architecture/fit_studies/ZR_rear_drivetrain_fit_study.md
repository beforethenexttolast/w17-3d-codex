# ZR · Rear drivetrain and thermal fit study

Date: 2026-07-23  
Scope: original belt-drive rear with the original oil-shock build; Gate A may
still choose original carriers or the Rev-1 rear covers. Evidence:
[`p0_07_zone_fit_rollup.py`](../evidence/scripts/p0_07_zone_fit_rollup.py) →
[`p0_d28`](../evidence/p0/tables/p0_d28_zone_component_envelopes.md) /
[`p0_d29`](../evidence/p0/tables/p0_d29_zone_placements.csv).

---

## 1. Recommendation

**Freeze the ESC mount and the whole production rear batch.** The current
36×32×18 mm ESC planning block is stale. Hobbywing documents the non-waterproof
QuicRun 10BL120 Sensored G2 as **43×36.8×32.3 mm and 101.5 g including
wires**; its framed fan is 25×25×10 mm
([official product page](https://www.hobbywing.com/en/products/quicrun10bl120.html)).
Those values are **DOCUMENTED**, not a physical identification of the unit on
hand. D-28/ASM-49 must read its label and caliper it.

At the current assumed Z5R location, X=−60, L≈−25, base Z=3, the documented
body reaches Z=35.3 and its required 10 mm fan-air plane reaches Z=45.3
(DAT-F, **DERIVED**). The S0=0 shell is only about 19 mm high at |L|=30–40
there, so a side placement fails. A centreline placement approaches the shell
channel but collides with the central shock. No new PS-02/CAD-03 geometry is
justified before a physical body-on search.

The motor/gear/belt family remains credible because the donor design fixes it,
but the physical pulleys, shaft shoulders, spur bolt pattern and rear-stack
identity are unmeasured. Build them as one gate, not isolated interfaces.

## 2. Datums and confidence

- DAT-F, X, L and S0 are as stated in the study index.
- Rear wheel/axle station X=−90.9 is **DERIVED** from the registered shell arch.
- Rear axle Z=26…27 for 5–6 mm ride height is **DERIVED from an ASSUMPTION**:
  tyre radius 32 minus floor ground clearance 5…6.
- Motor, ESC, belt-plane, shock-eye and lateral shaft coordinates are
  **ASSUMPTION** until the rear dry assembly.
- Raw printed-part bboxes are **VERIFIED** by direct STL load; hardware sizes are
  **DOCUMENTED** or **ASSUMPTION** as labelled.

## 3. Component envelopes

| Component | Body envelope | Confidence | Installation addition |
|---|---:|---|---|
| 10BL120 Sensored G2 | 43×36.8×32.3; fan 25×25×10 mm | DOCUMENTED | ≥10 mm open above fan; 12 AWG exits and signal/program leads |
| Rocket 540 V3 17.5T | Ø36×54; Ø3.175×14.5 shaft | DOCUMENTED family value | solder tabs, sensor lead, pinion and axial tool pull |
| 140 mm belt set | belt length 140 mm; pulley geometry unknown | DOCUMENTED / ASSUMPTION | both rotating discs and both moving tangent runs |
| rear output shaft | diameter/shoulders/span unknown | ASSUMPTION | 6801 seats, four metal sleeves/spacers, gear and wheel retention |
| 75T / 28T, 48P | pitch Ø39.69 / 14.82; theoretical centre 27.25 mm | DERIVED | actual hubs, backlash and ≥2 mm radial guard |
| 6801 bearings ×2 | 12 ID×21 OD×5 mm | DOCUMENTED | coaxial seats without printed axial preload |
| rear shock | 68 mm eye-to-eye; body/stroke unknown | DOCUMENTED / ASSUMPTION | full compressed-to-extended swept cylinder |
| `beltdrivemotorlock` | 31.99×3.50×32.00 mm raw bbox | VERIFIED | installed transform/screw stack open |
| original carriers L/R | 81.50×25×10 / 81.50×35×10 mm raw | VERIFIED | Gate A may replace them with Rev-1 motor covers |

## 4. Placement and clearances

| Item | Candidate datum coordinate | Orientation | Confidence | Clearance result |
|---|---|---|---|---|
| rear axle/bearings/spur | X=−90.9, Z=26…27, L offsets TBD | common lateral axis | X DERIVED; L/Z ASSUMPTION | shell arch has only ≈4 mm around Ø64 tyre; full bump gate |
| motor | X≈−105, L≈0, axis Z≈27 | shaft lateral | ASSUMPTION | centre roof ≈55 mm at S0=0; transverse end/vent clearance unproved |
| ESC | X≈−60, L≈−25, base Z=3 | fan up | ASSUMPTION | **fails** S0=0 side ceiling; body/fan search required |
| belt | X≈−118…−82, belt side, Z≈10…45 | pulley planes vertical | ASSUMPTION | rotating KO-21; ≥8 mm to static loom/supports |
| rear shock | X≈−60…−25, L=0, Z≈10…45 | central/longitudinal | ASSUMPTION | moving KO-06; ≥8 mm to ESC/supports |

The 48P arithmetic proves only pitch geometry. It does not prove the motor slot
range can realize 27.25 mm, the 75T hub clears the pulley, or the 140 mm belt has
the required centre distance.

## 5. Mounting and interfaces

- Motor: donor motor plate plus `beltdrivemotorlock`; use the existing M3 kit.
  Do not add an insert where it changes motor-face seating. **ASSUMPTION** until
  screw length and counterbore depth are measured.
- Rear shaft: 6801 bearings and mandatory aluminium OD16/ID14 sleeves. Cut no
  sleeve before the complete axle stack gives the length.
- Spur/pulley: D-16 records bore, bolt count, PCD, screw head and stand-off.
  No slot drilling or hub relief before that record.
- ESC: future mount must be strap-retained, fan-up, tool-removable, and attached
  by shared donor screws/free M3 positions/plate clamps. Do not drill the floor.
- Belt and spur require a removable guard only after their true swept envelopes
  exist. Guard-to-rotating clearance target is ≥2 mm (**ASSUMPTION**), verified
  by hand rotation.

## 6. Cables, rails and thermal

- ESC takes the battery branch directly; it is on neither 5 V rail.
- Lift and insulate the ESC BEC red wire; its signal ground still joins the
  all-common-ground star. This is **DOCUMENTED plan-of-record** in Report L.
- Keep the three motor phase wires and sensor cable short in the rear/belt-side
  corridor. Cross Rail-A signal/antenna routes only at 90° and with ≥20 mm
  separation where practical (**ASSUMPTION**, validated by D-20).
- Motor and ESC are hot sources. No Rail-A board, LiPo or speaker enters their
  thermal envelope. Rear structural mounts remain ASA.
- D-19 records motor can, ESC case/fan exhaust, nearest ASA carrier and bearing
  carrier temperatures after the staged run. Stop for softening, belt dust,
  bearing heat or wire discoloration.

## 7. Mass and CG contribution

Documented/estimated rear drive mass is approximately motor 145–165 g
(**ASSUMPTION**), ESC 101.5 g (**DOCUMENTED**), and belt/gears/shaft/bearings/
spacers 100–150 g (**ASSUMPTION**). At X≈−70…−100 this is the largest rearward
moment in the car. The D-30 midpoint whole-car model produces 35.0% front with
the cockpit camera, below the assumed 36–40% tuning band. The drivetrain is
fixed mass; correction must come from forward optional equipment and measured
battery/electronics placement, not unsafe belt-side ballast.

## 8. Assembly and fit gates

1. **D-28 / ASM-49:** photograph label; record ESC L/W/H, fan, feet, wire exits,
   wire bend and mass.
2. **D-14/15/17:** assemble rear carriers/covers, spring mount, 68 mm shock,
   diffuser/backplate, preferred wing and DRS together; articulate through travel.
3. **D-16 / ASM-51:** record pulley teeth/OD/bore/width/planes, shaft shoulders,
   spur bolt PCD and motor-slot range; blue-check gear mesh and hand-rotate belt.
4. Re-run the body-on ESC search with 43×36.8×32.3 plus wire/fan gauges and real S0.
5. Only then parameterize a diagnostic ESC carrier; production still waits on
   thermal and service gates.

## 9. Remaining assumptions / stop conditions

Stop if the on-hand ESC is a WP variant, any wire must bend against its case,
fan gap is <10 mm, the shock comes within 8 mm of the ESC, the belt walks, the
spur/pulley holes mismatch, bearings require force beyond a controlled press
fit, a carrier softens, or a tyre touches the body at bump. No production rear
STL is released while Gate A or the ESC identity gate is open.

