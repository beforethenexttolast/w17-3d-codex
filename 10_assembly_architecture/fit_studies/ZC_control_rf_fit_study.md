# ZC · Control and RF fit study

Date: 2026-07-23  
Scope: two installed ESP32 DevKit V1 boards, one off-car spare, RP1 ELRS,
BL-M8812EU2/heatsink and two 5.8 GHz antennas.

---

## 1. Recommendation

Retain the logical split—RP1 forward in the quiet left bay; control/sound boards
and Wi-Fi on a removable deck—but treat the entire deck geometry as
**ASSUMPTION**. The generic ESP32 boards and on-hand Wi-Fi module have no
controlled physical measurement. The measured S0=0 shell makes the deck viable
only in a narrow inboard corridor, and the steering sweep still owns that edge.

Route the RP1's 65 mm T antenna forward toward X≈+120 and keep the two 70 mm
5.8 GHz routes near the airbox mouth around X≈−45. A 150 mm inter-system
separation is a design target (**ASSUMPTION**), not an RF law; D-20 RSSI/video
testing owns the placement. Do not shell-mount U.FL antennas because every
body removal would cycle the fragile connectors.

## 2. Datums and confidence

- Vehicle coordinates use DAT-F.
- RP1 body 13×11×3, 65 mm antenna and 2.2 g are **DOCUMENTED** by the
  [RadioMaster RP1 V2 page](https://www.radiomasterrc.com/products/rp1-expresslrs-2-4ghz-nano-receiver).
- Two 70 mm 5.8 GHz antennas and 28×28×3 heatsink are **DOCUMENTED** by BOM.
- ESP32 55×28×13 and Wi-Fi ≤60×32×12 are **ASSUMPTION** planning blocks, not
  measurements of the purchased boards.
- Every coordinate below is **ASSUMPTION** until S0, ASM-08 and D-32/33.
- No control/RF body is **VERIFIED** from a physical article or mesh in this
  repo; the documented RP1 value is not promoted to that confidence.

## 3. Envelopes

| Item | Body | Install envelope | Confidence |
|---|---:|---|---|
| ESP32 #1 / #2 | 55×28×13 planning each | 55×44×23 incl. side headers, USB plug/bend | ASSUMPTION |
| ESP32 #3 | same family | off-car spare | DOCUMENTED role / ASSUMPTION body |
| RP1 V2 | 13×11×3; 65 mm T antenna | pad, CRSF lead and antenna service loop | DOCUMENTED |
| BL-M8812EU2 | ≤60×32×12 allocated maximum | module, heatsink, USB, two U.FL exits and airflow | ASSUMPTION |
| heatsink | 28×28×3 | bond layer and module stack | DOCUMENTED |
| 5.8 antennas ×2 | 70 mm each | no sharp fold; protected U.FL roots and replaceable route | DOCUMENTED |

The spare ESP32 has no onboard volume or mass allocation.

## 4. Placement and shell clearance

Provisional coordinates (DAT-F, **ASSUMPTION**):

| Item | X | L | Z | Orientation |
|---|---:|---:|---:|---|
| ESP32 #1 | +10 | −32 | deck top +20 | USB outboard; long axis X |
| ESP32 #2 | −45 | −32 | deck top +20 | USB outboard; long axis X |
| Wi-Fi + heatsink | −45 | −18 | deck top +20 | heatsink up; U.FL aft |
| RP1 body | +20 | +38 | +3 | flat; CRSF aft |
| RP1 T antenna | +120 | +15 | ≈+30 | clear/transverse under shell |
| 5.8 roots | −45 | ±18 | ≈+35 | chassis posts; 70 mm longitudinal/shallow V |

At X=−20 the S0=0 ceiling is 39 mm at |L|=20 but 26 mm at |L|=30.
A planning ESP32 top around Z=33 therefore has 6 mm raw clearance inboard and
−7 mm outboard (**DERIVED**). It cannot be represented as a full-width flat
deck. Real S0 may help; outer header/USB geometry may erase that help.

The Wi-Fi P9 block is not a fit result. At X≈−45 its inboard edge also approaches
KO-01 and the shock/airbox channel. The real module must be trialled with
heatsink, both pigtails and camera USB.

## 5. RF, noise and moving keep-outs

- Keep RP1 body/antenna away from UBECs, XT junction, ESC, motor, rear shaft and
  5.8 GHz roots. Target ≥20 mm from conductive masses and ≥150 mm between the
  2.4 and 5.8 antenna regions (**ASSUMPTION**).
- Keep each U.FL route bend radius ≥10 mm and provide a service loop
  (**ASSUMPTION**, confirm the actual cable).
- Two video whips use different shallow orientations; neither is pressed
  against carbon/metal, the central shock or motor wires.
- No deck/support enters KO-01 X−80…+100, |L|≤22, Z22…38 without ASM-08.
- Antennas remain chassis-mounted so KO-14 body lift does not tug coax.
- Wi-Fi airflow uses the derived ≥14 mm continuous airbox channel; it is an
  airflow path, not a PCB pocket.

## 6. Mounting, rails and cables

- ESP32s: low standoffs/foam isolation plus positive clips or M3-supported deck;
  USB remains accessible body-off. Repeated deck fasteners use M3×5 inserts.
- RP1: thin foam pad plus an open carrier; do not hard-clamp its antenna coax.
- Wi-Fi: heatsink bonded before power, vented pocket plus zip/clip restraint.
  Both antennas connect before any Rail-A power.
- All installed control/video items use **Rail A clean**. RP1 CRSF and every
  signal carry common ground. Rail B never runs beside the antenna roots.
- Camera↔Wi-Fi USB crosses the module boundary at proposed CN-16; USB integrity
  must pass bench test. Otherwise deck+camera are one documented service module.
- ESC phase wires stay rear/right; CRSF, ADC and camera USB use the forward/left
  quiet route and cross power only at 90°.

## 7. Mass and CG

Control/video deck mass is 50–95 g at X≈−10, L≈−35, Z≈30
(**ASSUMPTION**). It is both right-biased and elevated. RP1's documented 2.2 g
is negligible. Keep board stacks one level high; vertical stacking worsens
shell fit, cooling and roll CG. D-30 uses this group in the −1.7 mm midpoint
lateral CG; missing the speaker-left or choosing light batteries can push the
model to −3.7 mm. Corner scales own the trim.

## 8. Assembly and fit gates

1. Caliper both installed ESP32 clones including headers and USB plugs; record
   hole pattern, port end and mass.
2. Caliper Wi-Fi PCB/case, heatsink stack, USB and both U.FL exit coordinates.
3. Seat shell and pin S0; install the real steering sweep and all deck dummies.
4. Prove ≥5 mm shell, ≥8 mm moving clearance, USB access and <60 s deck removal.
5. Dress 65/70 mm antenna samples on chassis posts; lower/remove shell ten times
   without coax load.
6. D-20 records ELRS RSSI/failsafe margin and video quality with motor/servos
   active under the separately governed powered-test sequence.

## 9. Remaining assumptions / stop conditions

Stop if the outer board edge touches the shell, a connector must be bent under
the board, U.FL is used as structural retention, the body tugs an antenna, the
Wi-Fi runs without heatsink/antennas, or Rail-B/motor wiring shares the RF lane.
No production deck/RX/antenna support before D-32/33, S0 and ASM-08.
