#!/usr/bin/env python3
"""Generate 01_inventory/inventory.csv for w17-3d-codex.

Read-only over unsorted_stl_raw/. Computes size, sha256, and for STLs the
triangle count + authored-frame bounding box. Joins with an explicit
per-file decision map. Unmatched model files are flagged loudly.
"""
import csv, hashlib, os, struct, sys

ROOT = "/Users/vitaliykhomenko/Documents/projects/w17-3d-codex"
RAW = os.path.join(ROOT, "unsorted_stl_raw")
OUT = os.path.join(ROOT, "01_inventory", "inventory.csv")

# ---------- decision tiers ----------
REQ = "REQUIRED"
OPT = "OPTIONAL"
UNC = "UNCERTAIN"
RJL = "REJECTED_LIVERY"          # wrong team/era body or aero
RJC = "REJECTED_WRONG_CHASSIS"   # revision/ball-joint parts we don't run
RJS = "REJECTED_SUPERSEDED"      # older version of a part we print differently
DUP = "DUPLICATE"                # identical file at a non-canonical path
REF = "REFERENCE"                # not printable: pdf/jpg/txt/ipt/3mf sources

# group, material
G02 = ("02_ASA_rear_drivetrain", "ASA black")
G03 = ("03_PETG_front_suspension_steering", "PETG")
G04 = ("04_PETG_wheels", "PETG")
G05 = ("05_PETG_floor", "PETG")
G06 = ("06_PLA_body_shell", "PLA matte black")
G07 = ("07_translucent_diffuser", "PLA white-transparent")

# basename -> (tier, group, material, uncertainty, note, human_check)
D = {}

def add(names, tier, grp=("", ""), unc="low", note="", check=""):
    for n in names:
        D[n] = (tier, grp[0], grp[1], unc, note, check)

# ---- REQUIRED: 02 ASA rear drivetrain (9) ----
add(["Leftrearaxle.stl", "Rightrearaxle.stl", "beltdrivemotorlock.stl",
     "newgearmotorlock.stl"], REQ, G02, "low",
    "Rear axle holder / motor lock: motor heat + torque; 100% rectilinear")
add(["Left Spacer for long axle.stl", "Right Spacer for long axle.stl",
     "NewSpacerleft.stl", "NewSpacerright.stl"], REQ, G02, "medium",
    "Rear axle spacer; rides inside 14mm metal sleeves",
    "verify which spacer pairing the long axle actually needs at assembly")
add(["Axle Main no grubs.stl"], REQ, G02, "medium",
    "Believed rear axle main (no grub screws variant)",
    "confirm role against drawing [7] before printing")

# ---- REQUIRED: 03 PETG front suspension/steering (8) ----
add(["2023WheelHubsSuspension5.stl", "2023WheelHubsSuspension5mir.stl",
     "Arm4.stl", "Crossarm3_extended.stl", "GuideRod.stl",
     "Steering Block4.stl", "Suspension Block_10.stl"], REQ, G03, "low",
    "Original oil-shock front part (locked config)")
add(["servosaverv7.stl"], REQ, G03, "low",
    "Servo saver; STL contains multiple bodies - import once, do not duplicate")

# ---- REQUIRED: 04 PETG wheels (7) ----
add(["Front_Rim_F1_2022.stl", "Rear_Rim_F1_2022.stl",
     "Front_Locking_Nut_F1_2022.stl", "Rear_Locking_Nut_F1_2022.stl"],
    REQ, G04, "low", "Printed rim set (Thingiverse 5414118); qty 2 each final")
add(["Front_Right_Wheel_Hub_2022_F104.stl"], REQ, G04, "low",
    "Only RIGHT hub exists - mirror in Bambu Studio for the left",
    "verify mirrored copy bearing seat 8x12x3.5 too")
