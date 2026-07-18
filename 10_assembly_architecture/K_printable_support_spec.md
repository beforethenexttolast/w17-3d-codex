# K · Printable Internal-Support Specification

Session 2 · 2026-07-18. Parts required by the H.4 architecture and the I zone plan.
**No production STL is created in this session** — this is the engineering spec that
feeds `T_cad_task_spec.md` (diagnostic CAD only). Confidence tags per
[`README.md`](README.md). Envelopes are allocations (min/expected/max where uncertain),
not final dimensions.

**Design rules (all parts):**
- Mount to the floor only via the existing **M3 slot-nut pattern** (drawing `[2]`) —
  no new holes in donor parts, no raw-model edits. D-27 (added S2) maps which slots
  are free after the mechanical build. **(P0) The digital D-27 map shows the free
  grid mostly does NOT exist** (one free M3 feature per side bay; none in the Z2R
  patch — `V` §10): supports may therefore also **share donor screw stacks or use
  plate-clamp/edge feet** — the no-new-holes rule is unchanged. PS-04's inboard
  edge gets the measured KO-01 number: **|L| ≥ 26 rear / ≥ 20 fwd at deck heights**
  (**L ≤ −26/−20** on the architecture-right belt side);
  PS-01 is parametrized for the S0 outcome (pack top ~28 passes under the rod band).
- Repeated-service fasteners (≥3 cycles) get **heat-set M3×5 inserts** (HW-INSERT,
  ASSEMBLY_NOTES plastic-thread rule); single-assembly joints may self-thread.
- Print material default **PETG** (warm chassis interior, near-heat brackets in
  **ASA**); walls ≥3 perimeters on load paths; no part relies on bridging over a
  cable channel (channels open-topped).
- Every part must be removable with hex drivers 1.5/2/2.5 without desoldering
  (Q, service rule).
- Status ladder: **CONCEPT → DIAG-CAD (T) → TP diagnostic print → Gate P2/P3 →
  production authorization (Gate P10)**. Nothing here is past CONCEPT today.

---

## K.1 Part register (summary)

