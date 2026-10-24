#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd "$(dirname "$0")" && pwd -P)
# shellcheck source=credential_env.sh
source "$script_dir/credential_env.sh"

usage() {
  echo "usage: $0 [--stdin|--check]" >&2
}

mode=prompt
if [[ $# -gt 1 ]]; then
  usage
  exit 64
elif [[ $# -eq 1 ]]; then
  case "$1" in
    --stdin) mode=stdin ;;
    --check) mode=check ;;
    *) usage; exit 64 ;;
  esac
fi

credential_file=$(delegation_credential_file)
if [[ "$mode" == check ]]; then
  if load_delegation_api_key; then
    echo "configured: $credential_file"
    exit 0
  fi
  echo "not configured: $credential_file"
  exit 1
fi

if [[ "$mode" == prompt ]]; then
  if [[ ! -t 0 ]]; then
    echo "error: run this command in an interactive terminal, or pipe a secret manager into --stdin" >&2
    exit 1
  fi
  read -r -s -p "Dedicated DeepSeek API key: " api_key
  printf '\n'
else
  IFS= read -r api_key
fi

if [[ -z "$api_key" || "$api_key" == *[!A-Za-z0-9._-]* ]]; then
  unset api_key
  echo "error: API key is empty or contains unsupported characters" >&2
  exit 65
fi

credential_dir=$(dirname "$credential_file")
umask 077
mkdir -p "$credential_dir"
chmod 700 "$credential_dir"
credential_stage=$(mktemp "$credential_dir/.credentials.env.XXXXXX")
cleanup() {
  rm -f -- "$credential_stage"
}
trap cleanup EXIT
printf 'DEEPSEEK_API_KEY=%s\n' "$api_key" > "$credential_stage"
unset api_key
chmod 600 "$credential_stage"
mv -f "$credential_stage" "$credential_file"
trap - EXIT

if [[ ${DSH_DELEGATE_SKIP_SERVICE_RESTART:-0} != 1 ]]; then
  if command -v systemctl >/dev/null 2>&1 \
    && systemctl --user cat codex-dsh-delegation.service >/dev/null 2>&1; then
    systemctl --user restart codex-dsh-delegation.service
  else
    runtime_root=${DSH_DELEGATE_RUNTIME_DIR:-"${XDG_DATA_HOME:-$HOME/.local/share}/dsh-delegation"}
    runner="$runtime_root/current/bin/dsh-delegate"
    if [[ -x "$runner" ]]; then
      "$runner" daemon stop >/dev/null 2>&1 || true
    fi
  fi
fi

echo "Dedicated DeepSeek API key configured for Codex delegation."
echo "Stored securely at: $credential_file"
