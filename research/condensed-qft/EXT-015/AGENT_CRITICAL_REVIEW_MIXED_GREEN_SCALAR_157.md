# EXT-015 REACH / 157 — critical mathematical review of the Gaussian–R1 Green-source lift

**Decision: BOUNDED ACCEPT of the exact one-Gaussian spectator-R1 source lift in 156; universal 150.L OPEN.**

**Reviewer provenance.** This is a separate, source-locked GCL *logical mathematical critic pass* using two distinct audit responsibilities: V157 reconstructs the positive distribution and source-stage proof, and A157 attacks the claimed scope and the finite-rank negative argument. Both passes run under one ChatGPT system and the same GitHub authentication as the primary author, consistent with GCL-AGENT-STAFFING-001. They are **not** independent authenticated researchers, a human expert panel or MATHCERT. The accompanying native GitHub COMMENT review (ID 5890708381) records substantive findings but is not an APPROVED review from a nonauthor account. The mathematical verdict below is bounded and never certifies 150.L.

## 1. Exact candidate, fixed inputs and source custody

| Item | Exact identity |
| --- | --- |
| Primary 156 | [MIXED_GREEN_SCALAR_COMMUTATOR_SOURCE_LIFT_156.md](MIXED_GREEN_SCALAR_COMMUTATOR_SOURCE_LIFT_156.md), reviewed Git blob fb683d69b5536df98805d104c9640234a486a2dd |
| Exact primary head | [PR 3296](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3296), commit 763ed33ed571f21b057744e0e65087d4985677ed |
| Exact standard-library fixture | [green_mixed_scalar_controls_156.py](fixtures/green_mixed_scalar_controls_156.py), Git blob 9e69c221e6f219f03c472229e5222ff7933ae9e3 |
| Scalar heat/Wick source 105 | Blob a8ce66ff0edec33e2aff299550fca2089d671033 |
| Mixed complete source 108 | Blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| Parameter source rule 126 | Blob 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| Normal-jet theorem 147 | Blob 89b3d4a835f3750114e983854585e33d8184cb1f |
| Primitive and R1 mapping 150 | Blob 03deca9212a9bea56743e482e5cb79edb46b9d7f |
| Previous 153/154/155 | Blobs ad0ba1a607e03337dd7489b1d2ea3415fd2afed9 / 7cd9ef2c329f87f97278296fb6c6ee3cdfb25058 / f453eaab8a7d34fdab1efb8f3e3c980df5dc6722 |

The first policy CI attempt on primary 156 failed because two display macros used an unsupported operator-name renderer. Its exact revised blob, listed above, replaces both with roman mathematical text without changing any formula or claim. All mathematical criticism here addresses that exact corrected source. Protected source admission and readback must be recorded separately; this text does not infer them from a merge request.

## 2. V157 — re-derive the exact normalized Gaussian identity

Take $e(t)=|t|/2$, $\kappa_\epsilon$ the centered normalized Gaussian of variance $\epsilon^2$, and $P_\epsilon=e*\kappa_\epsilon$. A direct calculation independent of the proposed source representation gives

$$
P_\epsilon(t)=\frac{\epsilon}{\sqrt{2\pi}}e^{-t^2/(2\epsilon^2)}
+\frac{t}{2}\mathrm{erf}\left(\frac{t}{\sqrt2\epsilon}\right),
\quad
P_\epsilon'(t)=\frac12\mathrm{erf}\left(\frac{t}{\sqrt2\epsilon}\right),
\quad
P_\epsilon''=\kappa_\epsilon.
\tag{157.1}
$$

The second equality follows because derivatives of the two exponential contributions to the first derivative cancel. It fixes the physical normalization; no factor of two or signed Jacobian is missing.

For a compact one-variable distribution $\rho(z)$ and scalar $s_\epsilon(z)$ independent of $y$, every partial moment in $y$ legitimately factors $s_\epsilon(z)\rho(z)$. In particular

$$
m_0(\chi\kappa_\epsilon\rho s)=\rho s(1+r_{0,\epsilon}),\qquad
m_1(\chi\kappa_\epsilon\rho s)=\rho s(z+r_{1,\epsilon}).
\tag{157.2}
$$

