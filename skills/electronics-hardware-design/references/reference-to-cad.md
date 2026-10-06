# Physical reference to parametric CAD

Use this workflow to reconstruct a board, enclosure, plate, or mating interface from an available specimen. Start with a flat support, calipers/ruler, annotated photos, and a simple fixture. Add camera, depth sensing, or a motion stage only where it reduces capture effort or reaches otherwise inaccessible features.

## Workflow map

1. Define the fit decision and specimen.
2. Establish datums and capture priorities.
3. Capture with suitable tools.
4. Register captures in a shared coordinate frame.
5. Bound uncertainty and tag confidence.
6. Cross-check critical geometry.
7. Hand off to parametric CAD and test the fit.

## 1. Define the fit decision and specimen

- Identify the specimen/revision, assembly state, removable parts, damage, and intended mating parts. Link existing drawings, datasheets, and native CAD; preserve their authority and explain discrepancies.
- State the needed decision: hole alignment, port opening, stand-off height, insert clearance, outer envelope, or cosmetic shape. Set an acceptable error from the available fit margin before choosing equipment.
- Measure the assembled state relevant to fit. Include solder, pins, jumpers, switch travel, plugged-in connectors, and cable/tool access where they constrain the design.
- Treat a measured specimen as evidence about that specimen. Obtain manufacturer limits or inspect additional units before claiming interchangeability or production variation.

## 2. Establish datums and capture priorities

- Choose repeatable, functional surfaces: datum A as the seating plane defining Z=0; datum B as a straight edge or 2 hole centers defining X; datum C as a corner, hole center, or stop fixing the origin along X. Define a right-handed frame with an annotated photo, explicit mm, +X/+Y/+Z, and the viewing side.
- Support a PCB on repeatable pads or stand-offs without bending it or resting on components. Do not use a rounded case edge, loose cable, or sloping cosmetic face as a datum when a functional interface is available.
- Measure positions from the shared datum rather than chaining edge-to-feature distances. If a datum is irregular, record how its line/plane was fitted and the observed deviation.
- Plan top/bottom/side captures around the same frame. Re-register after moving the specimen; do not silently mirror bottom-view coordinates.

| Feature / decision | Required capture | Permitted inference |
| --- | --- | --- |
| Mounting hole centers, spacing, slot limits | Contact caliper/pin measurements or a calibrated contact stage; cross-check pattern | Derive centers from measured opposing edges and diameter; retain the derivation |
| Board/plate thickness, seating heights, bottom projections | Contact thickness/depth/height measurement at the relevant locations | Derive a stack only from individually measured or authoritative dimensions |
| Connector mating plane, body extent, switch reach | Contact/depth measurement where accessible plus exact part drawing; inspect in the mating state | Use authoritative maxima for the identified part, after checking placement |
| Fastener/insert seat, hole diameter, pocket depth, wall thickness | Contact/depth measurement or suitable gauge; test actual hardware | Use nominal thread/insert geometry only after identifying the hardware |
| Outer silhouette, reliefs, cosmetic curves | Scaled planar photo or depth capture | Fit lines/arcs/symmetry as explicitly inferred geometry |
| Hidden or inaccessible feature | Alternate setup, disassembly if authorized, or authoritative source | Keep a bounded estimate provisional; add access/clearance or a closure measurement |

Treat a ruler reading as a manual direct measurement with its actual error bound. Require contact probing or caliper/gauge verification for tight fit-critical features; allow optical capture to locate candidates. If contact is impractical, document a validated alternative with enough accuracy for the fit budget. Never convert apparent symmetry or familiar screw size into a measured value.

For holes, use fitted pins where available: equal-pin outside span minus pin diameter gives center spacing; inside gap plus pin diameter gives the same spacing. Include pin clearance and diameter error. Avoid locating a center from a burred rim or a single visible edge.

## 3. Capture with suitable tools

