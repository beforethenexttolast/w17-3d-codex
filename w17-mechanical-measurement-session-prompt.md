# Session prompt — the mechanical measurement sitting (calipers, a scale, no power)

Paste into a Claude Code session started at `~/Documents/projects`.
**This file lives at `w17-3d-codex/w17-mechanical-measurement-session-prompt.md`; its links
are relative to that repo, so `../` means the workspace.**

**No power. No battery. No USB. Nothing flashed, nothing connected.** Calipers, a rule, a
depth gauge, a protractor, four kitchen scales, and your eyes.

> **Opus 5, `high`.** Long sitting, one table at a time. It is deliberately *not* an
> assembly session: nothing here is screwed down, glued, or cut. It exists because
> [`w17-3d-codex/10_assembly_architecture/AA_electronics_placement_study.md`](10_assembly_architecture/AA_electronics_placement_study.md)
> and every model in
> [`w17-3d-codex/11_cad/`](11_cad/README.md) are built on numbers that
> have never been measured, and each one is tagged `ASSUMED` until this sitting
> retires it.

---

## What this is for

Twenty-one rows. **M-00** asks what physically exists. **M-01 … M-20** replace guesses
with numbers, ordered by *what unblocks the most*, not by convenience.

Two of them decide whether the design survives at all:

- **M-01 (S0)** — the cage needs `9.82 mm` of an `11 mm` ceiling. That is a coin flip,
  and it is the single measurement that decides whether the second-floor cage is built.
- **M-02 (steering sweep)** — KO-01 is still *provisional*, and it is the most
  restrictive keep-out in the car, sitting exactly where the electronics want to be.

If you only have an hour, do **M-00, M-01, M-02, M-03**. Everything else can wait.

**Nothing here opens a gate.** A2 stays **NOT-EXECUTED** and Phase B stays **BLOCKED**
whatever the numbers say. Measuring is not building.

---

## Before you touch a repo

Run `git worktree list` and `git branch --show-current` in `w17-3d-codex`. If its tree
is on a branch that is not yours, **do not check out** — create a worktree outside
`~/Documents/projects` (see the workspace [`CLAUDE.md`](../CLAUDE.md) → *Concurrent sessions*).

---

## House rules for every row below

1. **Record value, unit, instrument, and date, and tag it `MEASURED`.** This project has
   been burned by order-spec numbers written in as though observed.
2. **Measure the real part, not the datasheet.** Where a row says *the purchased SKU*, it
   means the one in the drawer, not the one in the listing.
3. **Write the datum down too.** A number without the surface it was taken from is not a
   measurement, it is a rumour. Every row below names its datum.
4. **A measurement you could not take is a result.** Write "could not — <why>". Do not
   estimate to fill a cell.
5. **Nothing is forced.** If a dry fit binds, stop and write down where it binds. The fix
   is a relieved part in CAD, never a knife on a servo.
6. **No power at any point**, including "just to see the LED".

**Where the numbers go afterwards:** the `Value` column here, then the matching parameter
in [`w17-3d-codex/11_cad/w17_params.scad`](11_cad/w17_params.scad) — change
the value *and* its tag from `ASSUMED` to `MEASURED(file:line)`, delete its row from that
file's §9, and update §12 of the study. Three places, always all three.

---

## M-00 — What actually exists (do this first, it takes ten minutes)

[`05_printed_parts_log/PRINT_LOG.md`](05_printed_parts_log/PRINT_LOG.md) says **nothing has been printed**. You have said
some parts came back from the print shop. Until this table is filled in, no session can
tell which of those two statements is current — so **fill it in before measuring
anything**, and do not let anyone (including me) guess.

The file list per group is in
[`w17-3d-codex/MODEL_INVENTORY.md`](MODEL_INVENTORY.md) §REQUIRED. Tick the
group, then list the actual parts in the notes column.

