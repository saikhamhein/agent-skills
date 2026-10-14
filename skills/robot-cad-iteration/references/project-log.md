# Revision-linked robot project webpage

The log is a review surface for the real design, not a second CAD model or a substitute for showing progress in chat. Reuse the existing project page, assets and viewer when possible. A local HTML file or private project preview is sufficient; creating a public website, changing access or exposing private CAD requires the appropriate authorization. A private repository does not automatically make a deployed page private. Verify actual hosting access before sharing.

## Minimum useful page

1. **Latest review:** whole-assembly image, exact source revision/branch, build/export time and status (provisional, ready for review, accepted direction, or incomplete/blocked). Name the authoritative native assembly separately when it differs from the review candidate.
2. **Model access:** a real rotatable model if the environment can serve it, plus native source/export links within permitted access. Bind each model asset to its generating CAD revision, units and coordinate transform. If an embedded viewer is unavailable, use actual static views or a recorded orbit and say so. When rotation was requested, mark this as partial fulfillment and keep the viewer request unresolved. Never display inert rotate controls, an empty canvas, a placeholder mesh or an unrelated older model as a working current viewer.
3. **Revision log:** newest first, one entry per real meaningful iteration. Record date, revision, goal, changed geometry, fixed interfaces, same-view before/after images and the review question. Preserve previous entries rather than replacing history with the latest render.
4. **Feedback:** original note, referenced part/location/view/revision, current disposition and the user's response when received. “Implemented” is not “accepted.” A static page may link back to the actual feedback conversation; do not show a nonfunctional submit form. Real comment systems need tested persistence and authorization.
5. **Evidence and unresolved issues:** checks actually run, their scope and source revision; untested physical claims; known clashes, service limits and blocked operations; next small test or decision. Include genuine failed attempts when consequential, with their outcome. Never invent an attractive history of progress.

## Freshness and publishing discipline

- On each visible iteration, update the latest-review pointer and append the entry from the same source revision. Keep a compact asset record: source revision/hash, generator/export command, build time, image/model path, view and check result. The iteration card can supply this; no separate database is required.
- Replace “current” assets only after they open and match the intended revision. If export fails, retain the last valid assets labeled with their older revision and show the new revision as blocked. Do not silently pair new prose with stale images or reuse a check on changed geometry.
- Keep before and after images on the same framing, pose, visibility and scale, or explicitly describe why they differ. Captions identify both revisions. Surface whether a view hides panels; visibility is not removal evidence.
- Verify source/model/download links resolve for the intended viewer. Check model loading, rotation and reset if interactive; check mobile/desktop layout and image readability. Do not claim these interactions were tested when only HTML or asset existence was checked.
- Keep editing cheap: update the log at preview handoff, not after every CAD command. Prefer a short factual entry over design polish. If the page build blocks progress, send the real images and revision summary directly, then repair the log without stalling CAD.

## Using the bundled template

`assets/project-log.html` is a self-contained, responsive static shell with explicit empty states and no external scripts, telemetry or fake controls. Copy it into the project's log directory and replace its empty states with real project evidence. Add accessible figures/captions and real links only when those assets exist. Duplicate the revision article for actual iterations. Add an embedded model viewer only when supported and tested; otherwise retain labeled static/orbit review. Remove template guidance from the finished project page. Do not publish the empty template as a completed project log.
