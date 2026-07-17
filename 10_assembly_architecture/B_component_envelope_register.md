# B · Component Envelope Register — every onboard item

Session 1 · 2026-07-17. **Purpose:** no expected onboard component may silently vanish
from the space plan. Each row carries a physical *installation envelope* (not just the
raw part), a status, and an evidence source. Confidence tags per [`README.md`](README.md).

> **Reading the envelope.** *Body* = the part's own bounding box. *Install envelope* =
> body **+ connector body + wire exit + minimum bend radius + mounting feature + service
> pull-out clearance**. A raw bounding box is **never** treated as the space needed.
> Where our specific hardware is unmeasured, the body is an **ESTIMATED** typical value
> and the install envelope is flagged **TO MEASURE**.

**Source key:** BOM = `docs/bill_of_materials_v2.md`; DS = typical datasheet/typical part
(ESTIMATED — verify on arrival); HAND = on hand, measurable now; TRANSIT = ordered, not
yet in hand; DRW = supplier drawing; PROBE = STL/mesh probe this session.

---

## B.1 Physical envelope table

| ID | Component | Qty | Body (mm) | Install envelope (mm) | Status | Evidence |
|---|---|---|---|---|---|---|
| PWR-BAT | 2S LiPo pack | 1 (×2 **planned**, swap — none bought yet; corrected 1.5) | **≤75 × 45 × 25** (hard limit) | +XT60 lead exit ~20 & bend + strap/retention → allow ~**95 × 50 × 30** pocket | envelope CONFIRMED; pack not chosen | BOM, 2024-body README |
| DRV-MOT | Rocket 540 V3 motor | 1 | ~Ø36 × 53 (can) **EST** | + sensor lead + 3 phase wires (rear exit) + pinion | fixed by drivetrain geometry | BOM, DS |
| DRV-ESC | QuicRun 10BL120 ESC | 1 | ~36 × 32 × 18 + fan **EST** | + fan airflow clearance ≥10 top + 3 batt/3 motor wires + signal | TO MEASURE | BOM, DS, photo (ESC+fan mid-chassis) |
| SRV-STEER | DS3235SG steering servo | 1 | ~40 × 20 × 40.5 **EST** (std size) | into `Servoholder` pocket + horn sweep + 3-wire lead | fit-check TO MEASURE (Gate D residual) | BOM, DRW `[2]/[3]` |
| SRV-PAN | MG90S (pan) | 1 | ~23 × 12.2 × 29 **EST** | + horn sweep + lead; at camera gimbal | TO MEASURE | BOM, DS, CAMERA_GIMBAL_PLACEMENT |
| SRV-TILT | MG90S (tilt) | 1 | ~23 × 12.2 × 29 **EST** | + horn sweep + lead; at camera gimbal | TO MEASURE | BOM, DS |
| SRV-DRS | MG90S (DRS) | 1 | ~23 × 12.2 × 29 **EST** | into rear-wing DRS pocket + metal-rod link | fit-check TO MEASURE | BOM, DRW `[2]` |
| CTL-E1 | ESP32-WROOM DevKit V1 #1 (control) | 1 | ~55 × 28 × 13 **EST** (30-pin wide) | + Dupont pin field (both long edges, +8 each) + micro-USB end access | TO MEASURE / needs USB port | BOM, DS |
| CTL-E2 | ESP32-WROOM DevKit V1 #2 (sound/light) | 1 | ~55 × 28 × 13 **EST** | as E1; UART to E1 | TO MEASURE / USB access | BOM, DS |
| CTL-E3 | ESP32 spare | 1 | — | not installed (spare) | n/a | BOM |
| RX-ELRS | RadioMaster RP1 ELRS RX | 1 | ~20 × 12 × 3 **EST** + T-antenna | + antenna routing (keep away from metal/motor) | TO MEASURE | BOM, DS |
| VID-CAM | Camera SSC338Q + IMX335 board | 1 | **TO MEASURE** (board + heatsink + lens) | + lens FOV cone + cable exit + service pull | TO MEASURE (Gate C) | BOM, HAND |
| VID-WIFI | BL-M8812EU2 USB WiFi module | 1 | **TO MEASURE** (high-power USB module) | + 28×28×3 heatsink + 2× U.FL pigtails + airflow | TO MEASURE | BOM; ⚠ on-hand status **UNCONFIRMED** (1.5: only the camera is documented on hand — verify before relying on D-06b "now") |
| VID-ANT | 5.8 GHz U.FL omni antennas | 2 (of 5) | 70 mm whip each | + clearance from metal + mount at body edge | TO MEASURE placement | BOM |
| VID-HS | Heatsink for WiFi module | 1 (of 2) | **28 × 28 × 3** | bonded to module; adds to VID-WIFI stack | CONFIRMED | BOM |
| AUD-AMP | MAX98357A I2S amp | 1 | ~17 × 15 × 3 **EST** | + I2S 3-wire + 2 speaker wires | TO MEASURE | BOM, DS |
| AUD-SPK | Speaker 4 Ω 3 W | 1 | ~Ø28–40 × 6–12 **EST** | + baffle/port + 2 wires; wants a sidepod opening | TO MEASURE (model dims) | BOM |
| LGT-LED | WS2812B strip, 30 LED/1 m | 1 | 10 mm wide flexible strip, cut to segments | + 3-wire tails + 330 Ω + routing to brake/halo; **rear tail must be routed before the rear stack closes** (drawing `[7]` has a designed "Pass LED here" channel on the Rev-1 path; added 1.5) | segments TO DEFINE | BOM, DRW `[7]` |
| LGT-DIFF | `rearbacklightdiffuser` (printed) | 1 | 9.5 × 12 × 14.5 (DERIVED) | houses ≥1 WS2812; lens unpainted | CONFIRMED bbox | CSV, MODEL_INVENTORY |
| PWR-UBEC-A | UBEC 5 A (Rail A clean) | 1 | ~30 × 14 × 10 **EST** (heatshrink) | + in/out leads; feeds cam/wifi/ESP/RX/LED | TO MEASURE | BOM, DS |
| PWR-UBEC-B | UBEC 5 A (Rail B servo) | 1 | ~30 × 14 × 10 **EST** | + leads; feeds 4 servos + blower | TO MEASURE | BOM, DS |
| PWR-Y | XT60 Y-split (battery main) | 1 | ~XT60 body 16 × 8 × 8 ×3 + wye | bulky junction; needs a home | TO MEASURE | BOM |
| PWR-XT30 | XT30 accessory taps | few | ~12 × 6 × 6 each | low-current taps | — | BOM |
| PWR-CAP | 1000 µF / 16 V electrolytic | 1–2 | ~Ø10 × 20 **EST** | across servo rail / LED rail | TO MEASURE | BOM |
| PWR-PROT | Main-line fuse / overcurrent protection | 0 | — | **absent from BOM v2** — no fuse anywhere; the XT60 unplug is the de facto main disconnect and SW-PWR is undecided | **DECISION NEEDED** (deliberate omission vs oversight — added 1.5) | BOM (absence), Session 1.5 review |
| SNS-HALL | A3144 Hall sensor | 1 | TO-92 ~4 × 3 × 5 **EST** | at rear axle, gap to magnet ~1–3 mm; hot pocket | TO MEASURE mount | BOM, DS |
| SNS-MAG | Neodymium magnet 3 × 1 mm | 1 | Ø3 × 1 | glued to rear axle | CONFIRMED spec | BOM |
| SNS-DIV | Voltage divider (27k/10k) | 1 | 2 resistors, ~negligible | inline on battery sense wire | — | BOM |
| COOL-BLOW | Blower 5 V 20 mm (ACP2006) | 1 | ~20 × 20 × 10 **EST** | + XH2.54 + duct interface to camera | TO MEASURE (TRANSIT) | BOM |
| COOL-DUCT | Camera cooling duct (from `.scad`) | 1 | parametric — **TO DESIGN** | wraps blower→camera; 9 "MEASURE THESE" dims | TO MEASURE (Gate C) | FIRST_PRINT_DECISION §6 |
| SW-PWR | Power switch | 0–1 | ~15 × 8 × 12 **EST** | reference build mounts one on front floor | optional / TO DECIDE | photo `…55` |
| PWR-BUZZ | BX100 low-voltage buzzer | 0–1 | ~30 × 12 × 8 **EST** | optional independent alarm | optional | BOM |
| USB-PORT | ESP32 / camera USB service access | — | a *port*, not a part | needs a body opening or pigtail to reach USB | **DOES NOT EXIST** — TO DESIGN | A §7 |
| HW-INSERT | Heat-set inserts M3×5 | pack | per boss | for repeated-service bosses (body, battery) | recommended | BOM, ASSEMBLY_NOTES |
| HARNESS | Wiring loom, Dupont, silicone wire, zip ties, heatshrink | bulk | **the dominant volume** (see photos) | strain relief across every moving axis | TO MEASURE | photos, BOM |
| FUT-EXP | Future expansion (spare GPIO devices) | ? | unknown | reserve a little volume | placeholder | — |

