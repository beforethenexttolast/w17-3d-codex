# G · Session 1.5 — Skeptical Review Findings & Readiness Decision

Session 1.5 · 2026-07-17 · independent review-and-correction pass over the Session 1
evidence package (Reports A–F). Method: every load-bearing claim traced back to its
primary source — supplier drawings `[1] [2] [3] [7]` re-viewed page-by-page, key
body-off photos re-viewed, all 8 supplier READMEs + Parts List re-read, CSV bounding
boxes re-checked against Session 1's numbers, and the body-shell cavity probe
**independently re-implemented** (fresh script, 2 mm grid) since Session 1's script was
not kept. Corrections were applied **in place** in Reports A–F, each tagged "(1.5)".

## What was independently re-verified and held up

- All quoted STL bounding boxes (floors, shells, nose, wing, halo, camera pod,
  Servoholder, spring mounts, DRS arms, axle holders) match `01_inventory/inventory.csv`
  and the raw files.
- Drawing `[2]`: 12× M3 floor nuts, Servo Holder as a floor part, rear wing on the
  chassis spring-mount tower, DRS servo pocket + metal-rod linkage, bendable rear floor
  2. Drawing `[3]`: rod-to-servo-saver steering, hammer-tapped guide rods. Drawing
  `[7]`: bearings seat in the Motor Covers, wing/diffuser/backplate M3 stack, M4
  through-tyreslot wheel retention, "Pass LED here" channel, Light Cover identity
  question. Drawing `[1]`: 12× M3 slot-nut body assembly (2023-era body).
- 2024-body README: 3× M3 chassis mount (1 nose→front floor, 2 front floor→front body),
  ≤75×45×25 mm battery limit, 2S 1300–1500 mAh. Ryan's Parts List: original electronics
  set, 115×35×24 battery, 51 mm front shocks (the D-12 discrepancy is real), 14 mm-ID
  heat-protection sleeves.
- Photos `…54 (1)/(5)/(6)`, `…55`, `…56`: central shock + drivetrain congestion,
  ESC+fan mid-chassis, T-plug battery on the spine, zip-tie/tape mounting, front-floor
  power switch, one-piece clamshell lift-off — all as Session 1 described.
- Rear-shell cavity numbers reproduced within ~2 mm (ceiling ~72, interior width ~120,
  narrow tall channel). Session 1's ESTIMATED tag and "gross upper bound" framing were
  honest and correct.

## Findings register

