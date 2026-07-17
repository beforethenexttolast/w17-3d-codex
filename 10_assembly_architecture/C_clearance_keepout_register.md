# C · Chassis Clearance & Keep-out Register

Session 1 · 2026-07-17 · corrected in Session 1.5 (same day). Confidence tags per
[`README.md`](README.md). Dimensions are DERIVED bboxes (authored frame) unless noted;
**"usable" is always net of the keep-outs below.** ⚠ All shell "ceiling" figures are
measured above the **shell's own bottom edge**, not the chassis floor top — usable
height above the floor top is smaller by the (unmeasured) body↔floor overlap (D-01).

---

## C.1 Zone map (candidate installation zones)

| Zone | Location | Nominal envelope | Evidence | Verdict (Session 1) |
|---|---|---|---|---|
| **Z1 Nose** | forward of front axle, under nose shell | probe numbers cover the **front-shell taper only** (~18–35 mm); the actual nose cone `FRONTNOSE2024` is slender (outer ≤ ~42 mm) and **unprobed** (1.5) | PROBE (front shell), DRW `[1]` | provisional — camera/WiFi "in nose" needs nose interior (D-25) + real-camera check (D-06); **primary crash zone** (E-24) |
| **Z2 Front bay** | over front floor, behind nose, under front shell | up to ~42–53 mm ceiling; ≥45 mm pocket at cockpit hump is small (~34 long, 18–39 wide across the two probes) | PROBE | **contested** — steering push-rod (KO-01) + tower (KO-05); the big servo is **NOT here** in our config (1.5 — it sits mid-chassis, KO-19) |
| **Z3 Central tub / junction** | at the FRONT/REAR shell junction, over the floor | **tallest** usable: ceiling to ~72 mm, width to ~120 mm, but ≥45 mm-tall only ~14–40 mm wide | PROBE, v2 packing | **primary battery + airbox-spine zone** (best volume) — net of KO-06 shock, **KO-19 steering servo (1.5)** and loom |
| **Z4 Sidepods L/R** | lateral bulges either side of Z3 | **unmeasured** narrow pockets | DRW `[1]`, v2 packing | **TO MEASURE (D-03)** — planned for UBEC/amp/RX/speaker |
| **Z5 Rear spine** | centreline from junction to motor | occupied | photos `…54 (5)/(6)` | **mostly blocked** by central shock + wiring |
| **Z6 Rear drivetrain** | rear of floor | occupied by axle/spur/belt/motor | DRW `[2]/[7]`, photos | **prohibited** (mechanical + hot) |
| **Z7 Rear wing/DRS** | on the rear spring-mount tower | wing box + DRS pocket | DRW `[2]`, Gate A/B | gated (Gate A+B) |
| **Z8 Gimbal/camera** | cockpit (Option A) or halo-height pod (Option B) | halo bbox 75 × 39 × 25; pod `camera top 1.1` 16.7 × 17.7 × 6.9 | CAMERA_GIMBAL_PLACEMENT | **open decision** (not this session). Note (1.5): the optional **driver figure and Option A are mutually exclusive** cockpit occupants — decide together |

---

## C.2 Movement & access keep-out register

