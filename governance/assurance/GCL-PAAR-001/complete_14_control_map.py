#!/usr/bin/env python3
"""Reconcile pinned 14-repo source map to live branch gates and workflow activity.

This is an assertion routing/control map, not a mathematical or global PASS.
"""
from __future__ import annotations
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).parent
ORIGIN='grandchallenge/'
CLASSES={
 '.github':'ORG_GOVERNANCE_REVIEW_AND_WORKER_CLERKS',
 'ADAPTIVE-INTELLIGENCE-ATLAS':'RESEARCH_MANUSCRIPT_EDITORIAL',
 'AETHER':'RESEARCH_SOFTWARE_VALIDATION',
 'BUTTERFLY':'RESEARCH_TOOLCHAIN_VALIDATION',
 'COMPUTATIONAL-DIFFICULTY-ATLAS':'MATHEMATICAL_PUBLICATION_AND_EDITORIAL',
 'gcl-standards':'GOVERNANCE_STANDARDS_AND_POLICY_TESTS',
 'GCT-EXECUTIVE':'PRIVATE_EXECUTIVE_SOURCE_AND_GOVERNANCE',
 'GLOSS':'FORMAL_SOFTWARE_LIBRARY',
 'GSD':'RESEARCH_EXPERIMENT_AND_EVALUATOR',
 'lean-action':'REUSABLE_PROOF_BUILD_ACTION',
 'MODULUS':'RESEARCH_SOFTWARE_TESTS',
 'QUANTUM-TECHNOLOGIES':'RESEARCH_SCIENTIFIC_PROGRAMMES',
 'TROVE-CURATA':'EDITORIAL_CURATION_AND_ACCEPTANCE',
 'upload-pages-artifact':'REUSABLE_PUBLICATION_ACTION',
}

def api(url):
    result=subprocess.run(['gh','api',url],capture_output=True,text=True,timeout=35)
    if result.returncode:
        raise ValueError(f'GitHub readback failed for {url}: {result.stderr[:200]}')
    return json.loads(result.stdout)

def main():
    source_path=ROOT/'ESTATE_CONTRACT_SOURCES_20261017.json'
    scope_path=ROOT/'ESTATE_SCOPE_20261017.json'
    source=json.loads(source_path.read_text())
    scope=json.loads(scope_path.read_text())
    pinned={e['repository']:e for e in scope['repositories'] if not e['prior_six_repo_control_sample']}
    assert len(pinned)==14 and len(source['entries'])==14
    assert source['scope_sha256']==hashlib.sha256(scope_path.read_bytes()).hexdigest()
    rows=[]
    for entry in source['entries']:
        repo=entry['repository']; name=repo.split('/')[-1]
        assert repo in pinned and entry['head']==pinned[repo]['head_sha']
        assert entry['status']=='PINNED_SOURCE_ONLY_NOT_ENFORCEMENT'
        branch=api(f'repos/{repo}/branches/{pinned[repo]["default_branch"]}')
        effective=api(f'repos/{repo}/rules/branches/{pinned[repo]["default_branch"]}')
        workflows=api(f'repos/{repo}/actions/workflows?per_page=100')
        active={w['path']:w for w in workflows.get('workflows',[]) if w.get('state')=='active'}
        legacy=None
        if branch['protected'] is True and not effective:
            legacy=api(f'repos/{repo}/branches/{pinned[repo]["default_branch"]}/protection')
        mapped=entry.get('workflows',[])
        paths={x['path'] for x in mapped}
        assert len(paths)==len(mapped)
        jobs=[{'workflow_path':w['path'], 'pinned_blob_sha':w['blob'],
            'job_ids':w['job_ids'], 'dispatch_events':list(w['events'] or {}),
            'observed_live_active':w['path'] in active}
            for w in mapped]
        required=[]
        for rule in effective:
            if rule['type']=='required_status_checks':
                required += [c['context'] for c in rule.get('parameters',{}).get('required_status_checks',[])]
        types=sorted(set(rule['type'] for rule in effective))
        if legacy is not None:
            if legacy.get('required_pull_request_reviews') is not None:
                types.append('pull_request')
            if legacy.get('required_status_checks') is not None:
                types.append('required_status_checks')
                required += legacy['required_status_checks'].get('contexts',[])
            if legacy.get('allow_force_pushes',{}).get('enabled') is False:
                types.append('non_fast_forward')
            types=sorted(set(types))
        state='PROTECTED_WITH_PR_AND_REQUIRED_CI' if (
            branch['protected'] and 'pull_request' in types and bool(required)) else (
            'PROTECTED_WITH_PR_NO_REQUIRED_CI' if branch['protected'] and 'pull_request' in types else
            'NO_EFFECTIVE_PR_BRANCH_PROTECTION')
        rows.append({'repository':repo,'assertion_class':CLASSES[name],
           'scope_pinned_main_sha':entry['head'],
           'observed_current_main_sha':branch['commit']['sha'],
           'current_main_equals_pinned':branch['commit']['sha']==entry['head'],
           'source_inventory':{'governance_count':entry['counts']['governance'],
             'tests_count':entry['counts']['tests'],
             'workflow_count':entry['counts']['workflows'],
             'source_governance_blobs':entry.get('governance_sources',[]),
             'source_test_blobs':entry.get('test_sources',[])},
           'controller_consumer_routes':jobs,
           'branch_enforcement':{'protected':branch['protected'],
             'mechanism':'LEGACY_BRANCH_PROTECTION' if legacy is not None else 'GITHUB_RULESETS',
             'effective_rule_types':types,'required_status_contexts':sorted(set(required)),
             'observed_class':state},
           'source_map_state':'PINNED_PRODUCER_AND_WORKFLOW_CONSUMER_IDENTIFIED',
           'specific_job_success_at_pinned_sha':'NOT_VERIFIED_IN_THIS_MAP',
           'independent_specialist_semantic_review':'NOT_VERIFIED_IN_THIS_MAP',
           'public_mirror_accuracy':'NOT_VERIFIED_IN_THIS_MAP',
           'end_to_end_claim_admission':'NOT_VERIFIED_IN_THIS_MAP',
           'private_content_fully_inspected':not entry['private']})
        print(name,state,'sampled workflows',len(mapped),flush=True)
    assert {r['repository'] for r in rows}==set(pinned)
    result={'record_type':'GCL_PAAR_001_FOURTEEN_REPOSITORY_CONTROL_MAPPING/1',
      'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'source_map_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),
      'pinned_scope_sha256':hashlib.sha256(scope_path.read_bytes()).hexdigest(),
      'scope':'14 repositories outside original 6-repository sample',
      'count':len(rows), 'entries':rows,
      'branch_control_readbacks':sum(r['branch_enforcement']['protected'] for r in rows),
      'known_workflow_routes':sum(len(r['controller_consumer_routes']) for r in rows),
      'semantic_enforcement_established':False,
      'scientific_or_gcl_wide_assurance_certified':False}
    path=ROOT/'ESTATE_CONTROL_MAPPING_14_20261017.json'
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':str(path),'repos':len(rows),
      'required_ci_repos':[r['repository'] for r in rows if r['branch_enforcement']['required_status_contexts']],
      'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))

if __name__=='__main__':main()
