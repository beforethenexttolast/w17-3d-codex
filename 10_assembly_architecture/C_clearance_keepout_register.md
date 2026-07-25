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
| **KO-01** | Steering push-rod sweep | floor **centreline**, mid→front | corrected provisional band **X−80…+100, Z22…38, |L|≤22**; horn/rod hardware absent from STLs | **moving** (steering) | anything between side-mounted servo horn and front saver, including battery/deck inboard edges | corrected D-26/report `Y`, DRW `[2]`/`[3]` | ASM-08: shaft/horn/spacers + three rod stations, full lock-to-lock and bump sweep |
| **KO-02** | Front tie-rods + turnbuckles + steering arms | front, both sides, outboard | wide arc at wheels | **moving** | front-corner electronics (none planned) | DRW `[3]`, photos | lock-to-lock sweep |
| **KO-03** | Front wheel/tyre envelope | front corners | tyre **Ø64 × 30 mm** (Tamiya 54198) + steer + bump | **moving** (steer + suspension) | body inner faces, nose sides | BOM, DRW | fit at full steer + full bump |
| **KO-04** | Front suspension travel | front, both sides | 52 mm **eye-to-eye** shocks (stroke ≪ 52, TBD — wording fixed 1.5); A-arm arc | **moving** | front shell underside | BOM, photos | compress/rebound, check bind |
| **KO-05** | Front block `Suspension Block_10` | front centre | raw bbox ~37×37×70.79; assembled vertical range **Z−14…+23**, with the 70.79 axis longitudinal | **static** occupancy | Z2 volume | corrected D-26 four-hole registration, report `Y` | floor/block registration derived; physical assembly check |
| **KO-06** | **Central rear shock (68 mm) path** | rear **centreline** | shock body + spring + **stroke**; lies along spine | **moving** (suspension) | **Z3/Z5 electronics spine** — direct conflict | photos `…54 (5)/(6)`, Gate A | **Gate A**: seat *and articulate* through travel next to placed electronics |
| **KO-07** | Rear rocker / spring-mount articulation | rear tower | `Spring mount 2 REV1` 24.7 × 22.5 × 34.8 + arc | **moving** | rear-stack parts, wing mount | Gate A, CSV | Gate A dry-fit / slicer |
| **KO-08** | Rear axle + spur + belt + pinion | rear, transverse | axle span + Ø spur; rotating | **rotating** | rear floor tail, wiring | DRW `[2]/[7]`, photos | spin free, mesh backlash |
| **KO-09** | Motor body + heat | rear, transverse | ~Ø36 × 53 mm + **hot** | **static + thermal** | rear-spine electronics | BOM, photos | thermal after run (E-05) |
| **KO-10** | Rear wheel/tyre envelope | rear corners | tyre **Ø64 × 35 mm** (Tamiya 51400) + bump | **moving** | body inner, diffuser | BOM | full bump |
| **KO-11** | Steering servo horn sweep | **mid-chassis, rear floor** (`Servoholder`, drawing `[2]`) | side-mounted DS3235SG has horizontal/lateral shaft; normal 25T horn stands in a vertical longitudinal plane and its tip drives the rod fore/aft | **moving** | adjacent electronics | DRW `[2]`/`[3]`, report `Y` | no-force servo fit + horn/rod clearance (D-09/D-26) |
| **KO-12** | DRS servo + arm + rod | rear wing | MG90S + `DRS Arm 2021` 58 mm + rod | **moving** | rear-wing/diffuser volume | DRW `[2]`, Gate B | DRS actuation dry-fit |
| **KO-13** | **Gimbal pan/tilt sweep** | camera location | 2× MG90S full throw; **hard-stops feed firmware** | **moving** | body/halo intrusion into FOV | CAMERA_GIMBAL_PLACEMENT §4 | measure hard-stop angles (post A2/Phase-B gate) |
| **KO-14** | **Body clamshell insertion/removal path** | whole car | shell drops vertically over everything | **assembly access** | tallest electronics, antennas, wing | photo `…56`, README `[1]` | lower body, check nothing fouls/roof clearance |
| **KO-15** | Screw/tool access | 12× floor M3, 3× body M3, drivetrain M3 | driver reach to each boss | **service access** | buried bosses | DRW `[2]`, ASSEMBLY_NOTES | reach-test each fastener with body-on/off |
| **KO-16** | Cooling airflow path | nose→camera→rear | vents "front-in / rear-out" (v2) | **thermal/airflow** | camera, ESC, WiFi, motor | v2 packing, MATRIX heat map | verify inlet/outlet not blocked by wiring |
| **KO-17** | Antenna clearance | ELRS 2.4 GHz + 2× 5.8 GHz + WiFi | keep from metal (motor, sleeves, shock, axle) | **RF** | RX + video links | BOM, E-06 | range/RSSI check at chosen placement |
| **KO-18** | Guide-rod / king-pin press-fits | front uprights | tap-in pins | **assembly order** (not serviceable late) | front-end teardown | DRW `[3]` | confirm ~3 mm bore (D-05) |
| **KO-19** | **Steering-servo body + `Servoholder`** | **mid-chassis centreline, rear floor** (drawing `[2]`) | holder 58 longitudinal ×22.89 high ×10 thick; side-mounted DS case approximately 40 longitudinal ×40.4 lateral ×20 high, plus lead/ears; holder clear arch 42×18.5 | **static** occupancy (horn sweep = KO-11) | **Z3/Z5 electronics + battery placement** — an occupant the Rev-1.1 photos do not show | corrected mesh/drawing study `Y`, Gate D | real DS case fit (D-09), exact holder seat, shell shoulder + D-02 dry-fit |

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

