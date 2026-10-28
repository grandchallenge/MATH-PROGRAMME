# EXT-015 REACH-R2 / 083 — common-domain test on the marked six-vertex host

**Verdict: the proposed intrinsic pole-only edge-factor prescription does not descend the actual regulated-kernel domain defined below.** The counterexample retains the entire regulator-dependent family and every Laurent coefficient. It is not the finite-state obstruction of 071. On the fixed host, moving one common scalar factor $\epsilon^2$ from edge 01 to edge 45 leaves the entire evaluated kernel unchanged, but the complete source-local forest recursion gives different finite distributions. Both legal disjoint triangle spinneys are included. This refutes this prescription on this domain; it does not prove that renormalization, a smaller domain, an enriched analytic domain, a different finite normalization, or a common BV operator is impossible.

One primary construction and one correction pass were made. The correction replaces an invalid independent-edge differentiation argument by the actual tangent vertex derivative, which cancels the cycle-null witness. It also checks the complete forest sum, rather than inferring its failure from one intermediate counterterm. No replacement host or further construction search is undertaken. Original R2 and dependent positive R4 remain open.

## 1. Inputs, category and actual domain

The governing protocol is [081](REACH_REASSESSMENT_081.md); the reconciled source audit is [082](REASSESSMENT_FRESH_AUDIT_082.md). The protected input before reassessment was `9cc483334648d94ea6226a76874151a3eabd33b1`. The audited source cut for this study is `afb5a6873562a9050b8a1fb65dee42f399db9967`. Sources 046, 061, corrected 065 and 071 have the following Git blobs at that cut and in the working files read here:

| Source | Git blob |
| --- | --- |
| [046](R2_BRIDGE_TREE_LAURENT_BV_046.md) | `d061de4cfb8081b1ccfbf0c6171fea7c423e639e` |
| [061](R2_FILTERED_NORMAL_JET_INSERTION_061.md) | `c38269ebf92c40c268d33af1b0e1fff3caf05b9f` |
| [065](R2_NESTED_GAUSSIAN_JET_FOREST_065.md) | `87b013559eb8485d80f7fa714db0b65a9272d6ed` |
| [071](R2_FINITE_LAURENT_INSERTION_OBSTRUCTION_071.md) | `13d1441dd5a745f7726d6b01843b2129331e4b2d` |
| Reused exact arithmetic and old-host regression, [fixture 065](fixtures/check_nested_gaussian_jet_forest_065.py) | `9e1e58d5df15cdbbeec5c443199d748742d5d45c` |

Use one-dimensional vertex positions, root at 0, and work on $X=\mathbb R^6/\mathbb R\cong\mathbb R^5$ with $y_j=x_j-x_0$. Orient every edge from its smaller to its larger endpoint and put $z_{ab}=x_b-x_a$. The fixed host is

$$
H=K_4(01,02,03,12,13,23)+04+14+05+15+45,
\qquad |V|=6,\quad |E|=11,\quad h_H=6.
$$

The two overlapping nonnested sources are $F_4=K_4+04+14$ and $F_5=K_4+05+15$, each of rank four. They share $K_4$. Let $G=H\setminus\{45\}$, of rank five. The propagators are the same Gaussian pair throughout:

$$
\kappa_\epsilon(t)=(2\pi)^{-1/2}\epsilon^{-1}e^{-t^2/(2\epsilon^2)},
\qquad P_\epsilon=(|\cdot|/2)*\kappa_\epsilon,
\qquad P_\epsilon''=\kappa_\epsilon.
\tag{83.1}
$$

**Actual domain being tested.** For each subgraph, start with finite sums of edge-factor families built from finite derivatives of $\kappa_\epsilon$, and, on the marked edge, $P_\epsilon$ or its finite derivatives. Allow polynomial edge-coordinate decorations and finite Laurent-polynomial scalar coefficients in $\epsilon$. Evaluate the product at the actual differences $z_e(y)$. Identify two expressions whenever their functions of $(\epsilon,y)$ agree for every $\epsilon>0$ and every $y$. Call the resulting real vector space $\mathscr U$; retain the exact family and its full distribution-valued Laurent asymptotic expansion. Thus $\mathscr U$ is a concrete space of smooth regulated kernels, not a free vector space on graphs or factorizations.

