#!/usr/bin/env python3
"""Generate MEASUREMENT_RECORD_SHEET.csv and .md from one row list.

Usage:  gen_measurement_sheet.py <repo-root>

ONE SOURCE. Both sheets are written from the single list `S` below, so the
printable sheet and the machine-readable twin cannot drift. Never hand-edit
either sheet — edit this file and re-run it.

THE `param` COLUMN IS LOAD-BEARING.
    id,param,quantity,unit,value,tolerance,photo_ref,notes

`param` holds the BARE w17_params.scad parameter name that this one cell
sets, or is EMPTY for a register-only row. `11_cad/tools/ingest_measurements.py`
reads `param` first and will not guess a mapping from prose.

Two rules keep the chain honest, and both come out of the 2026-09-05 review:

 1. ONE ROW PER PARAMETER. The ingest tool refuses (CONFLICT) when two rows
    target the same parameter, so a quantity read at several stations gets
    N register-only cells plus ONE derived row that carries the `param`
    (M-01.worst, M-02a.min, M-02b.max, M-02c.max).

 2. A MEASURED STOCK DIMENSION IS NOT A FEATURE DIMENSION. The hole a screw
    passes through, the bore an insert melts into and the slot a cable tie
    threads through are all `stock + clearance`. Those rows are register-only
    and say "DO NOT ENTER INTO SCAD" — the feature parameter stays a CAD
    decision made from the recorded stock number.
"""
import csv, os, sys

REPO = sys.argv[1]

# (station_key, id, param, quantity, unit, tolerance, photo_required_text, notes)
S = []
def r(st, i, q, u, tol, photo, notes, param=""):
    S.append((st, i, q, u, tol, photo, notes, param))

NOSCAD = "DO NOT ENTER INTO SCAD — register-only. "

# ---------------- Station 0 ----------------
st = "0 — What actually exists (M-00)"
for gid, name, n in [("02","Rear axle + drivetrain (ASA)",8),
                     ("03","Front suspension + steering (PETG)",8),
                     ("04","Wheels (PETG)",7),
                     ("05","Floor (PETG)",8),
                     ("06","Body shell (PLA matte black)",7),
                     ("07","Brake-light diffuser",1)]:
    r(st, f"M-00.g{gid}", f"Group {gid} — {name} ({n} files): none / some / all, then WHICH parts",
      "text", "-", "the group as laid out",
      "Condition per part: good / warped / layer split / supports still on / TP / unknown material. Unknown material or settings = a DIAGNOSTIC part, not a build part.")
r(st, "M-00.g99", "OPTIONAL / UNCERTAIN / anything else printed", "text", "-", "",
  "Name them; do not fold them into a REQUIRED group.")
for pid, part, why in [
    ("p1","Servoholder.stl","gates M-28, the ~1.7 mm steering-servo interference (OP-B)"),
    ("p2","FloorBoard2.stl","gates M-20, the three centreline splice screws (OP-G)"),
    ("p3","2023NewFrontFloorLargerParts.stl","gates M-20 and the floor datum DAT-F itself"),
    ("p4","NEW BODY 2024 REAR.stl (+ FRONT 1)","M-01 needs a shell to seat — no shell, no S0, cage stays a proposal"),
    ("p5","2023NEWSideVent1/2.stl","gates M-15, the charge-flap candidate CF-1"),
    ("p6","2021Rearwing with DRS.stl + DRS Arm for 2021 Rear Wing.stl","gates M-14, the DRS linkage")]:
    r(st, f"M-00.{pid}", f"Does `{part}` exist? condition?", "yes/no + text", "-", "",
      f"Called out by name because it {why}.")

# ---------------- Station 1 Block A ----------------
st = "1A — MH-ET D1-Mini ESP32 (bench, calipers)"
r(st,"M-03a.1","Bare PCB length (jaws on FR4 edges)","mm","±0.2","","esp_len. STOP if outside 39 x 31 +/-1: not the planned SKU.")
r(st,"M-03a.2","Bare PCB width","mm","±0.2","","esp_wid.")
r(st,"M-03b","PCB thickness on a bare edge","mm","±0.1","","esp_pcb_t; slot_w derives from it. Expect 1.6.")
r(st,"M-03c","TOTAL thickness with headers fitted, at its thickest (incl. tallest underside tail)","mm","±0.2","","esp_thk_headers. STOP if > 13.0 — the assert at w17_params.scad:391 fires and the cage design stops.", param="esp_thk_headers")
r(st,"M-03d.1","Mounting-hole pitch measured ALONG THE 39 mm LONG EDGE (centre to centre)","mm","±0.2","","esp_hole_dx = the pitch along the LONG edge (33.0 ASSUMED against esp_len 39.0). Long edge, not 'X on the bench': the board is loose, so name the edge, never a car axis.", param="esp_hole_dx")
r(st,"M-03d.2","Mounting-hole pitch measured ALONG THE 31 mm SHORT EDGE (centre to centre)","mm","±0.2","","esp_hole_dy = the pitch along the SHORT edge (25.0 ASSUMED against esp_wid 31.0).", param="esp_hole_dy")
r(st,"M-03d.3","Mounting-hole diameter","mm","±0.2","","esp_hole_d. If there are no holes at all, say so.", param="esp_hole_d")
r(st,"M-03e","WHICH EDGE carries the service port: long or short, and which end","text","-","the port edge with silkscreen legible","esp_usb_edge; decides the clip notch. Port on a LONG edge changes the wall-seat service face. Write the literal the parameter takes: fwd_short / aft_short / inb_long / outb_long.", param="esp_usb_edge")
r(st,"M-03f.1","WHICH CONNECTOR it actually is: USB-C / micro-USB B / other","text","-","the connector, shell shape readable","esp_usb_type. CLOSES OP-I. micro-USB rewrites AA 4.7 service story and 5.6 clip-notch rule, not just a hole size. Write the literal: usb_c / micro_usb / other.", param="esp_usb_type")
r(st,"M-03f.2","Connector shell width","mm","±0.2","","esp_usb_w.", param="esp_usb_w")
r(st,"M-03f.3","Connector shell height","mm","±0.2","","esp_usb_h.", param="esp_usb_h")
r(st,"M-03f.4","Connector protrusion past the PCB edge","mm","±0.2","","service opening depth.")
r(st,"M-03f.5","Connector offset from that edge's centreline","mm","±0.2","","esp_usb_offset.", param="esp_usb_offset")
r(st,"M-03g.1","With a DEAD cable fitted: plug-body projection past the PCB edge","mm","±0.5","","Service access; KO-34. The cable's far end connects to NOTHING.")
r(st,"M-03g.2","Cable minimum bend radius before the plug is levered","mm","±0.5","","Service access at the X+42..+46 tongue.")
r(st,"M-03h.1","Component-free margin from the FORWARD short edge, on the OUTBOARD face","mm","±0.5","","OUTBOARD FACE = the face carrying the TALLER components, i.e. the one that will point AWAY from the register wall once the board stands on edge. Mark it with tape before measuring. OP-H / clip stations.")
r(st,"M-03h.2","Component-free margin from the AFT short edge, on the OUTBOARD face","mm","±0.5","","OUTBOARD FACE as defined in M-03h.1. OP-H.")
r(st,"M-03h.3","Component-free margin from the INBOARD long edge, on the OUTBOARD face","mm","±0.5","","OUTBOARD FACE as defined in M-03h.1. OP-H.")
r(st,"M-03h.4","Component-free margin from the OUTBOARD long edge, on the OUTBOARD face","mm","±0.5","the outboard face flat-on with a rule alongside","OUTBOARD FACE as defined in M-03h.1. OP-H. STOP if no bare land at X+10 or X+34 — clip_station_x [10,34] stands on components. board_seat_x0 is a DECISION this row unlocks, not a number it reads: register-only.")
r(st,"M-03x.1","Board #2: length and thickness-with-headers (cross-check)","mm (L x T)","±0.2","","Register-only — label the two numbers. If any board differs by more than the tolerance they are not one SKU: take every M-03 row per board.")
r(st,"M-03x.2","Board #3: length and thickness-with-headers (cross-check)","mm (L x T)","±0.2","","Register-only — label the two numbers. Same.")
r(st,"M-03i","OPTIONAL: adjacent header pin pairs read off the silkscreen","text","-","both silkscreen edges, every label readable","A2 review F12 + open finding F20. Do NOT let this delay the M-04 verdict.")
r(st,"M-04","Female header + MH-ET male pins, SEATED: total stack height","mm","±0.1","","esp_socket_stack. GO/NO-GO on socketing vs S0 >= 9.82. NO-GO = STOP, do not solder; F12 reopens. Marginal is a report, not a judgement. Needs a female header from stock.", param="esp_socket_stack")

