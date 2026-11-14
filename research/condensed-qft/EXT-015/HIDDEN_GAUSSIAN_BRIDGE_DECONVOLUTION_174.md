# EXT-015 REACH / 174 — exact Gaussian-deconvolution obstruction for hidden bridge histories

**Primary verdict: BOUNDED NEGATIVE CONSTRUCTION TEST.** The remaining first Green core cannot have an exact representative within the entire finite one-Gaussian hidden-bridge subclass specified below, including arbitrary legal completed R1 coefficients, properly forgotten spectators and fixed finite physical derivatives. A stronger regular-stage condition excludes rapid-equivalent representatives. Neither statement is a complete classification of 108.7 histories or a resolution of universal 150.L or residual W acyclicity.

## 1. Pinned premises and target

Retain the exact protected mathematical sources 105 (blob a8ce66ff0edec33e2aff299550fca2089d671033), 108 (587c15fd6e24f6e6b14de574ff878221cdbd5cb6), 126 (5b05c6147d237ca1d22e4dcbce9262b0f038c163), 150 (03deca9212a9bea56743e482e5cb79edb46b9d7f), 165 (24b82716d41d309438fcb7a97bbacab0b724afde), 168 (e2c43f218c9175b919c51f371acb8c04e659faea), no-hidden primary171 (4d4818e6927eb951a3810c621f94832de1371e33), critic172 (573858897e18bb1230e8445f8eb9d1bfa73ab5a2), and ledger173 (e93ad78ad299de25f59136c5979909e5c69142f5). PR3326 protected 171 at merge 68437bc28cddbea57c06632db4035a83a7da5b42; PR3331 protected 172–173 at merge 2f4d068b1767fe6d1cb4d9fa6207b806458c2dc5. The reviewer was the same ChatGPT/GitHub account, not independent external mathematical certification. Documentary checkpoint CP189 remains to be advanced.

Use the existing one-dimensional compact data, with $\rho(0)\ne0$ and $\chi=1$ near the anchor. The first core, whose source status governs both original Green output membership problems by 165/168, is

$$
A_\epsilon(x,z)=\chi(x)e(x)\rho(z)\kappa_\epsilon(z),
\qquad
e(x)=|x|/2,
\qquad
\kappa_\epsilon(t)=\frac{e^{-t^2/(2\epsilon^2)}}{\sqrt{2\pi}\epsilon}.
\tag{174.1}
$$

Choose an open interval $J$ about zero where the fixed smooth $\rho$ is nowhere zero.

## 2. A nontrivial existing hidden-source subclass

Define $\mathcal B_{\rm bridge}$ as the finite additive image of legal original 108.7 histories of the following form. Retain output vertices $x,z$; introduce a marked forgotten vertex $y$ and possibly any fixed finite collection of properly forgotten spectators $r$. Use the **identity partition** on these augmented coordinates and a fixed compact R1 coefficient $T(x,y,r)$ independent of $z$. Give it a genuine admitted scalar heat coefficient

$$
a_\epsilon(x,z,y,r)
=\rho(z)\kappa_\epsilon(z-y)b_\epsilon(x,y,r).
\tag{174.2}
$$

Here $b_\epsilon$ may depend on all non- $z$ physical coordinates and the regulator, but must itself satisfy the existing fixed completed scalar-stage indices, auxiliary weights and all-corner estimates of 105/108/126. No arbitrary positive-scale scalar is admitted by stipulation. The Gaussian is the **already legal relative heat edge**. Compact cutoffs and original pushforward densities are retained, so the forgotten projection is proper. Include fixed finite physical derivatives of the *inner convolution before the outer $\rho(z)$ multiplication*, via the original differentiated source maps and the complete finite Leibniz rule. Completed coefficient tensors and finite sums are allowed. The input R1 cone, noncharacteristic multiplication and all parameter rows must pass the original 108 conditions. This is a genuine nonempty source subclass, not a new class of operators.

