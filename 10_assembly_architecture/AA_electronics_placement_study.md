# AA · Electronics placement study — "what goes where", and the second-floor cage

**Date:** 2026-09-03 · **Session:** mechanical takeover (owner decision A3, 2026-09-02) ·
**Author:** Claude Code, `design/placement-and-cage`

> **Why the letter `AA` and not `X`.** The top-level series runs A–W, Y, Z; `X` was
> already spent on [`cad/reports/X_diagnostic_cad_review.md`](cad/reports/X_diagnostic_cad_review.md),
> which this package's [`README.md`](README.md) lists in the same table. Re-using `X`
> at top level would create two "report X"s. The series therefore continues at `AA`.

---

## 0. What this document is, and what it is not

**Is:** the single "what goes where" answer for every onboard module, the engineering
concept for the **second-floor board cage** the owner asked for, a linkage check for
**DRS**, placement candidates for the **USB-C charge flap**, a concept for the **GCS
box**, and the ordered **measurement list** that turns all of it from a plan into
numbers.

**Is not:** a proof that anything fits. Nothing in this study has been dry-fitted,
printed, or powered. Every fit statement is a *gauge* — arithmetic on registered
geometry with the shell registered at its lower bound (S0 = 0). **A2 remains
NOT-EXECUTED and Phase B remains BLOCKED**; no dimension here authorizes a production
print, a shell cut, a hole in a donor part, or any powered work.

**Supersedes nothing.** It *consumes* the Session-1/2/3/4A registers (A–W), the
2026-07-23 fit studies, the 2026-07-24 cassette audit
([`fit_studies/ZK_electronics_cassette_fit_study.md`](fit_studies/ZK_electronics_cassette_fit_study.md)),
and the owner's batch-1 calipers, and adds the layer none of them carried: a single
ordered placement answer plus the printable structure that realises it. Where it
disagrees with an earlier row it says so explicitly and names the evidence.

### Provenance tags (used on every number in this document)

| Tag | Meaning |
|---|---|
| **MEASURED**(`file:line`) | a real instrument touched a real part; the citation is the record |
| **DERIVED**(source) | computed from registered mesh geometry or arithmetic on MEASURED values |
| **DOCUMENTED**(part) | vendor drawing / datasheet for the *part family* — hedged: our unit is unverified |
| **ESTIMATED**(reason) | plausible planning value with the reasoning stated; not a measurement |
| **ASSUMED** | a value that **must be measured before it is printed to**; every one is listed in §12 and is a named parameter in [`../11_cad/w17_params.scad`](../11_cad/w17_params.scad) |

This maps 1:1 onto the package's existing VERIFIED / DERIVED / DOCUMENTED / ASSUMPTION
vocabulary ([`fit_studies/README.md:19-20`](fit_studies/README.md)); MEASURED is used
where a *dated owner caliper record* exists, which the older vocabulary folded into
VERIFIED.

---

## 1. Inputs

Every row was read at HEAD of this repo (`0386b2f`) or at the cited workspace path.

| # | Input | What it supplies | Provenance |
|---|---|---|---|
| I-01 | [`evidence/p0/tables/p0_d01_floor_datum.md:20`](evidence/p0/tables/p0_d01_floor_datum.md) | DAT-F is one continuous flat plane, Z = 0, over both floor plates | DERIVED (4 mm-grid ray survey, 2516 samples) |
| I-02 | [`evidence/p0/tables/p0_d01_floor_datum.md:45-88`](evidence/p0/tables/p0_d01_floor_datum.md) | complete M3 feature map: 35 part rows / 33 unique assembled coordinates ±0.2 | DERIVED (mesh) |
| I-03 | [`evidence/p0/tables/p0_d01_floor_datum.md:100-126`](evidence/p0/tables/p0_d01_floor_datum.md) | centre-band solid/open map: SOLID X−84…−16, OPEN X−14…−4 and X ≤ −94, opening at X+78 | DERIVED |
| I-04 | [`evidence/p0/tables/p0_d02_d03_d04_clearance.md:12-24`](evidence/p0/tables/p0_d02_d03_d04_clearance.md) | 13-station shell ceiling profile at S0 = 0 (lower bound) | DERIVED |
| I-05 | [`evidence/p0/tables/p0_d02_d03_d04_clearance.md:33-46`](evidence/p0/tables/p0_d02_d03_d04_clearance.md) | tall-channel (airbox) widths by station | DERIVED |
| I-06 | [`evidence/p0/tables/p0_d02_d03_d04_clearance.md:50-63`](evidence/p0/tables/p0_d02_d03_d04_clearance.md) | sidepod pocket survey, both sides | DERIVED |
| I-07 | [`evidence/p0/tables/p0_d27_deckside_map.md:35-51`](evidence/p0/tables/p0_d27_deckside_map.md) | the 12-slot free grid **does not exist** — one free M3 feature per side bay | DERIVED + occupancy PARTIALLY RESOLVED |
| I-08 | [`C_clearance_keepout_register.md:30-48`](C_clearance_keepout_register.md) | KO-01…KO-19 | mixed; each row carries its own tag |
| I-09 | [`C_clearance_keepout_register.md:78-107`](C_clearance_keepout_register.md) | KO-20…KO-36 (remaining-component + cassette extensions) | mixed |
| I-10 | [`D_measurement_plan.md:43-49`](D_measurement_plan.md) | S0 ∈ 0…~11, physically unpinned; battery bay length ≈ 78 mm | DERIVED / S0 PARTIALLY RESOLVED |
| I-11 | [`E_constraint_risk_register.md:9-34`](E_constraint_risk_register.md), [`:50-58`](E_constraint_risk_register.md), [`:68-75`](E_constraint_risk_register.md) | E-01…E-41 risk register | — |
| I-12 | [`I_zone_layer_plan.md:45-48`](I_zone_layer_plan.md) | clearance policy: ≥5 mm static, ≥8 mm static-to-moving, ≥10 mm above the ESC fan | policy |
| I-13 | [`fit_studies/ZK_electronics_cassette_fit_study.md:93-109`](fit_studies/ZK_electronics_cassette_fit_study.md) | the stepped-T cassette reference gauge and every cell coordinate | ASSUMED gauges over MEASURED bodies |
| I-14 | [`fit_studies/ZK_electronics_cassette_fit_study.md:125`](fit_studies/ZK_electronics_cassette_fit_study.md) | **required S0 ≥ 9.82 mm** for the two on-edge board seats | DERIVED |
| I-15 | [`fit_studies/ZK_electronics_cassette_fit_study.md:173-188`](fit_studies/ZK_electronics_cassette_fit_study.md) | ESC station **FAIL-STATION / RELOCATE** | DERIVED from MEASURED body |
| I-16 | [`fit_studies/ZA_accessory_servo_fit_study.md:26-27`](fit_studies/ZA_accessory_servo_fit_study.md) | 2021 wing raw bbox 105.1×82×60; `DRS Arm for 2021 Rear Wing` raw bbox 58×5×10 | VERIFIED raw STL / transforms ASSUMED |
| I-17 | [`w17-batch1-measurements-for-codex.md:38-51`](../../w17-batch1-measurements-for-codex.md) | owner's dated no-power caliper + scale session, 2026-07-24 | MEASURED |
| I-18 | [`w17-electrical-inputs-for-codex.md:7-70`](../../w17-electrical-inputs-for-codex.md) | board SKU, PDB contents, charge module, full connector map | FIRM identity / TARGET envelopes |
| I-19 | [`w17-pdb-build-and-connector-guide.md:36-57`](../../w17-pdb-build-and-connector-guide.md) | XT90-S master is **body-accessible** and the charger taps the **pack side** of it | owner decisions F9a/F9b |
| I-20 | [`w17-gcs-box-guide.md:86-108`](../../w17-gcs-box-guide.md) | GCS box contents, envelope inputs, non-dimensional requirements | vendor / `[TBD-caliper]` |
| I-21 | [`w17-control-fw/lib/config/include/config/PinMap.hpp:16-61`](../../w17-control-fw/lib/config/include/config/PinMap.hpp) | control pin map incl. SP3T strap pins GPIO27 / GPIO32 | code at HEAD |
| I-22 | [`w17-control-fw/docs/bt_showoff_design.md:103`](../../w17-control-fw/docs/bt_showoff_design.md) | the selector is *"reachable under the engine cover — the shell itself stays unmodified (owner constraint)"* | owner constraint |
| I-23 | [`learning-manual/14_glovebox_owners_booklet.md:79-85`](../../learning-manual/14_glovebox_owners_booklet.md), [`:177`](../../learning-manual/14_glovebox_owners_booklet.md), [`:230`](../../learning-manual/14_glovebox_owners_booklet.md) | giftee-facing promises: hidden USB-C flap, charge-state light at the flap, key outside, selector under the engine cover, *don't open her up* | product requirement |
| I-24 | `review-seeds/w17-control-fw.v2report.json` → `timing-1` (high, PLAUSIBLE) | Hall GPIO35 edge storm can starve the 50 Hz control tick; **GPIO34–39 have no internal pull-ups** | code review, 2026-09-03 |
| I-25 | `review-seeds/w17-soundlight-fw.v2report.json` → `refutedTitles[0]` | the WS2812 Schottky data-line-margin finding (`safety-3`) was **REFUTED** and must not be reopened | code review, 2026-09-03 |
| I-26 | [`MODEL_INVENTORY.md:92-107`](../MODEL_INVENTORY.md), [`:109-122`](../MODEL_INVENTORY.md), [`:186-194`](../MODEL_INVENTORY.md) | donor part identities and bboxes for floor, body, wing/DRS groups | filename/bbox classification, not visually inspected |
| I-27 | [`HARDWARE_INVENTORY.md`](../../HARDWARE_INVENTORY.md) | authoritative arrival ledger (this repo never re-asserts arrivals) | owner log |

