# agent-skills

Reusable agent skills for electronics hardware design, including mechanical integration and manufacturing workflows.

## Available skills

- [Electronics Hardware Design](skills/electronics-hardware-design/SKILL.md): component selection, PCB placement and routing, CAD-linked mechanical design, validation, and traceable releases.

## Use

Open the linked `SKILL.md` and use its referenced workflows, templates, and optional release-audit helper for the task at hand. To use it with a skill-enabled agent, install the complete `skills/electronics-hardware-design` directory through that agent's supported skill workflow, then invoke `$electronics-hardware-design`.

Hosting this skill in the repository does not automatically install or activate it in an agent. The release-audit helper checks file inventory and integrity; it does not qualify hardware.
