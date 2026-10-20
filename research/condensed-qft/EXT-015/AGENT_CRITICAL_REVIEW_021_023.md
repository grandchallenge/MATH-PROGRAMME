# EXT-015D / 023 — GCL mathematical critical audit of completion and polynomial results

**Disposition:** ACCEPT the bounded mathematical statements in [021](DERIVED_WEIGHT_COMPLETION_BOUNDARY_021.md) and [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md), with the exact category and degree restrictions below. This is a separately written critical argument by GCL's mathematical specialist function; it is not a different authenticated GitHub reviewer, formal certificate, or external peer review.

**Protected provenance:** [EXT-015D result 021, PR #2775](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2775) (protected merge commit 1ddcc677f3a4c90152ae638b3350ff0f7859d443); [homogeneous polynomial result 022, PR #2776](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2776) (separate protected review PR). Existing first-Ext result [019](FIXED_SOURCE_EXT1_ISOMORPHISM_019.md) and [audit 020](AGENT_CRITICAL_REVIEW_019_020.md).

## 1. Hostile check of the actual real-liquid counterexample

For the original fixed Fréchet source $H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}$, let $G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)}$ and $G=\varinjlim_bG_b$. The infinite weight product $\prod_{w\ge0}G$ is a **different coefficient object** than $G$ in theorem 019. Select bumps $\phi_w$ supported near separated points tending to infinity, and a continuous functional $\lambda:H\to\underline{\mathbb R}$ with $\lambda(h_0)=1$ for some $h_0$. Product universality gives a liquid morphism

$$
h\longmapsto(\lambda(h)\phi_w)_{w\ge0}.
$$

Its image at $h_0$ cannot belong to $\prod_wG_b$ for any fixed $b$. Thus the natural map $\varinjlim_b\mathrm{Hom}(H,\prod_wG_b)\to\mathrm{Hom}(H,\prod_wG)$ is **not surjective**. Each finite weight prefix *is* supported at a finite $b$. The categorical non-epimorphism is also valid: singleton evaluation is exact because $\underline{\mathbb R}$ is projective in the real-liquid category, and it detects this particular missing global section.

**Verdict:** Correct. The example refutes the naive interchange of uncompleted support colimit and weight completion. It does **not** contradict theorem 019 and is **not** a refutation of Costello–Gwilliam's correctly completed coproduct.

## 2. Hostile check of the derived inverse-limit anomaly

For the tower $K_N=[E\to E/A_N]$ with $E=\mathbb R^{(\mathbb N)}$, $A_N=\bigoplus_{j\ge N}\mathbb Re_j$, each differential onto $E/A_N\cong\mathbb R^N$ is surjective and each bonding map is surjective in each cochain degree. Thus $H^1(K_N)=0$. The inverse limit is $[E\hookrightarrow\mathbb R^{\mathbb N}]$, whose degree-one cohomology is the nonzero quotient $\mathbb R^{\mathbb N}/\mathbb R^{(\mathbb N)}$.

The tower of kernels $H^0(K_N)=A_N$ fails the Mittag–Leffler property; the Roos sequence $(e_N)$ is nontrivial modulo the difference map, giving exactly this quotient as $\varprojlim_N^1 A_N$. The explicit finite fixture in [021](fixtures/check_completion_roos_021.py) checks finite-prefix ranks and the growing support of partial solutions; the **infinite** nonvanishing follows from the argument, not the fixture.

**Verdict:** Correct. Surjective cochain maps do **not** imply that cohomology commutes with inverse limits. Conversely, a levelwise quasi-isomorphism between two degreewise-surjective towers does induce a quasi-isomorphism of their limits because both towers compute their homotopy limits. The source of a new class is a nonzero $\varprojlim^1H^0$ term, not a failure of degreewise surjectivity.

## 3. Audit of the homogeneous polynomial bridge

The relevant source is the **classical** completed symmetric power $E_w=\mathrm{Sym}^w_\pi(H)$, later realized into real liquid modules; the paper makes no unjustified identification with a derived liquid categorical symmetric power.