| Tool | Practical role | Setup and limits |
| --- | --- | --- |
| Manual calipers, depth rod, pins, ruler | Establish critical dimensions and validate automated capture | Clean/zero, check a known size near the working range, use light consistent contact, record approach and access limits |
| RGB camera | Annotate features; recover planar outlines and approximate centers | Fix focus/zoom and camera, use diffuse light, include a checked scale/fiducials in the feature plane, correct lens distortion if material |
| ToF/depth camera | Find broad height envelopes, raised parts, and regions worth probing | Check minimum range and behavior on the actual surfaces; reject mixed edge pixels, holes, glare, and invalid returns; verify against known heights |
| Contact probe on an XYZ stage | Automate accessible points/heights and repeat measurements | Check stage scale, squareness, backlash, tip offset/radius, trigger direction, and contact repeatability; fixture the specimen securely |

- For planar camera measurements, rectify perspective using at least 4 well-spread coplanar fiducials with known coordinates. Verify scale at an unused known span. A planar transform cannot correct features at different heights; capture those in their own plane or measure them by contact.
- Record images/depth frames before filtering. Keep acquisition settings and a checked reference span/step. Do not treat pixel size, sensor resolution, or a vendor accuracy figure as the achieved accuracy of the setup.
- Validate a cheap ToF sensor on representative dark, shiny, narrow, and sloping surfaces. Use it for fit dimensions only after demonstrating a suitable bound at the working distance; averaging cannot remove systematic surface bias.
- Use a BLTouch-style probe for accessible, supported surfaces along its qualified approach direction. Do not assume it measures side walls, hole diameters, or sub-mm XY coordinates. Guard travel, use slow contact and low force, and verify every automatic move can avoid components and exposed conductors.
- Use a turntable for coverage of outer surfaces; capture its axis and angle and register each pose. Use XYZ motion when controlled contact locations/heights are required. Begin manually if a stage would take longer to qualify than measuring the needed features.

## 4. Register captures in a shared coordinate frame

- Keep raw sensor/stage coordinates separate from object coordinates. Record units, axis order/sign, origin, datum definition, and each sensor-to-object transform with the capture/setup ID.
- For 3D registration, use at least 3 well-spaced non-collinear corresponding landmarks with enough observations to establish the functional plane and axis. Prefer extra landmarks for checking the fit. Use a rigid transform after scale calibration; do not distort or rescale measured geometry to force agreement.
- For planar camera registration, retain the image-to-plane mapping and the plane's object-frame pose separately. For a turntable or a flipped board, solve the new pose from visible landmarks instead of relying on commanded angles alone.
- Measure an unused check landmark/span after registration. Record residuals at fitted landmarks and the independent check error, including where it lies relative to the measured features. Low residuals near the fiducials do not establish accuracy far away.
- Re-capture datums after re-fixturing or drift. Stop merging datasets if checks exceed the relevant error budget. Keep failed captures with rejection reasons rather than averaging misregistered data.

## 5. Bound uncertainty and tag confidence

- Take at least 3 independent readings of each critical feature, releasing/reseating the tool between readings. For an automated setup, repeat after re-homing or re-fixturing at least once. Record raw values and min/max; increase repetitions or change method if readings disagree enough to affect fit.
- Separate repeatability from likely bias: instrument scale/zero, jaw or probe contact, lens/perspective, surface-dependent depth bias, stage backlash, fixture movement, and registration. Repeated readings alone cannot establish accuracy.
- Record a conservative working interval `value_mm +/- bound_mm`. Use an applicable instrument/setup accuracy bound plus observed variation and registration/contact allowances, without double-counting terms already covered. For a simple DIY estimate, sum plausible bounds rather than assuming independent statistical errors. Label it an engineering bound with its basis, not a certified confidence interval.
- Propagate bounded intervals through derived geometry. For a difference, add the input bounds conservatively; retain correlations if established rather than inventing precision. For rotations/nonlinear constructions, check extremal cases or sweep the permitted input ranges.
- Keep measurement uncertainty, unit-to-unit variation, fabrication tolerance, and deliberate assembly clearance as separate parameters. Do not bury uncertain geometry in an arbitrary larger opening or round it to a standard value without recording the decision.

