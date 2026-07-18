# p0_06 — D-27 deck-side mounting map (architecture RIGHT = belt side = L<0)

Frame: P0 vehicle. Sources: p0_02 feature map + this session's keep-outs.

## Keep-out overlays

- **KO-01 rod band** — X -50..+135, |L|<=18 (rear)..12 (fwd), Z 35..62
- **KO-19 servo+holder** — X -25..-52 (bracket stations), |L|<=12, Z 0..58
- **belt/spur cutout** — X -98..-117, L -34..-60 — NO plate (through)
- **joint window** — X -14..-4 centre |L|<14 OPEN; splice screws to +24
- **motor/axle bay** — X <= -94 centre — open + rotating (KO-08/09)
- **ESC bay allocation** — X -60..-90, L -10..-52 (P11) — PS-02 territory
- **vent + shell-lip zone** — X +27..+62, |L| 41..62 — vent screws + body seat

## Fastener features, deck-relevant band (L +5 .. -60, X +30 .. -100)

| X | L | feature | usable as | blockers |
|---|---|---|---|---|
|   +22.69 |   +0.00 | ff M3-sq THROUGH(edge) | FloorBoard2 splice screw | occupied; centre band |
|   +14.26 |   +0.00 | ff M3-sq THROUGH(edge) | FloorBoard2 splice screw | occupied; centre band |
|    +7.50 |   +0.00 | ff M3-sq THROUGH(edge) | FloorBoard2 splice screw | occupied (splice); centre band |
|   -27.76 |  -13.50 | bf M3-sq THROUGH | rear-floor bracket station (fwd pair) | KO-19 candidate seat — VERIFY at dry-fit |
|   -39.99 |  -32.86 | bf M3-sq THROUGH(edge) | single, mid-bay | FREE candidate: PS-03 shelf / PS-04 post |
|   -46.55 |   +0.00 | bf slot/pocket UNDERSIDE(bottom -2.0) | UNDERSIDE(bottom -2.0) | assign at P1 dry-fit |
|   -70.64 |  -50.38 | bf M3-sq THROUGH(edge) | axle-holder row 3 | occupied |
|   -70.64 |  -45.25 | bf M3-sq THROUGH(edge) | axle-holder row 2 | occupied |
|   -70.65 |  -40.25 | bf M3-sq THROUGH(edge) | axle-holder row 1 | occupied (axle holder, 3-position row) |
|   -80.18 |  -30.75 | b2 M3-sq THROUGH(edge) | unassigned M3-class feature | assign at P1 dry-fit |
|   -85.76 |  -13.50 | bf M3-sq THROUGH | rear bracket station (rear pair) | spring-mount territory (Gate A) |
|   -85.93 |   -5.00 | bf M3-sq THROUGH(edge) | splice/b2 stack bolt | occupied (3-layer joint) |
|   -85.93 |   -5.00 | b2 M3-sq THROUGH | splice/b2 stack bolt | occupied (3-layer joint) |
|   -85.93 |   +5.00 | bf M3-sq THROUGH(edge) | unassigned M3-class feature | assign at P1 dry-fit |
|   -85.93 |   +5.00 | b2 M3-sq THROUGH | unassigned M3-class feature | assign at P1 dry-fit |

## D-27 anchor answers for the T CAD tasks (P0)

- **PS-03/PS-04/PS-05 (UBEC shelf + deck posts):** the deck-side bay
  X 0..-60, L -15..-50 contains only ONE free fastener feature
  ((-40.0, -32.9)); the bay is otherwise plain 4 mm plate. Supports
  spanning to the centre-band splice screws or clamping the plate edge
  will be needed — the "12-slot" reuse assumption does NOT hold on this
  side: most M3 features are occupied by the donor build or sit in the
  centre band under KO-01/KO-19.
- **PS-15 junction block (Z2R, X +10..+40, L -15..-50):** NO existing
  fastener feature in that patch (plain plate + vent zone outboard).
- **PS-01 battery tray (mirror side, L>0):** same picture mirrored —
  one free single at (-39.9, +17.1); bay otherwise plain.
- Consequence recorded for K/T: the floor M3 slot-nut pattern is NOT a
  12-position free grid; new supports must either share donor screws,
  use the few free singles, or add plate-clamp feet (no new holes in
  donor parts — rule unchanged).

Status: feature positions DIGITALLY CONFIRMED (mesh-measured, +-0.2);
occupancy hypotheses PARTIALLY RESOLVED (drawing [2] consumers not all
mesh-verified); side naming per header; final free-slot availability =
PHYSICAL CONFIRMATION at the P1 dry-fit (D-27 stays two-stage).