| Group (from MODEL_INVENTORY) | Count | Any printed? | Which ones | Condition |
|---|---:|---|---|---|
| 02 — Rear axle + drivetrain (ASA) | 8 | ☐ none ☐ some ☐ all | | |
| 03 — Front suspension + steering (PETG) | 8 | ☐ none ☐ some ☐ all | | |
| 04 — Wheels (PETG) | 7 | ☐ none ☐ some ☐ all | | |
| 05 — Floor (PETG) | 8 | ☐ none ☐ some ☐ all | | |
| 06 — Body shell (PLA matte black) | 7 | ☐ none ☐ some ☐ all | | |
| 07 — Brake-light diffuser | 1 | ☐ none ☐ some ☐ all | | |
| OPTIONAL / UNCERTAIN / anything else | — | ☐ none ☐ some | | |

**Condition,** per part that exists: `good` / `warped` / `layer split` / `supports still
on` / `test print (TP)` / `unknown material`. A part whose **material or settings are
unknown** is a diagnostic part, not a build part — say so, because it changes what a dry
fit proves.

Six parts matter more than the rest for this sitting, so call them out by name:

| Part | Exists? | Why it matters here |
|---|---|---|
| `Servoholder.stl` | ☐ | M-06b: the ~1.7 mm steering-servo interference (OP-B) |
| `FloorBoard2.stl` | ☐ | M-20: the three centreline splice screws (OP-G) |
| `2023NewFrontFloorLargerParts.stl` | ☐ | M-20, and the floor datum DAT-F itself |
| `NEW BODY 2024 REAR.stl` (+ FRONT 1) | ☐ | **M-01 (S0) needs a shell to seat** |
| `2023NEWSideVent1/2.stl` | ☐ | M-15: the charge-flap candidate CF-1 |
| `2021Rearwing with DRS.stl` + `DRS Arm…` | ☐ | M-14: the DRS linkage |

> **If the shell does not exist, M-01 cannot be taken**, and the cage stays a proposal.
> Say so plainly rather than substituting a "close enough" body.

---

## M-01 — S0, the shell-bottom clearance · **the one that decides the cage**

**What:** the height of the seated shell's bottom edge above the floor top (DAT-F), at
**four or more points** around the car.
**Datum:** DAT-F (floor top, `Z = 0`) ↔ the shell's bottom edge, **shell seated and only
lightly pressed** — not clamped, not lifted.
**Tool:** depth gauge or feeler stack. Coupon **C-4**
([`11_cad/fit_check_coupons.scad`](11_cad/fit_check_coupons.scad),
`coupon="c4"`) is a stepped gauge printed for exactly this: slide it in and read the
tallest step that still passes. **Nothing on that gauge stands proud of a step** — the
step numbers are cut *into* the step tops and the handle is deliberately shorter than
the lowest step, so the only thing that can ever stop the gauge going in is the step
itself. (An earlier version had the numbers raised 0.6 mm, which would have made every
reading 0.6 mm high against a margin of 1.18 mm, and in the unsafe direction.) The
steps run **2…11 mm**: if the shell edge is lower than the 2 mm step, record
*"below the lowest step"* — that is a real answer and a serious one, not a failed
measurement.
**Tolerance:** ±0.5 mm.
**Parameter:** `s0_measured`.

| Point | Where (X, side) | Reading (mm) |
|---|---|---|
| 1 | forward, belt side | |
| 2 | forward, mirror side | |
| 3 | rear, belt side | |
| 4 | rear, mirror side | |
| 5 (optional) | over the cassette, either side | |

**Record all readings, not the smallest.** The *spread* is a second result: a shell that
does not sit flat is a different problem from a shell that sits low, and the cage cares
about both.

**How to read the answer:** the cage needs `S0 ≥ 9.82` and S0 is bounded `0…~11`.

