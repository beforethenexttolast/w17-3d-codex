// =====================================================================
// w17_params.scad — the source of every SHARED dimension in 11_cad/
// =====================================================================
//
//  Repo:    w17-3d-codex          Branch: design/placement-and-cage
//  Study:   ../10_assembly_architecture/AA_electronics_placement_study.md
//  Date:    2026-09-03
//
//  RULE OF THIS FILE (it is the whole point of it):
//  ------------------------------------------------------------------
//  Every number below carries a provenance tag, and every dimension
//  SHARED by more than one model lives here — models import this file
//  and use names.
//
//  It is NOT the only place a number may be written, and claiming that
//  would be a lie you could check in ten seconds. A number used by
//  exactly one file is declared at the top of that file, still named and
//  still tagged. Today those are: the coupon plate/label constants
//  (fit_check_coupons.scad:30-32,:42,:89,:224-228), the print-plate spacing in
//  second_floor_cage.scad, gcs_box.scad's local constants, and two
//  shape-proportion defaults in lib/w17_lib.scad (:109 extra_h, :135
//  relief_frac), both of them named default arguments. What is banned is an ANONYMOUS literal in geometry — a
//  bare 8 inside a cylinder() — because nobody can later tell whether it
//  was measured or invented.
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
//  A2 IS NOT-EXECUTED AND PHASE B IS BLOCKED. Nothing in this file
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
wall_std          = 2.5;    // POLICY(AA §5.4 NOMINAL register/box wall). The cage's
                            //   actual register wall is wall_t (§6): this nominal
                            //   less the PDB's drop-in clearance.
fit_clearance     = 0.20;   // ASSUMED (see §9) per-side print clearance, retired by
                            //   coupon C-1. It lives here, with the other process
                            //   constants, because it is a property of THIS printer
                            //   and THIS filament rather than of any one part — and
                            //   because §6's register wall is derived from it.
$fn               = 48;     // render quality; not a physical dimension


// ---------------------------------------------------------------------
// 2. Fastener + insert family
// ---------------------------------------------------------------------

screw_m3_clear_d  = 3.4;    // ASSUMED-adjacent: the clearance HOLE Ø (= M3 thread OD + clearance), used directly as cylinder(d=) in gcs_box/coupons — NEVER a measured thread OD; M-22b.1 records the stock and is register-only. Confirmed by coupon C-1
screw_m3_head_d   = 6.0;    // DOCUMENTED(ISO 7380 button head M3, nominal)
insert_m3_d       = 4.0;    // ASSUMED (see §9) the BORE the brass M3x5 insert is melted INTO (w17_lib w17_standoff cuts cylinder(d=insert_d)) — NOT the measured knurl OD, which would leave nothing to grip; M-22a.1/.1b record the stock and are register-only. Brand-dependent
insert_m3_h       = 5.7;    // ASSUMED (see §9) brass heat-set M3x5 length == pocket depth, 1:1, so M-22a.2 sets this one directly
insert_boss_wall  = 2.0;    // POLICY(hoop wall around a heat-set insert, >= 2 mm)


// ---------------------------------------------------------------------
// 3. Vehicle datums and the two numbers everything hangs on
// ---------------------------------------------------------------------

// S0 — shell bottom edge above DAT-F. Bounded 0 .. ~11 mm, NEVER measured.
// The value below is the REQUIREMENT (AA §5.3), parked here as a placeholder
// so the models render. It is not a measurement. Measurement: M-01.
s0_measured       = 9.82;   // ASSUMED (see §9)

// The worst finite shell roof sampled over BOTH board seats at S0 = 0.
roof_z_worst      = 27.18;  // DERIVED(ZK:123 the limiting shell point sampled over both
                            //   seats, at approximately X+3 / L-37; the arithmetic that
                            //   turns it into required S0 is ZK:125)

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

