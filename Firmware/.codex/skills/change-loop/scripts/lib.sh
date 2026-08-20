#!/usr/bin/env bash
# Shared configuration and helpers for change-loop and plan-changes.
set -euo pipefail

# Exported for callers that source this library (notably run_loop.sh).
# shellcheck disable=SC2034
CL_SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Provider/model/effort selection belongs solely to Firmware/PROVIDER_ADAPTER.md. This helper
# carries only local validation and neutral-gate settings while no provider adapter exists.
# Keep repair-control state out of the production server tree. For this suite the
# serialized active runtime defaults to the parent workspace; callers should use
# an owning experiment's .agent-workspace/server-repairs/<repair-id> path when one
# is already known.
CL_RUNTIME_DIR="${CL_RUNTIME_DIR:-../.agent-workspace/server-repair-runtime/current}"
MAX_ITERS="${MAX_ITERS:-8}"
CL_TEST_TAIL_LINES="${CL_TEST_TAIL_LINES:-120}"
CL_PYTHON_BIN="${CL_PYTHON_BIN:-python3}"
CL_BASH_BIN="${CL_BASH_BIN:-bash}"

cl_die() {
  printf 'change-loop: ERROR: %s\n' "$*" >&2
  exit 2
}

cl_note() {
  printf 'change-loop: %s\n' "$*" >&2
}

cl_require_command() {
  command -v "$1" >/dev/null 2>&1 || cl_die "required command '$1' was not found on PATH"
}

cl_require_positive_integer() {
  local name="$1"
  local value="$2"
  [[ "$value" =~ ^[1-9][0-9]*$ ]] || cl_die "$name must be a positive integer; got '$value'"
}

cl_init_repo() {
  cl_require_command git
  local requested_root="${CL_REPO_ROOT:-.}"
  local discovered
  discovered="$(git -C "$requested_root" rev-parse --show-toplevel 2>/dev/null)" ||
    cl_die "CL_REPO_ROOT must name a directory inside the target git repository; got '$requested_root'"
  CL_REPO_ROOT="$(cd "$discovered" && pwd)"

  if [[ "$CL_RUNTIME_DIR" = /* || "$CL_RUNTIME_DIR" =~ ^[A-Za-z]:[\\/] ]]; then
    CL_RUN_DIR="$CL_RUNTIME_DIR"
  else
    CL_RUN_DIR="$CL_REPO_ROOT/$CL_RUNTIME_DIR"
  fi
  mkdir -p "$CL_RUN_DIR"
  CL_RUN_DIR="$(cd "$CL_RUN_DIR" && pwd)"
  local runtime_scope_root="$CL_REPO_ROOT"
  if [[ "$(basename "$CL_REPO_ROOT")" == "BYO-Firmware-MCP" ]]; then
    runtime_scope_root="$(cd "$CL_REPO_ROOT/.." && pwd)"
  fi
  case "$CL_RUN_DIR/" in
    "$runtime_scope_root/"*) ;;
    *) cl_die "CL_RUNTIME_DIR must resolve inside the Firmware suite: $CL_RUN_DIR" ;;
  esac
  CL_STATE_DIR="$CL_RUN_DIR/state"
  CL_LOG_DIR="$CL_RUN_DIR/logs"
  CL_PLAN_PATH="$CL_RUN_DIR/plan.md"
  mkdir -p "$CL_STATE_DIR" "$CL_LOG_DIR"
  export CL_REPO_ROOT CL_RUN_DIR CL_STATE_DIR CL_LOG_DIR CL_PLAN_PATH
}

cl_require_server_repository() {
  # Change-loop is intentionally not a general-purpose implementation harness.
  # It may repair only the production BYO-Firmware-MCP repository, identified
  # by its repository root, never an isolated fresh-experiment workspace or a
  # firmware application repository. Do not infer server identity from an
  # internal source-package directory.
  [[ "$(basename "$CL_REPO_ROOT")" == "BYO-Firmware-MCP" ]] ||
    cl_die "change-loop is reserved for the BYO-Firmware-MCP production server repository; got '$CL_REPO_ROOT'"
}

cl_validate_plan_file() {
  local plan="${1:-$CL_PLAN_PATH}"
  [[ -s "$plan" ]] || cl_die "main-model plan is missing or empty: $plan"
  local heading
  for heading in \
    '## Source change list' \
    '## Repository context and assumptions' \
    '## Plan items' \
    '## Out of scope / must not change' \
    '## Acceptance gate'; do
    grep -Fq "$heading" "$plan" ||
      cl_die "main-model plan is missing required heading '$heading': $plan"
  done
  grep -Eq '^### CL-[0-9]{3} .+' "$plan" ||
    cl_die "main-model plan has no concrete CL-NNN item: $plan"
  if grep -Eq '<[^>]+>|<!-- Repeat CL-NNN' "$plan"; then
    cl_die "main-model plan still contains template placeholders: $plan"
  fi
}

cl_file_oid() {
  local path="$1"
  if [[ -f "$path" ]]; then
    git hash-object -- "$path"
  else
    printf '%s\n' MISSING
  fi
}

cl_safe_repo_relative_path() {
  local path="$1"
  [[ -n "$path" ]] || return 1
  [[ "$path" != /* && ! "$path" =~ ^[A-Za-z]:[\\/] ]] || return 1
  [[ "$path" != ".." && "$path" != ../* && "$path" != */../* && "$path" != */.. ]] || return 1
  [[ -f "$CL_REPO_ROOT/$path" ]] || return 1
}

cl_print_config() {
  cat <<EOF
PROVIDER_ADAPTER_STATUS=pending
CL_RUNTIME_DIR=$CL_RUNTIME_DIR
MAX_ITERS=$MAX_ITERS
CL_TEST_TAIL_LINES=$CL_TEST_TAIL_LINES
EOF
}
