# EXT-015 REACH / 168 — a completed relative-scalar antiderivative for the second Green arm

**Primary mathematical disposition: CONSTRUCTIVE PARTIAL.** The second core $B$ of protected 165 has an exact whole-positive-regulator representative in the **existing** completed mixed 108.7 source, with an identity-partition pure-covector R1 coefficient and an explicitly proved fixed-stage scalar heat coefficient. Consequently the labelled and genuinely symmetric source-membership questions reduce to the **same single remaining core $A$**. The first core $A$, general Lemma 150.L, and residual $W$ acyclicity remain **OPEN**. This is a candidate primary claim pending source-locked mathematical review and protected admission, not MATHCERT certification.

## 1. Immutable contract and precise new claim

This computation uses the protected 165 primary (blob `24b82716d41d309438fcb7a97bbacab0b724afde`), 166 mathematical critic (`29b440786b9a7db1a414fbaaa33d259ff5eab787`), 167 ledger (`9f00bde4fc1e10ea62fd14f6b2475ba0a8741e60`), and their protected merge/readback in PRs 3313/3314. The exact inherited mathematical source blobs are 105 `a8ce66ff0edec33e2aff299550fca2089d671033`, 108 `587c15fd6e24f6e6b14de574ff878221cdbd5cb6`, 126 `5b05c6147d237ca1d22e4dcbce9262b0f038c163`, 141 `de6b608c8def91dd0b8b2d98fe410348ac92a17d`, 150 `03deca9212a9bea56743e482e5cb79edb46b9d7f`, 159 `555088f3da2c87dc02304dcf44b2738510f65062`, and 162 `20febc0e1196990addf446f0054f5e9e563ba615`. The restricted 168 assignment is governed by checkpoint CP188 and MATH-PROGRAMME #2657. No source class is enlarged.

Fix $\rho\in C_c^\infty(U)$, $\rho(0)\ne0$, $\chi\in C_c^\infty(U)$ as in 165, and the Gaussian heat density and one-dimensional Green kernel

$$
K(Y)=\frac{e^{-Y^2/2}}{\sqrt{2\pi}},\qquad
\kappa_\epsilon(y)=\epsilon^{-1}K(y/\epsilon),\qquad
e(t)=|t|/2.
\tag{168.1}
$$

Define the smooth positive-regulator convolution

$$
Q_\epsilon(t)=\int_{\mathbb R}e(t-y)\rho(y)\kappa_\epsilon(y)\,dy.
\tag{168.2}
$$

The two 165 cores are

$$
A_\epsilon(x,z)=\chi(x)e(x)\rho(z)\kappa_\epsilon(z),\qquad
B_\epsilon(x,z)=\chi(x)Q_\epsilon(x)\delta_0(z).
\tag{168.3}
$$

**Proposition 168.1 (exact complete source of the second arm).** The *actual* family $B$, before the uniform rapid quotient, is in $\mathcal P_2$ as defined in 108.7. It is represented by a single **no-hidden, identity-partition, order-zero** existing mixed history with fixed compact supports, fixed R1 cone and one fixed scalar polyhomogeneous heat stage. Its source map is jointly continuous on the completed projective coefficient source; compactly smooth parameter families $\rho(a,\cdot)$ with fixed physical support admit genuine 126 coefficient rows. In particular it is an exact source-level second-antiderivative of the already admitted $\partial_x^2B$ of 165.17, without asserting any inverse-derivative operation on general mixed histories.

## 2. Explicit existing 108.7 history and exact evaluation

Choose fixed $\eta_x,\eta_z\in C_c^\infty(U)$ such that $\eta_x=1$ on $\operatorname{supp}\chi$ and $\eta_z=1$ near zero. On the **two physical block coordinates** $(x,z)$ take

$$
T(x,z)=\chi(x)\delta_0(z),\qquad
a_\epsilon(x,z)=\eta_x(x)\eta_z(z)Q_\epsilon(x-z).
\tag{168.4}
$$

Use the identity partition, zero insertion derivative, identity proper projection, and the original physical density $dx\,dz$. The retained output is the 108.7 history

$$
q_*\partial^0(i_{\mathrm{id}})_*[a_\epsilon T]
=\chi(x)Q_\epsilon(x-z)\delta_0(z)
=\chi(x)Q_\epsilon(x)\delta_0(z)
=B_\epsilon(x,z).
\tag{168.5}
$$

