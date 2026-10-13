# QFT-COND-005 / DRM-014 — Derived LF mapping and the higher-Ext gate

**Disposition:** Proved the *source-side* derived mapping formula; established a scalar-output vanishing case for its first Roos correction; exhibited an explicit algebraic counterexample showing that an exact degree-zero Hom comparison need not lift to degree-one Ext even with split monomorphic target stages. The **actual higher-Ext comparison for liquid compact-support output stages remains open**. No full Costello–Gwilliam B.6 comparison is claimed.

Dependencies: [LFO-013](LFO3_SURJECTIVITY_THEOREM_013.md), [DLI-011](DERIVED_LIMIT_OBSTRUCTION_011.md), [LPR-012](LIQUID_ROOS_PERSISTENCE_LFO3_012.md) and [CF-001](COMPLETE_FILTERED_LIQUID_WEISS_006.md).

## 1. Theorem DRM-1: derived mappings out of a compact-support source

Fix $0<p\leq1$, $\mathcal A=\mathrm{Liq}_p(\mathbb R)$, and $\mathcal C=D(\mathcal A)$. Choose a countable cofinal compact exhaustion $K_a$ of the Euclidean open $U$, and put

$$
E_a=\underline{\mathcal D_{K_a}(U)},\qquad
A_p(U)=\varinjlim_a E_a.
$$

Filtered colimits are exact in $\mathcal A$, so this filtered colimit of heart objects also computes their derived colimit.

**Theorem DRM-1.** For every $Y\in\mathcal C$, the enriched derived mapping object satisfies

$$
\mathrm{RHom}_{\mathcal C}(A_p(U),Y)
\simeq
R\varprojlim_a\mathrm{RHom}_{\mathcal C}(E_a,Y).
\tag{14.1}
$$

**Proof.** In any stable category, mapping **out** of a colimit converts it into a limit of mapping objects. Apply this to the filtered colimit defining $A_p(U)$. The inverse limit on the right is a homotopy limit, never an unqualified ordinary inverse limit. $\square$

Since we have a countable tower of complexes of real vector spaces, the Roos mapping-fiber formula yields the Milnor short exact sequence

$$
0\longrightarrow
\varprojlim\nolimits_a^1\mathrm{Ext}_{\mathcal A}^{n-1}(E_a,Y)
\longrightarrow
\mathrm{Ext}_{\mathcal A}^{n}(A_p(U),Y)
\longrightarrow
\varprojlim_a\mathrm{Ext}_{\mathcal A}^{n}(E_a,Y)
\longrightarrow0
\tag{14.2}
$$

for every integer $n$. Here the derived mapping group $\mathrm{Ext}^n(X,Y)$ means morphisms $X\to Y[n]$ in $\mathcal C$; if $Y$ is a complex, this is not necessarily the heart's Yoneda Ext. The standard Roos/Milnor assertion uses exactness of products of complexes of real vector spaces.

**A positive scalar-output case.** When $Y=\underline{\mathbb R}$, the tower

$$
\mathrm{Hom}_{\mathcal A}(E_{a+1},\underline{\mathbb R})
\longrightarrow
\mathrm{Hom}_{\mathcal A}(E_a,\underline{\mathbb R})
\tag{14.3}
$$

has surjective transition maps. Under the fully faithful Fréchet realization these are restrictions of continuous linear functionals, and Hahn–Banach extends every continuous real functional from the topologically embedded subspace $\mathcal D_{K_a}(U)$ to $\mathcal D_{K_{a+1}}(U)$. Therefore the tower is Mittag–Leffler and

$$
\varprojlim\nolimits_a^1
\mathrm{Hom}_{\mathcal A}(E_a,\underline{\mathbb R})=0.
\tag{14.4}
$$

The same holds for a fixed finite-dimensional real target. It does **not** follow that higher stagewise Ext vanishes, or that the corresponding first correction vanishes for arbitrary LF outputs.

For finitely many source opens, the derived tensor preserves filtered colimits separately. When the already-established nuclear Fréchet/liquid tensor comparison is applied at each finite support tuple, (14.1) extends to the multi-indexed source-stage system.

## 2. Theorem DRM-2: the exact remaining derived target question

Fix a nuclear Fréchet source $H$, notably one of the actual completed projective tensor stages $H_{\mathbf a}$. Let $G_b=\mathcal D_{L_b}(V)$ and $A_p(V)=\varinjlim_b\underline{G_b}$.

There is a canonical derived comparison

$$
\Theta_H:
\varinjlim_b\mathrm{RHom}_{\mathcal C}(\underline H,\underline{G_b})
\longrightarrow
\mathrm{RHom}_{\mathcal C}(\underline H,A_p(V)).
\tag{14.5}
$$

**Criterion DRM-2.** This is an equivalence **if and only if** the maps

$$
\varinjlim_b\mathrm{Ext}_{\mathcal A}^{n}(\underline H,\underline{G_b})
\longrightarrow
\mathrm{Ext}_{\mathcal A}^{n}(\underline H,A_p(V))
\tag{14.6}
$$

are isomorphisms for every $n\geq1$.

**Proof.** Filtered colimits of complexes of real vector spaces are exact, so the cohomology of the source of (14.5) is the colimit of its cohomology. LFO-013 proves the assertion in degree zero. Since $\underline H$ and each $\underline{G_b}$ are heart objects, negative Ext vanishes on both sides. Consequently the comparison is a quasi-isomorphism precisely when (14.6) holds in every positive degree. $\square$