*Deliberately not onboard (noted 1.5): FT232RL USB-UART (bench flashing tool), ES24TX
TX module, chargers, thermal paste and other consumables — bench/off-car items from BOM
v2, excluded from the space plan on purpose.*

---

## B.2 Electrical / thermal / orientation attributes

| ID | Rail | V | I typ / peak | Heat | Connector(s) | Orientation / vibration / access |
|---|---|---|---|---|---|---|
| PWR-BAT | source | 7.4 V 2S | high (motor draw) | mild warmth | XT60 | flat, strapped; **removable often** — service-critical |
| DRV-MOT | ESC | 7.4 V | **high / very high** | **hot** | bullet ×3 + sensor | fixed transverse; strong vibration source |
| DRV-ESC | battery | 7.4 V | high | **hot** (has fan) | XT60 in, bullets out, signal; **isolate the ESC's internal BEC +5 V (red) wire — the UBECs own the rails** (BOM bench note; carried in 1.5) | fan needs airflow; keep clear of camera rail electrically |
| SRV-STEER | B | 5–6 V | ~1–3 A peak | warm | 3-pin | horn sweep clearance; into `Servoholder` |
| SRV-PAN/TILT/DRS | B | 5 V | ~0.5–1 A peak ea | warm | 3-pin | positional (not 360°); horn sweep; gimbal stiffness matters (VR) |
| CTL-E1/E2 | A (clean) | 5 V→3.3 V | ~0.1–0.5 A | warm | micro-USB + pins | **USB access needed**; ESD; keep RF sense wiring short |
| RX-ELRS | A | 5 V | low | cool | 5-pin CRSF/UART | **antenna orientation + metal clearance** (2.4 GHz) |
| VID-CAM | **A only** (never USB rail) | 5 V | moderate | **runs hot** | solder pads + lens | lens boresight/roll alignment (VR); no lens clamping; forced-air likely |
| VID-WIFI | A | 5 V | moderate–high | **runs hot** (heatsink mandatory) | USB + 2× U.FL | antennas on **before** power; 5.8 GHz — separate from ELRS 2.4 GHz |
| AUD-AMP | A | 5 V | moderate on transients | warm | I2S 3-wire + spk | keep speaker wires from sense lines |
| AUD-SPK | (amp) | — | — | — | 2-wire | wants a vent/port to be audible |
| LGT-LED | A (5 V) | 5 V | ~0.6 A typical animated; **~1.8 A worst-case** (60 mA/LED × 30, full white — corrected 1.5; cap in firmware or budget the rail) | mild | 3-wire + 330 Ω + 1000 µF | flexible; brake at rear, halo at cockpit |
| PWR-UBEC-A | battery→5 V | 5 V/5 A | — | warm | leads | "clean" rail — physically separate routing from Rail B |
| PWR-UBEC-B | battery→5–6 V | 5–6 V/5 A | — | warm | leads | servo rail — noisy; keep from video rail |
| SNS-HALL | A | 5 V | low | — (but hot *location*) | 3-wire, 10k pull-up | 1–3 mm to axle magnet; hot rear pocket |
| COOL-BLOW | **B / decoupled 5 V** (never camera rail) | 5 V | low | — | XH2.54 | ducted to camera; inlet/outlet path required |