For source insertions, also allow the actual finite-order normal delta jets produced below, multiplied by complements which are smooth for every positive regulator. Legal products of jets on vertex-disjoint source diagonals are allowed. No product of jets on overlapping source diagonals is in the definition. All expansions and limits are in $\mathcal D'(X)$, uniformly on bounded compact smooth test families. There is no assertion here about the global normal topology of R1.

For comparison, a **source-channel input** records actual source and complement families separately, together with their vertex embeddings. It has more mathematical data than their product. A forest map on source-channel inputs is not yet a map on $\mathscr U$: it must preserve every equality of their evaluated products. This distinction is the compatibility test, rather than a choice of names for the same object.

The coefficient closure just stated is a hypothesis of the obstruction. A domain excluding the two scalar allocations below does not automatically contain this counterexample. Conversely, retaining their provenance as different inputs changes the domain and requires an explicit account of that additional data.

## 2. Primary source-local construction and its analytic meaning

Write $\mathrm{PP} A$ for the finite sum of the negative Laurent coefficients of an actual family $A$, including their regulator powers. Write $\mathrm{CT} A$ for its coefficient of degree zero. These operations on whole families are representation independent by uniqueness of asymptotic coefficients. A fixed finite truncation of the source state is never used.

For a connected cyclic bridgeless source $\gamma$, a proper spinney $S$ is a set of pairwise vertex-disjoint proper cyclic bridgeless sources. Define in increasing edge count, on source-channel inputs,

$$
\overline R_{\gamma,\epsilon}
=T_{\gamma,\epsilon}
+\sum_{\substack{S\ne\varnothing\\S\text{ proper spinney}}}
(-1)^{|S|}\left(\prod_{\beta\in S}C_{\beta,\epsilon}\right)
T_{\gamma\setminus S,\epsilon},
\qquad C_{\gamma,\epsilon}=\mathrm{PP}\overline R_{\gamma,\epsilon},
\qquad R_{\gamma,\epsilon}=\overline R_{\gamma,\epsilon}-C_{\gamma,\epsilon}.
\tag{83.2}
$$

Here the complement product is multiplied into the embedded source jets **before** taking its asymptotic expansion. A counterterm is calculated from its source alone. Nested forests occur inside the already prepared $C_\beta$; overlapping sources occur in separate summands. Formula (83.2) is not a product of every proper source counterterm.

**Claim 83.2, analytic existence on source channels.** For this finite host and its subgraphs, each fixed finite decoration in the stated grammar gives a finite pole part, finite-order local source counterterms, and a finite distributional limit after (83.2), as a source-channel calculation.

**Proof and hypotheses.** For an all-Gaussian connected source, its reduced Laplacian is positive definite. Rescaling its relative coordinates by $\epsilon$ gives a fixed Gaussian times a polynomial, with a single integer scalar degree. If the source contains the marked Wick edge, removing that edge still leaves a connected Gaussian backbone: the source is bridgeless. Moreover $P_\epsilon(\epsilon t)=\epsilon P_1(t)$; $P_1$ has at most linear growth, $P_1'$ is bounded, and its higher derivatives are Gaussian-polynomial functions. Thus the same rescaling has integrable moments of every order. In a legal insertion, delta jets in the source normals act on the actual complement jets; the remaining quotient Gaussian backbone is connected and positive definite. For disjoint sources their normal coordinates are independent, so the product is an exterior tensor product after a linear change of coordinates of absolute Jacobian one. Induction on edge count gives a finite sum of this same type.

Taylor expansion of a compact smooth test to any required degree, with Gaussian moment bounds and exponentially small tails outside a fixed collision neighborhood, proves the expansion and strong remainder bound. Finite derivatives and fixed polynomial decorations preserve these estimates. All negative coefficients are supported on the source diagonal and have finite derivative order. After subtracting them, the first remaining coefficient is degree zero, or the family tends to zero if that coefficient vanishes. This proves existence for each channel, with no uniform jet bound over all decorations. It does **not** prove that (83.2) respects equalities which change the source/complement allocation. That is tested in section 5.

**Normal complement action, actual domain and hostile control.** If $u$ is a source-normal coordinate and $q$ a quotient coordinate, multiplication by the positive-regulator complement $f_\epsilon$ is the ordinary distributional action

