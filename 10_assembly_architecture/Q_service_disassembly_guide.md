# Q · Service & Disassembly Guide

Session 2 · 2026-07-18. Rule zero: **normal maintenance never requires desoldering**
(M module boundaries guarantee it). Rule one: battery disconnected (CN-01/CN-02) before
any hands-in service; no service while the drivetrain can spin. Tools baseline: hex
1.5/2/2.5, small Phillips (servo horns), fingers. Timed targets are demonstrated at
ASM-47 and re-run at Gate P10.

| Operation | Remove | Disconnect | Tools | Sequence & notes | Recalibrate after | Wire-damage risk | Desolder? |
|---|---|---|---|---|---|---|---|
| **Emergency kill** | — | **CN-02 loop-key** through cockpit opening (DN-02) | none | pull key; ≤2 s | no | none | no |
| **Battery swap** | body (3× M3 into inserts) | CN-01, strap | hex 2 | body off (≤30 s, one CN-14 unplug) → strap → pack out of PS-01; target <60 s body-off | no | low (H-01 short) | no |
| **Body removal** | 3× M3 | CN-14 at PS-07 | hex 2 | lift clamshell vertically (KO-14); park on soft surface (paint) | no | low — 80 mm loop | no |
| **Deck-out (MOD-DECK)** | body → 2× M3 (inserts) at deck front | CN-07 bank, **CN-16 camera-USB at deck edge (S3/DN-11)**, CN-17/18 U.FL (at posts) | hex 2 | unplug bank + CN-16 → front screws → unhook rear → lift; target <60 s | no | medium — U.FL fragile: handle at guides | no |
| **ESP programming / USB** | per DN-08: none (pigtails at PS-17) or body-off | — | USB cable | if pigtail route: connect at cockpit rim; else body off + reach deck USB windows. **(S3) Rails OFF (CN-02 key out) during any USB session unless the dev boards' USB-isolation diodes are verified at Gate P4 — a laptop port must never back-feed Rail A (VID-WIFI alone can pull ~2 A; O.4)** | no | low | no |
| **Steering-servo service** | body; PS-01 tray *if* D-26 shows overlap; linkage ball-ends off horn | CN-08 | hex 2, Phillips | open linkage → holder screws → servo out; **re-centre in firmware before relinking (ASM-07/08 repeat)** | **yes — centre + toe** | medium (lead through X1) | no |
| **Receiver replacement** | body | CN-19 | none | peel RX from PS-06 pad, antenna out of guide; re-seat antenna in guide (geometry!) | re-bind; D-20 spot-check | low | no |
| **Antenna replacement** | body | U.FL at module (VID-ANT) / none (RX whip) | none | unzip from posts/guide; support U.FL at connector | RSSI spot-check | U.FL fragile | no |
| **Camera replacement** | body → MOD-CAM module | CN-09/10/12/24 + **CN-16 at deck edge (S3/DN-11 — H-07 run un-dresses from R1 with the module)** | hex 2 | module out whole → bench: duct off (PS-11), board out of soft mount — mount survives (Gate C rule) | **boresight + roll (ASM-26 checks)** | medium at gimbal loops | **no** at the car (S3: CN-16 unplugs the USB run; the camera-side solder joint stays inside the module — board swap on the bench remains solder work) |
| **Gimbal servo replacement** | as camera module | CN-09/10 | Phillips | at bench; note horn spline position before removal | **gimbal centre; hard-stop re-record** | low | no |
| **Comms/WiFi module swap** | deck-out | USB pad joint is soldered — swap = re-solder **at bench** | iron (bench) | deck out → heatsink transfer → 4 solder pads (documented exception: modem swap is repair, not maintenance) | video re-check (ASM-40/41) | low | **yes — repair-class only** |
| **ESC replacement** | body | CN-04, CN-22, 3 motor bullets, fan gap re-check | hex 2 | strap off PS-02 → out; re-set sensored mode; phase order per ASM-16 note | ESC calibration per manual | low | no |
| **Regulator (UBEC) replacement** | body → deck-out | CN-05/06 in, CN-23 out | hex 2 | lift from PS-03 ribs; re-verify rail voltage (ASM-21) before deck-in | rail voltage check | low | no |
| **Fan/blower replacement** | body | CN-12 | none | off PS-11; duct check after | airflow felt-check | low | no |
| **DRS service** | body (wing stays on chassis) | CN-11 | Phillips | pocket access per drawing `[2]`; rod off horn first | DRS endpoints re-check | low (loop at stack) | no |
| **Rear LED tail service** | none (designed pull-through) | CN-13 (+CN-15 if shared pull) | none | pull old tail back through PS-09 with a draw string tied on; reverse to install | LED test pattern | medium — use the draw-string method, never bare-pull | no |
| **Hall sensor service** | none | CN-15 at X1 | none | pull service loop, PS-16 clip open, re-gauge 1–3 mm gap | telemetry spot-check | low | no |
| **Lower-layer access (PS-15/UBEC/harness)** | body → deck-out (→ battery out for Z3L work) | per zone | hex 2 | everything at floor level is reachable with deck + battery out — by design (H.4) | per subsystem touched | low | no |
| **Fuse replacement** | body (or cockpit reach if seat allows) | — | fingers | mini-blade from PS-15 seat; **investigate the cause before re-powering** | ASM-35 style limited power-up | none | no |

**Wear-item watchlist:** 3 body-boss inserts (E-08 — inspect at every 10th body-off),
CN-07 bank (high-cycle — inspect latches), U.FL connectors (rated ~30 mates — replace
pigtail, not module), strap hook-and-loop, TP-labelled anything (must never be found
on the car — E-22).
