from pathlib import Path
import json,os,subprocess,shutil,time
root=Path(__file__).resolve().parents[2]; out=Path(__file__).resolve().parent
mapping=json.loads((root/'master_planning/SUBAGENT_ROLE_MODEL_MAPPING.json').read_text())
role=mapping['roles']['REVIEWER']['primary']; cmd=[str(shutil.which('claude')) if x=='claude' else x for x in role['headless_command']]
cmd=[(out/'followup-prompt.txt').read_text(encoding='utf-8') if x=='{task_text}' else x for x in cmd]
cmd[1:1]=['--tools','Read,Glob,Grep','--allowedTools','Read','Glob','Grep']
os.environ['CLAUDE_CONFIG_DIR']=str(root/'.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/live-provider-homes/claude')
started=time.time()
with (out/'review-followup.stdout.json').open('w',encoding='utf-8') as so,(out/'review-followup.stderr.txt').open('w',encoding='utf-8') as se:
 p=subprocess.Popen(cmd,cwd=root,stdout=so,stderr=se,shell=False,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/'review-followup.child.json').write_text(json.dumps({'pid':p.pid,'provider':role['provider'],'model':role['model'],'reasoning_effort':role['reasoning_effort'],'tools':['Read','Glob','Grep']}))
 code=p.wait()
(out/'review-followup.done.json').write_text(json.dumps({'exit_code':code,'elapsed_seconds':time.time()-started}))
