# F · Input Brief for Session 2 (Assembly Architecture)

Session 1 · 2026-07-17. This is the hand-off. Session 2 designs the assembly
architecture; it should **rely on Reports A–E** and not re-run the investigation.
Confidence tags per [`README.md`](README.md).

---

## 1. Zones — confirmed / provisional / prohibited

**Confirmed usable (with stated caveats):**
- **Z3 Central tub / shell junction** — the **best** volume: ceiling to ~72 mm, width to
  ~120 mm; the primary home for the **battery (low)** and an **airbox-spine electronics
  stack (tall, narrow ~14–40 mm — marginal for an ESP32 + Dupont-pin envelope of
  ~44 mm; pin orientation must be solved, A §6)**. *Caveats (1.5):* net of KO-06 central
  shock + **KO-19 steering-servo body (DS3235SG sits mid-chassis in `Servoholder` —
  NOT at the front as the reference photos suggest)** + loom; and all ceiling figures
  are measured above the **shell bottom edge**, not the floor top — subtract the
  (unmeasured, D-01) body↔floor overlap before trusting any height.
- **Floor top surface** as the universal mounting datum (flat, 8 mm, M3-slotted).

**Provisional usable (needs a measurement first):**
- **Z1 Nose** — the probe numbers (~18–35 mm) cover only the **front-shell taper**; the
  actual nose cone `FRONTNOSE2024` is slender and **unprobed** (1.5) — camera/WiFi "in
  nose" only after D-25 (nose interior) + D-06 (real camera), and note it is the
  **primary crash zone** (E-24).
- **Z2 Front bay** — shallow (~42–53 mm), and **contested** by the steering rod (KO-01)
  + tower (KO-05). (1.5: the big steering servo is NOT here in our config — it sits
  mid-chassis, KO-19.)
- **Z4 Sidepods L/R** — planned for UBEC/amp/RX/speaker but **internal clearance
  unmeasured** (D-03).
- **Z8 Camera/gimbal** — cockpit (A) vs halo-pod (B) is an **open decision**
  (`CAMERA_GIMBAL_PLACEMENT.md`), not for Session 2 to *close* mechanically until the
  occlusion check + D-06/D-07.

**Prohibited (do not place electronics):**
- **Z6 Rear drivetrain** (axle/spur/belt/motor — mechanical + hot, KO-08/09).
- **Z5 Rear spine centreline within the 68 mm shock stroke band** (KO-06).
- **Front centreline within the steering-rod sweep** (KO-01).
- **Any wheel/tyre envelope** (Ø64 tyres + steer + bump, KO-03/10) and **suspension
  travel arcs** (KO-04).

---

## 2. Components

**Mandatory onboard (must be placed — Report B):** battery; motor; ESC (+fan); steering
servo DS3235SG; 3× MG90S (pan/tilt/DRS); 2× ESP32 (control + sound/light); ELRS RP1 RX;
camera board; WiFi module (+28×28×3 heatsink); 2× 5.8 GHz antenna; MAX98357A amp;
speaker; WS2812 strip; 2× UBEC; XT60 Y-split; 1000 µF cap(s); A3144 Hall + magnet;
voltage divider; blower + duct; the wiring harness (its bulk is a first-class component).

**Optional / deferrable:** power switch; BX100 buzzer; spare ESP32; future-expansion
reserve; cosmetic driver figure/helmet/wall mount/sharkfin/side-wing deco. (1.5: the
driver figure and cockpit-camera Option A are mutually exclusive — Z8 note.)

**Undecided protection/disconnect (added 1.5):** BOM v2 contains **no fuse or main-line
protection**, and the power switch is undecided — today the XT60 unplug is the only
disconnect. Session 2 must place an explicit decision (keep the deliberate omission, or
add fuse/switch), not silently assume one (B: PWR-PROT/SW-PWR).

**Unknown envelopes (block a complete space plan until measured):** camera, WiFi module
(**possession unconfirmed** — verify before counting on D-06b "now", 1.5), ESC,
DS3235SG, MG90S, speaker, UBECs, caps, blower, harness bulk (see D-06…D-10).

---

## 3. Critical measurements before final CAD (from Report D)

Start-now (hardware on hand / slicer): **D-06** camera, **D-06b** WiFi module (**only
once confirmed in hand** — 1.5), **D-13** read drawings [4]/[6]/[8]/[9], **D-14/D-15/
D-17** Gate A + rear wing (slicer + diagnostic TP), **D-01/02/03/04/11** slicer-assembly
+ dummy-block dry-fit, **D-05/D-22** bore/seat, **D-25** nose-cone interior sections (1.5).

On-arrival / powered: **D-08** ESC, **D-09** servos, **D-12** front shock, **D-16** spur
bolt pattern, **D-19** thermal (incl. UBECs), **D-20** RF, **D-21** CG, **D-23**
adapters, **D-24** rail-current budget (1.5). **D-18** gimbal hard-stops is additionally
gated behind firmware A2 + Phase B.

---

## 4. Architecture requirements Session 2 must honour

1. **Design the electronics mounts *around* the placed mechanicals**, not the reverse —
   the central shock, drivetrain and steering rod are fixed keep-outs (C).
