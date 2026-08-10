#!/usr/bin/env python3
from __future__ import annotations
import copy
from validate_workflow_semantics import load_workflows, workflow_semantic_errors

def main()->int:
    workflows=load_workflows();assert not workflow_semantic_errors(workflows=workflows)
    duplicate=copy.deepcopy(workflows);duplicate['pages.yml']['name']=duplicate['ci.yml']['name'];assert any('workflow names must be unique' in e for e in workflow_semantic_errors(workflows=duplicate))
    runner=copy.deepcopy(workflows);runner['ci.yml']['jobs']['validate-json']['runs-on']='ubuntu-latest';assert any('runs-on must be pinned' in e for e in workflow_semantic_errors(workflows=runner))
    classifier=copy.deepcopy(workflows)
    for s in classifier['ci.yml']['jobs']['impact']['steps']:
        if 'policy_impact.py classify' in str(s.get('run','')):s['run']='echo omitted'
    assert any('impact classifier' in e for e in workflow_semantic_errors(workflows=classifier))
    aggregate=copy.deepcopy(workflows);aggregate['ci.yml']['jobs']['validate-json']['needs']=['impact'];assert any('aggregate impact and policy-shard' in e for e in workflow_semantic_errors(workflows=aggregate))
    gate=copy.deepcopy(workflows)
    for s in gate['ci.yml']['jobs']['log-gcd-lean']['steps']:
        if 'formal_replay_gate.py decide' in str(s.get('run','')):s['run']=str(s['run']).replace('formal_replay_gate.py decide','formal_replay_attestation.py decide')
    assert any('formal replay impact-gate' in e for e in workflow_semantic_errors(workflows=gate))
    pages=copy.deepcopy(workflows);pages['pages.yml']['concurrency']['cancel-in-progress']='false';assert any('cancel stale' in e for e in workflow_semantic_errors(workflows=pages))
    print('workflow semantic rejection tests passed');return 0
if __name__=='__main__':raise SystemExit(main())
