# O · Thermal, RF/EMI, Vibration & Safety Design

Session 2 · 2026-07-18. Validation: D-19 (thermal), D-20 (RF), Gate P8 body-on. All
airflow statements are design intents with a named physical path — verified, not
assumed, at P8.

## O.1 Thermal architecture

**Heat sources (ranked):** DRV-MOT (hot, rear, documented donor failure zone E-05) →
DRV-ESC (hot, own fan) → VID-WIFI (hot, heatsink mandatory) → VID-CAM (hot, ducted
blower) → UBECs at load (D-19 adds them) → SRV-STEER (warm) → LEDs (mild).

**Airflow path (front-in / rear-out, per the v2 intent, now with named openings):**
- **Inlets:** front-shell lower gaps + cockpit opening (both exist on the donor shell);
  the floor **side vents L/R** (35 × 37 × 20 printed parts) as secondary low inlets.
- **Path:** along the two side bays (R1/R2 keep the loom combed low so air moves over
  the deck and battery), converging at the shell junction.
- **Exhausts:** the **airbox tall channel** acts as the thermal chimney over the deck's
  WiFi slot (this is why VID-WIFI sits in the deck rear slot); rear-shell openings
  around the drivetrain/diffuser region exhaust the motor/ESC pocket. **If the slicer
  assembly (D-01 sitting) shows the rear shell is closed above the motor, a rear vent
  becomes a DECISION-NEEDED body modification — flagged now (DN-10), not discovered
  at P8.**
- **Forced air:** ESC's own fan (≥10 mm free above, PS-02); COOL-BLOW ducted to the
  camera (Gate C duct); no other fans planned.
- **Recirculation risks:** under-deck pocket (mitigated: PS-03 floor slotted, deck
  ribs run fore-aft so the bay is open-ended); sidepod dead air if the speaker port
  blocks flow (checked at D-03).
- **Printed parts near heat:** PS-02, PS-09, PS-16 in **ASA**; PS-04 deck in **PETG**
  (WiFi proximity — not PLA); everything else PETG by default (K rules).
- **Measurement points (D-19):** WiFi heatsink, camera board, ESC case, motor can,
  UBEC-A/B cases, deck underside at the WiFi slot, PS-02 near-fan wall, battery after
  a drive.
- **Test procedure:** bench powered baseline (body off, 10 min idle + load bursts) →
  body-on static repeat → 5-min drive → immediate IR sweep of all points. **(S3)** During
  the body-on static run, confirm flow *direction* with a thread/tissue tell-tale at
  every named inlet and exhaust — buoyant "chimney" flow is weak at standstill and must
  be verified, not assumed; a reversed or dead tell-tale at the airbox channel is a
  fail even if temperatures pass. **Pass
  (provisional):** WiFi heatsink ≤ 70 °C, PETG structure ≤ 55 °C, ASA ≤ 80 °C, battery
  ≤ 45 °C; fail → duct/vent redesign before Gate P9.

## O.2 RF / EMI architecture

- **RX-ELRS:** Z2L front-left, antenna guided **forward** along the shell inside
  (PS-06); ≥40 mm from any metal (turnbuckles/kingpins are the nearest — checked at
  P3); ≥150 mm from the 5.8 GHz posts; ≥80 mm from UBEC switching bodies.
- **VID-WIFI + VID-ANT:** deck rear slot; two whips on PS-12 posts in a shallow V
  (spatial + polarization diversity), tips clear of the shell in the airbox channel
  (RF-transparent PLA above them). Pigtails ≤80 mm, no tight bends. Antennas fitted
  **before power, always** (module protection rule).
- **Coax route:** U.FL pigtails only (no extensions); they never cross H-03.
- **Separation from motor/ESC wiring:** the entire RF corner (Z2L) is diagonal-opposite
  the ESC bay (Z5R); H-03 stays right-rear; rule N.1-3 keeps parallel runs ≥20 mm.
