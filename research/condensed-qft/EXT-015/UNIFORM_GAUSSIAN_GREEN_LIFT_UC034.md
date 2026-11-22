# EXT-015 REACH / UC034 — the whole-stage Green lift for one Gaussian edge

**Candidate result.** For a fixed Gaussian edge joining the integrated retained vertex to the other retained vertex, the entire localized compact Green remainder has a continuous exact lift on each original complete two-vertex graph stage. Two fixed existing histories represent its unnormalized cusp integral. This includes arbitrary graph coefficients on that stage, at the retained collision and with the original rapid relation. The full 150.L for freely coupled scalars and general hidden histories is a separate obligation.

## 1. Exact interface

Work on the original physical interval $U$ in ZFC in the real liquid heart for fixed $0<p\le1$. Use 105.5 scalar stages, [108.1 and 108.6–7](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md), the supplied parameter rows of [126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md), and the original compact operators of [150](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) and [UC013](FILTERED_COMPACT_GREEN_SOURCE_UC013.md).

Fix one admissible complete input $E_{s,K,\Gamma}$ on the distinct block coordinates $(u,c)$, with $K\Subset U^2$ and $\Gamma$ avoiding every physical partition conormal. Here $u$ is integrated and $c$ is retained. Fix a compact smooth output cutoff $L(x,c)$ and put $V_\epsilon(u,c)=\kappa_\epsilon(u-c)T(u,c)$, with the original normalized unit-width Gaussian. The density is $du\,dc$ after the usual fixed density absorption. The target is $Lh_1(1-C_2)V$. Label exchange gives the other operator with the same proof. A fixed finite coordinate derivative or cutoff in the original input can be transferred by the finite Leibniz rule when the resulting integral kernels keep the fixed Gaussian or its fixed physical derivatives. The basic theorem uses the Gaussian itself.

We construct $L(e*_1V)$, where $e(t)=|t|/2$. The two affine moment terms have the admitted 150 and UC025 lifts. The whole filtered primitive $Lh_1C_2V$ has the UC013 lift on the original source. All cutoffs are fixed before a coefficient is chosen. Choose $\theta\in C_c^\infty(U)$ equal to one on neighborhoods of the old $u$ support and the $c$ projection of the support of $L$. Choose a smooth compact difference cutoff $\varphi$ equal to one near zero and on every relevant difference of the old $u$ support and the $x$ projection of that support. Set $k(t)=\varphi(t)e(t)$. Then the exact cusp integral is

$$
L(x,c)\int \theta(u)\kappa_\epsilon(u-c)W_T(x-u,u,c)\,du,
\qquad W_T(t,u,c)=k(t)T(u,c).
\tag{UC34.1}
$$

All intermediate products and integrals can be taken in distributions after extension by zero off the fixed compact supports. The coordinate change $t=x-u$ has unit absolute determinant.

## 2. Fixed conic split and the good history

Use Fourier variables $(\tau,\alpha,\beta)$ dual to $(t,u,c)$ and the convention of UC031. Choose $q$ real, smooth, even, zero near the origin and equal to its angular part outside a ball. The angular part is one on an open conic neighborhood of the two $\tau$ axes, and supported where $|(\alpha,\beta)|\le|\tau|/4$. Write

$$
W_T^{\mathrm b}=q(D)W_T,\qquad
W_T^{\mathrm g}=(1-q(D))W_T .
\tag{UC34.2}
$$

Under $(t,u,c)=(x-u,u,c)$ a possible covector from the original tensor wavefront is $(\tau,\alpha-\tau,\beta)$. A nonzero $\tau$ requires $x=u$. If this covector were conormal to an augmented partition, join its $x$ and $u$ blocks, which have the same physical value. The covector sums remain zero since the two old sums are zero. Delete $x$ after restoring $\alpha$ in the $u$ slot. The covector induced on the original blocks is $(\alpha,\beta)$ with sum zero on each of the resulting blocks. If it is nonzero, this contradicts $\Gamma$. If $\tau=0$, deleting the zero $x$ slot gives the same contradiction directly. The entire forbidden intersection is therefore confined to the two $\tau$ axes. The multiplier $1-q$ removes both in a fixed open cone at high frequencies.

