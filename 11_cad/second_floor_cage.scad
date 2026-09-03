// =====================================================================
// second_floor_cage.scad — the owner's "second floor" for the two ESP32s
// =====================================================================
//
//  Study:  ../10_assembly_architecture/AA_electronics_placement_study.md  §5
//  Owner's ask (A3, 2026-09-02): "maybe develop additional inner cage or
//  structure to put some devices (like ESPs) on the 'second floor' inside."
//
//  WHAT THIS IS: a proposal you can look at and measure against. It is a
//  DRAFT. Every dimension comes from w17_params.scad and roughly half of
//  them are tagged ASSUMED, which means they have never been measured.
//
//  WHAT THIS IS NOT: a printable production part. A2 is NOT-EXECUTED and
//  Phase B is BLOCKED. Print the fit_check_coupons.scad coupons first
//  (C-1, then C-2 and C-3), measure the car (M-01, M-02, M-03, M-07), put
//  the real numbers in w17_params.scad, and only then talk about printing
//  this.
//
//  ---------------------------------------------------------------------
//  Why the shape looks the way it does — the short version
//  ---------------------------------------------------------------------
//  Two constraints, and between them they leave almost nothing legal:
//
//   1. KO-01, the steering rod's sweep, forbids anything taller than
//      Z14 anywhere inside |L| 30. (Provisional band Z22..38 at |L| 22,
//      plus the 8 mm static-to-moving policy, on both axes.)
//   2. The PDB fills X+1..+46, L +-27.5, Z1..14. Nothing may cross that
//      in the middle, because Z14 IS the PDB's own audit top.
//
//  Intersect them: above Z14 the only legal band is |L| 30..43, and that
//  band is EXACTLY one board thick. So there is no legal cross-member
//  above the base plate anywhere over the PDB, and no legal wall beside
//  a board above Z14. The cage that survives is:
//
//      base plate  Z0..1, full width  ... the only centreline crossing
//      register walls  |L| 27.5..30, Z1..14  ... PDB register + board back
//      low outboard rails  Z1..4  ... they form the board's bottom slot
//      aft end guides  X+1..+3, |L| 30..43  ... the only full-height part
//      two clips per board     ... flush at the board top, zero added height
//
//  The boards stand on edge. That is not a stylistic choice: laid flat a
//  board needs 31 mm of lateral band and the car has 13 (AA §5.1, SF-B).
// =====================================================================

include <w17_params.scad>
include <lib/w17_lib.scad>


// ---------------------------------------------------------------------
// render_mode — what you get when this file is rendered
//   "part"     printable geometry only (what render.sh exports to STL)
//   "context"  the part plus transparent ghosts of the PDB cell, both
//              boards, the KO-01 band and the cassette tongue, so you can
//              SEE why nothing may go in the middle. Ghosts are excluded
//              from any exported STL by construction (w17_ghost).
//   "section"  context, cut in half at X+22 so you can look inside
// ---------------------------------------------------------------------
render_mode = "part";

// Sub-part selector, so render.sh can export the clip separately:
//   "all" | "cage" | "clip"
part = "all";


// =====================================================================
//  The cage
// =====================================================================

module cage_base_plate() {
    // The tapered outline: full L+-43 across the wing, narrowing to the
    // registered tongue at L+-29.5 by X+46. It is the ONLY member that
    // crosses the centreline, and it lies below the PDB's Z1 seat.
    linear_extrude(height = base_t)
        polygon([[wing_x0, -wing_l_half],
                 [wing_x1, -wing_l_half],
                 [tongue_x1, -tongue_l_half],
                 [tongue_x1,  tongue_l_half],
                 [wing_x1,   wing_l_half],
                 [wing_x0,   wing_l_half]]);
}

