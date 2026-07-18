# L · Provisional Power Architecture & Rail-Current Budget

Session 2 · 2026-07-18. **Everything sizing-related here is PROVISIONAL and gated by
D-24 (RST-05)** — no final UBEC allocation, wire gauge, connector rating, or fuse
rating is fixed in this document. The WS2812 load is carried at **~1.8 A worst-case**
(R-03) unless a firmware cap or final LED count changes it, with evidence.

---

## L.1 Topology T1 — RECOMMENDED (dual UBEC, ESC-BEC isolated)

```
 PWR-BAT 2S ──CN-01──▶ PS-15 JUNCTION BLOCK
                        │  [CN-02 loop-key disconnect — per DN-02]
                        │  [PWR-PROT fuse, accessory branch — per DN-01]
                        ├────────────CN-04──▶ DRV-ESC ──▶ DRV-MOT (3 phase + sensor)
                        │                        │ BEC +5 V (red) ── ✂ ISOLATED (DN-03)
                        │                        └ signal CN-22 ◀── CTL-E1 (GND common)
                        ├─fuse─┬─CN-05─▶ PWR-UBEC-A ─CN-23A─▶ RAIL A 5 V "clean"
                        │      └─CN-06─▶ PWR-UBEC-B ─CN-23B─▶ RAIL B 5–6 V "servo"
                        └─ XT30 tap row (CN-20 spare = FUT-EXP) + GND test post

 RAIL A: VID-CAM · VID-WIFI · CTL-E1 · CTL-E2 · RX-ELRS · LGT-LED (both segments)
         · AUD-AMP · SNS-HALL (5 V) · [PWR-BUZZ opt]      + 1000 µF at LED strip input
 RAIL B: SRV-STEER · SRV-PAN · SRV-TILT · SRV-DRS · COOL-BLOW   + 1000 µF at PS-03
 GROUND: single star at PS-15; every signal pair carries its ground (no chassis return)
```

- **ESC-BEC isolation (explicit, R-07/RST-05):** the ESC's internal BEC red wire is
  lifted at CN-22 and insulated — **the UBECs own the rails** (BOM bench note, carried
  as plan-of-record DN-03). ESP32 #1 drives the ESC *signal* only; grounds common.
- **Dual-UBEC interaction:** outputs are **never paralleled**; the only shared nodes
  are battery input and star ground. Rail A and Rail B are routed physically apart
  (N §routes) so servo transients cannot couple into video/logic wiring.
- **Common ground:** mandatory single star at PS-15 (ELEC-02 rule); the CN-23 loops
  sit on the +5 V side so ammeter insertion never breaks ground.
- **Rail B voltage:** 5 V baseline. 6 V is attractive for DS3235SG torque but MG90S
  is a 4.8–6 V part sharing the rail → **DN-09** decides at bench (default 5 V).

## L.2 Topology T2 — ALTERNATIVE (ESC BEC drives Rail B)

If a UBEC fails or D-24 shows Rail B headroom is fine on the ESC's internal BEC:
ESC BEC (rating **TO MEASURE** — datasheet claim unverified for the 10BL120) powers
Rail B; UBEC-B becomes the spare; UBEC-A unchanged on Rail A. Cost: servo rail quality
now depends on the ESC under motor load; steering transients share the ESC's internal
regulator. **Not recommended**; retained because ESC-BEC usage must be an explicit
decision, not an omission (R-07). Choosing T2 requires a D-24-style bench measurement
of the ESC BEC under steering stall **before** adoption.

## L.3 Protection & disconnect options (DECISION-NEEDED — owner)