# ---------------- Station 1 Block B ----------------
st = "1B — PDB components and connector bodies (bench, calipers)"
r(st,"M-05a.1","1000 uF electrolytic: body diameter","mm","±0.2","","Board planning; not a height candidate.")
r(st,"M-05a.2","1000 uF: INSTALLED HEIGHT above the seating plane (not lead tips)","mm","±0.2","","pdb_stack_h candidate (M-05d).")
r(st,"M-05a.3","1000 uF: lead length below the body","mm","±0.5","","Board planning.")
for half, hid in [("male","1"),("female","2")]:
    r(st,f"M-05b.{hid}l",f"XT60 {half} half: body LENGTH, as it will lie on the board","mm","±0.2","","KO-33 dock body. NOT a height candidate.")
    r(st,f"M-05b.{hid}w",f"XT60 {half} half: body WIDTH","mm","±0.2","","KO-33 dock body. NOT a height candidate.")
    r(st,f"M-05b.{hid}h",f"XT60 {half} half: INSTALLED HEIGHT above the board seating plane","mm","±0.2","","pdb_stack_h candidate (M-05d). One number per cell: only the HEIGHT is a candidate.")
for part, hid, extra in [("XT90-S anti-spark FEMALE","1","the half that faces the live pack"),
                         ("XT90H-M male","2","")]:
    r(st,f"M-05c.{hid}l",f"{part} half: body LENGTH","mm","±0.2","",(extra+". " if extra else "")+"NOT a height candidate.")
    r(st,f"M-05c.{hid}w",f"{part} half: body WIDTH","mm","±0.2","","NOT a height candidate.")
    r(st,f"M-05c.{hid}h",f"{part} half: INSTALLED HEIGHT above the board seating plane","mm","±0.2","","pdb_stack_h candidate (M-05d).")
r(st,"M-05c.3","Mated overall LENGTH of the pigtail pair","mm","±0.5","","Finger access body-on. THIS IS A LENGTH, NOT A HEIGHT — it is NOT an M-05d candidate.")
r(st,"M-05c.4","PULL AXIS: which way the finger pulls","text","-","the mated pair with an arrow on tape along the pull axis","Charge/run interlock ritual (F9a/F9b).")
r(st,"M-05d","TALLEST PDB PART = max(M-05a.2, M-05b.1h, M-05b.2h, M-05c.1h, M-05c.2h, 9.1 UBEC MEASURED) — INSTALLED HEIGHTS above the board seating plane ONLY. Write the arithmetic, not just the answer","mm","±0.2","","pdb_stack_h. Mated lengths (M-05c.3) and body lengths/widths are NOT candidates. STOP if > 13: PDB audit top Z14 vs KO-01 bottom Z22 is the 8 mm policy with nothing spare. Report; do not re-plan the cage at the bench.", param="pdb_stack_h")
r(st,"M-06","PDB finished outline, mounting holes, connector exits","-","-","",NOSCAD+"BLOCKED — the PDB does not exist; no substrate bought. Built at A2 build week, and its outline is a DESIGN OUTPUT, not a measurement. pdb_len/pdb_wid stay ASSUMED. Do not cut a pocket to 55 x 45.")
for cid, conn in [("a","XT30"),("b","3-pin servo (JR)"),("c","JST-XH 3-pin"),("d","JST-XH 4-pin"),
                  ("e","JST-XH 5-pin"),("f","JST-PH 2-pin"),("g","U.FL head + pigtail diameter"),
                  ("h","camera<->WiFi shielded 4-pin / micro-USB")]:
    r(st, f"M-21.{cid}", f"{conn}: body L x W x H, and MATED depth (pair plugged together)",
      "mm (L x W x H; mated)","±0.2","","KO-33 dock bodies; M connector matrix; Z wire schedule. Sanity-checks pass_slot_w/h (10 x 6). Register-only: no parameter consumes these, so the four numbers may share one cell — label each.")