- **Crossing rules:** any signal crossing power does so at 90° at X1/X2 only.
- **Body-shell effects:** PLA/PETG is RF-transparent (E-06 note) — but the **silver
  nose paint and any metallic-flake livery coats are not guaranteed transparent**:
  keep both antenna systems out of line-of-sight-through-painted-metallic regions;
  the W17 black base is carbon-look paint, not carbon fill (verify the chosen cans at
  P8 with a simple RSSI A/B check — recorded as part of D-20).
- **Replacement access:** whips unzip from posts (Q); RX peels from PS-06.
- **ESP32 onboard radios (S3):** both DevKits carry 2.4 GHz WiFi/BT radios. Their
  intended state must be **declared by firmware configuration** (off vs in use); if any
  ESP32 radio is in use it joins the D-20 matrix as a third 2.4 GHz emitter sitting on
  the deck next to the CRSF wiring — test it against ELRS LQ explicitly.
- **Coexistence test (D-20/ASM-41):** ELRS link stats (LQ/RSSI) at range with WiFi
  streaming at max bitrate, body on; then WiFi throughput with ELRS at 100 mW.
  **WiFi module remains a dummy envelope until possession + D-06b (RST-06)** — P8
  cannot pass on the dummy; it waits for the real module.

## O.3 Vibration & crash

- **Rigid mounts:** PS-15, PS-03, PS-02 (strap), PS-16, `Servoholder` (donor).
- **Isolated mounts:** ESP32s on foam pads + standoffs; camera **board** soft-mounted
  inside MOD-CAM (per CAMERA_GIMBAL_PLACEMENT §3 — isolate the board, not the gimbal
  frame, so boresight stays stiff); speaker on TPU/EVA ring (TPU = external spool —
  AMS rev 1 cannot feed it; EVA foam is the no-new-material fallback).
- **Connector retention:** JR plugs get printed clips (PS-08 feature); XT are friction-
  safe; JST-XH latched; U.FL secured by pigtail guides (the connector itself is fragile
  — guides take the load).
- **Cable fatigue:** loops at every moving interface (M.1 list); combs ≤60 mm spacing
  near motion; grommets at PS-09 and floor-slot passes.
- **Thread-locking:** blue thread-lock **metal-to-metal only** (never into plastic —
  ASSEMBLY_NOTES rule); inserts for ≥3-cycle joints.
- **Crash exposure:** nose/wings are consumables (E-17) — that is exactly why **no
  electronics are allocated forward of the front axle** (RST-04/E-24); the deck sits
  inboard of the shell flanks; the battery strap + PS-01 end walls take a 20 g forward
  load; the gimbal module hard-stops must survive a servo stall (KO-13 requirement on
  PS-10, measured under D-18 rules when firmware-gated work unlocks).

## O.4 Safety review (explicit items)

| Item | Treatment |
|---|---|
| Fuse / overcurrent | DN-01 (recommended accessory-branch mini-blade, rated after D-24) — L.3 |
| Main disconnect | DN-02 (recommended loop-key at PS-15, cockpit-reachable) — L.3 |
| Exposed live terminals | all PS-15 contacts recessed; spare taps capped (CN-20) |
| Connector gender | live side = female/shrouded (M.2 rule) |
| Reverse polarity | keyed XT/JST families only; no bare Dupont power |
| Cable abrasion | grommets + chamfered printed edges (K rule) |
| Wire pinching | KO-14 body-lowering check with harness dressed (ASM-33) |
| Battery restraint | PS-01 strap + end walls; balance lead parked |
| Hot surfaces | motor/ESC labelled zone; ASA parts there; post-drive touch rule |
| Rotating drivetrain | H-03 dressed clear; no service while powered (Q rule) |
| Suspension interference | Gate P3 sweep checks with loom dressed |
| Connection sequence | antennas→heatsink→bench-limited→battery (L.3 sequencing) |
| Current-limited first power-up | ASM-35: 0.5 A limit logic-only → 2 A staged rails |
| USB back-powering (S3) | rails OFF (CN-02 key out) during USB programming unless dev-board USB-isolation diodes are verified at Gate P4; never USB-power the deck with VID-WIFI fitted (L.3.1, Q rule) |
