# EXT-015 REACH / 196 — critical test of improper zero-width source integration and source-stage completion

**Mathematical disposition: BOUNDED ACCEPT with one documentary-only source195 custody correction, no mathematical author correction; conditional on the exact anchored-scalar channel and on protected source custody.** Verifier V196 and Adversary A196 are separate logical source-locked passes by the same ChatGPT/GitHub identity; neither is an independent nonauthor APPROVED review, external referee or MATHCERT certificate.

## 1. Exact source and non-promoted antecedents

The frozen primary candidate is [DEFECT_WIDTH_INTEGRAL_SOURCE_COMPLETION_195.md](DEFECT_WIDTH_INTEGRAL_SOURCE_COMPLETION_195.md), original source Git blob 122ab5d709f983abe0eb3bedcc9a8890d620bc67, and corrected exact mathematical source Git blob 9165aa604fcad4935ccfa541334d023deda8ce5a (documentary-only upstream custody correction, commit cf009eee5f079dcb3cd960d39df99bb8eceea9aa on PR3362). Its proposed defect is the same exact expression as the now **protected** primary192, Git blob 6003987b03980ae65ead3e286109be1eed02c8c7, native PR3360 merge ff1f71ff5686a4adcac659bd6e6e817a77139666, and protected critic193 blob 39873b26b2b1e9085d77cdb0964658ef7bd6b69d. Admission of primary192 is a source-custody fact, not by itself a proof of primary195. The standalone identities of primary195 follow from protected scalar105 (blob a8ce66ff0edec33e2aff299550fca2089d671033), mixed108 (587c15fd6e24f6e6b14de574ff878221cdbd5cb6), parameter126 (5b05c6147d237ca1d22e4dcbce9262b0f038c163), original first core165 (24b82716d41d309438fcb7a97bbacab0b724afde), and the already protected anchored nonpolynomial source construction in canonical PR3355 merge f71362ef0fba3a3b73d023a63f74efc3651b2bc3. Supplement DG-186B is separately protected by PR3354 merge 51aecf3d1d42a41127ef1b5e890dafb8e16d232f.

The critic tests legality of the fixed-width source, distributional integration of a legal continuum of source values, nonrapidness of every fixed truncation, and nonconvergence inside a single complete scalar stage. It must not infer full source image closure or a global negative answer to the first Green core.

## 2. V196 — independent Gaussian heat-time and normalisation check

Write $e(x)=|x|/2$, so $e''=\delta_0$. Since $P_\sigma=e*\kappa_\sigma$ and $\partial_\sigma \kappa_\sigma=\sigma\partial_x^2\kappa_\sigma$ for positive $\sigma$, distributional convolution gives

$$
\partial_\sigma P_\sigma
=\sigma\partial_x^2(e*\kappa_\sigma)
=\sigma\kappa_\sigma.
\tag{196.1}
$$

Substituting $\sigma=a\epsilon$ while holding $\epsilon$ fixed yields $\partial_aP_{a\epsilon}=a\epsilon^2\kappa_{a\epsilon}$. Integration from a positive $d$ to $b$ gives exactly $P_{b\epsilon}-P_{d\epsilon}$; the limit $d\downarrow0$ gives $P_{b\epsilon}-e$ in ordinary distributions. This establishes the equality with the width integral in primary195 without assuming Bochner integrability in any original source stage. Its density and scalar coefficient are consistent: the $a\epsilon^2$ factor comes from the scale derivative, not from forgetting a physical vertex.

For each fixed width $a>0$, attach two real physical relative Gaussian edges $x-h$ and $z-h$ to a hidden vertex $h$ constrained by a genuine original R1 $\delta_0(h)$. At $h=0$, a pure nonzero $h$ covector cannot have zero sum on its partition block, so the R1 coefficient avoids each original forbidden partial-partition conormal. Two admitted 105 scalar edges, fixed cutoffs, positive fixed width rescalings, a finite scalar Laurent factor and proper forgetting give exactly the proposed $a\epsilon^2\chi(x)\rho(z)\kappa_{a\epsilon}(x)\kappa_\epsilon(z)$ as one legal finite108 history. Replacing the first relative edge by the original Wick factor $P_{a\epsilon}(x-h)$ gives the admitted smooth Wick history at that fixed width. In both cases, fixed source supports, complete scalar index stages and compatible source-controlled126 rows are furnished by original105/108; none is asserted uniformly as $a$ approaches zero.

**V196 ACCEPT the fixed-width source legality and the distributional identity.**

## 3. A196 — rapidness and zero-width stage stress tests

For any fixed positive $d<b$, the truncated difference of two positive-width admitted Wick histories is itself in the original finite mixed source. Its exact residual is the width-d smoothed cusp difference, and the heat-semigroup formula gives

