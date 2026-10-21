# EXT-015 REACH-R2 / 039 — a renormalized BV operator on the full fixed-label atomic-jet polynomial algebra

**Disposition: NEW BOUNDED MATHEMATICAL CANDIDATE; mathematical critical audit required.** This is a constructive extension of [R2 finite-part 032](R2_LOCAL_FINITE_PART_032.md) and is deliberately **compatible** with the moving-atom cusp obstruction [036](R2_MOVING_ATOM_CUSP_OBSTRUCTION_036.md). It constructs a genuine second-order differential/BV operator for **every finite polynomial of fixed-location atomic jets**, not merely a scalar subtraction, together with local diagonal counterterms, a well-defined zero-regulator endpoint and Wick-conjugated disjoint-open factorization. It does **not** establish smooth dependence on colliding locations, arbitrary distributional kernels, a physically canonical renormalization prescription or a general interacting QFT.

**Source:** protected D14 [028](D14_REGULATED_BV_SYZYGY_028.md), D21 [030](D21_MICROLOCAL_ZERO_SCALE_BV_030.md), reviewed R2 benchmark [032–034](R2_LOCAL_FINITE_PART_032.md), [R2 cusp no-go 036](R2_MOVING_ATOM_CUSP_OBSTRUCTION_036.md). **Research base protected head:** c1a74217a3d55a4db40394dc7dcef3acd38b6832. Parent: [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

## 1. Actual distributional jet sources, with fixed labels

Let $U\subseteq\mathbb R$ be open. For every $a\in U$ and integer $k\ge0$ define the **sign-normalized Dirac jet**

$$
j_{a,k}=(-1)^k\delta_a^{(k)},\qquad
\langle j_{a,k},f\rangle=f^{(k)}(a).
\tag{39.1}
$$

Let $e_{a,k}$ be an even generator and $\theta_{a,k}$ an odd generator representing the two free-field copies of the same distributional jet. Define the **free graded-commutative polynomial algebra**

$$
A(U)=
\mathrm{Sym}\bigl(\bigoplus_{a\in U,k\ge0}\mathbb R e_{a,k}\bigr)
\otimes
\Lambda\bigl(\bigoplus_{a\in U,k\ge0}\mathbb R\theta_{a,k}\bigr).
\tag{39.2}
$$

Every polynomial uses only finitely many labels, jet orders and generators. No topology on moving labels is imposed; the labels are fixed points. Define the degree-one Koszul differential by

$$
d(e_{a,k})=0,\qquad
d(\theta_{a,k})=e_{a,k+2},
\tag{39.3}
$$

extended by the graded derivation rule. It is the $\partial_x^2$ free differential on these normalized distributional jets, and $d^2=0$.

The algebra (39.2) is a **specified polynomial subspace** of the unrestricted distributional polynomials of D14 at positive regulator scale. It includes all same-site atomic products rejected by D21's unrenormalized microlocal domain.

## 2. Exact renormalized propagator coefficients

Fix a **real scheme parameter** $\lambda\in\mathbb R$. For distinct locations $a\ne b$, retain the exact zero-scale free propagator

$$
p^\lambda_{a k,b l}
=
\left.\partial_x^k\partial_y^l
\frac{|x-y|}{2}\right|_{x=a,y=b},
\qquad a\ne b.
\tag{39.4}
$$

This is well defined to every order because $a\ne b$, and vanishes when $k+l\ge2$. For equal locations $a=b$, instead choose the full, internally compatible smooth jet of the **local polynomial**

$$
Q_\lambda(x-y)=\frac{\lambda}{2}(x-y)^2,
\qquad
p^\lambda_{a k,a l}
=
\left.\partial_x^k\partial_y^lQ_\lambda(x-y)\right|_{x=y=a}.
\tag{39.5}
$$

Its only nonzero coefficients are

$$
p^\lambda_{a0,a2}=p^\lambda_{a2,a0}=\lambda,
\qquad
p^\lambda_{a1,a1}=-\lambda.
\tag{39.6}
$$

The complete matrix $p^\lambda$ is symmetric under exchange of the two generator indices. It is translation covariant and invariant under reflection of the ambient line when jet parity is transformed accordingly. The local ambiguity $\lambda$ is **not** fixed by unrenormalized pointwise convergence.

Define the even, second-order Wick contraction operator

$$
B_\lambda=
\frac12\sum_{a,k,b,l}
p^\lambda_{a k,b l}
\partial_{e_{a,k}}\partial_{e_{b,l}}.
\tag{39.7}
$$

It is an honest linear operator on $A(U)$: on each polynomial only finitely many summands act nontrivially, and each application lowers polynomial arity by two. It is *not* an infinite divergent scalar expression.

## 3. A genuine renormalized BV operator and Wick conjugation

**Theorem 39.1 (fixed-label atomic-jet BV).** Put

$$
\Delta_\lambda=[B_\lambda,d]
=\lambda\sum_{a\in U}
\partial_{e_{a,0}}\partial^L_{\theta_{a,0}},
\tag{39.8}
$$

where the odd derivative is a left Grassmann derivative. Then

$$
d^2=\Delta_\lambda^2=0,\qquad
d\Delta_\lambda+\Delta_\lambda d=0,\qquad
[B_\lambda,\Delta_\lambda]=0.
\tag{39.9}
$$

Consequently $d_\hbar=d+\hbar\Delta_\lambda$ is a square-zero differential on $A(U)[[\hbar]]$, and

$$
W_\lambda=\exp(\hbar B_\lambda),\qquad
W_\lambda d W_\lambda^{-1}
=d+\hbar\Delta_\lambda.
\tag{39.10}
$$

The operator $\Delta_\lambda$ is a **nonzero local second-order BV operator when $\lambda\ne0$**: in particular,

$$
\Delta_\lambda(e_{a,0}\theta_{a,0})=\lambda.
\tag{39.11}
$$

**Proof.** Apply the graded Leibniz formula to (39.3) and the constant-coefficient quadratic differential operator (39.7). The only terms in $[B_\lambda,d]$ arise when one even derivative of $B_\lambda$ hits the coefficient $e_{a,k+2}$ of $d$; they are

$$
[B_\lambda,d]
=
\sum_{a,k,b,l}
p^\lambda_{b l,a(k+2)}
\partial_{e_{b,l}}\partial^L_{\theta_{a,k}}.
\tag{39.12}
$$

For $b\ne a$ these coefficients vanish because off-diagonal derivatives of $|a-b|/2$ of total order at least two are zero. For $b=a$ the local polynomial jet (39.6) has a nonzero coefficient with a second derivative in the odd-source slot **only** at $k=l=0$, where it equals $\lambda$. This gives (39.8) on **all** polynomials, not just on quadratic generators.

Each term of $\Delta_\lambda$ contains one odd derivative, so its square vanishes by anticommutation of left Grassmann derivatives; even derivatives commute. The free differential also squares to zero because it kills every even generator. The anticommutator $d\Delta_\lambda+\Delta_\lambda d$ vanishes because $d$ differentiates with coefficients $e_{a,k+2}$ for $k\ge0$, while $\Delta_\lambda$ differentiates only with respect to the independent $e_{a,0}$ and $\theta_{a,0}$ variables; all odd-derivative cross terms cancel. Constant-coefficient even derivatives $B_\lambda$ commute with constant-coefficient mixed derivatives $\Delta_\lambda$. Finally, the Baker–Campbell–Hausdorff conjugation truncates after its first commutator and yields (39.10). For each finite polynomial, the formal exponential of $B_\lambda$ is actually a finite sum in polynomial arity. $\square$

This explicitly verifies a **class-wide differential**, square-zero, locality and Wick conjugation on the entire fixed-atom jet polynomial algebra. It is not a claim that the resulting theory already has a full B.6 differentiable-space enrichment.

## 4. Local counterterms from the positive regulator, without residual divergence

Take the D14 even mollifier $\kappa\in C_c^\infty(\mathbb R)$ supported in $[-1,1]$, of mass one, with $\kappa(z)=\kappa(-z)$. Let

$$
\kappa_\epsilon(z)=\epsilon^{-1}\kappa(z/\epsilon),
\qquad
P_\epsilon=\tfrac12|\cdot|*\kappa_\epsilon.
\tag{39.13}
$$

The positive-scale operator $B_\epsilon$ on the atomic jets has coefficients

$$
p^\epsilon_{a k,b l}
=\left.\partial_x^k\partial_y^lP_\epsilon(x-y)\right|_{x=a,y=b}.
\tag{39.14}
$$

Define the **local, same-site counterterm operator**

$$
C_{\epsilon,\lambda}
=\frac12\sum_{a,k,l}
\bigl(p^\epsilon_{a k,a l}-p^\lambda_{a k,a l}\bigr)
\partial_{e_{a,k}}\partial_{e_{a,l}}.
\tag{39.15}
$$

Every sum is locally finite on each polynomial. Note that this counterterm subtracts the full family of same-site **jet** divergences, not merely $\kappa_\epsilon(0)$ for the base generators.

**Theorem 39.2 (exact regulated endpoint on every fixed-label polynomial).** For any polynomial $F\in A(U)$, there exists $\epsilon_F>0$ such that

$$
(B_\epsilon-C_{\epsilon,\lambda})F=B_\lambda F
\quad\text{whenever }0<\epsilon<\epsilon_F.
\tag{39.16}
$$

The equality holds **coefficientwise and exactly** on that finite input polynomial, not just asymptotically. The same statement holds for every finite Wick exponential and its inverse acting on $F$. Thus

$$
W_{\epsilon,\lambda}^{\mathrm{ren}}
=\exp\bigl(\hbar(B_\epsilon-C_{\epsilon,\lambda})\bigr)
\longrightarrow W_\lambda
\tag{39.17}
$$

coefficientwise on the full finite-polynomial domain, with all divergent same-site jets canceled by a genuinely local counterterm operator. The renormalized BV differential is obtained by exact conjugation and is $d_\hbar$ from Theorem 39.1.

**Proof.** Each $F$ involves only finitely many atom labels $S$. If $a\ne b$ are labels in $S$, then choose $\epsilon$ smaller than $|a-b|$, using compact support of $\kappa$. On the entire interval between $a-b-\epsilon$ and $a-b+\epsilon$, the function $|z|/2$ is affine, so convolution with an even probability-density mollifier leaves it **exactly unchanged**, including all its derivatives at $a-b$. Hence $p^\epsilon_{a k,b l}=p^\lambda_{a k,b l}$ for distinct labels and every jet order. At the same label $a=b$ the counterterm (39.15) cancels by definition, leaving $p^\lambda$. Only finitely many labels and indices in $F$ and its contractions contribute, so (39.16) holds for sufficiently small $\epsilon$. Repeating the same argument on the finitely many polynomial outputs of iterated $B_\lambda$ proves (39.17). All counterterms are supported on identical atom labels; no correction is made at distinct positions. $\square$

Changing the arbitrary finite parameter $\lambda$ to another value $\lambda'$ changes $B_\lambda$ by a **local** constant-coefficient same-site operator and conjugates the two resulting quantum complexes exactly by $W_{\lambda'}W_\lambda^{-1}$. This is genuine finite renormalization-scheme dependence, although no canonical physical value of $\lambda$ is selected.

