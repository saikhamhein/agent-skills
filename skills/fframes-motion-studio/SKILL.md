---
name: fframes-motion-studio
description: Plan, art-direct, animate, preview, render, and review motion graphics and science explainers with native FFrames Rust/SVG and FFmpeg. Use for video briefs, timed storyboards, visual-style or motion comparisons, FFrames scene implementation, narration/caption timing, animation transformations, and final encoded-video quality checks. Includes 51 visual style briefs, 10 motion profiles, 13 video structures, and a science-explainer override.
---

# FFrames Motion Studio

Move fast, break things in reversible drafts: render the smallest useful shot, inspect it, and improve it from feedback. Treat every video as a communication problem. Preserve source assets and approved outputs; fast iteration never substitutes for scientific accuracy, rights checks, or final-media review.

## Start with one useful shot

1. Read applicable repository instructions and identify the message, requested format, language, and renderer pin. Reuse existing assets and infer reversible defaults; ask only for a decision that blocks useful work.
2. Sketch one beat and render a short clip that tests the hardest visual relationship or timing choice. Use [native implementation](references/fframes.md) for the API details you need. A complete storyboard, catalog selection, narration track, and full QC suite are not prerequisites for a draft.
3. Watch that clip and check the changed behavior, relevant text, and scene boundaries. Share or use feedback, fix the largest issue, and repeat. Expand the story and asset system only after the direction works.
4. Consult [science and language guidance](references/science.md) for educational claims and [review and audio guidance](references/review.md) as sound or release work needs them. Keep provisional claims and review limits visible.

Use an existing pinned generator, Cargo.lock, backend, and wrappers when available; otherwise use the supported native setup. The API examples target FFrames 1.2.0, so verify signatures for the version actually installed. The two bundled helpers use Python 3.11+ standard library; encoded-file checks use FFmpeg/ffprobe. No browser renderer or second animation framework is required.

## Expand the working direction: 3 independent layers

The catalog planner is optional; a short shot can start with a few tokens and a handwritten beat. Choose **visual style** (palette, typography, geometry, texture), **motion language** (easing, staging, camera, transitions), and **video structure** (story beats). Load only the chosen entries through the planner instead of reading every catalog into context.

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
- As shots develop, capture the details needed to reproduce them: purpose, frame range, entities, labels, narration/captions, model state, camera, transition, useful holds, and exit state. Do not fill a large shot ledger before testing the first beat. Mark intended static holds and black intervals.
- Establish Rust design tokens for colors, type scale, spacing, stroke weights, safe areas, and transitions. Keep related objects semantically consistent. Use SVG primitives for exact diagrams; use attributed raster assets only where they help.
- Maintain one moving focal point where possible. Reveal relationships in sequence and retain useful labels. Use decorative easing for labels/camera, physical equations for scientific trajectories, and longer holds where the explanation needs them.
- Keep a fixed seed for procedural variation. Evaluate every frame from its time/index, model parameters, and immutable assets. Do not advance mutable simulation state per render call or use unseeded randomness.

## Implement and iterate natively

Generate the crate through an existing wrapper or the supported FFrames generator, replace the starter demo, and implement `Video`/`Scene` with `svgr!`, typed animation timelines, embedded/licensed media, and an explicit audio map. Use shared components when actual reuse warrants them. Preserve Cargo.lock and generator provenance. Read the project's CLI `--help` before inventing flags.

Use the project wrappers where available. Inside a generated crate, select the command needed for the current question; this is a command menu, not a mandatory sequence:

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

## Review the release candidate

Drafts need targeted checks and honest limits. Before final delivery, inspect the actual encoded file. When using a plan, run the helper on the final MP4 and the **retimed** plan:

```bash
python3 scripts/qc.py --video /path/to/final.mp4 --plan /path/to/plan.json \
  --out-dir /path/to/project/output/preview/final-qc
```

Without a plan, use ffprobe/FFmpeg or equivalent tooling to verify encoded dimensions, FPS, duration and any required audio against the brief; do not create planner metadata solely to pass a helper.

When using the helper, set `audio_required` for narration videos. Record intentional intervals in `planned_holds` / `planned_black` as objects with `start_seconds`, `end_seconds`, and a `reason`; these are video-global seconds. The helper checks dimensions, average FPS, duration, audio presence, required-audio silence, and true-peak ceiling; it detects suspect black/frozen intervals, measures loudness, hashes the file, and makes a contact sheet from the **encoded video**. Use a fresh output folder for each run.

If using the helper, read `qc.json` and open `qc-sheet.jpg`. In all cases, watch the full file, listen to any audio, and inspect text at full resolution. Automatic metadata/audio passes leave status `review_required`; exit 0 is not release approval. Black/freeze detection is heuristic and static teaching holds are valid. Check relevant native diagnostics, source rights, captions and delivery-size readability. Educational claims and language need appropriate review; seek qualified human review for unresolved expertise or when requested, and label pending review honestly. A generic motion clip does not require an external science or language reviewer. Correct, rerender, and repeat the affected checks. Record real evidence in the project's review system; never invent approval or a reviewer.

Finish with the actual artifact locations, implemented style/motion choices, measured output properties, checks performed, and any blocked native or human reviews. Run the project's release validator/package command when authorized. Publish or message others only when the task authorizes it.
