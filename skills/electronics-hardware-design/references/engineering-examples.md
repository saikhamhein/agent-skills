# Reusable engineering examples

These hypothetical examples illustrate decisions and focused checks. Values are illustrative, not design defaults or claims about qualified hardware. Use authoritative data for the actual parts and conditions.

## A same-package part is not necessarily a drop-in

Two supervisor variants can share a package but assign reset and ground to different pins. Compare the exact suffix, pin table, and footprint mapping before wiring or substitution. For an early shortlist, flag the mapping as pending; do not require a complete assembly audit merely to compare candidates.

## Compare implemented circuits, not bare IC prices

A cheaper regulator may need more output capacitance, a larger inductor, or a different operating mode. Include the support network and relevant assembly cost when selecting it. Check light-load behavior only if ripple, noise, or efficiency at that operating point matters to the application.

## Inductor substitution has a fault corner

A hypothetical substitute rated for 3 A saturation is not established as suitable for a regulator whose switch limit can reach 4 A. Check peak/RMS current, DCR, hot saturation behavior, and fault energy. Typical room-temperature curves do not guarantee hot performance. Use calculations to choose the next safe bench test, not to relabel unmeasured behavior as qualified.

## Nominal capacitance can hide a large change

A ceramic capacitor's effective capacitance can fall under DC bias. Use data for the exact part and distinguish typical curves from guaranteed bounds; account for relevant temperature and tolerance effects. If substituting a polymer/ceramic network, revisit the regulator's stability constraints and test the load response rather than reopening unrelated interface checks.

## A cutoff threshold is not a clamp guarantee

A static overvoltage threshold below a downstream limit does not establish that transient overshoot stays below that limit. Delay, source impedance, stored energy, and recovery matter. Validate the protection with controlled energy and dummy loads before attaching valuable equipment. One fault scenario does not prove broad immunity.

## Clean connectivity can coexist with broken return geometry

A zone-priority change can leave a ground void even when all nets remain connected. After changing fills, inspect the actual polygons and affected signal return paths. At layout release inspect every copper layer; during a local experiment start with the touched regions and their coupled paths.

## Assembly and mechanical checks catch different failures

A same-net via touching a pad may pass electrical DRC yet wick solder. A metal insert can contact copper beneath soldermask even in a nominally collision-free enclosure model. Check the intended via process and conductive hardware envelopes separately; use positive insulation where required and test the actual fit before powered use.

## Export coordinates need an independent spot check

An exporter can emit footprint anchors where the assembler expects component centers. Compare a few representative polarized, through-hole, and asymmetric parts against the intended placement convention. A changed exporter or origin justifies broader coordinate parity checks; a text-only label correction does not.

## A stackup change can invalidate retained routing

Keeping differential-pair copper while switching stackup changes impedance. Recalculate the affected interface and adjust the routing or explicitly identify the unresolved prototype risk. A previous build's waiver never becomes the new board's default geometry.
