# Component selection and substitution

## Establish constraints before shopping

Capture interface/version and role, input/output ranges, worst-case loads and transients, voltage domains, environment, isolation/protection, size, serviceability, test strategy, target cost, assembly route, and expected sourcing horizon. Separate known requirements from assumptions. Turn missing information that could invalidate the architecture into a stop gate; use clearly bounded assumptions for reversible comparisons.

Make a block diagram and power tree appropriate to the task. Budget conversion loss, conduction/cable/connector drop, inrush, current-limit tolerance, thermal dissipation, startup sequencing, and fault energy at relevant operating corners. Distinguish nominal, guaranteed, and calculated values. Preserve units, conditions, and conservative margins in the calculation record.

## Compare the candidates that matter

For each serious candidate, record:

- Exact manufacturer, orderable MPN including suffix, package, temperature/voltage grade, lifecycle, source URL and document revision/date
- Required performance versus guaranteed limits at the actual conditions, absolute maximum constraints, loss/temperature margin, timing and startup behavior
- Tolerance, temperature, DC-bias, aging and fault sensitivities where relevant; identify typical curves and engineering reserves rather than treating them as guaranteed minima
- Required support components, land-pattern/assembly needs, test access, firmware/configuration needs, and total implementation cost
- Distributor code, stock/price observation date, assembly-service eligibility if relevant, and an alternate/requalification path
- Why selected or rejected, unresolved risks, and the evidence needed to close them

Separate fitted-part cost from purchase multiples/attrition, feeders, PCB, assembly, freight, tax, and accessories. An assembly-service catalogue classification is not allocated stock, and retail inventory need not be the assembler's inventory. Include the complete support network when comparing architectures.

Use manufacturer datasheets and application notes for technical authority. Distributor pages support stock, ordering identity, and service eligibility; they do not override pin tables or package drawings. Do not copy a formerly successful IC merely because it worked in another architecture.

Use [the component matrix](../assets/templates/component-matrix.csv) and [decision record](../assets/templates/decision-record.md) when they reduce repeated work. Keep enough evidence to review a conclusion without storing a reasoning transcript.

## Qualify each selected part end to end

1. **Electrical identity:** match exact MPN to function, pinout, pin type, polarity, exposed pad, reserved/NC pins, reset/enable strapping, sequencing, and legal operating conditions. Resolve family-level ambiguities before wiring.
2. **Implementation:** check reference designs against this application; verify decoupling, stability constraints, feedback/compensation, protection coordination, crystal/clock loading, pull resistors, configuration storage, and fault handling where applicable. Treat application schematics as examples, not proof.
3. **Footprint:** compare the actual symbol-to-pad numbering and copper/solder-mask/paste geometry against the exact package drawing and recommended land pattern. Record the local library identifier and revision/hash. Check pin-one orientation, body/courtyard/height, exposed-pad paste and via strategy, connector mating plane, and mounting features.
4. **Model:** map each fitted reference to a model and classify it as exact manufacturer geometry, package-equivalent, or dimensional proxy. Record source, scale, transform, origin, and fit-relevant uncertainty. A plausible 3D model does not verify a footprint.
5. **Assembly:** reconcile exact MPN, value, footprint, fitted/DNP status, quantity, and reference set across schematic, PCB, BOM, assembly BOM, and placement file. Check polarity and rotation conventions with the intended assembler. Expand grouped references deterministically for comparison; explain approved omissions such as hand-fitted parts.

## Substitutions reopen affected gates

A distributor-code change, unavailable package variant, “equivalent” MOSFET, regulator, connector, or passive can change the design. Classify an alternate as exact drop-in, local-layout change, or architecture change. Recheck exact identity, pinout, recommended footprint, ratings/derating, dynamic behavior, configuration, protection, thermals, 3D fit, assembly orientation, lifecycle, and cost as applicable. Identify affected calculations, tests, and artifacts. Regenerate them after approval if the baseline is frozen; do not only edit the BOM.

Useful stop conditions include uncertain package/pin mapping, exceeded stress or thermal limits, unsupported fabrication geometry, unresolved interface compatibility, and unavailable critical parts without a qualified alternate. Report the smallest decision needed to proceed.
