# EXT-015 REACH / 160 — role-scoped mathematical critic of non-spectator Gaussian W test 159

**Verdict: BOUNDED ACCEPT after material correction of labelled versus symmetric W; universal source lift 150.L OPEN.**

## 1. Exact locked sources and review provenance

| Source | Exact Git blob or commit |
| --- | --- |
| [Primary 159](NONSPECTATOR_GREEN_GAUSSIAN_R1_TEST_159.md) | 555088f3da2c87dc02304dcf44b2738510f65062 |
| Primary exact head in [PR #3300](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3300) | f20a103678d3f6aa758f91cf46e294761d934aba |
| [Exact test fixture](fixtures/nonspectator_green_controls_159.py) | eaacdd57d77e9cbaddef23f697fe7b170aefbc8b |
| Exact-head substantive GitHub review | COMMENTED, ID 5891645324; not a nonauthor APPROVED review |
| Mixed source 108 / scalar heat 105 | 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 / a8ce66ff0edec33e2aff299550fca2089d671033 |
| Diagonal extraction 147 / residual split 150 | 89b3d4a835f3750114e983854585e33d8184cb1f / 03deca9212a9bea56743e482e5cb79edb46b9d7f |
| Prior bounded accepted 156/157/158 | fb683d69b5536df98805d104c9640234a486a2dd / f9f195b7e852b716304c060a40a23b14bac7e410 / 2f910446b1027be1e28ff13bb901652dd806b355 |

The review is a fresh **logical Verifier V160 and Adversary A160 pass** inside the same ChatGPT system and GitHub identity as the author, in accordance with GCL-AGENT-STAFFING-001. It is not an independently authenticated human or external mathematical certificate. The GitHub COMMENT review records exact source provenance; it is not the source of mathematical truth.

**Material correction:** Initial primary wording incorrectly called an unsymmetrized labelled two-slot joint-kernel input an element of the symmetric residual W of (150.8a). The current exact reviewed source corrects this by constructing the degree-zero slot average and computing its additional Green term. The uncorrected assertion is REJECTED; the corrected proof is the subject of this verdict.

## 2. V160 — source legality and exact Green identity

With $\rho\in C_c^\infty(U)$, $\rho(0)\ne0$, put $T(y,z)=\delta_0(y)\rho(z)$. Every nonzero wavefront covector of $T$ has form $(\eta,0)$, whereas the forbidden diagonal conormal is $(\tau,-\tau)$. This remains true at $(0,0)$. Thus multiplying $T$ by the *admitted* Gaussian scalar $\kappa_\epsilon(y-z)$ gives a legal original identity-partition mixed history, with no overlapping R1 product.

The evaluated input is $v_\epsilon(y,z)=\delta_0(y)w_\epsilon(z)$ with $w_\epsilon=\rho\kappa_\epsilon$. Its two partial $y$ moments are $w_\epsilon,0$. Since $G=e-e*b_0$ and $G''=\delta_0-b_0$, the normalized primitive is exactly

$$
h_yv_\epsilon(x,z)=G(x)w_\epsilon(z).
\tag{160.1}
$$

All convolutions use the ordinary $dy$ physical density. Both affine moments of $\delta_0-b_0$ vanish, making $G$ compact; its derivative retains the nonzero jump of $|x|/2$ at the origin.

**V160-A PASS:** a genuine integrated-coordinate R1 singularity, legal Gaussian scalar and exact compact whole-distribution primitive.

## 3. V160 — labelled kernel, actual symmetric W and both primitives

The already admitted partial-moment and singleton bump-reinsertion maps of 150 §5 provide a finite source representation of $Qv_\epsilon$ for $Q=(1-B_y)(1-B_z)$. Write $w_\epsilon^\circ=(1-B_z)w_\epsilon$. The labelled element is

$$
v_\epsilon^{W,\mathrm{lab}}
=(\delta_0-b_0)(y)\,w_\epsilon^\circ(z).
\tag{160.2}
$$

Its four labelled affine moments vanish, and the intrinsic labelled extraction $P$ vanishes because every composing history has distinct retained blocks. It does **not** automatically belong to the symmetric object W. The **source-admitted** symmetric element is instead

$$
v_\epsilon^{W,\mathrm{sym}}(y,z)
=\tfrac12\left[v_\epsilon^{W,\mathrm{lab}}(y,z)
+v_\epsilon^{W,\mathrm{lab}}(z,y)\right]\in W^0.
\tag{160.3}
$$

Its limit $\rho(0)(\delta_0-b_0)\boxtimes(\delta_0-b_0)$ is nonzero, so it is a genuine nonrapid degree-zero element. That alone gives **no** nonzero cohomology class.

Let $H_\epsilon=e*w_\epsilon^\circ$, compact and smooth at every positive scale because $w_\epsilon^\circ$ is smooth compact with zero affine moments. Then the two exact *ambient* Green formulas are

$$
h_yv_\epsilon^{W,\mathrm{lab}}(x,z)=G(x)w_\epsilon^\circ(z),
\quad
h_yv_\epsilon^{W,\mathrm{sym}}(x,z)
=\tfrac12\left[
G(x)w_\epsilon^\circ(z)+H_\epsilon(x)(\delta_0-b_0)(z)
\right].
\tag{160.4}
$$

The second summand is indispensable. Neither formula is *a priori* an output legal-source representation. No contraction on W is inferred.

**V160-B PASS:** proper symmetric category and exactly sourced residual input; earlier type conflation corrected.

## 4. V160 — zero-regulator conormal trap with exact Gaussian limits

For $\epsilon>0$, both $w_\epsilon^\circ$ and $H_\epsilon$ are smooth. The labelled output has possible singular covectors only $(\xi,0)$, and the symmetric output is the sum of a pure-$x$ and a pure-$z$ wavefront. Neither intersects the pure diagonal conormal $(\tau,-\tau)$ with $\tau\ne0$.

For every compact test $\varphi$, Gaussian Taylor expansion is

$$
\langle w_\epsilon,\varphi\rangle
=\sum_{n=0}^{N}
\frac{\epsilon^{2n}}{2^n n!}
(\rho\varphi)^{(2n)}(0)+O(\epsilon^{2N+2}),
\tag{160.5}
$$

where the remainder uses finitely many test derivatives and retains the appropriate finite-order bounds under fixed regulator differentiation. Consequently $w_\epsilon^\circ\to\rho(0)(\delta_0-b_0)$ and $H_\epsilon\to\rho(0)G$ in compact distributions. Both the labelled and symmetric primitive have the same limit

$$
\rho(0)G(x)(\delta_0-b_0)(z).
\tag{160.6}
$$

At $(x,z)=(0,0)$ the external tensor of the cusp $G(x)$ and the delta singularity in $z$ has $(\tau,-\tau)$ in its wavefront: localized transforms have a nonrapid inverse-quadratic $x$ tail and a nondecaying delta $z$ transform. This does not contradict 108; its boundary coefficients can themselves be distributions.

**V160-C PASS:** fixed-positive-regulator wavefront avoidance does **not** imply diagonal-conormal avoidance of the leading boundary coefficient, including for a genuine symmetric W source.

## 5. A160 — adversarial source-lift tests and sharp limits

**Illegal augmented R1 shortcut.** The candidate three-slot coefficient $G(x)\delta_0(y)\rho(z)$ has wavefront $(\tau,-\tau,0)$ at $x=y=0$, a forbidden conormal to the partition $\{x,y\}$ with $z$ singleton. It cannot be inserted as an R1 input simply to keep the original Gaussian edge. This does not reject other legal hidden-variable constructions.

**No-hidden, spectator-regular strict-face shortcut.** Choose separated rectangles $I\times J$, where $I$ lies in a nonzero smooth portion of $G$ away from zero and $J$ contains zero. For a fixed finite sum of no-hidden, identity-partition, two-slot scalar-PHG/R1 histories whose R1 coefficient is smooth in spectator $z$ on this rectangle, all scalar heat-stage coefficients at the *strict regulator face* are smooth tangentially, and the completed R1 source coefficients are smooth in $z$ with values in distributions in $x$. Hence the actual limit, if it exists, is smooth in $z$ after cancellation of divergent powers and logarithms. The labelled primitive tends to (160.6), which contains a nonzero delta in $z$ on $I\times J$. It cannot belong to this **restricted source template**.

The **symmetric** primitive has a positive-regulator delta in the second summand of (160.4), so the spectator-regular no-go is **not** claimed for it. Hidden vertices, other R1 cones, overlapping-stratum cancellation and all other allowed finite histories are untested. In particular, neither result proves general nonmembership in $\mathcal P_2$ or positive cohomology of W.

**A160 PASS:** both narrowly quantified obstructions, with all general source nonmembership claims withheld.

## 6. Finite controls, exact execution and disposition

The exact fixture blob eaacdd57d77e9cbaddef23f697fe7b170aefbc8b executed on the CHAD OS account with exit zero, capture ID 8d601df9516647cba466cee673a41c0d: 242 five-site inputs, 26,620 exact labelled/symmetric Green pairings, 234 nonzero W projections and 81 polynomial Gaussian moment tests. This is finite algebra only, not independent authenticated mathematical certification or a microlocal proof.

| Claim | Final critic decision |
| --- | --- |
| Legal Gaussian input and whole compact primitive | ACCEPT |
| Labelled kernel and corrected symmetric W source | ACCEPT after correction |
| Positive-scale avoidance / boundary diagonal-conormal emergence | ACCEPT |
| Direct hidden-anchor R1 factorization | REJECT, forbidden partition conormal |
| No-hidden spectator-regular two-slot output template | REJECT, strict-face obstruction for **labelled** output |
| Every existing mixed-source history and full lemma 150.L | **OPEN** |
| Residual W acyclicity; original R3, 126.14, higher weights and M5/R4 | **OPEN** |

**Canonical bounded verdict:** BOUNDED_ACCEPT__SYMMETRIC_W_BOUNDARY_CONORMAL__RESTRICTED_LIFT_OBSTRUCTION__150L_OPEN.

This critic document is not itself an acceptance ledger or protected merge. Source 159 requires separate protected admission/readback, ledger 161 and CP186 reconciliation. The next research input must confront the permitted hidden-source and genuinely non-spectator R1 cones, not reassert an illegal augmented Green factor.
