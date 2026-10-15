# Lightweight revision log

Use a log when it helps an ongoing design stay understandable. Reuse an existing page or a short local document; do not create a website or viewer just to satisfy this workflow. A log should take less effort than the change it records.

## Minimum useful entry

- Source revision and a clear whole-assembly preview
- Changes since the identified previous review, including incidental changes, their reason/impact and the question they answer
- Link to the source/model/part-manifest comparison beside the CAD, with mechanically checked versus unchecked coverage
- Focused check result and any important unknown
- Feedback or the next decision

Keep the user-facing summary short and high-impact. Surface changed assumptions, scope or unplanned drift immediately; recording them here is not a substitute for notification or a required decision. Follow [change-review.md](change-review.md) to reconcile the note against actual differences before commit or handoff.

Add matching-camera before/after views, part annotations or export links when they help. Keep accepted direction separate from validated engineering. Record actual results and failures; do not invent a progress history.

## Keep evidence attached to the right revision

Update the latest-view pointer only after the new asset opens and matches its source. If export fails, retain the last valid view with its older revision and label the new attempt incomplete. Reuse check results only while the relevant geometry and assumptions remain unchanged.

For feedback, keep the original note with its part, view and revision. Mark it implemented, superseded or unresolved; only the user can establish their acceptance. A screenshot annotation is often enough.

## Optional interactive page

The [HTML template](../assets/project-log.html) provides static empty states, not a model viewer. Replace them with real evidence and remove unused sections. Do not present the unfilled template as completed work.

When an interactive viewer is requested and supported, bind the review mesh to its native source and check actual model loading, rotation, selection and note persistence as applicable. If unavailable, give labeled static views or an orbit video and explain the missing requested interaction. Avoid fake controls and inert forms.

Verify links and intended access before sharing. A private repository does not make a separately deployed page private; publication needs the relevant authorization. Keep the log local when public access is unnecessary.

If log work blocks progress, send the actual preview and short update directly. Repair the log later without holding up CAD.