add(["F104 tyreslot1 no grubs tighter.stl", "F104 tyreslot2 no grubs tighter.stl"],
    REQ, G04, "medium", "Tighter Rev1.1 rear tyre-slot adapters (wanted versions)",
    "final quantity unproven (1 or 2 each) - confirm one per side at assembly; watch for heat-softening near axle, ASA fallback if it deforms")

# ---- REQUIRED: 05 PETG floor (7) ----
add(["2023NewBackFloorLargerPart2.stl", "2023NewBackFloorLargerParts.stl",
     "2023NewFrontFloorLargerParts.stl", "Diffuser.stl", "FloorBoard2.stl"],
    REQ, G05, "medium", "Original floor set (NOT Revision 1.1 front floor)",
    "cross-check against drawing [2] FLOOR ASSEMBLY that no floor piece is missing")
add(["2023NEWSideVent1.stl", "2023NEWSideVent2.stl"], REQ, G05, "medium",
    "Floor side vents; SideVent1 STL contains multiple bodies - import once",
    "cross-check against drawing [2]")

# ---- REQUIRED: 06 PLA body (5) ----
add(["NEW BODY 2024 FRONT 1.stl", "NEW BODY 2024 REAR.stl",
     "NEW BODY 2024 Mirror.stl", "new halo 2.1.stl"], REQ, G06, "low",
    "Generic 2024 body shell, painted W17; 0.12-0.16mm layers")
add(["camera top 1.1.stl"], REQ, G06, "low",
    "Revised camera-top pod (holds FPV camera)")

# ---- REQUIRED: 07 diffuser (1) ----
add(["rearbacklightdiffuser.stl"], REQ, G07, "low",
    "Brake-light diffuser with WS2812 hole; 1-2 walls over lens, lens NEVER painted")

# ---- OPTIONAL (5) ----
add(["fulldrivercut2.stl"], OPT, ("optional", "PLA"), "low",
    "Cosmetic driver figure (50MB, 1M triangles) - long print, display only")
add(["Fullhelm2.stl"], OPT, ("optional", "PLA"), "low", "Cosmetic driver helmet")
add(["wall mount.stl"], OPT, ("optional", "any"), "low", "Wall display mount for the car")
add(["sharkfinnew2.stl"], OPT, ("optional", "PLA"), "medium",
    "Sharkfin (modern style); 1.9mm thin - fragile, cosmetic",
    "confirm the 2024 body wants a separate sharkfin at all")
add(["sidewingdeco.stl"], OPT, ("optional", "PLA"), "medium",
    "Side wing decoration; 1mm thin", "confirm fitment on 2024 body")

# ---- UNCERTAIN (rocker gate) ----
rocker_check = "GATE: confirm Spring mount 2 REVISION 1 seats the 68mm coilover in slicer; fits -> hybrid rocker path, else original mount and skip REV4/springblock"
add(["Spring mount 2 REVISION 1.stl", "Spring Block.stl"], UNC,
    ("pending_rear_gate", "ASA if selected"), "high",
    "Hybrid rocker candidate for 68mm rear shock", rocker_check)
add(["RearSpringMountREV4.stl", "springblock.stl"], UNC,
    ("pending_rear_gate", "ASA if selected"), "high",
    "Revision spring-rear mount - only if rocker does NOT fit", rocker_check)
add(["Rear Back Motor Cover REVISION 1.stl", "Rear Left Motor Cover REVISION 1.stl",
     "Rear Right Motor Cover REVISION 1.stl"], UNC,
    ("pending_rear_gate", "ASA if selected"), "medium",
    "Revised motor covers - only valid with the hybrid rocker path", rocker_check)
add(["Diffuser backplate.stl"], UNC, ("pending_rear_gate", "ASA or PETG"), "medium",
    "NOT the brake-light diffuser", "verify whether chosen rear assembly needs it (drawing [7])")

