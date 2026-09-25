"""Read-only evidence audit for the non-direct-Codex fallback smoke test."""
import hashlib
import json
from pathlib import Path

run = Path(__file__).resolve().parent
repo = run.parents[2]
mapping = json.loads((repo / '.plans/SUBAGENT_ROLE_MODEL_MAPPING.json').read_text(encoding='utf-8'))
selected, skipped = [], []
for role, allocation in mapping['roles'].items():
    for index, binding in enumerate(allocation.get('fallback_policy', {}).get('fallbacks', []), 1):
        entry = dict(role=role, fallback_index=index, binding=binding)
        direct_codex = binding['provider'] == 'codex' and binding['cli'] == 'codex' and binding['launch_config'].get('launcher', 'codex') == 'codex'
        (skipped if direct_codex else selected).append(entry)
assert len(selected) == 1 and selected[0]['role'] == 'test_author', 'fallback scope changed'
assert len(skipped) == 7, 'excluded direct-Codex scope changed'
expected = selected[0]['binding']
assert expected['model'] == 'claude-opus-4-8'
assert expected['launch_config'] == {'effort': 'max'}

epoch = run / 'workspace/.harness-runtime/epochs/d5f003706ec444198a018186f69ed547/lanes'
lane = json.loads((epoch / 'test-author-opus-02/lane.json').read_text(encoding='utf-8'))
worktree = Path(lane['worktree_path'])
status = json.loads(Path(lane['controller_status_path']).read_text(encoding='utf-8'))
proof = json.loads((worktree / '.agent-workspace/fallback-proof.json').read_text(encoding='utf-8-sig'))
result = json.loads((worktree / 'RESULT.json').read_text(encoding='utf-8-sig'))
assert proof['answer'] == 424 and proof['role'] == 'test_author_fallback_1'
assert proof['challenge'] == 'fallback-opus-max-101'
for record in (proof, result):
    assert record['lane_id'] == lane['lane_id'] and record['run_id'] == lane['run_id']
digest = result.pop('content_hash')
assert digest == hashlib.sha256(json.dumps(result, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()
assert result['outcome'] == 'PASS' and status['result_state'] == 'valid'
assert status['cleanup_proven'] is True and status['provider_state']['exit_code'] == 0
assert lane['provider'] == dict(id=expected['provider'], model=expected['model'], launch_config=expected['launch_config'])
events = [json.loads(line) for line in Path(lane['controller_events_path']).read_text(encoding='utf-8').splitlines()]
argv = [item['detail'] for item in events if item.get('event_type') == 'provider_started']
assert len(argv) == 1 and '--model claude-opus-4-8 --effort max' in argv[0]
assert '--fallback-model' not in argv[0]
transcript = [json.loads(line) for line in Path(lane['transcript_path']).read_text(encoding='utf-8').splitlines()]
native_result = [event for event in transcript if event.get('type') == 'result'][-1]
assert native_result['is_error'] is False and 'claude-opus-4-8' in native_result['modelUsage']
assert native_result['session_id'] == lane['session']['session_id']
tool_results = [block for event in transcript if event.get('type') == 'user' for block in event.get('message', {}).get('content', []) if isinstance(block, dict) and block.get('type') == 'tool_result' and not block.get('is_error')]
assert tool_results, 'no successful tool result'
failed = json.loads((epoch / 'test-author-opus-01/lane.json').read_text(encoding='utf-8'))
failed_status = json.loads(Path(failed['controller_status_path']).read_text(encoding='utf-8'))
assert failed_status['cleanup_proven'] is True
print(json.dumps(dict(outcome='PASS', selected=selected, skipped_direct_codex=skipped,
                     successful_lane=lane['lane_id'], run_id=lane['run_id'],
                     provider_session=lane['session']['session_id'],
                     actual_model=list(native_result['modelUsage']), result_hash=digest,
                     successful_tool_results=len(tool_results), argv=argv,
                     cleanup_proven=True, failed_identifier_attempt_preserved=True), indent=2))
