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