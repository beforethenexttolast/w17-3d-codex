# w17-3d-codex — Claude Code instructions (3D printing & fabrication subproject)

This repo owns everything physical about the W17 RC F1 car's printed parts: model
selection, slicing, printing, fitment, finishing, painting, decals, and printed-part
assembly. It is Claude-territory (its own git repo). The wider project: 1/10-scale FPV
RC F1 (Mercedes W17 livery, #63) on the OpenRC RC-01 belt-drive chassis — firmware and
electronics live in the sibling repos (`w17-control-fw`, `w17-soundlight-fw`,
`w17-ground-station`); workspace rules in the parent `CLAUDE.md` apply here too.

**Relation to the Codex print repo:** `~/Documents/Codex/w17-rc-print-codex` (ChatGPT
Codex-owned) processed the same STL corpus earlier. It is **read-only forever** from
Claude sessions — its reports may be *consulted skeptically*, never edited, and our
files are staged from `unsorted_stl_raw/` originals, never from its queue (its queue
contains untracked orphan files).

## Priorities (in order)

1. Realistic final appearance (it's a gift-grade W17 replica).
2. Durability under RC driving (vibration, crashes, motor heat).
3. Beginner-friendly process — Vitaliy has never 3D printed; explain the *why*,
   cite files, separate facts from assumptions.
4. Safe finishing/printing (fumes, dust, solvents — safety notes are load-bearing).
5. Traceability of every raw file (original name + location + SHA-256 survive forever).
6. No destructive file operations without a clearly stated, strong reason.

## Hardware facts (stable)

Bambu Lab **X1 Carbon**, 0.4 mm nozzle, **AMS rev 1** (cannot feed TPU — external
spool for TPU). Enclosed → ASA is viable. Bed 256×256×256 mm. Slicer: Bambu Studio.
Filament stock snapshot lives in `MATERIAL_DECISION_MATRIX.md` (update it there).

## Folder & document map (each topic has ONE home — don't duplicate)

| Path | Owns |
|---|---|
| `GENERAL_PLAN.md` | phase roadmap + live open-questions list |
| `BUILD_SHEET.md` | locked config, key numbers, print order, gates (print scope only) |
| `MODEL_INVENTORY.md` + `01_inventory/inventory.csv` | per-file classification (MD is authoritative; CSV regenerated via `01_inventory/build_inventory.py`) |
| `MATERIAL_DECISION_MATRIX.md` | material choices + Decision log (MD-NNN) |
| `PRINT_SPEC.md` | slicer workflow + starting profiles |
| `BEGINNER_3D_PRINTING_GUIDE.md` | concepts/skills teaching |
| `FINISHING_GUIDE.md` | everything post-print + consolidated safety |
| `ASSEMBLY_NOTES.md` | drawings/photo map, fasteners, stage checklists |
| `PRINT_LOG_TEMPLATE.md` | all record templates + ID conventions |
| `docs/` | historical originals (v1/v2 build sheets, print_spec_v2) — never edit |
| `unsorted_stl_raw/` | raw archive — **never modify, rename, or delete anything in it** |
| `02_ready_to_slice/` | copies of selected files only, + `MANIFEST.md` (SHA-256) |
| `04_test_prints/`, `05_printed_parts_log/`, `06_finishing/`, `07_assembly_notes/` | TP / P / FIN / ASM records |
| `09_rejected_or_uncertain/REVIEW.md` | why each rejected/uncertain file is parked |

**Status lives in logs** (`PRINT_LOG.md`, inventory statuses, GENERAL_PLAN open list) —
never in this file. Edit this CLAUDE.md only when an invariant changes.

## Naming conventions

- **Models:** raw files keep their original names always. Copies in
  `02_ready_to_slice/` keep the original basename; group membership is the subfolder.
- **Print profiles:** `profile-<part-class>-<material>-vNN.md` in `03_print_profiles/`.
- **Print attempts:** `P-NNN` (chronological, failures included, never reused).
- **Test prints:** `TP-NNN-<short-name>.md` in `04_test_prints/`.
- **Finished parts:** physical label = its P-NNN; finishing record `FIN-<part-name>.md`.
- **Failed prints:** same P-NNN + FAILURE ANALYSIS block (template §2).
- **Material decisions:** `MD-NNN` entries in the matrix Decision log.
- **Photos:** `08_reference_photos/YYYY-MM-DD_<what>.jpg`.

## How Claude works here

- **Classifying models:** from filenames, READMEs, measured bounding boxes, and the v2
  docs — never claim geometric certainty without slicer/visual confirmation by the
  user. New/unknown files → UNCERTAIN tier in `09_rejected_or_uncertain/REVIEW.md`
  with a reason and what would resolve them. Never guess a part into REQUIRED.
- **Material decisions:** every change is an MD-NNN entry (what/why/deviation/approval/
  revisit-trigger). Deviations from `docs/print_spec_v2.md` are stated explicitly and
  need Vitaliy's approval.
- **Print settings:** starting values from `PRINT_SPEC.md`; whatever is actually used
  goes in `03_print_profiles/` and the P-NNN entry. Never edit PRINT_SPEC to match one
  print — it changes only when a *default* should change.
- **Uncertain models:** stay uncertain until a named gate (A–D pattern) is resolved by
  the user; then update inventory + CSV + REVIEW.md together.
- **Build sheets:** `BUILD_SHEET.md` is the living one; bump content only on real
  config changes and note what changed and why in its appendix. `docs/` versions are
  frozen history.
- **Print logs:** append-only, newest on top, template-driven. A session that prints
  or fits anything ends with the log updated.

## What Claude must NOT do

- Modify/rename/delete anything under `unsorted_stl_raw/` or `docs/`.
- Touch `~/Documents/Codex/` (any repo) — read-only, and only when needed.
- Edit the workspace root `CLAUDE.md`.
- Copy files into `02_ready_to_slice/` without a MANIFEST row (path + SHA-256).
- Present filename-derived guesses as facts; hide uncertainty.
- Commit binaries (`.gitignore` blocks STL/3MF/IPT/images/PDF — keep it that way).
- Tell the user to skip test prints or safety steps to save time.
- Flash, power, or drive hardware decisions — that's the firmware repos' domain, with
  its own gates.

## Safety rules (non-negotiable, repeat to the user when relevant)

- **Hot printer parts:** nozzle to 300 °C, bed to 110 °C — no touching during/after
  prints; maintenance cold only.
- **Fumes/ventilation:** ASA/ABS emit styrene — enclosed printer, ventilated room, door
  closed to living spaces, air out before lingering. PLA/PETG still deserve airflow.
- **Sanding dust:** dust mask/respirator; wet-sand when possible; no dry-sanding
  sessions in living rooms; clean up with wet wipe, not compressed air.
- **Cutting/trimming:** fresh blades cut *away* from fingers; deburring tool over knife
  where possible; eye protection when clipping supports (they fly).
- **Spray paint / primers / clear coat:** outdoors or serious ventilation; organic-vapor
  respirator for repeated sessions; no ignition sources; let cans reach room temp;
  never spray near the printer or electronics.
- **Solvents (IPA, acetone):** gloves, ventilation, fire risk; acetone attacks ASA (and
  that's sometimes useful — welding — but never near finished paint).
- **Glue:** CA bonds skin instantly and fogs clear parts — nitrile gloves, eye
  protection; epoxy = sensitizer, gloves always.
- **Fillers/putty:** sand only with mask; solvent-based putties need ventilation.
- **Threaded inserts:** soldering iron ~200+ °C — burns + plastic fumes; stable grip,
  never toward a finger, let parts cool before handling.
- Keep all of the above away from kids/pets; dispose of solvent/oily rags in sealed
  containers (self-ignition risk).

## Session workflow

1. Read `GENERAL_PLAN.md` (current phase + open questions) and skim the latest
   `PRINT_LOG.md` entries before proposing work.
2. Work one topic at a time; show diffs before committing; small focused commits.
3. End sessions with logs/statuses updated and open questions current.
