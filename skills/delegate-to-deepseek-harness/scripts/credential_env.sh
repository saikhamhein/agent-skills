#!/usr/bin/env bash

delegation_credential_file() {
  printf '%s/dsh-delegation/credentials.env\n' "${XDG_CONFIG_HOME:-$HOME/.config}"
}

load_delegation_api_key() {
  local credential_file line api_key
  credential_file=$(delegation_credential_file)
  [[ -f "$credential_file" ]] || return 1
  IFS= read -r line < "$credential_file" || true
  [[ "$line" == DEEPSEEK_API_KEY=* ]] || return 2
  api_key=${line#DEEPSEEK_API_KEY=}
  [[ -n "$api_key" && "$api_key" != *[!A-Za-z0-9._-]* ]] || return 2
  export DEEPSEEK_API_KEY="$api_key"
  export DSH_DELEGATE_CREDENTIAL_SOURCE=dedicated-file
}
