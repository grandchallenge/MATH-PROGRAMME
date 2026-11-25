#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exe=$(mktemp)
out=$(mktemp)
trap 'rm -f "$exe" "$out"' EXIT
g++ -std=c++17 -O2 -Wall -Wextra -Werror verify_cap_defect.cpp -o "$exe"
"$exe" > "$out"
cmp "$out" CAP_DEFECT_GRAPH_EVIDENCE.json
python3 verify_frontier_plateau.py > "$out"
cmp "$out" FRONTIER_PLATEAU_EVIDENCE.json
sha256sum -c SHA256SUMS.txt
