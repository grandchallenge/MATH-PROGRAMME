# EXT-015 REACH / 181 — critical verification of finite mixed Gaussian-width independence

**Mathematical disposition: BOUNDED ACCEPT, conditioned on protected custody of exact primary180.** Verifier V181 and Adversary A181 are logically separate source-locked assessments by the **same** ChatGPT/GitHub producer account, not an independent nonauthor APPROVED review, external referee or MATHCERT certification. Universal Lemma150.L, residual W acyclicity, original R3 and full 108.7 first-core source status remain OPEN.

## 1. Exact source identity

The primary is [MIXED_TERMINAL_GAUSSIAN_INDEPENDENCE_180.md](MIXED_TERMINAL_GAUSSIAN_INDEPENDENCE_180.md), Git blob fac58764ac29e518ac522e0451a9c9829e86720b, corrected exact PR3344 head 1abb1a1b16d113732bf05daeb796b153d901c39a. The only revision from the earlier source head 68f4c0e027399637e1d69c27077d7b37d3a1f421 was renderer-safe mathematical support notation. The current exact-head mathematical COMMENT review ID is 5908082860, by the same producer account, not nonauthor APPROVED. **The source's protected merge/readback is a distinct admission requirement.**

Protected premises: 105 blob a8ce66ff0edec33e2aff299550fca2089d671033; 108 blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6; 126 blob 5b05c6147d237ca1d22e4dcbce9262b0f038c163; first-core 171 blob 4d4818e6927eb951a3810c621f94832de1371e33; single-bridge 174 blob 7c470ba092d917dc434a8883e5afaff7bce1dfc6; terminal 177 blob 8f9f214cfced47d7a52790fab42544b6035e56ad; critical178 blob 5518f9e35932b5fd957a73a66cf150f2fb023974; ledger179 blob 4ede931aadd36e552badefe482f760e9114e8a3d. CP192 protected at PR3342 merge 1388c32ee8db914f399a3b4190a446f093d8432a.

## 2. V181 — independent proof of the nontrivial support lemma

The 180.1 claim is stronger than the ordinary **upper** Paley–Wiener estimate and must not be accepted by mere reference to positivity of the Laplace transform: effective R1 coefficients may be signed or complex distributions. The relevant classical external inputs are the converse Paley–Wiener–Schwartz compact-support theorem and the quadrant Phragmén–Lindelöf principle; see Boman–Hörmander (1999), Introduction (1.1)–(1.3), and standard one-dimensional complex analysis.

Here is a self-contained reduction of the one-sided support conclusion to those named theorems. Let $u$ be a nonzero compact distribution and $b=\sup\mathrm{supp}\,u$. Its Fourier–Laplace transform $F(\zeta)$ is entire of exponential type and has a polynomial bound on real $\zeta$. Suppose that for some $a<b$ its positive imaginary-axis values satisfy $|F(it)|\le C e^{at}$ for all $t\ge0$. Choose a polynomial degree $N$ above its real-axis Fourier growth and define

$$
G(\zeta)=\frac{e^{ia\zeta}F(\zeta)}{(\zeta+i)^N}.
\tag{181.1}
$$

The denominator has no zero in the upper half-plane. The function $G$ is bounded on the **entire real axis** by the polynomial Fourier bound, and on the **positive imaginary axis** because $|e^{ia(it)}F(it)|=e^{-at}|F(it)|\le C$. It is holomorphic in the upper half-plane and has growth of order at most one there. Phragmén–Lindelöf on the first and second quadrants (opening $\pi/2$, permitted growth order strictly below two) bounds $G$ throughout the upper half-plane. Therefore

$$
|F(\zeta)|\le C'(1+|\zeta|)^N e^{a\,\mathrm{Im}\zeta},
\qquad \mathrm{Im}\zeta\ge0.
\tag{181.2}
$$

The original compact support supplies the standard lower-half-plane Fourier–Laplace estimate using any fixed finite lower endpoint $-R$. Combine the two to obtain a full-plane Paley–Wiener–Schwartz estimate for the **strictly smaller** interval $[-R,a]$. Its converse forces $\mathrm{supp}\,u\subset[-R,a]$, contradicting $b>a$. Thus no such upper exponential rate $a<b$ exists, establishing the one-sided support indicator

