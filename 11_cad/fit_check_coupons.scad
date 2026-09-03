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

label_h    = 0.6;    // ESTIMATED(2-3 layers of text relief; readable, not fragile)
label_size = 3.5;    // ESTIMATED(text height that survives a 0.4 nozzle)
plate_t    = 4.0;    // ESTIMATED(stiff enough not to bow while you test a fit)

// POLICY: a face that SHIPS WITH OpenSCAD, so a coupon rendered on another
// machine is the same coupon. Liberation Sans is in the application bundle
// itself (Contents/Resources/fonts/Liberation-2.00.1, registered by
// fonts/10-liberation.conf), which "Helvetica" — the previous value — is not:
// it was being resolved from the host's system fonts. OpenSCAD does NOT warn
// when a font is missing, it silently substitutes, so that failure mode is
// invisible in render.sh's log and would have shown up as differently shaped
// labels on somebody else's machine. Override with -D if you must.
label_font = "Liberation Sans";

// `label(...)` builds text as a solid standing label_h proud of z = 0. Use it
// inside a union() for a raised label, or inside the second half of a
// difference() -- placed at (surface_z - label_h) -- to engrave one. C-4 must
// engrave; see B-2 in its section below.
module label(txt, size = label_size) {
    linear_extrude(height = label_h)
        text(txt, size = size, halign = "left", valign = "baseline",
             font = label_font);
}


// =====================================================================
//  C-1 — peg / hole tolerance ladder
// =====================================================================
//  ANSWERS: how much bigger than a 3 mm printed peg does a 3 mm printed hole
//  have to be, on THIS printer and THIS filament, before the two go together
//  by hand?
//
//  HOW THE LADDER IS BUILT, and this is the whole point of it: EVERY PEG IS
//  THE SAME, at the nominal clip_peg_d. Only the hole changes, as
//  clip_peg_d + 2 * step. So the radial gap at step i is exactly step i, and
//  the number you write down IS fit_clearance. No halving, no doubling, no
//  arithmetic at the bench.
//
//  That mirrors the part it calibrates, which is the only way a coupon is
//  worth printing: second_floor_cage.scad builds the clip's peg at nominal
//  clip_peg_d and the base plate's hole at clip_peg_d + 2*fit_clearance.
//  An earlier version of this coupon shrank the peg AND grew the hole by the
//  same step, so its radial gap was 2*step while the cage's is 1*fit_clearance
//  — reading it would have set fit_clearance to twice the value the printer
//  actually needs, and every peg, slot and pocket in 11_cad/ takes its
//  clearance from that one number.
//
//  HOW TO USE: try each numbered pair by hand — no tools, no force. Record the
//  FIRST step that assembles by hand and stays put when shaken, and put that
//  step's own value into fit_clearance in w17_params.scad, per material.
//  Steps 1 and 2 are NEGATIVE: their holes are smaller than the peg. If either
//  goes together by hand, this printer is running under size, which is a result
//  in its own right — report it, do not force it.
//
//  It matters here more than usual: the board clips locate on printed pegs
//  (second_floor_cage.scad), and a peg that needs a hammer is a peg that
//  splits a base plate in a crash.
c1_steps = [-0.15, -0.05, 0.05, 0.10, 0.15, 0.20, 0.30];   // 7 steps, radial gap
c1_pitch = 14;
c1_peg_h = 8.0;      // ESTIMATED(long enough to grip between finger and thumb.
                     //   Note it is NOT the car's engagement: the clip's peg is
                     //   base_t = 1 mm deep into the base plate. This coupon
                     //   measures the FIT, not the engagement length)

module coupon_c1() {
    n = len(c1_steps);
    w = n * c1_pitch + 8;
    difference() {
        union() {
            translate([0, -14, 0]) cube([w, 28, plate_t]);
            translate([4, 8, plate_t])
                label("C-1: pegs all 3.00, holes grow. Step = the gap.", 3.0);
            // the pegs, on the upper row -- ALL THE SAME, all nominal
            for (i = [0 : n-1])
                translate([6 + i*c1_pitch, 4, plate_t])
                    cylinder(h = c1_peg_h, d = clip_peg_d);
            // step numbers
            for (i = [0 : n-1])
                translate([3 + i*c1_pitch, -6, plate_t])
                    label(str(i+1), 4.0);
        }
        // the matching holes, on the lower row: the ONLY thing that varies
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
                cube([esp_len, wall_t, wall_top_z - base_t]);            // register wall
                translate([0, wall_t + slot_w, 0])
                    cube([esp_len, rail_t, rail_h]);                     // low rail
            }
            // the two clip stations, drawn as blocks so you can see
            // exactly where they would touch the board
            for (px = clip_station_x)
                translate([10 + px - clip_len/2, 6 + wall_t + slot_w, plate_t])
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
        translate([10, 6 + wall_t + slot_w/2, plate_t + rail_h])
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
//  NOTHING ON THIS GAUGE MAY STAND PROUD OF A STEP. The digits are CUT INTO
//  the step tops, not raised on them. A 0.6 mm raised digit makes every step
//  read 0.6 mm taller than it is, and the whole question here is whether S0
//  clears 9.82 mm out of an 11 mm bound -- a 1.18 mm margin, half of which a
//  raised digit would silently eat. (It also put the exported bounding box at
//  Z 0..11.6 for an 11 mm top step, which is how the error was caught.)
//
//  Steps span 2..11 mm: the printable part of the 0..11 bound
//  (D_measurement_plan.md:43-49). A 0 mm step is not a solid and a 1 mm step is
//  a single layer-stack that would flex on the way in. If the shell edge is
//  under 2 mm the gauge reads "lower than the lowest step", which is itself a
//  usable answer -- record it as such rather than reaching for a feeler.
c4_steps    = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
c4_step_l   = 12;
c4_handle_l = 30.0;  // ESTIMATED(enough to hold with two fingers, well clear of
                     //   the shell edge you are reading against, and long enough
                     //   that the engraved name fits ON IT: at 24 mm the name ran
                     //   off the end and cut into the 2 mm step's reading face)
c4_handle_t =  3.0;  // ESTIMATED(stiff enough not to flex when pushed, and BELOW
                     //   the lowest step so the handle can never be the thing
                     //   that stops the gauge going in)

module coupon_c4() {
    n = len(c4_steps);
    difference() {
        union() {
            // handle, so a hand is never near the shell edge while reading
            translate([-c4_handle_l, -9, 0])
                cube([c4_handle_l, 18, c4_handle_t]);
            for (i = [0 : n-1])
                translate([i*c4_step_l, -9, 0])
                    cube([c4_step_l, 18, c4_steps[i]]);
        }
        // the reading, ENGRAVED into the top of each step (see the note above)
        for (i = [0 : n-1])
            translate([i*c4_step_l + 1.5, -7, c4_steps[i] - label_h])
                label(str(c4_steps[i]), 4.5);
        // and the coupon's own name, engraved into the handle for the same
        // reason -- on two lines, so it stays on the handle
        translate([-c4_handle_l + 2, 2, c4_handle_t - label_h])
            label("C-4 S0 gauge", 3.0);
        translate([-c4_handle_l + 2, -6, c4_handle_t - label_h])
            label("M-01", 3.0);
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