Use these evidence tags alongside the numerical bound; a tag never replaces it:

| Confidence | Evidence | Allowed CAD use |
| --- | --- | --- |
| Verified | Direct/authoritative geometry checked independently; bounds support the fit decision | Drive critical interface parameters within the stated specimen/scope |
| Measured | Direct capture with setup checks and repeats; independent check incomplete | Drive a prototype with an explicit open fit check |
| Inferred | Symmetry, image tracing, nominal geometry, or derivation relying on unverified assumptions | Drive cosmetic geometry or bounded provisional parameters |
| Unknown | Missing, conflicting, or unbounded evidence | Block dependent critical fit; obtain data or make the interface adjustable |

Preserve evidence type separately: a computed hole center derived from verified edges remains derived, even when its confidence becomes Verified.

Keep 1 compact measurement record per project. Include a setup header with specimen ID/revision, datum photo, tools/settings/checks, capture date, raw-data paths, transforms, registration/check errors, and assumptions. Use this table for manual notes or equivalent CSV fields:

| Feature ID / CAD parameter | Datum / units | Raw readings / source | Method / evidence type | Nominal / bound | Confidence | Independent check / result | Fit decision / open action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1_X / mount_1_x | A-B-C / mm | 3.28, 3.34, 3.31; photo-01 | Caliper + pin / derived center | 3.31 +/- 0.15 | Measured | Pending calibrated camera check | Prototype only; check pattern before freeze |

Treat the row as a format example, not a default dimension or tool capability.

## 6. Cross-check critical geometry

- Validate critical features with a second method that can resolve the acceptance margin: e.g. caliper/pin hole spacing against calibrated camera coordinates, contact heights against a depth gauge or known spacer stack, or a measured hole pattern against a printed drilling/fit template.
- Avoid shared failure modes. A second reading from the same image or 2 calculations using the same scale is not independent validation. A fit coupon checks the actual interface but does not independently prove every numerical dimension.
- Compare intervals: investigate if the difference exceeds the sum of the methods' bounds. If they agree but both bounds exceed the fit allowance, improve capture or adjust the design; agreement alone is insufficient. Do not average conflicting methods to create a convenient nominal.
- Record the second method, raw result, its bound, comparison, and acceptance criterion. Keep unresolved features provisional. Use a quick local coupon for holes, connector openings, insert pockets, or stack heights before printing an entire enclosure.

## 7. Hand off to parametric CAD and test the fit

1. Freeze a measurement-record revision. Pass specimen identity, datums/transforms, tagged feature table, raw evidence, inferred constraints, and unresolved checks to the CAD task.
2. Create named parameters for measured nominal geometry, uncertainty bounds, supplier/process tolerances, and intended clearance. Link critical parameters to feature IDs. Preserve measurements even when selecting a different design nominal.
3. Constrain functional planes, mounting patterns, and mating interfaces first. Build a conservative keep-out envelope for uncertain bodies/projections. Add inferred curves, symmetry, and styling after critical fit is stable; do not let cosmetic constraints move measured interfaces.
4. Evaluate worst-case fit using intervals and fabrication allowances. For centered openings, include feature-position error on each side in addition to body size. For hole patterns, assess relative positions and actual fastener float rather than treating each diameter alone.
5. Example: a body measured as 12.0 +/- 0.2 mm, an opening undersize allowance of 0.2 mm, and a required total free width of 0.4 mm require a nominal opening of at least 12.8 mm when centered with negligible position error. Add measured misalignment separately. These example allowances are not printer defaults.
6. Recompute and inspect the native model at nominal and limiting cases. Print a cheap coupon or partial enclosure in the intended orientation/material; test the real board, connectors, and fasteners. Record measured coupon dimensions to distinguish capture error from print error before changing parameters.
7. Update the record and affected CAD parameters after validation. Return to [mechanical-cad.md](mechanical-cad.md) for assembly, drawings, and release checks. Include the measurement-record revision and open critical checks in the handoff; release with unresolved critical geometry only under the existing bounded prototype-waiver process.
