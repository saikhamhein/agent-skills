# Integrating into an educational animation pipeline

Use the consuming repository's renderer, typography, timeline and asset conventions when available. Integrate one short shot first; do not migrate a pipeline or create a second metadata system just to try illustrated animation.

## Native FFrames integration

Follow the installed FFrames pin and official API references. Retain Cargo.lock and generator provenance. Bring transparent PNG poses into the native media provider and select them with integer, end-exclusive frame intervals. Transform around a shared contact anchor. Keep equations, exact geometry, shaped text and physical state in Rust/SVG, and reuse existing audio/caption tools.

For compatible facial transitions, precompute transparent in-between frames with the bundled helper and select one per output frame. Body/hand changes use their own generated pose states and stepped intervals. Preserve common canvases and anchors; do not dissolve incompatible whole bodies. Install Pillow/OpenCV only when a selected preprocessing step needs them.

Use existing design tokens when provided. For new work, choose palette, typography, safe areas and dimensions from the brief, then test the longest caption and most demanding pose at delivery size. Do not impose a particular brand, zone layout, font size or opening treatment.

## Language-sensitive typography

For Burmese, use Unicode and a licensed font with appropriate shaping support. Inspect actual glyph ink, stacked marks and line breaks on the rendering backend. Mixed Latin letters and digits need compatible font coverage and deliberate sizing. Use phrase-level timing; whitespace counts do not reliably estimate Burmese speech duration. Measure real narration before locking audio-led timing.

Keep fluent-language review pending when it has not occurred; do not equate a loaded font with correct shaping or an approved script. These checks apply when Burmese is requested, not as a default language choice. Apply equivalent script-specific checks for other languages.

## Drafts and release

A provisional clip can use simple captions and silent timing. Check the changed behavior, show it, and iterate. Before release, verify scientific claims and model limits, text/language, media correctness, asset rights and any required attribution. Curriculum mapping is needed when requested; leave unknown source metadata unknown.

Deliver the exact approved media with reproducible sources and useful commands. Do not rerender solely to rename a draft as final or invent approval forms. Publishing requires authorization separate from generating a local video.
