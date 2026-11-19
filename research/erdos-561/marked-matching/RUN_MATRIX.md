# Erdős #561 — saturated matching run matrix

| Audit gate | Command | Exact expected outcome |
| --- | --- | --- |
| Mathematical manuscript | `python3 ci/math_markdown_gate.py --file SHARP_SATURATED_MATCHING_DEFICIENCY_THEOREM.md` | PASS |
| Designated matching bound | `python3 verify_marked_matching_exact.py` | 685 atlas + 260 seeded graphs + 4 disjoint K5 family instances, matching deficiency formula agreement |
| Two avoiding-colouring constructions | `python3 verify_coloring_constructions.py` | 685 atlas types under both schemes + 330 exact-edge-count tests; blue/star and red-disjoint-P3 tests pass |
| Final remaining 22 parameters | `python3 verify_final_three_star_gate.py` | 18 Strategy B, 4 Strategy A; zero uncovered |
| Four-stage exact source chain | `python3 verify_chain_reconciliation.py` | 75 → 39 → 25 → 22 → 0; all pair sets nested, zero missing/unjustified drops |
| Full standalone replay | `bash run_all.sh` | `ERDOS561_MATCHING_ALL_22_METHOD_CASES_CLOSED_CONDITIONALLY` |
| Canonical ledger | JSON Schema `schemas/claim_ledger.schema.json` | Finite work CHECKED, broad paper mathematics and conditional Ramsey scope UNDER_REVIEW |
| Source integrity | `sha256sum -c SHA256SUMS.txt` | Every committed source exact |

The full replay requires Python 3.10+ and NetworkX 3.4.2. Default upstream certificate paths are relative to this directory within the protected MATH-PROGRAMME repository. Before the prerequisite parent PR #3569 merges, set `UPSTREAM_561_EVEN_CAP_CERTIFICATE` to a SHA-verified exact copy of its committed source. The optional reconciliation overrides are `ERDOS561_UPSTREAM_75`, `ERDOS561_UPSTREAM_39`, `ERDOS561_UPSTREAM_25`, and `ERDOS561_UPSTREAM_22`.

No GPU is needed, no source is written to protected main directly, no interactive solver is required, and there are no repeated GitHub API requests inside any verification script.