# ---------------- Station 1 Block C ----------------
st = "1C — Process and fastener stock (bench, calipers)"
r(st,"M-22a.1","Heat-set insert M3x5: outside diameter at the widest KNURL (RECORD ONLY — this is NOT insert_m3_d)","mm","±0.1","",NOSCAD+"insert_m3_d (4.0 ASSUMED) is the BORE the insert is melted INTO — lib/w17_lib.scad:98-100 cuts cylinder(d = insert_d) into the boss top. A bore equal to the knurl OD leaves the brass nothing to bite. Report the knurl OD; the bore is a CAD decision made from it and M-22a.1b.")
r(st,"M-22a.1b","Heat-set insert M3x5: BODY (minor) outside diameter below the knurl","mm","±0.1","",NOSCAD+"The second half of the bore decision: the melt bore sits between this and the knurl OD. NEW CELL — the sitting previously recorded only the knurl.")
r(st,"M-22a.2","Heat-set insert M3x5: overall LENGTH","mm","±0.1","","insert_m3_h (5.7 ASSUMED) is the pocket DEPTH, and pocket depth = insert length 1:1 (lib/w17_lib.scad:92-101, w17_standoff insert_h). This one IS the parameter.", param="insert_m3_h")
r(st,"M-22b.1","M3 screw: thread outside diameter (RECORD ONLY — this is NOT screw_m3_clear_d, which is the clearance HOLE diameter = thread OD + clearance)","mm","±0.1","",NOSCAD+"screw_m3_clear_d (3.4) is used DIRECTLY as a hole diameter — gcs_box.scad:115,162,212 and fit_check_coupons.scad:139 all do cylinder(d = screw_m3_clear_d). Writing a measured ~3.0 thread OD there makes every screw hole too small for its own screw. It is also tagged ASSUMED-adjacent, so the ingest tool will not patch it in any case.")
r(st,"M-22b.2","M3 screw: button-head diameter","mm","±0.1","",NOSCAD+"screw_m3_head_d (6.0) is DOCUMENTED(ISO 7380), not ASSUMED — the ingest tool does not patch it. > 6.0 undersizes every counterbore: report it as a finding.")
r(st,"M-22b.3","M3 screw: head height","mm","±0.1","",NOSCAD+"Counterbore depth input.")
r(st,"M-22c.1","Cable tie: strap WIDTH (RECORD ONLY — this is NOT zip_slot_w, which is the SLOT the strap threads through)","mm","±0.1","",NOSCAD+"zip_slot_w (4.0) IS the slot rectangle — lib/w17_lib.scad:176-179 cuts cube([slot_w, slot_l, t]). w17_params.scad:243 sizes it 4.0 for a 3 mm tie, i.e. slot = strap + dressing room. STOP if the strap is wider than 3.5: the 4.0 slot then has under 0.5 mm of dressing room. Report the strap; the slot is a CAD decision.")
r(st,"M-22c.2","Cable tie: strap THICKNESS (RECORD ONLY — this is NOT zip_slot_l)","mm","±0.1","",NOSCAD+"zip_slot_l (2.5) is the slot's other side, same lib/w17_lib.scad:176-179 cube. Slot = strap + dressing room, never strap alone.")
r(st,"M-22c.3","Cable tie: head thickness","mm","±0.1","",NOSCAD+"Clearance under the base plate.")
r(st,"M-22d","OPTIONAL (needs wire stock): OD of a dressed 4-way silicone bundle","mm","±0.5","",NOSCAD+"Sanity for pass_slot_w/h (10 x 6) and tail_hole_d (8.0), all ESTIMATED — not ASSUMED, so not tool-patchable.")
r(st,"C-1.1","RESERVED — per-side print clearance read off coupon C-1 (the peg/hole ladder). NOT a caliper row: leave blank until TP-001 is printed and read","mm","±0.05","","fit_clearance (0.20 ASSUMED). The ONLY row on this sheet that a printed part answers. Procedure and the exact export command: 11_cad/COUPON_PRINT_PLAN.md section C-1. Record the first ladder step that fits and stays put when shaken; steps 1-2 are negative controls.", param="fit_clearance")

