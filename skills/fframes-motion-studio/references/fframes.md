# Translate motion direction to native FFrames

Target the consuming project's pinned FFrames version. These examples reference version 1.2.0. Use its existing generator and backend instead of bootstrapping an unrelated rendering stack. Read the [official skill](https://github.com/dmtrKovalenko/fframes/blob/v1.2.0/skills/fframes-video/SKILL.md), [API guide](https://github.com/dmtrKovalenko/fframes/blob/v1.2.0/skills/fframes-video/references/api.md), and [Rust API](https://docs.rs/fframes/1.2.0/fframes/) for exact signatures. The references below guide translation; they are not a replacement crate/template.

| Source concept | Native implementation |
| --- | --- |
| Browser scene / DOM tree | A Rust `Scene` returning SVG through `svgr!` |
| Global JavaScript seek/time | Scene-relative `frame.index` / `frame.seconds()`, or video-global `frame.global_index` |
| CSS palette/type/spacing variables | Rust constants or token structs; SVG attributes |
| CSS transforms and camera | `Transform` values and enclosing SVG groups; calculate pivot compensation |
| GSAP/CSS easing names | Supported `Easing` variants or explicit absolute-time functions |
| Screenshot preview/render | Native `frame`, `strip`, `inspect`, `preview`, and `render` commands |
| Browser assets/font loading | Licensed media and fonts in the generated crate's media provider |
| Three.js object/effect | SVG geometry for exact diagrams; supported Skia shaders only when justified and verified |
| FFmpeg final pass | Final-file verification, audio analysis, contact sheets, delivery conversion |

## Scenes and time

Keep scenes as fields of the video (or zero-sized instances) so `define_scenes` can return references. Render active scenes using `ctx.render_scenes(&frame)`. Use `Duration::Frames` when exact frame counts matter; use measured audio duration when narration determines timing. Check the resolved timeline and total output after adding `Overlap::Previous` because overlap windows affect duration.

Write literal SVG text as quoted strings in `svgr!`; use Rust expressions for typed values. Build static subtrees once and wrap them in animated transforms/opacity. Scope SVG gradient/mask/filter IDs to each component instance. Avoid zero-size SVG geometry: use a small positive dimension or omit the subtree until it appears.

Evaluate scientific state analytically from absolute time whenever possible. For an integration model, precompute a deterministic trajectory with fixed solver step and interpolate by frame time. Seeking frame 900 before frame 0 must give the same image as sequential rendering. Use seeded noise or deterministic functions for texture/drift, never a mutable RNG advanced once per frame.

## Easing translation

For catalog `in`, `out`, and generic `smooth`, choose `Easing::EaseIn`, `EaseOut`, or `EaseInOut` and record that interpretation. For an explicit curve, use `CubicBezier(x1, y1, x2, y2)` with documented control points. For a spring, use `Easing::Spring { mass, stiffness, damping }` with physically valid parameters; catalog shorthand is not Rust syntax. Do not assume these curves exactly reproduce catalog labels such as `outQuart` or `outBack`.

If an exact quartic/sine/back curve matters, implement a tested normalized function with `u = clamp((t-start)/duration, 0, 1)` and evaluate it directly. Use `frame.animate` with `fframes::timeline!` for compile-time keyframes; use `frame.animate_runtime` / `AnimateRuntimeInput` and `AnimationRuntime` for data-driven start times and staggering. Consult the pinned API for lifetimes and field types. Use ample spring settling time and inspect the end state.

For scientific motion, compute position from the stated model, not an artistic spring. At fixed angular velocity, for example, `theta(t) = theta0 + omega*t`, `x = cx + r*cos(theta)`, `y = cy + r*sin(theta)`, and speed `v = omega*r`. Distinguish SVG downward-positive y from the scientific coordinate convention and label any screen mapping.

## Typography and assets

Add real font files and their licenses; catalog font strings are design suggestions only. Use the exact registered family/weight in SVG and `FontQuery`. Call `text_width` / `text_break_lines` to measure rendered text rather than estimating width from character count. Handle failed lookup explicitly; silent fallback is not evidence the chosen font is present. Inspect text diagnostics and full-resolution frames on the selected backend.

Use the generated media provider, commonly `include_media_dir!`, with its path resolved against the Cargo workspace root. Prepare media before creating the render context. For large/stereo assets use the documented runtime media provider. Keep private/large media outside Git according to the project; record hashes, licenses, and transformation provenance. Do not use starter/demo font licensing as evidence that an added font is licensed.

## Effects and backends

Translate CSS-like shadows into supported SVG filters; avoid expensive changing filters on CPU unless measured acceptable. Translate blur/reveals into opacity, masks, clip paths, and transforms. Build exact charts/physics diagrams from calculated SVG coordinates. Use Skia GPU shader APIs only with that backend, test shader compilation, and inspect actual output. The CPU backend does not execute Skia shaders; explicitly implement an SVG fallback or report a blocked effect.

Use native Rust/SVG for cut, fade, mask, wipe, push, and zoom transitions. Prototype one transition and inspect its boundaries before applying it everywhere. Keep CPU-safe defaults for headless work. Preserve intentional still frames, and do not introduce shake, glitch, particles, or tracking changes merely to fill the screen.
