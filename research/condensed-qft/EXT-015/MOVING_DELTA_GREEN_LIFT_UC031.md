# EXT-015 REACH / UC031 — exact Green lift for the coupled moving delta

**Candidate result.** The moving delta allowed by UC028's hostile control has an exact Green-remainder representation through retained collision when its coupled relative factor is a fixed Schwartz profile with a fixed regulator power. In particular the original coupled Gaussian works, as does the output of a genuine two-edge Gaussian bridge with a smooth hidden-vertex coefficient. The construction uses two existing augmented histories for the unsplit cusp integral. The moment and filtered terms have their original admitted lifts. The original rapid relation is preserved. Universal 150.L remains open.

## 1. Original input, output and density

Use ZFC, the real liquid heart for fixed $0<p\leq1$, and the given physical interval $U$ containing 0. The source class is the actual 105/108 finite image of completed mixed stages and the family rule of 126. Use the compact Green operator $h_1$, affine moment operator $B_1$, and filtered $C_2$ of [150](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) and [UC013](FILTERED_COMPACT_GREEN_SOURCE_UC013.md). Set $e(t)=|t|/2$. Cutoffs have fixed compact support inside the indicated physical intervals. All coordinate pushforwards use physical coordinate densities, after absorbing any fixed history density as a smooth multiplier.

In independent old retained blocks $(u,c)$ take the admitted history

$$
V_\epsilon(u,c)=a_\epsilon(u,c)\delta(u+c)\,\epsilon^\nu \rho((u-c)/\epsilon),
\qquad
\nu\in\mathbb Z,\quad \rho\in\mathcal S(\mathbb R;\mathbb R),
\tag{UC31.1}
$$

with $a$ smooth jointly through the regulator endpoint, on fixed compact support. Regulator-independent smooth cutoffs are included. The delta has covector proportional to $(1,1)$. All collision conormals have zero total covector. Thus the moving delta times the fixed graph cutoff which is one on the amplitude support is in one complete original graph stage. The relative scalar factor is smooth for positive regulator. On the pair heat front it is a fixed scaled Schwartz function times $\epsilon^\nu$, and at the strict-face corners the Schwartz bounds absorb every finite power from physical and regulator derivatives. This gives the original fixed scalar stage, also uniformly for bounded sets of $\rho$ and $a$. In particular $\kappa_{\sigma\epsilon}(u-c)$ has $\nu=-1$ and $\rho=\kappa_\sigma$ for fixed $\sigma>0$. A finite product of scaled Gaussian and Wick factors on this difference, with at least one Gaussian factor and fixed derivative orders, has the same form whenever all the other profiles and their derivatives grow at most polynomially. The original model's fixed Wick profiles and their fixed derivatives have this growth by their Gaussian convolution formula.

At fixed $c$, the integrated variable is $u$, and $d(u+c)/du=1$. For a fixed smooth output cutoff $L$ put $A_\epsilon(x,c)=L(x,c)a_\epsilon(-c,c)$, using smooth zero extensions as needed. Direct distributional evaluation gives

$$
L(x,c)(e*_1 V_\epsilon)(x,c)
=A_\epsilon(x,c)\,e(x+c)\,\epsilon^\nu \rho(-2c/\epsilon).
\tag{UC31.2}
$$

The multiplication and pushforward are well-defined at each positive regulator. For the only nondifferentiated cusp in this formula, the expanded conormal to $x=u$ has a nonzero $x$ covector, whereas the delta in $u+c$ has $x$ covector zero. Equivalently first pair the cusp against the smooth compact output test in $x$, so the remaining function of $u$ is smooth and may be tested against the delta. There is no determinant from the midpoint in (UC31.2).

## 2. A fixed graph cone split at the retained midpoint

