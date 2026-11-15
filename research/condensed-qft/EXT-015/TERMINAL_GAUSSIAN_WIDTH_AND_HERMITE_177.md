# EXT-015 REACH / 177 — terminal Gaussian-width and Hermite hidden-source obstruction

**Primary mathematical disposition: BOUNDED NEGATIVE.** This tests an existing-source subclass with arbitrary finite compact hidden histories that reduce to one or more terminal Gaussian convolution edges. Every finite list of terminal widths strictly below the target width, or every width strictly above, fails to represent the first Green core **exactly**. If all widths match the target, and the effective hidden coefficients retain the original R1 diagonal-conormal exclusion, finite Hermite-decorated combinations also fail. Mixed-width lists straddling the target, non-Gaussian retained-variable dependence, general partition jets, the full source status of $A$, universal 150.L and residual $W$ acyclicity remain OPEN.

## 1. Frozen source and target

Retain existing protected 105 (blob a8ce66ff0edec33e2aff299550fca2089d671033), 108 (587c15fd6e24f6e6b14de574ff878221cdbd5cb6), 126 (5b05c6147d237ca1d22e4dcbce9262b0f038c163), 165 (24b82716d41d309438fcb7a97bbacab0b724afde), the second-arm source168 (e2c43f218c9175b919c51f371acb8c04e659faea), first-arm no-hidden theorem171 (4d4818e6927eb951a3810c621f94832de1371e33), and single-bridge proof174 (7c470ba092d917dc434a8883e5afaff7bce1dfc6), critic175 (a7a48135ed2a44af405714cd4132574aaf05a0e5), ledger176 (006cdfe3a9f04edf247dff066f7e283fc68161ba). Original 174 was protected in PR3332 at cb152d233986119a860e9e89c3292960f6f2ba27, review/ledger in PR3337 at 8fa05de84241457eae6898f6327ce8791b0f9a59, and CP191 in PR3338 at 054bf5dfe5c60ecd580537250dec1ee2c38000f9. Those source objects are protected/read back; same-system logical reviewers are not independent mathematical certifiers.

Fix compact smooth $\chi,\rho$ with $\chi=1$ near zero and $\rho(0)\ne0$. Set

$$
f(x)=\chi(x)|x|/2,\quad
\kappa_{\sigma}(t)=(\sqrt{2\pi}\sigma)^{-1}e^{-t^2/(2\sigma^2)},
\quad
A_\epsilon(x,z)=f(x)\rho(z)\kappa_\epsilon(z).
\tag{177.1}
$$

The source membership of the two original labelled/symmetric Green outputs is equivalent to full membership of this remaining $A$ core by protected 165/168. Choose an open interval $J$ around zero with $\rho$ nowhere zero.

## 2. Precisely delimited terminal source subclass

A legal **terminal Gaussian source** is an existing finite 108.7 history which, after evaluating its already admissible scalar/R1 partition, projection, derivative and completed-tensor operations, has the exact positive-regulator output

$$
S_\epsilon(x,z)=\rho(z)\sum_{j=1}^{m}\sum_{k=0}^{d_j}
 c_{jk}(\epsilon)\epsilon^k
 \partial_z^k\bigl[\kappa_{a_j\epsilon}*_{y}
 U_{j,\epsilon}(x,\cdot)\bigr](z).
\tag{177.2}
$$

The numbers $m,d_j$, positive width ratios $a_j$ and scalar coefficient list are finite and fixed. Each $U_{j,\epsilon}$ is a compactly supported distribution in $(x,y)$ for each positive regulator; its support lies in the fixed compact physical hull of the original source. Coefficients $c_{jk}(\epsilon)$ are genuine values of declared, fixed complete scalar stages, not arbitrary escaping-index series. All prior hidden Gaussian/Wick edges, nonfactorable **upstream** coordinate dependence, proper forgotten spectator integrals, finite normal jets, source-controlled 126 parameter rows and completed projective 108.6 coefficients are allowed *provided that the actual evaluated history has the displayed terminal factorization*. The sole retained- $z$ dependence beyond the outer $\rho$ is the listed Gaussian factors and their finite derivatives. Histories with essential additional retained- $z$ dependence are outside this class.

This definition describes a **subset of already lawful 108.7 histories**, not an authorization to use arbitrary $U$ as new source coefficients. For equal-width claims only, additionally require every $U_{j,\epsilon}$ to have wavefront excluding the diagonal conormal $(\tau,-\tau)$ to $x=y$ at the joint anchor. This is proved for the 174 identity-partition upstream R1 histories with smooth multipliers, proper spectators and finite derivatives. It is **not** asserted for arbitrary nonidentity partition inclusions, which could create that conormal. The different-width theorem below needs no R1 hypothesis on the effective compact coefficients.

## 3. Compact Fourier bounds and width exclusion

**Lemma 177.1.** For a compactly supported distribution $U(x,y)$ and an arbitrary fixed compact smooth $x$ test $\phi$, its $y$ -Fourier transform $F_\phi(\zeta)$ is entire; for some constants $C,N,R$ depending on this fixed distribution/test/support,

$$
|F_\phi(\xi)|\le C(1+|\xi|)^N\quad(\xi\in\mathbb R),\qquad
|F_\phi(it)|\le C(1+|t|)^Ne^{R|t|}
\quad(t\in\mathbb R).
\tag{177.3}
$$

The result survives finitely many $y$ derivatives with higher polynomial degree. **Proof.** A compact distribution has finite order. Testing it against a compact cutoff times $e^{-i\zeta y}$ bounds its derivatives by a polynomial in $|\zeta|$ and the maximum of $|e^{-i\zeta y}|$ on its compact support. For real and pure imaginary $\zeta$ these give (177.3). The pairing is entire by finite-order parameter differentiation. $\square$

