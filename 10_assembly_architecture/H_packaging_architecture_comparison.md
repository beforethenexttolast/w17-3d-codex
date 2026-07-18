# H · Packaging Architecture Comparison & Selection

Session 2 · 2026-07-18. Consumes Reports A–G unchanged; honours restrictions RST-01…07
(`G_session1_5_review_findings.md` readiness verdict). Confidence tags per
[`README.md`](README.md). **Nothing here closes a Session-1 gate; every vertical number
is PROVISIONAL until D-01/D-02 (RST-01).**

---

## H.1 Opening engineering move — text-based virtual dry-fit

Method: parameter-range dry-fit on paper. Every uncertain dimension is carried as a
**min / expected / max** range, never collapsed to one number. Datums are named
explicitly (RST-01):

- **DAT-F** — chassis **floor-top** plane (the universal mounting datum; its relation
  to the shell is TO MEASURE, D-01).
- **DAT-S** — body-shell **bottom edge** (the datum all Session-1 "ceiling" probe
  numbers use).
- **DAT-T** — top face of a lower tray (tray thickness above DAT-F).
- **DAT-D** — top face of the upper deck (where deck-mounted component heights start).
- All component-top heights are quoted **above DAT-F** unless suffixed “(DAT-S)”.

### H.1.1 Governing parameters (ranges, not numbers)

| Param | Meaning | Min | Expected | Max | Status / resolver |
|---|---|---|---|---|---|
| **P1** | Δ(DAT-F above DAT-S): height of floor top above shell bottom edge when assembled | 2 | 6–10 | 15 | **TO MEASURE — D-01** |
| **P2c** | Net centreline ceiling over Z3 above DAT-F ( = ~72 (DAT-S) − P1 ) | 57 | 62–66 | 70 | DERIVED from ESTIMATED probe + P1; validate D-02/D-04 |
| **P2s** | Side-bay ceiling above DAT-F at ±30–55 mm off centreline (shell curves down; probe did not resolve the side profile) | 25 | 35–45 | 55 | **TO MEASURE — D-02** |
| **P3** | Battery stack top: tray 2.5–3 + pack 25 + strap ~3 | 29 | 30–32 | 34 | DERIVED (pack limit CONFIRMED) |
| **P4** | Deck plane DAT-D height (over 10 mm UBEC bodies + clearance) | 20 | 24–28 | 32 | design choice, gated by P2s |
| **P5** | ESP32 install height on deck (flat board 13 + low-profile wiring) | 18 | 20–25 | 28(Dupont vertical) | ESTIMATED (B, CTL-E1) |
| **P6** | KO-19 top: DS3235SG 40.5 + `Servoholder` base + horn | 42 | 45–48 | 52 | ESTIMATED; D-09 |
| **P7** | Steering push-rod **line height** above DAT-F along its run (servo horn ≈ 35–45 up to `servosaverv7` atop the 71 mm tower — see H.1.2) | 30 | 40–60 (sloped) | 70 | **TO MEASURE — D-26 (new, S2)** |
| **P8** | KO-06 shock band: width / height over rear-spine centreline | 24 w | 28–30 w / ≤40 h | 34 w / 45 h | ESTIMATED; Gate A dry-fit |
| **P9** | WiFi-module max **allowable** envelope (incl. 28×28×3 heatsink, pigtails exiting aft) for the selected slot | — | ≤ 60 × 32 × 12 | hard cap | **ALLOCATED (S2)** — RST-06 dummy spec, §K PS-13 |
| **P10** | Battery pocket allocation (pack + XT60 exit + strap) | — | 95 × 50 × 30 | hard cap | CONFIRMED allowance (B, PWR-BAT) |
| **P11** | ESC bay allocation (36×32×18 body + fan + ≥10 air above fan + wire exits) | 45×40×36 | 50 × 42 × 40 | 55×45×46 | ESTIMATED; D-08 |

