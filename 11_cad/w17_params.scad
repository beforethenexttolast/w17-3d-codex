// =====================================================================
// w17_params.scad — the single source of every dimension in 11_cad/
// =====================================================================
//
//  Repo:    w17-3d-codex          Branch: design/placement-and-cage
//  Study:   ../10_assembly_architecture/AA_electronics_placement_study.md
//  Date:    2026-09-03
//
//  RULE OF THIS FILE (it is the whole point of it):
//  ------------------------------------------------------------------
//  Every number below carries a provenance tag. No number appears
//  anywhere else in 11_cad/ — models import this file and use names.
//
//    MEASURED(file:line)  a real instrument touched a real part
//    DERIVED(source)      arithmetic on registered geometry / MEASURED values
//    DOCUMENTED(part)     vendor figure for the part FAMILY, our unit unverified
//    ESTIMATED(reason)    a planning value, reasoning stated, not a measurement
//    POLICY(source)       a rule the package chose, not a physical fact
//    ASSUMED              a guess that MUST be measured before it is printed to
//
//  Every ASSUMED value lives in section 9 under its own banner, is listed
//  in the study's §12, and names the measurement (M-nn) that retires it.
//
//  A2 IS NOT EXECUTED AND PHASE B IS BLOCKED. Nothing in this file
//  authorises a production print, a shell cut, a hole in a donor part,
//  or any powered work. The models here render so the owner can SEE a
//  proposal and so fit-check coupons can be printed in draft.
//
//  Coordinate frame (used by every model in 11_cad/):
//    OpenSCAD x  =  vehicle X, positive FORWARD, X=0 at the floor joint
//    OpenSCAD y  =  vehicle L, lateral; belt/architecture-right side is L<0
//    OpenSCAD z  =  vehicle Z, up from DAT-F (floor top) = 0
//  (AA §2; fit_studies/README.md:12-16)
// =====================================================================


// ---------------------------------------------------------------------
// 1. Print / process constants (this printer, this filament)
// ---------------------------------------------------------------------

nozzle_d          = 0.4;    // DOCUMENTED(Bambu X1C 0.4 mm, repo CLAUDE.md)
layer_h           = 0.20;   // POLICY(PRINT_SPEC.md starting profile)
wall_min          = 1.6;    // DERIVED(4 perimeters x 0.4 nozzle) minimum load-bearing wall
wall_std          = 2.5;    // POLICY(AA §5.4 register wall thickness)
$fn               = 48;     // render quality; not a physical dimension


// ---------------------------------------------------------------------
// 2. Fastener + insert family
// ---------------------------------------------------------------------

screw_m3_clear_d  = 3.4;    // ASSUMED-adjacent: typical M3 clearance; confirmed by coupon C-1
screw_m3_head_d   = 6.0;    // DOCUMENTED(ISO 7380 button head M3, nominal)
insert_m3_d       = 4.0;    // ASSUMED (see §9) brass heat-set M3x5 outside Ø, brand-dependent
insert_m3_h       = 5.7;    // ASSUMED (see §9) brass heat-set M3x5 length
insert_boss_wall  = 2.0;    // POLICY(hoop wall around a heat-set insert, >= 2 mm)


// ---------------------------------------------------------------------
// 3. Vehicle datums and the two numbers everything hangs on
// ---------------------------------------------------------------------

// S0 — shell bottom edge above DAT-F. Bounded 0 .. ~11 mm, NEVER measured.
// The value below is the REQUIREMENT (AA §5.3), parked here as a placeholder
// so the models render. It is not a measurement. Measurement: M-01.
s0_measured       = 9.82;   // ASSUMED (see §9)

// KO-01, the steering rod sweep. PROVISIONAL until the ASM-08 lock-to-lock
// sweep is physically run. It is the most restrictive keep-out in the car.
ko01_x_lo         = -80;    // ASSUMED (see §9) C_clearance_keepout_register.md:30-48
ko01_x_hi         = 100;    // ASSUMED (see §9)
ko01_l_half       = 22;     // ASSUMED (see §9)
ko01_z_lo         = 22;     // ASSUMED (see §9)
ko01_z_hi         = 38;     // ASSUMED (see §9)

// Clearance policy (I_zone_layer_plan.md:45-48)
clr_static        = 5;      // POLICY static-to-static, also the print/flex budget
clr_moving        = 8;      // POLICY static-to-moving
clr_esc_air       = 10;     // POLICY open air above the ESC fan intake