The final equality is the ordinary restriction of a smooth coefficient to the support of $\delta_0(z)$; it is **exact for every $\epsilon>0$**, not a Wick expansion, approximation or rapid equivalence. There is no integration Jacobian to omit: $q=i_{\mathrm{id}}=\mathrm{id}$, with the standard $dx\,dz$ test-pairing density. The cutoff factors act as one on the support of $T$; all physical supports are fixed compact subsets of $U^2$.

The wavefront of $T$ has only $(0,\zeta)$ covectors. The only proper nontrivial two-block partition conormal is the conormal of $x=z$, whose nonzero covectors have the form $(\tau,-\tau)$. These cones are disjoint. Thus the original R1 graph stage $E_{s,K,\Gamma}$ may be chosen with a closed permitted pure-$z$ cone, with $s$ large enough for the fixed delta. The scalar factor is smooth for every positive regulator. The noncharacteristic R1 pullback, product and graph-stage tensor maps are *exactly* those admitted in 108 §§2,4; no forbidden overlapping distributional product, hidden-vertex anchor, or new conormal source is used.

It remains necessary to prove that $a_\epsilon$ is in one fixed, **complete** scalar stage of 105, not merely smooth for $\epsilon>0$. That is the content of the next section.

## 3. Fixed all-face scalar heat estimates

**Lemma 168.2 (heat-smoothed weighted Green cusp).** For every fixed compact $t$-interval, the actual function $(\epsilon,t)\mapsto Q_\epsilon(t)$, multiplied by a fixed compact cutoff in $t$, is polyhomogeneous on the ordinary two-point heat blowup of $\{\epsilon=0,t=0\}$, with compatible all-order b-derivative remainder estimates. Its index family may be fixed once and for all: integer powers without logarithms, including the nonnegative integer saturation, with front-face leading order at least $1$, strict regulator-face leading order at least $0$, and fixed lower auxiliary weights chosen below those exponents. The map $\rho\mapsto Q$ is continuous from each fixed-support $C_K^\infty$ stage to this **one** 105.5 complete scalar stage. Fixed smooth physical cutoff and pullback by $t=x-z$ preserve that stage on the complete two-vertex heat collision space.

**Proof.** At positive scale $Q_\epsilon''=\rho\kappa_\epsilon$, so $Q_\epsilon$ is smooth in $t$; its derivatives under any fixed $\epsilon>0$ are ordinary convergent Gaussian integrals. On the front chart $t=\epsilon X$, substitute $y=\epsilon Y$ to obtain the *exact* expression

$$
Q_\epsilon(\epsilon X)
=\epsilon\int_{\mathbb R}e(X-Y)\rho(\epsilon Y)K(Y)\,dY.
\tag{168.6}
$$

For each $N\ge0$, Taylor's formula with integral remainder gives, on bounded $X$-charts and after every prescribed finite ordinary or b-derivative,

$$
Q_\epsilon(\epsilon X)
=\sum_{n=0}^{N}\epsilon^{n+1}
\frac{\rho^{(n)}(0)}{n!}J_n(X)
+\epsilon^{N+2}\mathcal R_N(\epsilon,X),
\quad
J_n(X)=\int e(X-Y)Y^nK(Y)\,dY.
\tag{168.7}
$$

Every fixed derivative of $\mathcal R_N$ is bounded on compact $X$ sets by finitely many $C^r$ seminorms of $\rho$, using Gaussian polynomial moments. The same bounds hold after finite parameter derivatives of $\rho$. Thus the full front expansion has a fixed index family $1+\mathbb N_0$, with no escaping jet depth.

On either strict-face chart $|t|\ge\delta>0$, put

$$
M_{j,\epsilon}=\int y^j\rho(y)\kappa_\epsilon(y)\,dy
\quad(j=0,1).
\tag{168.8}
$$

Since $e(t-y)=(|t|-\operatorname{sgn}(t)y)/2$ whenever $|y|<|t|$, splitting the Gaussian integral at $|y|=|t|$ yields

$$
Q_\epsilon(t)
=e(t)M_{0,\epsilon}
-\tfrac12\operatorname{sgn}(t)M_{1,\epsilon}
+E_\epsilon(t),
\tag{168.9}
$$

