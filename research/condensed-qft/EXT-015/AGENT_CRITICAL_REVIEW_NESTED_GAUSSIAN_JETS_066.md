# EXT-015 REACH / 066 — exact-head critical audit of the nested K4–five-vertex–six-vertex Gaussian forest

**Verdict:** BOUNDED ACCEPT of the finite nested-Gaussian graph theorem, subject to protected admission. This is a distinct logical GCL mathematical critic pass, using the established one-authentication role-scoped model, **not** an independent external referee or MATHCERT certificate.

**Exact source identity:** [R2/065 candidate PR #2864](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2864), exact author HEAD \`5a882ad2402c4aa8f4258ae6610e93e9cd9c41ec\`; proof blob \`f02fd14d6d3154e11c63f3b9d2263c762226fec3\`; [exact executable fixture](fixtures/check_nested_gaussian_jet_forest_065.py) blob \`99b34aa6bfc3d864e7a3d9d738ccf5c646eff1d5\`. The proof and fixture at those identities are the material reviewed.

## 1. What was tested, and which broader claims are excluded

The graph chain is a complete four-vertex K4 on edge set $01,02,03,12,13,23$, with five-vertex source $F=K4\cup\{04,14\}$ and six-vertex host $G=F\cup\{05,15\}$. All are fixed, labeled, unit Gaussian one-dimensional delta-edge graphs. They have cycle ranks three, four and five. Crucially, the source K4 has an *intrinsic prepared derivative counterterm* before its insertion into $F$, and the preparation of $F$ has a further *intrinsic prepared second-derivative counterterm* before its insertion into $G$.

Review exclusions: (a) a single smooth-complement Leibniz identity mistaken for a two-level nested singular-source forest; (b) treating vertex-sharing sources as disjoint; (c) double-subtracting nested children already in a prepared source; (d) omitting the Taylor derivative of the complement Gaussian when a delta derivative is inserted; (e) confusing a nonzero coefficient on one polynomial probe with validation of the other coefficients; (f) claiming a general all-graph forest construction or an overlapping-nonnested singular-source compatibility result.

## 2. Independent graph and forest verification

Take the reduced Laplacian of each graph with root 0. The exact matrix-tree determinants are

$$
\tau(K4)=16,\quad \tau(F)=40,\quad \tau(G)=96.
\tag{66.1}
$$

Exhaustive proper edge-subset enumeration gives 85 proper 1PI connected bridgeless subgraphs in the six-vertex graph, with cycle-rank multiplicities

$$
(h=1,2,3,4)\longmapsto(18,35,24,8).
\tag{66.2}
$$

An important hostile test is to compare **vertex sets** of every pair of proper 1PI sources. No disjoint vertex sets occur in this graph, even if some edge sets are disjoint. Thus allowed forests consist of strict chains, not products of falsely deemed edge-disjoint counterterms.

Their chain-length counts are exactly

$$
(\#\mathcal F_0,\#\mathcal F_1,\#\mathcal F_2,
\#\mathcal F_3,\#\mathcal F_4)
=(1,85,605,1179,672).
\tag{66.3}
$$

The sum is 2542. This enumeration is not inferred from the tree counts alone; it is independently reconstructed by strict edge-set nesting in the exact standard-library fixture.

**Verdict:** ACCEPT full proper source and compatible forest inventory for this fixed graph.

## 3. Check of recursive local jet subtraction, including signs

For each intrinsic 1PI source $\gamma$, its regulated bare Gaussian factor has cycle rank $h_\gamma$ and covariance $\epsilon^2Q_\gamma^{-1}$. Its local negative-power expansion contains exactly the even monomial jets of degree $|\alpha|<h_\gamma$. Since the independent relative coordinates may be chosen differently for different sources, inserting a proper source $\beta$ requires an explicit linear change from parent coordinates to normal variables $u$ of $\beta$ and quotient variables $q$. It is not generally valid to treat parent monomial $y^\alpha$ as a polynomial solely in $q$.

The source recurrence evaluated in the fixture and the proof is: bare $\gamma$ moments minus *immediate prepared-source insertions* of each proper 1PI $\beta$. Here “immediate” means the outermost source in a forest, **not** only maximal edge-count sources. Each prepared $\beta$ coefficient already contains all shorter chains inside $\beta$, and thus induction enumerates every strict forest chain exactly once.

For insertion of a normal delta monomial, the correct coefficient is extracted from

$$
\exp\!\left[
-\tfrac12 u^TA_{\gamma|\beta}u
-u^TB_{\gamma|\beta}q\right]\Phi_\alpha(u,q),
\tag{66.4}
$$

then integrated against the quotient Gaussian covariance $D_{\gamma|\beta}^{-1}$. A missing first normal derivative of the smooth complement would remove terms linear in $u$ and break the calculation. A missing normal Hessian would remove quadratic $u$ terms and incorrectly erase nested K4 derivative contacts. The fixture evaluates those linear and quadratic Taylor contributions exactly, using rational Wick contractions with source coefficients in a rational squarefree-radical basis.

The signs of derivative counterterms follow from evaluation of positive-regulator Gaussian tests by even-order delta derivatives. The *prepared source scalar or derivative coefficients themselves* may have negative signs; no artificial positivity condition was assumed.

**Verdict:** ACCEPT source-intrinsic preparation recurrence and exact Gaussian normal-jet insertion as bounded finite graph identities. This is not an extension to products of singular distributions on overlapping nonnested collision diagonals.

## 4. Hostile derivative-bearing five-vertex source

The inherited K4 source recovers the independently protected moments

$$
m_{K4,0}
=\frac5{12}-\frac{3\sqrt2}{2}+2\sqrt6,
\quad m_{K4,(1,1)}=-\frac7{72},
\quad m_{K4,(1,2)}=-\frac7{144}.
\tag{66.5}
$$

The derivative source term *inserted into the five-vertex proper source* contributes

$$
I_{F\leftarrow K4,(1,1)}=-\frac{7\sqrt2}{144}.
\tag{66.6}
$$

After all **36** proper sources of $F$ are prepared (including their own nested chains), the independently source-determined five-vertex second moment is

$$
\boxed{
b_F=\frac{\sqrt{10}}{50}
-\frac{52\sqrt{21}}{441}
+\frac{7\sqrt2}{144}
-\frac{\sqrt5}{25}
+\frac{4\sqrt{15}}{25}
-\frac{\sqrt6}{18}<0.
}
\tag{66.7}
$$

The strict negativity is certified by integer rational enclosing square-root bounds; it is not a numerical near-zero assumption. The nonzero intrinsic second-normal delta coefficient of $F$ is therefore unavoidable in the fixed pole-only subtraction convention.

In the host $G$, integrating the two smooth tip edges $05,15$ over the quotient coordinate gives

$$
f_\epsilon(y_1)=
\frac{1}{2\sqrt\pi\,\epsilon}
e^{-y_1^2/(4\epsilon^2)},\quad
f_\epsilon''(0)=-\frac{1}{4\sqrt\pi}\epsilon^{-3}.
\tag{66.8}
$$

The $\partial_{y_1}^2\delta_F$ term of the five-vertex source has coefficient $(2\pi)^{-2}(b_F/2)\epsilon^{-2}$. Its scalar Leibniz correction is consequently

$$
(2\pi)^{-2}\frac{b_F}{2}\epsilon^{-2}f_\epsilon''(0)
=-\frac{b_F}{32\pi^{5/2}}\epsilon^{-5}.
\tag{66.9}
$$

Because $b_F<0$, this correction is positive. It differs both in source identity and normalization from the earlier single-K4 edge contacts R2/059 and R2/061. **This is the first reviewed second-level nested differentiated-source contact in this thread**, not the first occurrence of a delta-jet times a smooth Gaussian.

**Verdict:** ACCEPT five-vertex intrinsic source differentiation and its nested six-vertex contact.

## 5. Adversarial fourth-moment test on the complete six-vertex host

For $G$, $h_G=5$ and there are five independent normal coordinates. The only negative Laurent orders are

$$
\epsilon^{-5}\delta_G,\quad
\epsilon^{-3}\partial_y^2\delta_G,\quad
\epsilon^{-1}\partial_y^4\delta_G.
\tag{66.10}
$$

The 1+15+70=86 scalar/quadratic/quartic moments in the fixture include all mixed normal derivatives; only checking one diagonal entry would be insufficient.

The corrected exact source recursion gives a nonzero fourth monomial moment

$$
\boxed{
m_{G,(1,1,1,1)}=\frac{\sqrt6}{72}-\frac{\sqrt3}{32}<0.
}
\tag{66.11}
$$

The rational inequality follows because $\sqrt6/72<\sqrt3/32$ is equivalent to $\sqrt2<9/4$. Pair with a smooth compact test agreeing near the collision with $(x_1-x_0)^4$. Lower-order delta jets annihilate this test, while its fourth derivative at the collision is nonzero. The prepared amplitude therefore has an uncancelled order $\epsilon^{-1}$ divergence if a fourth-order subtraction is withheld.

The fixture recomputes and verifies all 86 coefficients, the two graph symmetries $(2\leftrightarrow3)$ and $(4\leftrightarrow5)$, and both strict sign claims using integer square bounds. Its authenticated CHAD execution capture \`807f52d6707c45a98df6c92f7baf7144\` returned all PASS. Mathematical Markdown preflight of the exact author source returned PASS, CHAD capture \`18209ef832c24636a7b68b1ffb905075\`.

Once the three negative orders are subtracted, the next even Gaussian moment scales as $\epsilon^{+1}$, uniformly on bounded compact smooth test families. The Gaussian remainder proof uses the same fixed unit kernels and finitely many quotient graphs; no uniformity over arbitrary graph families is inferred.

**Verdict:** ACCEPT a necessary fourth-derivative *overall* counterterm on this fixed graph; the completed finite subtraction yields the claimed strong distributional $O(\epsilon)$ remainder.

## 6. Overall verdict and exact protected admission conditions

**BOUNDED ACCEPT**: R2/065 proves a complete finite nested singular-source forest in a five-loop six-vertex graph, with K4 derivative source nested inside an intrinsically derivative-bearing five-vertex source, plus a new nonzero fourth-order pole. It advances beyond the previous single-source insertion theorems R2/059–064.

Still **not proved**: a *pair of overlapping nonnested* derivative-bearing source diagonals, arbitrary all-graph BPHZ forest naturality, BV nilpotence, interacting QME, normal-topology Weiss descent, or liquid higher Ext. Keep [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) OPEN.

Protected admission requires [author PR #2864](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2864) to pass and merge first, followed by this exact-head logical critic PR, then independent protected-main readback of the source proof, fixture and review. The logical critic is not self-certifying a GitHub merge by writing this file.
