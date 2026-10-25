# EXT-015 R2/057 — source-locked mathematical audit and exact regression evidence

**Claim class:** CONDITIONAL MATHEMATICAL AUDIT, not mathematical certification or protected admission of the underlying manuscript.

**Audited exact source:** [R2/057 research candidate](https://github.com/grandchallenge/MATH-PROGRAMME/blob/ad3af43cde619070803071ab18d244cbb824e872/research/condensed-qft/EXT-015/R2_FULL_DOUBLE_BRIDGE_LOCAL_FOREST_057.md), branch head \`ad3af43cde619070803071ab18d244cbb824e872\`, Markdown blob \`5c7616b5f24614c92668ac4ba7906dac63b1128b\`. Exact proof equations (57.1)–(57.15) were audited against the public candidate; this audit does not modify that source. The related publication restriction and clearance path are recorded at [CONTROL #50](https://github.com/grandchallenge/CONTROL/issues/50). The research owner remains [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

## 1. Exhaustive finite graph and forest check

The graph has two labeled unit triangles on vertices \`0,1,2\` and \`3,4,5\`, with distinct crossing edges \`03,14\`. Enumerating every proper edge subset and retaining the connected bridgeless subgraphs with a cycle gives precisely ten proper one-particle-irreducible sources. Their edge-count multiplicities are \`3:2,4:1,5:2,6:3,7:2\`. Six have cycle rank one; four have cycle rank two.

Forest compatibility is strict edge-subgraph nesting or **vertex** disjointness, not merely edge-disjointness. There are ten singleton choices, twelve nested two-source choices, and one disjoint pair consisting exactly of the two original triangles; no compatible three-source forest occurs. Together with the empty forest there are **24 proper forests**. This count was regenerated from the graph edges, not entered as a fixed target.

**Decision:** ACCEPT inventory and compatibility enumeration.

## 2. Source-local recursive counterterms

For any source graph $\gamma$ let $h_\gamma=|E_\gamma|-|V_\gamma|+1$ and $\tau(\gamma)$ denote its unit-weight spanning-tree sum. The normalized Gaussian coefficient is $(2\pi)^{-h_\gamma/2}\tau(\gamma)^{-1/2}$. The proper-source recursion in equation (57.5) uses counterterms of strictly smaller *intrinsic source graphs*, never coefficients recalibrated to their containing graph.

For the four two-loop proper sources, each contains three mutually overlapping proper one-loop cycles and **no disjoint child pair**. Computing every quotient graph by exact vertex contraction, preserving loop edges as smooth Gaussian factors, gives source-child quotient tree sums:

- each $\tau=11$ source: child counts \`(3,2,1)\`, paired with source-cycle lengths \`(3,4,5)\`;
- each $\tau=14$ source: child counts \`(4,2,1)\`, paired with source-cycle lengths \`(3,5,6)\`.

Therefore the **equations** (57.5) and (57.6) are correct. But the sentence in the manuscript's proof beginning *Source-level contraction gives the quotient spanning-tree values* incorrectly prints \`(3,8,5)\` and \`(6,10,12)\`. Those figures must be replaced by the source-child counts above. The old figures cannot be justified as tree sums for those quotient graphs.

**Decision:** ACCEPT formulas (57.5)–(57.6) with a mandatory one-sentence prose correction. Reject the draft as editorially final while the false counts remain.

## 3. Full forest and derivative counterterm audit

The original six-vertex graph has $\tau(G)=30$. The ordered quotient tree sums for its ten proper 1PI sources are exactly \`(8,8,4,2,2,2,2,1,1,1)\`; the unique disjoint pair has quotient tree sum two. These *full-graph quotient* counts must not be confused with the *source-child quotient* counts of Section 2.

The full forest preparation contains a negative contribution for each of ten singleton source counterterms, a positive contribution for the one disjoint pair, and the twelve nested terms already represented in recursively prepared proper two-loop source coefficients. Explicitly adding those nested terms once again would double count them. The exact-arithmetic regression evaluates the scalar coefficient in (57.12) as

$$
\mathfrak a_G=
\frac14+\frac{\sqrt2}{2}+\frac{\sqrt3}{3}
+\frac{\sqrt{10}}5+\frac{\sqrt{30}}{30}
-\frac{\sqrt{14}}7-\frac{\sqrt{22}}{11}
$$

and the first diagonal of the local second-derivative coefficient matrix in (57.13) as

$$
(\mathfrak B_G)_{00}
=-\frac{5\sqrt6}{96}
+\frac{\sqrt2}{24}
+\frac{7\sqrt{30}}{600}.
$$

Both are nonzero. Exact rational quotient covariances yield a symmetric five-by-five derivative matrix, not a scalar substitute.

Each prepared term is a normalized centered Gaussian on the quotient collision space, multiplied by a fixed Laurent scale. Taylor expansion against compactly supported smooth tests has only the $\epsilon^{-3}$ scalar and $\epsilon^{-1}$ second-derivative negative orders; parity excludes $\epsilon^{-2}$ and $\epsilon^0$ for the full rank-three graph. Gaussian moment bounds yield an $O(\epsilon)$ strong-distribution remainder after subtracting the two exact full-diagonal counterterms. This reasoning is **specific to the fixed unit Gaussian delta-edge model**, not an assertion of a general BV/QME or Costello–Gwilliam B.6 theorem.

**Decision:** ACCEPT the bounded theorem's full-graph coefficients and limit under the stated Gaussian model.

## 4. Authenticated replay, review provenance and release boundary

The new stand-alone [R2/057 exact regression](fixtures/check_full_double_bridge_forest_057.py) uses standard-library Python only: \`Fraction\` coefficients in a squarefree-radical basis; exhaustive 1PI and forest enumeration; exact quotient contractions, determinants, inverses and covariance embeddings. Authenticated CHAD read-only execution of the **published fixture candidate branch** returned PASS for the source recursion, all 24 forests, all quotient determinants, the seven-radical overall scalar and the full symmetric derivative matrix.

The critical assessment is a separate **logical review pass**, not an independent human/agent GitHub identity, an external referee, or a certificate by MATHCERT. It is explicitly source-locked to the **uncorrected** research head cited above. An additional exact-head critical appraisal of the corrected manuscript remains applicable once the source correction is genuinely authorized and published.

The fixture and this audit are **separate verification artifacts**. Neither performs, replaces, disguises or resubmits the previously denied manuscript \`update_file\` operation. Their protected admission does not imply that R2/057 has merged.

## 5. Final disposition

**CONDITIONAL ACCEPT as a bounded mathematical result; DO NOT mark R2/057 protected-admitted.** Outstanding conditions: (1) legitimately clear the specifically held manuscript correction; (2) amend that one sentence while preserving source identities and the correct equations; (3) review the exact corrected source and pass relevant validations; (4) protected-merge the corrected manuscript and review and verify protected \`main\` readback.

The larger mathematical obligations, including general mixed Wick/delta forest naturality, global BV and QME, normal-topology Weiss descent and liquid Ext, remain separately OPEN.