# ---------------- Station 1 Block D ----------------
st = "1D — Other on-hand parts (bench, calipers)"
r(st,"M-16.1","IP2326 charge module: body length","mm","±0.2","","chg_l. STOP if any axis exceeds the 30 x 25 x 10 cell.", param="chg_l")
r(st,"M-16.2","IP2326: body width","mm","±0.2","","chg_w.", param="chg_w")
r(st,"M-16.3","IP2326: body height","mm","±0.2","","chg_h.", param="chg_h")
r(st,"M-16.4","IP2326: mounting-hole positions and diameter (if any)","mm","±0.2","","ASM-59 seat.")
r(st,"M-16.5","IP2326: which edge carries the onboard Type-C, and its protrusion","mm + text","±0.2","","CF-1/CF-6 flap decision.")
r(st,"M-16.6","IP2326: which face gets hot","text","-","","Thermal face; no pocket may be cut before this row.")
r(st,"M-16.7","IP2326: where the leads exit","text","-","","")
r(st,"M-16.8","IP2326: is the state LED on the board (light-pipe) or can it fly on two wires?","text","-","both faces, silkscreen legible","CLOSES OP-C. The photo is also the evidence this is a genuine BALANCING charger, not boost+CV. Two sources conflict (29x26x6 vs 18.3x31 in a <=10 mm cell) and NEITHER is a caliper record.")
r(st,"M-11a","ESC: full label text / variant, transcribed exactly","text","-","the label, sharp, all of it","Retires the on-hand identity ASSUMPTION. STOP if it is not QuicRun 10BL120 G2 Sensored — the measured 44.2x33.7x34.0 body belongs to another part.")
r(st,"M-11c","ESC: foot / mounting-tab centres and tab hole diameter","mm","±0.5","","esc_* install envelope; the OP-A relocation search. Record 'no tabs' if tape-mounted.")
r(st,"M-11d","ESC: which face each lead exits (battery in, 3 phase, signal) and each free length","mm + text","±2","the ESC with all leads laid out flat","KO-20 install envelope; N cable routing.")
r(st,"M-14b.1","MG90S: body L x W x H","mm (L x W x H)","±0.2","","Register-only (no parameter consumes it yet) — label the three numbers. STOP if it differs from documented TowerPro 22.8 x 12.2 x 28.5 by > 0.5: these are clones and every pocket is sized wrong.")
r(st,"M-14b.2","MG90S: mounting-ear pitch","mm","±0.2","","Pocket geometry.")
r(st,"M-14b.3","MG90S: ear hole diameter","mm","±0.2","","")
r(st,"M-14b.4","MG90S: boss height above the case","mm","±0.2","","")
r(st,"M-14b.5","MG90S: spline height and tooth COUNT","mm + count","±0.2","","Horn compatibility.")
r(st,"M-14b.6","MG90S: lead exit face","text","-","","Pocket orientation; DRS lead route.")
r(st,"M-14c","MG90S horn radii actually supplied, per hole, from the spline centre; and how many horns per servo","mm","±0.2","","DRS throw arithmetic with M-14d. If no horns came, M-14d/e/f cannot close.")
r(st,"M-14g1.1","Rod-end (M4 ball joint): ball diameter","mm","±0.2","","DRS + steering linkage.")
r(st,"M-14g1.2","Rod-end: thread size / pitch","text","-","","")
r(st,"M-14g1.3","Rod-end: ball-centre to thread-end distance","mm","±0.2","","Sets usable rod length with M-14g2.")
r(st,"M-18a.1","Speaker: cone diameter","mm","±0.2","","spk_* residual. NOTE: outline is already MEASURED 35.3 x 25.1 x 6.1 — the part is RECTANGULAR, not a round basket. Record the shape as found.")
r(st,"M-18a.2","Speaker: mounting-hole pattern and diameter","mm","±0.2","","PS-14 / KO-28 baffle.")
r(st,"M-18a.3","Speaker: total depth including the magnet","mm","±0.2","","Sidepod pocket depth.")
r(st,"M-23.1","Camera: PCB length","mm","±0.2","","Gate C / D-06 / D-34. No camera mount CAD until every M-23 row exists.")
r(st,"M-23.2","Camera: PCB width","mm","±0.2","","")
r(st,"M-23.3","Camera: PCB thickness","mm","±0.2","","")
r(st,"M-23.4","Camera: heatsink envelope L x W x H","mm (L x W x H)","±0.2","","Register-only — label the three numbers.")
r(st,"M-23.5","Camera: lens outside diameter","mm","±0.2","","Duct interface; FOV opening.")
r(st,"M-23.6","Camera: lens axial length","mm","±0.2","","")
r(st,"M-23.7","Camera: lens axis offset from the PCB centre (both axes)","mm","±0.2","","Boresight; KO-24.")
r(st,"M-23.8","Camera: mounting-hole pattern and diameter","mm","±0.2","","")
r(st,"M-23.9","Camera: cable-exit face and direction","text","-","","Service pull.")
r(st,"M-23.10","Camera: total axial depth, lens tip to heatsink back","mm","±0.2","camera identity photo + one square-on shot of the lens face","STOP if it disagrees with the owner ground truth 19.2 x 19.2 transverse x 30.7 axial by > 1 mm — the documented body reference is then the wrong unit.")
r(st,"M-24.1","Wi-Fi antenna: whip length","mm","±1","","KO-26 routing reserve. Expect ~70 mm.")
r(st,"M-24.2","Wi-Fi antenna: U.FL head body dimensions","mm","±1","","")
r(st,"M-24.3","Wi-Fi antenna: pigtail coax diameter","mm","±1","","")
r(st,"M-24.4","Wi-Fi antenna: minimum bend radius before the coax kinks","mm","±1","","KO-26 wants >= 10 mm coax bend.")
r(st,"M-25.1","FRONT shock: eye-to-eye length","mm","±0.5","","D-12 — resolves the 51 mm requirement vs 52 mm received-stock-label conflict. If it is neither, report both.")
r(st,"M-25.2","FRONT shock: body diameter","mm","±0.5","","KO-04 swept cylinder.")
r(st,"M-25.3","FRONT shock: fully compressed length","mm","±0.5","","Stroke = eye-to-eye minus this.")
r(st,"M-25.4","FRONT shock: spring OD and free length","mm","±0.5","","")
r(st,"M-25.5","REAR 68 mm shock: eye-to-eye length","mm","±0.5","","KO-06 — the central shock in the electronics spine.")
r(st,"M-25.6","REAR shock: body diameter","mm","±0.5","","")
r(st,"M-25.7","REAR shock: fully compressed length","mm","±0.5","","Feeds M-14h (swept arm vs shock at full compression).")
r(st,"M-25.8","REAR shock: spring OD and free length","mm","±0.5","","")
r(st,"M-26.1","Spur: tooth count","count","-","","D-16 / D-30.")
r(st,"M-26.2","Spur: outside diameter","mm","±0.2","","KO-08 / KO-21 guard.")
r(st,"M-26.3","Spur: bore diameter","mm","±0.1","","")
r(st,"M-26.4","Spur: bolt-hole PCD","mm","±0.1","","D-16 — must match the belt-set pulley.")
r(st,"M-26.5","Spur: bolt-hole diameter and count","mm + count","±0.1","spur and pulley faces side by side, bolt holes visible","STOP if the spur and pulley bolt patterns do not match: the drivetrain as bought cannot be assembled. Report before any rear print.")
r(st,"M-26.6","Belt-set pulley: tooth count","count","-","","")
r(st,"M-26.7","Belt-set pulley: outside diameter","mm","±0.2","","")
r(st,"M-26.8","Belt-set pulley: width","mm","±0.2","","Belt guard width.")
r(st,"M-26.9","Belt-set pulley: bore diameter","mm","±0.1","","")
r(st,"M-26.10","Belt-set pulley: bolt-hole PCD, diameter and count","mm + count","±0.1","","D-16 pair with M-26.4/.5.")
r(st,"M-26.11","Belt: width","mm","±0.2","","KO-21.")
r(st,"M-26.12","Belt: measured length (laid flat, pitch line)","mm","±1","","BOM says 140 mm — a length alone cannot establish the axes.")
r(st,"M-26.13","Pinion: tooth count","count","-","","")
r(st,"M-26.14","Pinion: outside diameter","mm","±0.2","","Mesh centre with the spur.")
r(st,"M-26.15","Pinion: bore diameter","mm","±0.1","","Motor shaft is 3.3 measured.")
r(st,"M-26.16","Rear output shaft: diameter","mm","±0.1","","")
r(st,"M-26.17","Rear output shaft: shoulder positions along its length","mm","±0.2","","Spacer stack.")
r(st,"M-27a.1","A3144 Hall: TO-92 body L x W x thickness","mm (L x W x T)","±0.2","","Register-only — label the three numbers. SNS-HALL envelope; PS-16 bracket.")
r(st,"M-27a.2","A3144: lead pitch","mm","±0.2","","")
r(st,"M-27a.3","A3144: lead length","mm","±0.5","","")
r(st,"M-27b","Neodymium magnet: diameter x thickness","-","-","","BLOCKED — magnets ordered / in transit. The 3 x 1 spec is CONFIRMED on paper only.")
r(st,"M-13","SP3T boot-mode selector: body, throw, panel cut-out, terminal projection","-","-","",NOSCAD+"BLOCKED — no switch selected or bought (owner shopping residue). sp3t_body_l/w/h and sp3t_cutout_l/w stay ASSUMED; five parameters cannot come from one cell, so they are re-cut into cells when a switch exists.")
r(st,"M-17a.1","ES24TX: variant — IS IT THE PRO?","text","-","the module's model marking","gcs_tx_*. The vendor 70 x 49 x 32.5 figure is valid ONLY if it is the Pro. A nano/Slim is RE-MEASURED, not scaled. Answer this cell BEFORE filling M-17a.2l/w/h.")
r(st,"M-17a.2l","ES24TX: body LENGTH (without antenna)","mm","±0.5","","gcs_tx_l.", param="gcs_tx_l")
r(st,"M-17a.2w","ES24TX: body WIDTH (without antenna)","mm","±0.5","","gcs_tx_w.", param="gcs_tx_w")
r(st,"M-17a.2h","ES24TX: body HEIGHT (without antenna)","mm","±0.5","","gcs_tx_h.", param="gcs_tx_h")
r(st,"M-17a.3","ES24TX: JR hook dimensions and which faces carry connectors","mm + text","±0.5","","Bulkhead panel is laid out from connector faces, not bodies.")
r(st,"M-17b.1l","FT232RL board: body LENGTH","mm","±0.5","","gcs_ftdi_l — no measurement exists anywhere in the workspace.", param="gcs_ftdi_l")
r(st,"M-17b.1w","FT232RL board: body WIDTH","mm","±0.5","","gcs_ftdi_w.", param="gcs_ftdi_w")
r(st,"M-17b.1h","FT232RL board: body HEIGHT","mm","±0.5","","gcs_ftdi_h.", param="gcs_ftdi_h")
r(st,"M-17b.2","FT232RL: connector faces","text","-","","Bulkhead layout.")
r(st,"M-17c.1","RT5370 dongle: body L x W x H with the USB shell","mm (L x W x H)","±0.5","",NOSCAD+"SPARE / 2.4 GHz fallback only. This does NOT retire gcs_wifi_* for the primary adapter, so it stays register-only however good the number is.")
r(st,"M-17d","Approved dual-band 5 GHz-AP-capable Wi-Fi adapter: body + connector faces","-","-","",NOSCAD+"BLOCKED — not procured. Top of the owner shopping residue; also gates the hotspot half of the Windows validation suite. gcs_wifi_l/w/h get their own cells when the adapter exists.")
r(st,"M-17e","USB hub: body + connector faces, cables seated","-","-","",NOSCAD+"BLOCKED — not procured. gcs_hub_l/w/h get their own cells when the hub exists.")

