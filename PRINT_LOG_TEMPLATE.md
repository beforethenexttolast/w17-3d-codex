# Print Log & Decision Templates

Copy-paste templates for every record this subproject keeps. Where each record lives:

| Record | Template | Lives in |
|---|---|---|
| Print attempt (success or fail) | §1 | `05_printed_parts_log/PRINT_LOG.md` (newest on top) |
| Failed print post-mortem | §2 (appended to its §1 entry) | same |
| Test/calibration print | §1 with `TP-NNN` id | `04_test_prints/TP-NNN-<name>.md` |
| Material decision | §3 | appended to `MATERIAL_DECISION_MATRIX.md` §"Decision log" |
| Fitment check | §4 | `04_test_prints/` (test parts) or `05_printed_parts_log/` (real parts) |
| Assembly note | §5 | `07_assembly_notes/` |
| Finishing note | §6 | `06_finishing/FIN-<part>.md` |

**ID conventions** (used across all records so entries cross-reference cleanly):
- Print attempts: `P-NNN` (P-001, P-002 … chronological, failures included — never reuse a number).
- Test prints: `TP-NNN`.
- Physical parts: label the printed part itself (pencil/marker on a hidden face or a masking-tape tag) with its `P-NNN`.
- Photos: `08_reference_photos/YYYY-MM-DD_<P-NNN or what>.jpg`.

---

## 1. Print attempt

```markdown
### P-NNN · <part name> · YYYY-MM-DD
- **Model file:** <exact filename> (source: <path in unsorted_stl_raw/ or 02_ready_to_slice/>)
- **Qty on plate:** 1
- **Material:** <PLA matte black / PETG-HF blue / ASA black / …> — brand/spool: <…> — dried? <yes/no, hrs @ °C>
- **Printer / nozzle:** Bambu X1C / 0.4 mm — plate: <textured PEI / cool / …>
- **Profile:** <03_print_profiles/ name or "PRINT_SPEC.md §<class> defaults">
- **Layer height:** <0.2 mm> · **Walls:** <4> · **Top/bottom:** <4/4>
- **Infill:** <40% gyroid> · **Supports:** <none / tree, where> · **Brim:** <no / 5 mm>
- **Orientation:** <which face down, why — load direction note>
- **Est. time / filament:** <from slicer> · **Actual time:** <…>
- **Result:** ✅ success / ⚠ usable-with-flaws / ❌ failed
- **Problems:** <stringing / warp / layer shift / adhesion / none>
- **Measurements:** <bearing seat Ø, critical dims vs expected>
- **Fitment:** <not checked yet / see fitment entry below>
- **Photos:** <08_reference_photos/… or "to add">
- **Next action:** <use as-is / reprint with change X / redesign / part done>
```

## 2. Failed print post-mortem (append to the failed P-NNN entry)

```markdown
- **FAILURE ANALYSIS (P-NNN)**
  - **Failed at:** <layer ~N / N% / first layer / after removal>
  - **Failure mode:** <adhesion loss / warp lift / layer split / clog / spaghetti / crack in use>
  - **Suspected cause:** <wet filament / orientation across load / speed / temperature / draft / bad overhang>
  - **Evidence:** <what you saw; photo path>
  - **Keep or scrap:** <scrap — recycled / kept as tolerance reference>
  - **Change for retry:** <ONE variable at a time when diagnosing>
  - **Retry:** P-NNN+m
```

## 3. Material decision

```markdown
### MD-NNN · <part or part-group> · YYYY-MM-DD
- **Decision:** <material + color>
- **Alternatives considered:** <…>
- **Why:** <heat / load / crash / cosmetics / stock on hand>
- **Deviates from docs/print_spec_v2.md?** <no / yes — how + why>
- **Approved by Vitaliy:** <pending / yes YYYY-MM-DD>
- **Revisit if:** <part deforms in sun / cracks in crash / …>
```

## 4. Fitment check

```markdown
### FIT · <part A> ↔ <part B/component> · YYYY-MM-DD (part: P-NNN)
- **Interface:** <bearing seat / tyre bead / screw boss / pin>
- **Nominal:** <design dim> · **Measured:** <caliper reading>
- **Fit:** press / snug / slip / loose / does-not-fit
- **Assembled + disassembled OK?** <y/n>
- **Under load?** <hand-flex / spin test / not tested>
- **Verdict:** ✅ good / adjust slicer <how> / post-process <ream, sand> / redesign
- **Next action:** <…>
```

## 5. Assembly note

```markdown
### ASM · <sub-assembly> · YYYY-MM-DD
- **Parts (P-NNN ids):** <…>
- **Fasteners/inserts used:** <M3×8 + nylock / M3×5 heat-set / CA glue / epoxy>
- **Reference drawing:** <unsorted_stl_raw/...pdf page / photo>
- **Problems:** <…>
- **Torque/care notes:** <plastic bosses — snug, not tight>
- **Result + photo:** <…>
```

## 6. Finishing note

```markdown
### FIN · <part> · started YYYY-MM-DD
- **Target finish:** quick-functional / realistic-body / durable-RC (FINISHING_GUIDE.md workflow)
- **Steps done:** [ ] deburr [ ] sand 240 [ ] sand 400 [ ] filler primer [ ] sand 600
  [ ] primer [ ] base coat <color> [ ] accents <color> [ ] decals [ ] gloss clear [ ] final clear
- **Products used:** <primer/paint/clear names>
- **Masked interfaces:** <bearing seats / lens / screw holes — confirm before every coat>
- **Dry/cure waits:** <per can instructions — note actuals>
- **Problems:** <runs / silvering / fisheyes>
- **Photos per stage:** <…>
```
