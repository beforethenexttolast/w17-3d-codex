#!/usr/bin/env python3
"""Parametric geometry for the five P0-authorized W17 diagnostic CAD tasks."""
from __future__ import annotations

from dataclasses import dataclass

from lib.meshkit import (Mesh, Parameters, annulus, arrow, box, cylinder,
                         frame_rect, open_shell, text_mesh, text_size,
                         wireframe_box)


@dataclass
class Part:
    filename: str
    cad_task: str
    support_id: str
    title: str
    mesh: Mesh
    features: tuple[str, ...]
    parameter_ids: tuple[str, ...]
    expected_size: tuple[float, float, float]
    bbox_tolerance: float
    print_orientation: str
    assembly_reference: str
    diagnostic_only: bool = True


def _label(mesh: Mesh, text: str, x: float, y: float, z: float, p: Parameters,
           max_width: float | None = None, max_height: float | None = None) -> None:
    cell = p.f("SH-LABEL-CELL")
    if max_width is not None:
        natural, _ = text_size(text, cell)
        if natural > max_width:
            cell *= max_width / natural
    if max_height is not None:
        _, natural = text_size(text, cell)
        if natural > max_height:
            cell *= max_height / natural
    mesh.add(text_mesh(text, x, y, z, cell, p.f("SH-LABEL-HEIGHT")))


def _square_hole_pad(cx: float, cy: float, z: float, outer: float, height: float,
                     p: Parameters) -> Mesh:
    hole = p.f("SH-M3-CLEARANCE")
    rail = (outer - hole) / 2
    return frame_rect(cx - outer / 2, cy - outer / 2, z, outer, outer, height, rail)


def _plate_clamp(p: Parameters, task_label: str) -> Mesh:
    sx = p.f("CLAMP-JAW-X")
    sy = p.f("CLAMP-JAW-Y")
    wall = p.f("CLAMP-WALL")
    gap = p.f("CLAMP-JAW-GAP")
    kx, ky, kz = p.f("CLAMP-KEY-X"), p.f("CLAMP-KEY-Y"), p.f("CLAMP-KEY-Z")
    mesh = Mesh()
    mesh.add(box(0, 0, 0, sx, sy, wall))
    mesh.add(box(0, 0, wall + gap, sx, sy, wall))
    mesh.add(box(0, 0, wall, wall, sy, gap))
    mesh.add(box((sx - kx) / 2, (sy - ky) / 2, 2 * wall + gap, kx, ky, kz))
    _label(mesh, task_label, wall, wall, wall + gap - p.f("SH-LABEL-HEIGHT") / 2,
           p, max_width=sx - 2 * wall)
    return mesh


def _clamp_receiver(mesh: Mesh, x: float, y: float, z: float, p: Parameters,
                    open_direction: str = "+y") -> None:
    """Three-rail open receiver for the removable clamp-foot key."""
    kx, ky = p.f("CLAMP-KEY-X"), p.f("CLAMP-KEY-Y")
    rail = p.f("TRAY-WALL-T")
    height = p.f("CLAMP-KEY-Z")
    if open_direction == "+y":
        mesh.add(box(x - rail, y - rail, z, rail, ky + rail, height))
        mesh.add(box(x + kx, y - rail, z, rail, ky + rail, height))
        mesh.add(box(x, y - rail, z, kx, rail, height))
    elif open_direction == "-y":
        mesh.add(box(x - rail, y, z, rail, ky + rail, height))
        mesh.add(box(x + kx, y, z, rail, ky + rail, height))
        mesh.add(box(x, y + ky, z, kx, rail, height))
    else:
        raise ValueError("unsupported receiver direction")


def _battery_dummy(p: Parameters) -> Part:
    x, y, z = p.f("BAT-BODY-X"), p.f("BAT-BODY-Y"), p.f("BAT-BODY-Z")
    install_y, install_z = p.f("BAT-INSTALL-Y"), p.f("BAT-INSTALL-Z")
    wall, rib = p.f("SH-SHELL-WALL"), p.f("SH-FRAME-RIB")
    xtx, xty, xtz = p.f("BAT-XT60-X"), p.f("BAT-XT60-Y"), p.f("BAT-XT60-Z")
    bend = p.f("BAT-BEND-X")
    cable_d = p.f("BAT-CABLE-D")
    facets = int(p.f("SH-CYLINDER-FACETS"))
    install_x = max(x + bend, p.f("BAT-INSTALL-X"))
    body_y = (install_y - y) / 2
    mesh = open_shell(0, body_y, 0, x, y, z, wall)
    # The installation cage makes the registered restraint/strap allowance
    # tangible without pretending it is part of the selected battery body.
    mesh.add(wireframe_box(0, 0, 0, x, install_y, install_z, rib))
    # The 20 mm forward allowance is an open cage; the XT60 body sits inside it.
    mesh.add(wireframe_box(x, (install_y - max(xty, rib * 2)) / 2, 0,
                           install_x - x, max(xty, rib * 2), max(xtz, rib * 2), rib))
    mesh.add(open_shell(x, (install_y - xty) / 2, 0,
                        min(xtx, install_x - x), xty, xtz, wall))
    cable_x = x + min(xtx, install_x - x)
    if install_x > cable_x:
        mesh.add(cylinder(cable_x, install_y / 2, cable_d / 2,
                          cable_d, install_x - cable_x, facets, "x"))
    # Balance-test mass pocket is deliberately open and marked, never concealed.
    mpx, mpy, mpz = (p.f("BAT-MASS-POCKET-X"), p.f("BAT-MASS-POCKET-Y"),
                     p.f("BAT-MASS-POCKET-Z"))
    mesh.add(open_shell((x - mpx) / 2, (install_y - mpy) / 2, wall,
                        mpx, mpy, mpz, wall))
    _label(mesh, "PWR-BAT TP", wall * 2, body_y + wall * 2,
           wall * 0.8, p, x * 0.62)
    _label(mesh, "MASS TEST", (x - mpx) / 2 + wall,
           (install_y - mpy) / 2 + wall,
           wall + wall * 0.8, p, mpx - 2 * wall)
    _label(mesh, "XT60", x + wall, (install_y - xty) / 2 + wall, wall * 0.8, p,
           install_x - x - 2 * wall)
    mesh.add(arrow(x * 0.55, body_y + y * 0.78, wall * 0.8, x * 0.30, y * 0.12,
                   p.f("SH-ARROW-HEIGHT"), "+x"))
    return Part(
        "cad01_pwr_bat_max.stl", "CAD-01", "PS-13", "PWR-BAT maximum installation dummy",
        mesh,
        ("component ID", "orientation arrow", "XT60 installed plug", "forward cable exit",
         "initial cable bend cage", "50 x 30 restraint/strap installation cage",
         "balance-test mass pocket"),
        ("BAT-BODY-X", "BAT-BODY-Y", "BAT-BODY-Z", "BAT-INSTALL-X",
         "BAT-INSTALL-Y", "BAT-INSTALL-Z", "BAT-XT60-X",
         "BAT-XT60-Y", "BAT-XT60-Z", "BAT-BEND-X", "BAT-CABLE-D",
         "BAT-MASS-POCKET-X",
         "BAT-MASS-POCKET-Y", "BAT-MASS-POCKET-Z"),
        (install_x, install_y, install_z), 0.5,
        "open body and restraint cage up; DAT-F-facing base on bed",
        "free diagnostic body; arrow +X is forward")