The two full Gaussian moments are exactly 1 and $z$, not merely asymptotic. Substitution into the moment-normalized Green convolution gives the full identity (156.8), including both tail-moment errors and the full convolution tail. The ordinary Lebesgue $dy$ density is retained; there is no extra inverse regulator measure factor. The compact support of the normalized primitive follows directly from the two vanishing affine moments, as proved in 150.3–150.6.

**Verdict V157-A: PASS for whole-positive-regulator distribution identity, normalization, and support.** No equality only modulo rapid terms has been substituted for actual equality.

## 3. V157 — independently check scalar-flat tails, including the singular crossing

On the fixed compact support of $\theta$ in the $z$ coordinate, the distance from that support to the complement of the plateau $\chi=1$ is a strictly positive $\delta$. Thus every contribution of $\chi-1$ has $|y-z|\ge\delta$. For each integer $N$, fixed derivative multi-index and compact $x,z$ set,

$$
\left|\partial_\epsilon^k\partial_z^l
\left[\theta(z)r_{j,\epsilon}(z)\right]\right|
\le C_{N,k,l}\epsilon^N.
\tag{157.3}
$$

For the convolution tail $R_\epsilon$, $e$ grows only linearly and its first derivative is bounded away from its jump. The integral of the Gaussian tail with those polynomial weights is smaller than any regulator power. The potential failure would be differentiating the nonsmooth $e(x-y)$ twice or more under the integral. Distributionally one instead uses

$$
\partial_x^2R_\epsilon(x,z)=(\chi(x)-1)\kappa_\epsilon(x-z).
\tag{157.4}
$$

Where $\theta(z)\ne0$, the coefficient $\chi(x)-1$ is supported at positive distance from $z$, so the right side and all its subsequent derivatives are exponentially small. This covers arbitrary fixed $x$ derivatives, not merely derivatives avoiding the singular surface by assumption. Multiplying by the fixed output cutoff $\psi$ makes all physical supports compact. Consequently the retained remainder and all mixed regulator/physical derivatives are flat along every regulator boundary face of the two-vertex heat blowup. Since $\epsilon$ pulls back to a positive unit times a finite boundary monomial, arbitrary powers of $\epsilon$ absorb every requested finite b-weight and derivative loss.

Source 105.5 admits such actual flat functions in the fixed scalar power/logarithmic stage. It is crucial that the author **retains** the flat terms in the finite representation; dropping them would prove equality only in a quotient, and would not meet 150.L's actual-history requirement.

**Verdict V157-B: PASS for exact scalar-stage membership and all faces in this two-slot geometry.**

## 4. V157 — R1 typing, completed coefficient map and parameter rows

The output distributional R1 factor is $T'(x,z)=\phi(x)\rho(z)$. Its wavefront covectors have zero $x$ component. A forbidden two-slot diagonal conormal would have nonzero and opposite $x,z$ components, so the output cone is admissible even if $\rho$ is a point delta or a finite delta derivative.

The scalar coefficient $A_\epsilon(x,z)$ is a fixed compactly supported combination of the admitted Wick edge $P_\epsilon(x-z)$, smooth physical moment factors and a scalar-flat remainder, multiplied by an allowed spectator scalar $s_\epsilon(z)$. The pullback of the one-slot scalar stage to the two-slot heat space is the ordinary interior b-map of 105.4. The multiplication and fixed index-family union belong to the scalar theorem 105.6; there is **no zero-width interior Green factor** inserted as either a scalar or R1 coefficient. The output has the single legal existing-history form

