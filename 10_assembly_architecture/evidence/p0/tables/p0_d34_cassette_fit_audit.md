# p0_d34 — lift-out electronics cassette physical audit

This table is additive evidence. It does not revise D-28, prior placements,
conclusions, source STLs or production-CAD authorization.

## Fit result

**CONDITIONAL-GO to a full-scale repack dummy; NO production CAD/STL.**
The named lower target cells pack in plan and under the shell, but the
everything-inside claim is not closed: PDB-to-KO clearance, Wi-Fi placement
and a non-conflicting ganged dock remain open.

| Check | Arithmetic / mesh result | Confidence | Disposition |
|---|---|---|---|
| Mini-board X row | 97.36 mm clean interval; one 39 mm wall row leaves 58.36 mm before plug/wall allowance | DERIVED + ASSUMPTION install | PASS gauge |
| Mini-board steering separation | inner wall-seat faces at \|L\|=30 versus KO-01 boundary \|L\|=22 | DERIVED | 8 mm gauge; ASM-08 remains |
| Mini-board shell shoulder | worst finite S0=0 roof 27.18 mm at X+3/L-33; Z32 top +5 requires S0≥9.82 mm | DERIVED shell + ASSUMPTION cell | CONDITIONAL; only 1.18 mm surplus at S0+11 |
| PDB target vs shell | 45 X ×55 L footprint at X+1…+46/L±27.5, Z1…19; worst finite roof 35.86 at X+22/L-27.5 | DERIVED shell + TARGET envelope | PASS target gauge; 11.86 mm static-policy surplus at S0=0 |
| PDB target vs KO-01 | PDB top Z19 to provisional moving envelope start Z22 = 3 mm | DERIVED from TARGET placement | HOLD: 5 mm short of 8 mm moving policy until ASM-08 replaces KO-01 |
| Lower named stuffing | PDB target + rear charge target + insulated amp/RP1 deck | TARGET/ASSUMPTION | packs in the stepped-T gauge; real holes/exits/thermal faces remain |
| Decoupled pedestal | gimbal is floor/front-structure referenced; old cassette Z38 + 60 = Z98 arithmetic retired | architecture VERIFIED / geometry ASSUMPTION | old roof failure removed; halo/FOV/sweep/conduit open |
| Battery/ESC side bodies | no cassette plan overlap; inner faces are only 0.5/1.5 mm outside raw KO-01, not 8 mm | DERIVED plan + DOCUMENTED ESC | CONDITIONAL on measured steering, shell, pack and ESC service volumes |
| Wi-Fi + straight dock | Wi-Fi ≤60×32×12 remains uncalipered/unplaced; straight dock body projection X+42…+58/L±32 overlaps pedestal X+51…+65/L±11 | ASSUMPTION | full layout OPEN; D-06b + wrapped/notched connector dummy |
| Existing floor holes | front candidates are vent/body-seat territory; rear candidates are single/asymmetric or servo/axle contested | VERIFIED feature map / ASSUMPTION occupancy | no clean four-point pattern |

## Supplied target cells and remaining assumptions

| Cell | Audit allocation | Confidence / rule |
|---|---:|---|
| PDB-CELL | 55×45×18 mm, ~50 g; includes 2× UBEC, 1000 µF cap, divider, USB-C charge input and star ground | FIRM contents / TARGET envelope and mass; final board L/W/H/holes/exits remain ASSUMPTION and ASM-22 |
| CHG-CELL | 30×25×10 mm | TARGET envelope / SKU TBD; ASSUMPTION until selected and calipered at ASM-59 |
| AMP-CELL | 17.8×19.4×3 mm reference | purchased-board geometry ASSUMPTION; insulated Z13…16 deck and exits to ASM-22/55 |
| CASSETTE STRUCTURE | rear stem X−31…+1/L−18.5…+17.5; forward wing X+1…+42/L±43; tapered tongue X+42…+46/L±29.5; top Z19 | stepped-T ASSUMPTION gauge only |
| MINI WALL SEATS | each 39 X ×31 Z ×~13 L; X+3…+42, L±30…43, Z1…32 | MH-ET identity/envelope FIRM input; holes, live plugs and wall retention ASSUMPTION |
| DOCK BODY SEATS | XT60 20×20×12; XT30 16×16×10; 3-pin 16×10×8; XH3/4/5 12/15/18 square ×9; USB4 16×16×10; U.FL 12×12×6 | family/count FIRM; every body allocation ASSUMPTION pending terminated-part calipers |
| PEDESTAL / CONDUIT | foot/core X+51…+65/L±11; 10×18 clear, 2 mm trial wall →14×22 outer; ≥25 mm lower slack | ASSUMPTION; sequential USB4/servo plug pull-through, bend and wall coupon at CAS-09 |

## Mass / balance sensitivity

The prior midpoint remains 1782 g, 35.0% front / 65.0% rear and Z-CG 22.2 mm.
The updated ledger replaces the old 52.5 g PWR midpoint with the supplied
~50 g PDB TARGET mass at X+23.5/Z10; it does not double-count the UBECs/cap.
Let C be charge-module + printed cassette/dock mass not otherwise in the
ledger at X+10/Z10, and P be added pedestal mass at X+35/Z25:

- before C/P: 1778.4 g, 36.61% front / 63.39% rear, Z-CG 21.33 mm;
- illustrative C=25 g and P=20 g (**ASSUMPTION, not mass claims**): 1823.4 g, 36.88% front / 63.12% rear, Z-CG 21.22 mm;
- exact formula: total=1778.4+C+P; X moment=−7341.25+10C+35P;
  Z moment=37933.5+10C+25P (g·mm); front%=100·(X-CG+90.9)/237.

The illustration remains within the planning uncertainty and does not approve
balance. Physical PDB/charge/cassette/pedestal weights and four-corner scales
own the final result.

## Mounting and umbilical

- Existing holes alone do not make a clean, stable, serviceable four-point pattern.
- The former X−15/+35, L±12 service-boss pattern is now REJECTED: its rear
  pair lies inside the charge target and its front pair inside the PDB target.
  Hiding service screws below modules would defeat lift-out access.
- CAS-07 must establish a new reversible external saddle/clamp pattern with a
  transparent full-stack dummy. M3×5 inserts remain coupon-gated; donor drilling
  remains prohibited. No replacement coordinates are inferred here.
- The fixed hollow pedestal carries one shielded USB4 + two 3-pin servo leads
  through a 10×18 clear target section to an R1/R2 exit below Z22.
- Firm dock minimum: XT60×1, XT30×2, 3-pin servo×5, XH3×3 and shielded USB4×1;
  plus auxiliary blower/speaker seats. Internal seats reserve XH4, XH3, XH5
  and 2×U.FL bodies. A straight access-edge dock overlaps the pedestal;
  only a full-size stepped/wrapped dummy may select the final topology.

## Reproducibility

- Registered 2024 shell loaded through p0_03; S0=0 is the lower bound.
- No STL was written, transformed in place, relieved or declared production-ready.
- PDB contents, mini identity/envelope and connector map are supplied inputs.
  PDB/charge final geometry, connector bodies, install retention, pedestal
  and cassette structure remain ASSUMPTION/DEFER with named ASM checks.