## 5. Disjoint-open prefactorization is algebraically coherent

For each open $U\subset\mathbb R$, the classical polynomial algebra $A(U)$ is functorial under inclusions by the corresponding inclusion of jet generators, and has ordinary multiplication maps from finitely many pairwise disjoint opens. The family $B_{\lambda,U}$ commutes with inclusions, because all its coefficients depend only on atom labels and local jet orders.

**Corollary 39.3 (renormalized algebraic prefactorization).** For pairwise disjoint opens $U_1,\ldots,U_r\subset V$, set

$$
\mu^\lambda_{U_1,\ldots,U_r\subset V}
=
W_{\lambda,V}\,
\mu^{\mathrm{cl}}_{U_1,\ldots,U_r\subset V}
\left(\bigotimes_iW_{\lambda,U_i}^{-1}\right).
\tag{39.18}
$$

These maps define a zero-scale **algebraic free prefactorization algebra** of cochain complexes on the fixed-atom jet polynomial functor, compatible with the renormalized BV differential $d_\hbar$. Associativity, permutation symmetry and the unit follow from conjugation of the classical diagrams.

The prefactorization includes Wick cross-contractions between distinct atom locations, but never requires continuous differentiability as two atoms move toward one another. Thus it respects the exact obstruction in 036 rather than bypassing it.

