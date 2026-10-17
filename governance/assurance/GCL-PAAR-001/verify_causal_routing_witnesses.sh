#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
while IFS=$'\t' read -r name pr sha run wf; do
  [[ "$name" == repo ]] && continue
  repo="grandchallenge/$name"
  [[ "$(gh pr view "$pr" -R "$repo" --json headRefOid --jq .headRefOid)" == "$sha" ]]
  [[ "$(gh run view "$run" -R "$repo" --json headSha --jq .headSha)" == "$sha" ]]
  [[ "$(gh run view "$run" -R "$repo" --json conclusion --jq .conclusion)" == failure ]]
  log="$(gh run view "$run" -R "$repo" --log-failed)"
  [[ "$log" == *'RoutingGateError: workflow routing coverage mismatch'* ]]
  tree="$(gh api "repos/$repo/git/trees/$sha?recursive=1")"
  [[ "$(jq -r .truncated <<< "$tree")" == false ]]
  jq -e --arg p ".github/workflows/$wf" '.tree[]|select(.type=="blob" and .path==$p)' <<< "$tree" >/dev/null
  registry="$(gh api "repos/$repo/contents/.ghos-routing/workflows.json?ref=$sha" --jq .content | base64 -d)"
  ! jq -e --arg p ".github/workflows/$wf" '.workflows[]|select(.path==$p)' <<< "$registry" >/dev/null
  echo "$repo #$pr: PASS_BOUNDED_ROUTING_REJECTION"
done < CAUSAL_ROUTING_CASES_20261017.tsv
