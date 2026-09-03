// =====================================================================
// lib/w17_lib.scad — shared helpers for every W17 model in 11_cad/
// =====================================================================
//
//  Rule: this file contains NO dimensions. Everything it needs arrives as
//  a parameter from w17_params.scad. If you find yourself typing a number
//  here, it belongs in w17_params.scad with a provenance tag.
//
//  Beginner note on how OpenSCAD works, because this repo teaches:
//  a `module` is a named shape you can stamp out repeatedly. Shapes are
//  combined with union() (glue together, the default), difference()
//  (cut the second shape out of the first) and intersection() (keep only
//  the overlap). `translate()` moves a shape; `rotate()` turns it. That
//  is essentially the whole language used below.
//
//  Convention used by every module here: shapes are built at the origin
//  and the CALLER positions them, EXCEPT where a module's name says
//  otherwise (e.g. w17_box_between, which takes absolute corners).
// =====================================================================

EPS = 0.01;   // a hair, used only to make difference() cuts poke through
              // a surface cleanly. Not a physical dimension.


// ---------------------------------------------------------------------
// Boxes and positioning
// ---------------------------------------------------------------------

// A box defined by its two opposite corners in world coordinates.
// Much easier to read against a study that quotes cells as X a..b, L ±c, Z d..e.
module w17_box_between(p0, p1) {
    lo = [min(p0[0], p1[0]), min(p0[1], p1[1]), min(p0[2], p1[2])];
    hi = [max(p0[0], p1[0]), max(p0[1], p1[1]), max(p0[2], p1[2])];
    translate(lo) cube([hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2]]);
}

// A cell quoted the way the study quotes them: X x0..x1, L ±l_half, Z z0..z1.
module w17_cell(x0, x1, l_half, z0, z1) {
    w17_box_between([x0, -l_half, z0], [x1, l_half, z1]);
}

// Mirror a child across the vehicle centreline AND keep the original.
// Used constantly: almost everything on this car exists twice.
module w17_both_sides() {
    children();
    mirror([0, 1, 0]) children();
}


// ---------------------------------------------------------------------
// Chamfers and lead-ins
// ---------------------------------------------------------------------

// A 45° lead-in wedge that runs along X, used to flare the mouth of a slot
// so a board finds it blind. `len` along x, `w` the slot width, `c` the chamfer.
module w17_slot_lead_in(len, w, c) {
    translate([0, -w/2 - c, 0])
        rotate([0, 90, 0])
            linear_extrude(height = len)
                polygon([[0, 0], [0, w + 2*c], [c, w + c], [c, c]]);
}

// A chamfered rectangular prism: a box with its four vertical edges cut.
// Chamfers matter on a printed part because a sharp outside corner is where
// a knock starts a crack, and because the first layer curls there.
module w17_chamfered_box(sz, c) {
    hull() w17_both_sides()
        for (sx = [c, sz[0]-c])
            translate([sx, sz[1]/2 - c, 0])
                cylinder(h = sz[2], r = c);
}


// ---------------------------------------------------------------------
// Standoffs and inserts
// ---------------------------------------------------------------------

// A printed standoff: a pillar with an optional through-hole or a pocket
// for a heat-set brass insert.
//   h        pillar height
//   od       outside diameter
//   bore     0 = solid, >0 = through-hole of that diameter
//   insert_d / insert_h  > 0 = sink an insert pocket in the TOP instead
module w17_standoff(h, od, bore = 0, insert_d = 0, insert_h = 0) {
    difference() {
        cylinder(h = h, d = od);
        if (bore > 0)
            translate([0, 0, -EPS]) cylinder(h = h + 2*EPS, d = bore);
        if (insert_d > 0 && insert_h > 0)
            translate([0, 0, h - insert_h])
                cylinder(h = insert_h + EPS, d = insert_d);
    }
}

// A boss for a heat-set insert, sized from the insert and a hoop wall.
// The soldering iron melts the brass in; the hoop is what stops it splitting.
module w17_insert_boss(insert_d, insert_h, wall, extra_h = 1.5) {
    w17_standoff(h = insert_h + extra_h,
                 od = insert_d + 2*wall,
                 insert_d = insert_d,
                 insert_h = insert_h);
}

