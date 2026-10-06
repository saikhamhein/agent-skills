---
name: fframes-motion-studio
description: Plan, art-direct, animate, preview, render, and review motion graphics and science explainers with native FFrames Rust/SVG and FFmpeg. Use for video briefs, timed storyboards, visual-style or motion comparisons, FFrames scene implementation, narration/caption timing, animation transformations, and final encoded-video quality checks. Includes 51 visual style briefs, 10 motion profiles, 13 video structures, and a science-explainer override.
---

# FFrames Motion Studio

Treat every video as a communication problem. Resolve the brief, storyboard the reasoning, implement deterministic native scenes, inspect representative frames, and review the encoded result. Follow repository instructions and existing lesson contracts before applying any catalog preference.

## Start with the project

1. Read `AGENTS.md`, project tooling/pins, the target lesson's script, storyboard, references, and review records. Preserve unrelated changes. Resolve the learning objective/message, audience, language, aspect ratio, delivery length, asset rights, narration, and requested output. Infer routine choices from the project; ask only for missing decisions that materially block the work.
2. Read [native implementation](references/fframes.md) before writing animation. Read [science and Burmese guidance](references/science.md) for educational work, and [review and audio guidance](references/review.md) before rendering.
3. Use the project's pinned generator, Cargo.lock, native backend, wrappers, and asset locations. This skill targets FFrames 1.2.0; check the official API for the project's actual pin. Use Python 3.11+ standard library for the 2 bundled helpers and FFmpeg/ffprobe for encoded-file checks. No browser renderer, Playwright, DOM, CSS animation runtime, or second animation framework is required.

## Resolve 3 independent layers

Choose **visual style** (palette, typography, geometry, texture), **motion language** (easing, staging, camera, transitions), and **video structure** (story beats). Load only the chosen entries through the planner instead of reading every catalog into context.

From the installed skill directory, list IDs:

```bash
python3 scripts/plan.py --catalog
```

Write a draft outside the installed skill, preferably in the project's ignored working-output folder:

```bash
python3 scripts/plan.py --type science-explainer --style minimal --motion calm \
  --format 9:16 --seconds 90 --fps 30 --brief 'Explain how radius affects tangential speed at fixed angular velocity.' \
  --output-dir /path/to/project/output/preview/lesson-plan
```

Use `--type <catalog-id>` for other structures. Add `--education` to replace any structure with the question → model → mechanism → check → recap teaching arc. Explicit style/motion flags still apply, subject to project constraints. Use `--seed` to record a reproducible procedural seed. The helpers are planners/checkers; they do **not** generate a finished Rust video or implement every effect in the catalogs.

The planner produces `plan.json` and `storyboard.md` with integer frame ranges, selected profiles, and draft fields. End frames are exclusive. It refuses to overwrite a draft. Adopt the content into the project's authoritative storyboard and metadata; do not create a competing release contract. Retime after measuring narration, adjust beat shares to match comprehension, and keep the total frame budget consistent. Draft shares are suggestions, not fixed pedagogical timings.

Treat catalog CSS-like shadow/font/ease names as descriptions. Translate them using `references/fframes.md`; never paste them into Rust as APIs. Font names are suggestions, not bundled/installed font assets. Record deliberate simplifications when a backend cannot implement a requested effect. See [catalog provenance and license](references/provenance.md).

## Build the story and visual system

- Define 1 primary message or learning objective and the viewer's question. Write original narration before detailed polish. Record the scientific model, units, assumptions, sources, and understanding check for lessons.
- For each shot specify its purpose, start/end frame, visible entities, exact labels, narration/captions, model state, camera, transition, reading/thinking time, and exit state. Mark intended static holds and black intervals.
- Establish Rust design tokens for colors, type scale, spacing, stroke weights, safe areas, and transitions. Keep related objects semantically consistent. Use SVG primitives for exact diagrams; use attributed raster assets only where they help.
- Maintain one moving focal point where possible. Reveal relationships in sequence and retain useful labels. Use decorative easing for labels/camera, physical equations for scientific trajectories, and longer holds where the explanation needs them.
- Keep a fixed seed for procedural variation. Evaluate every frame from its time/index, model parameters, and immutable assets. Do not advance mutable simulation state per render call or use unseeded randomness.

## Implement and iterate natively

Generate the crate through the project wrapper, replace the starter demo, and implement `Video`/`Scene` with `svgr!`, typed animation timelines, embedded/licensed media, and an explicit audio map. Use shared components when actual reuse warrants them. Preserve Cargo.lock and generator provenance. Read the project's CLI `--help` before inventing flags.

Run the project wrappers where available; inside a generated crate the normal inspection sequence is:

```bash
cargo run --release --locked -- timeline
cargo run --release --locked -- inspect --help
cargo run --release --locked -- strip --help
cargo run --release --locked -- frame --help
cargo run --release --locked -- audio --help
cargo run --release --locked -- render --help
```

Inspect boundaries, representative states, and full-resolution typography. Review native reports plus strip/frame images. Use the native player when the selected backend supports it; CPU rendering and exported frames support headless review. Add narration/captions, then render a draft and repair specific problems. Verify the resolved timeline after adding scene overlaps; never assume overlap math matches the planned frame budget.

For comparisons, keep script, timing, models, format, and seed fixed while varying only style or motion; render representative frames and short native clips. For a transformation, retain the original message/approved science and change the requested layer. For benchmarks, record backend, machine/tool versions, frames/resolution, elapsed render time, and artifact hashes; do not claim browser or GPU performance without measurements.

## Review the actual deliverable

Run the encoded-file helper on the final MP4 and the **retimed** plan:

```bash
python3 scripts/qc.py --video /path/to/final.mp4 --plan /path/to/plan.json \
  --out-dir /path/to/project/output/preview/final-qc
```

Set `audio_required` for narration videos. Record intentional intervals in `planned_holds` / `planned_black` as objects with `start_seconds`, `end_seconds`, and a `reason`; these are video-global seconds. The helper checks dimensions, average FPS, duration, audio presence, required-audio silence, and true-peak ceiling; it detects suspect black/frozen intervals, measures loudness, hashes the file, and makes a contact sheet from the **encoded video**. Use a fresh output folder for each run.

Read `qc.json`, open `qc-sheet.jpg`, watch the full file, listen to audio, and inspect text at full resolution. Automatic metadata/audio passes leave status `review_required`; exit 0 is not release approval. Black/freeze detection is heuristic and static teaching holds are valid. Native diagnostics, human language/science review, source rights, captions, and phone-sized readability remain required. Correct, rerender, and repeat the affected checks. Record real evidence in the project's review system; never invent approval or a reviewer.

Finish with the actual artifact locations, implemented style/motion choices, measured output properties, checks performed, and any blocked native or human reviews. Run the project's release validator/package command when authorized. Publish or message others only when the task authorizes it.
