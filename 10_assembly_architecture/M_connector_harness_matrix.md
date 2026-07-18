# M · Connector & Harness Architecture

Session 2 · 2026-07-18. Modules first, connectors second: the vehicle divides into
serviceable electrical modules; every module boundary is a connector, everything
inside a module may be soldered. **All gauges/ratings PROVISIONAL until D-24 (RST-05);
lengths PROVISIONAL until D-10 routing dry-fit.** **No unsecured Dupont-style
connectors anywhere on the completed vehicle** — deck-internal Dupont is allowed only
on the bench, replaced by JST-XH/solder before Gate P6.

## M.1 Electrical modules

| Module | Contents | Boundary connectors | Comes out as one piece? |
|---|---|---|---|
| MOD-PWR | PWR-BAT, PS-15 (Y, fuse, disconnect, taps), UBEC-A/B | CN-01/02/04/05/06/23A/23B/20 | battery yes; junction stays |
| MOD-DRV | DRV-ESC + DRV-MOT + phase/sensor leads | CN-04 (power), CN-22 (signal) | ESC yes; motor with drivetrain |
| MOD-STR | SRV-STEER (in `Servoholder`) | CN-08 | servo yes (linkage open) |
| MOD-DECK | PS-04 deck: CTL-E1/E2, AUD-AMP, VID-WIFI(+HS), antenna posts | **CN-07 bank** + CN-17/18 U.FL + **CN-16 camera-USB (S3, per DN-11)** | **yes — the design goal** |
| MOD-RX | RX-ELRS + antenna on PS-06 | CN-19 | yes |
| MOD-CAM | camera + pan/tilt + blower + duct on PS-10/11 | CN-09/10/12 + Rail A feed pigtail (CN-24) + **CN-16 camera-USB at the deck edge (S3, per DN-11)** | **yes — gated module** |
| MOD-RLD | rear tail: LGT-LED-BRK, SNS-HALL, SRV-DRS extension | CN-13/15/11 | tail pull-through |
| MOD-BODY | shell: LGT-LED-HALO (+ spare pin) | **CN-14 at PS-07** | with the shell |
| MOD-SVC | USB pigtails (optional, DN-08) | CN-25 (USB parked ends) | — |

**Aliases:** `CN-DECK` (used in Reports I/K) **= CN-07**; `CN-BODY` **= CN-14**. The
numeric IDs are authoritative.

**Solder-vs-connector policy:** solder inside modules (camera↔WiFi USB D± per BOM —
CONFIRMED soldered; divider inline; LED tail to its strip). **Disconnect mandatory** at
every module boundary above, at both moving-interface crossings (gimbal, wing), and at
the body shell (one CN-14). **Bulkhead-style** interface only at PS-07 (body) and the
CN-07 deck anchor — more bulkheads were rejected (K). **Service loops required** at:
deck (50 mm at CN-07), gimbal axes (60 mm), body disconnect (80 mm), Hall (60 mm
pull-through), tail (80 mm). **Spare conductors justified** only in CN-07 (2) and
CN-14 (1). **Excessive connectorization rejected:** none mid-run in any rail.

**(S3 correction — DN-11, risk E-26):** Session 2 carried the camera↔WiFi USB D± run
as solder-only "inside the gimbal module" (BOM bench note) — but VID-WIFI sits on
**MOD-DECK** and the camera in **MOD-CAM**, so the soldered run crosses a module
boundary, defeating both modules' one-piece removal (Q deck-out drill) and violating
this file's own rule that every module boundary is a connector. Correction: **CN-16**
(matrix below), seated at the **deck forward-inboard edge beside the CN-07 anchor** so
deck-out stays a one-station operation; the long run stays dressed in R1 with the
chassis/camera side. USB-2.0 signal integrity through CN-16 must be **bench-verified at
Gate P4** before the BOM solder note is amended — owner decision **DN-11** (fallback:
keep solder-only and document deck + camera module as one combined service unit).

## M.2 Connector matrix

Family defaults: power = XT60/XT30 (keyed, latching by friction, polarized); servo =
JR 3-pin **with printed retention clip** (PS-08 comb feature); signal/LED/sensor =
JST-XH 2.54 (keyed, latched); RF = U.FL (VID-ANT) — replace-not-repair items.
M/F rule: **the side that can be live gets female/shrouded contacts.**