- **≥ 9.82** — the cage survives the arithmetic. It still proves no fit.
- **< 9.82** — **stop, and do not shave the cage.** The honest response is to reopen the
  board orientation with a real number in hand, which
  [`ZK_electronics_cassette_fit_study.md:363-364`](10_assembly_architecture/fit_studies/ZK_electronics_cassette_fit_study.md) already demands as a
  production stop. Report the number; the decision is mine.

---

## M-02 — The real steering sweep · **replaces provisional KO-01**

**What:** with the steering assembled, sweep it **lock to lock** and through its bump
travel, and record the rod's swept envelope: height at three stations, and its lateral
extent.
**Datum:** DAT-F for heights; centreline for lateral.
**Tool:** rule + a marker on the rod; photograph both locks.
**Tolerance:** ±2 mm — this is an envelope, not a feature.
**Parameters:** `ko01_z_lo`, `ko01_z_hi`, `ko01_l_half`.

| Station | Rod lowest Z | Rod highest Z | Max \|L\| reached |
|---|---|---|---|
| forward (X ≈ +40) | | | |
| middle (X ≈ 0) | | | |
| rear (X ≈ −40) | | | |

Then: **does anything already fitted enter that envelope?** List it. The current
provisional band is `Z 22…38` at `|L| ≤ 22`, and the PDB sits `8.00 mm` below it with
**zero reserve**.

---

## M-03 — The MH-ET D1-Mini board · **feeds seven parameters, OP-H and OP-I**

**What / datum / tool:** PCB edge; calipers; ±0.2 mm.

| # | Measurement | Value | Parameter |
|---|---|---|---|
| a | length × width, bare PCB | | `esp_len`, `esp_wid` |
| b | PCB thickness | | `esp_pcb_t` |
| c | total thickness **with headers fitted**, at its thickest | | `esp_thk_headers` |
| d | mounting-hole pitch, X and Y, and hole Ø | | `esp_hole_dx/dy/d` |
| e | **which edge carries the service port** — long or short, and which end | | `esp_usb_edge` (and it decides the clip notch) |
| f | **which connector it actually is** — USB-C, micro-USB B, or something else — then its shell width × height and how far it protrudes past the PCB edge | | `esp_usb_type`, `esp_usb_w/h` |
| g | with a cable plugged in: how far the plug body sticks out, and its bend radius | | (service access) |
| h | **component-free zones**: how far in from each edge is the board bare on the outboard face? | | **OP-H / clip stations** |

Row **(f)** is not a formality. **Two project documents disagree about the connector
itself**: `w17-electrical-inputs-for-codex.md:8,10` says *"onboard micro-USB serial …
micro-USB on one short edge"*, and the ZK cassette study's line 102 says *"both USB-C
service ends face X+42"*. Neither is a caliper record, and the CAD, the service-opening
story and the clip notch have all been written for USB-C. **Look at the board and say
which it is** — one sentence retires the whole conflict (study **OP-I**).

Row **(h)** is the one nobody thinks to take and it decides the cage's retention. The
board band is *exactly one board thick*, so the two clips necessarily stand where the
board's outboard components are. Coupon **C-3** is the physical check; this row is the
number that tells us where to put the stations before printing it.

---

## M-04 — Socket stack (if socketing is still on)

Already specified in detail in
[`w17-socket-stack-caliper-prompt.md`](../w17-socket-stack-caliper-prompt.md) — run that
row from there, not from here, and bring back the same GO/NO-GO.
**Parameter:** `esp_socket_stack`. **Tolerance:** ±0.1 mm.

---

## M-05 / M-06 — The PDB

**Datum:** PCB top for heights, board edge for outlines. **Tool:** calipers, ±0.2 mm.

| # | Measurement | Value | Parameter |
|---|---|---|---|
| M-05a | 1000 µF capacitor height above the PCB | | `pdb_stack_h` |
| M-05b | XT60 body height above the PCB | | |
| M-05c | loop-key / XT90-S body, and its **pull axis** | | |
| M-05d | **the tallest thing on the board, whatever it turns out to be** | | `pdb_stack_h` |
| M-06a | finished board outline, L × W | | `pdb_len`, `pdb_wid` |
| M-06b | mounting-hole positions, if any | | |
| M-06c | where every connector exits, and in which direction | | (dock face) |

