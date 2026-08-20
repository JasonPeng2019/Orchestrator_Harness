#!/usr/bin/env bash
# Change-loop validation and future-provider boundary. A live provider adapter is intentionally
# not implemented in this Firmware package yet.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib.sh"

usage() {
  cat <<'EOF'
Usage:
  run_loop.sh --self-check
  run_loop.sh --dry-run

`--self-check` validates the package layout, shell syntax, prompt construction, and neutral test
gate. `--dry-run` prints the selected logical role settings. A live change loop cannot start until
the Firmware provider adapter is deliberately implemented; this command creates no provider
session while that adapter is pending.
EOF
}

compose_prompt() {
  local role="$1"
  local iteration="$2"
  local target="$CL_STATE_DIR/$role.prompt.md"
  local policy_helper="$CL_SKILL_DIR/../../../scripts/orchestration/prompt_policy.py"
  local policy_target="$target.policy-bound.tmp"
  cat "$CL_SKILL_DIR/templates/${role}_prompt.md" >"$target"
  sed -i "s#\\.change-loop/state#$CL_STATE_DIR#g" "$target"
  sed -i "s#\\.change-loop/plan\\.md#$CL_PLAN_PATH#g" "$target"
  sed -i "s#\\.change-loop/plan-review\\.md#$CL_RUN_DIR/plan-review.md#g" "$target"
  sed -i "s#\\.change-loop/plan-amendments\\.md#$CL_RUN_DIR/plan-amendments.md#g" "$target"
  cat >>"$target" <<EOF

## Current turn

- Iteration: $iteration
- Repository root: $CL_REPO_ROOT
- Plan: $CL_PLAN_PATH
- One-time plan review: $CL_RUN_DIR/plan-review.md
- Reviewed plan amendments, if any: $CL_RUN_DIR/plan-amendments.md
- Design-charter checkpoint log: $CL_RUN_DIR/DESIGN_CHARTER_CHECKS.md
- Latest neutral report: $CL_STATE_DIR/test_report.md
- Runtime state: $CL_STATE_DIR

Read the plan from disk before acting. If the neutral report exists, read it too.
At every design-charter checkpoint required by your role prompt, reread the complete charter and
append a dated entry to the named checkpoint log before continuing. Each entry must name the
contemplated diff/test feature, the charter properties applied, any assumption or tie-breaker,
rejected board/OS/toolchain-specific alternatives, and scope exclusions.
EOF
  [[ -s "$policy_helper" ]] ||
    cl_die "autonomous prompt-policy helper is missing: $policy_helper"
  "$CL_PYTHON_BIN" "$policy_helper" "$target" "$policy_target"
  mv "$policy_target" "$target"
  printf '%s\n' \
    "be10f776c27fa8ffb46b8d395ac791ee0d73c235cf8a0d079fc960612a00f126" \
    >"$CL_STATE_DIR/$role.autonomy-policy.sha256"
  printf '%s\n' "$target"
}

