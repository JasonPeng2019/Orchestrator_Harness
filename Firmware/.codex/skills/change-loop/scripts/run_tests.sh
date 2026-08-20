#!/usr/bin/env bash
# Neutral gate: execute tester-authored commands and trust only their exit codes.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib.sh"

usage() {
  cat <<'EOF'
Usage:
  run_tests.sh [--dry-run]

Reads:
  .change-loop/state/spec_test_cmd
  .change-loop/state/spec_test_mode
  .change-loop/state/regression_test_cmd
  .change-loop/state/regression_test_mode

Each mode file starts with RUN or REUSE and a nonempty second-line rationale.
REUSE is accepted only for a previously passing command whose command and test
manifest fingerprints are unchanged. Writes suite logs, pass caches, and
.change-loop/state/test_report.md. Exits 0 when both suites have current RUN
passes or validated REUSE passes; exits 1 for a test failure and 2 for
missing/invalid gate configuration.
EOF
}

dry_run=0
case "${1:-}" in
  --help | -h)
    usage
    exit 0
    ;;
  --dry-run)
    dry_run=1
    ;;
  "")
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

cl_init_repo
cl_require_positive_integer CL_TEST_TAIL_LINES "$CL_TEST_TAIL_LINES"

spec_cmd_file="$CL_STATE_DIR/spec_test_cmd"
regression_cmd_file="$CL_STATE_DIR/regression_test_cmd"
spec_mode_file="$CL_STATE_DIR/spec_test_mode"
regression_mode_file="$CL_STATE_DIR/regression_test_mode"
[[ -s "$spec_cmd_file" ]] || cl_die "missing spec test command: $spec_cmd_file"
[[ -s "$regression_cmd_file" ]] || cl_die "missing regression test command: $regression_cmd_file"
[[ -s "$spec_mode_file" ]] || cl_die "missing spec test mode: $spec_mode_file"
[[ -s "$regression_mode_file" ]] ||
  cl_die "missing regression test mode: $regression_mode_file"
spec_cmd="$(cat "$spec_cmd_file")"
regression_cmd="$(cat "$regression_cmd_file")"
spec_mode="$(head -n 1 "$spec_mode_file" | tr -d '\r' | tr '[:lower:]' '[:upper:]')"
regression_mode="$(
  head -n 1 "$regression_mode_file" | tr -d '\r' | tr '[:lower:]' '[:upper:]'
)"
spec_reason="$(tail -n +2 "$spec_mode_file" | sed '/^[[:space:]]*$/d' | head -n 1)"
regression_reason="$(
  tail -n +2 "$regression_mode_file" | sed '/^[[:space:]]*$/d' | head -n 1
)"
[[ "$spec_mode" == RUN || "$spec_mode" == REUSE ]] ||
  cl_die "invalid spec test mode '$spec_mode'; expected RUN or REUSE"
[[ "$regression_mode" == RUN || "$regression_mode" == REUSE ]] ||
  cl_die "invalid regression test mode '$regression_mode'; expected RUN or REUSE"
[[ -n "$spec_reason" ]] || cl_die "spec test mode requires a second-line rationale"
[[ -n "$regression_reason" ]] ||
  cl_die "regression test mode requires a second-line rationale"

if [[ "$dry_run" -eq 1 ]]; then
  printf 'Spec mode: %s\nSpec command: %s\n' "$spec_mode" "$spec_cmd"
  printf 'Regression mode: %s\nRegression command: %s\n' \
    "$regression_mode" "$regression_cmd"
  exit 0
fi

cl_require_command "$CL_BASH_BIN"
cl_require_command sha256sum
spec_log="$CL_STATE_DIR/spec_test_output.log"
regression_log="$CL_STATE_DIR/regression_test_output.log"

run_suite() {
  local role="$1"
  local command="$2"
  local mode="$3"
  local log="$4"
  local snapshot="$CL_STATE_DIR/$role.manifest.snapshot"
  local cache="$CL_STATE_DIR/$role.pass-cache"
  [[ -s "$snapshot" ]] || cl_die "missing $role manifest snapshot: $snapshot"

  local command_sha manifest_sha expected_command_sha expected_manifest_sha
  command_sha="$(printf '%s' "$command" | sha256sum | awk '{print tolower($1)}')"
  manifest_sha="$(sha256sum "$snapshot" | awk '{print tolower($1)}')"

  if [[ "$mode" == REUSE ]]; then
    [[ -s "$cache" ]] ||
      cl_die "$role requested REUSE without prior passing evidence: $cache"
    expected_command_sha="$(sed -n '1p' "$cache" | tr -d '\r')"
    expected_manifest_sha="$(sed -n '2p' "$cache" | tr -d '\r')"
    [[ "$command_sha" == "$expected_command_sha" ]] ||
      cl_die "$role requested REUSE after its test command changed"
    [[ "$manifest_sha" == "$expected_manifest_sha" ]] ||
      cl_die "$role requested REUSE after its test manifest/files changed"
    printf 'Reused prior PASS after tester-confirmed unaffected-diff review.\n' >"$log"
    return 0
  fi

  rm -f "$cache"
  local status
  if (cd "$CL_REPO_ROOT" && "$CL_BASH_BIN" -lc "$command") >"$log" 2>&1; then
    status=0
  else
    status=$?
  fi
  if [[ "$status" -eq 0 ]]; then
    printf '%s\n%s\n' "$command_sha" "$manifest_sha" >"$cache.tmp"
    mv "$cache.tmp" "$cache"
  fi
  return "$status"
}

if run_suite spec_tester "$spec_cmd" "$spec_mode" "$spec_log"; then
  spec_status=0
else
  spec_status=$?
fi
if run_suite regression_tester \
  "$regression_cmd" "$regression_mode" "$regression_log"; then
  regression_status=0
else
  regression_status=$?
fi

spec_result=FAIL
regression_result=FAIL
[[ "$spec_status" -eq 0 ]] && spec_result=PASS
[[ "$regression_status" -eq 0 ]] && regression_result=PASS
[[ "$spec_status" -eq 0 && "$spec_mode" == REUSE ]] && spec_result='PASS (REUSED)'
[[ "$regression_status" -eq 0 && "$regression_mode" == REUSE ]] &&
  regression_result='PASS (REUSED)'

report="$CL_STATE_DIR/test_report.md"
{
  printf '# Neutral test gate\n\n'
  printf '## Spec suite: %s\n\n' "$spec_result"
  printf -- '- Mode: `%s`\n- Rationale: %s\n' "$spec_mode" "$spec_reason"
  # The single quotes preserve Markdown backticks; values are printf arguments.
  # shellcheck disable=SC2016
  printf -- '- Command: `%s`\n- Exit code: `%s`\n\n' "$spec_cmd" "$spec_status"
  printf '```text\n'
  tail -n "$CL_TEST_TAIL_LINES" "$spec_log" || true
  printf '\n```\n\n'
  printf '## Regression suite: %s\n\n' "$regression_result"
  printf -- '- Mode: `%s`\n- Rationale: %s\n' \
    "$regression_mode" "$regression_reason"
  # shellcheck disable=SC2016
  printf -- '- Command: `%s`\n- Exit code: `%s`\n\n' "$regression_cmd" "$regression_status"
  printf '```text\n'
  tail -n "$CL_TEST_TAIL_LINES" "$regression_log" || true
  printf '\n```\n'
} >"$report"

cat "$report"
if [[ "$spec_status" -eq 0 && "$regression_status" -eq 0 ]]; then
  exit 0
fi
exit 1