module cage_register_wall() {
    // Stops dead at wall_top_z. An assert in w17_params.scad enforces it.
    // Inner face registers the PDB's L+-27.5 edge; outer face is where the
    // board's PCB plane begins.
    difference() {
        w17_box_between([wing_x0, wall_l_in,  base_t],
                        [wing_x1, wall_l_out, wall_top_z]);

        // two cable pass-throughs so every PDB rail tap reaches the board
        // above it as a short vertical run (AA §4.2)
        for (px = [wing_x0 + 9, wing_x1 - 9])
            translate([px, wall_l_in - EPS, base_t + pass_slot_h/2 + 1])
                w17_cable_pass(pass_slot_w, pass_slot_h, wall_std + 2*EPS);
    }
}

module cage_outboard_rail() {
    // A low rail. Together with the register wall's outer face it forms
    // the 1.8 mm slot the board's bottom long edge drops into. It is LOW
    // (Z1..4) on purpose: it only has to catch a 1.6 mm PCB edge, and the
    // only tall thing allowed in this band is the board itself.
    w17_box_between([board_seat_x0, board_l_in + slot_w, base_t],
                    [wing_x1,       rail_out,            base_t + rail_h]);
}

module cage_aft_guide() {
    // The only place in the cassette where full-height structure is legal:
    // outboard of |L| 30 (clear of KO-01) and aft of the PDB in X.
    //
    // Three pieces:
    //   block  X+1..+3, |L| 27.5..33.6, Z1..14 -- ties wall to rail and
    //          gives the board's aft edge something to butt against
    //   post   X+3..+5, |L| 31.8..35.8, Z1..30 -- the full-height member,
    //          reaching over the board's aft 2 mm on the OUTBOARD side
    // The post stops at guide_top_z, which is BELOW board_top_z: it is the
    // §5.3 escape route, and nothing in this cage may rise above the board.
    union() {
        w17_box_between([guide_x0, wall_l_in, base_t],
                        [guide_x1, rail_out,  wall_top_z]);

        w17_box_between([guide_x1, board_l_in + slot_w, base_t],
                        [guide_x1 + guide_post_l,
                         board_l_in + slot_w + guide_post_t, guide_top_z]);
    }
}

module cage_bottom_slot_lead_in() {
    // A chamfer along the top of the outboard rail so the board finds the
    // slot without being looked at. Cutting tool.
    translate([board_seat_x0 - EPS, board_l_in + slot_w, base_t + rail_h])
        rotate([0, 0, 0])
            linear_extrude(height = slot_lead_in)
                polygon([[0, 0], [wing_x1 - board_seat_x0 + 2*EPS, 0],
                         [wing_x1 - board_seat_x0 + 2*EPS, -slot_lead_in],
                         [0, -slot_lead_in]]);
}

module cage_base_features() {
    // Cutting tools applied to the base plate.
    union() {
        // cable-tie slot pairs down the centre of each side bay, so a loom
        // is clamped every <=60 mm near motion (AA §4.9)
        w17_both_sides()
            for (px = [wing_x0 + 10, wing_x0 + 24, wing_x0 + 36])
                translate([px, (wall_l_in + wall_l_out)/2 + 6, 0])
                    w17_zip_slot_pair(zip_slot_w, zip_slot_l, zip_slot_bridge, base_t);

        // peg holes for the two board clips (see clip(), below)
        w17_both_sides()
            for (px = clip_station_x)
                translate([px, rail_out + clip_foot_w/2, -EPS])
                    cylinder(h = base_t + 2*EPS, d = clip_peg_d + 2*fit_clearance);

        // LED / Hall tail exit at the rear outboard corner, PS-09 route.
        // Rounded, because this is exactly where a loom flexes.
        w17_both_sides()
            translate([wing_x0 + 4, wing_l_half - 6, -EPS])
                cylinder(h = base_t + 2*EPS, d = 8);
    }
}

module cage() {
    difference() {
        union() {
            cage_base_plate();
            w17_both_sides() cage_register_wall();
            w17_both_sides() cage_outboard_rail();
            w17_both_sides() cage_aft_guide();
        }
        cage_base_features();
        w17_both_sides() cage_bottom_slot_lead_in();
    }
}


