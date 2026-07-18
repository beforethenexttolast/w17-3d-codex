# W · Session 4A P0 Verification & Checkpoint Review

Session 4A verification · 2026-07-18 · independent geometry-tooling,
mechanical-integration and evidence-asset review of Report V and the P0 updates to
D/I/J/K/S/T. No CAD or production geometry was created.

## Verdict

**P0 VERIFIED WITH MINOR CORRECTIONS — READY FOR CHECKPOINT.** No unresolved
CRITICAL or HIGH finding remains. The numerical P0 conclusions reproduce; the
corrections below repair a signed-coordinate instruction, stale summary graphics,
CSV serialization and evidence annotation/terminology defects without changing the
architecture or any measured value.

## Script and reproducibility validation

- `p0_01_stlkit_selftest.py`: **22/22 PASS**.
- `p0_00_validate_frames.py`: **15/15 model bboxes PASS**, maximum permitted delta
  0.11 mm.
- `p0_00` through `p0_06`: exit 0 in documented order, twice.
- The two runs produced byte-identical logs and byte-identical evidence outputs.
- The regenerated pre-review evidence matched the checked-in working-tree evidence
  byte-for-byte before corrections.
- All staged and raw STL SHA-256 hashes were unchanged before/after the runs.
- The requested `py_compile` first encountered the sandboxed macOS global bytecode
  cache; rerun with `PYTHONPYCACHEPREFIX` under `/tmp` passed for every script. No
  cache was created in the repository.
- Paths are repository-relative; missing inputs raise `FATAL`/`FileNotFoundError`;
  no scratchpad dependency or source-STL write path exists. Ray misses remain empty
  results, not cavity claims; exact-face behavior is characterized by the self-test
  and measurement planes are offset where thickness is inferred.

## Independent high-impact spot checks

| Check | Independent result | Reported result | Status |
|---|---|---|---|
| Floor joint | tongue y 1.005…3.005 at front x=-90; groove crossings 0.005/0.365/3.645/4.005 at back x=+0.8; transformed butt faces agree within 0.01 mm | registration ±0.2 mm | reproduced |
| DAT-F | six rays at X +100/+20/−20/−80 and both sides top at vehicle Z=+0.005 mm | continuous Z=0 plane | reproduced |
| Battery length | solid at X −5/−25/−55/−83, L +35; endpoint span 78 mm | ≈78 mm | reproduced |
| M3 map | 35 part rows → 33 unique assembled coordinates after two coaxial stacked-plate duplicates | 33 unique features | reproduced/clarified |
| Deck-side patch | only (−39.99, −32.86) lies in X 0…−60, L −15…−50 | one free geometric candidate | reproduced |
| Saver | pivot (−0.351, −43.803); outer arm radii 17.98/18.09 mm | ≈18.0 mm | reproduced |
| D-26 stations | nominal S1/S2/S3 = 47/50.39/54 mm before table rounding | 47/51/54 mm | reproduced |
| P2 profile | X 0: 71.2/40.1/29.5/27.8; X −20: 68.0/39.2/26.4/24.7; X −40: 64.9/38.3/22.6/21.9 mm at L 0/20/30/40 | P2c 65…71, P2s 26…41 headline band | reproduced |
| Airbox | width at ceiling ≥45: 38/26/14 mm at X +30/−20/−70 | 38→14 mm | reproduced |
| Nose | tip x_n=-60 is blob; x_n=-28 is open-sided cowl; x_n=+28 has 29.0 mm centre height and 44.2 mm interior width in the installation ring | tip/cowl/ring distinction | reproduced |
| Sidepods | X=0, L +45/−45 ceilings 30.48/30.43 mm | symmetric speaker candidates | reproduced |

The D-26 absolute Z stations remain slicer-estimated because the servo/tower seating
is not physically assembled; this review reproduced the stated arithmetic and mesh
ingredients, not a physical closure.

## Evidence and status review

- All seven final evidence tables were read. Both CSVs parse to a uniform schema
  after correction. The table/figure station values correspond.
- All 35 SVGs (floor map + 34 sections) pass `xmllint`; six representative local
  renders were inspected. Titles/axis notes are readable after correction.
- Final evidence contains no exploratory output, binary render, diagnostic STL,
  absolute scratch path or missing reference.
- Status vocabulary is disciplined: digital geometry does not close S0, ASM-08,
  D-06, physical driver-left/right naming, final fastener occupancy, right-deck
  feasibility, camera placement or production authorization.
- DAT-F/DAT-S/S0 are separated. KO-19 is preserved. KO-01 is carried into the deck
  boundary, UBEC shelf and X1/X2 routing. ESP32 fallback F-2 and a primary nose
  camera are rejected consistently; DN-07 remains open.
- CAD-01, CAD-02, CAD-04, CAD-06 and CAD-08 have diagnostic authorization/inputs.
  CAD-05 remains gated by S0/P1; CAD-03 by D-08/Gate A; CAD-07 by physical D-26;
  PS-10/11/14/17 remain behind their stated gates. No production CAD is authorized.

## Findings register

| ID | Severity | File | Claim | Evidence | Correction | Final status |
|---|---|---|---|---|---|---|
| F4A-01 | MEDIUM | D, I, K, T, V, `p0_05` | right-deck boundary written as positive `L >= 26` | P0 defines architecture-right/belt side as L<0 | changed to `abs(L) >= 26` and explicit right-side `L <= -26` (forward: 20) | CORRECTED |
| F4A-02 | MEDIUM | I | primary stack diagram retained pre-P0 DAT-S sign and rising-rod text; airbox prose left F-2 conditional | V/D establish S0 0…~11, rod Z 35…62 and F-2 rejection | replaced stale diagram values and rejected F-2 explicitly | CORRECTED |
| F4A-03 | LOW | `p0_03`, station CSV | comma in `nose beam, tower zone` produced a 12-column row | independent `csv.reader` schema audit | emit CSV with `csv.writer`; all rows now 11 columns | CORRECTED |
| F4A-04 | LOW | `p0_02`, `p0_04`, SVGs | long titles/notes clipped in local renders | six-file visual sample | shortened titles; added concise axis/sign notes | CORRECTED |
| F4A-05 | LOW | `stlkit`, D, V, `p0_02`, `p0_05` | toolkit named unresolved lateral sign as driver-left; 33-feature count and arm-hole output were ambiguous | frame audit; 35 rows minus two coaxial duplicates; pivot appeared in radius list | use neutral L convention; state 35 rows/33 unique; exclude pivot from arm-hole list | CORRECTED |

## Physical work carried forward

S0 and driver-side naming at P1; D-26 lock-to-lock height/sweep at ASM-08; D-06
camera calipers (and D-06b after WiFi possession); D-27 final occupancy at P1;
Servoholder/bracket consumers; body screw landing points; assembled DAT-F flatness and
screw protrusion; nose vertical dry-fit. These remain open exactly as Report V states.
