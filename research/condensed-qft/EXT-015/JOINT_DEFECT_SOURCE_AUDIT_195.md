# EXT-015 REACH / 195 — a conic source decomposition of the anchored cusp and its joint defect

**Primary disposition: POSITIVE SOURCE CONSTRUCTION, awaiting source-locked critical review196.** The first core $A$ has a finite representative in the existing completed105/108 source class. It is the sum of one original R1 Gaussian-bridge history and one relative scalar heat history with a single pure-anchor R1 delta. Consequently the full defect $D$ of192 also has an actual source, before the rapid quotient. The construction uses the admitted general fixed-index scalar polyhomogeneous enlargement. It does not assert a formula using only finitely many raw Gaussian/Wick factors, a general Green inverse, universal150.L, residual $W$ acyclicity, original R3, full126.14 or final REACH integration.

## 1. Frozen contract and the actual question

CP214 assigns this primary from exact input80e3288b06aacfa900e95e8f45f10b144952cf75 on `research/reach-joint-profile195-input-frozen-20261115`. That ref was resolved locally to this exact commit. The following actual source paths were read and compared with the frozen input; all were unchanged at the working checkout when construction began:

- protocol090, scalar105, completed mixed108 and source-controlled parameter126;
- the first/second core165, admitted second arm168, no-hidden171, hidden bridge174 and mixed-width180;
- canonical `NONPOLYNOMIAL_GAUSSIAN_SOURCE_AUDIT_186.md` and the distinct `DOUBLE_GAUSSIAN_HIDDEN_MEAN_SOURCE_186.md`;
- network energy189, zero-energy192, its critical193 and ledger194.

In particular105.5 admits actual smooth-interior scalar functions with fixed compatible all-face power/logarithmic expansions.108.6 completes mixed coefficients inside fixed stages, and108.7 takes the evaluated finite source image. The larger positive-scale auxiliary-noise envelope of105.2 is not substituted for this source class. No source operation or rapid relation is enlarged here.

Work in ZFC, real liquid modules for fixed $0<p\le1$, on the original interval $U$ containing0. Retain the fixed compact smooth cutoffs, with $\chi=1$ near0 and $\rho(0)\ne0$, and the normalizations

$$
e(r)=|r|/2,\qquad
\kappa_\epsilon(t)=(\sqrt{2\pi}\epsilon)^{-1}e^{-t^2/(2\epsilon^2)},\qquad
A_\epsilon(x,z)=\chi(x)e(x)\rho(z)\kappa_\epsilon(z).
\tag{195.1}
$$

For fixed $b>0$, the source-admitted smoothed core of192 is $\widetilde A_\epsilon=\chi(x)P_{b\epsilon}(x)\rho(z)\kappa_\epsilon(z)$, and the exact defect is

$$
D_\epsilon=\widetilde A_\epsilon-A_\epsilon.
\tag{195.2}
$$

The heat-width formula192.12 is a correct distributional identity. Its zero-width endpoint is nonsmooth at positive final regulator, and integration over a variable heat width is not a declared108 operation. We therefore do not treat that formula as a source. The new mechanism is instead a fixed conic decomposition of a distribution, followed by a direct all-corner proof for one actual scalar coefficient.

## 2. A fixed microlocal split with only one forbidden cone

Use two actual physical coordinates $(r,t)$, and put

$$
U(r,t)=e(r)\delta_0(t).
\tag{195.3}
$$

This distribution is not an R1 input. It is only the ambient distribution to be decomposed. Use the Fourier convention $\widehat f(\zeta)=\int e^{-iw\cdot\zeta}f(w)\,dw$, with inverse factor $(2\pi)^{-2}$ in two dimensions. Write $\zeta=(\xi,\eta)$. Choose one real smooth angular function $Q$, invariant under $\zeta\mapsto-\zeta$, equal to1 on a conic neighborhood of both forbidden rays $\eta=-\xi$, and supported in a slightly larger neighborhood satisfying

$$
0<c|\xi|\le |\eta|\le C|\xi|.
\tag{195.4}
$$