$$
f_\epsilon\,\partial_u^\alpha\delta(u)
=\sum_{\beta\le\alpha}(-1)^{|\beta|}
{\alpha\choose\beta}
(\partial_u^\beta f_\epsilon)(0,q)\,
\partial_u^{\alpha-\beta}\delta(u).
\tag{83.3}
$$

The proof is the finite distributional Leibniz formula, so multiplication by two smooth complements composes associatively on actual jets, independently of their factorization. For a one-normal second jet it includes $-2f_u(0,q)\delta'$ as well as $f_{uu}(0,q)\delta$. For $f_\epsilon=\kappa_\epsilon(q-u)\kappa_\epsilon(q)$ and a test equal near the collision to $u q$, the pairing is $2q f_u(0,q)=2q^2\epsilon^{-2}f_\epsilon(0,q)$ before the $q$ integral. It is nonzero. Freezing the complement value loses it. The new fixture checks this mixed term; it also rebuilds the inherited nonzero derivative moment for insertion from K4 into $F_4$ $-7\sqrt2/144$. No limiting singular complement is multiplied into a source jet.

## 3. Fixed-host forests and a nonzero even-rank finite control

There are 277 proper cyclic bridgeless edge sources in $H$, with rank counts $30,90,99,47,11$ in ranks one through five. These counts are an exhaustive control on (83.2), not the scientific result. The new host has exactly two disjoint pairs of cyclic sources:

$$
(023,145),\qquad (123,045).
\tag{83.4}
$$

For example, $023$ uses edges $02,03,23$ and $145$ uses $14,15,45$. Each pair consists of triangles on complementary vertex sets. There can be no triple of disjoint cyclic sources on six vertices. All other compatible proper collections are obtained by nesting and these disjoint alternatives. In particular, $F_4$ and $F_5$ never occur together in a spinney or forest. Their delta jets are never multiplied.

The reduced determinants are

$$
\tau(K_4)=16,\quad \tau(F_4)=\tau(F_5)=40,
\quad\tau(G)=96,\quad\tau(H)=192.
\tag{83.5}
$$

**Exact moment rule.** Root each source at its least vertex, let $Q_\gamma$ be its reduced Laplacian, and use independent source normals $u$ and quotient coordinates $q$. Decompose the complement exponent as $u^TAu+2u^TBq+q^TDq$, with $D$ positive definite; an empty quotient has determinant one. For a test monomial $\Phi_\alpha$, a single source insertion is

$$
I_{\gamma\leftarrow\beta,\alpha}
=(\det D)^{-1/2}
\sum_\eta m_{\beta,\eta}
\mathbb E_{N(0,D^{-1})}
\left[[u^\eta]\left(e^{-u^TAu/2-u^TBq}\Phi_\alpha(u,q)\right)\right].
\tag{83.6}
$$

The sum is over the pole jets actually present in that source. The factor $1/\eta!$ in the source counterterm cancels the factorial from differentiation; the even derivative sign is positive. Consequently

$$
m_{\gamma,\alpha}
=\tau_\gamma^{-1/2}\mathbb E_{N(0,Q_\gamma^{-1})}[y^\alpha]
-\sum_{\beta\subsetneq\gamma}I_{\gamma\leftarrow\beta,\alpha}
+\sum_{\{\beta,\beta'\}\text{ disjoint}}I_{\gamma\leftarrow\{\beta,\beta'\},\alpha}.
\tag{83.7}
$$

For either disjoint triangle pair, the source scalar moments are $1/\sqrt3$ each. Collapsing the pair leaves one relative coordinate $q$ and $n$ crossing Gaussian edges. The insertion moment is $1/(3\sqrt n)$ times the Gaussian moment of the collapsed test with variance $1/n$. This supplies the last sum, including inside proper sources. For $H$, $n=5$. On $y_1^6$, the two pair terms sum to $2\sqrt5/125$, which is nonzero. Thus omitting disjoint products is detected by an actual test, not just a count.

**Nonzero finite host, not an odd-rank zero-limit shortcut.** In the all-delta converted host put $t=x_5-x_4$. After preparing every proper source and subtracting the overall poles, a compact smooth test equal near the full collision to $t^6$ has finite pairing

