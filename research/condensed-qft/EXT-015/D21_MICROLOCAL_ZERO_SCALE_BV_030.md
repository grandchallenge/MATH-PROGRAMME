# EXT-015D / D21 / 030 — a microlocally admissible zero-scale free BV prefactorization model

**Disposition: NEW CANDIDATE MATHEMATICS; independent critical audit pending.** Relative to protected D14 [result 028](D14_REGULATED_BV_SYZYGY_028.md) and [review 029](AGENT_CRITICAL_REVIEW_D14_029.md), this note constructs a **proper, nontrivial** microlocally controlled subcollection of compact distributional polynomial kernels on which the zero-regulator BV differential and Wick prefactorization operations are well defined. It proves closure under all contractions, disjoint-open structure maps, and a coefficientwise zero-scale limit. It establishes algebraic Weiss descent. It **does not** construct an internal product for overlapping supports, renormalize excluded diagonal classes, prove Costello–Gwilliam B.6 differentiable-topological completion for these microlocal spaces, or solve the original liquid syzygy Ext problem.

**Exact starting revision:** D14 protected main at commit cb05306a6fb144155d5d4285a3f0847715c7e360.

**Mathematical references:** Hörmander's wavefront-set product, pullback and proper pushforward theorems (Analysis of Linear Partial Differential Operators I, §§8.2.4–8.2.12); Brunetti–Fredenhagen, [Microlocal Analysis and Interacting Quantum Field Theories](https://arxiv.org/abs/math-ph/9903028), for the wider context of transversality and renormalization; Costello–Gwilliam, [Factorization Algebras in Quantum Field Theory, Vol. I](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf), Appendices B.2 and B.6. The particular condition and closure argument below are established here, not attributed to those papers.

## 1. The actual domain

Let $U\subseteq\mathbb R$ be open. At arity $n\geq 1$ and for any set partition $\pi$ of $\{1,\dots,n\}$, define the partial diagonal

$$
D_\pi(U)=\{x\in U^n:\ x_i=x_j\text{ whenever }i,j\text{ belong to one block of }\pi\}.
\tag{30.1}
$$

Partitions of a subset may equivalently be completed by singleton blocks. Put

$$
\mathfrak N_n(U)
=
\bigcup_{\substack{\pi\text{ a partition}\\ \pi\text{ has a block of size }\geq2}}
\bigl(N^*D_\pi(U)\setminus 0\bigr)
\subset T^*U^n\setminus0.
\tag{30.2}
$$

Explicitly, for a block $B$ of $\pi$, a conormal covector obeys $\sum_{i\in B}\xi_i=0$, while singleton coordinates have $\xi_i=0$. Define