Choose a real radial cutoff $\psi$ equal to0 near0 and1 for radius at least2, and set $q(\xi,\eta)=\psi(|\zeta|)Q(\zeta/|\zeta|)$. Define the two fixed tempered distributions

$$
U_{\rm bad}=q(D)U,\qquad U_{\rm good}=U-U_{\rm bad}.
\tag{195.5}
$$

Since $e''=\delta_0$, the Fourier transform of $e$ equals $-\xi^{-2}$ away from $\xi=0$. Any distributional extension ambiguity at $\xi=0$ is killed by $q$, which vanishes on an open neighborhood of that axis. Thus the bad piece has the exact ordinary symbol

$$
\widehat U_{\rm bad}(\xi,\eta)=-\frac{q(\xi,\eta)}{\xi^2}.
\tag{195.6}
$$

It is a classical symbol of order $-2$ in two dimensions, supported in195.4. Integration by parts in frequency shows that $U_{\rm bad}$ is smooth away from $(r,t)=(0,0)$. At that point its wavefront lies in the closed bad cone. The high-frequency symbol of $1-q(D)$ vanishes on an open neighborhood of the forbidden rays. Consequently $U_{\rm good}$ has no nonzero $(\tau,-\tau)$ covector at $r=t=0$. Away from that point, the only singularities of $U$ occur at $t=0,r\ne0$, with pure $t$ covectors; the bad piece is smooth there. Those points are away from the physical diagonal $r=t$.

It follows that, for any fixed compact smooth cutoffs, the localized good piece is in an original R1 graph sector on the physical vertices $(r,t)$: its closed cone avoids the entire diagonal conormal, not just the two rays at one frequency. The conic separation is fixed before varying the regulator. The Fourier cutoff is used to choose this one R1 coefficient; no pseudodifferential operation on every mixed source is being asserted.

## 3. The scalar heat lemma, including the strict corner

Choose $\eta_0\in C_c^\infty(U)$ equal to1 near0. Define the actual function

$$
J_\epsilon(r,s)=\int_{\mathbb R}
\kappa_\epsilon(s-t)\eta_0(t)U_{\rm bad}(r,t)\,dt,
\qquad
B_\epsilon(r,s)=\chi(r)\rho(s)J_\epsilon(r,s).
\tag{195.7}
$$

The integral is a distributional partial convolution initially; the lemma proves that it is a scalar function for every $\epsilon>0$.

**Lemma195.1 (partial heat smoothing of this conic point symbol).** $B$ is smooth for positive regulator and belongs to one fixed complete105.5 scalar stage on the three-vertex relative heat collision space with differences $r=x-h$ and $s=z-h$. Its face indices can be chosen in the nonnegative integers with logarithmic degree at most1, enlarged by integer saturation, and with fixed auxiliary lower weights strictly below0. Every interior derivative, every b-derivative remainder and every recursive corner coefficient has the corresponding finite seminorm bound. Multiplication by smooth fixed-support parameter cutoffs gives continuous maps into this same stage.

**Proof.** First isolate the precise point singularity. The degree $-2$ angular symbol

$$
p_0(\xi,\eta)=-\frac{Q(\zeta/|\zeta|)}{\xi^2}
\quad (\zeta\ne0)
\tag{195.8}
$$

has a radial finite-part extension across frequency0: in polar coordinates subtract the value of the test at0 from its radial integral near0. The resulting logarithmic subtraction is a constant multiple of that value. Its inverse Fourier transform $H$ is associated homogeneous of degree0:

$$
H(\lambda r,\lambda t)=H(r,t)+c_0\log\lambda,
\qquad \lambda>0,
\tag{195.9}
$$

for one fixed real constant $c_0$. Away from the origin, frequency integration by parts proves smoothness of $H$ and all angular derivatives. Thus $H=c_0\log|(r,t)|+h((r,t)/|(r,t)|)$ there, with smooth angular $h$; this is locally integrable at0. Its high-frequency wavefront is still confined to195.4. The extension at frequency0 changes only smooth polynomial terms.