$$
\left\langle\lim_{\epsilon\downarrow0}R_{H,\epsilon},\phi_{t^6}\right\rangle
=(2\pi)^{-3}A,
\qquad
A=\frac{5\sqrt3}{64}+\frac{265\sqrt2}{1536}
-\frac{16685\sqrt6}{46656}+\frac{1160\sqrt7}{3969}
-\frac{41\sqrt{30}}{810}<0.
\tag{83.8}
$$

This is a finite sixth-derivative full-diagonal coefficient because $h_H=6$. Every pole has derivative degree zero, two or four and vanishes on this test. Formula (83.7), rational Gaussian Wick pairing, and exact square-root enclosure give (83.8); the fixture prints an interval whose upper endpoint is strictly negative. The same rebuilt recursion preserves the nonzero finite quartic source moment from corrected 065,

$$
m_{F_4,y_1^4}=\frac{3\sqrt{10}}{125}-\frac{8\sqrt{21}}{343}\ne0,
\tag{83.9}
$$

and its $4\leftrightarrow5$ copy. No finite term of a proper source is inserted as an extra counterterm in this pole-only prescription.

**Proof versus finite computation.** Equations (83.6)–(83.7), the source induction and section 2 prove what the finite calculation represents and why its limit is a distribution. The fixture exhausts the finite edge subsets, uses exact rational matrices and squarefree radicals, and evaluates all required source pole moments, including fourth-order source normals. It verifies finite algebra only. It is neither an infinite-graph theorem nor a BV certificate.

## 4. Marked conversion: failed primary operator and the single tangent correction

Let $K_{G,\epsilon}=\prod_{e\in G}\kappa_\epsilon(z_e)$ and $T^P_{H,\epsilon}=P_\epsilon(t)K_{G,\epsilon}$. On independent edge coordinates, differentiating the marked factor twice gives the actual identity $P_\epsilon''=\kappa_\epsilon$. For an undecorated factorization this evaluates to the all-delta host. It does not by itself define an operator on the quotient $\mathscr U$.

**Primary hostile control.** On independent edge space put $\ell=z_{45}-z_{05}+z_{04}$. Its evaluation on every vertex configuration is zero. The decorated kernel $\ell^2 P_\epsilon(z_{45})K_{G,\epsilon}$ therefore represents zero in $\mathscr U$. Independent marked-edge differentiation gives

$$
\left.\partial_{z_{45}}^2\left(\ell^2 P_\epsilon(z_{45})K_{G,\epsilon}\right)\right|_{z=z(y)}
=2P_\epsilon(t)K_{G,\epsilon}\ne0.
\tag{83.10}
$$

All families are smooth at positive regulator. Nonvanishing follows from positivity of $P_\epsilon$ and the Gaussians. Thus the operator $\partial_{z_{45}}^2$ on the **whole decorated marked factor** does not descend this evaluated domain. An operation that only replaces a named propagator and deliberately leaves its decoration untouched is a different source-channel operation. Formula (83.10) does not refute an actual vertex-domain BV identity.

**Correction and actual vertex identity.** Take the tangent vertex derivative

$$
D=\tfrac12(\partial_{x_5}-\partial_{x_4}).
$$

Then $Dt=1$, $D\ell=0$, and $D$ changes the four spokes $04,14,05,15$ with coefficients $-1/2,-1/2,1/2,1/2$. Consequently

$$
DK_{G,\epsilon}=-t\epsilon^{-2}K_{G,\epsilon},
\qquad D^2K_{G,\epsilon}=(t^2\epsilon^{-4}-\epsilon^{-2})K_{G,\epsilon},
$$

and the ordinary product rule proves the exact positive-regulator identity

$$
D^2T^P_{H,\epsilon}
=\kappa_\epsilon(t)K_{G,\epsilon}
-2t\epsilon^{-2}P_\epsilon'(t)K_{G,\epsilon}
+(t^2\epsilon^{-4}-\epsilon^{-2})P_\epsilon(t)K_{G,\epsilon}.
\tag{83.11}
$$

This derivative sends the cycle-null witness to zero, including all chain-rule terms. No vertex direction can vary only $z_{45}$ while keeping every edge of $G$ fixed: $G$ is connected, so those fixed differences force a common vertex translation. The extra terms in (83.11) are therefore necessary, not an anomaly to discard. Constant vertex derivatives commute with the full Laurent expansion and its coefficient extraction on actual distribution families, so (83.11) survives taking whole-family coefficients. What remains unproved is its compatibility with a **descended** common source-local renormalization map. It would be circular to define that map by transporting the graph label and then declare (83.11) a renormalized BV theorem.

