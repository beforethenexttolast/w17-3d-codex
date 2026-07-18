# N · Cable-Routing Plan

Session 2 · 2026-07-18. Harness/connector IDs per `M_…`; zones per `I_…`; combs and
guides per `K_…` (PS-08/09). Routes are PROVISIONAL until the D-10 wiring dry-fit and
D-26 rod-line measurement. Bend-radius rule: ≥5× cable OD everywhere, ≥8× at moving
interfaces. Edge protection (chamfer/grommet) wherever a harness passes a printed edge
or floor slot.

## N.1 Routing principles

1. **Two edge highways, open centre:** Rail A + signals run the **left** floor edge
   (R1); battery-voltage power + Rail B run the **right** floor edge (R2). The
   centreline (KO-01/19/06) is crossed only at defined stations.
2. **Crossing stations:** **X1** — floor level immediately **aft of the `Servoholder`**
   (behind the horn sweep, under the rod line per D-26), used by CN-15/H-08 branches
   and the CN-08 steering lead; **X2** — floor level at the **forward edge of Z3**
   (ahead of the battery, behind the tower base), used by H-04's RX/camera branches.
   Both crossings at 90°, combed both sides, ≥8 mm from any moving part.
3. **Noise separation:** H-03 (motor/ESC) never runs parallel to R1 within 20 mm;
   where H-04 (Rail A) and H-05 (Rail B) share the right bay for a short span they are
   combed into separate PS-08 fingers.
4. **Rear tail before the stack closes** (R-09/ASM-13): H-08 is laid into the
   drawing-`[7]` LED channel region with its service loop **before** ASM-10…12 close
   the rear; pull-through replacement is the design requirement on PS-09.

## N.2 Per-harness routes

| H | Route (physical) | Installed at | Entry → exit | Restraint | Loops | Heat/motion clearance | Removal |
|---|---|---|---|---|---|---|---|
| H-01 | battery → fwd along PS-01 wall → PS-15 | ASM-15 | tray notch → PS-15 fwd | tray comb | none (short) | clear of KO-01 overhead | unplug CN-01 |
| H-02 | inside PS-15 + short right hop to PS-03 (CN-05/06) | ASM-17 | block internal | block walls | — | — | at block |
| H-03 | PS-15 aft along R2 → ESC; ESC aft → motor (short) | ASM-16 | R2 combs → PS-02 grooves | PS-02 dressing groove | 30 mm at ESC | ≥8 mm from KO-06/08; sleeves hot zone (ASA combs) | CN-04 + bullets |
| H-04 | CN-23A up to CN-07 (deck power); branch at X2 → PS-06 (RX feed in CN-19 run) and → CN-24 (camera feed, fwd along R1) ; LED feeds: brake into H-08 at X1, halo to CN-14 at cockpit rim | ASM-17/22 | PS-03 → deck anchor / X2 | PS-08 R1+R2 combs | 50 mm at CN-07 | under rod line only at X2 (D-26) | per branch connector |
| H-05 | CN-23B aft: CN-08 (steer, exits at X1), CN-09/10 + CN-12 fwd-left to MOD-CAM base (via X1 then R1), CN-11 into H-08 tail | ASM-17/26/28 | PS-03 → X1 | combs at X1 both sides | 60 mm at gimbal axes | ≥8 mm to horn sweep (KO-11) | per connector |
| H-06 | deck-internal (I2S, UART E1↔E2, dividers) + CN-19 CRSF from Z2L along R1 → CN-07; CN-22 ESC signal from deck aft edge down to ESC; CN-21 speaker lead crosses at **X2** to Z4L if DN-07 selects the sidepod (S3) | ASM-22/23 | R1 → deck anchor | deck combs | CN-07 50 mm | above floor only, no motion crossings | with MOD-DECK |
| H-07 | camera↔WiFi USB D± run deck↔module (**CN-16 boundary at the deck fwd-inboard edge — S3/DN-11**): **routed R1**, twisted, ≤150 mm | ASM-26 | CN-16 at deck edge → module base | R1 combs + module clip | 60 mm across gimbal | never near H-03 | long run with MOD-CAM; deck unplugs at CN-16 |
| H-08 | rear tail: from X1 aft along **left** rear floor edge on PS-09 → CN-13 (brake LED into diffuser), CN-15 (Hall at axle), CN-11 (DRS up the stack) | **ASM-13 (pre-route)** | X1 → PS-09 channel | PS-09 rail + grommet | 80 mm tail + 60 mm Hall | ASA guide in hot pocket (E-05); ≥8 mm from KO-07/08/12 sweeps | pull-through |
| H-09 | CN-14 at PS-07 → up the shell inner surface to halo base (shell side taped/anchored) | ASM-27 | cockpit rim | PS-07 + shell anchors | 80 mm at CN-14 | clear of KO-14 insertion path | with shell |
| H-10 | U.FL pigtails: WiFi slot → PS-12 posts, ≤80 mm, no sharp bends | ASM-30 | deck rear | pigtail guides | — | — | at posts |
| H-11 | (opt, DN-08) USB pigtails E1/E2 → PS-17 park at cockpit rim, along R1 | ASM-31 | deck right edge → rim | R1 combs | 60 mm | — | unplug at boards |