def _esc_dummy(p: Parameters) -> Part:
    bx, by, bz = p.f("ESC-BODY-X"), p.f("ESC-BODY-Y"), p.f("ESC-BODY-Z")
    bend, mount = p.f("ESC-BEND-X"), p.f("ESC-MOUNT-ALLOW")
    xtx, xty, xtz = p.f("BAT-XT60-X"), p.f("BAT-XT60-Y"), p.f("BAT-XT60-Z")
    fd, fz, air = p.f("ESC-FAN-D"), p.f("ESC-FAN-Z"), p.f("SH-FAN-CLEARANCE")
    bullet_d, pitch = p.f("ESC-BULLET-D"), p.f("ESC-BULLET-PITCH")
    wall, rib, facets = p.f("SH-SHELL-WALL"), p.f("SH-FRAME-RIB"), int(p.f("SH-CYLINDER-FACETS"))
    body_x = bend
    fwd = max(bend, xtx)
    mesh = Mesh()
    mesh.add(open_shell(body_x, 0, 0, bx, by, bz, wall))
    mesh.add(box(body_x - mount, -mount, 0, bx + 2 * mount, by + 2 * mount, wall))
    mesh.add(open_shell(body_x + bx, (by - xty) / 2, 0, fwd, xty, xtz, wall))
    for offset in (-pitch, 0, pitch):
        mesh.add(cylinder(0, by / 2 + offset, bullet_d / 2, bullet_d, bend, facets, "x"))
    mesh.add(annulus(body_x + bx / 2, by / 2, bz, fd, fd * 0.70, fz, facets))
    mesh.add(wireframe_box(body_x + (bx - fd) / 2, (by - fd) / 2, bz + fz,
                           fd, fd, air, rib))
    _label(mesh, "DRV-ESC TP", body_x + wall * 2, wall * 2, wall * 0.8, p, bx * 0.75)
    _label(mesh, "PHASE", wall, by * 0.58, wall * 0.8, p, bend - 2 * wall)
    _label(mesh, "XT60", body_x + bx + wall, (by - xty) / 2 + wall,
           wall * 0.8, p, fwd - 2 * wall)
    mesh.add(arrow(body_x + bx * 0.52, by * 0.78, wall * 0.8, bx * 0.35, by * 0.12,
                   p.f("SH-ARROW-HEIGHT"), "+x"))
    mesh.add(arrow(body_x + bx * 0.25, by * 0.50, bz + fz, air * 0.75, by * 0.16,
                   p.f("SH-ARROW-HEIGHT"), "+y"))
    return Part(
        "cad01_drv_esc.stl", "CAD-01", "PS-13", "DRV-ESC installation dummy",
        mesh,
        ("component ID", "forward orientation arrow", "airflow arrow", "forward XT60 plug",
         "three aft phase exits", "phase bend allowance", "fan volume",
         "10 mm cooling volume", "mounting allowance"),
        ("ESC-BODY-X", "ESC-BODY-Y", "ESC-BODY-Z", "ESC-FAN-D", "ESC-FAN-Z",
         "SH-FAN-CLEARANCE", "ESC-MOUNT-ALLOW", "ESC-BEND-X", "ESC-BULLET-D",
         "ESC-BULLET-PITCH"),
        (bend + bx + fwd, by + 2 * mount, bz + fz + air), 0.5,
        "mounting flange on bed; fan and cooling cage up", "free diagnostic body; +X is forward")


def _ubec_dummy(p: Parameters, rail_name: str) -> Part:
    bx, by, bz = p.f("UBEC-BODY-X"), p.f("UBEC-BODY-Y"), p.f("UBEC-BODY-Z")
    lead, lead_d = p.f("UBEC-LEAD-X"), p.f("UBEC-LEAD-D")
    air, allow = p.f("UBEC-AIR-Z"), p.f("UBEC-MOUNT-ALLOW")
    wall, rib, facets = p.f("SH-SHELL-WALL"), p.f("SH-FRAME-RIB"), int(p.f("SH-CYLINDER-FACETS"))
    mesh = Mesh()
    mesh.add(open_shell(lead, 0, 0, bx, by, bz, wall))
    mesh.add(box(lead - allow, -allow, 0, bx + 2 * allow, by + 2 * allow, wall))
    mesh.add(cylinder(0, by / 2, lead_d / 2, lead_d, lead, facets, "x"))
    mesh.add(cylinder(lead + bx, by / 2, lead_d / 2, lead_d, lead, facets, "x"))
    mesh.add(wireframe_box(lead, 0, bz, bx, by, air, rib))
    _label(mesh, f"RAIL {rail_name} TP", lead + wall, wall, wall * 0.8, p, bx - 2 * wall)
    _label(mesh, "IN", wall, by * 0.58, wall * 0.8, p, lead - 2 * wall)
    _label(mesh, "OUT", lead + bx + wall, by * 0.58, wall * 0.8, p, lead - 2 * wall)
    mesh.add(arrow(lead + bx * 0.30, by * 0.78, wall * 0.8, bx * 0.35, by * 0.12,
                   p.f("SH-ARROW-HEIGHT"), "+x"))
    filename = f"cad01_pwr_ubec_{rail_name.lower()}.stl"
    return Part(
        filename, "CAD-01", "PS-13", f"PWR-UBEC Rail {rail_name} installation dummy",
        mesh,
        ("component ID", f"Rail {rail_name} marking", "orientation arrow", "input lead",
         "output lead", "both initial bend zones", "cooling allowance", "mounting allowance"),
        ("UBEC-BODY-X", "UBEC-BODY-Y", "UBEC-BODY-Z", "UBEC-LEAD-X", "UBEC-LEAD-D",
         "UBEC-AIR-Z", "UBEC-MOUNT-ALLOW"),
        (2 * lead + bx, by + 2 * allow, bz + air), 0.5,
        "mount allowance on bed; open body and cooling cage up", "free diagnostic body; +X follows intended lead flow")


