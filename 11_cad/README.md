# `11_cad/` — parametric drafts for the electronics packaging

**Created:** 2026-09-03 · **Owner decision:** A3, 2026-09-02 (mechanical design moves
to Claude Code) · **Study:**
[`../10_assembly_architecture/AA_electronics_placement_study.md`](../10_assembly_architecture/AA_electronics_placement_study.md)

---

## Read this first

Nothing in this folder is a production part.

**A2 is NOT-EXECUTED and Phase B is BLOCKED.** No file here authorises a production
print, a shell cut, a hole in a donor part, or any powered work. Roughly half of the
dimensions these models are built from have never been measured — they are tagged
`ASSUMED` in [`w17_params.scad`](w17_params.scad) §9 and each names the measurement
that retires it.

The only things here meant to meet a printer soon are the four **fit-check coupons**,
and they are TP-class: draft settings, physically labelled `TP`, logged in
[`../04_test_prints/`](../04_test_prints), and never installed on the car
(risk **E-22**).

**Order of operations, and it is not negotiable:**

1. Print coupon **C-1** (peg/hole ladder). It calibrates `fit_clearance`, which every
   other model depends on.
2. Run the owner measurement session
   ([`../w17-mechanical-measurement-session-prompt.md`](../w17-mechanical-measurement-session-prompt.md)) —
   at minimum **M-01** (S0), **M-02** (the real steering sweep) and **M-03** (the board).
3. Print **C-2**, **C-3**, **C-4**.
4. Put the real numbers into `w17_params.scad`, replacing the `ASSUMED` tags.
5. *Then* talk about printing a cage.

---

## Files

