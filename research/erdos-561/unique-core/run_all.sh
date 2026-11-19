#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
case "$(lean --version)" in
  *'Lean (version 4.33.0-rc1'*'62eed1db4d67327ec8120be05f1a1b0847d74561'*) ;;
  *) echo 'ERROR: Lean version mismatch' >&2; exit 21;;
esac
if grep -nE '^[[:space:]]*(sorry|admit|axiom)[[:space:]]' Erdos561UniqueLargeCore.lean; then
  echo 'ERROR: proof placeholder' >&2; exit 22
fi
lean Erdos561UniqueLargeCore.lean
exe="$(mktemp /tmp/gcl-erdos561-general-XXXXXX)"
trap 'rm -f "$exe"' EXIT
c++ -std=c++17 -O2 -Wall -Wextra -Werror -o "$exe" verify_general_core.cpp
actual="$("$exe")"
expected='PASS {graphs:33866,cap_instances:91727,obstructions:273,exact_lovasz_comparisons:2809,general_cases:91657,general_obstructions:263}'
[ "$actual" = "$expected" ] || { printf '%s\n' "$actual"; echo 'FAIL graph corpus changed'; exit 23; }
python3 verify_parameter_gate.py
python3 verify_independent_gate.py
printf '%s\n' "$actual"
echo 'REPLAY_PASS: kernel arithmetic, graph obstructions, exact 249/90 parameter certificate'