The restrictions matter: no unseparated $z$ dependence in $b_\epsilon$ or $T$, no other heat bridge, no different Gaussian width and no nonidentity partition inclusion. Arbitrary existing histories not satisfying these restrictions are **not** excluded by the theorem.

**Lemma 174.1 (the effective coefficient retains the R1 conormal exclusion).** For every positive regulator, every output $S$ in this subclass is exactly

$$
S_\epsilon(x,z)
=\rho(z)\int\kappa_\epsilon(z-y)U_\epsilon(x,y)\,dy,
\tag{174.3}
$$

with a compact distribution $U_\epsilon$ whose wavefront excludes all nonzero diagonal conormals $(\tau,-\tau)$ at $x=y$. This applies to finite sums, fixed derivatives and projective coefficient completion.

**Proof.** Multiply $T$ by the positive-scale smooth scalar $b_\epsilon$ and properly forget the spectator variables. The wavefront pushforward relation says that a projected covector $(\tau,-\tau)$ could only come from an augmented covector $(\tau,-\tau,0_r)$, which is forbidden by the **original** R1 partial equality partition $x=y$ with each spectator in a separate block. Derivatives preserve wavefront containment. Differentiating the convolution in $z$ is equivalent, by $\partial_z\kappa_\epsilon(z-y)=-\partial_y\kappa_\epsilon(z-y)$ and distributional integration by parts, to differentiating $U_\epsilon$ in $y$; $x$ derivatives act directly on $U_\epsilon$. The finite jointly continuous source maps from 108.6 justify the same identities for completed projective coefficient tensors. The finite sum of the resulting permitted distributions again excludes the forbidden diagonal conormal. Proper projection retains the physical density. $\square$

No regulator-zero extension of $U_\epsilon$ is assumed.

## 3. Exact Gaussian injectivity forces a forbidden source

**Lemma 174.2 (distribution-valued Gaussian injection).** For fixed $\epsilon>0$, if compactly supported distributions $U,V$ on $(x,y)$ have Gaussian convolutions agreeing for $z$ in any nonempty real interval, then $U=V$.

**Proof.** Pair with an arbitrary compact smooth $x$ test. Convolution in $y$ against $\kappa_\epsilon(z-y)$ produces an **entire function** in complex $z$ for any compactly supported finite-order distribution in $y$. Equality on the real interval therefore extends to all $z$. Fourier transformation in $z$ gives

$$
e^{-\epsilon^2\xi^2/2}(\widehat U-\widehat V)=0.
\tag{174.4}
$$

The Gaussian multiplier is nowhere zero. Its reciprocal need not act on the entire tempered space: local division on every compact frequency interval suffices to show that the Fourier-transform distribution vanishes. Varying the $x$ test proves $U=V$. $\square$

**Theorem 174.3 (exact single-bridge exclusion).** No finite member of $\mathcal B_{\rm bridge}$ evaluates identically to $A_\epsilon$ for all positive $\epsilon$.

**Proof.** Suppose one does. Cancel the nonzero fixed $\rho(z)$ on $J$. By Lemma 174.1,

$$
\kappa_\epsilon*U_\epsilon
=\chi(x)e(x)\kappa_\epsilon(z)
=\kappa_\epsilon*\bigl[\chi(x)e(x)\delta_0(y)\bigr]
\quad (z\in J).
\tag{174.5}
$$

By Lemma 174.2, for **every fixed** $\epsilon>0$ this forces

$$
U_\epsilon(x,y)=\chi(x)e(x)\delta_0(y).
\tag{174.6}
$$

At $(x,y)=(0,0)$ the transverse tensor-product wavefront of $e(x)=|x|/2$ with $\delta_0(y)$ contains $(\tau,-\tau)$ for each $\tau\ne0$. This is a forbidden R1 conormal to $x=y$, contradicting Lemma 174.1. The contradiction holds for *arbitrary completed legal coefficients* in the bridge class: exact evaluation plus injectivity forces the illegal coefficient independently of presentation. $\square$

