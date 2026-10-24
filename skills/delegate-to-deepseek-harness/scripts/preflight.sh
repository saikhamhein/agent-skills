#!/usr/bin/env bash
set -u

script_dir=$(cd "$(dirname "$0")" && pwd -P)
# shellcheck source=credential_env.sh
source "$script_dir/credential_env.sh"

if ! load_delegation_api_key; then
  setup_command="$script_dir/configure_api_key.sh"
  printf '{"status":"credentials-required","dedicated_api_key":false,"setup_command":"%s"}\n' \
    "$setup_command"
  exit 78
fi

runtime_root=${DSH_DELEGATE_RUNTIME_DIR:-"${XDG_DATA_HOME:-$HOME/.local/share}/dsh-delegation"}
runner="$runtime_root/current/bin/dsh-delegate"

if [[ -x "$runner" ]]; then
  "$runner" preflight
  exit $?
fi
if command -v dsh-delegate >/dev/null 2>&1; then
  dsh-delegate preflight
  exit $?
fi
if command -v dsh >/dev/null 2>&1; then
  printf '{"status":"fallback-only","sdk_available":false,"dsh_available":true}\n'
  exit 0
fi
printf '{"status":"fail","sdk_available":false,"dsh_available":false}\n'
exit 1