// Four standoffs on a rectangular hole pattern, centred on the origin.
module w17_standoff_pattern(dx, dy, h, od, bore = 0, insert_d = 0, insert_h = 0) {
    for (sx = [-dx/2, dx/2], sy = [-dy/2, dy/2])
        translate([sx, sy, 0])
            w17_standoff(h, od, bore, insert_d, insert_h);
}


// ---------------------------------------------------------------------
// Board features
// ---------------------------------------------------------------------

// A rectangular pocket for a PCB lying flat, with a finger relief on both
// short ends so the board can be lifted out without a tool.
//   l, w, t  board length, width, thickness to be recessed
//   clear    per-side clearance (from the C-1 coupon, never guessed twice)
module w17_board_pocket(l, w, t, clear) {
    translate([-(l + 2*clear)/2, -(w + 2*clear)/2, -EPS])
        cube([l + 2*clear, w + 2*clear, t + EPS]);
    // finger reliefs: half-round scallops at both short ends
    for (sx = [-1, 1])
        translate([sx * (l + 2*clear)/2, 0, -EPS])
            cylinder(h = t + EPS, d = w * 0.45);
}

// The four mounting holes of a board, as a cutting tool. Centred on origin.
// NOTE: the study forbids LOADING a PCB's own holes in the car (AA §5.6).
// This exists for bench trays and coupons, where locating is the whole job.
module w17_board_holes(dx, dy, d, depth) {
    for (sx = [-dx/2, dx/2], sy = [-dy/2, dy/2])
        translate([sx, sy, -EPS])
            cylinder(h = depth + 2*EPS, d = d);
}

// A vertical edge slot that grips a PCB standing on edge: a channel of
// width `w`, `depth` deep, `len` long, with a chamfered mouth.
// Built lying along X, mouth facing +Z, centred on y = 0.
module w17_edge_slot(len, w, depth, lead_in) {
    translate([0, -w/2, -EPS]) cube([len, w, depth + EPS]);
    translate([0, 0, depth]) w17_slot_lead_in(len, w, lead_in);
}

// A USB-C access notch, as a cutting tool, opening along +X.
module w17_usb_notch(w, h, depth, clear) {
    translate([-EPS, -(w + 2*clear)/2, 0])
        cube([depth + 2*EPS, w + 2*clear, h + 2*clear]);
}


// ---------------------------------------------------------------------
// Cable management
// ---------------------------------------------------------------------

// A pair of cable-tie slots. A tie passes down one, across the back of the
// plate and up the other, so a loom is clamped without any glue or hardware.
// Built as a CUTTING TOOL through a plate of thickness `t`, lying in XY,
// centred on the origin, the pair separated along Y.
module w17_zip_slot_pair(slot_w, slot_l, bridge, t) {
    for (sy = [-(bridge + slot_l)/2, (bridge + slot_l)/2])
        translate([-slot_w/2, sy - slot_l/2, -EPS])
            cube([slot_w, slot_l, t + 2*EPS]);
}

// A rounded rectangular cable pass-through, as a cutting tool through a
// wall of thickness `t`. Rounded because a sharp printed corner is a
// wire-insulation slicer, and this is exactly where a loom flexes.
module w17_cable_pass(w, h, t) {
    r = min(w, h) / 2;
    translate([0, 0, -EPS])
        rotate([-90, 0, 0])
            translate([0, 0, -EPS])
                linear_extrude(height = t + 4*EPS)
                    hull() for (sx = [-(w/2 - r), (w/2 - r)])
                        translate([sx, 0]) circle(r = r);
}


// ---------------------------------------------------------------------
// Context / keep-out helpers (these are NOT parts — never printed)
// ---------------------------------------------------------------------

// Draw a ghost: OpenSCAD's % modifier renders a shape transparently and
// EXCLUDES it from the exported geometry. Every context body in these
// models uses it, so an exported STL can never accidentally contain a
// keep-out volume or a mock-up of somebody's circuit board.
module w17_ghost() {
    %children();
}