self_check() {
  local required=(
    "$CL_SKILL_DIR/SKILL.md"
    "$CL_SKILL_DIR/scripts/lib.sh"
    "$CL_SKILL_DIR/scripts/agent.sh"
    "$CL_SKILL_DIR/scripts/run_tests.sh"
    "$CL_SKILL_DIR/scripts/run_loop.sh"
    "$CL_SKILL_DIR/templates/doer_prompt.md"
    "$CL_SKILL_DIR/templates/spec_tester_prompt.md"
    "$CL_SKILL_DIR/templates/regression_tester_prompt.md"
    "$CL_SKILL_DIR/../plan-changes/SKILL.md"
    "$CL_SKILL_DIR/../plan-changes/scripts/plan.sh"
    "$CL_SKILL_DIR/../plan-changes/templates/plan_prompt.md"
    "$CL_SKILL_DIR/../plan-changes/templates/plan.md"
    "$CL_SKILL_DIR/../../../scripts/orchestration/prompt_policy.py"
  )
  local file
  for file in "${required[@]}"; do
    [[ -s "$file" ]] || cl_die "self-check missing required file: $file"
  done
  for file in "$CL_SKILL_DIR"/scripts/*.sh "$CL_SKILL_DIR"/../plan-changes/scripts/*.sh; do
    "$CL_BASH_BIN" -n "$file"
  done

  local temporary
  temporary="$(mktemp -d)"
  trap 'rm -rf "$temporary"' RETURN
  git -C "$temporary" init -q
  mkdir -p "$temporary/.change-loop/state"
  printf "printf 'spec-run\\n' >> .change-loop/state/spec-runs\n" \
    >"$temporary/.change-loop/state/spec_test_cmd"
  printf "printf 'regression-run\\n' >> .change-loop/state/regression-runs\n" \
    >"$temporary/.change-loop/state/regression_test_cmd"
  printf 'RUN\nInitial self-check execution.\n' \
    >"$temporary/.change-loop/state/spec_test_mode"
  printf 'RUN\nInitial self-check execution.\n' \
    >"$temporary/.change-loop/state/regression_test_mode"
  printf 'self-check\n' >"$temporary/.change-loop/state/spec_tester.manifest.snapshot"
  printf 'self-check\n' \
    >"$temporary/.change-loop/state/regression_tester.manifest.snapshot"
  (
    cd "$temporary"
    CL_RUNTIME_DIR=.change-loop "$CL_SKILL_DIR/scripts/run_tests.sh" >/dev/null
    printf 'REUSE\nNo covered source or contract changed.\n' \
      >.change-loop/state/spec_test_mode
    printf 'REUSE\nNo covered source or contract changed.\n' \
      >.change-loop/state/regression_test_mode
    CL_RUNTIME_DIR=.change-loop "$CL_SKILL_DIR/scripts/run_tests.sh" >/dev/null
  )
  grep -q 'Spec suite: PASS (REUSED)' "$temporary/.change-loop/state/test_report.md"
  grep -q 'Regression suite: PASS (REUSED)' \
    "$temporary/.change-loop/state/test_report.md"
  [[ "$(wc -l <"$temporary/.change-loop/state/spec-runs")" -eq 1 ]]
  [[ "$(wc -l <"$temporary/.change-loop/state/regression-runs")" -eq 1 ]]

  CL_REPO_ROOT="$temporary"
  CL_RUN_DIR="$temporary/.change-loop/custom-runtime"
  CL_STATE_DIR="$CL_RUN_DIR/state"
  CL_LOG_DIR="$CL_RUN_DIR/logs"
  CL_PLAN_PATH="$CL_RUN_DIR/plan.md"
  mkdir -p "$CL_STATE_DIR" "$CL_LOG_DIR"
  local composed_prompt
  composed_prompt="$(compose_prompt doer 1)"
  grep -Fq "$CL_PLAN_PATH" "$composed_prompt"
  grep -Fq "$CL_RUN_DIR/plan-review.md" "$composed_prompt"
  grep -Fq "$CL_RUN_DIR/plan-amendments.md" "$composed_prompt"
  grep -Fq "$CL_STATE_DIR/test_report.md" "$composed_prompt"
  ! grep -Fq '.change-loop/plan.md' "$composed_prompt"
  "$CL_SKILL_DIR/scripts/agent.sh" --dry-run doer "$composed_prompt" >/dev/null
  ! grep -Eiq '\bcodex[[:space:]]+exec\b|\bqwen[[:space:]]+code\b|CL_CODEX_(BIN|FLAGS)' \
    "$CL_SKILL_DIR/scripts/agent.sh" "$CL_SKILL_DIR/scripts/lib.sh"
  printf 'change-loop self-check: PASS (syntax, layout, prompt, neutral gate, and pending provider boundary)\n'
}

case "${1:-}" in
  --help | -h)
    usage
    exit 0
    ;;
  --self-check)
    cl_require_command "$CL_BASH_BIN"
    cl_require_command "$CL_PYTHON_BIN"
    cl_require_command git
    self_check
    exit 0
    ;;
  --dry-run)
    printf 'Provider adapter pending; no server-repair role will be launched.\n'
    cl_print_config
    exit 0
    ;;
  "")
    cl_die \
      "provider launch is intentionally pending; select and implement the Firmware provider adapter before starting a live server-repair loop"
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