A sufficient *conditional* hypothesis is that $\underline H$ admits a projective resolution by finitely presentable projectives of $\mathcal A$. Termwise Hom would then commute with all filtered target colimits. Neither nuclearity nor derived tensor flatness establishes that hypothesis for $\underline{\mathcal D_K(U)}$.

## 3. Theorem DRM-3: a split-inclusion algebraic Ext obstruction

**This is an example in an ordinary module category, not in the actual liquid test-function target diagram.** It shows why the logical step from underived LFO3 to derived LFO3 is invalid without more hypotheses.

Take $k=\mathbb R$, let $V$ be a vector space over $k$ with basis $e_0,e_1,\ldots$, and define the commutative square-zero ring

$$
R=k\oplus V,\qquad
(a,v)(b,w)=(ab,aw+bv),\qquad V^2=0.
$$

Let $M=R/V\cong k$, let $N_b=R^b$ with the **split inclusions** $R^b\hookrightarrow R^{b+1}$, and set $N=\bigoplus_{j\geq0}R$.

**Underived Hom comparison holds:**

$$
\varinjlim_b\mathrm{Hom}_R(M,N_b)
\xrightarrow{\sim}
\mathrm{Hom}_R(M,N).
\tag{14.7}
$$

Indeed, a map $R/V\to T$ corresponds to an element of $T$ annihilated by $V$. That annihilator is $V^b$ for $N_b$ and $V^{(\mathbb N)}$ for $N$. Thus the left side is exactly the right side.

**But the degree-one comparison is not surjective:**

$$
\varinjlim_b\mathrm{Ext}^1_R(M,N_b)
\longrightarrow
\mathrm{Ext}^1_R(M,N).
\tag{14.8}
$$

Apply $\mathrm{Hom}_R(-,T)$ to the short exact sequence $0\to V\to R\to M\to0$. Since $R$ is projective, the connecting exact sequence gives

$$
\mathrm{Ext}^1_R(M,T)
\cong
\mathrm{Hom}_R(V,T)/
\{v\mapsto vt:t\in T\}.
\tag{14.9}
$$

Define a map $f:V\to N$ linear over $R$, assigning to each basis vector $e_j$ the element $e_0$ in the target summand indexed by $j$ and zero in all other summands. It is $R$-linear because $V$ acts trivially on both $V$ and its image in the target's square-zero ideal. Every finite stage $N_b$ has a **uniform finite target-summand support bound**. Every coboundary $v\mapsto vt$ also has finite target-summand support, because $t\in N$ is a direct-sum element. But $f$ has unbounded target-summand support. Hence its nonzero extension class $[f]$ is not in the image of (14.8). $\square$

The source $M$ is cyclic but is not finitely presented: its first syzygy $V$ is infinitely generated. The example demonstrates that degree-zero Hom factorization plus even **split monomorphic** target transitions does not automatically imply degree-one derived factorization.

The accompanying exact finite fixture checks how many target summands the restriction of $f$ to the first $N$ basis vectors necessarily occupies. A finite regression cannot prove the infinite Ext statement; the displayed argument does.

## 4. The distinct Costello–Gwilliam B.6 enrichment gate

In Costello–Gwilliam, Vol. 1, Appendix B.6, Definition B.6.0.7 requires differentiable cofibrations and completeness; Definition B.6.0.8 requires **completed** coproducts. Lemma B.6.0.11 additionally requires conditions on inverse-system fibrations, stabilization of finite filtration quotients and quasi-isomorphisms on fibers. Definition B.6.1.1 concerns **smooth, filtration-compatible multilinear cochain maps**. These are not merely linear maps of underlying complexes.

Two questions must remain distinct:

1. **Actual liquid Ext gate:** compute or compare (14.6), starting with $n=1$ for an explicit $H=\mathcal D_K(U)$ and the actual target stages $G_b=\mathcal D_{L_b}(V)$. The algebraic example is only a warning, not a refutation.
2. **Differentiable filtered gate:** preserve Costello–Gwilliam's plotwise smoothness, cofibration/fibration conditions, filtration-compatible multilinear structure, complete tensor and the declared weak equivalences. The split-weight factorization construction in CF-001 does not supply a full equivalence of those categories.

The correct order of further work is: derive a real-liquid degree-one compact-support Ext comparison or obstruction; check source $\varprojlim^1$ where applicable; only then compare smooth B.6 mapping complexes and descent. No interacting or renormalized quantum observable result is claimed.

## 5. Sources and status

- Clausen–Scholze, [Condensed Mathematics and Complex Geometry](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf), Fréchet/liquid realization.
- Scholze, [Lectures on Analytic Geometry](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf), derived real liquid modules.
- Costello–Gwilliam, [Factorization Algebras in Quantum Field Theory, Vol. 1](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf), Appendix B.6.0.7–B.6.1.1.

**Mathematical status:** DRM-1 and the scalar Mittag–Leffler case are proved from standard source-backed results; DRM-2 is a proved exact criterion; DRM-3 is an explicit proved algebraic counterexample. **Higher Ext of the actual compact-support liquid stages is not yet determined.** No novelty claim or complete B.6 equivalence.
