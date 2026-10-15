# Audio and review

## Prepare sound deliberately

Choose the narration source the user/project authorizes: reviewed human recording or an explicitly selected provider. This skill includes no TTS account, music library, paid service, or browser sound renderer. Do not create or upload speech to an external provider without task authorization. Keep raw audio in the project's ignored location, with rights and hashes recorded.

Trim/edit narration without changing scientific meaning. Use licensed recordings or separately implemented procedural sound, documenting sample rate, seed, parameters, and source rights. Match accents to explanatory events when useful; do not distort lesson timing to fit a music beat grid. Use FFrames audio tracks and mix controls from the [pinned audio reference](https://github.com/dmtrKovalenko/fframes/blob/v1.2.0/skills/fframes-video/references/audio.md); verify file availability and track timing before rendering. Use ducking/gain/fades to retain speech intelligibility. Require measured final-file audio and listening, not only a waveform picture.

## Match review depth to the stage

For a first shot, inspect the behavior being tested and obvious media/text defects, then iterate. Run the broader checks below on the release candidate or when a change puts that layer at risk; they are not a gate before every draft.

## Keep the review layers distinct

Use only layers present in the deliverable. External expert review is needed when the content or unresolved expertise requires it, or the user requests it; never invent reviewer approval. The helper details below apply when using that helper, not as a requirement to generate planner metadata.

| Layer | Evidence |
| --- | --- |
| Native structure | Resolved FFrames timeline; inspect diagnostics; missing fonts/media, SVG validity, panic/layout errors addressed |
| Composition and motion | Strip/onion/frame previews, scene boundaries, safe areas, semantic consistency, visible labels and useful holds |
| Final encoded media | `qc.py` when plan metadata exists, or equivalent ffprobe/FFmpeg checks against the brief; actual encoded output, dimensions/FPS/duration and applicable audio checks |
| Language and teaching | Applicable glyph/terminology/caption checks, measured narration pacing; educational learning check and actual expert-review evidence when needed |
| Scientific and rights review | Educational model/units/source checks when applicable; curriculum records only for claimed alignment; asset rights and an applicable project release validator |

Use native diagnostics for layout/SVG problems; the encoded-file helper does not inspect individual SVG bounding boxes or detect internal text collisions. A native inspect pass also cannot certify teaching quality or scientific correctness.

`qc.py` exits 1 when an implemented automated check fails and 0 when those checks pass; its report still requires manual review. Exit 2 means invalid inputs or a failed tool invocation. It writes a fresh output folder, `qc.json`, and a 4×3 encoded-frame contact sheet. Check `suspect_intervals` even when the exit code is 0. Use explicit planned holds/black intervals with reasons rather than dismissing unexpected output. Detection uses heuristic thresholds, so visually review all flagged intervals and scene boundaries.

The helper checks the average stream frame rate, not every frame timestamp, and duration tolerance is max(2 frames, 0.1 seconds). It checks a -1 dBTP true-peak ceiling and reports integrated loudness without enforcing a universal loudness target. Declare project-specific loudness and narration-level targets separately; listen on practical devices. Silent audio is acceptable only when narration/audio is not required. Audio intelligibility and sync remain manual checks.

A 12-frame sheet is a sample. Watch the complete video to catch flicker, glitches between samples, silent gaps, abrupt cuts, and caption errors. Check glyphs at native resolution. Record ffmpeg/ffprobe, Rust/FFrames, backend, OS, and font versions with production provenance. Rerender after source edits; review the final encoded artifact rather than reusing checks from a draft. Publish only when authorized.