// The two derived limits the whole cage obeys (AA §5.4):
//   nothing taller than this, anywhere inside ko01_l_guard
ko01_z_guard      = ko01_z_lo - clr_moving;   // DERIVED = 14
ko01_l_guard      = ko01_l_half + clr_moving; // DERIVED = 30


// ---------------------------------------------------------------------
// 4. Cassette envelope (ZK reference gauge — ASSUMPTION gauges over
//    MEASURED bodies; fit_studies/ZK_electronics_cassette_fit_study.md:96-97)
// ---------------------------------------------------------------------

base_t            = 1.0;    // DERIVED(AA §5.4: base plate occupies Z0..1)
wing_x0           = 1;      // DERIVED(ZK:96 forward wing X+1..+42)
wing_x1           = 42;     // DERIVED(ZK:96)
wing_l_half       = 43;     // DERIVED(ZK:96 L±43)
tongue_x1         = 46;     // DERIVED(ZK:96 tapered tongue X+42..+46)
tongue_l_half     = 29.5;   // DERIVED(ZK:96 L±29.5)

// PDB target cell. Rotated: 45 mm side fore-aft, 55 mm side lateral.
pdb_x0            = 1;      // DERIVED(ZK:97)
pdb_x1            = 46;     // DERIVED(ZK:97)
pdb_l_half        = 27.5;   // DERIVED(ZK:97)
pdb_z0            = 1;      // DERIVED(ZK:97)
pdb_z1            = 14;     // DERIVED(ZK:97 installed audit top; == ko01_z_guard, exactly)
pdb_len           = 55;     // ASSUMED (see §9) TARGET plan envelope, M-06
pdb_wid           = 45;     // ASSUMED (see §9) TARGET plan envelope, M-06
pdb_stack_h       = 13;     // ASSUMED (see §9) tallest component, M-05


// ---------------------------------------------------------------------
// 5. The two ESP32 boards (MH-ET Live D1-Mini ESP32, USB-C)
// ---------------------------------------------------------------------

esp_len           = 39.0;   // DOCUMENTED(SKU class, w17-electrical-inputs-for-codex.md:9)
esp_wid           = 31.0;   // DOCUMENTED(same)
esp_pcb_t         = 1.6;    // DOCUMENTED(standard 1.6 mm FR4)
esp_thk_headers   = 13.0;   // ASSUMED (see §9) installed thickness with headers, M-03

// Registered on-edge seats (ZK:99-100 / AA §3 rows 1-2)
board_seat_x0     = 3.0;    // ASSUMED (see §9) OP-H turns on whether this can move aft
board_seat_z0     = 1.0;    // DERIVED(ZK:99 seat Z1..32) parametric escape route, AA §5.3
board_l_in        = 30.0;   // DERIVED(ko01_l_guard) PCB plane inboard face
board_l_out       = 43.0;   // DERIVED(ZK:99 outer face) == wing_l_half
board_top_z       = 32.0;   // DERIVED(board_seat_z0 + esp_len)

// hole pattern + USB-C: no MH-ET drawing exists in any project document
esp_hole_dx       = 33.0;   // ASSUMED (see §9) M-03
esp_hole_dy       = 25.0;   // ASSUMED (see §9) M-03
esp_hole_d        = 3.2;    // ASSUMED (see §9) M-03
esp_usb_w         = 9.0;    // ASSUMED (see §9) M-03
esp_usb_h         = 3.5;    // ASSUMED (see §9) M-03
esp_usb_offset    = 0.0;    // ASSUMED (see §9) offset of the port from the edge centreline, M-03
esp_socket_stack  = 11.0;   // ASSUMED (see §9) seated female+male header stack, M-04


// ---------------------------------------------------------------------
// 6. The cage itself (AA §5.4, as corrected 2026-09-03)
// ---------------------------------------------------------------------

wall_l_in         = 27.5;   // DERIVED(== pdb_l_half; the wall registers the PDB edge)
wall_l_out        = 30.0;   // DERIVED(== board_l_in)
wall_top_z        = 14.0;   // DERIVED(== ko01_z_guard; the wall MUST stop here)

rail_h            = 3.0;    // ESTIMATED(enough to catch a 1.6 mm PCB edge without a tall thin wall)
rail_t            = 1.8;    // ESTIMATED(printable rail, >= wall_min at 4 perimeters minus squish)
slot_w            = 1.8;    // ESTIMATED(esp_pcb_t 1.6 + 0.2 hand-fit; coupon C-1 confirms)
slot_lead_in      = 0.6;    // ESTIMATED(45° chamfer so the board finds the slot blind)

