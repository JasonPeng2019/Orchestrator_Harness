import datetime,json,pathlib,subprocess,sys,time
root=pathlib.Path(__file__).resolve().parents[3]
run=root/'fresh-experiments/A22_20260726-062324'
cfg=root/'harness_watcher_implementation/canary-20260801-attention-r6.json'
epoch='20260801-attention-r6';sig='sig-20260801-attention-r6-synthetic-atlas-001';lane=f'{epoch}:Atlas:A22'
time.sleep(5)
now=datetime.datetime.now(datetime.timezone.utc);created=now.isoformat();delivery=(now+datetime.timedelta(seconds=10)).isoformat();response=(now+datetime.timedelta(seconds=120)).isoformat()
meta={'signal_id':sig,'lane_id':lane,'agent_blocked':True,'delivery_deadline_utc':delivery,'response_deadline_utc':response}
base=[sys.executable,'-m','harness_watcher_implementation','--config',str(cfg),'record-attention','--role','subagent','--source-id','Atlas','--epoch-id',epoch]
for kind in ('AGENT_SIGNAL_CREATED','AGENT_WAIT_STARTED'):
 r=subprocess.run(base+['--event-id',sig,'--kind',kind,'--metadata',json.dumps(meta,separators=(',',':'))],cwd=root,text=True,capture_output=True,check=True)
 o=json.loads(r.stdout); assert str(root/'harness_watcher/runs'/epoch) in o['path']
signal={'schema':'manager-signal/v1','signal_id':sig,'event_id':sig,'kind':'HELP','lane_id':lane,'task':'A22','phase':'R6_SYNTHETIC_READINESS','created_utc':created,'deadline_utc':response,'delivery_deadline_utc':delivery,'agent_blocked':True,'summary':'Synthetic host-only readiness request: publish CONTINUE.','evidence_paths':[]}
sp=run/'.agent-workspace/manager-signals'/f'{sig}.json';sp.parent.mkdir(exist_ok=True);sp.write_text(json.dumps(signal,indent=2)+'\n')
rp=run/'.agent-workspace/manager-responses'/f'{sig}.json';deadline=time.monotonic()+120
while time.monotonic()<deadline:
 if rp.exists():
  o=json.loads(rp.read_text());
  if o.get('event_id')==sig:
   for kind in ('AGENT_RESPONSE_RECEIVED','AGENT_WORK_RESUMED'):
    subprocess.run(base+['--event-id',sig,'--kind',kind,'--metadata',json.dumps(meta,separators=(',',':'))],cwd=root,check=True)
   pathlib.Path(__file__).with_name('SYNTHETIC_LANE_COMPLETE.json').write_text(json.dumps({'signal_id':sig,'response':o,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
   raise SystemExit(0)
 time.sleep(.25)
raise SystemExit('response timeout')
