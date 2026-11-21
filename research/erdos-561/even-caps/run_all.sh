#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 verify_even_caps_constructive.py
python3 verify_even_cap_parameters.py
python3 verify_even_cap_original_transfer.py
printf 'EVEN_CAPS_RESEARCH_REPLAY_PASS\n'