# ---- UNCERTAIN (body completeness) ----
body_check = "open NEW BODY 2024 FRONT 1 in slicer: is nose/front wing integrated? If not, this part is needed (and is the silver-nose piece -> print white/grey)"
add(["FRONTNOSE2024.stl"], UNC, ("pending_body_check", "PLA white/grey"), "medium",
    "2024 nose; likely the separate silver-nose piece the build sheet mentions", body_check)
add(["2024 Revised Front Wing.stl"], UNC, ("pending_body_check", "PLA"), "medium",
    "2024 front wing - unclear if 2024 body includes one", body_check)
add(["pin.stl"], UNC, ("pending_body_check", "PLA or PETG"), "low",
    "Body mounting pin", "check if 2024 body (M3 bolts) still uses pins")

# ---- UNCERTAIN (camera/duct - wait for measurements) ----
cam_check = "GATE: measure real camera + ACP2006 blower before choosing/rendering"
add(["camera_blower_duct.scad"], UNC, ("pending_camera", "PETG"), "high",
    "Parametric OpenSCAD duct - SOURCE, not sliceable; render STL after measuring", cam_check)
add(["cameranose.stl", "camera 2 colour.stl", "f104camera.stl"], UNC,
    ("pending_camera", "PETG or PLA"), "low",
    "Dummy/alternative camera pod - probably unneeded (camera top 1.1 selected)", cam_check)
add(["Servoholder.stl"], UNC, ("pending_fit", "PETG"), "low",
    "Original servo holder", "check against drawing [3] whether oil-shock front uses it or the servo mounts differently")

# ---- REJECTED: wrong livery / era aero ----
add(["NEW BODY 2024 FRONT 1 SF24.stl", "NEW BODY 2024 REAR SF24.stl",
     "NewFrontNose SF24.stl"], RJL, note="Ferrari SF24 shell - we paint W17 on generic 2024")
add(["FRONT BODY BLACK.stl", "FRONT BODY MULTICOLOUR.stl", "FRONT BODY ORANGE 1.stl",
     "FRONT BODY ORANGE 2.stl", "FRONT BODY ORANGE 3.stl", "FRONT WING MCL38 ORANGE 1.stl",
     "FRONTNOSE BLACK.stl", "FRONTNOSE MULTICOLOUR.stl", "FRONTNOSE ORANGE.stl",
     "NEW BODY 2024 REAR BLACK.stl", "NEW BODY 2024 REAR ORANGE 1.stl",
     "NEW BODY 2024 REAR ORANGE 2.stl", "NEW BODY 2024 REAR ORANGE 3.stl",
     "NEW BODY 2024 REAR ORANGE 4.stl"], RJL, note="McLaren MCL38 colour-split shell")
add(["MCL60 2023 Rear Wing.stl"], RJL, note="McLaren MCL60 2023 wing")
add(["FRONTNOSE2021.stl", "NewFrontNose2021_3.stl", "2021 front wing wing.stl",
     "2021Rearwing with DRS.stl", "2021 front wing sides.stl",
     "2021Rearwingflapdeco.stl", "2021deco.stl", "sharkfinnew2021.stl",
     "2021sidevent2.stl"], RJL, note="2021-era body/aero")
add(["2023 Front Wingsplit.stl", "2023WINGDECO.stl", "2023WINGDECO2.stl",
     "2023WINGDECO3.stl", "2023 Top Body RB19.stl", "2023 Top Body2.stl",
     "2023NewSidepodsopen.stl", "FRONTNOSE2023tighterpins.stl",
     "LargerturningvaneLeft.stl", "LargerturningvaneRight.stl"], RJL,
    note="2023-era body/aero (2023 top-body chassis line, not our 2024 shell)")
add(["sf23topbody.stl", "sf23horn.stl", "sf23sharkfin.stl", "cameratopsf23.stl",
     "pinsf23.stl"], RJL, note="Ferrari SF23 variant")

