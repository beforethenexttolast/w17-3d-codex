# General Plan — raw STLs → finished W17

The execution roadmap for the whole 3D-printing/fabrication subproject. Phases run
roughly in order; 5–7 loop per part group. The original 21 Jul 2026 deadline is a
**soft target** (decision 2026-07-10) — quality and learning come first, but the
critical path is marked so effort lands where it matters.

**Critical path:** coupons → wheel fit test → rear gate (rocker) → mechanical groups →
body shell print → paint (the long pole — days of cure time) → assembly. Cosmetic
extras (driver figure, wall mount) are never on it.

**Inputs today:** 210 raw files classified in `MODEL_INVENTORY.md` (37 required /
5 optional / 16 gated), materials decided (`MATERIAL_DECISION_MATRIX.md`), X1C + AMS +
filament on hand, nothing printed yet.

---

## Phase 1 — Inventory & classification ✅ done on paper (2026-07-10)
- **Goal:** know what every raw file is and whether we print it.
- **Inputs:** `unsorted_stl_raw/`, docs v1/v2, Codex-repo reports (read-only cross-check).
- **Outputs:** `MODEL_INVENTORY.md`, `01_inventory/inventory.csv`, `09_rejected_or_uncertain/REVIEW.md`, `02_ready_to_slice/` + manifest.
- **Done criteria:** every file has tier/material/uncertainty + SHA-256; selected files staged with traceability. **Pending: Vitaliy reviews the inventory.**
- **Risks:** classification from filenames, not geometry — mitigated by Phase 2.

