#!/usr/bin/env python3
"""Conservative change router for optional GCL synthetic assurance pilots.

Required GCL conformance policy and security checks are never routed here.
Schedules/manual dispatch run both; missing or malformed event/diff runs both.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

SHA40 = re.compile(r'[0-9a-f]{40}\Z')
SHARED = frozenset({
    '.github/workflows/gcl-conformance.yml',
    'ci/workflow_conformance_pilot_impact.py',
    'ci/test_workflow_conformance_pilot_impact.py',
    'requirements/policy.txt',
})
ASSURANCE_FILES = frozenset({'ci/assure_pr.py', 'tests/test_assurance_product.py'})
DISCLOSURE_FILES = frozenset({'ci/disclose_pr.py', 'tests/test_disclosure_gate.py'})


def classify(paths: list[str] | None) -> tuple[bool, bool, str]:
    if paths is None:
        return True, True, 'UNKNOWN_DIFF_RUN_BOTH'
    for path in paths:
        if not path or path.startswith('/') or '..' in path.split('/'):
            return True, True, 'UNSAFE_PATH_RUN_BOTH'
    shared = any(p in SHARED for p in paths)
    assurance = shared or any(p in ASSURANCE_FILES or p.startswith('assurance/') for p in paths)
    disclosure = shared or any(p in DISCLOSURE_FILES or p.startswith('disclosure/') for p in paths)
    return assurance, disclosure, 'EXACT_PATH_IMPACT'


def event_range(event_name: str, event: dict) -> tuple[str, str] | None:
    if event_name == 'pull_request':
        pr = event['pull_request']
        base, head = pr['base']['sha'], pr['head']['sha']
    elif event_name == 'merge_group':
        group = event['merge_group']
        base, head = group['base_sha'], group['head_sha']
    elif event_name == 'push':
        base, head = event['before'], event['after']
    else:
        return None
    if not isinstance(base, str) or not isinstance(head, str):
        return None
    if not SHA40.fullmatch(base) or not SHA40.fullmatch(head) or base == '0' * 40:
        return None
    return base, head


def diff_paths(base: str, head: str) -> list[str] | None:
    result = subprocess.run(['git', 'diff', '--name-only', '-z', base, head, '--'],
                            capture_output=True, timeout=25)
    if result.returncode:
        return None
    try:
        return [x.decode('utf-8') for x in result.stdout.split(b'\0') if x]
    except UnicodeDecodeError:
        return None


def plan(event_name: str, event: dict) -> tuple[bool, bool, str]:
    if event_name in ('schedule', 'workflow_dispatch'):
        return True, True, 'EXPLICIT_FULL_PILOT_REPLAY'
    try:
        commits = event_range(event_name, event)
    except (KeyError, TypeError):
        commits = None
    if not commits:
        return True, True, 'INVALID_EVENT_RANGE_RUN_BOTH'
    return classify(diff_paths(*commits))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--event-name', default=os.environ.get('GITHUB_EVENT_NAME', ''))
    parser.add_argument('--event-path', default=os.environ.get('GITHUB_EVENT_PATH', ''))
    parser.add_argument('--github-output', default=os.environ.get('GITHUB_OUTPUT', ''))
    args = parser.parse_args()
    try:
        event = json.loads(Path(args.event_path).read_text())
        assure, disclose, reason = plan(args.event_name, event)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        assure, disclose, reason = True, True, 'EVIDENCE_READ_ERROR_RUN_BOTH'
    if args.github_output:
        with Path(args.github_output).open('a') as f:
            f.write(f'assurance={str(assure).lower()}\n')
            f.write(f'disclosure={str(disclose).lower()}\n')
    print(json.dumps({'assurance': assure, 'disclosure': disclose, 'reason': reason}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