$$
q_*[A_\epsilon T'],\qquad q=\mathrm{id},
\tag{157.5}
$$

with identity partition and no forbidden same-block jet. The cutoff equalities make this an actual identity of distributions, not just an equality of scalar asymptotic coefficients.

Fix a one-slot graph space $E_{s,K,\Gamma}$ and one spectator scalar stage $S_\lambda^{(z)}$. The map on completed coefficients is induced by a continuous smooth-tensor map $\rho\mapsto \phi\boxtimes\rho$ and a fixed scalar-stage multiplication map $s\mapsto A[s]$. Their projective tensor extends continuously into one output completed $E'\widehat\otimes_\pi S'$, with a support, cone, finite index family, density and history independent of relaxed Sobolev orders. Compatible derivative rows have the same maps and Leibniz derivatives. The separately known full ambient estimate (150.6) preserves uniform rapid equality on the evaluated whole-family image. These arguments cover the stated **spectator subspace**, not all of 126.14 or 108.7.

**Verdict V157-C: PASS for this fixed completed sector and its compatible 126 rows.**

## 5. A157 — actively attack the novelty and no-go claims

**Singular R1 witness:** Set $\rho=\delta_{z_0}$ with $z_0\in K$. At each positive regulator, the source $\chi(y)\rho(z)$ and output $\phi(x)\rho(z)$ have a one-slot conormal with zero component in the other variable, so both satisfy the two-slot R1 exclusion. The exact scalar multiplier regularizes the new $x=z$ collision. At regulator zero the scalar Wick factor approaches a cusp; the limiting product is *not* itself a legitimate pure R1 coefficient at the double point, but the fixed completed scalar/R1 **positive-family** representation remains legal. The source cannot be checked merely by taking its zero-scale wavefront.

**Finite separated-mode attack:** Differentiate the proposed finite-rank representation twice in the integrated output coordinate on an interval where the moment bumps vanish. One obtains a fixed finite span of $f_j(x,z_0)$ containing every normalized Gaussian $\exp[-\lambda(x-z_0)^2]$. For $N+1$ distinct rates, the even-derivative matrix at $x=z_0$ has entries proportional to $\lambda^k$, a nonzero Vandermonde determinant. The finite span is impossible. This proves a strict no-go for **epsilon-independent separated $y$ modes with spectator-only scalar coefficients**. It does not exclude the actual one-history nonseparable Wick scalar constructed in the same primary. No impossibility result for arbitrary 108.7 histories follows.

**Commutator attack:** In (156.2), the two finite moment correction terms do not vanish merely because the convolved scalar is smooth. The hostile R1 point example of 154 verifies the scalar/Green commutator can be nonzero. The 156 calculation retained these terms correctly. The 242-input/2662-pairing rational fixture is consistent with the identity, but cannot validate a continuous infinite-dimensional source map.

**Scope attack:** The admissible source $T(y,z)=\delta_0(y)\rho(z)$ from 154 has a singularity in the integrated coordinate and is NOT of the spectator form $\chi(y)\rho(z)$. The new proof cannot pass that input through the smooth R1 tensor map or its Gaussian-flat scalar reduction. Hidden vertices, arbitrary jets, all enlarged collision corners, nontrivial scalar indices depending on the integrated variable, and the unrestricted residual cochain object all remain outside the proof.

**Verdict A157: no contradiction in the specified theorem; reject every proposed extension beyond the single Gaussian spectator sector.**

## 6. Final mathematical disposition

| Inference | Critic verdict |
| --- | --- |
| Exact full normalized Green/scalar commutator | ACCEPT |
| Gaussian–spectator R1 source representation | **ACCEPT WITH FIXED-STAGE HYPOTHESES** |
| Actual equality, not only rapid equivalence | ACCEPT |
| Completed projective coefficient source and compatible mixed rows in that sector | ACCEPT WITH FIXED SUPPORT/CONE/STAGE |
| Fixed finite separated Gaussian-mode ansatz | REJECT: genuine Vandermonde obstruction |
| Gaussian/Wick edge replaced by zero-width singular scalar | NOT ADMITTED |
| Generalized 150.L for all distinct-block histories | **UNPROVED** |
| Residual $W$ acyclicity and original R3 | **UNPROVED** |
| 126.14 full family recovery, higher weights, actual lifting and M5/R4 | **OPEN** |

**Canonical decision: BOUNDED_ACCEPT__EXACT_GAUSSIAN_SPECTATOR_LIFT__150L_OPEN.**

One primary 156 and one renderer-only correction after the first CI attempt; no mathematical source correction was required. The subsequent 158 ledger must distinguish this logical-role mathematical review from the source's protected GitHub admission and must not report any broader completion. A new research step should target a **non-spectator R1 distribution with a genuine conormal in the integrated coordinate** and analyze its complete augmented collision corners; the case just reviewed is a successful base case, not the universal theorem.
