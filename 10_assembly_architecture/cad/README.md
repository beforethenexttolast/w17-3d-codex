# W17 P0 diagnostic CAD

`(CAD-01/P0-CAD)` This directory contains reproducible, text-controlled diagnostic
geometry for only the P0-authorized tasks: CAD-01, CAD-02, CAD-04, CAD-06 and CAD-08.
It contains no production vehicle geometry and no donor STL import path.

## System and structure

The repository had no OpenSCAD/FreeCAD source convention and neither tool is installed
locally. The existing geometry convention is dependency-free Python operating in
millimetres (`evidence/scripts/stlkit.py` and the P0 scripts), so this implementation
extends that convention:

```text
cad/
├── parameters/cad_parameters.csv        authoritative parameters and status/source trace
├── sources/lib/meshkit.py               deterministic closed-shell primitives + PNG renderer
├── sources/parts.py                     authorized diagnostic part definitions
├── sources/generate.py                  STL/build-plate generation
├── sources/validate.py                  automated geometry/policy validation
├── reports/diagnostic_cad_manifest.md   implementation and output manifest
├── reports/generated_part_validation.md generated validation results
├── reports/P1_dry_fit_checklist.md      exact physical dry-fit evidence checklist
├── reports/X_diagnostic_cad_review.md   independent recovery/finalization review
└── generated/
    ├── stl/                              ignored diagnostic binaries
    └── renders/                          ignored local visual-inspection PNGs
```

The CSV is the single source of dimensional values. Unknown values remain rows with
`provisional`, `expected`, `minimum`, `maximum`, or physical-dependency status; source
code derives layout positions from those named parameters. Dimensionless fractions in
the source only distribute diagnostic ribs, labels and access gauges inside the named
envelopes.

## Generate and validate

Run from the repository root:

```bash
python3 10_assembly_architecture/cad/sources/generate.py
python3 10_assembly_architecture/cad/sources/validate.py
```

Generation deletes only stale `*.stl` files inside the fixed diagnostic output folder,
deletes stale `*.png` files inside the fixed render folder, then writes the exact
authorized sets. Validation checks syntax-independent mesh facts,
parameter coverage, task whitelist, non-empty geometry, millimetre headers, bounding
boxes, bed orientation, triangle area, closed/oriented edge incidence, D-26 height,
build-plate membership/count/no-overlap/fit, donor-hash inequality, the exact 19-render
set, stale outputs and byte-for-byte deterministic regeneration.

## Binary policy

The repository-wide `.gitignore` excludes `*.stl` and `*.png`. Generated binaries stay
local and do not appear in normal Git diffs; the tracked text reports carry their names,
bounding boxes, feature audit and truncated SHA-256 values. Do not force-add them.

## Pre-print limitation

No Boolean mesh engine or Bambu Studio CLI is installed. Primitive shells are closed and
consistently oriented, but labels and some intersecting diagnostic primitives are not
Boolean-unioned. The automated report exposes strict `>2` edge-incidence counts. Inspect
and repair/union in Bambu Studio before any TP print; a successful local STL export alone
is not a print authorization.

## Final review

The independent recovery/finalization audit is
[`reports/X_diagnostic_cad_review.md`](reports/X_diagnostic_cad_review.md). Its verdict is
**DIAGNOSTIC CAD VERIFIED WITH MINOR CORRECTIONS**: the source/output set is complete for
the authorized diagnostic scope, with Bambu Studio preflight and physical P1 still open.