# ---------------- Station 2 ----------------
st = "2 — The scale (no power, no battery connected)"
r(st,"M-08a","ESP32 #1 with headers","g","±1","","CG ledger; replaces the DevKit-class ~9-10 g estimate.")
r(st,"M-08b","ESP32 #2 with headers","g","±1","","CG ledger.")
r(st,"M-08c","IP2326 charge module","g","±1","","CG ledger; ASM-59.")
r(st,"M-08d","XT90-S loop key + leads (mated pigtail pair)","g","±1","","CG ledger.")
r(st,"M-08e.1","MG90S #1","g","±1","","Documented 13.4 g is a genuine-TowerPro figure.")
r(st,"M-08e.2","MG90S #2","g","±1","","")
r(st,"M-08e.3","MG90S #3","g","±1","","")
r(st,"M-08f","Camera assembly as it will install","g","±1","","KO-24 / gimbal load.")
r(st,"M-08g","PDB, assembled","-","-","","BLOCKED — not built (see M-06). The ~50 g is a TARGET.")
r(st,"M-08h","Cassette assembly","-","-","","BLOCKED — does not exist; nothing in 11_cad/ has been printed.")
r(st,"M-08i","Pedestal","-","-","","BLOCKED — does not exist.")
r(st,"M-08j","ZEEE 5200 bench-only pack, bagged, on the scale","g","±1","","Retires an explicit ASSUMED (~250-300 g). NOT a car pack (138x47x37 vs <=75x45x25) — bench handling only, keep it out of any car CG ledger.")
r(st,"M-09","Four-corner weights, rolling assembly","-","-","","BLOCKED TWICE — no rolling assembly, and tyres are in transit. NO balance claim and NO ballast cut until this table exists.")

# ---------------- Station 3 ----------------
st = "3 — Car, shell off (gated by M-00)"
for fid, coord, what in [
    ("1","X +7.50, L 0","splice screw"),
    ("2","X +14.26, L 0","splice screw"),
    ("3","X +22.69, L 0","splice screw"),
    ("4","X -27.76, L -13.50","rear bracket"),
    ("5","X -27.76, L +16.50","rear bracket"),
    ("6","X -39.99, L -32.86","free single (belt side)"),
    ("7","X -39.94, L +17.14","free single (mirror side)"),
    ("8","X +57.50, L 0","centreline pedestal candidate"),
    ("9","X +64.24, L 0","centreline pedestal candidate")]:
    r(st, f"M-20.{fid}", f"{what} at {coord}: FREE or OCCUPIED — try an actual M3 screw, do not judge by eye; if occupied, by what",
      "free/occupied + text","-","one photo per OCCUPIED feature showing what occupies it",
      "Coordinates are the car frame defined at the top of the runbook (X + toward the nose; L- = BELT side, L+ = MIRROR side). D-27 stage 2. Splice screws are OP-G's only anchors inside the cassette footprint; X+57.50/+64.24 are the pedestal's only anchors. Occupied = those ideas die here, which is cheaper than finding out with a printed part in hand. NO new holes in donor parts.")
