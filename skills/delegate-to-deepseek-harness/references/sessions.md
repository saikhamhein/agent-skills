# Durable sessions

## Identity

`dsh-delegate` computes a stable session ID from:

- schema version;
- canonical Git root, or the supplied directory outside Git;
- Git branch by default;
- optional session lane name.

The absolute project path is deliberately part of the identity. Separate
checkouts and worktrees receive separate sessions and cannot accidentally share
mutation context.

Inspect the selected identity without spending API tokens:

```bash
dsh-delegate session-id --cwd /absolute/path/to/project --json
```

## Reuse and reset

Reuse the default session for sequential work on the same branch. Choose a
named lane for a feature that spans branches or needs independent context:

```bash
dsh-delegate run "..." --cwd /path/to/project --session-name feature-auth
```

Use `--fresh` when the task is unrelated, the accumulated assumptions are
stale, or a clean comparison is valuable. Fresh sessions do not delete the
durable log of the default session.

## Context discipline

Persistence reduces repeated repository orientation, but old conversation is
still input context. Do not use one endless project-wide conversation for every
task. Prefer branch scope, use named lanes for long features, and start fresh
after major redesigns or when old assumptions repeatedly interfere.

Always repeat the current scope and acceptance criteria. Files remain the source
of truth; prior model statements do not override the workspace.

## Process lifetime

The CLI auto-starts one private loopback daemon and keeps an official SDK
runtime open for each active project configuration. Separate orchestrator calls reuse
that runtime and logical session, preserving conversation and session-owned
shell state.

Inspect or stop it explicitly:

```bash
dsh-delegate daemon status
dsh-delegate daemon stop
```

The current SDK cannot attach a new process to an already persisted SDK
session. After a daemon restart, the CLI creates a new runtime generation for
the same logical project lane. Project files remain intact, but in-memory
conversation and shell state begin fresh. Restorable cross-process sessions can
be added when Harness exposes SDK resume semantics.
