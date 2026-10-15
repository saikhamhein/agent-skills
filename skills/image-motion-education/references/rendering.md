# Standalone rendering

Use this path for standalone image animation. Existing native projects keep their renderer; see [project integration](project-integration.md). These helpers composite images and extract atlas cells. They do not generate artwork, synthesize narration, validate science, shape text or decide whether two facial states are compatible. The separate [facial helper](continuity.md) precomputes transparent in-between frames for reviewed compatible pairs.

## Runtime

Python 3.11+, Pillow, FFmpeg and ffprobe are sufficient. Use a project-local virtual environment. The bundled requirements pin the Pillow version used during validation; record actual Python/FFmpeg versions with each production. Reuse a compatible existing environment when available.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r /path/to/image-motion-education/scripts/requirements.txt
```

On Windows, use `.venv\Scripts\python.exe`. FFmpeg is a separately installed system/project dependency. These base commands do not install OpenCV or a TTS service. For the facial helper, use `scripts/requirements-flow.txt` in the virtual environment; see [continuity](continuity.md).

When changing helper behavior or diagnosing an environment problem, run helper tests from the skill folder with `python3 -m unittest discover -s tests -v`. They exercise synthetic fixtures, timing, fresh output protection, atlas margins and a complete FFmpeg encode/decode. They do not prove an ImageGen asset system, voice quality or lesson quality.

## Transparent atlas inspection and extraction

Generate genuine transparent PNG assets through ImageGen. Audit the original equal grid before extraction:

```bash
python3 /path/to/skill/scripts/audit_atlas_safe_margins.py atlas.png \
  --columns 3 --rows 1 --names observe,act,resolve --min-margin-ratio 0.08
python3 /path/to/skill/scripts/split_grid_atlas.py atlas.png poses \
  --columns 3 --rows 1 --names observe,act,resolve --keep-cell-size
```

The margin threshold is adjustable to the artwork. This alpha test cannot detect anatomy mistakes, copied identities or a cut-off feature that happens to end inside the margin. Inspect those visually. Opaque backgrounds fail the margin test; request a corrected transparent asset through the image tool.

`--keep-cell-size` preserves equal canvases instead of tight crops, making anchors easier to maintain. It requires atlas dimensions divisible by the grid. The default crops alpha bounds with 12 px padding; record anchor compensation when using it. Both modes retain antialiased pixels. Use fresh output directories; the splitter refuses a nonempty one. Names are plain stems, not paths.

## Minimal render spec

Paths resolve relative to the JSON spec. Supply actual raster assets; this example is a schema illustration, not a ready-to-render film.

```json
{
  "duration": 4.0,
  "canvas": {"width": 1080, "height": 1920, "fps": 30, "motion_fps": 10, "background": "#101C2B"},
  "character_stages": [
    {"start": 0, "asset": "poses/observe.png", "x": 540, "bottom": 1160, "scale": 1},
    {"start": 1.2, "asset": "poses/act.png", "x": 540, "bottom": 1160, "scale": 1},
    {"start": 2.2, "asset": "poses/resolve.png", "x": 540, "bottom": 1160, "scale": 1}
  ],
  "prop_tracks": [
    {"scene_start": 0, "scene_end": 4, "appear": 0.5, "asset": "props/object.png", "x": 760, "y": 800, "width": 180}
  ],
  "subtitle_tracks": [
    {"start": 0.5, "end": 3.5, "asset": "text/reviewed-caption.png", "x": 540, "y": 1320, "height": 80}
  ],
  "contact_sheet_times": [0, 1.2, 2.2, 3.5]
}
```

For a background image, add `canvas.background_asset`; its pixel dimensions must equal the canvas. Prepare the composition intentionally before rendering. Adapt this example to the requested composition and any existing design system.

- `duration * fps` must be an integer frame count. Express event times as frame index divided by FPS. Intervals include the start and exclude the end.
- Character stages begin at 0, have unique starts and last until the next stage or video end. `x` is image center, `bottom` is the transformed image's bottom edge, and `scale` must be positive. These are **image coordinates**, not detected feet or elbows.
- Pose changes and prop/caption boundaries use full timeline precision. `motion_fps` quantizes local entrance/landing transforms only. Captions are not delayed to the character cadence.
- Holds are stable by default: shadow opacity and decorative displacement/rotation/scale changes are zero. For purposeful landings, set `landing_duration`, `landing_x`, `landing_y`, `landing_rotation`, `landing_scale` on the chosen stage. The x/rotation sign alternates by stage index; inspect it, or write an explicit custom transform when direction matters. `rotation` is a constant pose angle in degrees.
- Prop entrance controls are `entrance_duration`, `entrance_steps`, `entrance_x`, `entrance_y`, `entrance_rotation`, `start_scale`. Only enable them where they explain the entrance. They are artistic transforms, not physical simulation.
- Reuse is allowed for returns, blinks and comparisons. Record its meaning in the action ledger. `allow_pose_reuse: false` optionally rejects duplicate pose paths; it does not detect visual similarity.
- Subtitle tracks accept **pre-rendered** transparent images: use reviewed, shaped native text rasterized by the project's text tools by default. The helper does not create text. `height` sets the whole image height, not font size or visible glyph height. Supply tracks in ascending nonoverlapping time order. It draws at most one caption card at a time.
- Layer order is background → props → character → caption. The starter supports one active character and one static background. For multiple actors, foreground occlusion, moving contact anchors or changing backgrounds, adapt the native project or implement explicit scene/layer tracks; do not claim the starter already supports them.
- The renderer does not clamp assets to safe areas or detect collisions. Check all transformed bounds and visual states. Rendered frames are opaque RGB; original PNG assets retain alpha for native integration.

## Frames, encode and audio

Use a fresh frames folder and contact-sheet path to avoid stale frames or overwriting approved output:

```bash
python3 /path/to/skill/scripts/render_semantic_cartoon.py render-spec.json frames \
  --contact-sheet contact-sheet.png
ffmpeg -n -hide_banner -loglevel error -framerate 30 -start_number 0 \
  -i frames/frame-%04d.png -c:v libx264 -preset medium -crf 18 \
  -pix_fmt yuv420p -movflags +faststart animation-silent.mp4
```

Match `-framerate` to the spec and use even dimensions for this yuv420p encode. `--limit-frames N` makes a partial renderer smoke test; never label that output a full render.

When narration exists, first measure its duration with ffprobe and align the visual frame count to complete phrases and an ending hold. Prepare one approved audio mix with the intended lead-in/pauses and optional music/SFX. Only after verifying that it fits the visual duration, mux it (the 4-second value is illustrative):

```bash
ffmpeg -n -hide_banner -loglevel error -i animation-silent.mp4 -i audio-mix.wav \
  -map 0:v:0 -map 1:a:0 -af apad -c:v copy -c:a aac -b:a 192k \
  -t 4 -movflags +faststart final.mp4
```

`-t` can truncate speech: replace it with the verified visual duration only after checking the mix. Omit the mux for intentionally silent work. Do not silently substitute a TTS provider or assume Burmese voice quality. Read [review](review.md) and inspect the encoded file.
