# EXT-015 REACH / 180 — independence of finite Gaussian terminal widths over compact source distributions

**Primary mathematical disposition: CONSTRUCTIVE BOUNDED NEGATIVE THEOREM.** In the actual finite terminal Gaussian/Hermite subclass defined by protected 177, a source with arbitrarily mixed positive terminal widths has an exact representation of the first Green core $A$ **only if** its total effective contribution at the target width equals the forbidden cusp-times-anchored-delta distribution, and all contributions at other widths vanish as distributions. In particular, no finite mixed-width source without a target-width term can represent $A$ exactly; if the effective target-width coefficients retain the original permitted R1 diagonal-conormal exclusion, no such finite mixed-width source can represent $A$ either. This settles the mixed-width cancellation problem **inside the terminal factorization** but does not decide nonterminal retained-output scalars, arbitrary partition inclusions, the full 108.7 source, universal 150.L, or residual $W$ acyclicity.

## 1. Immutable source and external analytic input

Retain protected 105 scalar Gaussian/Wick (Git blob a8ce66ff0edec33e2aff299550fca2089d671033), 108 complete mixed coefficients (587c15fd6e24f6e6b14de574ff878221cdbd5cb6), 126 source-controlled parameter rows (5b05c6147d237ca1d22e4dcbce9262b0f038c163), 165 Green two-arm reduction (24b82716d41d309438fcb7a97bbacab0b724afde), exact B arm168 (e2c43f218c9175b919c51f371acb8c04e659faea), no-hidden 171 (4d4818e6927eb951a3810c621f94832de1371e33), hidden single-bridge 174 (7c470ba092d917dc434a8883e5afaff7bce1dfc6), and protected terminal-width primary177 (8f9f214cfced47d7a52790fab42544b6035e56ad), critic178 (5518f9e35932b5fd957a73a66cf150f2fb023974), ledger179 (4ede931aadd36e552badefe482f760e9114e8a3d). Primary177 was protected in PR3339 at merge 6ec0694fd8606e8f9b446101a43ac1e51f8e9922 and 178–179 in PR3341 at merge c896f1497405fd10db21cc95becb1062bee9d413. Source blobs were re-read on protected main. Reviewer roles are logically separate but use the same system/account, not independent mathematical certification.