$$
P_{d\epsilon}-e
=\int_0^{d^2\epsilon^2/2}\kappa_{\sqrt{2t}}\,dt,\qquad
\int(P_{d\epsilon}-e)\,dx=d^2\epsilon^2/2.
\tag{196.2}
$$

Choose an output test equal to one near both anchors, with compact support in the cutoffs. The $x$ tail beyond a fixed neighborhood is Gaussian-flat; the $z$ Gaussian moment integral is $\rho(0)+O(\epsilon^2)$. Their product gives precisely

$$
\langle D^{(b)}-D^{[d,b]},\phi\otimes\zeta\rangle
=d^2\rho(0)\epsilon^2/2+O(\epsilon^4).
\tag{196.3}
$$

The coefficient cannot vanish because $d>0$ and $\rho(0)\ne0$. A uniformly rapid distribution family has rapidly small pairing with this fixed test. Therefore no *fixed* $d>0$ truncation is rapid-equivalent to the exact defect. This is an explicit all-regulator statement, not a claim about letting $d$ depend on $\epsilon$.

For every positive regulator, $P_{b\epsilon}$ is smooth and $e$ has one unit derivative jump across zero. On a patch with $\chi=1$ and nonzero $\rho\kappa_\epsilon$, the defect's derivative jump is minus $\rho(z)\kappa_\epsilon(z)$, so it is not $C^1$ in the cusp coordinate. Every source from the **specified anchored-scalar channel with original fixed R1 $\delta_0(h)$ and scalar105 complete smooth coefficients** evaluates to a $C^\infty$ function at any fixed positive regulator: restricting a smooth scalar coefficient to $h=0$ is continuous in every interior scalar $C^r$ seminorm, and 108's completed projective tensor map preserves these fixed estimates. A limit in one such complete stage would therefore have smooth positive-scale output. The defect cannot be that limit.

Independently, at fixed $\epsilon>0$ the twice-differentiated truncated scalar at zero is

$$
\partial_x^2(P_{b\epsilon}-P_{d\epsilon})(0)
=(\sqrt{2\pi}\epsilon)^{-1}(b^{-1}-d^{-1}),
\tag{196.4}
$$

which diverges as $d\downarrow0$. This explicitly shows why the family has no bounded interior $C^2$ seminorm as it approaches the forbidden zero-width endpoint. The source-image conclusion is strictly limited to this anchored scalar stage; it says nothing about alternate legal R1 singularities or partition-jet source histories.

**A196 ACCEPT the fixed-positive-truncation nonrapid statement and the anchored-scalar-stage nonconvergence claim. REJECT any inference that the entire mixed $\mathcal P_2$ source image is closed in the ambient distribution topology or that the defect is globally excluded from $\mathcal P_2$.**

## 4. Bounded adjudication ledger

| Question | V196/A196 |
| --- | --- |
| Exact scale derivative and parameter integral identity | ACCEPT |
| Legal original105/108 positive-width anchored Gaussian and Wick histories | ACCEPT at each fixed positive width |
| Each fixed positive lower-width truncation gives a complete source | ACCEPT |
| Such a fixed truncation is equivalent modulo original uniform rapid | FALSE by order-two pairing |
| Ordinary distribution limit as lower width tends to zero | EXISTS |
| Source-stage limit within the same anchored smooth scalar complete channel | EXCLUDED by positive-regulator cusp and derivative seminorm blowup |
| Source status via a different admitted R1/partition/completed history | OPEN |
| Full first Green core, universal150.L, residual W acyclicity, original R3, full126.14, higher weights, lifting and M5/R4 | OPEN |

**Review decision: BOUNDED ACCEPT of the documentary-corrected primary195, Git blob 9165aa604fcad4935ccfa541334d023deda8ce5a, as a fixed-channel no-go and a legal source-approximation result.** Source status of the exact defect and first core stays OPEN. No continuous source integral across $a=0$ or infinite jet completion may be inferred from pointwise admission of each positive-width integrand. This report and its companion ledger197 require native exact-head checks, protected merge and exact source readback before the result can be recorded as protected.

## 5. V196/A196 one-correction replay

The single primary195 author correction changed only the upstream192–194 Git custody from pending to protected, added the actual protected review193 blob, and replaced stale procedural text. It did **not** modify the Gaussian identities (195.1–195.10), test estimate (195.11), jump (195.12), stage restriction, or divergent seminorm (195.13). I re-read corrected exact source195 Git blob `9165aa604fcad4935ccfa541334d023deda8ce5a` and rechecked the original V196/A196 mathematical argument against those unchanged claims. **BOUNDED ACCEPT remains valid with one documentary correction; no new mathematical claim is promoted.**