$$
\limsup_{t\to\infty}\frac1t\log|\langle u,e^{ty}\rangle|
=\sup\mathrm{supp}\,u.
\tag{181.3}
$$

In particular, any bound by a polynomial times $\exp(-\delta t^2+Rt)$ for fixed $\delta>0$ implies bounds by $e^{at}$ for **every real** $a$, which forces $u=0$. This justifies the critical nonpositive-distribution step that 180 explicitly identifies as external, without confusing a direct upper growth estimate with a converse support theorem.

For the finite Gaussian-width identity, pair with arbitrary compact $x$ tests. Gaussian convolutions of compact hidden distributions extend as entire functions of the output variable. From equality on an interval, Fourier continuation at $\xi=it$ yields a sum of terms $e^{a_j^2\epsilon^2t^2/2}L_j(t)=0$. Isolate the largest width, divide by its exponential, and use the compact upper bounds for all lower widths. The largest-width Laplace coefficient must obey a super-Gaussian **upper** bound and hence vanish by (181.3). Repeat descending over finitely many widths. The argument is performed for each fixed positive $\epsilon$ and each $x$ test; it does not posit any regulator-uniform indicator bound or arbitrary source inverse.

**V181 PASS: finite distinct Gaussian-width convolution operators are linearly independent on compact distributions for the exact-identity problem.**

## 3. A181 — source correctness and hostile controls

For original legal terminal source histories, transfer finite Hermite derivatives to the compact effective input and group contributions at each width. The independence theorem then forces all non-target-width groups to vanish and the target-width coefficient to equal $f(x)\delta_0(y)$. If width one is absent this is impossible regardless of R1 cone. If the unit-width aggregate avoids the original R1 $x=y$ diagonal conormal, its forced cusp-times-delta coefficient contradicts the cone.

The scope is essential. Noncompact upstream Gaussian coefficients allow heat-semigroup convolution identities between different widths; the independence theorem **fails** there. The original source requires fixed compact physical support at every 108 stage, so such a noncompact control is not an admitted counterexample. An infinite series of widths is also outside the fixed finite-history 108 definition. Finite completed coefficient tensors remain allowed only through their actual evaluated compact stage, not an uncontrolled ambient-limit source.

Nonidentity partition inclusions may introduce an effective diagonal conormal, and scalar factors depending genuinely on retained output $z$ can invalidate the terminal factorization. The theorem does not exclude those cases. Equality modulo the all-derivative uniform rapid ideal is weaker than exact equality, so neither the Fourier entire continuation nor the width independence solves that quotient problem without new source-controlled estimates.

**A181 PASS the bounded terminal-factorizable exact theorem. REJECT universal 150.L, full $A$ nonmembership, residual W cohomology, R3, full 126.14, higher weights, lifting or M5/R4 promotion.**

## 4. Decision and next research

| Claim | Critical decision |
| --- | --- |
| One-sided support indicator for signed/complex compact distributions | ACCEPT, using quadrant Phragmén–Lindelöf and Paley–Wiener converse |
| Linear independence of finite distinct Gaussian convolution widths over compact distributions | ACCEPT |
| Any finite terminal-factorizable source lacking width one represents $A$ exactly | EXCLUDED |
| Unit-width effective R1-compatible source together with arbitrary other finite widths represents $A$ exactly | EXCLUDED |
| Target-width coefficient with possible partition-generated diagonal conormal | OPEN |
| Essential nonterminal retained-coordinate scalar factors, arbitrary rapid equivalence | OPEN |
| Full original 108.7 first-core membership, universal 150.L, residual W acyclicity and R3 | OPEN |

**Canonical critical scope: FINITE_COMPACT_MIXED_GAUSSIAN_WIDTHS_INDEPENDENT__TARGET_R1_REQUIRED__GENERAL_NONTERMINAL_OPEN.** Bounded ledger182 must preserve the exact theorem and cite the external analytic dependency. The next substantive target 183 is genuinely nonterminal scalar/partition coupling, not another width-only ansatz.