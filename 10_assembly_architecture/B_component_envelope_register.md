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

> **HAND / TRANSIT here mean *measurement-readiness*, not an arrival ledger.** They record
> whether this repo can measure/fit the part yet — **not** when it shipped or arrived. The
> authoritative arrival / on-hand log for the whole build is `../HARDWARE_INVENTORY.md`
> (workspace-level, current as of 2026-07-22); if it and a flag here ever disagree on
> arrival, that file wins. This register never asserts a part *was measured or fitted* until
> a dated measure/fit record says so.

---

## B.1 Physical envelope table

| ID | Component | Qty | Body (mm) | Install envelope (mm) | Status | Evidence |
|---|---|---|---|---|---|---|
| PWR-BAT | 2S LiPo pack | 1 (×2 **planned**, swap — none bought yet; corrected 1.5) | **≤75 × 45 × 25** (hard limit) | +XT60 lead exit ~20 & bend + strap/retention → allow ~**95 × 50 × 30** pocket | envelope CONFIRMED; pack not chosen | BOM, 2024-body README |
| DRV-MOT | Rocket 540 V3 motor | 1 | ~Ø36 × 53 (can) **EST** | + sensor lead + 3 phase wires (rear exit) + pinion | fixed by drivetrain geometry | BOM, DS |
| DRV-ESC | QuicRun 10BL120 ESC | 1 | ~36 × 32 × 18 + fan **EST** | + fan airflow clearance ≥10 top + 3 batt/3 motor wires + signal | TO MEASURE (HAND) | BOM, DS, photo (ESC+fan mid-chassis); on hand `../HARDWARE_INVENTORY.md` §3 |
| SRV-STEER | DS3235SG steering servo | 1 | 40 × 20 × 40.4 **DOCUMENTED** standard case envelope | installed side-on: ~40 longitudinal ×40.4 lateral ×20 high in `Servoholder`; horizontal/lateral shaft + vertical 25T horn + lead. Holder arch 42×18.5, so fit remains physical | fit-check TO MEASURE (HAND; Gate D residual) | BOM, DRW `[2]/[3]`, DS drawing, report `Y`; on hand `../HARDWARE_INVENTORY.md` §6 |
| SRV-PAN | MG90S (pan) | 1 | ~23 × 12.2 × 29 **EST** | + horn sweep + lead; at camera gimbal | TO MEASURE | BOM, DS, CAMERA_GIMBAL_PLACEMENT |
| SRV-TILT | MG90S (tilt) | 1 | ~23 × 12.2 × 29 **EST** | + horn sweep + lead; at camera gimbal | TO MEASURE | BOM, DS |
| SRV-DRS | MG90S (DRS) | 1 | ~23 × 12.2 × 29 **EST** | into rear-wing DRS pocket + metal-rod link | fit-check TO MEASURE | BOM, DRW `[2]` |
| CTL-E1 | dual-core ESP32-WROOM-32 D1-Mini-ESP32 / MH-ET Live MiniKit #1 (control) | 1 | **39 × 31 × ~13 with headers — FIRM input** | wall-mounted vertically; micro-USB at service edge; keep live-plug/header/wire-bend volume open | identity/body envelope FIRM; holes and installed service volume TO CALIPER | owner/Claude selection; **not** C3/S2/S3 SuperMini |
| CTL-E2 | dual-core ESP32-WROOM-32 D1-Mini-ESP32 / MH-ET Live MiniKit #2 (sound/light) | 1 | **39 × 31 × ~13 with headers — FIRM input** | as E1; link2/I2S/WS2812 pin map unchanged | identity/body envelope FIRM; holes and installed service volume TO CALIPER | owner/Claude selection; **not** C3/S2/S3 SuperMini |
| CTL-E3 | ESP32 spare | 1 | — | not installed (spare) | n/a | BOM |
| RX-ELRS | RadioMaster RP1 ELRS RX | 1 | ~20 × 12 × 3 **EST** + T-antenna | + antenna routing (keep away from metal/motor) | TO MEASURE | BOM, DS |
| VID-CAM | Camera SSC338Q + IMX335 board | 1 | **TO MEASURE** (board + heatsink + lens) | + lens FOV cone + cable exit + service pull | TO MEASURE (Gate C) | BOM, HAND |
| VID-WIFI | BL-M8812EU2 USB WiFi module | 1 | **TO MEASURE** (high-power USB module) | + 28×28×3 heatsink + 2× U.FL pigtails + airflow | TO MEASURE (HAND) | BOM, HAND — on hand per `../HARDWARE_INVENTORY.md` §1 (arrived 07-17); measure now (D-06b) |
| VID-ANT | 5.8 GHz U.FL omni antennas | 2 (of 5) | 70 mm whip each | + clearance from metal + mount at body edge | TO MEASURE placement | BOM |
| VID-HS | Heatsink for WiFi module | 1 (of 2) | **28 × 28 × 3** | bonded to module; adds to VID-WIFI stack | CONFIRMED | BOM |
| AUD-AMP | MAX98357A I2S amp | 1 | ~17 × 15 × 3 **EST** | + I2S 3-wire + 2 speaker wires | TO MEASURE | BOM, DS |
| AUD-SPK | Speaker 4 Ω 3 W | 1 | ~Ø28–40 × 6–12 **EST** | + baffle/port + 2 wires; wants a sidepod opening | TO MEASURE (model dims) | BOM |
| LGT-LED | WS2812B strip, 30 LED/1 m | 1 | 10 mm wide flexible strip, cut to segments | + 3-wire tails + 330 Ω + routing to brake/halo; **rear tail must be routed before the rear stack closes** (drawing `[7]` has a designed "Pass LED here" channel on the Rev-1 path; added 1.5) | segments TO DEFINE | BOM, DRW `[7]` |
| LGT-DIFF | `rearbacklightdiffuser` (printed) | 1 | 9.5 × 12 × 14.5 (DERIVED) | houses ≥1 WS2812; lens unpainted | CONFIRMED bbox | CSV, MODEL_INVENTORY |
| PWR-UBEC-A | UBEC 5 A (Rail A clean) | 1 | ~30 × 14 × 10 **EST** (heatshrink) | + in/out leads; feeds cam/wifi/ESP/RX/LED | TO MEASURE | BOM, DS |
| PWR-UBEC-B | UBEC 5 A (Rail B servo) | 1 | ~30 × 14 × 10 **EST** | + leads; feeds 4 servos + blower | TO MEASURE | BOM, DS |
| PWR-PDB | cassette power-distribution board incl. 2× UBEC, 1000 µF cap, divider, charge input/interlock and star ground | 1 | **55 × 45 × ~18 TARGET**, ~50 g TARGET | + XT60/XT30 bodies, loop-key finger access, tall-part airflow and M3 floor/service envelope | contents FIRM; final geometry/mass ASSUMPTION / ASM-22 | `../w17-electrical-inputs-for-codex.md`; ZK |
| PWR-CHG | 5 V USB-C → 2S balancing charge board | 1 | **30 × 25 × ~10 TARGET** | + USB-C/balance/battery exits, thermal face and charge/run service access | SKU TBD; TARGET/ASSUMPTION / ASM-59 | `../w17-electrical-inputs-for-codex.md`; OP-49 |
| PWR-Y | XT60 Y-split (battery main) | 1 | ~XT60 body 16 × 8 × 8 ×3 + wye | bulky junction; needs a home | TO MEASURE | BOM |
| PWR-XT30 | XT30 accessory taps | few | ~12 × 6 × 6 each | low-current taps | — | BOM |
| PWR-CAP | 1000 µF / 16 V electrolytic | 1–2 | ~Ø10 × 20 **EST** | across servo rail / LED rail | TO MEASURE | BOM |
| PWR-PROT | Main-line fuse / overcurrent protection | 0 | — | **absent from BOM v2** — no fuse anywhere; the XT60 unplug is the de facto main disconnect and SW-PWR is undecided | **DECISION NEEDED** (deliberate omission vs oversight — added 1.5) | BOM (absence), Session 1.5 review |
| SNS-HALL | A3144 Hall sensor | 1 | TO-92 ~4 × 3 × 5 **EST** | at rear axle, gap to magnet ~1–3 mm; hot pocket | TO MEASURE mount | BOM, DS |
| SNS-MAG | Neodymium magnet 3 × 1 mm | 1 | Ø3 × 1 | glued to rear axle | CONFIRMED spec | BOM |
| SNS-DIV | Voltage divider (27k/10k) | 1 | 2 resistors, ~negligible | inline on battery sense wire | — | BOM |
| COOL-BLOW | Blower 5 V 20 mm (ACP2006) | 1 | ~20 × 20 × 10 **EST** | + XH2.54 + duct interface to camera | TO MEASURE (HAND) | BOM; on hand `../HARDWARE_INVENTORY.md` §13 |
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
| **VID-WIFI** WiFi module | bulky, hot, 2 antennas — a major body | HAND — on hand per `../HARDWARE_INVENTORY.md` §1 (arrived 07-17); measure now (D-06b) |
| **DRV-ESC** 10BL120 + fan | governs mid-chassis volume + airflow | HAND — on hand per `../HARDWARE_INVENTORY.md` §3; measure now (D-08) |
| **SRV-STEER** DS3235SG | must fit `Servoholder` pocket | HAND — on hand per `../HARDWARE_INVENTORY.md` §6; fit-check now (D-09) |
| **MG90S** ×3 | pockets + horn sweep | TRANSIT — fit-check on arrival (D-09) |
| **AUD-SPK** speaker | needs a sidepod pocket + port | TO MEASURE (model dims) |
| **UBEC ×2, amp, RX, blower** | sidepod/airbox pockets | HAND — on hand per `../HARDWARE_INVENTORY.md` (§5 / §4 / §2 / §13); measure now. Caps = §D build-from-stock (owned, not delivery-verified) |
| **PWR-PDB** | target envelope packs only when rotated; final tall-part/connector/loop-key layout owns the cassette | refine 55×45×18/~50 g TARGET after component placement; ASM-22 calipers/holes/exits |
| **PWR-CHG** | SKU controls holes, thermal face and USB-C/balance exits | select after pack, then caliper against 30×25×10 TARGET at ASM-59 |
| **HARNESS** loom bulk | the *dominant* real-world volume (photos) | only knowable at wiring dry-fit (D-10) |

