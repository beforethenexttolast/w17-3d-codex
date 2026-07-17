# A · Assembly Evidence Report — W17 on OpenRC RC-01

Session 1 · 2026-07-17 · provisional evidence model. Confidence tags per
[`README.md`](README.md).

---

## 1. Sources inspected

### 1.1 Repository / engineering documents (read in full)
- `CLAUDE.md` (workspace + repo), `GENERAL_PLAN.md`, `BUILD_SHEET.md`,
  `MODEL_INVENTORY.md`, `ASSEMBLY_NOTES.md`, `CAMERA_GIMBAL_PLACEMENT.md`,
  `FIRST_PRINT_DECISION.md`, `MATERIAL_DECISION_MATRIX.md`, `PRINT_SPEC.md`.
- `docs/00_BUILD_SHEET_v2.md` (the historical "**Where it packs**" electronics packing
  plan + power rails), `docs/bill_of_materials_v2.md` (the current buy-list / component
  list), `docs/w17_wiring_assembly_atlas.html` (wiring topology — text extracted; noted
  stale on some numbers per `FIRST_PRINT_DECISION.md §5`).
- `01_inventory/inventory.csv` (210 rows: SHA-256, triangle count, authored-frame
  bounding boxes) and `01_inventory/build_inventory.py` (its generator — reviewed to
  confirm the bbox method: proper binary-STL vertex min/max, **trustworthy**).
- Supplier READMEs: Ryan's `READ ME.txt` + `Parts List.txt` + `Prerequisites.txt`;
  `New 2024 Body/READ ME.txt`; `New 1.1 Rear Upgrades/READ ME.txt`; `New 1.1 Steering
  Upgrades/READ ME.txt`; `Photos to help installation/READ ME.txt`.

### 1.2 Visual references (actually viewed, not just filenamed)
Installation drawings — `unsorted_stl_raw/Ryans Creations Open RC F1 Car/Drawings for
Installation/` (each is a single-page A3 sheet):
- `[0] FULL CAR.pdf`, `[0] FULL CAR EXPLODED VIEW.pdf`, `[1] BODY ASSEMBLY.pdf`,
  `[2] FLOOR ASSEMBLY.pdf`, `[3] FRONT SUSPENSION ASSEMBLY.pdf` — **all viewed this
  session.**
- Rev-1 revised drawings `[4]`–`[9]` live in a *different* folder
  (`RC-01 Revision 1 Files/Revised Drawings/`); `[5]`/`[7]` were reviewed 2026-07-10
  (findings in `ASSEMBLY_NOTES.md`); `[4]/[6]/[8]/[9]` remain **not visually reviewed**
  (see D-13).

Build photos — `unsorted_stl_raw/RC-01 Revision 1.1/Photos to help installation/`
(**25** JPEGs, Dec 2024, the designer's own Rev-1.1-era build in **McLaren MCL38 papaya**
livery — geometry reference, not our livery; count corrected in Session 1.5 — the folder
holds 25, not 24; `ASSEMBLY_NOTES.md` carries the same off-by-one). **16 of 25 viewed in
Session 1** (key ones re-verified in Session 1.5); the 9 unviewed are redundant
finished-car beauty shots (two outdoor-track sessions). The body-off internal shots
(`…54 (1)`, `…54 (4)/(5)/(6)`, `…55`, `…55 (1)/(3)/(5)`, `…56`) carried essentially all
the packaging evidence.

> ⚠ **Configuration caveat (added Session 1.5).** The photographed build runs the
> **Rev-1.1 direct front-facing steering** — the servo drops into the front-floor hole
> (1.1 Steering README) with a front-mounted FPV camera on the same printed housing.
> **Our locked config uses the original steering**: the servo sits **mid-chassis in
> `Servoholder` on the rear floor** (drawing `[2]`) driving a long rod forward to the
> servo-saver. Photo-derived front-bay occupancy must NOT be transferred to our build
> unchanged — our front bay loses the servo box but our **central zone gains it** (KO-19).

### 1.3 Independent computation (this session)
Read-only STL probe (pure-Python vertex parse + vertical-ray ceiling probe + triangle
binning) over the raw shells/floor. Used to (a) **verify** CSV bounding boxes and
(b) characterise the body-shell interior cavity. Script kept in the session scratchpad,
**not** added to the repo.

---

## 2. The vehicle architecture (what we are packaging into)