def _esp_dummy(p: Parameters, board_id: str) -> Part:
    bx, by, bz = p.f("ESP-BODY-X"), p.f("ESP-BODY-Y"), p.f("ESP-BODY-Z")
    hy = p.f("ESP-HEADER-Y")
    ux, uy, uz, bend = (p.f("ESP-USB-X"), p.f("ESP-USB-Y"), p.f("ESP-USB-Z"),
                        p.f("ESP-USB-BEND-X"))
    wall, rib = p.f("SH-SHELL-WALL"), p.f("SH-FRAME-RIB")
    body_y = (hy - by) / 2
    mesh = Mesh()
    mesh.add(open_shell(0, body_y, 0, bx, by, bz, wall))
    mesh.add(box(0, 0, 0, bx, rib * 2, bz * 0.72))
    mesh.add(box(0, hy - rib * 2, 0, bx, rib * 2, bz * 0.72))
    # Two small ties per side keep the header-envelope rails captive to the
    # body dummy; without them the STL prints as three unrelated pieces.
    rail_y = rib * 2
    bridge_y = body_y - rail_y + wall
    for xx in (bx * 0.20, bx * 0.76):
        mesh.add(box(xx, rail_y - wall / 2, 0, rib, bridge_y, wall))
        mesh.add(box(xx, body_y + by - wall / 2, 0, rib, bridge_y, wall))
    mesh.add(open_shell(bx, (hy - uy) / 2, 0, ux, uy, uz, wall))
    mesh.add(wireframe_box(bx + ux, (hy - uy) / 2, 0, bend, uy, max(uz, rib * 2), rib))
    _label(mesh, f"CTL-{board_id} TP", wall * 2, body_y + wall, wall * 0.8, p, bx * 0.48)
    _label(mesh, "USB ACCESS", bx + wall, (hy - uy) / 2 + wall, wall * 0.8,
           p, ux + bend - 2 * wall)
    _label(mesh, "PINS", bx * 0.36, wall * 0.4, wall * 0.8, p, bx * 0.24)
    mesh.add(arrow(bx * 0.56, body_y + by * 0.78, wall * 0.8, bx * 0.32, by * 0.12,
                   p.f("SH-ARROW-HEIGHT"), "+x"))
    return Part(
        f"cad01_ctl_{board_id.lower()}.stl", "CAD-01", "PS-13",
        f"ESP32 {board_id} installed-service dummy", mesh,
        ("component ID", "orientation arrow", "pin-header envelope", "permanently occupied USB plug",
         "USB cable bend", "USB access side", "mounting/standoff allowance"),
        ("ESP-BODY-X", "ESP-BODY-Y", "ESP-BODY-Z", "ESP-HEADER-Y", "ESP-USB-X",
         "ESP-USB-Y", "ESP-USB-Z", "ESP-USB-BEND-X", "ESP-MOUNT-ALLOW"),
        (bx + ux + bend, hy, bz), 0.5, "board plane on bed; USB service stub horizontal",
        "free diagnostic body; +X is USB/access side")


def _wifi_dummy(p: Parameters) -> Part:
    bx, by, bz = p.f("WIFI-BODY-X"), p.f("WIFI-BODY-Y"), p.f("WIFI-BODY-Z")
    pig, pig_d = p.f("WIFI-PIGTAIL-X"), p.f("WIFI-PIGTAIL-D")
    cn16, power = p.f("WIFI-CN16-X"), p.f("WIFI-POWER-X")
    hsx, hsy, hsz = p.f("WIFI-HS-X"), p.f("WIFI-HS-Y"), p.f("WIFI-HS-Z")
    air = p.f("WIFI-AIR-Z")
    wall, rib, facets = p.f("SH-SHELL-WALL"), p.f("SH-FRAME-RIB"), int(p.f("SH-CYLINDER-FACETS"))
    forward = max(cn16, power)
    body_x = pig
    mesh = Mesh()
    mesh.add(open_shell(body_x, 0, 0, bx, by, bz, wall))
    for yy in (by * 0.32, by * 0.68):
        mesh.add(cylinder(0, yy, pig_d / 2, pig_d, pig, facets, "x"))
    mesh.add(open_shell(body_x + bx, by * 0.18, 0, power, by * 0.22, min(bz, power), wall))
    mesh.add(wireframe_box(body_x + bx, by * 0.60, 0, cn16, by * 0.22,
                           min(bz, cn16), rib))
    mesh.add(box(body_x + (bx - hsx) / 2, (by - hsy) / 2, bz, hsx, hsy, hsz))
    mesh.add(wireframe_box(body_x + (bx - hsx) / 2, (by - hsy) / 2, bz + hsz,
                           hsx, hsy, air, rib))
    _label(mesh, "UNCONFIRMED", body_x + wall * 2, wall * 1.4, wall * 0.8, p, bx - 4 * wall)
    _label(mesh, "ENVELOPE", body_x + wall * 2, by * 0.48, wall * 0.8, p, bx - 4 * wall)
    _label(mesh, "VID-WIFI MAX TP", body_x + wall * 2, by * 0.73, wall * 0.8, p, bx - 4 * wall)
    _label(mesh, "AFT COAX", wall, by * 0.42, wall * 0.8, p, pig - 2 * wall)
    _label(mesh, "POWER", body_x + bx + wall, by * 0.18 + wall, wall * 0.8, p,
           power - 2 * wall)
    _label(mesh, "CN16", body_x + bx + wall, by * 0.60 + wall, wall * 0.8, p,
           cn16 - 2 * wall)
    mesh.add(arrow(body_x + bx * 0.56, by * 0.88, wall * 0.8, bx * 0.30, by * 0.10,
                   p.f("SH-ARROW-HEIGHT"), "+x"))
    return Part(
        "cad01_vid_wifi_max.stl", "CAD-01", "PS-13", "VID-WIFI unconfirmed maximum envelope dummy",
        mesh,
        ("UNCONFIRMED ENVELOPE marking", "component ID", "orientation arrow", "two aft pigtail exits",
         "power exit", "CN-16 boundary", "cable bend volumes", "confirmed heatsink",
         "cooling allowance"),
        ("WIFI-BODY-X", "WIFI-BODY-Y", "WIFI-BODY-Z", "WIFI-HS-X", "WIFI-HS-Y",
         "WIFI-HS-Z", "WIFI-AIR-Z", "WIFI-PIGTAIL-X", "WIFI-PIGTAIL-D",
         "WIFI-CN16-X", "WIFI-POWER-X"),
        (pig + bx + forward, by, bz + hsz + air), 0.5,
        "body base on bed; heatsink/cooling cage up", "free diagnostic body; +X power/CN-16, -X aft/coax")


