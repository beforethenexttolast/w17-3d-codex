# D · Measurement Plan — what must be measured before final CAD

Session 1 · 2026-07-17. Every unresolved measurement that gates the assembly
architecture. **Blocks** column: C=CAD/mount design, P=printing, W=wiring, F=final
assembly. "Dummy OK?" = can a printed/foam dummy of the right envelope substitute until
the real part arrives. Confidence tags per [`README.md`](README.md).

| ID | Measurement | Reference points | Tool | Accuracy | Why it matters | Decisions affected | Dummy OK? | Blocks |
|---|---|---|---|---|---|---|---|---|
| **D-01** | Battery bay **usable length** + internal bosses/bulkheads | floor top plane ↔ shell interior at the junction (Z3) | slicer (assemble floor+FRONT+REAR shells) → then calipers on prints | ±2 mm | length is the *unproven* battery dimension (§7); width/height already ~clear | final battery pack; retention scheme | **yes** (75×45×25 foam block) | C, F |
| **D-02** | **Net** electronics-spine volume with mechanicals *placed* | central shock + drivetrain + steering rod in situ ↔ shell roof | dry-fit + calipers/photos | ±3 mm | geometry cavity is a gross upper bound; net is far smaller | whole electronics layout | partial | C, F |
| **D-03** | Sidepod L/R **internal pocket** clearance | inner sidepod wall ↔ floor edge | slicer section + printed dry-fit | ±2 mm | UBEC/amp/RX/speaker are planned here, unmeasured (Z4) | sidepod mounts, speaker port | yes | C, F |
| **D-04** | **Roof clearance** over the tallest electronics stack | top of ESP32/airbox stack ↔ shell underside (KO-14) | dry-fit body-on | ±2 mm | taller stack than original; clamshell may foul | ESP32 stack height, airbox spine | yes | F |
| **D-05** | King-pin knuckle **bore ≈ 3 mm** | `Steering Block4` pivot bore | slicer measure + calipers on print | ±0.1 mm | M3×30 dowel fit; steering geometry | reprint tolerance if off | no | P, F |
| **D-06** | **Camera** board + heatsink + lens W/H/thickness/total depth/lens Ø/lens offsets/holes/cable exit | the real SSC338Q+IMX335 (**on hand**) | **calipers, now** | ±0.2 mm | governs pod/duct/FOV; "no product-page dims" (Gate C) | camera mount + duct + placement | no | C, P |
| **D-06b** | **WiFi module** + heatsink envelope + U.FL exit | real BL-M8812EU2 (⚠ possession **UNCONFIRMED** — 1.5: Session 1 marked it on-hand but only the camera is documented on hand; verify first) | calipers, on confirm/arrival | ±0.5 mm | bulky, hot, 2 antennas — a major body | airbox/nose packing, RF | no | C |
| **D-07** | Camera **FOV cone + boresight/roll datum + service pull** | lens axis ↔ body opening; mount ↔ chassis straight-ahead | bench + protractor/level | ±1° roll | VR: tilted horizon = nausea; FOV must clear body | mount design, placement A vs B | dummy for pull only | C |
| **D-08** | **ESC 10BL120 + fan** L/W/H + wire exits + fan airflow gap | real ESC on arrival | calipers | ±0.5 mm | governs mid-chassis volume + airflow (KO-16) | ESC location, duct routing | yes | C, F |
| **D-09** | **DS3235SG** + **MG90S** fit-checks | `Servoholder` pocket; DRS/gimbal pockets | calipers + trial fit on arrival | ±0.3 mm | Gate D residual + DRS/gimbal pockets | floor batch print, wing print | no | P, F |
| **D-10** | **Harness bulk + strain-relief** across moving axes | routed loom on placed chassis | wiring dry-fit + photos | qualitative | loom is the dominant real volume (photos) | cable channels, tie-down bosses | no | W, F |
| **D-11** | **USB / programming access** for 2× ESP32 + camera console | USB ports ↔ nearest body opening | dry-fit | ±2 mm | no service port exists today (A §7) | body opening or pigtail design | yes | C, F |
| **D-12** | **Front shock eye-to-eye 51 vs 52 mm** | ordered front shocks | calipers on arrival | ±0.5 mm | 1 mm discrepancy (Ryan vs v2); front geometry | front shock-mount fit | no | F |
| **D-13** | Review Rev-1 drawings **[4]/[6]/[8]/[9]** | the PDFs (not yet viewed) | Read/inspect | — | may carry rear-stack/floor/final-install detail for Gate A | Gate A closure evidence | n/a | (evidence) |
| **D-14** | **Gate A**: does the selected rear rocker/spring-mount **seat AND articulate** the **68 mm** shock? | `Spring mount 2 REV1` ↔ 68 mm coilover eye-to-eye | slicer + diagnostic TP dry-fit | ±1 mm + motion | **BLOCKER** for the whole rear stack | rear-stack file set, ASA batch | TP diag prints | P, F |
| **D-15** | Rear-stack identity: do **Motor Covers replace `Left/Rightrearaxle`**? which STL is "Light Cover"? | drawing `[7]` vs parts | slicer + `[7]` + TP dry-fit | — | decides which files are REQUIRED | rear file list | TP diag | P |
| **D-16** | **Spur ↔ belt-pulley bolt pattern** | 3Racing 75T spur ↔ belt-set pulley | calipers on arrival | ±0.2 mm | mesh/mount validity | drivetrain assembly | no | F |
| **D-17** | **2021 rear wing + mount + DRS arm + diffuser/backplate** combined fit | on the chosen rear stack | slicer + TP dry-fit | ±1 mm | Gate B closure (coupled to Gate A) | wing choice, DRS geometry | TP diag | P, F |
| **D-18** | **Gimbal hard-stop angles** per axis + usable travel | finished mount mechanical limits | protractor on built mount | ±2° | feeds firmware safety endpoints (blocker 1) | firmware gimbalConfig | no | (firmware) F |
| **D-19** | **Thermal run** temps: camera, ESC, WiFi module, motor bay, **both UBECs at load** (1.5) | on-bench powered, then in-body | IR thermometer / thermocouple | ±3 °C | decides ducting, ASA vs PETG, PLA-pod risk | duct load-bearing?, material | no | F |
| **D-20** | **RF separation / RSSI** ELRS 2.4 GHz vs WiFi 5.8 GHz vs metal | antennas at chosen placement | link stats / RSSI | qualitative | control + video reliability | antenna placement, KO-17 | no | F |
| **D-21** | **CG + L/R + F/R mass balance** | assembled rolling chassis | scale (per-corner if possible) | ±5 g | F1 handling; battery/electronics placement drives it | component placement | partial | F |
| **D-22** | **Mirrored front hub** bearing seat Ø12 (for 8×12×3.5) | Bambu-mirrored `Front_Right_Wheel_Hub` | slicer + calipers on print | ±0.1 mm | left hub only exists as a mirror | wheel print | no | P, F |
| **D-23** | Tyre-slot adapter **qty (1 vs 2/side)** + heat-soften watch | at rear-axle assembly + after first drives | trial + IR after run | — | qty + PETG→ASA fallback | wheel print qty, material | no | F |
| **D-24** | **Rail A + Rail B peak current** vs the 5 A UBEC ratings (LED full-white, servo stall transients, WiFi at max power) — *added 1.5* | bench: inline ammeter / shunt at each UBEC output | ±0.2 A | no rail budget exists; worst-case sums can approach/exceed 5 A (B.2 note, E-23) | UBEC sizing, firmware LED cap, harness wire gauge | no | W, F |
| **D-25** | **`FRONTNOSE2024` nose-cone interior** cross-sections (width/height at 3+ stations) — *added 1.5* | slicer Measure on the raw STL (view-only) | ±1 mm | the nose was never probed (authored on end; roof method inapplicable); "camera/WiFi in nose" is undecidable without it | camera placement, duct route, E-24 crash exposure | n/a | C |

## Start-now vs blocked

- **Do now (hardware on hand):** D-06 (calipers on the real camera; **D-06b only after
  the WiFi module is confirmed in hand** — 1.5), D-13 (read the 4 un-reviewed drawings),
  D-14/D-15/D-17 (slicer + diagnostic-TP wave), D-05/D-22 (slicer bore/seat checks),
  D-25 (slicer nose-cone sections), D-01/D-02/D-03/D-04/D-11 (slicer-assembly of
  floor + shells → then dummy-block dry-fit).
- **Blocked until parts arrive:** D-08, D-09, D-12, D-16, D-23 (measure on arrival);
  D-19, D-20, D-21, D-24 (need powered hardware); **D-18 is additionally gated behind
  the firmware A2 + Phase-B safety milestone** (`CAMERA_GIMBAL_PLACEMENT.md §4`).
- **Dummy strategy:** foam/printed blocks at the ESTIMATED envelopes (Report B) can
  unblock D-01/D-02/D-03/D-04/D-08/D-11 packaging studies *before* the real electronics
  arrive — this is the fastest way to de-risk the central packaging question.
