// =====================================================================
// fit_check_coupons.scad — the four things to print FIRST
// =====================================================================
//
//  Study: ../10_assembly_architecture/AA_electronics_placement_study.md §11
//
//  These are the only files in 11_cad/ that are meant to meet a printer
//  soon. They are TP-class test prints: draft settings, physically labelled
//  "TP", logged in ../04_test_prints/, and NEVER installed on the car
//  (MODEL_INVENTORY.md:27-35, risk E-22).
//
//  coupon = "c1" peg / hole tolerance ladder   <- print this one FIRST
//           "c2" standoff height gauge
//           "c3" MH-ET hole pattern + edge slot
//           "c4" S0 / deck-height stepped gauge
//
//  Order matters. C-1 calibrates every clearance the other three (and the
//  cage, and the trays) depend on. Do not print a cage before C-1 and C-3
//  have passed.
//
//  Each coupon carries its own raised label so a drawer full of little
//  printed rectangles is still readable in six months.
// =====================================================================

include <w17_params.scad>
include <lib/w17_lib.scad>

coupon = "c1";

label_h    = 0.6;    // ESTIMATED(2-3 layers of raised text; readable, not fragile)
label_size = 3.5;    // ESTIMATED(text height that survives a 0.4 nozzle)
plate_t    = 4.0;    // ESTIMATED(stiff enough not to bow while you test a fit)


module label(txt, size = label_size) {
    linear_extrude(height = label_h)
        text(txt, size = size, halign = "left", valign = "baseline",
             font = "Helvetica");
}


// =====================================================================
//  C-1 — peg / hole tolerance ladder
// =====================================================================
//  ANSWERS: what clearance does THIS printer and THIS filament actually
//  need for a 3 mm peg in a 3 mm hole, and for an M3 screw shank?
//
//  HOW TO USE: try each numbered pair by hand, no tools, no force. Record
//  the FIRST step that assembles by hand and stays put when shaken. That
//  number becomes fit_clearance in w17_params.scad, per material.
//
//  It matters here more than usual: the board clips locate on printed pegs
//  (second_floor_cage.scad), and a peg that needs a hammer is a peg that
//  splits a base plate in a crash.
c1_steps = [-0.15, -0.05, 0.05, 0.10, 0.15, 0.20, 0.30];   // 7 steps, per side
c1_pitch = 14;

module coupon_c1() {
    n = len(c1_steps);
    w = n * c1_pitch + 8;
    difference() {
        union() {
            translate([0, -14, 0]) cube([w, 28, plate_t]);
            translate([4, 8, plate_t])
                label("C-1 peg/hole ladder  (record the first hand-fit step)", 3.0);
            // the pegs, on the upper row
            for (i = [0 : n-1])
                translate([6 + i*c1_pitch, 4, plate_t])
                    cylinder(h = 8, d = clip_peg_d - 2*c1_steps[i]);
            // step numbers
            for (i = [0 : n-1])
                translate([3 + i*c1_pitch, -6, plate_t])
                    label(str(i+1), 4.0);
        }
        // the matching holes, on the lower row
        for (i = [0 : n-1])
            translate([6 + i*c1_pitch, -10, -EPS])
                cylinder(h = plate_t + 2*EPS, d = clip_peg_d + 2*c1_steps[i]);
    }
}


// =====================================================================
//  C-2 — standoff height gauge
// =====================================================================
//  ANSWERS: does a printed standoff actually reach its nominal height once
//  the first layer has squished and the part has shrunk?
//
//  HOW TO USE: caliper each pillar top against the plate top. Pass is
//  +-0.15 mm over all five. If they are consistently short, that offset
//  goes into every standoff height in w17_params.scad, not into a fudge in
//  one model.
c2_heights = [4, 6, 8, 10, 12];

module coupon_c2() {
    n = len(c2_heights);
    w = n * 12 + 8;
    union() {
        translate([0, -10, 0]) cube([w, 20, plate_t]);
        translate([4, 5, plate_t]) label("C-2 standoff heights", 3.0);
        for (i = [0 : n-1]) {
            translate([8 + i*12, -3, plate_t])
                w17_standoff(c2_heights[i], 8, screw_m3_clear_d);
            translate([5 + i*12, -9, plate_t])
                label(str(c2_heights[i]), 3.0);
        }
    }
}