**Nothing above is allowed to disappear from the Session-2 space plan** — each is carried
into Report F as a mandatory or optional envelope with its resolution route.

## B.5 Remaining-component fit-study roll-up (2026-07-23)

This section uses the steering-study vocabulary exactly: **VERIFIED / DERIVED /
DOCUMENTED / ASSUMPTION**. It supersedes conflicting planning blocks in B.1; the
complete 58-row table is
[`evidence/p0/tables/p0_d28_zone_component_envelopes.md`](evidence/p0/tables/p0_d28_zone_component_envelopes.md),
reproduced by `evidence/scripts/p0_07_zone_fit_rollup.py`.

| ID/group | Corrected body/envelope | Confidence | Register consequence |
|---|---|---|---|
| **DRV-ESC** | **43×36.8×32.3 mm**, 101.5 g incl. wires; framed fan 25×25×10; add ≥10 mm open above fan | DOCUMENTED for non-WP Sensored G2; on-hand identity ASSUMPTION | supersedes 36×32×18; PS-02/CAD-03/dummy frozen pending D-28 |
| **DRV-MOT** | Ø36×54 can, Ø3.175×14.5 shaft; add tabs/sensor/pinion pull | DOCUMENTED family; real can physical residual | rear thermal/gear gate |
| **DRV-SPUR/PINION** | 48P pitch Ø39.69 / Ø14.82; theoretical pitch-centre 27.25 mm | DERIVED | does not close hub/bolt/backlash |
| **PWR-BAT-1** | ≤75×45×25; 95×50×30 installed allocation | DOCUMENTED limit / ASSUMPTION mass and connector | one active onboard candidate only |
| **PWR-BAT-2** | same body, **off-car swap** on selected architecture | DERIVED packaging conclusion | two-onboard requires a new architecture/power review |
| **MG90S ×3** | 22.8×12.2×28.5, 13.4 g each | DOCUMENTED genuine TowerPro; clone fit ASSUMPTION | caliper/pocket/sweep D-35 |
| **RX-ELRS** | 13×11×3; 65 mm T antenna; 2.2 g | DOCUMENTED | replaces ~20×12×3 estimate |
| **VID-WIFI / ESP32 ×2** | Wi-Fi ≤60×32×12 allocation / each ESP wall-seat gauge ~39×31×~13 with headers | Wi-Fi ASSUMPTION; ESP family/pins VERIFIED by owner, installed envelope ASSUMPTION | D-28 DevKit blocks remain historical; cassette re-audit uses the two D1-Mini-ESP32 gauges |
| **VID-CAM** | sensor identity **IMX335 FIRM**; MC800S-V3 base 19.2×19.2 transverse ×30.7 axial remains the documented body reference | identity FIRM; complete installed envelope ASSUMPTION until D-34 | no camera mount CAD until board/heatsink/lens/exits are calipered |
| **AUD-AMP / AUD-SPK** | 19.4×17.8×3 reference / Ø28–40×6–12 planning | ASSUMPTION for purchased parts | D-36 physical measure |
| **LGT-LED** | 10 mm strip, 33.33 mm pitch; proposed 7 installed pixels | DOCUMENTED stock / ASSUMPTION segmentation | one centre, 2+2 indicators, 2 halo; remainder spare |
| **SHK-FRONT/REAR** | front **51 mm requirement / 52 mm received-stock label**; rear 68 mm; actual eye-to-eye/body/stroke unknown | DOCUMENTED conflict and rear length / ASSUMPTION physical | D-12/D-37 must resolve front value; full swept cylinders remain ASSUMPTION |
| **TYRE-F/R** | Ø64×30 / Ø64×35 | DOCUMENTED | body-on full steer/bump gate |
| **SNS-HALL/MAG** | max 4.17×3.10×1.57 / Ø3×1 | DOCUMENTED | bracket/gap/field remain ASSUMPTION |