$$
\mathscr C_n(U)
=
\{T\in\mathcal E'(U^n):\
\mathrm{WF}(T)\cap\mathfrak N_n(U)=\varnothing\},
\qquad
\mathscr C_0(U)=\mathbb R.
\tag{30.3}
$$

Here $\mathcal E'$ denotes compactly supported distributions; all graded even/odd kernels are taken from the corresponding permutation-invariant graded pieces of $\mathscr C_n$. For $n=1$, $\mathfrak N_1=\varnothing$ and **every** compactly supported distribution is admitted. For $n\geq2$, smooth compactly supported kernels are admitted, as are many off-diagonal singular kernels. Thus this is neither the purely smooth subspace nor all of $\mathcal E'(U^n)$.

The restriction must involve **every partial diagonal, including simultaneous disjoint collisions**; avoidance of conormals to single pair diagonals is insufficient (Section 5).

We use $\mathscr C(U)=\bigoplus_{n\geq0}\mathscr C_n(U)$ at finite polynomial arity and $\mathscr C(U)[[\hbar]]$ coefficientwise in the formal quantum parameter. The direct sum is a graded vector space and a subcomplex; **we do not assert it is closed under multiplication of arbitrary two kernels on the same open**. The operative multiplications are the prefactorization maps from *pairwise disjoint* opens.

## 2. All required contraction operators preserve the domain

For two distinct slots $i,j$ let $p_{ij}:U^n\to U^{n-2}$ delete these coordinates. For any smooth $L(x_i,x_j)$, define

$$
C^L_{ij}(T)=p_{ij*}\bigl(L(x_i,x_j)\,T\bigr).
\tag{30.4}
$$

Every such map is well-defined and sends $\mathscr C_n(U)$ into $\mathscr C_{n-2}(U)$. It preserves compact support by properness of the projection restricted to $\mathrm{supp}(T)$.

At zero regulator scale use, in the difference variable,

$$
K_0(x,y)=\delta(x-y),\qquad
P_0(x,y)=\frac12|x-y|.
\tag{30.5}
$$

**Theorem 30.1 (microlocal closure).** Formula (30.4), interpreted as the Hörmander product followed by proper pushforward, defines $C^{K_0}_{ij}$ and $C^{P_0}_{ij}$ on every $\mathscr C_n(U)$, and both outputs again lie in $\mathscr C_{n-2}(U)$. The same conclusion holds for the smooth positive-scale kernels $K_\epsilon=\kappa_\epsilon(x-y)$ and $P_\epsilon=P_0*_{\mathrm{difference}}\kappa_\epsilon$ of D14. Coordinatewise finite-order differential operators, permutations and extension by zero along an open inclusion also preserve every $\mathscr C_n$.

**Proof.** Both singular kernels in (30.5), regarded as distributions on $U^n$, have wavefront sets contained in $N^*D_{\{i,j\}}\setminus0$, with all other covector components zero. Condition (30.3) ensures

$$
\mathrm{WF}(T)\cap\bigl(-\mathrm{WF}(K_0)\bigr)
=
\mathrm{WF}(T)\cap\bigl(-\mathrm{WF}(P_0)\bigr)
=\varnothing.
\tag{30.6}
$$

Thus their distribution products with $T$ exist canonically. All resulting products have compact support, so pushforward under $p_{ij}$ is defined.

To check the **important output condition**, suppose an output of (30.4) had a wavefront covector $\eta\in N^*D_\sigma$ in the remaining coordinates, for some nontrivial partition $\sigma$. The wavefront bounds for a product and pushforward imply that at some point of $\mathrm{supp}(T)$ there are covectors $\xi$ of $T$ (possibly zero) and $\nu$ of $L$ (possibly zero) such that

$$
\xi+\nu=p_{ij}^*\eta,
\qquad
\nu\in N^*D_{\{i,j\}}\text{ when }\nu\neq0.
\tag{30.7}
$$

If $\nu=0$, the nonzero covector $\xi=p_{ij}^*\eta$ lies in the conormal of the partition $\sigma$ extended by singleton blocks $i,j$, contradicting (30.3). If $\nu\neq0$, the base point also has $x_i=x_j$ and $\xi=p_{ij}^*\eta-\nu$ is a conormal to the **simultaneous** partial diagonal consisting of $\sigma$ together with the block $\{i,j\}$. The two blocks concern disjoint index sets, so $\xi$ is nonzero and (30.3) again excludes it. This argument applies to smooth $L$ with only the $\nu=0$ case, and to singular $K_0,P_0$ with both cases. The wavefront bounds also handle terms with a zero covector of $T$: these cannot account for a nonzero $\eta$ because $\nu$ has no component on the remaining coordinates. Compact supports justify each proper pushforward.

Differential operators do not enlarge wavefront sets. Extension by zero of a distribution already compactly supported in the open submanifold introduces no boundary singularities. Permutations preserve the finite family of partial diagonals. $\square$

**Remark (the decisive distinction).** Applying a BV contraction can leave a singularity on a *different* diagonal. The simultaneous-partition exclusion in (30.2) is what rules out this failure and permits repeated contractions.

## 3. A zero-regulator quantum prefactorization complex

Let $d$ be the free differential induced by $D=\partial_x^2$ from the odd linear generators to the even ones, with the same cohomological/Koszul conventions as D14. Define $\Delta_0$ by summing all allowed even–odd $C^{K_0}_{ij}$ contractions with signs; define the even degree-zero operator $B_0$ by summing the even–even $C^{P_0}_{ij}$ contractions, with the standard factor $1/2$ for equal-slot combinatorics.

**Theorem 30.2 (zero-scale free quantum structure).** On $\mathscr C(U)[[\hbar]]$ the contractions satisfy

$$
[d,\Delta_0]=0,\qquad \Delta_0^2=0,\qquad
[B_0,d]=\Delta_0,\qquad [B_0,\Delta_0]=0.
\tag{30.8}
$$

Consequently

$$
W_0=\exp(\hbar B_0),\qquad
d_0=d+\hbar\Delta_0=W_0dW_0^{-1}
\tag{30.9}
$$

are defined coefficientwise, $W_0$ is invertible and $d_0^2=0$. For pairwise disjoint $U_1,\dots,U_r\subset V$ the maps

$$
\mu^{(0)}_{U_1,\dots,U_r\subset V}
=W_{0,V}\,\mu^{\mathrm{cl}}_{U_1,\dots,U_r\subset V}
\left(\bigotimes_{a=1}^rW_{0,U_a}^{-1}\right)
\tag{30.10}
$$

define a **zero-scale free prefactorization algebra of formal cochain complexes** on the microlocal domain $\mathscr C$, with natural extension-by-zero unary maps.

**Proof.** When kernels are supported in pairwise disjoint opens, every coincident coordinate pair lies entirely within one input group. The wavefront bound for an exterior tensor product is the product of the individual wavefront sets with support-zero sections adjoined. Any nonzero forbidden conormal to a partition in the product would restrict to a nonzero forbidden conormal in one input group; a partition connecting different disjoint opens has no base point on the support. Thus exterior products from disjoint opens preserve (30.3), as do finite symmetrizations and their extension into $V^n$.

For the commutators, differentiate $P_0$ distributionally:

$$
\partial_x^2P_0(x,y)=\partial_y^2P_0(x,y)=\delta(x-y)=K_0(x,y).
\tag{30.11}
$$

On a two-generator even–odd product this is exactly $B_0d-dB_0=\Delta_0$, with signs fixed as in D14. On an arbitrary admissible kernel, the same identity follows from distributional integration by parts and the legitimate wavefront products/restrictions of Theorem 30.1, not from a density assertion about decomposable distributions. All fixed-kernel contractions commute in the graded sense when performed in distinct slots. After graded antisymmetrization, the two-odd contractions cancel, giving $\Delta_0^2=0$ and $[B_0,\Delta_0]=0$; the identity for $[d,\Delta_0]$ follows from (30.11) or the graded Jacobi identity. Every intermediate contraction stays in $\mathscr C$ by Theorem 30.1.

Each $B_0$ lowers finite arity by two, hence the formal exponential is finite on each polynomial coefficient and invertible. Its conjugation yields (30.9). Formula (30.10) conjugates the classical disjoint-open maps by a natural family of cochain isomorphisms; therefore the unit, permutation and associativity diagrams commute. Restriction of the global kernels to smaller opens implies that $B_0$ commutes with extension by zero, so unary maps are the usual inclusions. $\square$

The zero-scale operator $\Delta_0$ is strictly local across disjoint opens because $\delta(x-y)$ has diagonal support. Ordinary disjoint-open multiplication is therefore **also** a chain map for $d_0$ on this domain. Formula (30.10), which retains Wick cross-contractions through $P_0$, is the compatible zero-scale limit of D14's *specific* positive-scale Wick structures. These are distinct permissible prefactorization structures on the same underlying zero-scale complexes.

## 4. Compatibility with the admitted positive-scale family

**Theorem 30.3 (zero-scale endpoint of strict Wick transport).** Every positive-scale $W_\epsilon$, $d_\epsilon$ and $\mu^{(\epsilon)}$ from D14 restricts to $\mathscr C$. For each fixed compactly supported admissible kernel, the contractions of $K_\epsilon$ and $P_\epsilon$ converge distributionally to those of $K_0$ and $P_0$ as $\epsilon\downarrow0$. Consequently the formal operations have coefficientwise distributional limits on this restricted domain, and

$$
\mathcal R_{\epsilon\to0}=W_0W_\epsilon^{-1}
=\exp\bigl(\hbar B_{P_0-P_\epsilon}\bigr)
\tag{30.12}
$$

is an exact isomorphism of the positive-scale and zero-scale prefactorization diagrams on $\mathscr C$. The cocycle extends to the endpoint $0$.

**Proof.** Restriction/stability is Theorem 30.1. Convergence of $K_\epsilon\to\delta$ and $P_\epsilon\to |x-y|/2$ follows in distributions from the approximate identity. The transversality (30.6), together with local wavefront cones separated from the forbidden conormals over each fixed compact support, licenses transverse regularization and the product/pushforward limit. Equivalently, in local Fourier coordinates normal to a collision diagonal, the excluded normal directions permit the standard wavefront-restricted diagonal trace. Pairing the normal variable against $\kappa_\epsilon$ tends to this trace, while pairing against $P_\epsilon$ tends to the admissible Hörmander product with $P_0$. Since every coefficient of the exponential involves finitely many contractions, convergence holds termwise. The equality (30.12), intertwining and cocycle are exact algebraic conjugation identities, and do **not** rely on a uniform operator-norm UV limit. $\square$

**Scope of topology:** The theorem asserts distributional convergence for each fixed kernel and a formal algebraic prefactorization isomorphism. It does **not** yet certify joint continuity or a full B.6 differentiable-space homotopy-limit comparison for the LF/Hörmander wavefront topology. That analytic/topological upgrade is a separate gate.

### Corollary 30.3a (algebraic Weiss descent)

The classical underlying complex $U\mapsto\mathscr C(U)$ satisfies Weiss Čech descent **as a complex of real vector spaces**, and therefore its zero-scale Wick conjugate satisfies the same descent coefficientwise and after completion in the formal parameter $\hbar$.

**Proof.** For a Weiss cover $\{U_\alpha\}$ of $U$ and fixed arity $n$, the opens $\{U_\alpha^n\}$ cover the product $U^n$; every tuple of $n$ points is contained in some member of the Weiss cover. Compactly supported distributional kernels with condition (30.3) admit partitions of unity on $U^n$, since multiplication by a smooth cutoff neither enlarges wavefront sets nor invalidates (30.3). Symmetrize the cutoffs under the finite permutation group to retain graded invariants. The standard compact-support Čech contracting argument for extension-by-zero cosheaves gives an exact augmented Čech complex in each fixed arity. The classical differential preserves arity, so its total Čech comparison is a quasi-isomorphism arity by arity; direct sums are exact in real vector spaces. At every quotient modulo a finite power of $\hbar$ the filtration is a split finite sum of these comparisons, and its transition maps are surjective. Degreewise inverse limits of the resulting towers preserve the comparison via the Mittag–Leffler condition. Wick conjugation transports the complete diagrams and preserves quasi-isomorphisms. $\square$

This is **not** a declaration of completed differentiable B.6 descent; the requisite locally convex admissible-cone topology, smooth-family control and fibration statements remain unproved.

## 5. Hostile controls and sharp exclusions

**Pairwise tests fail.** Fix a compactly supported smooth cutoff $\rho$ nonzero near the origin and set

$$
T(x_1,x_2,x_3,x_4)
=\rho(x_1,x_2,x_3,x_4)\,
\delta(x_1-x_2-x_3+x_4).
\tag{30.13}
$$

On the support hypersurface, the singular covector is proportional to $(1,-1,-1,1)$; it is **not** conormal to any *single* pair diagonal. At a point where simultaneously $x_1=x_2$ and $x_3=x_4$, however, it is conormal to their common partial diagonal. After a $(1,2)$ delta contraction the output is a nonzero smooth coefficient times $\delta(x_3-x_4)$, so pairwise-transversality alone is not stable. Condition (30.2) excludes (30.13) where needed.

**Original UV-divergent classes still fail.** The two-generator same-point kernel $\delta_a(x)\delta_a(y)$ has a wavefront covector $(\xi,-\xi)$ at $(a,a)$ and violates (30.3). Thus the old $\kappa(0)/\epsilon$ divergence is not spuriously reclassified as convergent; the domain is genuinely smaller.

**No ordinary overlapping-open algebra.** Two allowed one-point deltas at the same $a$ may not be multiplied as an internal tensor kernel at $U$, since their exterior tensor lies outside $\mathscr C_2(U)$. This precludes an unrestricted internal BV algebra. It does **not** affect factorization maps from pairwise disjoint opens, where the supports cannot collide.

**Exact rational control.** For $f(x)=x^3(1-x)^3$ on $[0,1]$, treating the extension by zero only as a finite regularity diagnostic, the triangular polynomial integrations give

$$
\int_0^1 f(x)^2\,dx=\frac1{12012},
\quad
\frac12\int_0^1\!\int_0^1 f(x)f(y)|x-y|\,dx\,dy=\frac1{205920},
\tag{30.14}
$$

and the exact integration-by-parts identity

$$
\frac12\int_0^1\!\int_0^1f(x)f''(y)|x-y|\,dx\,dy
=\frac1{12012}.
\tag{30.15}
$$

The finite rational fixture [030](fixtures/check_microlocal_uv_030.py) verifies these numbers and the simultaneous-partition hostile witness without numerical floating-point tolerances. The fixture is not a substitute for wavefront analysis; $f$ extended by zero is not $C^\infty$.

## 6. Actual result and remaining decisive mathematics

| Obligation | Disposition |
| --- | --- |
| A nontrivial proper zero-scale domain closed under all free BV and Wick contractions | **PROVED here as a candidate**, subject to independent audit |
| Formal free zero-scale prefactorization and exact extension of D14 positive-scale transport | **PROVED here as a candidate** |
| Algebraic, coefficientwise formal Weiss descent | **PROVED here as a candidate** |
| Completed Costello–Gwilliam B.6 differentiable Weiss descent for wavefront-constrained spaces | **OPEN**; requires chosen nuclearity/completion/fibration model and uniform family-wavefront estimates |
| Canonical counterterms extending diagonal-singular local distributional kernels | **OPEN** |
| Interacting quantum field theory or unrestricted local BV algebra | **NOT CLAIMED** |
| Actual first projective liquid syzygy $K_0$ Ext¹ filtered-output comparison, hence higher fixed-source Ext | **OPEN**; unaffected by this construction |

**Next substantive mathematics:** (1) put $\mathscr C_n$ in a precisely specified LF/Hörmander locally convex smooth-family category and prove (or refute) the completed B.6 descent after formal completion in $\hbar$; (2) determine explicit extensions/counterterms for a first excluded diagonal class, with compatibility with (30.12); (3) separately resolve $\varinjlim_b\mathrm{Ext}^1_{\mathrm{Liq}_p}(K_0,G_b)\to\mathrm{Ext}^1_{\mathrm{Liq}_p}(K_0,G)$ for the actual projective cover of [016](AGENT_CRITICAL_REVIEW_AB_016.md), not an imagined Fréchet replacement.

**Provenance boundary:** This is a new GCL mathematical candidate, not an independently certified result. The earlier D14 protected-admitted mathematics remains untouched; EXT-015D and QFT-COND-005 stay open.