guide_x0          = 1.0;    // DERIVED(aft of board_seat_x0, on the wing)
guide_x1          = 3.0;    // DERIVED(== board_seat_x0)
guide_top_z       = 30.0;   // ASSUMED (see §9) M-07; may stop below board_top_z
guide_top_margin  = 2.0;    // DERIVED(board_top_z - guide_top_z) the §5.3 escape route

retainer_t        = 3.0;    // ESTIMATED(a 3 mm bar in PETG over a 39 mm span, hand load only)
retainer_w        = 8.0;    // ESTIMATED(wide enough for an M3 thumbscrew boss)

zip_slot_w        = 4.0;    // ASSUMED (see §9) fits a 3 mm cable tie; tie stock not calipered
zip_slot_l        = 2.5;    // ASSUMED (see §9)
zip_slot_bridge   = 3.0;    // ESTIMATED(material left between a slot pair)

pass_slot_w       = 10.0;   // ESTIMATED(a 4-way silicone bundle plus dressing room)
pass_slot_h       = 6.0;    // ESTIMATED(same)

// Declared encroachment, and it must stay declared:
// the board's PCB plane starts exactly at board_l_in = ko01_l_guard = 30.
// Anything gripping the PCB from inboard sits inside the guard band. The
// cage therefore grips the board ONLY from outboard above wall_top_z, and
// the inboard backing (the register wall) stops at wall_top_z. There is no
// inboard structure above Z14 anywhere in these models. See AA §5.4.


// ---------------------------------------------------------------------
// 7. Other modules the models draw as CONTEXT ONLY (never as parts)
// ---------------------------------------------------------------------

esc_l             = 44.2;   // MEASURED(w17-batch1-measurements-for-codex.md:41)
esc_w             = 33.7;   // MEASURED(same)
esc_h             = 34.0;   // MEASURED(same)
esc_air_gap       = clr_esc_air; // POLICY

chg_l             = 30.0;   // ASSUMED (see §9) two sources conflict, M-16
chg_w             = 25.0;   // ASSUMED (see §9)
chg_h             = 10.0;   // ASSUMED (see §9)

sp3t_body_l       = 20.0;   // ASSUMED (see §9) no switch selected, M-13
sp3t_body_w       =  9.0;   // ASSUMED (see §9)
sp3t_body_h       = 12.0;   // ASSUMED (see §9)
sp3t_cutout_l     = 13.0;   // ASSUMED (see §9)
sp3t_cutout_w     =  5.0;   // ASSUMED (see §9)

spk_l             = 35.3;   // MEASURED(w17-batch1-measurements-for-codex.md:47)
spk_w             = 25.1;   // MEASURED(same)
spk_h             =  6.1;   // MEASURED(same)
spk_port_d        = 22.0;   // ASSUMED (see §9) a design choice with no acoustic evidence, M-18

hall_gap          = 1.5;    // ASSUMED (see §9) target inside a 1..3 mm band, M-19

// DRS. The 58 mm figure in the inventory is a RAW BOUNDING BOX, not a
// pivot spacing. A four-bar linkage needs pivot-to-pivot lengths and we do
// not have one. Leaving this undef is deliberate: any model that needs it
// must fail loudly rather than invent a throw. Measurement: M-14d.
drs_arm_bbox_l    = 58.0;   // DOCUMENTED(ZA:26-27 raw STL bbox — NOT a pivot span)
drs_arm_pivot_span = undef; // DELIBERATELY UNSET — see AA §6

flap_open_w       = 16.0;   // ASSUMED (see §9) M-12
flap_open_h       = 11.0;   // ASSUMED (see §9) M-12
flap_wall         =  2.0;   // ASSUMED (see §9) M-12
vent_w            = 13.1;   // ASSUMED (see §9) this is the FLOOR slot, not the shell vent, M-15
vent_h            = 10.3;   // ASSUMED (see §9)


// ---------------------------------------------------------------------
// 8. GCS box (every envelope in here is a guess — AA §8)
// ---------------------------------------------------------------------

