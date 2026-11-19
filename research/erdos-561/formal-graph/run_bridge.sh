#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exe="$(mktemp /tmp/gcl-erdos561-factor-XXXXXX)"
trap 'rm -f "$exe"' EXIT
c++ -std=c++17 -O2 -Wall -Wextra -Werror -o "$exe" verify_factor_bridge.cpp
result="$("$exe")"
printf '%s\n' "$result"
expected='PASS {graphs:33866,cap_instances:91727,obstructions:273,exact_lovasz_comparisons:2809}'
if [ "$result" != "$expected" ]; then
  echo 'ERROR: the exact factor/capped-colouring verifier totals changed' >&2
  exit 31
fi
