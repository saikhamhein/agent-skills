# agent-skills

Reusable agent skills for electronics hardware design, native FFrames video production, and illustrated educational animation.

## Available skills

- [Robot CAD Iteration](skills/robot-cad-iteration/SKILL.md): integrated robot body/mechanism design, revision-bound visual feedback, targeted CAD checks and practical prototype loops. Original workflow informed by the Alpha Rolie journal; no unreleased CAD/tooling is bundled.

- [Electronics Hardware Design](skills/electronics-hardware-design/SKILL.md): component selection, PCB placement and routing, CAD-linked mechanical design, validation, and traceable releases.
- [FFrames Motion Studio](skills/fframes-motion-studio/SKILL.md): brief-to-storyboard workflow, 51 visual style briefs, 10 motion profiles, 13 video structures, native Rust/SVG implementation guidance, narration timing, science/Burmese review, and encoded-video QC.

- [Image Motion Education](skills/image-motion-education/SKILL.md): character and prop animation from generated still images, scene-specific performance planning, educational/FFrames integration, Burmese text guidance, and tested Pillow/FFmpeg helpers. Adapted from Xiayi Sun’s image-animation workflow with retained MIT attribution.

## Use

Install the complete skill directory through your agent's supported skill workflow, then invoke `$electronics-hardware-design`, `$fframes-motion-studio`, `$image-motion-education`, or `$robot-cad-iteration`. Open its `SKILL.md` and follow the referenced workflows and helpers. Hosting a skill here does not automatically install or activate it in an agent.

For local Codex, copy the chosen directory into the consuming project's `.agents/skills/`, or your supported user skill directory. See [official skill installation/discovery guidance](https://developers.openai.com/codex/skills/). Preserve the scripts, references, catalogs, metadata, and license notice together. Refresh/restart the agent if its skill selector has not updated.

Myanmar Science Visuals provides a pinned, hash-verified private-repository installer:

```bash
# Run from a checkout of myanmar-science-visuals, using Git credentials with access to this repo.
node scripts/install-motion-studio.mjs
node scripts/install-motion-studio.mjs --check
```

Motion Studio's bundled Python helpers use Python 3.11+ standard library; encoded-video QC additionally requires FFmpeg/ffprobe. The catalogs are art-direction briefs rather than 51 prebuilt native effects. Read [provenance and the retained MIT notice](skills/fframes-motion-studio/references/provenance.md) before redistributing the adapted catalog assets. The native workflow uses FFrames, with no browser rendering dependency.

The electronics release-audit helper checks file inventory and integrity; it does not qualify hardware. Motion Studio checks media properties and produces review evidence; it does not certify science, language, rights, or release approval.

Image Motion Education keeps existing native renderers in place. Its standalone helpers use Python 3.11+, the bundled Pillow pin, and FFmpeg/ffprobe; OpenCV and TTS are optional. Read its [rendering guide](skills/image-motion-education/references/rendering.md) and [source attribution](skills/image-motion-education/references/provenance.md). The article’s videos are reference material, not bundled production assets.

