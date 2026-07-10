# Assembly Notes — printed-part assembly map

How the printed parts go together: which supplier drawings/photos cover which stage,
what fasteners and hardware each stage needs, and per-stage checklists. Session records
go in `07_assembly_notes/` using the template in `PRINT_LOG_TEMPLATE.md` §5.

> ⚠ **Scope + caveats.** This maps the *supplier's* instructions for the stock RC-01 —
> our build deviates (own electronics, FPV camera, W17 paint), so treat drawings as
> geometry reference, not gospel. Electronics installation is owned by the firmware
> repos and `docs/00_BUILD_SHEET_v2.md`, not this file. Drawings `[0][1][2][3][5][7]`
> **were visually reviewed 2026-07-10** (key findings below); `[4][6][8][9]` and the
> photos still haven't been — verify against the actual pages as you use them.

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

### Key findings from the reviewed drawings (2026-07-10)

- **`[2]` Floor:** the **"Servo Holder" is a floor part** (→ `Servoholder.stl`,
  now required); the **rear wing mounts on the floor's spring-mount tower**, not the
  body; **"Insert small DRS Servo here (optional)"** + a metal rod to the servo horn —
  DRS was designed in from the start. Floor set in the drawing: Front Floor, Rear
  Floor, Rear Floor 2 (bendable — thin metal rod through the hole), Floorboard,
  Side Vents L/R, Diffuser — matches our group 05. 12× M3 nuts sit in floor slots.
- **`[3]` Front suspension:** the steering servo is NOT in the front assembly — a
  **long rod links the servo to the servo-saver** ("mount this hole with a rod to the
  steering servo motor"). Guide rods tap in gently with a hammer. Front assembly locks
  to the floor with nuts.
- **`[1]` Body (2023-era):** nose and front wing are always **separate printed parts**
  bolted on (12× M3 pattern) — no rear wing in the body drawing (it's on the chassis).
- **`[5]` Rev-1 body upgrades:** shows "Revised Front Nose" (=`FRONTNOSE2024`) and
  "Revised Front Wing" (=`2024 Revised Front Wing`) as separate parts, installed "as
  per original instructions".
- **`[7]` Rev-1 rear axle:** the Rev-1 stack seats the **bearings in the Motor Cover
  L/R parts** (no separate axle holders visible!), bolts **diffuser + rear wing +
  backplate** together with M3 (don't touch the axle), retains rear wheels by an
  **M4 bolt through the tyreslot into the axle**, and has a **"Pass LED here
  (optional)"** channel + "Light Cover" at the brake-light position. Non-printed:
  Tamiya F104 rim + tyre, M3/M4 bolts, 2 bearings.

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
| M4 rod-end ball joints | 24 mm | pack (BOM v2) | steering links |
| Turnbuckles | 3×32 mm | 2 (+crash spares) (BOM v2) | adjustable toe links — the crash-snap item |
| M3 ball studs | Tamiya/Sakura style | pack (BOM v2) | pivot balls the rod ends clip onto |
| King pins | M3×30 mm dowel + circlip | 2 (+spares) (BOM v2) | knuckle pivots — ⚠ confirm 3 mm bore in slicer |
| Steering servo | DS3235SG (standard size), 25T horn | 1 (in transit) | into `Servoholder` on the rear floor — ⚠ fit-check on arrival |
| DRS servo | MG90S micro, positional | 1 of 3 (in transit) | into the chosen rear wing's pocket + metal rod to horn (drawing `[2]`) |
| Front shocks | 52 mm ordered (BOM v2) | 2 (+spares) | ⚠ 51 (Ryan) vs 52 mm (v2) — measure on arrival |
| Rear shock | 68 mm (HSP, ordered) | 1 (+spare) | rear stack — gate #1 in `BUILD_SHEET.md` |
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
- [ ] Bearing carriers per resolved Gate A: original path = axle holders (L/R);
      Rev-1 path = bearings seat in the Motor Covers (drawing `[7]`)
- [ ] Motor lock, spur/pinion mesh (48P both, slight backlash)
- [ ] 68 mm shock into chosen mount (per resolved gate #1)
- [ ] Rear wing onto the chosen stack (+ DRS servo in pocket, metal rod to horn)
- [ ] Rear wheels onto axle via tyre-slot adapters (M4 bolt through tyreslot into
      axle per `[7]`) — there is **no separate rear-hub part** (v2's "ASA rear hub"
      has no matching STL); axle spins free, no wobble

### Stage 3 — Front suspension + steering
- [ ] Drawing `[3]`; original oil-shock parts only (no Rev 1.1 steering)
- [ ] King pins ~3 mm bore verified; uprights pivot freely
- [ ] Steering servo into `Servoholder` on the rear floor; long rod to the
      servo-saver (drawing `[3]`) — centre the servo in firmware BEFORE linkage
- [ ] M4 tie rods + turnbuckles + ball studs; equal lengths L/R before trim
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
- [ ] Nose (`FRONTNOSE2024`, silver) bolts to the front floor per the body READ ME;
      front wing per drawing `[5]`/original instructions
- [ ] Halo, mirrors, camera-top pod, brake-light diffuser (lens unpainted, WS2812 seated)
- [ ] Rear wing is a Stage-2 (chassis) item, not a body item — verify it cleared
      Stage 2 with DRS actuating before final body fit
- [ ] Wings: check for crash-sacrificial mounting (see `FINISHING_GUIDE.md` realism-vs-durability)

**Plastic-thread golden rule:** snug, not tight; re-threading the same plastic hole
repeatedly wears it — if a boss will see >3 assemble/disassemble cycles, fit an insert.
