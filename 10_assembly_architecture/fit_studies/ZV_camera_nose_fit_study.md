# ZV · Camera, nose/pod and cooling fit study

Date: 2026-07-23  
Scope: OpenIPC SSC338Q camera, `camera top 1.1`, legacy nose-camera prints,
5 V 20 mm blower and the parametric duct. Gimbal servos are detailed in ZA.

---

## 1. Recommendation

**Do not place the primary camera in the visible nose and do not emit camera
mount/duct STL.** The verified P0 nose sections show protected enclosed volume
only in the already-occupied rear installation ring: about 39–47 mm wide,
29–32 mm high and 40 mm long (**DERIVED**). Forward of it the underside is
open and the tip is effectively solid. This is not a protected camera bay.

Retain cockpit Option A as the preferred fit candidate because it is lower,
forward, better for driver POV and improves the D-30 front percentage by about
1.9 points versus the high airbox pod (**DERIVED from ASSUMPTION mass**).
Option A still needs the halo/FOV and full gimbal sweep tests. Option B remains
the fallback if the halo blocks Option A.

The user now names SSC338Q+IMX415; the repo's latest physical note says
SSC338Q+IMX335 while frozen BOM/atlas copies say IMX415. Board/heatsink/lens
dimensions—not sensor marketing—control the mount, but identity must be
photographed and recorded before design.

## 2. Datums and confidence

- DAT-F and S0 follow the index.
- Nose cavity sections are **DERIVED** from registered STL sections.
- Raw candidate-print bboxes are **VERIFIED**.
- `camera top 1.1` shares the rear-shell authored frame. Its vehicle envelope
  X=−61.6…−44.8, L=−8.8…+8.9, Z=73.35…80.27+S0 is **DERIVED** using
  X=146.6−raw_x, L=−(raw_y−1.855), Z=raw_z+S0.
- Camera body, blower depth/outlet and both option coordinates remain
  **ASSUMPTION**.

## 3. Envelopes and candidate prints

| Item | Body / raw bbox | Confidence | Finding |
|---|---:|---|---|
| SSC338Q camera | PCB/heatsink/lens/cable TO MEASURE | ASSUMPTION | no guessed dummy allowed |
| `camera top 1.1` | 16.75×17.72×6.92 mm | VERIFIED | exterior cover only; cannot prove board capacity |
| `cameranose` | 5.8×10.5×9.8 mm | VERIFIED | legacy/decorative candidate, no hardware interface proven |
| `camera 2 colour` | 26.3×14.9×12.6 mm | VERIFIED | legacy candidate, gated |
| `f104camera` | 26.3×15.0×10.8 mm | VERIFIED | legacy candidate, gated |
| blower | 20×20 face; depth/outlet unknown | DOCUMENTED / ASSUMPTION | inlet, collar and lead required |
| duct defaults | 20×8 collar; 18 mm transition; 1.4 wall | ASSUMPTION | source explicitly calls them placeholders |

The camera-board envelope must separately record PCB W/H/T, heatsink, total
lens depth/diameter/offset, holes, connectors and service pull.

## 4. Placement, FOV and moving clearances

| Option | Candidate datum | Confidence | Fit statement |
|---|---|---|---|
| A cockpit | X≈+60, L=0, module base Z≈20 | ASSUMPTION | open roof; halo/body FOV and pan sweep unresolved |
| B high pod | X≈−53, L=0, Z≈73+S0 | ASSUMPTION anchored to DERIVED cover | highest/rearward mass; cover far smaller than reserved gimbal |
| nose | rear ring near nose X≈183…187 | DERIVED cavity / rejected placement | ring already holds beam/tab/bolt; forward cowl not enclosed |

Reserve a 55×45×60 gimbal module only as an **ASSUMPTION** planning envelope.
At all usable pan/tilt angles require the lens barrel and FOV cone clear the
halo/body, with ≥5 mm static structure clearance. Servo horns/links require
≥8 mm to fixed shell/mounts. The mount needs roll trim; the centred optical axis
must align with X+ and remain level.

## 5. Cooling and thermal clearance

The SCAD source has nine required measurements: blower outlet W/H, blower-face
W/H, collar depth, camera-mouth W/H and duct length, plus fit/wall decisions.
Defaults are not production evidence.

- Blower uses decoupled **Rail B**; camera and Wi-Fi stay on **Rail A**.
- Air enters an unobstructed blower inlet, crosses the actual heatsink/hot side
  and exits into the derived rearward chimney. Recirculation into the inlet fails.
- Duct grips blower outlet and a board/heatsink support—never the lens barrel.
- PETG is the starting duct material. D-19 decides whether hotter material is
  needed; no PLA load-bearing duct against a hot camera.
- Record camera/heatsink inlet/outlet temperature and airflow tell-tale with
  body on. Stop for temperature rise, softened mount or stalled blower.

## 6. Mounting, fasteners and cables

- Common PS-10 base accepts Option A or B without modifying the donor shell.
- M3×5 inserts are allowed only in the new repeatedly serviced module base;
  use M3×8/10 as proven by boss depth. No screw may bear on PCB or lens.
- Board has compliant pads plus positive edge restraint; optical roll trim is
  mechanical and lockable.
- Camera power/USB, pan, tilt and blower use one strain-relieved module umbilical.
  Provide loops at both moving axes without entering the FOV or horn sweep.
- CN-16 or the documented combined-module fallback must let the camera come out
  without cutting wires. U.FL remains on the deck, not the moving gimbal.

## 7. Mass and CG

Camera+blower+two MG90S+mount is 55–85 g (**ASSUMPTION**). At Option A X=+60
the D-30 midpoint is 35.0% front. Moving the same mass to the derived cover
centre X≈−53.2 and an assumed group Z=70 at S0=0 drops it to 33.2% front and
raises whole-car Z-CG from 22.2 to 23.2 mm. Thus Option A is the
mechanical/balance preference if FOV and sweep pass; the result is not a claim
that the 36–40% assumed target is already met.

## 8. Assembly and fit gates

1. Photograph both camera sides and sensor/board markings; close IMX identity.
2. Caliper every D-06 field and weigh the assembly.
3. Caliper blower face/depth/outlet/inlet/holes and lead.
4. Place measured dummies at A and B with printed halo/body; record centred FOV,
   roll, pan/tilt hard contact and service pull.
5. Owner chooses A/B only after that comparison.
6. Parameterize the nine duct fields from measurements; print a labelled
   diagnostic duct only.
7. Prove airflow/temperature and module removal before any production STL.

## 9. Remaining assumptions / stop conditions

Stop if sensor identity remains ambiguous, the lens touches/clamps, the halo
enters centred FOV, a servo stalls on bodywork, a wire crosses the optical path,
the blower inlet is masked, hot exhaust recirculates, or camera removal needs
desoldering at the car. Legacy camera prints remain uncertain and unprinted
unless the measured module proves their interface.
