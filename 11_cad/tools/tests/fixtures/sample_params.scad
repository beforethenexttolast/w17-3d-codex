// Fixture w17_params.scad — a small stand-in for the real file, used only
// by test_ingest_measurements.py. It mimics the real file's tagging
// conventions closely enough to exercise the tool: several "ASSUMED
// (see §9)" definitions, one "ASSUMED-adjacent" line the tool must NOT
// touch, a string-valued ASSUMED param, and a section 9 table with rows
// that bundle more than one parameter.

esp_thk_headers   = 13.0;   // ASSUMED (see §9) installed thickness with headers, M-03
board_seat_x0     = 3.0;    // ASSUMED (see §9) OP-H turns on whether this can move aft
esp_usb_type      = "usb_c";      // ASSUMED (see §9) M-03(f)
guide_top_z       = 30.0;   // ASSUMED (see §9) M-07; may stop below board_top_z
board_top_z       = 32.0;   // DERIVED(board_seat_z0 + esp_wid)
guide_top_margin  = 2.0;    // DERIVED(board_top_z - guide_top_z) the escape route
pdb_len           = 55;     // ASSUMED (see §9) TARGET plan envelope, M-06
pdb_wid           = 45;     // ASSUMED (see §9) TARGET plan envelope, M-06
screw_m3_clear_d  = 3.4;    // ASSUMED-adjacent: typical M3 clearance; confirmed by coupon C-1

// ---------------------------------------------------------------------
// 9. ===================  ASSUMED — THE OWNER'S LIST  ==================
//    Every value referenced above as "ASSUMED (see §9)" is repeated here
//    with the measurement that retires it.
// ---------------------------------------------------------------------
//
//  M-03  esp_thk_headers                                13.0
//  M-03  board_seat_x0                                   3.0
//  M-03  esp_usb_type                              "usb_c"
//  M-06  pdb_len / pdb_wid                            55/45
//  M-07  guide_top_z                                    30.0
//
// -----------------------------------------------------------------------