**CONFIRMED (drawings `[0]`–`[3]` + photos).** The RC-01 is a 1/10 open-wheel F1 layout:

- A **flat printed floor** is the structural spine and the mounting datum for everything.
  It is assembled from: `2023NewFrontFloorLargerParts` (**182 × 137 × 8 mm**,
  length×width×thick — DERIVED bbox, reproduced this session), `2023NewBackFloorLargerParts`
  (**117 × 137 × 8 mm**), `2023NewBackFloorLargerPart2` (**74.5 × 68 × 8 mm**, the
  *bendable* diffuser tail — a thin metal rod through a hole lets it flex), `FloorBoard2`
  (**112 × 19 × 2 mm** centre strip), `Diffuser` (**68 × 50 × 40 mm**) and side vents
  L/R (**35 × 37 × 20 mm** each). 12× M3 nuts drop into floor slots and are captured by
  M3 bolts (drawing `[2]`).
- The **front suspension + steering** is a self-contained module bolting to the *front*
  floor (drawing `[3]`): central tower `Suspension Block_10` (**37 × 37 × 71 mm**, tall)
  carrying the `servosaverv7` on top, printed lattice A-arms (`Arm4`,
  `Crossarm3_extended`, `2023WheelHubsSuspension5` + mirror upright), `Steering Block4`
  uprights, `GuideRod` pivot pins (hammer-tapped), 52 mm oil shocks, king-pins (~3 mm
  bore, TO CONFIRM). A **long steering push-rod runs along the floor centreline** from
  the steering servo — which in our locked config sits **mid-chassis, in `Servoholder`
  on the rear floor part** (drawing `[2]`; corrected in Session 1.5 from "mid/front") —
  forward to the servo-saver ("mount this hole with a rod to the steering servo motor").
- The **rear axle + drivetrain** sits at the back of the floor (drawings `[2]`/`[7]`,
  photos `…54 (5)/(6)`): a **transverse** rear axle in bearing carriers, a **spur + belt
  drive** to a **transverse motor**, `beltdrivemotorlock`, 14 mm metal axle sleeves
  (heat protection), and a **single central rear oil shock (68 mm)** mounted roughly
  along the centreline. The **rear wing mounts to the chassis rear stack** (spring-mount
  tower), *not* to the body — with a DRS-servo pocket + metal-rod linkage designed in
  from the start (drawing `[2]`: "Insert small DRS Servo here (optional)").
- The **body** is a lift-off **clamshell**: `NEW BODY 2024 FRONT 1` (**161 × 129 × 54 mm**)
  + `NEW BODY 2024 REAR` (**156 × 127 × 73 mm**) + separate `FRONTNOSE2024`
  (**129 × 42 × 128 mm**) + `2024 Revised Front Wing` (**72 × 181 × 28 mm**) + `new halo
  2.1` (**75 × 39 × 25 mm**) + mirror + `camera top 1.1` (**16.7 × 17.7 × 6.9 mm**).
  Panels bolt together with slot-captured M3s (**12× per drawing `[1]` — which covers the
  2023-era body; the 2024 shell's own panel-bolt count is unverified**, corrected Session
  1.5), and the whole shell attaches to the chassis with **only 3 × M3** (1 nose→front
  floor, 2 front-floor→front body; 2024-body README) into tight self-threading holes.

**Implication.** Usable internal volume is essentially **the open space on top of the
flat floor, under the clamshell, minus the driver figure and minus the mechanicals that
already live there.** There is no enclosed "tub" or bay printed into the design.

---

## 3. Original assembly order & dependencies (CONFIRMED from drawings/photos)

The stock build order (which our print order in `BUILD_SHEET.md` mirrors):
1. **Floor** assembled first (front + rear + rear-2 + floorboard + side vents + diffuser),
   M3 nuts seated in slots. It is the datum.
2. **Rear axle / drivetrain** built onto the rear of the floor (axle → bearings in
   carriers → spur/pinion/belt → motor lock → central 68 mm shock into spring mount →
   rear wing + DRS onto the tower).
3. **Front suspension** module bolts to the front floor; king-pins and guide-rods are
   *tapped in* (drawing `[3]` — "insert gently, tap lightly with a hammer"); steering
   servo + long rod + tie-rods/turnbuckles set after.
