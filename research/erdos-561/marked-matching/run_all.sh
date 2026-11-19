#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 verify_marked_matching_exact.py
python3 verify_final_three_star_gate.py
python3 verify_coloring_constructions.py
python3 verify_chain_reconciliation.py
printf 'ERDOS561_MATCHING_ALL_22_METHOD_CASES_CLOSED_CONDITIONALLY\n'
