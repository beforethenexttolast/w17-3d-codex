# Camera + gimbal placement — requirements and trade study

**Status: requirements + trade study. The placement decision is OPEN (owner call).**
Date: 2026-07-14. This file is the **source of truth for camera/gimbal placement**.
`FIRST_PRINT_DECISION.md`'s camera-mount checklist points here; do not fork the decision
into a second document. The firmware/control side of the gimbal lives in
`w17-control-fw` (see cross-links at the end) — this repo decides only the mechanical
mount and placement.

## What is being placed

The FPV camera (SSC338Q + IMX335 + WiFi module) on a 2-axis MG90S pan/tilt gimbal,
driven today by the transmitter right stick via CRSF ch9/10 (fully implemented and
bench-noted in `w17-control-fw`). The long-term goal is VR-style driver-POV FPV
(iPhone in an Esperanza Shinecon EMV400 headset), which raises placement requirements
beyond "the lens sees the road" — see §3.

## 1. The two candidate placements

| | Option A — cockpit / driver-seat | Option B — halo-height pod |
|---|---|---|
| POV | True driver POV — best VR immersion | Elevated, slightly detached POV |
| Halo occlusion | **Risk: `new halo 2.1` may occlude a large part of the view** (the deciding check) | Above the halo — clean sightline |
| Pan clearance | Cockpit side walls may mechanically limit pan throw → smaller usable endpoints → less useful edge panning for head tracking | More clearance, wider usable endpoints |
| Existing printed-part fit | Sits within the cockpit opening; interacts with seat/body parts | `camera top 1.1` pod already exists as a Rev-1-era candidate (`BUILD_SHEET.md:20`) |
| VR comfort | Strong ground-rush motion cues at seat height (possible comfort penalty, unproven) | Weaker ground rush; possibly more comfortable, less "driver" |
| CG | Camera mass low and central-ish | Mass higher up — worse CG |

Decision rule proposed: **Option A unless the halo-occlusion check fails**, mirrored from
the owner's stated preference; the occlusion check is a dry-fit with the printed halo
before committing.

## 2. Baseline engineering requirements (either option)

- **Power:** camera + WiFi module stay on clean **Rail A**; the gimbal servos are on
  **Rail B** with the other servos (`w17-control-fw/docs/bill_of_materials_v2.md:177`).
  Placement must not force a servo lead across the rails.
- **Cooling:** the PETG `camera_blower_duct.scad` duct (fully parameterized, 9 "MEASURE
  THESE" dimensions — see `FIRST_PRINT_DECISION.md`) must reach the camera at the chosen
  position; blower is in transit.
- **Wiring:** run length back to the mid-bay ESP32 #1 (pan GPIO19, tilt GPIO23) and
  strain relief across the moving gimbal axes.
- **Serviceability:** camera removable without destroying the mount; no clamping stress
  on the lens barrel (grip board/heatsink) — same constraints as the
  `FIRST_PRINT_DECISION.md` camera-mount checklist.
- **Servo travel:** full MG90S horn travel must be mechanically clear or deliberately
  hard-stopped — see §4.

## 3. VR-specific requirements (these are new — the VR plan depends on them)

1. **Level horizon / roll alignment.** The iPhone VR client deliberately never
   roll-corrects the video (Codex VR plan: "head yaw, pitch, and roll never transform the
   displayed video"). A camera mounted with even a small roll error is a **permanently
   tilted horizon inside the headset** — a first-order nausea risk. The mount needs either
   precise roll alignment by construction or a small roll-trim adjustment.
2. **Stiffness / vibration.** Head-tracked VR magnifies mount wobble and rolling-shutter
   jello. Prefer stiff, short load paths; avoid cantilevered single-wall towers; consider
   soft-mounting the camera board itself (not the gimbal frame).
3. **Boresight.** Gimbal mechanical center must equal the car's straight-ahead. CRSF 992
   is the authoritative *commanded* center; the mount must make "992 = looking straight
   down the nose" true by construction or by trim.
4. **FOV interaction.** Record the camera lens FOV at the chosen position; the body/halo
   must not intrude into it at gimbal center, and the usable pan/tilt range should be
   chosen so the lens edge never stares into bodywork.

## 4. Hard-stop geometry feeds the firmware safety gate (blocker 1)

The measured mechanical limits of the finished mount become the per-axis `gimbalConfig`
servo endpoints in `w17-control-fw` — blocker 1 of the head-tracking safety gate
(`w17-control-fw/project-review/iphone_pan_tilt_firmware_readiness.md §8.1`). Today the
firmware runs full-throw defaults (500–2500 µs); a saturated head-tracking signal against
an unmeasured hard stop can stall an MG90S. Therefore, deliverables from the print side:

- physical pan/tilt hard-stop angles (or "no stop within servo throw") per axis;
- the degrees-of-travel per axis actually usable at the chosen placement;
- confirmation the mount survives a servo stall at the stop (or that stops are outside
  servo throw entirely).

Measurement itself is **powered-bench work, gated behind A2 closure + Phase B approval**
(`w17-control-fw/project-review/head_tracking_unlock_plan.md` step U3) — the print side
only has to make the geometry measurable and documented.

## 5. Open questions for the print side

- Does `new halo 2.1` occlude the Option-A sightline at gimbal center? (deciding check)
- Does `camera top 1.1` still fit Option B, or does the duct/mount replace it?
- Where does the blower duct attach in each option?
- Can roll trim (§3.1) be built into the mount cheaply?

## Cross-links

- `FIRST_PRINT_DECISION.md` — camera-mount design constraints + duct source notes
  (placement *decision* lives here, constraints live there).
- `w17-control-fw/project-review/head_tracking_unlock_plan.md` — unlock sequencing; U3
  consumes §4's geometry.
- `w17-control-fw/project-review/iphone_pan_tilt_firmware_readiness.md` — firmware
  readiness + blockers.
- `w17-control-fw/docs/bill_of_materials_v2.md` — power rails, camera/WiFi wiring.
