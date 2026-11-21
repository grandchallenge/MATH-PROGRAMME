# EXT-015 REACH / UC032 — nonauthor review of the coupled moving-delta lift

**Bounded accept.** UC031 gives an exact lift of the whole localized $h_1(1-C_2)$ for the stated moving delta with a fixed Schwartz relative profile and fixed regulator power. This includes the coupled Gaussian, the stated hidden Gaussian bridge, and fixed finite derivative decorations. The original completed sources, supplied parameter rows, and rapid quotient carry the result. Universal 150.L remains open. No author correction was required.

## 1. Frozen sources

I reviewed [UC031](MOVING_DELTA_GREEN_LIFT_UC031.md) at commit `d908b816d810b6473740b4c83da4a067a9b84b3d`, blob `c0b632314cc2f68864878e9cee6653bfa491b794`. I verified that commit at the retained remote ref `research/reach-moving-delta-uc031-primary-20261121` and the scientific input `05771e70b4fa5f23e8df0bdd5d30bbe7c982cf3f` at `research/reach-moving-delta-uc031-input-20261121`. The primary's parent `2b8888d64c60355c5b43f7607878b3b147344300` records CP264 before construction. I checked these dependency blobs at the frozen input and primary commits.

| Dependency | Verified blob |
| --- | --- |
| [105 scalar stages and heat space](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | `a8ce66ff0edec33e2aff299550fca2089d671033` |
| [108 mixed histories and rapid curves](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | `587c15fd6e24f6e6b14de574ff878221cdbd5cb6` |
| [126 parameter rows](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | `5b05c6147d237ca1d22e4dcbce9262b0f038c163` |
| [150 compact Green normalization and open lemma](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) | `03deca9212a9bea56743e482e5cb79edb46b9d7f` |
| [Corrected 195 conic split and heat proof](JOINT_DEFECT_SOURCE_AUDIT_195.md) | `fc0fddb678f0cc0c1b9764bb449ab6d9150b33d0` |
| [UC013 filtered Green lift](FILTERED_COMPACT_GREEN_SOURCE_UC013.md) | `05ed1fafdbc35cc63c1423d4e48292d24193d029` |
| [UC025 moments and rapid descent](CLUSTER_TRANSLATION_GREEN_LOCALIZATION_UC025.md) | `32132370301c80394d14aeaa3124bef9f561d00d` |
| [Corrected UC028 ordered fibre and hostile input](ORDERED_FIBRE_GREEN_LIFT_UC028.md) | `6b623f83aeb7c9eb2019a38747a0332d5e152f91` |
| [UC030 bounded ordered-fibre acceptance](ORDERED_FIBRE_GREEN_ACCEPTANCE_UC030.md) | `74a3e067f3eb5a7c8a148d01ee90e8167148bab8` |

I performed this review in a distinct nonauthor agent context of the same Codex system and shared Windows CHAD worktree. The disposition records internal mathematical scrutiny. Protected admission, external peer certification, and MATHCERT have separate authority.

## 2. Physical fibre and all partition conormals

The covectors of the cut-off $\delta(u+c)$ are proportional to $(1,1)$, outside the two-block collision conormal. The relative scalar has its fixed Schwartz profile and regulator power on the two-point front. In strict corner charts, rapid decay of the scaled argument profile absorbs each fixed derivative and requested order of vanishing. This supplies the original 105 scalar stage. Holding the actual spectator $c$ gives UC028's moving slice. Holding the midpoint of $(u,c)$ would fix a different variable.

At fixed $c$, $\partial_u(u+c)=1$, so the delta sets $u=-c$ with unit density in $du$. Pairing $e(x-u)$ against a smooth compact $x$ test first gives a smooth function of $u$. The localized fibre output is therefore $A_\epsilon(x,c)e(x+c)\epsilon^\nu\rho(-2c/\epsilon)$. The sign matters for a noneven profile. The new midpoint $m=(x+c)/2$ is introduced only in the coefficient of the augmented history.

The identity $e''=\delta_0$ gives $\widehat W_b=-q/\xi^2$ because the cutoff avoids the $\xi=0$ ambiguity. Differentiated symbol bounds give smoothness off the origin. On a smaller cone about $\eta=-\xi$, the Fourier transform of $W_g$ vanishes at high frequency. Physical localization convolves with a Schwartz transform, giving rapid decay in a still smaller cone by separation from the high-frequency support. Off the origin any original wavefront is pure $y$.

After pullback by $(x,c,y)\mapsto(m,y)$, a possible covector has the form $(\xi/2,\xi/2,\eta)$. Conormals to partition diagonals require zero sum on each block.

| Partition | Check |
| --- | --- |
| $x\mid c\mid y$ | Each individual covector must vanish. |
| $xc\mid y$ | The sums force $\xi=\eta=0$. |
| $xy\mid c$ | The singleton forces $\xi=0$ and the joined sum then forces $\eta=0$. |
| $cy\mid x$ | The singleton forces $\xi=0$ and the joined sum then forces $\eta=0$. |
| $xcy$ | The sum is $\xi+\eta$. At $m=y=0$ its zero directions are the two removed rays. Away from there any covector is pure $y$ with nonzero sum. |

The conic gap and compact localization give a fixed closed admissible cone. The other graph, $\delta_0(h)$, has a sole nonzero $h$ covector, so its block sum is nonzero in every partition. Both coefficients belong to fixed complete graph stages.

## 3. Schwartz smoothing and the full scalar collar

The degree $-2$ angular symbol of corrected 195 has a radial $dR/R$ finite part. Scaling shifts it by a multiple of the frequency delta. Thus its inverse transform $H$ changes by $b_0\log\lambda$ under dilation by $\lambda>0$. Smoothness off the point gives a smooth angular term plus $b_0\log|(r,y)|$. These locally integrable terms obey the same scaling law. Any extra distribution at the point would consist of delta derivatives of scaling degrees $-2-j$, so that law excludes a point-supported remainder. The cut symbol differs from the finite part in compact frequency support. Consequently $\theta W_b-H$ is smooth with polynomially bounded derivatives in the integration variable on compact physical sets. Its convolution against $K(Y)$ at $y=s-\epsilon Y$ is smooth through zero by weighted Schwartz seminorm bounds.

For $H_\epsilon=k_\epsilon*_yH$, high-frequency derivative integrals use polynomial factors times derivatives of $\widehat K(\epsilon\eta)$. On the support, $|\eta|$ bounds a fixed positive multiple of the whole frequency, so sufficiently weighted Schwartz seminorms control every requested derivative by finite powers of $\epsilon^{-1}$. The compact frequency part acts on finitely many test derivatives. This proves positive-scale smoothness and moderate bounds. The exact scaling identity is

$$
H_\epsilon(\lambda r,\lambda s)
=H_{\epsilon/\lambda}(r,s)+b_0\left(\int K\right)\log\lambda .
$$

The central front chart follows by setting $\lambda=\epsilon$. For the strict face, take a compact output annulus inside a slightly enlarged annulus $A'$, with positive inner radius. A sufficiently small point cutoff $\vartheta$ gives $|s-y|\ge d>0$ whenever $\vartheta H$ contributes on $A'$. This compact point piece is in $L^2$ by the logarithmic form. Each fixed regulator derivative of the separated kernel is $O(\epsilon^N)$ for any $N$, using a finite weighted Schwartz seminorm. Cauchy–Schwarz in the bounded $y$ interval gives the same rapid $L^2$ bound for the separated convolution on $A'$. Multiply by an output cutoff supported in $A'$ and equal to one near the original annulus. This cut term has moderate $H^M$ bounds for every $M$, by subtracting the actual smooth complementary convolution from the Fourier-controlled whole. Interpolation with these bounds and Sobolev embedding give arbitrary rapidness in each fixed differentiated $C^j$ norm on the original annulus. This argument also applies to each fixed regulator derivative. The strict extension is the smooth complementary family plus the flat extension of the separated family. Every estimate uses finitely many Schwartz seminorms.

For $a=|(r,s)|$, $\omega=(r,s)/a$, and $\sigma=\epsilon/a$, the strict corner has the actual expression $H_\sigma(\omega)+b_0(\int K)\log a$. The smooth extension just proved works on a neighborhood of the entire angular circle, supplying all Taylor remainders. The formula keeps the actual family when $\int K=0$.

Write $z_1=x-h$ and $z_2=c-h$ in the source of (UC31.6). The map $(z_1,z_2)\mapsto((z_1+z_2)/2,z_2)$ is invertible. On the full radial blowup it changes angle smoothly and changes radius by a smooth positive factor. The three **source** pair directions are $z_1=0$, $z_2=0$, and $z_1=z_2$, with disjoint angular loci. Near a locus use a transverse angular coordinate $v$. The remaining center is $\sigma=v=0$, with $a$ passive. The charts $\sigma=\tau,\ v=\tau V$ and $v=\pm\tau,\ \sigma=\tau S$ give smooth pullbacks of the smooth term, leaving a single full-front logarithm up to smooth terms. The regulator is $a\tau$ and $a\tau S$, respectively, so the fixed power has its actual monomial shifts. Taylor bounds in these charts give the recursive new-face remainders. Away from the radial front the strict extension is already smooth before each pair blowup. This supplies the original full 105 scalar stage even though the linear map changes the pair directions. Fixed ordinary derivatives incur the finite shifts of 105.6. No density change in the physical fibre is involved.

## 4. Exact outputs, finite derivatives, and rapid descent

The good history uses its fixed graph and the scalar $2A_\epsilon\epsilon^{\nu+1}k_\epsilon(c-y)$. This is the two-point stage pulled back by vertex forgetting and decorated by the fixed power and smooth multipliers. The bad history uses the verified three-point scalar and $\delta_0(h)$, with unit delta pairing in $dh$. Adding the good $dy$ integral and the bad output restores $W_g+W_b=e(m)\delta_0(y)$ with $\theta(0)=1$. The sum is $2A_\epsilon\epsilon^{\nu+1}e(m)k_\epsilon(c)$, the original fibre since $2e(m)=e(x+c)$ and $\epsilon k_\epsilon(c)=\rho(-2c/\epsilon)$. In the Gaussian case $k_\epsilon=\tfrac12\kappa_{\sigma\epsilon/2}$. In a unit-amplitude scaled box the Green convolution has profile $e(X+C)\kappa_\sigma(2C)$, nonzero at $X=C\ne0$. The substitution $c=\epsilon C$ gives fixed-test limit $\tfrac12 A_0(x,0)e(x)\delta_0(c)$. This verifies the nonrapid core before the affine and filtered corrections.

The hidden bridge has independent $d$ and nonzero-total graph covector $(1,1,0)$. Completing the square with $S=\sigma_1^2+\sigma_2^2$ gives mean $(\sigma_2^2u+\sigma_1^2c)/S$ and widths $\sqrt S\,\epsilon$ and $b\epsilon$, where $b=\sigma_1\sigma_2/\sqrt S$. Their product is exactly $\sigma_1\sigma_2\epsilon^2$, preserving Gaussian normalization. Substituting $d=\mu+b\epsilon Y$ in the actual $dd$ density gives the normalized Gaussian average of the zero-extended smooth amplitude. Joint derivatives are bounded by compact smooth seminorms and Gaussian moments, giving a smooth extension through zero with projected compact support. This permits simultaneous collision of both edges.

For $\delta^{(n)}(u+c)$ the test pairing acts by $(-1)^n\partial_u^n$ at $u=-c$. Each derivative on the cusp contributes another minus sign and a cusp derivative. Each derivative on the relative scalar replaces the Schwartz profile by its derivative and shifts the regulator power down one. The finite Leibniz multiplicities and amplitude derivatives remain. Output $\partial_x$ produces the cusp derivatives from a lift localized with a cutoff equal to one near the final support. Retained derivatives commute with the unnormalized convolution before the output cutoff, with the finite Leibniz terms when differentiating cutoffs. These are existing fixed finite 108 operations. The moment and filtered terms apply to the actual decorated input.

The bilinear amplitude/profile estimates give a continuous linear map on the corresponding completed projective tensor stage. At positive regulator its identity holds by continuity of evaluation. Continuous linear maps carry coefficient derivatives within each supplied 126 row. The actual identity preserves cross-row equality, including cancellations between source histories. The supports, cones, scalar stages, and finite history lists can stay fixed across the allowed graph-order relaxations.

Subtracting the actual two affine moment terms by 150 and UC025, then subtracting the whole UC013 filtered primitive, gives $Lh_1(1-C_2)V$ before quotient. At fixed mixed derivative of regulator order $k$, choose $t$ as the maximum of zero and the finitely many inherited negative Sobolev orders. The compact Green bound (150.6) is uniform in $H^{-t}$, and the differentiated conic heat multiplier costs at most $\epsilon^{-k}$ across the finite Leibniz sum. Input power $N+k$ gives output power $N$ with $t$ chosen before $N$. This bounds the whole evaluated difference and the rapid entry of each analytic/rapid equality graph. The actual identity supplies the matching analytic entry, giving descent through the original covers and 126 quotient.

## 5. Scope and source check

The proof depends on the fixed affine moving-delta relation and the stipulated relative profile. It reaches the retained collision even though the unsplit augmented graph has a forbidden all-equal direction there. General distributional integrated-block dependence, arbitrary coupled scalar stages paired with such graphs, and general hidden histories remain in the open universal 150.L obligation. Residual acyclicity, full parameter family recovery, and final integration remain open.

The mathematical Markdown gate uses the existing isolated Windows CHAD evidence interpreter with explicit UTF-8 mode and GCL caches outside the worktree. The environment is unpinned and no dependencies were installed. The gate checks source structure. The disposition above follows from the exact-source mathematical review.
