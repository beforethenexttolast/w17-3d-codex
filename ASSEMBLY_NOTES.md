# Assembly Notes — printed-part assembly map

How the printed parts go together: which supplier drawings/photos cover which stage,
what fasteners and hardware each stage needs, and per-stage checklists. Session records
go in `07_assembly_notes/` using the template in `PRINT_LOG_TEMPLATE.md` §5.

> ⚠ **Scope + caveats.** This maps the *supplier's* instructions for the stock RC-01 —
> our build deviates (own electronics, FPV camera, W17 paint), so treat drawings as
> geometry reference, not gospel. Electronics installation is owned by the firmware
> repos and `docs/00_BUILD_SHEET_v2.md`, not this file. The PDFs/photos have **not been
> visually reviewed by Claude** (binary files) — the mapping below is from their
> filenames and READ MEs; verify against the actual pages as you use them.

---

## Reference material map (all paths under `unsorted_stl_raw/`)

### Drawings — original car (Ryan's Creations)
`Ryans Creations Open RC F1 Car/Drawings for Installation/`

| PDF | Covers | Used in stage |
|---|---|---|
| `[0] FULL CAR.pdf` | complete car overview | orientation, any stage |
| `[0] FULL CAR EXPLODED VIEW.pdf` | every part exploded | part identification |
| `[1] BODY ASSEMBLY.pdf` | body shell + nose + wings mounting | Stage 6 |
| `[2] FLOOR ASSEMBLY.pdf` | floor + diffuser + side vents | Stage 4 |
| `[3] FRONT SUSPENSION ASSEMBLY.pdf` | front arms, uprights, shocks, steering | Stage 3 |

### Drawings — Revision 1 upgrades
`RC-01 Revision 1 Files/Revised Drawings/` (same set duplicated inside
`RC-01 Revision 1.1/Original + Revision 1 Files…/RC-01 Revision 1 Files/Revised Drawings/`)

| PDF | Covers | Used in stage |
|---|---|---|
| `[4] REVISED FILES.pdf` | what Revision 1 changed | pre-read before printing |
| `[5] BODY UPGRADES.pdf` | revised wing/nose/rear cover | Stage 6 |
| `[6] FLOOR UPGRADES.pdf` | revised floor suspension parts | Stage 4 (only if used) |
| `[7] REAR AXLE UPGRADES.pdf` | rear axle holders, motor covers, spring mounts | Stage 2 |
| `[8] FRONT AXLE UPGRADES.pdf` | revised front axle parts | Stage 3 (only if used) |
| `[9] FINAL REVISED INSTALLATION.pdf` | full revised install | any |

### Photos
`RC-01 Revision 1.1/Photos to help installation/` — 24 real build photos
(Rev 1.1-era build; useful even though we skip the 1.1 steering). Support contact in
its READ ME (ryanscreations28@gmail.com).

---

## Hardware / fastener list

From `Ryans Creations Open RC F1 Car/Parts List.txt` (mechanical section), adjusted to
our locked config. Electronics rows intentionally omitted (our electronics differ —
see `docs/00_BUILD_SHEET_v2.md`).

| Hardware | Spec | Qty | Where used |
|---|---|---|---|
| Front bearings | 8×12×3.5 mm | 4 (2/wheel) | front hubs |
| Rear bearings | 12×21×5 mm (6801) | 2 | rear axle holders |
| M3 bolts | 8 / 10 / 12 / 20 / 30 mm lengths | assorted | everywhere; body uses 3× (self-threading into tight holes per 2024-body READ ME) |
| M3 nuts | standard (+ nylock where vibration) | assorted | — |
| Metal spacers | **14 mm ID**, rear axle | 4 (2/side) | between printed spacers and axle — **heat protection, do not omit** |
| M4 double-sided rod | 40 mm | 2 | steering arms |
| M4 tie rods | 22 mm | 6 (4 steering + 2 servo) | steering linkage |
| Front shocks | Tamiya CVA Super Mini ~51–52 mm | 2 | ⚠ 51 (Ryan) vs 52 mm (build sheet v2) — measure on arrival |
| Rear shock | 68 mm | 1 | rear rocker/mount — gate #1 in `BUILD_SHEET.md` |
| Pinion / spur | 28T / HPI 75T, both 48-pitch | 1+1 | belt drive |
| Heat-set inserts (optional, recommended) | brass **M3 × 5 mm** | pack | high-wear screw bosses — install per `BEGINNER_3D_PRINTING_GUIDE.md`, safety in `FINISHING_GUIDE.md` |
| Metal sleeves (optional) | 5 mm OD × M3, 5 mm long | 4 | replaces printed `GuideRod` in front suspension |
| Tyre glue | CA suitable for rubber tyres | 1 | tyres → printed rims |

## Assembly stages (checklist skeletons)

Order follows the print order in `BUILD_SHEET.md`. Do a **dry fit (no glue, loose
screws) of every stage first**, then final assembly after painting.

### Stage 1 — Wheels
- [ ] Bearings press into hubs (from test-fit gate) — snug, seated square
- [ ] Tyre-slot adapters (tighter Rev 1.1 versions) onto rims
- [ ] Test-fit one Tamiya tyre before final gluing; glue per `FINISHING_GUIDE.md` CA notes
- [ ] Locking nuts thread on without stripping (printed threads — gentle)

### Stage 2 — Rear axle + drivetrain
- [ ] Drawing `[7]`; 14 mm metal sleeves ON THE AXLE before printed spacers
- [ ] Axle holders (L/R), motor lock, spur/pinion mesh (48P both, slight backlash)
- [ ] 68 mm shock into chosen mount (per resolved gate #1)
- [ ] Rear hub (ASA) + wheels; axle spins free, no wobble

### Stage 3 — Front suspension + steering
- [ ] Drawing `[3]`; original oil-shock parts only (no Rev 1.1 steering)
- [ ] King pins ~3 mm bore verified; uprights pivot freely
- [ ] M4 tie rods + servo linkage; equal lengths L/R before trim
- [ ] Shocks mounted; suspension compresses/returns without binding

### Stage 4 — Floor
- [ ] Drawing `[2]`; original floor set (not Rev 1.1 front floor)
- [ ] Diffuser + side vents; floor sits flat, no rock

### Stage 5 — Electronics install
- Out of scope here → firmware repos + `docs/00_BUILD_SHEET_v2.md` packing/rails.
- [ ] Only printed-part duty: mounts/pockets fit their components; nothing rattles.

### Stage 6 — Body + cosmetics (after painting)
- [ ] Drawing `[1]` + 2024-body READ ME: 3× M3 bolts, holes are tight/self-threading —
      thread carefully once, don't strip; consider M3×5 inserts if they wear
- [ ] Halo, mirrors, camera-top pod, brake-light diffuser (lens unpainted, WS2812 seated)
- [ ] Wings: check for crash-sacrificial mounting (see `FINISHING_GUIDE.md` realism-vs-durability)

**Plastic-thread golden rule:** snug, not tight; re-threading the same plastic hole
repeatedly wears it — if a boss will see >3 assemble/disassemble cycles, fit an insert.
