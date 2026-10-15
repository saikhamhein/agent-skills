# Practical starting points

These are adaptable starting points for a new design, not personal preferences or universal electrical requirements. Existing design constraints and the current request take precedence.

## Start with something inspectable

- Sketch the power tree or place the connectors and one functional block first. Show the result while changes are cheap.
- Use labeled provisional parts and envelope models for exploration. Resolve their exact pinout, package, ratings, and fit before those assumptions become wiring, fabrication, or power-on decisions.
- Group circuitry by function and put support parts near their loads. Keep useful whitespace for routing, probing, and rework rather than optimizing area prematurely.
- Use simple routing with a consistent grid and few unnecessary bends. Horizontal/vertical/45-degree segments are a useful conventional starting point; pad escapes, RF structures, and controlled interfaces may need other geometry. Inspect actual turns rather than treating segment orientation as proof of a routing rule.
- Choose trace widths, layers, and vias from current, return-path, interface, and fabrication needs. Avoid a universal width or top-layer-only rule.
- Prefer inexpensive fit coupons and one representative drawing over a complete enclosure print or polished drawing packet when validating an uncertain interface or visual style.

## Spend effort where it changes the result

Use an economical manufacturing process that meets the design. Calculate controlled-interface geometry against its actual stackup. Decide whether paid impedance verification or other services are justified by interface margin, build quantity, and consequences of failure; neither always purchase nor always omit them.

Keep technical dimensions and assembly composition linked to CAD where practical. A presentation render can communicate appearance but cannot establish fit or replace editable geometry. Preserve units and coordinate transforms when moving between tools.

Package only the sources, outputs, and evidence needed for the requested handoff. Publication destination, manufacturing order, licensing, and scope expansion require their own authorization; a convenient workflow does not supply it.