The Fourier difference between195.6 and this extension is compactly supported as a distribution in frequency. Its inverse $R=U_{\rm bad}-H$ is smooth, with polynomial growth for each fixed derivative. Hence

$$
\eta_0(t)U_{\rm bad}(r,t)=H(r,t)+G(r,t),
\quad
G=(\eta_0-1)H+\eta_0R.
\tag{195.10}
$$

Here $G$ is smooth everywhere: the factor $\eta_0-1$ vanishes on a neighborhood of the only singular point of $H$. Its derivatives have polynomial growth in $t$ on every compact $r$ set. Ordinary Gaussian Taylor estimates therefore make $\kappa_\epsilon*_tG$ a smooth family through $\epsilon=0$, with even heat Taylor coefficients and all differentiated remainders on compact physical sets. This part lifts smoothly to every collision blowup.

Consider $H_\epsilon=\kappa_\epsilon*_tH$. At high frequency its Fourier transform is $e^{-\epsilon^2\eta^2/2}p_0$. On195.4, $|\eta|$ is bounded below by a positive multiple of the whole frequency. Gaussian decay therefore makes every differentiated high-frequency integral absolutely convergent for $\epsilon>0$. The finite-part low-frequency term acts on a smooth integrand and is smooth as well. This proves positive-regulator scalar smoothness. It also proves, on each compact physical set, a finite inverse-regulator bound for every physical and regulator derivative: after differentiation, the radial high-frequency estimate is an integral of a fixed power of the radius times $e^{-c\epsilon^2|\zeta|^2}$. The borderline undifferentiated integral costs at most $|\log\epsilon|$, which is bounded by a fixed additional inverse power. The orders and powers may depend on the derivative request; they are finite and fixed for that request.

The front chart is especially simple. Gaussian mass one and195.9 give the exact equality

$$
H_\epsilon(\epsilon R_1,\epsilon S_1)
=F(R_1,S_1)+c_0\log\epsilon,
\qquad F=H_1\in C^\infty(\mathbb R^2).
\tag{195.11}
$$

Every fixed derivative of $F$ is bounded on a compact front chart by the preceding Fourier integral. No nonsmooth $|R_1|$ coefficient is inserted into the scalar stage. The logarithm is essential at the critical order $-2$ in dimension2 and is allowed by105.5.

We check the strict regulator face using two actual heat convolutions before taking any Taylor polynomial. Fix an output annulus $A=\{a_0\le |(r,s)|\le a_1\}$, with a slightly larger compact annulus for derivative estimates. Choose one fixed smooth point cutoff $\vartheta_0(r,t)$ equal to1 near the input origin and supported in $|(r,t)|<\delta_0$, where $\delta_0<a_0/10$. Define

$$
H_{\rm sm}=(1-\vartheta_0)H,\qquad
S_\epsilon=\kappa_\epsilon*_tH_{\rm sm},\qquad
Z_\epsilon=\kappa_\epsilon*_t(\vartheta_0H),\qquad
H_\epsilon=S_\epsilon+Z_\epsilon.
\tag{195.12a}
$$

The last equality is an exact equality of the two actual partial heat convolutions. The input $H_{\rm sm}$ is globally smooth and has polynomial growth in $t$, with every derivative, on each compact $r$ set. In particular $S_\epsilon$ is an actual smooth heat family through regulator zero. It is not its finite Taylor polynomial. With $K(Y)=(2\pi)^{-1/2}e^{-Y^2/2}$ its mixed derivatives are given by

$$
\partial_r^u\partial_s^v\partial_\epsilon^kS_\epsilon(r,s)
=\int_{\mathbb R}(-Y)^kK(Y)
\partial_r^u\partial_t^{v+k}H_{\rm sm}(r,s-\epsilon Y)\,dY.
\tag{195.12b}
$$

