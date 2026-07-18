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
| **D-24** | **Rail A + Rail B peak current** vs the 5 A UBEC ratings — state matrix (S3): idle · normal running peak · cold-boot inrush · steering stall · LED full-white · WiFi max bitrate · audio peak · combined plausible peak · pathological all-load; **plus accessory-branch input current at PS-15** (the DN-01 fuse rates on the 7.4 V input side, ≈ ΣP_out/V_bat/η), Rail A hold-up through WiFi bursts (scope, L.5), Rail B voltage *at the servo connector* under stall, and one deliberate rail-output overload observation (does the UBEC current-limit or not — L.3.1). **Requires the real VID-WIFI (RST-06).** — *added 1.5, scope extended S3* | bench: CN-23 ammeter loops at each UBEC output + a PS-15 input-side loop; PSU/scope grounds tied to the PS-15 star only (test-equipment grounding) | inline DC ammeter + oscilloscope for <10 ms transients (S3 — the Tool cell was missing; row was column-shifted) | ±0.2 A; scope for transients | no rail budget exists; worst-case sums can approach/exceed 5 A (B.2 note, E-23); the fuse cannot be rated from output-side numbers alone | UBEC sizing, firmware LED cap (DN-04), fuse rating (DN-01), harness wire gauge | no | W, F |
| **D-25** | **`FRONTNOSE2024` nose-cone interior** cross-sections (width/height at 3+ stations) — *added 1.5* | slicer Measure on the raw STL (view-only) | ±1 mm | the nose was never probed (authored on end; roof method inapplicable); "camera/WiFi in nose" is undecidable without it | camera placement, duct route, E-24 crash exposure | n/a | C |
| **D-26** | **Steering push-rod line height above floor top at 3 stations + lock-to-lock sweep band** — *added S2* | servo horn (mid-chassis) ↔ `servosaverv7` atop the 71 mm tower; measure in the slicer assembly, re-verify at ASM-08 dry-fit | slicer + calipers/rule | ±2 mm | drawings imply a **rising diagonal (~35→~70 mm) over the central zone** (H §1.2, risk E-25) — deck inboard edge, battery overhead clearance, and both crossing stations X1/X2 depend on it | PS-01/PS-04/PS-06 geometry, N routing, KO-01 vertical extent | partial (rod mock) | C, W, F |
| **D-27** | **Floor M3 slot-map: which of the 12 slot-nut positions remain free** after the mechanical build, + their coordinates | drawing `[2]` slot pattern ↔ assembled floor | slicer + dry assembly | ±1 mm | every printed support (K) mounts only via existing slots — no new holes in donor parts | PS-01/02/03/05/06/07/08/15 mounting, T CAD tasks | yes | C, F |

## P0 digital-stage results (Session 4A, 2026-07-18 — tagged (P0); details + reproduction in `V_P0_geometry_measurement_results.md`, evidence in `evidence/p0/`)

| ID | Digital-stage result | Status | Physical residual |
|---|---|---|---|
| **D-01** | DAT-F = one flat plane (verified); P0 vehicle frame + all part transforms fixed; joint measured (x_ff = x_bf − 90.15 ± 0.2); full feature/thickness map; **battery bay length ≈ 78 mm > 75 — length fits**. **NEW: S0 (shell bottom edge above floor top) bounded 0…~11 — replaces the P1 assumption, which had the sign backwards (shell edge is AT or ABOVE the floor top, not below)** | DIGITALLY CONFIRMED (plane/frame/length) · S0 PARTIALLY RESOLVED | S0 pin at first body-on (P1) — **highest-value measurement on the car**; assembled flatness at ASM-05 |
| **D-02** | Full 13-station × 5-lateral profile at S0=0 (lower bound): P2c = 65–71 (Session-1 ~72 confirmed); **P2s = 26–41** (37–52 if S0≈11) — low half of the H.1.1 range | DIGITALLY CONFIRMED (S0=0 profile) · absolute PARTIALLY RESOLVED | S0; shell-seated gauge check at P3 (D-04 procedure) |
| **D-03** | Both sidepods: pocket band \|L\| 30…54, ceilings 22–30 (X +20…−40); Ø28–40×6–12 speaker fits either side; left-side install quantified for the I.4 balance path | DIGITALLY CONFIRMED (S0=0) | audibility/port at dry-fit; DN-07 owner call |
| **D-04** | Tall-channel (≥45) width stationed: 38→32→26→16→14 (X +30→−80); chimney continuous and viable; **ESP32 fallback F-2 fails its own ≥16 mm condition at the stack stations (module ≠ PCB)** | DIGITALLY CONFIRMED (S0=0) | P8 flow tell-tale + temps (unchanged) |
| **D-25** | Nose oriented + verified; 16 interior sections: enclosed cavity ONLY in the occupied rear installation ring (39–47 w × ~29–32 h × ~40 long); cowl-only forward, solid tip — **no protected camera volume** | DIGITALLY CONFIRMED (relative) · vertical map SLICER-ESTIMATED ±2 | nose dry-fit for the ±2; E-24/DN-05 unchanged |
| **D-26** | Slicer stage delivered: rod is a HIGH near-level line Z ≈ 42–58 (NOT 35→70); saver arm radius 18.0 measured; **KO-01 band = Z 35–62, \|L\| ≤ 18 rear → 12 fwd**; deck inboard edge \|L\| ≥ 26 (rear)…20 (fwd), i.e. L ≤ −26/−20 on the architecture-right belt side; X1 crossing must pass below Z 35 | GEOMETRICALLY DERIVED (relative) · SLICER-ESTIMATED (absolute) | ASM-08 physical stage (unchanged, two-stage) |
| **D-27** | Complete fastener map in vehicle coords (±0.2): **35 part-level M3 rows = 33 unique assembled coordinates** (two coaxial back-floor/rear-2 pairs); **the 12-slot free grid does not exist** — deck-side bay has ONE free M3 feature (−40.0, −32.9), PS-15 patch has none; supports need shared donor screws / free singles / plate-clamp feet (no new holes rule unchanged) | DIGITALLY CONFIRMED (positions) · occupancy PARTIALLY RESOLVED | P1 dry-fit occupancy pass (two-stage, unchanged) |

Side-naming note (P0): architecture-RIGHT = belt side = L<0 in the P0 frame (fully
determines all relative placements); the driver-left/right *name* is a one-glance
check at P1 (`V` §3).

## Start-now vs blocked

- **Do now (hardware on hand):** D-06 (calipers on the real camera; **D-06b only after
  the WiFi module is confirmed in hand** — 1.5), D-13 (read the 4 un-reviewed drawings),
  D-14/D-15/D-17 (slicer + diagnostic-TP wave), D-05/D-22 (slicer bore/seat checks),
  D-25 (slicer nose-cone sections), D-01/D-02/D-03/D-04/D-11 (slicer-assembly of
  floor + shells → then dummy-block dry-fit), **D-26/D-27 (S2: rod line + slot map —
  both start in the same slicer sitting; they gate the Gate-P1 dry-fit and the T CAD
  tasks)**.
- **Blocked until parts arrive:** D-08, D-09, D-12, D-16, D-23 (measure on arrival);
  D-19, D-20, D-21, D-24 (need powered hardware); **D-18 is additionally gated behind
  the firmware A2 + Phase-B safety milestone** (`CAMERA_GIMBAL_PLACEMENT.md §4`).
- **Dummy strategy:** foam/printed blocks at the ESTIMATED envelopes (Report B) can
  unblock D-01/D-02/D-03/D-04/D-08/D-11 packaging studies *before* the real electronics
  arrive — this is the fastest way to de-risk the central packaging question.