// Registered on-edge seats (ZK:101-102, the two ESP32 wall-seat rows / AA §3 rows 1-2.
// ZK:99 and ZK:100 are the RP1 and BL-M8812EU2 seats and have nothing to do with these.)
board_seat_x0     = 3.0;    // ASSUMED (see §9) OP-H turns on whether this can move aft
board_seat_z0     = 1.0;    // DERIVED(ZK:101 seat Z1..32) parametric escape route, AA §5.3
board_l_in        = 30.0;   // DERIVED(ko01_l_guard) PCB plane inboard face
board_l_out       = 43.0;   // DERIVED(ZK:101 outer face L-43) == wing_l_half
board_top_z       = 32.0;   // DERIVED(board_seat_z0 + esp_wid: the 31 mm side stands up)

// hole pattern + USB-C: no MH-ET drawing exists in any project document
esp_hole_dx       = 33.0;   // ASSUMED (see §9) M-03
esp_hole_dy       = 25.0;   // ASSUMED (see §9) M-03
esp_hole_d        = 3.2;    // ASSUMED (see §9) M-03
esp_usb_w         = 9.0;    // ASSUMED (see §9) M-03
esp_usb_h         = 3.5;    // ASSUMED (see §9) M-03
esp_usb_offset    = 0.0;    // ASSUMED (see §9) offset of the port from the edge centreline, M-03
esp_socket_stack  = 11.0;   // ASSUMED (see §9) seated female+male header stack, M-04

// TWO PROJECT DOCUMENTS DISAGREE ABOUT THE CONNECTOR ITSELF, and the whole package
// has so far assumed one of them without saying so:
//   w17-electrical-inputs-for-codex.md:8,10 — "onboard micro-USB serial",
//                                             "micro-USB on one short edge"
//   ZK:102                                  — "both USB-C service ends face X+42"
// Neither is a caliper record. AA §1 now records the conflict; M-03(e)/(f) records
// the connector TYPE as well as its position and edge. The two strings below are
// what the models currently believe, written down so the belief is visible.
// esp_usb_w/h above are sized for the LARGER family. That ordering is CONNECTOR
// FAMILY GENERAL KNOWLEDGE, not a project record and not a caliper reading -- a
// USB-C shell is wider and taller than a micro-B one -- and it is used only to
// say WHICH WAY to be wrong, never as a dimension. Over-sizing a clearance
// opening is the safe direction — but a micro-USB board also changes AA §4.7's service story
// and §5.6's clip-notch rule, not just a hole size.
esp_usb_type      = "usb_c";      // ASSUMED (see §9) M-03(f)
esp_usb_edge      = "fwd_short";  // ASSUMED (see §9) M-03(e) — the forward short edge


// ---------------------------------------------------------------------
// 6. The cage itself (AA §5.4, as corrected 2026-09-03)
// ---------------------------------------------------------------------

// The register wall. Its INNER face registers the PDB and its OUTER face is where the
// board's PCB plane begins. The outer face cannot move: it is both board_l_in and the
// KO-01 lateral guard. So the PDB's drop-in clearance is paid for out of wall
// thickness, and the wall ends up thinner than the wall_std nominal. That is the right
// trade — a wall face sitting exactly on the PDB's L±27.5 edge is an interference fit
// with the thing it is supposed to locate, and the cassette is a LIFT-OUT assembly:
// the PDB has to drop in by hand.
wall_l_in         = pdb_l_half + fit_clearance;  // DERIVED = 27.7
wall_l_out        = board_l_in;                  // DERIVED = 30 (== ko01_l_guard)
wall_t            = wall_l_out - wall_l_in;      // DERIVED = 2.3, asserted vs wall_min
wall_top_z        = 14.0;   // DERIVED(== ko01_z_guard; the wall MUST stop here)

rail_h            = 3.0;    // ESTIMATED(enough to catch a 1.6 mm PCB edge without a tall thin wall)
rail_t            = 1.8;    // ESTIMATED(printable rail, >= wall_min at 4 perimeters minus squish)
slot_w            = 1.8;    // ESTIMATED(esp_pcb_t 1.6 + 0.2 hand-fit; coupon C-1 confirms)
slot_lead_in      = 0.6;    // ESTIMATED(45° chamfer so the board finds the slot blind)

