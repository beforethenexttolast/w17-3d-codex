# T · CAD-Task Specification (next session — diagnostic CAD only)

Session 2 · 2026-07-18. Input spec for the CAD session. **Scope: diagnostic-print
geometry only — no production STL is authorized by this document** (production needs
Gate P10, per part). Only parts justified by the H.4 architecture appear; gated parts
(PS-10/11/14/17) are listed with their blockers and get **no CAD** until unblocked.
Common constraints for all tasks: mount only via floor M3 slot-nut pattern (D-27 map);
no raw-model edits; parametrics named so a D-01/D-02 value change is a one-number
edit; every part embosses its PS-ID + "TP" on diagnostic variants (E-22); print
constraints per K (materials, orientation, walls).

| CAD | Part | Parent geometry | Attach | Confirmed dims | Parameterized dims | Unresolved (blockers) | Keep-outs | Fasteners/inserts | Cable features | Diagnostic acceptance | Production gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CAD-01 | **PS-13 dummy set** (print first — unblocks Gate P1) | none (free bodies) | none | battery 75×45×25; UBEC 30×14×10; ESP32 55×28×13 (+rails→44); ESC 36×32×18+fan Ø30×8; servo 40×20×40.5+horn; **(S3) every dummy carries its connector/wire-exit stubs per K PS-13: battery XT60 fwd, ESC XT60 fwd + bullets aft, UBEC leads both ends, WiFi pigtails aft, ESP32 micro-USB plug stub outboard** | WiFi dummy = **P9 60×32×12** labelled DUMMY | camera block **excluded** until D-06 | — | — | stub geometry per K PS-13 (S3) | ±0.5 mm of register values; embossed IDs | n/a — never production |
| CAD-02 | PS-01 battery tray | floor top (DAT-F), Z3L slots | 2–3 M3 slot nuts | pack limit 75×45×25; pocket P10 95×50×30 | slot span (D-27); wall offset to KO-19 (D-02); fore-aft trim ±10 | rod clearance overhead (D-26) | KO-19 ≥5; KO-01 per D-26; left shell wall (D-02) | M3×8 CSK; no inserts | fwd wire notch; strap slots; balance-lead clip | dummy pack in/out no-tools; sweeps clear | P10 after P3 + D-21 |
| CAD-03 | PS-02 ESC mount | floor, Z5R slots | 2 M3 | — (ESC EST 36×32×18) | pocket L/W/H from **D-08**; aft edge from Gate A geometry | D-08; Gate A | KO-06 ≥8; fan air ≥10 above | M3×8; strap slots | bullet groove aft; signal comb | ESC dummy seats; 10 mm gauge passes | P10 after P3/D-04 |
| CAD-04 | PS-03 UBEC shelf (+ rear deck hooks) | floor, Z3R slots | 2 M3 | UBEC EST 30×14×10 ×2 | pocket sizes (on-arrival measure); hook height ties to P4 | D-24 upsize risk | KO-19 inboard; deck above | M3×8 | lead combs both ends; cap zip point; CN-23 park | UBEC dummies seat; leads reach PS-15 | P10 after P7 (upsize known) |
| CAD-05 | PS-04 deck plate (+ PS-12 posts integrated) | PS-05 posts + PS-03 hooks | 2 M3→**inserts** front; rear hooks | plate ≈130×55×3; ESP32 footprints; P9 WiFi pocket (dummy) | inboard edge line (D-26); length (D-02); pocket final (D-06b) | **D-02, D-04, D-06b, D-26** | centreline; ESC fan bay; shell roof −5 | M3×8 into inserts | CN-07 anchor pocket + CN-16 seat beside it (S3, per DN-11); edge combs; U.FL guides; USB windows | loaded with dummies: in/out <60 s; body closes (KO-14) | P10 after P3+P6 |
| CAD-06 | PS-05 posts ×3–4 | floor slots / PS-15 shoulders / PS-03 | M3 + printed seats | Ø10–12 | **height = P4 (D-02 value)** — the one-number parametric | D-02, D-27 | UBEC leads | insert top (front pair) | — | deck plane level ±1 mm | P10 with PS-04 |
| CAD-07 | PS-06 RX carrier + antenna guide | floor, Z2L slot | 1 M3 + pad | RX EST 20×12×3 | guide length/curve to shell line (slicer view); rod offset (D-26) | D-26 | KO-01 sweep; ≥80 mm from PS-15 | M3×8 | CRSF exit + loop hook; antenna channel (open-top) | RX dummy seats; antenna geometry repeatable | P10 after P8 (D-20) |
| CAD-08 | PS-15 junction block | floor, Z2R slots | 2 M3 → **inserts** | XT60 body 16×8×8; mini-blade seat std; XT30 tap pitch | seat presence/blanks per **DN-01/DN-02**; post shoulders tie to P4 | DN-01/02; D-24 rating | KO-01 overhead (D-26); cockpit-reach line for the key | M3×8 inserts | recessed contacts; tap caps; GND post; key reachable body-on | all connectors matable by fingers; key reach demo | P10 after P7 |
| CAD-09 | PS-08 comb/clip set | floor slots + tray edges | push-fit + opt M3 | slot geometry (drawing `[2]` + D-27) | finger count/spacing; heights per route | D-10 bulk | never cover an M3 boss | optional M3 | open-top fingers; zip anchors | holds dressed loom, no span >80 mm | P10 after P6 |
| CAD-10 | PS-09 rear-tail guide | rear floor edge (left) | 1–2 M3 / clip | — | channel per **Gate A stack choice**; grommet bore | **Gate A** | KO-07/08/12 sweeps | M3 or clip | draw-string channel; end grommet; loop park | tail pull-through demo | P10 after P3 rear |
| CAD-11 | PS-16 Hall bracket | bearing-carrier region | clip | sensor TO-92; gap 1–3 mm | clip geometry per **Gate A stack**; gap shim steps 0.5 | **Gate A / D-15** | KO-08 rotation | none (clip) | lead exit + loop | gap gauge passes; ASA print | P10 after P3 rear |
| CAD-12 | PS-07 body-disconnect clip | floor slot edge at cockpit rim | clip + 1 M3 opt | CN-14 = JST-XH 4p housing dims | rim offset (slicer view) | CN family confirm (M) | KO-14 shell path | opt M3 | XH cradle + both-side strain relief | body-off ≤30 s incl. unplug | P10 after P6 |
| — | PS-10 gimbal base / PS-11 duct interface | **NO CAD** — blocked by D-06, D-07, halo-occlusion, Gate C set, DN-05/06 (RST-04) | | | | | | | | | |
| — | PS-14 speaker carrier | **NO CAD** — blocked by D-03 + DN-07 | | | | | | | | | |
| — | PS-17 USB retainer | **NO CAD** — blocked by D-11 + DN-08 | | | | | | | | | |

