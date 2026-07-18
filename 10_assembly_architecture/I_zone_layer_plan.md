# I · Zone & Layer Plan — open-spine, twin side-bay architecture

Session 2 · 2026-07-18. Implements the H.4 selection. Datums per H.1 (DAT-F floor top,
DAT-S shell bottom edge, DAT-T tray top, DAT-D deck top); parameters P1…P11 per H.1.1.
Session 4A P0 has supplied the D-01/D-02 lower-bound geometry; **absolute shell/deck
height remains PROVISIONAL until physical S0 is pinned at Gate P1.** Zone IDs extend
the Session-1 Z1–Z8 set with side/level suffixes: `L`/`R`/`C` (left/right/centre) and
`L0`/`L1` (floor level / deck level).

---

## I.1 Vertical stack diagram (explicit datums)

```
        (heights above DAT-F; shell clearances at S0=0; add physical S0)

  P2c 65–71 ──────────────╮ shell roof over Z3 centreline (P0, S0=0)
                           │
  Z 35–62 ─ ─ ─ ─ ─ ─ ─ ─ ─ ── │  KO-01 steering-rod reserved band (D-26)
                           │      │ high, near-level; X1/X2 cross below Z35
  P2s 26–41 ──────╮       │      │            (P0, S0=0; add S0)
                   │ shell │      │
  DAT-D ~20   ═════╪═══════╪══════╪══════ deck top (conditional on S0; removable)
   ESP32 top =     │       │      │       DAT-D + P5 (18–28) → must clear P2s
  DAT-T  ~3 ───────┤       │      │
                   │       │  KO-19 servo top P6 42–52 (centre, mid-chassis)
  DAT-F  0 ════════╧═══════╧══════╧══════ chassis floor TOP (universal datum)
  −8               floor plate (8 mm, CONFIRMED)
  DAT-S  S0 (0…~11)       body-shell bottom edge (physical pin at Gate P1)
```

**(P0 — Session 4A; details `V_P0_geometry_measurement_results.md`):** the old P1
sign assumption is superseded: the shell bottom edge (DAT-S) sits AT or ABOVE DAT-F
by **S0 ∈ 0…~11 (physical pin at Gate P1)**. Measured at S0=0 (lower bound):
**P2c = 65–71 ✔ (est. ~57–70 held)**; **P2s = 26–41** (37–52 if S0≈11) — the deck
survives only as a narrow inboard deck (plate ≈ L −50…−26, P4 ≈ 20) in the S0 ≥ ~6
world; the H.4 fallback-A trigger is armed but NOT fired pending S0. **P7 (rod):
measured band Z 35–62, |L| ≤ 18 rear → 12 fwd — a high level line, not 35→70.**
Battery bay length ≈ 78 > 75 ✔ (D-01); pack top (~28) passes under the rod band.

Safety clearance policy (applies at every level): **≥ 5 mm** static-to-static,
**≥ 8 mm** static-to-moving (rod, horn, shock, belt), **≥ 10 mm** above the ESC fan,
re-validated at Gate P3 with real parts. **(S3)** The 5 mm static allowance is also the
print-tolerance / assembly-tolerance / shell-flex budget — D-04 is gauged with the
shell seated and lightly pressed, not held clear.

## I.2 Plan-view zone grid

```
        FRONT                                                        REAR
  ┌────────────┬──────────────┬────────────────┬──────────────┬──────────┐
  │  Z1 nose   │  Z2 front bay│  Z3 junction   │ Z5 rear spine│ Z6 drive │
  │ (unmeasured│ Z2L: RX+ant  │ Z3L-L0 battery │  KO-06 shock │ train    │
  │  D-25,     │ Z2C: rod+twr │ Z3C: KO-19+rod │ Z5R: ESC bay │ (prohib.)│
  │  E-24)     │ Z2R: junction│ Z3R-L0 UBECs   │ Z5C: prohib. │ + Z7 wing│
  │            │      block   │ Z3R-L1 DECK    │              │  /DRS    │
  └────────────┴──────────────┴────────────────┴──────────────┴──────────┘
   Z4L/Z4R sidepods flank Z3 (unmeasured, D-03) · Z8 gimbal = cockpit region
   ZB = body-shell-mounted (halo LED, antennas) · airbox channel = thermal/RF only
```