# ---- REJECTED: wrong chassis (Revision 1 / 1.1 front we don't run) ----
add(["New Left Wheel Hub.stl", "New Right Wheel Hub.stl",
     "New Steering Arm with Ball Joint Left.stl",
     "New Steering Arm with Ball Joint Right.stl",
     "New Steering Servo Holder.stl",
     "NewFrontFloorSuspensionUpgrade REVISION_1.1.stl"], RJC,
    note="Rev 1.1 ball-joint steering - incompatible with locked oil-shock front")
add(["ARM1 extended.stl", "ARM1 extended bottom.stl", "ARM1 extended bottom Left.stl",
     "ARM1 extended bottom Right.stl", "Armblock.stl", "Servomount for steering.stl",
     "Servomount for steering bottom.stl", "Steering Arm 1.stl",
     "Steering Block 12x5x3 Bearings .stl"], RJC,
    note="Revision-1 front axle upgrade set - locked config uses original front")
add(["NewFrontFloorSuspensionUpgrade REVISION 1.stl",
     "NewBackFloorSuspension UpgradeBack REVISION 1.stl",
     "NewBackFloorSuspension UpgradeFront3 REVISION 1.stl"], RJC,
    note="Revision-1 suspension floor - locked config uses original floor")

# ---- REJECTED: superseded ----
add(["F104 tyreslot1 no grubs.stl", "F104 tyreslot2 no grubs.stl"], RJS,
    note="Superseded by the 'tighter' Rev1.1 adapters")
add(["RCRNewRearCover rev1.stl", "NewRearCovertighterholes.stl"], RJS,
    note="Old rear covers - 2024 REAR shell replaces them")
add(["2024 halo.stl"], RJS, note="Superseded by new halo 2.1")
add(["cameratop.stl"], RJS, note="Superseded by camera top 1.1")
add(["Mirrors 2024.stl"], RJS, note="Superseded by NEW BODY 2024 Mirror")
add(["Newinvaxle2full.stl", "newinvaxleextended.stl"], RJS,
    note="Old invert-axle parts - belt-drive rear uses Left/Rightrearaxle")
add(["Print_In_Place DRSv2.stl", "DRS Diffuser.stl",
     "DRS Arm for 2021 Rear Wing.stl", "DRS Arm for 2023 Rear Wing.stl"], RJS,
    note="DRS system - dropped from v2 build (no DRS in locked config)")

# ---- REFERENCE (non-printable) ----
add(["Leftrearaxle.3mf"], REF, note="Alternate format of selected Leftrearaxle.stl - use the STL")
add(["2024 Revised Front Wing.ipt", "FRONTNOSE2024.ipt", "FRONTNOSE2024.0002.ipt",
     "Diffuser backplate.ipt", "beltdrivemotorlock.ipt"], REF,
    note="Autodesk Inventor CAD source")

# canonical-path substrings for basenames that exist at >1 path
CANON = {
    "Axle Main no grubs.stl": "Original + Revision 1",
    "Diffuser backplate.stl": "Original + Revision 1",
    "Diffuser backplate.ipt": "Original + Revision 1",
    "Rear Back Motor Cover REVISION 1.stl": "Original + Revision 1",
    "Rear Left Motor Cover REVISION 1.stl": "Original + Revision 1",
    "Rear Right Motor Cover REVISION 1.stl": "Original + Revision 1",
    "Spring Block.stl": "Original + Revision 1",
    "Spring mount 2 REVISION 1.stl": "Original + Revision 1",
    "rearbacklightdiffuser.stl": "Original + Revision 1",
    "fulldrivercut2.stl": "Original + Revision 1",
    "wall mount.stl": "Original + Revision 1",
    "MCL60 2023 Rear Wing.stl": "Original + Revision 1",
    "2024 Revised Front Wing.stl": "Original + Revision 1",
    "ARM1 extended.stl": "Original + Revision 1",
    "Armblock.stl": "Original + Revision 1",
    "NewFrontFloorSuspensionUpgrade REVISION 1.stl": "Original + Revision 1",
    "NewBackFloorSuspension UpgradeBack REVISION 1.stl": "Original + Revision 1",
    "NewBackFloorSuspension UpgradeFront3 REVISION 1.stl": "Original + Revision 1",
    "2023NEWSideVent1.stl": "Ryans Creations",
    "2023NEWSideVent2.stl": "Ryans Creations",
    "FloorBoard2.stl": "Ryans Creations",
    "NewFrontNose2021_3.stl": "Ryans Creations",
    "cameranose.stl": "Ryans Creations",
    "FRONTNOSE2024.0002.ipt": "Body Upgrades",
}