r(st,"M-28.1","Servoholder PRINTED arch: clear opening length","mm","±0.2","","Mesh figure is 42.0. Servo face measured 40.25 -> ~1.75 mm clearance.")
r(st,"M-28.2","Servoholder PRINTED arch: clear opening height","mm","±0.2","","Mesh figure is 18.5. Servo face measured 20.2 -> ~1.7 mm INTERFERENCE, as predicted.")
r(st,"M-28.3","Does the DS3235SG enter side-on WITHOUT FORCE?","pass/fail","-","the servo offered to the arch, plus a close-up of the binding point","STOP if it binds. Do not file, force or heat. A test-grade print can bind from layer swell alone; the fix is production tolerance or a measured CAD relief. OP-B / Gate D residual — this gates the whole floor print batch.")
r(st,"M-28.4","If it binds: exactly WHERE","text","-","","The location is the CAD input.")
r(st,"M-28.5","Shaft-centre orientation used (boss-forward X-46.76 vs reversed X-66.76)","text","-","","Still unpinned; record which you used.")
r(st,"M-29.1","Steering Block4 king-pin bore diameter, side 1","mm","±0.1","","D-05; M3x30 dowel fit. Outside 3.0 +0.15/-0.05 = a reprint tolerance change, decided in CAD.")
r(st,"M-29.2","Steering Block4 king-pin bore diameter, side 2","mm","±0.1","","D-05.")
r(st,"M-30.1","Front hub (original RIGHT): bearing seat diameter for 8x12x3.5","mm","±0.1","","D-22 baseline.")
r(st,"M-30.2","Front hub (Bambu-MIRRORED left): bearing seat diameter","mm","±0.1","","D-22 — the left hub exists only as a mirror. Off by > 0.1 = tolerance pass before the wheel print.")
M02_GATE = ("PRECONDITION: M-02a-e need the FRONT END ASSEMBLED — steering blocks, king pins, rod ends and front "
            "shocks fitted — and the chassis blocked up on the floor pan so the wheels hang free and the suspension "
            "is unloaded. If it is not, write 'could not — front end not assembled'. DO NOT sweep a partly-assembled rod. ")
for sid, station in [("1","forward, X ~ +40"),("2","middle, X ~ 0"),("3","rear, X ~ -40")]:
    r(st, f"M-02a.{sid}", f"Steering rod LOWEST Z at {station}, swept lock-to-lock and through bump (datum DAT-F)",
      "mm","±2","both locks, photographed from the same place",
      M02_GATE+NOSCAD+"Feeds M-02a.min. Provisional band is Z 22..38 at |L| <= 22, with the PDB 8.00 mm below it and ZERO reserve.")
r(st,"M-02a.min","LOWEST Z of the three M-02a readings = min(M-02a.1, M-02a.2, M-02a.3). Write the arithmetic","mm","±2","","ko01_z_lo — the single defining cell. One row per parameter: the three station readings above are register-only.", param="ko01_z_lo")
for sid, station in [("1","forward, X ~ +40"),("2","middle, X ~ 0"),("3","rear, X ~ -40")]:
    r(st, f"M-02b.{sid}", f"Steering rod HIGHEST Z at {station}", "mm","±2","",M02_GATE+NOSCAD+"Feeds M-02b.max.")
r(st,"M-02b.max","HIGHEST Z of the three M-02b readings = max(M-02b.1, M-02b.2, M-02b.3)","mm","±2","","ko01_z_hi — the single defining cell.", param="ko01_z_hi")
for sid, station in [("1","forward, X ~ +40"),("2","middle, X ~ 0"),("3","rear, X ~ -40")]:
    r(st, f"M-02c.{sid}", f"Max |L| the rod reaches at {station}", "mm","±2","",M02_GATE+NOSCAD+"Feeds M-02c.max.")
r(st,"M-02c.max","GREATEST |L| of the three M-02c readings = max(M-02c.1, M-02c.2, M-02c.3)","mm","±2","","ko01_l_half — the single defining cell.", param="ko01_l_half")
r(st,"M-02d.1","Most FORWARD X reached by any swept point of the rod (+X is toward the nose)","mm","±2","",M02_GATE+"ko01_x_hi. NEW ROW: section 9 lists ko01_x_lo/x_hi under M-02 but the prompt's M-02 table has no cell for them.", param="ko01_x_hi")
r(st,"M-02d.2","Most REARWARD X reached by any swept point of the rod","mm","±2","",M02_GATE+"ko01_x_lo. Same note. EXPECT A NEGATIVE NUMBER (a rearward point is a NEGATIVE X; provisional ko01_x_lo = -80 at w17_params.scad:94) — do not write it positive. Nothing in 11_cad/ consumes ko01_x_lo yet: no geometry and no assert reads it, so this row only retires the §9 record, it does not change any rendered part.", param="ko01_x_lo")
r(st,"M-02e","Does anything ALREADY FITTED enter that envelope? List every item and where","text","-","anything found inside the envelope",M02_GATE+"KO-01 / KO-11 / KO-36. STOP-READ: measured z_lo < 22 or l_half > 22 shrinks the guard band (ko01_z_guard 14, ko01_l_guard 30) and drives the PDB's already-negative-by-5mm gap further negative. Report; do not re-derive the cage at the bench.")

# ---------------- Station 4 ----------------
st = "4 — Car, shell seated (gated by M-00; needs the shell)"
for pid, where in [("1","forward, BELT side (L-)"),("2","forward, MIRROR side (L+)"),
                   ("3","rear, BELT side (L-)"),("4","rear, MIRROR side (L+)"),
                   ("5","OPTIONAL: over the cassette, either side")]:
    r(st, f"M-01.{pid}", f"S0 — shell bottom edge above floor top (DAT-F) at: {where}. Shell seated and only LIGHTLY pressed",
      "mm","±0.5","the gauge in place at one point, showing the seating",
      NOSCAD+"Feeds M-01.worst and M-01.6. Coupon C-4 steps run 2..11 mm: read the tallest step that still passes; below the 2 mm step, write 'below the lowest step' — a real and serious answer. Record ALL readings, not the smallest.")
r(st,"M-01.worst","S0 WORST (smallest) of the M-01 readings. Write which point it came from","mm","±0.5","","s0_measured — the single defining cell. The cage's gate is the WORST point, not an average. STOP if < 9.82: do NOT shave the cage; reopen board orientation (a production stop ZK already demands).", param="s0_measured")
r(st,"M-01.6","S0 SPREAD = max reading minus min reading (derived at the bench)","mm","±0.5","",NOSCAD+"STOP-READ: S0 is bounded 0..~11. > 11 = re-check the datum. Spread > 1.0 = the shell does not sit flat, a DIFFERENT problem from sitting low, and the cage cares about both.")
for sid, x in [("1","X +3"),("2","X +20"),("3","X +42")]:
    r(st, f"M-07.{sid}b", f"Clear height above DAT-F at {x}, BELT side (L-), across |L| 27..46, shell seated","mm","±1","",
      NOSCAD+"Feeds M-07.worst. This is a SHELL-INTERIOR CLEAR HEIGHT, not guide_top_z.")