| ID | Question | Options | Session-2 recommendation | Gate |
|---|---|---|---|---|
| **DN-01** | Fuse or not, and where | (a) none (RC status quo, BOM as-is) · (b) **mini-blade fuse on the accessory branch only** (feeds both UBECs; motor path unfused as in RC practice — ESC stall currents make a main fuse nuisance-trip or lie) · (c) full main-line fuse (30–40 A class) | **(b)** — protects the fine-wire loom that R-07 worried about, without pretending to protect the motor path; **rating set only after D-24** (placeholder 7.5 A) | D-24 → Gate P9 |
| **DN-02** | Main disconnect | (a) XT60 unplug, body-off (status quo) · (b) **loop-key XT60 at PS-15, reachable through the cockpit opening body-on** · (c) mechanical switch on accessory branch (rejected as *sole* disconnect — motor stays live) | **(b)** — a true all-battery kill without body removal; the reference build's front-floor switch (photo `…55`) shows the designer also wanted a reachable control | owner call, seat printed either way |
| **DN-03** | ESC-BEC | isolate (BOM bench note) vs use (T2) | **isolate** — plan-of-record | revisit only via T2 evidence |
| **DN-04** | WS2812 current cap | firmware brightness/current limit value vs full-white 1.8 A | cap in firmware to keep Rail A worst-case ≤80% of rating; **value set from D-24 bench data**, not assumed | D-24 |
| **DN-09** | Rail B voltage | 5 V vs 6 V | 5 V until MG90S behaviour at 6 V is bench-verified | Gate P4 |

### L.3.1 Protection engineering notes (S3)

- **What DN-01(b) actually protects:** the 7.4 V accessory-branch conductors and the
  UBEC inputs. It does **not** protect the Rail A/B **output** looms — those rely on the
  UBECs' internal current limiting, which is **unverified for these units**. D-24 adds a
  deliberate output-overload observation (fold-back vs no limit); if limiting is absent,
  per-rail resettable protection (polyfuse ~2–3 A hold on each rail) becomes a DN-01
  amendment rather than an assumption.
- **Fuse rating basis:** the mini-blade sees **input-side** current ≈ (P_railA +
  P_railB) / V_bat / η ≈ **8–9 A at pathological full load, ~6–7 A realistic** — the
  7.5 A placeholder may nuisance-trip. That is why D-24 now records the accessory-branch
  input current at PS-15, not only the CN-23 output loops.
- **Fuse-blow behaviour:** both rails die together while the motor branch stays live —
  safe **only because** the ESC fails to neutral on signal loss. That exact behaviour
  (ESC signal-loss = motor stop) is verified at Gate P4 bench before this reasoning is
  relied on.
- **Loop-key (DN-02) explicit requirements** — "loop key" converted to spec: XT60-class
  contacts (≥30 A cont. / 60 A burst at 2S); the key is a **male shell with bridged
  pins** (electrically dead when removed); the chassis seat is **female, recessed ≥2 mm**
  below the PS-15 shroud (no live contact touchable with the key out); retention = XT60
  friction (~40–60 N) plus a printed guard collar against brush-out; grip = rigid
  printed T-flag, one-finger pull through the cockpit opening in ≤2 s, body-on; the seat
  sits below the shell line (crash-shielded); it kills the **entire battery feed**
  (upstream of both the ESC and accessory branches, per T1); sequence: key in **last**
  (after CN-01), out **first** in any incident (Q, emergency row).
- **USB back-powering:** rails OFF (key out) during USB programming sessions unless the
  dev boards' USB-isolation diodes are verified at Gate P4 — a laptop port must never
  back-feed Rail A (VID-WIFI alone can pull ~2 A). Rule carried in O.4 and Q.

**Power sequencing (fixed order, O §safety):** WiFi heatsink bonded + antennas on
U.FL **before** any Rail A power → bench current-limited supply first (ASM-35: staged
0.5 A → 2 A limits) → battery only after polarity/continuity (ASM-34) → servo centring
(ASM-07) precedes linkage → D-24 measured (ASM-36) **before** the final harness is cut
to length (Gate P9).

**Service/test points:** CN-23A/B ammeter loops (bridge plugs when not measuring),
PS-15 ground post, XT30 tap row for bench feeds. D-24 is executable **without cutting
anything** — designed-in measurement.

---

## L.4 Provisional per-rail current budget (gated by D-24)

All figures **ESTIMATED** unless noted; margins are policy targets, not measurements.
"Simult." = counted in the worst-case simultaneous sum?

