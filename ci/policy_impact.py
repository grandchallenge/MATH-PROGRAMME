#!/usr/bin/env python3
"""Fail-closed impact classifier for Programme policy and formal replay lanes."""
from __future__ import annotations
import argparse, fnmatch, json, os, subprocess, sys
from pathlib import Path
from typing import Iterable
import jsonschema
ROOT=Path(__file__).resolve().parents[1]
CONTROL_PATH=ROOT/'governance/policy_impact_gating.json'; CONTROL_SCHEMA=ROOT/'schemas/policy_impact_gating.schema.json'
FORMAL_PATH=ROOT/'governance/formal_replay_policy.json'
REGISTRY_PATH=ROOT/'governance/policy_shard_registry.json'; REGISTRY_SCHEMA=ROOT/'schemas/policy_shard_registry.schema.json'
CMDG_GATE_PATH=ROOT/'governance/cmdg_workflow_impact_gating.json'
ALL_SHARDS=('core','fixtures','cmdg','administrative','campaigns','contracts','docs'); ALL_LANES=('log-gcd','pc-wp04','union-closed-mathcert')
FULL_FANOUT_PATHS={'.github/workflows/ci.yml','.github/workflows/cmdg-postmerge.yml','ci/policy_impact.py','ci/test_policy_impact.py','ci/cmdg_postmerge_readback.py','ci/run_policy_shard.py','ci/validate_policy_reachability.py','ci/test_policy_reachability.py','ci/validate_repository_execution.py','ci/test_repository_execution.py','ci/validate_workflow_semantics.py','ci/test_workflow_semantics.py','governance/policy_impact_gating.json','governance/policy_shard_registry.json','governance/cmdg_workflow_impact_gating.json','schemas/policy_impact_gating.schema.json','schemas/policy_shard_registry.schema.json','schemas/cmdg_workflow_impact_gating.schema.json','schemas/cmdg_postmerge_readback.schema.json'}
ZERO_SHA='0'*40
class ImpactError(RuntimeError):pass
def load_json(path:Path)->dict:
    v=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(v,dict):raise ImpactError(f'expected object: {path}')
    return v
def normalize_paths(paths:Iterable[str])->list[str]:
    out=[]
    for raw in paths:
        p=str(raw).replace('\\','/')
        if p.startswith('./'):p=p[2:]
        if not p or p.startswith('/') or p=='..' or p.startswith('../') or '/../' in p or p.endswith('/..'):raise ImpactError(f'unsafe changed path: {raw!r}')
        out.append(p)
    return sorted(set(out))
def matches_root(path:str,root:str)->bool:
    root=root.rstrip('/');return path==root or path.startswith(root+'/')
def matches_pattern(path:str,pattern:str)->bool:return fnmatch.fnmatchcase(path,pattern)
def enforce_cmdg_native_filter_guard(changed:list[str],event_name:str)->None:
    if event_name!='pull_request' or not CMDG_GATE_PATH.is_file():return
    control=load_json(CMDG_GATE_PATH)
    if control.get('control_id')!='MP-CMDG-WORKFLOW-IMPACT-GATING-001' or control.get('status')!='ACTIVE_ON_PROTECTED_MERGE':raise ImpactError('CMDG workflow impact gating control identity/status drift')
    guard=control.get('native_path_filter_guard')
    patterns=control.get('pull_request_paths')
    if not isinstance(guard,dict) or guard.get('event')!='pull_request':raise ImpactError('CMDG native path-filter guard contract drift')
    if not isinstance(patterns,list) or not patterns or not all(isinstance(x,str) and x for x in patterns):raise ImpactError('CMDG pull-request path closure missing')
    try:limit=int(guard.get('max_changed_files',0))
    except (TypeError,ValueError):raise ImpactError('CMDG native path-filter guard limit invalid')
    if limit!=300:raise ImpactError('CMDG native path-filter guard must remain at conservative 300-file bound')
    if len(changed)<=limit:return
    relevant=[p for p in changed if any(matches_pattern(p,pattern) for pattern in patterns)]
    if relevant:
        raise ImpactError(f'CMDG native path-filter guard: {len(changed)} changed files exceeds conservative {limit}-file bound and includes governed CMDG dependencies; split the PR')
