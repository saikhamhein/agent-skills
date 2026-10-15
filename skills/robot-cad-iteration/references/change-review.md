# Lightweight CAD change review

Use this within the normal edit–preview–feedback loop. The goal is reliable awareness, not a larger review ceremony.

## Compare against the user's review baseline

Record the previous reviewed revision and current candidate. Keep the accepted direction distinct from the most recent preview: showing a revision does not make it accepted. If several commits occurred between reviews, compare the full interval, not only the latest commit. If there is no usable baseline, say so and establish one; do not imply that preserved geometry has been verified.

Before a consequential change, explain what, why and impact. For example, a requested slimmer cover may require moving a mount or reducing cable clearance. Surface that dependency before making it. If it departs from agreed direction or fixed interfaces, ask for a decision; if already within approved scope, continue and include it in the next change summary.

## Reconcile intent with actual differences

Before commit or handoff, inspect the real source diff and compare rebuilt models and structured part manifests for the baseline and candidate. Generate the manifest from the model/source where possible; a manually maintained manifest has the same omission risk as a handwritten log.

Use stable part IDs and explicit units/reference frames. Compare the fields relevant to the design:
- Added, removed or replaced parts, quantities and mounting relationships
- Key dimensions, overall envelope and mounting coordinates
- Part placement and orientation
- Material/density assumptions, mass and relevant center-of-mass changes
- Joint type, axis, origin, limits and connected parts
- Changed design assumptions and unresolved dependencies

An existing CSV, JSON or native CAD report is enough. Reuse it; do not invent a new system for each iteration. Represent unknowns explicitly, not as zero or unchanged. Record extraction method, source revisions and any comparison tolerance. Numeric/manifest comparisons do not necessarily catch topology, internal geometry or visual differences; inspect affected bodies and use matching-camera before/after views where relevant. Screenshots alone do not verify dimensions, hidden interfaces or mass.

Match every detected consequential difference to the change summary and reconcile unexpected differences. Restore unintended drift or obtain a decision before retaining a departure from agreed direction. Record low-impact details in the supporting artifact. Do not silently accept drift merely because the model builds.

## Tell the user what the comparison covers

Each preview needs a brief "Changes since previous review" note: major differences first, including incidental changes, their reason and practical impact. Link the detailed comparison beside the CAD. Keep changed assumptions and decisions in the message, not buried in that artifact.

Distinguish:
- **Mechanically checked:** actual generated fields/files compared and results
- **Visually inspected:** views and affected regions inspected
- **Unchecked / unavailable:** missing baseline, unavailable mass data, omitted fields or other coverage limits

Do not report a check as run merely because it is prescribed here. A handwritten log cannot guarantee completeness; neither a source diff nor a manifest alone proves there were no other model changes. Bound any unchanged claim to the evidence, such as "mount coordinates unchanged in the generated manifest; internal geometry not compared."

For an early preview, report pending comparisons without holding feedback for polish. Complete the reconciliation before commit/handoff; if a check cannot run, explicitly disclose the gap and its risk, and pause any consequential decision that depends on it. Preserve quick reversible iterations, focused risk checks and the rule that detailed assembly walkthroughs happen only on explicit request.

## Compact review note

Adapt the existing [iteration card](../assets/iteration-card.md); a few lines usually suffice:

- Baseline → candidate: revision IDs
- Changes since previous review: requested + incidental; reason and impact
- Decision needed: only a departure that is not already approved
- Evidence: compared fields/files and relevant before/after views
- Coverage limits: unchecked areas; link to detailed comparison beside CAD

This note supports the user's review; it does not transfer responsibility for discovering omitted changes to them.
