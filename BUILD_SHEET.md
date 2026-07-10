# W17 FPV RC F1 — Build Sheet v3 (print & fabrication scope)

Consolidates `docs/00_BUILD_SHEET_v1.md` + `docs/00_BUILD_SHEET_v2.md` for the
**printing/fabrication side only** and updates them for **home printing on Vitaliy's
Bambu Lab X1 Carbon** (v1/v2 assumed a print shop). Electronics, wiring, GPIOs, power
rails, and radio setup are **out of scope here** — see `docs/00_BUILD_SHEET_v2.md`
(historical copy) and the firmware repos (`w17-control-fw`, `w17-soundlight-fw`).

**Car:** 1/10 FPV RC F1, OpenRC "RC-01" belt-drive chassis, generic 2024 body painted
as **Mercedes W17, #63 (Russell)**. Original deadline 21 Jul 2026 is now a **soft
target** — quality over speed.

---

## Locked configuration (print-relevant)

- **Chassis:** RC-01, **oil-shock** suspension — original floor + original front
  suspension/steering. NOT the Revision-1.1 ball-joint steering, NOT the Rev-1.1 front floor.
- **Body:** generic **2024 body** (`NEW BODY 2024 FRONT 1` + `REAR` + `Mirror` +
  `new halo 2.1` + `camera top 1.1`), painted as W17. Skip Ferrari SF24 / McLaren MCL38 /
  SF23 / RB19 team shells.
- **Wheels:** printed rims + hubs + locking nuts + tyre-slot adapters
  (Thingiverse 5414118 set + "tighter" Rev-1.1 adapters); **bare Tamiya tyres glued on**.
- **Drive:** belt drive; printed motor locks, axle holders, spacers (metal sleeves protect
  printed spacers from heat).

## Key numbers (tape-to-the-bench)

| What | Value |
|---|---|
| Rim bead Ø | **44 mm front / 47 mm rear** (matches measured STLs) |
| Tyres | **Tamiya 54198** (front, 30 mm wide) + **Tamiya 51400** (rear, 35 mm), 64 mm OD |
| Front bearings | 8×12×3.5 mm ×4 |
| Rear bearings | 6801 (12×21×5) ×2 |
| Shocks | 52 mm front / 68 mm rear (v1 said 51 mm front — see appendix) |
| Gears | 28T pinion / 75T spur, both **48-pitch** |
| Battery envelope | **≤75×45×25 mm 2S** (governs — see appendix on the 115 mm conflict) |
| King-pin bore | 3 mm (verify in slicer) |
| Nozzle / default layer | 0.4 mm / 0.2 mm (0.12–0.16 mm on visible bodywork) |

## Print order (build sequence)

Materials and full slicer settings live in `MATERIAL_DECISION_MATRIX.md` and
`PRINT_SPEC.md`; per-file status lives in `MODEL_INVENTORY.md`. Order:

| # | Group | Material (headline) | Gate before printing |
|---|---|---|---|
| 0 | **Test coupons** (bearing-seat + tyre-bead + tolerance coupons) | one per material in use | none — start here |
| 1 | **1 rim + 1 hub + adapters** → test-fit one Tamiya tyre + bearing | PETG | coupons measured OK; **tyres purchased** |
| 2 | Remaining 3 rims, hubs (mirror the Right hub for Left!), nuts, adapters | PETG (+ASA rear hub) | tyre + bearing fit confirmed |
| 3 | **Rear axle + drivetrain** (axle holders, motor locks, spacers, 68 mm shock mount) | ASA | ⚠ **spring-mount rocker slicer check** (below) |
| 4 | **Front suspension + steering** (original oil-shock set) | PETG | — |
| 5 | **Floor** (original front floor + back floor + floorboard + diffuser + side vents) | PETG | — |
| 6 | **Body shell** (front + rear + mirror + halo + camera top) — start early, paint is the long pole | PLA matte black | fine-layer profile test on a body offcut region first |
| 7 | **Brake-light diffuser** (`rearbacklightdiffuser`) | white/translucent, lens unpainted | — |
| 8 | **Camera cooling duct** (from `camera_blower_duct.scad`) | PETG | ⚠ camera + ACP2006 blower measured |
| 9 | Extras (wall mount display, driver figure, DRS arm if used) | any | explicitly optional |

**Golden rule (from v1/v2, unchanged):** layer lines are the weak axis — orient every
stressed part so the load runs **along** the layers, not across them. This matters more
than infill percentage.

## Open gates (must be resolved by a human before the affected print)

1. ⚠ **Rear shock mount:** confirm in Bambu Studio that `Spring mount 2 REVISION 1`'s
   rocker seats the **68 mm** coilover. Yes → hybrid rocker + revised rear motor covers.
   No → original rear mount; skip `RearSpringMountREV4` + `springblock`.
2. ⚠ **Camera duct:** render `camera_blower_duct.scad` only after measuring the real
   camera + blower; the .scad parameters are placeholders.
3. ⚠ **Front wheel hub:** only a **Right** hub STL exists — mirror it in Bambu Studio
   for the Left. Verify the mirrored bearing seat too.
4. ⚠ **Tyre purchase:** Tamiya 54198 + 51400 status unknown; needed by step 1.
5. ⚠ **Battery purchase:** buy to **≤75×45×25 mm** (see appendix), carry 2.

## Finishing (summary — full method in `FINISHING_GUIDE.md`)

Prime everything visible (grey; **white** under silver-nose + Petronas turquoise areas)
→ base/accent paint → **gloss clear** → decals → final clear (satin/matte to taste)
→ cure → assemble. **Mask the diffuser lens — never paint it** (red comes from the
WS2812 via firmware).

---

## Appendix — v1 → v2 → v3: what changed and why

Resolved in favor of **v2** wherever v1 and v2 disagree (v2 explicitly supersedes v1);
v3 changes only the shop→home-printer assumption and scopes out electronics.

| Topic | v1 said | v2/spec says | v3 (this doc) |
|---|---|---|---|
| Wheel material | hubs + tyre slots in **ASA** (group 2) | **PETG** rims/nuts/adapters, ASA only rear hub | v2 — wheels aren't near motor heat; PETG is tough and easier |
| Motor/ESC | "sensored 17.5T", ESC 10BL120 | drops turn count; pins 28T/75T 48P | electronics out of scope here; gears kept (print-relevant mesh) |
| Front shock length | 51 mm (Ryan's parts list; v1 implies) | **52 mm** | v2 value; ⚠ minor unresolved 1 mm discrepancy vs Ryan's list — measure the actual shocks on arrival |
| Diffuser | body-group afterthought | own group: translucent, lens unpainted | v2 |
| Camera duct | absent | PETG duct from .scad | v2, gated on measurement |
| Printer | print shop ("shop stocks ASA") | print shop | **home X1C** — ASA availability solved (2 spools on hand, enclosed printer); ventilation duty moves to us, see `PRINT_SPEC.md` safety |
| Battery envelope | ≤75×45×25 | ≤75×45×25 | unchanged. ⚠ Ryan's `Parts List.txt` says 115×35×24 — that battery **will not fit the 2024 body**; the READ ME for the 2024 body itself confirms ≤75 mm. Buy to 75 mm. |
| Deadline | none | 21 Jul 2026 | soft target (user decision 2026-07-10) |

Unresolved items intentionally carried forward: spring-mount rocker check (open in both
v1 and v2), camera-duct measurements. Nothing has been physically printed as of
2026-07-10 — see `05_printed_parts_log/PRINT_LOG.md` for live status.