def _amp_dummy(p: Parameters) -> Part:
    bx, by, bz = p.f("AMP-BODY-X"), p.f("AMP-BODY-Y"), p.f("AMP-BODY-Z")
    lead, allow, adjust = p.f("AMP-LEAD-X"), p.f("AMP-MOUNT-ALLOW"), p.f("AMP-ADJUST-D")
    wall, rib = p.f("SH-SHELL-WALL"), p.f("SH-FRAME-RIB")
    body_x = lead
    cage_rail = min(wall * 0.5, bz * 0.20)
    mesh = Mesh()
    mesh.add(open_shell(body_x, 0, 0, bx, by, bz, min(wall, bz * 0.35)))
    mesh.add(box(body_x - allow, -allow, 0, bx + 2 * allow, by + 2 * allow,
                 min(wall, bz * 0.35)))
    mesh.add(wireframe_box(0, by * 0.22, 0, lead, by * 0.56, max(bz, cage_rail * 2.1), cage_rail))
    mesh.add(wireframe_box(body_x + bx, by * 0.22, 0, lead, by * 0.56,
                           max(bz, cage_rail * 2.1), cage_rail))
    # The access column starts on the mounting flange so no frame is suspended
    # above the open-top body during printing.
    mesh.add(wireframe_box(body_x + (bx - adjust) / 2, (by - adjust) / 2, 0,
                           adjust, adjust, bz + adjust, rib * 0.55))
    _label(mesh, "AUD-AMP TP", body_x + wall, wall, wall * 0.6, p, bx - 2 * wall)
    _label(mesh, "I2S", wall, by * 0.40, wall * 0.6, p, lead - 2 * wall)
    _label(mesh, "SPK", body_x + bx + wall, by * 0.40, wall * 0.6, p, lead - 2 * wall)
    mesh.add(arrow(body_x + bx * 0.28, by * 0.78, min(wall, bz * 0.35) * 0.8,
                   bx * 0.40, by * 0.10, p.f("SH-ARROW-HEIGHT"), "+x"))
    return Part(
        "cad01_aud_amp.stl", "CAD-01", "PS-13", "AUD-AMP installation dummy", mesh,
        ("component ID", "orientation arrow", "I2S connector exit", "speaker connector exit", "both cable bends",
         "mounting allowance", "adjustment/tool access volume"),
        ("AMP-BODY-X", "AMP-BODY-Y", "AMP-BODY-Z", "AMP-MOUNT-ALLOW", "AMP-LEAD-X",
         "AMP-ADJUST-D"),
        (2 * lead + bx, by + 2 * allow, bz + adjust), 0.5,
        "mount allowance on bed; adjustment cage up", "free diagnostic body; I2S -X, speaker +X")


def _servo_dummy(p: Parameters) -> Part:
    bx, by, bz = p.f("SERVO-BODY-X"), p.f("SERVO-BODY-Y"), p.f("SERVO-BODY-Z")
    radius, hz = p.f("SERVO-HORN-R"), p.f("SERVO-HORN-Z")
    lead, lead_d = p.f("SERVO-LEAD-X"), p.f("SERVO-LEAD-D")
    wall, facets = p.f("SH-SHELL-WALL"), int(p.f("SH-CYLINDER-FACETS"))
    mesh = open_shell(lead, radius - by / 2, 0, bx, by, bz, wall)
    mesh.add(cylinder(0, radius, lead_d / 2, lead_d, lead, facets, "x"))
    mesh.add(annulus(lead + bx / 2, radius, bz, 2 * radius, p.f("SH-M3-CLEARANCE"), hz, facets))
    _label(mesh, "SRV-STEER TP", lead + wall * 2, radius - by / 2 + wall,
           wall * 0.8, p, bx * 0.75)
    _label(mesh, "LEAD", wall, radius - lead_d, wall * 0.8, p, lead - 2 * wall)
    mesh.add(arrow(lead + bx * 0.55, radius + by * 0.28, wall * 0.8,
                   bx * 0.30, by * 0.12, p.f("SH-ARROW-HEIGHT"), "+x"))
    # The horn disc hides the body-floor label from above, so repeat a short ID
    # on the diagnostic sweep surface for unambiguous P1 photographs.
    _label(mesh, "SRV TP", lead + bx * 0.20, radius - by * 0.10,
           bz + hz - 0.20, p, bx * 0.62)
    return Part(
        "cad01_srv_steer.stl", "CAD-01", "PS-13", "SRV-STEER/KO-19 installation dummy",
        mesh,
        ("component ID", "orientation arrow", "body envelope", "horn sweep envelope",
         "lead exit", "initial lead bend"),
        ("SERVO-BODY-X", "SERVO-BODY-Y", "SERVO-BODY-Z", "SERVO-HORN-R",
         "SERVO-HORN-Z", "SERVO-LEAD-X", "SERVO-LEAD-D"),
        (lead + bx, 2 * radius, bz + hz + p.f("SH-LABEL-HEIGHT") - 0.20), 0.5,
        "servo body base on bed; horn-sweep disc up", "free diagnostic body; lead exits -X")