Mass and connector/service additions are part of the envelope. A documented body
does not become a complete install envelope until its real exits, mounts and motion
have been recorded.

## B.6 Cassette physical-audit extension (2026-07-24)

This is a non-production fit-gauge overlay for
[`fit_studies/ZK_electronics_cassette_fit_study.md`](fit_studies/ZK_electronics_cassette_fit_study.md).
It does not replace B.5 or turn a placeholder into a purchased-part dimension.

| ID | Physical audit envelope | Confidence | Gate consequence |
|---|---|---|---|
| **CAS-BOX** | stepped-T gauge: rear stem X−31…+1/L−18.5…+17.5; forward wing X+1…+42/L±43; tapered tongue X+42…+46/L±29.5; cell-driven top Z19 | ASSUMPTION | named lower targets pack, but Wi-Fi/dock/mounting and moving clearance remain open |
| **CAS-PDB-CELL** | **55×45×18 mm, ~50 g TARGET** at X+1…+46/L±27.5/Z1…19; includes 2× UBEC + cap | contents FIRM; final dimensions/mass ASSUMPTION | shell gauge passes; only 3 mm to KO-01 versus 8 mm policy |
| **CAS-CHG-CELL** | **30×25×10 mm TARGET** at X−31…−1/L−13…+12/Z1…11 | SKU TBD / ASSUMPTION / DEFER seat | ASM-59 selects/calipers SKU; no hole or thermal face inferred |
| **CAS-ESP-L/R** | two 39 X ×31 Z ×~13 L wall-seat envelopes: X+3…+42, L−43…−30 and +30…+43, Z1…32 | identity/envelope FIRM; installed geometry ASSUMPTION | clears provisional KO-01 laterally by 8 mm; requires S0≥9.82 and live-plug check |
| **CAS-PEDESTAL** | hollow floor/front-structure pedestal X+51…+65/L±11; conduit target 10×18 clear with 2 mm trial wall →14×22 outer | ASSUMPTION; MG90S DEFER | 5 mm to PDB tongue/5.6 mm to front block; plug, wall, steering, halo/FOV/sweep gated |
| **CAS-DOCK** | firm minimum 1×XT60, 2×XT30, 5×3-pin servo, 3×XH3, 1×shielded USB4 plus auxiliary seats; internal XH4/XH3/XH5 +2×U.FL | map FIRM; body allocations/topology ASSUMPTION | straight X+42…+58/L±32 projection overlaps pedestal; stepped/wrapped full-size dummy required |
| **DRV-ESC-CURRENT** | 44.2×37×24.2 mm, 100 g loose; height includes fan to top screw | DOCUMENTED owner physical ground truth | retains prior provisional study result as history; new body/wire/fan station gate required |
| **VID-CAM-CURRENT** | IMX335 MC800S-V3 base 19.2×19.2 transverse ×30.7 axial | DOCUMENTED owner physical ground truth | mount, exits, mass, blower, lens/FOV and gimbal sweep still open |

The final PDB geometry/mass, charge SKU and every terminated connector body
remain ASSUMPTION until their named ASM checks. The MG90S, exact 2S pack and
charge-module seat remain **DEFERRED**.
The board-selection verification is electrical identity/pin availability only:
control retains all 11 signals including input-only GPIO34 battery ADC1 and
GPIO35 Hall; sound/light retains link2 RX16, I2S 22/25/26 and WS2812 GPIO4.
Firmware and pin maps therefore remain unchanged. Mechanical closure still uses
the assumed installed envelope until the exact dual-core WROOM-32 SKU is
calipered; a C3/S2/S3 SuperMini is a different, rejected family for this gauge.