def formal_lane_impacts(paths:list[str],formal:dict,force_full:bool)->dict[str,bool]:
    if force_full:return {lane:True for lane in ALL_LANES}
    globals_={str(x) for x in formal.get('global',{}).get('inputs',[])}
    if any(p in FULL_FANOUT_PATHS or p in globals_ for p in paths):return {lane:True for lane in ALL_LANES}
    result={}
    for lane in ALL_LANES:
        policy=formal.get('lanes',{}).get(lane)
        if not isinstance(policy,dict):raise ImpactError(f'formal lane missing: {lane}')
        roots=[str(x) for x in policy.get('roots',[])];files={str(x) for x in policy.get('files',[])}
        result[lane]=any(p in files or any(matches_root(p,r) for r in roots) for p in paths)
    return result
def shard_impacts(paths:list[str])->tuple[list[str],list[str]]:
    active={'core'};unknown=[]
    if any(p in FULL_FANOUT_PATHS for p in paths):return list(ALL_SHARDS),[]
    for p in paths:
        lower=p.lower();matched=False
        if p.startswith('docs/') or p in {'mkdocs.yml','requirements/docs.txt'}:active.add('docs');matched=True
        if p.startswith('tools/render_visual_pedagogy') and p.endswith('.py'):
            active.update({'contracts','docs'});matched=True
        if p.startswith('fixtures/algebraic/') or p.startswith('fixtures/formal/') or any(t in lower for t in ('grobner','chaidez','researchmath','log_gcd')):active.add('fixtures');matched=True
        if p.startswith('fixtures/cmdg/') or 'cmdg' in lower:active.add('cmdg');matched=True
        if any(t in lower for t in ('administrative','maintenance','autonomy')):active.add('administrative');matched=True
        if p.startswith('campaigns/') or 'campaign' in lower:active.add('campaigns');matched=True
        if p=='requirements/policy.txt' or p.startswith('.github/workflows/') or p.startswith('experiments/'):active.add('contracts');matched=True
        if p.startswith('ci/') and any(t in lower for t in ('programme','workflow','policy','repository_execution','retired')):active.add('contracts');matched=True
        if p.startswith('tests/'):
            if 'administrative' in lower:active.add('administrative')
            elif 'cmdg' in lower:active.add('cmdg')
            elif 'campaign' in lower:active.add('campaigns')
            else:active.add('contracts')
            matched=True
        if p.startswith('schemas/') or p.startswith('governance/') or p.startswith('evidence/'):active.add('contracts');matched=True
        if p.endswith('.md') or p in {'README.md','CONTRIBUTING.md'}:active.add('docs');matched=True
        if not matched:unknown.append(p)
    if unknown:return list(ALL_SHARDS),unknown
    return [s for s in ALL_SHARDS if s in active],[]
def classify_paths(paths:Iterable[str],*,event_name:str='pull_request',schedule:str|None=None)->dict:
    changed=normalize_paths(paths);enforce_cmdg_native_filter_guard(changed,event_name);control=load_json(CONTROL_PATH);formal=load_json(FORMAL_PATH);formal_cron=str(control['formal_replay']['sentinel']['cron']);full_cron=str(control['policy_dag']['full_policy_sentinel_cron']);clean={lane:False for lane in ALL_LANES}
    if event_name=='schedule':
        if schedule==formal_cron:return {'event_mode':'formal_sentinel','changed_paths':[],'unknown_paths':[],'policy_shards':['core'],'formal_dirty':clean}
        if schedule==full_cron:return {'event_mode':'full_policy_sentinel','changed_paths':[],'unknown_paths':[],'policy_shards':list(ALL_SHARDS),'formal_dirty':clean}
        return {'event_mode':'unknown_schedule','changed_paths':[],'unknown_paths':[f'schedule:{schedule}'],'policy_shards':list(ALL_SHARDS),'formal_dirty':{lane:True for lane in ALL_LANES}}
    if event_name=='workflow_dispatch':return {'event_mode':'manual_full','changed_paths':changed,'unknown_paths':[],'policy_shards':list(ALL_SHARDS),'formal_dirty':{lane:True for lane in ALL_LANES}}
    shards,unknown=shard_impacts(changed);dirty=formal_lane_impacts(changed,formal,bool(unknown))
    if event_name=='push' and 'docs' not in shards:shards=[s for s in ALL_SHARDS if s in set(shards)|{'docs'}]
    return {'event_mode':'transition','changed_paths':changed,'unknown_paths':unknown,'policy_shards':shards,'formal_dirty':dirty}