def _junction_dummy(p: Parameters) -> Part:
    bx, by, bz = p.f("JUNC-DUMMY-X"), p.f("JUNC-DUMMY-Y"), p.f("JUNC-DUMMY-Z")
    hand, wire, extract = p.f("JUNC-HAND-X"), p.f("JUNC-WIRE-X"), p.f("JUNC-EXTRACT-X")
    tool = p.f("JUNC-TOOL-D")
    wall, rib = p.f("SH-SHELL-WALL"), p.f("SH-FRAME-RIB")
    body_x = hand
    aft = max(wire, extract)
    mesh = Mesh()
    mesh.add(open_shell(body_x, 0, 0, bx, by, bz, wall))
    mesh.add(wireframe_box(0, 0, 0, hand, by, bz, rib))
    mesh.add(wireframe_box(body_x + bx, 0, 0, aft, by, bz, rib))
    # Connector body allowances at the mating face: XT60 plus three XT30-class bodies.
    xtx, xty, xtz = p.f("BAT-XT60-X"), p.f("BAT-XT60-Y"), p.f("BAT-XT60-Z")
    mesh.add(open_shell(body_x - min(xtx, hand), by * 0.10, 0,
                        min(xtx, hand), xty, xtz, wall))
    tx, ty, tz = p.f("JUNC-XT30-X"), p.f("JUNC-XT30-Y"), p.f("JUNC-XT30-Z")
    for yy in (by * 0.43, by * 0.63, by * 0.83):
        mesh.add(open_shell(body_x - min(tx, hand), yy - ty / 2, 0,
                            min(tx, hand), ty, tz, min(wall, tz * 0.25)))
    # Full-height tool column is printable from the bed and still leaves the
    # intended driver clearance visible through its open centre.
    mesh.add(wireframe_box(body_x + bx * 0.44, (by - tool) / 2, 0,
                           tool, tool, bz + tool, rib * 0.55))
    _label(mesh, "PS-15 BANK TP", body_x + wall * 2, wall * 1.4, wall * 0.8, p, bx - 4 * wall)
    _label(mesh, "MATE HAND", wall, by * 0.44, wall * 0.8, p, hand - 2 * wall)
    _label(mesh, "WIRE EXIT", body_x + bx + wall, by * 0.44, wall * 0.8, p, aft - 2 * wall)
    mesh.add(arrow(body_x + bx * 0.38, by * 0.80, wall * 0.8, bx * 0.30, by * 0.12,
                   p.f("SH-ARROW-HEIGHT"), "-x"))
    mesh.add(arrow(body_x + bx + wall, by * 0.18, wall * 0.8, aft * 0.75,
                   by * 0.10, p.f("SH-ARROW-HEIGHT"), "+x"))
    return Part(
        "cad01_ps15_connector_bank.stl", "CAD-01", "PS-13/PS-15",
        "PS-15 connector-bank/access dummy", mesh,
        ("component ID", "connector-bank body", "XT60 allowance", "XT30 allowances",
         "mating direction arrow", "mating-hand volume", "wire-entry/exit volume",
         "initial bend volume", "tool-access volume", "service-removal direction"),
        ("JUNC-DUMMY-X", "JUNC-DUMMY-Y", "JUNC-DUMMY-Z", "JUNC-HAND-X", "JUNC-WIRE-X",
         "JUNC-TOOL-D", "JUNC-EXTRACT-X", "BAT-XT60-X", "BAT-XT60-Y", "BAT-XT60-Z",
         "JUNC-XT30-X", "JUNC-XT30-Y", "JUNC-XT30-Z"),
        (hand + bx + aft, by, bz + tool), 0.5,
        "connector bank base on bed; access cages horizontal", "free diagnostic body; mating -X, removal/wires +X")


def _battery_tray(p: Parameters) -> Part:
    sx, sy, base = p.f("TRAY-BAY-X"), p.f("TRAY-OUTER-Y"), p.f("TRAY-BASE-Z")
    wall_z, wall_t = p.f("TRAY-WALL-Z"), p.f("TRAY-WALL-T")
    slot = p.f("TRAY-STRAP-SLOT")
    balance_gap = p.f("TRAY-BALANCE-CLIP-GAP")
    origin_x, origin_l = p.f("TRAY-ORIGIN-X"), p.f("TRAY-ORIGIN-L")
    mesh = Mesh()
    # Open base: three transverse ribs expose DAT-F interruptions and screw heads.
    mesh.add(box(0, 0, 0, wall_t, sy, base))
    mesh.add(box(sx / 2 - wall_t / 2, 0, 0, wall_t, sy, base))
    mesh.add(box(sx - wall_t, 0, 0, wall_t, sy, base))
    gap0, gap1 = sx / 2 - slot / 2, sx / 2 + slot / 2
    for yy in (0, sy - wall_t):
        mesh.add(box(0, yy, 0, gap0, wall_t, wall_z))
        mesh.add(box(gap1, yy, 0, sx - gap1, wall_t, wall_z))
    # Aft corner restraint only; the forward face stays open for insertion and XT60.
    mesh.add(box(0, 0, base, wall_t, sy * 0.22, wall_z - base))
    mesh.add(box(0, sy * 0.78, base, wall_t, sy * 0.22, wall_z - base))
    # The mirror free feature is too close to the KO-19 policy boundary for a
    # wide diagnostic ear.  Two outboard reversible-clamp receivers are used.
    _clamp_receiver(mesh, sx * 0.22, sy - p.f("CLAMP-KEY-Y"), 0, p, "+y")
    _clamp_receiver(mesh, sx * 0.68, sy - p.f("CLAMP-KEY-Y"), 0, p, "+y")
    # Outboard ballast land; it is a visible ledge for 5 g adhesive strips.
    ballast_x = p.f("TRAY-BALLAST-X")
    mesh.add(box((sx - ballast_x) / 2, sy - wall_t * 2, wall_z - p.f("TRAY-BALLAST-Z"),
                 ballast_x, wall_t * 2, p.f("TRAY-BALLAST-Z")))
    # Open-top two-finger park for the balance lead; it stays inside the 50 mm
    # tray allocation and does not close the battery insertion path.
    clip_x = sx * 0.78
    clip_y = sy - wall_t * 2
    clip_h = wall_z * 0.62
    mesh.add(box(clip_x - balance_gap / 2 - wall_t, clip_y, 0,
                 wall_t, wall_t * 2, clip_h))
    mesh.add(box(clip_x + balance_gap / 2, clip_y, 0,
                 wall_t, wall_t * 2, clip_h))
    _label(mesh, "PS-01 TP", wall_t * 1.4, sy * 0.30, base * 0.8, p, sx * 0.34)
    _label(mesh, "XT60 FWD", sx * 0.58, sy * 0.30, base * 0.8, p, sx * 0.30)
    _label(mesh, "5G BALLAST", (sx - ballast_x) / 2, sy - wall_t * 2,
           wall_z - p.f("TRAY-BALLAST-Z") * 0.8, p, ballast_x,
           max_height=wall_t * 2)
    mesh.add(arrow(sx * 0.58, sy * 0.70, base * 0.8, sx * 0.30, sy * 0.10,
                   p.f("SH-ARROW-HEIGHT"), "+x"))
    return Part(
        "cad02_ps01_battery_tray.stl", "CAD-02", "PS-01", "PS-01 diagnostic battery tray",
        mesh,
        ("PS-ID TP marking", "DAT-F open base", "78 mm bay gauge",
         "two reversible plate-clamp receivers",
         "open forward insertion path", "XT60 notch/arrow", "20 mm strap passages",
         "balance-lead park", "side restraint", "outboard 5 g ballast land",
         "visible floor-interruption windows"),
        ("TRAY-BAY-X", "TRAY-OUTER-Y", "TRAY-BASE-Z", "TRAY-WALL-Z", "TRAY-WALL-T",
         "TRAY-ORIGIN-X", "TRAY-ORIGIN-L", "TRAY-STRAP-W", "TRAY-STRAP-SLOT",
         "TRAY-BALANCE-CLIP-GAP",
         "TRAY-TRIM-X", "TRAY-BALLAST-X", "TRAY-BALLAST-Z", "CLAMP-KEY-X",
         "CLAMP-KEY-Y", "CLAMP-KEY-Z"),
        (sx, sy, wall_z), 0.5, "DAT-F/open-rib face on bed",
        f"assembly origin X={origin_x} L={origin_l} Z=DAT-F")


