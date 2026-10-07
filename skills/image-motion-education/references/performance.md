# Performance and assets

## Direct an action

Give each beat an explanatory verb: compare, place, open, pour, measure, look, predict or reveal. The character's gaze and hands should point to the object or relationship the viewer needs to notice. Avoid unrelated pointing, idle bobbing or a generic pose library repeated throughout a lesson.

One action can need several poses: notice → prepare → contact → consequence → settle. Choose only the states that make that action legible. Compare silhouettes, head angle, hand activity and prop relationships across the whole storyboard. Repetition is useful for controlled comparisons and callbacks; record why it returns rather than banning reuse or demanding a fixed number of differences.

For an experiment, show the initial condition before the intervention and hold its result. Keep the measuring tool or object identity consistent. If a character is only an observer, their reaction must not imply that they caused the physical process.

## Timing choices

Keep delivery FPS separate from pose cadence. A 30 fps video can hold selected poses for several frames while a physical model moves continuously. Use a small number of deliberate action states and longer resolved holds; do not apply one low-FPS quantizer to captions, scientific motion and sound.

As a starting experiment, hold action intermediates for roughly 0.15–0.3 seconds and a resolved pose for at least 0.5 seconds. Dense ideas and Burmese copy usually need longer. These are adjustable performance suggestions, not reading-speed guarantees. A blink needs an open–closed–open cycle. Short close/open phases may disappear if quantized with the body poses, so schedule their actual frames separately. Do not blink on a rigid repeating timer.

## Transition choice

| Change | Implementation | Review focus |
| --- | --- | --- |
| Same pose, slight emphasis | Small anchored transform | Feet/hands remain attached; scale does not pulse accidentally |
| Arm, body, held object or occlusion changes | Generated intermediate states, then discrete switches | Anatomy, object count, contact and identity continuity |
| Eyelid/gaze only, same geometry | Generated facial states; optional localized optical flow | Pupil count, edge halos, closed eyes reopening |
| New scene/viewpoint | Cut at a meaningful boundary | Attention target, orientation and explanatory continuity |

Optical flow estimates pixel movement; it does not understand anatomy or recover hidden surfaces. Use it only for pairs already inspected as compatible. Normalize scale and facial/contact anchors first. If implemented, warp and blend with premultiplied alpha, inspect dense transition frames and switch to generated intermediate art if eyes or edges distort. Do not stretch an illustration to simulate a new hand pose. The bundled renderer does not implement optical flow, rigging or lip-sync.

## Generate separable, consistent assets

Define an identity anchor with stable face, proportions, clothes, palette and distinctive marks. Reuse that approved original anchor in later image-generation requests. Record each reference's role: identity, material, palette, environment or composition.

A useful asset request states:

```text
Asset: transparent action poses for an illustrated lesson.
Identity reference: the supplied original character.
Style: [medium, palette, lighting and edge treatment].
Action: [specific interaction, including both hands and gaze target].
States: [preparation], [contact/intermediate], [resolved result].
Keep: character proportions, clothes, prop design, camera and light direction.
Layout: separate complete silhouettes with generous transparent padding.
No text, extra props or baked-in cast shadow unless explicitly required.
```

Request 10–15% breathing room around an atlas cell as a useful starting margin. Inspect tails, fingertips, noses and prop corners. Run the supplied audit on the **unsplit transparent atlas**, then split. A crop with missing fingers cannot be repaired by making it smaller. Regenerate the affected source. Keep source and derived crops separately.

Cropping every pose independently changes its coordinate frame. Record a meaningful anchor such as the midpoint between planted feet or the resting elbow. Normalize to a shared canvas or compensate in placement. The starter renderer uses the image's bottom edge, not a detected foot: it needs consistent transparent padding and pose scale. A held object should normally be drawn with the holding pose or have a documented hand anchor and occlusion order.

Ask for backgrounds without independently moving subjects, labels or scientific apparatus. Reserve negative space before generation. Keep light, ground plane, perspective and texture scale consistent. Do not mirror text, scientific directions or asymmetrical landmarks to fill another composition.

Generated artwork can establish context, but exact force arrows, graphs, geometry and quantities should use the verified native model. Keep symbolic artwork visually distinct from measured data. Preserve the requested brand/layout when borrowing a reference's material or mood.