| Zone ID | Keep-out | Location | Usable/keep-out dims | Restriction type | Affected components | Evidence | Required physical test |
|---|---|---|---|---|---|---|---|
| **KO-01** | Steering push-rod sweep | floor **centreline**, mid→front | rod spans the rear-floor `Servoholder` → front servo-saver (corrected 1.5); translates/rotates | **moving** (steering) | anything on the centreline between servo and saver — incl. the Z3 battery zone edge | DRW `[2]`/`[3]` | dry-fit: full lock-to-lock, mark swept band |
| **KO-02** | Front tie-rods + turnbuckles + steering arms | front, both sides, outboard | wide arc at wheels | **moving** | front-corner electronics (none planned) | DRW `[3]`, photos | lock-to-lock sweep |
| **KO-03** | Front wheel/tyre envelope | front corners | tyre **Ø64 × 30 mm** (Tamiya 54198) + steer + bump | **moving** (steer + suspension) | body inner faces, nose sides | BOM, DRW | fit at full steer + full bump |
| **KO-04** | Front suspension travel | front, both sides | 52 mm **eye-to-eye** shocks (stroke ≪ 52, TBD — wording fixed 1.5); A-arm arc | **moving** | front shell underside | BOM, photos | compress/rebound, check bind |
| **KO-05** | Front tower `Suspension Block_10` | front centre | **37 × 37 × 71 mm** solid | **static** occupancy | Z2 volume | CSV, DRW `[3]` | — (bbox CONFIRMED) |
| **KO-06** | **Central rear shock (68 mm) path** | rear **centreline** | shock body + spring + **stroke**; lies along spine | **moving** (suspension) | **Z3/Z5 electronics spine** — direct conflict | photos `…54 (5)/(6)`, Gate A | **Gate A**: seat *and articulate* through travel next to placed electronics |
| **KO-07** | Rear rocker / spring-mount articulation | rear tower | `Spring mount 2 REV1` 24.7 × 22.5 × 34.8 + arc | **moving** | rear-stack parts, wing mount | Gate A, CSV | Gate A dry-fit / slicer |
| **KO-08** | Rear axle + spur + belt + pinion | rear, transverse | axle span + Ø spur; rotating | **rotating** | rear floor tail, wiring | DRW `[2]/[7]`, photos | spin free, mesh backlash |
| **KO-09** | Motor body + heat | rear, transverse | ~Ø36 × 53 mm + **hot** | **static + thermal** | rear-spine electronics | BOM, photos | thermal after run (E-05) |
| **KO-10** | Rear wheel/tyre envelope | rear corners | tyre **Ø64 × 35 mm** (Tamiya 51400) + bump | **moving** | body inner, diffuser | BOM | full bump |
| **KO-11** | Steering servo horn sweep | **mid-chassis, rear floor** (`Servoholder`, drawing `[2]` — location corrected 1.5) | DS3235SG horn arc | **moving** | adjacent electronics | DRW `[2]`/`[3]`, BOM | servo fit + horn clearance (D-09) |
| **KO-12** | DRS servo + arm + rod | rear wing | MG90S + `DRS Arm 2021` 58 mm + rod | **moving** | rear-wing/diffuser volume | DRW `[2]`, Gate B | DRS actuation dry-fit |
| **KO-13** | **Gimbal pan/tilt sweep** | camera location | 2× MG90S full throw; **hard-stops feed firmware** | **moving** | body/halo intrusion into FOV | CAMERA_GIMBAL_PLACEMENT §4 | measure hard-stop angles (post A2/Phase-B gate) |
| **KO-14** | **Body clamshell insertion/removal path** | whole car | shell drops vertically over everything | **assembly access** | tallest electronics, antennas, wing | photo `…56`, README `[1]` | lower body, check nothing fouls/roof clearance |
| **KO-15** | Screw/tool access | 12× floor M3, 3× body M3, drivetrain M3 | driver reach to each boss | **service access** | buried bosses | DRW `[2]`, ASSEMBLY_NOTES | reach-test each fastener with body-on/off |
| **KO-16** | Cooling airflow path | nose→camera→rear | vents "front-in / rear-out" (v2) | **thermal/airflow** | camera, ESC, WiFi, motor | v2 packing, MATRIX heat map | verify inlet/outlet not blocked by wiring |
| **KO-17** | Antenna clearance | ELRS 2.4 GHz + 2× 5.8 GHz + WiFi | keep from metal (motor, sleeves, shock, axle) | **RF** | RX + video links | BOM, E-06 | range/RSSI check at chosen placement |
| **KO-18** | Guide-rod / king-pin press-fits | front uprights | tap-in pins | **assembly order** (not serviceable late) | front-end teardown | DRW `[3]` | confirm ~3 mm bore (D-05) |
| **KO-19** | **Steering-servo body + `Servoholder`** (added 1.5) | **mid-chassis centreline, rear floor** (drawing `[2]`) | DS3235SG ~40 × 20 × 40.5 **EST** + holder 22.9 × 10 × 58 + 3-wire lead | **static** occupancy (horn sweep = KO-11) | **Z3/Z5 electronics + battery placement** — an occupant the reference photos do NOT show (they use the Rev-1.1 front servo) | DRW `[2]`, Gate D | DS3235SG fit (D-09) + placement in the D-02 dry-fit |

---

## C.3 Keep-out confidence

| Keep-out | Confirmed / Estimated / Needs validation |
|---|---|
| KO-05 (front tower bbox), KO-03/KO-10 (tyre OD from BOM) | **CONFIRMED** |
| KO-08 (drivetrain rotation), KO-01 (steering rod on centreline), KO-14 (clamshell lift-off) | **CONFIRMED** from drawings + photos |
| KO-06 (central shock in electronics spine) | **CONFIRMED conflict**, magnitude **needs Gate-A dry-fit** |
| KO-04 (front travel), KO-11 (servo horn), KO-12 (DRS) | **ESTIMATED** — need real shock/servo dry-fit |
| KO-13 (gimbal sweep / hard-stops) | **needs physical validation** (gated behind firmware A2 + Phase-B, per CAMERA_GIMBAL_PLACEMENT) |
| KO-19 (steering-servo body, mid-chassis) | location **CONFIRMED** (drawing `[2]`); size **ESTIMATED** until D-09 |
| KO-16 (airflow), KO-17 (antenna RF) | **needs physical validation** (thermal run + RSSI) |

**Cross-cutting conclusion:** the three keep-outs that most threaten the build are
**KO-06 (central rear shock in the electronics spine)**, **KO-14 (clamshell clearance
over a taller-than-original electronics stack)**, and **KO-01 (steering rod owning the
front centreline)** — joined in Session 1.5 by **KO-19 (the DS3235SG body sitting
mid-chassis in the same central zone the battery and loom want)**. All are validated
only by a *physical or slicer dry-fit with the mechanicals placed* — none can be closed
from geometry alone.
