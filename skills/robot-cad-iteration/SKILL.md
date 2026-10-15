---
name: robot-cad-iteration
description: Develop robot assemblies through short, source-backed CAD and timeboxed visual-feedback iterations with a revision-linked project webpage, keeping body design, mechanisms and packaging connected with lightweight functional checks. Use for integrated robot CAD or repeated robot design revisions, not standalone PCB work or claims of validated locomotion.
---

# Robot CAD iteration

Turn the next design question into inspectable geometry and a quick functional check. Keep the user's design character and build objective intact. A review mesh, native assembly, simulation and built robot are different deliverables.

This skill is an original workflow informed by the Alpha Rolie journal, not its unreleased CAD tooling or an exact reproduction of the author's prompts. Read [source-and-limits.md](references/source-and-limits.md) when explaining the inspiration or model/tool claims.

## Establish a small working loop

Inspect the current editable source and a whole-robot view first. Keep native assembly, component candidate and review-viewer revisions distinct; a larger revision number from another branch does not make it authoritative. Identify the concept that must survive, actual available hardware, fabrication process, desired behavior and one immediate question to resolve. Reuse existing CAD tools and project conventions; do not migrate tools or build a custom viewer merely to use this skill.

If editable sources are missing, continue with a clearly provisional concept or a measurement-based reconstruction plan when useful. Identify missing interface evidence; do not claim preserved geometry or print-ready fit from unscaled screenshots.

For a new assembly, start with a simple complete layout: body envelope, actuator axes, link lengths, wheel/foot contacts, battery, compute and major harness volumes. Distinguish measured or supplier-backed geometry from provisional proxies. Check the silhouette and packaging together before detailing one component in isolation. For an existing design, preserve frozen interfaces and constrain the change instead of rebuilding the robot.

## Keep the visible feedback loop short

Aim for the first rough **complete-assembly preview in about five minutes** after starting usable design work. This is a soft target for reducing blind waiting, not a promise of completed engineering. Reuse the baseline, simple solids and existing rendering tools. If loading, missing inputs or broken geometry prevent a useful preview, report the actual blocker around that checkpoint with the last valid view clearly dated; do not hide the failure, fabricate a new view or silently spend thirty minutes polishing an unusable model.

Work in short rounds, each with **one visible coherent change** and one clear review question. A coherent change may require several coordinated parts, supports or cable routes; do not artificially limit it to one body. Set the next preview checkpoint based on the current tool cost and keep the user informed if that changes. Stop after a direction-setting preview when acceptance is needed; continue independent work that does not depend on that choice.

Before each preview, perform a quick sanity pass: build/recompute succeeds, intended bodies exist at plausible scale and placement, changed geometry is not visibly broken, and obvious clashes with immediate neighbors are exposed or resolved. Inspect the actual resulting whole assembly. If it is broken, show a diagnostic view labeled as such alongside the last valid baseline rather than presenting it as a viable candidate.

Show a clear complete-assembly preview early and after each meaningful change, plus a matching-camera before/after of the changed region when useful. Prefer an existing CAD-native or depth-buffered renderer for solid assemblies; avoid painter-sorted polygon plots such as Matplotlib Poly3D, which can misorder overlapping faces. Use readable solid shading and lighting; hide tessellation edges and fix triangle artifacts that obscure the shape. Inspect the rendered image, not just successful file creation. Label its source revision and provisional limits. Ask about the concrete design decision, not a generic “thoughts?” Do not delay the preview for a polished report, exhaustive analysis or a growing test suite. Direction approval does not automatically start a deeper review or establish engineering acceptance or fabrication permission.

## Keep a useful project webpage

Maintain a compact project log alongside the design when this workflow is used for ongoing robot work. Read [project-log.md](references/project-log.md) for the latest-model view, revision images, changes, feedback and unresolved issues. Start from [project-log.html](assets/project-log.html) only if no suitable page already exists; updating the log must not delay the CAD preview. Keep it local/private unless sharing is authorized. The template is a static starting point, not a working CAD viewer or a published site.

## Model an integrated object