| ID | Severity | Doc | Subsystem | Finding | Evidence | Consequence | Correction | Remaining validation | Status |
|---|---|---|---|---|---|---|---|---|---|
| R-01 | **HIGH** | A §2/§5, C Z2/Z3/KO-01/KO-11, F §1 | steering / packaging | Session 1 placed the steering servo "mid/front" and Z2 listed it as a front-bay occupant — but the **reference photos show the Rev-1.1 direct front-facing servo, which is NOT our config**; drawing `[2]` puts `Servoholder` (and therefore the DS3235SG body) **mid-chassis on the rear floor**, inside the prime Z3/Z5 electronics/battery zone | drawing `[2]` (re-viewed); 1.1 Steering README ("slide the servo in the front floor hole" = the *new* method); photo `…55` | central-zone volume was over-counted; a ~40×20×40 servo + holder + horn sweep was missing from the zone the battery and airbox stack target | A §1.2 caveat + §2/§5 fixes; **new KO-19**; Z2/Z3 verdicts fixed; KO-01/KO-11 locations fixed; F §1/§8 updated | servo placement enters the D-02 dummy dry-fit; DS3235SG fit D-09 | CORRECTED |
| R-02 | **HIGH** | A §6, C Z1, F §1 | video / packaging | **The nose cone `FRONTNOSE2024` was never probed** — it is authored on end (129×42×128), so the vertical-ray roof method silently produced nothing for it; Session 1's "nose ~18–35 mm" figures describe the front-shell taper, yet Z1 cited "PROBE" as evidence for the *nose* zone | 1.5 re-probe (nose bbox orientation); A §6 text | "camera/WiFi in the nose" could have been laid out against numbers that describe a different part | A §6 correction; Z1 rewritten; **new D-25** (slicer nose sections); **new E-24** (nose = crash zone) | D-25 + D-06 before any nose layout; placement stays an owner call | CORRECTED |
| R-03 | **HIGH** | B §B.2, E, F §4 | electrical | **No per-rail current budget existed**, and the WS2812 row understated worst-case draw ~3× ("up to ~0.6 A" vs ~1.8 A full-white for 30 LEDs @ ~60 mA/LED); Rail A and Rail B worst-case sums can each approach/exceed their 5 A UBECs | BOM v2 (5 A UBECs, rail assignments); WS2812B datasheet-typical 60 mA/LED | undetected brown-out risk: video/control loss (Rail A) or steering glitches (Rail B) discovered only on the car | LGT-LED row corrected; B.2 rail-budget note; **new E-23**; **new D-24**; F §4.3 extended | D-24 bench measurement at peak load | CORRECTED |
| R-04 | MEDIUM | B §B.1/B.4, D-06b, F §2/§3 | video / process | **WiFi-module "on hand" status is unsupported**: only the camera is documented on hand (`FIRST_PRINT_DECISION.md §2`); the module is an ordered AliExpress line and absent from the 2026-07-17 delivery note (`GENERAL_PLAN.md` item 5) | BOM §1; FIRST_PRINT_DECISION §2; GENERAL_PLAN item 5 | D-06b was presented as start-now work; a session could be planned around measuring a part that isn't there | status downgraded to UNCONFIRMED in B/D/F; A §8 row added | physically verify possession; then D-06b | CORRECTED (verify) |
| R-05 | MEDIUM | A §6, F §1 | packaging | "Consistent with the plan to stack the ESP32s in the airbox" was **too confident**: the ≥45 mm-tall channel is ~14–40 mm wide (1.5 re-probe) vs a ~44 mm ESP32+Dupont install envelope (B, CTL-E1) | 1.5 re-probe; B CTL-E1 envelope | Session 2 could commit to a vertical airbox stack that doesn't fit with normal pin exits | downgraded to "marginal"; pin-orientation constraint stated in A §6 + F §1 | D-02 net-volume dry-fit + D-04 roof clearance | CORRECTED |
| R-06 | MEDIUM | A §6, C header, F §1 | dimensional integrity | **Vertical datum unstated**: all shell "ceiling" figures are measured above the shell's own bottom edge; body↔floor overlap is unmeasured and the floor is 8 mm thick — usable height above the floor top is smaller than every quoted number | probe method (both Session 1's description and the 1.5 re-implementation); FIRST_PRINT_DECISION §7 carried the caveat, C/F dropped it | height-driven decisions (battery 25 mm, stack height, KO-14) could consume phantom headroom | explicit datum warnings added to A §6, C header, F §1 | D-01 slicer assembly fixes the true datum | CORRECTED |
| R-07 | MEDIUM | B, E, F §2 | electrical / safety | **No fuse / main-disconnect anywhere in the component register or BOM**, and the power switch was "optional / TO DECIDE" with no forcing function — the XT60 unplug is the only disconnect on a 2S pack feeding a dense loom | BOM v2 (absence); reference build has a front-floor switch (photo `…55`) | a short in the loom has no protection; the omission was invisible rather than decided | **new PWR-PROT row** in B; F §2 "undecided protection/disconnect" block | Session 2 places the explicit decision | CORRECTED (decision open) |
| R-08 | MEDIUM | A §2 | body / fasteners | "Panels bolt together (12× M3)" was attributed to the 2024-body README — actually the **12× M3 slot-nut pattern is drawing `[1]`, the 2023-era body**; the 2024 shell's own panel-bolt count is undocumented | drawing `[1]` (re-viewed); 2024-body README (says only 3× M3 chassis mount) | KO-15 fastener-access planning could assume an unverified count | A §2 re-attributed and flagged unverified | count the 2024 panel bolts at the slicer visual confirm | CORRECTED |
| R-09 | LOW | A §3 | assembly order | Three dependencies missing: servo must be **powered+centred before the steering linkage** closes; the electronics set must be **bench-verified before burial** under the shell; the **rear LED tail must be routed before the rear stack closes** (drawing `[7]` "Pass LED here" channel on the Rev-1 path) | ASSEMBLY_NOTES stage 3; v2 build sequence step 3; drawing `[7]` | retrofit teardowns discovered at assembly time | added to A §3 "Additional dependencies"; LGT-LED row updated | — | CORRECTED |
| R-10 | LOW | B PWR-BAT | power | "×2 owned" was wrong — no battery has been bought (deliberately last; BOM §D "sourced locally", GENERAL_PLAN item 5 "battery not final") | GENERAL_PLAN; FIRST_PRINT_DECISION §2 | a reader could believe the pack dimension risk is closed | corrected to "×2 planned" | E-04 / D-01 unchanged | CORRECTED |
| R-11 | LOW | A §1.2 | evidence bookkeeping | Photo count wrong: the folder holds **25** JPEGs, not 24 (16 viewed → 9 unviewed, not 8). `ASSEMBLY_NOTES.md` carries the same pre-existing off-by-one (left as-is — pre-Session-1 doc) | `ls` of the photos folder | minor — undercounts unviewed evidence | corrected in A §1.2 | none | CORRECTED |
| R-12 | LOW | C KO-01/KO-04 | suspension / steering | Wording defects: KO-01 said the rod runs "front-servo→saver"; KO-04 called 52 mm a "stroke" (it is eye-to-eye) | drawings `[2]`/`[3]`; BOM §10 | keep-out bands mis-sized if taken literally | both fixed | lock-to-lock / travel dry-fits unchanged | CORRECTED |
| R-13 | LOW | D-14 (supporting evidence) | rear stack / Gate A | New supporting evidence found (not recorded by Session 1): drawing `[7]`'s spring-lock note "**adjust as per size of rear spring**" implies the Rev-1 mount has designed-in adjustability — relevant to whether it can seat the 68 mm shock | drawing `[7]` (re-viewed 1.5) | none adverse — mildly de-risks Gate A; the articulation check stands | recorded here; Gate A scope unchanged (no gate reopened/closed) | D-14 slicer + diagnostic TP | NOTED |
| R-14 | EDITORIAL | B §B.4, C Z8, D-19 | cross-refs | B.4 pointed the WiFi row at D-06 (should be D-06b); driver figure vs cockpit-camera Option A mutual exclusion unnoted; UBEC self-heating absent from the D-19 thermal list | — | minor traceability gaps | all fixed | — | CORRECTED |

