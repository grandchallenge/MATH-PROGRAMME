# EXT-015 REACH / 076 — critical audit of the global cone topology obstruction

**Provenance:** distinct logical mathematical critic pass after the author source was frozen, within the same Codex session/account. No external independent certification is claimed.

**Exact source:** commit `b286ef54238a41c3866a8e71640d8796617dcbb1`; [075](R1_GLOBAL_CONE_PLOT_OBSTRUCTION_075.md) blob `fa4e57a5f8f8e27e68815cf873ebb26e94982991`; [fixture](fixtures/check_global_cone_plot_obstruction_075.py) blob `2cb30f30c58ba8e8677e70885fc38bed0b1c0175`.

## 1. The published theorem applies to the actual cone

The forbidden set is a finite union of closed nonzero partial-diagonal conormals and is invariant under sign. Its complement is therefore open. At a collision point, the covectors used in Lemma 75.1 have nonzero total sum and cannot lie in any partial-diagonal conormal; their limit is a pair conormal. This verifies nonclosedness directly, rather than importing an unrelated microcausal cone.

The normal-sector support/cone pairs are cofinal with the compact and angular-distance exhaustion in section 3.1 of Dabrowski–Brouder. Restriction to unit covectors over a fixed compact makes the admissible closed cone compact and separated from the complement. This checks the topology identification required before applying their Theorem 34 and Corollary 36.

**Assessment:** support the negative completeness and regularity verdict for the specified ordinary global inductive topology. The argument is restricted to arity at least two; the empty/full open-cone exceptions are not swept into the conclusion.

## 2. Real symmetric kernels are genuinely included

A counterexample in an unsymmetrized complex space alone would not settle the actual symmetric polynomial-kernel case. The source therefore applies real part and coordinate averaging to the published bounded Mackey-Cauchy sequence. Both maps are continuous on the ordinary inductive union because they act continuously on each normal sector into the transformed admissible sector.

The chosen covector rays and their sign/exchange orbits are pairwise distinct. At each selected ray, only one transformed summand is singular, so the finite averages cannot cancel its singularity. Their distributional limit has the same isolated-ray property, using the tail-cone control in the published construction. Closedness of wavefront then forces the forbidden limiting ray.

Thus the projected sequence is bounded and Mackey-Cauchy in the real symmetric subspace and has no limit in that subspace. Its tail wavefronts are not contained in any single closed admissible cone. This last statement is necessary: failure of a seminorm bound alone would not prove the failed plot lift after rescaling.

**Assessment:** support the real symmetric arity-two reduction and the no-common-sector property.

## 3. The curve is smooth in the stronger global LCS topology

At every nonzero parameter the bump expression is locally finite. All estimates use an arbitrary continuous seminorm of the ordinary global inductive LCS and the bounded sequence, not just weak distributional tests. The quadratic decay dominates the exponential derivative and difference-quotient factors of every fixed order.

It follows inductively that all derivatives at zero exist in the actual incomplete space, equal zero and are continuous. No infinite sum at a fixed parameter, integration in a completion or appeal to weak smoothness is needed. This proves Bastiani smoothness.

If this curve had a local lift to one normal sector, its nonzero values at the bump centers would put every tail wavefront into that sector's closed admissible cone. The scalar amplitudes cannot remove wavefront directions. The forbidden boundary limit gives a contradiction.

**Assessment:** support Theorem 75.3 and the failure of the inverse distributional identity between these two plot structures. This is an actual failed lift for the ordinary global LCS, stronger than the previously admitted ambient-strong example of 033.

## 4. Hostile checks and retained scope

The finite fixture verifies distinct sign/permutation rays, the collision-normal boundary, disjoint bump intervals and 2673 quadratic exponent controls. It does not construct or numerically certify an infinite family of distributions. The source correctly separates the published countersequence theorem from the new REACH-specific cone and curve arguments.

The result does not invalidate the refined DVS of 069, whose plots are defined by local sector lifts. Nor does it prove every operation on the ordinary LCS discontinuous or rule out unrelated alternative comparisons. It settles the requested ordinary complete/regular union and its identity with the refined plots in the negative.

**Verdict:** accept the stated topology obstruction and failed plot lift as a bounded source-semantic return. The uniform regulator endpoint still needs its own proof; do not close R1 or the REACH parents on this result alone. Original degree-two liquid surjectivity and global renormalized BV remain separate open obligations.
