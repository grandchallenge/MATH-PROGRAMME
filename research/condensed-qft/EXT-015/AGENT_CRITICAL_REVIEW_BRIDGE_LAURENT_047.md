# EXT-015 REACH-R2 / 047 — source-locked mathematical critical review of associative bridge Laurent gluing

**Reviewer provenance:** Separate GCL logical mathematical critic pass against [R2/046 candidate PR #2831](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2831), exact candidate head \`b0a1d919f5a57066fb60f951a30987150be92337\`. Same authenticated GitHub actor; this does **not** constitute an externally authenticated referee or independent MATHCERT certification. Review is of theorem logic and counterexamples, separate from source authoring. The protected research predecessor is R2/044–045 on main.

## A. Hostile test of the bridge-coordinate change

Let $G_1,\ldots,G_q$ be disjoint connected delta subgraphs. If the quotient of their vertex sets after adding bridges is a tree, choose one global vertex root. Within each component choose differences to an internal vertex root; for each bridge choose the **actual endpoint difference**, not simply the difference of component roots. Because the bridge quotient is a tree, starting at the global root one can recover the root of each adjacent component using its parent's root, its internal endpoint displacement, and the bridge endpoint difference. This recursively gives a bijective *integer* linear coordinate transformation. Ordering the recovery by tree depth gives a triangular matrix with unit diagonal, hence determinant $\pm1$.

Thus the volume normalization in 046 is valid, and all internal kernels depend only on their own component differences while each bridge kernel depends only on its assigned bridge coordinate. A cyclic quotient would defeat this independence, so the restriction to bridge trees is essential, not cosmetic. Internal blocks may themselves contain arbitrarily many cycles.

**Disposition:** ACCEPT the coordinate decomposition for any finite tree of connected subgraphs.

## B. Gaussian exactness, singular Wick bridge and strong asymptotics

A connected internal Gaussian delta subgraph with cycle rank $h_i$ has the exact normalized density form $c_i\epsilon^{-h_i}\rho_{\epsilon,Q_i}$; R2/044 independently established its constant $c_i$. The heat semigroup on the corresponding delta diagonal produces this normalized Gaussian distribution. On a delta bridge, the one-dimensional heat semigroup sends $\delta$ to $\kappa_{\epsilon,w}$. On a Wick bridge, the **same semigroup** sends $P_0=|t|/2$ to its smooth convolution $P_{\epsilon,w}$. This is a valid exact identity in tempered distributions for each positive $\epsilon$, even if a bridge is Wick-type and there is no spanning globally delta-connected graph.

The separate variables guarantee that the total product is the exterior tensor product of well-defined distributions. Finite test-Taylor expansions and Gaussian moment bounds give coefficientwise asymptotics in even powers of $\epsilon$. Applying heat to the cusp $P_0$ gives a polynomially bounded tempered distribution; its derivatives include ordinary Dirac distributions but no need to evaluate a singular distribution at an individual collision point. The distinction correctly resolves the earlier moving-atom scalar cusp obstruction: *smooth distribution outputs* are not scalar point evaluations.

Since the internal-block factors contribute $\epsilon^{-h_i}$ and the normalized bridges contribute no independent power after keeping their coordinate unscaled, the total pole is $H=\sum_i h_i$. This is not the same as the scaling exponent obtained by forcing **all** relative variables into one small diagonal; Wick bridge variables are genuinely free externally.

**Disposition:** ACCEPT the exact heat identity and strong Laurent asymptotic expansion for the bounded Gaussian block-tree category. The finite-part local counterterms need not have support on the full vertex diagonal when a Wick bridge is present; they are instead supported on component collision strata, as explicitly stated in the source.

## C. Rigorous gluing associativity and what it does not prove

A Laurent series bounded below has only finitely many decompositions of any fixed exponent into sums of exponents from finitely many such series. Its Cauchy product is therefore well-defined and associative. Distinct graph-block variables have canonical exterior tensor products and all bridge variables are independent. A choice of gluing tree root changes only the unimodular coordinate parametrization of the **same** regulated distribution. Equality of its asymptotic coefficients then establishes composition independence.

**Hostile limitation:** Associativity is obtained only by retaining the **whole Laurent state** until all bridge insertions have been performed, and projecting to the coefficient of $\epsilon^0$ at the end. The finite-part projection is not multiplicative. The candidate correctly does not claim a universal category of arbitrary graph gluing: adding an edge that creates a cycle is not a bridge and can create overlapping singular subgraphs, the central unsolved research obligation.

**Disposition:** ACCEPT Theorem 46.3 within the bridge-tree class. REJECT any interpretation that it proves the universal Zimmermann forest recursion.

## D. Explicit two-triangle anomalous finite part and its correction

For two unit triangles with a unit Gaussian bridge, the graph has six vertices, seven edges, five independent relative coordinates and cycle rank two. The weighted spanning-tree count is $3\cdot3=9$. Its scalar normalization is therefore $c=1/(6\pi)$. The two internal triangle variances along the selected long-distance path are each $2/3$; the bridge variance is one. Their sum is $7/3$, also obtained as the inverse reduced full-graph Laplacian's entry for $x_0-x_5$.

The finite-part pairing with a local quadratic test $(x_0-x_5)^2$ and normalized global root factor is exactly

$$
\frac1{6\pi}\cdot\frac73=\frac7{18\pi}.
\tag{47.1}
$$

Each triangle separately has odd cycle rank, so its Gaussian finite part is zero. Therefore applying a naive gluing operation **only** to the individually renormalized values would give zero. The missing terms come from three positive-order Gaussian moments pairing with the corresponding negative powers in the other factors. This shows an explicit finite-part *gluing defect*, not a physical QME anomaly or proof of inconsistency of renormalization generally.

For four unit triangles linked in a chain of delta bridges, total cycle rank four and scalar normalization $1/(36\pi^2)$. Pairing with the bridge-coordinate polynomial $t_1^2t_2^2$ gives precisely that nonzero finite part while each separate triangle again has zero. This independently falsifies any binary finite-part-only gluing model.

**Disposition:** ACCEPT (46.11)–(46.15) under the stated Gaussian scheme and normalized tests.

## E. Free Wick-to-delta bridge relation beyond a globally connected delta backbone

The core identity is $P_{\epsilon,w}''=\kappa_{\epsilon,w}$. In the heat-semigroup normal form the same scalar factor, heat operator and exponent occur for either edge choice. Only its base distribution is changed, from $P_0$ to $\delta$. Because the bridge derivative $\partial_{t_e}^2$ commutes with every constant-coefficient second derivative in the heat operator, it commutes with all Laurent coefficients and the final coefficient extraction.

The nonzero two-triangle Wick finite part is

$$
\frac1{12\pi}
\left[
(\mathcal L_A+\mathcal L_B)(\delta_A\boxtimes\delta_B)\boxtimes P_0(t)
+(\delta_A\boxtimes\delta_B)\boxtimes\delta(t)
\right].
\tag{47.2}
$$

Differentiating twice in $t$ gives the two triangle-internal second derivative terms tensored with $\delta(t)$, plus $\delta_A\boxtimes\delta_B\boxtimes\delta''(t)$; precisely the delta-bridge finite part. This checks a nontrivial **free edge-level BV relation after gluing** without a connected pre-existing delta backbone, and is stronger than the corresponding restricted claim of R2/044.

**Adversarial scope:** This proves neither a globally defined second-order BV operator, $\Delta^2=0$ on every renormalized graph composition, the quantum master equation, nor higher-order interacting contractions. An additional cycle-creating edge may break the coordinate separation and the proof. The next mathematical obligation is precisely the nonbridge insertion extension or a concrete obstruction.

**Disposition:** ACCEPT Theorem 46.4 as a bounded free graphwise identity.

## F. Final review status

| Claim | Verdict |
| --- | --- |
| Bridge-coordinate unimodular decomposition | ACCEPT, quotient tree mandatory |
| Exact distributional heat identity and full Laurent germ | ACCEPT, Gaussian blocks and bridges |
| Associative gluing of Laurent *states* | ACCEPT, bridge tree only |
| Local/partial-diagonal finite-part subtraction | ACCEPT, dependent on Gaussian scheme |
| Two- and four-triangle finite-part insertion defects | ACCEPT, normalized exact witnesses |
| Free Wick/BV bridge conversion identity | ACCEPT, edge-level only |
| Universal overlapping-subgraph forest recursion and full BV/QME | OPEN |
| Differentiable Costello–Gwilliam B.6 and liquid Ext | OPEN |

**Verification boundary:** The exact-standard-library fixture [046](fixtures/check_bridge_laurent_046.py) exercises weighted Laplacian and bridge determinants, graph variance, coefficientwise Laurent convolution, four-triangle witness and the formal Wick-to-delta conversion. A computer pass is arithmetic evidence, not a substitute for the distributional proofs above. Protected validation and exact-main readback are still required. This mathematical role check is not an independent human referee.

**Next experimental/theorem decision:** introduce a single cycle-creating additional edge between previously bridged blocks. Its kernel couples previously independent Gaussian coordinates, and a candidate universal counterterm must reconcile the bridge-state Laurent composition with the cycle-subgraph renormalization in 042. Either prove a consistent overlap recursion on that first mixed graph or exhibit a computable obstruction with explicit surviving delta derivatives.

**Parent:** [EXT-015 R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) remains OPEN.