**Checked and found sound (no correction needed):** the decision audit in F §7 (no
resolved gate reopened, no open gate treated as closed — verified against
`GENERAL_PLAN.md`, `BUILD_SHEET.md`, `MODEL_INVENTORY.md`, `FIRST_PRINT_DECISION.md`);
the original-vs-planned electronics comparison (A §4) against Ryan's Parts List and BOM
v2; tyre/bearing/gear/shock key numbers; the E-01/E-02/E-03 core packaging finding; the
Z4 sidepods TO-MEASURE call; keep-outs KO-02…KO-10, KO-12…KO-18; the D-plan's
reference-point/tool/accuracy discipline; firmware safety boundaries in F §4.8.

---

## Session 2 readiness decision

### Verdict: **READY WITH RESTRICTIONS**

The Session 1 package is genuinely evidence-based — sources were actually read and
viewed, bounding boxes reproduce, confidence tags are mostly honest, and the central
finding (electronics packaging around the placed mechanicals is the open problem, with
no printed mounts existing) survives skeptical re-derivation intact. The defects found
were real but correctable in place; none invalidates the package's architecture-input
framing.

Session 2 **may begin** the assembly-architecture work (zone allocation, mount/tray
concepts, dummy-block dry-fit planning), with these named restrictions — each must stay
**provisional** until its listed evidence lands:

1. **Any height-driven layout** (battery 25 mm stack, airbox stack height, KO-14 roof
   clearance) — provisional until **D-01/D-02** establish the true floor-top↔shell
   datum (R-06).
2. **The ESP32 airbox-spine stack** — provisional until **D-02/D-04** confirm a ≥44 mm
   pin envelope (or a fore-aft/soldered alternative) actually passes the 14–40 mm tall
   channel (R-05).
3. **Central-zone allocation** — must place **KO-19 (DS3235SG mid-chassis)** from the
   start; validated in the **D-02 dummy dry-fit** with the servo (or a dummy) present
   (R-01).
4. **Camera placement** — no nose layout before **D-25 + D-06**, and the E-24 crash
   exposure enters the Option A/B decision, which remains an **owner call** (R-02).
5. **Electrical architecture** — harness/UBEC sizing provisional until **D-24**; the
   ESC-BEC isolation and the fuse/main-disconnect decision must appear explicitly in
   the Session 2 output (R-03, R-07).
6. **D-06b** only after WiFi-module possession is physically confirmed (R-04).
7. All pre-existing gates stand unchanged: **Gate A/B (D-14/D-15/D-17), Gate C, servo
   fit (D-09), battery purchase (D-01), gimbal endpoints (D-18, behind firmware
   A2 + Phase B)**.

Nothing on this list requires waiting to *start* Session 2: restrictions 1–3 are
resolvable inside Session 2's own opening move (the slicer-assembly + dummy-block
dry-fit that F §8 already prescribes), and 4–7 gate only their named sub-decisions.