## Phase 2 — Model review & print-readiness checks
- **Goal:** visually confirm, in Bambu Studio, what Phase 1 only inferred.
- **Inputs:** `02_ready_to_slice/`, the four gates in `MODEL_INVENTORY.md`.
- **Actions:** open each group in the slicer; resolve **Gate A** (rocker vs 68 mm shock), **Gate B** (is the nose/wing integrated in the 2024 front shell?), **Gate D** (Servoholder); check every part for thin walls/errors (slicer will flag non-manifold meshes); mirror the front hub and verify it.
- **Outputs:** gates resolved → inventory + REVIEW.md updated; final part list frozen.
- **Human decisions:** all four gates are human calls (Claude can't see geometry).
- **Done criteria:** zero UNCERTAIN rows left except Gate C (camera measurement, blocked on hardware).
- **Risks:** a "required" part turns out wrong → back to inventory, not a crisis.

## Phase 3 — Material decisions ✅ done on paper (2026-07-10)
- **Outputs:** `MATERIAL_DECISION_MATRIX.md` (MD-001). **Pending: Vitaliy sign-off**, then per-group confirmation at first print. Changes go in the Decision log, never silently.

## Phase 4 — Bambu Studio slicing profiles
- **Goal:** working, saved profiles per part class.
- **Inputs:** `PRINT_SPEC.md` starting profiles.
- **Actions:** build the 4 real presets (body / PETG structural / ASA drivetrain / small-detail) in Bambu Studio, save each, note deltas in `03_print_profiles/`.
- **Done criteria:** profiles exist in the slicer AND are documented.
- **Risks:** HF PETG at full speed → weak parts (capped in spec); preset drift undocumented → always log.

## Phase 5 — Test prints
- **Goal:** de-risk every material + every critical fit before real parts.
- **Actions (order):** PLA coupon → PETG coupon (dry filament first) → ASA coupon (ventilation drill) → body-shell wall slice at 0.12 mm → wheel fit set (1 rim + 1 hub + 1 adapter). Log each as `TP-NNN` in `04_test_prints/`; measure with calipers per `BEGINNER_3D_PRINTING_GUIDE.md`.
- **Human decisions:** buy Tamiya tyres 54198 + 51400 (needed for the fit test); accept/adjust tolerances.
- **Done criteria:** all three materials produce clean coupons with measured shrinkage; bearing seats and tyre bead verified.
- **Risks:** ASA misbehaves → fallback path in MATERIAL_DECISION_MATRIX.md.

## Phase 6 — Fitment checks
- **Goal:** printed parts fit real hardware before batch printing.
- **Inputs:** test parts + hardware (bearings, tyres, shocks, axle, motor).
- **Actions:** bearing press-fit, tyre bead, shock mounts (Gate A outcome), axle/sleeve/spacer stack, king-pin 3 mm bore; record FIT entries; iterate one variable at a time.
- **Done criteria:** every critical interface has a FIT entry with verdict ✅.
- **Risks:** hardware not ordered in time (tyres/shocks) — order during Phase 4/5.

## Phase 7 — Full prints
- **Goal:** all 37 required parts printed to spec.
- **Actions:** batch by material per `BUILD_SHEET.md` print order (rear ASA → front PETG → floor → wheels ×4 → body 0.12 mm → diffuser); log every attempt (`P-NNN`); label every physical part; keep failed parts as tolerance references until the build ends.
- **Done criteria:** every required row in the inventory has a successful P-NNN; dry-fit assembly (no glue/paint) passes.
- **Risks:** the two big shells (10 h+ prints) fail late → print them when you can watch the first hour; a crash-prone part (wings) breaking later is *normal* — reprint capacity is the plan, not a failure.

## Phase 8 — Sanding & surface preparation
- **Goal:** body parts ready for primer; mechanical parts deburred.
- **Method:** `FINISHING_GUIDE.md` (grit ladder, per-material notes). Mask/protect all mechanical interfaces before any abrasive or primer work.
- **Done criteria:** body set primed and blemish-free at arm's length; FIN entries opened per part. **Safety: dust mask, wet-sand where possible.**

## Phase 9 — Painting & decals
- **Goal:** the W17 look: black base, Petronas teal accents, silver nose, #63.
- **Actions:** workflow (b) in `FINISHING_GUIDE.md`; decal design/sourcing is a **human task** (Inkscape from reference photos or purchased set); gloss clear → decals → final clear; cure fully before handling.
- **Human decisions:** exact teal shade (test card vs reference photos), decal source, gloss vs satin final.
- **Done criteria:** finished shells cured ≥ per-can spec, no paint on any interface.
- **Risks:** paint is the calendar long pole (multi-day cures) — start body prints early; paint-attacks-plastic accidents → always test on the Phase 5 wall slice.

## Phase 10 — Final assembly
- **Goal:** rolling, driving car with finished body.
- **Method:** `ASSEMBLY_NOTES.md` stages 1–6 with drawings `[0]`–`[9]`; electronics install is the firmware repos' domain — this project only guarantees the printed mounts fit.
- **Done criteria:** all stages checked; car rolls, suspension works, body mounts securely; ASM entries recorded.
- **Risks:** self-threading M3 bosses strip → heat-set inserts (bought optional, recommended).

## Phase 11 — Documentation & iteration (continuous)
- **Goal:** the knowledge base stays true after contact with reality.
- **Actions:** after every session: PRINT_LOG / FIT / ASM / FIN entries current, inventory statuses updated, deviations logged in the matrix Decision log; reprint-and-improve loop for weak/ugly parts; photos into `08_reference_photos/`.
- **Done criteria (project end):** a future reader could rebuild the car from this repo alone; final photos archived; leftover open questions closed or explicitly parked.

---

## Standing open questions / human checks (live list)

Tracked here until resolved; details in `MODEL_INVENTORY.md`:

1. **Gate A + rear wing/DRS (coupled)** — check the selected rear rocker /
   spring-mount / rear-stack configuration correctly **seats and articulates with
   the 68 mm rear shocks** (rear length confirmed 2026-07-10; 51/52 mm are
   front-only). Rev-1 path may replace the L/R axle holders — drawing `[7]`.
   **Preferred wing: old `2021Rearwing with DRS`** (Vitaliy 2026-07-10); DRS remains
   a goal. Gate open until: 68 mm path checked (slicer/dry assembly) + rear stack
   confirmed + wing mount confirmed + 2021 wing checked with mount/DRS arm/
   diffuser-backplate + remaining doubts settled by **diagnostic TPs** (policy in
   `MODEL_INVENTORY.md`). `newgearmotorlock` demoted to diagnostic candidate (belt
   lock primary).
2. **Gate B front — RESOLVED 2026-07-10:** `FRONTNOSE2024` + `2024 Revised Front Wing`
   → REQUIRED (drawing `[5]`, body README, bbox math). Residual: slicer visual confirm
   of shell+nose+wing together; formally reject `pin.stl` once no pin holes are seen.
3. **Gate C (research/design task)** — camera integration is undecided. Camera =
   SSC338Q + IMX335 (on hand); blower in transit. `camera_blower_duct.scad` = duct
   design candidate (fully parameterized, placeholder defaults — inspected
   2026-07-10); a diagnostic default-render for visual check is allowed now. Design
   only from real calipers measurements — checklist in `FIRST_PRINT_DECISION.md` §6;
   production duct blocked until camera + blower measured, placement decided,
   airflow/lens-clearance/service-access checked. **Placement requirements + the
   driver-seat vs halo-height trade study now live in `CAMERA_GIMBAL_PLACEMENT.md`
   (2026-07-14, source of truth — includes VR/head-tracking requirements and the
   hard-stop geometry the firmware safety gate needs); the placement decision itself
   remains open.**
4. **Gate D — RESOLVED 2026-07-10:** `Servoholder` is the floor servo mount (drawing
   `[2]`) → REQUIRED. Residual: DS3235SG fit-check on arrival, before the floor batch.
5. Hardware **partially delivered 2026-07-17:** MR128ZZ 8×12×3.5 front bearings ×10
   (need 4 + spares), metal 3×32 mm turnbuckles **×2 (count confirmed — matches the
   wanted 2; closes the ×1-vs-×2 doubt in `learning-manual/open_questions.md` #22)**,
   plastic M4 rod-end linkage balls ×10, M3 tie-rod-end ball joint caps, steel
   fully-threaded rods, aluminium tube **OD 16 × ID 14 mm, 300 mm — the rear-axle
   spacer stock (ID matches the 14 mm-ID metal-spacer spec in `ASSEMBLY_NOTES.md`;
   cut 4 spacers, 2/side — heat protection, do not omit; spacer cut length TBD at
   rear-axle dry assembly)**.
   **Still in transit:** tyres 54198/51400, 52/68 mm shocks, servos (DS3235SG + MG90S),
   king pins, belt set, rear 6801 bearings, blower. On arrival: measure front shocks
   (51 vs 52 mm), spur↔pulley bolt pattern, both servo fit-checks. Delivered bearings
   unblock the **Stage-1 wheel test-fit gate** (coupons → rim/hub print → press-fit)
   once the first hub is printed. Until the rest arrives:
   hardware-dependent fitment blocked; **printed↔printed diagnostic dry assembly allowed**
   (`ASSEMBLY_NOTES.md`). **Battery not final** — approximate shell probe done
   (`FIRST_PRINT_DECISION.md` §7: width/height clear with margin, length unproven);
   keep ≤75×45×25 mm; slicer-assembly measure next, physical fit final.
6. Tyre-slot adapter final quantity (1 or 2 per side) — at assembly.
7. Rear tyre-slot adapters heat-watch after first drives (PETG → ASA if soft).
8. Review this session's inventory + material matrix (Vitaliy).
9. Execute `FIRST_PRINT_DECISION.md` (rev. 2026-07-10 third pass): coupons printable
   now; the coupled rear decision (slicer + diagnostic TP wave) is the next sitting;
   camera measurement checklist can start in parallel.