guide_x0          = 1.0;    // DERIVED(aft of board_seat_x0, on the wing)
guide_x1          = 3.0;    // DERIVED(== board_seat_x0)
guide_top_z       = 30.0;   // ASSUMED (see §9) a cage DESIGN OUTPUT; M-07 reads a shell-interior clear height, which BOUNDS it, not its value (see M-07.worst) — may stop below board_top_z
guide_top_margin  = 2.0;    // DERIVED(board_top_z - guide_top_z) the §5.3 escape route — a HARDCODED literal: RECOMPUTE it by hand whenever guide_top_z moves; no assert re-derives it

rail_out          = board_l_in + slot_w + rail_t;  // DERIVED = 33.6, outboard face of rail/guide

// The aft end guide, and the one thing in the cage that reaches over a board.
// It occupies the board's aft 2 mm of component zone on the OUTBOARD side.
// That is a real intrusion and coupon C-3 is what proves or kills it.
guide_post_l      = 2.0;    // ESTIMATED(how far the post overlaps the board's aft edge)
guide_post_t      = 4.0;    // ESTIMATED(thick enough to stand 29 mm tall without a rib)

// Board retention. It is a CLIP, not a bar, and not a screw. Three CAD
// findings forced that, and all three are worth remembering:
//
//  1. NOTHING MAY RISE ABOVE board_top_z. A bar lying over the board's top
//     edge adds its own thickness, and AA §5.3's required S0 is computed
//     from the board top: 3 mm of bar turns 9.82 mm into 12.82 mm, which is
//     outside the 0..11 mm bound S0 is known to live in. It would kill the
//     design on paper. The clip's top face is flush at board_top_z.
//  2. THERE IS NOWHERE FOR A HEAT-SET INSERT. An M3x5 insert needs an 8 mm
//     boss; the aft end guide is 2 mm long in X, and above Z14 the only
//     legal band is |L| 30..43, which the board fills.
//  3. RETENTION MUST TOUCH THE COMPONENT ZONE. The band is exactly one
//     board thick (AA §5.2), so any structure that reaches over the board
//     stands in the space its outboard components occupy. The only choice
//     is HOW MUCH and AT HOW FEW STATIONS. Two clips per board is the
//     smallest answer that still resists a 20 g crash load. WHERE those
//     stations may be depends on the real board's component layout —
//     M-03, then coupon C-3 with a board in hand.
//
// The clip drops onto a printed peg in the base plate; the peg/hole fit is
// exactly what coupon C-1's ladder measures, so the clip is also the first
// part that consumes a real coupon result.
clip_len          = 6.0;    // ESTIMATED(a short station, to touch as few components as possible)
clip_t            = 2.0;    // ESTIMATED(5 perimeters; it is loaded in compression, not bending)
clip_foot_w       = 5.0;    // ESTIMATED(enough footprint to stand a 31 mm upright on)
clip_peg_d        = 3.0;    // ESTIMATED(matches coupon C-1's 3 mm peg/hole ladder)
clip_finger_h     = 2.0;    // ESTIMATED(overlap onto the board's top edge)
clip_finger_gap   = 0.4;    // ESTIMATED(so the finger clears the PCB face, not clamps it)
clip_station_x    = [10, 34];  // ESTIMATED(two stations, spread over the 39 mm board)
// fit_clearance is in §1 with the other process constants.

zip_slot_w        = 4.0;    // ASSUMED (see §9) the SLOT the tie threads through = strap width + dressing room (fits a 3 mm tie); M-22c.1 records the strap and is register-only. Tie stock not calipered
zip_slot_l        = 2.5;    // ASSUMED (see §9) the slot's other side = strap thickness + dressing room; M-22c.2 records the strap and is register-only
zip_slot_bridge   = 3.0;    // ESTIMATED(material left between a slot pair)