Write $m=(x+c)/2$ and introduce a dummy coordinate $y$. As in the conic point construction of [corrected 195](JOINT_DEFECT_SOURCE_AUDIT_195.md), start with the fixed plane distribution $W(r,y)=e(r)\delta_0(y)$. Use the Fourier convention with phase $-i(r\xi+y\eta)$. Choose a real even smooth angular cutoff $Q$ equal to 1 near both rays $\eta=-\xi$ and supported where $0<c_0|\xi|\le|\eta|\le C_0|\xi|$ for constants $c_0,C_0>0$. Let $q$ be this cutoff times a smooth radial cutoff zero near the origin and equal to 1 for radius at least two. Put

$$
W_b=q(D)W,\qquad W_g=W-W_b,\qquad
\widehat W_b(\xi,\eta)=-q(\xi,\eta)/\xi^2 .
\tag{UC31.3}
$$

The last formula follows from $e''=\delta_0$ since the cutoff kills the extension at $\xi=0$. Frequency integration by parts makes $W_b$ smooth off the plane origin. At that point $W_g$ has no wavefront in a fixed smaller neighborhood of $\eta=-\xi$, as follows from the vanishing high-frequency symbol of $1-q(D)$ there. Elsewhere the wavefront of $W_g$ is the original pure $y$ direction of the delta.

Pull back $W_g$ by the submersion $(x,c,y)\mapsto(m,y)$. Its covectors are contained in those of the form $(\xi/2,\xi/2,\eta)$ with the two-variable exclusions just proved. For the three singleton partition the conormal is zero. For the partition joining $x$ to $c$, the remaining covector $\eta$ must vanish and the sum on the joined block is $\xi$, so the intersection is zero. For a pair involving $y$ and one retained slot, the other retained slot forces $\xi=0$ and then the sum on the pair forces $\eta=0$. For the all-equal partition the only forbidden direction has $\xi+\eta=0$. This ray is excluded when $m=y=0$, and at any other point of the graph singular support the covector is pure $y$ and has nonzero total sum. The cone exclusion has a fixed closed separation after multiplication by compact smooth cutoffs. The graph remains admissible even when all three vertices coincide. This is the reason for using the midpoint in the coefficient, without changing the actual spectator $c$ in the physical pushforward.

Fix $\theta\in C_c^\infty(U)$ equal to 1 near 0. Put $K(t)=\rho(-2t)$ and $k_\epsilon(t)=\epsilon^{-1}K(t/\epsilon)$. Define the scalar distributional integral

$$
J_\epsilon(r,s)=\int k_\epsilon(s-y)\theta(y)W_b(r,y)\,dy .
\tag{UC31.4}
$$

The next section shows that $J$ is an admissible scalar after its specified midpoint substitution.

## 3. Scalar heat estimates for the discarded graph directions

The split (UC31.3) is the one used in 195, but here the partial smoothing allows any fixed Schwartz kernel $K$ and must pass through the different relative coordinate map of section 4. The needed statement is that $J$ is smooth for $\epsilon>0$ and has a smooth-plus-logarithm lift on the single radial blowup of $\{\epsilon=r=s=0\}$ in $\{\epsilon\ge0\}$. Its strict face is smooth away from the radial corner, and the coefficient and all-order remainder maps are continuous in $K\in\mathcal S$. We verify the Schwartz extension and this precise radial version.

Let $H$ be the inverse Fourier transform of the radial finite-part extension of $-Q(\xi,\eta)/\xi^2$. In two frequency dimensions the radial pole is order one in the integral $dR/R$. Subtracting the value of the test at frequency zero near $R=0$ gives the finite part. The scaling defect is a multiple of the delta at frequency zero. Thus $H(\lambda z)=H(z)+b_0\log\lambda$ with a fixed real constant $b_0$, where $z=(r,y)$ and $\lambda>0$. Frequency integration by parts makes $H$ smooth away from zero. Its physical form there is a smooth angular term plus $b_0\log|z|$, hence locally integrable. The difference $W_b-H$ has smooth inverse transform because the difference of the Fourier distributions is compactly supported. Every fixed derivative grows at most polynomially. Consequently $\theta W_b=H+G$, with $G=(\theta-1)H+\theta(W_b-H)$ smooth everywhere and with all its derivatives of polynomial growth in $y$ on compact $r$ sets. Its contribution to (UC31.4) is the smooth family through zero