def _ubec_shelf(p: Parameters) -> Part:
    sx, sy = p.f("SHELF-X"), p.f("SHELF-Y")
    base, rib = p.f("SHELF-BASE-Z"), p.f("SHELF-RIB")
    bx, by, bz = p.f("UBEC-BODY-X"), p.f("UBEC-BODY-Y"), p.f("UBEC-BODY-Z")
    clear = p.f("SHELF-POCKET-CLEAR")
    origin_x, origin_l = p.f("SHELF-ORIGIN-X"), p.f("SHELF-ORIGIN-L")
    free_x = p.f("SH-RIGHT-FREE-X") - origin_x
    free_y = p.f("SH-RIGHT-FREE-L") - origin_l
    mesh = frame_rect(0, 0, 0, sx, sy, base, rib)
    # One central cross-rib plus two open-ended pocket lanes; all lead exits stay visible.
    mesh.add(box(sx / 2 - rib / 2, rib, 0, rib, sy - 2 * rib, base))
    pocket_x = (sx - bx) / 2
    divider_y = sy / 2 - rib / 2
    for yy in (0, divider_y, sy - rib):
        mesh.add(box(pocket_x, yy, 0, bx, rib, base + bz))
    lane_gaps = ((rib, divider_y), (divider_y + rib, sy - rib))
    expected_gap = max(by + 2 * clear, by + 2 * p.f("UBEC-MOUNT-ALLOW"))
    for yy0, yy1 in lane_gaps:
        if yy1 - yy0 < expected_gap:
            raise ValueError("UBEC shelf lane does not clear the diagnostic dummy")
        # Open comb fingers at both ends represent lead routing without covering it.
        comb = p.f("SHELF-LEAD-COMB-GAP")
        half = ((yy1 - yy0) - comb) / 2
        for xx in (0, sx - rib):
            mesh.add(box(xx, yy0, 0, rib, half, base + bz * 0.55))
            mesh.add(box(xx, yy1 - half, 0, rib, half, base + bz * 0.55))
    ear_outer = max(p.f("SH-M3-CLEARANCE") + 2 * rib, p.f("SHELF-POST-SHOULDER-D"))
    mesh.add(_square_hole_pad(free_x, free_y, 0, ear_outer, base, p))
    _clamp_receiver(mesh, sx * 0.62, 0, 0, p, "-y")
    # Two replaceable-post shoulders; these are seats only, never CAD-05 deck geometry.
    shoulder = p.f("SHELF-POST-SHOULDER-D")
    for cx, cy in ((sx - shoulder / 2, shoulder / 2),
                   (sx - shoulder / 2, sy - shoulder / 2)):
        mesh.add(_square_hole_pad(cx, cy, 0, shoulder, base + rib, p))
    wall = p.f("SH-SHELL-WALL")
    _label(mesh, "RAIL A", pocket_x + rib, rib + wall,
           base * 0.8, p, bx - 2 * rib)
    _label(mesh, "RAIL B", pocket_x + rib, divider_y + rib + wall,
           base * 0.8, p, bx - 2 * rib)
    _label(mesh, "PS-03 TP", rib * 1.4, sy / 2 - rib, base * 0.8, p, sx * 0.28)
    mesh.add(arrow(sx * 0.64, sy / 2, base * 0.8, sx * 0.26, sy * 0.10,
                   p.f("SH-ARROW-HEIGHT"), "+x"))
    return Part(
        "cad04_ps03_ubec_shelf.stl", "CAD-04", "PS-03", "PS-03 diagnostic UBEC shelf",
        mesh,
        ("PS-ID TP marking", "DAT-F open frame", "verified-free-feature ear",
         "reversible plate-clamp receiver",
         "Rail A pocket", "Rail B pocket", "lead combs both ends", "open airflow floor",
         "removal access", "two replaceable-post shoulders", "orientation arrow"),
        ("SHELF-X", "SHELF-Y", "SHELF-Z-MAX", "SHELF-BASE-Z", "SHELF-RIB",
         "SHELF-POCKET-CLEAR", "SHELF-ORIGIN-X", "SHELF-ORIGIN-L",
         "SHELF-POST-SHOULDER-D", "SHELF-LEAD-COMB-GAP", "SH-RIGHT-FREE-X",
         "SH-RIGHT-FREE-L", "SH-D26-Z-MIN", "SH-D26-Z-MAX", "CLAMP-KEY-X",
         "CLAMP-KEY-Y", "CLAMP-KEY-Z"),
        (sx, sy, base + bz), 0.5, "DAT-F/open-frame face on bed",
        f"assembly origin X={origin_x} L={origin_l} Z=DAT-F; geometry remains below Z={p.f('SHELF-Z-MAX')}")


