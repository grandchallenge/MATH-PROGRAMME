#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
version="$(lean --version)"
case "$version" in
  *'Lean (version 4.33.0-rc1'*'62eed1db4d67327ec8120be05f1a1b0847d74561'*) ;;
  *) echo "ERROR: expected pinned Lean 4.33.0-rc1 / 62eed1db, got: $version" >&2; exit 21;;
esac
if grep -nE '^[[:space:]]*(sorry|admit|axiom)[[:space:]]' Erdos561Finite.lean Erdos561CoreArithmetic.lean; then
  echo 'ERROR: forbidden proof placeholders' >&2; exit 22
fi
lean Erdos561CoreArithmetic.lean | tee core_lean_result.txt
lean Erdos561Finite.lean | tee finite_lean_result.txt
echo 'LEAN_CHECKED: 4 core arithmetic lemmas and 5 finite parameter statements'
