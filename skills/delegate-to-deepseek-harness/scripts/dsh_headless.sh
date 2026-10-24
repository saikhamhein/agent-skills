#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "usage: $0 <task> [cwd]" >&2
  exit 64
fi

task=$1
cwd=${2:-$PWD}

lifecycle_completion_marker='Task fully completed and verified. Closing session.'
lifecycle_blocked_marker='Task blocked and reported. Closing session.'
if [[ "$task" != *"Lifecycle Override:"* ]] || {
  [[ "$task" != *"$lifecycle_completion_marker"* ]] &&
    [[ "$task" != *"$lifecycle_blocked_marker"* ]]
}; then
  lifecycle_override=$(printf '%s\n' \
    'Lifecycle Override:' \
    '1. Execute the task completely and verify all required outputs.' \
    '2. After the final required action, explicitly trigger the state-update cycle and transition every internal TODO or pending action to a terminal state.' \
    "3. If successful, output a final completion artifact and state exactly: \"$lifecycle_completion_marker\"" \
    "4. If a real blocker prevents completion, report it truthfully, clear any pending/TODO state, and state exactly: \"$lifecycle_blocked_marker\"" \
    '5. Do not wait for further input after reaching either terminal state. Immediately exit the execution loop so the headless runner cannot hang.')
  task="${task%$'\n'}"$'\n\n'"$lifecycle_override"
fi

if ! command -v dsh >/dev/null 2>&1; then
  echo "error: dsh is not installed or not on PATH" >&2
  exit 127
fi
if [[ ! -d "$cwd" ]]; then
  echo "error: cwd does not exist: $cwd" >&2
  exit 66
fi
if [[ -z "${task//[[:space:]]/}" ]]; then
  echo "error: task must not be empty" >&2
  exit 64
fi

cd "$cwd"
log=$(mktemp "${TMPDIR:-/tmp}/dsh-headless-XXXXXX.log")
echo "worker log: $log" >&2
dsh --profile headless "$task" 2>&1 | tee "$log"