## 6. Hostile checks and scientific limits

- **Actual UV divergent generator:** on the coincident base even–odd jet, the regulator gives $\kappa_\epsilon(0)=\kappa(0)/\epsilon$, whereas the counterterm-corrected mixed BV contraction equals the finite nonzero $\lambda$. This is the concrete new feature over the scalar extension 032.
- **All jet orders controlled:** $C_{\epsilon,\lambda}$ subtracts every same-site derivative of $P_\epsilon$, including high-order jet divergences. Every polynomial has finite degree, so the operation is algebraically well-defined.
- **Higher polynomial degrees controlled:** the quadratic Wick operator and induced BV operator act on every polynomial degree. Exact BCH gives algebraic coherence, not merely a table of two-point values.
- **No moving-atom smooth plot claim:** $\lambda$ does not smooth the absolute-value cusp for independently moving atoms. The theorem operates with fixed atom labels; a full DVS enrichment still needs normal topology, allowed smooth families and renormalized configuration-space extension.
- **No universality claim:** the local finite jet $Q_\lambda$ is a chosen scheme, not proven canonical, regulator-independent without scheme data, compatible with every interaction, or defined on all distributional kernels. Overlapping-collision extension for general distributions remains outside the proof.
- **No logical shortcut for liquid Ext:** the R3 syzygy comparison is independent.

**Exact control:** The standard-library fixture [039](fixtures/check_fixed_atomic_bv_039.py) checks all graded operator identities on seeded finite atomic-jet polynomials with rational coefficients, pair symmetry and explicit local values. It does not certify the infinite-dimensional algebraic theorem on its own.

**Status:** This is a **bounded, substantive GB2 partial result** on the fixed-location atomic-jet subcategory, requiring an independent GCL mathematical critical audit. It is stronger than the earlier scalar GB1 benchmark but weaker than a distributionally smooth and fully differentiable renormalized BV theory. Keep issue #2797 and the parent EXT-015D open.
