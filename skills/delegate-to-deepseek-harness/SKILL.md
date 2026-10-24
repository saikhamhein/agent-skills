---
name: delegate-to-deepseek-harness
description: Delegate bounded, implementation-heavy, repetitive, or read-heavy coding work from Codex to DeepSeek Harness using durable per-project sessions, with an official headless fallback. Keep Codex responsible for scope, risky judgment, review, integration, and final verification. Do not use for trivial edits, secrets, deployments, destructive operations, or work that cannot be independently checked.
---

# Delegate to DeepSeek Harness

Use DeepSeek Harness as an implementation worker. Keep Codex as orchestrator,
reviewer, and final authority.

## Choose what to delegate

Delegate a complete logical unit when it is context-heavy, mechanical,
repetitive, or independently verifiable. Keep architecture, ambiguous product
judgment, security-sensitive decisions, tiny edits, and final verification in
Codex.

Never send secrets or privileged credentials in a worker brief. Do not delegate
publishing, deployment, destructive external actions, or work that cannot be
checked independently.

## Check the dedicated credential

Before the first delegation in a task, run `scripts/preflight.sh`. If it reports
`credentials-required`, pause delegation and tell the user to run
`scripts/configure_api_key.sh` in a private terminal. Never ask the user to
paste an API key into ChatGPT, a worker brief, or a command argument. Resume
only after preflight succeeds.

The dedicated key keeps Codex delegation usage separate from the user's normal
Harness activity. Read `references/setup.md` only when configuring, rotating,
or troubleshooting credentials.

## Choose the session

The default worker session is durable per Git project and branch. Reuse it for
related work so DeepSeek retains the project conversation across invocations.

- Use the default branch-scoped session for ordinary work.
- Add `--session-name <lane>` for a long-lived feature or investigation lane.
- Add `--session-scope project` only when context should follow all branches.
- Add `--fresh` for an unrelated task or when prior context is stale.

Read `references/sessions.md` when selecting, resetting, or troubleshooting a
session.

## Write the worker brief

Give DeepSeek a self-contained contract even when it has prior project context:

```text
Objective:
<one concrete outcome>

Scope:
<allowed files/modules and explicit non-goals>

Constraints:
<compatibility, API, style, dependency, or user constraints>

Acceptance criteria:
- <observable condition>
- <observable condition>

Verification contract:
- allowed_paths: <glob list>
- checks: <test/lint/typecheck/build commands>
- invariants: <no_new_dependencies | no_public_api_change | no_untracked_files>
- limits: <max_changed_files | max_diff_lines>
- review_mode: receipt | targeted | full

Rules:
- Work only inside the supplied cwd.
- Inspect before editing and preserve unrelated changes.
- Do not commit, push, publish, deploy, rotate credentials, or perform destructive external actions.
- If blocked, report the blocker instead of guessing.
```

Prior session history is helpful context, not an authority. Repeat current
constraints and acceptance criteria in every delegation.

The wrapper automatically appends a lifecycle override to every worker task.
It requires DeepSeek to close internal TODO/pending state, emit a terminal
completion or blocked artifact, and exit instead of waiting after the final
action. Do not copy or duplicate that override in the worker brief.

## Run the worker

Resolve this skill directory and run:

```bash
scripts/dsh_delegate.sh "<worker brief>" "<absolute project cwd>"
```

Optional session controls follow the cwd:

```bash
scripts/dsh_delegate.sh "<worker brief>" "<absolute cwd>" --session-name feature-auth
scripts/dsh_delegate.sh "<worker brief>" "<absolute cwd>" --fresh
```

The script loads the dedicated credential, then uses the official Python SDK
and a stable session ID. If the SDK is not installed, it may use `dsh --profile
headless`; that fallback is explicitly non-persistent. Both paths receive the
automatic lifecycle override that prevents a completed run from remaining in
TODO state. Read
`references/setup.md` only for installation or connectivity work.

## Wait without polling

The wrapper normally blocks until DeepSeek returns a terminal result. If a run
continues asynchronously or its completion must be checked later, do not use
repeated status commands, short sleeps, or tool-output polling. Create a
scheduled task as a heartbeat in the current thread to check the existing
session and workspace at a reasonable cadence.

The heartbeat must stay quiet while nothing meaningful has changed. It should
notify only when the work completes, fails, is blocked, or needs user action;
run the verification contract when completion is reported; and stop or pause
itself after reaching a terminal state. Do not schedule a heartbeat for an
ordinary synchronous run that finishes in the current turn. If scheduled tasks
are unavailable, report that limitation and use one bounded wait rather than a
polling loop.

## Verify the result

Treat the worker report as a claim. Run the contract verifier first:

```bash
scripts/verify_workspace.sh --cwd "<absolute cwd>" \
  --allowed-paths '<glob>' --checks '<command>'
```

Then review according to `review_mode`:

- `receipt`: a passing contract is sufficient.
- `targeted`: inspect the changed-file summary or named risky hunks.
- `full`: inspect the complete diff for auth, payments, migrations,
  concurrency, security, public APIs, or broad architecture.

If the contract passes, stop. Reopen implementation only for a concrete
contract failure or predefined high-risk trigger. After two failures with the
same cause, take over or report the blocker.