2. **Keep the battery low and central**; hold the **≤ 75 × 45 × 25 mm** envelope; make it
   **serviceable without stripping the 3× M3 body bosses** (heat-set inserts, or a
   battery-access path that doesn't require full body-off) (E-04, E-08).
3. **Two-rail electrical discipline is physical, not just schematic** — route Rail A
   (clean: camera/WiFi/ESP/RX/LED) physically apart from Rail B (servos/blower); keep the
   ESC/motor noise and heat away from the camera rail; **isolate the ESC's internal BEC
   +5 V (red) wire so the UBECs own the rails** (BOM bench note, carried in 1.5); and
   **budget both rails against their 5 A UBECs** before the final harness (D-24, E-23).
4. **RF separation** — ELRS 2.4 GHz and WiFi 5.8 GHz antennas apart from each other and
   clear of metal (motor, sleeves, shock, axle). Body is PLA/PETG = RF-transparent (use
   it).
5. **Thermal** — ASA rear + 14 mm metal sleeves (mandatory); ducted airflow for the
   camera and WiFi module; vents front-in / rear-out; don't trap heat in a closed pocket.
6. **Service access** — plan for USB/programming reach (2× ESP32 + camera), camera
   removal without destroying the mount, and strain relief across every moving axis.
7. **VR/gimbal** — camera mount must give roll alignment (or trim), boresight = straight
   ahead, stiffness, and **measurable hard-stops** for the firmware safety gate.
8. **Firmware safety boundaries are non-negotiable** (workspace `CLAUDE.md`): no
   iPhone→control path; gimbal is stick-driven CRSF ch9/10 only; W3 head-tracking is
   log-only. The mount only has to make the geometry measurable — it must not assume any
   active-pan/tilt authorisation.

---

## 5. Decisions Session 2 MAY make

- The **electronics mount/tray architecture** (what carries the ESP32 stack, UBECs, RX,
  amp, WiFi module, blower) — provided it is validated by a **dummy-block dry-fit** first.
- **Battery location + retention** within Z3 (after D-01).
- **Cable-channel / strain-relief / tie-down** scheme.
- Which **Gate-A rear-stack path** to adopt **once D-14/D-15 are done** (slicer +
  diagnostic TP evidence), and the coupled **rear-wing/DRS** choice (D-17).
- **Sidepod pocket** usage (after D-03).
- A **USB/service-access** provision in the body.

## 6. Decisions Session 2 MUST NOT make yet

- **Do not finalise the battery pack purchase** before D-01 (bay length + bosses).
- **Do not production-print the ASA rear group** before Gate A closes (D-14/D-15).
- **Do not production-print the rear wing/DRS** before the combined Gate-B check (D-17).
- **Do not design the camera mount/duct from assumed dimensions** — only from D-06 real
  measurements (Gate C).
- **Do not close the camera *placement* decision (Option A vs B)** on mechanical grounds
  before the halo-occlusion check + D-06/D-07 (owner call, per
  `CAMERA_GIMBAL_PLACEMENT.md`).
- **Do not set gimbal servo endpoints / assume active pan-tilt** — that is firmware-side,
  gated behind A2 + Phase B (D-18).
- **Do not reopen resolved decisions** (Gate B front nose+wing REQUIRED; Gate D
  `Servoholder`; original oil-shock chassis; belt drive; 2024 body/W17 livery) — they
  remain valid (see the decision audit below).

---

## 7. Decision audit — what remains valid vs needs validation

| Decision | Source | Status | Still compatible w/ assembly? | Needs physical validation? |
|---|---|---|---|---|
| OpenRC RC-01, original oil-shock chassis (not Rev-1.1 steering/floor) | BUILD_SHEET | **valid** | yes | no |
| Belt drive (original solution), `beltdrivemotorlock` primary | BUILD_SHEET | **valid** | yes | spur↔pulley (D-16) |
| 2024 body painted W17 #63 | BUILD_SHEET | **valid** | yes | no |
| Gate B front: `FRONTNOSE2024` + `2024 Revised Front Wing` REQUIRED | MODEL_INVENTORY (drw `[5]`) | **valid** | yes | slicer visual confirm |
| Gate D: `Servoholder` on rear floor | MODEL_INVENTORY (drw `[2]/[3]`) | **valid** | yes | DS3235SG fit (D-09) |
| Battery ≤ 75 × 45 × 25 mm | 2024-body README | **valid** | yes | bay length (D-01) |
| Rear shock **68 mm** confirmed | GENERAL_PLAN | **valid** | **gated** | Gate A articulation (D-14) |
| Rear wing = 2021 w/ DRS (preferred) | user 2026-07-10 | **directional** | **gated** | combined fit (D-17) |
| Rear stack path (original vs Rev-1) | — | **OPEN** | ? | **Gate A (D-14/D-15)** |
| Camera integration + placement | CAMERA_GIMBAL_PLACEMENT | **OPEN (research/design)** | ? | D-06/D-07 (owner call) |
| DRS reinstated (MG90S, CH6) | BOM v2 | **valid** | yes | DRS pocket fit |
| Electronics packing plan ("where it packs") | BUILD_SHEET_v2 | **intent only — no printed mounts exist** | **UNPROVEN** | **the central open question (E-01/02/03)** |

---

## 8. The one thing to carry forward

The mechanics of the RC-01 are buildable and well-evidenced. **The unproven part is
whether our full electronics package physically fits and can be mounted in the open
centre volume that is already occupied by the central rear shock, the drivetrain and the
steering linkage — including the mid-chassis DS3235SG servo body (KO-19, added 1.5) —
with no printed mounts yet designed for any of it.** Session 2 should
open with the **dummy-block dry-fit (D-01/02/03/04)** and the **Gate-A slicer/TP wave
(D-14/D-15/D-17)**, because those two studies convert the biggest unknowns into facts
before any architecture is committed.
