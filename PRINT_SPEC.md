# Print Spec — Bambu Studio on the X1 Carbon

The slicing authority for this project. Consolidates `docs/print_spec_v2.md`
(historical, written for a print shop) into a home-printing spec for **Vitaliy's
Bambu Lab X1 Carbon, 0.4 mm nozzle, AMS rev 1**. Which part gets which material:
`MATERIAL_DECISION_MATRIX.md`. Which files to print at all: `MODEL_INVENTORY.md`.
Concepts explained from zero: `BEGINNER_3D_PRINTING_GUIDE.md`. Settings actually used
per print get recorded in `03_print_profiles/` + `05_printed_parts_log/PRINT_LOG.md`.

**Golden rule (repeated on purpose):** layer lines are the weak axis — a part fails
*between* layers. Orient every stressed part so the load runs **along** the layers.
This matters more than infill percentage.

---

## The slicing workflow, step by step

1. **Import** — drag the STL from `02_ready_to_slice/<group>/` into Bambu Studio (or
   File → Import). Import each STL **once**: `servosaverv7` and `2023NEWSideVent1`
   contain multiple bodies by design — don't add extra copies of them.
2. **Pick printer/plate** — X1 Carbon 0.4 nozzle; **Textured PEI Plate** as default
   (forgiving release, nice bottom texture); Cool Plate only if a glass-smooth bottom
   face matters (then use glue stick with PETG — PETG can bond too hard to smooth plates
   and chip them).
3. **Pick filament preset** — match the actual spool (Bambu PLA Matte, Generic PETG HF,
   Generic ASA…). The preset carries temperatures; you rarely touch those.
4. **Orient** (`R` rotate / `F` place-face-on-plate):
   - Strongest direction = within a layer. Put the expected load in the XY plane.
   - Prettiest surface = top or walls. Support scars = wherever supports touch.
   - Flattest large face down — but for bodywork prefer supports on the *inside*.
   - Mirror here when needed: select part → right-click → **Mirror** → axis
     (required for the **left front wheel hub** — only a Right STL exists).
5. **Set process preset** — start from the profiles below.
6. **Supports** — enable only if needed; **paint-on supports** (brush icon) beat global
   supports on bodywork: put them on inner faces, never on show surfaces.
7. **Slice** and **inspect the preview** — this step catches 90% of failures:
   - Scrub layers bottom→top. Look for: floating islands (need support), paper-thin
     walls (< 2 perimeters wide), the seam line position, first-layer coverage.
   - Check **line type** view: "overhang" coloring shows what's at risk.
   - Read the estimate: time + grams. Anything > 6 h or > 80 g on a first attempt of a
     new part class deserves a smaller test first (see test-print rules).
8. **Print** — AMS slot selected, plate clean (wash with dish soap when adhesion drops;
   IPA between prints). Watch the **first layer** before walking away.

## Starting profiles by part class

Numbers cross-checked against the Codex repo's `bambu_studio_settings_by_material.md`
and re-derived from print_spec_v2; where they give ranges, a single starting value is
picked. Tune from here and record actuals in `03_print_profiles/`.

### 1 · Cosmetic body panels (group 06 — shell, halo, mirror, camera pod)
| Setting | Value |
|---|---|
| Layer height | **0.12 mm** (0.16 acceptable to halve time on the big shells) |
| Walls | 3 |
| Top/bottom | 5 / 5 |
| Infill | 25% gyroid |
| Supports | **tree, paint-on, inside faces only** — never on outer skin |
| Brim | off (add 3 mm if a shell corner lifts) |
| Speed | use the preset; don't chase speed on show parts |
| Seam | **rear/inner** — set Seam position: Aligned, then check preview; move via seam-paint if it lands on a visible curve |
| Ironing | optional, top surfaces only (nose deck) — test on a coupon first |