The one genuinely **external analytic input** required below is the classical one-dimensional *Paley–Wiener support-indicator theorem* for compact distributions. One reference for the precise supporting-function/indicator relationship is J. Boman and L. Hörmander, "A Paley–Wiener theorem for the analytic wave front set," *Asian Journal of Mathematics* 3 (1999), 757–770, introduction (1.1)–(1.3), [full text](https://www.intlpress.com/site/pub/files/_fulltext/journals/ajm/1999/0003/0004/AJM-1999-0003-0004-a003.pdf). Its application is an ordinary one-dimensional distribution theorem, not a claim about the GCL 108 source completion. The specific one-sided consequence is stated and used explicitly as Lemma 180.1.

Fix compact smooth $\chi,\rho$ as in 165, with $\chi=1$ near zero and $\rho(0)\ne0$. Write

$$
f(x)=\chi(x)|x|/2,\quad
A_\epsilon(x,z)=f(x)\rho(z)\kappa_\epsilon(z),\quad
\kappa_{\sigma}(t)=
(\sqrt{2\pi}\sigma)^{-1}\exp(-t^2/(2\sigma^2)).
\tag{180.1}
$$

## 2. A one-sided Paley–Wiener fact stronger than an upper bound

**Lemma 180.1 (support detected by the Laplace growth indicator).** If $u\in\mathcal E'(\mathbb R)$ is nonzero with compact support and $L_u(t)=\langle u(y),e^{ty}\rangle$, then

$$
\limsup_{t\to+\infty}\frac{\log|L_u(t)|}{t}
=\sup\mathrm{supp}u\in\mathbb R.
\tag{180.2}
$$

In particular, for every $\delta>0$ and real $R,N$, no nonzero compact distribution can satisfy

$$
|L_u(t)|\le C(1+t)^N
\exp(-\delta t^2+Rt)
\quad\text{for all sufficiently large }t>0.
\tag{180.3}
$$

**Reason.** Equation (180.2) is the one-dimensional one-sided support-function indicator assertion of the classical Paley–Wiener theory. The upper bound is immediate from compact support and finite distribution order. The converse is the nontrivial support-indicator statement: the *least exponential rate along the positive real Laplace direction* is fixed by the rightmost point of distributional support, even for signed or complex finite-order compact distributions. It cannot be replaced merely by the easy upper estimate used in 177. Lemma (180.3) follows because its logarithm divided by $t$ tends to negative infinity, contradicting the finite support endpoint. We explicitly cite the indicator theorem instead of incorrectly treating a one-sided lower bound for a sign-changing distribution as an elementary positivity argument. $\square$

The lemma applies to each actual positive regulator separately. It makes **no** uniform claim about source-stage seminorms as the regulator tends to zero.

## 3. Independence of distinct Gaussian widths

**Theorem 180.2 (finite Gaussian-width linear independence over compact distributions).** Fix $\epsilon>0$ and pairwise distinct positive numbers $a_1,\ldots,a_m$. If distributions $V_j\in\mathcal E'(\mathbb R)$ obey

$$
\sum_{j=1}^m\kappa_{a_j\epsilon}*V_j=0
\quad\text{as distributions on a nonempty open interval},
\tag{180.4}
$$

then every $V_j=0$. The same conclusion holds for compact distributions $V_j(x,y)$ with an arbitrary additional retained variable $x$, and for a finite sum of fixed derivatives of the Gaussian factors after those derivatives are transferred onto $V_j$.

**Proof.** Pair with an arbitrary compact smooth $x$ test when needed. Each Gaussian convolution of a compact distribution is entire in the output variable $z$. Thus equality on a nonempty interval extends to all real $z$, and its Fourier transform is an identity of entire Fourier–Laplace functions. Let $L_j(t)$ denote the paired Laplace transform of $V_j$ at imaginary frequency $\xi=it$. Then

$$
\sum_j\exp(a_j^2\epsilon^2t^2/2)L_j(t)=0
\quad(t\in\mathbb R).
\tag{180.5}
$$

Let $a_*$ be the largest width in the finite list. Divide by its Gaussian exponential and isolate its Laplace coefficient:

$$
L_*(t)=-\sum_{a_j<a_*}
 \exp(-(a_*^2-a_j^2)\epsilon^2t^2/2)L_j(t).
\tag{180.6}
$$

Every other compact coefficient satisfies an ordinary upper Fourier–Laplace bound $|L_j(t)|\le C_j(1+t)^{N_j}e^{R_jt}$ for $t>0$, as in 177.1. Since the width gaps are fixed and positive, (180.6) implies for sufficiently large $t$

$$
|L_*(t)|\le C(1+t)^N\exp(-\delta t^2+Rt)
\quad\text{for some }\delta>0.
\tag{180.7}
$$

By Lemma180.1 the compact distribution producing $L_*$ must be zero. For a distribution-valued $x$ coefficient the argument applies to **every** compact $x$ test; hence $V_*=0$ as a distribution. Remove this width and repeat the same descending finite induction. For $m=1$, Gaussian injectivity gives the conclusion directly. This establishes all $V_j=0$, including cancellations among arbitrary finite-order compact coefficients. $\square$

The theorem is a **linear independence theorem for Gaussian convolution operators acting on compact distributions**, not a claim that each Gaussian source factor is individually in an admissible 108 stage. Those source admissibility checks remain separate.

## 4. Original mixed-source corollary; what remains open

**Corollary 180.3 (complete terminal-width decomposition).** Let a genuine legal finite source in the terminal-Gaussian subclass of 177.2 be represented by any finite number of positive width ratios, including ratios above and below one, and any fixed finite Hermite decorations. At each positive regulator, transfer the Hermite derivatives to the compact hidden distributions and group all terms with the same width $a$. The actual output is

$$
S_\epsilon=\rho(z)\sum_{a\in\Lambda}
\bigl(\kappa_{a\epsilon}*_{y}V_{a,\epsilon}\bigr),
\qquad
V_{a,\epsilon}=
\sum_{\substack{j,k\\a_j=a}}
c_{jk}(\epsilon)\epsilon^k
\partial_y^kU_{j,\epsilon}.
\tag{180.8}
$$

If $S_\epsilon=A_\epsilon$ exactly for every positive regulator, then

$$
V_{a,\epsilon}=0\quad(a\ne1),\qquad
V_{1,\epsilon}=f(x)\delta_0(y).
\tag{180.9}
$$

The second equation presupposes that width one occurs in the list. If there is **no** width-one term, exact equality is impossible even without any effective R1 cone hypothesis. If width one occurs and the effective $V_{1,\epsilon}$ avoids the prohibited diagonal conormal $(\tau,-\tau)$ to $x=y$, equality is likewise impossible. In particular, arbitrary mixed-width cancellation cannot rescue a finite completed source when its *target-width effective block* obeys the permitted R1 condition.

**Proof.** Divide by the fixed nonzero $\rho$ on an interval $J$ about zero. Subtract the target $\kappa_\epsilon*f\delta_0$, treating width one as an additional group if absent. Apply Theorem180.2 at each fixed positive regulator to the finite list of distinct widths. This forces (180.9). If the width-one group is absent, it would force nonzero $f\delta_0=0$, contradiction. If the width-one group has a permitted R1 cone, its wavefront cannot contain $(\tau,-\tau)$ at the origin; the forced coefficient $f(x)\delta_0(y)$ does contain that conormal, another contradiction. No assumption about the effective cones of the *other* width groups is needed. $\square$

The source class still excludes essential additional retained- $z$ scalar factors, nonterminal output-variable dependence, and nonidentity partition inclusions whose effective width-one coefficient may have a diagonal conormal. It does not claim the full original $\mathcal P_2$ is equal to its terminal-factorizable subcollection. **No modulo-rapid conclusion** follows from analytic continuation of an exact identity, and no source inverse of the Green second derivative has been supplied.

## 5. Claims, adversarial checks and successor

Theorem180.2 would fail without **compact** effective upstream support: the Gaussian heat semigroup gives a nontrivial cancellation identity with noncompact upstream Gaussian coefficients. This is a hostile control, not an admissible fixed compact R1 source. Theorem180.2 also fails as stated for infinitely many widths with uncontrolled limits; original 108.7 sources use finite histories and fixed completed stages, not arbitrary escaping infinite width sums. A scalar multiplying a terminal Gaussian that depends genuinely on retained $z$ cannot be transferred into a compact coefficient independent of $z$ by an unproved manipulation; such sources lie outside this result.

| Question | 180 disposition |
| --- | --- |
| Linear independence of finitely many distinct Gaussian convolution widths over compact distributions | **PROVED**, using the named one-sided Paley–Wiener support indicator |
| Arbitrary mixed terminal widths, finite Hermite decorations and completed compact upstream histories | **CLASSIFIED for exact equality:** only a target-width effective coefficient can survive |
| No target-width term | **EXCLUDED for exact A**, without R1 cone |
| Target-width effective coefficient avoids original R1 diagonal conormal | **EXCLUDED for exact A** |
| Target-width effective coefficient may acquire a diagonal jet through nonidentity partition inclusion | OPEN; no cone assumption |
| General rapid equivalence and essential nonterminal retained-output scalar dependence | OPEN |
| Full original 108.7 first-core membership, universal 150.L, residual W acyclicity, original R3, full 126.14, higher weights, lifting, M5/R4 | OPEN |

**Successor 183, after source-locked V181/A181 critic and bounded ledger182:** analyze the remaining legally admitted histories with nonterminal retained-variable scalar couplings and nonidentity partition-jet inclusions; either construct one complete original 108.7 source for $A$ with genuine 126 rows, or prove an invariant that spans all finite histories and original uniform rapid equivalence. The current theorem proves only a strong **terminal-factorizable exact-source classification**, not global $W$ acyclicity.

This is a mathematical primary requiring competent source-locked review, protected PR checks, native merge and exact proof-blob readback. Same-system logical criticism or CI cannot certify external mathematical validity.