## I.3 Zone register

Fields: datum · envelope (min/expected/max where uncertain) · status · installed /
prohibited · keep-outs · mounting · mass (ESTIMATED) · heat · RF · access/cables ·
dependencies. “—” = not applicable.

### Z3L-L0 — Battery bay (left junction, floor level)
- **Datum:** DAT-F via tray PS-01 (DAT-T ≈ 3).
- **Envelope:** P10 = 95 × 50 × 30 allocation; pack hard-limit ≤ 75 × 45 × 25 (CONFIRMED).
- **Status:** RECOMMENDED (location) / PROVISIONAL (exact fore-aft station until D-01/D-02).
- **Installed:** PWR-BAT + strap + XT60 lead exit forward.
- **Prohibited:** anything mounted above the pack (top must stay open for swap).
- **Keep-outs:** KO-19 inboard face (≥5 mm), KO-01 rod overhead (P7, D-26), left shell wall.
- **Mounting:** tray PS-01 on floor M3 slot-nut pattern (D-27 maps usable slots).
- **Mass:** pack 80–120 g + tray ~15 g — the main left-side ballast. **Heat:** mild. **RF:** none.
- **Access:** body-off top access; connector reach at forward end (junction block).
- **Cables:** XT60 forward to PS-15; balance lead parked on tray clip.
- **Depends on:** D-01 (bay length/bosses), D-02 (KO-19 spacing), D-26.

### Z3R-L0 — UBEC shelf (right junction, floor level)
- **Datum:** DAT-F. **Envelope:** ~70 × 40 × 12 used of the bay (UBECs are 30 × 14 × 10 EST ×2).
- **Status:** RECOMMENDED. **Installed:** PWR-UBEC-A, PWR-UBEC-B, PWR-CAP, SNS-DIV.
- **Prohibited:** high components (deck passes over at P4). **Keep-outs:** KO-19 inboard, deck posts.
- **Mounting:** integrated pocket row in PS-02/PS-03. **Mass:** ~30 g. **Heat:** warm at load
  (D-19 includes UBECs). **RF:** switching noise — keep RX + antennas ≥ 80 mm away.
- **Access:** remove deck (2 fasteners) → full reach. **Cables:** inputs from PS-15 junction
  (short, right-forward); Rail A up to deck; Rail B aft+across to servo/gimbal/DRS/blower.
- **Depends on:** D-02, D-24 (may force a UBEC upsize → envelope re-check).

### Z5R — ESC bay (right rear spine, floor level)
- **Datum:** DAT-F. **Envelope:** P11 = 50 × 42 × 40 expected (D-08 measures the real ESC).
- **Status:** RECOMMENDED. **Installed:** DRV-ESC, fan up, ≥10 mm free above fan (no deck over it).
- **Prohibited:** Rail-A electronics (noise + heat). **Keep-outs:** KO-06 shock band inboard
  (≥8 mm), KO-08/09 drivetrain aft, rear shell wall.
- **Mounting:** PS-02 ESC mount (strap-over, thermal standoff from floor).
- **Mass:** 40–65 g. **Heat:** hot — needs the rear-out exhaust path (O §thermal).
- **RF:** the noise source — motor/battery wires kept short, right-rear only.
- **Access:** direct top access, body-off. **Cables:** XT60 in (fwd), 3 bullets aft to motor,
  signal wire up-forward to deck edge.
- **Depends on:** D-08; Gate A geometry fixes the shock band edge.

### Z3R-L1 — Removable electronics deck (right, deck level)
- **Datum:** DAT-D = P4 (20–32) on posts from the floor slots.
- **Envelope:** deck plate ~130 × 55 expected, spanning Z2R rear → Z3R; component build
  height P5 above DAT-D; top must clear P2s by ≥5 mm — **Gate P1/P3 validates**.