def _post(p: Parameters, height_id: str, height: float) -> Part:
    diameter, bore = p.f("POST-D"), p.f("POST-BORE")
    facets = int(p.f("SH-CYLINDER-FACETS"))
    base = diameter * 1.5
    cx = cy = base / 2
    mesh = annulus(cx, cy, 0, diameter, bore, height, facets)
    # Marking flag is attached at DAT-F and keeps the post ID readable after print.
    flag_x, flag_y, flag_z = diameter * 1.35, diameter, p.f("POST-KEY-Z")
    mesh.add(box(cx + diameter / 2 - p.f("SH-FRAME-RIB") / 2,
                 cy - flag_y / 2, 0, flag_x, flag_y, flag_z))
    _label(mesh, f"H{int(height)}", cx + diameter / 2, cy - flag_y * 0.30,
           flag_z * 0.75, p, flag_x * 0.82)
    _label(mesh, "PS-05", cx + diameter / 2, cy + flag_y * 0.08,
           flag_z * 0.75, p, flag_x * 0.82)
    actual = mesh.bbox()
    size = tuple(actual[1][i] - actual[0][i] for i in range(3))
    return Part(
        f"cad06_ps05_post_h{int(height):02d}.stl", "CAD-06", "PS-05",
        f"PS-05 replaceable diagnostic post {height:g} mm", mesh,
        ("PS-ID marking", f"H{int(height)} height marking", "DAT-F bottom reference",
         "M3 through passage", "replaceable shoulder interface", "no deck geometry"),
        ("POST-D", "POST-BORE", height_id, "POST-KEY-X", "POST-KEY-Z", "SH-DAT-F-Z"),
        size, 0.5, "DAT-F post end and marking flag on bed",
        f"Z=0 at DAT-F/seat; nominal top Z={height:g} mm")


def _junction_support(p: Parameters) -> Part:
    sx, sy, max_z = p.f("JUNC-SUPPORT-X"), p.f("JUNC-SUPPORT-Y"), p.f("JUNC-SUPPORT-Z")
    base, rib = p.f("JUNC-SUPPORT-BASE-Z"), p.f("SHELF-RIB")
    origin_x, origin_l = p.f("JUNC-SUPPORT-ORIGIN-X"), p.f("JUNC-SUPPORT-ORIGIN-L")
    vent_x = p.f("JUNC-VENT-X-MIN") - origin_x
    vent_y = abs(origin_l) - p.f("JUNC-VENT-L-ABS-MIN")
    mesh = Mesh()
    # L-shaped open frame: no structure occupies the P0 vent/body-seat quadrant.
    mesh.add(box(0, 0, 0, min(vent_x, sx), rib, base))
    mesh.add(box(0, sy - rib, 0, sx, rib, base))
    mesh.add(box(0, rib, 0, rib, sy - 2 * rib, base))
    mesh.add(box(sx - rib, max(vent_y, rib), 0, rib, sy - max(vent_y, rib) - rib, base))
    mesh.add(box(min(vent_x, sx) - rib, rib, 0, rib, sy - 2 * rib, base))
    # Modular connector/decision seats are open rails: no DN-01/DN-02 choice is baked in.
    xtx, xty, xtz = p.f("BAT-XT60-X"), p.f("BAT-XT60-Y"), p.f("BAT-XT60-Z")
    seat_x = rib * 0.75
    mesh.add(frame_rect(seat_x, rib * 3.5, 0, xtx + 2 * rib, xty + 2 * rib,
                        min(xtz, max_z - base), rib))
    fx, fy = p.f("JUNC-FUSE-X"), p.f("JUNC-FUSE-Y")
    mesh.add(frame_rect(seat_x, sy * 0.36, 0, fx + 2 * rib, fy + 2 * rib,
                        min(max_z - base, fy + 2 * rib), rib))
    kx, ky = p.f("JUNC-KEY-X"), p.f("JUNC-KEY-Y")
    mesh.add(frame_rect(seat_x, sy * 0.64, 0, kx + 2 * rib, ky + 2 * rib,
                        min(max_z - base, ky), rib))
    tx, ty, tz = p.f("JUNC-XT30-X"), p.f("JUNC-XT30-Y"), p.f("JUNC-XT30-Z")
    xt30_x = sx - tx
    for yy in (sy - 3 * ty - 2 * rib, sy - 2 * ty - rib, sy - ty):
        mesh.add(frame_rect(xt30_x, yy, 0, tx, ty,
                            min(tz, max_z - base), rib * 0.65))
    _clamp_receiver(mesh, rib * 1.5, 0, 0, p, "-y")
    _clamp_receiver(mesh, min(vent_x, sx) - p.f("CLAMP-KEY-X") - rib, 0, 0, p, "-y")
    _label(mesh, "PS-15 TP", rib * 1.3, sy * 0.25, base * 0.8, p, sx * 0.44)
    _label(mesh, "DN01 OPEN", rib * 1.3, sy * 0.51, base * 0.8, p, sx * 0.46)
    _label(mesh, "DN02 OPEN", rib * 1.3, sy * 0.80, base * 0.8, p, sx * 0.46)
    _label(mesh, "R2", sx * 0.70, sy - rib * 1.8, base * 0.8, p, sx * 0.12)
    mesh.add(arrow(sx * 0.52, sy * 0.44, base * 0.8, sx * 0.34, sy * 0.10,
                   p.f("SH-ARROW-HEIGHT"), "+x"))
    mesh.add(arrow(sx * 0.42, sy * 0.20, base * 0.8, sx * 0.24, sy * 0.08,
                   p.f("SH-ARROW-HEIGHT"), "-x"))
    expected_z = max(min(xtz, max_z - base), min(max_z - base, fy + 2 * rib),
                     min(max_z - base, ky), min(tz, max_z - base), base + rib)
    return Part(
        "cad08_ps15_junction_support.stl", "CAD-08", "PS-15",
        "PS-15 diagnostic junction-block support", mesh,
        ("PS-ID TP marking", "DAT-F open L-frame", "vent/body-seat exclusion notch",
         "reversible-clamp interface", "XT60 seat", "three XT30 test seats",
         "DN-01 OPEN modular seat", "DN-02 OPEN modular seat", "mating direction arrow",
         "service-removal arrow", "R2 neighboring harness route",
         "PS-15 post placement explicitly deferred to P1",
         "open tool and finger access"),
        ("JUNC-SUPPORT-X", "JUNC-SUPPORT-Y", "JUNC-SUPPORT-Z", "JUNC-SUPPORT-BASE-Z",
         "JUNC-SUPPORT-ORIGIN-X", "JUNC-SUPPORT-ORIGIN-L", "JUNC-VENT-X-MIN",
         "JUNC-VENT-L-ABS-MIN", "JUNC-XT30-X", "JUNC-XT30-Y", "JUNC-XT30-Z",
         "JUNC-FUSE-X", "JUNC-FUSE-Y", "JUNC-KEY-X", "JUNC-KEY-Y",
         "SH-D26-Z-MIN", "SH-D26-Z-MAX",
         "CLAMP-KEY-X", "CLAMP-KEY-Y", "CLAMP-KEY-Z"),
        (sx, sy, expected_z), 0.5, "DAT-F/open-frame face on bed",
        f"assembly origin X={origin_x} L={origin_l} Z=DAT-F; geometry capped below Z={max_z}")