| CN | Harness | From → To | Purpose | V | I prov.* | Cond. | Family (alt) | Gauge* | Len.* | Mount / exit | Cycles | ASM in/out |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CN-01 | H-01 | PWR-BAT → PS-15 | battery main | 7.4 | 30+ | 2 | XT60 (—) | 14–16 | 80 | PS-15 fwd seat | high | 15 / Q-bat |
| CN-02 | H-02 | PS-15 loop-key | main disconnect | 7.4 | 30+ | 2 | XT60 loop (switch) | 14–16 | 60 | PS-15 top, cockpit-reach | high | 18 / Q-emerg |
| CN-04 | H-02/03 | PS-15 → DRV-ESC | ESC feed | 7.4 | 30+ | 2 | XT60 (—) | 14–16 | 90 | PS-15 aft | med | 16 |
| CN-05 | H-02 | PS-15 → UBEC-A in | Rail A feed | 7.4 | 3 | 2 | XT30 (solder) | 20 | 70 | fuse side | low | 17 |
| CN-06 | H-02 | PS-15 → UBEC-B in | Rail B feed | 7.4 | 3 | 2 | XT30 (solder) | 20 | 80 | fuse side | low | 17 |
| CN-23A/B | H-04/05 | UBEC outs (ammeter loops) | D-24 test points | 5–6 | 5 | 2 ea | XT30 pair (—) | 18 | 40 | PS-03 top | med | 17 / D-24 |
| CN-07 | H-04+06 | chassis loom → MOD-DECK | **deck bank: 2× 5 V + 2× GND (S3 — one XH contact is ~3 A; deck peak ≈4 A must split across pins), CRSF TX+RX (S3 — CRSF is a 2-conductor UART pair, per CN-19), ESC sig, LED-brk data, LED-halo data, ADC, Hall, +2 spare** | 5 | 4 | ~12 (S3) | 2× JST-XH ganged in printed shroud (Micro-Fit 3.0 — 5 A/pin — if D-24 confirms >3 A on a power pin) | 22–24 | 50 loop | PS-04 fwd-inboard anchor | **high** | 22 / Q-deck |
| CN-08 | H-05 | Rail B → SRV-STEER | steering | 5–6 | 3 | 3 | JR+clip (—) | 20 | 60 | R2 at KO-19 exit | med | 06 |
| CN-09/10 | H-05/07 | Rail B → SRV-PAN/TILT | gimbal | 5 | 1 ea | 3 ea | JR+clip (—) | 22 | 100 | module base | med | 26 / Q-cam |
| CN-11 | H-08 | Rail B ext → SRV-DRS | DRS | 5 | 1 | 3 | JR+clip (—) | 22 | 150 | rear stack edge | med | 28 / Q-wing |
| CN-12 | H-05 | Rail B → COOL-BLOW | blower | 5 | 0.3 | 2 | JST-XH (stock XH) | 24 | 80 | module base | med | 29 |
| CN-13 | H-08 | tail → LGT-LED-BRK | brake LED | 5 | 0.6 | 3 | JST-XH (solder+loop) | 24 | 120 | PS-09 end | low | 13 |
| CN-14 | H-09 | chassis → MOD-BODY | halo LED + spare | 5 | 0.7 | 4 | JST-XH at PS-07 (—) | 24 | 80 loop | cockpit rim | **high** | 27 / every body-off |
| CN-15 | H-08 | tail → SNS-HALL | wheel speed | 5 | 0.02 | 3 | JST-XH (solder) | 26–28 | 100 | X1 station | low | 24 |
| CN-16 (S3) | H-07 | VID-CAM USB run → VID-WIFI (deck) | camera↔WiFi USB D± module boundary (**DN-11**) | sig (USB 2.0) | — | 3–4 (D+, D−, GND, +shield/spare) | JST-SH/GH 4p latched, signal-grade (solder-only = DN-11 fallback) | 28–30 twisted | in H-07 ≤150 | deck fwd-inboard edge, beside CN-07 anchor | **high** (every deck-out) | 26 / Q-deck + Q-cam |
| CN-19 | H-06 | RX-ELRS → deck | CRSF | 5 | 0.1 | 4 | JST-XH (RX stock) | 26 | 90 | PS-06 aft | med | 23 |
| CN-20 | H-02 | PS-15 spare tap | FUT-EXP | 7.4 | 3 | 2 | XT30 capped | — | — | tap row | — | — |
| CN-21 | H-06 | AUD-AMP → AUD-SPK | speaker | — | 1 | 2 | JST-XH (solder) | 24 | 60–150 (DN-07) | deck edge | low | 22 |
| CN-22 | H-06 | CTL-E1 → ESC signal | throttle (**red wire REMOVED/insulated — DN-03**) | sig | — | 2+shield opt | JR, red pin blanked | 26 | 70 | ESC lead | low | 16 |
| CN-24 | H-04 | Rail A → MOD-CAM feed | camera/WiFi 5 V | 5 | 2.5 | 2 | XT30 (JST-XH if <2 A after D-24) | 20 | 90 | module base | med | 26 |
| CN-17/18 | H-10 | VID-WIFI → VID-ANT | 5.8 GHz RF | — | — | coax | U.FL (—) | — | ≤80 | pigtail guides | low | 30 |
| CN-25 | H-11 | E1/E2 USB → PS-17 park | programming (opt) | 5 | 0.5 | — | micro-USB pigtail | — | 150 | cockpit rim | med | 31 |

\* provisional; **final at Gate P9 after D-24** (current), D-10 (lengths).

Twisting/shielding: motor phase wires kept short + together (H-03); servo leads
twisted; CRSF twisted; ADC + Hall runs twisted with their grounds; LED data with its
ground return; coax untouched. No shield terminations planned at 2S power levels —
revisit only if D-20 shows noise.

## M.3 Labeling convention

- Connector flags: heat-shrink flag `CN-xx` at every mate, both halves.
- Rail colour code: **Rail A = blue** marker band, **Rail B = yellow**, battery-voltage
  = **red**, signal = white, ground = black wire (or black band).
- Harness sleeves: `H-xx` printed flag at each end + at crossings X1/X2.
- Module tags: `MOD-…` on the printed carrier (embossed where the part allows).
- The D-24 bridge plugs (CN-23) are labelled `BRIDGE — REMOVE TO MEASURE`.
