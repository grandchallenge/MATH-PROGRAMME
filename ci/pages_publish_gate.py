#!/usr/bin/env python3
"""Conservative Pages source-change gate; never replaces artifact validation."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import urllib.request

# Source dependency audit: mkdocs.yml loads the two compendium hooks; each
# reads precisely the source paths listed below. Batch/queue/review receipts
# are *not* site inputs until admitted into the editorial source records.
SITE_PREFIXES = (
    'docs/',
    'governance/erdos_compendium/editorial/',
    'governance/erdos_compendium/EDITORIAL_',
    'governance/oai26_documentary/editorial/',
)
SITE_FILES = frozenset({
    'mkdocs.yml', 'requirements/docs.txt', 'requirements/policy.txt',
    'governance/erdos_catalogue/REGISTRY.json',
    'governance/oai26_documentary/FAMILY_CATALOGUE.json',
    'governance/oai26_documentary/EDITORIAL_ADMISSIONS.json',
    'ci/erdos_compendium.py', 'ci/erdos_compendium_hook.py',
    'ci/oai26_compendium.py', 'ci/oai26_compendium_hook.py',
})


def site_source(path: str) -> bool:
    if not path or path.startswith('/') or '..' in path.split('/'):
        return True
    return path in SITE_FILES or any(path.startswith(x) for x in SITE_PREFIXES)


def decision(previous: str | None, current: str, paths: list[str] | None):
    if previous is None:
        return True, 'NO_VERIFIED_PRIOR_DEPLOYMENT'
    if paths is None:
        return True, 'DIFF_UNVERIFIED_PUBLISH'
    relevant = sorted(x for x in paths if site_source(x))
    if relevant:
        return True, 'SITE_INPUT_CHANGED:' + ','.join(relevant[:7])
    return False, 'SITE_INPUTS_UNCHANGED'


def latest_deployed(repository: str, token: str) -> str | None:
    def get(url):
        req = urllib.request.Request(url, headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + token,
            'X-GitHub-Api-Version': '2022-11-28'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.load(response)
    root = f'https://api.github.com/repos/{repository}/deployments'
    entries = get(root + '?environment=github-pages&per_page=10')
    if not isinstance(entries, list):
        raise ValueError('malformed deployments')
    for row in entries:
        if not isinstance(row.get('id'), int):
            raise ValueError('malformed deployment ID')
        statuses = get(root + f"/{row['id']}/statuses?per_page=1")
        if not isinstance(statuses, list):
            raise ValueError('malformed deployment statuses')
        if statuses and statuses[0].get('state') == 'success':
            sha = row.get('sha')
            if not isinstance(sha, str) or len(sha) != 40:
                raise ValueError('invalid deployed SHA')
            return sha
    return None


def compared_paths(repository: str, token: str, previous: str, current: str) -> list[str] | None:
    """REST compare, fail open on divergence or GitHub's 300-file cap."""
    if previous == current:
        return []
    url = f'https://api.github.com/repos/{repository}/compare/{previous}...{current}'
    request = urllib.request.Request(url, headers={
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + token,
        'X-GitHub-Api-Version': '2022-11-28'})
    with urllib.request.urlopen(request, timeout=25) as response:
        result = json.load(response)
    if result.get('status') != 'ahead':
        return None
    files = result.get('files')
    if not isinstance(files, list) or len(files) >= 300:
        return None
    paths = []
    for row in files:
        name = row.get('filename')
        if not isinstance(name, str):
            return None
        paths.append(name)
        if row.get('previous_filename'):
            paths.append(row['previous_filename'])
    return paths


def run(repository: str, current: str, token: str):
    try:
        previous = latest_deployed(repository, token)
        if previous is None:
            return True, 'NO_RECENT_SUCCESSFUL_PAGES_DEPLOYMENT'
        return decision(previous, current, compared_paths(repository, token, previous, current))
    except (OSError, ValueError) as exc:
        return True, 'DEPLOYMENT_EVIDENCE_UNAVAILABLE:' + type(exc).__name__


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--github-output', required=True)
    args = parser.parse_args()
    publish, reason = run(args.repository, args.head, os.environ['GH_TOKEN'])
    with Path(args.github_output).open('a') as output:
        output.write('publish=' + str(publish).lower() + '\n')
        output.write('reason=' + reason + '\n')
    print('GCL_PAGES_PUBLISH_DECISION', json.dumps({'publish': publish, 'reason': reason}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
