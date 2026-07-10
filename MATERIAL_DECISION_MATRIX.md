# Material Decision Matrix

Which filament for which part and why — built around **what's already on the shelf**
(Bambu X1 Carbon, AMS rev 1, all 1.75 mm). Re-evaluated skeptically from
`docs/print_spec_v2.md` per Vitaliy's 2026-07-10 decision: *prefer beginner-safe,
keep harder materials only where the case is genuinely strong.* New decisions get
logged in the **Decision log** at the bottom (template: `PRINT_LOG_TEMPLATE.md` §3).

## Filament on hand (2026-07-10)

| Material | Colors / spools | Use here |
|---|---|---|
| PLA matte | beige ×3, grey ×2, white, black ×2, green | **body shell (black)**, optional cosmetics, test coupons |
| PLA (regular) | black ×2 | body backup / coupons |
| PLA white-transparent | ×1 | **brake-light diffuser** (matches spec exactly) |
| PETG high-speed (HF) | blue ×2, black | **wheels, front suspension, floor, camera duct** |
| Wood PETG | ×1 | ⚠ cosmetic only — wood-fill is weaker + abrasive-ish; NOT for loaded parts |
| ASA | black ×2 | **rear axle + drivetrain** (group 02) |
| TPU 90A | translucent blue ×2, green ×2, red | no required use — see TPU section |
| Misc (orange, …) | assorted | coupons, jigs |

**No purchases needed to start.** The only *candidate* gap: a dedicated silver/grey
spool is NOT needed — the silver nose is painted, not printed silver (print white/grey
matte PLA, on hand).

## Per-group decisions

| Part group | Material | Why | Deviation from spec? |
|---|---|---|---|
| Body shell (06) | **PLA matte black** | cosmetic; matte hides layer lines, black base = fewer paint coats; PLA is the easiest to print + sand at fine layers | none |
| Brake-light diffuser (07) | **PLA white-transparent** | must transmit WS2812 light; spec asks white/natural translucent | none — spec allowed PLA or PETG; PLA chosen (on hand, easier) |
| Floor (05) | **PETG (HF black or blue)** | load-bearing, low to the ground, may sit in sun inside a black car; PETG's higher Tg (~80 °C vs PLA ~60 °C) and toughness | none |
| Front suspension + steering (03) | **PETG (HF)** | loaded but away from motor heat; PETG is far more beginner-friendly than ASA and tough enough | none (spec: PETG preferred, ASA optional) |
| Wheels: rims, nuts, adapters (04) | **PETG (HF)** | loaded; hidden under tyres; PETG grips CA glue well for tyre bonding | none — plus heat-watch note on rear adapters (below) |
| Rear axle + drivetrain (02) | **ASA black** | KEPT after re-evaluation — see the ASA case below | none |
| Camera duct (08, gated) | **PETG** | sits against a hot camera; PLA would creep | none |
| Optional cosmetics | **PLA matte** (any color — painted anyway) | easiest; not safety-relevant | none |
| Test coupons | same material as the part they de-risk | a PLA coupon tells you nothing about ASA shrinkage | n/a |

### The ASA decision (re-evaluated, kept)

The beginner-safe instinct says "swap ASA → PETG". Re-checked honestly:

- **For ASA:** the rear drivetrain is the *documented failure point* of this design —
  Ryan added 14 mm metal axle sleeves specifically because printed parts melted near
  the motor/axle. ASA Tg ≈ 100 °C vs PETG ≈ 80 °C. Parts are 100% infill, small, hidden.
  Two ASA spools are on hand and the X1C is enclosed — the two classic blockers
  (no enclosure, no stock) don't apply.
- **Against:** styrene fumes (needs room ventilation + closed door, activated-carbon
  filter helps), more warp-prone (small parts + brim mitigate), one more material for a
  beginner to learn.