**M-05d governs the whole cage.** The PDB's audit top is `Z14` and KO-01's bottom is
`Z22`: that is exactly the 8 mm moving-clearance policy with **nothing spare**. If the
real stack is taller than 13 mm, the cage's constraint arithmetic changes.

---

## M-07 — Cassette deck heights

**What:** with the shell seated, the clear height available above the floor at
`X +3`, `X +20`, `X +42`, across `|L| 27…46` on both sides.
**Datum:** DAT-F. **Tool:** depth gauge. **Tolerance:** ±1 mm.
**Parameter:** `guide_top_z`.

| Station | belt side (L−) | mirror side (L+) |
|---|---|---|
| X +3 | | |
| X +20 | | |
| X +42 | | |

The worst value here should agree with M-01 plus the modelled roof (`27.18` at
`X+3 / L−37`). **If it does not, one of the two is wrong** — say which you trust and why.

---

## M-08 / M-09 — Mass and balance

**Tool:** kitchen scale, ±1 g. Four scales for M-09, ±5 g.
**No power, no battery connected** — the pack is weighed on its own, off the car.

| M-08 item | Mass (g) |
|---|---|
| ESP32 #1 with headers | |
| ESP32 #2 with headers | |
| PDB, assembled | |
| charge module | |
| XT90-S loop key + leads | |
| cassette assembly (whatever exists) | |
| pedestal (whatever exists) | |

**M-09 — four-corner weights, rolling assembly**, on a flat surface:

| Corner | Mass (g) |
|---|---|
| front left | |
| front right | |
| rear left | |
| rear right | |

The planning ledger says **36.50 / 63.50 %** front/rear at 1717.6 g. That is
bookkeeping, not a measurement, and **no balance claim may be made and no ballast cut
until this table exists**.

---

## M-10 — Tyre arch clearance

**What:** clearance between tyre and arch at **full steer** and **full bump**, both ends,
body on.
**Tool:** feeler gauge, ±0.5 mm.
The registered margins are **3.5 mm and 4 mm** — already below policy (risk **E-30**), so
this row is looking for a problem that is probably there.

| Corner | at full steer | at full bump | at both together |
|---|---|---|---|
| front left | | | |
| front right | | | |
| rear left | | | |
| rear right | | | |

---

## M-11 — The ESC · **the largest unsolved packaging problem**

**What:** the exact label/variant, the body **with its fan**, its feet, where its wires
exit — and, at every station you would consider putting it, **how much open air is above
it** with the body seated.
**Datum:** DAT-F. **Tool:** calipers + rule, ±0.5 mm. **Parameters:** `esc_*`.

| # | Measurement | Value |
|---|---|---|
| a | full label text / variant | |
| b | body L × W × H **including the fan** | |
| c | foot / mounting-tab positions | |
| d | wire exit faces and directions | |
| e | candidate station 1: where, and clear air above | |
| f | candidate station 2: where, and clear air above | |
| g | candidate station 3: where, and clear air above | |

The measured body is `44.2 × 33.7 × 34.0 mm` and policy wants **10 mm of open air** above
the fan intake — a required plane at `Z 45.5` that **no registered shell station
supplies**, even at `S0 = 11`. This row is looking for a home, not confirming one
(**OP-A**).

---

## M-12 — Shell interior at the charge-flap candidates

**Datum:** shell inner face. **Tool:** calipers, ±0.5 mm. **Parameters:** `flap_*`.

| Candidate | Wall thickness | Local depth behind | What is behind it |
|---|---|---|---|
| CF-1 (side vent) | | | |
| CF-2 (floor opening at X+39.18, \|L\| 55.71) | | | |

