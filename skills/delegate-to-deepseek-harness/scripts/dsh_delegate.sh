#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd "$(dirname "$0")" && pwd -P)
# shellcheck source=credential_env.sh
source "$script_dir/credential_env.sh"

credential_rc=0
load_delegation_api_key || credential_rc=$?
case $credential_rc in
  0) ;;
  1) echo "note: no dedicated key; using Harness' own credential" >&2 ;;
  *)
    echo "error: dedicated credential file is malformed" >&2
    echo "fix it securely in a terminal: $script_dir/configure_api_key.sh" >&2
    exit 78
    ;;
esac

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <task> [cwd] [dsh-delegate options...]" >&2
  exit 64
fi

task=$1
shift
cwd=${1:-$PWD}
if [[ $# -gt 0 ]]; then shift; fi

runtime_root=${DSH_DELEGATE_RUNTIME_DIR:-"${XDG_DATA_HOME:-$HOME/.local/share}/dsh-delegation"}
runner="$runtime_root/current/bin/dsh-delegate"

if [[ -x "$runner" ]]; then
  exec "$runner" run "$task" --cwd "$cwd" "$@"
fi

if command -v dsh-delegate >/dev/null 2>&1; then
  exec dsh-delegate run "$task" --cwd "$cwd" "$@"
fi

echo "note: persistent SDK runtime not installed; using one-shot dsh headless" >&2
exec "$script_dir/dsh_headless.sh" "$task" "$cwd"