**Two inputs conflict and the owner must adjudicate** (also §12, OQ-1): the charge module
is `~29 × 26 × ~6 mm` in [`w17-electrical-inputs-for-codex.md:38`](../../w17-electrical-inputs-for-codex.md)
and `18.3 × 31 mm` footprint in a `≤10 mm` cell in
[`fit_studies/ZK_electronics_cassette_fit_study.md:73`](fit_studies/ZK_electronics_cassette_fit_study.md).
Neither is a caliper record. No pocket may be cut to either until ASM-59 measures the
purchased SKU.

---

## 2. Frame, datums and the two numbers everything hangs on

Coordinates are the P0 vehicle frame throughout: **X+ forward** (X = 0 at the
front/rear floor joint), **L** lateral from the centreline with the belt /
architecture-right side at **L < 0**, **Z up from DAT-F = floor top = 0**
(I-01, [`fit_studies/README.md:12-16`](fit_studies/README.md)).

Two unmeasured numbers gate almost every row below:

- **S0** — the height of the shell's bottom edge above DAT-F, bounded **0 … ~11 mm**
  and never physically pinned (I-10). Every ceiling in this study is quoted at
  **S0 = 0**, i.e. the pessimistic bound. ⚠ *Naming collision:* the A2 gate once called
  `S0` was renamed **SF** on 2026-08-04 ([`w17-socket-stack-caliper-prompt.md:19-21`](../../w17-socket-stack-caliper-prompt.md));
  a bare `S0` anywhere in the mechanical package is this clearance.
- **The real steering sweep** — KO-01 is still the *provisional* band
  X −80…+100, |L| ≤ 22, Z 22…38, pending the ASM-08 physical lock-to-lock sweep
  (I-08). It is the single most restrictive keep-out in the car, and it sits exactly
  where the electronics want to be.

Clearance policy, unchanged (I-12): **≥5 mm** static-to-static (this is also the
print-tolerance and shell-flex budget), **≥8 mm** static-to-moving, **≥10 mm** of open
air above the ESC fan intake.

---

## 3. What goes where — the master placement table