### 2 · Structural brackets (groups 03/05 — suspension, steering, floor; PETG HF)
| Setting | Value |
|---|---|
| Layer height | 0.20 mm |
| Walls | **4** (floor pieces: 3) |
| Top/bottom | 5 / 5 |
| Infill | **50% gyroid** (floor: 40%) |
| Supports | only where geometry forces it; normal supports fine (scars hidden) |
| Speed | **Strength-oriented: cap outer/inner walls ~150 mm/s** (HF PETG layer-adhesion caveat — see MATERIAL_DECISION_MATRIX.md) |
| Adhesion | textured PEI; dry the PETG first if it strings |

### 3 · Rear drivetrain (group 02 — ASA black) ⚠ the critical batch
| Setting | Value |
|---|---|
| Layer height | 0.20 mm |
| Walls | 4–5 |
| Infill | **100% rectilinear** (non-negotiable, from spec) |
| Top/bottom | 5 / 5 |
| Brim | **on, 5–8 mm** (ASA warps) |
| Environment | enclosed (door closed, glass on), **room ventilated — styrene fumes**, let parts cool IN the chamber (slow cooldown prevents warp/cracks) |
| Speed | slow — use the Strength preset and don't rush |
| First | print the ASA test coupon before any real part |

### 4 · Flexible / impact parts (TPU 90A — only if a redesign calls for it)
0.20 mm · walls 3 · 20% gyroid · speed ~25 mm/s · **external spool, NOT the AMS rev 1**
· dry TPU 8 h first · no supports if avoidable (TPU supports tear badly).

### 5 · Small detail parts (nuts, adapters, pins, diffuser)
0.16–0.20 mm · walls 3 (diffuser: **1–2 over the lens**, 15–20% infill, top/bottom 3/3)
· print **several small parts per plate** but grouped by material · locking nuts: thread
axis vertical so the thread prints clean (verify in preview).

### 6 · Test / calibration prints (always first)
- **Material coupon** per new material: 25×25×10 block + one 8×12 mm bearing-seat hole +
  one M3 hole — measures shrinkage, hole undersizing, and surface on YOUR machine.
- **Part-specific fit tests:** 1 rim + 1 hub + 1 adapter before the wheel batch (tyre +
  bearing fit); a 2–3 cm slice of body shell wall (cut in slicer: right-click → Cut)
  to test the 0.12 mm look + primer behavior before a 10 h shell print.
- 0.20 mm, walls 4, 40% — settings should mimic the real part's class, not be "fast".

## Decision rules (when to deviate)

- **Slow down** when: first print of a new material, any 100%-infill part, layer-adhesion-critical parts, TPU always.
- **Dry filament** when: stringing, popping, fuzzy surfaces; PETG/ASA/TPU by default if the spool sat out > a week (table in MATERIAL_DECISION_MATRIX.md).
- **Split a part** when: it doesn't fit the 256 mm bed (nothing in this project — the 182 mm floor fits), or when one region needs supports everywhere and a cut would eliminate them (glue plan in FINISHING_GUIDE.md).
- **Reorient instead of adding supports** whenever the scarred face would be visible.
- **Test-print first** when: part > 4 h, any critical fit (bearing seats, tyre beads, shock mounts), any new material, any mirrored part (mirrored hub!).
- **Adaptive layer height:** fine for organic cosmetic parts (halo, driver figure) — check the preview banding; skip it on mechanical parts.

## Quantities (from build docs — confirm at assembly)

Rims 2F + 2R · hubs 1 + 1 mirrored · locking nuts 2F + 2R · tyre-slot adapters 1 of
each, **possibly 2 — unproven** · everything else 1× (multi-body STLs count as one import).

## Safety at the printer

Hot end 250–300 °C, bed up to 110 °C — no fingers during/right after; ASA = ventilate
the room during and after, keep the door of the room closed, don't sit next to it for
hours; let the chamber air out before opening wide; nozzle flush/poop bin emptied cold.
Full fume/dust safety: `FINISHING_GUIDE.md`.
