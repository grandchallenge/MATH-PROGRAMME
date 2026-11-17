# Erdős #560 — source-locked Phase C formal applicability and kernel scope

Task: `ERDOS-PV-0560-C`. Exclusive authenticated task claim: `8b6a32fa6fc8fd037051835fa54542f81ecca50e`. The protected predecessor is the admitted Phase B mathematical evidence at merge `997a3d8068c3b2a036d5811bfabfce2b92a4be15`, with separate custody merge `123701f543f32c7bf92197f77f39405a3702f8f4`. The prior worker return is issue #3230 comment #6944746101. This record reviews the **bounded off-diagonal theorem**, not the open diagonal Erdős problem.

## Source authority and exact semantics

Primary paper: Conlon, Fox, Wigderson, *Three early problems on size Ramsey numbers*, arXiv:2111.05420v2, section 2, Proposition 2.2 and equation (1), https://arxiv.org/html/2111.05420v2 . The theorem concerns a finite simple graph with any number of host vertices, its **number of edges**, and non-induced copies of a complete bipartite graph with parameters at least two on the smaller side and at least two more on the larger side. The proved paper bound is the off-diagonal inequality for the size Ramsey number, not the unsolved diagonal asymptotic.

The catalogue is pinned to `teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89` (file blob `4e60263a80af6207aca494d2e1388e44fa372889`, entry 560). The admitted source-audit issue #1831 body SHA-256 is `2bafa6656b0d797f8b7637be2d7ff77e7682e329467a9df9c858da7e9b7708c1`. In the *frozen* Google DeepMind formal-conjectures snapshot at `85f863718beeec7b58a3a1926ee92e3472bc2020`, the expected `FormalConjectures/ErdosProblems/560.lean` is **absent (GitHub HTTP 404)**. No completed existing formal proof may be inferred from an upstream moving head.

