# EXT-015D / 030 — UV-admissible smooth-kernel Wick theory

**Status: mathematical proof for GCL critical audit.** This result builds on the protected positive-scale distributional BV theorem [028](D14_REGULATED_BV_SYZYGY_028.md). It proves the existence of a **zero-scale** free quantum Wick prefactorization theory on an explicitly restricted domain of **smooth compactly supported polynomial kernels**, including all-degree completed Weiss descent. It does **not** construct an unrestricted distributional or interacting renormalized theory.

## 1. An explicit stable domain

Let $A_{\mathrm{sm}}(U)$ be the graded direct sum over finite arities $n$ of compactly supported smooth kernels on $U^n$, with the graded permutation action and the two-term free scalar differential $d$ induced by $\partial_x^2$ on odd variables. Its LF differentiable plots and smooth exterior tensor products are those of Costello–Gwilliam, Vol. I §4.2 and Appendix B.2/B.6.

For a kernel $F(s,t,z)$, where $s,t$ are two contracted variables and $z$ lists all remaining variables, define

$$
C_{\delta}F(z)=\int_U F(t,t,z)\,dt,
\qquad
C_{P_0}F(z)=\frac12\int_{U^2}|s-t|F(s,t,z)\,ds\,dt.
\tag{30.1}
$$

Both integrals give **smooth compactly supported functions of the remaining variables**. Derivatives commute with integration and all outputs are supported in the compact projection of $\operatorname{supp}F$. On each fixed compact-support Fréchet stage they are continuous, and on the regular LF union they are differentiably smooth. Summing graded even–odd contractions $C_\delta$ defines the local BV operator $\Delta_0$; summing even–even contractions $C_{P_0}$ defines the Wick propagator operator $B_0$. Both lower polynomial arity by two, so their exponentials are finite on each polynomial input.

## 2. Strong positive-scale convergence

Choose an even normalized nonnegative mollifier $\kappa\in C_c^\infty(\mathbb R)$ and set

$$
\kappa_\epsilon(t)=\epsilon^{-1}\kappa(t/\epsilon),
\qquad
P_\epsilon=\tfrac12|\cdot|*\kappa_\epsilon.
\tag{30.2}
$$

These are precisely the positive-scale kernels of [028](D14_REGULATED_BV_SYZYGY_028.md).

**Theorem 30.1 (full test-function topology).** For every smooth compact-support polynomial kernel $F$ of finite arity,

$$
\Delta_\epsilon F\longrightarrow\Delta_0F,
\qquad
B_\epsilon F\longrightarrow B_0F
\tag{30.3}
$$

as $\epsilon\downarrow0$, in the Fréchet topology of **one fixed compact-support stage**, including every derivative in the surviving variables.

**Proof.** For the mixed contraction use $s=t+\epsilon v$ and extend $F$ by zero to the ambient Euclidean space, yielding

$$
C_{\kappa_\epsilon}F(z)
=\int_{\mathbb R^2}\kappa(v)F(t+\epsilon v,t,z)\,dv\,dt.
$$

On a common compact set, every derivative in $z$ converges uniformly to the corresponding derivative of $F(t,t,z)$; dominated convergence gives convergence in all test-function seminorms. For the even-even contraction, the Lipschitz function $|t|/2$ has $P_\epsilon\to P_0=|t|/2$ **uniformly on compacts**. Multiply by the fixed smooth compact kernel and integrate; all $z$ derivatives converge uniformly. In both cases the output support stays in one compact projection. Finitely many graded pair contractions preserve the statement. $\square$

**Corollary 30.2.** The formal Wick operators $W_\epsilon=\exp(\hbar B_\epsilon)$ and their inverses converge **coefficientwise** on $A_{\mathrm{sm}}(U)[[\hbar]]$ to $W_0=\exp(\hbar B_0)$ and its inverse. Each coefficient receives only finitely many arity-lowering contractions, so Theorem 30.1 applies repeatedly.

## 3. A zero-scale smooth free quantum factorization model

**Theorem 30.3 (complete UV-admissible free model).** The exact identities

$$
[B_0,d]=\Delta_0,\qquad
[B_0,\Delta_0]=0,\qquad
W_0dW_0^{-1}=d+\hbar\Delta_0
\tag{30.4}
$$