**Theorem 177.2 (same-side width obstruction).** If a finite legal terminal source (177.2) has either all $0<a_j<1$, or all $a_j>1$, it **cannot equal $A_\epsilon$ at every positive regulator**, even with arbitrary compact upstream distributions, completed coefficients, different widths within the same side, Hermite decorations, and finite cancellations.

**Proof.** Choose $\phi$ with $c_\phi=\langle f,\phi\rangle\ne0$. Divide an alleged equality by the nowhere-zero $\rho$ on $J$. The Gaussian convolutions are entire in $z$ after pairing with $\phi$; equality on $J$ extends to all real $z$. For each fixed positive regulator, Fourier transformation gives

$$
\sum_j e^{-a_j^2\epsilon^2\xi^2/2}
 P_{j,\epsilon}(\xi) F_{j,\epsilon,\phi}(\xi)
=c_\phi e^{-\epsilon^2\xi^2/2},\qquad
P_{j,\epsilon}(\xi)=\sum_{k=0}^{d_j}c_{jk}(\epsilon)(i\epsilon\xi)^k.
\tag{177.4}
$$

If every $a_j>1$, the polynomial Fourier bounds on the real line make the left side decay strictly faster than its nonzero right side as $|\xi|\to\infty$. If every $a_j<1$, continue the entire identity to $\xi=it$. With $a_{\max}<1$, Lemma 177.1 bounds the left side by a polynomial in $|t|$ times $\exp(a_{\max}^2\epsilon^2t^2/2+R|t|)$, while the right side has magnitude $|c_\phi|\exp(\epsilon^2t^2/2)$. This is impossible for large $|t|$. All constants may depend on the **fixed** positive regulator; no regulator-uniform Fourier estimate or uncontrolled inverse heat map is used. $\square$

The theorem does **not** cover a list of terminal widths straddling one, or a list containing a width exactly one alongside other widths; no cancellation theorem for those mixed cases has been proved.

## 4. All equal widths: Hermite terms are finite hidden derivatives

**Theorem 177.3 (equal-width Hermite obstruction).** Suppose every $a_j=1$ in (177.2), and the effective compact $U_{j,\epsilon}$ have the permitted R1 diagonal-conormal exclusion stated in section 2. Then no finite such legal history represents $A$ exactly.

**Proof.** Distributional integration by parts transfers each $z$ derivative of the Gaussian convolution onto the corresponding compact hidden coefficient, with the standard physical density. Combine the finite terms into

$$
V_\epsilon=\sum_{j,k}c_{jk}(\epsilon)\epsilon^k
  \partial_y^kU_{j,\epsilon},\qquad
S_\epsilon=\rho(z)[\kappa_\epsilon*_{y}V_\epsilon].
\tag{177.5}
$$

Finite derivatives and sums preserve the absence of the forbidden $x=y$ conormal. By the exact local Gaussian injectivity proved in 174.2, equality on $J$ forces $V_\epsilon=f(x)\delta_0(y)$ for each positive regulator. At the joint origin its cusp-times-delta wavefront contains nonzero $(\tau,-\tau)$, contradicting the effective R1 cone. This includes finite polynomial/Hermite dependence on the retained relative coordinate via the fixed derivatives in (177.2), and completed source combinations, without invoking a regulator-zero graph limit. $\square$

An arbitrary partition inclusion may create an effective diagonal jet after pushforward, so its admission into the equal-width case requires its **own** cone argument, not a blanket assertion from the original R1 input.

## 5. Sharp examples, claims and next target

For a smooth compact $g(x)$, the legal original pure-hidden-delta R1 source $g(x)\delta_0(y)$ with terminal width one evaluates exactly to $g(x)\rho(z)\kappa_\epsilon(z)$. Thus the equal-width theorem detects the independent cusp, not the Gaussian anchor itself. For a single width $a<1$, Gaussian deconvolution would require $f(x)\kappa_{\epsilon\sqrt{1-a^2}}(y)$ as the compact effective input, which is noncompact in $y$; for $a>1$, it requires a Fourier transform growing super-Gaussianly on the real line, impossible for compact distributions. At $a=1$, it requires $f(x)\delta_0(y)$, compact but forbidden by the effective R1 cone. This gives three distinct mechanisms behind the same finite terminal-source obstruction.

| Question | 177 status |
| --- | --- |
| Every finite terminal width strictly less than one, or every width strictly greater than one | **EXCLUDED for exact A**, no effective R1 hypothesis needed |
| All equal-width terminal Hermite combinations with effective permitted R1 coefficients | **EXCLUDED for exact A** |
| Mixed terminal-width lists straddling one, or including equal width with others | OPEN |
| Essential nonpolynomial retained-variable scalar dependence and arbitrary partition inclusions | OPEN |
| General rapid-equivalent source in these subclasses without extra fixed-stage hypotheses | OPEN |
| Full source membership/nonmembership of A, universal 150.L, residual W acyclicity, R3, full 126.14, higher weights and M5/R4 | OPEN |

**Successor 180 after source-locked critical review178 and bounded ledger179:** investigate mixed-width cancellations and remaining legal hidden sources with non-Gaussian retained-coordinate couplings, arbitrary partition inclusions and completed source cancellations. A positive result must give one complete admitted source with proper densities, all heat corners, R1 cone and 126 rows; a negative result must exclude all genuinely permitted finite histories. Do not certify the universal Lemma 150.L, residual W acyclicity or programme closure on this bounded theorem.

This is a primary mathematical manuscript candidate, not an independently certified theorem.