For every fixed finite weight $w$, Valdivia–Vogt gives $H\cong s$. The completed nuclear Köthe tensor theorem (Vogt and Lykova, Example 6.7) gives $s^{\widehat\otimes_\pi w}\cong s$, using the polynomial pairing of $\mathbb N^w$ with $\mathbb N$. Finite-group averaging is a continuous idempotent, so $E_w$ is a complemented Fréchet subspace of a space isomorphic to $H$. In particular the real-liquid source $\underline{E_w}$ is a retract of $\underline H$.

The natural target-stage comparison for $\mathrm{Hom}$ is isomorphic for the source $\underline H$ by LFO-013, and for first liquid Ext by 019–020. **Both properties pass to source retracts**, because Hom and Ext are additive in the source and the comparison is natural. Weight zero is the projective scalar object, and the same conclusion holds directly.

For any actual projective resolutions $P_{w,\bullet}$, the finite-prefix completed complex comparison is

$$
\varprojlim_N\varinjlim_b
\bigoplus_{w<N}\mathrm{Hom}(P_{w,\bullet},G_b)
\longrightarrow
\prod_w\mathrm{Hom}(P_{w,\bullet},G).
$$

Finite direct sums commute with filtered colimits, and the inverse limit of finite prefixes is their product. At this **linear-derived** layer all target cochain groups are real vector spaces, whose products and filtered colimits are exact. Thus the induced maps on cohomology $H^0$ and $H^1$ are precisely products of the already established per-weight comparisons and are isomorphisms. Here the weight quotient projections are **split**, so the degree-zero cohomology tower is Mittag–Leffler; the hostile derived example above does not apply to this particular split tower.

**Verdict:** Correct as an algebraic positive theorem for this specific family of real-liquid polynomial-source mapping complexes, in cohomological degrees zero and one. Nothing in the argument supplies smooth Costello–Gwilliam pro-cochains, completed monoidal liquid tensor comparisons in arbitrary degree, or an equivalence of interacting quantum observable factorization algebras.

## 4. What B.6 still requires

Costello–Gwilliam, *Factorization Algebras in Quantum Field Theory* Vol. I, Appendix B.6, distinguishes (i) complete differentiable filtered spaces and cofibrations (Definition B.6.0.7), (ii) completed coproducts (B.6.0.8), (iii) fibration, eventual finite-quotient stabilization and fiber quasi-isomorphism conditions for inverse-limit comparisons (Lemma B.6.0.11), and (iv) **smooth multilinear**, filtration-preserving maps (Definition B.6.1.1). Their [primary source](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf#page=479) was checked directly, including the mathematical requirements on printed pages 470–471.

The proofs in 021 and 022 verify a concrete **underlying linear-derived subproblem**, not the smooth cochain comparison. In particular, none supplies a specific differentiable plot on the full quantum observable complex or the Weiss-Cech completed descent map. These gates are retained as OPEN.

## 5. Status and next theorem obligation

| Work | Adjudication |
| --- | --- |
| 021: actual test-function-source obstruction to uncompleted weight/support interchange | ACCEPT, PROVED |
| 021: two-term Roos/Milnor derived completion counterexample | ACCEPT, PROVED |
| 021: safe comparison of degreewise-surjective quasi-isomorphic inverse towers | ACCEPT, PROVED UNDERLYING COMPLEXES |
| 022: symmetric powers of the fixed source are retracts of its nuclear Fréchet model | ACCEPT, PROVED |
| 022: weight-completed linearized polynomial-source comparison on $H^0,H^1$ | ACCEPT, PROVED |
| Actual Costello–Gwilliam smooth cochain equivalence | OPEN |
| Higher liquid Ext beyond degree one, interacting BV operations, complete quantum filtration, and Weiss descent | OPEN |

**Next mathematical obligation:** Construct the precise natural comparison morphism from the fixed-source polynomial mapping complexes of 022 to an **actual** differentiable pro-cochain model of the free linear theory on nested intervals. Supply the domain and codomain plot structures; verify all differentiable cofibration/fibration and smooth multilinear compatibility conditions at each finite quantum weight. Only after this explicit construction may one invoke B.6.0.11 and prove a completed Weiss-descent result. That research is agent-owned and does not require a routine Human Steward action.
