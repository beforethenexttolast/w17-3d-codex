// =====================================================================
// gcs_box.scad — the ground-station box, as a STRATEGY rather than a box
// =====================================================================
//
//  Study: ../10_assembly_architecture/AA_electronics_placement_study.md §8
//  Contents/wiring/power: ../../w17-gcs-box-guide.md (settled elsewhere)
//
//  READ THIS BEFORE LOOKING AT THE MODEL
//  ---------------------------------------------------------------------
//  EVERY DIMENSION OF EVERY MODULE IN THIS BOX IS A GUESS. Exactly one
//  envelope is even vendor-documented (ES24TX Pro, 70 x 49 x 32.5, and only
//  if the unit on hand is the Pro). The FT232RL, the Wi-Fi adapter and the
//  USB hub have no measurement anywhere in this workspace, and the hub is
//  not procured. Measurement M-17 is what makes this file real.
//
//  So the model is deliberately not "a box for these four modules". It is:
//
//    SLED ARCHITECTURE.  A plain rectangular base tray with a repeating M3
//    grid. Each module rides a small printed sled carrying only that
//    module's pocket and its strain relief. When a module is finally
//    calipered -- or swapped for a different one -- you reprint one sled,
//    not the box. It is the only design that survives four unknown
//    envelopes, and it is the reason this file can exist at all today.
//
//    BULKHEAD PANEL.  One end wall is a separate 2.4 mm panel carrying the
//    uplink strain relief, the antenna exit, the blanked DC barrel and the
//    flash-access port. Port positions change by reprinting a panel.
//
//  Fixed decisions that are NOT guesses (they are requirements, from §8):
//   - the antenna lives OUTSIDE the print, always. RF does not transmit
//     from inside a closed box pressed against a hub PCB.
//   - vent slots over the TX module: it is the box's only real dissipator,
//     and a sealed print is the wrong default even at 25-100 mW.
//   - the lid screws into heat-set inserts, not self-tapped plastic: this
//     box gets opened during bring-up far more than three times.
//   - PETG. Neither hot nor cosmetic; PLA would creep under a permanently
//     tensioned uplink cable.
//
//  part = "tray" | "sled" | "bulkhead" | "lid" | "all"
//  sled_for = "tx" | "ftdi" | "wifi" | "hub"
// =====================================================================

include <w17_params.scad>
include <lib/w17_lib.scad>

part     = "all";
sled_for = "tx";

// Internal envelope: the four modules laid out side by side, plus air.
// Derived from the ASSUMED module sizes, so it moves when they are measured.
gcs_in_l = max(gcs_tx_l, gcs_ftdi_l, gcs_wifi_l, gcs_hub_l) + 2*gcs_clear;
gcs_in_w = gcs_tx_w + gcs_ftdi_w + gcs_wifi_w + gcs_hub_w + 5*gcs_clear;
gcs_in_h = max(gcs_tx_h, gcs_ftdi_h, gcs_wifi_h, gcs_hub_h) + gcs_clear;

sled_wall = 2.0;    // ESTIMATED(a sled carries no load but its own module)
sled_lip  = 4.0;    // ESTIMATED(how far the pocket wall comes up the module)
foot_h    = 3.0;    // ESTIMATED(non-slip foot pad recess depth)


// ---------------------------------------------------------------------
//  The tray: a plain box with a grid. It knows nothing about the modules.
// ---------------------------------------------------------------------
module gcs_tray() {
    difference() {
        union() {
            // outer shell, open top and open bulkhead end
            difference() {
                cube([gcs_in_l + 2*gcs_wall, gcs_in_w + 2*gcs_wall,
                      gcs_in_h + gcs_floor]);
                translate([gcs_wall, gcs_wall, gcs_floor])
                    cube([gcs_in_l, gcs_in_w, gcs_in_h + EPS]);
                // the bulkhead end is a separate printed panel
                translate([gcs_in_l + gcs_wall - EPS, gcs_wall, gcs_floor])
                    cube([gcs_wall + 2*EPS, gcs_in_w, gcs_in_h + EPS]);
            }
            // lid bosses, one per corner, with heat-set inserts
            for (sx = [gcs_wall + 6, gcs_in_l + gcs_wall - 6],
                 sy = [gcs_wall + 6, gcs_in_w + gcs_wall - 6])
                translate([sx, sy, gcs_floor])
                    w17_standoff(gcs_in_h, insert_m3_d + 2*insert_boss_wall,
                                 0, insert_m3_d, insert_m3_h);
        }
        // the M3 sled grid in the floor
        for (gx = [gcs_wall + gcs_grid_pitch :
                   gcs_grid_pitch :
                   gcs_wall + gcs_in_l - gcs_grid_pitch],
             gy = [gcs_wall + gcs_grid_pitch :
                   gcs_grid_pitch :
                   gcs_wall + gcs_in_w - gcs_grid_pitch])
            translate([gx, gy, -EPS])
                cylinder(h = gcs_floor + 2*EPS, d = screw_m3_clear_d);

        // vent slots over the TX module's bay -- the only real dissipator
        for (vy = [gcs_wall + 8 : 6 : gcs_wall + gcs_tx_w])
            translate([gcs_wall + 10, vy, -EPS])
                cube([gcs_tx_l - 20, 2.5, gcs_floor + 2*EPS]);

        // non-slip foot recesses: it lives on a desk and gets tugged by one
        // cable, so mass stays low and grip comes from pads, not from bulk
        for (sx = [12, gcs_in_l + 2*gcs_wall - 12],
             sy = [12, gcs_in_w + 2*gcs_wall - 12])
            translate([sx, sy, -EPS])
                cylinder(h = foot_h, d = 14);
    }
}