4. **Electronics** dropped onto the open floor and wired (photos) — **this is the step
   with no printed structure**: in the reference build everything is zip-tied/taped to
   the bare floor.
5. **Body** clamshell assembled, then lowered over the whole car and fixed with 3× M3.

**Hard assembly dependencies (order cannot be freely reordered):**
- Guide-rods / king-pins are **press/tap fits** → they must go in before the surrounding
  structure closes around them; hard to service later (see §5).
- The **central rear shock and the drivetrain occupy the centre-rear spine first**;
  electronics are packed *around* them, so electronics packaging is **constrained by,
  and downstream of, the mechanical build** — you cannot design the electronics tray
  without the mechanicals placed.
- The **body goes on last** and comes off first for any service — but it is retained by
  only 3 self-threading M3 into PLA (a wear point; see E and `ASSEMBLY_NOTES.md`
  plastic-thread rule).

**Additional dependencies (added Session 1.5):**
- **Steering servo must be powered and centred in firmware BEFORE the long rod/linkage
  is attached** (`ASSEMBLY_NOTES.md` stage 3) — i.e. a partial electronics bring-up is a
  prerequisite of finishing the *mechanical* steering, not a later layer.
- **The full electronics set must be bench-verified before it is buried under the shell**
  (v2 build sequence step 3: "verify before it's buried") — plan a powered, body-off
  test state into the assembly order.
- **The rear brake-light LED tail must be routed before the rear stack closes** — on the
  Rev-1 path drawing `[7]` provides a designed "Pass LED here (optional)" channel through
  the Light-Cover area; on the original path an equivalent route must be found. Retrofit
  after the drivetrain is assembled means partial rear teardown.

---

## 4. Original build vs planned W17 electronics — the central difference

**CONFIRMED.** The gap between what the RC-01 was designed to carry and what we intend to
carry is the single most important finding of this session.

| | Original design (Ryan `Parts List.txt`) | Planned W17 (BOM v2) |
|---|---|---|
| Receiver/brain | **1×** Dumbo-RC X6 (RX+ESC-driver in one) | **RP1 ELRS RX + 2× ESP32-WROOM DevKit** (control + sound/light) |
| ESC | 10BL60 | 10BL120 (larger) + its cooling fan |
| Motor | 3650 3900 KV (~Ø36 × 50 mm) | Rocket 540 V3 sensored (~Ø36 × 53 mm + sensor lead) |
| Servos | **1** (steering) | **4** (steering DS3235SG + pan + tilt + DRS MG90S) |
| FPV / video | none | **camera board + USB WiFi module + 2× antenna + blower + duct** |
| Audio | none | **MAX98357A amp + 4 Ω speaker** |
| Lighting | none | **WS2812 strip** (brake + halo) |
| Power | 1 BEC (in RX) | **2× UBEC (Rail A clean + Rail B servo)** + XT60 Y-split + 1000 µF caps |
| Sensors | none | **A3144 Hall + magnet + 27k/10k voltage divider** |
| Battery | **115 × 35 × 24 mm** (long) | **≤ 75 × 45 × 25 mm** (2024-body limit — shorter, fatter) |

**Reading.** We are inserting **~3–4× the component count** — and an entirely new *video*
+ *audio* + *dual-processor* + *4-servo* subsystem — into the **same or a smaller** open
volume, whose battery pocket is *shorter* than the original. The original electronics
already crowd the centre spine (see §5). This is the packaging problem stated plainly.

The intended placement (from `docs/00_BUILD_SHEET_v2.md` "Where it packs") is:
battery → central floor tub; **2× ESP32 → engine-cover / airbox spine**; both UBECs +
amp + RX → sidepod pockets; camera + WiFi module + blower + duct → nose/airbox; speaker
→ a sidepod; Hall → at the rear axle. **None of these pockets exist as printed parts** —
they are, at present, an *intent*, not a design (see §6, E-01).

---

## 5. Photographic findings — the reference build internals

From the body-off photos (McLaren-liveried Rev-1.1 build; geometry only):

- **`…54 (1)` (top-down, body off) — the key image.** All electronics sit on the **open
  top of the flat floor along the centreline**, between the front suspension tower and
  the rear motor. Even the *minimal* original set (single RX + ESC + one servo + battery
  + one small fan + a front FPV camera) produces a **dense rat's-nest of wiring** down
  the centre spine. CONFIRMED: there is no tray; components are cable-tied/taped to bare
  floor. (Re-verified Session 1.5.)
