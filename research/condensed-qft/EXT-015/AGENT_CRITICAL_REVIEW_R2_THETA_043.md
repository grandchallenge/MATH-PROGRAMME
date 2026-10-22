# EXT-015 REACH-R2 / 043 — hostile mathematical audit of overlapping-cycle and delta-jet renormalization

**Distinct logical critic pass; not external certification.** Source-locked author candidate [042](R2_OVERLAPPING_CYCLES_DELTA_JETS_042.md), exact research head \`46d3de72d59d70ec450f581890338348a9361a8b\` on branch \`research/ext015-r2-overlap-theta-042-20261022\`. This review is a separate derivation and identifies both valid bounded claims and the remaining obligations. It does not authorize promotion to a general BPHZ/Epstein–Glaser renormalization theorem or a smooth BV algebra.

## 1. Exhaustive 1PI cycle inventory

For the five-edge theta graph with edge set $\{12,23,13,24,34\}$, an edge subset is a minimal nontrivial cycle precisely when each of its used vertices has degree two and the used subgraph is connected. Enumerating the subsets gives three cycles: $123$, $234$ and $1243$. Their edge counts are $3,3,4$; each pair shares one or more edges. The square cycle spans **all four vertices** but is still a proper edge subgraph because edge $23$ remains outside it.

**Hostile qualification:** There are other proper edge subsets that *contain* a cycle and a pendant edge; these are not additional **1PI** cyclic subgraphs because deleting the pendant edge disconnects them. The source correctly distinguishes these, after an explicit correction. A claim of "exactly three cyclic edge subsets" without the 1PI condition would be false.

The graph has two independent cycles yet three simple cycles. Its cycle rank is two, not three. Treating the three subgraph counterterms as a triple product would be mathematically invalid; the shared collision directions would force powers of identical Dirac deltas.

## 2. Independent scaling derivation

With $u=x_1-x_2$, $v=x_2-x_3$, $w=x_3-x_4$, $s=x_3$, the Jacobian has absolute value one. The five-edge product is

$$
T_\epsilon=\kappa_\epsilon(u)\kappa_\epsilon(v)
\kappa_\epsilon(u+v)\kappa_\epsilon(v+w)\kappa_\epsilon(w).
$$

Set $z=(u,v,w)$ and let $W(z)$ be the product of the five unscaled kernels. Substitution $z=\epsilon y$ gives $\epsilon^{-2}\int W(y)\phi(s,\epsilon y)\,dy\,ds$. Since $\kappa$ is even, the full simultaneous reflection $y\mapsto-y$ leaves $W$ fixed. Hence the first- and third-order moments vanish. The leading divergence is $M_0\epsilon^{-2}\delta_G$ and the *finite* next term is one-half the matrix of second moments acting on second derivatives of the delta. The Taylor remainder has $O(\epsilon^2)$ strong-distribution bound.

This is not merely heuristic power counting: the compact support of the smooth kernel supplies uniform finite moments and uniform test-seminorm control.

## 3. Independent examination of every proper subgraph subtraction

Triangle $A=123$ imposes $u=v=0$. Its two uncontracted edges become two copies of $\kappa_\epsilon(w)$; the insertion is $(c_3/\epsilon)\delta(u)\delta(v)\kappa_\epsilon(w)^2$. It contributes $c_3b_2/\epsilon^2$ to the full-diagonal pole and $(c_3b_{2,2}/2)\partial_w^2\delta_G$ as its finite residue.

Triangle $B=234$ imposes $v=w=0$. Its two remaining factors become $\kappa_\epsilon(u)^2$ and produce the same pole, with finite residue $(c_3b_{2,2}/2)\partial_u^2\delta_G$.

The square $C=1243$ is a four-edge cycle of rank three. Its isolated-cycle counterterm is $(c_4/\epsilon)\delta(u)\delta(v)\delta(w)$. The remaining chord has **exact** value $\kappa_\epsilon(v)|_{v=0}=\kappa(0)/\epsilon$ on that delta, yielding $c_4\kappa(0)/\epsilon^2\delta_G$. Omitting this term is an incorrect subgraph inventory; inserting it changes the overall pole from the naive two-triangle coefficient.

Thus the remaining divergence after the **three separate** insertions is

$$
\epsilon^{-2}\bigl(M_0-2c_3b_2-c_4\kappa(0)\bigr)\delta_G.
$$

The whole-graph subtraction with exactly this coefficient cancels it. The leftover finite second-derivative distribution is the stated expression. All operations are well-defined at fixed positive $\epsilon$ and the final distributional limit is strong.

**Audit verdict:** ACCEPT Theorem 42.1 for this exact graph, even smooth compact mollifier, displayed subgraph normalization and one-overlap subtraction prescription. Do not extrapolate to arbitrary overlapping nests or canonical forest insertion.

## 4. Exact adversarial box control

For the even box density $\mathbf 1_{(-1,1)}/2$, the weight is constant $1/32$ on

$$
|u|,|v|,|u+v|,|v+w|,|w|\le1.
$$

Conditioning on $|v|=t$ leaves independent $u,w$ intervals of length $2-t$. Therefore $M_0=(1/16)\int_0^1(2-t)^2dt=7/48$; its second moments are exactly

$$
M_{uu}=M_{ww}=13/320,\qquad
M_{vv}=1/30,\qquad
M_{uv}=M_{vw}=-1/60,\qquad M_{uw}=1/120.
$$

The square-cycle coefficient is the origin density of the fourth convolution power of the box; equivalently the $L^2$ norm squared of the triangular two-fold convolution, hence $c_4=1/3$. The triangle coefficient is $3/8$, the box's squared $L^2$ norm is $1/2$, and $\kappa(0)=1/2$. This independently gives the **negative** overall coefficient $-19/48$, which is not an error: subgraph subtractions may exceed the original positive pole.

The finite derivative distribution in (42.15) follows by subtracting the two triangle second moments; the square term has no finite moments after multiplication by its chord. Pairing with the supplied quadratic test polynomial gives $-47/192$ exactly, for every sufficiently small positive regulator scale. The mathematical result uses smooth mollifiers; the box calculation is a deliberately nonsmooth rational control, not a replacement for the distributional proof.

## 5. Nested subdivergence and arbitrary delta jets

For a triangle with an attached leaf, the triangle and remaining edge factors separate in appropriate relative coordinates. The triangle weight is inversion-even, so the difference between its regulated distribution and the local counterterm has vanishing constant and first Taylor terms; the first possible remainder after the $\epsilon^{-1}$ prefactor is $O(\epsilon)$. This proves Proposition 42.2. No additional local pole remains.

For the whole-graph delta-jet theorem, let $n$ be vertex count, $m$ edge count, and $R=\sum_e r_e$ the sum of derivative orders. A spanning-tree linear coordinate change has $n-1$ relative variables; product scaling gives exponent $\omega=m+R-(n-1)$. The weight is compactly supported because spanning-tree edge factors bound each independent difference. The test-function Taylor series to order $\omega$ proves the local subtraction formula and its finite limit, including the sign $(-1)^{|\alpha|}$ dictated by derivatives of delta.

This **does** cover every finite connected graph with arbitrary nonnegative derivative orders as a *whole-diagonal Taylor subtraction*. It **does not** give a local counterterm assignment on every overlapping proper subgraph compatible with all forest identities. Independent edge-jet insertions and vertex derivatives of a full renormalized amplitude are distinct notions; the latter commute with the distributional limit by continuity of differentiation, as correctly restricted in 042.

**Audit verdict:** ACCEPT Proposition 42.2 and Theorem 42.3 within their stated fixed-graph/distributional scopes. Keep the universal subgraph recursion and master equation OPEN.

## 6. Hostile changes of hypothesis and next exact gate

- **Non-even regulator:** If $\kappa$ is not even, the first moments of the full graph and relevant subgraph weights may be nonzero. The $\epsilon^{-1}$ first-derivative delta counterterms can no longer be omitted. Thus evenness is a genuine theorem hypothesis, not aesthetic convenience.
- **Graphwise versus global consistency:** The whole-graph Taylor prescription always provides a finite local limit but may fail consistency when the same subgraph appears inside different supergraphs. Nothing in 042 yet proves a universal character, Hopf-algebra antipode identity, insertion homomorphism, or all-scheme cocycle.
- **Operator question:** Finite graphwise distributional amplitudes do not automatically define a second-order BV operator preserving a specified domain under every composition. This remains the central missing bridge.
- **Topology:** Strong convergence against test functions does not imply a Costello–Gwilliam B.6 equivalence, normal-cone smooth exterior products, or full Weiss descent.

**Next theorem to attempt:** define a universal subgraph-local subtraction operator respecting the inclusion-poset of singular subgraphs, prove it satisfies composition and overlap/nesting identities on a class larger than the single theta graph, and then check the induced BV differential/bracket and quantum master equation. A counterexample to consistency is equally acceptable if exhibited in exact distributions.

## 7. Status and provenance

**Bounded mathematical verdict:** Theorems 42.1 and 42.3 and Proposition 42.2 ACCEPT as internally checked **candidates**, not externally certified or protected-admitted. Exact rational fixture and source Markdown preflight have passed on the authenticated CHAD runner at branch head \`46d3de72d59d70ec450f581890338348a9361a8b\`. Research source [042](R2_OVERLAPPING_CYCLES_DELTA_JETS_042.md), test [042](fixtures/check_overlapping_cycle_subtractions_042.py). The earlier platform safety hold for PR creation of R2/041 remains [CONTROL #44](https://github.com/grandchallenge/CONTROL/issues/44); this review does not request the blocked operation again. Research obligation #2797 stays OPEN.
