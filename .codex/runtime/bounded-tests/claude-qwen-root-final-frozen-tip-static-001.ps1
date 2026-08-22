$dev = 'C:\Users\Jason\Documents\Jason\Orchestrator_Harness\.codex\dev'
$config = 'C:\Users\Jason\Documents\Jason\Orchestrator_Harness\.codex\dev\pyproject.toml'
$sources = @(
    'orchestrator_harness/claude_adapter.py', 'orchestrator_harness/claude_installer.py',
    'orchestrator_harness/qwen_adapter.py', 'orchestrator_harness/qwen_installer.py',
    'orchestrator_harness/provider.py', 'orchestrator_harness/invocation.py',
    'orchestrator_harness/lane_controller.py', 'orchestrator_harness/codex_adapter.py',
    'orchestrator_harness/cli.py', 'orchestrator_harness/__init__.py',
    'examples/disposable_claude_coding_fixture.py', 'examples/disposable_qwen_coding_fixture.py',
    'orchestrator_harness/assets/claude/orchestrator_harness_post_tool_use.py',
    'orchestrator_harness/assets/claude/orchestrator_harness_stop.py',
    'orchestrator_harness/assets/qwen/orchestrator_harness_notification.py',
    'orchestrator_harness/assets/qwen/orchestrator_harness_post_tool_use.py',
    'orchestrator_harness/assets/qwen/orchestrator_harness_stop.py',
    'orchestrator_harness/tests/test_compat_claude_adapter.py',
    'orchestrator_harness/tests/test_compat_provider_allowlist.py',
    'orchestrator_harness/tests/test_compat_provider_argv.py',
    'orchestrator_harness/tests/test_compat_transcript_parse.py',
    'orchestrator_harness/tests/test_compat_qwen_adapter.py',
    'orchestrator_harness/tests/test_qwen_provider.py',
    'orchestrator_harness/tests/test_provider_adapter_registry.py'
)

uv run --project $dev --locked ruff check --config $config --no-cache @sources
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
uv run --project $dev --locked basedpyright --project pyrightconfig.json @sources
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m py_compile @sources
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m unittest orchestrator_harness.tests.test_compat_claude_adapter orchestrator_harness.tests.test_compat_provider_allowlist orchestrator_harness.tests.test_compat_provider_argv orchestrator_harness.tests.test_compat_transcript_parse orchestrator_harness.tests.test_compat_qwen_adapter orchestrator_harness.tests.test_qwen_provider orchestrator_harness.tests.test_provider_adapter_registry -v
exit $LASTEXITCODE
