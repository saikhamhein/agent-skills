#!/usr/bin/env bash
# Deterministic verification receipt for delegated coding work.
set -u

usage() {
  echo "usage: $0 [--cwd DIR] [--baseline DIR] --allowed-paths GLOB[,GLOB...] [--checks CMD] [--invariants LIST] [--max-changed-files N] [--max-diff-lines N]" >&2
  exit 1
}

cwd=$PWD
baseline=
allowed=()
checks=()
invariants=
max_files=
max_lines=

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cwd) [[ $# -ge 2 ]] || usage; cwd=$2; shift 2 ;;
    --baseline) [[ $# -ge 2 ]] || usage; baseline=$2; shift 2 ;;
    --allowed-paths) [[ $# -ge 2 ]] || usage; IFS=',' read -ra parts <<< "$2"; allowed+=("${parts[@]}"); shift 2 ;;
    --checks) [[ $# -ge 2 ]] || usage; checks+=("$2"); shift 2 ;;
    --invariants) [[ $# -ge 2 ]] || usage; invariants=$2; shift 2 ;;
    --max-changed-files) [[ $# -ge 2 ]] || usage; max_files=$2; shift 2 ;;
    --max-diff-lines) [[ $# -ge 2 ]] || usage; max_lines=$2; shift 2 ;;
    *) echo "error: unknown option: $1" >&2; usage ;;
  esac
done

[[ -d "$cwd" ]] || { echo "error: cwd does not exist: $cwd" >&2; exit 1; }
[[ -z "$baseline" || -d "$baseline" ]] || { echo "error: baseline does not exist: $baseline" >&2; exit 1; }
cd "$cwd"

use_git=0
git rev-parse --git-dir >/dev/null 2>&1 && use_git=1
changed=()
if [[ $use_git -eq 1 ]]; then
  while IFS= read -r -d '' file; do changed+=("$file"); done < <(
    git status --porcelain=v1 -z 2>/dev/null | while IFS= read -r -d '' entry; do
      printf '%s\0' "${entry:3}"
    done
  )
else
  [[ -n "$baseline" ]] || { echo '{"error":"not a git repo and no --baseline given"}' >&2; exit 1; }
  while IFS= read -r file; do changed+=("$file"); done < <(
    diff -rq "$baseline" . 2>/dev/null |
      sed -n 's/^Files .* and \.\(.*\) differ$/\1/p; s/^Only in \.\(.*\): \(.*\)$/\1\/\2/p'
  )
fi

scope_ok=true
unexpected=()
for file in "${changed[@]}"; do
  matched=0
  for pattern in "${allowed[@]}"; do
    if [[ "$file" == $pattern ]]; then matched=1; break; fi
  done
  if [[ $matched -eq 0 ]]; then unexpected+=("$file"); scope_ok=false; fi
done

if [[ $use_git -eq 1 ]]; then
  diff_lines=$(git diff --numstat 2>/dev/null | awk '{sum += $1 + $2} END {print sum + 0}')
else
  diff_lines=$(diff -r -U0 "$baseline" . 2>/dev/null | grep -cE '^[+-][^+-]' || true)
fi

new_deps=false
public_api_change=false
untracked=false
IFS=',' read -ra inv_list <<< "$invariants"
for invariant in "${inv_list[@]}"; do
  case "$invariant" in
    no-new-deps)
      if [[ $use_git -eq 1 ]] && git diff -- package.json pyproject.toml 2>/dev/null | grep -qE '^\+[^+].*(dependencies|requires|project.dependencies)'; then
        new_deps=true
      fi
      ;;
    no-public-api-change)
      if [[ $use_git -eq 1 ]] && git diff 2>/dev/null | grep -qE '^[+-].*(export |def [^_]|class [^_])'; then
        public_api_change=true
      fi
      ;;
    no-untracked)
      if [[ $use_git -eq 1 ]] && git status --porcelain 2>/dev/null | grep -q '^??'; then untracked=true; fi
      ;;
    "") ;;
    *) echo "error: unknown invariant: $invariant" >&2; exit 1 ;;
  esac
done

tests_json="[]"
test_failed=false
if [[ ${#checks[@]} -gt 0 ]]; then
  parts=()
  for command in "${checks[@]}"; do
    output=$(bash -c "$command" 2>&1)
    status=$?
    [[ $status -eq 0 ]] || test_failed=true
    command_json=$(printf '%s' "$command" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
    tail_json=$(printf '%s' "$output" | tail -n 5 | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
    parts+=("{\"command\":$command_json,\"exit_code\":$status,\"tail\":$tail_json}")
  done
  tests_json="[$(IFS=,; echo "${parts[*]}")]"
fi

limits_ok=true
risk_flags=()
if [[ -n "$max_files" && ${#changed[@]} -gt $max_files ]]; then
  limits_ok=false
  risk_flags+=("changed_files_${#changed[@]}_over_max_${max_files}")
fi
if [[ -n "$max_lines" && $diff_lines -gt $max_lines ]]; then
  limits_ok=false
  risk_flags+=("diff_lines_${diff_lines}_over_max_${max_lines}")
fi
$new_deps && risk_flags+=("new_dependencies_detected")
$public_api_change && risk_flags+=("public_api_changed")
$untracked && risk_flags+=("untracked_files_present")

overall_pass=true
$scope_ok || overall_pass=false
$limits_ok || overall_pass=false
$new_deps && overall_pass=false
$public_api_change && overall_pass=false
$untracked && overall_pass=false
$test_failed && overall_pass=false

VW_STATUS=$overall_pass VW_SCOPE=$scope_ok VW_DIFFLINES=$diff_lines \
VW_CHANGED_COUNT=${#changed[@]} VW_TESTS=$tests_json \
VW_CHANGED_LIST=$(printf '%s\n' "${changed[@]}") \
VW_UNEXPECTED=$(printf '%s\n' "${unexpected[@]}") \
VW_FLAGS=$(printf '%s\n' "${risk_flags[@]}") python3 <<'PY'
import json
import os

def lines(name):
    return [line for line in os.environ.get(name, "").splitlines() if line]

print(json.dumps({
    "status": "pass" if os.environ["VW_STATUS"] == "true" else "fail",
    "changed_files": int(os.environ["VW_CHANGED_COUNT"]),
    "changed_file_list": lines("VW_CHANGED_LIST"),
    "diff_lines": int(os.environ["VW_DIFFLINES"]),
    "scope_ok": os.environ["VW_SCOPE"] == "true",
    "unexpected_files": lines("VW_UNEXPECTED"),
    "tests": json.loads(os.environ["VW_TESTS"]),
    "risk_flags": lines("VW_FLAGS"),
}, ensure_ascii=False))
PY