| ID | Name | Zone | Solves | Status | Blocking measurements |
|---|---|---|---|---|---|
| PS-01 | Battery tray + restraint | Z3L-L0 | E-04/E-08: locate + restrain pack, protect from floor hardware | CONCEPT — diagnostic CAD allowed | D-01, D-02, D-26, D-27 |
| PS-02 | ESC mount | Z5R | E-01: ESC off bare floor, fan clearance, wire exits | CONCEPT — diag CAD allowed | D-08, Gate A edge |
| PS-03 | UBEC shelf (pocket row) | Z3R-L0 | E-01: regulators located, deck understructure | CONCEPT — diag CAD allowed | D-02, D-24 (upsize risk) |
| PS-04 | Removable electronics deck | Z3R-L1 | E-01/E-03: carries CTL-E1/E2, AUD-AMP, VID-WIFI; one-module service | CONCEPT — diag CAD allowed | D-02, D-04, D-06b, D-26 |
| PS-05 | Deck posts (×3–4) | Z2R/Z3R | deck height + removability | CONCEPT (may merge into PS-03/PS-15) | D-02, D-27 |
| PS-06 | RX carrier + antenna guide | Z2L | E-06/KO-17: RX located, antenna geometry repeatable | CONCEPT — diag CAD allowed | D-20, D-26 |
| PS-07 | Body-disconnect bulkhead clip | cockpit rim | ZB rule: one-connector body lift-off | CONCEPT | CN-BODY family pick (M) |
| PS-08 | Cable combs / floor clips (set) | edges | E-15: loom restraint, abrasion, moving-axis clearance | CONCEPT — diag CAD allowed | D-10 |
| PS-09 | Rear-tail guide + strain relief | Z5→Z7 | R-09: LED tail + Hall + DRS routed before rear stack closes | CONCEPT | Gate A path pick |
| PS-10 | Gimbal module base | Z8 | common Option-A/B camera interface | CONCEPT — **gated** | D-06, D-07, halo check |
| PS-11 | Blower/duct interface mount | Z8 | Gate C duct (from `camera_blower_duct.scad`) held to PS-10 | CONCEPT — **gated** | Gate C set |
| PS-12 | 5.8 GHz antenna posts ×2 | deck rear | KO-17: antenna position + pigtail reach | CONCEPT (integrate into PS-04) | D-06b, D-20 |
| PS-13 | Dummy-envelope block set | — | Gate P1 dry-fit (RST-06 WiFi dummy P9 among them) | **diagnostic print allowed now** | none (that's the point) |
| PS-14 | Speaker carrier | Z4L | AUD-SPK port + isolation | CONCEPT — **gated** | D-03, DN-07 |
| PS-15 | Power junction block | Z2R | R-07: XT60 inlet, Y, fuse/disconnect seat, XT30 taps, test points | CONCEPT — diag CAD allowed | DN-01/02, D-24 |
| PS-16 | Hall sensor bracket | rear axle | SNS-HALL gap 1–3 mm in hot pocket | CONCEPT | D-15/Gate A, magnet station |
| PS-17 | USB service-pigtail retainer | cockpit rim | E-09/D-11 programming access | CONCEPT — **gated** | D-11, DN-08 |

**REJECTED structure (Phase-3 discipline — no problem, no part):** central spine
(centreline is occupied — H.1.2); full internal cage (duplicates the 8 mm floor's
stiffness for mass/print cost); full-width bridge deck (crosses KO-01 below P7max);
left-side deck (would bury the battery, E-08); dedicated LED-controller carrier (no
such device — WS2812 is driven by CTL-E2 directly); connector bulkhead wall across
the chassis (one CN-BODY clip suffices; a wall adds mass and blocks airflow).

---

## K.2 Detailed specifications

### PS-01 — Battery tray + restraint
- **Purpose / problem:** locate PWR-BAT repeatably at Z3L-L0, keep the pack off the
  M3 slot-nut heads, restrain it against ~20 g forward crash load (O §vib), give the
  strap an anchor, and carry the ±10 mm fore-aft trim slots used at D-21 balance.
- **Envelope:** plate ~100 × 55 × 3 (DAT-T ≈ 3); end walls ~12 tall fore/aft; total
  allocation stays inside P10 (95 × 50 × 30 pocket + wall thickness).
- **Datum:** DAT-F. **Mounts:** 2–3 floor M3 slots (D-27). **Carries:** pack + strap;
  XT60 lead exits forward; balance-lead park clip on the outboard wall.
- **Clearances:** ≥5 mm to KO-19 inboard; ≥8 mm below the KO-01 rod line (D-26);
  left shell wall per D-02.
- **Fasteners:** M3×8 countersunk into slot nuts; **no inserts** (tray itself rarely
  removed; the pack lifts out of it). Strap: 20 mm hook-and-loop through printed slots.
- **Material/print:** PETG, plate printed flat (layers parallel to load), 3 walls,
  ≥25% infill; strap slots chamfered (edge protection).
- **Heat/vibration:** mild/strapped mass — end walls take the crash load along layers.
- **Cable features:** forward wire exit notch + one PS-08-style comb finger.
- **(S3) Ballast land:** the outboard wall carries a flat land for self-adhesive 5 g
  wheel-weight strips — the designed **L/R** trim path (I.4); the ±10 mm slots trim
  F/R only.
- **Access/removal:** pack lifts out with strap open, body-off; tray removal = 2–3 M3.
- **Mass concern:** ~15 g target. **Diagnostic status:** TP print allowed after D-01/D-02
  numbers exist (Gate P2). **Production blocker:** Gate P3 + D-21 trim confirmed.
- **Acceptance (diagnostic):** dummy pack (PS-13) clicks in/out without tools; no contact
  with KO-19/rod dummy at full steering sweep; strap reachable body-off.

### PS-02 — ESC mount
- **Purpose:** hold DRV-ESC at Z5R with fan up and ≥10 mm free air above, decouple it
  from floor heat paths, and fix the wire-exit geometry (XT60 fwd, bullets aft, signal up-fwd).
- **Envelope:** within P11 (50 × 42 × 40 expected). **Datum:** DAT-F.
- **Mounts:** 2 floor slots (D-27); ESC held by strap-over + perimeter lip (no clamping
  of the case; fan intake unobstructed laterally).
- **Clearances:** ≥8 mm to KO-06 shock band inboard; ≥10 mm above fan (KO-14 check);
  aft clearance to KO-08/09 per Gate A geometry.
- **Fasteners:** M3×8 + slot nuts; strap. **Material:** **ASA** (adjacent to the hot rear
  pocket, E-05), flat print, 4 walls.
- **Cable features:** bullet-wire dressing groove aft; signal-wire comb up the inboard lip.
- **Removal:** strap off → ESC out with connectors; mount stays. **Mass:** ~12 g.
- **Blockers:** D-08 (real ESC dims) before diagnostic TP fit; Gate A before the aft
  edge is final. **Acceptance:** ESC dummy seats; fan gap gauge (10 mm) passes body-on
  (Gate P3/D-04).

### PS-03 — UBEC shelf
- **Purpose:** pocket row for PWR-UBEC-A/B (+ PWR-CAP, SNS-DIV solder joints), forming
  the lower half of the right bay and the landing for two PS-05 posts.
- **Envelope:** ~75 × 42 × 14. **Datum:** DAT-F. **Mounts:** 2 floor slots.
- **Clearances:** deck above at P4 (≥6 mm over UBEC bodies for airflow); KO-19 inboard.
- **Fasteners:** M3×8 + slot nuts; UBECs retained by pocket ribs + one zip point each
  (their leads are the strain relief risk — combs at both ends).
- **Material:** PETG, flat, 3 walls. **Heat:** UBECs warm at load — pocket floor slotted
  open for convection (D-19 watches them). **Mass:** ~10 g.
- **Removal:** deck off (2 fasteners) → UBECs lift out of ribs. **Blockers:** D-02;
  D-24 outcome may upsize a UBEC → pocket parametric. **Acceptance:** UBEC dummies seat;
  leads reach PS-15 without crossing the centreline at floor level outside station X1 (N).

### PS-04 — Removable electronics deck
- **Purpose:** single service module carrying CTL-E1, CTL-E2 (flat, fore-aft row, USB
  outboard-right), AUD-AMP, VID-WIFI rear slot, 5.8 GHz antenna roots (PS-12 integrated),
  and the CN-DECK disconnect anchor. The E-01 core deliverable.
- **Envelope:** plate ~130 × 55 × 3 at DAT-D = P4 (20–32); build height above deck ≤ P5.
  **Top of tallest component must clear shell by ≥5 mm — validated at Gate P1/P3, D-04.**
- **Datum:** DAT-D (referenced to DAT-F via posts; **PROVISIONAL until D-01/D-02, RST-01**).
- **Mounts:** 3–4 PS-05 posts; 2 front fasteners are M3 into **heat-set inserts**
  (service item, many cycles), rear edge hooks into PS-03 (tool-free rear).
- **Board mounting:** ESP32s on M2.5/M3 corner standoffs printed into the deck +
  foam-tape pad (vibration); amp on a 2-screw pad; WiFi slot = P9 dummy pocket
  (≤ 60 × 32 × 12, pigtails aft — **RST-06: dummy until possession + D-06b**).
- **Clearances:** inboard edge stops at the KO-01/KO-19 line from D-26 dry-fit; aft edge
  stops before the ESC fan bay; centreline never crossed.
- **Cable features:** CN-DECK anchor pocket at the forward-inboard corner + **CN-16
  camera-USB seat beside it (S3, per DN-11)**; comb fingers along the outboard edge;
  U.FL pigtail guides to the rear posts; USB end windows.
- **Material:** **PETG** (WiFi heat nearby — not PLA), flat, 3 walls, ribbed underside
  (2 longitudinal ribs, no bridging over pockets).
- **Removal:** unplug CN-DECK → 2 front M3 → lift rear hooks → deck out as one module.
- **Mass:** plate ~25 g; loaded 55–75 g (I.4 ledger). **Blockers:** D-02/D-04/D-26
  before TP; D-06b before the WiFi pocket is cut for real. **Acceptance (diagnostic):**
  loaded with PS-13 dummies, deck installs/removes in <60 s body-off; body then closes
  (KO-14) with the 5 mm gauge passing.

### PS-05 — Deck posts (×3–4)
- **Purpose:** set DAT-D height; make deck height a **parametric print variable** so
  D-01/D-02 outcomes change one number, not the architecture.
- **Envelope:** Ø10–12 × P4 posts with M3 insert top (front pair) / hook seat (rear).
- **Mounts:** front pair lands on PS-15 shoulders / floor slots; rear pair on PS-03.
- **Material:** PETG, vertical print acceptable (compression member), 4 walls solid top.
- **Blockers:** D-02, D-27. **Acceptance:** deck plane level within ±1 mm over its length.

### PS-06 — RX carrier + antenna guide
- **Purpose:** locate RX-ELRS flat at Z2L and give the antenna a repeatable forward
  guide (KO-17: geometry survives service).
- **Envelope:** ~30 × 20 × 8 pad + 60–80 mm open guide channel forward along the shell line.
- **Mounts:** 1 floor slot + adhesive pad option. **Material:** PETG, flat.
- **Clearances:** ≥80 mm from UBECs/PS-15 (switching noise); clear of KO-01 sweep (D-26);
  antenna tip ≥40 mm from any metal (KO-17).
- **Cable:** CRSF 4-wire exits aft toward CN-DECK with a small service loop.
- **Removal:** RX peels off pad / lifts from clip; carrier stays. **Mass:** <5 g.
- **Blockers:** D-26 (rod), D-20 validates. **Acceptance:** antenna geometry reproducible
  after RX removal/refit; RSSI check at Gate P8.

### PS-07 — Body-disconnect bulkhead clip
- **Purpose:** hold the CN-BODY connector (halo LED feed, + spare pins) at the cockpit
  rim so the shell lifts off after one unplug; strain-relieves both sides.
- **Envelope:** ~25 × 15 × 12 clip. **Mounts:** clips to a floor slot edge near the
  cockpit opening (chassis side); the shell side is a taped/zip anchor (no shell mods
  in this session). **Material:** PETG. **Blockers:** CN-BODY family choice (M),
  shell-side anchor decided at Gate P6. **Acceptance:** body-off in ≤30 s incl. unplug.

### PS-08 — Cable comb / floor-clip set
- **Purpose:** E-15 loom discipline: open-top combs clipping into free floor M3 slots
  and tray edges; keeps R1/R2 edge routes off moving parts, provides tie points every
  ≤60 mm near motion.
- **Envelope:** comb ~18 × 10 × 12, qty ~8–12. **Material:** PETG, flat. **Fasteners:**
  push-fit into slot + optional M3. **Blockers:** D-10 (bulk), D-27 (free slots).
- **Acceptance:** full harness dressed with no unsupported span >80 mm, no contact with
  KO-01/04/06/08 sweeps at Gate P3/P6.

### PS-09 — Rear-tail guide + strain relief
- **Purpose:** carries H-08 (brake LED + SNS-HALL + SRV-DRS extension) along the rear
  floor edge into the drawing-`[7]` "Pass LED here" channel region **before the rear
  stack closes** (R-09); strain-relieves at the moving wing/stack boundary.
- **Envelope:** ~60 × 12 × 10 rail + end grommet. **Material:** **ASA** (hot pocket).
- **Blockers:** Gate A path decision (original vs Rev-1 stack changes the channel);
  **spec now, geometry after Gate A**. **Acceptance:** tail replaceable from outside
  after the stack is closed (pull-through with service loop).

### PS-10 / PS-11 — Gimbal module base / blower-duct interface *(gated)*
- **Purpose:** one chassis-side interface plate at Z8 accepting either Option-A or
  Option-B mast; PS-11 holds the Gate-C duct (from `camera_blower_duct.scad`) to it.
  Must provide roll-trim seating and make hard-stops measurable (KO-13; D-18 stays
  firmware-gated — no active pan/tilt assumption).
- **Blockers:** **D-06, D-07, halo-occlusion check, Gate C set — no CAD before these**
  (RST-04 / F §6). Envelope reserve only: 55 × 45 × 60 at Z8.

### PS-12 — Antenna posts (fold into PS-04)
- Two Ø8 posts at the deck rear corners, whip antennas (VID-ANT) zip-anchored in a
  shallow V (polarization diversity), U.FL pigtail reach ≤80 mm from the WiFi slot
  (P9). ≥150 mm from the ELRS antenna tip (O §RF). Gate: D-06b + D-20.
- **(S3) Fallback variant:** if no deck exists (fallback Architecture A) or the posts
  prove too low, print a **standalone chassis-mounted post pair** (same Ø8 geometry on
  a floor-slot foot near the airbox mouth) — **never shell-mounted**: shell whips would
  tether the body through the ~30-mate U.FL at every body-off (I ZB rule).

### PS-13 — Dummy-envelope block set *(diagnostic prints allowed now)*
- **Purpose:** Gate P1 dry-fit bodies. Set: battery 75×45×25; ESC 36×32×18 + 8 fan disc;
  ESP32 55×28×13 + pin rails to 44 wide; UBEC 30×14×10 ×2; DS3235SG 40×20×40.5 + horn
  disc (KO-19 stand-in until the real servo arrives); **WiFi dummy at the P9 max
  envelope 60×32×12 labelled "DUMMY — RST-06"**; camera stand-in only after D-06 sets
  numbers (until then the camera is *not* dry-fitted with a guessed block).
- **(S3) Connector/wire-exit stubs are part of every dummy, not an option** — a
  body-only block passes dry-fits that the real connector geometry fails: battery block
  + XT60 lead stub forward (16×8×8 body + ~20 mm bend allowance); ESC block + XT60 stub
  fwd + 3-bullet stub aft; UBEC blocks + lead stubs both ends; WiFi dummy + 2 pigtail
  stubs aft; ESP32 blocks + a micro-USB **plug** stub (~10×8×5 + 15 mm cable bend) at
  the outboard end (permanently occupied if DN-08 selects parked pigtails).
- **Material:** any draft filament; every block embossed "TP" + its ID (E-22).
- **Acceptance:** each block within +0.5 mm of its register envelope; used only for
  Gate P1/P3, never installed on the car.

### PS-14 — Speaker carrier *(gated D-03)*
- Ring carrier + foam/TPU isolation ring (TPU = external spool, AMS rev 1 cannot feed
  it — or use EVA foam), port aligned to a sidepod opening; fallback under-deck mount
  facing the airbox channel. **No CAD before D-03**; DN-07 picks the location.

### PS-15 — Power junction block
- **Purpose:** the single power node (R-07 answer): battery XT60 inlet seat, Y-split
  cradle, **fuse holder seat (mini-blade) + main-disconnect provision (loop-key XT60
  seat)** — both fitted per DN-01/DN-02 decisions — XT30 tap row (incl. 1 spare =
  FUT-EXP), ground/test post for D-24 measurements, and the front PS-05 post shoulders.
- **Envelope:** ~55 × 40 × 20. **Datum:** DAT-F at Z2R. **Mounts:** 2 floor slots +
  inserts (service item). **Material:** PETG, flat, 3 walls.
- **Safety features:** all live contacts recessed/shrouded; source sides female (O §S);
  the disconnect seat must be reachable through the cockpit opening (emergency kill
  without body-off — see DN-02).
- **Cable:** XT60 inlet fwd (from battery), UBEC feeds aft-right, ESC feed aft, taps up.
- **Blockers:** DN-01/DN-02 + D-24 for the fuse rating; the block prints with the seat
  either way (empty seat if DN-01 = "no fuse"). **Acceptance:** every connector matable
  and removable with fingers, body-off; disconnect reachable body-on through cockpit.

### PS-16 — Hall sensor bracket
- **Purpose:** hold SNS-HALL at 1–3 mm gap to the axle magnet in the hot rear pocket.
- **Envelope:** ~15 × 10 × 12. **Material:** **ASA** (E-05 pocket). **Mounts:** clips to
  the bearing-carrier region — geometry depends on Gate A stack choice (**blocked**).
- **Acceptance:** gap gauge 1–3 mm; sensor replaceable without drivetrain teardown
  (lead has a service loop to X1).

### PS-17 — USB service-pigtail retainer *(gated D-11 / DN-08)*
- Parks two micro-USB pigtails (CTL-E1/E2) + camera-console lead at the cockpit rim
  for programming without body removal — only if DN-08 selects the pigtail route over
  a body port / plain body-off. No CAD before D-11.