### H.1.2 New finding (S2, DERIVED — must be verified): the steering rod is a *high* diagonal keep-out

Session 1 treated KO-01 as a centreline sweep without a stated height. Drawing `[3]`
puts `servosaverv7` **on top of** `Suspension Block_10` (37 × 37 × **71 mm** tall,
CONFIRMED bbox), and drawing `[2]` puts the servo horn mid-chassis at ~35–45 mm. If
both ends are where the drawings say, the rod runs as a **rising diagonal (~35 → ~70 mm
above DAT-F) along the centreline** — i.e. it crosses the central zone at exactly
*deck* height, not floor height. Consequences:

1. **No structure or harness may bridge the centreline** between the servo horn and the
   front tower below ~P7max (70 mm) until D-26 measures the real line + sweep width.
2. Any “upper deck” must either stay in the **side bays** or provide an **open
   centreline channel**.
3. This kills the remaining appeal of a full-width bridge deck and of the tall airbox
   ESP32 stack (already marginal per RST-02) — both would sit in or beside the rod line.

**D-26 (added to Report D this session):** measure rod line height at 3 stations + the
lock-to-lock sweep band, in the slicer assembly and again at mechanical dry-fit.

### H.1.3 Dry-fit conclusions (all PROVISIONAL)

- **Centreline (Z3/Z5, full length): reserved.** Occupants: KO-19 servo (P6), KO-01 rod
  (P7), KO-06 shock band (P8), drivetrain. Electronics do not enter it. This is the
  **open-spine principle** and it holds across every parameter range above.
- **Left side bay** (junction zone, ~55 × 95 × P2s): fits **P10 battery pocket** at L0
  with nothing above it in min-P2s worlds; deck above battery only if P2s ≥ 45.
- **Right side bay**: fits **P11 ESC bay** at L0 (rear) + UBEC pair (10 mm tall) at L0
  (forward) + a **deck at P4 over the UBECs** carrying 2× ESP32 flat, fore-aft in a row
  (each 55 × 28 × P5). Worst-case top = P4max + P5max = 60 → **fails even the P2s *maximum* (55) (S3 label fix — the S2 text said "min-P2s")**;
  expected case = 26 + 22 = 48 → passes expected P2s only near the centreline side of
  the bay. **The deck must sit as close inboard as the rod sweep allows** — the D-02
  dummy dry-fit decides, which is exactly what RST-02 requires.
- **Front bay (Z2)**: low, contested on the centreline only. Off-centre floor is usable
  for **flat, low** items: ELRS RX (3 mm) + its antenna forward-left; power-junction
  parts forward-right. Ceiling 42–53 (DAT-S) − P1 → ~30–50 net: adequate for these.
- **Nose (Z1)**: no numbers exist (RST-04). Nothing is allocated there. Both camera
  options stay protected placements (cockpit/halo); nose remains REJECTED-for-primary
  unless D-25 + D-06 later prove a protected pocket (owner call, E-24).
- **Airbox tall channel (14–40 wide)**: reserved as **thermal chimney + WiFi-antenna
  space**, not as a PCB volume (RST-02). The ESP32 airbox stack survives only as a
  *fallback* (H.4) pending D-02/D-04.

---

## H.2 Candidate architectures

### Architecture A — Direct single-level installation
Everything mounts flat on the floor with minimal printed brackets (reference-build
style, but bracketed instead of zip-tied). Battery left, ESC right, ESP32s flat on the
remaining floor, UBECs where they fall, loom on top.

- For: lowest CG; no dependence on P1/P2 heights; simplest prints; closest to the
  proven reference build.
- Against: floor area is the scarce resource once KO-19 + KO-01 + KO-06 + battery +
  ESC are placed — the remaining footprint (~two ~50 × 90 side strips minus wire runs)
  cannot take 2× ESP32 + WiFi + amp + RX + junction *flat* without burying some under
  others; service = excavation; harness lies on top of everything (reference photos
  show the result); WiFi module ends up in dead air.

