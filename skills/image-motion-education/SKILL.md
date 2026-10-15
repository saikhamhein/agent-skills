---
name: image-motion-education
description: Create illustrated educational animations from still-image characters, scene-specific action sequences, blinks, gaze changes and props, using deterministic compositing instead of a video model. Use for cutout, paper, painted, ink or toy-like explainers and character-led teaching scenes. Complements an existing native animation pipeline; exact diagrams and equations stay in that pipeline.
---

# Image Motion Education

Move fast, break things in reversible drafts: build one useful action, watch it, and iterate before expanding the film. Preserve source assets and approved media. Make the character demonstrate, observe or react to the idea being taught. Plan just enough performance to generate the next useful shot. A camera move over one still is not a substitute for a changing action. Each return to an action should develop the explanation; do not recycle gestures, bounces, blinks or camera moves merely to fill time.

## Choose the production path

Read the user's brief and repository instructions first. Keep the requested language, duration, audience, identity, audio choices and output format. Select this workflow when illustrated action adds explanatory value; a character is optional when the mechanism alone explains the concept.

- **Existing native project:** use its renderer, fonts, timeline, safe areas and release workflow. Bring generated PNG poses and props into that pipeline. For FFrames Rust/SVG, pair this with `$fframes-motion-studio`; see [native integration](references/project-integration.md). This skill does not authorize a renderer migration.
- **Standalone image animation:** use Python/Pillow and FFmpeg. Read [rendering](references/rendering.md) for the bundled stepped-pose renderer, dependency setup, commands and limitations. The bundled `morph_rgba_pair.py` uses OpenCV for compatible facial transitions; install its optional dependencies when that technique is chosen.

This is a still-image animation method. Do not call a text-to-video or image-to-video model unless the user asks for that separate approach.

## Make a small clip first

Choose one explanatory beat and the few states it needs. Reuse available artwork or generate only those states, then render a short clip with provisional timing and simple text. Watch the action at delivery size; check the specific contact, transition, or reading problem being tested. Use feedback to revise it before building more assets. A full storyboard, identity atlas, facial system, narration track, or audit suite is not required to start. Respect assets-only requests by returning the smallest useful asset sample instead.

## Develop the teaching and performance

Define one observable learning objective, one central question and one understanding check. Establish the model and verified sources. Outline an observation, a visible mechanism, a pause to predict, and a reveal that answers the question. Adjust that structure to the subject and requested length.

Consult [performance and asset design](references/performance.md) for the shot you are building. Use [action and facial continuity](references/continuity.md) when the shot needs multi-state actions, blinks or gaze changes. A three-expression identity sheet is not a finished performance asset set. As the sequence grows, record the timing, teaching purpose, captions, actions and assets needed to reproduce it; add gaze, contact and transition details when relevant. Reuse the project's storyboard; the [action ledger](assets/action-ledger.md) is an optional starter, not a second required metadata system.

Choose a coherent material, palette, edge treatment, lighting, character identity and background density. Inspect references and distinguish style references from character identity assets. Develop an original character when the reference is supplied for style; do not import unrelated logos or signature character details. Honor user-owned characters and explicit adaptation requests.

Measure recorded or authorized generated narration before locking the timeline. Otherwise use caption-led timing and mark narration absent or pending. Do not assume a TTS voice exists, choose a paid provider, or infer narrator identity from appearance. Keep the script unchanged during alignment. Plan optional licensed music and synchronized sound effects around the explanation and reading holds.

## Grow assets around working shots

Use the available ImageGen tool for new raster artwork and image edits; follow the installed imagegen skill when present. Request transparent output directly for cutouts. Retain source images, prompts, references and licenses in the project's asset locations.

Generate only the identity reference, backgrounds, props and scene-specific states needed for the next shot; expand once the direction works. Specify hands, gaze, contact points and what changes in each state. Keep exact labels, equations and captions as editable, shaped text by default; generate a decorative backing separately. If the user explicitly requires image-generated text, inspect every glyph and disclose unresolved text defects.

For atlases, inspect the original cells before splitting. The bundled alpha-margin audit detects empty or edge-touching cells; it cannot judge anatomy, identity or missing objects. Prefer individual images when a grid sacrifices useful resolution. Do not remove backgrounds or repaint assets with an improvised Python image editor; use ImageGen for those edits. The supplied scripts inspect/extract atlas cells, composite animation frames, and interpolate verified compatible facial states. The facial helper does not repair incompatible artwork or generate new actions.

Use each short clip to test the next uncertainty: a complete action, held-object contact, facial transition, or final-size text. Do not require every feature in the first proof. Fix the largest defect, get feedback, and expand. Follow the requested review cadence without adding approval gates.

## Animate, review and deliver

Separate performance motion from scientific state. Poses can be stepped; model trajectories, directions, quantities and relationships must come from the stated model. Keep contact points stable, purposeful holds long enough to read, and major transitions connected by cause and effect. Evaluate frames from absolute time and immutable assets so seeking gives the same result as sequential rendering.

Classify adjacent states: same-image transform, generated pose step, compatible facial interpolation, or scene cut. Default to generated steps for changing hands, silhouettes or occlusions. Do not dissolve incompatible whole bodies into transparent ghosts. Facial interpolation requires aligned anatomy and inspection of intermediate frames; use the bundled helper and [continuity guide](references/continuity.md). Do not interpolate between unrelated body poses.

For drafts, check the changed shot and report what is provisional. Use [review](references/review.md) for the release candidate. Inspect action boundaries, dense transitions, full-resolution text, contact sheets and the encoded file. Check narration and music by listening when available. Record actual evidence and limits; metadata checks cannot certify pedagogy or language.

Deliver the requested video, reproducible source/commands, required assets and useful captions/cover according to the project's handoff. Preserve exact approved media. Production authorization does not imply social publishing.

See [provenance and observed examples](references/provenance.md) for the article, MIT-licensed upstream helpers, and what was actually inspected.