$$
\int K(Y)G(r,s-\epsilon Y)\,dY .
$$

Fixed joint derivatives are bounded by finitely many Schwartz seminorms, by differentiating under the integral. This is ordinary smoothness on compact physical sets and gives all heat corner Taylor bounds for this part.

For $H_\epsilon=k_\epsilon*_y H$, frequency multiplication is by $\widehat K(\epsilon\eta)$. On the high-frequency cone, $|\eta|$ bounds a positive fixed multiple of $|(\xi,\eta)|$. Every specified physical and regulator derivative is integrable at infinity using sufficiently many Schwartz seminorms of $K$. The compact low-frequency finite part acts on smooth functions, with finitely many derivatives. This proves smoothness at positive regulator and fixed polynomial upper bounds in $\epsilon^{-1}$ for every differentiated norm on compact physical sets. The possible borderline logarithm is included in such bounds. The scale identity, with $M_K=\int K(Y)\,dY$, is exact:

$$
H_\epsilon(\lambda r,\lambda s)
=\bigl(k_{\epsilon/\lambda}*_y H\bigr)(r,s)+b_0M_K\log\lambda .
\tag{UC31.5}
$$

It gives smooth front coordinates $(r/\epsilon,s/\epsilon)$ on compact central front charts, plus a single logarithm.

For the strict face use any fixed physical annulus in $(r,s)$ away from zero, and a smooth cutoff $\vartheta(r,y)$ equal to 1 near the origin and supported in a sufficiently small point neighborhood compared with the annulus. The actual contribution of $(1-\vartheta)H$ is smooth through zero by the same argument as $G$. For the remaining contribution of $\vartheta H$, where $r$ is outside the point support the integral is zero. Where $r$ lies on that support and the output is on the annulus, $s-y$ is bounded away from zero. Each mixed derivative of the scaled Schwartz multiplier is then $O(\epsilon^N)$ for every chosen $N$, in each fixed finite physical test norm. Compact support gives one finite negative Sobolev order for each regulator derivative independently of $N$. Thus this actual separated contribution is rapidly small in that finite order. It has moderate positive Sobolev norms by subtracting the actual smooth part from the already moderately bounded whole $H_\epsilon$. On a slightly larger annulus, interpolation with such a positive order and Sobolev embedding give arbitrarily rapid bounds in every fixed differentiated $C^j$ norm on the smaller annulus. The constants are bounded by finite combinations of Schwartz seminorms. The resulting actual smooth strict-face extension includes the separated part, extended flatly. No finite Taylor polynomial replaces either part.

At a radial/strict corner use $\lambda=|(r,s)|$, $\omega=(r,s)/\lambda$ and $\sigma=\epsilon/\lambda$. Formula (UC31.5) is $H_\sigma(\omega)+b_0M_K\log\lambda$. The preceding strict estimate holds on the entire angular circle, including all angular derivatives and all ordinary derivatives in $\sigma$. Taylor's theorem in the fixed smooth corner coordinates supplies the complete recursive remainder estimates. This proves the claimed form on the single radial blowup. The argument retains the actual family even when $M_K=0$, in which case the displayed logarithm vanishes. It is not an identification by moments.

## 4. Exact evaluation by two existing histories

The good history uses the independent physical vertices $(x,c,y)$, the identity partition and no insertion derivatives, retaining $(x,c)$ and forgetting $y$. Its graph factor is $\theta(y)W_g(m,y)$ with fixed compact $x,c$ cutoffs equal to 1 on the needed support. Its scalar factor is $2A_\epsilon(x,c)\epsilon^{\nu+1} k_\epsilon(c-y)$. This scalar is a pullback of a single relative Schwartz stage by forgetting vertices, times the permitted power and smooth multipliers. Its graph cone is exactly the one checked in section 2.