This repairs the primary derivative test and is the sole correction pass. The next section reports the remaining compatibility failure of the same proposed subtraction, including its full forest sum.

## 5. Exact full-forest representation defect with all Laurent data retained

**Contract under test.** The input is the actual family in $\mathscr U$. On a displayed edge factorization, apply intrinsic source-local pole subtraction (83.2) to the actual decorated source carried by each edge subset. Require the resulting finite distribution to depend only on the actual evaluated input. In particular, a common scalar $\epsilon^2$ may be written on any edge without changing the input. This is a descent requirement, not a claim that $\mathrm{PP}$ is linear over Laurent scalar functions.

Let $a_e=\kappa_\epsilon(z_e)$ and compare the two edge-factor presentations

$$
\mathcal A^{(01)}=(\epsilon^2a_{01})\prod_{e\ne01}a_e,
\qquad
\mathcal A^{(45)}=(\epsilon^2a_{45})\prod_{e\ne45}a_e.
\tag{83.12}
$$

Both are exactly $\epsilon^2T_{H,\epsilon}$, even before imposing vertex-cycle relations. They have identical complete regulator-dependent families, full normal distributional jets and all Laurent coefficients. There is no finite-state information loss.

For allocation $\lambda\in\{01,45\}$, a source containing $\lambda$ has effective scalar degree $h_\gamma-2$. Its intrinsic pole part therefore uses precisely the even normal moments with $|\eta|<h_\gamma-2$; other sources use $|\eta|<h_\gamma$. The normalized moments are recomputed by (83.6)–(83.7) with those source-specific ranges. A triangle carrying $\epsilon^2$ has no pole counterterm. Disjoint spinneys containing that triangle consequently contribute zero; both other disjoint contributions are retained wherever legal. This completely specifies the calculation without fitting a counterterm to the host.

**Theorem 83.5, bounded failure of this descent contract.** For a compact test equal near the full collision to $t^4$, the two full pole-subtracted forest results from (83.12) satisfy

$$
\left\langle\lim_{\epsilon\downarrow0}
\left(R_H^{(01)}-R_H^{(45)}\right),\phi_{t^4}\right\rangle
=(2\pi)^{-3}B\ne0,
$$

$$
B=\frac1{288}+\frac{329\sqrt2}{2304}-\frac{49\sqrt3}{72}
-\frac{1103\sqrt5}{3600}+\frac{2651\sqrt6}{15552}
-\frac{92\sqrt7}{1323}+\frac{8\sqrt{30}}{675}
+\frac{41\sqrt{42}}{196}<0.
\tag{83.13}
$$

**Proof.** Section 2 supplies the actual expansions and limits. Each allocation has total effective degree four, so its finite term pairs with the degree-four Taylor coefficient of the test. Its lower-degree overall poles vanish on $t^4$ and cannot change this pairing. Recompute every containing source in increasing edge number with its effective pole range, while sources not containing the allocated edge retain the already intrinsic counterterms. Equation (83.7), including both disjoint pairs, gives the following normalized finite pairings:

$$
\begin{aligned}
b_{01}={}&\frac{91}{288}+\frac{61\sqrt2}{288}-\frac{43\sqrt3}{288}
-\frac{4\sqrt5}{45}-\frac{47\sqrt6}{432}
+\frac{4\sqrt7}{63}-\frac{\sqrt{30}}{90},\\
b_{45}={}&\frac5{16}+\frac{53\sqrt2}{768}+\frac{17\sqrt3}{32}
+\frac{87\sqrt5}{400}-\frac{4343\sqrt6}{15552}
+\frac{176\sqrt7}{1323}-\frac{31\sqrt{30}}{1350}
-\frac{41\sqrt{42}}{196}.
\end{aligned}
\tag{83.14}
$$

Subtracting gives (83.13). Every entry is obtained from rational Gaussian Wick moments and inverse square roots of positive integer determinants by the finite recursion (83.6)–(83.7). The executable fixture rebuilds those matrices and source moments, asserts the complete radical expression, and encloses it using integer square bounds at precision $10^{12}$; its upper endpoint is strictly negative. No numerical fit or floating-point sign decision occurs. Since the inputs in (83.12) are equal and the outputs have a nonzero difference on one actual compact smooth test, the proposed map cannot descend $\mathscr U$. This proof concerns the stated finite prescription and domain.

