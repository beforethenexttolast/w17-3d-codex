# U · Session 3 — Skeptical Review Findings & Readiness Decision

Session 3 · 2026-07-18 · independent senior design-review pass over the Session 2
architecture set (Reports H–T) under the Session-1/1.5 evidence base (A–G). Method:
every report read in full; the H.3 weighted comparison and the L.4 rail budgets
**recomputed independently**; the BOM (`../docs/bill_of_materials_v2.md`) re-read at
the lines Session 2 cites; all 48 ASM steps and all 19 Q procedures walked in order;
the full CN/H/PS/DN/D/E/Z ID space swept mechanically for orphans and collisions.
Corrections were applied **in place**, each tagged "(S3)". Nothing was committed
(by design). No measurement was invented; no production CAD/STL was created.

## What was independently re-verified and held up

- **H.3 arithmetic** reproduces exactly: weights sum 99 (max 495); A = 295, B = 400,
  C = 267, D = 326. Two criterion pairs overlap ("low measurement dependency" w8 +
  "rework risk after D-01/D-02" w7; "serviceability" w9 + "access" w8) — but the
  double-count *hurts* the winner: zeroing both measurement-dependency criteria gives
  A 235 / **B 355** / C 237 / D 304. The Hybrid B+D selection is robust to the
  scoring defect and is evidence-based, not narrative preference (F3-15).
- **L.4 arithmetic** reproduces exactly: Rail A 2.26 A typ / 6.02 A worst-case;
  Rail B 1.55 A typ / 5.65 A all-stall / ≈4.45 A realistic. The "worst-case exceeds
  the 5 A UBEC" reading (E-23) is correct and correctly deferred to D-24.
- **ID space is clean**: CN-01…CN-25 (CN-03 unused, CN-16 was unused and is now
  assigned by S3), H-01…H-11, PS-01…PS-17, DN-01…DN-10 (now …DN-11), D-01…D-27,
  E-01…E-25 (now …E-26) — used consistently across I/J/K/L/M/N/P/Q/R/S/T; the
  CN-DECK=CN-07 / CN-BODY=CN-14 aliases are declared in M.
- **Assembly order** (ASM-01…48): servo powered+centred (07) before linkage closure
  (08); rear LED tail pre-routed (13) before rear-stack closure — and this rule is
  present in *every* relevant document (A §3, K PS-09, N.1-4, P ASM-13, J, Q);
  lower layer bench-tested (19) before the deck (20–22); everything bench-verified
  (32) before shell burial (33); D-24 (36) before final harness cut (P9). No
  ordering defect found beyond the two gate-prerequisite gaps below.
- **Q's no-desolder claim** holds for 18 of 19 procedures once F3-01 is corrected;
  the WiFi-module swap is an honestly documented repair-class exception.
