# EXT-015 REACH-R2 / 041 — distribution-valued moving collisions: exact forest amplitudes and first cyclic renormalization

**Disposition:** NEW SUBSTANTIVE MATHEMATICAL CANDIDATE, not externally certified. This establishes well-defined collision distributions for arbitrary forest diagrams of the free one-dimensional delta/BV and cusp/Wick kernels, with **smooth distribution-valued parameter translations even through collisions**. It also isolates and renormalizes the first genuinely divergent cyclic diagram by an explicit local counterterm. It does **not** produce a general BV algebra on arbitrary collision graphs, an interacting QFT, or completed Costello–Gwilliam B.6 differentiable Weiss descent.

**Source:** admitted [D14 regulated free model 028](D14_REGULATED_BV_SYZYGY_028.md), [D21 microlocal zero-scale 030](D21_MICROLOCAL_ZERO_SCALE_BV_030.md), [R0 critical review 033](R0_CRITICAL_AUDIT_D21_033.md), [R1 normal sectors 035](R1_NORMAL_CONE_CONTINUOUS_CONTRACTIONS_035.md), and [R2 finite-part 032](R2_LOCAL_FINITE_PART_032.md), [moving-atom cusp obstruction 036](R2_MOVING_ATOM_CUSP_OBSTRUCTION_036.md). The preceding **fixed-label atomic BV candidate** is [039 PR #2814](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2814); it remained open when this work was launched. The proof below is **independent of assuming its protected admission**. Initial protected baseline SHA a99c760568127ab7cb152df52db0beee8e54e271. Mathematical tools: Hörmander distributions, submersion pullback and tensor products; Brunetti–Fredenhagen, [microlocal extension framework](https://arxiv.org/abs/math-ph/9903028).

## 1. Collision configurations and exact edge distributions

Let $V$ be a finite labeled vertex set, $X=\mathbb R^V$, and let $F=(V,E)$ be a finite **forest** with arbitrarily oriented edges. For an edge $e=(i,j)$ set $d_e(x)=x_i-x_j$, and collect them in the difference map

$$
D_F:X\longrightarrow\mathbb R^E,
\qquad D_F(x)=(d_e(x))_{e\in E}.
\tag{41.1}
$$

Choose, independently for each edge, a one-dimensional distribution

$$
t_e\in\mathcal D'(\mathbb R);
\tag{41.2}
$$

the physical cases are $t_e(z)=\partial_z^r(|z|/2)$, including $|z|/2$, the sign distribution, $\delta_0$ and all higher delta derivatives. For the normalized jet pairing, $\partial_{x_i}^k\partial_{x_j}^lP_0(x_i-x_j)=(-1)^l\partial_z^{k+l}(|z|/2)$.

Set

$$
A_F(t)=D_F^*\left(\mathop{\boxtimes}_{e\in E}t_e\right)\in\mathcal D'(X).
\tag{41.3}
$$

The right-hand side is a **pullback of a tensor-product distribution**; it is *not* an undefined multiplication of delta distributions on a collision diagonal.

**Theorem 41.1 (canonical forest collisions).** For every finite forest $F$ and every family (41.2), the distribution (41.3) exists without wavefront restrictions on the individual edge distributions. It agrees with the usual product $\prod_{e\in E}d_e^*t_e$ whenever the latter is written using Hörmander's wavefront product. It includes configurations in which **every** vertex position coincides. Its value is independent of the order of the edge factors and independent of the orientation choices after the natural reflection $z\mapsto-z$ of each $t_e$.

**Proof.** The oriented incidence matrix of a forest has linearly independent rows. To prove this without relying on a rank formula, take an edge incident to a leaf, whose leaf-coordinate coefficient appears in no other edge row; its coefficient in a linear dependence must vanish. Remove the leaf and induct over all edges. Thus $D_F$ has full row rank $|E|$ and is a surjective linear submersion, so the distributional pullback $D_F^*$ exists for **every** distribution on $\mathbb R^E$. The exterior tensor product in (41.3) always exists. A linear change of coordinates using one root coordinate in each connected component plus all forest differences explicitly identifies (41.3) with $\bigotimes_e t_e$ tensored with a smooth constant distribution in the root coordinates; hence the construction is canonical.

For the alternate product construction, each wavefront covector of $d_e^*t_e$ is proportional to the row of the incidence matrix for $e$. If a nonempty collection of such edge covectors could sum to zero at a point, the incidence-row independence would force every coefficient to vanish. Hörmander's sufficient product criterion is therefore satisfied for any collection of edge singularities. The wavefront product and the submersion/tensor pullback agree by local coordinate factorization, and hence globally. Permuting tensor factors produces the canonical permutation isomorphism; reversing an edge amounts to composing the corresponding one-dimensional factor with reflection. $\square$

**Not restricted to pairwise distinct positions:** unlike pointwise scalar evaluation of the delta kernel, the output is a genuine distribution *over the moving position variables*, well defined even at collisions.

## 2. Genuine smooth families with distribution-valued outputs

Let $M$ be a finite-dimensional parameter manifold and let $a:M\to\mathbb R^V$ be smooth. For fixed $F,t_e$, define a family of translated distributions on $X$ by

$$
A_{F,m}(x)=A_F(t)(x-a(m)).
\tag{41.4}
$$

**Theorem 41.2 (smooth collision-parameter translation).** The family $m\mapsto A_{F,m}$ is $C^\infty$ as a map $M\to\mathcal D'(X)$ in the ordinary strong distribution topology. This is true even when some or all values of $a_i(m)$ coincide. In particular each formal parameter derivative exists distributionally and obeys the usual chain rule, involving derivatives of $A_F$.

**Proof.** Translation of an arbitrary distribution is $C^\infty$ for finite-dimensional translation parameters in the strong topology of $\mathcal D'$. Indeed, for a test function $\phi$ the translated pairing is evaluation of the fixed distribution on a smoothly translated test function. For a bounded test-function set, the translations for parameters in a compact neighborhood have uniformly controlled support and all derivatives. Taylor's theorem in the test-function Fréchet topology gives uniform convergence of difference quotients on such bounded sets, proving strong smoothness; iterating gives every derivative. Composing with the smooth finite-dimensional map $a$ proves (41.4). Nothing requires a pointwise scalar value of the singular kernel on a collision locus. $\square$

**Important separation of categories:** strong smoothness of a **distribution-valued translated amplitude** does not imply smoothness of a **scalar result obtained by pulling it back along a moving collision diagonal**. Such pullbacks may be undefined. In particular this theorem does not contradict the exact scalar cusp obstruction in [036](R2_MOVING_ATOM_CUSP_OBSTRUCTION_036.md), or the R0 oscillatory example showing that zero-scale diagonal contraction is not continuous on arbitrary ambient-distribution smooth families. Theorem 41.2 does not establish an enriched prefactorization multimorphism for the full collection of diagrams.

## 3. Free differential/BV identities within the forest sector

The free propagator distribution obeys, on the entire difference line,

$$
P_0(z)=\frac{|z|}{2},
\qquad
P_0''=\delta_0=K_0.
\tag{41.5}
$$

All derivatives of (41.5) hold in $\mathcal D'(\mathbb R)$. They therefore remain true after tensor product with other edge distributions and pullback along the submersion $D_F$. Differentiation in a vertex position differentiates its adjacent edge factors by the distributional Leibniz rule; **the graph stays a forest**.

**Corollary 41.3 (forest-sector compatibility).** Every fixed forest amplitude is compatible with the free propagator identity relating Wick and BV edges, arbitrary finite jet derivatives, and repeated edge **differentiation**. Deleting edges, taking disjoint unions of forests, and adding a new edge **only when acyclicity is preserved** all retain well-defined distribution amplitudes. The corresponding finite graphwise Wick/BV differential identities that never introduce a cyclic set of singular edges are legitimate equalities in distributions.

This is **not** a claim that the full Wick exponential or BV second-order bracket defines an operator on arbitrary products of moving atoms: unrestricted pairing graphs can contain cycles, and pointwise distribution products of those edges may not exist. To obtain a full renormalized operator one must define compatible extensions for *all* problematic graphs and verify the required relations across their overlaps.

## 4. A genuine cyclic divergence in the original delta/BV kernel

Let $\kappa\in C_c^\infty(\mathbb R)$ be **even, nonnegative, nonzero, mass one**, with $\kappa_\epsilon(z)=\epsilon^{-1}\kappa(z/\epsilon)$. At three independent atom locations define the smooth *triangle collision amplitude*

$$
T_\epsilon(x_1,x_2,x_3)=
\kappa_\epsilon(x_1-x_2)
\kappa_\epsilon(x_2-x_3)
\kappa_\epsilon(x_3-x_1).
\tag{41.6}
$$

This corresponds, for example, to three free mixed even/odd BV pair contractions arranged as an oriented cycle; with one even and one odd generator at each vertex. It is a kernel product on **parameter configuration space**, not a cyclic contraction claim within D21's admissible WF domain.

Write $u=x_1-x_2$, $v=x_2-x_3$ and $s=x_3$; this is a linear change of variables of absolute determinant one. Define the finite, positive regulator-shape constant

$$
c_\kappa=
\int_{\mathbb R^2}
\kappa(\alpha)\kappa(\beta)\kappa(\alpha+\beta)
\,d\alpha\,d\beta>0.
\tag{41.7}
$$

Strict positivity follows, for instance, whenever the even smooth mollifier is positive on a neighborhood of zero; nonnegative nonzero even mollifiers are not automatically positive near zero, so we **assume positivity near zero** for the strict inequality.

**Theorem 41.4 (first cycle's local counterterm, exact leading coefficient).** The family $T_\epsilon$ does not converge in $\mathcal D'(\mathbb R^3)$ as $\epsilon\downarrow0$. More precisely, with the distributions

$$
\delta_\triangle=\delta(x_1-x_2)\delta(x_2-x_3)
\tag{41.8}
$$

and using the standard normalization in $(u,v,s)$, one has

$$
T_\epsilon-
\frac{c_\kappa}{\epsilon}\delta_\triangle
\longrightarrow0
\quad\text{in }\mathcal D'(\mathbb R^3),
\tag{41.9}
$$

with remainder $O(\epsilon)$ against each fixed compact test function, and locally uniformly on bounded sets of test functions. The subtraction is supported on the **triple collision diagonal**, is translation invariant and symmetric under cyclic relabeling. Finite additional multiples of $\delta_\triangle$ are scheme choices not fixed by the chosen cancellation prescription.

**Proof.** Write $\phi(s,u,v)$ for the test function after the coordinate change. The regulated pairing becomes

$$
\langle T_\epsilon,\phi\rangle
=
\epsilon^{-1}
\int_{\mathbb R}\int_{\mathbb R^2}
\kappa(\alpha)\kappa(\beta)\kappa(\alpha+\beta)
\phi(s,\epsilon\alpha,\epsilon\beta)
\,d\alpha\,d\beta\,ds.
\tag{41.10}
$$

The leading term is exactly $(c_\kappa/\epsilon)\int\phi(s,0,0)\,ds$, the pairing with the local distribution in (41.8). For a nonnegative test function with nonzero restriction to the triple diagonal, it diverges at positive rate $1/\epsilon$. The difference in (41.9) is obtained by subtracting this leading term inside (41.10). The weight
$w(\alpha,\beta)=\kappa(\alpha)\kappa(\beta)\kappa(\alpha+\beta)$ is invariant under $(\alpha,\beta)\mapsto(-\alpha,-\beta)$ because $\kappa$ is even. Its first moments in $\alpha$ and $\beta$ therefore vanish. Taylor expansion of $\phi(s,\epsilon\alpha,\epsilon\beta)$ through first order yields a remainder bounded by $\epsilon^2 C$ times the second-derivative test seminorm, uniformly for $(\alpha,\beta)$ in the compact support of $w$ and $s$ in a fixed compact. Multiplication by the prefactor $\epsilon^{-1}$ leaves $O(\epsilon)$. This establishes convergence strongly on fixed compact-support test families as claimed. Symmetry follows by permuting the three differences; the $c_\kappa$ product is unchanged. $\square$

**Scaling and necessity.** The triangle has three regularized delta edges but only two independent relative-position coordinates. Each mollifier contributes one inverse power of $\epsilon$, while relative-coordinate integration contributes two powers: the leftover $1/\epsilon$ is the first graph-cycle excess. The wavefront covectors of the three diagonal deltas have a nonzero linear dependence, so Hörmander's product criterion fails. The divergence in (41.10) shows that, for this regulator class, this failure is not merely an inconclusive sufficient criterion: there is an actual diverging family.

## 5. Exact arbitrary simple-cycle extension

For a simple cycle with $m\ge3$ vertices, take edge differences $u_1,\dots,u_{m-1}$ along a spanning tree and the closing difference $u_m=-\sum_{i<m}u_i$. Define the smooth regulated cycle product $T_{m,\epsilon}$ of $m$ copies of $\kappa_\epsilon$. Put

$$
c_{\kappa,m}=
\int_{\mathbb R^{m-1}}
\left(\prod_{j=1}^{m-1}\kappa(u_j)\right)
\kappa\left(\sum_{j=1}^{m-1}u_j\right)
\,du_1\cdots du_{m-1}.
\tag{41.11}
$$

**Corollary 41.5 (simple cycles share the same divergence order).** With even $\kappa$ positive near zero, each unrenormalized simple-cycle amplitude diverges as $(c_{\kappa,m}/\epsilon)$ times the appropriately normalized delta distribution on the full coincidence diagonal. Subtracting that local term gives a distribution that tends to zero with remainder $O(\epsilon)$ on compact test families. The proof is exactly the rank $m-1$ change-of-variables and simultaneous sign-reversal symmetry used above; the result is **only** for a single isolated simple cycle of identical undifferentiated delta edges.

It does not solve overlapping cycles, derivatives of delta on cycles, interacting Feynman graphs, forest-formula consistency for subdivergences, or quantum master equation anomalies.

## 6. Exact rational hostile control

For a deliberately **nonsmooth** algebraic diagnostic let

$$
\kappa_{\mathrm{box}}(z)=
\frac12\,\mathbf1_{\{|z|<1\}}.
\tag{41.12}
$$

This is a mass-one, even compact-support approximate-identity density, **not** a legal $C_c^\infty$ mollifier for the analytic theorem. Its triangle coefficient is

$$
c_{\mathrm{box}}
=\frac18\operatorname{Area}\{(\alpha,\beta)\in[-1,1]^2:
|\alpha+\beta|\le1\}
=\frac38.
\tag{41.13}
$$

The central hexagon has area three. Under the same box weight the odd first moments vanish and the unnormalized second moments are

$$
\int\alpha^2 w\,d\alpha d\beta
=\int\beta^2 w\,d\alpha d\beta=\frac5{48},
\qquad
\int\alpha\beta w\,d\alpha d\beta=-\frac5{96}.
\tag{41.14}
$$

The exact rational fixture [041](fixtures/check_collision_forest_cycle_041.py) verifies the incidence rank for all labeled forests through five vertices, cycle dependence, coefficient $3/8$ and the first two moments, without numerical tolerances. The fixture does not substitute for the general Schwartz distribution or microlocal proof.

## 7. Mathematical status and next obligation

| Object | Result | Claim limit |
| --- | --- | --- |
| Moving-position forest products of all free propagator and delta jets | Canonical distributions on the full collision configuration, Theorem 41.1 | Forest graph sector; not arbitrary graphs |
| Smooth movement of collision configurations | Strong-distribution-valued $C^\infty$ translation family, Theorem 41.2 | Not pointwise scalar collision evaluation or full DVS |
| Free differential identity for forest-edge derivatives | Distributional compatibility, Corollary 41.3 | Not a global BV operator across cyclic contractions |
| One triangle of three regulated delta edges | Exact leading $1/\epsilon$ divergence and **local** counterterm, Theorem 41.4 | Does not define interacting renormalization |
| Isolated simple cycles of undifferentiated delta edges | Exact local leading counterterm, Corollary 41.5 | No overlapping graph or derivative-jet forest formula |
| All overlapping configurations, completed B.6 and actual liquid higher Ext | **OPEN** | Separate substantive proofs still required |

**Immediate next theorem target:** construct a consistent **subgraph-local subtraction/extension recursion** for two overlapping or nested cycles with delta-jet edges; show the required identities under contraction, graph gluing and regulator change, or display an exact anomaly. For differentiable enrichment, replace strong translation smoothness with plots controlled in appropriate normal wavefront cones that are stable under the permitted multilinear operations, and prove completed Weiss descent separately.

**Governance:** Bounded new mathematics; requires a distinct source-locked mathematical critical review and protected admission. Parent [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797), [REACH-R1 #2796](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2796), and parent EXT-015D #2657 remain open. Do not claim that this candidate completes GB2 or a general quantum field theory.