- **`…54 (5)/(6)` (rear close-ups).** The **motor + belt/spur** dominate the rear
  (transverse). The **central 68 mm-class shock lies roughly along the centreline in the
  middle of the car — precisely where the electronics want to go.** The ESC and its
  round cooling fan sit mid-chassis. A T-plug (Deans) battery lead and a LiPo pack sit on
  the centreline ahead of the motor. CONFIRMED spatial conflict between the central rear
  damper and the electronics zone.
- **`…55`, `…55 (1)/(3)/(5)` (front).** Printed **lattice A-arms** (triangulated — look
  robust); a **large steering servo dropped into the front floor just aft of the front
  tower** — ⚠ this is the **Rev-1.1 direct-steering install, NOT our layout** (Session
  1.5: our servo sits mid-chassis in `Servoholder`; see §1.2 caveat) — with a
  front-facing FPV camera on the same printed housing; **a power switch mounted on the
  front floor** (re-verified 1.5); wide front track with the wheels cantilevered well
  outboard on the arms; blue-anodised turnbuckles/ball-joints on the steering links.
- **`…56` (body-off ¾).** The **entire top body + nose lifts off as a clamshell** to
  expose the whole car — good for service access, but the shell sits *close* over the
  motor/shock/wiring; head-clearance between the top of the electronics stack and the
  underside of the roof is small.
- **Finished-car shots (`…53`, `…54`, `…54 (2)`, `17.14.*`).** Confirm overall
  proportions and that the body fully encloses the electronics; no internal detail.

---

## 6. Usable-space observations (from geometry + photos)

**Cavity probe — body shells (ESTIMATED; single-shell, authored frame, outer-roof
envelope minus 1.2 mm wall, floor = shell zmin, ignores ribs/bosses and ignores the
mechanicals already occupying the spine). Cross-checks `FIRST_PRINT_DECISION.md §7`;
independently re-derived in Session 1.5 (fresh script, 2 mm grid) — headline numbers
reproduced.**

> ⚠ **Vertical datum (made explicit in Session 1.5).** All "ceiling" heights are
> measured above the **shell's own bottom edge**, NOT above the chassis floor top. The
> shell's lower edge overlaps the floor by an unknown amount when assembled, and the
> floor itself is 8 mm thick — so **usable height above the floor top will be smaller**
> than every number below. The body↔floor vertical registration is unmeasured until the
> D-01 slicer assembly.

- **`NEW BODY 2024 REAR` shell:** a **wide but mostly shallow** bay — interior width up
  to ~**120 mm** and ceiling up to ~**72 mm** over the forward ~100 mm of its length; but
  the region that is **≥ 45 mm tall is only ~18–36 mm wide** (1.5 re-probe: 14–40 mm — a
  narrow central channel, i.e. the airbox spine). **Marginal, not "consistent", for the
  ESP32 airbox-stack plan** (downgraded Session 1.5): a DevKit with Dupont pins is a
  ~44 mm-wide install envelope (B, CTL-E1) vs a 14–40 mm-wide tall channel — pins must
  exit fore-aft / be soldered low-profile, or the stack sits lower where the bay widens.
  Resolve at D-02/D-04.
- **`NEW BODY 2024 FRONT 1` shell:** **shallower** — ceiling ~**42–53 mm**; the ≥ 45 mm-
  tall region is only ~**34 mm long × ~39 mm wide** at the cockpit hump (1.5 re-probe
  found the ≥45 mm band even narrower, ~18 mm — treat the smaller number as the planning
  bound). The rest of the shell tapers low toward its forward end.
- **The separate nose cone `FRONTNOSE2024` was NOT probed** (correction Session 1.5):
  it is authored standing on end (129 × 42 × 128 bbox, long axis vertical), so the
  vertical-ray roof method does not apply to it, and Session 1's "nose ~18–35 mm"
  figures describe the **front shell's forward taper only**. The true nose cone is a
  slender ~129 mm cone with outer cross-section ≤ ~42 mm — its interior is **TO MEASURE**
  (D-25) before any "camera/WiFi in the nose" layout is drawn.
- **Tallest usable volume is at the FRONT-of-REAR / shell junction** — matching the v2
  "central floor tub" battery location and the ≤ 75 × 45 × 25 mm envelope.

