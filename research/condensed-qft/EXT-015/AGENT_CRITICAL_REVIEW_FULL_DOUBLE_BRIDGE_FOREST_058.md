# EXT-015 REACH / 058 — exact-head critical mathematical review of R2/057

**Logical GCL mathematical critic; bounded ACCEPT, not an external referee or a MATHCERT certificate.** This critique is source-locked to corrected [R2/057](R2_FULL_DOUBLE_BRIDGE_LOCAL_FOREST_057.md), [source PR #2855](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2855), **exact corrected source HEAD** \`243e89d6f6d2e4e86949f73a2d4894142ff250ba\`, Markdown blob \`2e07802262f44d16f5e1d33197216f77b235b2fd\`, and complete corrected source SHA256 \`54c1446f5fbffa37aa79abc4053c9e444e583482a3387484ba94b5e4f6bfc4c8\`. Prior source-locked conditional audit [057 evidence](AGENT_SOURCE_AUDIT_FULL_DOUBLE_BRIDGE_057.md) and [exact regression fixture](fixtures/check_full_double_bridge_forest_057.py) are protected-admitted on main via [PR #2854](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2854). The original incorrect quotient-count sentence has now been corrected on the exact source branch and verified by committed-file readback.

## 1. Hostile source correction and normalization check

The entire correction is a **single sentence-level mathematical explanation**, not an unreported change to theorem assumptions, recurrences, constants or regulator. Previously the source proof for Lemma 57.2 confused *proper two-loop subgraph contracted-child* spanning-tree determinants with other graph-level numbers. The corrected source now gives the child quotient determinants:

- Each proper two-loop $\tau=11$ source: three proper cyclic children, with quotient tree counts $(3,2,1)$ for triangle, square and five-cycle sources, respectively.
- Each proper two-loop $\tau=14$ source: three proper cyclic children, with quotient tree counts $(4,2,1)$ for triangle, five-cycle and six-cycle sources, respectively.

The source-local scalar recursion

$$
a_\gamma=\tau(\gamma)^{-1/2}
-\sum_{\beta\subsetneq\gamma,\ \beta\mathrm{\ 1PI}}
a_\beta\,\tau(\gamma/\beta)^{-1/2}
\tag{58.1}
$$

then yields exactly

$$
\begin{aligned}
a_F=a_H&=\frac{1}{\sqrt{11}}-\frac13
-\frac1{\sqrt8}-\frac1{\sqrt5},\\
a_J=a_K&=\frac1{\sqrt{14}}-\frac1{\sqrt6}
-\frac1{\sqrt{10}}-\frac1{2\sqrt3}.
\end{aligned}
\tag{58.2}
$$

These values depend on intrinsic proper source graphs and their quotient graphs, not the containing six-vertex graph. The positive or negative signs of prepared counterterms are not positivity claims about physical amplitudes.

**Disposition:** ACCEPT the corrected proof explanation and intrinsic scalar recurrence. The erroneous $(3,8,5)$ and $(6,10,12)$ source-child counts must not reappear in any admitted statement.

## 2. Exhaustive compatibility and inclusion-exclusion

The fixed eight-edge six-vertex graph comprises triangles on $\{0,1,2\}$ and $\{3,4,5\}$ and crossing edges $03,14$. Enumerating each proper edge subset and requiring connectedness after removing any of its own edges gives exactly **10 proper 1PI cyclic subgraphs**, with edge cardinalities $3:2,\ 4:1,\ 5:2,\ 6:3,\ 7:2$. There are precisely **12 strict nested pairs**, one **vertex-disjoint** pair consisting of the original two triangles, and no three-member compatible proper forest. Thus there are exactly

$$
1+10+12+1=24
\tag{58.3}
$$

proper forests. Mere disjointness of edge *names* without disjoint vertices is not sufficient for the distinguished disjoint forest.

All nested children of a prepared two-loop source are included in that source's recursively prepared coefficient. They are not multiplied again when its parent source is inserted into the full graph. Conversely, the one disjoint pair contributes its **positive** counterterm product, acting on independent triangle collision coordinates. Omitting that pair would break forest factorization and produce a false scalar pole.

**Disposition:** ACCEPT exact forest enumeration, nesting signs and absence of simultaneous overlapping singular delta products.

## 3. Independent Gaussian and derivative-jet audit

For any connected unit Gaussian delta graph $\gamma$ with cycle rank $h_\gamma$ and spanning-tree sum $\tau_\gamma$, the normalized regulator amplitude is $(2\pi)^{-h_\gamma/2}\tau_\gamma^{-1/2}\epsilon^{-h_\gamma}$ times a centered Gaussian probability density on independent relative coordinates. After contracting each proper source, the quotient remains a Gaussian state with its precision given by the reduced graph Laplacian. The full graph has $\tau(G)=30$; its ten proper-source quotient determinants in the order of the research table are

$$
(8,8,4,2,2,2,2,1,1,1),
\qquad \tau(G/(A\cup B))=2.
\tag{58.4}
$$

These **whole-graph quotient** determinants are different quantities from the corrected proper-source child counts in Section 1.

Expanding the full graph and each legitimate forest insertion through the second centered Gaussian moment yields exactly two divergent powers at cycle rank three: $\epsilon^{-3}\delta_G$ and $\epsilon^{-1}$ times a symmetric matrix of second derivatives of the full-collision delta. The intrinsic scalar and matrix coefficients agree with equations (57.9)–(57.13). In particular, the dimensionless scalar coefficient is

$$
\mathfrak a_G=
\frac14+\frac{\sqrt2}{2}+\frac{\sqrt3}{3}
+\frac{\sqrt{10}}5+\frac{\sqrt{30}}{30}
-\frac{\sqrt{14}}7-\frac{\sqrt{22}}{11}
\tag{58.5}
$$

and the first diagonal entry of the second-derivative coefficient matrix is

$$
(\mathfrak B_G)_{00}
=-\frac{5\sqrt6}{96}+\frac{\sqrt2}{24}
+\frac{7\sqrt{30}}{600}\ne0.
\tag{58.6}
$$

Subtracting *both* local divergent terms leaves a strong distributional $O(\epsilon)$ remainder on bounded compact smooth test families. This uses exact Gaussian tails, even moments and fixed finite graph data; it does not presume arbitrary graph-kernel or BV closure. Subtracting the scalar pole alone fails on suitable quadratic tests.

**Disposition:** ACCEPT the two counterterm Laurent orders and strong finite-limit theorem for the *specified unit Gaussian graph model*.

## 4. Exact-head provenance and independent limits

The original source file was read back after GitHub's exact update: corrected blob \`2e07802262f44d16f5e1d33197216f77b235b2fd\`. The corrected committed source was fetched through authenticated CHAD and passed the mathematical Markdown gate. The exact standard-library fixture protected on main was independently replayed and passed its full 10-source, 24-forest, quotient-determinant, radical and covariance-matrix controls. Authenticated CHAD run \`deba868a658b4220ae4f355b2dd72f34\` recorded those outcomes and the corrected source SHA256 \`54c1446f5fbffa37aa79abc4053c9e444e583482a3387484ba94b5e4f6bfc4c8\`. The fixture still prints an outdated informational note about the former source defect; that note is not a failing assertion and should be corrected separately as documentation hygiene.

This is an independent **logical mathematical critic pass** on the exact updated source, performed under the established GCL same-authentication agent-role model. It must not be described as a separately authenticated external referee or a complete proof certificate. The GitHub protected policy checks and merge-group admission are separate required evidence.

## 5. Final verdict and remaining work

**ACCEPT R2/057 as a bounded proved and exactly tested Gaussian proper-subgraph forest result**, for source and mathematical review admission through the protected programme process. The earlier incorrect explanatory count has been corrected, and the exact committed source matches the separately validated local version byte-for-byte.

Do **not** infer a general all-graph Bogoliubov/BPHZ character or compatibility with arbitrary differentiated delta/Wick cycle insertions, a globally closed BV coderivation or nilpotence, an interacting quantum master equation, Costello–Gwilliam B.6 smooth Weiss descent, or liquid higher Ext. Those questions remain open under [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

**Governed admission conditions:** source PR #2855 and this exact-head logical review must each pass required checks and protected merge, then be independently read back from protected main. Until those steps happen, this document's verdict is mathematical review evidence, **not** a claim that either source or review is formally merged.
