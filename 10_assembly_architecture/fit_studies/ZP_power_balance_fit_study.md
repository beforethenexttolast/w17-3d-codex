# ZP · Power, twin-pack feasibility and balance fit study

Date: 2026-07-23  
Evidence: [`p0_d28`](../evidence/p0/tables/p0_d28_zone_component_envelopes.md),
[`p0_d29`](../evidence/p0/tables/p0_d29_zone_placements.csv), and
[`p0_d30`](../evidence/p0/tables/p0_d30_mass_balance.md).

---

## 1. Recommendation

**Install one 2S pack and keep the second BOM pack off-car as the charged swap.**
This is the only configuration compatible with the selected side-bay architecture
on present evidence. Two packs end-to-end require at least 150 mm versus the
78 mm derived bay; stacked flat require about 53–56 mm including tray/strap
versus S0=0 side ceilings of 26–41 mm; mirrored left/right packs consume the
right UBEC/deck/ESC allocation and do not clear the steering corridor.

This is a mechanical conclusion, not permission to parallel batteries. Any
two-onboard electrical proposal is a new power architecture and requires a
separate safety review outside this repo.

The single-pack candidate at X≈−44, L≈+25, base Z=3 is still **ASSUMPTION**. It
fails the S0=0 shoulder profile and overlaps provisional KO-01 vertically.
Therefore hold the battery purchase and production tray until S0 and the
physical steering sweep close D-31/ASM-50.

## 2. Datums and confidence

- DAT-F, X, L and S0 follow the index.
- Derived solid bay length X≈−5…−83 = 78 mm is **DERIVED**.
- Pack hard maximum 75×45×25 is **DOCUMENTED** by BOM v2.
- Pack mass 80–120 g, connector bend and all candidate coordinates are
  **ASSUMPTION** until a specific pack is selected.
- The two-rail topology and all-common-ground rule are **DOCUMENTED** in Report L;
  physical connector and UBEC envelopes remain **ASSUMPTION**.
- No power-part body envelope is **VERIFIED** from a mesh or physical article in
  this repo; D-31/32 must create that evidence before any pocket is sized.

## 3. Component envelopes

| Item | Body | Confidence | Installed envelope |
|---|---:|---|---|
| pack 1 + pack 2 | each ≤75×45×25 mm | DOCUMENTED limit | each 95×50×30 incl. XT60/strap planning allocation |
| UBEC-A / UBEC-B | 30×14×10 planning blocks | ASSUMPTION | body, two lead exits and ≥5 mm convection |
| servo cap | 1000 µF/16 V, Ø10×20 planning can | ASSUMPTION | insulated short leads and zip restraint |
| LED cap | same if second stock capacitor exists | ASSUMPTION | within 50 mm electrical lead length of strip input |
| divider | 27 kΩ / 10 kΩ | DOCUMENTED values | heatshrunk branch plus ADC tap |
| XT60 / XT30 | exact variants TO MEASURE | ASSUMPTION | finger access, recessed live side, bend/strain relief |
| BX100 | 30×12×8 planning block | ASSUMPTION | buzzer holes and balance-lead access unobstructed |

No production pocket may use the planning blocks as if they were hardware
measurements.

## 4. Placement, shell and moving clearances

Candidate pack 1 occupies X≈−81.5…−6.5, L≈+2.5…+47.5, Z=3…28 before
strap (**ASSUMPTION**, DAT-F). At X=−20…−40, the measured S0=0 shell ceiling
near L=45 drops from 27 to about 24 mm. The pack therefore has −1…−4 mm raw
margin before the required 5 mm static allowance (**DERIVED fail**).

Its top also overlaps KO-01 Z22…38. Where heights overlap, the 8 mm moving
policy puts static structure outside |L|=30, but a 45 mm pack placed fully
outside that boundary would extend beyond the shell shoulder. The real horn/rod
sweep, real S0 and a 75×45×25 dummy must be tested together; no coordinate
alone closes this.

Provisional low-layer coordinates, all **ASSUMPTION**:

