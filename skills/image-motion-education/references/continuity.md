# Action sequences and facial continuity

The author’s two-layer performance workflow is retained here: generated states
carry meaningful body/prop actions; compatible facial states carry blinks and gaze
changes. See [provenance](provenance.md) for the upstream source and MIT license.

## Build a performance, not an expression slideshow

A reusable character sheet locks identity. A lesson needs states designed for its
actual action: notice an object, prepare, make contact or change position, observe
the consequence, and hold the result. Choose the stages the action needs rather
than assigning every scene the same number of images. For example, examining a
cloth can use a glance toward it, a lowered head, a closer inspection, then a gaze
toward the demonstrated result. The character must not appear to cause the science
by looking at it.

Design gaze targets, eyes, head, paws, prop contact and the final state together.
Eyes can lead a voluntary head/hand action; a reaction to a demonstrated event must
follow the visible evidence. Give the result time to read. Use stillness between
actions, not periodic idle motion. Do not make every scene repeat the same blink,
lean, reaction and reset.

For character-led animation, plan both layers:

- **Action:** starting posture → preparation → intermediate/contact states →
  consequence → resolved hold. Generate states for changes in paws, pose, props,
  silhouette or occlusion. Inspect the complete contact path, not just endpoints.
- **Face:** a motivated glance or complete blink near a thought boundary. A blink
  must show open → closing → closed → opening → open; gaze should arrive at its
  intended target. Leave the character still during a dense explanation.

Do not turn this into a compulsory blink in every shot. Include a readable facial
performance where it adds life without competing with the lesson. Record its
timing separately from stepped body action and exact scientific state.

## Choose the transition

| Pair | Treatment |
| --- | --- |
| Same image, small intentional repositioning | Native transform around a stable contact anchor |
| Same canvas, face geometry, silhouette, paws, props and lighting; only eyes/gaze change | Reviewed facial interpolation |
| Changed head/body angle, paws, fur markings, mouth interior, props or occlusion | Generated intermediate states with stepped timing |
| New camera or scene | A motivated scene cut |

A shared character identity alone does not make a pair safe. Do not morph between
the cat’s seated, crouching and raised-paw identity poses. Generate compatible
face-only variants of the particular scene pose first. Never crossfade incompatible
whole bodies to hide a pose change. If a trial makes eyes smear, fur swim or the
white sticker border breathe, use better aligned/generated states.

## Timing at the delivery frame rate

Start with roughly 80–140 ms closing, 60–120 ms closed, and 100–180 ms reopening for
a blink; roughly 250–450 ms for a gaze shift; and 160–300 ms for a generated action
stage. These are directing starting points, not universal timing requirements.
Quantize to the actual delivery FPS and inspect the full cycle at normal speed.
At 30 fps, for example, a blink may use 3 closing intervals, 2 closed intervals,
and 4 reopening intervals. Reading and thinking holds are longer and content-led.

## Bundled facial-interpolation helper

Use `scripts/morph_rgba_pair.py` only after inspecting a compatible pair. It
normalizes whole canvases by height/bottom, estimates bidirectional DIS optical
flow on neutral composites, and warps/blends premultiplied RGBA. It does not detect
eyes, align facial landmarks, restrict itself to a face region, create new poses,
repair anatomy, rig a character, or perform lip-sync. Equal canvas sizes are a
basic check, not proof of alignment. If necessary, prepare properly registered
source states before invoking it.

Install the optional extra in a virtual environment; a working OpenCV installation
already exposing `cv2.DISOpticalFlow_create` can be reused. Do not install multiple
OpenCV wheel variants into the same environment.

```bash
.venv/bin/python -m pip install -r /path/to/skill/scripts/requirements-flow.txt
.venv/bin/python /path/to/skill/scripts/morph_rgba_pair.py \
  face-open.png face-closed.png blink-close \
  --frames 4 --canvas-width 760 --canvas-height 760 \
  --target-height 680 --bottom 720
```

The output includes both normalized endpoints: four images represent three
transition intervals. Choose counts from the intended frame budget, hold the
closed state explicitly, then interpolate a separately verified reopening pair.
Avoid accidentally doubling boundary frames when joining sequences. Use a fresh
output folder. `morph.json` records input hashes, parameters and runtime versions;
it does not certify visual quality.

For FFrames, embed the reviewed PNG sequence and select frames by absolute frame
index. Face transitions can run at delivery FPS while body steps have longer
holds; captions and scientific trajectories keep their own timing. For the
standalone renderer, list the precomputed images as explicit pose stages. Neither
renderer calls this helper automatically. Do not generate a motion proof or full
video while the owner has paused rendering or requested assets only.

## Review before expanding the film

When rendering is authorized, prove one complete action and its facial performance
in a short clip. Inspect every short facial intermediate plus both sides of each
body-pose switch, and watch normal-speed playback. Check eye count and reopening,
gaze target, muzzle and whiskers, sticker-border stability, body/contact anchors,
prop identity and the changed final state. Full sequence review matters: attractive
individual images do not establish convincing acting.

The helper tests use synthetic inputs to check endpoints, alpha edges, output
protection and a real OpenCV run. They do not approve a production character pair.
