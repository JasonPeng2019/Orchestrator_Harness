"""Read-only audit of this run's completed launch-smoke artifacts, not a scheduler."""
import hashlib
import json
import sys
from pathlib import Path

run = Path(__file__).resolve().parent
repo = run.parents[2]
mapping = json.loads((repo / '.plans/SUBAGENT_ROLE_MODEL_MAPPING.json').read_text(encoding='utf-8'))
roles = [role for role in mapping['roles'] if role != 'root']
rows = []
for workspace in ('workspace', 'ollama-workspace'):
    for lane_path in sorted((run / workspace / '.harness-runtime/epochs').glob('*/lanes/*/lane.json')):
        lane = json.loads(lane_path.read_text(encoding='utf-8'))
        worktree = Path(lane['worktree_path'])
        status = json.loads(Path(lane['controller_status_path']).read_text(encoding='utf-8'))
        row = dict(lane=lane['lane_id'], run_id=lane['run_id'], workspace=workspace, provider=lane['provider'],
                   session=lane.get('session'), cleanup=status.get('cleanup_proven'), lifecycle=lane['lifecycle'])
        try:
            proof = json.loads((worktree / '.agent-workspace/preferred-proof.json').read_text(encoding='utf-8-sig'))
            result = json.loads((worktree / 'RESULT.json').read_text(encoding='utf-8-sig'))
            role = proof['role']
            row['role'] = role
            expected = mapping['roles'][role]
            n = roles.index(role) + 1
            assert proof['challenge'] == f'binding-{role}-{n}', 'challenge mismatch'
            assert proof['answer'] == 17 * 19 + n, 'answer mismatch'
            for record in (proof, result):
                assert record['lane_id'] == lane['lane_id'], 'lane mismatch'
                assert record['run_id'] == lane['run_id'], 'run mismatch'
            digest = result.pop('content_hash')
            assert digest == hashlib.sha256(json.dumps(result, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest(), 'hash mismatch'
            assert result['outcome'] == 'PASS', 'non-PASS result'
            assert status.get('result_state') == 'valid', 'native result invalid'
            assert status.get('cleanup_proven') is True, 'cleanup unproven'
            assert status['provider_state'].get('exit_code') == 0, 'provider exit not zero'
            assert lane['provider']['model'] == expected['model'], 'model mismatch'
            expected_config = dict(expected['launch_config'])
            assert lane['provider']['launch_config'] == expected_config, 'config mismatch'
            assert lane['provider']['id'] == expected['provider'], 'provider mismatch'
            assert lane.get('session', {}).get('session_id'), 'missing native session'
            events = [json.loads(line) for line in Path(lane['controller_events_path']).read_text(encoding='utf-8').splitlines() if line.strip()]
            argv = [item['detail'] for item in events if item.get('event_type') == 'provider_started']
            assert argv and expected['model'] in argv[0], 'missing model argv evidence'
            if expected_config.get('launcher') == 'ollama':
                assert argv[0].startswith('ollama launch codex --model '), 'wrong Ollama transport'
            transcript = []
            for line in Path(lane['transcript_path']).read_text(encoding='utf-8').splitlines():
                try:
                    transcript.append(json.loads(line))
                except ValueError:
                    pass  # Ollama may include its own textual startup output.
            tool_calls = sum(event.get('type') == 'item.completed' and event.get('item', {}).get('type') == 'command_execution' and event['item'].get('exit_code') == 0 for event in transcript)
            tool_calls += sum(block.get('type') == 'tool_use' for event in transcript for block in event.get('message', {}).get('content', []) if isinstance(block, dict))
            assert tool_calls, 'missing actual tool execution'
            row.update(outcome='PASS', answer=proof['answer'], tool_calls=tool_calls, content_hash=digest, argv=argv)
        except (OSError, ValueError, KeyError, AssertionError) as exc:
            row.update(outcome='INCOMPLETE', reason=str(exc))
        rows.append(row)
passed = sorted({row.get('role') for row in rows if row['outcome'] == 'PASS'})
missing = sorted(set(roles) - set(passed))
print(json.dumps(dict(passed_roles=passed, missing_roles=missing, lanes=rows), indent=2))
sys.exit(bool(missing))