### Architecture B — Two-level electronics stack (side-bay decks, open spine)
L0: heavy/high-current/low items (battery LEFT, ESC + UBECs RIGHT, junction block).
L1: one removable **right-side deck** over the UBEC zone carrying 2× ESP32 flat +
amp + WiFi module (rear edge, in the airbox chimney draft). Centreline stays open
(H.1.2). Left side keeps nothing above the battery.

- For: matches the dry-fit; battery stays top-accessible; deck removes as one module
  with a single service disconnect; boards get airflow height; wiring splits cleanly
  (power low / signal high).
- Against: vertical-datum dependency (RST-01) — deck top rides the P2s uncertainty;
  adds ~25–35 g structure on the right (balanced by ~100+ g battery on the left);
  deck fasteners + posts to design.

### Architecture C — Printed internal skeleton
A spine + side rails + bridges cage tying front tower to rear stack, with decks hung
off it.

- For: stiffest; one-piece electronics cage could lift out whole.
- Against: the centreline a spine would use is **exactly the occupied volume**
  (rod/servo/shock — H.1.2); a perimeter cage duplicates the floor’s own stiffness
  (8 mm plate, 12× M3) for mass and print time we don’t need; largest print+design
  effort; worst measurement dependency (every member touches an unmeasured surface);
  highest rework risk when D-01/D-02 land.

### Architecture D — Distributed modular architecture
Spread subsystems into every zone: RX + divider in the front bay, UBECs + amp +
speaker in the sidepods, ESP32s central, camera cockpit, WiFi + antennas rear, LEDs
in shell/tail, DRS at the wing.

- For: decongests the centre; natural thermal/RF separation; small independent
  mounts print easily.
- Against: the two zones it leans on hardest are the two **unmeasured** ones —
  sidepods (D-03) and nose (D-25) — so it has the worst dependency on missing
  measurements; longest harness runs and most connectors; service touches many small
  mounts instead of one deck.

---

## H.3 Weighted comparison

Weights reflect W17 priorities (F §4, RST list), not generic preference: mechanical
feasibility, movement clearance, serviceability, assembly order, access, electrical
safety, thermal, and **low dependency on unresolved measurements** carry the weight.
Scores 1–5 (5 best), PROVISIONAL judgement on today’s evidence.

| Criterion (weight) | A single-level | B two-level side-bay | C skeleton | D distributed |
|---|---|---|---|---|
| Mechanical feasibility / component fit (10) | 2 | 4 | 3 | 4 |
| Movement clearance (rod/shock/servo, KO-19/01/06) (10) | 3 | 5 | 2 | 4 |
| Serviceability / module replacement (9) | 2 | 5 | 3 | 3 |
| Assembly-order feasibility (8) | 4 | 4 | 2 | 3 |
| Access (USB, connectors, battery, tools) (8) | 2 | 4 | 3 | 3 |
| Electrical safety / rail separation practical (8) | 3 | 4 | 4 | 4 |
| Thermal viability (7) | 2 | 4 | 3 | 4 |
| **Low** dependency on unresolved measurements (8) | 4 | 3 | 2 | 1 |
| RF separation / antenna placement (6) | 3 | 4 | 3 | 5 |
| Wiring congestion (6) | 2 | 4 | 3 | 3 |
| CG / balance (5) | 5 | 4 | 3 | 4 |
| Structural + print complexity (4) | 5 | 4 | 1 | 3 |
| Risk of rework after D-01/D-02 (7) | 4 | 3 | 2 | 2 |
| Expansion capacity (3) | 2 | 4 | 4 | 3 |
| **Weighted total (max 495)** | **295** | **400** | **267** | **326** |

