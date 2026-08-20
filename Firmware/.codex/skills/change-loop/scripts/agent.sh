#!/usr/bin/env bash
# Provider-adapter boundary for one future change-loop role.
#
# The Firmware suite deliberately does not implement a provider launcher yet. Keeping this
# executable as a validating placeholder makes an accidental live
# server-repair start fail before it creates a provider session or writes runtime state.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib.sh"

usage() {
  cat <<'EOF'
Usage:
  agent.sh [--dry-run] ROLE PROMPT_FILE

ROLE is doer, spec_tester, or regression_tester. This command validates the selected logical
role only. It intentionally does not start or resume a provider session. A provider adapter must
be selected and implemented before a live BYO-Firmware-MCP repair can begin.
EOF
}

dry_run=0
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
elif [[ "${1:-}" == "--dry-run" ]]; then
  dry_run=1
  shift
fi

[[ "$#" -eq 2 ]] || {
  usage >&2
  exit 2
}
role="$1"
prompt_file="$2"
case "$role" in
  doer | spec_tester | regression_tester) ;;
  *) cl_die "ROLE must be doer, spec_tester, or regression_tester" ;;
esac
[[ -s "$prompt_file" ]] || cl_die "prompt file is missing or empty: $prompt_file"

if [[ "$dry_run" -eq 1 ]]; then
  printf 'Provider launch pending: role=%s prompt=%s; see Firmware/PROVIDER_ADAPTER.md\n' \
    "$role" "$prompt_file"
  exit 0
fi

cl_die \
  "provider launch is intentionally pending for role=$role; select and implement the Firmware provider adapter before starting a live repair"
