# Setup

## Install from a clone

Prerequisites are Bash, Python 3.10 or newer, Git, Codex, and a DeepSeek API
credential already usable by Harness. Install either the separate persistent
`dsh-delegate` runtime or the `dsh` CLI with its `headless` profile configured.

```bash
git clone https://github.com/saikhamhein/agent-skills.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R agent-skills/skills/delegate-to-deepseek-harness \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

This copies the skill, helper scripts and references. This repository does not
bundle the persistent Python runtime, its installer, a systemd service, or the
Harness CLI. The launcher looks for `dsh-delegate` at
`~/.local/share/dsh-delegation/current/bin/dsh-delegate` (overridable with
`DSH_DELEGATE_RUNTIME_DIR`) and then on `PATH`. Without it, the launcher uses
`dsh --profile headless`; those runs are one-shot and do not retain project
conversation context. See [sessions.md](sessions.md) for the separate runtime's
session behavior.

Codex detects skill changes automatically; restart only if the skill does not
appear.

## Dedicated API credential

Create a separate API key in the DeepSeek console, then configure it from a
private terminal:

```bash
~/.codex/skills/delegate-to-deepseek-harness/scripts/configure_api_key.sh
```

The prompt does not echo the key. The script stores it in
`~/.config/dsh-delegation/credentials.env` with mode `0600` and restarts the
delegation service. The service and bundled delegation launcher load this file;
normal DSH usage continues to use its existing credential.

For secret-manager automation, send the key over standard input rather than a
command argument:

```bash
secret-manager-command |
  ~/.codex/skills/delegate-to-deepseek-harness/scripts/configure_api_key.sh --stdin
```

Never paste a key into ChatGPT, a worker brief, shell history, or this
repository. Run `configure_api_key.sh --check` to check presence without
revealing the key.

## Configuration

Optional environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `DSH_DELEGATE_DSH_HOME` | `~/.dsh` | Explicit Harness home; the dedicated environment key overrides the shared credential |
| `DSH_DELEGATE_PROVIDER` | `deepseek-official` | Provider route |
| `DSH_DELEGATE_MODEL` | `deepseek-v4-flash` | Worker model |
| `DSH_DELEGATE_PROFILE` | `sdk` | SDK-serving Harness profile |
| `DSH_DELEGATE_REASONING_EFFORT` | unset | Provider reasoning effort |
| `DSH_DELEGATE_MAX_TOKENS` | unset | Positive output-token cap |
| `DSH_DELEGATE_REQUEST_TIMEOUT` | `7200` | Turn timeout in seconds |
| `DSH_DELEGATE_SESSION_SCOPE` | `branch` | `branch` or `project` |
| `DSH_DELEGATE_FALLBACK` | `headless` | `headless` or `none` |
| `DSH_DELEGATE_STATE_DIR` | `~/.local/state/dsh-delegation` | Private daemon state |

## Diagnose

```bash
~/.codex/skills/delegate-to-deepseek-harness/scripts/preflight.sh
dsh-delegate session-id --cwd /path/to/project --json
systemctl --user status codex-dsh-delegation.service
```

The skill preflight requires the dedicated credential file and reports only its
presence. It never prints the key.

## Headless fallback

When the Python SDK is unavailable, the skill may call the installed `dsh`
headless profile. Headless runs are one-shot and do not resume project context.
No automatic fallback occurs after an SDK run begins, because retrying a
possibly mutating task could duplicate work.
