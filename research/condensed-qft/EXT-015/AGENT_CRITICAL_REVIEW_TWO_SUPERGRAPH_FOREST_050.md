# EXT-015 REACH / 050 — adversarial mathematical audit of the first two-supergraph forest theorem

**Distinct logical GCL mathematical critic, not an external referee or second GitHub identity.** Audited candidate [R2/049](R2_TWO_SUPERGRAPH_LOCAL_FOREST_049.md), exact author PR [#2835](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2835), source head \`4710e36f5cf1426742c6d5f2c878df929e72fc70\`, and fixture [049](fixtures/check_two_supergraph_forest_049.py). The mathematical audit is source-locked. No review conclusion below implies global Bogoliubov/Zimmermann coherence, a renormalized BV coderivation or interacting quantum field theory.

## 1. Independent finite-inventory and intrinsic-source check

**Theta graph:** For $E=\{12,23,13,24,34\}$, all proper 1PI cyclic edge subsets consist exactly of two triangles and the four-edge square. Each pair shares an edge, so the proper forests are empty or a singleton. The four-edge square spans the whole vertex set but is still a proper edge subgraph because the chord $23$ is excluded. Cyclic edge subsets with appended bridge edges are not additional 1PI objects.

**Parallel-edge triangle:** With labeled parallel edges $a,b$ joining $1,2$ and other edges $23,13$, the proper 1PI inventory is precisely the two labeled triangles and the two-edge parallel bubble. Each pair overlaps. Omitting the bubble would give a false overlapping-subgraph preparation.

The source cycle counterterms depend only on the isolated 1PI subgraph:
- Gaussian two-edge parallel bubble coefficient $b_2=1/(2\sqrt\pi)$.
- Gaussian triangle coefficient $c_3=1/\sqrt{6\pi}$.
- Gaussian square coefficient $c_4=1/\sqrt{8\pi}$.

The triangle counterterm is the **same** distribution $(c_3/\epsilon)\delta_\triangle$ in the two supergraphs. Only after embedding into a larger graph are the **other, still-regulated smooth edge factors** multiplied in. This distinction is mathematically essential: supergraph independence applies to the subgraph counterterm assignment, not to its insertion after multiplication by the complement.

**Disposition:** ACCEPT the exact cycle inventory and counterterm source-independence for these two supergraphs. No assertion for arbitrary multigraphs has been checked.

## 2. Recompute theta normalization and finite residue independently

In tree differences $(u,v,w)$, the five-edge exponent has reduced precision

$$
Q_\Theta=
\begin{pmatrix}2&1&0\\1&3&1\\0&1&2\end{pmatrix},\qquad
Q_\Theta^{-1}=
\begin{pmatrix}5/8&-1/4&1/8\\-1/4&1/2&-1/4\\1/8&-1/4&5/8\end{pmatrix}.
\tag{50.1}
$$

Its determinant equals eight, and the original five Gaussian edges have cycle rank two. Therefore the bare leading term is $c_\Theta\epsilon^{-2}\delta_\Theta$, with $c_\Theta=1/(4\sqrt2\pi)$. The theta triangles leave two identical uncontracted Gaussians at the remaining relative variable, so each creates a leading $c_3b_2\epsilon^{-2}\delta_\Theta$ pole and the finite term $(c_3b_{2,2}/2)$ times the relevant pure second-derivative delta. The square subgraph collapses all four vertices and evaluates the remaining chord exactly at the diagonal, producing $c_4\kappa(0)\epsilon^{-2}\delta_\Theta$ with **no** second-derivative finite term.

Subtracting the three proper-cycle terms leaves the overall local pole

$$
g_\Theta=\frac1\pi
\left(\frac1{4\sqrt2}-\frac1{\sqrt6}-\frac14\right).
\tag{50.2}
$$

It is generally negative: proper counterterms can over-subtract the positive bare leading coefficient. Subtracting $g_\Theta\epsilon^{-2}\delta_\Theta$ cancels the only surviving negative order. The finite derivative distribution in (49.15) follows. On a test equal to $u^2$ near the collision locus, the result is exactly

$$
\frac1\pi\left(\frac5{32\sqrt2}-\frac1{4\sqrt6}\right).
\tag{50.3}
$$

No conclusion about physical positivity of renormalized distributions follows from the sign of these local coefficients.

## 3. Recompute the parallel-edge triangle independently

Here the four-edge exponent is $2u^2+v^2+(u+v)^2$, with precision

$$
Q_\Pi=\begin{pmatrix}3&1\\1&2\end{pmatrix},
\qquad Q_\Pi^{-1}
=\begin{pmatrix}2/5&-1/5\\-1/5&3/5\end{pmatrix}.
\tag{50.4}
$$

Its determinant is five, cycle rank two, and bare coefficient $c_\Pi=1/(2\pi\sqrt5)$. Each triangle counterterm collapses all three vertices, leaving the other parallel Gaussian at zero. Thus the two triangles contribute exactly $2c_3\kappa(0)\epsilon^{-2}\delta_\Pi$ and have **no** finite derivatives. The bubble collapse $\delta(u)$ leaves the two other edges both equal to the same regulated function of $v$, producing $\kappa_\epsilon(v)^2$. Its leading coefficient is $b_2^2\epsilon^{-2}\delta_\Pi$; its finite derivative is $(b_2b_{2,2}/2)\partial_v^2\delta_\Pi$.

The overall prepared pole is therefore

$$
g_\Pi=\frac1\pi
\left(\frac1{2\sqrt5}-\frac1{\sqrt3}-\frac14\right).
\tag{50.5}
$$

The finite residue on a test equal to $v^2$ near the collision locus is exactly

$$
\frac1\pi\left(\frac3{10\sqrt5}-\frac18\right).
\tag{50.6}
$$

The intrinsic triangle coefficient agrees with the theta case, whereas the graph-specific overall coefficient differs. This is precisely the intended locality comparison.

**Disposition:** ACCEPT Theorem 49.1 for the two named Gaussian supergraphs, with Gaussian regulator scheme and explicit relative-coordinate/delta normalizations.

## 4. Analytic remainder and allowed multiplication check

Every bare graph is a normalized Gaussian with a scalar $\epsilon^{-2}$ factor. Its centered odd moments vanish and its fourth-order Taylor remainder after keeping the second-order term is $O(\epsilon^2)$ against a fixed compact-supported bounded test family. Each proper subgraph insertion multiplies a delta distribution by **positive-regulator smooth** factors only. Its remaining factor is either $\kappa_\epsilon(z)^2$, whose second centered moment is finite, or a value $\kappa_\epsilon(0)$ times a full-diagonal delta. Hence every formal product used is a well-defined distribution at positive regulator scale. No $\delta(v)^2$ or product of distinct overlapping diagonal counterterms is formed.

The local overall $g_G\epsilon^{-2}\delta_G$ cancels every remaining negative-order term, leaving a strong limit. Source-local cycle counterterms are supported on the proper cycle diagonal; the graph-specific overall subtraction is supported on the full vertex collision diagonal. These are compatible with the stated **bounded notion of locality**.

**Hostile scope distinction:** A proof of cancellation for two supergraphs does not imply a general forest-prescription theorem. The counterterms for these source cycles have not yet been propagated through *all* distinct overlapping supergraphs, nor does the proof verify that overlapping nested forests in a six-edge graph cancel according to a universal recursion. "Same c3 in two supergraphs" is a real test but not a complete naturality theorem.

## 5. Nesting within a bridge-tree extension

The cyclic core has a renormalized family $R_{G,\epsilon}$ with a strong limit $L_G$ after its proper-cycle forest preparation and its own overall counterterm. Attaching a finite tree of normalized Gaussian bridge edges creates independent relative-coordinate factors with mass one. Their tensor product tends strongly to the corresponding product of Dirac deltas, and the distributional tensor product is hypocontinuous on bounded families of compact test functions. Consequently the full family converges to $L_G$ tensored with the bridge deltas, with no new bridge-associated negative power.

This is a **nested insertion** of previously renormalized cyclic cores inside a graph with only bridge extensions. It does not claim that the raw global finite part of the unprepared attached graph equals the prepared family; that equality need not hold because intermediate Laurent coefficients matter, as independently shown in R2/046.

**Disposition:** ACCEPT Proposition 49.2 under its exact bridge-tree hypothesis. It does not solve new cycle-creating overlaps.

## 6. Independent review verdict and the next obligation

The exact rational/surd fixture [049](fixtures/check_two_supergraph_forest_049.py) passed on authenticated CHAD: both three-cycle inventories, both precision matrix determinants/inverses, cancellation of both overall poles, the two finite test pairings and 11 symbolic attached-bridge cases. The fixture is a regression control; the source proofs supply the smooth Gaussian distributional convergence.

**Bounded ACCEPT:** R2/049 Theorem 49.1 and Proposition 49.2 provide genuine mathematics: *proper-subgraph* source-independent subtraction verified in two inequivalent overlapping supergraphs plus compatible nested bridge extension.

**OPEN:** (i) universal 1PI forest recursion on arbitrary graphs; (ii) counterterm closure under new cycle-creating insertions, including overlapping **higher** 1PI supergraphs; (iii) derivative-delta subgraph counterterms compatible with factor-local Wick-to-delta identities; (iv) globally defined BV second-order operator/nilpotence and interacting QME; (v) completed B.6 Weiss and original liquid higher-Ext.

**Next exact test:** add edge $14$ to theta (the complete graph $K_4$); list all **proper 1PI divergent subgraphs**, including higher-loop edge subsets. Test nested forests containing the theta subgraph and the other overlapping 1PI subgraphs, and determine whether its prepared overall subtraction is independent of whether the theta occurs alone, in the resulting $K_4$, or within a bridge extension. A positive exact forest recursion or an explicit counterexample should be accepted as scientific progress.

**Governance:** Source-locked GCL critic under one authenticated account, not an impersonated independent external specialist. Publish through protected PR queue and verify exact branch/source readback. Parent #2797 remains OPEN.