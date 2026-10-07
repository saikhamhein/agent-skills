# Sources, scope and observed examples

Inspired by Xiayi Sun's [I made animation with Codex, without using a video model](https://medium.com/@sherrysun/i-made-animation-with-codex-without-using-a-video-model-435b812c140e), read in full on 2026-10-07. The practical distinction is generated still artwork plus directed, deterministic animation. The article motivates meaningful pose changes and learning from repeated-gesture failures; it is not evidence that a particular educational explanation is correct.

The linked [sunxiayi/image-motion-animation](https://github.com/sunxiayi/image-motion-animation) was inspected at commit `875a0d402e488a2df358b11fb3cccc3f050c5968`. Its MIT license is retained in [upstream-license.txt](upstream-license.txt). The three bundled Python helpers derive from that commit's files of the same names. The educational instructions, project integration, ledger and tests were written for this adaptation.

Changes to the helpers: stable holds/no shadow by default; raster background support; exact pose/prop boundary timing separate from local transform cadence; intentional reuse allowed; clearer input checks; fresh output directories; optional preservation of atlas cell canvases; filename-stem validation. The starter still has one active character, fixed layer order and no optical-flow, narration or text-generation implementation.

## Video study

The Medium embeds were inspected through their public Vimeo players. The upstream repository also supplies Chinese-language compressed demos. These are related examples, not necessarily identical to the article's English edits. The three local MP4s were inspected at half-second intervals across their full timelines; browser examples were inspected at selected playback positions. This is visual motion study, not a claim of complete audio or language review.

| Example | Observed visual pattern | Application / limit |
| --- | --- | --- |
| [Translation story](https://vimeo.com/1217443176) | Flat cutout character paired with a topic prop cluster; reading, professional admiration and laptop-related poses change with the subject | Use scene-specific relationships; avoid a generic talking mascot |
| [Winter cat](https://vimeo.com/1217443179) | Consistent knitted clothing and soft environments; letters, writing and luggage give hands concrete tasks | Generate coherent object-contact states and preserve anchors; confirm final caption placement separately from visible player controls |
| [Designer toy](https://github.com/sunxiayi/image-motion-animation/blob/875a0d402e488a2df358b11fb3cccc3f050c5968/demos/designer-toy/designer-toy.mp4) | 21 s, 960×540, 24 fps; spoon/cup action around 4.5–7 s, foaming result/reaction around 8–11 s, flower pickup around 16 s followed by a hold | Several poses can express one action; cute props do not establish a scientifically valid experiment |
| [Retro screenprint](https://github.com/sunxiayi/image-motion-animation/blob/875a0d402e488a2df358b11fb3cccc3f050c5968/demos/retro-screenprint/retro-screenprint.mp4) | 18 s, 960×540, 24 fps; lowering a mask, touching the cheek, makeup-tool gestures and a mirror sequence share a cream/black/red graphic system | Material/palette can change while action grammar remains; inspect hand-to-face occlusion |
| [Zodiac ink](https://github.com/sunxiayi/image-motion-animation/blob/875a0d402e488a2df358b11fb3cccc3f050c5968/demos/zodiac-ink/zodiac-ink.mp4) | About 31.79 s including audio, 960×540, 24 fps; animal poses then a cycle and grouped associations, with long explanatory holds | A character narrator is optional; review edge safety because some sampled source text reaches/crosses the left edge |

Reference footage and generated characters are not bundled as new production assets. Learn from the method and create the lesson's own artwork. Keep the license notice with redistributed helper code; the software license does not establish rights to unrelated user-supplied images, music or fonts.

For implementation semantics, consult the [Pillow Image API](https://pillow.readthedocs.io/en/stable/reference/Image.html), [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html), and the consuming project's pinned native API. Do not infer runtime capabilities from the demo's appearance.
