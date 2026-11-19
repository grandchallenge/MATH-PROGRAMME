#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 verify_cut_profiles.py
python3 verify_five_vertex_block.py
python3 verify_motif_colorings.py
python3 verify_16to18_cut_profiles.py
python3 verify_16to18_colorings.py
printf 'ERDOS561_UNIQUE16_SOURCE_REPLAY_PASS\n'
