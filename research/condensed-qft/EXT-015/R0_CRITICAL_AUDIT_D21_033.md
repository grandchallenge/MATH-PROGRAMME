# EXT-015 REACH-R0 / 033 — mathematical critical audit of D21 with an exact smooth-family obstruction

**Independent-role mathematical audit disposition:** D21 is admitted as a **candidate** on protected main, not thereby independently certified. This is a separate hostile review pass, based on the exact D21 candidate head 85fcf808582ee6bc505f19b5ce2ca739657dcd4b (merged as [PR #2788](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2788)), and the admissibility formulae in [D21/030](D21_MICROLOCAL_ZERO_SCALE_BV_030.md). It does not claim an external referee or separate authenticated GitHub identity. This audit supplies a new, explicit **negative theorem** ruling out an unqualified smooth-family upgrade.

**Sources:** Hörmander wavefront-set multiplication/pullback/pushforward calculus; Brouder–Dang–Helein, [Studia Mathematica 232 (2016), pp. 201–226](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/232/3/91541/continuity-of-the-fundamental-operations-on-distributions-having-a-specified-wave-front-set-with-a-counterexample-by-semyon-alesker) (normal topology and Alesker's counterexample); GCL [D14/028](D14_REGULATED_BV_SYZYGY_028.md) and [D21/030](D21_MICROLOCAL_ZERO_SCALE_BV_030.md).

## 1. Hostile audit of the algebraic domain

Let $\mathscr C_n$ be compact distributional kernels whose wavefront sets avoid every nonzero conormal to a partial diagonal, **including simultaneous disjoint collisions**. The following scope-limited checks withstand direct analysis:

**A. Multiplication by a singular pair kernel and proper pushforward.** The wavefront of $\delta(x_i-x_j)$ and of $|x_i-x_j|/2$ is contained in the pair diagonal conormal. Multiplication with any $T\in\mathscr C_n$ therefore meets the Hörmander product criterion. A nonzero covector on an output partial-diagonal conormal after projection would come from either a forbidden input conormal to the same partition with inserted singleton slots, or the simultaneous partition obtained by adding the contracted pair. Both are excluded. Intermediate contractions remain admissible and compactly supported. This independently checks the essential **set-theoretic microlocal closure** claimed by 30.1.

**B. Disjoint opens.** If input support sets are spatially disjoint, a cross-input partial diagonal has empty intersection with their product support. Any forbidden conormal on a partition that does not cross input groups would restrict to a forbidden wavefront in at least one input. Symmetrization is finite. This validates the algebraic prefactorization domain for pairwise disjoint opens, but makes **no** assertion of joint smooth multilinearity for a topology on a space of parameter families.

**C. Wick commutators.** Once repeated contractions exist, the distribution identity

$$
\partial_x^2(|x-y|/2)=\delta(x-y)
$$

gives the same graded constant-kernel Wick commutators as the already-admitted positive-scale model. This is a symbolic algebraic identity; strong topological continuity and smooth variation of the kernels are separate questions. The existing exact-rational D14 regression checks signs in finite mode, not distributional smooth-family estimates.

**D. Exact regulator limit.** For each **fixed** $T$ with wavefront set disjoint from the relevant diagonal conormals, the zero-scale collision trace can be defined. Local Fourier transversality supports convergence of the corresponding mollifier traces for that fixed $T$, with appropriate compact localization. The D21 proof does not yet provide a quantitative locally uniform estimate for all elements in a chosen family of admissible cones/supports. Its pointwise claim must not be silently promoted to a smooth-family or completed DVS theorem.

**E. Weiss at algebraic level.** A Weiss cover of $U$ induces an ordinary cover $\{U_i^n\}$ of every finite $U^n$. Finite arity, compact supports and cutoff partitions provide an exact augmented ordinary-vector-space Cech diagram. Graded permutation invariants are exact over the reals. The countable formal quantum tower is degreewise surjective; its *derived inverse limit* is represented by the ordinary inverse limit of these surjective complex towers, so levelwise Cech quasi-isomorphisms remain quasi-isomorphisms at this algebraic completion. This is **not** enough for completed differentiable B.6 descent.

## 2. Exact adversarial theorem: the naive smooth-distribution plot class fails

**Theorem 33.1 (failure of naive distributionally smooth BV plots).** Let $U$ be an interval containing a compactly supported nonzero real smooth function $\rho$. For $t\in\mathbb R$, define a compactly supported kernel

$$
T_t(x,y)=
\begin{cases}
\rho(x)\rho(y)\cos((x-y)/t),&t\ne0,\\
0,&t=0.
\end{cases}
\tag{33.1}
$$

Then:

1. Every $T_t$ lies in $\mathscr C_2(U)$; for $t\ne0$ it is smooth and for $t=0$ it is zero.
2. The curve $t\mapsto T_t$ is smooth as a curve into **the strong space of compactly supported distributions**, with all derivatives at zero equal to zero, provided the supports remain in one fixed compact set.
3. Its zero-scale mixed-pair or even-pair diagonal contraction is **not continuous** in that parameter:

$$
C^{\delta(x-y)}_{12}(T_t)=
\begin{cases}
\displaystyle\int_U\rho(x)^2\,dx,&t\ne0,\\
0,&t=0.
\end{cases}
\tag{33.2}
$$

Thus the class of all ambient distributionally smooth plots valued pointwise in $\mathscr C_n$ is **not closed under zero-scale BV contraction**. The ordinary strong distribution topology restricted to $\mathscr C_2(U)$ is insufficient to make this contraction continuous, let alone differentiably enriched in the required sense.

**Proof.** Smoothness of each fiber makes its wavefront set empty. Let $\Phi(x,y)$ be any test function and write $z=x-y$. The pairing for $t\ne0$ is an oscillatory integral whose amplitude $\rho(x)\rho(y)\Phi(x,y)$ is smooth and compactly supported in the relative variable. For every integer $N$ integrate by parts $N$ times in $z$: the pairing is bounded by $C_N |t|^N$ uniformly as $\Phi$ ranges over any bounded set of test functions. Parameter differentiation introduces only finite powers of $1/t$, derivatives of the smooth compact amplitude, and oscillatory sine/cosine factors; increasing $N$ proves that every parameter derivative tends strongly to zero, with derivative zero at the origin. Since the support is fixed and compact, this also gives smoothness in the usual fixed-support strong distribution space, and hence in the compact-distribution strict inductive limit.

For the contraction, multiplication by $\delta(x-y)$ and pushforward are valid because every fiber is smooth. On the diagonal $\cos((x-x)/t)=1$ for $t\ne0$, whereas $T_0=0$. The scalar (33.2) is therefore discontinuous at zero. Since the usual BV contractions include this diagonal operation with parity chosen appropriately, their putative ambient-plot continuity fails. $\square$

**Decisive distinction:** This is a counterexample to an attempted **topological or smooth upgrade**, not to the **fixed-fiber** algebraic well-definedness of 30.1–30.2. It also explains why the topological work in Track A must not be skipped.

## 3. How to repair the smooth-family domain

A minimally viable alternative is to restrict plot families to those with **locally uniform wavefront cone separation and fixed compact support**, and equip the fixed-cone spaces with an appropriate **normal topology** of Brouder–Dang–Helein. The oscillatory curve (33.1) is not a convergence-to-zero family in the required normal topology at its collision conormal, even though each fiber has empty wavefront set. In particular, selecting the cone $\Gamma=\varnothing$ on smooth fibers does not force convergence in the smooth-function topology; derivatives of the oscillatory kernels become unbounded.

**Required quantitative work:** choose a bounded normal-topology seminorm family for input and output cones; prove stability under all contracted-pair pullbacks, multiplication and projected pushforwards, including parameters; separate linear continuity from multilinear hypocontinuity. Show that a normal-topology-smooth curve with locally uniform bounds is sent to a smooth curve. Analyze gluing, admissible-cone inductive limits, topology on completed arity products, and B.6 cofibrations. This remains REACH-R1 #2796, **OPEN**.

## 4. Critical dispositions

| D21 claim | Mathematical review |
| --- | --- |
| Theorem 30.1, closure of the restricted distributional kernels under singular contraction and pushforward | **ACCEPT, algebraic/microlocal scope**; no implied continuity in naive distribution topology |
| Theorem 30.2, Wick algebraic complex and disjoint-open formal prefactorization | **ACCEPT, algebraic scope**, anchored to D14 signs; no general overlapping-open multiplication |
| Theorem 30.3, endpoint transport on each fixed microlocally admissible kernel | **ACCEPT WITH SCOPE LIMIT** for fixed-kernel formal distributional operation; requires explicit uniform cone-estimate proof before any DVS strengthening |
| Corollary 30.3a, algebraic Weiss descent over vector spaces | **ACCEPT, purely algebraic scope**; completed B.6 differentiable Weiss descent remains OPEN |
| Unrestricted DVS claim for pointwise-admissible ambient-distribution smooth families | **REJECT** by exact Theorem 33.1 |
| Interacting renormalized QFT, all distributional diagonals, higher liquid Ext | **NOT CLAIMED, NOT SOLVED** |

**R0 closeout boundary:** This is an independently reasoned GCL critical pass, not an external referee certificate. It supports the bounded **algebraic** D21 claims while recording a strict topological counterexample; the standalone broader B.6 and renormalization obligations remain open. Admit this audit through the protected PR process, preserving its exact provenance. Parent [REACH-R0 #2795](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2795).