**(P0 — Session 4A measured inputs for these tasks; details `V` §13):** CAD-01
unchanged (proceed). CAD-02: bay length **78 mm ✔**; tray + strap must clear the
measured rod band (Z 35–62) only above Z 30; parametrize wall height for the S0
outcome. CAD-04/CAD-08: rod-safe (≤ Z 14); **anchor via shared donor screws /
free singles ((−40.0, −32.9)) / plate-clamp feet** — the free slot grid does not
exist (D-27). CAD-06 posts: parametric height unchanged, seats per the same rule.
**CAD-05 deck: HOLD final width/height until the S0 pin at Gate P1** — inboard
edge |L| ≥ 26 rear / 20 fwd (**L ≤ −26/−20** on the belt side); viable only as a narrow inboard deck at P4 ≈ 20 in the
S0 ≥ ~6 world. CAD-03 unchanged (D-08 + Gate A). Gated rows unchanged.

**Recommended CAD order:** CAD-01 (dummies, immediately — unblocks Gate P1) →
CAD-02/03/04/06/08 (lower layer, after P0 numbers land) → CAD-05/07/09 (deck +
periphery, after P1) → CAD-10/11/12 (after their gates). Every task's "unresolved"
column is a hard stop for that dimension — model it parametric, print it diagnostic,
never guess it into production.

## P0-CAD implementation result `(CAD-01/P0-CAD)`

CAD-01, CAD-02, CAD-04, CAD-06 and CAD-08 now have dependency-free parametric Python
sources under [`cad/`](cad/), controlled by one traceable CSV. Twenty individual
diagnostic STLs and six rational build-plate groups regenerate deterministically into
the repository-ignored diagnostic output folder. CAD-01 includes installed connector,
cable-bend, cooling/mount/access geometry; the Wi-Fi output is only the authorized P9
maximum and is marked `UNCONFIRMED ENVELOPE`. CAD-02 tests the 78 mm span, open
insertion/XT60/strap/balance provisions and reversible plate clamps. CAD-04 combines
the verified X=-39.99/L=-32.86 single with a clamp. CAD-06 provides H20/H26/H32 posts
without CAD-05 geometry. CAD-08 uses an open vent-safe L-frame, reversible clamps and
removable DN-01/DN-02 `OPEN` blanks. **(X review)** Its recovered fixed PS-05 shoulder
positions overlapped connector gauges; they are removed from diagnostic CAD and remain
a P1/S0-dependent placement input. CAD-06 interface fit is still exercised on PS-03.

Automated validation and visual-inspection results are in
[`cad/reports/generated_part_validation.md`](cad/reports/generated_part_validation.md)
and [`cad/reports/diagnostic_cad_manifest.md`](cad/reports/diagnostic_cad_manifest.md).
The exact physical checklist is
[`cad/reports/P1_dry_fit_checklist.md`](cad/reports/P1_dry_fit_checklist.md). No TP has
been printed, no right-deck decision has been taken, and no production row is unlocked.
CAD-03/05/07 and every explicitly gated row remain unchanged and absent.
