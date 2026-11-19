#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
case "$(lean --version)" in
  *'Lean (version 4.33.0-rc1'*'62eed1db4d67327ec8120be05f1a1b0847d74561'*) ;;
  *) echo 'ERROR: wrong Lean version' >&2; exit 21;;
esac
if grep -nE '^[[:space:]]*(sorry|admit|axiom)[[:space:]]' Erdos561GraphHandshake.lean Erdos561FourVertexCore.lean Erdos561FactorCut.lean; then
  echo 'ERROR: proof placeholder' >&2; exit 22
fi
lean Erdos561GraphHandshake.lean
lean Erdos561FourVertexCore.lean
lean Erdos561FactorCut.lean
echo 'LEAN_GRAPH_TRANCHE_PASS: graph and numeric Lovasz cut prerequisites only'
