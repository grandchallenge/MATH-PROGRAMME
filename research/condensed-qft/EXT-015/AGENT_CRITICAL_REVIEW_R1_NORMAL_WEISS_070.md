# EXT-015 REACH / 070 — critical audit of the locally normal free Weiss model

**Provenance:** distinct logical mathematical critic pass after the author source was frozen, within the same Codex session/account. This is not external independent certification.

**Exact source:** commit `0aa90c634a1c74fbf2dfbd9e419c11aab9f01ddb`; [069](R1_LOCALLY_NORMAL_COMPLETED_WEISS_069.md) blob `43d05f2b41cd5fd115a0294f85596a8b8e31cab0`; [fixture](fixtures/check_locally_normal_weiss_069.py) blob `90be2ccdbd212fee5b0da2e8fd88100d6a845387`.

## 1. Diffeology and flat connection

The source defines plots by local lifts into a common compact-support/admissible normal-cone sector. This is a definition of a refined diffeology, not a claim about the ordinary locally convex union. Constant plots, parameter pullback and local gluing hold directly. Two local sector lifts have a common finite-union support/cone enlargement, so addition and smooth scalar multiplication are defined. Parameter derivatives in the Bastiani definition stay in the same sector.

Different lifts give the same derivative after their continuous inclusion into distributions; thus the connection is well-defined. Ordinary parameter chain rule, Leibniz and commutation of partial derivatives give the natural flat connection required by B.1.0.3. This checks more than a class of pointwise admissible families.

The oscillatory R0 family still fails the refined plot condition. No contradiction with 033 is hidden by choosing an empty wavefront set separately in each fiber.

**Assessment:** support Lemma 69.1 on its stated locally normal plots.

## 2. Hypocontinuity is used with the correct quantifiers

For smooth finite-dimensional parameter plots, derivative images on compact coordinate neighborhoods are bounded in the fixed input sectors. Hypocontinuity controls one varying factor uniformly over the bounded image of the other; this is enough for continuity and the two-term difference-quotient identity. Repeating it proves all mixed parameter derivatives and the multilinear Leibniz rule. It does not imply a jointly continuous bilinear map on arbitrary input neighborhoods.

The cited normal-topology tensor theorem has exactly those bounded-set hypotheses. Its output cone contains the two zero-factor terms as well as the product of the nonzero cones. On disjoint opens, there is no collision block joining the two supports; any forbidden output covector would therefore already violate one input sector. Compact supports remove boundary-extension issues.

Continuous linear contraction maps from 035 may be composed with these tensor operations, and finite output-sector unions remain admissible. Consequently the finite Wick-conjugated structure maps are actual smooth multimorphisms compatible with connections.

**Assessment:** support Lemma 69.2 and Theorem 69.3. No general tensor product object for arbitrary differentiable spaces is inferred.

## 3. Completion and quotient lifts are explicit

Total weight is $n+2k$ on $\hbar^k C_n$. A BV contraction lowers $n$ by two and raises $k$ by one, so it preserves this weight; the classical differential preserves it as well. Each weight is finite in arities, and both Wick exponentials are finite there.

The product diffeology on all weights makes each tail a differentiable subspace. Truncation has the smooth chain section given by zero extension in the missing weights. This verifies the cofibration, quotient and fibration assertions directly, instead of treating algebraic surjectivity as a differentiable lifting theorem. The filtration is complete by construction. Each output weight of a multilinear map uses finitely many input weights, with additive filtration degrees.

**Assessment:** support Proposition 69.4 for this specified total-weight completion. Do not equate it with an uncompleted support colimit or an analytically convergent perturbation series.

## 4. The Weiss argument must use a bounded double complex

A Weiss cover induces a tuple-space cover. The physical partition-of-unity multipliers preserve the normal wavefront constraints. On any local sector plot, only finitely many of these multipliers meet the common compact support; hence the Čech homotopy lands locally in the required finite differentiable coproduct. Averaging partitions over the finite permutation group preserves the relevant symmetric subspaces.

The homotopy is horizontal. It does **not** commute with the classical physical differential, and the source correctly does not claim that it does. At fixed arity the vertical cohomological range is finite, so the horizontal-first double-complex argument has a bounded filtration in each total degree. Applying it at every parameter stalk proves the required differentiable weak equivalence. The arity-zero unit uses the nonempty augmented nerve.

Finite weights are finite sums of those arities. The natural Wick cochain isomorphism transports the classical augmented diagram to the quantum one weightwise. At completion, the source uses the completed coproduct prescribed by B.6.0.8, rather than reversing completion and support colimit. The towers are split differentiable fibrations; finite filtration quotients stabilize; successive fibers are the proved weightwise equivalences. These are the actual B.6.0.11 hypotheses.

**Assessment:** support Theorem 69.5 for the specified locally normal free model. This is stronger than the previously admitted purely algebraic descent.

## 5. Acceptance boundary and executable controls

Source and audit mathematical Markdown gates PASS. The fixture replay PASS: 1381 exact Čech homotopy/sign controls, an arity-four failure for an ordinary cover that is not Weiss at that arity, 15 mixed Leibniz identities, and total-weight/fixed-quotient controls. These are finite algebraic regressions, not numerical verification of normal topology or infinite descent.

**Overall bounded assessment:** support the differentiable plot/connection construction, smooth disjoint operations, explicit filtration lifting and completed free zero-scale Weiss descent as stated.

**Still unproved:** identification with a regular complete ordinary locally convex union over cones/supports; uniform smooth extension of the positive-scale regulator family to zero; a renormalized domain including excluded collision distributions; or an R4 liquid-derived comparison. Do not close the broader R1 issue merely by relabeling those requirements. Admit this bounded result through protected checks and read back the proof, fixture and audit; retain the larger REACH checkpoint as nonterminal.