Polynomial growth and Gaussian moments justify every derivative and its continuous extension to $\epsilon=0$. The same argument works on an interval of signed $\epsilon$; the family is even because $K$ is even. At zero its even derivatives are $(2j)!\,\partial_s^{2j}H_{\rm sm}/(2^j j!)$ and its odd derivatives vanish. On a neighborhood of $A$, $H_{\rm sm}=H$. Thus the actual Taylor polynomial of $S_\epsilon$ there is

$$
T_N(\epsilon,r,s)=\sum_{j=0}^N\frac{\epsilon^{2j}}{2^j j!}
\partial_s^{2j}H(r,s).
\tag{195.12}
$$

The separated point contribution $Z_\epsilon$ is controlled independently. Where $|r|>2\delta_0$ it vanishes, since partial convolution does not change $r$. On the rest of $A$, $|s|$ is bounded below by a constant greater than $a_0/2$, whereas its input support has $|t|<\delta_0$. Thus $|s-t|\ge\delta>0$ uniformly wherever this contribution can be nonzero on $A$. After fixed annular localization, every mixed derivative of its Gaussian multiplier is bounded by a fixed inverse power of $\epsilon$ times $e^{-\delta^2/(4\epsilon^2)}$. The compact distribution $\vartheta_0H$ has a finite negative Sobolev order. Smooth multiplier estimates and the compact partial pushforward estimate therefore give, for each fixed regulator derivative $k$, one finite order $t_k$ such that

$$
\|\partial_\epsilon^kZ_\epsilon\|_{H^{-t_k}(A)}
\le C_{k,L}\epsilon^L\quad\text{for every }L.
\tag{195.12c}
$$

The order $t_k$ does not depend on $L$. The statement includes finite physical derivatives after their corresponding fixed order losses. Annular cutoff derivatives obey the same separation estimate. The compact-input and output cutoffs in this estimate are fixed.

For this same actual $Z_\epsilon$, polynomial positive-Sobolev bounds follow by subtracting the actual $S_\epsilon$ from the whole $H_\epsilon$ in195.12a. The whole family has those bounds by the conic Fourier calculation above, and195.12b bounds every positive norm of $S_\epsilon$ through zero on the annulus. The argument applies to each fixed regulator derivative. Interpolation of195.12c with a sufficiently high moderate positive norm, followed by Sobolev embedding, yields

$$
\|\partial_\epsilon^kZ_\epsilon\|_{C^m(A)}
\le C_{k,m,L}\epsilon^L\quad\text{for every }L.
\tag{195.12d}
$$

Only this separated point contribution is asserted rapid. The different object $S_\epsilon-T_N$ has a finite Taylor remainder. Taylor's theorem applied to195.12b and the even extension gives the combined uniform estimate

$$
\|\partial_\epsilon^k(H_\epsilon-T_N)\|_{C^m(A)}
\le C_{N,k,m}\epsilon^{2N+2-k}.
\tag{195.12e}
$$

For $k\le2N+2$ this is the differentiated even Taylor remainder plus195.12d. For $k>2N+2$ the right side is a weaker bound, obtained from bounded higher derivatives of $S_\epsilon$ and rapidness of $Z_\epsilon$. Deeper truncation supplies any requested finite ordinary derivative. Every physical derivative is covered by increasing $m$ in this same estimate. Finite products of $\epsilon\partial_\epsilon$ preserve its undifferentiated weight $\epsilon^{2N+2}$. The constants are uniform over the complete compact angular annulus, including $r=0,s\ne0$, and over bounded fixed-support smooth decorations. This supplies a smooth strict-face extension with all the differentiated asymptotic seminorms, rather than only pointwise coefficients.

Put $a=|(r,s)|$, $\omega=(r,s)/a$ and $\sigma=\epsilon/a$ at the front/strict corner. Equations195.9 and195.12 give

$$
H_\epsilon(a\omega)=c_0\log a+H_\sigma(\omega),
\qquad
H_\sigma(\omega)\sim
\sum_{j\ge0}\frac{\sigma^{2j}}{2^j j!}
\partial_s^{2j}H(\omega).
\tag{195.13}
$$

