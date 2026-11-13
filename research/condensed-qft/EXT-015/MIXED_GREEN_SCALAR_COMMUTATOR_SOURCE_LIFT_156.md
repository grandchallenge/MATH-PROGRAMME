# EXT-015 REACH / 156 — mixed Green/scalar commutator and a legal Gaussian–R1 lift

**Disposition: NEW BOUNDED POSITIVE SOURCE-LIFT SECTOR; GENERAL LEMMA 150.L OPEN.** This primary construction exhibits exact completed 108.7 source representatives for a nontrivial Gaussian/Wick scalar edge coupled to an arbitrary *spectator-coordinate* R1 distribution, even when that distribution is singular. It also gives the exact scalar/Green commutator and proves a finite-separated-mode obstruction. It does **not** prove mixed lifting for arbitrary distinct-block histories, the residual joint-kernel acyclicity, the original R3 or complete REACH.

## 1. Exact mathematical inputs and scope

| Protected scientific input | Git blob |
| --- | --- |
| [105: scalar heat stages and Wick edge](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | a8ce66ff0edec33e2aff299550fca2089d671033 |
| [108: finite evaluated histories and completed coefficients](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| [126: source-controlled parameter rows](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [147: intrinsic diagonal jet decomposition](WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md) | 89b3d4a835f3750114e983854585e33d8184cb1f |
| [150: primitive, R1 convolution and unresolved 150.L](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) | 03deca9212a9bea56743e482e5cb79edb46b9d7f |
| [153: microlocal audit](MIXED_GREEN_KERNEL_MAPPING_AUDIT_153.md) | ad0ba1a607e03337dd7489b1d2ea3415fd2afed9 |
| [154: bounded logical critical review](AGENT_CRITICAL_REVIEW_GREEN_MAPPING_154.md) | 7cd9ef2c329f87f97278296fb6c6ee3cdfb25058 |
| [155: acceptance ledger](GREEN_MAPPING_AUDIT_ACCEPTANCE_155.md) | f453eaab8a7d34fdab1efb8f3e3c980df5dc6722 |

The current protected checkpoint CP184 in the registered REACH checkpoint assigns a **construct-or-refute** test of a mixed completed source lift. We use the original real liquid category, positive regulator, Gaussian normalization, source stages, partition-conormal R1 restriction, scalar index conventions and physical density. There is no enlargement of the source category. The new result is restricted to one identity-partition two-slot history with a spectator R1 coefficient; it is a genuine subcase, not the universal 150.L.

## 2. Exact scalar–Green commutator

Let $v\in\mathcal E'(U^2)$, let $a=a(x,z)$ be smooth near the common compact supports, and put $e(t)=|t|/2$, $C_j=e*b_j$, $m_j v(z)=\int y^jv(y,z)\,dy$. With the compact normalized primitive from 150.3,

$$
h_1v(x,z)=\int e(x-y)v(y,z)\,dy
-\sum_{j=0}^1C_j(x)m_jv(z).
\tag{156.1}
$$

All integrals are distributional proper pushforwards using ordinary $dy$. Multiplication by $a$ is smooth at every fixed regulator. Applying the definition twice, without assuming commutation, gives the exact identity

$$
\begin{aligned}
h_1(a v)-a(x,z)h_1v
={}&\int e(x-y)\bigl[a(y,z)-a(x,z)\bigr]v(y,z)\,dy\\
&-\sum_{j=0}^1 C_j(x)\bigl[m_j(a v)(z)-a(x,z)m_jv(z)\bigr].
\end{aligned}
\tag{156.2}
$$

This is a whole-distribution identity on the common compact hull, not a formal equality of regulator coefficients. In the first integral the extra output coordinate is independent of the original coefficient, so the distribution product is defined by the wavefront transversality of 153.3. For a polynomial $a(y,z)$ the difference $a(y,z)-a(x,z)$ is divisible by $y-x$, giving a finite combination of convolutions with $t|t|/2$ against smooth-polynomially weighted input distributions, plus the displayed finite moment corrections. This does **not** turn arbitrary regulated scalar factors into finite legal mixed histories.

A scalar depending only on the spectator variable $z$ commutes with both partial convolution and moment correction, and thus with $h_1$. The exact counterexample in review 154 shows why a scalar depending on the integrated variable cannot be moved out without the commutator.

## 3. An exact admitted Gaussian–spectator R1 source lift

**Theorem 156.1 (completed Gaussian–spectator lift).** Fix a nonempty interval $U$, a compact $K\Subset U$, and $\chi,\theta\in C_c^\infty(U)$ with $\chi=1$ on an open neighborhood $O$ of $K$, $\theta=1$ on a neighborhood of $K$ and $\operatorname{supp}\theta\Subset O$. Let $b_0,b_1$ be the fixed moment-normalizing bumps of 150.3. Fix an output cutoff $\psi\in C_c^\infty(U)$ equal to one on the interval hull of $\operatorname{supp}\chi\cup\operatorname{supp}b_0\cup\operatorname{supp}b_1$; choose $\phi\in C_c^\infty(U)$ with $\phi=1$ on $\operatorname{supp}\psi$.

Let $\rho\in E_{s,K,\Gamma}^{(z)}$ be any one-coordinate compact distribution, including a point delta or its derivatives, and let $s_\epsilon(z)$ occupy one *fixed admissible one-slot scalar power/logarithmic stage* of 105.5, independent of the integrated coordinate $y$. Write

$$
\kappa_\epsilon(t)=\frac{1}{\sqrt{2\pi}\epsilon}
\exp\!\left(-\frac{t^2}{2\epsilon^2}\right),
\qquad
v_\epsilon(y,z)=\chi(y)\,\kappa_\epsilon(y-z)\,s_\epsilon(z)\rho(z).
\tag{156.3}
$$

This is an admitted distinct-block mixed 108.7 input. There is an **exact equality of actual positive-regulator distributions** between $h_1v_\epsilon$ and one legal output history with identity partition, no extra singular jet, fixed R1 coefficient $\phi(x)\rho(z)$ and a scalar stage on the ordinary two-vertex collision heat space. The output source map is jointly continuous on every fixed complete $E_{s,K,\Gamma}^{(z)}\widehat\otimes_\pi S_\lambda^{(z)}$ input stage. Its support, output R1 cone, scalar indices, auxiliary weights and finite history list are fixed independently of relaxed Sobolev orders and the compatible 126 rows in **this subspace**. The result does not assert a mapping for an arbitrary $T(y,z)$, hidden-vertex history or same-block jet.

**Proof, Step A: exact Gaussian convolution and normalized moments.** By the original Wick identity 105.4, with standard Gaussian normalization,

$$
P_\epsilon(t):=(e*\kappa_\epsilon)(t)
=\frac{\epsilon}{\sqrt{2\pi}}
e^{-t^2/(2\epsilon^2)}
+\frac{t}{2}\operatorname{erf}\!\left(\frac{t}{\sqrt2\epsilon}\right),
\qquad P_\epsilon''=\kappa_\epsilon.
\tag{156.4}
$$

Define smooth tails

$$
\begin{aligned}
R_\epsilon(x,z)&=\int e(x-y)(\chi(y)-1)\kappa_\epsilon(y-z)\,dy,\\
r_{j,\epsilon}(z)&=\int y^j(\chi(y)-1)\kappa_\epsilon(y-z)\,dy
\quad(j=0,1).
\end{aligned}
\tag{156.5}
$$

The integrands in (156.5) are not compact in $y$, but Gaussian domination makes the integrals absolutely convergent, and they equal the differences of well-defined compact input integrals and full Gaussian moments. Because $\chi=1$ on $O\supset\operatorname{supp}\theta$, choose a positive distance $\delta$ from $\operatorname{supp}\theta$ to $\operatorname{supp}(\chi-1)$. If $z\in\operatorname{supp}\theta$, every $y$ in the tail integration obeys $|y-z|\ge\delta$. Polynomial factors from physical, parameter and regulator derivatives are dominated by $\exp(-\delta^2/(4\epsilon^2))$ times a fixed inverse power of $\epsilon$. For every $N$ and every fixed multi-derivative, the product of $\theta(z)$ with each $R_\epsilon$ and $r_{j,\epsilon}$ is $O(\epsilon^N)$ in every compact physical $C^r$ seminorm. For $R_\epsilon$, the first two $x$ derivatives follow from the dominated sign kernel, and the higher derivatives follow exactly from

$$
\partial_x^2R_\epsilon=(\chi(x)-1)\kappa_\epsilon(x-z).
\tag{156.6}
$$

This also controls derivatives when the integration point crosses the $x$-diagonal: Gaussian separation, not a fictitious smoothness of $e$, supplies the bound.

The uncut Gaussian zeroth and first moments are $1$ and $z$. Since $s_\epsilon(z)\rho(z)$ is independent of $y$, the genuine distributional moments are

$$
m_0v_\epsilon=s_\epsilon\rho\, (1+r_{0,\epsilon}),
\qquad
m_1v_\epsilon=s_\epsilon\rho\, (z+r_{1,\epsilon}).
\tag{156.7}
$$

Hence actual distributional convolution and subtraction yield

$$
\begin{aligned}
h_1v_\epsilon(x,z)=s_\epsilon(z)\rho(z)\bigl[
&P_\epsilon(x-z)-C_0(x)-zC_1(x)\\
&+R_\epsilon(x,z)-C_0(x)r_{0,\epsilon}(z)
-C_1(x)r_{1,\epsilon}(z)\bigr].
\end{aligned}
\tag{156.8}
$$

There is **no discarded flat error** in (156.8): the tail terms are retained as actual scalar functions.

**Step B: legal finite completed source.** Define the scalar coefficient

$$
A_\epsilon(x,z)=\psi(x)\theta(z)s_\epsilon(z)
\bigl[P_\epsilon(x-z)-C_0(x)-zC_1(x)
+R_\epsilon(x,z)-C_0(x)r_{0,\epsilon}(z)-C_1(x)r_{1,\epsilon}(z)\bigr].
\tag{156.9}
$$

The product $\psi\theta P_\epsilon$ is an admitted Gaussian/Wick scalar edge on the existing two-vertex collision space by 105.4–105.6. The cut-off functions $C_0,C_1$ and multiplication by $z$ are smooth physical scalar decorations. The last three terms in the square bracket, after multiplication by $\psi\theta$, are smooth and **flat with every derivative** at the regulator boundary. On every full collision corner, $\epsilon$ is a positive smooth unit times a finite monomial of boundary defining functions. Arbitrarily high $\epsilon$ powers absorb every prescribed corner weight and finite b-derivative loss, so these terms lie in the existing complete scalar flat-remainder stage of 105.5. They need no new asymptotic index family. Pulling $s_\epsilon(z)$ back from its allowed one-slot stage, then multiplying these fixed scalar factors, is a continuous scalar-stage map by 105.6, with one fixed finite union of index families and weight relaxations.

Let the R1 coefficient be $T'(x,z)=\phi(x)\rho(z)$. Its nonzero wavefront covectors have **zero $x$ component**, and hence cannot be forbidden conormals to the $x=z$ partition. The fixed smooth tensor map from the one-slot complete graph stage is continuous into a two-slot R1 graph stage with cone supported in $\{\xi_x=0\}$. Since $\phi=1$ on $\operatorname{supp}\psi$, the legal identity-partition 108.7 history

$$
q_*[A_\epsilon T']=A_\epsilon(x,z)\phi(x)\rho(z)
=h_1v_\epsilon(x,z),\qquad q=\operatorname{id},
\tag{156.10}
$$

is exactly the evaluated result: $\theta=1$ on the support of $\rho$, and the normalized primitive vanishes outside the hull where $\psi=1$.

All scalar operations and the fixed smooth tensoring have finite seminorm estimates, so their bilinear product extends continuously from simple tensors to the **completed projective** input. A parameter derivative acts by Leibniz on $s_\epsilon$ and $\rho$; the same fixed maps transport every compatible finite-order 126 row and commute with the actual derivative of its evaluated family. Relaxing the R1 Sobolev order does not change $\chi,\psi,\theta,\phi$, the output cone, source history or scalar index family. This is source-controlled continuity for the explicitly stated tensor subspace, without extrapolation to all of (150.9). $\square$

**Singular witness.** Choosing $\rho=\delta_{z_0}$ for $z_0\in K$ gives a source whose singular R1 coefficient is genuine, not a smooth surrogate. Its output R1 cone consists of covectors in the $z$ direction; multiplying by the smooth positive-scale Gaussian/Wick scalar and the actual flat tails creates no pure diagonal-conormal wavefront. The exact output is legal even though the formal interior zero-width Green factor would be forbidden as a standalone augmented source.

## 4. No finite separated-mode replacement for this Gaussian sector

**Proposition 156.2 (exact finite-rank obstruction).** The Gaussian factor $\kappa_\epsilon(y-z)$, and its normalized Green primitive on a suitable smooth compact input, cannot be represented for all positive $\epsilon$ by any **fixed finite number** of modes of the form

$$
\sum_{j=1}^{N} s_{j,\epsilon}(z)\,
h_1\bigl(f_j(y,z)\chi(y)\rho(z)\bigr),
\tag{156.11}
$$

where the $f_j$ are independent of $\epsilon$ and smooth in $(y,z)$, while the $s_{j,\epsilon}$ depend only on the spectator $z$ and the regulator. This excludes a finite separated-coordinate mode ansatz, **not** all finite legal histories 108.7.

**Proof.** Choose an open subinterval $I\Subset U$ containing $z_0$, with $\chi=1$ there and the normalized bump supports outside $I$ (the two bump moment conditions can be realized inside another disjoint subinterval). Choose smooth $\rho$ with $\rho(z_0)\ne0$. If (156.11) equalled $h_1(\chi\kappa_\epsilon\rho)$ as distributions for every small $\epsilon$, differentiate twice in $x$ and restrict to $x\in I$. Since both moment reinsertion bumps vanish on $I$, 150.4 gives

$$
\kappa_\epsilon(x-z_0)
=\sum_{j=1}^{N}s_{j,\epsilon}(z_0) f_j(x,z_0).
\tag{156.12}
$$

The right side lies in the fixed $N$-dimensional span of the $f_j(\cdot,z_0)$. Choose $N+1$ distinct positive Gaussian rates $\lambda_r=1/(2\epsilon_r^2)$. The functions $\exp[-\lambda_r(x-z_0)^2]$ are linearly independent on $I$: if a combination vanishes there, its even derivatives of orders $0,2,\ldots,2N$ at $x=z_0$ give a Vandermonde matrix in the distinct $\lambda_r$, with nonzero determinant. Gaussian normalizing constants are all nonzero. This contradicts the fixed $N$-dimensional span. $\square$

The contrast is substantive: the single **nonseparable Gaussian/Wick scalar edge** in (156.9) is a finite legal source history, whereas every fixed finite **separated** mode ansatz fails. Thus a failed Fourier/separation method does not imply nonrepresentability in the actual source category.

## 5. Exact finite hostile controls

The standard-library [156 fixture](fixtures/green_mixed_scalar_controls_156.py) checks the affine moment normalization and second-difference Green identity; exhausts all 242 nonzero ternary five-site input vectors over 11 output points for the whole commutator (156.2), giving 2662 exact rational pairings; verifies failure of the naive commutation on a point input; and checks nine exact nonsingular Gaussian-rate sampling matrices. Those finite tests detect algebraic errors. The infinite-rank theorem follows analytically from the Vandermonde derivative argument, and the analytic Gaussian source-stage theorem follows from the explicit uniform Gaussian tail estimates plus accepted 105/108/126 mapping results, **not** from the fixture.

## 6. Scope, negative controls and next mathematical obligation

| Problem | This primary return |
| --- | --- |
| Exact scalar–Green commutator | **PROVED** as ambient whole-distribution identity |
| Gaussian edge with arbitrary spectator R1 coefficient | **PROVED**, actual legal fixed-stage finite 108.7 source and completed tensor map |
| Fixed source-controlled 126 rows in that subspace | **PROVED** with common supports/cones and one scalar index stage |
| Universal finite separated-mode Gaussian ansatz | **DISPROVED**, narrow class only |
| Arbitrary mixed scalar/R1 source with R1 singular dependence on integrated variable | **OPEN** |
| Hidden vertices, arbitrary collision jets and all augmented corners | **OPEN** |
| Full restricted source-lifting lemma 150.L | **OPEN** |
| Residual joint cochain kernel $W$ and original R3 | **OPEN** |
| 126.14 full family recovery; higher weights; lifting; M5/R4 | **OPEN** |

The next frontier is a **non-spectator R1 test**: take a source with a genuine admissible conormal involving the integrated coordinate and a Gaussian edge that collides with it, calculate the resulting boundary profiles on the full augmented heat corner, and determine whether a finite existing scalar/R1 history with fixed stages represents it. No assumed scalar commutation, no escaping scalar-index modes, and no insertion of a zero-width positive-interior Green factor is allowed. If no legal representation exists, demonstrate exclusion from *every* permitted finite 108.7 history; failure of an ansatz alone is insufficient.

**Custody:** 156 is a new primary result with bounded claims and an exact finite fixture. It must undergo a separate source-locked mathematical critic pass 157, ledger 158, protected CI/merge/readback and checkpoint reconciliation. No inference of review, acceptance or programme closure is made by authoring this source.
