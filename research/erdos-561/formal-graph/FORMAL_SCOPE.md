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