- **Status:** RECOMMENDED / PROVISIONAL height (RST-01). **Installed:** CTL-E1, CTL-E2
  (flat, fore-aft in a row, USB ends outboard-right), AUD-AMP, VID-WIFI (rear slot, P9
  dummy ≤ 60 × 32 × 12 — RST-06), 5.8 GHz antenna roots (rear posts).
- **Prohibited:** anything needing floor access below it except the UBEC shelf (designed for it).
- **Keep-outs:** open centreline inboard (KO-01/KO-19 per D-26), ESC fan aft (deck stops
  short of the ESC bay), shell roof above.
- **Mounting:** PS-04 deck on PS-05 posts; 2 thumbscrew/M3 fasteners; lifts out as one module
  after 1 service disconnect (M: CN-DECK).
- **Mass:** deck+boards ~55–75 g at P4 height — the main deliberate CG cost, balanced by the
  left battery. **Heat:** WiFi module is the hot item — rear slot sits in the airbox-channel
  draft (O). **RF:** WiFi 5.8 GHz at the rear posts; keep ≥150 mm from ELRS (Z2L).
- **Access:** USB reachable body-off from the right; deck removal = 2 fasteners + CN-DECK.
- **Depends on:** D-02 (side-bay profile), D-04 (roof), D-06b (real WiFi), D-24, D-26.

### Z3C / Z5C — Central spine (PROHIBITED for electronics)
- Occupants: KO-19 servo + `Servoholder` (mid-chassis), KO-01 high near-level rod band, KO-06
  68 mm shock band, drivetrain approach. **Nothing else enters.** Cable crossings of the
  centreline: only at the two defined crossing stations (N §routes), 90°, above/below the
  rod per D-26, with ≥8 mm to any moving part.

### Z2L — Front-left bay (RF corner)
- **Datum:** DAT-F. **Envelope:** ~60 × 45 × (30–50 net) — low. **Status:** RECOMMENDED.
- **Installed:** RX-ELRS (3 mm thin) on PS-06 carrier; antenna guided forward along the
  shell inside (RF-transparent PLA, KO-17). SNS-DIV may sit here if not on the UBEC shelf.
- **Prohibited:** switching regulators, power wiring bundles (RF quiet corner).
- **Keep-outs:** KO-01 rod inboard/overhead, KO-05 tower aft, KO-04 arm travel outboard.
- **Mass:** <10 g. **Heat:** cool. **Access:** body-off top. **Depends on:** D-26, D-20.

### Z2R — Front-right bay (power junction)
- **Datum:** DAT-F. **Envelope:** ~60 × 45 × (30–50 net). **Status:** RECOMMENDED.
- **Installed:** PS-15 junction block: XT60 battery inlet, Y-split, fuse/disconnect
  position (L: DN-01/DN-02), XT30 taps. Deck forward posts land here.
- **Prohibited:** RF items. **Keep-outs:** as Z2L mirrored.
- **Access:** body-off; the disconnect must be the **first thing reachable** (safety, O §S).
- **Depends on:** D-24 (fuse rating), DN-01/02 decisions.

### Z4L / Z4R — Sidepods (TO MEASURE, D-03)
- **Status:** PROVISIONAL — no committed occupant. **Candidate:** AUD-SPK (left, port
  through sidepod grille) — decision DN-07 after D-03; fallback speaker under-deck right.
- **Prohibited until measured:** everything else. **Depends on:** D-03.

### Z1 — Nose (NOT ALLOCATED)
- **Status:** TO MEASURE (D-25) + crash zone (E-24, RST-04). No component allocated.
  Re-evaluated only as a **secondary** camera option after D-25 + D-06 (owner call).

### Z8 — Camera/gimbal region (cockpit / halo)
- **Status:** OPEN owner decision (Option A cockpit vs Option B halo pod, per
  `CAMERA_GIMBAL_PLACEMENT.md`; RST-04 keeps the nose out of it). Session 2 reserves a
  **common module interface**: PS-10 gimbal base mounts at the cockpit-region floor/shell
  station and accepts either option’s mast; envelope reserve ~55 × 45 × 60 (ESTIMATED,
  D-06/D-07 refine). Driver figure is mutually exclusive with Option A (G, R-14).
