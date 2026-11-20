#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 verify_star_host_iff.py
python3 verify_iterated_peeling.py
python3 verify_cone_colouring.py
python3 verify_unbounded_families.py
python3 verify_fast_vs_full.py
python3 search_rigid_12edge.py
python3 verify_rigid12_independent.py
python3 search_rigid_13edge.py 0 163
python3 verify_rigid13_independent.py
exe="$(mktemp /tmp/gcl-erdos561-rigid14-XXXXXX)"
trap 'rm -f "$exe"' EXIT
c++ -std=c++17 -O3 -Wall -Wextra -Werror -o "$exe" verify_rigid14_exact.cpp
"$exe" 0 256
python3 verify_rigid14_independent.py 0 256
exe15="$(mktemp /tmp/gcl-erdos561-rigid15-XXXXXX)"
trap 'rm -f "$exe" "$exe15"' EXIT
c++ -std=c++17 -O3 -Wall -Wextra -Werror -o "$exe15" verify_rigid15_exact.cpp
"$exe15" 0 386
python3 verify_rigid15_structural.py
python3 make_falsification_evidence.py
out="$(mktemp /tmp/gcl-erdos561-joint-star-XXXXXX)"
trap 'rm -f "$out" "$exe" "$exe15"' EXIT
python3 star_host_falsifier.py --level 3 --max-e 18 --max-hosts 4000 > "$out"
python3 - "$out" <<'PY'
import json,sys
s=[json.loads(x[7:]) for x in open(sys.argv[1]) if x.startswith('RESULT')]
assert len(s)==420 and all(x['status']=='STAR_HOST_NO_WITNESS' for x in s)
assert sum(x['count'] for x in s)==155737
print('STAR_HOST_COMPLETE_UP_TO_BOUND_PASS',len(s),sum(x['count'] for x in s))
PY
printf 'ERDOS561_JOINT_GENERAL_UNBOUNDED_SUBTHEOREMS_REPLAY_PASS\n'