**Local explanation and hostile control.** Already for the prepared diamond $D_0=\{01,02,03,12,13\}$, the scalar source pole has normalized coefficient

$$
a_{D_0}=\frac{\sqrt2}{4}-\frac{\sqrt6}{3}-\frac12\ne0,
\qquad C_{D_0,\epsilon}=(2\pi)^{-1}a_{D_0}\epsilon^{-2}\delta_{D_0}.
$$

Its full prepared family begins in degree $-2$. Hence $\mathrm{PP}(\epsilon^2\overline R_{D_0})=0$ whereas $\epsilon^2\mathrm{PP}(\overline R_{D_0})=(2\pi)^{-1}a_{D_0}\delta_{D_0}$. Inserting the difference into the smooth all-delta complement in $H$ has a nonzero finite pairing on $y_4^4$: after extracting $(2\pi)^{-3}$ it is $27/512-9\sqrt3/128-27\sqrt2/512<0$. The quotient matrix is $\left(\begin{smallmatrix}3&-1\\-1&3\end{smallmatrix}\right)$, determinant eight, with fourth moment $27/64$ in $y_4$. This stage calculation explains the defect, but is **not** used as a substitute for the full-forest result (83.13): larger counterterms could in principle have cancelled a stage discrepancy. They have been explicitly included in (83.14).

The failed requirement is compatibility between source-intrinsic pole projection and forgetting the regulator allocation. Whole-family pole projection itself is well-defined. The ordinary source-channel prescription itself is defined. The incompatibility arises when they are required to form this single map on evaluated products. An enriched domain may retain separate regulator/source variables as actual analytic data, or a different normalization may add finite contact terms. Either route changes hypotheses and still needs proof. This result says nothing about every such route.

## 6. Disjoint composition and proposed scale transport

**Disjoint composition on its actual domain.** For source jets on independent vertex sets, multiplication is the exterior tensor product followed by the stated linear coordinate map. This is an actual distribution operation, associative and symmetric, and it composes with smooth complement multiplication by (83.3). For full Laurent families the Cauchy coefficients are finite because each series is bounded below. This proves the disjoint composition used in (83.2). It neither legitimizes an overlapping singular product nor repairs the allocation relation (83.12).

**Honest dilation transport.** If $s>0$ and $S_s$ is pushforward under $y\mapsto sy$ on distributions, the bare all-delta and marked-Wick families satisfy respectively

$$
T^\kappa_{H,s\epsilon}=s^{-6}S_sT^\kappa_{H,\epsilon},
\qquad T^P_{H,s\epsilon}=s^{-4}S_sT^P_{H,\epsilon}.
\tag{83.15}
$$

The proof is $\kappa_{s\epsilon}(t)=s^{-1}\kappa_\epsilon(t/s)$, $P_{s\epsilon}(t)=sP_\epsilon(t/s)$ and the dimension-five Jacobian. Finite derivative or polynomial decorations change the displayed scalar degree by their homogeneous degree. On each component of degree $a$, $\mathcal T_s^a=s^{-a}S_s$ is an actual representation-independent transport with $\mathcal T_s^a\mathcal T_r^a=\mathcal T_{sr}^a$. A jet of normal degree $n$ scales by $s^{n-a}$. The fixture checks these cocycles on both relevant degrees and finite-jet orders. Uniform dilation also respects the channelwise homogeneous recursion. Because the forest map does not descend $\mathscr U$, this does not produce a common renormalized transport there.

**Independent-edge heat is not the required repair.** Smoothing every independent edge coordinate by the heat operator and then evaluating does not descend the vertex-cycle quotient. For $\ell^2F$, its infinitesimal generator $\tfrac12\sum_e\partial_{z_e}^2$ evaluates to $3F$ on $\ell=0$. The tangent vertex derivative in section 4 does preserve this relation. Actual dilation (83.15), independent-edge heat, and quantum transport are three different operations.

