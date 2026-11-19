#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exe="$(mktemp /tmp/gcl-erdos561-d2-XXXXXX)"
trap 'rm -f "$exe"' EXIT
c++ -std=c++17 -O2 -Wall -Wextra -Werror -o "$exe" verify_degree2_exhaustive.cpp
"$exe"
python3 verify_degree2_independent.py
python3 verify_cubic_sharpness.py
python3 verify_lowdegree_ledger.py
printf 'ERDOS561_LOWDEGREE_COMPLETE_REPLAY_PASS\n'