REF_EXT = {".pdf", ".jpeg", ".jpg", ".txt"}

def stl_stats(path):
    """Binary STL triangle count + bbox; returns (tris, dx, dy, dz) or None."""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        header = f.read(80)
        if size < 84:
            return None
        (n,) = struct.unpack("<I", f.read(4))
        if 84 + n * 50 != size:
            return None  # ASCII or corrupt
        mins = [float("inf")] * 3
        maxs = [float("-inf")] * 3
        # read in chunks
        CH = 20000
        remaining = n
        while remaining:
            take = min(CH, remaining)
            data = f.read(take * 50)
            for i in range(take):
                off = i * 50 + 12  # skip normal
                vals = struct.unpack_from("<9f", data, off)
                for v in range(3):
                    for a in range(3):
                        c = vals[v * 3 + a]
                        if c < mins[a]: mins[a] = c
                        if c > maxs[a]: maxs[a] = c
            remaining -= take
        return n, maxs[0] - mins[0], maxs[1] - mins[1], maxs[2] - mins[2]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

rows, unmatched = [], []
for dirpath, dirnames, filenames in os.walk(RAW):
    dirnames.sort()
    for fn in sorted(filenames):
        if fn == ".DS_Store":
            continue
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, ROOT)
        ext = os.path.splitext(fn)[1].lower()
        size = os.path.getsize(full)
        digest = sha256(full)
        tris = bx = by = bz = ""
        if ext == ".stl":
            st = stl_stats(full)
            if st:
                tris, bx, by, bz = st[0], f"{st[1]:.1f}", f"{st[2]:.1f}", f"{st[3]:.1f}"
            else:
                tris = "PARSE_FAIL"
        if fn in D:
            tier, grp, mat, unc, note, check = D[fn]
            if fn in CANON and CANON[fn] not in dirpath and tier != REF:
                tier, grp, mat = DUP, "", ""
                note = f"Identical-name duplicate; canonical copy under '{CANON[fn]}'"
                check = ""
        elif ext in REF_EXT:
            tier, grp, mat, unc, note, check = REF, "", "", "low", "", ""
            if ext == ".pdf":
                note = "Assembly drawing (not visually reviewed)"
            elif ext in (".jpeg", ".jpg"):
                note = "Supplier installation photo"
            else:
                note = "Supplier README / parts list"
        else:
            tier, grp, mat, unc, note, check = "UNMATCHED", "", "", "high", "", ""
            unmatched.append(rel)
        rows.append([rel, fn, ext.lstrip("."), size, digest, tris, bx, by, bz,
                     tier, grp, mat, unc, note, check])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["relative_path", "filename", "ext", "size_bytes", "sha256",
                "triangles", "bbox_x_mm", "bbox_y_mm", "bbox_z_mm",
                "tier", "print_group", "material", "uncertainty", "note",
                "human_check"])
    w.writerows(rows)

from collections import Counter
c = Counter(r[9] for r in rows)
print(f"total files: {len(rows)}")
for k in sorted(c):
    print(f"  {k}: {c[k]}")
if unmatched:
    print("\nUNMATCHED (need decisions):")
    for u in unmatched:
        print("  " + u)