The bad history uses independent physical vertices $(x,c,h)$ and the graph coefficient $\delta_0(h)$ with fixed compact spectator cutoffs equal to 1 where needed. Its only nonzero wavefront component is the $h$ covector, so every partition conormal is excluded. Use the scalar factor

$$
2A_\epsilon(x,c)\epsilon^{\nu+1}
J_\epsilon\left(\frac{(x-h)+(c-h)}{2},c-h\right)
\tag{UC31.6}
$$

with fixed smooth compact support localization. This is a scalar on the original three-vertex heat space. In the relative coordinates $(x-h,c-h)$ the displayed map is an invertible linear map of the two relative coordinates. It identifies the full radial center with the radial center of section 3 and lifts to a smooth diffeomorphism of the full radial blowups; at the corner it changes radial and angular variables by smooth positive units and a smooth angular diffeomorphism. The stage already has an arbitrary smooth angular strict expansion there. The three additional pair-collision blowups on the source act on this smooth lift and on the monomial/logarithmic factors. Near the full front each such blowup uses a strict-face variable and one smooth angular coordinate as normal variables, leaving the full radial variable passive. Away from it, the ordinary strict extension is smooth. Thus the simple radial proof suffices even though the midpoint map does not preserve all pair-collision lines. It is unnecessary to assert a b-map into a full collision space in the midpoint coordinates. One fixed scalar index family is the nonnegative integers with log degree at most one before multiplying by $\epsilon^{\nu+1}$, with fixed lower auxiliary weights below the leading orders. The power has its actual fixed face shifts and every requested finite ordinary derivative has its finite additional shifts as in 105. The smooth angular expansion and radial logarithm give all recursive seminorms, using the same scalar stage for all Schwartz coefficients with fixed $\nu$ and support data.

Both histories use ordinary coordinate pushforward without a midpoint coordinate change in the fibre density. The bad one forgets $h$ with the unit delta pairing. Its output is $2A_\epsilon\epsilon^{\nu+1}J_\epsilon(m,c)$. The sum with the good one therefore equals

$$
2A_\epsilon(x,c)\epsilon^{\nu+1}
\int k_\epsilon(c-y)\theta(y)\bigl(W_g+W_b\bigr)(m,y)\,dy
=2A_\epsilon(x,c)\epsilon^{\nu+1}k_\epsilon(c)e(m)
=A_\epsilon(x,c)\epsilon^\nu\rho(-2c/\epsilon)e(x+c).
\tag{UC31.7}
$$

This is precisely (UC31.2), including the sign of the possibly noneven profile. For a Gaussian, $k_\epsilon=\tfrac12\kappa_{\sigma\epsilon/2}$ and this half cancels the prefactor two. This equality keeps all low-frequency corrections and the full regulator dependence.

## 5. A hidden bridge and fixed finite decorations

For a concrete three-block original input add a forgotten physical vertex $d$ with a smooth compact amplitude $a_\epsilon(u,c,d)$ multiplying $\delta(u+c)$. Use the genuine two-edge scalar $\kappa_{\sigma_1\epsilon}(u-d)\kappa_{\sigma_2\epsilon}(d-c)$ with fixed positive widths. The graph coefficient still has only a nonzero-total $(1,1,0)$ covector. Put $S=\sigma_1^2+\sigma_2^2$, $\mu=(\sigma_2^2u+\sigma_1^2c)/S$, and $b=\sigma_1\sigma_2/\sqrt S$. Completing the square with the actual $dd$ density gives

$$
\kappa_{\sigma_1\epsilon}(u-d)\kappa_{\sigma_2\epsilon}(d-c)
=\kappa_{\sqrt S\,\epsilon}(u-c)\kappa_{b\epsilon}(d-\mu).
$$

The normalization is exact because $\sqrt S\,b=\sigma_1\sigma_2$. After proper forgetting of $d$ the new amplitude is $\int\kappa_1(Y)a_\epsilon(u,c,\mu+b\epsilon Y)\,dY$. Extension of the smooth compact original amplitude and the Gaussian moments prove joint smoothness through zero and all derivative estimates on fixed physical and parameter compact sets. Thus this admitted hidden history is included in (UC31.1), with no residual error. Both edges can participate in the same physical collision.