> **Rail budget (added Session 1.5).** No per-rail current budget existed anywhere in
> the project. Worst-case sums of the ESTIMATED rows above: **Rail A** — WiFi module
> (high-power USB, ~1–2 A) + camera (~0.5 A) + 2× ESP32 (~0.5 A) + RX (~0.1 A) + LED
> (up to ~1.8 A full-white) can **approach or exceed the 5 A UBEC**; **Rail B** —
> DS3235SG stall (~3 A) + 3× MG90S stalls + blower can transiently do the same. All
> figures are ESTIMATED → **bench-measure both rails at peak before the final harness**
> (D-24, risk E-23). UBEC self-heating at high load also joins the D-19 thermal run.

---

## B.3 Components with a COMPLETE envelope (usable now)

- **PWR-BAT** envelope (≤75 × 45 × 25 mm, hard designer limit — CONFIRMED) — *the pack
  itself* is not chosen, but the **envelope to design to** is fixed.
- **VID-HS** heatsink **28 × 28 × 3 mm** (CONFIRMED, BOM).
- **SNS-MAG** magnet Ø3 × 1 mm (CONFIRMED).
- Printed parts with CONFIRMED DERIVED bboxes: `rearbacklightdiffuser`, `camera top 1.1`,
  `Servoholder` (22.9 × 10 × 58), and all mechanical parts (see CSV / Report A).

## B.4 Components with MISSING dimensions (block a full space plan)

| Component | Why it matters | How to resolve |
|---|---|---|
| **VID-CAM** camera board + heatsink + lens | governs the nose/pod cavity + duct + FOV | **HAND — measure with calipers now** (Gate C, D-06) |
| **VID-WIFI** WiFi module | bulky, hot, 2 antennas — a major body | possession **UNCONFIRMED** (1.5) — verify, then measure (D-06b) |
| **DRV-ESC** 10BL120 + fan | governs mid-chassis volume + airflow | TRANSIT — measure on arrival (D-08) |
| **SRV-STEER** DS3235SG | must fit `Servoholder` pocket | TRANSIT — fit-check (D-09) |
| **MG90S** ×3 | pockets + horn sweep | TRANSIT — fit-check (D-09) |
| **AUD-SPK** speaker | needs a sidepod pocket + port | TO MEASURE (model dims) |
| **UBEC ×2, amp, RX, caps, blower** | sidepod/airbox pockets | mostly TRANSIT — measure on arrival |
| **HARNESS** loom bulk | the *dominant* real-world volume (photos) | only knowable at wiring dry-fit (D-10) |

**Nothing above is allowed to disappear from the Session-2 space plan** — each is carried
into Report F as a mandatory or optional envelope with its resolution route.