- **≥150 mm antenna separation** is geometrically realistic (Z2L forward antenna tip
  to deck-rear posts is a fore-aft run of roughly the chassis' middle half), and O.2
  correctly separates antenna-to-antenna, antenna-to-UBEC (≥80 mm) and
  antenna-to-metal (≥40 mm) requirements. Paint attenuation is already in D-20.
- **The open-spine principle** (H.1.2/I): held consistently everywhere — no report
  places structure or harness across the centreline except at X1/X2.
- **RST-01…07 restrictions** from Session 1.5: honoured throughout (heights
  PROVISIONAL, airbox stack demoted to fallback F-2, KO-19 placed from the start,
  nose unallocated, D-24 gating explicit, WiFi dummy discipline, no gate reopened).
- **P0 sufficiency for CAD-01**: CAD-01 (dummy set) needs only Report-B register
  envelopes — none of its inputs waits on P0; P0's D-01/02/04/25/26/27/06/03 cover
  every dimension the lower-layer diagnostic CAD consumes. No missing measurement
  found that would cause avoidable redesign at the dummy/diagnostic stage.

## Findings register

Severity: CRITICAL / HIGH / MEDIUM / LOW / EDITORIAL. Status: CORRECTED (fix applied
in place, tagged S3) · NOTED (review record only, no doc change needed).

| ID | Sev | Subsystem | Files | Finding | Evidence | Consequence | Correction | Remaining validation | Status |
|---|---|---|---|---|---|---|---|---|---|
| F3-01 | **HIGH** | video / service / harness | M, N, Q, J, K, T, P, S, E | **The camera↔WiFi USB D± run crossed the MOD-CAM/MOD-DECK boundary solder-only.** M.1's own rule says every module boundary is a connector, yet the BOM solder note was carried as "inside the gimbal module" while VID-WIFI sits on the removable deck and the camera in MOD-CAM. Q's deck-out drill (<60 s, "unplug CN-07 + U.FL → lift") and the camera-module one-piece removal were both physically impossible as written — the soldered run tethers the two modules. | BOM v2 "Camera ↔ WiFi-module solder: D+→DP, D−→DM, GND→GND"; M.1 module table; N H-07 "removal: with MOD-CAM" vs Q deck-out row | every deck service (UBEC swap, lower-layer access, board swap) degrades into un-dressing or stressing a soldered USB run; Gate P10 timed drills unpassable | **CN-16** defined (M.2): latched signal-grade 3–4-pos boundary connector at the **deck fwd-inboard edge beside the CN-07 anchor** — deck-out stays one-station; long run stays dressed with the chassis/camera side. Registered as owner decision **DN-11** (S) + risk **E-26** (E) since it amends a BOM bench note; USB-2.0 integrity bench-check added to Gate P4 (R). M.1/N/Q/J/K/T/P updated coherently. | DN-11 owner ratification; USB link integrity at Gate P4 (fallback: deck+camera documented as one combined service unit) | CORRECTED |
| F3-02 | **HIGH** | validation gates / power | R, P, D | **Gate P7 could "close" D-24 with the WiFi dummy installed** (P6 explicitly allows the dummy; P7 required only "P6; battery on hand"), after which P9 cuts the final harness from a Rail A measurement that lacks the single largest Rail A load (~2 A peak). P8 required the real module only "for the RF half" although the WiFi is also the top deck heat source. | R P7/P8 prerequisite cells; ASM-36 states list; L.4 Rail A table | final harness gauges, DN-01 fuse rating and DN-04 LED cap set from data missing ~⅓ of Rail A worst-case; thermal pass on a dummy is meaningless at the WiFi points | R P7 prerequisites now require the **real VID-WIFI**; ASM-36 gains the same prereq; R P8 wording extended to the WiFi-related D-19 thermal points | possession + D-06b (RST-06 unchanged) | CORRECTED |
| F3-03 | MEDIUM | connectors | M | **CN-07's provisional 4 A exceeds a single JST-XH contact (~3 A)**, and CRSF needs TX+RX (2 conductors, as CN-19 itself shows) — the "~10 conductor" bank was undersized on both counts. | M.2 CN-07 row vs XH family rating; CN-19 = 4-wire CRSF | overheated power pin at the highest-cycle connector on the car; or a missing CRSF conductor discovered at ASM-22 | CN-07 respecified: **2× 5 V + 2× GND**, CRSF TX+RX, ~12 positions; Micro-Fit 3.0 (5 A/pin) named as the mandatory alternative if D-24 confirms >3 A per power pin | D-24 current split; Gate P9 final family | CORRECTED |
| F3-04 | MEDIUM | power / measurement | D, P, L, R | **D-24 measured only the UBEC outputs (CN-23), but the DN-01 fuse rates on the 7.4 V input side** (input ≈ ΣP_out/V_bat/η ≈ 8–9 A pathological, 6–7 A realistic — the 7.5 A placeholder can nuisance-trip); the state matrix lacked cold-boot inrush and a combined-plausible-peak state; the D-24 table row was also column-shifted (Tool cell missing). | L.4 totals recomputed; D-24 row structure; DN-01(b) text | fuse rated from the wrong side of the converters; startup transients never captured; table row mis-parsed | D-24 row rebuilt (9 columns): full state matrix, **PS-15 input-side loop**, scope for <10 ms events, test-equipment grounding note; ASM-36 and R P7 updated to match; L.3.1 documents the input-side rating basis | D-24 execution (P7) | CORRECTED |
| F3-05 | MEDIUM | electrical safety | L | **DN-01(b)'s claim "protects the fine-wire loom" was half-true**: the accessory fuse protects the input branch; the Rail A/B **output** looms rely on unverified UBEC current limiting. Fuse-blow behaviour (both rails dead, motor branch live) is safe only if the ESC fails to neutral — asserted nowhere. **The "loop key" was a product name, not a spec.** | L.3 DN-01/DN-02 rows; T1 diagram | a rail-output short could burn 22–24 AWG wiring with the fuse intact; an under-specified key could be un-pullable, loose, or expose live contacts | New **L.3.1**: what the fuse does/doesn't protect + per-rail polyfuse amendment path + UBEC overload observation added to D-24; ESC signal-loss = motor-stop check added to Gate P4; loop-key converted to explicit electrical/mechanical requirements (XT60-class ≥30 A, dead-when-removed male key, recessed female seat, guard collar, T-flag, ≤2 s body-on pull, kills entire battery feed, in-last/out-first) | D-24 overload observation; P4 ESC behaviour check; DN-01/02 owner decisions | CORRECTED |
| F3-06 | MEDIUM | electrical safety / service | O, Q, L, R | **USB back-powering unaddressed**: plugging a laptop into an ESP32 USB (deck windows or DN-08 pigtails) can back-feed Rail A through the dev board's USB diode — with VID-WIFI on that rail (~2 A) the laptop port and diode are both overloaded. | O.4 table (absence); DN-08 route; dev-board topology | damaged laptop port / dev board during routine flashing | Rule added to O.4 + Q programming row + L.3.1: **rails OFF (key out) during USB sessions** unless dev-board isolation is verified at Gate P4 | P4 diode check | CORRECTED |
| F3-07 | MEDIUM | mass & balance | I, K | **The balance ledger did not add its own columns**: right 140–195 g vs left 100–140 g (speaker mass is DN-07-gated, not bankable) → **~30–60 g right-heavy**, partly at deck height — and the only designed trim (PS-01 ±10 mm slots) is fore-aft, useless for L/R. D-21 could detect the imbalance but had no correction path. | I.4 figures summed; PS-01 spec | permanent lateral CG bias + slightly raised right CG on an F1-handling-sensitive car, discovered at D-21 with no designed fix | I.4 rewritten with the sums and three named L/R trim paths (DN-07 weighting, **PS-01 outboard ballast land** — added to K, pack-mass selection); D-21 stays the detector | D-21 measured masses (no balance claim made without them) | CORRECTED |
| F3-08 | MEDIUM | RF / service | J, I, K | **The VID-ANT "ZB flank" fallback breaks two standing rules at once**: shell-mounted whips tether the body through U.FL pigtails rated ~30 mates (Q wear list) at every body-off, violating the one-disconnect body rule. | J VID-ANT row; I ZB row; M/Q U.FL notes | body removal (the most frequent service action) would consume U.FL life and risk the most fragile connector on the car | Fallback changed in J/I/K to a **standalone chassis-mounted PS-12 post pair** (also serving fallback Architecture A); shell-mount explicitly rejected | D-06b + D-20 validate the primary posts | CORRECTED |
| F3-09 | MEDIUM | fallback architecture | H (tagged addendum), K | **"Same harness topology, nothing else re-architects" overstated the fallback**: graph yes, but MOD-DECK's one-disconnect service property disappears, CN-22 grows from ~70 mm to near-full-chassis, H-07 re-routes, PS-12 needs the standalone variant, and the "junction shifts inboard-front" move interacts with KO-01/KO-05 and the DN-02 key's cockpit reach. | H.4 fallback text vs M/N/K geometry | fallback trigger (P2s < ~40) would be pulled expecting a remount and would meet un-planned harness/service rework | S3 addendum in H.4 names all four deltas + the PS-15 re-verification duty; PS-12 fallback variant added to K | only if D-01/D-02 trigger fallback A | CORRECTED |
| F3-10 | MEDIUM | CAD-01 dummies | K, T | **Dummies were body-only where connector/wire geometry decides fit**: battery XT60 exit, ESC bullet/XT60 exits, UBEC leads, WiFi pigtails, ESP32 USB plug (permanently occupied under the DN-08 pigtail route) were all absent from PS-13/CAD-01. | K PS-13 set list; B's own install-envelope rule ("a raw bounding box is never the space needed") | Gate P1 could pass a layout the real connector geometry fails — exactly the avoidable-redesign class P1 exists to prevent | Stub rule added to K PS-13 and T CAD-01: every dummy carries its connector/wire-exit stubs with bend allowances | Gate P1 executes with stubs | CORRECTED |
| F3-11 | LOW | RF coexistence | O | **ESP32 onboard 2.4 GHz radios absent from the coexistence matrix** — two WiFi/BT-capable DevKits sit on the deck near the CRSF run; their intended radio state was declared nowhere. | O.2 (absence); B CTL rows | if firmware ever enables an ESP32 radio, an untested third 2.4 GHz emitter appears next to the RC link | O.2 bullet: radio state must be declared by firmware config; if in use, joins the D-20 matrix | D-20 (only if radios used) | CORRECTED |
| F3-12 | LOW | routing | N | **CN-21's centreline crossing was unassigned** for the DN-07 sidepod-left speaker outcome (amp is on the right deck, speaker at Z4L). | N.2 H-06 row; M CN-21 60–150 mm | an undefined crossing invites an ad-hoc rat's-nest run at ASM-22 | H-06 row now routes CN-21 across at **X2** if DN-07 selects Z4L | D-03/DN-07 | CORRECTED |
| F3-13 | LOW | process / gates | R | **R P1 said the dummy dry-fit "unlocks diagnostic CAD" while T's order starts lower-layer CAD "after P0"** — a genuine sequencing contradiction between the gate table and the CAD spec. | R P1 unlock cell vs T order line | a CAD session would not know its own start condition | Harmonized: parametric CAD *modelling* may begin at P0; P1 unlocks diagnostic **printing** (P2) — matching the parts' parametric design intent | — | CORRECTED |
| F3-14 | LOW | thermal validation | O | **The chimney was validated only by outcome (IR temps)**, with no flow-direction observation — a recirculating or dead airbox channel could pass a short static test and fail on a long drive. | O.1 test procedure | false thermal pass at P8 | Thread/tissue tell-tale check at every named inlet/exhaust added to the O.1 procedure; a dead/reversed airbox tell-tale fails the gate even if temps pass | D-19 at P8 | CORRECTED |
| F3-15 | LOW | architecture selection | — (review record) | **H.3 double-counts measurement-dependency** (w8 + w7 rework-risk) and partially overlaps serviceability/access — but sensitivity analysis shows the defect penalizes the *loser* side: B wins 355 vs 304/237/235 even with both criteria zeroed. Selection stands. | recomputation (this report, §re-verified) | none — recorded so future re-scoring (P0 fail loop) doesn't inherit the double-count unknowingly | none needed in H (frozen); re-score after D-01/D-02, if triggered, should merge the two criteria | only on the P0-fail re-score path | NOTED |
| F3-16 | EDITORIAL | measurement plan | D | D-24's table row was column-shifted (Tool cell missing — accuracy sat in Tool, the why-text in Accuracy). | D row parse | mis-read row | fixed as part of the F3-04 rebuild | — | CORRECTED |
| F3-17 | EDITORIAL | assembly manual | P | ASM-02 required "D-26 done" without naming the stage — D-26 is two-stage (slicer at P0, physical confirm at ASM-08), so the bare wording read as circular. | D-26 row; ASM-08 | reader loops at ASM-02 | "(slicer stage — physical confirm lands at ASM-08)" clarifier added | ASM-08 closes the physical stage | CORRECTED |
| F3-18 | EDITORIAL | dry-fit text | H (tagged fix) | H.1.3 "fails min-P2s (55)" mislabeled the bound — 55 is the P2s **maximum**; the (correct, honest) point is that the worst-case stack fails even the best-case ceiling. | H.1.1 P2s row | reader misjudges how tight the deck really is | inline S3 label fix in H.1.3 | D-02 resolves P2s | CORRECTED |

**Printed-support review (area 5) — no parts rejected.** Each of PS-01…PS-17 traces to
a unique named problem; the overengineering candidates were already rejected by K's own
"REJECTED structure" list (spine, cage, bridge deck, left deck, LED-controller carrier,
bulkhead wall); PS-12 is already folded into PS-04, PS-05 already flagged for merging
into PS-03/PS-15, and the four speculative parts (PS-10/11/14/17) are already
CAD-blocked behind their gates. Commercial alternatives (standoffs, adhesive tie
mounts, foam) lose to the M3 slot-nut floor pattern on serviceability and heat;
PS-13 remains diagnostic-only. The 17-part count is justified as specified.

## Subsystem readiness matrix

| Subsystem | Status | Governing gates/notes |
|---|---|---|
| Recommended architecture (Hybrid B+D) | **READY FOR P0 MEASUREMENT** | selection verified (F3-15); P2s/D-26 decide the deck at P0/P1 |
| Fallback architecture (single-level A) | **READY FOR P0 MEASUREMENT** | viable with the F3-09 deltas now explicit |
| Battery zone (Z3L-L0, PS-01) | **READY FOR P0 MEASUREMENT** | D-01/D-02/D-26/D-27; purchase stays behind D-01 |
| ESC zone (Z5R, PS-02) | **BLOCKED BY MEASUREMENT** (D-08, Gate A edge) | dummy participates in P1 meanwhile |
| UBEC mounting (Z3R-L0, PS-03) | **READY FOR CAD-01 DUMMY WORK** | D-24 upsize risk kept parametric |
| Right-side removable deck (PS-04/05) | **READY FOR CAD-01 DUMMY WORK** | genuinely marginal (48 vs P2s≤55 expected) — exactly what P0/P1 exist to decide; fallback trigger defined |
| ESP32 placement (deck, flat) | **READY FOR CAD-01 DUMMY WORK** | D-02/D-04/D-26; USB stub added (F3-10) |
| RC receiver placement (Z2L, PS-06) | **READY FOR CAD-01 DUMMY WORK** | D-26/D-20 |
| Camera/gimbal interface (Z8, PS-10/11) | **BLOCKED BY COMPONENT SELECTION + MEASUREMENT** | DN-05/06 owner, D-06/D-07, halo check, Gate C — correctly CAD-blocked |
| Nose region (Z1) | **BLOCKED BY MEASUREMENT** (D-25) | correctly unallocated; crash zone E-24 |
| Steering & KO-19 | **READY FOR P0 MEASUREMENT** | D-26 slicer stage in P0; D-09 residual on arrival |
| Printed supports (set) | **READY FOR DIAGNOSTIC CAD** per T order | production locked behind P10 per part |
| Power topology (T1) | **READY FOR ELECTRICAL BENCH INTEGRATION** (P4) once parts arrive | budget PROVISIONAL by design until D-24 |
| Fuse (DN-01) | **PROVISIONAL** — owner decision + D-24 rating | input-side basis now stated (F3-04/05) |
| Main disconnect (DN-02) | **PROVISIONAL** — owner decision; spec now explicit (F3-05) | seat printed either way |
| Harness architecture (M) | **READY FOR CAD-01 DUMMY WORK** after F3-01/03 corrections | final at P9 |
| Cable routing (N) | **READY FOR CAD-01 DUMMY WORK** | D-10/D-26 validate; crossings defined incl. CN-21 |
| Thermal path | **PROVISIONAL** | design intent + named test (now incl. flow tell-tale); resolved only at P8 with real WiFi |
| RF architecture | **PROVISIONAL** | plan is sound; resolved at D-20/P8 with real module; ESP32 radios now in matrix |
| Assembly manual (P) | **READY** (supports P0→P10 execution) | F3-17 fixed; fallback deltas referenced via H addendum |
| Service procedures (Q) | **READY** after F3-01 correction | timed drills demonstrable at ASM-47 |
| CAD-01 dummy set | **READY FOR CAD-01 DUMMY WORK — start now** | needs no P0 input; stubs added (F3-10) |

## Final decision

### Verdict: **APPROVED FOR P0 + CAD-01**

The Session 2 architecture is internally credible: the selection survives independent
recomputation and a sensitivity check against its own scoring defect; every named
unknown (D-01…D-27) carries a method, datums, accuracy, affected decision and a
fail/redesign path; the gate chain P0→P10 is acyclic and, after the two S3
prerequisite fixes, cannot finalize hardware from dummy-derived data. The two
substantive design conflicts found (F3-01 camera-USB boundary, F3-08 antenna
fallback) are corrected in place and neither touches P0 measurement work or the
dummy-envelope set. CAD-01 requires no measurement at all and may start immediately;
P0 may start in the same slicer sitting. The corrections that remain open are
**owner decisions** (DN-01/02/05/06/07/08/11) and **arrival-dependent measurements**
— none is a reason to withhold P0 or CAD-01.

Conditions carried (not blockers): DN-11 owner ratification before Gate P4 wiring;
real-VID-WIFI prerequisites on P7/P8 stand; no balance claim before D-21; no
production CAD/STL before Gate P10 (unchanged).
