# Agent Skills: DeepSeek Delegation for Codex, Electronics, CAD and Animation

My personal collection of agent skills for coding delegation, electronics, CAD, video production and educational animation. I created and adapted these for my own projects and working preferences, and share them in case they are useful to others.

## DeepSeek delegation for Codex, with Claude support planned

### Why I built it

I wanted to spend fewer expensive-model tokens on implementation and large-document processing. My goal is to keep Codex and Claude Opus focused on thinking, planning and review, while delegating bounded implementation and read-heavy tasks to DeepSeek.

The published skill currently documents Codex setup and orchestration. Claude support is planned.

### How the workflow works

1. **Codex defines the task:** set the scope, constraints and acceptance criteria.
2. **DeepSeek does the bounded work:** implement a change, repair tests, explore a repository, or process a clearly scoped set of text documents.
3. **Codex verifies the result:** run the agreed checks and review changes before accepting them.

Keep architecture, ambiguous decisions, security-sensitive judgment and final verification with the lead agent. Give DeepSeek complete, independently checkable tasks rather than an open-ended project.

The aim is to reduce premium-model token usage. Actual token usage and cost depend on the task, context, retries and review overhead.

### Get started

Read the [DeepSeek Harness delegation skill](skills/delegate-to-deepseek-harness/SKILL.md), follow the [setup and prerequisites](skills/delegate-to-deepseek-harness/references/setup.md), and check the [session guide](skills/delegate-to-deepseek-harness/references/sessions.md).

Persistent project sessions require the separate `dsh-delegate` runtime, which is not bundled in this repository. The launcher can fall back to an installed DeepSeek Harness CLI with a configured headless profile; those runs are one-shot.

## Status and expectations

These skills are experimental and evolve with my work. They may be incomplete, contain mistakes, depend on a particular setup, or stop working as tools change. There is no guarantee that they will work for your use case, and no promise of support or maintenance.

Everything is provided **as is, without warranty**. Review the instructions and scripts before use, adapt project-specific assumptions, and independently check the results. Automated checks do not certify hardware safety, scientific accuracy, language quality, asset rights or production readiness.

## Working mindset

Move fast, learn from small failures, and iterate. Start with the smallest useful result, show it early, run focused checks, and improve it through feedback. Keep experiments reversible and save deeper reviews for real risks or release decisions. Speed is not a reason to hide failures or skip essential safety.

## Available skills

- [DeepSeek Delegation for Codex](skills/delegate-to-deepseek-harness/SKILL.md): bounded implementation and read-heavy work through DeepSeek Harness, with independent verification. Persistent sessions require the separate runtime; the headless fallback is one-shot. Claude support is planned.
- [Electronics Hardware Design](skills/electronics-hardware-design/SKILL.md): component selection, PCB layout, mechanical integration, validation and traceable releases.
- [Robot CAD Iteration](skills/robot-cad-iteration/SKILL.md): preview-first robot design, short feedback rounds, focused functional checks and revision-linked project logs.
- [FFrames Motion Studio](skills/fframes-motion-studio/SKILL.md): native FFrames production guidance, visual-style catalogs, planning and encoded-video checks.
- [Image Motion Education](skills/image-motion-education/SKILL.md): educational animation from still artwork, purposeful character actions and image-processing helpers.

## Use

Read the chosen skill's `SKILL.md`, then install the complete directory through your agent's supported skill workflow. Keep its references, scripts, assets and license notices together. Hosting a skill here does not automatically install or activate it.

Each skill has its own dependencies and limits. Follow the consuming project's current instructions and tool versions. The workflows are reusable; choose requirements, branding and design constraints for the task at hand.

## Ideas and attribution

I do not claim that all ideas, techniques or workflows in this repository are original to me. These skills combine personal experience with existing tools, public documentation, community work and adaptations of others' material. Credit belongs to the respective authors.

See [THIRD_PARTY.md](THIRD_PARTY.md) and each skill's provenance notes for known sources, adaptation details and retained notices. Referencing a project does not imply its author's endorsement.

## License

My contributions are released under the [MIT License](LICENSE). Third-party material retains its original copyright notices and applicable license terms; the root license does not replace them. Preserve all applicable notices when copying or redistributing.

Linked articles, videos, CAD projects, fonts and other external assets are not automatically covered by this repository's MIT license.