- Anchor joints, load paths, mounting interfaces and occupied volumes in one coordinate system. Use named parameters and explicit units; keep joint ownership and limits inspectable in the authoritative assembly.
- Tie the exterior to its purpose: supporting structure, cooling, cable protection, sensor sightlines and removable access. Develop silhouette, panel transitions and internals together. Do not cover an unresolved attachment with a floating cosmetic panel. Resolve unwanted gaps with supported transitions while preserving deliberate service seams; do not fuse removable panels merely to improve the render.
- Give new shell segments or accessories plausible support and attachment, and notice obvious blocked fasteners or trapped modules near the change. Flag unresolved service access without expanding the iteration into a detailed assembly walkthrough. A hidden-panel view explains geometry; it does not establish a removal path.
- Reserve real connector mates, cable bends, strain relief and movement envelopes before closing the skin. Do not render a decorative wire and call the harness solved.
- When a change affects motion, spot-check the relevant pose and nearby parts. Mark sampled-pose results as sampled; do not imply continuous collision freedom or load capability.

If available, use the companion `electronics-hardware-design` skill for exact part identity, measurement-to-CAD, tolerance, fabrication and release details. When it is not installed, obtain those inputs directly and report unresolved critical dimensions; this skill does not depend on that installation.

## Make feedback actionable

Use the existing CAD viewer, screenshots or annotations. For each correction retain the part/feature identifier, source revision, camera/view, selected location, annotation and original request. A full interactive feedback system is optional. A stable annotated screenshot plus a named feature is often sufficient.

Before revising, translate the feedback into a bounded geometry change and identify its neighbors: e.g. narrower cover while preserving a connector plane, bolt axis and cable clearance. Compare before/after at matching framing and report any changed functional interface. Keep the original annotation and record whether the request is implemented, retained, superseded or unresolved. Do not mark user acceptance on their behalf.

For an interactive viewer, treat selection, note persistence, revision binding and restoring views as actual functionality to test. Preserve drafts on save failure. Derive lightweight review geometry from the editable source and retain the mapping; a visually corrected mesh is not an editable CAD correction.

## Check function without growing the process

Default to a quick functional check of the changed result: build/recompute succeeds, the intended geometry is present at plausible scale and placement, and the changed feature works in its immediate context without an obvious clash. For a delivered export, open that actual file and confirm it is not empty, partial or misplaced. Reuse existing checks where relevant; do not add or expand a test suite by default, chase pass counts, or turn each iteration into an audit.

Add a targeted check only for a concrete risk introduced by the change, such as a blocked connector, moving-part collision or unsupported load-bearing attachment. Keep the check proportional to that risk and report what remains unknown. A known safety or integrity problem must be exposed or resolved, never hidden to meet a preview target. Reuse prior evidence only while its geometry, transforms, assumptions and scope still apply.

A detailed assembly/disassembly walkthrough starts **only when the user explicitly asks for it**. Do not start one merely because a design direction is accepted, a panel was added or this skill was invoked. When requested, trace reachable fasteners, disconnects and module exit paths in the combined assembly. Broader fit, motion, load, tolerance or service reviews are separate scoped work when requested or required to address an identified safety risk, not the default next phase. Do not claim build readiness from a quick check or a good-looking preview.

If the same operation fails twice, diagnose before retrying that route. A small disposable probe may distinguish a tool problem from a design problem; it need not become a permanent test. Preserve the working baseline and clearly label incomplete results.

## Close the loop with something buildable

When the user wants a physical prototype, choose the smallest useful part, coupon or subassembly that tests the highest-risk assumption. Define the process, actual mating hardware and observable acceptance condition before fabrication. Do not wait for every cosmetic detail to be final. Conversely, do not order or fabricate without the relevant authorization.

Capture actual fit, access, deflection or failure evidence and change the appropriate parameter. Never fix a measured error by quietly moving unrelated interfaces. Keep CAD clearance, simulation output and physical measurements separate. If hardware is unavailable, deliver the test-ready source and the specific measurement or build action still needed; do not claim the physical loop happened.

For each meaningful iteration, keep a few factual lines in the project log; [iteration-card.md](assets/iteration-card.md) is an optional prompt, not a form to complete. Never delay the preview to fill it out. Deliver editable source or generator, revision-matched review/export files, the changed result, checks actually run and the next physical question. A source-code generator is editable authority only when it reproducibly creates the delivered geometry; imported solids do not imply a recovered parametric feature history.


