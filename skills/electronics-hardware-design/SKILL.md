---
name: electronics-hardware-design
description: Select and qualify electronic components, organize PCB placement and routing, develop CAD-linked mechanical designs, measure physical references for parametric CAD, and prepare traceable hardware releases. Use for board-level electronics with or without an enclosure, including physical-reference reverse engineering, reviews, and revisions of an existing design.
---

# Electronics hardware design

Turn requirements into reviewable design evidence and a reproducible release. Work at the requested depth; a component comparison does not authorize board redesign, procurement, fabrication, or publication.

## Start with the current baseline

Identify the requested outcome, authoritative editable sources, exact revision, approvals, ordered or otherwise frozen geometry/BOM, and available tools. Inspect the actual files before proposing changes. If sources cannot be recovered, stop dependent editing and report what is missing; do not silently reconstruct or substitute an older revision.

For a narrow revision, identify the affected checks and use semantic/geometry diffs to preserve unrelated approved content. Do not restart the entire new-design workflow just to correct a label, substitute a qualified part, or replace a drawing sheet.

Keep four kinds of information separate:

1. **Engineering requirements:** interface, electrical, thermal, mechanical, safety, manufacturing, and test constraints derived from this design and current authoritative sources.
2. **Sai's design defaults:** read [references/sai-defaults.md](references/sai-defaults.md) when working for Sai. Apply where feasible; expose conflicts instead of silently compromising engineering.
3. **Project decisions:** approved dimensions, MPNs, stackup, costs, and geometry for the current project only. Recalculate for a new project.
4. **Accepted waivers:** bounded prototype exceptions with an owner, risk, evidence, and closure condition. A previous waiver is never a general design rule.

## Choose the relevant workflow

- Requirements, architecture, components, or substitutions: [references/component-selection.md](references/component-selection.md)
- Placement, routing, DRC, or visual PCB review: [references/pcb-layout.md](references/pcb-layout.md)
- Integrated robot body/mechanism iterations and visual feedback: use the companion `robot-cad-iteration` skill when available; retain the mechanical validation below.
- Enclosure, PCB models, fit, drawings, or assembly: [references/mechanical-cad.md](references/mechanical-cad.md)
- Physical reference, camera/ToF/probe capture, or manually measured geometry: read [references/reference-to-cad.md](references/reference-to-cad.md) before modeling, then follow the mechanical CAD workflow.
- Bring-up, validation claims, manufacturing handoff, or release: [references/validation-release.md](references/validation-release.md)
- Applying lessons from the USB DUT hub: [references/usb-dut-hub-lessons.md](references/usb-dut-hub-lessons.md). Its project values are examples, not defaults.

Read only the relevant references. Templates under [assets/templates](assets/templates) support concise decision/evidence records; adapt them to the work instead of creating unused paperwork.

## Non-negotiable handoffs

- Support parts, footprints, models, and production files with exact identity and revision evidence. A family name, distributor thumbnail, attractive render, or clean DRC is insufficient.
- Use current manufacturer datasheets and relevant application notes for design limits, and the selected fabricator/assembler's current capability data for manufacturing rules. Record URLs, revisions/dates, and the conditions used. Reconfirm price, stock, and supplier availability at purchasing time.
- Obtain missing approval before changing frozen/ordered design intent or expanding scope. Resolve ambiguous component identity, polarity, voltage domain, return path, clearance, or geometry before dependent release work.
- Validate electrical, geometric, assembly, visual, and physical behavior separately. State what passed, what remains untested, and what is waived. Never turn “zero DRC errors” or “released for prototype” into “validated hardware.”
- Preserve editable native sources and exact artifact provenance. Regenerate derivative drawings and manufacturing files from the frozen source revision; audit the complete release, including unchanged sections.

Record conclusions, evidence, assumptions, and tradeoffs, not a private reasoning transcript. Share the useful result first, with the smallest specific blocker or next decision when needed.