### Rail A — 5 V clean (UBEC-A, rated 5 A)

| Device | V | I typ | I peak | Evidence | Simult. | Measure |
|---|---|---|---|---|---|---|
| CTL-E1 | 5→3.3 | 0.10 | 0.30 | DS typical | yes | D-24 |
| CTL-E2 | 5→3.3 | 0.10 | 0.30 | DS typical | yes | D-24 |
| RX-ELRS | 5 | 0.05 | 0.10 | DS typical | yes | D-24 |
| VID-CAM | 5 | 0.35 | 0.60 | DS typical (runs hot) | yes | D-24 + D-19 |
| VID-WIFI | 5 | 0.90 | **2.00** | high-power USB class, **module unverified (RST-06)** | yes | **D-06b + D-24** |
| LGT-LED (30 px) | 5 | 0.60 | **1.80** | **binding worst case** (R-03) until DN-04 caps it | yes | D-24 |
| AUD-AMP | 5 | 0.15 | 0.90 | 3 W/4 Ω class transients | yes | D-24 |
| SNS-HALL (+div) | 5 | 0.01 | 0.02 | DS | yes | — |
| **Totals** | | **≈2.3 A** | **≈6.0 A** | | | |

**Reading:** worst-case exceeds the 5 A UBEC (E-23 confirmed at Session-2 granularity).
The simultaneity is *plausible* (full-white LED + audio + WiFi burst). Resolution paths,
in order: DN-04 firmware LED cap → re-budget; move AUD-AMP peaks (audio ducking under
LED events, firmware); UBEC-A upsize (PS-03 pocket is parametric). **Decision deferred
to D-24 by design.** Margin policy: sustained ≤ 80% of rating, transient ≤ 100%.

### Rail B — 5 V servo (UBEC-B, rated 5 A)

| Device | V | I typ | I peak | Evidence | Simult. | Measure |
|---|---|---|---|---|---|---|
| SRV-STEER DS3235SG | 5–6 | 0.80 | **3.00 (stall)** | DS class | yes | D-24 |
| SRV-PAN MG90S | 5 | 0.20 | 0.80 (stall) | DS class | one of two | D-24 |
| SRV-TILT MG90S | 5 | 0.20 | 0.80 (stall) | DS class | one of two | D-24 |
| SRV-DRS MG90S | 5 | 0.20 | 0.80 (stall) | DS class | no (event-driven) | D-24 |
| COOL-BLOW | 5 | 0.15 | 0.25 | DS class | yes | D-24 |
| **Totals** | | **≈1.6 A** | **5.65 A all-stall / ≈4.5 A realistic** | | | |

**Reading:** all-four-servo stall exceeds rating but is not a realistic drive state;
realistic worst (steer stall + one gimbal stall + blower + others typical) ≈ 4.5 A —
inside rating, **thin margin (~10%)**. Mitigations if D-24 confirms: firmware stagger of gimbal slews vs
steering events; endpoint limits (already a firmware-side requirement via D-18) reduce
stall dwell. UBEC-B upsize is the fallback.

### Battery / main path (context, unfused in DN-01(b))

Motor draw dominates (tens of A burst, 10BL120 class); XT60 + 14–16 AWG silicone on
H-01/H-03 per RC practice — **gauge finalized at Gate P9 after D-24**, not now.

## L.5 Transients & inrush

1000 µF at LED strip input + 1000 µF on Rail B (BOM bench fixes). WiFi module enumerate/
TX bursts on Rail A — UBEC-A must hold 5 V ±5% through them (D-24 scope trace, not just
ammeter). ESC startup: ESC on its own branch; its inrush never crosses the UBEC feeds
except at the shared battery — acceptable at 2S. First power-up is always
current-limited (ASM-35) with rails brought up one at a time via the CN-23 loops.

## L.6 Expansion allowance

CN-20 spare XT30 tap (battery-voltage, behind the DN-01 fuse) + 2 spare positions in
CN-07 (deck) + deck forward blank (I.3). Any future device must re-enter this budget
table before it gets power — the table is the gate, not the tap.