// ---------------------------------------------------------------------
//  A sled. One module, one pocket, one strain relief. Reprint, don't redesign.
// ---------------------------------------------------------------------
function sled_size(which) =
      which == "tx"   ? [gcs_tx_l,   gcs_tx_w,   gcs_tx_h]
    : which == "ftdi" ? [gcs_ftdi_l, gcs_ftdi_w, gcs_ftdi_h]
    : which == "wifi" ? [gcs_wifi_l, gcs_wifi_w, gcs_wifi_h]
    : which == "hub"  ? [gcs_hub_l,  gcs_hub_w,  gcs_hub_h]
    : undef;

module gcs_sled(which) {
    sz = sled_size(which);
    assert(!is_undef(sz), "sled_for must be tx | ftdi | wifi | hub");
    l = sz[0] + 2*sled_wall + 2*fit_clearance;
    w = sz[1] + 2*sled_wall + 2*fit_clearance;

    difference() {
        union() {
            cube([l, w, sled_wall + sled_lip]);
            translate([2, w + 1, 0]) rotate([0, 0, 0])
                linear_extrude(height = 0.6)
                    text(which, size = 4, font = "Helvetica");
        }
        // the module's pocket
        translate([sled_wall, sled_wall, sled_wall])
            cube([sz[0] + 2*fit_clearance, sz[1] + 2*fit_clearance,
                  sled_lip + EPS]);
        // two grid screws, on the tray's M3 pitch
        for (sx = [gcs_grid_pitch/2, l - gcs_grid_pitch/2])
            translate([sx, w/2, -EPS])
                cylinder(h = sled_wall + 2*EPS, d = screw_m3_clear_d);
        // cable-tie strain relief at the module's lead exit
        translate([l/2, w - sled_wall/2, 0])
            w17_zip_slot_pair(zip_slot_w, zip_slot_l, zip_slot_bridge, sled_wall);
        // finger relief, so a module lifts out without a screwdriver blade
        translate([l/2, 0, sled_wall])
            cylinder(h = sled_lip + EPS, d = w * 0.4);
    }
}


// ---------------------------------------------------------------------
//  The bulkhead panel: every port position lives here, and only here.
// ---------------------------------------------------------------------
module gcs_bulkhead() {
    difference() {
        cube([gcs_wall, gcs_in_w, gcs_in_h]);
        // uplink cable gland (rounded -- it is the cable that gets tugged)
        translate([-EPS, gcs_in_w * 0.25, gcs_in_h * 0.5])
            rotate([0, 90, 0])
                cylinder(h = gcs_wall + 2*EPS, d = 8);
        // antenna exit: the antenna is OUTSIDE the print, always
        translate([-EPS, gcs_in_w * 0.55, gcs_in_h * 0.5])
            rotate([0, 90, 0])
                cylinder(h = gcs_wall + 2*EPS, d = 7);
        // blanked DC barrel -- cut only if the bench says a 12 V input is
        // needed. Drawn as a scored outline, not a hole.
        translate([gcs_wall - 0.6, gcs_in_w * 0.75, gcs_in_h * 0.5])
            rotate([0, 90, 0])
                cylinder(h = 0.6 + EPS, d = 11);
        // flash-access port for the TX module
        translate([-EPS, gcs_in_w * 0.9, gcs_in_h * 0.4])
            cube([gcs_wall + 2*EPS, 14, 8]);
    }
    // strain-relief ears beside the gland
    for (sy = [gcs_in_w*0.25 - 9, gcs_in_w*0.25 + 9])
        translate([0, sy, gcs_in_h*0.5 - 3])
            cube([gcs_wall + 4, 3, 6]);
}


// ---------------------------------------------------------------------
//  Lid: captive M3 into the tray's heat-set inserts.
// ---------------------------------------------------------------------
module gcs_lid() {
    difference() {
        cube([gcs_in_l + 2*gcs_wall, gcs_in_w + 2*gcs_wall, gcs_wall]);
        for (sx = [gcs_wall + 6, gcs_in_l + gcs_wall - 6],
             sy = [gcs_wall + 6, gcs_in_w + gcs_wall - 6])
            translate([sx, sy, -EPS])
                cylinder(h = gcs_wall + 2*EPS, d = screw_m3_clear_d);
        // vent slots, mirroring the floor's, over the TX bay
        for (vy = [gcs_wall + 8 : 6 : gcs_wall + gcs_tx_w])
            translate([gcs_wall + 10, vy, -EPS])
                cube([gcs_tx_l - 20, 2.5, gcs_wall + 2*EPS]);
    }
}


// ---------------------------------------------------------------------
if (part == "tray")          gcs_tray();
else if (part == "sled")     gcs_sled(sled_for);
else if (part == "bulkhead") gcs_bulkhead();
else if (part == "lid")      gcs_lid();
else if (part == "all") {
    gcs_tray();
    translate([gcs_in_l + 2*gcs_wall + 10, 0, 0]) gcs_bulkhead();
    translate([0, gcs_in_w + 2*gcs_wall + 10, 0]) gcs_sled(sled_for);
    translate([0, 0, gcs_in_h + gcs_floor + 10]) gcs_lid();
} else assert(false, "part must be tray | sled | bulkhead | lid | all");

echo(str("[gcs_box] internal ", gcs_in_l, " x ", gcs_in_w, " x ", gcs_in_h,
         " mm — EVERY module envelope in this box is ASSUMED (M-17);",
         " the hub is not even procured. Sleds exist so this stays cheap."));
