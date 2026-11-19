# Run matrix — Erdős #561 joint three-by-three and degree-core gate

| ID | Runner | Scope | Acceptance |
|---|---|---|---|
| COR-01 | `python verify_core_and_switching.py` | Exhaustive atlas graph/degree-cap partitions, at most 7 vertices and 18 edges | 4,115 instances; 32 no-split and 0 violations of degree-core / edge / vertex bounds |
| ALG-01 | `python verify_odd_core.py` | All nonincreasing triples with largest size 2..10 on each side | 47,961 ordered pairs; 44,893 zero-switch and 46,120 core-threshold cases (3,054 positive-switch) |
| JOI-01 | `python verify_joint3_finite.py` | All nonincreasing triples with entries 1..7; positive switching and `d<=7` | 7,056 ordered pairs; exactly 82 critical cases: 74 edge contradictions, 8 vertex contradictions |
| ORI-01 | `python verify_original_remaining.py` | Original 3×3 residual cases with `D<=9` and largest sizes ≥2 | 4,566 small-parameter pairs; 851 not excluded by the stated elementary gates; output list sorted and reproducible |
| ODD-01 | `python verify_odd_core.py` | Independent finite arithmetic for odd-`D` equality-coloring corollary | Previous 851 cases, six eliminated, 845 remaining; 1-factorizations validated for odd `D=3,5,7,9` |
| SRC-01 | Manual review | Lovász `(g,f)`-factor theorem; Vizing; published two-component size Ramsey theorem | Exact hypotheses and source pins checked before mathematical promotion |
| RVR-01 | Different logical review or Lean | Theorem A cut inequality, switching case split, and finite-domain completeness | Required for formal mathematical admission; not yet completed |

**Resources:** CPU-only, standard Python for JOI/ORI; NetworkX for COR. No GPU, no GraphQL polling, no repeated Monte Carlo.

**Boundaries:** The 851 remaining parameter entries are not 851 certified-open instances. No claim beyond the exact theorems in the accompanying manuscript.
| EVE-01 | `python verify_even_core.py` | Constructive 1-factor/Hamilton-cycle cap partitions at exact degree-core equality | 20,433 checked cases, exactly 10 pure-complete odd/odd failures; parameter list 851→845→835 |
| EVI-01 | `python verify_even_core_independent.py` | Separate exhaustive cap-partition feasibility, no decomposition code | 3,608 bounded cases, 3,605 split-capable and 3 genuine exceptions |

| STB-01 | `python verify_one_slack.py` | Independent exhaustive near-equality cap feasibility for all D=3,4 missing-core patterns and bounded D=5,6; exact 3×3 parameter gate | 29,685 feasible near-core tests; 80 additional ordered exclusions; surviving filter 755 |

| LOW-01 | `python verify_low_slack_316.py` | Two-star-residual-conditional low-slack criterion over 4,566 ordered three-star pairs | 851 baseline, 316 excluded, 535 remain; exact sorted-set SHA-256 |
| LOW-02 | `python verify_low_slack_independent.py` | Separate antidiagonal implementation and pair-list digest | Exactly the same 316 ordered pairs; digest verified |
| LOW-03 | `python verify_core_isolation_atlas.py` | Brute-force capped colourings of all eligible graph atlas classes through 7 vertices | 77 graphs; 172 cap cases; 20 precisely characterized parity obstructions |

| D+2-ATL | `python verify_dplus2_atlas.py` | Complete NetworkX atlas n<=7, 4,100 cap cases below threshold | All 22 failures are isolated parity cliques; 9 nonclique failures occur above threshold |
| D+2-CORE | `python verify_dplus2_core_exhaustive.py` | All k=D+2 core+leaf complement constructions at D=2,3,4 | 41, 768, 27,449 graphs respectively, only isolated parity clique failures |
| D+2-PAR | `python verify_dplus2_parameters.py` | Exactly 4,566 low-D 3×3 ordered pairs under same baseline filter | 851 baseline, 512 excluded, 416 beyond previous odd/even/one-slack, 339 retained |