pass_slot_w       = 10.0;   // ESTIMATED(a 4-way silicone bundle plus dressing room)
pass_slot_h       = 6.0;    // ESTIMATED(same)
pass_slot_inset   = 9.0;    // ESTIMATED(each pass-through set this far in from its end
                            //   of the wing, so neither lands on the aft end guide)
pass_slot_z0      = 1.0;    // ESTIMATED(material left between the base plate and the
                            //   bottom of the pass-through opening)

// Cable-tie stations on the base plate (AA §4.9 wants a loom clamped every <=60 mm
// near motion; three stations over a 41 mm wing is far tighter than that).
zip_station_dx    = [10, 24, 36];  // ESTIMATED(stations measured forward from wing_x0)
zip_line_offset   = 6.0;    // ESTIMATED(the tie line sits this far outboard of the
                            //   register wall's mid-plane -> |L| 34.85, which is
                            //   outboard of the rail at 33.6 and inboard of the wing
                            //   edge at 43: a loom lane under the board's outboard face)

// LED / Hall tail exit at the rear outboard corner, PS-09 route.
tail_hole_d       = 8.0;    // ESTIMATED(same basis as pass_slot_w/h — a 4-way silicone
                            //   bundle plus dressing room. The loom is NOT calipered;
                            //   this is a chosen generosity, not a gauge over a body,
                            //   and it is a hole in free plate, so being 2 mm large
                            //   costs nothing and being 2 mm small costs a re-print)
tail_hole_x       = 4.0;    // ESTIMATED(inset forward of the wing's aft edge)
tail_hole_l_inset = 6.0;    // ESTIMATED(inset inboard of the wing's outer edge)

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
//  M-03  esp_usb_type                              "usb_c"  <- sources conflict, AA §1
//  M-03  esp_usb_edge                          "fwd_short"
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
//  C-1   fit_clearance                                  0.20
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
// DELIBERATELY ONE-SIDED. It fires if the real board turns out FATTER than the band,
// which is the failure that ends the design. A board that measures THINNER than 13 mm
// passes it and simply leaves slack in the band — AA §5.2's "exactly one board thick"
// stops being exact, in the harmless direction. See AA §5.2 for what that slack does
// and does not buy.
assert(board_l_out - board_l_in >= esp_thk_headers - 1e-9,
       "the 13 mm band is exactly one board thick — AA §5.2 no longer holds");
assert(wall_t >= wall_min,
       "the register wall has thinned below the 4-perimeter minimum (AA §5.4)");
assert(pdb_z1 <= ko01_z_guard,
       "PDB audit top has risen above the KO-01 guard: zero reserve is now negative");
assert(guide_top_z <= board_top_z,
       "the aft end guide may stop below the board top, never above it");
// The gate that decides whether this cage exists at all (AA §5.3):
s0_required       = board_top_z + clr_static - roof_z_worst;  // DERIVED = 9.82
s0_upper_bound    = 11.0;   // DERIVED(D_measurement_plan.md:43-49, S0 in 0..~11)

assert(s0_required <= s0_upper_bound,
       "the cage's tallest point now needs an S0 outside the 0..11 mm bound (AA §5.3)");
assert(is_undef(drs_arm_pivot_span),
       "drs_arm_pivot_span was given a value — the 58 mm figure is a bbox, not a pivot span");

// Machine-readable, and load-bearing: render.sh reads board_top_z from this line and
// asserts that cage_all's exported STL tops out at exactly that Z. That is what turns
// "nothing rises above the board top" from a claim in prose into a check that runs.
echo(str("PARAM board_top_z = ", board_top_z));

echo(str("[w17_params] S0 placeholder = ", s0_measured,
         " mm (REQUIREMENT, unmeasured) | KO-01 guard: nothing above Z",
         ko01_z_guard, " inside |L| ", ko01_l_guard,
         " | board band = ", board_l_out - board_l_in, " mm"));
