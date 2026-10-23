#!/usr/bin/env python3
"""Independent GitHub-hosted missed-run detector; no scheduler API or repair authority."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HEADER = 'GCL-SCHEDULER-RUN/1'
ALERT_HEADER = 'GCL-SCHEDULER-OUTAGE/1'
ALLOWED = {'SUCCEEDED', 'PARTIAL', 'BLOCKED', 'SAFETY_DENIAL', 'PERMISSION_ERROR', 'TRANSIENT_ERROR', 'NO_ELIGIBLE_WORK'}

def iso(value):
    if not isinstance(value, str) or not value:
        raise ValueError('not an ISO date')
    t = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if t.tzinfo is None: raise ValueError('timezone required')
    return t.astimezone(timezone.utc)

def fields(body, header):
    if not isinstance(body, str) or not body.startswith(header + '\n'): return None
    lines = body.strip().splitlines()
    out = {}
    for line in lines[1:]:
        if ': ' not in line: return None
        name, value = line.split(': ', 1)
        if not name or not value or name in out: return None
        out[name] = value
    return out

def evaluate(policy, comments, now):
    now = iso(now) if isinstance(now, str) else now
    if policy.get('desired_state') != 'ENABLED' or policy.get('cadence') != 'HOURLY':
        return {'state':'CONTRACT_NOT_ENABLED','reason':'protected desired state is not enabled'}
    issue = policy['heartbeat_issue']
    actors = set(policy['heartbeat_authorized_actors'])
    accepted=[];ignored=0;recovery_only=0
    for c in comments:
        f=fields(c.get('body'), HEADER)
        if f is None:continue
        try:
            posted = iso(c['createdAt']);reported=iso(f['RUN_AT_UTC'])
            valid=((c.get('author') or {}).get('login') in actors and f.get('TASK_KEY')==policy['task_key']
                   and f.get('OUTCOME') in ALLOWED and bool(f.get('NEXT_ACTION'))
                   and abs((posted-reported).total_seconds())<=1200
                   and posted<=now and posted>=iso(policy['heartbeat_activation_utc']))
        except (KeyError, ValueError, TypeError):valid=False
        if valid and f.get('RECOVERY_MODE'):\n            recovery_only+=1\n            continue\n        if valid:accepted.append((posted,c))
        else:ignored+=1
    accepted.sort(key=lambda row:row[0])
    last_time = accepted[-1][0] if accepted else iso(policy['heartbeat_activation_utc'])
    age_minutes=round((now-last_time).total_seconds()/60,3)
    episode='after-'+str(accepted[-1][1]['databaseId']) if accepted else 'since-activation'
    state='ALERT_MISSED_HEARTBEAT' if age_minutes>policy['heartbeat_grace_minutes'] else ('HEALTHY_HEARTBEAT' if accepted else 'AWAITING_FIRST_HEARTBEAT')
    return {'state':state,'task_key':policy['task_key'],'issue':issue,'now_utc':now.isoformat(),
            'last_valid_utc':last_time.isoformat(),'last_valid_comment':accepted[-1][1]['url'] if accepted else None,
            'age_minutes':age_minutes,'valid_count_in_window':len(accepted),'rejected_marker_count':ignored,'retrospective_recovery_count':recovery_only,
            'episode_id':hashlib.sha256((policy['task_key']+'|'+episode).encode()).hexdigest()[:24],
            'authority_boundary':'OBSERVATION_ONLY_NO_CHATGPT_SCHEDULER_API'}

def gh(args):
    p = subprocess.run(['gh','api',*args],text=True,capture_output=True,timeout=30)
    if p.returncode:raise RuntimeError('GitHub API failure: '+p.stderr[:500])
    return json.loads(p.stdout)

def recent_comments():
    q='query { repository(owner:"grandchallenge",name:"MATH-PROGRAMME") { issue(number:2763) { comments(last:100) { nodes { databaseId author { login } body createdAt url } } } } }'
    data=gh(['graphql','-f','query='+q])
    return data['data']['repository']['issue']['comments']['nodes']


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--policy',default='governance/recurring_queue_continuity.json')
    p.add_argument('--output')
    p.add_argument('--now')
    p.add_argument('--fixture-comments')
    a=p.parse_args()
    policy=json.loads(Path(a.policy).read_text())
    observations=json.loads(Path(a.fixture_comments).read_text()) if a.fixture_comments else recent_comments()
    now=a.now or datetime.now(timezone.utc).isoformat()
    result=evaluate(policy,observations,now)
    payload=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.output:Path(a.output).write_text(payload)
    sys.stdout.write(payload)
    return 1 if result['state'] in ('ALERT_MISSED_HEARTBEAT','CONTRACT_NOT_ENABLED') else 0
if __name__=='__main__':raise SystemExit(main())