for sid, x in [("1","X +3"),("2","X +20"),("3","X +42")]:
    r(st, f"M-07.{sid}m", f"Clear height above DAT-F at {x}, MIRROR side (L+), across |L| 27..46, shell seated","mm","±1","",
      NOSCAD+"Feeds M-07.worst. The WORST value must agree with M-01 plus the modelled roof (27.18 at X+3 / L-37). If it does not, ONE OF THE TWO IS WRONG — say which you trust and why, at the bench.")
r(st,"M-07.worst","WORST (smallest) of the six M-07 clear heights. Write which cell it came from","mm","±1","",
  NOSCAD+"This is the BOUND on the aft end guide, NOT guide_top_z itself. guide_top_z (30.0) is a cage DESIGN OUTPUT constrained by assert(guide_top_z <= board_top_z) with board_top_z = 32.0 (w17_params.scad:149,201,397); a clear height read under a seated shell is ~S0 + roof and will normally exceed 32, so entering it directly would fire that assert for the wrong reason. Report this number; guide_top_z is set in CAD from it, and guide_top_margin (DERIVED = board_top_z - guide_top_z, w17_params.scad:202) MUST be recomputed in the same edit.")
for sid in ["1","2","3"]:
    r(st, f"M-11e.{sid}", f"ESC candidate station {sid}: where it is (X, L) and how much OPEN AIR is above the fan intake, body seated",
      "mm + coords","±0.5", "the candidate with the ESC dry-placed (not fixed)",
      "OP-A / KO-20 / CAS-06. Policy wants 10 mm above the fan = a plane at Z 45.5 with the measured 34.0 body, and NO registered shell station supplies it even at S0 = 11. This row is looking for a home, not confirming one. If none of the three works, say so; the decision is the owner's.")
M12_SCOPE = "SCOPE: M-12 is taken on the SHELL, with the side-vent part REMOVED. M-15 is taken on the vent PART, in hand. They are not the same opening measured twice. "
r(st,"M-12.1","CF-1 (side vent aperture in the shell, vent part removed): shell wall thickness","mm","±0.5","",M12_SCOPE+"flap_wall.", param="flap_wall")
r(st,"M-12.2w","CF-1: clear opening WIDTH of the existing shell aperture","mm","±0.5","",M12_SCOPE+"flap_open_w (16.0 ASSUMED). NEW CELL — M-12 previously asked only for wall thickness and depth, so the two opening parameters it is supposed to retire had no cell.", param="flap_open_w")
r(st,"M-12.2h","CF-1: clear opening HEIGHT of the existing shell aperture","mm","±0.5","",M12_SCOPE+"flap_open_h (11.0 ASSUMED). NEW CELL, same reason.", param="flap_open_h")
r(st,"M-12.2d","CF-1: local depth behind the shell inner face","mm","±0.5","",M12_SCOPE+NOSCAD+"Charge-cell depth budget behind the flap.")
r(st,"M-12.3","CF-1: what is behind it","text","-","behind the candidate",M12_SCOPE+"OP-F.")
r(st,"M-12.4","CF-2 (floor opening at X +39.18, |L| 55.71): wall thickness","mm","±0.5","",NOSCAD+"CF-2 is the alternative candidate; only the chosen one sets flap_*.")
r(st,"M-12.5","CF-2: local depth behind","mm","±0.5","",NOSCAD+"")
r(st,"M-12.6","CF-2: what is behind it","text","-","behind the candidate","NO CUT IS AUTHORISED BY THIS ROW. It exists so the CF-1/CF-2 decision is made against numbers instead of preference; the shell stays unmodified.")
r(st,"M-15.1w","Side-vent PART in hand: clear opening WIDTH","mm","±0.2","",M12_SCOPE+"vent_w. WARNING: the 13.1 currently in w17_params.scad is the FLOOR SLOT, not the shell vent. Nobody has measured the vent.", param="vent_w")
r(st,"M-15.1h","Side-vent PART in hand: clear opening HEIGHT","mm","±0.2","",M12_SCOPE+"vent_h. Same warning: 10.3 is the floor slot.", param="vent_h")
r(st,"M-15.1d","Side-vent PART: internal depth","mm","±0.2","",M12_SCOPE+NOSCAD+"Insert depth available for a reversible flap.")
r(st,"M-15.2","Side-vent PART: how it mounts to the shell","text","-","","CF-1 reversibility.")
r(st,"M-15.3","Side-vent PART: visible face dimensions","mm","±0.2","",NOSCAD+"Cosmetic cost of an integrated flap.")
r(st,"M-10","Tyre arch clearance at full steer / full bump / both, four corners, body on","-","-","","BLOCKED — Tamiya tyres in transit. Registered margins are 3.5 and 4 mm, ALREADY below policy (E-30): this row is looking for a problem that is probably there.")

