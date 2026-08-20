"""Prove the 0.3 env channel end-to-end at the merge boundary.

The lane controller's provider launch path for a canonical invocation is:

1. ``build_child_environment(profile)`` -- scrub the child environment to the
   base allow-list (ANTHROPIC_* variables are cleared).
2. ``claude_config_override_env`` -- translate each claude-code
   ``config_overrides`` entry into ANTHROPIC_* child-env assignments.
3. ``apply_provider_env_overrides(scrubbed, overrides)`` -- merge the declared
   overrides AFTER isolation; an explicit override always wins.

This script reproduces exactly those three calls with the fixture's own
profile/override and shows that the merged child environment carries the
Ollama redirect even though the scrub removed every ANTHROPIC_* variable.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parents[2]
if str(HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(HARNESS_ROOT))

from orchestrator_harness.lane_controller import apply_provider_env_overrides
from orchestrator_harness.profile import RuntimeProfile, build_child_environment
from orchestrator_harness.provider import claude_config_override_env

OVERRIDE = 'model_provider="ollama"'

profile = RuntimeProfile(
    "profile-claude-hello",
    "implementer",
    "claude-code",
    "deepseek-v4-flash:0731-cloud",
    ("Read", "Bash", "Write", "Edit", "Glob", "Grep"),
    ("repo",),
    (),
    ("CLAUDE_CONFIG_DIR", "HOME"),
)
scrubbed, cleared = build_child_environment(profile)

translated = claude_config_override_env(OVERRIDE)
merged = apply_provider_env_overrides(scrubbed, translated)

print("config_overrides entry:", OVERRIDE)
print("claude_config_override_env ->", json.dumps(translated, sort_keys=True))
print()
print("ANTHROPIC_* present in scrubbed child env:", [
    key for key in scrubbed if key.upper().startswith("ANTHROPIC_")
])
print("ANTHROPIC_* among cleared variables:", [
    key for key in cleared if key.upper().startswith("ANTHROPIC_")
])
print("granted provider_needs surviving the scrub: CLAUDE_CONFIG_DIR =",
      any(k.upper() == "CLAUDE_CONFIG_DIR" for k in scrubbed),
      "| HOME =", any(k.upper() == "HOME" for k in scrubbed))
print()
print("merged child env ANTHROPIC_* entries:")
for key in sorted(merged):
    if key.upper().startswith("ANTHROPIC_"):
        print(f"  {key} = {merged[key]!r}")
print()
assert any(k.upper() == "ANTHROPIC_BASE_URL" for k in merged)
assert any(k.upper() == "ANTHROPIC_AUTH_TOKEN" for k in merged)
assert any(k.upper() == "ANTHROPIC_API_KEY" for k in merged)
assert merged.get("ANTHROPIC_BASE_URL") == "http://localhost:11434"
assert merged.get("ANTHROPIC_AUTH_TOKEN") == "ollama"
print("ENV_CHANNEL_PROOF=PASS (overrides re-injected after isolation)")
