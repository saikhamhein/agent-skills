# Mechanical CAD, fit, and drawings

## Preserve engineering authority

Identify the exact PCB/enclosure revisions, coordinate systems, units, approved interfaces, and ordered geometry. Work on a copy or branch of the frozen baseline. Link models to their actual source files and hashes. Native CAD is the authority for engineering composition; PDF and presentation images are derivatives.

Keep the distinction between a fully parametric source and a native CAD document containing imported STEP solids with geometry-linked views/dimensions. The latter is useful and editable, but does not restore the original feature history. State the limitation and retain the original generator/source where available.

## Establish measured geometry from a physical reference

When authoritative geometry is missing or needs checking against a physical specimen, use [reference-to-cad.md](reference-to-cad.md) before fixing CAD dimensions. Record specimen identity, datums, raw measurements, registration, uncertainty, and confidence. Keep measured specimen geometry distinct from manufacturer limits and designed clearances. For physical-reference work, carry the measurement record and unresolved fit-critical checks through drawings and the release audit.

## Make the model trustworthy before dressing it up

- Audit every fitted PCB reference against the current BOM, footprint, and model assignment. Track exact manufacturer models, package-equivalent models, dimensional proxies, and missing models separately.
- Verify scale, origin, rotation, polarity, connector mating plane, pin/lead exit, seating height, and maximum component envelope. Compare imported PCB geometry against the native board; visually plausible offsets can conceal a wrong transform.
- An attractive substitute connector model is not a BOM substitution or fit proof. Fit against the selected component's maximum dimensions and tolerances, including attached plugs/cables and service access.
- Maintain one PCB-to-enclosure transform. Use datums and explicit millimetres for mounting spacing, critical heights, openings, and fits. Check opposing views and mirrored bottom-side coordinates.

## Check fit, fasteners, and the assembly path

Inspect the exact final board/enclosure pair, not separate nominal models. Include board thickness tolerance, hole positional tolerance, component maximum bodies, connector envelopes, lid flex/clearance, wire bend/access, tools, standoffs, washers, screw heads, inserts, thread engagement, insertion depth, retention, and removal sequence as applicable.

Use CAD interference/distance checks and sections at critical interfaces. Include the conductive volume of fasteners and inserts relative to copper on both sides, vias, leads, and exposed pads. Do not treat soldermask as a reliable protective insulation barrier. Show the designed insulating geometry and carry its manufacturing/assembly tolerance into the test plan.

Record print/process orientation, material, shrinkage and dimensional assumptions where parts are fabricated. A collision-free nominal assembly does not validate a printed fit, insert retention, live insulation, or long-term mechanical behavior. Define practical inspection and physical fit/retention/insulation checks.

## Draw from geometry

Use native CAD drawing views and geometry-linked dimensions, sections, and detail views where the tool supports them. Recompute and inspect links after model changes; edge/face identifiers can change. For critical dimensions, compare the displayed value to actual source geometry and the design requirement.

Use conventional dimension notation with explicit mm, readable tolerances where needed, part/revision identification, scale, material/process notes, and a restrained title block. Avoid cryptic custom labels in place of dimensions. Keep manual notes distinguishable from associative dimensions; do not use scripted dimension text to disguise a drawing that can drift from the model.

For a new drawing style or broad report migration, produce one representative sheet and get approval before replacing the rest. Approval of one style permits applying that style within scope, not unseen geometry changes. Replace intended sheets in place and avoid duplicate mechanical sections.

## Keep assembly instructions in CAD

Author assembled/exploded poses, component placement, arrows, callouts, fastener identifiers, and assembly steps in the engineering CAD workflow. Make the sequence mechanically possible and tie each instruction to identifiable parts. Do not manually recreate technical annotations in a presentation renderer.

An optional presentation image can use a transferred, fully assembled scene if practical. Preserve geometry and keep it separate from manufacturing authority. Check all objects transferred; if the workflow cannot preserve the intended composition, omit it rather than rebuilding engineering content decoratively. Preview new imagery before integrating it into an established report.

## Audit the entire delivered packet

Reopen/recompute native files and render all pages. Check title blocks, page counts/order, clipping, dimension overlap, scale/readability, broken links, font substitution, and whether the file can be edited. Compare unchanged pages/geometry against the approved baseline, preferably with visual and semantic evidence.

Check a release content inventory, including schematic, actual copper layers, BOM, overall mechanical dimensions, native models/drawings, assembly and exploded instructions, fasteners/accessories, and approved renders. A successful replacement of five drawing sheets is not proof that the combined report still contains everything promised. Record missing or intentionally excluded content before release.

Maintain a small visual manifest mapping each requested/approved image to its intended role and report page. A finished-product image must not silently replace a required populated-PCB view. If that PCB view is stale, regenerate it from the current source and retain the product image in its intended role. Verify images are actually embedded where promised; delivering a separate image file does not establish report inclusion.