(Arithmetic: A = 2·10+3·10+2·9+4·8+2·8+3·8+2·7+4·8+3·6+2·6+5·5+5·4+4·7+2·3 = 295;
B = 4·10+5·10+5·9+4·8+4·8+4·8+4·7+3·8+4·6+4·6+4·5+4·4+3·7+4·3 = 400;
C = 3·10+2·10+3·9+2·8+3·8+4·8+3·7+2·8+3·6+3·6+3·5+1·4+2·7+4·3 = 267;
D = 4·10+4·10+3·9+3·8+3·8+4·8+4·7+1·8+5·6+3·6+4·5+3·4+2·7+3·3 = 326.)

---

## H.4 Selection

**RECOMMENDED — Hybrid B+D: “open-spine, twin side-bay, one removable deck”.**
Architecture B’s two-level side-bay core (battery left-low, ESC+UBECs right-low,
one removable right deck for ESP32s + amp + WiFi) **plus** Architecture D’s
distributed periphery exactly where distribution costs nothing measured-wise:
RX forward-left (RF), DRS at the wing (designed-in), Hall at the axle (designed-in),
brake LED in the tail (designed-in channel), halo LED on the shell with a body
disconnect, camera as a self-contained gimbal module at the cockpit-region mount
(Option A/B stays an owner call). Speaker: PROVISIONAL sidepod-left, gated D-03,
fallback under-deck. Full allocation in Reports I/J.

**FALLBACK — Architecture A (single-level, reduced-congestion variant).** If D-01/D-02
return min-range heights (P2s < ~40) the deck is deleted: ESP32s move flat to the
right-forward floor (Z2R) in place of the junction block (which shifts inboard-front),
WiFi lies flat at the airbox mouth, amp piggybacks the ESP32 mount. Same modules,
same harness topology, one level. Nothing else re-architects — this is why the harness
(M/N) is designed module-first.

**(S3 addendum — fallback deltas, so "same harness topology" is not over-read):** the
connection *graph* is unchanged, but four things do re-work in fallback A: (1) the
MOD-DECK one-disconnect service property disappears — boards mount individually and
CN-07 becomes a chassis-side bank near Z2R; (2) CN-22 (ESC signal) grows from ~70 mm to
a near-full-chassis run; (3) H-07 re-routes (WiFi at the airbox mouth ↔ camera) and the
CN-16/DN-11 boundary still applies; (4) PS-12 antenna posts need the standalone
chassis-mounted variant (K) — never shell-mounted. The "junction block shifts
inboard-front" move must re-verify KO-01/KO-05 clearance **and** the DN-02 loop-key's
cockpit reach before it is accepted.

**Subsystems whose placement cannot be selected yet** (carried explicitly, not
silently): camera/gimbal (Option A vs B — owner, D-06/D-07 + halo-occlusion check);
speaker (D-03); WiFi module final slot (dummy P9 until possession + D-06b, RST-06);
any nose use (D-25, E-24); DRS wing family (Gate A/B). None of these blocks the core
architecture: each has a reserved envelope + fallback in Report I.

**The ESP32 airbox stack (RST-02) is retained only as fallback F-2**: if the right
deck fails D-02/D-04 *and* the single-level fallback cannot host both boards, a
low-profile **soldered** (no Dupont) vertical carrier in the airbox channel may be
revisited — it requires giving up header-serviceability and proving ≥16 mm channel
width at the stack station. It is not part of the recommended path.

---

**The selection is implemented by:** zones [`I`](I_zone_layer_plan.md) · placements
[`J`](J_component_placement_matrix.md) · supports [`K`](K_printable_support_spec.md) ·
power [`L`](L_power_architecture.md) · harness [`M`](M_connector_harness_matrix.md) ·
routing [`N`](N_cable_routing_plan.md) · thermal/RF/safety
[`O`](O_thermal_rf_vibration_safety.md) · assembly [`P`](P_assembly_master_manual.md) ·
service [`Q`](Q_service_disassembly_guide.md) · gates [`R`](R_validation_gates.md) ·
decisions [`S`](S_decision_register.md) · CAD tasks [`T`](T_cad_task_spec.md).