// =====================================================================
//  C-3 — MH-ET hole pattern + edge slot
// =====================================================================
//  ANSWERS: three questions at once, with a real ESP32 in your hand.
//    a) does the board drop into the printed edge slot by hand, no bow?
//    b) does the assumed hole pattern actually line up?
//    c) do BOTH clip stations land on bare PCB, or on a component?
//
//  (c) is the one that decides the cage. The board band is exactly one
//  board thick (AA §5.2), so the clips necessarily stand in the outboard
//  component zone; this coupon is where we find out whether the two
//  stations we chose are on copper or on a capacitor.
//
//  Every dimension in this coupon is ASSUMED (M-03). That is the point:
//  the coupon is how they stop being assumed.
module coupon_c3() {
    l = esp_len + 20;
    w = esp_wid + 16;
    difference() {
        union() {
            cube([l, w, plate_t]);
            translate([4, w - 6, plate_t]) label("C-3 MH-ET slot + holes", 3.0);
            // one edge-slot wall, exactly as the cage builds it:
            // register wall face, 1.8 mm slot, low outboard rail
            translate([10, 6, plate_t]) {
                cube([esp_len, wall_std, wall_top_z - base_t]);          // register wall
                translate([0, wall_std + slot_w, 0])
                    cube([esp_len, rail_t, rail_h]);                     // low rail
            }
            // the two clip stations, drawn as blocks so you can see
            // exactly where they would touch the board
            for (px = clip_station_x)
                translate([10 + px - clip_len/2, 6 + wall_std + slot_w, plate_t])
                    cube([clip_len, clip_t, 12]);
            // four standoffs on the assumed hole pattern, to test (b)
            translate([10 + esp_len/2, w - 14, plate_t])
                w17_standoff_pattern(esp_hole_dx, esp_hole_dy, 4,
                                     esp_hole_d + 3, 0);
        }
        // the hole pattern itself, as blind locators
        translate([10 + esp_len/2, w - 14, plate_t + 4 - 2.5])
            w17_board_holes(esp_hole_dx, esp_hole_dy,
                            esp_hole_d - 2*fit_clearance, 2.5);
        // slot lead-in
        translate([10, 6 + wall_std + slot_w/2, plate_t + rail_h])
            w17_slot_lead_in(esp_len, slot_w, slot_lead_in);
    }
}


// =====================================================================
//  C-4 — S0 / deck-height stepped gauge
// =====================================================================
//  ANSWERS: what IS S0? — the height of the seated shell's bottom edge
//  above the floor top. It is measurement M-01 and it is the single number
//  that decides whether the second-floor cage exists at all.
//
//  HOW TO USE: with the shell seated and lightly pressed, slide the gauge
//  in from the side at four or more points around the car. Read the tallest
//  step that still slides under the shell edge. Record all four readings,
//  not just the smallest -- the SPREAD tells you whether the shell sits
//  flat, and a shell that does not sit flat is a different problem.
//
//  Steps span the whole known bound, 0..11 mm (D_measurement_plan.md:43-49).
c4_steps  = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
c4_step_l = 12;

module coupon_c4() {
    n = len(c4_steps);
    handle = 24;
    union() {
        // handle, so a hand is never near the shell edge while reading
        translate([-handle, -9, 0]) cube([handle, 18, 3]);
        translate([-handle + 2, 4, 3]) label("C-4  S0 gauge  (M-01)", 3.0);
        for (i = [0 : n-1]) {
            translate([i*c4_step_l, -9, 0])
                cube([c4_step_l, 18, c4_steps[i]]);
            // the reading, engraved on the top of each step
            translate([i*c4_step_l + 1.5, -7, c4_steps[i]])
                label(str(c4_steps[i]), 4.5);
        }
    }
}


// =====================================================================
if      (coupon == "c1") coupon_c1();
else if (coupon == "c2") coupon_c2();
else if (coupon == "c3") coupon_c3();
else if (coupon == "c4") coupon_c4();
else assert(false, "coupon must be c1 | c2 | c3 | c4");

echo(str("[coupons] ", coupon,
         " | TP-class draft print, label it TP, log it in ../04_test_prints/,",
         " and never install it on the car (E-22)"));
