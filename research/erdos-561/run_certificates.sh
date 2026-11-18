#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 exact_degree5_residual.py | tee /tmp/erdos561_python.txt
grep -q '"candidate_M": 11197' /tmp/erdos561_python.txt
grep -q '"passed": 2' /tmp/erdos561_python.txt
c++ -std=c++17 -O2 -o /tmp/erdos561_cpp exact_degree5_cpp_replay.cpp
/tmp/erdos561_cpp | tee /tmp/erdos561_cpp.txt
grep -q 'TOTAL tested=11197 arrows=2' /tmp/erdos561_cpp.txt
python3 exact_joint_upper.py
python3 exact_original_upper.py
python3 k_apex_colouring.py | tee /tmp/erdos561_kapex.txt
grep -q '"total": 3000' /tmp/erdos561_kapex.txt
grep -q '"failures": 0' /tmp/erdos561_kapex.txt
printf 'ERDOS561_CERTIFICATE_REPLAY_PASS\n'
