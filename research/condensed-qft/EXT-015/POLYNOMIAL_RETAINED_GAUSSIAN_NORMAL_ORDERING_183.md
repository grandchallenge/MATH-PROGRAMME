# EXT-015 REACH / 183 — polynomial retained-coordinate normal ordering across hidden Gaussian edges

**Primary mathematical disposition: BOUNDED POSITIVE NORMAL-ORDERING IDENTITY WITH CONDITIONAL FIRST-CORE EXCLUSION.** A fixed finite polynomial in the retained output coordinate multiplying a terminal Gaussian convolution can be moved exactly onto its compact upstream distribution as a finite differential operator. Consequently, polynomial retained-coordinate scalar decorations do **not** escape protected 180's mixed Gaussian-width independence theorem. This conclusion is conditional on actual terminal factorization and, for a target-width obstruction, the effective original R1 cone. It neither exhausts legal 108.7 histories nor solves the full first Green-core source membership.

## 1. Protected source and genuinely new boundary

Retain original protected scalar heat stages105 (Git blob a8ce66ff0edec33e2aff299550fca2089d671033), original complete mixed-source108 (587c15fd6e24f6e6b14de574ff878221cdbd5cb6), parameter rows126 (5b05c6147d237ca1d22e4dcbce9262b0f038c163), joint-corner165 (24b82716d41d309438fcb7a97bbacab0b724afde), protected terminal theorem177 (8f9f214cfced47d7a52790fab42544b6035e56ad), and protected mixed-width primary180 (fac58764ac29e518ac522e0451a9c9829e86720b). Primary180 has exact head 1abb1a1b16d113732bf05daeb796b153d901c39a, protected [PR3344](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3344) merge 28d978e788c9a1930a00056a0044ae3f4a124469; its blob was read back on protected main. Logical critical181 and bounded ledger182 are the separate [PR3346](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3346) admission work; no protected identity for that PR is presumed here.

As in 165, fix $f(x)=\chi(x)|x|/2$, compact smooth $\rho$ with $\rho(0)\ne0$, and the remaining first Green core

$$
A_\epsilon(x,z)=f(x)\rho(z)\kappa_\epsilon(z),
\qquad
\kappa_\sigma(t)=
\frac{1}{\sqrt{2\pi}\sigma}\exp\!\left(-\frac{t^2}{2\sigma^2}\right).
\tag{183.1}
$$

The unresolved mechanism after180 is **essential** retained-coordinate scalar dependence and general nonidentity partition inclusions. The present proof excludes a nontrivial part of the former: finite polynomial retained-coordinate $z$ factors applied to each terminal Gaussian convolution, including finite Hermite derivatives. No claim of a legal general source inverse, or of effective R1 cone preservation under arbitrary partition inclusion, is made.

## 2. Exact Gaussian intertwining

For $\sigma>0$, define $T_\sigma V=\kappa_\sigma*_{y}V$, taking $V$ compactly supported in $(x,y)$ and retaining $x$. Let

$$
H_\sigma=y-\sigma^2\partial_y.
\tag{183.2}
$$

**Lemma 183.1 (distributional normal ordering).** For every compact distribution $V(x,y)$ and every nonnegative integer $q$,

$$
z^q T_\sigma V=T_\sigma H_\sigma^q V,
\qquad
\partial_z^k T_\sigma V=T_\sigma\partial_y^k V.
\tag{183.3}
$$

In particular, with a finite polynomial $p(x,z,\epsilon)=\sum_{q=0}^d p_q(x,\epsilon)z^q$ whose $x$ coefficients are smooth,

$$
p(x,z,\epsilon)\,\partial_z^kT_\sigma V
=
T_\sigma\left[
\sum_{q=0}^d p_q(x,\epsilon)
H_\sigma^q\partial_y^k V\right].
\tag{183.4}
$$

**Proof.** At fixed $\sigma$, the distributional differentiation convention and the Gaussian identity give

$$
\partial_z\kappa_\sigma(z-y)
=-\partial_y\kappa_\sigma(z-y),
\qquad
(z-y)\kappa_\sigma(z-y)
=-\sigma^2\partial_z\kappa_\sigma(z-y).
\tag{183.5}
$$

