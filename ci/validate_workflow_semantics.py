#!/usr/bin/env python3
"""Validate semantic workflow identity, dependency, runner, execution, and publication contracts."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
from typing import Any
import yaml
ROOT=Path(__file__).resolve().parents[1]
EXPECTED_NAMES={'bsd-wp03-substrate.yml':'BSD WP03 substrate replay','bsd-wp04-target.yml':'BSD WP04 target scorecard','ci.yml':'Programme policy checks','pages.yml':'Deploy documentation site','pc-wp04.yml':'PC-WP04 certificate checks','pc-wp05.yml':'PC-WP05 archival checks'}
PYTHON_MINOR_LINE='3.12';POLICY_REQUIREMENTS=('jsonschema==4.26.0','PyYAML==6.0.3');DOCS_REQUIREMENTS=('mkdocs==1.6.1','mkdocs-material==9.7.7','pymdown-extensions==11.0.1','PyYAML==6.0.3');POLICY_INSTALL='python -m pip install --requirement requirements/policy.txt';DOCS_INSTALL='python -m pip install --requirement requirements/docs.txt';EXTERNAL_POLICY_INSTALL='python -m pip install --requirement "$GITHUB_WORKSPACE/requirements/policy.txt"';PINNED_REUSABLE_WORKFLOW=re.compile(r'^[^@\s]+/\.github/workflows/[^@\s]+@[0-9a-f]{40}$');LOCAL_REUSABLE_WORKFLOW=re.compile(r'^\./\.github/workflows/[^@\s]+[.]ya?ml$');SHARDS=('core','fixtures','cmdg','administrative','campaigns','contracts','docs')
def load_workflows(root:Path=ROOT)->dict[str,dict[str,Any]]:
    out={}
    for p in sorted((root/'.github/workflows').glob('*.y*ml')):
        v=yaml.load(p.read_text(encoding='utf-8'),Loader=yaml.BaseLoader);out[p.name]=v if isinstance(v,dict) else {}
    return out
def job_runs(w:dict,j:str)->list[str]:return [str(s.get('run','')) for s in w.get('jobs',{}).get(j,{}).get('steps',[]) if s.get('run')]
def all_runs(w:dict)->list[str]:return [str(s.get('run','')) for j in w.get('jobs',{}).values() for s in j.get('steps',[]) if s.get('run')]
def lines(runs:list[str])->set[str]:return {x.strip() for r in runs for x in r.splitlines() if x.strip() and not x.lstrip().startswith('#')}
def contains_command(runs:list[str],cmd:str)->bool:return cmd in lines(runs)
def marker(runs:list[str],m:str)->bool:return any(m in x for x in lines(runs))
def steps_using(job:dict,prefix:str)->list[dict]:return [s for s in job.get('steps',[]) if str(s.get('uses','')).startswith(prefix)]
def req(root:Path,rel:str)->tuple[str,...]:
    p=root/rel
    return tuple(x.strip() for x in p.read_text(encoding='utf-8').splitlines() if x.strip() and not x.lstrip().startswith('#')) if p.is_file() else ()
def registry_commands(root:Path)->set[str]:
    p=root/'governance/policy_shard_registry.json'
    if not p.is_file():return set()
    data=json.loads(p.read_text(encoding='utf-8'));return {' '.join(str(x) for x in cmd) for cmds in data.get('shards',{}).values() for cmd in cmds if isinstance(cmd,list) and cmd}
def needs(job:dict)->set[str]:
    v=job.get('needs',[]);return {str(x) for x in v} if isinstance(v,list) else ({str(v)} if v else set())
def workflow_semantic_errors(root:Path=ROOT,workflows:dict[str,dict[str,Any]]|None=None)->list[str]:
    e=[];workflows=load_workflows(root) if workflows is None else workflows;names=[]
    for f,expected in EXPECTED_NAMES.items():
        actual=str(workflows.get(f,{}).get('name',''));names.append(actual)
        if actual!=expected:e.append(f'{f}: workflow name must be exactly {expected!r}, found {actual!r}')
    for n in sorted({n for n in names if n and names.count(n)>1}):e.append(f'workflow names must be unique; duplicate {n!r}')
    setups=0
    for f,w in workflows.items():
        for jid,j in w.get('jobs',{}).items():
            reusable=str(j.get('uses',''))
            if reusable:
                if not (LOCAL_REUSABLE_WORKFLOW.fullmatch(reusable) or PINNED_REUSABLE_WORKFLOW.fullmatch(reusable)):e.append(f'{f}:{jid}: reusable workflow must be same-repository local or use a full commit SHA')
                continue
            if str(j.get('runs-on',''))!='ubuntu-24.04':e.append(f'{f}:{jid}: runs-on must be pinned to ubuntu-24.04')
            for s in j.get('steps',[]):
                if str(s.get('uses','')).startswith('actions/setup-python@'):
                    setups+=1
                    if str(s.get('with',{}).get('python-version',''))!=PYTHON_MINOR_LINE:e.append(f'{f}:{jid}: setup-python must use governed minor line {PYTHON_MINOR_LINE!r}')
        for line in lines(all_runs(w)):
            if 'pip install' in line and '--requirement' not in line:e.append(f'{f}: ad hoc or unpinned pip install is forbidden: {line}')
    if not setups:e.append('governed workflows must contain at least one setup-python step')
    if req(root,'requirements/policy.txt')!=POLICY_REQUIREMENTS:e.append('requirements/policy.txt must contain the exact governed policy pins')
    if req(root,'requirements/docs.txt')!=DOCS_REQUIREMENTS:e.append('requirements/docs.txt must contain the exact governed documentation pins')
    policy=workflows.get('ci.yml',{});triggers=policy.get('on',{});schedules=str(triggers.get('schedule','')) if isinstance(triggers,dict) else ''
    for cron in ('17 */6 * * *','43 8 * * *'):
        if cron not in schedules:e.append(f'ci.yml: missing protected policy sentinel cron {cron}')
    impact=policy.get('jobs',{}).get('impact',{})
    if not marker(job_runs(policy,'impact'),'ci/policy_impact.py classify'):e.append('ci.yml:impact must execute the fail-closed policy impact classifier')
    co=steps_using(impact,'actions/checkout@')
    if len(co)!=1 or str(co[0].get('with',{}).get('fetch-depth',''))!='0':e.append('ci.yml:impact must use one full-history checkout for exact transition diffing')
    shard=policy.get('jobs',{}).get('policy-shard',{});matrix=shard.get('strategy',{}).get('matrix',{}).get('shard',[])
    if tuple(str(x) for x in matrix)!=SHARDS:e.append('ci.yml:policy-shard matrix must enumerate every governed shard exactly once')
    sr=job_runs(policy,'policy-shard')
    if not contains_command(sr,POLICY_INSTALL):e.append('ci.yml:policy-shard is missing governed policy dependency command')
    if not contains_command(sr,DOCS_INSTALL):e.append('ci.yml:policy-shard is missing governed docs dependency command')
    if not marker(sr,'ci/run_policy_shard.py --shard'):e.append('ci.yml:policy-shard must execute the governed shard registry runner')
    if not marker(sr,'VERIFIED_POLICY_SHARD_NO_OP'):e.append('ci.yml:policy-shard must make irrelevant shard no-op explicit')
    reg=registry_commands(root)
    for cmd in ('python -m unittest discover -s tests -p test_*.py','python3 ci/validate_policy_reachability.py','python3 ci/test_policy_reachability.py','python3 ci/validate_repository_execution.py','python3 ci/test_repository_execution.py','python3 ci/validate_workflow_semantics.py','python3 ci/test_workflow_semantics.py','mkdocs build --strict'):
        if cmd not in reg:e.append(f'governed shard registry is missing executable coverage command {cmd}')
    agg=policy.get('jobs',{}).get('validate-json',{})
    if not {'impact','policy-shard'}.issubset(needs(agg)):e.append('ci.yml:validate-json must aggregate impact and policy-shard')
    if 'always()' not in str(agg.get('if','')):e.append('ci.yml:validate-json must run under always() to fail closed on upstream results')
    ar=job_runs(policy,'validate-json')
    for m in ('needs.impact.result','needs.policy-shard.result'):
        if not marker(ar,m):e.append(f'ci.yml:validate-json aggregator is missing result gate {m}')
    uploads=[s for j in policy.get('jobs',{}).values() for s in steps_using(j,'actions/upload-artifact@')];sites=[s for s in uploads if s.get('with',{}).get('name')=='validated-site']
    if len(sites)!=1:e.append('ci.yml must upload exactly one validated-site artifact')
    else:
        s=sites[0];cond=str(s.get('if',''))
        for m in ("matrix.shard == 'docs'","github.event_name == 'push'","github.ref == 'refs/heads/main'"):
            if m not in cond:e.append(f'ci.yml: validated-site upload condition is missing {m}')
        if str(s.get('with',{}).get('retention-days',''))!='1':e.append('ci.yml: validated-site artifact retention must be exactly one day')
    for m in ('tar --sort=name','sha256sum validated-site.tar.gz','git show -s --format=%ct HEAD'):
        if not marker(sr,m):e.append(f'ci.yml: missing deterministic validated-site packaging marker {m}')
    for jid,lane in {'log-gcd-lean':'log-gcd','pc-wp04-lean':'pc-wp04','union-closed-mathcert':'union-closed-mathcert'}.items():
        j=policy.get('jobs',{}).get(jid,{});runs=job_runs(policy,jid)
        if 'impact' not in needs(j):e.append(f'ci.yml:{jid} must depend on impact classification')
        for m in (f'formal_replay_attestation.py digest --lane {lane}',f'formal_replay_gate.py decide --lane {lane}','--mode "${MODE}"'):
            if not marker(runs,m):e.append(f'ci.yml:{jid} missing formal replay impact-gate marker {m}')
        if not marker(runs,'formal_replay_gate.py emit-receipt'):e.append(f'ci.yml:{jid} must emit protected replay receipts through the schedule-aware gate')
    if not contains_command(job_runs(policy,'pc-wp04-lean'),POLICY_INSTALL):e.append('ci.yml:pc-wp04-lean must install requirements/policy.txt')
    if not contains_command(job_runs(policy,'union-closed-mathcert'),EXTERNAL_POLICY_INSTALL):e.append('ci.yml:union-closed-mathcert must install the root policy requirements by absolute workspace path')
    if not marker(job_runs(policy,'log-gcd-lean'),'lake build'):e.append('ci.yml:log-gcd-lean must retain full Lean replay path')
    if not marker(job_runs(policy,'pc-wp04-lean'),'lake build'):e.append('ci.yml:pc-wp04-lean must retain full Lean replay path')
    if not marker(job_runs(policy,'union-closed-mathcert'),'bash ci/check_lean.sh'):e.append('ci.yml:union-closed-mathcert must retain pinned external replay path')
    if not contains_command(job_runs(workflows.get('pc-wp04.yml',{}),'pc-wp04-lean'),POLICY_INSTALL):e.append('pc-wp04.yml must install requirements/policy.txt')
    if not contains_command(job_runs(workflows.get('pc-wp05.yml',{}),'archival-policy'),POLICY_INSTALL):e.append('pc-wp05.yml archival policy must install requirements/policy.txt')
    pages=workflows.get('pages.yml',{});con=pages.get('concurrency',{})
    if str(con.get('cancel-in-progress','')).lower()!='true':e.append('pages.yml: concurrency must cancel stale in-progress publications')
    build=pages.get('jobs',{}).get('build',{});bif=str(build.get('if',''))
    for clause in ("github.event.workflow_run.conclusion == 'success'","github.event.workflow_run.head_branch == 'main'","github.event.workflow_run.event == 'push'"):
        if clause not in bif:e.append(f'pages.yml: build.if is missing semantic gate {clause}')
    checkout=steps_using(build,'actions/checkout@')
    if len(checkout)!=1:e.append('pages.yml: build must contain exactly one checkout step')
    elif checkout[0].get('with',{}).get('ref')!='${{ github.event.workflow_run.head_sha }}':e.append('pages.yml: checkout must use the validated workflow_run.head_sha')
    br=job_runs(pages,'build')
    if contains_command(br,DOCS_INSTALL) or contains_command(br,'mkdocs build --strict'):e.append('pages.yml: Pages must deploy the policy artifact without resolving dependencies or rebuilding MkDocs')
    for m in ('refs/heads/main:refs/remotes/origin/main','git rev-parse HEAD','git rev-parse refs/remotes/origin/main','actions/runs/{run_id}/artifacts','artifact.get("name") == "validated-site"','hashlib.sha256(artifact_zip)','hashlib.sha256(archive_path.read_bytes())','archive.extractall(site, filter="data")'):
        if not marker(br,m):e.append(f'pages.yml: missing exact-artifact publication check {m}')
    deploy=pages.get('jobs',{}).get('deploy',{});env=deploy.get('environment',{})
    if str(env.get('url',''))!='${{ steps.deployment.outputs.page_url }}':e.append('pages.yml: deploy environment must expose the deploy-pages page_url output')
    ds=steps_using(deploy,'actions/deploy-pages@')
    if len(ds)!=1 or ds[0].get('id')!='deployment':e.append('pages.yml: deploy-pages step must have id deployment')
    return e
def main()->int:
    errors=workflow_semantic_errors()
    if errors:
        for x in errors:print(x,file=sys.stderr)
        print(f'workflow semantic validation failed with {len(errors)} error(s)',file=sys.stderr);return 1
    print('workflow names, impact routing, formal replay gates, runners, dependencies, exact artifact promotion, and publication freshness are valid');return 0
if __name__=='__main__':raise SystemExit(main())