This upgrades the previous rejection of a *particular* naive product to exclusion of every possible single-bridge R1 coefficient, finite source derivative, proper spectator integration and completed cancellation in this restricted but substantial subclass.

## 4. Rapid equivalence under a genuine graph-regularity hypothesis

Let $\mathcal B_{\rm bridge}^{\rm reg}$ denote those bridge outputs whose effective $U_\epsilon$ extends continuously through $\epsilon=0$ **in one fixed complete permitted graph space** $E_{s,K,\Gamma}$, with the off-cone Sobolev seminorms of 108.1. This condition is stronger than merely being an allowed scalar heat source or pointwise R1 for positive regulator; it is not attributed to every original 108 history.

**Proposition 174.4.** No such graph-regular bridge is equal to $A$ modulo the original uniform finite-order rapid ideal.

**Proof.** The graph limit $U_0$ retains the permitted R1 wavefront exclusion. Convolution by the Gaussian approximate identity and convergence in the fixed graph stage imply

$$
\rho(z)(\kappa_\epsilon*U_\epsilon)(x,z)
\longrightarrow \rho(z)U_0(x,z)
\quad\text{in distributions}.
\tag{174.7}
$$

But $A_\epsilon$ has weak limit $\chi(x)e(x)\rho(0)\delta_0(z)$. A uniformly rapid difference has weak limit zero. On the open $J$ divide by $\rho$ to force $U_0=\chi(x)e(x)\delta_0(z)$, forbidden by the same R1 conormal. $\square$

**Adversarial control.** R1 membership for every $\epsilon>0$ does not imply a fixed R1 graph limit. For example smoothing the $x$ cusp on an exponentially flat scale $\exp(-1/\epsilon^2)$ produces pointwise smooth coefficients multiplying $\delta_0(y)$ and an ambient Gaussian bridge rapidly close in distribution seminorms, while the off-cone graph seminorms can diverge super-polynomially. No claim is made that this ambient family belongs to an accepted fixed scalar or completed R1 source. Thus **exact nonrepresentation does not prove a general rapid-quotient nonrepresentation** in the full bridge class. The regularity hypothesis in Proposition 174.4 is essential.

**Sharp positive comparison.** For a smooth compact $f(x)$, the legal pure- $y$ R1 input $f(x)\delta_0(y)$ with the same Gaussian bridge produces exactly $f(x)\rho(z)\kappa_\epsilon(z)$. The negative theorem detects coexistence of the independently singular cusp and absolute Gaussian anchor, not Gaussian concentration alone.

## 5. Bounded acceptance matrix and next step

| Question | 174 result |
| --- | --- |
| All finite no-hidden 108.7 sources (protected 171) | EXCLUDED for exact and rapid $A$ |
| All finite completed one-Gaussian hidden bridge sources specified in 174.2 | **EXCLUDED for exact $A$** |
| Bridge sources with a common fixed R1 graph limit | **EXCLUDED also modulo rapid** |
| General rapid quotient for the unrestricted one-bridge subclass | OPEN |
| Hidden sources with other scalar dependences, multiple edges or nonidentity partition inclusions | OPEN |
| Full source admission or exhaustive obstruction for $A$ | OPEN |
| Universal Lemma 150.L, residual W acyclicity, original R3, 126.14, higher weights, lifting and M5/R4 | OPEN |

**Next substantive 177, after mathematical critic 175 and ledger 176:** analyze remaining legal hidden histories with nonfactorable retained-coordinate scalar coefficients, multiple heat edges, partition inclusions and completed cancellations. Any exact positive source or full negative invariant must preserve all corner indices, proper densities, permitted R1 cones, projective completion, uniform rapid relation and genuine 126 parameter rows. Do not infer a cohomological or REACH closure from this bounded test.

This primary requires exact-head mathematical criticism, protected review/CI/merge and main readback. Neither source success nor protected admission is independent mathematical certification.
