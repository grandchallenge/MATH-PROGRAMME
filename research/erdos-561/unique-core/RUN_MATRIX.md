# Erdős #561 core-uniqueness verification matrix

| Step | Command | Expected output |
| --- | --- | --- |
| Lean compiler version | `lean --version` | `4.33.0-rc1`, commit `62eed1db4d67327ec8120be05f1a1b0847d74561` |
| Lean arithmetic prerequisite | `lean Erdos561UniqueLargeCore.lean` | Four general theorems; no user axioms or sorry |
| Exact graph-check compile | `c++ -std=c++17 -O2 -Wall -Wextra -Werror -o /tmp/gcl561core verify_general_core.cpp` | Zero errors and warnings |
| Exact graph check | `/tmp/gcl561core` | 33,866 graphs; 91,727 cap splits; 91,657 cases under threshold; 263 below-threshold failures, all classified |
| Independent parameter replay | `python3 verify_parameter_gate.py` | 851 old baseline; 512 old exclusions; 249 new (186 + 63); 90 remaining |
| Independent exact full-list comparison | `python3 verify_independent_gate.py` | Match complete 249 excluded and 90 remaining sets without importing primary verifier |
| Source hashes | `sha256sum -c SHA256SUMS.txt` | All content-identical |
| Mathematical Markdown | `python3 ci/math_markdown_gate.py --file GENERAL_SATURATED_CORE_UNIQUENESS_THEOREM.md` | PASS |
| Canonical ledger | Validate `CLAIM_LEDGER.json` against `schemas/claim_ledger.schema.json` | Narrow checked Lean plus unpromoted mathematical claims |

Tests and Lean certificates do not replace the unbounded paper argument or full formalization of Lovász's theorem. Exact 3×3 deductions depend on the previously admitted paper-level joint residual result.