## C.4 Remaining-component keep-outs (2026-07-23)

Coordinates use DAT-F and S0=0 lower-bound shell evidence. These rows extend,
not relax, KO-01…KO-19.

| ID | Keep-out | Datum/envelope | Confidence | Minimum / closure |
|---|---|---|---|---|
| **KO-20** | documented ESC body/fan/lead volume | candidate X−60, L−25, base Z3; body Z3…35.3, fan-air plane Z45.3 | body DOCUMENTED; placement ASSUMPTION | ≥10 mm above fan; current side placement fails S0=0; D-28 |
| **KO-21** | belt, spur, pinion and shaft rotation | rear axle X−90.9; Ø40.75 theoretical spur OD; belt tangent runs TBD | gear DERIVED; belt placement ASSUMPTION | ≥2 mm guard to rotation and ≥8 mm to static loom; D-16 |
| **KO-22** | front/rear tyre motion | axes X+146.1/−90.9; Ø64; front ±25° planning envelope X±35.3/L±27.1 | X/tyre DOCUMENTED/DERIVED; steer/travel ASSUMPTION | body-on full steer+bump; arch context only 3.5/4 mm |
| **KO-23** | battery body/strap/removal | pack candidate X−81.5…−6.5, L+2.5…+47.5, Z3…31 | limit DOCUMENTED; placement ASSUMPTION | ≥5 shell, ≥8 steering; fails S0=0 shoulder model; D-31 |
| **KO-24** | gimbal/camera/FOV/duct sweep | Option A X+60 or B X−53; 55×45×60 reserve | ASSUMPTION | ≥8 to fixed structure; lens/FOV clear; D-34/35 |
| **KO-25** | DRS servo/58 mm arm/flap/rod | rear wing around X−125 | arm bbox VERIFIED; transform ASSUMPTION | ≥8 to shock, LED loom and body; Gate A/B |
| **KO-26** | RF antenna/coax routes | RP1 65 mm forward; video 2×70 mm near airbox | lengths DOCUMENTED; routes ASSUMPTION | ≥10 mm coax bend, target ≥150 mm inter-system; D-20/D-33 |
| **KO-27** | Hall magnet/collar rotation | rear axle X−90.9; target face gap 1.5, validate 1–3 mm | X DERIVED; gap ASSUMPTION | controlled gap only; ≥8 to other rotating/moving parts; D-38 |
| **KO-28** | speaker cone/port | X−30, L+43, Z3…15 candidate | ASSUMPTION | ≥3 mm cone/vent, ≥5 shell; D-36 |
| **KO-29** | LED optical/harness paths | tail diffuser, wing ends, halo | printed bboxes VERIFIED; routes ASSUMPTION | ≥8 to DRS/shock/belt; body disconnect snag test |

