# PCB placement and routing

## Iterate on one useful layout increment

Show a rough placement or route one critical path early. For exploratory geometry, use clearly stated provisional process assumptions. Check the touched nets, nearby returns, and assembly or fit risks before extending the layout. Complete manufacturing review when preparing fabrication outputs, not before the first placement sketch.

## Establish real manufacturing and interface rules

Get the selected fabricator's current layer stackup/material/copper options, width/space, drill, annular ring, mask, edge, and assembly limits. Record the chosen process and cost tier. Set explicit global minimums and net-class constraints; default CAD rules may be too permissive or incomplete.

Calculate controlled-interface geometry from the actual stackup and applicable interface specification. Record field-solver/calculator version, dielectric assumptions, reference planes, pair width/spacing, copper/finished thickness, and tolerance limitations. Recompute when stackup or nearby copper changes. Do not copy another board's layer assignment or pair dimensions without recalculating.

Model power and thermal paths at the relevant corners. Include connectors, fuses, switches, MOSFETs, copper, vias, relief spokes, return paths, and supply/cable conditions. Separate board drop from cable drop and state the measurement planes. A budget is a prediction until hardware tests validate it.

## Place before routing

1. Lock only approved mechanical interfaces: outline, mounting holes, connectors, mating/keepout envelopes, and critical height limits. Record what may move.
2. Group by signal/power function. Place decoupling against the relevant pins and returns; minimize switching and high-current loops; separate sensitive analog/clock circuitry from noisy fields as the design requires.
3. Place high-speed source, sinks, and protection around direct routes and continuous reference planes. Resolve unavoidable crossings and bottlenecks before filling the board with support parts.
4. Review functional grouping, connector access, assembly clearances, rework/test access, polarity, silk readability, and component height in 2D and 3D. Fix placement-driven detours before polishing routes.

Show a placement overview for a significant redesign before investing in full routing if placement intent is unapproved. Small authorized support-part moves should serve a clear electrical, assembly, or organization benefit.

## Route with explicit electrical and assembly intent

- Preserve return-current continuity through plane changes and transitions. Check reference plane voids, board cutouts, split regions, and stitching strategy; a copper layer's name does not establish a usable return path.
- Route coupled interfaces as such: actual pair geometry through escapes, neck-downs, pads, vias, and layer changes matters. Evaluate applicable skew/length/stub and topology constraints from current interface guidance; avoid unnecessary tuning or decorative meanders.
- Keep current loops compact and sensitive nodes protected. Use widths/via counts/thermal paths justified by the load and process, not a universal trace-width rule.
- Use a simple, consistent routing style appropriate to the interface. If an angle rule applies, examine actual turns and short segments, not only segment orientations.
- Inspect via barrels/annular rings relative to pads, paste, component bodies, exposed pads, and assembly keepouts independently of electrical DRC. Check tenting/filling/capping and solder-wicking consequences with the intended process.
- Where solderability calls for thermal relief, evaluate spoke geometry against electrical/thermal needs. Justify solid exposed-pad or stitching connections individually rather than copying another design's relief choices blindly.
- Refill zones, verify thermals and isolated islands, and rerun connectivity after geometry edits. Local same-net copper or solid joins can bypass a nominal thermal-relief setting; inspect the actual poured result. Check polygon anchors and zone priorities: a removed unconnected high-priority island can still leave a lower-priority plane unexpectedly empty.

## Verify the changed layout; broaden checks for release

During iteration, run the relevant ERC/DRC and inspect changed fills. For layout release, run the full configured checks with recorded versions, constraints, exclusions, and fresh zone fills. Check missing/unconnected nets, schematic/PCB parity, supply/ground naming, differential-pair rules, silkscreen, mask, copper-to-edge, and mounting keepouts. Use targeted geometry checks for gaps the CAD rules cannot express.

Audit disabled or ignored checks explicitly rather than inheriting them silently. Record whether a reviewer reran a check, independently measured geometry, or only inspected an author's receipt. For custom validators, use negative tests that inject a known defect and show it is rejected.

Review actual copper-layer plots at useful scale for detours, tiny jogs, clutter, inconsistent grouping, accidental bottlenecks, reference-plane continuity, thermal spokes, and component/via relationships. At release inspect every copper layer, not just the top or 3D rendering; in a local iteration inspect affected regions and their interacting return paths. Document authorized exceptions without relabeling them as clean passes.

Any global translation, origin change, rotation, library update, or regenerated footprint warrants a coordinate/parity check of source, drill, Gerber, placement, and mechanical exports. Explicitly state origin, units, side, and rotation convention. Preserve a frozen revision for release and confirm derivatives match it.

Proceed to [validation and release](validation-release.md) only with the appropriate design checks complete and remaining physical tests explicitly tracked.