Write $\mathcal R_N(\sigma,\omega)=H_\sigma(\omega)-T_N(\sigma,\omega)$ on the unit angular annulus. The corrected estimate195.12e states explicitly that, for all fixed $k,\ell,\beta$,

$$
\sup_\omega\left|
\partial_\omega^\beta\partial_\sigma^k
(\sigma\partial_\sigma)^\ell\mathcal R_N
\right|
\le C_{N,k,\ell,\beta}\sigma^{2N+2-k}.
\tag{195.13a}
$$

The $c_0\log a$ term in195.13 is kept separately. The remainder and its heat coefficients are independent of $a$, so finite products of $a\partial_a$ add no loss there. Applied to the logarithm, they give $c_0$ or zero after the first derivative. At fixed physical $(r,s)$, ordinary regulator derivatives have their actual factors:

$$
\partial_\epsilon^k=a^{-k}\partial_\sigma^k,\qquad
\left|\partial_\epsilon^k\mathcal R_N(\epsilon/a,\omega)\right|
\le C a^{-k}\sigma^{2N+2-k}.
\tag{195.13b}
$$

They are not assigned unchanged scalar indices. Likewise an ordinary physical derivative at fixed $\epsilon$ is a finite $a^{-1}$ weighted combination of the controlled derivatives. For example, with $V_r,V_s$ the smooth tangential projections of the coordinate vectors onto the angular circle,

$$
\partial_r=a^{-1}\bigl[\omega_r(a\partial_a-\sigma\partial_\sigma)+V_r\bigr],\qquad
\partial_s=a^{-1}\bigl[\omega_s(a\partial_a-\sigma\partial_\sigma)+V_s\bigr].
\tag{195.13c}
$$

Repeated ordinary derivatives therefore introduce only their finite integer boundary-weight shifts. Smooth center variables remain passive. Smooth physical decorations have their ordinary Taylor expansions in $a$ with smooth angular and center coefficients. A remainder after order $M$ is bounded by $a^{M+1}$ under all the displayed b- and angular derivatives; multiplication by the retained logarithm gives at most $a^{M+1}(1+|\log a|)$. The already smooth heat term of $G$ in195.10 has a smooth pullback in the same charts. These observations include cutoff and center derivatives in the full corner bounds. They agree exactly with195.11 on the overlapping front chart, so the expansion concerns the actual heat-smoothed function and its flat tails.

We now carry these estimates through each remaining three-vertex partial face. The remaining relative pair-collision lines are $r=0$, $s=0$ and $r=s$ over $\epsilon=0$. Their angular directions are separated after the full-origin blowup. Near one such direction choose a smooth angular coordinate $v$ vanishing on that line. The additional center is $\{\sigma=v=0\}$, with $a$ and the physical center $h$ as passive variables. The two types of projective chart and the relevant vector fields are

$$
\begin{array}{lll}
\sigma=\tau,\quad v=\tau V:
&\tau\partial_\tau=\sigma\partial_\sigma+v\partial_v,
&\partial_V=\sigma\partial_v,\\
v=\pm\tau,\quad\sigma=\tau S:
&\tau\partial_\tau=\sigma\partial_\sigma+v\partial_v,
&S\partial_S=\sigma\partial_\sigma.
\end{array}
\tag{195.13d}
$$

All coefficients are bounded on compact projective charts; $a\partial_a$ and smooth center derivatives persist. In the first chart195.13a gives $\mathcal R_N=O(\tau^L)$, where $L=2N+2$, under every product of these new b-vector fields and $\partial_V$. Its coefficients $\sigma^{2j}c_j(v)$ become $\tau^{2j}c_j(\tau V)$, whose ordinary Taylor expansions in $\tau$ have smooth $V$ coefficients and uniformly bounded differentiated remainders. In the second chart the same remainder is $O(\tau^LS^L)$ under every product of $\tau\partial_\tau$ and $S\partial_S$. More precisely, an ordinary $S$ derivative of order $k$ satisfies the bound $O(\tau^LS^{L-k})$, because $\partial_S^k=\tau^k\partial_\sigma^k$ and195.13a applies. The finite terms become $\tau^{2j}S^{2j}c_j(\pm\tau)$. Taylor expansion of the smooth $c_j$ in $\tau$ gives all recursive new-face coefficients and remainders. For any prescribed finite depths at the new face $\tau=0$ and the lifted strict face $S=0$, take $L$ larger than both depths and Taylor expand the finite coefficient list far enough. The joint remainder then has the required weights at both faces; all its new b-derivatives obey the same weights. Thus the argument controls every recursive remainder seminorm, not only the leading angular coefficient.