# ---------------- Station 5 ----------------
st = "5 — Car, rear end (gated by M-00). Never test the pocket alone"
r(st,"M-14a.1","Wing DRS pocket: internal length (datum: pocket floor)","mm","±0.2","","STOP if the MG90S will not enter without distorting the pocket.")
r(st,"M-14a.2","Wing DRS pocket: internal width","mm","±0.2","","")
r(st,"M-14a.3","Wing DRS pocket: internal height","mm","±0.2","","")
r(st,"M-14a.4","Wing DRS pocket: wall thickness","mm","±0.2","","")
r(st,"M-14d.1","DRS arm: PIVOT-TO-PIVOT spacing (hole centre to hole centre)","mm","±0.2","the arm with the caliper across the two pivots",NOSCAD+"drs_arm_pivot_span is deliberately undef with assert(is_undef(...)) at w17_params.scad:405 that fires if anyone gives it a value. THIS ROW IS THE ONLY THING THAT MAY SET IT, and setting it is an explicit CAD edit that removes the assert — never a tool patch. The 58 mm in the inventory is a RAW BOUNDING BOX, not a pivot span.")
r(st,"M-14d.2","DRS arm: driving hole diameter","mm","±0.2","","")
r(st,"M-14d.3","DRS arm: driven hole diameter","mm","±0.2","","")
r(st,"M-14e.1","Flap hinge axis position (datum: hinge line, referenced to the wing datum)","mm","±0.5","","Four-bar geometry.")
r(st,"M-14e.2","Perpendicular distance, hinge axis to the arm's driven pivot","mm","±0.5","","Four-bar geometry.")
r(st,"M-14f.1","Flap CLOSED angle wanted (chord vs wing datum)","deg","±2","","DRS throw.")
r(st,"M-14f.2","Flap OPEN angle wanted","deg","±2","","DRS throw.")
r(st,"M-14g2","Rod length required between rod-end centres","mm","±0.2","","STOP if the linkage PRELOADS the flap at either end.")
r(st,"M-14h.1","Nearest approach of the swept arm to the 68 mm shock AT FULL COMPRESSION","mm","±1","","KO-25 wants >= 8 mm. The wing sits directly above the shock's territory.")
r(st,"M-14h.2","Nearest approach of the swept arm to the LED tail","mm","±1","","KO-25 / KO-29.")
r(st,"M-14h.3","Nearest approach of the swept arm to the body inner","mm","±1","","KO-25.")
r(st,"M-14i","Servo neutral orientation that puts the rod straight at flap-closed: mark horn and case","text","-","the horn at neutral, mark visible","STOP if a WIRE becomes the hard stop, an ear needs drilling, or the horn hits the wing.")
r(st,"M-18b","Sidepod port aperture you actually want (datum: vent face)","mm","±0.2","","spk_port_d (22.0 ASSUMED). This is a DECISION recorded as a number, not a discovered measurement — write down what you chose and why.", param="spk_port_d")
r(st,"M-19a.1","Hall carrier surface at the rear axle: what the sensor can be mounted to","text","-","the candidate surface with the sensor offered to it","PS-16 / D-38. If no carrier surface exists, the bracket becomes a new part.")
r(st,"M-19a.2","Hall carrier surface: its extent (L x W)","mm","±0.5","","")
r(st,"M-19a.3","Hall carrier surface: distance to the axle centreline","mm","±0.5","","")
r(st,"M-19b","Collar runout — how much the magnet face moves per revolution","-","-","","BLOCKED — magnets in transit. Use a NON-MAGNETIC gauge when it runs.")
r(st,"M-19c","Sensor-to-magnet gap actually achievable (target 1.5 inside a 1-3 mm band)","-","-","","BLOCKED — magnets in transit, so this cell stays EMPTY and hall_gap stays ASSUMED. NON-MAGNETIC gauge only: a steel gauge next to a Hall sensor and a magnet tells you about the gauge.", param="hall_gap")
r(st,"M-19d","Can the Hall lead be routed AWAY from the ESC and motor phase leads (no parallel run, 90 deg crossing if it must cross) and kept short with its pull-up near the board?","pass/fail","-","the intended route","GPIO35's interrupt has NO RATE BOUND and GPIO34-39 have NO internal pull-ups: a noisy Hall line CANNOT be rescued in software. FAIL = a design problem to report now, not a wiring-day problem.")

# ---------------- write ----------------
HEADER = ["id","param","quantity","unit","value","tolerance","photo_ref","notes"]

# One row per parameter is an invariant of the sheet, not a hope: fail loudly.
seen = {}
for st_, i, q, u, tol, photo, notes, param in S:
    if param:
        if param in seen:
            raise SystemExit(f"ERROR: '{param}' is targeted by both {seen[param]} and {i}; "
                             f"the ingest tool would drop both. One row per parameter.")
        seen[param] = i

csv_path = os.path.join(REPO, "MEASUREMENT_RECORD_SHEET.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(HEADER)
    for st_, i, q, u, tol, photo, notes, param in S:
        n = notes
        if photo:
            n = f"PHOTO REQUIRED — {photo}. {notes}".strip()
        w.writerow([i, param, q, u, "", tol, "", n])

md_path = os.path.join(REPO, "MEASUREMENT_RECORD_SHEET.md")
with open(md_path, "w") as f:
    f.write("""# Measurement record sheet — print this

**Sitting date: ____________  ·  Instrument (calipers, make/model): ____________________  ·  Scale: ____________________  ·  Recorded by: ____________**

**No power. No battery. No USB into a live port. Nothing forced, cut, drilled, filed or glued.**
**A2 stays NOT-EXECUTED and Phase B stays BLOCKED whatever the numbers say.**

Order, rationale, and the **coordinate/side definitions** every `X`, `L`, `Z`, `DAT-F`,
belt/mirror and outboard reference below depends on:
[`MEASUREMENT_SITTING_RUNBOOK.md`](MEASUREMENT_SITTING_RUNBOOK.md) — read its
"Coordinates, datums and sides" block **before** you write a signed number.
Machine-readable twin: [`MEASUREMENT_RECORD_SHEET.csv`](MEASUREMENT_RECORD_SHEET.csv) —
**both files are generated by `tools/gen_measurement_sheet.py` from one row list, so they
cannot drift. Never hand-edit either sheet.**

**A measurement you could not take is a result:** write `could not — <why>` in the Value box.
Never estimate to fill a cell. Photo refs are filenames under
`08_reference_photos/YYYY-MM-DD_<what>.jpg`.

**The `param` line under each cell** names the exact `11_cad/w17_params.scad` parameter that
cell sets, and is what `11_cad/tools/ingest_measurements.py` reads. **`param: (register-only)`
means the number is a record, not a parameter — do not enter it into `w17_params.scad`.**
Most often that is because the cell holds a *stock* dimension (a screw's thread, an insert's
knurl, a cable tie's strap) while the parameter is the *feature* that part must fit through
— which is stock **plus clearance**, a CAD decision.

""")
    last = None
    for st_, i, q, u, tol, photo, notes, param in S:
        if st_ != last:
            f.write(f"\n---\n\n## Station {st_}\n\n")
            last = st_
        f.write(f"### {i} — {q}\n\n")
        f.write(f"- **Unit:** {u}  ·  **Tolerance:** {tol}  ·  **param:** "
                f"{'`'+param+'`' if param else '(register-only)'}\n")
        f.write(f"- **Value:** `______________________`\n")
        if photo:
            f.write(f"- **PHOTO REQUIRED** — must show: {photo}.  **Photo ref:** `______________`\n")
        else:
            f.write(f"- **Photo ref (optional):** `______________`\n")
        if notes:
            f.write(f"- {notes}\n")
        f.write("\n")
    f.write(f"\n---\n\n**{len(S)} rows, of which {len(seen)} carry a `param`.** "
            "Transcribe into `w17-mechanical-measurement-session-prompt.md` (the record), "
            "then `11_cad/w17_params.scad` (value **and** tag **and** delete the §9 entry) — or let "
            "`11_cad/tools/ingest_measurements.py --sheet MEASUREMENT_RECORD_SHEET.csv` build that patch "
            "for review — then §12 of "
            "`10_assembly_architecture/AA_electronics_placement_study.md`. Then run `11_cad/render.sh` — "
            "**if an `assert()` fires, that is the sitting's most valuable output.**\n")

print(f"{len(S)} rows ({len(seen)} with a param) -> {csv_path}, {md_path}")