All fixed finite retained derivatives commute with the unnormalized compact Green convolution in their corresponding output variables. Fixed derivatives of the moving delta can also be included. Pair with the smooth output test first, then its integration by parts in $u$ gives a finite list of cusp derivatives at $x+c$, smooth amplitude derivatives on $u=-c$, and fixed derivatives of the relative profile. A differentiated relative profile is still Schwartz with the corresponding regulator shift. The cusp derivatives may equivalently be taken by output $\partial_x$ on the exact representation, with the finite Leibniz expansion for cutoffs. Choose cutoffs equal to one on a neighborhood of the needed support before differentiating. This uses only existing finite output decorations and admits their actual signs and derivatives, without varying derivative order with rapidness.

As a genuine singular control, on a box with amplitude one the output retains the cusp on $x+c=0$ at each positive regulator. The forbidden all-equal direction would be present in the unsplit augmented graph at the origin. For the Gaussian the output under $x=\epsilon X$, $c=\epsilon C$ has the nonzero profile $e(X+C)\kappa_\sigma(2C)$, including at $X=C\ne0$ within the scaled box. With nonnegative smooth physical test bumps equal to one near the origin in $c$ and nonzero near it in $x$, its positive fixed-test limit is one half of the integral of $e(x)$ times the $x$ bump, times the test and amplitude values along $c=0$. For the stated unit patch these may be chosen nonnegative and the limit is strictly positive. This checks the unit delta density and rules out treating the cusp core as a negligible error. It is a control on the unnormalized convolution, before the affine and filtered corrections.

## 6. Complete sources, original rapid quotient, and scope

The graph factors in the two histories are fixed. Smooth multiplier maps and the estimates in section 3 give continuous maps of amplitude and Schwartz profile into a fixed completed scalar stage by the projective seminorms. Finite derivatives and the hidden integration use their actual finite seminorm bounds. Fixed compact support, graph cone, indices, auxiliary weights and finite histories suffice for supplied rows formed in these spaces; all finite parameter differentiations commute with these maps, and compatible graph-order relaxations leave the scalar data unchanged. This covers profinite stage maps and the actual source-controlled smooth families of these inputs, with equality descending through evaluation on the original covers. It asserts no recovery theorem for arbitrary parameter families.

The two affine moment terms have their admitted 150/UC025 lifts, and UC013 supplies the full $h_1C_2$ contribution on the original source. Subtracting the latter and including the actual signed moment corrections gives $Lh_1(1-C_2)V$ using existing sources. Because the identities are actual at positive regulator, they preserve equality under different source presentations. To check the original negligible-error rule on evaluated inputs, use the compact Green bound of 150.6 and the derivatives of the existing conic heat multiplier. For a prescribed mixed parameter and regulator derivative of regulator order $k$, take the maximum of the finitely many involved input negative Sobolev orders. Choose it before the requested rapid power $N$. The heat derivatives cost at most $\epsilon^{-k}$, so input power $N+k$ suffices. These are bounds on the actual full operation and respect all input cancellations, with no heat-defect truncation.

The original moving-delta case and the admitted Gaussian bridge above have exact representations through the collision. The theorem uses the fixed affine delta relation and the stipulated relative profile form for its evaluation. Arbitrary distributional dependence in the integrated block, arbitrary coupled scalar stages and all hidden histories in 150.L still require a general argument. It follows neither that they all admit a lift nor that a failure of the coordinate split excludes membership.

**Custody.** Protected scientific input 05771e70b4fa5f23e8df0bdd5d30bbe7c982cf3f on research/reach-moving-delta-uc031-input-20261121. CP264 preceded candidate construction. The corrected 195 source is frozen input blob fc0fddb678f0cc0c1b9764bb449ab6d9150b33d0. The actual two-piece scalar proof above uses its finite-part decomposition and adds the Schwartz kernel and midpoint pullback estimates. The present result awaits distinct exact-source review and protected admission.
