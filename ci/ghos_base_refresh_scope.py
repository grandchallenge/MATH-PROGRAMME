#!/usr/bin/env python3
"""NOT ACTIVE: content-addressed fail-open GH-OS base-refresh proof."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess

SHA = re.compile(r"^[a-f0-9]{40}$")
CONTROL_INPUTS = (
    '.github/workflows', '.ghos-routing', 'requirements/policy.txt',
    'AGENTS.md', 'docs/governance/GHOS_ROUTING_CONTROL_RUNBOOK.md',
    'ci/ghos_execution_routing.py', 'ci/ghos_base_refresh_scope.py',
    'tests/test_ghos_base_refresh_scope.py', 'schemas/ghos_execution_routing.schema.json',
    'tests/test_ghos_execution_routing.py', 'ci/validate_workflow_coverage_v3.py',
    'governance/policy_shard_registry.json',
)

def git(root: Path, *args: str) -> str:
    r = subprocess.run(['git', *args], cwd=root, text=True, capture_output=True, timeout=12)
    if r.returncode:
        raise ValueError('unavailable exact Git identity')
    return r.stdout.strip()

def classify(root: Path, before: str, after: str, current: str) -> dict:
    result = {'record_type':'GHOS_BASE_REFRESH_EFFECTIVE_INPUT_PROOF/1',
              'before':before,'after':after,'current':current,
              'refresh':True,'reason':'FAIL_OPEN_UNVERIFIED_IDENTITY','changed_control_inputs':[]}
    try:
        if any(not SHA.fullmatch(s) for s in (before, after, current)):
            raise ValueError('invalid identity')
        if before == '0'*40 or before == after or after != current:
            raise ValueError('ambiguous protected push')
        if git(root,'rev-parse','HEAD') != current:
            raise ValueError('current checkout not event SHA')
        git(root,'cat-file','-e',before+'^{commit}')
        git(root,'cat-file','-e',after+'^{commit}')
        git(root,'merge-base','--is-ancestor',before,after)
        # No unchanged symlink may observe bytes *outside* the compared tree.
        # Reject rather than assume an unchanged link target means equal input.
        for revision in (before,after):
            trees = git(root,'ls-tree','-r',revision,'.github/workflows','.ghos-routing')
            for row in trees.splitlines():
                if row.startswith('120000 '):
                    raise ValueError('symlink in GHOS control tree')
            for path in CONTROL_INPUTS:
                if path in ('.github/workflows','.ghos-routing'):
                    continue
                entry=git(root,'ls-tree',revision,'--',path)
                if not entry or not entry.startswith(('100644 ','100755 ')):
                    raise ValueError('missing or symlinked protected input')
        changes = [p for p in CONTROL_INPUTS if git(root,'rev-parse',before+':'+p) !=
                   git(root,'rev-parse',after+':'+p)]
        result['changed_control_inputs'] = changes
        result['refresh'] = bool(changes)
        result['reason'] = 'CONTROL_INPUTS_CHANGED' if changes else 'CONTROL_INPUT_BYTES_IDENTICAL'
    except (OSError,ValueError,subprocess.TimeoutExpired):
        pass  # Missing evidence never authorizes suppression.
    return result

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path.cwd())
    for name in ('before','after','current'):
        parser.add_argument('--'+name,required=True)
    parser.add_argument('--github-output')
    args=parser.parse_args()
    result=classify(args.root,args.before,args.after,args.current)
    print(json.dumps(result,sort_keys=True))
    if args.github_output:
        with Path(args.github_output).open('a') as handle:
            handle.write('refresh='+str(result['refresh']).lower()+'\n')
            handle.write('reason='+result['reason']+'\n')
    return 0

if __name__=='__main__':raise SystemExit(main())
