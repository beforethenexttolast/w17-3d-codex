# V · Session 4A — P0 Geometry Measurement Results

Session 4A · 2026-07-18 · P0 digital/slicer-stage measurement session (authorized by
the Session-3 verdict **APPROVED FOR P0 + CAD-01**, `U_session3_review_findings.md`).
Cross-account recovery: the session resumed after an account-limit interruption; the
recovered state, toolkit repairs and validation are recorded in §1. **Nothing here
closes a physical measurement digitally; no production CAD/STL is authorized; the
Session-3 corrections (CN-16/DN-11, D-24 scope, P7/P8 prerequisites, balance ledger,
fallback deltas, dummy stubs) are all preserved unchanged.** Session output was left
uncommitted pending the independent checkpoint review recorded in Report W.

---

## 1. Recovery state, toolkit inspection & validation

- Recovered files: `evidence/scripts/stlkit.py` (333 lines, syntactically complete)
  and `evidence/scripts/p0_00_validate_frames.py` (56 lines, complete but carrying
  the interrupted edit's defect).
- **Repair to `p0_00_validate_frames.py`** (diagnosed, not assumed): the expected
  bbox for `new halo 2.1` was a transcription error — script said (75.0, 39.0, 25.0),
  `01_inventory/inventory.csv` says (74.9, 38.8, 24.9), and the mesh measures
  (74.94, 38.75, 24.86). Two `(None, None, None)` rows were filled from inventory:
  `Steering Block4` (31.0, 17.0, 30.0), `GuideRod` (6.2, 6.8, 6.2). After repair:
  **all 15 P0 model bboxes reproduce inventory.csv within the 0.11 mm tolerance
  (exit 0)** — third independent bbox confirmation (after Sessions 1 and 1.5).
- **New `p0_01_stlkit_selftest.py`**: 22 synthetic-geometry checks covering units
  passthrough, section semantics, scanline parity, even-odd spans, loop closure and
  area, non-watertight meshes (open loop + odd-parity detection), ray misses
  (empty list, never an "empty cavity"), multiple intersections, degenerate
  triangles, and binary/ASCII STL round-trip. **22/22 PASS.** One real toolkit
  semantic was characterized and documented in `stlkit.py` during validation: a
  section plane coincident with a flat face returns the face's closed *boundary*
  loop (no thickness info) — measurement planes are therefore always offset off
  exact faces (this bit the first floor survey and was corrected).
- Exploratory scratch scripts (`explore_floor*.py`, `explore_tower.py`) lived in
  the session scratchpad **outside the repo**; their validated logic is consolidated
  into `p0_02…p0_06` below. Nothing exploratory sits in the evidence tree.

**Reproducibility:** every number below regenerates by running, from the repo root:
`python3 10_assembly_architecture/evidence/scripts/p0_0N_….py` (N = 0…6, in order;
p0_06 consumes p0_02's CSV). Outputs land only in `evidence/p0/{tables,sections,
diagrams}`. No STL was modified (scripts are read-only loaders).

## 2. Sources

Models (all from `02_ready_to_slice/`, SHA-256-manifested copies): the three floor
plates, FloorBoard2, side vents, Servoholder, Suspension Block_10, servosaverv7,
Steering Block4, GuideRod, both 2024 shells, FRONTNOSE2024, new halo 2.1, plus rear
drivetrain parts for frame checks. Drawings (viewed as vector PDFs via direct page
render; source files untouched; annotations legible): `[2] FLOOR ASSEMBLY`,
`[3] FRONT SUSPENSION ASSEMBLY`, `[5] BODY UPGRADES`. Photos: the Rev-1.1 top-down
build photo (`…17.08.54 (1).jpeg`). Documents: 2024-body `READ ME.txt`, Reports A–U.

## 3. The P0 vehicle frame (D-01 §coordinate system)

| Axis | Definition | Basis |
|---|---|---|
| **X** | + forward; **X = 0 at the front↔rear floor joint plane** | tongue-and-groove mate (below); nose direction forced by the joint (the front floor's tongue is its rear edge) |
| **L** | lateral offset from the floor centreline (mm) | floor lateral symmetry plane (authored z = 68.5) |
| **Z** | + up; **Z = 0 at DAT-F = chassis floor TOP plane** | floor-top flatness survey (below) |

**Side naming (P0 resolution).** The architecture's RIGHT is *defined by the
drivetrain side* (J: ESC/deck on the motor/belt side). The floor's belt/spur
cutout sits at **L < 0** (X −98…−117), so **architecture-RIGHT = L < 0** in every
P0 table — all relative placements are fully determined. Whether that side is the
driver's right when standing behind the car is a naming check at Gate P1: the
Rev-1.1 photo shows belt = driver-right, while right-handed STL authoring implies
belt-side = driver-left; one of {mirrored export, revision difference, cutout
misread} applies. **|L| values are exact either way. PARTIALLY RESOLVED.**

**Transforms (translation/axis-relabel only; no rotation anywhere):**

| Part | X | L | Z | Status |
|---|---|---|---|---|
| 2023NewFrontFloorLargerParts | x + 89.00 | z − 68.5 | y − 4 | DIGITALLY CONFIRMED |
| 2023NewBackFloorLargerParts | x − 1.15 | z − 68.5 | y − 4 | DIGITALLY CONFIRMED |
| 2023NewBackFloorLargerPart2 | x + 25.22 | z − 68.5 | y − 12 (sits one plate LOWER) | GEOMETRICALLY DERIVED |
| FloorBoard2 | −x − 34.13 (flipped) | z − 9.5 | y − 5 (in the underside channel, Z −8…−6) | GEOMETRICALLY DERIVED |
| Shells (front frame; rear shell first −67.47 in x) | 146.6 − x | −(y − 1.855) | z + S0 (see §5) | GEOMETRICALLY DERIVED / S0 PARTIALLY RESOLVED |
| FRONTNOSE2024 | local x_n reported; rear ring ≈ X 183…187 | z_n − 64 | y_n + 13 (±2) | SLICER-ESTIMATED |

**Joint measurement:** front floor rear edge = full-thickness butt face at
authored x=−89.0 with a 2 mm wedge tongue to −91.0; back floor forward edge =
butt face x=+1.16 with the matching groove (bottom ≈ −0.85). Mated registration
x_ff = x_bf − 90.15 ± 0.2, cross-checked independently by the FloorBoard2 splice
strip: its pair-to-single hole span (93.6 mm) lands on both plates' holes within
0.2 mm. The rear-2 plate stacks one thickness LOWER (plan overlap + coaxial bolt
pair at X −85.93, L ±5 through back floor + rear-2 + splice = 3-layer joint) —
it is the diffuser tail, **not** part of the floor-top datum.

## 4. D-01 — chassis floor-top datum. Status: **DIGITALLY CONFIRMED** (plane + features) / **PHYSICAL CONFIRMATION REQUIRED** (assembled flatness, screw-head protrusion, S0)

Full tables: `evidence/p0/tables/p0_d01_floor_datum.md` + `p0_d01_feature_map.csv`;
diagram: `evidence/p0/diagrams/p0_d01_floor_map.svg`.

- **DAT-F is one continuous flat plane** across front + back floors (4 mm-grid ray
  survey, 2516 samples; deviations only at edge chamfers/joint edge). All ribs,
  recesses, skirts and the FloorBoard2 channel are **underside** features; the top
  is interrupted only by through-openings.
- Thickness classes: 4 mm plain plate; ~6 mm where the underside carries the 2 mm
  recess system (splice channel / nut pockets); 8 mm full-depth zones (centre spine
  block X 0…+69 |L|<22; outboard skirt bands |L| 59…68.5).
- **Centre-band interruptions:** solid X −84…−16 (the KO-19/Servoholder region has
  continuous floor); OPEN X −14…−4 (junction window over the FloorBoard2 lid at
  Z≈−6) with mixed spots to +24; OPEN X ≤ −94 (motor/axle bay); a 12×12 opening at
  (X +78, L 0) on the nose beam approach.
- **Plan silhouette:** full 137 mm width X −30…+30; wide plate ends at X ≈ +55;
  forward of that the floor is a narrowing **nose beam** (53 → 30 mm wide to
  X +180) — the "front bay" floor is beam, not plate, forward of X +55. Rear
  taper: 137 → 112 by X −110; diffuser tail (Z −8 top) to X −141.
- **Battery bay length (the D-01 unlock):** on the L>0 bay, solid plate spans
  X ≈ −5…−83 clear of the joint window and KO-19's centre band → **usable length
  ≈ 78 mm > 75 mm pack limit — length fits, GEOMETRICALLY DERIVED** (S0-independent).
  Pack *height* clearance is S0-conditional (§6). Battery purchase: length is no
  longer the blocker; hold for the S0 pin if the full 25 mm height is wanted.
- Regions unusable as support datums: all centre-band windows above; the vent +
  body-seat zone X +27…+62, |L| 41…62; the belt cutout; X ≤ −94; the beam (all
  of it — narrow, crash-adjacent, suspension territory).

## 5. Shell registration + the pivotal S0 residual (feeds D-02/D-03/D-04)

- The two 2024 shells are authored in ONE frame and **butt edge-to-edge** (rear
  shell −67.47 in x). Verified three ways after registration (X = 146.6 − x_s):
  the front-arch gap brackets a Ø64 tyre at X +146.1 with ~3.5 mm margins; the
  rear-arch gap brackets one at X −90.9 with ~4 mm margins; wheelbase = **237 mm**.
- Both shells share z = 0 exactly = **DAT-S** (shell bottom-edge plane).
- **S0 = height of DAT-S above DAT-F.** Digital bounds: **S0 ∈ [0 … ~11]**.
  0 = flank edges resting on the plate (mechanically forced lower bound: the
  flank edges at |L| 53–57 sit plan-wise over the 137 mm-wide plate). The upper
  hypothesis (~10.4, vent-blade-in-slot engagement) survived one geometric test
  and failed another (slot vs blade axis mismatch); the shell's two floor screws
  (2024-body README) could not be located digitally (no low bosses at the beam or
  vent stations). **This replaces Session-1's P1 (which assumed the floor top
  ABOVE the shell edge, 2–15 mm): measured, the relation is the other way or
  zero — every Session-1 "ceiling above DAT-S" number applies at DAT-F + S0.**
- **S0 is now the single highest-value physical measurement on the car:** set the
  printed shell on the printed floor and measure the edge height. Gate P1 item.

## 6. D-02 — body-to-floor clearance profile. Status: **DIGITALLY CONFIRMED as a lower-bound profile at S0=0** / **PARTIALLY RESOLVED absolutely (S0)** / **PHYSICAL CONFIRMATION at P1/P3**

Full profile (13 transverse stations × 5 lateral positions + widths at 4 heights +
per-station SVGs + 5 longitudinal SVGs): `evidence/p0/tables/p0_d02_d03_d04_clearance.md`,
`p0_d02_stations.csv`, `evidence/p0/sections/`. Headlines (raw ceilings above
DAT-F at S0=0; add S0 when pinned; subtract 5 mm I.1 policy for usable):

| Region | Ceiling @L0 | @\|L\|=20 | @\|L\|=30 | @\|L\|=40 |
|---|---|---|---|---|
| Junction Z3 (X 0) | 71 | 40 | 30 | 28 |
| Z3 core (X −20) | 68 | 39 | 26 | 25 |
| Z3/Z5 (X −40) | 65 | 38 | 23 | 22 |
| Z5 airbox mid (X −60) | 62 | 37 | 19 | 19 |
| Z2 rear (X +20) | 53 | 41 | 33 | 32 |

- **P2c (centreline) = 65–71 over Z3 — Session-1's ~72 estimate CONFIRMED** and
  now datum-clean.
- **P2s (side-bay band) = 26–41 at S0=0** (37–52 if S0≈11). H.1.1 expected 35–45:
  reality is the **low half of the H range unless S0 is generous**.
- Shell-bottom vs floor-clearance distinction is preserved: DAT-S = Z S0;
  everything above is inner-surface data (single-skin shell, ~1.6 mm walls).
- The cockpit aperture is open (no roof) X ≈ +32…+87; the front bay proper
  (Z2, X +10…+55) has 41/33/32 at |L| 20/30/40 — the best side-bay heights on
  the car (Z2R junction-block + RX zones validated with room).

## 7. D-04 — airbox channel. Status: **DIGITALLY CONFIRMED (S0=0 lower bound)**

- Tall-channel (ceiling ≥45) width by station: 38 (X+30) → 32 (X+10) → 26 (X−20)
  → 16 (X−40) → 14–16 (X−60…−80). **Session-1's "14–40 mm" range REPRODUCED**,
  now stationed. ≥60-tall channel: only 4–10 mm wide anywhere.
- **Thermal chimney: VIABLE** — a continuous 14+ mm channel with 58–72 mm crest
  runs from Z3 to the tail; the WiFi deck-rear slot sits under its intake end.
  Flow tell-tale validation at P8 unchanged (F3-14).
- **ESP32 airbox fallback F-2: NOT credible as a module install.** The fallback's
  own condition (≥16 mm channel at the stack station) fails rear of X −40
  (14–16 marginal), and a WROOM DevKit is 25.4+ mm wide before headers, USB plug
  (+10–15 with bend), mount and airflow allowance. PCB-only fit ≠ module fit —
  fallback F-2 should be considered geometrically dead on the recommended path
  (it was already demoted by RST-02; this is the number behind it).
- Antenna use of the channel (PS-12 posts at deck rear): unaffected — whips are
  Ø~6 and the channel takes them with room.

## 8. D-25 — FRONTNOSE2024 interior. Status: **DIGITALLY CONFIRMED (relative)** / **SLICER-ESTIMATED (absolute vertical, ±2)**

Orientation established and verified (mirror-symmetry about z_n=64 = lateral
centre; tip blob at x_n −64.5…−44; full-height closed installation ring
x_n +4…+44; top-cowl-only mid; underside open — **the nose beam is the nose's
floor**). Tables + 16 station SVGs: `p0_d25_nose_interior.md`, `evidence/p0/sections/`.

- Enclosed cavity exists **only in the rear installation ring**: interior width
  39→47 mm, height ~29–32 mm over the beam top, ~40 mm long — and that section
  already contains the beam, the front-shell mating tab and the nose bolt.
- Forward of x_n ≈ 0 the "nose" is a shallow top cowl (crest ~32 over the beam,
  sides OPEN); the tip is effectively solid (crash structure).
- Empty probes were diagnosed per the rule (open underside ≠ empty cavity; each
  station's class is printed).
- **Consequence: the visible nose offers NO protected, enclosed camera volume.**
  E-24 (crash exposure) stands with numbers behind it. The nose-camera option is
  NOT selected and is now numerically disfavoured; the owner decision remains
  formally open (DN-05 scope untouched).

## 9. D-26 — steering-rod line + sweep (slicer stage). Status: **GEOMETRICALLY DERIVED (relative)** / **SLICER-ESTIMATED (absolute)** / **ASM-08 physical stage OPEN**

Table: `p0_d26_rod_line.md`. Measured ingredients: saver pivot = vertical Ø3 bore
(mesh-measured), rod-attach holes at saver-local z 16–22 with **arm radius 18.0 mm**
about the pivot; tower 70.8 tall with its insert blade at the bottom; Servoholder
58 plate + DS3235SG ~40.5 EST (D-09 open).

| Station | X (band) | Z nominal | Z band | lateral band |
|---|---|---|---|---|
| S1 horn end | −30 (−50…−25) | 47 | 42…52 | ±6 nominal, sweep to ±16 |
| S2 mid-spine | +45 | 51 | 42…56 | ±10 |
| S3 saver end | +125 (+119/+129) | 54 | 50…58 | ±6, sweep to ±12 |

- **The rod is a HIGH, nearly-level line (Z ≈ 42–58), not H.1.2's 35→70 rising
  diagonal.** KO-01 reserved band (P0): **Z 35–62, |L| ≤ 18 rear tapering to
  ≤ 12 forward.**
- Consequences: PS-04 deck inboard edge **|L| ≥ 26 near the horn / ≥ 20 forward**
  (**L ≤ −26/−20 on the architecture-right belt side**)
  (at deck heights Z 20–45); the UBEC shelf (≤ Z 14) is untouched by the rod; the
  battery body (top ~28) passes UNDER the band — only straps/walls above Z 30
  respect KO-01. Deck insertion/removal crosses under nothing (rod is inboard of
  the deck). X1 crossing must pass **below Z 35** at the joint region.
- Rod diameter + joint allowances included in the band; lock-to-lock sweep and
  real heights remain **PHYSICAL CONFIRMATION REQUIRED at ASM-08** (unchanged).

## 10. D-27 — deck-side mounting map. Status: **DIGITALLY CONFIRMED (positions ±0.2)** / **PARTIALLY RESOLVED (occupancy)** / **P1 physical stage OPEN**

Table: `p0_d27_deckside_map.md` (+ the full both-sides map in `p0_d01_feature_map.csv`).

- Complete fastener inventory in vehicle coordinates: **35 part-level M3 rows collapse
  to 33 unique assembled coordinates** (the stacked back-floor/rear-2 pair contributes
  two coaxial duplicates), plus openings + recess zones across the three plates, each classified
  through/pocket/underside with nut-pocket edge probes.
- **The "12 free slot-nut positions" assumption does NOT hold.** In the deck-side
  bay (X 0…−60, L −15…−50) exactly ONE unassigned M3 feature exists
  ((−40.0, −32.9)); the PS-15 patch (Z2R) has NONE; the mirror battery bay has one
  ((−39.9, +17.1)). Everything else is occupied by the donor build (splice screws,
  bracket stations, axle-holder rows, 3-layer diffuser joint) or sits in the
  centre band under KO-01/KO-19.
- **Consequence for K/T:** supports must share donor screws, use the free singles,
  or add plate-clamp/edge feet — still with **no new holes in donor parts**.
  PS-01/03/04/05/15 CAD tasks get this as a design input (tagged (P0) in K/T).

## 11. D-03 — speaker candidate envelopes. Status: **DIGITALLY CONFIRMED (S0=0 lower bound); DN-07 stays OPEN**

- Both sidepod pockets measure alike (shell symmetric): interior band |L| ≈ 30…54,
  ceilings 22–30 (X +20…−40), shrinking aft; floor plate solid beneath except the
  vent zone (X +27…+62 outboard).
- A Ø28–40 × 6–12 speaker fits lying flat in EITHER sidepod with margin; a
  left-side (battery-side) install at X −20…−50, |L| ≈ 35–50 is geometrically
  comfortable and carries the I.4 balance argument (20–40 g at ~40 mm lever
  against the ~30–60 g right bias).
- Port/acoustic opening, service access and cable run (CN-21 crossing at X2 per
  F3-12) are layout-compatible; no final dimensions invented; **owner decision
  DN-07 remains open** with both candidate zones now quantified.

## 12. D-06 — camera envelope. Status: **PHYSICAL CONFIRMATION REQUIRED (unchanged — nothing measurable digitally)**

No caliper measurement of the SSC338Q+IMX335 exists anywhere in the repo; the P0
digital session cannot substitute it (Gate C: "never trust product-page dims").
Confirmed sub-envelopes only: VID-HS heatsink 28×28×3 (BOM), `camera top 1.1` pod
16.7×17.7×6.9 (bbox). The envelope separation demanded by the plan (PCB / lens /
soldered-vs-USB interface / cable exit / gimbal / motion / blower / duct) is
prepared as empty labelled rows in Report D's D-06 context — **D-06 remains the
top-priority bench measurement (hardware on hand), and no gimbal envelope was
invented.** CAD-01 correctly excludes the camera block (T row unchanged).

## 13. Required conclusions (the ten P0 questions)

1. **Hybrid B+D digitally credible?** **CONDITIONALLY YES.** The open-spine core,
   zone allocations, thermal chimney and harness plan all survive with real
   numbers. The right *deck* is the conditional part: at S0=0 the side-bay
   ceilings (26–41) cannot host deck-height boards outboard of |L|≈28; at
   S0≈8–11 the deck is marginal-viable exactly as H expected (48 vs ≤55).
   **The S0 pin (one physical measurement) decides it — the H.4 fallback-A
   trigger ("P2s < ~40") is armed but not fired.**
2. **Right-side deck vertical envelope plausible?** Only as a **narrow,
   inboard-hugged, minimum-height deck** (plate ≈ L −50…−26, P4 ≈ 20, boards in a
   fore-aft row) and only in the S0 ≥ ~6 world. At S0=0: NO (fallback A).
3. **D-26 corridor for the deck?** **YES** — the rod band (|L| ≤ 18–12, Z 35–62)
   leaves |L| ≥ 26 free at deck heights; on the belt side this is L ≤ −26.
4. **Airbox still a useful thermal chimney?** **YES** (continuous 14+ mm channel,
   58–72 crest, tail exit) — validate flow direction at P8 as planned.
5. **ESP32 airbox fallback plausible?** **NO** as a module install (F-2's own
   ≥16 mm condition fails at the stack stations; module ≠ PCB). Drop F-2 from
   planning consideration on the recommended path.
6. **Nose camera volume?** **NO protected enclosed volume** (only the occupied
   installation ring; cowl-only forward; solid tip). Decision formally open, now
   numerically disfavoured; E-24 stands.
7. **Speaker for lateral balance?** **YES, viable** — left-sidepod envelope
   quantified and comfortable; DN-07 stays the owner's call.
8. **CAD-01 dummy parameters change?** **NO** — dummy bodies + S3 stubs are
   register-driven and none of the P0 numbers touches them. CAD-01 may proceed.
9. **Ready for diagnostic CAD (post-P0 numbers):** CAD-01 (already free);
   CAD-02 battery tray (length 78 confirmed; parametrize height/strap for S0);
   CAD-04 UBEC shelf + CAD-08 PS-15 junction block (rod-safe below Z 14; use
   plate-clamp feet per D-27); CAD-06 posts (parametric height unchanged).
10. **Still blocked:** CAD-05 deck plate final width/height (**S0 pin + P1**),
    CAD-03 ESC mount (D-08 + Gate A, unchanged), CAD-07 RX carrier geometry
    fine-tune (D-26 physical stage), PS-10/11/14/17 (gates unchanged),
    anything production (P10, unchanged).

## 14. Physical confirmations still required (P0 hand-off list)

| # | Measurement | Where | Priority |
|---|---|---|---|
| 1 | **S0** — shell bottom-edge height above floor top | first body-on-floor placement (P1) | **highest on the car** |
| 2 | Left/right naming vs belt side | same P1 glance | high (naming only) |
| 3 | D-26 rod heights + lock-to-lock sweep | ASM-08 | high |
| 4 | D-06 camera calipers (+ D-06b WiFi after possession confirm) | bench, now | high (hardware on hand) |
| 5 | D-27 free-slot occupancy after mechanical build | P1 dry-fit | medium |
| 6 | Servoholder / bracket-station consumers (which bolts belong to which bracket) | P1 dry-fit | medium |
| 7 | Body 2-screw landing points (README's floor→body screws) | body assembly | medium |
| 8 | Assembled-floor flatness + splice screw-head protrusion at DAT-F | ASM-05 | low |
| 9 | Nose vertical mapping (±2 assumption) | nose dry-fit | low |

## 15. Known limitations

- All shell-interior numbers are single-skin inner-surface reads at S0=0 (lower
  bounds); ribs/local bosses inside the shells were not exhaustively mapped.
- The shells' bottom-edge outlines are open meshes locally (parity warnings
  handled per-station; no number was taken from an unpaired crossing).
- Occupancy assignments for donor fasteners are drawing-level hypotheses where
  the consuming part is not staged (spring mounts verified by pattern only).
- The front-suspension module's exact floor interface (blade landing, arm-bolt
  holes) could not be matched to front-floor features — absolute D-26 stations
  carry the stated bands; nothing downstream consumes them at better accuracy.
- Rounding: mesh coordinates ±0.2 unless stated; policy clearances NOT deducted
  in raw tables.

## 16. Files & evidence produced by Session 4A

Scripts (`evidence/scripts/`): p0_00 (repaired), p0_01 (new, self-test),
p0_02 (D-01/D-27 base), p0_03 (D-02/03/04), p0_04 (D-25), p0_05 (D-26),
p0_06 (D-27), stlkit.py (limitation note added). Tables (`evidence/p0/tables/`):
p0_d01_floor_datum.md, p0_d01_feature_map.csv, p0_d02_d03_d04_clearance.md,
p0_d02_stations.csv, p0_d25_nose_interior.md, p0_d26_rod_line.md,
p0_d27_deckside_map.md. Sections (`evidence/p0/sections/`): 13 transverse +
5 longitudinal D-02 SVGs, 16 D-25 nose SVGs. Diagrams: p0_d01_floor_map.svg.
Register updates tagged **(P0)**: D, I, J, K, S, T, README (this file is the
detail; registers carry only the deltas).
