# `11_cad/` — parametric drafts for the electronics packaging

**Created:** 2026-09-03 · **Owner decision:** A3, 2026-09-02 (mechanical design moves
to Claude Code) · **Study:**
[`../10_assembly_architecture/AA_electronics_placement_study.md`](../10_assembly_architecture/AA_electronics_placement_study.md)

---

## Read this first

Nothing in this folder is a production part.

**A2 is NOT EXECUTED and Phase B is BLOCKED.** No file here authorises a production
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
| [`w17_params.scad`](w17_params.scad) | **The only place a dimension may live.** Every value carries a provenance tag; every `ASSUMED` value is repeated in §9 against the measurement that retires it. Six `assert()`s encode the study's arithmetic so a later edit cannot silently break it. |
| [`lib/w17_lib.scad`](lib/w17_lib.scad) | Shared shapes: cells, standoffs, insert bosses, board pockets, hole patterns, edge slots with lead-ins, cable-tie slots, rounded cable pass-throughs, chamfered boxes, context ghosts. **Contains no dimensions at all** — everything arrives as an argument. |
| [`second_floor_cage.scad`](second_floor_cage.scad) | The cage the owner asked for. `render_mode = part / context / section`, `part = all / cage / clip`. |
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

**16 STL exports + 18 PNG previews. 18 rendered, 0 failed.** Every one reported
`Status: NoError`.

| Model | Triangles | Bounding box (mm) | X | L | Z |
|---|---:|---|---|---|---|
| `cage_all` | 3198 | 45.0x86.0x32.0 | 1.0..46.0 | -43.0..43.0 | 0.0..32.0 |
| `cage_body` | 2166 | 45.0x86.0x30.0 | 1.0..46.0 | -43.0..43.0 | 0.0..30.0 |
| `cage_clip` | 960 | 30.0x77.2x32.0 | 7.0..37.0 | -38.6..38.6 | 0.0..32.0 |
| `coupon_c1` | 21920 | 106.0x28.0x12.0 | 0.0..106.0 | -14.0..14.0 | 0.0..12.0 |
| `coupon_c2` | 11408 | 68.0x20.0x16.0 | 0.0..68.0 | -10.0..10.0 | 0.0..16.0 |
| `coupon_c3` | 6284 | 59.0x48.6x17.0 | 0.0..59.0 | 0.0..48.6 | 0.0..17.0 |
| `coupon_c4` | 11126 | 144.0x18.0x11.6 | -24.0..120.0 | -9.0..9.0 | 0.0..11.6 |
| `esp_bench_tray` | 1924 | 49.0x41.0x8.0 | 0.0..49.0 | -20.5..20.5 | 0.0..8.0 |
| `esp_shoe` | 200 | 39.4x5.2x6.6 | 0.0..39.4 | -2.6..2.6 | 0.0..6.6 |
| `gcs_bulkhead` | 656 | 6.4x162.0x38.5 | 0.0..6.4 | 0.0..162.0 | 0.0..38.5 |
| `gcs_lid` | 936 | 106.8x166.8x2.4 | 0.0..106.8 | 0.0..166.8 | 0.0..2.4 |
| `gcs_sled_ftdi` | 1506 | 49.4x27.4x6.0 | 0.0..49.4 | 0.0..27.4 | 0.0..6.0 |
| `gcs_sled_hub` | 1438 | 94.4x49.4x6.0 | 0.0..94.4 | 0.0..49.4 | 0.0..6.0 |
| `gcs_sled_tx` | 778 | 74.4x58.1x6.0 | 0.0..74.4 | 0.0..58.1 | 0.0..6.0 |
| `gcs_sled_wifi` | 834 | 64.4x34.4x6.0 | 0.0..64.4 | 0.0..34.4 | 0.0..6.0 |
| `gcs_tray` | 27220 | 106.8x166.8x41.5 | 0.0..106.8 | 0.0..166.8 | 0.0..41.5 |

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

## What these models still do not know

- **S0** (`s0_measured`) is a placeholder holding the *requirement*, 9.82 mm, not a
  measurement. 9.82 of an 11 mm ceiling is a coin flip, and it decides whether the
  cage is built at all. → **M-01**, coupon **C-4**.
- **KO-01**, the steering sweep, is provisional. It is the most restrictive keep-out
  in the car and it sits exactly where the electronics want to be. → **M-02**.
- **The board itself.** No MH-ET drawing exists in any project document: thickness with
  headers, hole pattern, and which short edge carries USB-C are all guesses. → **M-03**.
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

- **A number may only be added to `w17_params.scad`, and only with a provenance tag.**
  If a model file contains a literal dimension, that is a bug.
- When a measurement lands, change the value *and* its tag (`ASSUMED` → `MEASURED(file:line)`),
  and delete its row from §9. The study's §12 table and the measurement-session prompt
  are the other two places that list it.
- Run `./render.sh` before committing. If it exits non-zero, the geometry is not
  reasonable-about yet.
- Never commit anything from `out/`.