Conflict checks designed against: KO-19 (X1 sits **behind** the horn sweep), steering
linkage (CN-08 exits laterally at X1, never along the rod), suspension arcs (R1/R2 stay
inboard of KO-04/KO-10), rear shocks/rockers (H-08 on the left edge, shock band is
central — ≥8 mm), drivetrain (only H-03 approaches, short), servo horns (comb fingers
at X1), DRS (CN-11 service loop lets the wing articulate), gimbal motion (60 mm loops
across both axes), body insertion (H-09 loop + nothing above deck height on the shell
path — KO-14 check at ASM-33), fastener access (combs never cover an M3 boss — D-27
map is the authority).

## N.3 Diagram 1 — logical power & signal

```
                 ┌────────────── MOD-BODY ──────────────┐
                 │ LGT-LED-HALO ◀─data+5V─ CN-14        │
                 └───────────────────▲──────────────────┘
 PWR-BAT ─CN-01▶ PS-15 ─CN-04▶ ESC ─▶ MOT               │
   │  [CN-02 key][DN-01 fuse]   ▲ CN-22 sig (red ✂)     │
   │        ├─CN-05▶ UBEC-A ─CN-23A─▶ RAIL A ─┬─▶ CN-07 ─┤─▶ CTL-E1 ─UART─ CTL-E2 ─I2S▶ AMP▶ SPK
   │        └─CN-06▶ UBEC-B ─CN-23B─▶ RAIL B ─┤          │      ▲CRSF CN-19─ RX-ELRS   └data▶ LEDs
   │                                          │          └─▶ VID-WIFI ◀─USB D± solder─ VID-CAM
   │   RAIL B ─▶ CN-08 STEER · CN-09/10 PAN/TILT · CN-11 DRS · CN-12 BLOWER
   └── star GND at PS-15 (all grounds common)          Hall ─CN-15▶ CTL-E1 · divider ─▶ CTL-E1
```

## N.4 Diagram 2 — physical harness routing (top view)

```
  FRONT                              X2                        X1                REAR
  ┌──────────┬───────────────────────┼─────────────────────────┼───────────────────┐
  │ Z2L: RX  ●━━CN-19/H-04 branch━━━━┿━━━━━ R1 (Rail A+signal) ┿━━━ H-07/H-08 ━━━━▶│ tail:
  │  ant ◀── │                       │  LEFT EDGE              │   (PS-09, left)   │ CN-13/15
  │          │   [KO-01 rod ↑ high]  │[KO-19 servo][KO-06 shock│                   │
  │ CENTRE:  │      OPEN SPINE       │   CN-08 exits at X1     │   band]  [Z6 drv] │
  │          │                       │                         │                   │
  │ Z2R: PS-15●━━ H-02 ━ PS-03/UBECs ┿━━━━━ R2 (power+Rail B) ━┿━━ H-03 ━▶ ESC●━▶MOT│
  │ CN-01/02 │   [deck PS-04 above───┼──── CN-07 anchor]       │  (fan up)         │
  └──────────┴───────────────────────┴─────────────────────────┴───────────────────┘
   Z3L battery: H-01 fwd to PS-15 · deck U.FL → PS-12 posts (rear) · CN-14 at cockpit rim
```

## N.5 Diagram 3 — module disconnects

```
  MOD-BODY ──CN-14──┐                          ┌──CN-19── MOD-RX
  MOD-CAM ──CN-09/10/12/24──┤ (+CN-16 USB ↔ MOD-DECK, S3/DN-11)   ├──CN-08── MOD-STR
  MOD-RLD ──CN-13/15/11──┤  CHASSIS LOOM       ├──CN-04/22── MOD-DRV(ESC)
  MOD-DECK ──CN-07(+U.FL CN-17/18)──┤          ├──CN-01── PWR-BAT
                        └── PS-15 junction ────┘   (CN-02 loop-key = master kill)
  Rule: any module out = its CN set + its mount fasteners. No desoldering in service.
```
