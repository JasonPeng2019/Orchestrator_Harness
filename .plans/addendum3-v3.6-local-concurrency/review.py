"""Run the mapped read-only planning reviewer and retain its native response."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
root = out.parents[1]
phase = sys.argv[1]
mapping = json.loads((root / 'master_planning/SUBAGENT_ROLE_MODEL_MAPPING.json').read_text(encoding='utf-8-sig'))
role = mapping['roles']['REVIEWER']['primary']
prompt = (out / ('review-prompt.txt' if phase == 'initial' else 'followup-prompt.txt')).read_text(encoding='utf-8')
command = [shutil.which('claude') if value == 'claude' else value for value in role['headless_command']]
command[1:1] = ['--tools=Read,Glob,Grep', '--allowedTools=Read,Glob,Grep']
command = [prompt if value == '{task_text}' else value for value in command]
env = dict(os.environ, CLAUDE_CONFIG_DIR=str(root / '.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/live-provider-homes/claude'))
started = time.monotonic()
with (out / f'{phase}.stdout.json').open('w', encoding='utf-8') as stdout, (out / f'{phase}.stderr.txt').open('w', encoding='utf-8') as stderr:
    child = subprocess.Popen(command, cwd=root, env=env, stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
    (out / f'{phase}.child.json').write_text(json.dumps({'pid': child.pid, 'provider': role['provider'], 'model': role['model'], 'effort': role['reasoning_effort'], 'tools': ['Read', 'Glob', 'Grep']}), encoding='utf-8')
    code = child.wait()
(out / f'{phase}.done.json').write_text(json.dumps({'exit_code': code, 'elapsed_seconds': time.monotonic() - started}), encoding='utf-8')
sys.exit(code)
