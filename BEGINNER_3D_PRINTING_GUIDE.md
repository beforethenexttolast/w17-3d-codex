# Beginner 3D-Printing Guide — W17 RC Project

**Audience:** you have never 3D printed before. You have a Bambu Lab X1 Carbon with an
AMS (first revision) and a box of filament. This guide teaches the concepts and hands-on
skills; it deliberately does **not** repeat numbers that live elsewhere:

- Slicer settings and starting profiles → `PRINT_SPEC.md`
- Which material for which part → `MATERIAL_DECISION_MATRIX.md`
- Sanding/painting/gluing/inserts in depth + safety → `FINISHING_GUIDE.md`
- Which files to print at all → `MODEL_INVENTORY.md` and `BUILD_SHEET.md`

Read this top to bottom once, then use it as a reference. Sections marked ⚠ are the
ones that cost real money and time when ignored.

---

## 1. The file chain: STL → 3MF → G-code

Think of it like a compiler pipeline, because it is one:

| Stage | File | What it is | Analogy |
|---|---|---|---|
| Model | `.stl` | Bare triangle mesh of the shape. No units metadata (assumed mm), no colors, no settings. | Source code |
| Project | `.3mf` | Bambu Studio's project file: the mesh **plus** orientation, supports, settings, plate layout. | Build config + source |
| Sliced | `.gcode` / `.gcode.3mf` | Machine instructions: "move here, extrude this much, heat to X". | Compiled binary |

Bambu Studio opens STL and 3MF; the printer consumes only the sliced output. When you
hit **Print** in Bambu Studio it slices and sends in one step, so you rarely handle
G-code files directly — but understanding that the slicer is *generating toolpaths*,
not "sending the model", explains why every setting change requires re-slicing.

