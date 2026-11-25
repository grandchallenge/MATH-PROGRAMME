#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 verify_star_host_iff.py
python3 verify_iterated_peeling.py
python3 verify_cone_colouring.py
python3 verify_unbounded_families.py
python3 verify_rigid15_311_5221.py
python3 verify_unique_max_311_b221_family.py
python3 verify_joint_monotone_plateaus.py
python3 verify_rigid14_322_3111.py
python3 verify_original20_322_3111_3211.py
python3 verify_core_original_transfer.py
python3 verify_d2_original_211_2111.py
python3 verify_flat_tail_rigidity_family.py
python3 verify_flat_tail_multiarm.py
python3 verify_variable_tail_deficit.py
python3 verify_saturated_matching_joint.py
python3 verify_matching_degree_peeling.py
python3 verify_three_by_three_joint_induction.py
python3 verify_three_by_three_original_boundary.py
python3 verify_uniform_star_erdos561.py
python3 verify_unit_tail_two_stars.py
python3 verify_four_by_three_matching_bridge.py
python3 verify_five_by_three_matching_bridge.py
python3 verify_all_red_lengths_three_blue_staircase.py
python3 verify_all_s_blue_matching_bridge.py
python3 verify_recursive_three_blue_certificates.py --grid
python3 verify_recursive_red_matching_certificates.py --grid
python3 verify_recursive_vertex_budget_certificates.py --grid
python3 verify_recursive_fifth_core_certificates.py
python3 verify_gallai_no_triangle_support.py
python3 verify_blue_order_adaptive_gallai.py --guard-only
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
python3 verify_profile_mismatch.py
python3 verify_profile_mismatch_15edge.py
exe_profile="$(mktemp /tmp/gcl-erdos561-profile-XXXXXX)"
trap 'rm -f "$exe" "$exe15" "$exe_profile"' EXIT
c++ -std=c++17 -O3 -Wall -Wextra -Werror -o "$exe_profile" verify_profile_mismatch_cpp.cpp
"$exe_profile"
python3 make_falsification_evidence.py
out="$(mktemp /tmp/gcl-erdos561-joint-star-XXXXXX)"
trap 'rm -f "$out" "$exe" "$exe15" "$exe_profile"' EXIT
python3 star_host_falsifier.py --level 3 --max-e 18 --max-hosts 4000 > "$out"
python3 - "$out" <<'PY'
import json,sys
s=[json.loads(x[7:]) for x in open(sys.argv[1]) if x.startswith('RESULT')]
assert len(s)==420 and all(x['status']=='STAR_HOST_NO_WITNESS' for x in s)
assert sum(x['count'] for x in s)==155737
print('STAR_HOST_COMPLETE_UP_TO_BOUND_PASS',len(s),sum(x['count'] for x in s))
PY
printf 'ERDOS561_JOINT_GENERAL_UNBOUNDED_SUBTHEOREMS_REPLAY_PASS\n'
