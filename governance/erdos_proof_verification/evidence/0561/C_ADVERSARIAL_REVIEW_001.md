# Erdős #561 — Phase C separate adversarial semantic and formal pass

**Reviewer scope:** nonauthoring critical logical role under the same authenticated GitHub identity `fyremael`; **not** a separate human mathematician, external referee, or MathCERT certification. Reviewed the exact protected B evidence, frozen preprint v1, new `Erdos561Core.lean`, actual type/axiom output, five compiler-rejected false targets, and 12 fail-closed source-integrity tests.

## Proof and source challenges

| Adversarial question | Verified finding |
| --- | --- |
| Was the wrong Ramsey invariant proved? | No. The source concerns the minimum **number of host edges** for two different coloured target star forests. The local kernel code is integer arithmetic, and does not claim a complete Ramsey invariant at all |
| Is there a source-locked existing Lean theorem to replay? | No. The frozen 85f86371 `FormalConjectures/ErdosProblems/561.lean` returned GitHub HTTP 404. The 2026 paper is newer than the 2025 catalogue lock; no upstream substitution was made |
| Can a green arithmetic compile be misread as proof of Lovász? | No. The `Init` module has neither a graph component model nor an axiom-free proof of Lovász's factor theorem. The external theorem remains an explicit mathematical dependency |
| Is the truncation $d-\beta$ equivalent to $\max\{0,d-\beta\}$? | Yes for natural degrees and budgets. The kernel proved the `degree_minus_lower_eq_min` and `tight_degree_iff` identities with positive $\alpha$; hostile target with $\alpha=0$ was rejected |
| Does the local factor-budget equivalence silently permit an impossible degree? | No. `split_budget_iff` explicitly assumes that the selected subdegree $j\leq d$, and proves equivalence only to the numerical blue-complement bound |
| Could the source's odd-component term lose the boundary parity? | The actual kernel check proves flipping the boundary count by one flips parity. The hostile `omitted_edge_to_T_parity` target was rejected. B's $K_3$ cut also checks the same danger using actual edges |
| Is the claimed minimum-degree ratio valid without any ambient bound? | No; the actual `min_degree_ratio` declaration retains both $d\leq D$ and $\beta\leq D$. The source's Claim 3.9 requires $\Delta(G)\leq D$ |
| Could the all-small-components contradiction be vacuous? | Its `all_small_components_impossible` proof requires a positive $D$, at least unit budget, strict obstruction $A<r$, and the independently **assumed** cut boundary $rD\leq B$. It does not assert that every actual residual component is small |
| Could the large-component branch be asserted for arbitrary bounded-degree graphs? | No. The Lean lemma takes as *premise* the lower cut-edge count $\beta(D+r-2)+2\leq B$. That depends on disjoint star-center structure and a small residual. The $K_{13}$, $\alpha=3$, $\beta=9$ parity obstruction independently falsifies the attempt to omit that premise |
| Are parameter inequalities strict at the boundary? | `strict_factor_slope` requires $\alpha\geq2$, $\beta\geq2(\alpha+1)$, and $D=\alpha+\beta$. The altered equality-budget target was rejected. The final large-component contradiction is exact, including $r=1$ |
| Did the compiler accept holes, extra imports, or forged theorem types? | Eleven actual printed theorem types and axiom lists are hash-locked. A source scanner rejects `sorry`, `admit`, `axiom`, `unsafe`, `native_decide`, and import drift. Twelve adversarial tests reject modified type text, new axiom, missing axiom report, fake negative success, and false completion |
| Does `Classical.choice` signify a new proof axiom? | It is a standard Lean logical axiom present in some `omega`-based proofs and is listed in the exact permitted set along with `propext` and `Quot.sound`. No custom untrusted axiom or `sorryAx` is present. This cannot substitute for semantic verification |
| Did we independently prove all 2026 paper reductions? | **No.** The source's Claims 3.2–3.8 include extremal induction, matching and residual decomposition, two-index size jumps, and maximum-degree star-center localization. None has been kernel proved; the B proof assumed their conclusions. The paper's full Theorem 1.2 is not independently certified |
| Was a registered Colab mathematical reviewer or execution job used? | **No.** GCL's current protected Colab registry has only Erdős #41 and #248; its state is `LOCKED_OFFLINE` for arbitrary new jobs. CHAD performed a bounded local compiler replay, not an independently authenticated Colab run |

## Actual false-target evidence

The five separate Lean compilations exited with nonzero status and an actual `error:`: (1) false minimum identity, (2) degree saturation when $\alpha=0$, (3) wrong odd parity after an edge to $T$, (4) strict slope with equal degree budgets, and (5) an inverted large-component boundary. The exact negative source hashes, exit codes and diagnostic hashes are in `C_LEAN_CORE_REPLAY_001.json`. No negative result was accepted merely because a Python assertion failed.

## Scope disposition

**PASS** for a genuine no-hole Lean 4.33.0 kernel replay of eleven *auxiliary arithmetic lemmas*, with an independent semantic review and exact primary-source scope. **NOT VALIDATED** as a Lean graph-factor theorem, matching-star localization lemma, full You Theorem 1.2, original Erdős #561 conjecture, MathCERT submission, or independent human review.

**Next mandatory mathematical obligations:** formalize finite simple graph edges/degrees, the exact Lovász cut-component predicate including parity, source-to-Mathlib equivalence, the component boundary/star-center counting steps, and then independently replay or refute the paper's earlier Claims 3.2–3.8. For those missing graph statements, numerical simulations and this arithmetic proof are insufficient.