def git_changed_paths(base:str,head:str)->list[str]:
    if not base or not head or base==ZERO_SHA:raise ImpactError('transition diff base/head is unavailable')
    cp=subprocess.run(['git','diff','--name-only',base,head,'--'],cwd=ROOT,check=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if cp.returncode:raise ImpactError(f'git diff failed: {cp.stderr.strip()}')
    return [x for x in cp.stdout.splitlines() if x.strip()]
def changed_paths_from_event(event_name:str,event:dict)->list[str]:
    if event_name=='pull_request':
        pr=event.get('pull_request',{});return git_changed_paths(str(pr.get('base',{}).get('sha') or ''),str(pr.get('head',{}).get('sha') or ''))
    if event_name=='push':return git_changed_paths(str(event.get('before') or ''),str(event.get('after') or os.environ.get('GITHUB_SHA') or ''))
    return []
def write_output(path:str|None,result:dict)->None:
    if not path:return
    vals={'event_mode':result['event_mode'],'policy_shards':json.dumps(result['policy_shards'],separators=(',',':')),'unknown_count':len(result['unknown_paths']),'log_gcd_dirty':result['formal_dirty']['log-gcd'],'pc_wp04_dirty':result['formal_dirty']['pc-wp04'],'union_closed_dirty':result['formal_dirty']['union-closed-mathcert']}
    with open(path,'a',encoding='utf-8') as h:
        for k,v in vals.items():h.write(f"{k}={'true' if v is True else 'false' if v is False else v}\n")
def validate_control()->None:
    c=load_json(CONTROL_PATH);f=load_json(FORMAL_PATH);r=load_json(REGISTRY_PATH)
    jsonschema.validate(c,load_json(CONTROL_SCHEMA));jsonschema.validate(r,load_json(REGISTRY_SCHEMA))
    if c.get('control_id')!='MP-POLICY-IMPACT-GATING-001' or c.get('status')!='ACTIVE_ON_PROTECTED_MERGE':raise ImpactError('policy impact control identity/status drift')
    if c.get('classifier',{}).get('unknown_path_behavior')!='FULL_FANOUT':raise ImpactError('unknown path behavior must remain FULL_FANOUT')
    clean=c.get('formal_replay',{}).get('clean_transition',{})
    if clean.get('full_replay_allowed') is not False or clean.get('protected_attestation_required') is not True:raise ImpactError('clean formal transitions must remain attest-only')
    if int(clean.get('max_attestation_age_hours',0))!=int(f.get('sentinel',{}).get('required_full_replay_within_hours',-1)):raise ImpactError('clean sentinel bound drift')
    if c.get('formal_replay',{}).get('sentinel',{}).get('cron')!=f.get('sentinel',{}).get('scheduled_probe_cron'):raise ImpactError('formal sentinel cron drift')
    if tuple(c.get('policy_dag',{}).get('shards',[]))!=ALL_SHARDS or set(r.get('shards',{}))!=set(ALL_SHARDS):raise ImpactError('policy shard coverage drift')
    bad=('required_checks_removed_or_renamed','formal_proof_closure_weakened','formal_semantic_tcb_weakened','bypass_created','emergency_authority_created','direct_protected_push_authorized','human_steward_impersonation_authorized')
    if any(c.get('authority_boundary',{}).get(k) is not False for k in bad):raise ImpactError('authority boundary weakened')
    if any(v is not False for v in c.get('claim_boundaries',{}).values()):raise ImpactError('claim boundary weakened')
def main()->int:
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True);q=sub.add_parser('classify');q.add_argument('--event-path',default=os.environ.get('GITHUB_EVENT_PATH'));q.add_argument('--event-name',default=os.environ.get('GITHUB_EVENT_NAME','workflow_dispatch'));q.add_argument('--schedule',default=os.environ.get('GCL_EVENT_SCHEDULE'));q.add_argument('--github-output',default=os.environ.get('GITHUB_OUTPUT'));sub.add_parser('validate');a=p.parse_args()
    try:
        if a.command=='validate':validate_control();print('policy impact gating control: valid');return 0
        event=json.loads(Path(a.event_path).read_text(encoding='utf-8')) if a.event_path else {};paths=changed_paths_from_event(a.event_name,event);result=classify_paths(paths,event_name=a.event_name,schedule=a.schedule);write_output(a.github_output,result);print(json.dumps(result,sort_keys=True));return 0
    except (ImpactError,OSError,json.JSONDecodeError,jsonschema.ValidationError,KeyError,ValueError) as exc:print(f'policy impact classification error: {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
