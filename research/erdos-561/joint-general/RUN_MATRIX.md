# Erdős #561 — general joint residual research replay

| Test | Command | Expected |
| --- | --- | --- |
| Mathematical manuscript | `python3 ci/math_markdown_gate.py --file JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md` | PASS |
| Exact iff for star hosts | `python3 verify_star_host_iff.py` | 7,954 general and 5,917 joint tests, every red/blue arm assignment exhaustively covered |
| Constructive arbitrary-graph peeling | `python3 verify_iterated_peeling.py` | 1,162 graph/target cases, every branch and explicit target-embedding audit PASS |
| Original two-centre special case | `python3 verify_cone_colouring.py` | 1,283 graph/target cases, all branches PASS |
| Infinite-family parameter arithmetic | `python3 verify_unbounded_families.py` | 14,925 broad cases, 6,072 C1 examples, 1,944 C2 examples, 199 growing switching-surplus tests PASS |
| Bounded star-host adversary | `python3 star_host_falsifier.py --level 3 --max-e 18 --max-hosts 4000` | 420 qualifying parameter pairs; complete scan of 155,737 qualifying disjoint-star hosts below J, zero counterexamples |
| Nonstar one-vertex-identification adversary | `ERDOS561_EDGE_BUDGET=12 python3 search_five_fast.py 0 25` and `ERDOS561_EDGE_BUDGET=13 python3 search_five_fast.py 0 41` | 3,208 + 6,042 simple candidate graphs tested, zero joint witnesses (within specified host-generation class only) |
| Complete strict-switch 12-edge graph classification | `python3 search_rigid_12edge.py` then `python3 verify_rigid12_independent.py` | Two independent complete enumerations of 9,194 cubic-hub extensions: 130 pass necessary rigid tests, only one arrows B, none arrows both; exact minimum 13 |
| Complete strict-switch 13-edge graph classification | `python3 search_rigid_13edge.py 0 163` then `python3 verify_rigid13_independent.py` | Two independent complete enumerations of 31,667 quartic-hub extensions: 9,225 with enough vertices, only one arrows A, none arrows both; exact minimum 14 |
| Complete strict-switch 14-edge graph classification | `c++ -std=c++17 -O3 -Wall -Wextra -Werror -o /tmp/gcl_erdos561_rigid14 verify_rigid14_exact.cpp && /tmp/gcl_erdos561_rigid14 0 256` and `python3 verify_rigid14_independent.py 0 256` | Two separately implemented **full** 74,553-case enumerations; 72,512 B failures by two-vertex deletion, 1,914 A failures by red star, 127 A failures by explicit red matching; no joint host, exact minimum 15 |
| Exact new 3×4 equal-leading infinite family finite audit | `c++ -std=c++17 -O3 -Wall -Wextra -Werror -o /tmp/gcl561_rigid15 verify_rigid15_exact.cpp && /tmp/gcl561_rigid15 0 386` and `python3 verify_rigid15_structural.py` | Both **complete** independently implemented 84,653-case attachment checks, exactly one B-deletion survivor and no simultaneous Ramsey host; theorem for all a≥4 is proved on paper, not extrapolated from finite data |
| Independent graph arrow oracle cross-check | `python3 fast_A.py`, `python3 exact_arbitrary_host.py` | Exact red matching-1 characterization consistent with independent exhaustive 2^E two-colouring checks |
| Claim ledger schema | Validate `CLAIM_LEDGER.json` with `schemas/claim_ledger.schema.json` | Full problem OPEN; proved subclaims UNDER_REVIEW; bounded exact checks CHECKED |
| Integrity | `sha256sum -c SHA256SUMS.txt` | Exact files all match |

`run_all.sh` executes the short mathematical code checks and evidence receipt validation. The optional 9,250 nonstar candidate graph search takes tens of seconds on CHAD and is NOT re-run on every CI invocation. All four rigid finite complete proof checks, including the two independent 14-edge verifiers, are included in the full source replay. It uses only CPython 3.10+ and NetworkX 3.4.2. There is no GPU, remote query loop, SAT service or live GitHub dependence inside the numerical tests.

**Important boundary:** Finite experiments do not prove the full hypothesis, and a failure to find a counterexample in a restricted graph class is not a mathematical certificate. The mathematical proof is in the manuscript and remains subject to substantive internal mathematical review.