Ordinary derivatives retain their finite poles in these further charts as well. In the first chart

$$
\partial_\epsilon=a^{-1}\tau^{-1}
(\tau\partial_\tau-V\partial_V),
\tag{195.13e}
$$

whereas in the second chart $\partial_\epsilon=a^{-1}\tau^{-1}\partial_S=a^{-1}\tau^{-1}S^{-1}(S\partial_S)$. Hence a fixed ordinary regulator derivative of order $k$ incurs its finite $a^{-k}$ factor and the corresponding finite $\tau^{-k}$ and, in the second chart, $S^{-k}$ weight shifts. Ordinary physical derivatives similarly have only the finite poles obtained from195.13c and these projective changes. The undifferentiated scalar has nonnegative integer indices; derivatives pass to the computed stages with these finite lower-index shifts, as required by105, rather than being claimed to preserve the same lower indices.

Away from the full origin the scalar is already smooth through the strict face by195.12e. The analogous partial blowups there consequently pull back a smooth function. At the full front the charts195.13d cover each remaining line direction separately, so no further unresolved intersection of pair directions is left. The only logarithm is the retained $c_0\log a$ (or its front-chart expression195.11); the additional blowups leave $a$ unchanged and do not create a higher logarithmic degree. A single common undifferentiated index family $E_H=\mathbb N_0\times\{0,1\}$ at every face, with the required downward logarithmic closure and integer saturation, contains all these coefficients. One may choose the fixed auxiliary lower-weight vector $\mathbf b=(-1)_H$ at every face, including recursive coefficient spaces; it lies strictly below every leading exponent and absorbs the degree-one logarithm. For each fixed ordinary derivative, its computed finite integer index shifts and a correspondingly lower fixed auxiliary vector give the required derivative stage. These choices are made once per stage, independently of truncation depth, Cauchy nets and parameters. Fixed compact center decorations and all their derivatives satisfy the same estimates. There is no affine or absolute-anchor blowup being added to the original three-vertex collision space.

Finally multiply by $\chi(r)\rho(s)$ and any fixed smooth physical cutoffs. Their full Taylor expansions and bounded derivatives preserve the stated saturated index family, with fixed lower auxiliary weights below0 to absorb logarithms. Each requested target coefficient/remainder seminorm uses finitely many derivatives of these cutoffs, the fixed Fourier symbol, and a finite collection of the estimates above. This supplies the claimed complete scalar stage and continuity in fixed-support smooth parameter cutoffs. $\square$

The partial heat integral in195.7 defines and verifies one scalar coefficient. It is not a new variable-width integration operation on arbitrary sources. Membership follows directly from105.5's existing definition of scalar stages; no appeal to the unrestricted auxiliary-noise image is made.

## 4. Two legal finite108 histories and exact physical densities

**Proposition195.2 (actual source of the first core).** $A\in\mathcal P_2$, with the original108.7 source class and rapid ideal unchanged.

**Good history.** On the three independent physical vertices $(x,z,y)$, use the identity partition, no insertion derivative, retain $(x,z)$ and properly forget $y$. Take the coefficient

$$
T_g(x,z,y)=\chi(x)\rho(z)\eta_0(y)U_{\rm good}(x,y)
\tag{195.14}
$$