**No cut is authorised by this row.** It exists so that the CF-1 / CF-2 decision (**OP-F**)
is made against numbers instead of preference.

---

## M-13 — The SP3T boot-mode selector

No switch has been selected yet. When one is: body L × W × H, throw, the panel cut-out it
needs, and how far its terminals project behind the panel.
**Tool:** calipers, ±0.2 mm. **Parameters:** `sp3t_*`.

Also answer the placement question, because the CAD could not: **the cassette's forward
face below Z14 is entirely PDB.** Where can a hand actually reach a switch, under the
engine cover, with the shell otherwise untouched?

---

## M-14 — DRS geometry (nine rows)

**Rule: never test the pocket alone.** The DRS check runs with the real rear
shock/stack/wing/LED harness present.

| # | Measurement | Datum | Tool | Value |
|---|---|---|---|---|
| a | wing pocket internal L × W × H, and wall thickness | pocket floor | calipers ±0.2 | |
| b | MG90S body, ear pitch, ear hole Ø, boss height, spline height + count, lead exit | servo case face | calipers ±0.2 | |
| c | horn radii actually supplied, each hole | spline centre | calipers ±0.2 | |
| d | **arm pivot-to-pivot spacing**, and both hole Ø | hole centres | calipers ±0.2 | |
| e | flap hinge axis position, and its perpendicular distance to the arm's driven pivot | hinge line | calipers ±0.5 | |
| f | flap closed and open angles wanted | chord vs wing datum | protractor ±2° | |
| g | rod length between rod-end centres; rod-end type/thread | rod-end ball centres | calipers ±0.2 | |
| h | nearest approach of the swept arm to: the 68 mm shock at full compression, the LED tail, the body inner | swept envelope | feeler/rule ±1 | |
| i | servo neutral orientation that puts the rod straight at flap-closed | horn at neutral | mark + photograph | |

**Row (d) is the point of this table.** The `58 mm` in the inventory is a raw bounding
box, not a pivot span; `drs_arm_pivot_span` is deliberately left `undef` in
`w17_params.scad` and an `assert()` fires if anyone gives it a value. Row (d) is the only
thing that may set it.

**Stop** if a servo must distort its pocket, an ear needs drilling, the horn hits the
wing, the linkage preloads the flap, or a wire becomes the hard stop.

---

## M-15 — The side-vent parts (charge flap CF-1)

Internal geometry, how they mount to the shell, and the visible face dimensions of
`2023NEWSideVent1.stl` / `2023NEWSideVent2.stl`.
**Tool:** calipers, ±0.2 mm. **Parameters:** `vent_*`.

> ⚠ The `13.1 × 10.3` currently in `w17_params.scad` is the **floor** slot, not the
> shell vent. Nobody has measured the vent. That substitution is exactly the kind of
> error this sitting exists to remove.

---

## M-16 — The USB-C charge module · **resolves a live contradiction**

Two project documents give two different footprints for this part:

- `~29 × 26 × ~6 mm` — [`w17-electrical-inputs-for-codex.md:38`](../w17-electrical-inputs-for-codex.md)
- `18.3 × 31 mm` in a `≤10 mm` cell — [`ZK_electronics_cassette_fit_study.md:73`](10_assembly_architecture/fit_studies/ZK_electronics_cassette_fit_study.md)

**Neither is a caliper record**, and **no pocket may be cut to either**. Measure the
purchased SKU: body L × W × H, hole positions, the onboard Type-C connector's edge and
protrusion, which face gets hot, and where the leads exit.
**Tool:** calipers, ±0.2 mm. **Parameters:** `chg_*`. Also settle whether the state LED
is on the board (light-pipe needed) or can be flown on two wires.

---

## M-17 — The GCS box modules

Every one of these is currently a guess, and the hub is not procured.

| Module | L × W × H | Notes |
|---|---|---|
| ELRS TX module **as received** (is it the Pro?) | | |
| FT232RL USB-UART board | | |
| Wi-Fi adapter (the approved dual-band one) | | |
| USB hub (after procurement) | | |