// =====================================================================
//  The retainer — one per board, and that is the point
// =====================================================================
//
//  A single bar across both boards would cross |L| 30 at Z32, which is
//  inside the KO-01 + policy volume. Two bars, one per side, never do.
//
//  Printed and used lying flat; shown here in its installed position.
//  Its forward end is OP-H: with the registered seat X+3..+42 the board
//  already reaches the cassette wing's forward edge, so there is nothing
//  to land a forward post on. Either this bar cantilevers (as drawn) or
//  board_seat_x0 moves ~2 mm aft. M-03 decides.

module clip(station_x) {
    // One board clip. Two per board. It drops onto a printed peg hole in
    // the base plate, stands up outboard of the low rail, and reaches over
    // the board's top edge with a short finger.
    //
    // Its top face is FLUSH with board_top_z. That is the whole design
    // rule: AA §5.3's required S0 is measured from the board top, and any
    // millimetre added above it comes straight off a budget that is already
    // 9.82 of an 11 mm bound.
    //
    // It is not a snap. The board goes in first; the clips go on after; to
    // service, pull the two clips off their pegs with a fingernail. No
    // tool, no fastener, and nothing loaded through the PCB's own holes.
    finger_y0 = board_l_in + clip_finger_gap;   // just clear of the PCB face
    translate([station_x - clip_len/2, 0, 0]) {
        // the peg that locates it (a real peg/hole fit -- coupon C-1)
        translate([clip_len/2, rail_out + clip_foot_w/2, 0])
            cylinder(h = base_t, d = clip_peg_d);
        // foot
        w17_box_between([0,        rail_out, base_t],
                        [clip_len, rail_out + clip_foot_w, base_t + clip_t]);
        // upright, outboard of the rail, up to just under the board top
        w17_box_between([0,        rail_out, base_t],
                        [clip_len, rail_out + clip_t, board_top_z - clip_finger_h]);
        // finger over the board's top edge, top face FLUSH at board_top_z
        w17_box_between([0,        finger_y0, board_top_z - clip_finger_h],
                        [clip_len, rail_out + clip_t, board_top_z]);
    }
}

module clips() {
    w17_both_sides()
        for (px = clip_station_x)
            clip(px);
}


// =====================================================================
//  Context ghosts — never exported, only ever looked at
// =====================================================================

module ctx_pdb() {
    w17_ghost() w17_cell(pdb_x0, pdb_x1, pdb_l_half, pdb_z0, pdb_z1);
}

module ctx_boards() {
    w17_ghost() w17_both_sides()
        w17_box_between([board_seat_x0, board_l_in, board_seat_z0],
                        [board_seat_x0 + esp_len, board_l_out, board_top_z]);
}

module ctx_ko01() {
    // The provisional steering band itself, and the guard volume the
    // 8 mm policy adds around it. This is the shape that eats the car.
    w17_ghost() {
        w17_cell(wing_x0 - 20, tongue_x1 + 10, ko01_l_half, ko01_z_lo, ko01_z_hi);
        w17_cell(wing_x0 - 20, tongue_x1 + 10, ko01_l_guard, ko01_z_guard, ko01_z_hi + clr_moving);
    }
}

module context() {
    ctx_pdb();
    ctx_boards();
    ctx_ko01();
}


// =====================================================================
//  Assembly + render_mode dispatch
// =====================================================================

module assembly() {
    if (part == "all" || part == "cage") cage();
    if (part == "all" || part == "clip") clips();
}

if (render_mode == "part") {
    assembly();
} else if (render_mode == "context") {
    assembly();
    context();
} else if (render_mode == "section") {
    intersection() {
        union() { assembly(); context(); }
        translate([-200, -200, -100]) cube([200 + 22, 400, 400]);   // cut at X+22
    }
} else {
    assert(false, "render_mode must be part | context | section");
}

echo(str("[cage] mode=", render_mode, " part=", part,
         " | wall Z", base_t, "..", wall_top_z,
         " | guide Z", base_t, "..", guide_top_z,
         " | clip top Z", board_top_z, " (flush)",
         " | required S0 = ", s0_required, " of a ", s0_upper_bound, " mm bound",
         " | nothing above Z", ko01_z_guard, " inside |L| ", ko01_l_guard));