- **Verdict:** keep ASA for group 02 only. The parts are small and low-drama to print
  (the hard ASA failure mode is big flat parts warping — these aren't). Mitigations:
  print the **ASA test coupon first**, brim 5–8 mm, enclosed, ventilate during + after,
  slow cooldown. If ASA proves miserable, the honest fallback is **PETG + strict
  reliance on the metal sleeves + a heat check after the first minutes of driving** —
  acceptable but strictly worse; log it as a deviation if taken.

### Materials considered and rejected for this project

- **ABS:** everything ASA does, slightly worse UV/warp behavior — no reason when ASA is on hand.
- **PA / Nylon, PA-CF, PET-CF:** genuinely stronger, but hygroscopic to the point of
  needing a drybox workflow, expensive, and overkill for a 1/10 cosmetic-first build.
  A carbon-filled spool also demands a hardened nozzle (X1C has one) but adds zero
  visual value and real beginner complexity. **Not worth it** — revisit only if a
  specific part keeps breaking in crashes.
- **PC:** too demanding for the benefit here.
- **Silk/glitter/translucent PLA for the body:** telegraphs through paint, sands badly
  (spec agrees). Wood PETG same verdict for anything structural or painted-smooth.

### TPU 90A (on hand, no required use)

No part in the locked build calls for TPU. Honest options if wanted later: a front-wing
sacrificial bumper strip, or internal vibration pads under electronics mounts — both are
**redesigns, not existing STLs**; log as MD entries if pursued. Practical notes: AMS
rev 1 **cannot feed TPU** — external spool holder + direct path; print slow (~25 mm/s
for 90A); translucent colors are fine since these parts would be hidden. Do NOT use the
printed tyres/rims path for TPU — the build uses real Tamiya rubber.

## Heat map (which parts see heat, honest version)

| Zone | Heat source | Parts | Risk if PLA |
|---|---|---|---|
| Rear axle / motor | motor + drivetrain friction | group 02, rear tyre-slot adapters | deforms — documented; hence ASA + metal sleeves |
| Camera / nose | OpenIPC camera runs hot | camera duct, camera top pod | duct creeps (PETG); the PLA pod is a ⚠ watch item — if it softens, reprint pod in PETG and repaint |
| Floor | summer sun on black car | group 05 | sag over time — hence PETG |
| Body shell | sun only | group 06 | PLA accepted (cosmetic; garage the car in heat waves). ⚠ Don't leave the car in a parked car interior — PLA *will* warp there. |
| Battery bay | 2S LiPo mild warmth | floor tub | PETG floor covers it |

## Drying table (all these are hygroscopic)

Dry when you see stringing, popping sounds, or matte/rough extrusion. X1C chamber or a
filament dryer; AMS with fresh desiccant keeps dried spools dry.

| Material | Dry at | Duration |
|---|---|---|
| PLA | 45–50 °C | 6–8 h (rarely needed unless spools sat out) |
| PETG | 60–65 °C | 6–8 h (**likely needed** — HF PETG strings when damp) |
| ASA | 75–80 °C | 8 h (do this before the group-02 batch) |
| TPU | 55–60 °C | 8–12 h (very hygroscopic) |

## AMS slot planning

One material per plate/print (no multi-material prints in this project). Suggested
loadout per phase: coupons/body phase → PLA matte black + white-transparent + spare;
mechanical phase → PETG HF ×2 + ASA (ASA can also feed from external spool if AMS path
is finicky with it — some ASA spools are moisture-sensitive in the AMS without fresh
desiccant). TPU never in the AMS (rev 1 limitation).

## ⚠ High-speed PETG caveat (honest flag)

"High Speed" PETG is tuned for fast printing; at maximum speeds layer adhesion can be
somewhat below classic PETG. For the **structural** groups (02 is ASA anyway, but 03/04/05
PETG parts): use the Strength process preset or manually cap speed (~150 mm/s outer
walls or slower) rather than the fastest profile. This is a settings mitigation, not a
material problem — logged here so nobody slices suspension arms at draft speed.

## Decision log

New/changed material decisions append below using `PRINT_LOG_TEMPLATE.md` §3.

### MD-001 · baseline matrix · 2026-07-10
- **Decision:** the per-group table above.
- **Deviates from docs/print_spec_v2.md?** No material deviations; diffuser narrowed
  to PLA white-transparent (spec allowed PLA/PETG); ASA re-evaluated and kept.
- **Approved by Vitaliy:** direction approved 2026-07-10 ("re-evaluate; prefer
  beginner-safe"); per-part sign-off happens at first print of each group.
- **Revisit if:** ASA printing proves unmanageable (fallback documented above); rear
  tyre-slot adapters soften in driving (→ ASA); camera-top PLA pod softens (→ PETG).
