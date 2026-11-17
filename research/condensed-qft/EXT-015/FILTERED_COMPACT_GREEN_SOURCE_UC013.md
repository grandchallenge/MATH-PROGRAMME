# EXT-015 REACH / UC-OP-013 — the compact Green primitive on the filtered two-slot source

**Disposition: BOUNDED POSITIVE CONSTRUCTION, submitted for distinct criticism.** For the fixed two-slot conic heat filter below, each actual compact primitive of150.3 has continuous lifts on the entire original108 completed source. The final output cutoff, compact affine-moment corrections, scalar decorations, finite jets, partition densities and proper projections are retained exactly. The operation preserves the original fixed-order rapid relation and supplied126 coefficient rows. It does not prove the unfiltered150.L or a contracting homotopy on the complementary complex.

## 1. Frozen inputs, category and fixed data

The protected input is `32dbbb4635a9493a5b46cf9f0962e833a19120fe`, retained by `research/reach-filtered-green-uc013-input-frozen-20261117`. CP240 was committed at `250c074c14db939de1490da64d2a837830c561e6` before construction. This primary changes only this source.

| Dependency | Exact Git blob and use |
| --- | --- |
| [UC010](COMPLETED_CONIC_HEAT_SOURCE_OPERATOR_UC010.md) | `efe5a9a40011b8ba510fc56107406f7bbe86b7ff`; the actual whole-history heat filter, graph ideal, source extension and rapid bounds |
| [UC011](AGENT_CRITICAL_REVIEW_CONIC_HEAT_OPERATOR_UC011.md) | `0d509ef7b493c470fc6daad6fb273b50c21c520c`; distinct criticism of UC010 |
| [UC012](CONIC_HEAT_OPERATOR_ACCEPTANCE_UC012.md) | `dbe5fed29240dbb7a5a52f770422cc837f1c1afa`; accepted scope and the present bounded question |
| [Scalar105](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | `a8ce66ff0edec33e2aff299550fca2089d671033`; complete fixed-index scalar stages and heat pullbacks |
| [Mixed108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | `587c15fd6e24f6e6b14de574ff878221cdbd5cb6`; graph sources108.1, completed tensors108.6, entire histories108.7 and unchanged rapid rule108.3 |
| [Parameter126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | `5b05c6147d237ca1d22e4dcbce9262b0f038c163`; supplied whole-coefficient rows126.6 and uniform rapid graphs126.8 |
| [Comparison150](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) | `03deca9212a9bea56743e482e5cb79edb46b9d7f`; actual compact primitives150.3, support cancellation and ambient bound150.6 |

Work in ZFC in the real liquid heart of fixed exponent $0<p\le1$, on the original physical line and one fixed nonempty open interval $U$. All analytic source maps below are continuous maps between the admitted complete real Fréchet stages. Their images, closed equality graphs, intersections and quotients have108/126's liquid meaning. The domain is ordered and labeled, with all operator data fixed.

Specialize UC010 to $n=2$ and a connected directional heat convolution. Write its energy as $E(\xi)=\tau(\xi_1-\xi_2)^2$, with fixed $\tau>0$; multiple edges merely add their positive variances. Choose its even nonnegative angular selector $a$ equal to one near the two directions of $\xi_1+\xi_2=0$, with support sufficiently narrow that

$$
|\xi_1|\ge c|\xi|,\qquad |\xi_2|\ge c|\xi|,
\qquad E(\xi)\ge c|\xi|^2
\quad\text{on }\mathrm{supp}\,a
\tag{UC13.1}
$$

for some fixed $c>0$. This is an allowed UC010 selector: the two-slot nonzero partition conormal consists precisely of those two directions. Take its fixed radial cutoff $0\le\psi\le1$, equal to one near zero, and put

$$
q(\xi)=(1-\psi(\xi))a(\xi/|\xi|),\qquad
k_\epsilon=\mathcal F^{-1}(qe^{-\epsilon^2E/2}),\qquad
C_{2,\epsilon}u=\chi_{\mathrm{out}}(k_\epsilon*u),
\tag{UC13.2}
$$

where $\chi_{\mathrm{out}}\in C_c^\infty(U^2)$ is the actual final cutoff. The Fourier convention is that of UC010. No low-frequency term or spatial tail is removed from this definition.

Fix the actual real moment-dual bumps of150, $b_0,b_1\in C_c^\infty(U)$ with $\int t^a b_b(t)\,dt=\delta_{ab}$ for $0\le a,b\le1$. For $i=1,2$ retain exactly

$$
e(t)=|t|/2,\qquad
B_iv=\sum_{a=0}^1 b_a(x_i)\int z_i^a v(z_i,x_j)\,dz_i,
\qquad h_iv=e*_{x_i}(1-B_i)v,
\quad j\ne i.
\tag{UC13.3}
$$

All these integrals are distributional with the original physical density. The claim is about $G_i=h_iC_2$, not about $h_i$ on an arbitrary mixed source.

## 2. The scalar heat-symbol lemma, including negative degrees

Here is the analytic lemma used for the cutoff integral. Let $A(x,\xi)$ be a smooth classical symbol of integer order $m$ on $\mathbb R^2_\xi$, with smooth parameters $x$ in a fixed compact set. Assume it is zero near frequency zero and supported in the fixed cone (UC13.1). Thus, for each $N$, it has homogeneous terms of degrees $m,m-1,\ldots,m-N+1$ and a remainder in $S^{m-N}$, uniformly with every parameter derivative. Then

$$
K_\epsilon(x,r)=\mathcal F^{-1}_{\xi\to r}
\bigl(A(x,\xi)e^{-\epsilon^2E(\xi)/2}\bigr)
\tag{UC13.4}
$$

is polyhomogeneous on the blowup of $\{\epsilon=0,r=0\}$, on compact physical patches. A sufficient fixed front index family is all integer powers at least $-2-m$, with log order at most one, together with the nonnegative integer smooth powers. In the application $m=|\alpha|-2$, this is simply all integer powers at least $-|\alpha|$, with log order at most one. The statement includes compatible coefficients and every differentiated remainder estimate, with auxiliary lower weight strictly below the least power. It includes joint smoothness through $\epsilon=0$ away from $r=0$.

We give the proof because a formal symbol expansion would not establish the lemma. First consider a homogeneous angular term $A_d$ of degree $d$, multiplied by the fixed high-pass cutoff. Put $L=-2-d$. If $d>-2$, its homogeneous extension at frequency zero is locally integrable. If $d=-2-L$ with integer $L\ge0$, define a tempered extension by radial finite part: in its pairing with a Schwartz test, subtract the radial Taylor polynomial through degree $L$ at zero using one fixed radial cutoff. In polar frequency coordinates the measure is $t\,dt\,d\theta$, and the subtracted radial integrals are $t^{k-L-1}\,dt$, for $0\le k\le L$. This defines a finite-order distribution, smooth away from frequency zero. Changing that extension changes only derivatives of a delta at frequency zero, whose inverse transforms are smooth polynomials.

Set $\rho=(\epsilon^2+|r|^2)^{1/2}$, $\lambda=\epsilon/\rho$ and $\omega=r/\rho$. The exact substitution $\eta=\rho\xi$ gives the prefactor $\rho^L$. Radial integration of the Taylor terms just subtracted proves

$$
\mathcal F^{-1}(A_d e^{-\epsilon^2E/2})
=\rho^L F_d(x,\lambda,\omega)
+P_L(x,\epsilon,r)\log\rho+S_d(x,\epsilon,r),
\tag{UC13.5}
$$

in that finite-part convention, where $S_d$ is jointly smooth and includes any polynomial corrections from the chosen finite part. Here $P_L=0$ if $L<0$; if $L\ge0$, it is a homogeneous polynomial of total degree $L$ in $(\epsilon,r)$, possibly zero. Indeed the Taylor term of degree $k$ in

$$
\exp(i\omega\cdot\eta)\exp(-\lambda^2E(\eta)/2)
\tag{UC13.6}
$$

has total degree $k$ in $(\lambda,\omega)$: a heat factor contributes two of both radial and parameter degree. Only $k=L$ integrates as $dt/t$ and produces a logarithm. The terms $k<L$ integrate as powers and account for the ordinary smooth polynomial corrections. There is one logarithm, never a squared logarithm. Multiplication by the original high-pass cutoff changes the extended homogeneous distribution by a distribution of compact frequency support. Its inverse transform after multiplication by the heat multiplier is jointly smooth in $(\epsilon,r)$ through zero, with all parameter derivatives. Thus the actual high-pass homogeneous kernel is (UC13.5) plus an exact smooth term, retaining its complete low-frequency contribution.

The coefficient $F_d$ is smooth on the entire closed front hemisphere, including its strict corner $\lambda=0$. To check this, split frequency at $|\eta|=1$. The finite-part contribution at bounded frequency is smooth in $(x,\lambda,\omega)$, since its distribution is of finite order on compact support. At large frequency, ellipticity and homogeneity give, for every $a$ and multi-index $\beta$,

$$
\left|\partial_\eta^\beta\partial_\lambda^a
\left(A_d(x,\eta)e^{-\lambda^2E(\eta)/2}\right)\right|
\le C_{a,\beta}|\eta|^{d+a-|\beta|},
\qquad 0\le\lambda\le1,
\tag{UC13.7}
$$

also after any fixed $x$ derivative. Differentiated Gaussian factors are bounded polynomials in $\lambda|\eta|$ times a decaying Gaussian on this cone. Near the strict corner $|\omega|\ge c_0>0$. Integrating repeatedly by parts with $(\omega\cdot\partial_\eta)/(i|\omega|^2)$ makes the oscillatory integral absolutely integrable, uniformly after any prescribed $\lambda$, $\omega$ and $x$ derivatives: choose the number of integrations greater than $d+a+|\beta'|+2$, where $\beta'$ counts the inserted physical frequency powers. Dominated convergence then gives those derivatives at $\lambda=0$. On the complementary region $\lambda\ge c_0$, ellipticity gives Gaussian decay directly. These regions cover the front hemisphere. This proves actual strict-corner smoothness, rather than estimates restricted to positive $\lambda$. In particular there are no unaccounted $\log\lambda$ coefficients; the radial calculation produces only the displayed $\log\rho$ polynomial.

For the full classical symbol, subtract its first $N$ homogeneous terms with the fixed high-pass cutoff. Its remainder $R_N\in S^{m-N}$ satisfies

$$
\int_{\mathbb R^2}(1+|\xi|)^{a+|\beta|}
|\partial_x^\gamma R_N(x,\xi)|\,d\xi<\infty
\quad\text{if }N>m+a+|\beta|+2.
\tag{UC13.8}
$$

The estimate $|\partial_\epsilon^a e^{-\epsilon^2E/2}|\le C_a(1+|\xi|)^a$ for $0\le\epsilon\le e_0$ shows that its heat kernel is jointly $C^K$ through $(\epsilon,r)=0$ whenever $N>m+K+2$. This holds uniformly with any prescribed finite number of parameter derivatives.

For completeness, this provides the full scalar remainder topology as follows. Fix a requested front truncation depth $T$ and a requested derivative depth $D$. Choose $N$ so large that the last omitted front power exceeds $T+D+2$ and the remainder in (UC13.8) is $C^{T+D+3}$, increasing these integers when $T$ is negative. Separate the finite homogeneous kernels by (UC13.5), and subtract the ordinary Taylor polynomial of their smooth terms plus the $C^{T+D+3}$ remainder kernel through total degree greater than $T+D+1$. Taylor's integral remainder bounds all ordinary derivatives through the requested depth by the corresponding powers of $\rho$; its lifted b-derivatives have the same or better radial bounds. Every bound uses finitely many symbol seminorms. The finitely many homogeneous front terms have smooth hemisphere coefficients, so their angular derivatives and their Taylor remainders at $\lambda=0$ obey the same bounds. The same construction can be performed at any higher truncation. The coefficients agree on overlaps: the difference would be a finite power/logarithmic expansion of higher vanishing order, and its least nonzero power/log coefficient would contradict that estimate. Increasing $N$ adds only higher front powers; the lower ordinary Taylor coefficients of the combined regular part therefore agree by this uniqueness argument. The resulting compatible full coefficient list and all its remainders belong to one fixed-index complete105 stage. The index list and lower weight have not changed with $T,D,N$; these integers select finite proofs of its seminorm bounds. This proves the lemma.

## 3. The exact Green kernel with the prescribed final cutoff

Fix $i$, and let $j$ be the other coordinate. Write one original108 source summand in UC010's accepted finite source normal form

$$
u_\epsilon=\partial_y^\alpha B_*(A_\epsilon T),
\qquad T\in E_{s,K,\Gamma},\quad A\in S_\nu.
\tag{UC13.9}
$$

Here each of the two rows of $B$ selects one old block coordinate $w_b$; unretained block coordinates are still present in $w$. Its density is the original history density $d_h(w)\,dw$. Formula (UC13.9) denotes the actual elementary source evaluation, not a finite-separability assertion for a completed coefficient. As in UC010, derivatives in forgotten physical directions give zero. Scalar collision jets, finite complement normal derivatives and source partition derivatives first give finitely many such terms by the accepted105/108 finite source normal form. Their index, graph-order and density changes are retained. The retained derivative contributes exactly $(i\xi)^\alpha$ before the final cutoff.

Put $y=Bw$. Before the moment correction, the required scalar integral is

$$
V_{\alpha,\epsilon}(x,y)
=\int_{\mathbb R}e(x_i-z_i)\chi_{\mathrm{out}}(z_i,x_j)
(\partial^\alpha k_\epsilon)(z_i-y_i,x_j-y_j)\,dz_i.
\tag{UC13.10}
$$

For positive regulator $k_\epsilon$ is Schwartz, and this integral and its Fourier calculation are legitimate. Set $t=z_i-x_i$. Its exact inner Fourier amplitude is

$$
a_i(x,\sigma)
=\int_{\mathbb R}\frac{|t|}{2}
\chi_{\mathrm{out}}(x_i+t,x_j)e^{it\sigma}\,dt.
\tag{UC13.11}
$$

For $x$ in any fixed compact output patch, the integrand has one common compact $t$ support. Thus $a_i$ is smooth in $(x,\sigma)$, and piecewise integration by parts on $t<0$ and $t>0$ proves that it is a classical symbol of order $-2$. More explicitly, localize near $t=0$, Taylor-expand the cutoff there, and integrate by parts on the two half-lines. The derivatives of the localized remainder vanish to the stated Taylor order at zero; its next one-sided derivative has a finite jump. Repeated half-line integration by parts gives, uniformly with all $x$ derivatives and after $b$ frequency derivatives,

$$
a_i(x,\sigma)
\sim\sum_{l\ge0}\frac{\partial_i^l\chi_{\mathrm{out}}(x)}{l!}
i^{-l}\partial_\sigma^l(-\sigma^{-2}),
\qquad
\partial_\sigma^b R_N=O((1+|\sigma|)^{-2-N-b}).
\tag{UC13.12}
$$

The part localized away from zero is smooth compactly supported and gives a rapidly decreasing transform. This also proves the remainder bound for any prescribed number of $x$ derivatives, using finitely many derivatives of the fixed cutoff. The leading signs are $-\chi_{\mathrm{out}}/\sigma^2$ and $-2i\partial_i\chi_{\mathrm{out}}/\sigma^3$: $\partial_\sigma^l e^{it\sigma}=i^lt^le^{it\sigma}$. The possible delta ambiguities in the Fourier transform of $|t|/2$ lie on $\sigma=0$ and are annihilated by the conic selector. No inverse at that axis is used.

Fubini in the positive-regulator integral now gives the exact identity

$$
V_{\alpha,\epsilon}(x,y)
=(2\pi)^{-2}\int e^{i(x-y)\cdot\xi}
a_i(x,\xi_i)(i\xi)^\alpha q(\xi)
e^{-\epsilon^2E(\xi)/2}\,d\xi.
\tag{UC13.13}
$$

On the support of $q$, (UC13.1) turns the one-variable expansion (UC13.12) into a genuine two-variable classical symbol expansion of order $|\alpha|-2$. Frequency derivatives in either variable obey its symbol bounds. The low and bounded frequencies are smooth because $q$ vanishes near zero. Section2 therefore applies to the actual integral (UC13.10), including the variable final cutoff. Its front powers are $l-|\alpha|$, with at most one logarithm at a nonnegative resonant power; a sufficient fixed index list allows log order one at every integer power at least $-|\alpha|$. It includes the entire regular low-frequency contribution. In particular this is an exact-amplitude proof, rather than replacing the compact primitive by an uncut multiplier $-\xi_i^{-2}$.

The two moment kernels are

$$
M_{a,\alpha,\epsilon}(x_j,y)
=\int z_i^a\chi_{\mathrm{out}}(z_i,x_j)
(\partial^\alpha k_\epsilon)(z_i-y_i,x_j-y_j)\,dz_i,
\qquad a=0,1.
\tag{UC13.14}
$$

These are jointly smooth in $(\epsilon,x_j,y)$ through $\epsilon=0$. Indeed the Fourier transform of the compact smooth test $z_i^a\chi_{\mathrm{out}}(z_i,x_j)$ is Schwartz in $\xi_i$, uniformly with all $x_j$ derivatives. On the support of $q$, $|\xi|\le c^{-1}|\xi_i|$. Every derivative in $y,x_j,\epsilon$ inserts only a fixed polynomial frequency bound, absorbed by that Schwartz transform. Absolute integrability and dominated convergence prove the assertion for every mixed derivative. This uses both the angular separation and the actual cutoff; positive-regulator smoothness alone would be insufficient.

Choose one fixed compact smooth $\theta_G(x)$ supported in $U^2$ and equal to one on the following product: in coordinate $i$, the interval hull of the projection of $\mathrm{supp}\,\chi_{\mathrm{out}}$ and the bump supports; in coordinate $j$, the projection of $\mathrm{supp}\,\chi_{\mathrm{out}}$. These are compact subsets of $U$, since $U$ is an interval. Put $f_a=e*b_a$, which is smooth, and choose $\eta(w)=1$ near $K$, compactly supported in the old block patch. The exact compact scalar kernel for this history is

$$
\mathcal K_{h,i,\epsilon}(x,w)
=\theta_G(x)\eta(w)d_h(w)
\left[V_{\alpha,\epsilon}(x,Bw)
-\sum_{a=0}^1 f_a(x_i)M_{a,\alpha,\epsilon}(x_j,Bw)\right].
\tag{UC13.15}
$$

The bracket is the actual formula $h_i[\chi_{\mathrm{out}}\partial^\alpha k_\epsilon(\,\cdot-Bw)]$. Its two affine moments cancel outside the stated interval hull, by150.3; multiplication by $\theta_G$ therefore preserves the entire kernel. The separate affine tails have canceled before this compact representation is made. The old density $d_h$ is the one used in the source evaluation: for an induced partition density it includes its actual constant Gram determinant, and for coordinate-density pushforward it is one. The Green integration is in $z_i$ with its physical density and unit Jacobian. No probability or quotient-volume normalization is substituted.

## 4. Every collision corner and the fixed complete target stage

The singular graph in (UC13.15) is exactly

$$
D_h=\{x-Bw=0\},\qquad I_h=(\epsilon,x_1-(Bw)_1,x_2-(Bw)_2).
\tag{UC13.16}
$$

It is a physical partition diagonal on the genuine new vertices $(x_1,x_2)$ and old block vertices $w$. Each new vertex joins the block selected by its row of $B$; an unselected old vertex is a singleton. This remains true when both retained outputs select the same old block. The normal rank is two since $D_x(x-Bw)=I_2$, independently of the rank or kernel of $B$.

UC010's full-arrangement principalization applies to this same ideal. In detail, partition-diagonal intersections are partition diagonals. In a deepest-first order, a center contained in $D_h$ factors one common radial factor from this ideal in charts meeting its proper transform; in the other charts the residual ideal is the unit ideal. Incomparable centers separate after their intersection is blown up. Blowing up the remaining proper transform of $\{\epsilon=0,D_h\}$ principalizes the residual ideal, and subsequent blowups preserve invertibility. Thus on every chart of a finite compact corner atlas of the original full heat collision space $X_{m+2}$,

$$
\rho_h=(\epsilon^2+|x-Bw|^2)^{1/2}
=u_h\prod_G r_G^{a_G},\qquad u_h>0,\quad a_G\in\mathbb N_0.
\tag{UC13.17}
$$

Dividing the generators by this monomial gives a smooth normalized angular map to the single-graph front hemisphere. Section2 therefore pulls back at every simultaneous collision corner, including the strict regulator face. Its logarithm is the exact identity

$$
\log\rho_h=\log u_h+\sum_G a_G\log r_G.
\tag{UC13.18}
$$

It follows that one sufficient fixed scalar stage for the compact kernel (UC13.15) has face indices and lower weights

$$
E_G^{\mathcal K}
=\{(-|\alpha|a_G+l,k):l\in\mathbb N_0,\ k=0,1\},
\qquad b_G^{\mathcal K}=-|\alpha|a_G-1.
\tag{UC13.19}
$$

Unused slots have zero coefficients; this harmless enlargement also contains every smooth term and moment correction. The exponents and weights depend only on the fixed history and jet order. They do not depend on an input coefficient, truncation depth, rapidness request or126 row refinement.

To spell out the topology, the single-graph construction supplies compatible smooth hemisphere coefficients, their full Taylor coefficients at its boundary, and every weighted iterated b-derivative remainder. Substituting (UC13.17) gives products of fixed radial powers and full Taylor expansions of positive units. Applying a fixed target b-derivative uses finitely many single-graph b-derivatives and smooth coefficient derivatives. Choose its single-graph truncation sufficiently deep for the requested target face truncations. On the finite compact atlas, Taylor's integral remainders and the estimates in section2 bound every resulting target seminorm. Factors logarithmic in other faces are bounded by the one fixed extra negative power in (UC13.19); the same argument applies recursively to the coefficient stages on their intersections. Overlap identities are actual identities, so their coefficients agree by uniqueness. This is the complete fixed-index105 topology, rather than a bound on a single front-face profile. Pullback along the graph map has not introduced a nonpartition center or an auxiliary-noise physical coordinate.

## 5. Continuous lifts on the whole completion and entire-family descent

Let $\pi_w:(x,w)\mapsto w$. It is the original physical vertex-forgetting heat b-fibration105.4. Define the scalar source map

$$
L_h:S_\nu\longrightarrow S_{\nu'_h},\qquad
L_h(A)=\mathcal K_{h,i}\,\pi_w^*A.
\tag{UC13.20}
$$

Scalar105's continuous pullback and product maps apply with the actual kernel stage (UC13.19). In local monomial coordinates, if $\pi_w^*r_H=v_H\prod_G r_G^{c_{GH}}$, the output indices are the finite sums of the kernel indices and $c_{GH}E_H$, with integer saturation and the full Taylor expansions of the positive units $v_H$. Zero exponent contributes no index. Logarithms are expanded by their finite binomial rules. Fixed lower weights strictly below the corresponding sums, for example below $\sum_Hc_{GH}b_H-|\alpha|a_G-1$, suffice, recursively on coefficient spaces. These bounded-below locally finite index sets and weights are frozen for the stage. Each requested output seminorm is bounded by finitely many input scalar seminorms; its depth changes neither the index family nor its lower weights.

Choose $\theta_T(x)=1$ near the output support in (UC13.15), compactly supported in $U^2$, and extend the R1 coefficient by

$$
J_h(T)=\theta_T(x)T(w).
\tag{UC13.21}
$$

This has the admissible cone and continuity proof of UC010.16. For clarity, a possible singular covector is $(0,\zeta_w)$. If it were a nonzero enlarged physical partition conormal, deleting the new zero-covector entries would give a forbidden old partition conormal with the same nonzero $\zeta_w$; if every remaining block is a singleton, the conormal conditions instead force $\zeta_w=0$. Compact support separates this cone on the cosphere bundle from the finite forbidden conormal union. A fixed slight enlargement gives an admissible target cone. In product Fourier coordinates, either the new frequency dominates, controlled by rapid decay of $\widehat{\theta_T}$ and the finite old negative-Sobolev norm, or the old frequency lies outside the old cone, controlled by finitely many old off-cone seminorms. A finite coordinate cover gives a continuous map into a complete graph stage $E'_{h,s}$. The geometry and scalar choices are unchanged when the old finite Sobolev order is relaxed.

The completed projective tensor map is therefore

$$
\mathcal L_{h,i}=J_h\widehat\otimes_\pi L_h:
E_{s,K,\Gamma}\widehat\otimes_\pi S_\nu
\longrightarrow E'_{h,s}\widehat\otimes_\pi S_{\nu'_h}.
\tag{UC13.22}
$$

The target history uses the identity partition on $(x,w)$, multiplication of its scalar and R1 coefficients, and the proper physical projection forgetting $w$. On elementary tensors its exact distributional testing identity is

$$
e_{h'}\mathcal L_{h,i}(T\otimes A)
=p_{x*}[J_h(T)L_h(A)_\epsilon]
=h_iC_{2,\epsilon}e_h(T\otimes A).
\tag{UC13.23}
$$

The first equality is an original108.7 history, with the unchanged block density. The second follows from (UC13.10)–(UC13.15); pairing with $T$ is distributional, and no point evaluation of $T$ occurs. All external derivatives transferred from the old source have already been included in $\alpha$. If a derivative of the final output is requested subsequently, it differentiates every cutoff and moment term by the full Leibniz rule.

The left side of (UC13.23) is continuous in the complete source by108.6 and (UC13.22). On every compact positive-regulator interval the right side is also continuous: the filtered heat multiplier and all regulator derivatives are Schwartz, the final cutoff is fixed, and the compact Green map is continuous on the fixed-support distributions by150.6. Algebraic tensors are dense. Thus (UC13.23), together with every regulator derivative, holds on the entire completed source, including coefficients that have no finite separable expression. Finite direct sums and finite common refinements treat every finite history collection and all finite jet normal-form terms.

Consequently equality of entire source evaluations is preserved. In particular an exactly canceled sum from different partitions or projection histories has exactly zero output; no scalar coefficient is extracted from that canceled sum. The source maps give a bounded filtration shift for each prescribed finite input collection. Lift an arbitrary liquid source-image section on an extremally disconnected cover; compactness supplies finitely many complete stages there. Apply the maps and descend by (UC13.23). This gives actual real-liquid maps

$$
G_i=h_iC_2:\mathcal P_2\longrightarrow\mathcal P_2.
\tag{UC13.24}
$$

There is no assertion of a global source lift on every profinite test, injectivity of a completed tensor transition or a chosen splitting of the evaluated image.

## 6. The original rapid relation, its closed intersection and supplied126 rows

The original108.3 rule is preserved with no change of denominator. On the fixed output support of $C_2$, the compact150.6 estimate is

$$
\|h_i v\|_{H^{-t}}\le C_t\|v\|_{H^{-t}},\qquad t\ge0.
\tag{UC13.25}
$$

Its supports and bumps are independent of regulator. Regulator and parameter derivatives commute with this fixed distributional map. Combining (UC13.25) with accepted UC010.20 gives, after enlarging orders to be nonnegative if necessary,

$$
\|\partial_\epsilon^k(G_i u)_\epsilon\|_{H^{-t'_k}}
\le C_k\sum_{l=0}^k\epsilon^{-(k-l)}
\|\partial_\epsilon^l u_\epsilon\|_{H^{-t_l}},
\qquad t'_k=\max(0,t_0,\ldots,t_k).
\tag{UC13.26}
$$

For a requested decay power $L$, use input power $L+k$. The order $t'_k$ was fixed before $L$ and does not grow with it. This is a continuous map of complete rapid graph stages: each output weighted seminorm has a finite input-seminorm bound, with derivative compatibility supplied by the exact finite Leibniz formula. The bound acts on the whole evaluated distribution, so cancellations and completed coefficients require no separate rapid coefficient witnesses.

An actual analytic/rapid intersection witness is a complete closed equality graph equating a source evaluation with a rapid graph evaluation. Apply (UC13.22) to its analytic representative and (UC13.26) to its rapid representative. Equation (UC13.23) equates their outputs. Thus these are continuous maps of the closed equality graphs, and liquid image descent gives

$$
G_i(\mathcal P_2\cap\mathcal I_2^{\mathrm{rap}})
\subset\mathcal P_2\cap\mathcal I_2^{\mathrm{rap}},\qquad
\overline G_i:\mathcal Z_2\longrightarrow\mathcal Z_2.
\tag{UC13.27}
$$

This is the original fixed finite-order intersection and quotient, not the kernel of physical coefficient extraction or scalarwise flatness.

For a supplied126.6 coefficient row, apply the same finite source maps to every entry. Only the R1 Sobolev refinement changes between rows; all output geometry, scalar indices, lower weights and finite histories remain fixed. Continuous linearity preserves the coefficient parameter-derivative identities within a row. Across rows, actual evaluation identities are preserved by (UC13.23), including representatives differing by the kernel of a proper projection. Thus these are genuine target126.6 rows. For each mixed parameter/regulator derivative on a compact parameter set, (UC13.26) holds with $t'_k$ replaced by $\max(0,t_{\gamma,0},\ldots,t_{\gamma,k})$, uniformly on that set. Applying the same construction to their complete rapid equality graphs gives maps on the original126.9 images, intersections, quotients and parameter sheafifications. Parameter chart changes and restrictions commute with these fixed linear maps. This uses supplied row witnesses and does not construct witnesses from pointwise membership, so it proves no part of the missing full126.14 surjectivity.

## 7. Identities, nonzero quotient control and hostile cases

The actual distribution identity from150 holds on these outputs:

$$
D_iG_i=(1-B_i)C_2,
\qquad D_i=\partial_{x_i}^2.
\tag{UC13.28}
$$

Both sides now have actual source maps: the left side by (UC13.24) and the original physical derivative, and the right side by UC010 and150's smooth moment/reinsertion maps. Equality is before quotient and holds on completed sources and supplied parameter rows. It is a filtered right-inverse identity with the actual affine moment correction, not $D_iG_i=1$.

If $\chi_{\mathrm{out}}\ne0$, then $\overline G_i$ is nonzero. Choose real $\phi\in C_c^\infty(U^2)$ with $\chi_{\mathrm{out}}\phi\ne0$, and choose a conormal direction $\eta$ in the interior where $a=1$. Both $\eta_i$ are nonzero. As a temporary complex notation put $u_N=\phi e^{iN\eta\cdot x}$. On a ball $|\xi-N\eta|\le c_1N$ the multiplier $q$ is one for large $N$. The Schwartz tails of $\widehat\phi$ outside that ball show, for every fixed $K,M$ on compact physical sets,

$$
q(D)u_N=u_N+O_{C^K}(N^{-M}).
\tag{UC13.29}
$$

Indeed derivatives insert only polynomial frequencies, while the complement of that ball is separated by order $N$ from the translated Fourier center. Put $v_N=\chi_{\mathrm{out}}q(D)u_N$. Its $L^2$ norm stays bounded below. Integration by parts in $x_i$ against the compact amplitude $x_i^a\chi_{\mathrm{out}}\phi$ gives $m_{i,a}v_N=O(N^{-M})$, uniformly with any prescribed number of $x_j$ derivatives; (UC13.29) controls the error with its actual compact cutoff. Thus $B_iv_N=O_{L^2}(N^{-M})$. For some fixed finite $N$, $(1-B_i)v_N\ne0$, and (UC13.28) gives $h_iv_N\ne0$.

For that fixed input, $C_{2,\epsilon}u_N\to v_N$ smoothly on the output compact set as $\epsilon\to0$, by the Schwartz transform of $u_N$ and dominated convergence. Formula (UC13.25) gives $G_{i,\epsilon}u_N\to h_iv_N\ne0$ in distributions. A family rapid in any fixed finite negative Sobolev order has distributional limit zero, so this output is not in the original rapid ideal. At least one of the real and imaginary parts of this fixed smooth input has nonzero output. The theorem remains in the real category; neither a complex scalar extension nor an infinite admissible parameter family is needed. If the cutoff is zero, the operator is zero and this nonzero clause does not apply.

There is also a direct hostile check that the resonant logarithm cannot be omitted. Choose an off-diagonal point $b\in U^2$ with $\chi_{\mathrm{out}}(b)\ne0$. Such a point exists whenever the smooth cutoff is nonzero. The compact R1 input $T=\delta_b$ is legal: its support misses the physical two-slot collision, so its fiber conormal meets no forbidden partition conormal. At $x=b$, the $\alpha=0,l=0$ term of (UC13.13) gives

$$
\frac{(G_{i,\epsilon}\delta_b)(b)}{\log\epsilon}
\longrightarrow c_i\chi_{\mathrm{out}}(b),\qquad
c_i=(2\pi)^{-2}\int_{S^1}\frac{a(\theta)}{\theta_i^2}\,d\theta>0.
\tag{UC13.30}
$$

Indeed its radial integral is minus $\chi_{\mathrm{out}}(b)$ times the angular integral of $\int R^{-1}(1-\psi(R))e^{-\epsilon^2R^2E(\theta)/2}\,dR=-\log\epsilon+O(1)$, uniformly on the angular support. All symbol terms after the leading one have integrable radial tails at $r=0$ and remain bounded as $\epsilon\to0$. The moment kernels are smooth through zero by (UC13.14), so they cannot cancel this logarithm. This is an actual cutoff-and-moment control of the scalar kernel. A pointwise value alone is not a proof of nonzero rapid quotient; that separate conclusion was proved by the fixed smooth-input distributional limit above.

| Hostile control | What the proof actually supplies |
| --- | --- |
| Variable final cutoff with odd Taylor term | Exact amplitude (UC13.11) and the sign $-2i\partial_i\chi/\sigma^3$ retain its first commutator term; the entire symbol remainder is controlled, rather than discarded |
| Coordinate frequency axes | Both are avoided by (UC13.1); no division on an axis or unproved treatment of its delta ambiguity occurs |
| Negative homogeneous degrees and resonance | Radial finite part gives the exact smooth low-frequency correction and one polynomial $\log\rho$ term; strict-corner estimates are uniform through $\lambda=0$ |
| Finite jets, scalar normal derivatives and forgotten directions | Existing finite source normal form retains all complement terms; retained jets give $(i\xi)^\alpha$, and a forgotten derivative gives the zero map |
| Old scalar $A_\epsilon=\epsilon^{-2}f$, or an admitted power/log decoration | The whole pullback/product (UC13.20) is used, and all regulator derivatives differentiate the entire product |
| Genuinely completed coefficient and canceled histories | Density of algebraic tensors is used only after continuous complete source maps exist; exact whole evaluation (UC13.23) then descends through all cancellations |
| Coincident retained labels and forgotten block variables | The graph remains a legal partition with normal rank two; the original block density and proper projection are unchanged |
| Affine tails from the compact Green kernel | Actual moments cancel them before multiplication by the fixed support cutoff; no tail is declared negligible |
| Rapidness at arbitrarily high requested powers | Equation (UC13.26) keeps one finite order per mixed derivative independent of that power |
| Supplied126 rows versus scalar points | One common output history/scalar stage works across row refinements; closed equality graphs provide the intersection maps |

For the original eleven-edge host, its277 proper sources and two legal disjoint spinneys, the theorem applies only after an admitted actual physical projection or source presentation with exactly two retained output slots, supplied in the original108 complete sources. It then gives the compact primitive of that whole filtered two-slot family. It proves no Green mapping statement at the full host arity, does not identify its Gaussian multiplication edges with convolution factors, and does not multiply overlapping singular counterterms. The original087 subtraction and normalization are unchanged.

## 8. Exact scope and review boundary

This proves only the fixed ordered labeled maps $h_iC_2$ and their displayed identities for the chosen interval, cutoff, bumps, heat variances and selector. No claim is made that they preserve the diagonal-jet kernel $Y$ or the residual $W$, commute with the quantum differential, or form a homotopy on either complex. There is no unfiltered150.L, residual acyclicity, original liquid R3 comparison, full126.14 family recovery, scale transport, permutation equivariance, naturality in physical opens, physical locality, monoidal theorem, higher-weight comparison or final M5/R4 conclusion. These obligations remain **OPEN**.

The parent and this primary context co-developed the exact Fourier-amplitude, radial finite-part and domain mechanisms and cannot serve as the nonauthor critic. This is one primary construction. A fresh distinct UC014 criticism, at most one post-freeze correction, UC015 ledger integration, affected checks, protected admission and exact-source readback remain separate. Same-system logical criticism is internal review, not external certification, MATHCERT or independent execution attestation. No numerical fixture substitutes for the analytic estimates or categorical source maps.

The required mathematical Markdown source gate passed using the existing isolated Windows CPython3.12.12 evidence interpreter at `F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe`, with explicit `UV_CACHE_DIR` and `PYTHONPYCACHEPREFIX` under `LOCALAPPDATA\GCL`, outside the worktree. There is no admitted `uv.lock`; this local environment is explicitly **not pinned**. No dependencies were installed and no system/WSL environment was reused. This source gate checks mathematical Markdown structure, not mathematical truth or browser glyphs. No Git, GitHub, checkpoint or canonical mutation was performed by this construction context.