| Item | X | L | base Z | Orientation |
|---|---:|---:|---:|---|
| active pack | −44 | +25 | 3 | 75 X, 45 L, 25 Z; XT60 forward |
| UBEC-A | −15 | −38 | 3 | flat, clean-rail leads forward/up |
| UBEC-B + servo cap | −48 | −38…−48 | 3 | flat; cap adjacent |
| star/junction + XT taps | +10…+20 | −40 | 3 | contacts recessed, disconnect upward |
| divider | −5 | −35 | 3 | heatshrunk inline |
| pack 2 | off-car | off-car | off-car | labelled swap/storage pack |

Low UBEC bodies remain below KO-01 if their installed top stays ≤Z14. Their
leads may not rise into the rod band without the physical sweep.

## 5. Mounting and service

- Pack tray uses a strap, balance-lead clip, forward XT60 notch and a positive
  fore/aft stop; no foam tape as sole crash retention.
- Reuse an existing/shared M3 screw or reversible plate-clamp foot. Use M3×5
  inserts only in new repeated-service bosses; do not drill donor floors.
- Body-off pack removal must require no deck removal and no tool beyond the
  body fasteners. The second pack is stored in a LiPo-safe off-car location,
  not loose in the car.
- UBECs use vented pockets plus independent zip/strap retention so heatshrink
  bodies are not clamped hard.
- XT60 live contacts are recessed; the all-battery disconnect is first
  reachable. Connector mating cannot load a PCB or resistor joint.

## 6. Rail A, Rail B and common ground

```text
2S pack → main disconnect/star
         ├─ ESC/motor branch
         ├─ UBEC-A → Rail A: camera, Wi-Fi, ESP32×2, RP1, amp, LEDs, Hall
         └─ UBEC-B → Rail B: steering, pan, tilt, DRS, blower
all grounds → one common star; every signal carries its ground
```

- UBEC outputs are never paralleled. ESC BEC red is isolated.
- Servo cap sits across Rail B at the distribution point. LED cap sits across
  Rail A at the first strip input if the second capacitor exists.
- Divider high side senses battery; low side returns to the common star; ADC
  tap goes only to the control ESP32. Keep it away from phase wires.
- Rail-A and Rail-B bundles use different comb lanes. They may cross at 90° but
  do not share a long parallel run near the camera/RP1.

## 7. Mass, CG and battery decision

D-30 uses a deliberately broad 1455–2110 g whole-car range
(**ASSUMPTION**). Its midpoint with one 100 g pack at X=−44, L=+32 and the
camera in the cockpit is:

- total 1782 g;
- X-CG −7.9 mm, or 35.0% front / 65.0% rear;
- L-CG −1.7 mm (right/belt side negative).

The tuning target 36–40% front and |L-CG|≤2 mm is an **ASSUMPTION**, not a
donor specification. The single left pack materially counters the right ESC,
UBEC and deck. A hypothetical second 100 g pack in the right mirror bay moves
the same model to 34.2% front and L≈−3.3 mm while occupying required
electronics volume: worse in both packaging and the current balance ledger.

Battery fore/aft slots ±10 mm shift whole-car CG only ≈0.6 mm at midpoint mass.
Battery placement alone cannot fix a large rear bias. Prefer the lower/forward
camera option, keep optional audio forward/left, then use measured corner
weights—not guessed ballast.

## 8. Assembly and fit gates

1. Pin S0 with the shell seated on the assembled floor.
2. Print/cut two labelled 75×45×25 dummy blocks plus connector/strap stubs.
3. Install the real steering system and sweep full lock plus suspension bump.
4. Trial pack 1 at the stated candidate and every feasible ±10 mm X / small-L
   adjustment. Require ≥5 mm shell and ≥8 mm moving clearance.
5. Try pack 2 only to document the interference; do not remove electronics or
   invent wiring to make it pass.
6. Caliper/weigh the chosen pack, UBECs, capacitors, XT hardware and BX100.
7. D-24 measures both rails and D-39/ASM-58 weighs all four corners before
   tray position or ballast is frozen.

## 9. Remaining assumptions / stop conditions

Stop if the pack presses the shell, enters the rod sweep, needs a puncture-risk
fastener, cannot exit upward, or brings leads within 8 mm of moving parts. Stop
if UBEC outputs are tied together, the ESC BEC remains connected, common ground
is missing, a capacitor lead is unsupported, or any connector polarity is
ambiguous. No production battery/rail support is emitted before D-31, D-24 and
the selected pack's physical measurement.