In particular, no identification with the repaired R1 quantum transport is made here. With the audited convention $[B,d]=\Delta$, those formulas are $d^q=W dW^{-1}$, quantum-to-classical $W^{-1}$, $T_{\epsilon,\eta}=W_\eta W_\epsilon^{-1}$, and connection $W_\epsilon\partial_\epsilon(W_\epsilon^{-1}a)$. The present collision domain has not been shown invariant under these operators. Defining transport by a graph label would not prove that invariance or the forest intertwining equation.

## 7. Scope, exact next theorem and evidence

The positive results here are concrete: the new finite Gaussian source-channel forest, legal disjoint products, all required normal complement jets, the nonzero even-rank finite host (83.8), actual marked-edge identity with its tangent correction (83.11), and the genuine dilation law. The negative result is also concrete: the complete intrinsic pole-only forest map fails the stated actual-family descent test (83.12)–(83.14). Neither result closes the common renormalized BV assignment.

The **next theorem is a coherence theorem, not another graph count**: specify an actual analytic domain and its equality relation, then construct a source-local normalization whose complete forest map preserves those equalities, including regulator-allocation relations if they are retained. It must satisfy the vertex differential identity with every term of (83.11), agree on disjoint composition, and intertwine the actual repaired Wick transport on an invariant domain. If the intended domain retains independent regulator/source slots, prove the evaluation and change-of-presentation maps on that enriched data; do not replace this proof by retaining provenance labels. If the intended normalization changes finite terms, explicitly exhibit the finite contacts correcting (83.13) and prove the corresponding consistency relations under nested and disjoint insertions. No such common normalization or invariant analytic domain is constructed in this pass.

For comparison with primary literature, Brunetti–Fredenhagen, [Microlocal Analysis and Interacting Quantum Field Theories](https://arxiv.org/pdf/math-ph/9903028), Theorems 5.2–5.3, assume a distribution off a point with finite scaling degree and classify its extensions by local jet choices when that degree is large enough. Their theorem was checked directly; it does not identify a regulator pole-only graph prescription with a unique compatible extension, or imply the BV/transport relations tested here. The present proof uses explicit Gaussian rescaling, not an unverified application of that theorem. Local finite normalization freedom is one reason (83.13) must not be promoted into a universal impossibility claim.

The exact finite regression is [check_common_domain_083.py](fixtures/check_common_domain_083.py). It imports the frozen 065 fixture for rational/radical primitives and its unchanged old-host regressions, then changes the host, independently rebuilds its source inventory and matrices, includes both disjoint spinneys, expands proper-source normal jets through order four, and checks (83.8), (83.9), (83.13)–(83.14), the source-stage contact, the mixed Leibniz term, and the tangent/dilation controls. The script asserts exact radical values and strict rational sign enclosures. Finite algebra is the limit of its evidentiary scope.

Execution is Windows PowerShell on CHAD, using the existing isolated interpreter `F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe`, CPython 3.12.12. This worktree has no admitted root `uv.lock` or declared root Python project: the evidence environment is **unpinned**. No dependencies were installed, no lock was resolved, and no host/system Python or hosted compute was used. Each spawned Python process explicitly sets owner-local cache paths. Exact replay from the reassessment worktree is:

```powershell
$env:UV_CACHE_DIR='C:\Users\jamie\AppData\Local\GCL\uv'
$env:PYTHONPYCACHEPREFIX='C:\Users\jamie\AppData\Local\GCL\PythonBytecodeCache'
& 'F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe' -u 'research/condensed-qft/EXT-015/fixtures/check_common_domain_083.py'
& 'F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe' 'ci/math_markdown_gate.py' --file 'research/condensed-qft/EXT-015/R2_COMMON_DOMAIN_COMPATIBILITY_083.md'
git diff --check
```

Validation on 2026-10-27:

| Check | Result |
| --- | --- |
| Complete `check_common_domain_083.py` replay, Git blob `829f1c43d428a3d124c0c5312515d30ac61e4398` | PASS, including the asserted complete-forest discrepancy and strict rational negative intervals |
| Mandatory mathematical Markdown source preflight for this note | PASS |
| `git diff --check` | PASS |
| Runtime identity | CPython 3.12.12; `sys.prefix` is the stated evidence `.venv` and differs from `sys.base_prefix` |

The final working note blob is returned outside this self-referential document. This study edits only this note and its fixture. It does not commit, push, create a pull request, alter trackers/checkpoints, claim protected admission, or assert independent certification. R3 attempts and the later opposed review were not read.
