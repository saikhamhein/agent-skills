---
name: robot-cad-iteration
description: Develop robot assemblies through short CAD and visual-feedback iterations, connecting body design, mechanisms and packaging with focused functional checks. Use for integrated robot CAD or repeated robot design revisions.
---

# Robot CAD iteration

Make the next design question visible quickly. Build a small reversible change, inspect it, get feedback and repeat. Prefer a rough complete assembly over one polished part surrounded by unresolved interfaces. Preserve a working baseline so failed experiments are cheap to discard.

## Start with the next useful result

Inspect the editable source and whole-robot view. Identify the current revision, interfaces that must stay fixed, available hardware and fabrication process, and one question to resolve. Reuse the existing CAD stack; do not migrate tools or build a custom viewer just to use this skill.

For a new concept, lay out the body envelope, actuator axes, links, contacts, battery, compute and major harness volumes with simple solids. Label provisional geometry. If source is missing, a clearly provisional concept can still help; screenshots alone cannot establish preserved geometry or print-ready fit.

Aim for a rough complete-assembly preview within a few minutes of usable design work. Adapt that checkpoint to tool cost; report a real blocker rather than silently polishing for a long stretch. Each round should have one coherent visible change and one clear review question. Coordinated changes across several parts are fine when they answer the same question.

## Recommended tools

Reuse a working CAD stack first. For a scriptable setup, this combination has been exercised for parametric solids, STEP round-trips and geometry-derived previews:

- **CadQuery with Python:** named parameters, B-rep solids, assemblies, Boolean/intersection checks, tessellation and STEP export/import. Keep the Python generator as the parametric authority and reopen the delivered STEP to check solids, validity, scale and placement.
- **OpenCascade through CadQuery's OCP backend:** the solid-modeling kernel behind that path. Check the installed compatible backend rather than assuming another CAD kernel or proprietary integration is available; a separate low-level OCP implementation is usually unnecessary.
- **Blender, with CPU Cycles when suitable:** readable shaded previews from tessellated actual CAD bodies. Transfer part names, units and transforms consistently. Keep rendering meshes derived from the same source revision; a polished render is neither editable B-rep authority nor engineering validation. Use the existing CAD-native renderer if it is simpler.
- **Pillow, optionally:** arrange already-rendered views and add clearly labeled captions or review annotations. Preserve the geometry image; do not paint in missing parts or infer dimensions from altered pixels. It is a presentation aid, not a CAD engine.
- **FreeCAD, optionally:** inspect STEP solids or keep them in a native document when that helps review. Imported solids do not recover the generator's parametric feature history. Check that the actual installation opens the file; do not require a GUI or new tool migration for a small revision.

The exercised baseline included CadQuery 2.7.0 with cadquery-ocp 7.8.1.1.post1, Blender 4.3.2, and FreeCAD 1.0.0 for native imported-solid reopen checks. These are reference versions, not required pins or a guarantee for other platforms. Verify available versions and run a small compatibility probe when changing the stack. Pillow was used for preview layout; no particular Pillow release is required by this workflow.

All engineering previews must come from the actual model. Generated concept imagery may explore style when requested, but cannot stand in for CAD geometry or verification. None of these tools establishes physical fit, strength or safe operation on its own.

## Check enough to learn

Before presenting a viable candidate, recompute/build it, confirm intended bodies at plausible scale and placement, and inspect the changed region with its immediate neighbors. For a delivered export, open the actual file to catch empty, partial or misplaced geometry. If broken, show a labeled diagnostic view and the last working baseline.

Add checks for specific risks introduced by the change: a blocked connector, moving-part collision, unsupported attachment or inaccessible fastener. Reuse applicable checks instead of building a test suite for every revision. Sampled poses are not continuous collision proof; a nice preview is not load or fabrication qualification.

Keep known safety and integrity problems visible. Deeper load, tolerance, motion or service reviews belong to an explicit request, an identified consequential risk, or preparation for the relevant physical action. Do not make them a default phase after visual approval. Detailed assembly/disassembly walkthroughs start only when the user explicitly requests them. An identified access or safety risk still needs a focused check of that risk, without automatically expanding into a full walkthrough.

If the same operation fails twice, diagnose before repeating it. A disposable probe can isolate a tool problem; it need not become permanent infrastructure.

## Design the connected assembly

- Use one coordinate system, named parameters and explicit units for joints, load paths and mounting interfaces.
- Develop silhouette and structure together. New panels need plausible attachment; preserve deliberate service seams and removable access.
- Reserve actual connector mates, cable bends, strain relief, sensor sightlines and movement envelopes before closing the skin.
- Spot-check changed motion against neighboring parts. Note unresolved access or collision issues without expanding a small revision into a whole-system audit.
- For exact part identity, measurement, tolerance or release work, consult the companion electronics skill if available, or obtain the required inputs directly.

## Show the result and use feedback

Show an early whole-assembly preview, plus a matching-camera before/after when useful. Prefer CAD-native or depth-buffered solid rendering; inspect the output image for missing geometry and misleading occlusion. Label its source revision and provisional limits. Do not delay feedback for a polished report.

Use existing screenshots, annotations or a viewer. Retain the source revision, part/feature, view and correction. Translate feedback into a bounded change, such as narrowing a cover while preserving a connector plane and bolt axes. Compare the result and report changed interfaces. Implemented feedback is not automatically accepted feedback.

An interactive viewer is optional. If requested, test its real selection, note persistence and revision binding, and preserve drafts on save failure. A corrected review mesh does not replace an editable CAD correction.

## Keep the handoff light

A preview, brief change note, focused check result and next question usually suffice. For ongoing work, reuse a compact revision log; [project-log.md](references/project-log.md), [project-log.html](assets/project-log.html) and [iteration-card.md](assets/iteration-card.md) are optional aids. Do not build or update a webpage at the expense of the next useful preview.

When a physical prototype is wanted, choose the smallest coupon, part or subassembly that tests the riskiest assumption. Establish the mating hardware, fabrication process and observable success condition, then obtain any required authorization. Record actual fit, deflection or failure and revise the responsible parameter. Keep CAD clearance, simulation and physical evidence distinct.

Deliver the relevant editable source/generator and revision-matched outputs in the requested format. Avoid redundant bundles. A generator is editable authority only when it reproduces the delivered geometry; imported solids do not imply recovered parametric history.

See [source-and-limits.md](references/source-and-limits.md) for inspiration and attribution.