where on any fixed strict-face compact set, every prescribed derivative in $t$, $\epsilon$ and smooth parameters of $E$ is $O(\epsilon^N)$ for **every** $N$. Indeed the integrand of $E$ is supported in the Gaussian tail $|y|\ge|t|$ and differentiated tail bounds are at most a fixed power of $\epsilon^{-1}$ times $\exp(-c\delta^2/\epsilon^2)$. Both $M_j$ have full even-power Gaussian expansions, with continuous coefficients and fixed all-order remainders, exactly as in 162.5. Thus the strict regulator face has fixed nonnegative integer index set and all derivative estimates.

At the front/strict corner use $X=t/\epsilon\to\pm\infty$. Writing $m_n=\int Y^nK(Y)\,dY$, a direct split at $Y=X$ gives

$$
J_n(X)
=e(X)m_n-\tfrac12\operatorname{sgn}(X)m_{n+1}
+O\!\left((1+|X|)^{n+1}e^{-X^2/2}\right),
\tag{168.10}
$$

with the corresponding fixed-order b-derivative estimates (allowing a harmless larger polynomial). This is exactly the overlap of the front expansion (168.7) with the moment expansion (168.9). In the complementary blowup chart $\sigma=\epsilon/|t|$, the Gaussian tail is flat as $\sigma\downarrow0$, uniformly in the remaining bounded tangential variables after the appropriate boundary monomial is removed. This proves recursive corner compatibility and fixed auxiliary-weight bounds. The coefficients are not just formal: all identities hold for the original Gaussian integral, retaining the actual flat remainders.

On the two-point heat space for $x,z$, use relative coordinate $t=x-z$ and a smooth center variable. Equation (168.6) treats its unique relative front face; (168.9) treats its strict face, and (168.10) treats their corners. The cutoff $\eta_x(x)\eta_z(z)$ is a fixed smooth multiplier with ordinary corner Taylor expansion; all integer shifts are already in the saturated index family. Every defining seminorm of the target 105.5 stage is bounded by finitely many fixed-support $C^r$ seminorms of $\rho$. This proves the asserted continuous map into the complete scalar stage. $\square$

## 4. Completion, 126 parameter rows, rapid relation and consequence

**Proof of Proposition 168.1, continued.** The coefficient pair in (168.4) is the simple tensor

$$
T\otimes a\in E_{s,K,\Gamma}\widehat\otimes_\pi S_\lambda,
\tag{168.11}
$$

with **one** fixed permitted cone, compact hull, scalar heat index/auxiliary-weight family and zero insertion derivative. By Lemma 168.2, $\rho\mapsto a$ is continuous in the complete scalar coefficient topology; $T$ is fixed in the complete graph stage. Their tensor map and the 108.7 evaluation have the continuous finite-seminorm estimates of 108 §§2,4. No replacement by a weaker positive-interior or pointwise-completion topology is made. With $\rho(a,y)$ smooth in an external finite-dimensional parameter on compact charts and a common compact $y$-support, differentiate (168.2) under the Gaussian integral. All source derivatives are literally $T\otimes\partial_a^\alpha a$, lie in the *same* completed stage with compact-chart bounds, and are mutually compatible coefficient derivatives. Taking these as the actual depth-$r$ rows (or their finite graph-order relaxations) gives the genuine 126 §4 row identities and entire evaluation compatibility. Nothing is inferred for arbitrary previously admitted 126 families; the open surjectivity issue in 126.14 is untouched.

The source represents $B$ before quotienting. Hence it represents its class after quotient by the *unchanged* uniformly rapid all-mixed-derivative ideal; the equality defect in (168.5) is exactly zero under **every** rapid seminorm. Physical $x$ differentiation of this same legal history is among the already closed source operators of 105/108, so its second derivative is the 165.17 $\partial_x^2B$ with precisely the $\chi$ cutoff corrections of 165.20. This constructs an antiderivative **for this one matched source output**, not a continuous inverse derivative on any general mixed coefficient space. $\square$

**Corollary 168.3 (one-core reduction).** In the actual two-slot 108.7 source image,

$$
B\in\mathcal P_2,\quad
F^{\mathrm{lab}}\in\mathcal P_2\iff A\in\mathcal P_2,\quad
F^{\mathrm{sym}}\in\mathcal P_2\iff A\in\mathcal P_2.
\tag{168.12}
$$

