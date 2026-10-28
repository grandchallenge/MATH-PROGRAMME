# EXT-015 REACH-R1 / 077 — a uniform smooth regulator endpoint on the locally normal model

**Disposition:** positive endpoint theorem on the precise D21/069 microlocal domain. The regulated contraction operators extend smoothly to regulator zero in the topology of uniform convergence on bounded fixed-sector inputs. Their completed Wick transport is a smooth cochain isomorphism through zero, with an explicitly typed flat connection. This does not include the excluded collision kernels of R2.

**Inputs:** the actual even compact mollifier and primitive of [028](D14_REGULATED_BV_SYZYGY_028.md); fixed normal-sector wavefront calculus [035](R1_NORMAL_CONE_CONTINUOUS_CONTRACTIONS_035.md); the hypocontinuous smooth-plot lemma, total-weight completion and classical/refined Weiss proof of [069](R1_LOCALLY_NORMAL_COMPLETED_WEISS_069.md). The imported normal-topology product and pullback estimates are those of Brouder–Dang–Helein, [Continuity of the fundamental operations on distributions](https://arxiv.org/abs/1409.7662). The ordinary global inductive LCS is separately obstructed in [075](R1_GLOBAL_CONE_PLOT_OBSTRUCTION_075.md); it is not substituted for the refined plots here.

## 1. The actual mollifier curves are smooth in a fixed normal topology

Take the even function $\kappa\in C_c^\infty(\mathbb R)$ of 028, with integral one, and choose $R$ containing its support. Define

$$
\mu_r=\int_\mathbb R u^r\kappa(u)\,du,
\qquad
P_0(z)=|z|/2.
\tag{77.1}
$$

To include a neighborhood of zero in the regulator parameter, define distributions for every real $\epsilon$ by

$$
\begin{aligned}
\langle k_\epsilon,\phi\rangle
&=\int\kappa(u)\phi(\epsilon u)\,du,\\
P_\epsilon(z)
&=\int\kappa(u)P_0(z-\epsilon u)\,du.
\end{aligned}
\tag{77.2}
$$

At positive $\epsilon$ these are exactly the kernel $\kappa_\epsilon$ and primitive of 028. At zero they are $\delta_0$ and $P_0$. Let

$$
\Lambda_0=\{(0,\xi):\xi\ne0\}\subset\dot T^*\mathbb R.
\tag{77.3}
$$

**Lemma 77.1.** Both curves in (77.2) are Bastiani smooth into $\mathcal D'_{\Lambda_0}(\mathbb R)$ with its normal topology. They are even in $\epsilon$, and

$$
\begin{aligned}
\left.\partial_\epsilon^{2j}k_\epsilon\right|_0
&=\mu_{2j}\delta_0^{(2j)}
&& (j\ge0),\\
\left.\partial_\epsilon^{2j}P_\epsilon\right|_0
&=\mu_{2j}\delta_0^{(2j-2)}
&& (j\ge1).
\end{aligned}
\tag{77.4}
$$

All odd regulator derivatives at zero vanish. The zeroth derivative of the second curve is $P_0$.

**Proof.** For a bounded family of compact smooth tests, differentiating the first integral in (77.2) any number of times gives integrals of $u^r\kappa(u)\phi^{(r)}(\epsilon u)$. The compact support of $\kappa$ and uniform test seminorm bounds justify differentiation and Taylor remainders uniformly on that bounded family. Thus this is a smooth curve in the strong distribution topology, with the displayed delta derivatives.

For the second curve, pair with a test and transfer the translation to the test:
$\langle P_\epsilon,\phi\rangle=\int\kappa(u)\langle P_0,\phi(\,\cdot+\epsilon u)\rangle du$.
All translated tests stay in a fixed compact set for $\epsilon$ in a compact interval; their derivatives are uniformly bounded. The same argument proves strong smoothness and the derivatives of the primitive. Its second spatial derivative is the delta, giving (77.4). Evenness of $\kappa$ removes odd moments.

It remains to check the extra normal Fourier seminorms. A localization whose support misses zero is separated from zero. For sufficiently small $\epsilon$, the localized $k_\epsilon$ is identically zero. On that same localization, $P_\epsilon=P_0$ exactly when $R|\epsilon|$ is less than the separation: the absolute value is then affine in the integration variable, its constant term integrates to $P_0$, and its linear term has zero first moment. Hence every extra localized Fourier seminorm of the difference and its regulator derivatives vanishes near zero.

If the support of a localization contains zero, no nonempty covector cone is separated from $\Lambda_0$ there; it introduces no additional normal Fourier seminorm of that kind. This checks every defining seminorm at zero. Away from zero regulator, the kernels are jointly smooth ordinary functions and give normal-topology smooth curves locally. $\square$

No Gaussian replacement or positive-scale asymptotic ansatz is used. This is the actual compact mollifier of the admitted positive-scale model.

## 2. Uniform operator control on each admissible sector

Fix an arity $n$, a compact support $K\Subset U^n$ and a closed cone $\Gamma$ avoiding every forbidden partial-diagonal conormal. Let $E=E_{n;K,\Gamma}^{\,N}$ be the sector of 069. For a chosen pair of slots $i,j$, pull (77.2) back by $z=x_i-x_j$ and multiply by a compact smooth cutoff equal to one near $K$.

The submersion pullback and cutoff are continuous linear maps for the normal topology. Lemma 77.1 therefore gives smooth kernel curves in one compact-support sector whose cone is the pair-diagonal conormal $\Lambda_{ij}$. This cone is independent of $\epsilon$.

For either kernel, define the contraction by multiplying with $T\in E$ and properly projecting away the pair slots, using the parity appropriate to $B_\epsilon$ or $\Delta_\epsilon$. The fixed cone satisfies $\Gamma\cap(-\Lambda_{ij})=\varnothing$.

**Theorem 77.2.** There is one compact-support normal output sector $F$ with admissible output cone, independent of $\epsilon$ near zero, such that both contraction families are smooth curves in $L_b(E,F)$. Here $L_b$ denotes continuous linear maps with uniform convergence on every bounded subset of $E$.

In particular, for each bounded $B\subset E$ and each continuous output seminorm $q$,

$$
\begin{aligned}
\sup_{T\in B}
q\!\left(C^{k_\epsilon}_{ij}T-C^{\delta_0}_{ij}T\right)
&=O(\epsilon^2),\\
\sup_{T\in B}
q\!\left(C^{P_\epsilon}_{ij}T-C^{P_0}_{ij}T\right)
&=O(\epsilon^2).
\end{aligned}
\tag{77.5}
$$

Every regulator derivative converges in the same bounded-input operator topology, with limits obtained from (77.4). The constants may depend on the fixed sectors, bounded set and seminorm.

**Proof.** Normal-topology multiplication under the stated transverse cones is hypocontinuous with respect to bounded sets in both factors. Its target cone is the usual union of the two cones and their nonzero sums. Compactness and transversality give a closed such cone on the relevant support. Proper pushforward is continuous.

The output-cone calculation of 035 depends only on these cones, so it is uniform in the chosen kernel curve. Explicitly, a surviving forbidden output conormal from the input cone alone would lift to a forbidden input partition with the deleted slots singleton. A term from a sum with the pair conormal would force the two deleted input covectors to sum to zero at their collision, and hence a forbidden simultaneous partition. The pair-conormal term alone cannot survive projection with zero deleted covectors. Each possibility contradicts input admissibility. Thus a common closed output cone avoids every forbidden output conormal.

Let $\beta(q,T)$ denote multiplication followed by projection on these fixed sectors. Hypocontinuity with respect to bounded sets of $T$ says precisely that

$$
q\longmapsto\bigl[T\longmapsto\beta(q,T)\bigr]
\tag{77.6}
$$

is a continuous linear map from the fixed kernel sector into $L_b(E,F)$. Compose it with the smooth curves of Lemma 77.1. This proves the smooth operator-curve assertion and all derivative limits. Their first derivatives at zero vanish; Taylor's estimate for each bounded-input operator seminorm gives (77.5).

For any finite-dimensional parameter plot $T(t)$ in a fixed input sector, the same hypocontinuity and the mixed Leibniz argument of Lemma 69.2 show that $\beta(q_\epsilon,T(t))$ is jointly smooth in $(\epsilon,t)$, including zero. Inputs may themselves depend smoothly on both parameters in that common sector. $\square$

This is actual locally uniform control. It does not require a bound common to all admissible cones, all support sets or excluded singular kernels.

## 3. Completed Wick transport through zero

Use the total-weight completion of 069, with weight $n+2k$ on $\hbar^k C_n$, and the already fixed graded normalizations. Define on the admissible domain

$$
B_\epsilon=\sum_{\text{even pairs}}C^{P_\epsilon}_{ij},
\qquad
W_\epsilon=\exp(\hbar B_\epsilon),
\qquad
d_\epsilon^q=W_\epsilon d_{\mathrm{cl}}W_\epsilon^{-1}
=d_{\mathrm{cl}}+\hbar\Delta_\epsilon.
\tag{77.7}
$$

The inherited convention is $[B_\epsilon,d_{\mathrm{cl}}]=\Delta_\epsilon$ and $[B_\epsilon,\Delta_\epsilon]=0$, as in 028/030. Consequently $W_\epsilon$ maps classical to quantum and $W_\epsilon^{-1}$ is the classical trivialization. The fresh audit [082](REASSESSMENT_FRESH_AUDIT_082.md) corrects the previously reversed conjugation, transport and connection formulas together; it does not change the analytic domains or estimates.

At each total weight, every exponential and composition is finite. Theorem 77.2 gives finitely many compatible output sectors independent of $\epsilon$ for those finite compositions; their finite unions remain admissible. Thus $W_\epsilon$, its inverse and $d_\epsilon^q$ vary smoothly on every weight quotient, including zero. The distribution identity $P_\epsilon''=k_\epsilon$ holds for every real regulator in (77.2), so the admitted conjugation identity applies at zero as well.

For any two sufficiently small regulator values, including zero, put

$$
T_{\epsilon,\eta}=W_\eta W_\epsilon^{-1}.
\tag{77.8}
$$

**Theorem 77.3.** The maps (77.8) are smooth completed filtered cochain isomorphisms between the specified restricted quantum models. They satisfy

$$
\begin{aligned}
T_{\epsilon,\eta}d_\epsilon^q
&=d_\eta^q T_{\epsilon,\eta},\\
T_{\eta,\zeta}T_{\epsilon,\eta}
&=T_{\epsilon,\zeta}.
\end{aligned}
\tag{77.9}
$$

They are natural under interval inclusions and intertwine the Wick-conjugated disjoint factorization maps. Their joint dependence on the regulator values and locally normal input plots is smooth.

**Proof.** On a finite weight quotient, these statements follow by multiplying the finite conjugation expressions. Naturality follows from the same global translation-invariant kernels under extension by zero. The disjoint structure maps are the classical maps conjugated by $W_\epsilon$, so (77.8) intertwines them exactly.

Theorem 77.2 and the finite mixed-derivative rules prove smoothness on every quotient. Passing to the componentwise product plots and split weight tower of 069 proves the completed statement. This uses formal weight completion; it introduces no analytic convergence claim in $\hbar$ and no uniform estimate across infinitely many arities. $\square$

The endpoint comparison is with the positive-regulator theory restricted to this same admissible kernel domain. No quasi-isomorphism from that restricted model to the all-distributional positive-scale domain is asserted.

## 4. The regulator cochain connection is explicitly transported

The differential in (77.7) varies with the regulator. The compatible connection on this family is

$$
\nabla_\epsilon^q a
=
W_\epsilon\partial_\epsilon(W_\epsilon^{-1}a)
=
\partial_\epsilon a+
W_\epsilon(\partial_\epsilon W_\epsilon^{-1})a.
\tag{77.10}
$$

The classical trivialization $W_\epsilon^{-1}$ identifies it with ordinary differentiation on the constant classical cochain family. Hence it is flat, commutes with the quantum differential, is compatible with the disjoint structure maps and has horizontal transport (77.8). In additional input parameters it commutes with the ordinary parameter connection. All operations are well-defined smoothly per finite weight and hence in the formal completion.

Ordinary regulator differentiation by itself need not commute with a varying quantum differential. Formula (77.10) is the cochain connection used in the endpoint statement; the ordinary DVS connections at each fixed regulator remain those of 069.

The Weiss Čech comparison is natural under $W_\epsilon$ at each weight. Its finite quotients, split fibrations and eventual weight stabilization are precisely those checked in 069. Thus the completed differentiable Weiss equivalence holds on this refined restricted family through regulator zero, and (77.8) identifies the comparisons. No support-colimit/completion interchange is introduced.

## 5. R1 disposition and exclusions

Together, 069 and this note construct the specified locally normal completed free zero-scale model, its smooth operations and its uniform regulated endpoint. Note 075 settles the proposed ordinary complete/regular global union and identity plot comparison in the negative. These are answers to the distinct R1 analytic obligations, rather than assumptions of global regularity.

The proof does not admit the collision delta jets excluded by D21. It does not identify the refined plots with the obstructed ordinary LCS plots, prove global renormalized BV/QME or settle original-source liquid degree-two surjectivity. Those remain R2/R3/R4 obligations.

The [exact fixture](fixtures/check_uniform_normal_endpoint_077.py) checks the formal moment/delta-jet derivative identity and finite cochain transport, cocycle and connection identities. It includes a hostile check showing why the bare regulator derivative is not the cochain connection. The normal-topology and bounded-input estimates are the infinite proof above, not consequences of a finite matrix calculation.
