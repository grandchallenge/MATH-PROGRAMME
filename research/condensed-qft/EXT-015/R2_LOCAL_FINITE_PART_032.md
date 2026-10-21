# EXT-015 REACH-R2 / 032 — explicit singular extension, local ambiguity and exact renormalization-scale law

**Disposition: NEW BOUNDED MATHEMATICAL CANDIDATE; critical review required.** This completes the **GB1 benchmark** in the programme at the level of a singular distribution on the line. It is **not** a counterterm BV operator, a multi-diagonal forest formula or interacting QFT.

**Sources and scope:** The zero-scale obstruction is the admitted D14 [result 028](D14_REGULATED_BV_SYZYGY_028.md), Theorem 28.7; the extension-by-scaling-degree framework is described by [Brunetti–Fredenhagen](https://arxiv.org/abs/math-ph/9903028). The direct derivation here uses elementary distribution theory and does not appeal to a generalized extension theorem without checking hypotheses. Exact parent: [REACH-R2 issue #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797). Research source head at start: 37384b473239aee26fb6cbefde1b020f06b375fc.

## 1. Constructive extension of a nonintegrable diagonal singularity

Let $t^\circ$ on the punctured line be multiplication by $1/|z|$. Choose an even cutoff $\chi\in C_c^\infty(\mathbb R)$ with $\chi(z)=1$ near $0$. For every $\varphi\in C_c^\infty(\mathbb R)$ set

$$
\langle t_\chi,\varphi\rangle
=
\int_{\mathbb R}
\frac{\varphi(z)-\varphi(0)\chi(z)}{|z|}\,dz.
\tag{32.1}
$$

**Theorem 32.1 (well-defined extension and complete local freedom at fixed scaling degree).** Formula (32.1) defines a continuous distribution extending $t^\circ$. Its scaling degree at zero is exactly one. Every extension of $t^\circ$ whose scaling degree is at most one differs from $t_\chi$ by $c\delta_0$ for a uniquely specified real constant $c$.

**Proof.** Near zero, $\chi=1$ and $\varphi(z)-\varphi(0)=z\int_0^1\varphi'(sz)\,ds$. Its quotient by $|z|$ is locally bounded and integrable; outside a compact support it vanishes. For any compact $K$, choose a larger compact containing both $K$ and the support of $\chi$. The functional is controlled by a constant times $\sup|\varphi|+\sup|\varphi'|$ on that larger compact; hence it is a continuous distribution. For $\varphi$ supported away from zero its value agrees with the defining $1/|z|$ integral.

Under $\varphi_\lambda(z)=\lambda^{-1}\varphi(z/\lambda)$, substitution $z=\lambda u$ gives

$$
\langle t_\chi,\varphi_\lambda\rangle
=
\lambda^{-1}
\left(
\langle t_\chi,\varphi\rangle
+2\log\lambda\,\varphi(0)
\right)
\quad(\lambda>0),
\tag{32.2}
$$

because the integral of $\bigl(\chi(u)-\chi(\lambda u)\bigr)/|u|$ is $2\log\lambda$, as follows by differentiation in $\log\lambda$ and equality at $\lambda=1$. For every $\omega>1$ the product $\lambda^\omega\langle t_\chi,\varphi_\lambda\rangle$ tends to zero as $\lambda\downarrow0$, so the scaling degree is at most one. It is at least one because the restriction away from zero is exactly the homogeneous degree-minus-one distribution; equivalently choose $\varphi$ supported in a positive annulus, then the scale-transformed pairing equals a nonzero constant times $\lambda^{-1}$ when $\lambda$ is sufficiently small. Thus its scaling degree equals one.

Two extensions have difference supported at zero, hence by the point-support structure theorem their difference is a finite sum $\sum_{k=0}^N c_k\delta_0^{(k)}$. Since $\delta_0^{(k)}$ has scaling degree $k+1$, preserving the bound one forbids all $k>0$. Conversely adding $c\delta_0$ retains scaling degree one. $\square$

The scaling formula is intentionally written for every positive $\lambda$ with the **same fixed cutoff**, and includes the logarithmic scaling anomaly. There is no globally homogeneous extension respecting both the restriction $1/|z|$ and exact scaling at degree minus one.

## 2. Exact renormalization-group law from cutoff dilation

For each $R>0$ put $\chi_R(z)=\chi(z/R)$, and form $t_R=t_{\chi_R}$ by (32.1).

**Theorem 32.2 (exact finite scale change).** For arbitrary $R,S>0$,

$$
t_R-t_S=-2\log(R/S)\,\delta_0.
\tag{32.3}
$$

Equivalently the logarithmic derivative is

$$
\frac{d}{d\log R}t_R=-2\delta_0.
\tag{32.4}
$$

The coefficient is independent of the detailed shape of the normalized cutoff $\chi$.

**Proof.** Their action difference on $\varphi$ equals

$$
\langle t_R-t_S,\varphi\rangle
=
\varphi(0)\int_{\mathbb R}
\frac{\chi(z/S)-\chi(z/R)}{|z|}\,dz.
$$

The integral is finite because the two cutoffs agree near zero. Differentiate in $\log R$ under the integral; the derivative of $-\chi(z/R)$ is $(z/R)\chi'(z/R)$. Substitution $u=z/R$ gives

$$
\int_{\mathbb R}
\frac{u\chi'(u)}{|u|}\,du
=
\int_{\mathbb R}\mathrm{sgn}(u)\chi'(u)\,du=-2\chi(0)=-2.
$$

At $R=S$ the difference is zero, so integrate the derivative to obtain (32.3). This also proves (32.4). $\square$

The local term is an **exact cocycle**:

$$
c(R,T)=c(R,S)+c(S,T),
\qquad
c(R,S)=-2\log(R/S).
\tag{32.5}
$$

This is a small but genuine renormalization result: changing the subtraction scale changes the distribution only by a local delta counterterm, with a coefficient forced by the singularity.

## 3. Controlled bridge to D14, and what it does not imply

D14's divergent atomic mixed contraction is

$$
\Delta_\epsilon
(\delta_a^{\mathrm{even}}\delta_a^{\mathrm{odd}})
=\frac{\kappa(0)}{\epsilon}.
\tag{32.6}
$$

One may subtract $C_\epsilon=\kappa(0)/\epsilon$ on **that fixed generator pair**, giving a finite remainder (for example zero). This is **not** a definition of a renormalized BV operator on arbitrary distributional kernels. A genuine operator must simultaneously decide diagonal derivatives, overlapping subdiagonals, multilinear compatibility, cochain identities and regulator transport. The $1/|z|$ extension above is a mathematically explicit singularity benchmark, but it is **not falsely identified** with the actual $\delta_a\otimes\delta_a$ BV divergence.

**Next GB2 research:** form a finite atomic-jet kernel domain; calculate the complete Laurent/Taylor asymptotic of every pair contraction, including derivatives of deltas. Define subtraction maps and test their commutators with $d$, square-zero, Wick conjugation, disjoint-open factorization, and exact renormalized scale cocycle. Use multi-point/overlapping diagonal extensions before claiming general locality. If the identities fail, retain the exact obstruction as an anomaly; do not certify by numerical agreement.

## 4. Exact hostile algebra controls

A compact, even *finite-differentiability control* is

$$
\chi_4(z)=(1-z^2)^4\mathbf 1_{\{|z|<1\}},
\quad
\chi_5(z)=(1-z^2)^5\mathbf 1_{\{|z|<1\}}.
$$

These are not smooth at the endpoints to all orders, so they are **finite algebraic controls**, not legal replacements for the theorem's smooth cutoffs. Their cutoff-difference coefficient is exactly

$$
\int_\mathbb R
\frac{\chi_5(z)-\chi_4(z)}{|z|}\,dz
=-2\int_0^1 z(1-z^2)^4\,dz
=-\frac15.
\tag{32.7}
$$

The exact rational fixture [032](fixtures/check_local_finite_part_032.py) checks this cancellation and verifies a second binomial expansion. It does not establish scaling degree; that is the analytic proof above.

## 5. Acceptance boundary

- **New candidate mathematical theorem:** a well-defined extension of $1/|z|$, sharp scaling-degree-one classification, and exact logarithmic scale-change law.
- **Already known:** D14's unrestricted ultraviolet divergent atomic contraction.
- **Not established:** a domain-wide BV counterterm operator, coherent nested-diagonal subtraction, a renormalized zero-scale factorization theory, interacting QFT or a connection to higher liquid Ext.
- **Critical review required:** exact-hostile mathematical audit and source comparison before marking GB1 accepted or protected-mathematically-certified. No theorem from this note automatically closes REACH-R2 or EXT-015D.
