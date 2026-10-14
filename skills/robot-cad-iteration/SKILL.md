---
name: robot-cad-iteration
description: Develop robot assemblies through short, source-backed CAD and visual-feedback iterations, keeping body design, mechanisms, packaging and physical prototype tests connected. Use for integrated robot CAD or repeated robot design revisions, not standalone PCB work or claims of validated locomotion.
---

# Robot CAD iteration

Turn the next design question into inspectable geometry and a practical test. Keep the user's design character and build objective intact. A review mesh, native assembly, simulation and built robot are different deliverables.

This skill is an original workflow informed by the Alpha Rolie journal, not its unreleased CAD tooling or an exact reproduction of the author's prompts. Read [source-and-limits.md](references/source-and-limits.md) when explaining the inspiration or model/tool claims.

## Establish a small working loop

Inspect the current editable source and a whole-robot view first. Keep native assembly, component candidate and review-viewer revisions distinct; a larger revision number from another branch does not make it authoritative. Identify the concept that must survive, actual available hardware, fabrication process, desired behavior and one immediate question to resolve. Reuse existing CAD tools and project conventions; do not migrate tools or build a custom viewer merely to use this skill.

If editable sources are missing, continue with a clearly provisional concept or a measurement-based reconstruction plan when useful. Identify missing interface evidence; do not claim preserved geometry or print-ready fit from unscaled screenshots.

For a new assembly, start with a simple complete layout: body envelope, actuator axes, link lengths, wheel/foot contacts, battery, compute and major harness volumes. Distinguish measured or supplier-backed geometry from provisional proxies. Check the silhouette and packaging together before detailing one component in isolation. For an existing design, preserve frozen interfaces and constrain the change instead of rebuilding the robot.

Make the earliest useful deliverable visible: a full assembly with the affected area inspectable and a short statement of what is provisional. Do not wait for a polished report or a complete verification campaign before showing a design candidate. User review and engineering checks may proceed together, but neither substitutes for the other.

## Model an integrated object

- Anchor joints, load paths, mounting interfaces and occupied volumes in one coordinate system. Use named parameters and explicit units; keep joint ownership and limits inspectable in the authoritative assembly.
- Tie the exterior to its purpose: supporting structure, cooling, cable protection, sensor sightlines and removable access. Develop silhouette, panel transitions and internals together. Do not cover an unresolved attachment with a floating cosmetic panel. Resolve unwanted gaps with supported transitions while preserving deliberate service seams; do not fuse removable panels merely to improve the render.
- At each new shell segment or accessory, identify what supports it, how it fastens, how a tool reaches the fasteners, and what must move for service. Choose the service sequence for the combined assembly: first reachable fasteners, then disconnects, then a collision-free module exit. Prefer modest packaging growth over mutually blocked removal paths when service is required. A hidden-panel view explains geometry; it does not establish a removal path.
- Reserve real connector mates, cable bends, strain relief and movement envelopes before closing the skin. Do not render a decorative wire and call the harness solved.
- Compare relevant poses and nearby parts, not only the neutral stance. Mark sampled-pose results as sampled; do not imply continuous collision freedom or load capability.

If available, use the companion `electronics-hardware-design` skill for exact part identity, measurement-to-CAD, tolerance, fabrication and release details. When it is not installed, obtain those inputs directly and report unresolved critical dimensions; this skill does not depend on that installation.

## Make feedback actionable

Use the existing CAD viewer, screenshots or annotations. For each correction retain the part/feature identifier, source revision, camera/view, selected location, annotation and original request. A full interactive feedback system is optional. A stable annotated screenshot plus a named feature is often sufficient.

Before revising, translate the feedback into a bounded geometry change and identify its neighbors: e.g. narrower cover while preserving a connector plane, bolt axis and cable clearance. Compare before/after at matching framing and report any changed functional interface. Keep the original annotation and record whether the request is implemented, retained, superseded or unresolved. Do not mark user acceptance on their behalf.

For an interactive viewer, treat selection, note persistence, revision binding and restoring views as actual functionality to test. Preserve drafts on save failure. Derive lightweight review geometry from the editable source and retain the mapping; a visually corrected mesh is not an editable CAD correction.

## Verify the change without stalling the build

1. Regenerate the affected source and inspect geometry validity, exported part identity and placement. Check exported solid count and expected bounds as well as command success; an empty or partial export is a failure. Reopen a representative export; for the delivered assembly, reopen the actual delivered source/export, not an unrelated sample.
2. Check the changed interfaces and neighbors: fit, interference, tool/fastener access, wiring, motion and service paths as applicable. Include assembly-level checks whenever a local change affects global loading, motion, wiring or removal.
3. Inspect the updated complete assembly and useful sections from the same revision. Preserve outstanding contacts or inaccessible parts visibly in the result.
4. Reuse prior evidence only where geometry, transforms, assumptions, tool versions and check scope still match. A successful run on a prior revision is not evidence for changed geometry.
5. If the same operation fails twice, pause that route and diagnose the cause before retrying. Use a smaller disposable test when it can distinguish a tool problem from a design problem. Preserve the working baseline and incomplete state.

Use checks proportional to the iteration. Do not manufacture huge pass counts or paperwork in place of opening the model and checking the changed physical interfaces.

## Close the loop with something buildable

When the user wants a physical prototype, choose the smallest useful part, coupon or subassembly that tests the highest-risk assumption. Define the process, actual mating hardware and observable acceptance condition before fabrication. Do not wait for every cosmetic detail to be final. Conversely, do not order or fabricate without the relevant authorization.

Capture actual fit, access, deflection or failure evidence and change the appropriate parameter. Never fix a measured error by quietly moving unrelated interfaces. Keep CAD clearance, simulation output and physical measurements separate. If hardware is unavailable, deliver the test-ready source and the specific measurement or build action still needed; do not claim the physical loop happened.

For each meaningful iteration, adapt [iteration-card.md](assets/iteration-card.md) into a short working record. Deliver editable source or generator, revision-matched review/export files, the changed result, checks actually run and the next physical question. A source-code generator is editable authority only when it reproducibly creates the delivered geometry; imported solids do not imply a recovered parametric feature history.
