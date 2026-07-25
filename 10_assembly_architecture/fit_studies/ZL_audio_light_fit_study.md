# ZL · Audio and lighting fit study

Date: 2026-07-23  
Scope: MAX98357A breakout, 4 Ω 3 W speaker, 30 LED/m WS2812B stock, halo and
rear lenses/diffuser.

---

## 1. Recommendation

Place the speaker low in the left sidepod at X≈−30, L≈+43, base Z=3 and the amp
on the removable deck/low shelf near X≈−5, L≈−40. Both coordinates are
**ASSUMPTION**, but the speaker candidate has the best existing shell evidence:
a 12 mm-tall body leaves about 9–12 mm raw, 4–7 mm after the 5 mm static policy,
at S0=0 (**DERIVED**). The port, actual speaker and service access remain open.

Use only a small, purposeful subset of the 30 LED/m strip: one rear brake/rain
pixel in `rearbacklightdiffuser`, two pixels per rear indicator and two along
the halo—seven installed pixels (**ASSUMPTION**). Hazard reuses both indicators;
rain/brake reuse the centre pixel. Do not force all 30 pixels into the car.

## 2. Datums and confidence

- Vehicle coordinates use DAT-F.
- `rearbacklightdiffuser` 9.5×12×14.5 and `new halo 2.1`
  74.94×38.75×24.86 raw bboxes are **VERIFIED**.
- WS2812 strip width 10 mm and pitch 33.33 mm are **DOCUMENTED** from the BOM's
  30 LED/1 m stock.
- MAX98357A 19.4×17.8×3 mm is a reference breakout size only and is
  **ASSUMPTION** for the purchased clone.
- Speaker Ø28–40×6–12, all placement transforms and segment counts are
  **ASSUMPTION**.

## 3. Envelopes

| Item | Body | Installed envelope | Confidence |
|---|---:|---|---|
| MAX98357A | 19.4×17.8×3 reference | headers/terminal block, I2S and speaker bends | ASSUMPTION |
| speaker | Ø28–40×6–12 planning range | basket, cone excursion, isolation ring, baffle/port | ASSUMPTION |
| WS2812 strip | 10 wide, 33.33 pitch | cut pads, 3-wire tails, adhesive/anchors and diffuser | DOCUMENTED stock |
| rear diffuser | 9.5×12×14.5 raw | one pixel/lens and rear-stack transform | VERIFIED raw / ASSUMPTION transform |
| halo | 74.94×38.75×24.86 raw | 10 mm strip path, wire exit and body disconnect | VERIFIED raw / ASSUMPTION route |

## 4. Placement, lens and clearances

| Item | Datum coordinate | Orientation | Confidence |
|---|---|---|---|
| speaker | X≈−30, L≈+43, base Z=3 | cone/port outboard | ASSUMPTION |
| amp | X≈−5, L≈−40, base/deck Z≈15 | flat, speaker terminals outboard | ASSUMPTION |
| centre brake/rain pixel | X≈−125, L=0, Z≈35 | behind translucent diffuser, lens aft | ASSUMPTION |
| indicator pairs | rear wing, L≈±40 | 66.7 mm two-pixel runs | ASSUMPTION |
| halo pair | halo centre path, ≈66.7 mm | curved/straight path TBD | ASSUMPTION |

Speaker cone/basket needs ≥3 mm free excursion/vent space (**ASSUMPTION**) and
cannot use the shell as a hard clamp. The port opening must not weaken a shell
boss or enter the body-removal edge. All LED optical faces remain unpainted.
Rear strip/tail requires ≥8 mm from DRS arm, shock, belt and axle.

Two pixels span 33.33 mm centre-to-centre and about 66.7 mm from the start of
the first pitch to the next two-pixel repeat (**DERIVED planning length**).
Actual cut-pad and diffuser positions must be measured on the physical strip;
no lens geometry is inferred from pitch alone.

## 5. Mounting method

- Speaker carrier uses a compliant isolation ring and a removable M3-supported
  bracket/plate clamp; do not screw through the cone frame without its real holes.
- Amp uses standoffs/foam plus positive retention on the removable deck. The
  terminal block faces the speaker route.
- LED strip uses its adhesive plus printed end anchors—adhesive alone is not
  sufficient under vibration/heat.
- Tail diffuser is translucent PLA/PETG as already specified; one or two thin
  optical walls and no primer/paint on the lens.
- Halo strip remains shell-mounted and disconnects through the single body
  connector. No loose tail can snag during KO-14 body lift.

## 6. Rail and cable assignment

Amp and LEDs use **Rail A clean** and common ground. Place 330 Ω in series with
the first LED data input and a 1000 µF/16 V reservoir across 5 V/GND at the
strip input if the second capacitor is available. Keep the amp's speaker pair
twisted and away from ADC/RP1/camera USB. The brake tail is pre-routed before
the rear stack; indicator/halo segments use service connectors and strain relief.

The 30-pixel worst case remains 1.8 A **DOCUMENTED arithmetic** (60 mA/pixel
upper bound). Installing seven pixels lowers physical stock use but does not
replace the D-24 measurement or the firmware current/brightness cap decision.

## 7. Mass and balance

Speaker+amp+installed segments are 25–55 g (**ASSUMPTION**). Left-side speaker
placement is deliberate ballast against the right ESC/deck and improves the
D-30 lateral ledger. Its exact benefit depends on the real 20–40 g speaker.
Do not add decorative LED mass at high Z solely to chase balance.

## 8. Assembly and fit gates

1. Caliper/weigh speaker and amp including connectors/holes.
2. Body-on dummy-fit speaker; prove ≥5 mm shell/static clearance, cone/port
   freedom, tool access and left-side balance benefit.
3. Place actual strip offcuts on rear diffuser, both wing ends and halo; record
   pixel centres, cut pads, wire exits and optical coverage.
4. Hand-sweep DRS/shock and remove shell ten times with harness installed.
5. Bench-check amp audibility/heat and LED voltage/current under D-24.
6. Production carriers/lenses follow only after those dimensions close D-36.

## 9. Remaining assumptions / stop conditions

Stop if the speaker presses the shell, a port cuts a boss, the amp connector
touches the roof, a diffuser needs paint on its optical face, a strip crosses a
hinge/shock/belt, the body snags a lead, or full-white demand browns Rail A.

