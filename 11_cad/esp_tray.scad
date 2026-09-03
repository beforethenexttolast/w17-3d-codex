// =====================================================================
// esp_tray.scad — two ways to hold an MH-ET D1-Mini ESP32
// =====================================================================
//
//  Study: ../10_assembly_architecture/AA_electronics_placement_study.md §5
//
//  variant = "shoe"  the on-edge carrier that goes in the car
//  variant = "bench" a flat desk tray that does NOT go in the car
//
//  ---------------------------------------------------------------------
//  Why two, and why the flat one is not a vehicle part
//  ---------------------------------------------------------------------
//  Laid flat, a D1-Mini needs 31 mm of lateral band. The only band the car
//  has between the steering keep-out and the shell shoulder is 13 mm wide
//  (AA §5.2), and pushing outboard to |L| 50 meets shell ceilings of 7-9 mm.
//  That is why the flat mezzanine (SF-B) was rejected and the boards stand
//  on edge. The "bench" variant below exists for flashing and bring-up on
//  a desk, where none of that applies -- and it is the only place in this
//  repo where a PCB's own mounting holes are used, because on a desk
//  locating the board IS the whole job.
//
//  ---------------------------------------------------------------------
//  The shoe, and what it buys
//  ---------------------------------------------------------------------
//  The cage grips the bare PCB directly. That works, but every service
//  cycle then abrades the board's own edge. The shoe is a sacrificial
//  U-channel that the board lives in permanently: the shoe wears, not the
//  ESP32, and a worn shoe is a 20-minute reprint.
//
//  It is a DRAFT. esp_len / esp_wid / esp_pcb_t are DOCUMENTED for the SKU
//  class, not measured on our board (M-03), and the shoe's own thickness
//  eats the board band, which is exactly 13 mm wide with nothing spare.
//  Coupon C-3 with a real board decides whether the shoe is affordable at
//  all -- if it is not, the cage grips the bare PCB and this file stays a
//  bench tray.
// =====================================================================

include <w17_params.scad>
include <lib/w17_lib.scad>

variant = "shoe";     // "shoe" | "bench"

shoe_t      = 1.6;    // ESTIMATED(4 perimeters; it is a wear part, not a structural one)
shoe_grip   = 3.0;    // ESTIMATED(how far the channel comes up the board's face)
bench_h     = 6.0;    // ESTIMATED(standoff height: clears the board's underside pins)
bench_wall  = 2.0;    // ESTIMATED
bench_lip   = 3.0;    // ESTIMATED(a rim, so the tray does not slide off a desk edge)
bench_chamfer   = 2.5;  // ESTIMATED(corner chamfer; a sharp printed corner starts cracks)
bench_boss_wall = 1.5;  // ESTIMATED(hoop around the locating pip)
bench_pip_depth = 2.5;  // ESTIMATED(blind locator depth -- a locator, never a fastener)
shoe_window_l   = 10.0; // ESTIMATED(relief window, so the shoe cannot trap a low component)
shoe_window_at  = [0.30, 0.70];  // ESTIMATED(fractions along the shoe's length)
shoe_end_stop_h = 2.0;  // ESTIMATED(how far the end stops stand above the grip)


// ---------------------------------------------------------------------
//  The on-edge shoe
// ---------------------------------------------------------------------
module esp_shoe() {
    // A U-channel in section: the board's bottom long edge sits in it.
    // Built lying along X with the channel opening upward, at the origin,
    // so it can be printed flat -- which puts the print layers ACROSS the
    // load path, the rule K_printable_support_spec.md applies everywhere.
    ch_w  = esp_pcb_t + 2*fit_clearance;
    out_w = ch_w + 2*shoe_t;
    len   = esp_len + 2*fit_clearance;

    difference() {
        union() {
            // channel body
            translate([0, -out_w/2, 0]) cube([len, out_w, shoe_t + shoe_grip]);
            // end stops, so the board cannot slide out lengthwise
            for (sx = [0, len - shoe_t])
                translate([sx, -out_w/2, 0])
                    cube([shoe_t, out_w, shoe_t + shoe_grip + shoe_end_stop_h]);
        }
        // the channel the PCB sits in
        translate([shoe_t, -ch_w/2, shoe_t])
            cube([len - 2*shoe_t, ch_w, shoe_grip + EPS + shoe_end_stop_h]);
        // chamfered mouth, so the board finds it blind
        translate([shoe_t, 0, shoe_t + shoe_grip])
            w17_slot_lead_in(len - 2*shoe_t, ch_w, slot_lead_in);
        // a relief window per side, so the shoe cannot trap a component
        // that sits low on the board's edge -- and so you can see the board
        for (f = shoe_window_at)
            translate([len*f - shoe_window_l/2, -out_w/2 - EPS, shoe_t + slot_lead_in])
                cube([shoe_window_l, out_w + 2*EPS, shoe_grip]);
    }
}


// ---------------------------------------------------------------------
//  The bench tray (desk only -- never in the car)
// ---------------------------------------------------------------------
module esp_bench_tray() {
    plate_l = esp_len + 2*bench_wall + 2*bench_lip;
    plate_w = esp_wid + 2*bench_wall + 2*bench_lip;

    difference() {
        union() {
            // base plate with chamfered corners
            w17_chamfered_box([plate_l, plate_w, bench_wall], bench_chamfer);
            // four standoffs on the board's hole pattern
            translate([plate_l/2, 0, bench_wall])
                w17_standoff_pattern(esp_hole_dx, esp_hole_dy,
                                     bench_h, esp_hole_d + 2*bench_boss_wall, 0);
            // a low rim
            difference() {
                w17_chamfered_box([plate_l, plate_w, bench_wall + bench_lip], bench_chamfer);
                translate([bench_wall, -(plate_w/2 - bench_wall), bench_wall])
                    cube([plate_l - 2*bench_wall, plate_w - 2*bench_wall,
                          bench_lip + EPS]);
            }
        }
        // locating pips: shallow blind holes in the standoff tops.
        // NOTE the study forbids LOADING a PCB's own holes in the car
        // (AA §5.6). On a desk, locating the board is the entire job, so
        // this is the one place they are used -- and only as a locator,
        // never with a screw pulled down through them.
        translate([plate_l/2, 0, bench_wall + bench_h - bench_pip_depth])
            w17_board_holes(esp_hole_dx, esp_hole_dy,
                            esp_hole_d - 2*fit_clearance, bench_pip_depth);
        // USB-C access notch through the rim, on the +X short edge
        translate([plate_l - bench_wall - EPS,
                   esp_usb_offset,
                   bench_wall + bench_h - esp_usb_h/2])
            w17_usb_notch(esp_usb_w, esp_usb_h, bench_wall + 2*EPS, fit_clearance + bench_boss_wall);
        // cable-tie pair, so a USB lead is strain-relieved on the desk
        translate([bench_lip + bench_chamfer, 0, 0])
            w17_zip_slot_pair(zip_slot_w, zip_slot_l, zip_slot_bridge, bench_wall);
    }
}


// ---------------------------------------------------------------------
if (variant == "shoe") {
    esp_shoe();
} else if (variant == "bench") {
    esp_bench_tray();
} else {
    assert(false, "variant must be shoe | bench");
}

echo(str("[esp_tray] variant=", variant,
         " | board ", esp_len, " x ", esp_wid, " x ", esp_pcb_t,
         " (DOCUMENTED for the SKU class, NOT measured -- M-03)"));
