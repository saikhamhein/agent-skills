---
name: electronics-hardware-design
description: Select electronic components, design and revise PCB layouts, develop CAD-linked mechanical designs, measure physical references, and prepare hardware for testing or manufacturing. Use for board-level electronics with or without an enclosure.
---

# Electronics hardware design

Move fast, break things in reversible design experiments, and learn from the result. Start with a useful draft, not a release audit. Keep electrical hazards, physical damage, manufacturing commitments, and unsupported performance claims outside that experimentation budget.

## Default loop: build, inspect, adjust

1. Identify the requested outcome and current editable sources. For a revision, inspect the actual baseline and frozen interfaces; for a new concept, state the few assumptions needed to start.
2. Choose the smallest useful increment: a power-tree sketch, candidate comparison, one circuit block, rough placement, or a fit coupon. Use a branch/copy or parameters that make changes easy to reverse.
3. Produce an early visible result. Label provisional geometry, parts, and performance honestly. Do not wait for full qualification, complete sourcing, polished drawings, or a release manifest to show an exploratory draft.
4. Run checks tied to what changed and what could fail next. Resolve a wrong pinout before wiring, dangerous voltage before powering, or uncertain fit before ordering; keep unrelated checks out of the loop.
5. Share the result, the meaningful uncertainty, and the next useful experiment. Iterate within the requested scope. Broaden verification when coupling, concrete risk, or release warrants it.

A component comparison does not authorize board redesign, procurement, fabrication, or publication. Preserve approved/ordered geometry and seek missing authorization before changing it. If authoritative source files are missing, do independent comparisons or clearly labeled concepts; do not silently substitute a reconstructed baseline.

## Read only the relevant guidance

- Starting a concept or choosing practical defaults: [practical-defaults.md](references/practical-defaults.md)
- Components or substitutions: [component-selection.md](references/component-selection.md)
- Placement, routing, and copper review: [pcb-layout.md](references/pcb-layout.md)
- Enclosures, fit, drawings, and assembly: [mechanical-cad.md](references/mechanical-cad.md)
- Measured physical references: [reference-to-cad.md](references/reference-to-cad.md)
- Bring-up, validation claims, or manufacturing handoff: [validation-release.md](references/validation-release.md)
- Short reusable engineering examples: [engineering-examples.md](references/engineering-examples.md)

Use templates under [assets/templates](assets/templates) only when they reduce work. They are optional records, not prerequisites for iteration. For robot body/mechanism work, the companion `robot-cad-iteration` skill may help if available.

## Keep the evidence honest

- Distinguish requirements, provisional defaults, project decisions, and explicitly accepted prototype exceptions. A previous design or waiver does not establish a new requirement.
- Use exact part/package identities and current manufacturer limits before committing dependent engineering. Check current fabricator capabilities before finalizing manufacturing geometry; refresh price/stock before purchasing.
- Check electrical, geometric, assembly, and physical behavior separately when relevant. A render or clean DRC does not establish working hardware. State what was calculated, inspected, measured, or remains untested.
- Use current-limited, protected bring-up and safe fault-test plans. Resolve hazardous uncertainty before energizing equipment or exposing people to it.
- Preserve native editable sources. At release, regenerate requested derivatives from the identified revision and check the delivered packet's integrity and completeness.

Record conclusions, evidence, assumptions, and tradeoffs rather than a private reasoning transcript. Lead with the useful result.
