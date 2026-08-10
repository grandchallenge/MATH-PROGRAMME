#!/usr/bin/env python3
"""Clean/dirty/sentinel gate for content-addressed formal replay."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import formal_replay_attestation as formal
PROTECTED_EVENTS={'push','schedule'}
def validate(repo:Path,policy:dict,lane:str,receipt:dict,max_age:float)->tuple[bool,str]:
    lp=formal.lane_policy(policy,lane); digest,_=formal.compute_digest(repo,policy,lane)
    required={'schema_version':1,'lane':lane,'status':formal.RECEIPT_STATUS,'input_digest':digest,'repository':policy['global']['repository'],'origin_ref':'refs/heads/main','policy_operation':policy.get('operation')}
    for k,v in required.items():
        if receipt.get(k)!=v:return False,f'receipt_{k}_mismatch'
    if receipt.get('origin_event') not in PROTECTED_EVENTS:return False,'receipt_origin_event_not_protected'
    origin=str(receipt.get('origin_commit',''))
    if not formal.SHA40.fullmatch(origin):return False,'receipt_origin_commit_invalid'
    if not formal.is_ancestor(repo,origin):return False,'receipt_origin_not_ancestor'
    try: created=formal.parse_time(str(receipt['created_at']))
    except Exception:return False,'receipt_created_at_invalid'
    age=(formal.now_utc()-created).total_seconds()
    if age<0:return False,'receipt_from_future'
    if age>=max_age*3600:return False,'protected_sentinel_stale'
    if receipt.get('command')!=lp.get('command'):return False,'receipt_command_mismatch'
    if receipt.get('proof_semantic_tcb')!=lp.get('proof_semantic_tcb'):return False,'receipt_tcb_mismatch'
    return True,'protected_attestation_healthy'
def output(path:str|None,values:dict)->None:
    if not path:return
    with open(path,'a',encoding='utf-8') as h:
        for k,v in values.items():h.write(f"{k}={'true' if v is True else 'false' if v is False else v}\n")
def decide(repo:Path,policy:dict,lane:str,receipt_path:Path,mode:str,out:str|None)->int:
    if mode not in {'clean','dirty','sentinel'}:raise formal.PolicyError('unsupported replay mode')
    max_age=float(policy['sentinel']['required_full_replay_within_hours'] if mode=='clean' else policy['sentinel']['reuse_max_age_hours'])
    if not receipt_path.is_file():reuse,reason=False,'receipt_missing'
    else:
        try:reuse,reason=validate(repo,policy,lane,json.loads(receipt_path.read_text(encoding='utf-8')),max_age)
        except Exception as exc:reuse,reason=False,f'receipt_invalid:{type(exc).__name__}'
    if mode=='clean' and not reuse:
        vals={'reuse':False,'reason':reason,'status':'FORMAL_REPLAY_SENTINEL_STALE'};output(out,vals);print(json.dumps(vals,sort_keys=True));print(f'FORMAL_REPLAY_SENTINEL_STALE: {lane}: {reason}',file=sys.stderr);return 3
    vals={'reuse':reuse,'reason':reason,'status':formal.REUSE_STATUS if reuse else 'FULL_FORMAL_REPLAY_REQUIRED'};output(out,vals);print(json.dumps(vals,sort_keys=True));return 0
def main()->int:
    p=argparse.ArgumentParser();p.add_argument('--repo',default='.');p.add_argument('--policy',default=str(formal.DEFAULT_POLICY));sub=p.add_subparsers(dest='command',required=True)
    d=sub.add_parser('decide');d.add_argument('--lane',required=True);d.add_argument('--receipt',required=True);d.add_argument('--mode',required=True,choices=('clean','dirty','sentinel'));d.add_argument('--github-output')
    e=sub.add_parser('emit-receipt');e.add_argument('--lane',required=True);e.add_argument('--output',required=True);e.add_argument('--origin-commit',required=True);e.add_argument('--origin-run-id',required=True);e.add_argument('--origin-run-attempt',default='1');e.add_argument('--origin-event',required=True);e.add_argument('--origin-ref',required=True);e.add_argument('--result-file',action='append',default=[])
    a=p.parse_args();repo=Path(a.repo).resolve()
    try:
        policy=formal.load_policy(repo/a.policy)
        if a.command=='decide':return decide(repo,policy,a.lane,repo/a.receipt,a.mode,a.github_output)
        receipt=formal.emit_receipt(repo,policy,a.lane,repo/a.output,origin_commit=a.origin_commit,origin_run_id=a.origin_run_id,origin_run_attempt=a.origin_run_attempt,origin_event=a.origin_event,origin_ref=a.origin_ref,result_files=[repo/x for x in a.result_file]);print(json.dumps(receipt,sort_keys=True));return 0
    except (formal.PolicyError,OSError,json.JSONDecodeError,KeyError,ValueError) as exc:print(f'formal replay gate error: {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
