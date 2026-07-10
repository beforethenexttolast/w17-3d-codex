# FINISHING GUIDE — from raw print to finished W17 part

Everything that happens **after** a part comes off the printer: trimming, sanding,
priming, painting, decals, clear coat, gluing, inserts, and protecting the result.

Written for a first-time finisher. Slicer settings live in `PRINT_SPEC.md`; which
material each part uses lives in `MATERIAL_DECISION_MATRIX.md`; measuring/tolerance
concepts live in `BEGINNER_3D_PRINTING_GUIDE.md`. Record what you actually did to each
part in `06_finishing/` using the "Finishing note" template from `PRINT_LOG_TEMPLATE.md`.

**Target look:** Mercedes W17 Petronas livery — black body, teal/turquoise accents,
silver nose detail, #63 (Russell) — that still survives being an RC car that crashes.

> ⚠️ **Read the consolidated safety block (§12) before your first sanding or spray
> session.** Short version: dust mask or respirator when sanding, spray only outdoors
> or with serious ventilation, gloves + eye protection by default, no ignition sources
> near solvents.

---

## 1. Surface prep fundamentals

### 1.1 Know your plastic before you sand it

| Material (our use) | Sanding behavior | Painting behavior | Watch out for |
|---|---|---|---|
| **PLA / PLA matte** (body shell, cosmetic) | Sands well but **melts at low temperature** — friction heat from power sanding or fast hand sanding gums it up | Takes primer + acrylic well | Heat: sand slowly, by hand; keep finished PLA parts out of hot cars/direct summer sun |
| **PETG** (floor, suspension, wheels) | **Gummy** — clogs paper, smears instead of cutting; hard to get a crisp finish | **Poor paint adhesion bare** — paint peels unless you scuff-sand + use a plastic-adhesion primer | Mostly leave PETG parts unpainted (they're hidden); if painting, scuff + adhesion primer is mandatory |
| **ASA** (rear hub / motor-adjacent) | Sands and finishes very well | Takes primer/paint well | **Acetone dissolves it** — that's a feature for smoothing/welding but a hazard near painted parts; ours are hidden mechanical parts, leave unfinished |

Uncertainty note: filament brands vary. Every paint/primer combination gets tested on a
**scrap or test-coupon print first** (you will have coupons from the test-print phase —
keep them, they are your paint mules).

### 1.2 Trimming and deburring (every part, 2 minutes)

Do this to *every* printed part before anything else:

1. **Remove supports and brim** by hand, then slice off stubs with a fresh hobby-knife
   blade (cut *away* from your fingers; a dull blade is more dangerous than a sharp one).
2. **Deburr holes and edges** — a deburring tool or a twist of a larger drill bit by
   hand removes the "elephant foot" flare at the bottom edge and crumbs inside holes.
3. **Check mating faces** — drag a fingernail across surfaces that touch other parts;
   any bump you feel will misalign the assembly. Flat-sand those faces on sandpaper
   taped to glass/tile (move the part, not the paper).

### 1.3 Sanding: the grit ladder

Coarse grits shape, fine grits polish. Skip more than one step and you'll chase
scratches forever.

| Grit | Use | Stop here if… |
|---|---|---|
| 120 | Knock down support scars, seams, big layer steps | never (too coarse to leave visible) |
| 240 | Remove 120 scratches, general layer-line leveling | part is hidden mechanical (Workflow A) |
| 400 | Pre-primer smoothing | going to filler primer (it fills the rest) |
| 600 | Between primer coats (wet) | ready for color coats |
| 800–1000 (optional) | Between color/clear coats for a show finish | you're happy |

- **Wet sanding** (dip paper in water, sand wet) from 400 up: suppresses dust, stops
  clogging, gives a better surface. Use waterproof (usually black) paper. Dry the part
  fully before any spraying.
- **Dry sanding** below 400: wear a mask, work over something you can wipe clean.
- **Support scars:** 120 → 240 locally, then blend outward so you don't sand a dish
  into the surface. On visible bodywork it's better to have avoided supports there in
  the first place (see `PRINT_SPEC.md` on orientation).
- **PLA rule:** slow strokes, light pressure, no power tools. If the surface starts
  looking shiny/smeared, you're melting it — slow down.

---

## 2. Primer

### 2.1 Filler primer vs regular primer

- **Filler primer** (a.k.a. high-build primer, "primer filler"): thick, sandable spray
  that **fills layer lines and fine scratches**. This is the single biggest cheat for
  making a 3D print look injection-molded. Workflow: spray 2–3 coats → wet-sand 400/600
  → repeat once if lines still show.
- **Regular primer**: thin uniform base that gives paint something to grip and shows
  defects. Use as the final layer before color, or alone on parts that are already smooth.
- **Plastic-adhesion primer** ("plastic primer", adhesion promoter): required on PETG,
  helpful on everything. If a rattle-can says "for plastics," that's the one you want.

### 2.2 Spray-can technique (applies to primer, paint, and clear)

1. Can at room temperature; shake **2 full minutes** after the ball rattles.
2. Part clean and grease-free: wash with dish soap + water, dry, then a quick wipe with
   isopropyl alcohol (IPA). Don't touch the surface afterwards — hang it on wire or pin
   it to a cardboard turntable.
3. Distance **20–30 cm**, moving passes that **start and end off the part** — never
   pull the trigger while aimed at the part.
4. **Several thin coats beat one wet coat.** Each pass should look slightly under-done.
5. **Flash time** between coats: 5–15 min (read the can). Full recoat/sand window:
   usually 1 h or after 24–48 h — respect it, or the next coat can wrinkle the last one.
6. Ambient: 15–25 °C, low humidity, no wind (outdoors: pick a calm dry day).

### 2.3 Spot putty for seams

The body prints in front + rear sections. After joining (see §7), skim the seam with
**one-part spot/glazing putty**, let it dry, sand 240 → 400, then filler-prime. Repeat
thin rather than applying thick. Putty is for scratches and seams, not for sculpting.

---

## 3. Painting the W17

### 3.1 Rattle-cans, not airbrush (for now)

Recommendation: **spray cans for the whole first car.** An airbrush gives finer control
but adds a compressor, paint thinning ratios, cleaning discipline, and a new failure
mode to a first-ever paint job. Cans of primer + gloss black + teal + silver + clear
will do this livery justice. Revisit airbrushing for car #2.

### 3.2 Paint chemistry, one paragraph

Over a proper primer coat, **acrylic** spray paint is the beginner-safe default: mild
solvents, forgiving, widely available. **Lacquer** dries fast and hard but its hot
solvents can attack plastics and *other paint layers* — only over full-cured primer,
always test. **Enamel** is tough but slow-curing and unfriendly to recoat timing. Rule
that replaces all theory: **same-brand system (primer → color → clear) tested on a
scrap print** = no nasty surprises. Water-based acrylics (brush or spray) are the
safest chemistry of all for small details.

### 3.3 The black body: why you still paint it

The shell prints in black PLA already. You *can* leave it bare (Workflow C does), but
primer + gloss black paint is what makes it stop looking 3D-printed: filler primer
kills the layer lines, and sprayed gloss black is far deeper and more even than any
filament surface. Skip the base coat only where the part is barely visible or you've
chosen durability-over-looks for that part.

### 3.4 Livery sequence (light → dark is easier, but here base is dark)

1. **Gloss black base** over primer, 2–3 thin coats, cure per can (usually 24–48 h
   before masking on it — tape on soft paint = ruined base).
2. **Mask for teal accents** (see §4): the W17's teal runs along the lower sidepods,
   floor edge, front-wing elements and mirrors. Work from your reference photos in
   `08_reference_photos/`.
3. **Teal/turquoise coat** in the exposed areas, 2 thin coats. Pull tape carefully.
4. **Silver nose detail**: for small areas, brush-paint acrylic silver or use a silver
   paint marker — masking + spraying tiny zones is where beginners make runs.
5. **Fixing runs:** stop, let it cure fully (days, not hours), wet-sand the run flat
   with 600–800, re-spray that panel. Never dab wet paint.

Uncertainty: exact W17 teal shade — match by eye against photos; "Petronas teal" style
shades exist across brands. Test card in daylight before committing.

---

## 4. Masking

- Use **proper masking tape** (automotive/painter's, or washi tape for tight curves) —
  never packing/office tape (bleeds, lifts paint).
- **Burnish the edge** (rub it down with a fingernail or soft tool) — that edge is the
  paint line you'll see.
- Spray **away from the tape edge**, not into it, in the lightest coats of the job.
- **Pull tape at a 45° angle, slowly**, when the last coat is touch-dry (not fully
  cured, not wet) — the cleanest lines come from pulling neither too early nor days late.

### 4.1 The hard rule: paint never touches mechanical interfaces

Mask (or paint before assembly and keep clear) **all** of:

- bearing seats and bearing bores
- screw holes, self-threading holes, and heat-set insert holes
- locating pins and pin sockets (body mounting pins!)
- tyre-mating surfaces on rims and the tyre-slot adapters
- belt path, gear teeth areas, axle bores
- any face that slides or clamps against another part

Paint thickness (~0.05–0.15 mm across a few coats) is real: a painted pin no longer
fits its painted socket. When in doubt, plug holes with tape or silicone earplug bits
before spraying.

---

## 5. Decals

### 5.1 Waterslide decals, start to finish

Waterslide paper = the model-kit standard; thinnest, most paint-like result.

1. **Design** the artwork: PETRONAS-style wordmarks, #63, sponsor-style marks, scaled
   to the printed body. Design in Inkscape/affinity from reference photos — **this is a
   you task**; measure the body panel with calipers and lay out at 1:1. (I can't
   confirm any ready-made licensed W17 1/10 decal set exists — treat buying one as
   "search and verify," not a plan.)
2. **Print** on waterslide paper matching your printer: **inkjet paper for inkjet,
   laser paper for laser** — they are not interchangeable.
3. **Seal inkjet prints** with 2–3 light coats of clear acrylic (inkjet ink is
   water-soluble — unsealed decals dissolve in the water bath). Laser prints usually
   still benefit from one sealing coat. Dry fully.
4. **Cut** each decal close to the artwork edge.
5. **Soak** 15–30 s in room-temperature water until the film starts sliding on its
   backing.
6. **Slide** onto the (gloss, clean) surface, position with a wet soft brush, wick
   water from under it with paper towel from center outwards. No air bubbles.
7. **Setting solution** (Micro Set / Micro Sol type): Set under the decal helps
   adhesion; Sol on top softens the film so it snuggles over curves. Don't touch a
   Sol-wet decal — it looks wrinkled, then dries flat.
8. **Dry 24 h**, then **seal under clear coat** (§6) or it will not survive handling,
   let alone driving.

**The white problem:** inkjet printers have no white ink — anything white in the design
comes out transparent. On our black body that matters. Options: design decals that are
teal/silver only; buy **white or light-colored waterslide base paper** and cut close;
use a laser printer with white toner (rare); or use vinyl for the white elements.

### 5.2 Alternatives to waterslide

- **Printable vinyl / vinyl stickers**: thicker edge but robust and beginner-proof;
  good for the big #63 numbers. A craft cutter (Cricut-type) makes crisp shapes, or
  order custom-cut vinyl online.
- **Dry transfers**: crisp, thin, but limited stock designs and one-shot application.
- **Paint + mask**: for simple shapes (stripes), masking beats decals on durability.

Start with: vinyl for large/white elements, waterslide for fine multi-color logos.

---

## 6. Clear coat

- **Look:** modern F1 bodies read as **gloss**; gloss also gives waterslides the best
  surface. Satin hides surface imperfections better if the paint job came out uneven.
  Matte reads "prototype/carbon" — use deliberately.
- **Chemistry:** use **acrylic clear over waterslide decals** — hot lacquer clears can
  wrinkle or eat decal film. Same-brand-as-paint is safest; test on the coupon that
  carries a test decal.
- **Application:** 2–3 thin coats. First coat over decals extra-light ("dust coat") to
  lock them down before wetter coats.
- **Cure before handling:** touch-dry in an hour, but wait **48 h+ before gripping,
  masking again, or assembling**, and a week before judging final hardness.
- Electric RC = no nitro fuel, so no fuel-proofing needed; the enemies are hands,
  gravel rash, and UV. Gloss acrylic clear handles all three acceptably; expect battle
  scars anyway.

---

## 7. Gluing printed parts

| Glue | Strengths | Weaknesses | Use here for |
|---|---|---|---|
| **CA (super glue)** + optional activator | Fast, precise, great on PLA | **Brittle** under impact/vibration; **fogs/blooms** white near clear or glossy surfaces | Small cosmetic parts, tacking before epoxy |
| **2-part epoxy (5–30 min)** | Strong, gap-filling, some flex, sticks to everything | Slow, messy, needs clamping | **Structural joins: body front↔rear seam, wing mounts** |
| **Acetone-based cement** | True solvent **weld on ASA/ABS** | Does nothing permanent on PLA/PETG; attacks paint | ASA-to-ASA only (we barely need it) |

- Nothing solvent-welds PLA or PETG properly — mechanical bond (epoxy, CA) or screws.
- **Surface prep:** scuff both faces 240 grit, wipe with IPA, dry. Glue on glossy paint
  = glue on nothing, so glue **before** painting or mask glue lands.
- **Increase glue area** when possible: print/insert a backing strip behind a butt
  joint instead of gluing edge-to-edge.
- **When to use screws instead:** anything you'll disassemble (body off chassis,
  electronics access), anything highly loaded that a printed joint + glue can't take,
  and anywhere the original design already has screw bosses — don't glue what was
  designed to unscrew.

---

## 8. Threaded inserts and fasteners (finishing-stage rules)

Full insert technique is in `BEGINNER_3D_PRINTING_GUIDE.md`; at finishing time:

- **Install inserts after painting** (or mask the holes) — a painted insert hole is
  undersized and the paint burns when the hot insert goes in.
- **Thread-locker (blue/medium):** metal-to-metal joints near motor vibration only
  (motor mount screws, grub screws). **Never on or into plastic** — it can attack some
  plastics and you'll never service it.
- **Nylock nuts** wherever a nut can vibrate loose (suspension pivots, wheel-adjacent).
- **Torque discipline:** snug + an eighth-turn. Plastic threads strip exactly one
  quarter-turn after "one more for luck." Into inserts you may go slightly firmer; into
  self-threaded plastic, gentler.

---

## 9. Weatherproofing and protecting electronics

- Printed PLA/PETG/ASA parts shrug off splashes; **PLA dislikes sustained heat + sun**
  more than water (don't leave the car on a dashboard). Painted + cleared surfaces are
  effectively sealed anyway.
- The **electronics** are the wet-weather limit, not the plastic — treat this car as
  dry-weather until the electronics side says otherwise (conformal coating and sealing
  are the firmware/electronics repos' domain, not this guide's).
- During finishing work: **electronics and finishing never share a table.** Sanding
  dust is conductive-ish grit in bearings and switches; overspray wrecks connectors.
  Mask every opening (camera bore, wire pass-throughs, vents) whenever a part with
  electronics nearby gets sprayed — ideally, all painting happens before electronics
  installation.

---

## 10. Realism vs crash durability

An F1 body is thin winglets and sharp edges; an RC car is a crash machine. Decide
**per part, before finishing it**:

- **Beauty-first parts** (display-quality paint, fine decals): top body, halo,
  mirrors, driver area. Accept that a wall hit breaks them; finish accordingly.
- **Durability-first parts** (skip fine finish, maybe thicker print): front wing —
  it *will* hit things first. Keep its finish simple so reprints don't hurt.
- **Sacrificial mounting:** where the design allows, mount fragile aero on pins or
  light glue joints that **pop off instead of snapping the part** (a mirror that
  disappears into the grass beats a mirror stub). Don't epoxy fragile winglets to the
  body if they can pin on.
- **Print spares before painting session #1:** front wing ×2, mirrors ×2, small
  winglets ×2 — paint them in the same session so replacements match.
- Wings/end-plates in matte finishes hide scuffs better than gloss; consider satin
  clear on the front wing even if the body is gloss.

---

## 11. Three beginner-safe workflows

### Workflow A — Quick functional finish (hidden chassis/mechanical parts)

*Floor, mounts, hubs, suspension, anything invisible.*

**Materials:** hobby knife, deburring tool, 240 grit, calipers.

1. Remove supports/brim; slice off stubs.
2. Deburr every hole and edge; test-fit bearings/screws (see fitment workflow in
   `BEGINNER_3D_PRINTING_GUIDE.md`).
3. Flat-sand only mating faces that rock or wobble.
4. Done. **No paint on mechanical parts.** Log it in `06_finishing/` (one line is fine).

### Workflow B — Realistic painted body finish (the W17 shell)

*Body front + rear, nose, halo, mirrors, wings you want pretty.*

**Materials:** grits 240/400/600 (wet-dry), spot putty, filler primer, plastic primer,
gloss black, teal, silver acrylic (marker or pot), waterslide/vinyl decals, acrylic
gloss clear, masking tape, IPA, gloves, mask, epoxy (for the seam).

1. Deburr; dry-fit front↔rear body; epoxy the seam if they join permanently (§7); cure.
2. Sand 240 → 400 overall; spot-putty the seam and defects; re-sand.
3. 2–3 coats **filler primer**; wet-sand 400 → 600; repeat once if layer lines show.
4. 1–2 coats regular/plastic primer; wet-sand 600 lightly.
5. 2–3 thin coats **gloss black**; cure 24–48 h.
6. Mask; 2 coats **teal** accents; pull tape at touch-dry; cure.
7. Brush/marker **silver** nose details.
8. Apply **decals** (§5); dry 24 h.
9. 2–3 coats **acrylic gloss clear** (first coat a dust coat); cure 48 h+.
10. Unmask interfaces, install on car. Photograph for `08_reference_photos/`, log in
    `06_finishing/`.

*Elapsed calendar time: about a week — the cures, not the work, set the pace. Don't
compress cures; that's how paint jobs wrinkle.*

### Workflow C — Durable outdoor/RC finish (driver-spec, not show-spec)

*A car you'll actually thrash. Same steps, fewer of them, tougher choices.*

1. Workflow A mechanical prep on everything.
2. Body: sand 240 → 400, skip putty perfection; one filler-primer round only.
3. Color: black stays **bare black PLA or one black coat**; teal as **vinyl stripes**
   instead of masked paint (vinyl peels instead of chipping, and re-sticks).
4. Numbers/logos: vinyl stickers.
5. **Satin acrylic clear**, 2 coats, everywhere except mechanical interfaces.
6. TPU and flexible parts: **leave unpainted** (paint cracks off flexing parts).
7. Keep the unpainted spare wing set in the pit box.

---

## 12. Consolidated safety block

**Defaults for every finishing session: nitrile gloves, safety glasses, ventilation,
no food/drink at the bench, wash hands after. Keep everything here away from kids and
pets, including "empty" cans and used rags.**

- **Sanding dust (PLA/PETG/ASA/putty/primer):** fine plastic dust does not belong in
  lungs. Wear at minimum a well-fitting **FFP2/N95 dust mask** for dry sanding; prefer
  **wet sanding** (≥400 grit) which suppresses dust almost entirely. Wipe surfaces with
  a damp cloth, don't blow dust into the air. Primer/putty dust counts double.
- **Spray paint, primer, clear coat:** solvent aerosols. **Spray outdoors** or in a
  doorway-draft setup with the part outside; for anything more than an occasional can,
  use an **organic-vapor respirator (A1/OV cartridge)** — a dust mask does nothing
  against solvent fumes. No smoking, flames, water heaters, or sparks anywhere near;
  aerosols are flammable. Don't puncture or heat cans; let empties gas off outdoors.
- **Solvents (IPA, acetone):** skin-drying, eye hazard, **highly flammable**. Small
  amounts on a cloth, capped bottles, away from ignition. Acetone additionally
  dissolves ASA parts and most paints — and CA activator is basically solvent too.
- **CA glue:** bonds skin in seconds (that's its party trick) — nitrile gloves, never
  wipe a spill with bare fingers, keep debonder or acetone nearby *for skin only,
  never eyes*. Eye contact = rinse and medical help. CA fumes irritate eyes/nose —
  ventilate; large CA + cotton contact can generate heat.
- **Epoxy and fillers/putty:** skin sensitizer with repeated contact — gloves every
  time; sand only after full cure (uncured dust is the nasty kind).
- **Heat-set inserts / hot tools:** soldering iron at ~200 °C+ — burns happen at the
  *other* end of the part too (heat travels). Work on a non-flammable surface; don't
  breathe the wisp of overheated-plastic fume, especially from ASA (styrene) — that
  wisp means you're too hot anyway.
- **Printer itself:** nozzle runs ~200–300 °C, bed up to ~110 °C — hands out during and
  right after printing; ASA printing needs the enclosure closed and the room ventilated
  (styrene odor = increase ventilation).
- **Rag disposal:** rags soaked with oil-based products (some enamels, oils, certain
  primers) can **self-heat and ignite** in a wad. Dry them flat outdoors, then bin, or
  store in a sealed metal container with water. Water-based acrylic rags are safe —
  but the habit costs nothing.
- **Cutting/trimming:** fresh blades, cut away from yourself, part braced on the
  bench not your palm. Most hobby blood is donated to dull hobby knives.

---

*When you finish a part, log it: `06_finishing/FIN-<part-name>.md` (template in
`PRINT_LOG_TEMPLATE.md`), plus a photo in `08_reference_photos/`. Future-you repainting
a crashed wing will want to know exactly which teal that was.*