gcs_tx_l          = 70.0;   // ASSUMED (see §9) vendor ES24TX Pro, and ONLY if ours is the Pro
gcs_tx_w          = 49.0;   // ASSUMED (see §9)
gcs_tx_h          = 32.5;   // ASSUMED (see §9)
gcs_ftdi_l        = 45.0;   // ASSUMED (see §9) nothing recorded anywhere, M-17
gcs_ftdi_w        = 18.0;   // ASSUMED (see §9)
gcs_ftdi_h        = 10.0;   // ASSUMED (see §9)
gcs_wifi_l        = 60.0;   // ASSUMED (see §9)
gcs_wifi_w        = 25.0;   // ASSUMED (see §9)
gcs_wifi_h        = 12.0;   // ASSUMED (see §9)
gcs_hub_l         = 90.0;   // ASSUMED (see §9) hub NOT PROCURED
gcs_hub_w         = 40.0;   // ASSUMED (see §9)
gcs_hub_h         = 15.0;   // ASSUMED (see §9)

gcs_grid_pitch    = 10.0;   // POLICY(a repeating M3 sled grid; sleds reprint, the box does not)
gcs_wall          =  2.4;   // ESTIMATED(6 perimeters at 0.4 — a desk box, tugged by one cable)
gcs_floor         =  3.0;   // ESTIMATED(stiffer than the walls; it carries the grid)
gcs_clear         =  6.0;   // POLICY(air around the TX module, the box's only real dissipator)


// ---------------------------------------------------------------------
// 9. ===================  ASSUMED — THE OWNER'S LIST  ==================
//    Every value referenced above as "ASSUMED (see §9)" is repeated here
//    with the measurement that retires it. NONE of these is a measurement.
//    Printing a production part to any of them is forbidden.
//    Mirror of AA §12 and of ../w17-mechanical-measurement-session-prompt.md
// ---------------------------------------------------------------------
//
//  M-01  s0_measured                                   9.82  <- the REQUIREMENT, not a fact
//  M-02  ko01_x_lo/x_hi/l_half/z_lo/z_hi   -80/100/22/22/38  <- provisional steering band
//  M-03  esp_thk_headers                                13.0
//  M-03  esp_hole_dx / esp_hole_dy / esp_hole_d  33/25/3.2
//  M-03  esp_usb_w / esp_usb_h / esp_usb_offset   9/3.5/0.0
//  M-03  board_seat_x0                                   3.0  <- OP-H
//  M-04  esp_socket_stack                               11.0
//  M-05  pdb_stack_h                                    13.0
//  M-06  pdb_len / pdb_wid                            55/45
//  M-07  guide_top_z                                    30.0
//  M-12  flap_open_w / flap_open_h / flap_wall   16/11/2.0
//  M-13  sp3t_body_l/w/h, sp3t_cutout_l/w   20/9/12, 13/5
//  M-14d drs_arm_pivot_span                          undef   <- refuses to be guessed
//  M-15  vent_w / vent_h                          13.1/10.3
//  M-16  chg_l / chg_w / chg_h                      30/25/10  <- sources conflict
//  M-17  gcs_tx_*, gcs_ftdi_*, gcs_wifi_*, gcs_hub_*
//  M-18  spk_port_d                                    22.0
//  M-19  hall_gap                                       1.5
//  C-1   insert_m3_d / insert_m3_h / screw_m3_clear_d
//  C-1   zip_slot_w / zip_slot_l                     4.0/2.5
//
// ---------------------------------------------------------------------


// ---------------------------------------------------------------------
// 10. Self-checks. These run on every render and stop it if the geometry
//     drifts away from the study's arithmetic.
// ---------------------------------------------------------------------

assert(wall_top_z == ko01_z_guard,
       "register wall must stop exactly at the KO-01 guard height (AA §5.4)");
assert(wall_l_out == ko01_l_guard,
       "register wall outer face must sit on the KO-01 lateral guard (AA §5.4)");
assert(board_l_out - board_l_in >= esp_thk_headers - 1e-9,
       "the 13 mm band is exactly one board thick — AA §5.2 no longer holds");
assert(pdb_z1 <= ko01_z_guard,
       "PDB audit top has risen above the KO-01 guard: zero reserve is now negative");
assert(guide_top_z <= board_top_z,
       "the aft end guide may stop below the board top, never above it");
assert(is_undef(drs_arm_pivot_span),
       "drs_arm_pivot_span was given a value — the 58 mm figure is a bbox, not a pivot span");

echo(str("[w17_params] S0 placeholder = ", s0_measured,
         " mm (REQUIREMENT, unmeasured) | KO-01 guard: nothing above Z",
         ko01_z_guard, " inside |L| ", ko01_l_guard,
         " | board band = ", board_l_out - board_l_in, " mm"));