and the scalar relative Gaussian $\kappa_\epsilon(z-y)$, with fixed smooth compact source decorations equal to1 on the coefficient support. This coefficient is compact. Its $(x,y)$ wavefront avoids the diagonal conormal by section2. Its $z$ covector is zero. A forbidden three-vertex partition conormal could then arise only from the $x=y$ block or the full coincident block with $\xi_x+\xi_y=0$; both have already been excluded. A partition joining $z$ to just one other vertex would require a nonzero $z$ covector or force all covectors to be zero. Thus195.14 belongs to one fixed permitted original R1 graph space, with a sufficiently large finite Sobolev order.

The raw relative Gaussian is an admitted105 scalar. The exact good output, with the ordinary $dx\,dz\,dy$ density, is

$$
A_{g,\epsilon}(x,z)=\chi(x)\rho(z)
\int\kappa_\epsilon(z-y)\eta_0(y)U_{\rm good}(x,y)\,dy.
\tag{195.15}
$$

There is no independent singular anchor multiplied into this R1 coefficient.

**Bad history.** On different three-vertex input coordinates $(x,z,h)$ use the identity partition, zero insertion derivative and proper forgetting of $h$. Choose compact smooth $\theta_x,\theta_z$ equal to1 on the supports of $\chi,\rho$, and a compact $\theta_h$ equal to1 near0. Use the original pure-anchor coefficient

$$
T_b(x,z,h)=\theta_x(x)\theta_z(z)\theta_h(h)\delta_0(h).
\tag{195.16}
$$

Its only nonzero covectors are in the $h$ slot, so it avoids every forbidden partial-partition conormal. Use scalar $B_\epsilon(x-h,z-h)$, with any additional compact physical cutoffs equal to1 on the required coefficient/output support. Lemma195.1 proves this scalar directly on the actual three-vertex relative heat space; it does not treat the absolute $z$ coordinate as a relative graph edge. The exact bad output is

$$
A_{b,\epsilon}(x,z)
=\int B_\epsilon(x-h,z-h)T_b(x,z,h)\,dh
=B_\epsilon(x,z).
\tag{195.17}
$$

The physical delta pairing has coefficient1. The differences $(x-h,z-h)$ are ordinary coordinates on the relative configuration with passive center $h$; there is no weighted-mean projection or unrecorded change-of-variable determinant. The fixed physical support makes both forgetting maps proper.

Add195.15 and195.17. Because $U_{\rm good}+U_{\rm bad}=e(x)\delta_0(y)$ and $\eta_0=1$ near0, the entire positive-regulator output is

$$
\begin{aligned}
A_{g,\epsilon}+A_{b,\epsilon}
&=\chi(x)\rho(z)\int\kappa_\epsilon(z-y)
\eta_0(y)\bigl(U_{\rm good}+U_{\rm bad}\bigr)(x,y)\,dy\\
&=\chi(x)e(x)\rho(z)\kappa_\epsilon(z)
=A_\epsilon.
\end{aligned}
\tag{195.18}
$$

This identity retains all smooth low-frequency and physical-cutoff corrections in195.7 and195.14. None is discarded as negligible. Each summand is one legal original108.7 history. This proves the proposition before passage to any quotient. $\square$

## 5. Completion, parameter rows and the full defect

The good coefficient lies in a fixed complete $E_{s,K,\Gamma_g}$ and its Gaussian lies in a fixed complete scalar stage. The bad coefficient lies in a fixed pure-anchor graph stage and its scalar lies in the fixed complete stage of Lemma195.1. Their two simple tensors therefore belong to a finite direct sum of the existing completed sources108.6. The geometric evaluations are the existing continuous maps108.7, with all proper densities retained. No approximation by escaping scalar indices, changing cones or growing insertion orders is required.

For smooth parameter variations of $\chi,\rho$ with common compact supports, keep $Q,\psi,\eta_0$ and all histories fixed. Multiplication of the fixed $U_{\rm good}$ by the smooth cutoff derivatives is continuous in the same R1 graph stage. Lemma195.1 supplies continuous scalar coefficient derivatives in the same fixed scalar stage for the bad history. Every finite parameter row can therefore be taken to be the actual coefficient derivatives of these two tensors. Regulator derivatives are those of the same entire evaluations. These are the coefficient-level within-row identities and entire-history cross-row identities of126.6, not output bounds asserted to lift afterwards. Finite joins and cover-local profinite plots use the original completed-source image maps and descent of actual test pairings. This supplies genuine source-controlled126 rows for this construction; it does not prove the missing recovery of all previously admitted families in126.14.