For a future Mathlib implementation, `SimpleGraph.IsCompleteBetween` is the appropriate predicate, not `SimpleGraph.IsBipartiteWith` (which constrains *the graph's own* edges rather than demanding all cross-edges). Pinned Mathlib source `leanprover-community/mathlib4@79d0395a1825a6264ad5d269e35e60537518955e:Mathlib/Combinatorics/SimpleGraph/Basic.lean`, Git blob `f0d556b1218da889dbb72747f39a573cd694ef78`, contains the direct predicate and its disjointness/symmetry theorems. Its API was source-read, **not** compiled in this replay.

## Actual Lean 4 kernel replay

The newly written `experiments/erdos_proof_verification/0560/Erdos560Core.lean` imports only `Init`, using the exact installed Lean 4.33.0 release (compiler commit `d8b18978322de05a8f3dba51ef03cf5461676c17`). It does *not* import Mathlib, avoids relying on a network checkout, and is useful as a foundational bridge but is not a source-to-Mathlib equivalence.

The Lean kernel has checked **12 named declarations**:

1. `completeBetween_disjoint`: loopless cross-completeness implies the two sides are disjoint, even without separately assuming disjointness
2. `right_subset_neighbors`: any fixed left-side vertex is adjacent to every right-side vertex
3. `completeBetween_symm`: reverses sides in a symmetric graph
4. `completeBetween_mono`: adding edges to the host preserves each non-induced complete-bipartite copy
5. `n_le_two_pow`: elementary exponential domination for natural parameters
6. `integral_factor_cleared`: universally proves the exact nonnegative-integer-cleared factor inequality
7. `strict_gate_base`: proves the strict threshold at exponent four
8. `strict_gate_step`: proves its preservation under incrementing the exponent
9. `strict_gate_all`: proves the strict gate for **all** exponents at least four
10. `integral_denominators_positive`: establishes that clearing the factor's denominators preserves inequality direction
11. `gap_ge_two`: establishes the necessary lower bound on the power-tail exponent
12. `t_ge_four`: checks the published numerical threshold follows from the off-diagonal hypotheses

The two quantitative targets are, for integers with appropriate lower bounds,

$$
(s-1)s^a\leq(a-1)2^{s+a}(s-1)^a
\quad(s\geq2,\ a\geq2),
$$

and

$$
2\,18^t<25^t\quad(t\geq4).
$$

These bridge the exact arithmetic factor and the final strict probabilistic budget **conditional on** the still-unformalized graph-count estimate. The compiler exit was zero, all twelve `#print axioms` reports were captured, and the only axioms found were `propext` and `Quot.sound`; none contained `sorryAx`, `Classical.choice`, or user-injected axioms. This is actual Lean verification of exactly those twelve declarations, not a proof of the whole probability bound.

Frozen machine receipt: `C_LEAN_CORE_REPLAY_001.json`; positive compiler output `C_LEAN_CORE_STDOUT_001.txt`; fail-closed replay and byte validator `ci/erdos_pv_0560_formal_replay.py`. CI rechecks the frozen receipt without requiring a Lean installation. A bounded local `--execute` invocation refreshes the receipt **only** with exact Lean v4.33.0 and replays three deliberately false targets, all of which must fail.

## Exact residual proof obligations

**Missing mathematical-formal bridge 1 — copy-count bucket injection.** For every finite simple host graph on `Fin n`, with its vertices ordered by nonincreasing degree and parameters as in the paper, define the `Finset` of oriented, *non-induced*, complete-between pairs of cardinalities `s` and `t`. At each last-left-vertex rank, prove its cardinality is no larger than the number of ways to choose the other `s-1` left vertices times the number of ways to choose a right `t`-subset of that vertex's neighborhood. This is the missing named, source-normalized inequality

$$
N_i\leq\binom{i-1}{s-1}\binom{d_i}{t}.
$$

The exact source-to-formal equivalence must use non-induced adjacency, unique ordered sides for unequal side sizes, and `card_edges` rather than vertex count.

**Missing bridge 2 — analytic summation.** Turn the finite bucket bound into the total bound. Establish the degree ordering `i d_i\leq2q`, the binomial estimates, the comparison of the finite sum with an integral tail for exponent at least two, and the normalizations between real powers/ratios and the integer-cleared `integral_factor_cleared` declaration. The existing twelve declarations do not imply this sum inequality by themselves.

**Missing bridge 3 — two-colour finite counting.** Encode a two-colouring of the host *edge set* and prove the exact cardinality/probability `2^(1-s*t)` for a particular copy to be monochromatic. Use a finite union bound/first moment that does not falsely assume copy events independent, and combine it with the proven strict numerical gate. Verify the host budget and minimum-edge quantifiers; a single host or colouring example is insufficient.

These are real missing source-to-formal proofs, not tool diagnostics to be dismissed. The frozen provider has no #560 formal proof to replay. A no-sorry theorem for the full published Proposition 2.2 has **not** been produced.

## Status and acceptance boundary

- `FORMAL_APPLICABILITY = YES` for a complete future Mathlib development
- `CORE_KERNEL_REPLAY = PASS` for twelve *supporting* claims, with direct axiom reports
- `FORMAL_PROVIDER_AVAILABLE = NO` at the source lock
- `FULL_PROPOSITION_2_2_KERNEL_REPLAY = NOT_PROVED`
- `RESIDUAL = FORMALIZATION_WORK_REQUIRED__COPY_COUNT_TAIL_FIRST_MOMENT`
- `MATHCERT = NOT_SUBMITTED`; `DIAGONAL_CONJECTURE = OPEN`

The bounded Phase C assignment is an applicability and adversarial-replay **review**, and these results can be admitted as an exact bounded review without representing formalization of the full primary proposition as complete. A subsequent formalization requires an explicit governed proof assignment and fresh exact-head replay; phase D's documentary review, if opened, cannot promote the conjecture or a non-existent complete formal proof.