**Immediate conflict delta:** KO-20 and KO-23 are now top-tier packaging
blockers. The official ESC envelope invalidates the old Z5R planning block, and
the single active battery still fails the lower-bound shoulder/steering model.

## C.5 Cassette keep-out extension (2026-07-24)

These rows add the physical consequences of the proposed lift-out architecture.
They neither resolve S0 nor relax the 5 mm static / 8 mm moving policies.

| ID | Keep-out | Datum/envelope | Confidence | Closure |
|---|---|---|---|---|
| **KO-30** | two mini-board wall seats versus steering and shell shoulder | each X+3…+42, L±30…43, Z1…32 against KO-01 \|L\|≤22/Z22…38; registered worst shoulder 27.18 mm at S0=0 | DERIVED from ASSUMPTION installed cells | 8 mm lateral separation is nominal; D-04 must prove S0≥9.82 and ASM-08 must prove the real moving gap |
| **KO-31** | decoupled pedestal/gimbal versus opening, halo and front structure | trial outer core X+51…+65/L±11; 10×18 clear conduit / 14×22 outer; gimbal datum/sweep TBD | architecture change VERIFIED; geometry/sweep ASSUMPTION, MG90S DEFER | terminated-plug conduit coupon + D-04/ASM-53 body/halo-on FOV and no-power sweep dummy |
| **KO-32** | four-point saddle versus target cells and donor floor | former centres (−15,±12)/(+35,±12) now lie inside charge/PDB targets | DERIVED from TARGET placements | former pattern REJECTED; transparent full-stack dummy must prove external four-point saddle/clamp; no hidden screws/drilling |
| **KO-33** | ganged dock mating and bend volume | map minimum firm; straight body projection X+42…+58/L±32 overlaps pedestal X+51…+65/L±11 | map FIRM; bodies/topology ASSUMPTION | caliper XT60/XT30/3-pin/XH3/4/5/USB/U.FL; stepped/wrapped dock dummy and body-off unplug |
| **KO-34** | cassette vertical lift/tool/USB envelope | stepped-T gauge plus two forward-facing micro-USB plugs and the still-unresolved external saddle/clamp release axes; pedestal stays fixed | ASSUMPTION | timed lift around the fixed pedestal with body, dock and USB plugs present |
| **KO-35** | pedestal hollow conduit versus steering and cassette removal | shielded USB4 + 2×3-pin leads through 10×18 clear target; ≥25 mm lower slack; turn into R1/R2 below Z22 | bundle FIRM; section/bodies/bends ASSUMPTION; MG90S leads DEFER | 2 mm-wall coupon, sequential terminated-plug pull-through, powered sweep and cassette lift |
| **KO-36** | target PDB/amp deck versus provisional steering | PDB X+1…+46/L±27.5/Z1…19; amp/RP1 deck ends Z16; KO-01 starts Z22 | TARGET/ASSUMPTION placement | PDB gap 3 mm (5 mm short of 8); amp/RP1 gap 6 mm (2 short); ASM-08 must replace KO-01 |

The old KO-30 110 mm board-row failure and old KO-31 Z98 additive roof failure
are removed. KO-30 shoulder/S0, KO-31 actual pedestal sweep, KO-32 mounting,
KO-33/34 service, KO-35 conduit and KO-36 target-stack steering remain
production stops.