The source-admitted $\widetilde A$ of192 and195.18 now give

$$
D=\widetilde A-A\in\mathcal P_2.
\tag{195.19}
$$

Thus the exact nonsmooth joint profile $(P_b(X)-e(X))K(Z)$ is represented by a finite sum of existing completed sources. Its nonzero order-two test coefficient and failure of rapidness remain exactly those proved in192.13; source membership does not make it zero in the boundary. No infinite delta-jet series is used. Every equality defect in195.18 and195.19 is identically zero, and hence belongs to the unchanged fixed-order rapid ideal for every mixed derivative without an inverse-heat estimate.

## 6. Hostile controls and scientific boundary

| Potential failure | Control in this construction |
| --- | --- |
| Illegal input $e(x)\delta_0(y)$ | Used only as the ambient distribution being split; never supplied as an R1 source. |
| Bad conic directions left in the good R1 coefficient | $q=1$ on an open high-frequency neighborhood of both forbidden rays; fixed compact localization preserves the exclusion. |
| Positive-scale cusp in the proposed scalar |195.4 makes partial heat smoothing elliptic on the bad wavefront; the front function $F$ is smooth by its Gaussian-damped Fourier integral. |
| Missing critical-order term | The degree0 logarithmic anomaly is retained in195.9–195.13 and admitted by the existing105 stage. |
| Strict-face estimate only pointwise away from the singular point | Annular negative-order Gaussian-tail rapidness plus all-positive-order moderation gives every differentiated remainder, including $r=0,s\ne0$. |
| Missing three-vertex partial faces | Smooth annular/angular coefficients at $r=0,s=0,r=s$ make their further blowups harmless; fixed integer/log indices are retained. |
| Hidden zero-width heat endpoint declared a source operation | Not used; one fixed scalar is admitted by a direct105.5 membership proof. |
| Formal jets substituted for the actual joint profile | The two entire evaluations195.18 and195.19 are exact for every positive regulator. |
| New arbitrary product of singular R1 coefficients | None; each history has one R1 coefficient multiplied only by a smooth positive-regulator scalar. |
| Conflict with174/180/192 terminal exclusion | The bad history has genuine retained-output relative scalar dependence, outside those terminal hypotheses. |
| Conflict with171 no-hidden exclusion | Both actual histories have one forgotten physical vertex. |

**Claim submitted for review196:** accept or reject Lemma195.1 with its uniform strict-corner estimates, the fixed R1 cones in195.14/195.16, and their two whole source evaluations. If accepted, the answer to the central source-membership question is positive: both $A$ and $D$ are actual original105/108 sources, with source-controlled126 rows in the stated explicit parameter families. By165/168 this also supplies source membership of the particular labelled and symmetric Green outputs already reduced to $A$. It supplies no general source-level antiderivative map for arbitrary mixed histories.

This is one primary construction and its sole consolidated author correction, requested in section3 of review196 frozen at6c395353bcb36eb786df0260da649ceceaf1602d on `research/reach-joint-profile195-primary-review-frozen-20261115`, and bound by CP216. The correction changes only Lemma195.1's strict-annular and corner proof: it separates the actual smooth heat convolution from the actual separated point contribution, gives the differentiated Taylor remainder, and tracks all additional partial-face derivatives and weights. The conic split, the two source histories and their exact equality are unchanged. The corrected source still requires freeze and source-locked196 rereview; no affirmative reviewed scientific disposition is inferred here. Scientific review, editorial integration, native protected admission, exact readback and canonical tracker reconciliation remain separate. Producer and internal reviewer contexts share the Codex system and historical dependencies; no external or independently authenticated mathematical certification is asserted. Universal150.L, residual $W$ acyclicity, originalR3, full126.14, higher weights, actual lifting and M5/R4 remain OPEN.