The tensor wavefront bound, the fixed angular multiplier exclusion and multiplication by smooth compact cutoffs give one closed permitted cone for the localized pullback of $W_T^{\mathrm g}$. For the tensor use the full product cone including the zero directions in each factor. For the angular exclusion, localization convolves the Fourier transform with a Schwartz function, which is rapidly decreasing in any smaller cone separated from the high-frequency support. On compact supports the pullback and cutoff preserve a finite global $H^{-s'}$ norm: for $s'\ge\max(s,0)$ the tensor estimate follows from $\widehat k\in L^2$ and the product Fourier weight, and the fixed order-zero multiplier, invertible linear change and cutoff are bounded at that order. The complete graph map is continuous. Indeed its closed graph follows from the distributional identity and continuity of the same operations on compactly supported distributions into distributions. The input and restricted-support output graph spaces are Fréchet. Equivalently use the fixed-factor tensor estimate in the normal topology. [Brouder–Dang–Hélein, normal distribution topology](https://arxiv.org/abs/1409.7662)

Take this compactly localized good coefficient as the graph factor on $(x,u,c)$. Choose the graph cutoffs equal to one on the supports needed for $L$ and $\theta$. Multiply by the scalar $L(x,c)\theta(u)\kappa_\epsilon(u-c)$ and properly forget $u$. This is the first existing history. Its compact geometry and cone are fixed across graph-order refinements.

## 3. The removed cone is one scalar on four vertices

Use new genuine physical copies $(a,b)$ for the two input vertices. Let

$$
z=(x-c,c-a,c-b),\qquad
P(\tau,\alpha,\beta)=q(\tau,\alpha,\beta)\widehat k(\tau).
$$

With the $u$ window temporarily replaced by one, the kernel to be tested against $T(a,b)$ is the ordinary inverse Fourier integral

$$
F_\epsilon(z)=(2\pi)^{-3}
\int_{\mathbb R^3} e^{iz\cdot(\tau,\alpha,\beta)}
P(\tau,\alpha,\beta)e^{-\epsilon^2(\alpha-\tau)^2/2}
\,d\tau\,d\alpha\,d\beta .
\tag{UC34.3}
$$

In fact the phase before integration is $\tau(x-u)+\alpha(u-a)+\beta(c-b)$. Set $u=c+r$. The $r$ integration against $\kappa_\epsilon(r)$ gives the displayed Gaussian multiplier exactly, including its normalization. There is no determinant in the physical $du$ pairing. The relative arguments in $z$ have full rank three, and their zero set is exactly the four-vertex total collision.

Here are the complete scalar bounds for this integral. On the support of $q$ the linear form $\alpha-\tau$ bounds a positive multiple of the full frequency norm. Also $k''=\delta_0+g$ with $g$ smooth compactly supported. Thus $P=-q/\tau^2$ plus a Schwartz symbol on this cone. There is exactly one homogeneous term of degree $-2$, with the high-frequency cutoff. In frequency dimension three its extension $p=-q_{\rm ang}/\tau^2$ is locally integrable at zero. The Fourier difference $P-p$ is the sum of a compact-frequency integrable distribution and a rapidly decreasing symbol. Its heat kernel is jointly smooth through zero with all derivative bounds on compact physical sets. The homogeneous part has the exact radial form

$$
\rho^{-1}F_*\bigl(\epsilon/\rho,z/\rho\bigr),\qquad
\rho=(\epsilon^2+|z|^2)^{1/2}.
\tag{UC34.4}
$$

For the angular coefficient $F_*$, near $\epsilon/\rho>0$ absolute Gaussian convergence suffices. At the strict corner $|z/\rho|$ is bounded below. With a fixed frequency cutoff around zero, its low-frequency integral is smooth by local integrability. For the remaining oscillatory integral, each heat-parameter derivative of order $j$ and frequency derivative of order $l$ of the angular symbol times the heat factor is bounded by $C_{j,l}|\omega|^{-2+j-l}$ at high frequency, uniformly for the normalized heat parameter in $[0,1]$. This follows by absorbing bounded powers of the normalized parameter times frequency into the Gaussian on its fixed support cone. After any requested angular derivative, integrate by parts in frequency along the normalized physical direction until the resulting majorant is integrable in dimension three. The denominators are smooth and bounded since that direction has norm bounded below. Dominated convergence gives every differentiated strict extension. This proves (UC34.4) with smooth compact-hemisphere coefficients, including the strict endpoint. The ordinary jointly smooth difference contributes Taylor coefficients and all their derivative bounds. These are the dimension-three instance of the calculation in UC013 §2, with no radial logarithm for this homogeneous degree.

Restore the original window without an asymptotic substitution. For $c$ on a fixed neighborhood of the relevant compact projection, define

$$
g_{\epsilon,c}(r)=(1-\theta(c+r))\kappa_\epsilon(r).
$$

Every Schwartz seminorm of $g_{\epsilon,c}$, including any fixed number of $c$ and regulator derivatives, is $O(\epsilon^N)$ for every $N$, uniformly on that neighborhood. Its nonzero support stays a fixed positive distance from $r=0$. Replace the heat factor in (UC34.3) by $\widehat g_{\epsilon,c}(\tau-\alpha)$ to obtain exactly the omitted tail kernel. Because $\tau-\alpha$ bounds full frequency on the cone, its Schwartz seminorm estimates absorb every frequency factor arising from any fixed physical derivatives. Integrating in the three frequencies shows that the tail is jointly smooth and flat through $\epsilon=0$, in each fixed physical and regulator derivative norm. In a compact scalar support cutoff this is an existing smooth-through-zero scalar. Subtract this actual kernel from (UC34.3). The resulting $\widetilde F_\epsilon(x,c,a,b)$ keeps the exact $\theta$ window in (UC34.1).

For the target scalar stage apply the partition principalization of [UC013 §4](FILTERED_COMPACT_GREEN_SOURCE_UC013.md) to $(\epsilon,z)$. The total diagonal is a center of the full original arrangement. Blowing up it and the other partition centers factors $\rho$ as a positive smooth unit times a product of boundary defining functions $r_G^{a_G}$. In charts where smaller centers have already been blown up, their radial factors are extracted first. Intersecting centers separate after their common intersection is blown up. The normalized angular coordinates in (UC34.4) are smooth in the resulting charts. Thus (UC34.4) and the smooth terms lie in one fixed scalar stage with, for example, integer index sets bounded below by $-a_G$ and auxiliary weights $-a_G-1$. Taylor expansion of the smooth unit and hemisphere coefficients, including along the strict corner, gives compatible recursive remainder bounds at every face. This uses the complete original heat arrangement on four physical vertices, not a new collision center. The exact flat tail and all fixed smooth cutoffs are included in this same stage.

For the second history use $T(a,b)$ with a fixed compact smooth singleton factor in each of $x,c$, the scalar $L(x,c)\widetilde F_\epsilon(x,c,a,b)$ with fixed compact support cutoffs, and forget $a,b$. Adding zero covectors in the output slots preserves partition-conormal exclusion by deleting those slots from any tested partition. The cutoffs are one on the relevant input and output supports. At positive regulator the integrated-frequency decay gives absolute convergence of the resulting Fourier pairing against $\widehat T(\alpha,\beta)$, which is of polynomial growth for compact $T$. Equivalently test (UC34.1) in $x,c$ first. Fourier inversion for that compact test gives the same kernel using the same window. This identifies the evaluation of the second history with exactly the removed-cone contribution in (UC34.1), for every $T$ on the graph stage. In particular no pointwise replacement of $T$ or expansion in its relative Fourier modes is used.

## 4. Uniformity, hostile controls and rapid descent

The first history is the continuous graph map of section 2 tensored with a fixed scalar. The second is smooth singleton tensoring with a fixed scalar of section 3. These are continuous linear maps into a fixed finite sum of the complete projective sources. Their sum is (UC34.1) by the exact split. Include the existing affine moment terms and subtract the entire UC013 filtered primitive. This gives the target $Lh_1(1-C_2)$ on the whole complete graph stage. All coefficients and fixed finite source operations act in the same scalar stages under the supplied graph-order refinements. Actual equality gives compatibility across rows, including after parameter differentiation. On each profinite coefficient plot the maps are the continuous stage maps, and on original image sections one descends the equality on the allowed covers.

- **Motion and superposition.** In a fixed compact patch take $\eta(u,c)\delta(u+\lambda c-(1+\lambda)a)$ with $a$ in a compact interval and $1/2\le\lambda\le2$. Its covectors are positive multiples up to an overall sign of $(1,\lambda)$ and uniformly avoid the forbidden conormal. Each fixed parameter derivative of order $j$ is a finite sum of cutoff delta derivatives of order at most $j$ with smooth coefficients. The normal Fourier estimate in rotated coordinates gives a common $H^{-s_j}$ bound for $s_j>j+1/2$, and every off-cone request has the usual rapid Fourier bound with a uniform angular gap. Hence bounded signed measures on the compact parameter rectangle give bounded superpositions in the same stage for $j=0$. The construction commutes with their integrals by testing and continuity. Prescribed derivatives use those same geometric and scalar output data at their relaxed graph orders. Direct evaluation gives the cusp $e(x+\lambda c-(1+\lambda)a)$ times the Gaussian at $(1+\lambda)(a-c)$ and the pulled-back amplitude. Its unit fibre Jacobian is the UC031 one at $\lambda=1,a=0$.
- **Joint high frequencies.** On the removed cone, even when $|\omega|$ has order $\epsilon^{-1}$ and the old frequencies are a fixed nonzero fraction of $|\tau|$, the bound $|\alpha-\tau|\ge3|\tau|/4$ holds. The scaled front integral and its derivatives are controlled by the same majorants on this region. High frequencies of $T$ are paired in the appended physical graph coefficient. No decay in an isolated relative mode as in the false 150.12–14 estimate is needed. The two histories recombine before comparing coefficients or taking limits.
- **Nonzero heat defect and cancellation.** The UC016 Gaussian control has a nonzero finite-order heat defect. This construction includes it exactly by subtracting the whole filtered primitive, rather than suppressing its first nonzero coefficient. Equivalent scalar allocations give the same full positive family and hence the same output. On each fixed support, use an input flat multiplier such as $\exp(-1/\epsilon^2)$ as a direct rapid control. The same conclusion for differences or cancellation between entire source presentations follows from the following actual-family estimate.

For mixed parameter and regulator derivative of regulator order $j$, use 150.6 and UC16.12. The differentiated filter costs at most $\epsilon^{-j}$ across the finite Leibniz sum. Take the maximum of the finitely many involved input negative Sobolev orders before choosing the desired output power $N$. The input power $N+j$ suffices. The bounds are uniform on compact parameter sets, and test actual evaluated differences, so no order is varied with $N$. The operation therefore descends on the original rapid equivalence relation and on the analytic and rapid equality witnesses in the supplied 126 rows.

## 5. Claims and custody

The new mechanism is the joint conic split followed by exact Fourier transfer of the removed part to a scalar on physical input and output copies. It makes a linear source lift on every original complete two-vertex graph stage for the fixed Gaussian edge. It uses the relative collision geometry and does not require the extra smooth-slicing assumption of UC028 or the affine-delta factorization of UC031. Its off-diagonal restriction agrees with the already admitted evaluated map of UC025 by actual equality. The hidden-vertex extension is a separate stage after review of this proof. Universal 150.L, the residual cohomology, full parameter family recovery and final integration are not adjudicated by this theorem.

Scientific input dedb9534247758611acc216c1cd7cef4da329c17, retained ref research/reach-uniform-gaussian-uc034-input-20261121. CP267 was bound before this construction. The candidate is frozen for distinct nonauthor review.