For a compact distribution paired against the Gaussian, these imply

$$
\partial_z T_\sigma V=T_\sigma\partial_y V,
\qquad
zT_\sigma V=T_\sigma(yV-\sigma^2\partial_y V).
\tag{183.6}
$$

Iterate the second operator identity to obtain the first formula in (183.3). In expanding $H_\sigma^q$, retain the **noncommutative** order: $[\,\partial_y,y\,]=1$. Replacing $H_\sigma^q$ by the naive binomial $\sum_j{q\choose j}y^{q-j}(-\sigma^2\partial_y)^j$ without commutator corrections would be wrong for $q\ge2$. The derivative identity, linearity, and the fact that multiplication by smooth $p_q(x,\epsilon)$ commutes with $y$ and $\partial_y$ give (183.4). Compact support makes all pairings and integrations by parts legitimate. $\square$

**Corollary 183.2 (fixed compact stage and R1 cone).** Each coefficient in (183.4) is compactly supported in the **same** $(x,y)$ support as $V$, and its wavefront set is contained in $\mathrm{WF}(V)$, since $H_\sigma$ and multiplication by smooth functions are finite differential operations. Thus, if $V$ excludes the original forbidden nonzero $(\tau,-\tau)$ conormal to $x=y$, the coefficient on the right of (183.4) excludes it too. The same holds after any finite sum with the **same permitted effective cone**. At the level of evaluated actual families with fixed polynomial degree, this identity introduces only finitely many derivatives and powers $\sigma^2=a^2\epsilon^2$; it requires no regulator-zero inverse Gaussian or unbounded differential order. It is not an independent proof that every possible 108.7 input has the effective cone after a nonidentity partition map.

## 3. Mixed-width obstruction with polynomial output scalars

Define the **polynomial terminal-decorated** evaluated source subclass: a finite collection of actual legal completed 108.7 histories with exact positive-regulator output

$$
S_\epsilon(x,z)=\rho(z)
\sum_{j=1}^{m}\sum_{k=0}^{d_j}
p_{jk}(x,z,\epsilon)\,
\partial_z^k\!\left[
T_{a_j\epsilon}U_{jk,\epsilon}\right](x,z),
\tag{183.7}
$$

where the positive width ratios $a_j$ and polynomial degrees of $p_{jk}$ are fixed, every coefficient is a smooth multiplier in $x$ drawn from an actual legal completed scalar stage, and each $U_{jk,\epsilon}$ is a compact effective upstream distribution at every positive regulator with one fixed compact physical support. The displayed factorization must follow from actual legal histories; (183.7) does not enlarge the source by admitting arbitrary inputs. The outer $\rho$ is the same fixed nonzero-near-zero multiplier as in the first-core problem.

**Theorem 183.3.** Set $\sigma_j=a_j\epsilon$, and put

$$
V_{a,\epsilon}=
\sum_{\substack{j,k\\a_j=a}}
\sum_{q=0}^{\deg_zp_{jk}}
p_{jk,q}(x,\epsilon)
H_{a\epsilon}^{q}\partial_y^k U_{jk,\epsilon}.
\tag{183.8}
$$

Then, as exact distributions at each positive regulator,

$$
S_\epsilon=\rho(z)\sum_{a\in\Lambda}
T_{a\epsilon}V_{a,\epsilon}.
\tag{183.9}
$$

If $S_\epsilon=A_\epsilon$ exactly on a fixed neighborhood of the joint anchor, then every non-target-width aggregate $V_{a,\epsilon}$ vanishes and the target-width aggregate, when present, is

$$
V_{1,\epsilon}=f(x)\delta_0(y).
\tag{183.10}
$$

Consequently exact representation is impossible if there is **no** width one. It is also impossible if every input contributing to the width-one block, **after every actual partition and forgetting operation**, avoids the original forbidden diagonal R1 conormal, so that Corollary183.2 applies to its evaluated effective upstream coefficient.

