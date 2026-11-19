# Erdős #561: first Lean 4 kernel-checked dependency tranche

**Scope:** exact subset of the current 3×3 joint-residual research candidate, not certification of the general theorem. This is a new material branch, intentionally separate from draft PR #3523 while the non-author review request for that PR is active.

**Compiler:** Lean 4.33.0-rc1, commit `62eed1db4d67327ec8120be05f1a1b0847d74561`, Release, x86_64 Linux. Imports only `Init` and `Lean.Elab.Tactic.Omega`; no Mathlib dependency, no `sorry`, no added axioms, no `native_decide`. The finite proofs use definitional reduction via `decide` and Lean's kernel. The arithmetic lemmas use the built-in `omega` tactic where indicated. Lean may use its ordinary foundation (`propext`, `Classical.choice`, `Quot.sound`) for `omega` proofs; the finite certificate reports no axioms.

## Stage 1: non-author review request

Repository PR `grandchallenge/MATH-PROGRAMME#3523`, mathematical material head `433e1aa5ef938faf2d2bb71bfa4f2dd64f4c6601`, author `fyremael`: a real GitHub review request was placed with `jimsteeg`, a member of the `referees` team and distinct from the author. Review questions are in PR comment `7004690481`. A request is **not** a completed substantive review, approval, certified theorem or protected merge. The current mathematical ledger remains `UNDER_REVIEW`.

## Stage 2: exactly what Lean checked

**`Erdos561Finite.lean`** defines the 84 nonincreasing triples `a≥b≥c≥1` with largest entry ≤7. It enumerates all 7,056 ordered pairs and computes the same antidiagonal star-forest edge weights used in the manuscript. Five closed theorems are checked:

1. `triple_count`: exactly 84 triples.
2. `bounded_parameter_gate`: for every ordered pair with positive switching and forced `D≤7`, either the hypothetical edge count violates the core degree-sum bound or its required forest order exceeds the core vertex bound.
3. `relevant_candidate_count`: exactly 82 bounded positive-switch pairs.
4–5. `edge_exclusions_count` and `vertex_exclusions_count`: 74 edge-budget failures and eight remaining vertex-budget failures.

The second through fifth theorems are *arithmetic about the explicitly defined weights*, not proofs that graph Ramsey arrowing reduces to those inequalities. The structural reduction is an external paper-level claim in PR #3523.

**`Erdos561CoreArithmetic.lean`** establishes four universally quantified NATURAL-NUMBER lemmas: `saturated_edge_budget`, `saturated_vertex_budget`, `saturation_low_slack` and `saturation_low_slack_from_sum`. They express the degree-sum and low-slack inequalities from explicit numeric premises (including the necessary maximum-degree-vertex count). These are not yet the graph-theoretic argument that a failed capped edge partition must have ≥D+1 saturated vertices.

## Proof obligations that remain OPEN in Lean

- Formal finite-simple-graph definitions and proof of handshake/degree-sum facts leading to the arithmetic hypotheses.
- Formal specialization of Lovász's `(g,f)`-factor theorem to the failed `(α,β)` capped partition, including exact odd-component criterion and the high-degree-core lemma.
- Formal version or source-locked imported theorem for the two-component star-forest size-Ramsey bound (Chunlin You, arXiv:2610.25958v1), and its hypotheses for star size 1.
- Formal proof that the two simultaneously required residual Ramsey relations imply the lower-bound reduction and correspond to the computed arithmetic alternatives; then the original Ramsey value and its upper host.
- Independent `jimsteeg` mathematical review of the material 3×3 proof, with authenticated disposition. This is requested, not returned.

**No claim that the unrestricted Erdős #561 conjecture is solved or that the entire 3×3 joint residual theorem has been formally verified.** The source files provide independently rerunnable, bounded computational/arithmetical proof evidence only. CI success and successful Lean compilation do not by themselves grant MATHCERT or protected mathematical admission.