def _decision_blanks(p: Parameters) -> Part:
    fx, fy = p.f("JUNC-FUSE-X"), p.f("JUNC-FUSE-Y")
    kx, ky = p.f("JUNC-KEY-X"), p.f("JUNC-KEY-Y")
    gap = p.f("SH-BUILD-PLATE-GAP")
    thick = p.f("JUNC-SUPPORT-BASE-Z")
    mesh = Mesh()
    mesh.add(box(0, 0, 0, fx, fy, thick))
    mesh.add(box(fx + gap, 0, 0, kx, ky, thick))
    _label(mesh, "DN01", 0, 0, thick * 0.75, p, fx)
    _label(mesh, "OPEN", 0, fy * 0.48, thick * 0.75, p, fx)
    _label(mesh, "DN02", fx + gap, 0, thick * 0.75, p, kx)
    _label(mesh, "OPEN", fx + gap, ky * 0.48, thick * 0.75, p, kx)
    return Part(
        "cad08_ps15_dn_open_blanks.stl", "CAD-08", "PS-15",
        "PS-15 DN-01/DN-02 open-decision test blanks", mesh,
        ("DN-01 OPEN marking", "DN-02 OPEN marking", "removable diagnostic blanks",
         "no fuse choice", "no disconnect choice"),
        ("JUNC-FUSE-X", "JUNC-FUSE-Y", "JUNC-KEY-X", "JUNC-KEY-Y",
         "JUNC-SUPPORT-BASE-Z"),
        (fx + gap + kx, max(fy, ky),
         max(thick, thick * 0.75 + p.f("SH-LABEL-HEIGHT"))), 0.5,
        "flat blank faces on bed", "removable gauges only; decisions remain open")


def build_parts(p: Parameters) -> dict[str, Part]:
    parts = [
        _battery_dummy(p), _esc_dummy(p), _ubec_dummy(p, "A"), _ubec_dummy(p, "B"),
        _esp_dummy(p, "E1"), _esp_dummy(p, "E2"), _wifi_dummy(p), _amp_dummy(p),
        _servo_dummy(p), _junction_dummy(p), _battery_tray(p),
        Part("cad02_ps01_plate_clamp_foot.stl", "CAD-02", "PS-01",
             "PS-01 reversible plate-clamp foot coupon", _plate_clamp(p, "PS01"),
             ("PS-ID marking", "4 mm floor-plate jaw", "removable support key", "no chassis hole"),
             ("SH-FLOOR-THICKNESS", "CLAMP-JAW-X", "CLAMP-JAW-Y", "CLAMP-JAW-GAP",
              "CLAMP-WALL", "CLAMP-KEY-X", "CLAMP-KEY-Y", "CLAMP-KEY-Z"),
             (p.f("CLAMP-JAW-X"), p.f("CLAMP-JAW-Y"),
              2 * p.f("CLAMP-WALL") + p.f("CLAMP-JAW-GAP") + p.f("CLAMP-KEY-Z")),
             0.5, "jaw back/flat side on bed for coupon print", "reversible 4 mm plate-edge test; fit before loading"),
        _ubec_shelf(p),
        Part("cad04_ps03_plate_clamp_foot.stl", "CAD-04", "PS-03",
             "PS-03 reversible plate-clamp foot coupon", _plate_clamp(p, "PS03"),
             ("PS-ID marking", "4 mm floor-plate jaw", "removable support key", "no chassis hole"),
             ("SH-FLOOR-THICKNESS", "CLAMP-JAW-X", "CLAMP-JAW-Y", "CLAMP-JAW-GAP",
              "CLAMP-WALL", "CLAMP-KEY-X", "CLAMP-KEY-Y", "CLAMP-KEY-Z"),
             (p.f("CLAMP-JAW-X"), p.f("CLAMP-JAW-Y"),
              2 * p.f("CLAMP-WALL") + p.f("CLAMP-JAW-GAP") + p.f("CLAMP-KEY-Z")),
             0.5, "jaw back/flat side on bed for coupon print", "reversible 4 mm plate-edge test; fit before loading"),
        _post(p, "POST-HEIGHT-LOW", p.f("POST-HEIGHT-LOW")),
        _post(p, "POST-HEIGHT-MID", p.f("POST-HEIGHT-MID")),
        _post(p, "POST-HEIGHT-HIGH", p.f("POST-HEIGHT-HIGH")),
        _junction_support(p), _decision_blanks(p),
        Part("cad08_ps15_plate_clamp_foot.stl", "CAD-08", "PS-15",
             "PS-15 reversible plate-clamp foot coupon", _plate_clamp(p, "PS15"),
             ("PS-ID marking", "4 mm floor-plate jaw", "removable support key", "no chassis hole"),
             ("SH-FLOOR-THICKNESS", "CLAMP-JAW-X", "CLAMP-JAW-Y", "CLAMP-JAW-GAP",
              "CLAMP-WALL", "CLAMP-KEY-X", "CLAMP-KEY-Y", "CLAMP-KEY-Z"),
             (p.f("CLAMP-JAW-X"), p.f("CLAMP-JAW-Y"),
              2 * p.f("CLAMP-WALL") + p.f("CLAMP-JAW-GAP") + p.f("CLAMP-KEY-Z")),
             0.5, "jaw back/flat side on bed for coupon print", "reversible 4 mm plate-edge test; fit before loading"),
    ]
    by_name = {part.filename: part for part in parts}
    if len(by_name) != len(parts):
        raise ValueError("duplicate generated filename")
    return by_name
