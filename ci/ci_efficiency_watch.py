#!/usr/bin/env python3
"""Read-only, bounded weekly CI/Pages/GraphQL efficiency sentinel."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

import workflow_conformance_pilot_impact as impact

BASE = 'https://api.github.com/repos/grandchallenge/MATH-PROGRAMME'
MAX_CALLS = 32

class BudgetExceeded(Exception):
    pass

class Reader:
    def __init__(self, token, maximum=MAX_CALLS):
        self.token, self.maximum, self.calls = token, maximum, 0

    def get(self, path):
        if self.calls >= self.maximum:
            raise BudgetExceeded('REST call budget exhausted')
        self.calls += 1
        url = path if path.startswith('https://') else BASE + path
        req = urllib.request.Request(url, headers={
            'Authorization': 'Bearer ' + self.token,
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'})
        with urllib.request.urlopen(req, timeout=18) as response:
            return json.load(response)

def pilot_outcomes(jobs):
    result = {}
    for key, prefix in [('assurance','GCL ASSURE PR synthetic dossier'),
                        ('disclosure','GCL DISCLOSE PR synthetic release gate')]:
        matched = [j['conclusion'] for j in jobs if j['name'].startswith(prefix)]
        result[key] = matched[0] if len(matched) == 1 else None
    return result

def audit(reader, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    report = {'record_type':'GCL_CI_EFFICIENCY_SENTINEL/1',
              'checked_at_utc': now.isoformat(), 'alerts': [],
              'inconclusive': [], 'observations': [],
              'scope': {'max_rest_calls': reader.maximum, 'graphql_calls': 0,
                        'max_pr_runs': 6, 'max_pages_runs': 12,
                        'max_project_workflow_runs': 100}}
    alerts, gaps, obs = report['alerts'], report['inconclusive'], report['observations']
    try:
        runs = reader.get('/actions/workflows/gcl-conformance.yml/runs?per_page=18')['workflow_runs']
        prs = [r for r in runs if r.get('event') == 'pull_request'
               and r.get('status') == 'completed'
               and r.get('created_at', '') >= '2026-11-16T08:16:23Z'][:6]
        for run in prs:
            info = {'kind':'conformance_pr', 'run_id':run['id'], 'head':run['head_sha']}
            jobs_doc = reader.get(f'/actions/runs/{run["id"]}/jobs?per_page=60')
            if jobs_doc.get('total_count',0) > len(jobs_doc.get('jobs',[])):
                gaps.append({'run':run['id'],'reason':'TRUNCATED_JOBS'})
                continue
            actual = pilot_outcomes(jobs_doc['jobs'])
            info['pilots'] = actual
            matched = reader.get(f'/commits/{run["head_sha"]}/pulls?per_page=10')
            linked = [p for p in matched if p.get('head',{}).get('sha') == run['head_sha']
                      and p.get('base',{}).get('ref') == 'main']
            if len(linked) != 1:
                gaps.append({'run':run['id'],'reason':'PR_IDENTITY_UNVERIFIED'})
                obs.append(info)
                continue
            # Commit-to-PR association omits changed_files: fetch the exact PR.
            pr = reader.get(f'/pulls/{linked[0]["number"]}')
            if pr.get('head',{}).get('sha') != run['head_sha'] or pr.get('base',{}).get('ref') != 'main':
                gaps.append({'run':run['id'],'reason':'PR_HEAD_CHANGED'})
                obs.append(info)
                continue
            if pr.get('changed_files',101) > 100:
                gaps.append({'run':run['id'],'reason':'PR_FILES_OVER_100'})
                obs.append(info)
                continue
            info['pr'] = pr['number']
            files = reader.get(f'/pulls/{pr["number"]}/files?per_page=100')
            if len(files) != pr['changed_files']:
                gaps.append({'run':run['id'],'reason':'PR_FILES_COUNT_DRIFT'})
                obs.append(info)
                continue
            paths = [p for f in files for p in (f['filename'], f.get('previous_filename')) if p]
            expected = impact.classify(paths)[:2]
            info['expected'] = dict(zip(('assurance','disclosure'),expected))
            for key, needed in info['expected'].items():
                if not needed and actual[key] == 'success':
                    alerts.append({'kind':'IRRELEVANT_PILOT_START','run':run['id'],
                                   'pr':pr['number'],'pilot':key})
                if actual[key] is None:
                    gaps.append({'run':run['id'],'reason':'PILOT_JOB_AMBIGUOUS','pilot':key})
            obs.append(info)
        pages = reader.get('/actions/workflows/pages.yml/runs?per_page=12')['workflow_runs']
        report['pages_run_counts'] = {state:sum(p.get('conclusion') == state for p in pages)
                                      for state in ('success','skipped','failure','cancelled')}
        deployments = reader.get('/deployments?environment=github-pages&per_page=12')
        report['deployment_heads'] = [d['sha'] for d in deployments]
        duplicates = sorted({d['sha'] for d in deployments
                             if sum(x['sha'] == d['sha'] for x in deployments) > 1})
        if duplicates:
            gaps.append({'reason':'REPEATED_DEPLOYMENT_SHA_REVIEW','heads':duplicates})
        # Workflow-run counts are a bounded proxy for demand, not proof of
        # GraphQL points spent. GitHub rate_limit is actor/token-scoped.
        projection = reader.get('/actions/workflows/erdos-catalogue-queue-projection.yml/runs?per_page=100')
        project_runs = projection.get('workflow_runs', [])
        if projection.get('total_count', 0) > 100:
            gaps.append({'reason':'PROJECT_WORKFLOW_HISTORY_TRUNCATED',
                         'total_count':projection['total_count']})
        event_counts = {}
        for run in project_runs:
            event = run.get('event', 'unknown')
            event_counts[event] = event_counts.get(event, 0) + 1
        report['project_workflow_recent_runs'] = {
            'sampled':len(project_runs), 'events':event_counts,
            'note':'Last 100 workflow runs, not a time-window rate or GraphQL attribution'}
        if event_counts.get('issue_comment', 0) >= 80:
            gaps.append({'reason':'HIGH_COMMENT_TRIGGER_VOLUME_REVIEW',
                         'sampled_comment_runs':event_counts['issue_comment']})
        limits = reader.get('https://api.github.com/rate_limit')['resources']['graphql']
        report['graphql_budget'] = {k:limits.get(k) for k in ('remaining','limit','reset')}
        remaining, reset = limits.get('remaining'), limits.get('reset')
        if isinstance(remaining,int) and isinstance(reset,int):
            until_reset = reset - int(now.timestamp())
            if remaining < 500 and until_reset > 1800:
                alerts.append({'kind':'GRAPHQL_BUDGET_PRESSURE','remaining':remaining,
                               'seconds_until_reset':until_reset})
    except (BudgetExceeded, OSError, ValueError, KeyError, TypeError,
            urllib.error.URLError) as exc:
        gaps.append({'reason':'EVIDENCE_READ_INCOMPLETE',
                     'error_class':type(exc).__name__,'message':str(exc)[:120]})
    report['rest_requests'] = reader.calls
    report['status'] = ('ALERT' if alerts else 'INCONCLUSIVE' if gaps
                        else 'OBSERVED_NO_ALERT')
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    data=audit(Reader(os.environ['GH_TOKEN']))
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    content=json.dumps(data,indent=2,ensure_ascii=False)+'\n'
    path.write_text(content,encoding='utf-8')
    digest=hashlib.sha256(content.encode()).hexdigest()
    path.with_suffix(path.suffix+'.sha256').write_text(digest+'  '+path.name+'\n')
    print('CI_EFFICIENCY_WATCH',json.dumps({'status':data['status'],
         'rest_requests':data['rest_requests'],'alerts':len(data['alerts']),
         'inconclusive':len(data['inconclusive']),'sha256':digest}))
    return 1 if data['alerts'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