hold on all smooth compact-support polynomial kernels. For disjoint opens $U_1,\dots,U_r\subset V$ define

$$
\mu^{(0)}_{U_1,\dots,U_r\subset V}
=W_{0,V}\circ\mu^{\mathrm{cl}}_{U_1,\dots,U_r\subset V}
\circ\bigotimes_iW_{0,U_i}^{-1}.
\tag{30.5}
$$

These maps define a **smooth formal differentiable quantum prefactorization algebra, complete in $\hbar$** on $A_{\mathrm{sm}}(U)[[\hbar]]$. It is the coefficientwise limit, on this specified domain, of the positive-scale Wick operations of 028; the **completed differentiable Weiss map is an equivalence in every cohomological degree**.

**Proof.** Distributionally $(|t|/2)''=\delta_0$. On smooth compact-support kernels integration by parts has no boundary terms; therefore $[B_0,d]$ is exactly the mixed diagonal BV contraction. The graded constant-kernel contractions commute in the requisite sense, giving the remaining relations. Formal conjugation proves the differential has square zero.

The Wick maps $W_{0,U}$ and their inverses are smooth and natural under extension by zero, since the same global Green kernel is restricted to each open and contraction preserves compact output support. Conjugating the classical structure maps therefore yields cochain maps obeying all prefactorization associativity, inclusion, unit and symmetry identities. Each formal coefficient is a finite composition, so Corollary 30.2 proves the stated positive-scale limit.

The $W_0$ define a **natural isomorphism of classical and zero-scale Wick prefactorization diagrams**. The classical smooth polynomial complex has completed differentiable Weiss descent by [024–025](AGENT_CRITICAL_REVIEW_FREE_SCALAR_025.md); tensoring with formal power series and using split finite $\hbar$ quotient towers preserves the Weiss equivalence by Costello–Gwilliam B.6.0.11. Natural Wick conjugation transports the completed Čech diagram isomorphically. $\square$

**Important boundary:** The **ordinary** multiplication is also a cochain map for disjoint opens under the local diagonal BV differential, as shown in 024. The Wick multiplication (30.5) is generally a **different** quantum factorization structure because its cross contractions use the nonlocal Green kernel. We do not identify these two multiplication laws without a separate intertwiner.

## 4. Scale transport including zero, but only on the smooth domain

For $\epsilon,\eta\ge0$ define

$$
\mathcal R_{\epsilon\to\eta}=W_\eta W_\epsilon^{-1}.
\tag{30.6}
$$

The maps intertwine the Wick-twisted differentials and all factorization operations, satisfy the **strict cocycle** for every three scales, and preserve the formal filtration. In particular the positive-to-zero map exists on the smooth domain. The difference $P_\epsilon-P_0$ is compactly supported in relative coordinate, though it is not smooth at the diagonal. Its contraction against the specified **smooth** kernels is nevertheless defined and continuous.

The full distributional no-go of 028 remains valid: for coincident even–odd delta generators the positive-scale BV contraction is $\kappa(0)/\epsilon$, diverging as $\epsilon\to0$; the two-even kernel involving $\delta''$ also makes the Wick primitive diverge. **Neither example belongs to** the smooth test-kernel domain of this theorem.

## 5. Exact boundary and next work

| Obligation | Mathematical verdict |
| --- | --- |
| Smooth compact polynomial kernel domain closed under BV and Wick contractions | PROVED |
| UV convergence at every finite arity in the LF test-function topology | PROVED |
| Formal zero-scale Wick-corrected quantum prefactorization and smooth Weiss descent | PROVED |
| Scale cocycle extended to zero on the smooth domain | PROVED |
| Unrestricted compact-distributional UV limit | REFUTED by 028 |
| Microlocally enlarged distribution domain, interacting renormalization | OPEN |
| First-syzygy liquid Ext comparison for original coefficients | OPEN |

**Next mathematical obligation:** Prove closure of a genuinely larger microlocal distribution space under repeated diagonal BV contractions and Wick operations, or exhibit its first exact failure. Hörmander's wavefront transversality is only a condition for an **individual** diagonal pullback; full repeated-contraction and Weiss stability do not follow automatically. Separately address the first-syzygy liquid Ext comparison from Theorem 28.2. No Human Steward routine review is required.
