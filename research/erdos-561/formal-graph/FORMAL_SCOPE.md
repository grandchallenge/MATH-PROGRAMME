# Erdős #561 — graph-level Lean dependency tranche

**Status:** Exact, narrowly scoped graph-theoretic Lean checks; not certification of the full Erdős #561 conjecture or the three-star joint residual theorem.

`Erdos561GraphHandshake.lean` represents a graph with an arbitrary finite vertex type `Fin n` and a finite list of edges, each given by a pair of endpoints. The edge-list incidence degree counts endpoints (a loop contributes two); ordinary finite simple graphs are included as a subcase, but the Mathlib `SimpleGraph` embedding itself has not been formalized.

Lean formally proves `handshake` (the total degree equals twice the edge count), `saturated_edge_budget` (at least `D+1` degree-`D` vertices imply `D*(D+1) ≤ 2*e`), `saturated_vertex_budget` (for `D≥1`, `(D−1)*(D+1)+v_pos ≤ 2*e`), and `low_slack_exact_core` (for `D≥2`, if `s<D−1` in the stated degree-excess budget, exactly `D+1` vertices have degree `D`). All these theorems are general in the finite vertex count and edge list. The proof uses only standard Lean foundations (`propext`, `Quot.sound`, and `Classical.choice` for the low-slack theorem), and no `sorry`, user axiom, `admit`, or `native_decide`.

`Erdos561FourVertexCore.lean` is a kernel-checked **semantic canary**: all 64 labelled graphs on four vertices, all positive degree-cap splits, and every red-edge selection are checked, together with the triangle obstruction. It is not a substitute for the general factor theorem.

## Still not formalized

- **Critical:** the Lovász `(g,f)`-factor theorem implication that failure of a capped red/blue edge partition forces at least `D+1` maximum-degree vertices, including connectedness.
- The source-locked You two-component size-Ramsey theorem, both simultaneous residual vertex deletions, canonical Ramsey upper host, and the original three-star or unrestricted size-Ramsey statements.
- Independent source-semantic scope of `jimsteeg`'s empty-body GitHub APPROVED review on mathematical research PR #3523. Written scope requested in PR comment `7006007758`.

The previous narrow formal evidence PR #3535 has merged. Its non-required protected material-profile delegated-review check failed with `candidate specialist class unresolved or mixed`; this is documented in PR comment `7006011645`, and the merge does not override that review classifier. This new tranche remains a separate draft source submission until policy-compliant adjudication.

## Lovász factor bridge: proved on paper, partially verified in Lean

The new `LOVASZ_CAP_PARTITION_BRIDGE.md` gives a complete ordinary mathematical proof, from the **published ordinary** Lovász `(g,f)`-factor theorem, that failure of an `(alpha,beta)` degree-capped red/blue partition requires a connected component on at least `D+1` maximum-degree vertices. Its `q(S,T)` counts components whose vertices are all tight `g=f` and which satisfy the stated parity condition. This is **not** the stronger, different parity-factor theorem.

`Erdos561FactorCut.lean` checks six general Nat lemmas: lower/upper proportional envelopes for the factor bounds; the `r(D-r+1)≥D` boundary estimate when `1≤r≤D`; positive-weight boundary allocation; summation over a list of q disjoint boundary pairs; and the scaled Lovász cut inequality assuming the weighted component contribution. The kernel reports only standard axioms `propext` and `Quot.sound` for all six. Its source does not import, assert as a new axiom, or pretend to prove the **general** Lovász `(g,f)`-factor theorem, the graph tight-component extraction, or the combinatorial cut identities.

`verify_factor_bridge.cpp` provides a wholly separate finite sanity check. It exhausts all 33,866 labelled graphs on two through six vertices and every possible split of their maximum degree (91,727 instances), observes 273 actual cap-partition failures and checks that all have the large connected degree-D core. For the 2,809 selected instances (all graphs through five vertices plus a deterministic six-vertex sample), it independently computes the exact ordinary Lovász `(g,f)` component-parity criterion for all disjoint S,T and agrees with constructive red/blue edge assignment. The C++ test is not a formal infinite proof.

**Promotion boundary:** The connected core lemma is paper-level proved *conditional on the accepted published Lovász factor theorem*, not yet machine-verified in its entirety. The new ledger distinguishes the narrow six Lean-checked Nat lemmas (`CHECKED`) from the full classical-theorem-dependent bridge (`UNDER_REVIEW`). The complete three-star joint residual, its 82-case graph reduction, and unrestricted Erdős #561 remain separate downstream mathematical obligations.