**Why we never touch raw STLs.** An STL is the only ground truth we have for a part
(we didn't design most of these; they came from three different downloads). If we scale,
mirror, or "repair" a file in place, we can never again tell whether a bad fit came from
the designer or from us. So in this repo:

- `unsorted_stl_raw/` is **read-only, forever**. Never move, rename, edit, or delete there.
- Files we intend to print are **copied** into `02_ready_to_slice/`, each with a row in
  `MANIFEST.md` recording where it came from and its SHA-256 checksum.
- Any modification (mirroring a hub, splitting a body) happens in Bambu Studio and is
  saved as a **3MF project** with a new versioned name — the STL copy stays pristine.

Save your work as 3MF projects (`File → Save Project`). A 3MF remembers everything;
re-importing an STL and redoing orientation/supports from memory is how settings silently
drift between prints.

## 2. What slicing actually does

The slicer cuts the model into horizontal layers and plans a path for a 0.4 mm nozzle
to draw each layer in molten plastic. Everything below is a knob on that process.

### Walls (perimeters)
Each layer's outline is traced 2–4 times, forming the solid "shell". Walls carry almost
all of a part's strength — going from 2 to 4 walls does far more for durability than any
infill change, at modest time cost. The outermost wall is also the visible surface.

### Infill
The sparse lattice filling the inside. It exists to support the top surfaces and to
brace the walls, not primarily for strength. Patterns: **gyroid** (our default —
uniform strength in all directions, prints fast, looks like a wavy sponge) and
**rectilinear at 100%** (completely solid, used only where the spec demands it, e.g.
torque-loaded drivetrain parts). Between ~15% and ~40% you buy small strength gains for
a lot of time and weight; beyond that, only 100%-solid is a meaningfully different part.

### Top/bottom layers
Solid "lids" closing the part above the infill and against the plate. Too few top layers
over sparse infill → dimpled, see-through top surface ("pillowing").

### Layer height
The vertical thickness of each slice, with a 0.4 mm nozzle usable from ~0.08 to 0.28 mm:

- **0.20 mm** — the workhorse. Good strength, reasonable time. Default for everything mechanical.
- **0.12–0.16 mm** — for visible bodywork. Curved surfaces (nose, engine cover) show
  layer "stair-stepping" on shallow slopes; finer layers halve the stairs and cut sanding
  work dramatically. Costs roughly proportionally more time (0.12 ≈ 1.7× longer than 0.2).
- Layer height changes *vertical* resolution only; holes and outlines in the XY plane
  are unaffected.

### Seams
Each layer's outer wall starts and stops somewhere; those points stack into a faint
vertical scar. On bodywork you tell the slicer to hide the seam on a rear edge or
sharp corner (see `PRINT_SPEC.md`). On mechanical parts, ignore it.

### Supports
Printers can't extrude into thin air. Overhangs steeper than ~50° from vertical and
bridges longer than a few mm need scaffolding printed underneath, snapped off afterward.
Supports always **scar the surface they touch** — a matte, slightly torn texture. That's
why orientation matters so much on cosmetic parts: rotate the part so supports land on
the *inside/hidden* face. **Tree supports** (our default) grow like branches, touch less
of the part, and remove more easily; **normal (grid) supports** are denser and better
under large flat ceilings. One rule: check *where* supports will touch before every
cosmetic print, in the slicer preview.

### Bed adhesion
The whole print's success is decided by layer one. The first layer is squished onto a
heated **textured PEI plate** (the X1C's standard plate) which grips molten plastic and
releases it when cool. Failure modes: nozzle too far → spaghetti; part peels mid-print →
warped corner or lost part. Helpers: a **brim** (single-layer skirt fused to the part's
base, cut off later) for tall/narrow parts, and **glue stick** — which on this plate is
mostly used as a *release agent* for PETG, not an adhesive (PETG can bond so hard to PEI
it tears the plate coating). Specifics per material: `PRINT_SPEC.md`.

## 3. First prints on the X1 Carbon — walkthrough

The X1C automates most classic beginner pain (bed leveling, flow calibration). Your job
is mainly loading filament correctly and checking the first layer.

1. **Set up the printer** per Bambu's quick-start (unpack, remove all foam/screws marked
   orange, install AMS on top, connect via the Bambu Handy app or LAN). Run the guided
   self-test when prompted — it calibrates vibration compensation and the lidar.
2. **Load filament.** Spools go in the AMS; it identifies Bambu-brand spools via RFID,
   third-party spools you declare manually in the device screen or Bambu Studio (set
   brand/material — this drives temperatures). ⚠ **TPU never goes through the AMS
   (rev 1)** — it's too flexible and will jam in the feed path. TPU prints from the
   **external spool holder** on the back, fed directly.
3. **Dry filament if in doubt.** PETG/ASA/TPU that has sat unsealed for weeks prints
   visibly worse (see mistake list below). The X1C can dry a spool on the heated bed
   under a box, but a cheap filament dryer is the better tool. When to dry: `PRINT_SPEC.md`.
4. **First print: a Benchy or Bambu's pre-sliced samples,** in PLA from your stock. Not
   a car part. You are learning the workflow, not producing.
5. **In Bambu Studio:** `File → Import` an STL (or open a sample project) → select
   printer X1C 0.4 nozzle → select filament (must match what's loaded/AMS slot) →
   choose a preset (see `PRINT_SPEC.md`) → **Slice plate** → inspect the preview
   layer-by-layer with the right-hand slider → **Print plate**, leaving timelapse and
   AI failure detection on.
6. **Watch the entire first layer.** Seriously — 90% of failures announce themselves in
   the first 5 minutes. You want evenly squished, slightly flattened lines with no gaps
   between them and no plastic balling around the nozzle. The X1C's lidar first-layer
   inspection helps but is not a substitute for your eyes early on.
7. **Removing the part:** wait until the bed cools below ~35 °C (the part often audibly
   un-sticks). Take the flexible plate out, **bend it** — the part pops off. Never pry
   with a blade toward your hand; for stubborn PETG, flex more or wait longer, don't force.
8. Put the plate back, wipe occasionally with isopropyl alcohol when prints stop
   sticking well (skin oils are the usual culprit). Wash with dish soap if IPA stops helping.

Do two or three throwaway prints (Benchy, a calibration cube, one of our test coupons)
before the first real part. Budget an evening for this; it repays itself immediately.

## 4. ⚠ Common beginner mistakes

| Symptom | Actual cause | Fix |
|---|---|---|
| Popping sounds, steam, fuzzy/stringy surface, weak parts | **Wet filament** (esp. PETG, ASA, TPU) | Dry the spool; store with desiccant in sealed bags |
| Fine hairs between features | Stringing — wet filament or temp too high | Dry first, then lower nozzle temp 5–10 °C |
| Part corner lifts off plate mid-print | Warping — bed too cold, draft, or big flat ASA part without enclosure prep | Close door/lid (ASA), brim, clean plate |
| First layer lines don't touch each other | Plate needs cleaning, or z-offset issue (rare on X1C) | IPA wipe, re-run calibration |
| Part fused to plate | PETG on bare PEI | Thin glue-stick layer as release agent next time; cool fully, flex plate |
| Bottom edge bulges outward ("elephant foot") | First layer over-squish + heat | Mostly cosmetic; chamfer with a deburring tool; matters for fit only on precise bases |
| Part looks perfect but snaps easily along a line | Load is across layer lines — wrong orientation | Reorient so layers run along the stress (see §12) |
| "The slicer preview looked fine" | You checked the model, not the **sliced preview** | Always inspect the preview: supports' touch points, thin walls that vanished, gaps |
| Hole too small for its screw/bearing | Normal! Printed holes come out undersized | Expect it; measure, then drill/ream or adjust (see §8) |
| Sanded PETG looks worse than before | PETG smears and fuzzes when sanded dry at high grit speed | PETG is for hidden/mechanical parts; cosmetics are PLA + primer (see `FINISHING_GUIDE.md`) |
| AMS grinding/jam with flexible filament | TPU in the AMS rev 1 | External spool holder only |
| Print #2 doesn't match print #1 | Settings drifted — re-imported STL, forgot a changed setting | Save and reuse **3MF projects**; log every print (§6) |

## 5. Labeling and version tracking of physical parts

Printed parts multiply, and three near-identical rims with different tweaks are
indistinguishable a week later. The system:

- Every print gets a log entry with an ID: real parts in
  `05_printed_parts_log/PRINT_LOG.md`, test prints as `TP-NNN` files in `04_test_prints/`.
- **Write the ID on the part** the moment it comes off the plate: soft pencil or fine
  permanent marker on an inner/hidden face (inside of body shell, underside of mounts).
  If no hidden face exists, a masking-tape flag with the ID.
- Parts that will be painted: pencil only where primer will cover, or tape — marker can
  bleed through light paint.
- A part with no ID and no log entry is a mystery object; when in doubt, re-measure it
  against the log before trusting it on the car.

## 6. Documenting failures and iterating on fit

A failed print is data you paid for; without notes it's just wasted plastic. For every
attempt — success or failure — fill the *Print attempt* template in
`PRINT_LOG_TEMPLATE.md` (file, material, profile, orientation, result, problems). For
failures, add the *Failed print* fields: at what height/time it failed, what it looked
like, your best-guess cause, and what you'll change. **Change one variable at a time**
— temperature *or* orientation *or* speed — or you learn nothing from the retry.

The fit-iteration loop:

1. Print the smallest thing that answers the question (a coupon with just the bearing
   pocket, not the whole hub — cut it out in Bambu Studio with the cut tool if needed).
2. Measure part and counterpart with calipers (§7). Write numbers down, not "a bit tight".
3. Decide: tune (drill, ream, sand, scale by 0.5%?) or re-slice with a change, or
   redesign (§11).
4. Retest the coupon, not the full part. Only print the full part when the coupon fits.

## 7. Calipers 101

Digital calipers are your multimeter for plastic. Zero them closed before each session.

- **Outside dims:** big flat jaws, gentle contact — plastic compresses; use the same
  light pressure every time. Take 2–3 readings at different spots (prints aren't
  perfectly uniform).
- **Holes:** the small top (inside) jaws, opened inside the hole, rocked slightly to
  find the maximum — that's the diameter. Note printed holes are slightly polygonal and
  narrower near the bottom (first-layer squish), so measure mid-depth when possible.
- **Depths:** the depth rod at the tail end, base flat on the rim of the pocket.
- **Steps/shoulders:** the flats behind the jaw tips.
- **Shrinkage check:** print a 20 mm calibration cube in the target material, measure
  X/Y/Z. PLA on the X1C is typically within ±0.1 mm; ASA shrinks noticeably more.
  Knowing *your* numbers per material beats any table from the internet.

## 8. Tolerance thinking

FDM parts are not machined parts. Baseline expectations with a 0.4 mm nozzle:

- **Holes print undersized** by roughly 0.1–0.3 mm (melted plastic bulges inward on
  curves). Vertical holes are rounder; horizontal holes come out slightly D-shaped.
- **Clearance starting points** for a printed peg in a printed hole:
  0.1 mm total → press/snug fit; 0.2 mm → sliding fit; 0.3 mm+ → loose/rattly.
  These are *starting points* — verify with a coupon per material.
- **First-layer squish** widens the bottom ~0.1–0.2 mm (elephant foot): chamfered or
  deburred bases fit better into pockets.
- **Bearings** (8×12×3.5 front, 6801 rear on this car): the seat should be a light
  press fit. If the printed pocket is tight, that's often *good* — do not enlarge in the
  slicer until you've tried a gentle press; a loose bearing seat is far worse.
- **Drilling/reaming beats reprinting** for round holes that are only 0.1–0.4 mm under:
  a hand-twisted drill bit of the target size cleans a hole in seconds. Reprint only
  when the error is systematic and you'll print the part again anyway.
- Designers bake their own printer's tolerances into their STLs. Ryan's files were
  tuned on *his* printer — expect the first fit of pins ("tighter pins" variants exist
  in the raw files for exactly this reason) to need testing. That's why the build order
  starts with test fits (`BUILD_SHEET.md`).

## 9. Holes and screws

Three ways a screw meets plastic, in order of preference for this project:

1. **Machine screw + heat-set insert** (§10) — strong, reusable, vibration-tolerant.
   Use for anything opened more than once or holding electronics.
2. **Self-threading into plastic:** an M3 screw driven into a ~2.5 mm hole cuts its own
   thread. Fine for low-stress, rarely-opened joints (the 2024 body mounts are designed
   this way — "tight self-threading holes" per the supplier's README). Two rules: don't
   overtighten (strips instantly), and after ~3–5 reinsertions expect the thread to wear.
3. **Machine screw + trapped nut** — strong and cheap; needs a hex pocket in the design.
   Use when the design already has one.
4. **Threads printed in plastic** (modeled threads): OK at M8-and-larger sizes; at M3
   scale, printed threads are decoration. The locking nuts on the wheel axles in this
   project are printed *as whole nuts* (large, coarse) — that's the working exception.

If a screw feels crunchy going in, back out and check — cross-threading plastic ruins
the hole silently.

## 10. Heat-set threaded inserts

Brass sleeves with knurled outsides and machine threads inside; you melt them into a
printed hole and get metal threads in plastic. Ryan's parts list calls for optional
**M3×5 short inserts** — worth having for the electronics tray and anything serviced often.

Technique: hole diameter ~0.2–0.4 mm smaller than the insert's outer diameter (an M3×5
insert typically wants a ~4.0–4.2 mm hole — check your insert's datasheet; hole depth ≥
insert length + 1 mm), soldering iron at ~250 °C with a flat or dedicated insert tip,
rest the insert on the hole, press **slowly and vertically** with the iron until flush,
keep it square, remove iron, don't touch for 30 s. Practice twice on a coupon first —
inserts pushed in crooked or too deep are very hard to fix. Melting plastic releases
fumes and the iron is at soldering temperature; ventilation and full safety rules in
`FINISHING_GUIDE.md`.

Material note: inserts hold excellently in PETG and ASA, adequately in PLA (PLA creeps
under sustained load near warm electronics — another reason mounts aren't PLA; see
`MATERIAL_DECISION_MATRIX.md`).

## 11. Reprint, tune, or redesign?

Decision guide when a part isn't working:

- **Tune the physical part** (drill, sand, trim): one dimension is off by <0.4 mm, part
  is otherwise sound. Fastest loop.
- **Re-slice and reprint** (new orientation/settings/material): failure is print-quality
  related — delamination, wrong orientation for the load, ugly supported surface, warp.
- **Redesign the model** when the problem is *in the geometry*:
  - Same failure mode twice despite setting changes.
  - Walls thinner than ~0.8 mm (2 × nozzle) that the slicer partially drops.
  - A load fundamentally across layers that no orientation fixes (then the shape, or
    material, or a metal reinforcement must change).
  - Fit is off by design (designer's printer ≠ yours) and the part will be printed many
    times — fixing the source beats drilling every copy.
  - Part exceeds printability (huge overhang, needs splitting — see `PRINT_SPEC.md`).

  Redesign for us means: parametric edit if a `.scad` source exists (the camera duct),
  simple mesh surgery in Bambu Studio (cut/scale/mirror, saved as a new 3MF), or asking
  for a modified STL. We do not sculpt STL meshes by hand. Uncertain parts go to
  `09_rejected_or_uncertain/REVIEW.md` rather than into hopeful reprints.

## 12. ⚠ "Strong enough for RC use?"

An RC car is a vibration testbed that periodically hits walls. The physics you must
internalize:

**Layer adhesion is the weak axis.** A printed part is like wood: strong along the
grain (within a layer), weak across it (between layers). Parts break by layers
separating. **The golden rule from the build sheet: orient every stressed part so the
layer lines run along the load, never across it.** A suspension arm printed flat
(layers along the arm) survives; printed upright (layers across the arm) it snaps at
the first curb like a stack of biscuits.

- **Vibration:** constant on brushless RC. It backs screws out (thread-lock on
  metal-to-metal only — most thread-lockers attack plastics, use it only where the
  liquid can't wick onto printed parts; nyloc nuts and inserts are safer), fatigues
  thin printed clips, and loosens press fits over time. Check fasteners after the first
  runs.
- **Crashes:** the nose, front wing and rear wing take the hits. There is a real
  tradeoff here — a beautifully sanded 0.12 mm PLA wing is *more* brittle than an ugly
  PETG one. Decisions per part in `MATERIAL_DECISION_MATRIX.md`; accept now that wings
  are consumables and plan to reprint them.
- **Heat:** motor, ESC and sun-baked cars soften PLA (it deforms from ~55–60 °C). This
  is why motor-adjacent parts aren't PLA regardless of how strong they feel cold.
- **Hand tests that mean something:** flex a printed coupon of the same material +
  orientation until it gives — you'll feel whether it bends (PETG), fights back (ASA),
  or cracks sharply (PLA). Try to delaminate a test cube by hand across its layers.
  A part you can visibly flex at assembly torque is under-walled or wrong material.
- **A pretty print can still be weak:** surface quality shows tuning; strength lives in
  orientation, walls, and material — all invisible from outside. Trust the log entry
  (which recorded them), not the looks.

**Uncertainty marker:** the clearance and shrinkage numbers in §7–§9 are sound generic
starting points for a well-tuned X1C but have *not* yet been validated on your machine
and your spools — the first test coupons (see `GENERAL_PLAN.md`, test-print phase)
exist precisely to replace these numbers with measured ones. Update this guide's
numbers once you have real data.
