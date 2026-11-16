#!/usr/bin/env python3
"""Offline first-parent formal impact shadow replay; never executes Lean.

Compares the protected old router semantics against the guarded candidate on
identical historical Git identities. This is retrospective reclassification,
not proof that historic toolchains or former policies were identical.
"""
from __future__ import annotations
import argparse
import collections
from contextlib import contextmanager
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'ci'))
import formal_validation as formal
import formal_contract_dependency as contracts


def run(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def historical_paths(parent: str, head: str, *, legacy: bool) -> list[str]:
    if legacy:
        text = run('diff', '--name-only', '--diff-filter=ACMR', parent, head)
        return formal.normalize_paths(text.splitlines())
    return formal.diff_paths(parent, head, ROOT)


def old_plan(paths: list[str], registry: dict) -> dict:
    # Force the newly guarded exception to its historical (always-full) path.
    # The router's other material, shared-CMDG and unknown-path cases remain
    # unchanged and are compared exhaustively in the replay.
    with mock.patch.object(formal, 'contract_only_safe', return_value=(False,'PREVIOUS_POLICY')):
        return formal.classify_paths(paths, registry)


def describe(plan: dict) -> dict:
    return {name:plan[name] for name in ('reason','lanes','control_plane_hits','unknown_paths')}


def replay(commits: int, history_head: str) -> dict:
    history_sha = run('rev-parse', history_head)
    original = json.loads(run('show',history_sha + ':governance/formal_validation_registry.json'))
    candidate = formal.load_registry(ROOT)
    all_ids = {lane['id'] for lane in candidate['lanes']}
    permitted = set(contracts.CONTRACT_FILES)
    guard_ok, guard_reason = contracts.contract_only_safe(ROOT, candidate)
    if not guard_ok:
        raise RuntimeError('NO-GO: dependency guard unproved: '+guard_reason)
    revisions = run('rev-list','--first-parent','--max-count',str(commits+1),history_sha).splitlines()
    rows=[];counts=collections.Counter()
    for current,parent in zip(revisions,revisions[1:]):
        old_paths=historical_paths(parent,current,legacy=True)
        new_paths=historical_paths(parent,current,legacy=False)
        record={'commit':current,'parent':parent,
                'original_diff_paths':old_paths,'candidate_diff_paths':new_paths}
        try:
            old=old_plan(old_paths,original)
            new=formal.classify_paths(new_paths,candidate)
            record['old']=describe(old)
            record['candidate']=describe(new)
            lost=set(old['lanes'])-set(new['lanes'])
            if lost:
                old_control=set(old['control_plane_hits'])
                # Never accept losing *any* lane except an old full fanout
                # caused exclusively by registered non-formal contracts.
                if not old_control or not old_control <= permitted:
                    raise AssertionError(f'NONCONTRACT_LANE_OMISSION:{sorted(lost)}')
                if set(new['lanes']) & all_ids - set(old['lanes']):
                    raise AssertionError('unexpected new lane set')
                counts['justified_full_replay_avoided'] += 1
                record['disposition']='GUARDED_CONTRACT_ONLY'
            elif set(new['lanes'])-set(old['lanes']):
                counts['extra_protective_lane_selection']+=1
                record['disposition']='MORE_PROTECTIVE'
            else:
                counts['unchanged_selection']+=1
                record['disposition']='SAME'
        except (formal.FormalValidationError, AssertionError) as exc:
            record['disposition']='REQUIRES_REVIEW'
            record['error']=type(exc).__name__+':'+str(exc)[:160]
            counts['requires_review']+=1
        rows.append(record)
    result={'record_type':'GCL_FORMAL_FANOUT_FIRST_PARENT_SHADOW/1',
            'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'protected_base_head':history_sha,
            'first_parent_transitions':len(rows),
            'full_fanout_patterns_preexisting':len(original['control_plane']['full_fanout_patterns']),
            'formal_lanes':len(candidate['lanes']),
            'guard':{'approved':guard_ok,'reason':guard_reason,
                     'audited_python_files':sorted(contracts.audited_code_paths(ROOT,candidate)),
                     'exact_contract_file_allowlist':sorted(permitted)},
            'counts':dict(counts), 'transitions':rows,
            'limitations':['Shadow uses current protected baseline policy against older changes; historical policy was not reconstructed commit-by-commit.',
                           'No Lean proofs executed by the shadow runner.',
                           'Historical queue/runner decisions may differ from current policy.',
                           'Runner elapsed minutes are not billing minutes.']}
    return result


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--commits',type=int,default=350)
    parser.add_argument('--history-head',default='HEAD',
                        help='exact commit identity used for historical first-parent transitions')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    if not (1 <= args.commits <= 2000):
        parser.error('--commits must be 1..2000')
    doc=replay(args.commits, args.history_head)
    dest=Path(args.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    encoded=json.dumps(doc,indent=2,sort_keys=True)+'\n'
    dest.write_text(encoded)
    print('SHADOW',json.dumps({'base':doc['protected_base_head'],
          'transitions':doc['first_parent_transitions'],
          'counts':doc['counts'],'sha256':hashlib.sha256(encoded.encode()).hexdigest(),
          'output':str(dest)}))
    return 1 if doc['counts'].get('requires_review',0) else 0

if __name__=='__main__':
    raise SystemExit(main())