**Tool:** calipers, ±0.5 mm. **Parameters:** `gcs_*`. Note each module's **connector
faces** too — the bulkhead panel is laid out from those, not from the bodies.

---

## M-18 / M-19 — Speaker and Hall

| # | Measurement | Datum | Tool | Value | Parameter |
|---|---|---|---|---|---|
| M-18a | speaker basket Ø, cone Ø, mounting-hole pattern, depth | basket rim | calipers ±0.2 | | `spk_*` |
| M-18b | the sidepod port aperture you actually want | vent face | calipers ±0.2 | | `spk_port_d` |
| M-19a | Hall carrier surface: what the sensor can be mounted to at the rear axle | axle face | calipers ±0.5 | | |
| M-19b | collar runout — how much the magnet face moves per revolution | axle face | non-magnetic gauge ±0.5 | | |
| M-19c | the sensor-to-magnet gap actually achievable, target 1.5 mm inside a 1–3 mm band | magnet face | non-magnetic gauge ±0.5 | | `hall_gap` |

**Use a non-magnetic feeler for M-19.** A steel gauge next to a Hall sensor and a magnet
tells you about the gauge.

**While you are at the rear axle:** confirm the Hall lead can be routed **away from the
ESC and motor phase leads** — no parallel run, crossing at 90° if it must cross — and
that it can be kept short with its pull-up near the board. This is not cosmetic: the
control firmware's GPIO35 interrupt has no rate bound, GPIO34–39 have no internal
pull-ups, and a noisy Hall line cannot be rescued in software.

---

## M-20 — Free-feature occupancy

**What:** with the mechanical build as far along as it is, walk the registered M3
features and record which are **genuinely free** — try an M3 screw, do not judge by eye.

| Feature | Coordinate | Free? | What occupies it |
|---|---|---|---|
| splice screw | X +7.50, L 0 | ☐ | |
| splice screw | X +14.26, L 0 | ☐ | |
| splice screw | X +22.69, L 0 | ☐ | |
| rear bracket | X −27.76, L −13.50 | ☐ | |
| rear bracket | X −27.76, L +16.50 | ☐ | |
| free single (belt side) | X −39.99, L −32.86 | ☐ | |
| free single (mirror side) | X −39.94, L +17.14 | ☐ | |
| centreline pedestal candidate | X +57.50, L 0 | ☐ | |
| centreline pedestal candidate | X +64.24, L 0 | ☐ | |

The three collinear splice screws are the **only** existing-hole anchor candidates inside
the cassette footprint (**OP-G**), and the two centreline features at X+57.50 / +64.24 are
the pedestal's only candidate anchors. If they are occupied, both ideas die here, which is
a good outcome — it is cheaper than finding out with a printed part in hand.

---

## What to do with the results

1. Fill the tables in **this file** and commit it in `w17-3d-codex` — it is the record.
2. For each row, update `11_cad/w17_params.scad`: the value, **and** the tag
   (`ASSUMED` → `MEASURED(<file>:<line>)`), **and** delete its entry from that file's §9.
3. Update §12 of `AA_electronics_placement_study.md` to match.
4. Run `11_cad/render.sh`. If an `assert()` now fires, **that is the sitting's most
   valuable output** — the geometry has moved outside what the study's arithmetic allows,
   and the design needs revisiting before anything is printed.
5. If **M-00** found printed parts, add them to `05_printed_parts_log/PRINT_LOG.md` with
   what is actually known (source, date, shop, material if known) and mark the unknowns
   as unknown.

---

**Safety, restated because it is easy to drift:** no power, no battery, no USB, nothing
flashed or connected — calipers, a rule, a scale and your eyes. No part is forced, cut,
drilled or glued in this sitting. **A2 stays NOT-EXECUTED and Phase B stays BLOCKED**
whatever the numbers say. Show diffs before committing.