- **Depends on:** D-06, D-07, halo-occlusion check; hard-stop measurability (KO-13, D-18
  stays firmware-gated).

### Z6 — Rear drivetrain (PROHIBITED — unchanged from Session 1)
- Axle/spur/belt/motor: mechanical + hot (KO-08/09). No electronics except the
  designed-in SNS-HALL on PS-16 (ASA) and SNS-MAG on the axle. Approach only via
  H-03 (short) and H-08 (left edge, PS-09).

### Z7 — Rear wing / DRS (gated Gate A/B)
- **Installed (by donor design):** SRV-DRS in the wing pocket + rod (KO-12); brake-LED
  tail terminates at `rearbacklightdiffuser` via the drawing-`[7]` channel.
- **Status:** gated — unchanged (RST-07). Harness provision (M/N) is designed now;
  physical closure follows Gate A/B.

### ZB — Body-shell-mounted region
- **Installed:** halo WS2812 segment (+ its 330 Ω/feed tail), mirrors/deco. **(S3)**
  The 5.8 GHz antenna tips are **not** a ZB fallback: shell-mounted whips would tether
  the shell through the ~30-mate-rated U.FL pigtails at every body-off, breaking the
  one-disconnect rule. If the deck posts prove too low, the fallback is the standalone
  chassis-mounted PS-12 variant (K).
- **Rule:** everything shell-mounted reaches the chassis through **one** body disconnect
  (CN-BODY, M) near the cockpit opening — the shell must lift off after unplugging one
  connector (+ the 3× M3).

### Airbox channel (14–40 mm wide tall slot, rear shell)
- **Status:** reserved for **airflow (thermal chimney) + WiFi antenna placement**, not
  PCBs (RST-02). **Fallback F-2 is geometrically rejected by P0**: the rear stack
  stations narrow to 14–16 mm before module headers, USB plug, mount and airflow.

### Reserved expansion
- The forward 25–30 mm of the deck plate (blank, pre-drilled M2/M3 grid) + one spare
  XT30 tap at PS-15 + 2 spare deck harness positions in CN-DECK. FUT-EXP satisfied
  without new volume claims.

## I.4 Balance ledger (ESTIMATED, verify at D-21)

Left: battery 80–120 g + tray 15 + RX ~5 = **100–140 g** (+ speaker 20–40 only if
DN-07 lands Z4L — a *gated* mass, not bankable). Right: ESC 40–65 + UBECs 30 +
deck+boards+WiFi 55–75 + junction 15–25 = **140–195 g**.
**(S3) The ledger as allocated is right-heavy by ~30–60 g without the speaker (~0–45 g
with it), and part of that right-side mass rides at deck height.** The ±10 mm PS-01
slots trim **fore-aft only** — they cannot correct L/R. Named L/R trim paths, in order:
(1) DN-07 weighting — the sidepod-left speaker position carries a balance argument, not
only an audio one; (2) the PS-01 outboard-wall **ballast land** (self-adhesive 5 g
wheel-weight strip positions, added to K); (3) pack selection toward the heavier end of
80–120 g. D-21 measures per-corner (detects L/R and diagonal); correction uses these
paths. Centre: servo 60 + shock + drivetrain + motor (fixed). Front/rear: junction-zone
battery mass partially offsets the rear motor+drivetrain; fine F/R trim at D-21 by
sliding the battery station fore-aft within Z3L (±10 mm slots).

---

**Downstream documents:** placements → [`J`](J_component_placement_matrix.md) ·
printed supports → [`K`](K_printable_support_spec.md) · power →
[`L`](L_power_architecture.md) · connectors/harnesses →
[`M`](M_connector_harness_matrix.md) · routing → [`N`](N_cable_routing_plan.md) ·
thermal/RF/safety → [`O`](O_thermal_rf_vibration_safety.md) · assembly →
[`P`](P_assembly_master_manual.md) · service → [`Q`](Q_service_disassembly_guide.md) ·
gates → [`R`](R_validation_gates.md) · decisions → [`S`](S_decision_register.md) ·
CAD hand-off → [`T`](T_cad_task_spec.md).