**Proof.** Lemma183.1 converts each term of (183.7) into one Gaussian convolution with the same width and a compact distributional input. Group equal widths to get (183.9). On an interval where $\rho$ is nonzero, subtract the target $\kappa_\epsilon*f(x)\delta_0(y)$, viewed as a width-one term. Each Gaussian convolution of a compact distribution is entire in $z$, so the local equality becomes a global equality. Apply protected Theorem180.2, whose finite-width independence requires **only compact effective inputs**, not R1 cones. It forces all non-target blocks to vanish and the unit-width block to be (183.10). If width one is absent this contradicts $f\ne0$. For width one, the required $f(x)\delta_0(y)$ has the forbidden nonzero $(\tau,-\tau)$ conormal at $(x,y)=(0,0)$, whereas finite polynomial normal ordering does not introduce such a wavefront direction into an effective R1-compatible block. $\square$

The result extends 180 beyond a pure terminal Hermite family to arbitrary **finite polynomial retained-coordinate $z$ scalar decorations**. It does not treat a genuinely nonpolynomial retained scalar, noncompact upstream support, infinite polynomial degree, arbitrary rapid equivalence or a partition map that creates a target-width diagonal conormal.

## 4. Hostile nonpolynomial control: multiplying Gaussians changes the width

An important obstruction to overgeneralization is the exact identity, for $a,b>0$ and $c=(a^{-2}+b^{-2})^{-1/2}$,

$$
\exp\!\left(-\frac{z^2}{2b^2\epsilon^2}\right)
\kappa_{a\epsilon}(z)
=\frac{c}{a}\kappa_{c\epsilon}(z).
\tag{183.11}
$$

Thus an **essential nonpolynomial** retained-output scalar can turn one Gaussian width into another without an upstream noncompact deconvolution. The scalar in (183.11) is a legitimate smooth function at every positive regulator, but **this identity does not establish that the relevant product is a legal 105/108 history** with the original graph cones, collision corners, density and 126 rows. It merely shows why Theorem180.2 cannot be extended to arbitrary retained-output scalar multipliers by an algebraic argument. Conversely, the width-changing identity does not create the missing $f(x)$ cusp out of legal R1 input.

The operator formula itself may be iterated for a polynomial of fixed degree even when its coefficients depend polynomially or moderately on the regulator. It must not be extended to an infinite Taylor expansion of (183.11) without proving convergence in a **single original complete** 108 source stage, fixed all-corner heat indices, and compatible rapid/126 control. A formal expansion with order tending to infinity is not a finite admitted history.

## 5. Adversarial scope, acceptance targets and successor

| Question | 183 status |
| --- | --- |
| Fixed finite polynomial retained-coordinate $z$ multipliers after a terminal Gaussian edge | **EXACTLY NORMAL-ORDERED** into compact effective inputs |
| R1 cone under the finite polynomial normal-ordering operator | **PRESERVED**, if the effective input cone was already permitted |
| Any finite set of such polynomial terminal histories without width one equals $A$ | **EXCLUDED for exact equality** |
| Target-width polynomial terminal history with permitted effective R1 cone equals $A$ | **EXCLUDED for exact equality** |
| Nonpolynomial retained-output scalars can change Gaussian width analytically | **EXHIBITED**, without source-admission claim |
| Source legality of (183.11), arbitrary nonidentity partition inclusions, full all-corner source geometry | **OPEN** |
| Uniform rapid equivalence, universal 150.L, original first-core source membership, residual W acyclicity, original R3, full126.14, higher weights, actual lifting, M5/R4 | **OPEN** |

The proof is a source-respecting analytical reduction, **not** an assertion that all source histories can be made terminal. A proper critical review must check the sign in (183.6), the noncommutative $H_\sigma^q$ recurrence, original fixed support and wavefront properties, and whether source-completed polynomial coefficients actually satisfy the stipulated smoothness and finite-degree hypotheses.

**Successor 186 after critical184 and bounded ledger185:** determine which genuine nonpolynomial retained-output scalar Gaussian products are legal under the original 105/108 all-corner and R1 contracts, and whether any nonidentity partition jet can generate (183.10) without an illegal input. A positive result must construct an actual exact completed source for $A$ with 126 rows; a negative result must prove an invariant across the full allowed finite histories and uniform rapid quotient. Neither an algebraic Gaussian identity nor a new conditional subclass exclusion certifies 150.L or $W$ acyclicity.