| File | What it is |
|---|---|
| [`w17_params.scad`](w17_params.scad) | **The only place a *shared* dimension may live** (model-local ones are declared at the top of their own model, still named and still tagged). Every value carries a provenance tag; every `ASSUMED` value is repeated in §9 against the measurement that retires it. **Eight** `assert()`s encode the study's arithmetic so a later edit cannot silently break it, and `render.sh` checks one of them against the exported solid rather than the arithmetic (below). |
| [`lib/w17_lib.scad`](lib/w17_lib.scad) | Shared shapes: cells, standoffs, insert bosses, board pockets, hole patterns, edge slots with lead-ins, cable-tie slots, rounded cable pass-throughs, chamfered boxes, context ghosts. **Contains no dimension of the vehicle** — every size arrives as an argument. Two *proportions of a shape* do live here, as named and tagged default arguments a caller can override: `extra_h` (:109, the headroom a heat-set boss gets above its insert) and `relief_frac` (:135, how much of a pocket's width the finger scallop takes). |
| [`second_floor_cage.scad`](second_floor_cage.scad) | The cage the owner asked for. `render_mode = part / context / section`, `part = all / cage / clip / clip_print`. **`clip` and `clip_print` are not the same export:** `clip` shows the four clips where they sit on the car, standing 31 mm in the air; `clip_print` is the plate you actually slice, with all four laid down in the print orientation. Slicing `clip` would print four towers whose layer lines run straight across the crash load. |
| [`esp_tray.scad`](esp_tray.scad) | `variant = shoe` (the on-edge carrier for the car) or `bench` (a desk tray for flashing — explicitly **not** a vehicle part). |
| [`fit_check_coupons.scad`](fit_check_coupons.scad) | `coupon = c1 / c2 / c3 / c4`, per study §11. |
| [`gcs_box.scad`](gcs_box.scad) | The ground-station enclosure, as a *sled strategy* rather than a box — four of its five module envelopes have no measurement anywhere. |
| [`render.sh`](render.sh) | Renders everything to `out/`. Fails loudly on any warning, non-manifold status, or empty result. |
| [`tools/stl_stats.py`](tools/stl_stats.py) | Triangle count + bounding box of an STL, tab separated, used by `render.sh --table`. |

`out/` is gitignored, and the repo `.gitignore` already blocks `*.stl` and `*.png`
everywhere, so no binary can be committed from here.

---

## Coordinate frame

Every model is authored in the **P0 vehicle frame**, not in "part coordinates":

| OpenSCAD axis | Vehicle meaning |
|---|---|
| `x` | **X**, positive **forward**; X = 0 at the front/rear floor joint |
| `y` | **L**, lateral; the belt / architecture-right side is **L < 0** |
| `z` | **Z**, up from **DAT-F** (floor top) = 0 |

This is why the bounding boxes below read like the study's cell tables. It also means
a model can be checked against a keep-out by eye: if a number in the `Z` column is
above 14 while the `L` column is inside ±30, something is wrong.

---

## Rendering

```bash
cd 11_cad
./render.sh              # STL + PNG preview for every model
./render.sh --stl        # STL only (much faster)
./render.sh --table      # render, then print the table below
```

If OpenSCAD is not at `/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD`, set
`OPENSCAD=/path/to/OpenSCAD` first.

**"Clean" is enforced, not assumed.** A render only counts if OpenSCAD exits zero,
emits no `WARNING` or `ERROR`, reports manifold `Status: NoError`, and leaves a
non-empty STL. Anything else fails the script.

### Render results — OpenSCAD 2026.09.01, manifold backend, 2026-09-03

**17 STL exports + 19 PNG previews. 17 rendered, 0 failed.** Every one reported
`Status: NoError`, and the one geometric check the script makes passed:

```
ok     cage_all  max Z = 32.0000 == board_top_z (AA §5.3 / §5.6)
```

That check is not a duplicate of the `assert()`s. The asserts test the *arithmetic*;
this one reads the **exported solid** — the thing a slicer would see — pulls its
bounding box through [`tools/stl_stats.py`](tools/stl_stats.py), and compares its top
to `board_top_z`, which it reads back out of `w17_params.scad` rather than hardcoding.
It is the mechanised form of the study's §5.6 rule that nothing in the cage may rise
above the board's top edge — the rule that, broken by 3 mm, pushes the required S0
from 9.82 mm to 12.82 mm and takes it outside the bound S0 is known to live in.

| Model | Triangles | Bounding box (mm) | X | L | Z |
|---|---:|---|---|---|---|
| `cage_all` | 3214 | 45.0x86.0x32.0 | 1.0..46.0 | -43.0..43.0 | 0.0..32.0 |
| `cage_body` | 2182 | 45.0x86.0x30.0 | 1.0..46.0 | -43.0..43.0 | 0.0..30.0 |
| `cage_clip` | 960 | 30.0x77.2x32.0 | 7.0..37.0 | -38.6..38.6 | 0.0..32.0 |
| `cage_clip_print` | 960 | 32.0x44.8x6.0 | 0.0..32.0 | -3.2..41.6 | 0.0..6.0 |
| `coupon_c1` | 19754 | 106.0x28.0x12.0 | 0.0..106.0 | -14.0..14.0 | 0.0..12.0 |
| `coupon_c2` | 11500 | 68.0x20.0x16.0 | 0.0..68.0 | -10.0..10.0 | 0.0..16.0 |
| `coupon_c3` | 6240 | 59.0x48.6x17.0 | 0.0..59.0 | 0.0..48.6 | 0.0..17.0 |
| `coupon_c4` | 10616 | 150.0x18.0x11.0 | -30.0..120.0 | -9.0..9.0 | 0.0..11.0 |
| `esp_bench_tray` | 1924 | 49.0x41.0x8.0 | 0.0..49.0 | -20.5..20.5 | 0.0..8.0 |
| `esp_shoe` | 200 | 39.4x5.2x6.6 | 0.0..39.4 | -2.6..2.6 | 0.0..6.6 |
| `gcs_bulkhead` | 656 | 6.4x162.0x38.5 | 0.0..6.4 | 0.0..162.0 | 0.0..38.5 |
| `gcs_lid` | 936 | 106.8x166.8x2.4 | 0.0..106.8 | 0.0..166.8 | 0.0..2.4 |
| `gcs_sled_ftdi` | 1506 | 49.4x27.4x6.0 | 0.0..49.4 | 0.0..27.4 | 0.0..6.0 |
| `gcs_sled_hub` | 1438 | 94.4x49.4x6.0 | 0.0..94.4 | 0.0..49.4 | 0.0..6.0 |
| `gcs_sled_tx` | 778 | 74.4x58.1x6.0 | 0.0..74.4 | 0.0..58.1 | 0.0..6.0 |
| `gcs_sled_wifi` | 834 | 64.4x34.4x6.0 | 0.0..64.4 | 0.0..34.4 | 0.0..6.0 |
| `gcs_tray` | 27220 | 106.8x166.8x41.5 | 0.0..106.8 | 0.0..166.8 | 0.0..41.5 |

**`cage_clip` and `cage_clip_print` are the same four clips in two orientations.**
`cage_clip` is the **installed view** — four 31 mm towers standing where they sit on
the car. `cage_clip_print` is the **print plate**: the same four laid down a quarter
turn about L, so the clip's 6 mm length becomes the 6 mm print height and every layer
runs the full length of the upright rather than across the crash load. Slice
`cage_clip_print`; look at `cage_clip`.

Two entries render as **PNG only, by design**: `cage_context` and `cage_section`. The
`%` modifier that draws the ghost bodies (the PDB cell, both boards, the KO-01 guard
volume) is a *preview-only* construct — a full `--render` drops it. That is exactly
the property that guarantees a ghost can never end up inside an exported STL, so
those two views deliberately have no STL. Looking at them is the whole point of them.

Every part is inside the X1C's 256 mm bed. The largest is `gcs_tray` at
106.8 × 166.8 mm.

---

## What the CAD found that the prose had not

Drawing the cage falsified three statements the study had made without doing the
arithmetic. All three are now fixed in both places, and they are the most useful
thing in this folder:

1. **Nothing may rise above the board top.** Study §5.3 computes the required shell
   clearance from the board's top plane: `32 + 5 − 27.18 = 9.82 mm`, against an S0
   that is bounded `0 … ~11` and has never been measured. A 3 mm retainer bar lying
   *over* the board makes that `35 + 5 − 27.18 = 12.82 mm` — outside the bound. It
   would not make the cage tighter; it would end it. Retention is therefore a **clip
   whose top face is flush at Z32**, and `w17_params.scad` now asserts
   `s0_required ≤ 11` on every render.
2. **There is nowhere for a heat-set insert.** §5.6 had specified an M3 thumbscrew
   into an M3×5 insert. An insert needs a boss of `4.0 + 2×2.0 = 8 mm` diameter; the
   aft end guide is **2 mm long in X**, and above Z14 the only legal lateral band is
   `|L| 30…43`, which the board fills. The first render put the boss overhanging the
   cassette's aft edge to X−2 and straight through the board seat.
3. **Retention necessarily stands in the board's component zone.** §5.2 always said
   the band is exactly one board thick; the consequence it never drew is that
   *anything* reaching over a board is in the space its outboard components occupy.
   The only variables are how much and at how few stations. Two clips per board is the
   smallest answer that resists the 20 g crash load — and **where** they may sit is
   decided by a real board, which is **M-03** then coupon **C-3**.

---

## What an independent review found that the CAD had not

A second reviewer read this package at `636a816` against the study and the source
documents. Two of its findings were **blocking**, and both were of the same kind: a
*measuring instrument that lied about what it measured*.

1. **The C-1 ladder measured twice the gap it reported.** It shrank the peg by the
   step *and* grew the hole by the step, so its radial gap was `2 × step`, while the
   cage builds a peg at nominal `clip_peg_d` against a hole at
   `clip_peg_d + 2 × fit_clearance` — a radial gap of `1 × fit_clearance`. Printing
   and reading that coupon would have written a `fit_clearance` **twice** what this
   printer needs into the one parameter every peg, slot and pocket here derives its
   clearance from. Every peg on the coupon is now identical; only the hole varies; the
   step you record *is* `fit_clearance`.
2. **The C-4 S0 gauge added height to its own reading.** Its step numbers were
   extruded 0.6 mm *proud* of every step top — the exported bounding box was
   `Z 0…11.6` for an 11 mm top step. The gauge exists to decide whether S0 clears
   9.82 mm out of an 11 mm bound, a margin of 1.18 mm, and a raised digit would have
   eaten half of it in the unsafe direction at every point on the car. The digits are
   cut *into* the steps now, and the export is `Z 0…11.0` exactly.

Three more findings were structural rather than cosmetic:

3. **The register wall had zero clearance to the board it registers.** Its inner face
   sat at `|L| 27.5`, exactly on the PDB's own edge, in an assembly whose test of
   success is that one hand lifts it out. `wall_l_in` is now
   `pdb_l_half + fit_clearance`; because the outer face cannot move (it is both the
   PCB plane and the KO-01 lateral guard) the clearance is paid out of wall thickness,
   so the wall is **2.3 mm, not the 2.5 mm nominal**, and a new `assert` holds it
   above the four-perimeter minimum.
4. **The aft end guide is clear of the PDB laterally, not fore-aft.** Both the study
   and the model said it was "aft of the PDB in X". It is not: the guide is
   `X +1…+5` and the PDB cell is `X +1…+46`. What makes it legal is that it sits at
   `|L| 31.8…35.8` — outboard of the KO-01 guard *and* outboard of the PDB's
   `L ±27.5` edge. It passes **beside** the PDB.
5. **`part="clip"` exported a view, not a print.** Four clips standing 31 mm in the
   air, while the file's own comment said the clip is "printed lying flat". Anyone who
   sliced it would have printed four towers with their layer lines across the crash
   load. `part="clip_print"` now exists and both tables above say which is which.

And one that only a font check would catch: the coupons asked for **Helvetica**, which
does not ship with OpenSCAD — it was resolving from the host's system fonts, and
OpenSCAD **does not warn** when a font is missing, it silently substitutes. `render.sh`
could never have caught it. The label face is now `Liberation Sans`, which lives inside
the application bundle, and it is a parameter, so `-D` overrides it.

---

## What these models still do not know

- **S0** (`s0_measured`) is a placeholder holding the *requirement*, 9.82 mm, not a
  measurement. 9.82 of an 11 mm ceiling is a coin flip, and it decides whether the
  cage is built at all. → **M-01**, coupon **C-4**.
- **KO-01**, the steering sweep, is provisional. It is the most restrictive keep-out
  in the car and it sits exactly where the electronics want to be. → **M-02**.
- **The board itself.** No MH-ET drawing exists in any project document: thickness with
  headers, hole pattern, and which short edge carries the service port are all guesses.
  → **M-03**.
- **Whether that port is even USB-C.** This whole package assumes it is, and one of the
  two documents that describe the board disagrees:
  [`w17-electrical-inputs-for-codex.md:8,10`](../../w17-electrical-inputs-for-codex.md)
  says *"onboard micro-USB serial … micro-USB on one short edge"*, while `ZK:102` says
  *"both USB-C service ends face X+42"*. Neither is a caliper record. `esp_usb_w/h` are
  sized for the larger of the two families, which is the safe direction to be wrong in
  for a clearance opening, and `esp_usb_type` now records the assumption instead of
  hiding it. → **M-03(f)**, and study §1.
- **Whether the shoe is affordable.** `esp_tray.scad`'s shoe adds 2 × 1.6 mm to a band
  that is exactly one board thick. → coupon **C-3**.
- **`board_seat_x0`, i.e. OP-H.** The boards' forward end has nothing to land on. Either
  each clip cantilevers or the seat moves ~2 mm aft. → **M-03**.
- **Everything about the GCS box.** Four of five module envelopes have no measurement
  anywhere in the workspace and the hub is not procured. → **M-17**.
- **The DRS throw.** `drs_arm_pivot_span` is deliberately `undef` and an `assert()`
  fires if anyone gives it a value. The 58 mm in the inventory is a raw STL bounding
  box, not a pivot spacing, and a linkage computed from it would be invented. → **M-14d**.

---

## Editing rules

- **Every number that will ever meet a physical object must be a named parameter with a
  provenance tag.** Shared ones live in `w17_params.scad`; ones used by a single model may
  be declared at the top of that model, still named and still tagged. An *anonymous
  literal* in geometry — a bare `8` inside a `cylinder()` — is a bug, because nobody can
  later tell whether it was measured or invented.
  The one exemption, stated so it is not abused: pure **layout** arithmetic on a test
  coupon (where a label sits, how far apart two rows are on a plate) is not a fit
  dimension and does not need a tag.
- When a measurement lands, change the value *and* its tag (`ASSUMED` → `MEASURED(file:line)`),
  and delete its row from §9. The study's §12 table and the measurement-session prompt
  are the other two places that list it.
- Run `./render.sh` before committing. If it exits non-zero, the geometry is not
  reasonable-about yet.
- Never commit anything from `out/`.