Indeed (165.6) gives $F^{\mathrm{sym}}=(A+B)/2+R^{\mathrm{sym}}$ with source-admitted $R^{\mathrm{sym}}$, and two is invertible over the real liquid heart. Adding or subtracting the now-admitted $B$ proves the equivalence. These are **membership equivalences, not a proof of $A$ membership**. In particular the genuinely symmetric input does not leave an independent $B$-arm source-membership blocker.

## 5. Hostile control: why the same-block delta-to-cusp replacement fails for $A$

There is a tempting *legal but wrong* candidate, using exactly the first matched partition $\{x,y\}\mid\{z\}$ from 165.18 and replacing its pure-block R1 delta by the fixed pure-block R1 cusp:

$$
C_\epsilon(x,z)
=\chi(x)e(x)\rho(z)\kappa_\epsilon(x-z).
\tag{168.13}
$$

This is a valid single existing 108.7 source: R1 $\chi(t)e(t)\rho(z)$ has only pure-$t$ wavefront; the relative Gaussian is an admitted two-block heat scalar; order-zero inclusion $x=y=t$ and proper forgetting of $y$ carry unit density. However **$C\ne A$**, and the discrepancy is not uniformly rapid. The exact joint-normal difference is

$$
(C-A)_\epsilon(\epsilon X,\epsilon Z)
\longrightarrow\rho(0)e(X)\bigl[K(X-Z)-K(Z)\bigr],
\tag{168.14}
$$

which is nonzero. More strongly, as ordinary physical distributions,

$$
C_\epsilon\longrightarrow\chi(x)e(x)\rho(x)\delta(x-z),
\qquad
A_\epsilon\longrightarrow\chi(x)e(x)\rho(0)\delta_0(z).
\tag{168.15}
$$

Choose any sufficiently small $a\ne0$ with $\rho(a)\ne0$ and $\chi(a)=1$; a fixed test supported close to $(a,a)$ pairs nontrivially with the first limit and vanishes on the second. Thus $C-A$ is not even weakly zero, much less rapid. Differentiating $C$ also produces the nonvanishing mixed terms from differentiating $\kappa_\epsilon(x-z)$; simply integrating the R1 delta on its matched block is not a source-level Green antiderivative of $\partial_x^2A$.

This control rejects **only this explicit same-block replacement**, not arbitrary finite completed histories. In particular neither the forbidden hidden R1 coefficient $e(x)\delta_0(y)$ nor an unproved scalar coefficient $\kappa_\epsilon(z)$ on the two-point *relative* heat space is imported as a putative repair. A general exclusion theorem must classify **all** legal finite histories and possible cancellations, including hidden vertices and completed coefficients; no such theorem is given here.

## 6. Accepted-scope matrix and exact successor

| Claim | 168 status |
| --- | --- |
| One explicit **existing** source for $B$, including all physical densities and exact positive-regulator values | **PROVED IN PRIMARY; awaits critical review/admission** |
| All-corner fixed-stage polyhomogeneity and completed/126 source rows for $B$ | **PROVED IN PRIMARY; awaits critical review/admission** |
| Symmetric and labelled membership governed by the same $A$ core | **CONDITIONAL ON REVIEW OF 168.1** |
| Naive same-block cusp replacement of the first matched delta history | **EXPLICITLY REJECTED**, nonrapid discrepancy |
| Exact completed source of $A$ or exhaustive nonmembership in $\mathcal P_2$ | **OPEN** |
| Universal Lemma 150.L or residual $W$ acyclicity | **OPEN** |
| Original R3, 126.14 full recovery, higher weights, actual lifting, M5/R4 | **OPEN** |

**Next scientific target 171, after source-locked critical mathematical review 169 and bounded ledger 170:** settle whether the first anchored-cusp core $A$ has *any* finite existing 108.7 source, or construct a genuine invariant excluding every finite admitted source on the actual restricted $W/Y$ domain. Account for hidden auxiliary vertices, all-corner fixed heat indices, R1 partition cones, proper physical densities, completed coefficient maps, rapid equivalence and genuine source-controlled 126 rows. Neither the legal matched second derivative nor the failed simple replacement is an exhaustive obstruction. Preserve OPEN status for general 150.L, $W$ acyclicity, original R3 and terminal REACH integration.