One row per module. **Deck** is the vertical level: `FLOOR` = bolted/strapped to the
donor floor and stays when the cassette lifts; `CAS-L0` = cassette lower bay;
`CAS-L1` = cassette rear service deck; `CAS-W` = cassette wall seat (the "second
floor", §5); `PED` = the fixed floor-referenced cockpit pedestal; `SHELL` = travels
with the body; `WING` = on the rear wing assembly; `REAR` = rear drivetrain zone.

| # | Module | Body (provenance) | Zone / deck | Station (S0=0 gauge) | Why there |
|---|---|---|---|---|---|
| 1 | **ESP32 #1 (control)**, MH-ET D1-Mini | 39 × 31 × ~13 with headers — DOCUMENTED(SKU class, [`w17-electrical-inputs-for-codex.md:9`](../../w17-electrical-inputs-for-codex.md)); ASSUMED installed height | **CAS-W**, belt side | X +3…+42, L −43…−30, Z 1…32 | on edge is the only orientation that fits: it needs 13 mm of lateral band, and the only band outside KO-01 (\|L\|≥30) and inside the shell shoulder (≲43) is 13 mm wide (§5.2). USB-C faces the X+42 service edge. All 11 control signals fan out forward/inboard to the dock |
| 2 | **ESP32 #2 (sound + light)** | same | **CAS-W**, mirror side | X +3…+42, L +30…+43, Z 1…32 | mirrored, same access edge; puts the **WS2812 data pin (GPIO4)** and the **I2S trio (26/25/22)** on the side the LED loom and the speaker already live on, so the two most timing-sensitive single-ended runs stay short (§4.2) |
| 3 | **RP1 ELRS RX + T-antenna** | 13.4 × 11.4 × 4.05, 1.6 g — MEASURED([`w17-batch1-measurements-for-codex.md:48`](../../w17-batch1-measurements-for-codex.md)); 65 mm antenna DOCUMENTED | **CAS-L1** body; antenna to **SHELL-line forward guide** | body X −12.2…+0.8, L −6…+5, Z 13…16.05; antenna dressed forward along the inner shell line | tiny and light, so it costs nothing to put it on the insulated rear service deck next to the dock; the antenna is the part that needs placement, not the board — it goes forward, away from the 5.8 GHz roots and away from the ESC/motor metal (KO-17, KO-26) |
| 4 | **BL-M8812EU2 Wi-Fi + 28×28×3 heatsink** | 32.4 × 32.0 × 7.0 incl. heatsink, 11.2 g with antennas — MEASURED([`w17-batch1-measurements-for-codex.md:40`](../../w17-batch1-measurements-for-codex.md)) | **CAS-L1**, rear stem, heatsink **up** | X −31…+1, L −16.2…+16.2, Z 12…19; clear-air reserve Z 19…29 | it is the hottest thing on the cassette and it must sit under the airbox draft, which is the rear stem; heatsink up into moving air, U.FL roots at its X+1 edge turning outward (I-13) |
| 5 | **2× 5.8 GHz U.FL whip antennas** (70 mm) | 70 mm whip — DOCUMENTED | chassis-mounted posts at the cassette rear; **never shell-mounted** | roots reserved 12 × 12 × 6 at L −8 / +8, tips in a shallow V | shell-mounted whips would tether the body through ~30-mate-rated U.FL pigtails at every body-off, breaking the one-disconnect rule ([`I_zone_layer_plan.md:179-186`](I_zone_layer_plan.md)); target ≥150 mm from the ELRS tip |
| 6 | **Camera (SSC338Q + IMX335)** on the pan/tilt gimbal | base 19.2 × 19.2 × 30.7 — DOCUMENTED(MC800S-V3, [`B_component_envelope_register.md:177`](B_component_envelope_register.md)); complete installed envelope **ASSUMED** | **PED** — fixed hollow cockpit pedestal, floor-referenced | outer core X +51…+65, L ±11 | Option A (cockpit) is preferred for CG and driver POV; decoupling it from the cassette is what retired the old additive Z98 stack failure (I-13). It stays put when the cassette lifts, so the camera's boresight/roll trim is not re-made at every service |
| 7 | **Pedestal ↔ floor joint** | — | **FLOOR** | uses existing centreline M3 through-holes at **X +57.50** and **X +64.24**, L = 0 (I-02) | **New finding.** Those two registered M3 features fall inside the pedestal footprint. Two collinear screws cannot resist rotation on their own; add a third non-threaded locating spigot into the 12.1 × 12.1 opening at X +78.11 (I-02). ⚠ Occupancy unverified — both may already carry the nose/front-wing mount; the P1 two-stage occupancy pass owns this (I-07) |
| 8 | **ESC QuicRun 10BL120 G2** | 44.2 × 33.7 × **34.0**, 100 g — MEASURED([`w17-batch1-measurements-for-codex.md:41`](../../w17-batch1-measurements-for-codex.md)) | **FLOOR**, rear-right — **station is FAILED, relocation open** | old station X −49.2…−5, L −60.5…−26.8 fails by 3.2 mm laterally and 7.0…13.1 mm vertically (I-15) | heavy, hot, and the noisiest thing on the car — it must stay on the floor, off the cassette, close to the motor to keep the three phase wires short. **Its replacement station is an open problem (§10, OP-A)**; the body is 34 mm tall and needs a Z45.5 intake-air plane that no registered shell station supplies at S0 = 0 |
| 9 | **Motor (Rocket 540 V3 17.5T)** | 55 body / 70 with shaft × Ø35.8 can, 156.7 g — MEASURED([`w17-batch1-measurements-for-codex.md:42`](../../w17-batch1-measurements-for-codex.md)) | **REAR**, fixed by donor design | X ≈ −105, transverse | not a placement decision — the belt drive fixes it. It is the single heaviest item and the reason the car is rear-biased (§4.3) |
| 10 | **2× UBEC 5 V / 5 A** | 44.3 × 22.1 × **9.1**, 10 g each — MEASURED([`w17-batch1-measurements-for-codex.md:45`](../../w17-batch1-measurements-for-codex.md)) | **CAS-L0**, on the PDB | flat, side by side (~44 × 44 footprint on the 55 × 45 plan) | the 9.1 mm measurement is what makes a low PDB possible at all; keeping both on one board keeps Rail A and Rail B lanes separable and keeps switching noise inside one shielded-ish cell, away from the RX corner |
| 11 | **PDB** (XT60 in, 2× UBEC, 1000 µF, 27k/10k divider, star ground) | 55 × 45 plan — **TARGET**; installed audit top **Z14** — DERIVED(I-13:97) | **CAS-L0**, rotated | X +1…+46, L ±27.5, Z 1…14 | it is the electrical keystone: every rail, the divider and the ground star are one part, so one board under the boards is the shortest total wire length. Rotated so its 45 mm side runs fore-aft. `KO-01 bottom Z22 − Z14 = 8 mm` — exactly the moving policy, **zero reserve** |
| 12 | **MAX98357A I2S amp** | 18.7 × 17.9 × 3.0, 10.4 g with speaker — MEASURED([`w17-batch1-measurements-for-codex.md:46-47`](../../w17-batch1-measurements-for-codex.md)) | **CAS-L1**, next to RP1 | X −31…−13.2, L −10.2…+9.2, Z 13…16 | 3 mm tall and weightless; it belongs beside its board's I2S header, not in the sidepod, so the 5-wire I2S run stays inside the cassette and only the 2-wire speaker pair crosses to the sidepod |
| 13 | **Speaker (4 Ω 3 W)** | 35.3 × 25.1 × 6.1 — MEASURED([`w17-batch1-measurements-for-codex.md:47`](../../w17-batch1-measurements-for-codex.md)) | **FLOOR**, left sidepod (Z4L) | X ≈ −30, L ≈ +43, Z 3…15; port outward | the sidepod is the only place with an existing outward opening; D-03 shows the pocket band \|L\| 30…54 with 22–30 ceilings accepts it either side (I-06). **Left** is chosen deliberately: it is a named L/R balance trim path against a right-heavy ledger ([`I_zone_layer_plan.md:203-209`](I_zone_layer_plan.md)) |
| 14 | **WS2812B loom (7 installed pixels planned)** | 9.5 mm strip width, 17 g/m — MEASURED([`w17-batch1-measurements-for-codex.md:49`](../../w17-batch1-measurements-for-codex.md)) | tail → **WING/REAR**, halo → **SHELL** | tail via the drawing-`[7]` "Pass LED here" channel; halo under `new halo 2.1` | the tail **must be pre-routed before the rear stack closes** ([`K_printable_support_spec.md:184-191`](K_printable_support_spec.md)) — it is not retrofittable. Halo segment reaches the chassis through the single CN-BODY disconnect |
| 15 | **1000 µF LED reservoir + 330 Ω series + 1N5819** | Ø10 × 20 ESTIMATED(electrolytic class) | at the **strip input**, not on the PDB | first-LED end of the loom | [`w17-pdb-build-and-connector-guide.md:120-125`](../../w17-pdb-build-and-connector-guide.md) puts the LED reservoir at the strip input, which is where an inrush reservoir does its job. A second 1000 µF lies flat on the PDB for Rail B |
| 16 | **A3144 Hall + Ø3×1 magnet** | ≤4.17 × 3.10 × 1.57 — DOCUMENTED; magnet Ø3×1 CONFIRMED | **REAR**, at the rear axle X −90.9 | face gap target 1.5 mm, validate 1–3 mm (KO-27) | fixed by the magnet on the axle. **Routing is a safety-relevant choice** — see §4.5 and I-24 |
| 17 | **BX100 low-voltage buzzer (optional)** | 40.1 × 28.6 × 13.0, 13.4 g — MEASURED([`w17-batch1-measurements-for-codex.md:50`](../../w17-batch1-measurements-for-codex.md)) | **not a cassette occupant** — floor, if fitted at all | owner opt-in | it is the largest optional item on the car and buys nothing the firmware's own low-battery behaviour does not already give the giftee. Recommend: **omit**; the volume it wants is the volume the ESC relocation needs |
| 18 | **XT90-S anti-spark loop key** | ASSUMED body and pull axis | **FLOOR**, inline on the pack lead, **body-accessible** | at the pack-side battery edge | the giftee's entire on/off ritual is this key ([`learning-manual/14_glovebox_owners_booklet.md:91-96`](../../learning-manual/14_glovebox_owners_booklet.md)). It is off the PDB by decision F9b so that "key out = safe to charge" is a real electrical interlock and not a story (I-19). It must be pullable **with the body on** |
| 19 | **USB-C charge board (IP2326 class) + charge-state LED** | conflicting inputs, see §1 — **ASSUMED** | **CAS-L0**, rear stem lower layer; port + LED at the **flap** (§7) | board X −31…−1, L −13…+12, Z 1…11 | it taps the pack side of the master (I-19), so it lives near the pack lead entry. The *port and its state light* are a separate placement problem from the board, and they are the giftee-visible half (§7) |
| 20 | **2S LiPo pack** | selected pack 69 × 35 × 18, 88 g — MEASURED([`fit_studies/ZK_electronics_cassette_fit_study.md:70`](fit_studies/ZK_electronics_cassette_fit_study.md)); hard limit ≤75 × 45 × 25 | **FLOOR**, left, off the cassette | X −77…−8, trial L +30…+65, Z 1.5…19.5 | heaviest single removable mass → lowest possible, and **left** to fight the right-heavy ledger. Nothing may be mounted above it: the top must stay open for the swap. Bay length ≈78 mm ✔ (I-10) |
| 21 | **DS3235SG steering servo + `Servoholder`** | 40.25 (54.5 with lugs) × 37.8 × 20.2, 70.3 g — MEASURED([`w17-batch1-measurements-for-codex.md:43`](../../w17-batch1-measurements-for-codex.md)) | **FLOOR**, mid-chassis centreline — **an occupant, not a placement** | holder X −85.76…−27.76, Z 0…22.89 | fixed by drawing `[2]`. Everything else is placed *around* it. The measured 20.2 mm side face against the 18.5 mm arch is a real **~1.7 mm interference** (§10, OP-B) |
| 22 | **MG90S ×3 (pan, tilt, DRS)** | 22.8 × 12.2 × 28.5, 13.4 g each — DOCUMENTED(genuine TowerPro; clones vary) | pan/tilt → **PED**; DRS → **WING** pocket | pan/tilt at the pedestal head; DRS at X ≈ −125, L ≈ 0, Z ≈ 55…80 | pan/tilt follow the camera by definition; DRS is fixed by the donor wing's own pocket. Reserve a **15 mm horn radius** around every spline until the real horns are measured ([`fit_studies/ZA_accessory_servo_fit_study.md:42`](fit_studies/ZA_accessory_servo_fit_study.md)) |
| 23 | **SP3T boot-mode selector** (GPIO27 = SOLO, GPIO32 = SHOW, centre = LAPTOP) | slide-switch body **ASSUMED** | **CAS**, on the cassette's X+42 service edge, beside the two USB-C ports | — | the design already commits to *"a labeled slide switch on the cassette, reachable under the engine cover — the shell itself stays unmodified"* (I-22). Putting it on the same edge as the USB-C ports means **one** access opening serves flashing, mode selection and service. Common goes to the ground star; both throws are ordinary GPIO with internal pull-ups (I-21) |

### 3.1 Rows this table deliberately changes

| Change | From | To | Evidence |
|---|---|---|---|
| Amp station | Z3R-L1 deck beside CTL-E2 ([`J_component_placement_matrix.md:29`](J_component_placement_matrix.md)) | CAS-L1 rear service deck | the deck architecture was replaced by the cassette (I-13); the amp follows its I2S header |
| BX100 | "optional / PS-15 side" ([`J_component_placement_matrix.md:46`](J_component_placement_matrix.md)) | **recommend omit** | 40.1 × 28.6 × 13.0 MEASURED is large for a duplicated function, and the ESC needs volume |
| SP3T selector | not placed anywhere in A–Z | cassette X+42 access edge | I-21/I-22; the selector post-dates the whole mechanical package |
| Pedestal anchor | "floor/front structure, joint TBD" ([`J_component_placement_matrix.md:147`](J_component_placement_matrix.md)) | candidate: existing ff M3 at X+57.50 / +64.24 + spigot at X+78.11 | I-02 (occupancy still unverified) |

---

## 4. The nine rationales, stated once

### 4.1 Thermal
Three heat sources, three different answers. The **motor and ESC** stay in the rear
pocket with the rear-out exhaust path and never share a bay with Rail-A electronics
(E-05, KO-09, KO-16). The **Wi-Fi module** is the cassette's only real dissipator and
therefore takes the rear stem under the airbox chimney, heatsink up, with a
Z19…29 clear-air reserve above it — the tall channel is 26–32 mm wide at those
stations (I-05), which is a chimney, not a pocket. The **UBECs** self-heat at load and
sit on an open-slotted PDB floor. Nothing on the cassette is allowed to sit in the
ESC's exhaust.

### 4.2 Wiring and rails
Rail A (clean) = camera, Wi-Fi, both ESP32s, RP1, amp, LED, Hall. Rail B (servos) =
steering, pan, tilt, DRS, blower. ESC/motor ride the battery branch. Grounds meet at
**one star on the PDB** (I-18). Placement follows the rails, not the other way round:
the two boards sit directly above the PDB so every rail tap is a short vertical run;
the amp sits beside its own board so the 5-wire I2S never leaves the cassette; the
speaker's 2-wire pair is the only audio conductor that crosses to the sidepod. The
ESC's signal lead carries **signal and ground only — the ESC's internal BEC +5 V is
isolated** ([`B_component_envelope_register.md:81`](B_component_envelope_register.md)).

### 4.3 CG and four-corner balance
The current planning ledger is **1717.6 g, 36.50 / 63.50 % front/rear, Z-CG 21.50 mm**
in the conservative 1.00 m-LED bookkeeping case
([`fit_studies/ZK_electronics_cassette_fit_study.md:250`](fit_studies/ZK_electronics_cassette_fit_study.md)) —
inside the assumed 36–40 % front band, but **not a measurement**. Motor 156.7 g + ESC
100 g are the rear anchor and cannot move. The named trim paths, in order: pack to the
**left**, speaker to the **left**, the PS-01 outboard **ballast land**, and pack
station ±10 mm fore/aft. Everything the cassette adds is deliberately low (PDB top
Z14) or light (control/RF group ~31.8 g). **No ballast may be cut, and no balance
claim made, before D-39 four-corner scales.**

### 4.4 RF separation
Two links, two bands, one rule: physical separation and no metal nearby (KO-17, KO-26).
ELRS 2.4 GHz lives forward-left with its 65 mm T antenna dressed along the inner shell
line; the two 5.8 GHz whips live at chassis-mounted posts at the cassette rear,
≥150 mm from the ELRS tip, roots turning outward with ≥10 mm coax bend, never clamped
at the plug. Neither antenna may run beside the pack or the ESC/motor leads. The
PLA/PETG body is RF-transparent, which is the one thing in the RF budget working in
our favour. All of it is **unproven until D-20 / D-33** (E-32).

### 4.5 The Hall lead is a control-safety route, not just a wire
The 2026-09-03 control-firmware review (I-24, `timing-1`, high, gift-blocking) found
that the GPIO35 rising-edge ISR has **no interrupt-rate bound**: an edge storm can
starve the 50 Hz control tick while LEDC holds the last ESC duty. It also records the
hardware fact that **GPIO34–39 have no internal pull-ups**, so a floating or noisy
Hall line cannot be rescued in software. Mechanical consequence, and it is a real one:

- route the 3-wire Hall lead **away from the ESC and motor phase leads** — no parallel
  run, cross at 90° if it must cross;
- keep it **short**, with its external 10 kΩ pull-up as close to the board as
  practical;
- give it its own guide on the rear-tail rail (PS-09), not a shared bundle with the
  three phase wires.

This is routing guidance derived from a code finding; the firmware-side rate bound is
a separate fix and is **not this document's to make** — `[fix-wave: timing-1]`.

### 4.6 The LED data lead
Keep the WS2812 data run from ESP32 #2 GPIO4 short and away from the servo and motor
looms — ordinary single-ended 800 kHz signal-integrity practice, and the reason the
sound/light board sits on the same side as the loom (row 2). ⚠ For the record: the
adversarial review's Schottky **data-line margin finding (`safety-3`) was REFUTED**
(I-25) and **must not be reopened**; the routing guidance above stands on
signal-integrity grounds alone, not on that finding.

### 4.7 USB-C reachability and the one service opening
Both board USB-C connectors face the **X+42 cassette edge**, and the SP3T selector
joins them there. That single edge is the whole service story: flash board #1, flash
board #2, choose the boot mode. It is reached **under the engine cover** with the
shell otherwise untouched (I-22) — which is also exactly the access the booklet
promises the giftee for the selector, and no more (I-23). The **charge** USB-C is a
*different* port with a *different* audience and is placed separately (§7).

### 4.8 Speaker port, LED routes, one-hand lift-out, selector reachability
The speaker wants an outward opening — the left sidepod's existing vent (DN-07). The
LED tail is pre-routed (row 14). The cassette's service intent is unchanged and
one-handed: **body off → pull the master key → unplug the ganged dock → release the
external saddle → lift the cassette straight up around the fixed pedestal**
([`fit_studies/ZK_electronics_cassette_fit_study.md:287-290`](fit_studies/ZK_electronics_cassette_fit_study.md)).
Every part of that path is a **gate**, not a proof: the saddle does not exist yet
(CAS-07), and the ganged dock's straight front face is rejected (KO-33).

### 4.9 Vibration and crash
20 g forward is the design crash load ([`K_printable_support_spec.md:70-71`](K_printable_support_spec.md)).
Consequences: the pack is strapped, not clipped; boards are retained by edge guides
plus a per-side retainer, never by their own PCB holes; every printed load path prints with
layers across the load, not along it; ties every ≤60 mm near motion; and the front
crash zone (E-24) carries **nothing** — the nose has no protected cavity at all (D-25
found cowl-only forward of the installation ring).

---

## 5. The second-floor cage

> **Owner's ask, verbatim intent (A3, 2026-09-02):** *"maybe develop additional inner
> cage or structure to put some devices (like ESPs) on the 'second floor' inside."*

### 5.1 What "second floor" resolves to here

There are two ways to give the ESP32s a second level, and the geometry picks one of
them for us.

**SF-A — twin on-edge wall seats (RECOMMENDED).** Each board stands on its 39 mm edge,
PCB plane vertical and parallel to the centreline, occupying `X +3…+42, |L| 30…43,
Z 1…32`. The boards genuinely ride *over* the PDB cell (Z1…14) without a mezzanine
plate; the "second floor" is realised as the *upper 18 mm* of a full-height wall seat.

**SF-B — flat mezzanine plate over the PDB (REJECTED, with arithmetic).** A board laid
flat is 13 mm tall over its deck. To keep its top clear of the provisional KO-01 band
by the 8 mm moving policy the top must be ≤ Z14 — i.e. the deck top must be ≤ Z1,
which is the cassette floor. Over a PDB whose own audit top is Z14 the mezzanine cannot
exist on the centreline. Moving it outboard does not save it: flat, the board needs
**31 mm of lateral band**, but the band between KO-01's \|L\| ≥ 30 boundary and the
shell shoulder is only ~13 mm wide at these stations — and pushing out to \|L\| = 50
meets ceilings of **9 mm at X+20 and 7 mm at X+40** (I-04). SF-B fails on both axes at
S0 = 0 and is not recovered by S0 = 11 at the outboard stations.

**Therefore the cage is a stepped twin-wall board cage, not a deck.** This is not a
rejection of the owner's idea — it is the same idea, executed in the only orientation
the car has room for.

### 5.2 The 13 mm band, shown

| Constraint | Value | Source |
|---|---|---|
| KO-01 lateral boundary (provisional) | \|L\| ≤ 22 | I-08 |
| + 8 mm moving policy | boards must start at \|L\| ≥ 30 | I-12 |
| board thickness with headers | ~13 mm | DOCUMENTED(SKU), ASSUMED installed |
| board outer face | \|L\| = 43 | I-13 |
| shell shoulder collapse | ceiling 7–9 mm at \|L\| = 50, X +20…+40 | I-04 |

`43 − 30 = 13 mm` — the band is exactly one board thick. There is no second
arrangement hiding here.

### 5.3 Deck height from the seated-shell datum, and the S0 gate

Board top = **Z32**. Static policy adds 5 mm, so the shell roof must be at **Z37**
above DAT-F over the seats. The worst finite roof sampled over both seat footprints is
**Z27.18** at approximately X+3 / L−37, hence:

```
required S0 = 32 + 5 − 27.18 = 9.82 mm
```

S0 is bounded 0…~11 (I-10). **9.82 of an 11 mm ceiling is not a margin — it is a
coin flip**, and it is the single measurement that decides whether this cage is built
at all. It is measurement **M-01** in §9 and it is the reason the cage's board-top
height is a parameter (`cage_board_top_z`), not a constant.

Two parametric escape routes are built into the model so a bad S0 is a number change,
not a redesign:

- `board_seat_z0` — lift the boards off the cassette floor (default 1 mm). Lowering to
  0 buys 1 mm.
- `guide_top_margin` — the aft end guide (§5.4, the only full-height member) may stop
  **below** the board's top edge, leaving the per-side retainer as the only structure
  at full height, local rather than continuous.

If S0 measures below ~9.8 mm the honest answer is **not** to shave the cage: it is to
reopen the board orientation with a real number in hand, which is what
[`fit_studies/ZK_electronics_cassette_fit_study.md:363-364`](fit_studies/ZK_electronics_cassette_fit_study.md)
already demands as a production stop.

### 5.4 Shape: why it steps

The cage cannot be a simple box. Two independent constraints forbid the obvious
shapes, and between them they leave exactly one legal envelope for structure.

1. **KO-01 forbids height near the centreline.** The provisional band is Z22…38 at
   \|L\| ≤ 22 (I-08); applying the 8 mm static-to-moving policy (I-12) on **both**
   axes, nothing may be taller than **Z14** anywhere inside **\|L\| ≤ 30**.
2. **The PDB forbids structure in the middle.** The PDB cell is `X +1…+46,
   L ±27.5, Z 1…14` (I-13). Any member crossing that X band inside \|L\| ≤ 27.5 above
   Z1 lands on the board it is supposed to sit *above* — including a Z14-capped one,
   because **Z14 *is* the PDB's audit top**.

Intersect the two. Above Z14 the only legal lateral band is \|L\| 30…43, and §5.2
already showed that band is **exactly one board thick**. Therefore:

> **There is no legal cross-member anywhere above the cassette base plate between
> X+1 and X+46, and no legal wall *beside* a board above Z14.** Any sketch of this
> cage as a full-height twin-wall box is arithmetically wrong, and the two lines above
> are why.

What survives:

- **Base plate, Z0…1, full width** — the *only* member that crosses the centreline.
  It lies *below* the PDB's Z1 seat, in what is already the isolation layer. The cage
  is therefore **a feature of the cassette base, not a separate box bolted on top of
  it**;
- **two low register walls** at **\|L\| 27.5…30.0**, **Z1…14** (2.5 mm thick, capped at
  Z14 by constraint 1). The inner face lands exactly on the PDB's L±27.5 edge and gives
  it a lateral register; the outer face is where the board's PCB plane starts. They
  back the boards' lower 13 mm and are the boards' guard against the steering rod.
  **They stop at Z14 — that cap is the "step"**;
- **two aft end guides** at **X +1…+3, \|L\| 30…43**, rising from the base plate to the
  board top: a U-channel per side that the board's aft short edge slides down into.
  This is the *only* place in the cassette where full-height structure is legal —
  outboard of \|L\| 30 (constraint 1) and clear of the PDB in X (constraint 2);
- **two per-side retainers** over the board tops (§5.6) — not one bar;
- **no top bridge, no forward end wall, no cross-member between X+1 and X+46.**
  Torsional stiffness comes from the base plate, the two register walls, and the two
  aft end guides acting as C-channels closed by the retainers.

The boards clip to the **outboard** faces of the register walls: PCB plane at
\|L\| 30…31.6, components projecting outboard to \|L\| ≤ 43.

**What this leaves open, as a parameter and not a fudge.** Each board's *forward* end
has no post to land on. The registered seat runs X+3…+42 and the cassette wing ends at
X+42; forward of that the tapered tongue narrows to \|L\| ≤ 29.5 (I-13) and cannot
carry outboard structure, and the 5 mm from the tongue to the pedestal is a static
clearance, not free volume. So the forward end is either a **cantilevered retainer** or
the board seat shifts ~2 mm aft to buy a forward drop-leg. `board_seat_x0` exists in
[`../11_cad/w17_params.scad`](../11_cad/w17_params.scad) for exactly this, and **M-03**
(the board's real length) decides it. Recorded as **OP-H**.

### 5.5 Mounting: what it may attach to, and what it may not

The no-new-holes rule in donor parts is absolute
([`K_printable_support_spec.md:10-12`](K_printable_support_spec.md)). Within the
cassette footprint (X −31…+46) the registered M3 features are (I-02):

| Feature | Coordinate | Part file | Disposition |
|---|---|---|---|
| splice screw | X +22.69, L 0 | `FloorBoard2.stl` ↔ `2023NewFrontFloorLargerParts.stl` | **candidate shared donor stack** — collinear trio, needs longer M3 + spacer |
| splice screw | X +14.26, L 0 | same | same |
| splice screw | X +7.50, L 0 | same | same |
| rear bracket (fwd pair) | X −27.76, L −13.50 | `2023NewBackFloorLargerParts.stl` | **contested** — KO-19 candidate seat |
| rear bracket (fwd pair) | X −27.76, L +16.50 | same | **contested** |

Everything else in that footprint is plain plate. The four former cassette boss
centres `(−15, ±12)` and `(+35, ±12)` are **REJECTED** — they lie inside the charge and
PDB target cells (I-13 §5).

**Proposal (new, and it needs the P1 occupancy check before it is anything else):** the
three collinear centreline splice screws at X +7.50 / +14.26 / +22.69 are the only
existing-hole anchor candidates inside the cassette footprint, and they lie under the
PDB cell where the cassette base already has structure. Sharing that donor stack with
longer M3 screws through a low centreline foot would give the cassette a **registered
fore-aft datum** it does not otherwise have, leaving the external saddle to do only
what it is good at — clamping down. Constraints that make this a proposal and not a
design: the trio is collinear (no rotation resistance on its own), the centre band is
**OPEN at X −14…−4** and MIXED at each splice station (I-03), the screws are the
donor floor splice and their length headroom is unknown, and the study may not assume
the splice can take a taller stack.

Outside the cassette, the free singles remain as recorded: `(−39.99, −32.86)` belt
side and `(−39.94, +17.14)` mirror side, plus `b2 (−80.18, ±30.75)` and
`bf (−85.93, +5.00)` unassigned (I-02, I-07).

### 5.6 Retention: tool-less, and it never touches a PCB hole

Three edges, no fastener through the board, and **nothing above the board's top
edge** — that last rule is the one the CAD found, and it is load-bearing.

- The board's **bottom long edge** drops into a 1.8 mm slot in the base plate
  (chamfered lead-in), and its **aft short edge** butts the aft end guide's block,
  with a 2 mm post reaching over its aft-outboard corner (§5.4). Two edges located
  before anything is fitted.
- Its inboard face is backed for its lower 13 mm by the register wall; above Z14
  nothing may stand beside it, so the **top long edge** is captured instead — by
  **two clips per board**, at two short stations, each dropping onto a printed peg in
  the base plate and reaching over the top edge with a 2 mm finger.
- **The clips' top faces are flush with the board top (Z32).** §5.3's required S0 is
  measured from that plane: a 3 mm bar lying *over* the board turns `32 + 5 − 27.18 =
  9.82` into `35 + 5 − 27.18 = 12.82` mm, which is **outside the 0…11 mm bound S0 is
  known to live in**. A retainer that adds height does not make the cage worse — it
  ends it. [`../11_cad/w17_params.scad`](../11_cad/w17_params.scad) asserts
  `s0_required ≤ 11` on every render so this cannot come back by accident.
- **There is no screw and no heat-set insert**, and that is arithmetic, not taste. An
  M3×5 insert needs an 8 mm boss; the aft end guide is **2 mm long in X**, and above
  Z14 the only legal band is \|L\| 30…43, which the board fills. There is nowhere in
  the cage to put one. The clips are tool-less: board in, clips on, fingernail off.
- **Retention necessarily touches the component zone.** The band is exactly one board
  thick (§5.2), so anything reaching over a board stands where its outboard components
  are. The only variables are *how much* and *at how few stations*. Two clips per board
  is the smallest answer that still resists the 20 g crash load; **where** they may sit
  is decided by the real board — **M-03**, then coupon **C-3** with a board in hand.
- **The PCB's own mounting holes are never used, never enlarged, never loaded** — the
  same rule the package already applies to servo ears and bearing seats
  ([`K_printable_support_spec.md:308-310`](K_printable_support_spec.md)).
- A clip may be **notched at its USB-C station** if M-03 puts the port on a long edge;
  if the port is on the forward short edge, as currently assumed, the clips are already
  clear of it and flashing needs no disassembly either way.
- The SP3T selector mounts in the cassette's **X+42 dock face**, below Z14 and inboard
  of the boards, beside the two USB-C openings, so one hand reaches both ports and the
  switch.

### 5.7 Pass-throughs

| Pass-through | Where | Notes |
|---|---|---|
| ganged dock face | X +42 edge, **stepped/wrapped, not straight** | a straight X+42…+58 / L±32 projection overlaps the pedestal and is rejected (KO-33) |
| U.FL coax roots ×2 | X +1 module edge, L −8 / +8 | 12 × 12 × 6 reserve each, ≥10 mm bend, never clamp a plug |
| pedestal conduit | fixed pedestal, **not through the cage** | 10 × 18 clear target / 14 × 22 outer; camera USB + 2 × 3-pin descend sequentially |
| LED / Hall tail | rear floor edge via PS-09 | pre-routed before the rear stack closes |
| USB-C service ×2 + SP3T | X +42 dock face, below Z14 | one opening, three functions |
| charge USB-C + pack balance | **dock/edge route, never the pedestal conduit** | explicit ZK rule (I-13 §7) |

### 5.8 It stays a lift-out cassette

The cage is *part of* the cassette, not a second thing bolted to the floor. Test of
success: with the body off, pulling the master key, unplugging the dock and releasing
the saddle must let **one hand** lift base plate + PDB + cage + both boards + the rear
service deck **straight up**, past the fixed pedestal, with both USB-C plugs and the
selector still fitted. That is a timed drill at CAS-34 / Q, and it is not passed
today.

---

## 6. DRS linkage check

**What exists.** `2021Rearwing with DRS.stl` (raw bbox 105.1 × 82 × 60) with a
designed DRS-servo pocket and a metal-rod linkage per drawings `[0]`/`[2]`;
`DRS Arm for 2021 Rear Wing.stl` (raw bbox **58 × 5 × 10**); one MG90S; a metal rod;
the flap (I-16, [`MODEL_INVENTORY.md:189`](../MODEL_INVENTORY.md),
[`ASSEMBLY_NOTES.md:51`](../ASSEMBLY_NOTES.md)).

**What is actually known.** Only the two raw bounding boxes. Every transform —
where the pocket is, where the hinge axis lies, where the arm's two pivots are —
is **ASSUMED** ([`fit_studies/ZA_accessory_servo_fit_study.md:28-30`](fit_studies/ZA_accessory_servo_fit_study.md)).

> ⚠ **The 58 mm is a bounding box, not a pivot spacing.** A four-bar linkage is
> defined by its pivot-to-pivot lengths, and we do not have one of them. Any throw
> calculation from 58 mm would be invented. This study does not make one.

**The keep-outs.** KO-12 (servo + 58 mm arm + rod, moving) and KO-25 (≥8 mm to the
68 mm shock, the LED loom and the body, around X ≈ −125), both gated behind Gate A
and Gate B (I-08, I-09).

**The four things that can kill it, in the order they will show up.**

1. The pocket does not accept the purchased MG90S without distorting — clone ears and
   bosses vary and no clone has been calipered.
2. The arm's throw does not sweep the flap through its designed angle without
   preloading it at either end.
3. The swept arm violates the 8 mm policy against the central 68 mm shock — the wing
   sits directly above the shock's territory.
4. The DRS lead cannot reach the dock without crossing the belt/spur rotation or the
   LED tail (KO-21, KO-29).

**Geometry to measure (M-14 in §9), with datums:**

| # | Measurement | Datum | Tool / accuracy |
|---|---|---|---|
| a | wing pocket internal L × W × H, and its wall thickness | pocket floor | calipers ±0.2 |
| b | MG90S body, ear pitch, ear hole Ø, boss height, spline height and count, lead exit | servo case face | calipers ±0.2 |
| c | horn radii actually supplied (each hole) | spline centre | calipers ±0.2 |
| d | **arm pivot-to-pivot spacing** and both hole Ø | hole centres | calipers ±0.2 — *the number the 58 mm bbox does not give* |
| e | flap hinge axis position and its perpendicular distance to the arm's driven pivot | hinge line | calipers ±0.5 |
| f | flap closed and open angles wanted | chord vs wing datum | protractor ±2° |
| g | rod length between rod-end centres, rod-end type/thread | rod-end ball centres | calipers ±0.2 |
| h | nearest approach of the swept arm to: the 68 mm shock body at full compression, the LED tail, the body inner | swept envelope | feeler/rule ±1 |
| i | servo neutral orientation that puts the rod straight at flap-closed | horn at neutral | mark and photograph |

**Rule:** never test the pocket alone — the DRS check runs with the real rear
shock/stack/wing/LED harness present
([`fit_studies/ZA_accessory_servo_fit_study.md:96`](fit_studies/ZA_accessory_servo_fit_study.md)).
**Stop** if a servo must distort its pocket, an ear needs drilling, the horn hits the
wing, the linkage preloads the flap, or a wire becomes the hard stop.

---

## 7. USB-C charge flap — placement candidates

**The constraints, and they are unusually tight.**

- **Giftee promise:** *"She charges through a small hidden flap — the same plug as most
  phones (USB-C)"*, with *"a little light [that] tells you how it's going"* at the flap
  area, and *"don't open her up"*
  ([`learning-manual/14_glovebox_owners_booklet.md:79-85`](../../learning-manual/14_glovebox_owners_booklet.md),
  [`:177`](../../learning-manual/14_glovebox_owners_booklet.md),
  [`:230`](../../learning-manual/14_glovebox_owners_booklet.md)).
- **Owner constraint:** *"the shell itself stays unmodified"* (I-22).
- **Package constraint:** *"the hidden port must use an existing opening or reversible
  insert; this study authorizes no shell cut"*
  ([`fit_studies/ZK_electronics_cassette_fit_study.md:355-356`](fit_studies/ZK_electronics_cassette_fit_study.md)).
- **Safety ritual:** key out before charging (I-19), so the flap and the key should be
  reachable in one ergonomic gesture, not on opposite ends of the car.
- **Showpiece first:** priority 1 of this repo is realistic final appearance
  ([`../CLAUDE.md:18`](../CLAUDE.md)).

**Candidates.**

| ID | Where | Pros | Cons / cosmetic cost | Verdict |
|---|---|---|---|---|
| **CF-1** | **Reprint `2023NEWSideVent1.stl` / `2023NEWSideVent2.stl` with the flap integrated** | zero shell cut — the vent is a part we print anyway; a flap seam reads as a vent louvre; the sidepod already faces the correct side for the pack; fully reversible (keep the stock vent) | needs the vent's real internal geometry; the flap becomes a visible feature on a livery panel; multi-body STL flagged in inventory | **RECOMMENDED** — highest ratio of giftee usability to cosmetic cost |
| **CF-2** | Reversible printed insert in the existing floor opening at **X +39.18, \|L\| 55.71** (13.1 × 10.3 through-slot, I-02) | genuinely existing opening; invisible from any display angle | it is on the *underside* — the giftee must lift or tip the car to charge, which fights "she sits on a shelf looking good"; the state LED would be invisible | **fallback** |
| **CF-3** | Under the **engine cover**, sharing the selector access | zero cosmetic cost; already an accepted giftee gesture (§4.7) | breaks the "hidden flap" promise — it becomes "open the engine cover to charge", i.e. opening her up; couples a daily action to a service action | **not recommended** (product regression) |
| **CF-4** | Reversible insert in the **cockpit opening**, under a printed cockpit cover / driver plate | no cut; central; the state LED could share the halo sightline | mutually exclusive with the driver figure and with camera Option A ([`C_clearance_keepout_register.md:22`](C_clearance_keepout_register.md)); the cockpit is the pedestal's territory | **rejected** while camera Option A stands |
| **CF-5** | New cut in the rear shell behind the sidepod | free placement | **violates the no-shell-mod constraint**; irreversible on a painted PLA shell; the highest cosmetic risk on the car | **rejected** |
| **CF-6** | The IP2326's own onboard Type-C reached by a short captive **pigtail** parked at CF-1's flap | avoids trusting a printed shroud to align a receptacle; the module keeps its own connector | a parked pigtail can be pulled into the car; needs a retainer | **combine with CF-1** — decide at ASM-59 once the SKU's Type-C edge is calipered |

**The state LED goes wherever the flap goes.** It is the giftee's only charging
feedback, and the booklet already reserves a row for its colours. It is on the charge
module, so CF-1 needs either a light-pipe from the board to the flap face or a
2-wire flying LED — **an ASM-59 decision once the SKU is in hand**, not a decision
this study can make.

**Nothing is authorized here.** CF-1 requires the vent parts' real internal geometry
(M-15), the charge SKU's real body and Type-C edge (M-16), and an owner call between
CF-1 and CF-2.

---

## 8. GCS box — concept

The contents, wiring and power budget are settled on the Claude side
([`w17-gcs-box-guide.md`](../../w17-gcs-box-guide.md)); the **enclosure** is now this
repo's (A3). What it must hold: ELRS TX module, FT232RL USB-UART, the approved dual-band
5 GHz-AP-capable Wi-Fi adapter (RT5370 demoted to spare), a USB hub, one uplink cable,
and — only if the bench says so — a 12 V barrel input (I-20).

**The blocking fact:** exactly one envelope in the box is even vendor-documented
(ES24TX Pro 70 × 49 × 32.5 mm, 51 g, *and only if the on-hand unit is the Pro*). The
FT232RL, the adapter and the hub have **no measurement anywhere in the workspace**, and
the hub is not procured. So the concept is deliberately a *layout strategy*, not a
box:

- **Sled architecture.** A plain rectangular base tray with a repeating M3 grid; each
  module rides a small printed **sled** that carries only that module's pocket and
  strain relief. When a module is calipered — or swapped — one sled is reprinted, not
  the box. This is the only design that survives four unknown envelopes.
- **Bulkhead panel.** One end wall is a separate printed panel carrying the uplink
  strain relief, the antenna exit, the blanked DC barrel and the optional flash-access
  port. Port positions change by reprinting a 2 mm panel.
- **Antenna outside the print, always** — RF does not transmit from inside a closed box
  pressed against a hub PCB (I-20 requirement 1).
- **Vent slots over the TX module** — it is the box's only meaningful dissipator; a
  sealed print is the wrong default even at the pinned 25–100 mW.
- **Lid on captive M3 into heat-set inserts**, not self-tapped: this box will be opened
  during bring-up more than three times.
- **Non-slip feet and mass low** — it lives on a desk beside a laptop and will be
  tugged by one cable.
- **Material:** PETG. It is neither hot nor cosmetic; PLA would creep under a
  permanently tensioned uplink cable.

`gcs_box.scad` implements exactly this and **every dimension in it is ASSUMED**
(§12). It renders so the owner can see the strategy, not so anything can be printed.

---

## 9. Ordered measurement list

Ordered by **what unblocks the most**, not by convenience. Every row names the
existing D-plan / ASM / CAS identity it feeds and the
[`../11_cad/w17_params.scad`](../11_cad/w17_params.scad) parameter it fills. The
printable owner session is
[`../w17-mechanical-measurement-session-prompt.md`](../w17-mechanical-measurement-session-prompt.md).

| # | Measurement | Feeds | Datum | Tool | Tol. | Parameter | Value | Date |
|---|---|---|---|---|---|---|---|---|
| **M-00** | **Printed-parts inventory** — which donor parts physically exist, and their condition | everything; the print log says nothing is printed and the owner says otherwise | — | eyes + labels | — | — | | |
| **M-01** | **S0** — shell bottom edge above floor top, ≥4 points | D-04 / CAS-02; **the whole cage** | DAT-F ↔ shell bottom edge, shell seated and lightly pressed | depth gauge / feeler | ±0.5 | `s0_measured` | | |
| **M-02** | Steering lock-to-lock + bump sweep: rod height at 3 stations, lateral extent | D-26 / ASM-08 / CAS-01; replaces provisional KO-01 | DAT-F | rule + marker | ±2 | `ko01_z_lo`, `ko01_z_hi`, `ko01_l_half` | | |
| **M-03** | MH-ET board: outline, thickness bare and with headers, hole pattern + Ø, **which short edge carries USB-C**, plug protrusion, live-plug bend | CAS-03; cage slots | PCB edge | calipers | ±0.2 | `esp_len/wid/thk_hdr`, `esp_hole_*`, `esp_usb_*` | | |
| **M-04** | Female-header + male-pin stack height, seated | the socketing GO/NO-GO ([`w17-socket-stack-caliper-prompt.md`](../../w17-socket-stack-caliper-prompt.md)) | seated stack | calipers | ±0.1 | `esp_socket_stack` | | |
| **M-05** | Tallest PDB part: 1000 µF cap height, XT60 body height, loop-key body | CAS-04 / ASM-22; **PDB top governs the KO-01 gap** | PCB top | calipers | ±0.2 | `pdb_stack_h` | | |
| **M-06** | PDB finished outline + mounting holes + connector exits | CAS-04 | board edge | calipers | ±0.2 | `pdb_len/wid` | | |
| **M-07** | Cassette deck candidate heights: clear height available at X+3, +20, +42 over \|L\| 27…46 | aft end guide height (§5.4) | DAT-F, shell seated | depth gauge | ±1 | `guide_top_z` | | |
| **M-08** | Module weights: both boards, PDB assembled, charge module, XT90-S, cassette, pedestal | D-39 / CAS-11 | — | scale | ±1 g | — | | |
| **M-09** | **Four-corner weights**, rolling assembly | D-39 / ASM-58 | four scales | scales | ±5 g | — | | |
| **M-10** | Tyre arch clearance at full steer + full bump, both ends | D-37 / E-30 (margins are only 3.5 / 4 mm) | body-on | feeler | ±0.5 | — | | |
| **M-11** | ESC: exact label/variant, body with fan, feet, wire exits, and the **air volume above** available at every candidate station | D-28 / CAS-06 — **the failed station** | DAT-F | calipers + rule | ±0.5 | `esc_*` | | |
| **M-12** | Shell interior at the CF-1 / CF-2 charge-flap candidates: wall thickness, local depth, what is behind | §7 | shell inner face | calipers | ±0.5 | `flap_*` | | |
| **M-13** | SP3T switch body, throw, panel cut-out, terminal projection | §3 row 23 | switch body | calipers | ±0.2 | `sp3t_*` | | |
| **M-14** | **DRS geometry set (a)–(i)** of §6 | Gate B / D-35 / ASM-54 | per row | calipers + protractor | ±0.2 / ±2° | `drs_*` | | |
| **M-15** | Side-vent parts: internal geometry, mounting, visible face | CF-1 | vent seat | calipers | ±0.2 | `vent_*` | | |
| **M-16** | Charge SKU: body, height, holes, onboard Type-C edge, thermal face, exits — **resolves the §1 conflict** | ASM-59 / J-CHG-001 | board edge | calipers | ±0.2 | `chg_*` | | |
| **M-17** | GCS modules: FT232RL board, Wi-Fi adapter, hub (after procurement), TX module as-received | §8 | body | calipers | ±0.5 | `gcs_*` | | |
| **M-18** | Speaker basket/cone/holes + the chosen sidepod port aperture | D-36 / PS-14 | basket rim | calipers | ±0.2 | `spk_*` | | |
| **M-19** | Hall carrier surface, collar runout, achievable 1–3 mm gap band | D-38 / PS-16 | axle face | non-magnetic gauge | ±0.5 | `hall_gap` | | |
| **M-20** | Free-feature occupancy pass: which of the registered M3 features are genuinely free after the mechanical build | D-27 stage 2 | assembled floor | eyes + M3 screw | — | — | | |

**No power for any of it.** M-08…M-10 need a rolling assembly, not a live one.

---

## 10. Risks and open problems

Existing register rows this study depends on and does not close: **E-01** (no printed
mounts exist — this study is the answer to it, on paper), **E-02/E-03** (the central
shock and the component count), **E-27** (ESC envelope), **E-29** (pack not cleared
against S0 and steering), **E-30** (arch margins below policy), **E-35** (the two board
envelopes need S0 ≥ 9.82 and real holes/headers/plugs), **E-36** (pedestal), **E-37**
(no clean four-point pattern), **E-38** (dock bodies), **E-39** (USB + lift-out around
the pedestal), **E-41** (PDB 3 mm→8 mm to KO-01 and the Wi-Fi seat).

New or re-stated open problems this study raises:

| ID | Problem | Why it is here | Owner action |
|---|---|---|---|
| **OP-A** | **The ESC has no station.** Measured 34 mm body + 10 mm intake plane = Z45.5 required; no registered S0 = 0 shell station supplies it over the outboard footprint, and S0 = +11 does not recover it (I-15) | it is the largest single unsolved packaging problem on the car, and it is a *heat* problem, not just a space one | decide at M-11 with the body seated: relocate inboard/aft, accept a documented lower air gap with a measured thermal run, or change the ESC |
| **OP-B** | **DS3235SG vs `Servoholder` arch:** measured 20.2 mm face into an 18.5 mm arch = **~1.7 mm interference**, exactly as predicted ([`w17-batch1-measurements-for-codex.md:88-96`](../../w17-batch1-measurements-for-codex.md)) | it gates the whole floor print batch | no-force dry fit; if it binds, the fix is a relieved holder in CAD, **never a knife on the servo** |
| **OP-C** | **Charge-module identity conflict** (§1) | two documents give two different footprints; a pocket cut to either could be wrong | caliper the purchased SKU (M-16) |
| **OP-D** | **The cassette has no retention.** CAS-07 rejected the four-boss pattern; the external saddle does not exist | nothing lifts out until something holds it down | full-stack transparent dummy at CAS-07; evaluate the §5.5 centreline-splice proposal at M-20 |
| **OP-E** | **BX100 in or out?** 40.1 × 28.6 × 13.0 MEASURED, duplicating a firmware function | it competes for exactly the volume OP-A needs | owner call; this study recommends **out** |
| **OP-F** | **Charge flap CF-1 vs CF-2** | a product decision (showpiece vs invisibility) with a mechanical consequence | owner call after M-12 / M-15 |
| **OP-G** | **The three centreline splice screws** as a shared donor stack (§5.5) | it would give the cassette a real datum, or it is occupied and the idea dies | M-20 |
| **OP-H** | **The boards' forward end has nothing to land on.** KO-01 + the PDB leave no legal structure above Z14 except outboard of \|L\| 30, and the registered seat X+3…+42 already reaches the wing's forward edge (§5.4) | it decides whether each retainer cantilevers or the seat shifts ~2 mm aft — a difference in stiffness, not in cosmetics | **M-03**, then a C-3 coupon with a real board |

---

## 11. Fit-check coupon plan

**Rule: coupons before production prints, always.** Each coupon is a `TP-NNN` entry in
[`../04_test_prints/`](../04_test_prints), physically labelled `TP`, printed in draft
settings, and **never installed on the car**
([`../MODEL_INVENTORY.md:27-35`](../MODEL_INVENTORY.md), E-22). Sources:
[`../11_cad/fit_check_coupons.scad`](../11_cad/fit_check_coupons.scad).

| Coupon | What it answers | Pass criterion | Feeds |
|---|---|---|---|
| **C-1 peg/hole tolerance ladder** | what clearance this printer + this filament actually needs for an M3 through-hole and a 3 mm peg (7 steps, −0.15…+0.30) | the first step that assembles by hand without force, recorded per material | `fit_clearance` for every model |
| **C-2 standoff height gauge** | does a printed standoff hit its nominal height after squish and shrink | ±0.15 mm over 5 heights | `cage_*_z`, `pdb_seat_z` |
| **C-3 MH-ET hole-pattern + edge-slot coupon** | does a real board drop into the printed edge slot, and does the hole pattern line up | board seats by hand, no bow, no forcing; USB-C plug seats with the coupon fitted; **both clip stations land on bare PCB, not on a component** | `esp_*`, `cage_slot_w` |
| **C-4 S0 / deck-height gauge** | a stepped gauge that reads S0 directly under the seated shell at ≥4 points | consistent step reading at all points, ±0.5 | `s0_measured` (M-01) |

**Order:** C-1 first (it calibrates everything else), then C-2 and C-3 together, then
C-4 with the shell. Do not print a cage before C-1 and C-3 pass.

---

## 12. ASSUMED parameters — the list that must be measured before printing

Every entry is a named parameter in
[`../11_cad/w17_params.scad`](../11_cad/w17_params.scad), grouped there under an
explicit `ASSUMED` banner. None of them is a measurement.

| Parameter | Current value | Why it is a guess | Measurement |
|---|---|---|---|
| `s0_measured` | 9.82 (the *requirement*, used as a placeholder) | S0 has never been physically measured; 0…11 bound only | **M-01** |
| `esp_thk_headers` | 13.0 | "with headers" from the SKU class, not our board | M-03 |
| `esp_hole_dx`, `esp_hole_dy`, `esp_hole_d` | 33.0 / 25.0 / 3.2 | no MH-ET hole pattern exists in any project document | M-03 |
| `esp_usb_edge`, `esp_usb_w/h/offset` | X+ short edge, 9.0 / 3.5 / centred | ZK records the USB-C edge as unresolved | M-03 |
| `esp_socket_stack` | 11.0 | the socketing GO/NO-GO measurement is owed | M-04 |
| `pdb_len`, `pdb_wid`, `pdb_stack_h` | 55 / 45 / 13 | TARGET envelope; the tall part is unknown since the UBEC turned out to be 9.1 mm | M-05, M-06 |
| `guide_top_z` | 30 | the aft end guide's top, derived from a board top that is itself gated on S0 | M-07 |
| `board_seat_x0` | 3.0 (ZK's registered seat) | an ASSUMPTION gauge, and OP-H turns on whether it can move ~2 mm aft | M-03 |
| `ko01_z_lo/hi`, `ko01_l_half` | 22 / 38 / 22 | **provisional** steering band, physically unmeasured | **M-02** |
| `esc_l/w/h`, `esc_air_gap` | 44.2 / 33.7 / 34.0 MEASURED, air gap 10 ASSUMED | body is measured; the required intake plane is a policy number, not a datasheet | M-11 |
| `chg_l/w/h` | 30 / 25 / 10 | two conflicting sources (§1) | **M-16** |
| `sp3t_body_l/w/h`, `sp3t_cutout_*` | 20 / 9 / 12, cut-out 13 × 5 | no switch has been selected or calipered | M-13 |
| `drs_arm_pivot_span` | **unset — deliberately** | the 58 mm is a bbox; using it as a pivot span would be invention | **M-14d** |
| `flap_*` | opening 16 × 11, wall 2.0 | no shell interior measurement exists at any flap candidate | M-12 |
| `vent_*` | 13.1 × 10.3 from the floor opening | the *shell* vent's geometry is unmeasured; only the floor slot is registered | M-15 |
| `gcs_tx_l/w/h` | 70 / 49 / 32.5 | vendor figure, **and only if the unit is the Pro** | M-17 |
| `gcs_ftdi_*`, `gcs_wifi_*`, `gcs_hub_*` | 45×18×10 / 60×25×12 / 90×40×15 | **nothing is recorded anywhere**; hub not procured | M-17 |
| `spk_*` | 35.3 × 25.1 × 6.1 MEASURED body; port Ø 22 ASSUMED | the port aperture is a design choice with no acoustic evidence | M-18 |
| `hall_gap` | 1.5 | target inside a 1–3 mm band, never achieved on hardware | M-19 |
| `insert_*`, `screw_*` | M3×5 insert Ø4.0 × 5.7, M3 clearance 3.4 | typical brass-insert values; brand-dependent. **The cage uses none** (§5.6); the GCS box lid does | C-1 |
| `clip_*`, `fit_clearance` | 6 × 2 mm clip at X+10 / X+34, 0.20 mm per side | station positions are guesses until a real board is looked at; the clearance is what coupon C-1 measures | M-03, **C-1**, C-3 |

---

## 13. What this study does not prove

1. That the everything-inside claim closes. It does not — that verdict remains
   **CONDITIONAL-GO to a full-scale dummy** (I-13 §1) and nothing here upgrades it.
2. That any board, module or cassette fits. Every fit is a gauge at S0 = 0 against a
   provisional steering band.
3. That the ESC has a home (OP-A).
4. That the cassette can be held down (OP-D).
5. That the DRS linkage articulates (§6 — the pivot span is not known).
6. That the charge flap can exist without a shell cut (§7 — CF-1 is unmeasured).
7. Anything at all about powered behaviour. **A2 NOT-EXECUTED, Phase B BLOCKED**;
   nothing in this repo may be flashed, powered, or connected.

**Downstream:** parametric drafts →
[`../11_cad/`](../11_cad/README.md) · owner measurement session →
[`../w17-mechanical-measurement-session-prompt.md`](../w17-mechanical-measurement-session-prompt.md) ·
keep-outs → [`C`](C_clearance_keepout_register.md) · risks →
[`E`](E_constraint_risk_register.md) · gates → [`R`](R_validation_gates.md).
