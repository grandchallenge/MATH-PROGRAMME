#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'governance/policy_shard_registry.json'
def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--shard',required=True); p.add_argument('--log'); a=p.parse_args()
    try:
        data=json.loads(REGISTRY.read_text(encoding='utf-8'))
        if data.get('registry_id')!='MP-POLICY-SHARDS-001': raise RuntimeError('policy shard registry identity drift')
        commands=data.get('shards',{}).get(a.shard)
        if not isinstance(commands,list) or not commands: raise RuntimeError(f'unknown or empty policy shard: {a.shard}')
        log=Path(a.log) if a.log else ROOT/f'policy-shard-{a.shard}.log'
        shard_started=time.perf_counter()
        with log.open('w',encoding='utf-8') as fh:
            for i,cmd in enumerate(commands,1):
                if not isinstance(cmd,list) or not cmd or not all(isinstance(x,str) and x for x in cmd): raise RuntimeError('invalid shard command')
                rendered=' '.join(cmd); print(f'[{a.shard} {i}/{len(commands)}] {rendered}'); fh.write('$ '+rendered+'\n'); fh.flush()
                started=time.perf_counter()
                cp=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,check=False)
                elapsed=time.perf_counter()-started
                out=cp.stdout or ''; sys.stdout.write(out); fh.write(out)
                timing=f'POLICY_SHARD_TIMING shard={a.shard} operation={i} seconds={elapsed:.3f} status={"PASS" if cp.returncode==0 else "FAIL"}\n'
                print(timing,end=''); fh.write(timing); fh.flush()
                if cp.returncode: return cp.returncode
        total=time.perf_counter()-shard_started
        print(f'POLICY_SHARD_TIMING_TOTAL shard={a.shard} seconds={total:.3f}')
        print(f'policy shard {a.shard}: success'); return 0
    except (OSError,RuntimeError,json.JSONDecodeError) as exc:
        print(f'policy shard execution error: {exc}',file=sys.stderr); return 2
if __name__=='__main__': raise SystemExit(main())
