#!/usr/bin/env bash
# Deterministic scaffold/validator only. The current main model authors the plan directly.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAN_SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$(cd "$PLAN_SKILL_DIR/.." && pwd)"
CHANGE_LOOP_DIR="$SKILLS_DIR/change-loop"
# shellcheck source=../../change-loop/scripts/lib.sh
# shellcheck disable=SC1091
source "$CHANGE_LOOP_DIR/scripts/lib.sh"

usage() {
  cat <<'EOF'
Usage:
  plan.sh --prepare CHANGE_LIST_FILE
  plan.sh --prepare --file CHANGE_LIST_FILE
  plan.sh --prepare --text "free-form requested changes"
  plan.sh --validate
  plan.sh --dry-run CHANGE_LIST_FILE
  plan.sh --self-check

Preparation copies the request and scaffolds the external CL_RUNTIME_DIR/plan.md. The current
main/orchestrating model must inspect the repository and author that plan
directly. This script never starts or resumes a planning agent.

Validation rejects missing headings, missing CL-NNN items, and template
placeholders before change-loop may execute.
EOF
}

self_check() {
  local template="$PLAN_SKILL_DIR/templates/plan.md"
  local contract="$PLAN_SKILL_DIR/templates/plan_prompt.md"
  [[ -s "$template" && -s "$contract" ]] || cl_die "plan templates are missing"
  grep -q '^## Plan items' "$template" || cl_die "plan template lacks Plan items"
  grep -q '^## Out of scope / must not change' "$template" ||
    cl_die "plan template lacks out-of-scope section"
  grep -q 'Exact intended behavior' "$template" ||
    cl_die "plan template lacks intended-behavior field"
  grep -q 'current main/orchestrating model authors this plan directly' "$contract" ||
    cl_die "plan authoring contract does not bind authorship to the main model"
  printf 'plan-changes self-check: PASS (main-model authorship, scaffold, validation contract)\n'
}

operation='prepare'
dry_run=0
input_mode='file'
input=''
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help | -h)
      usage
      exit 0
      ;;
    --self-check)
      self_check
      exit 0
      ;;
    --prepare)
      operation='prepare'
      shift
      ;;
    --validate)
      operation='validate'
      shift
      ;;
    --dry-run)
      dry_run=1
      operation='prepare'
      shift
      ;;
    --file)
      [[ "$#" -ge 2 ]] || cl_die "--file requires a path"
      [[ -z "$input" ]] || cl_die "provide exactly one change-list input"
      input_mode='file'
      input="$2"
      shift 2
      ;;
    --text)
      [[ "$#" -ge 2 ]] || cl_die "--text requires a value"
      [[ -z "$input" ]] || cl_die "provide exactly one change-list input"
      input_mode='text'
      input="$2"
      shift 2
      ;;
    --*)
      cl_die "unknown option: $1"
      ;;
    *)
      [[ -z "$input" ]] || cl_die "provide exactly one change-list input"
      input_mode='file'
      input="$1"
      shift
      ;;
  esac
done

if [[ "$operation" == validate ]]; then
  [[ -z "$input" ]] || cl_die "--validate accepts no change-list input"
  [[ "$dry_run" -eq 0 ]] || cl_die "--dry-run cannot be combined with --validate"
  cl_init_repo
  cl_require_server_repository
  cl_validate_plan_file "$CL_PLAN_PATH"
  cl_require_command sha256sum
  plan_sha256="$(sha256sum "$CL_PLAN_PATH" | awk '{print tolower($1)}')"
  printf 'Main-model plan validation: PASS\n'
  printf 'Plan SHA-256: %s\n' "$plan_sha256"
  printf '===== %s =====\n' "$CL_PLAN_PATH"
  cat "$CL_PLAN_PATH"
  exit 0
fi

[[ -n "$input" ]] || {
  usage >&2
  exit 2
}

if [[ "$input_mode" == file ]]; then
  [[ -s "$input" ]] || cl_die "change-list file is missing or empty: $input"
  changes="$(cat "$input")"
else
  changes="$input"
  [[ -n "${changes//[[:space:]]/}" ]] || cl_die "change-list text must not be empty"
fi

cl_init_repo
cl_require_server_repository
changes_copy="$CL_RUN_DIR/changes.md"

if [[ "$dry_run" -eq 1 ]]; then
  printf 'Would prepare main-model plan inputs; no planning agent will run.\n'
  printf 'Input copy: %s\nPlan scaffold: %s\n' "$changes_copy" "$CL_PLAN_PATH"
  printf 'Authoring contract: %s\n' "$PLAN_SKILL_DIR/templates/plan_prompt.md"
  exit 0
fi

# A new request invalidates any old plan and review. The current main model
# authors the newly scaffolded plan after this deterministic preparation step.
rm -f "$CL_RUN_DIR/plan-review.md" "$CL_RUN_DIR/plan-amendments.md"
printf '%s\n' "$changes" >"$changes_copy"
while IFS= read -r line || [[ -n "$line" ]]; do
  if [[ "$line" == '- Source: `.change-loop/changes.md`' ]]; then
    printf -- '- Source: `%s`\n' "$changes_copy"
  else
    printf '%s\n' "$line"
  fi
done <"$PLAN_SKILL_DIR/templates/plan.md" >"$CL_PLAN_PATH"

cat <<EOF
Prepared main-model planning workspace.

- Request copy: $changes_copy
- Plan scaffold: $CL_PLAN_PATH
- Authoring contract: $PLAN_SKILL_DIR/templates/plan_prompt.md

The current main/orchestrating model must now inspect the repository and author
$CL_PLAN_PATH directly. Do not delegate plan authorship to a subagent, codex
exec session, doer, or tester. When complete, run:

  bash $PLAN_SKILL_DIR/scripts/plan.sh --validate
EOF