**These numbers are a gross upper bound.** They describe the *empty shell*. The photos
show the central rear shock, the drivetrain, the steering rod and the wire loom already
consuming much of that channel, so **net electronics volume is materially smaller than
the geometry suggests** and cannot be quantified without the mechanicals placed (Session
2 slicer-assembly or physical dry-fit — D-01/D-02).

**Cavities that only *appear* usable but are blocked:**
- The tall central channel of the rear shell → occupied by the **central rear shock
  travel** + rear drivetrain + wiring.
- The front floor centreline → occupied by the **long steering push-rod** (a *moving*
  keep-out) and the front tower.
- The sidepods (planned for UBEC/amp/RX/speaker) → their true internal clearance is
  **unmeasured** (the shells were probed on the centreline; the sidepod pockets are
  narrow and were not resolved — TO MEASURE, D-03).
- The nose → the front shell tapers **low** toward its forward end (~18–35 mm), and the
  actual nose cone (`FRONTNOSE2024`) is unprobed and slender (see above); camera + WiFi
  + blower "in the nose/airbox" needs the nose interior measured (D-25) AND the real
  camera board measured (Gate C, D-06). The nose is also the **primary crash zone**
  (E-24, added Session 1.5) — front-mounting the dearest electronics is a risk decision,
  not just a fit question.

---

## 7. Inaccessible / hard-to-service areas (CONFIRMED / DERIVED)

- **Guide-rods & king-pins** — tap/press fits; effectively not serviceable without
  partial front-end teardown.
- **Anything under the drivetrain / behind the motor** — buried by the spur/belt/motor
  and the central shock; the Hall sensor + axle magnet at the rear axle are in a
  congested, hot pocket.
- **Battery** — if it lives in the central tub under the clamshell, swapping it needs the
  **body off** (3× M3) each time. For a "swap 2 packs for runtime" plan (v2), that is a
  repeated body-removal cycle on 3 self-threading PLA bosses → **thread-wear risk**
  (E-08); heat-set inserts strongly indicated.
- **USB / programming access** for the 2× ESP32 and the camera console — **no service
  port exists** in the current body; today it would require body removal (E-09, D-11).
- **Camera** — if inside a duct/pod, removal-without-destroying-the-mount is a stated
  requirement not yet designed (`CAMERA_GIMBAL_PLACEMENT.md §2`; D-06/D-07).

---

## 8. Confidence summary of the main conclusions

| Conclusion | Confidence |
|---|---|
| RC-01 architecture, assembly order, floor-as-datum, clamshell body, 3× M3 mount | **CONFIRMED** (drawings + READMEs + photos; re-verified 1.5) |
| Central rear shock + drivetrain occupy the electronics spine | **CONFIRMED** (photos `…54 (5)/(6)`; re-verified 1.5) |
| Steering servo sits **mid-chassis** (`Servoholder`, rear floor) in our config | **CONFIRMED** (drawing `[2]`; added 1.5 — photos show the Rev-1.1 *front* servo instead) |
| Planned electronics ≈ 3–4× original count into same/smaller volume | **CONFIRMED** (Parts List vs BOM v2; re-verified 1.5) |
| No printed mounts/trays exist for the new electronics | **CONFIRMED** (MODEL_INVENTORY — only `Servoholder` + DRS pocket) |
| STL bounding boxes in the CSV | **CONFIRMED** (independently reproduced in Session 1 AND again in 1.5) |
| Body-shell interior cavity figures | **ESTIMATED** (single-shell probe; upper bound; datum = shell bottom edge, not floor top) |
| ESP32 stack fits the tall airbox channel | **ESTIMATED — marginal** (channel 14–40 mm vs ~44 mm pin envelope; D-02/D-04) |
| Battery ≤ 75 × 45 × 25 fits width/height near junction | **ESTIMATED** (mesh probe; length + bosses unproven) |
| Nose-cone (`FRONTNOSE2024`) interior | **TO MEASURE** (D-25 — never probed; authored on end) |
| Sidepod internal clearances (UBEC/amp/RX/speaker) | **TO MEASURE** |
| Real camera/blower envelopes | **TO MEASURE** (Gate C) |
| WiFi-module possession ("on hand") | **UNCONFIRMED** (downgraded 1.5 — only the camera is documented on hand) |
| Gate-A rear stack seats *and articulates* the 68 mm shock | **TO MEASURE** (BLOCKER) |
