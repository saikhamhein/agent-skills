# Sai's design defaults

These are Sai's expressed working preferences. They are not universal electrical rules or automatic permission to change a frozen design. Current task instructions and engineering constraints control any conflict. Explain necessary exceptions.

## PCB organization and review

- Treat visual organization as part of design quality. Group circuitry by function and keep supporting components with their functional block. Preserve accepted whitespace when further tightening is secondary.
- Prefer horizontal, vertical, and 45-degree straight segments with 45-degree direction changes; avoid abrupt right-angle corners. Inspect actual copper layers. A rendered board alone cannot establish routing quality.
- Prefer ordinary signal traces around 0.20 mm or wider where practical. Interface-controlled geometry may require narrower widths; calculate and check the selected low-cost fabrication process rather than forcing one width everywhere.
- Use a consistent routing grid. Exact pad escapes and differential-pair geometry may need documented offsets. Remove needless bends and tiny segments, including by moving support parts where authorized; do not cosmetically quantize an awkward route.
- Prefer top-layer signal routing, with bottom continuation when useful. Complementary routing directions are an organizational guide, not a reason to add unnecessary high-speed bends.
- Avoid vias under component bodies and ordinary via-to-pad contact unless assembly-compatible and specifically justified. Exposed-pad thermal vias and deliberate stitching need their own implementation checks. Same-net DRC does not prove assembly suitability.
- Use the selected manufacturer’s actual rules and an economical process. Include global rule floors and separate pad/body/via assembly checks.
- At final layout, center the board on its drawing sheet and establish a useful documented grid/fabrication origin. Preserve relative geometry and verify coordinate exports after any translation.

## Impedance and cost

Design to the impedance required by each interface, including a supported stackup and geometry. By default, skip the paid fabrication impedance-control/verification service. Explain a genuine need for that service before selecting it. This cost preference does not waive signal-integrity analysis or physical qualification, and USB's impedance target is not every interface's target.

## Mechanical communication

- Prefer CAD-native, geometry-linked engineering views and dimensions, sections/details, explicit millimetres, and a restrained professional title block. Make one representative sample for approval before a broad visual redesign.
- Keep technical assembly/exploded composition, arrows, callouts, and instructions in the engineering CAD workflow. An optional presentation renderer may produce an unchanged-geometry assembled image; it must not become the engineering authority.
- Preview new presentation imagery before integrating it into an established report. Preserve already approved useful renders unless replacement is requested.

## Scope-specific delivery choices

The hub used a lean Git-first release: native editable sources, final report, and useful manufacturing files without redundant source bundles or cache trees. Treat that as a project precedent; establish the destination and packaging needed for the current project. It does not authorize publishing to any repository or selecting a license.
