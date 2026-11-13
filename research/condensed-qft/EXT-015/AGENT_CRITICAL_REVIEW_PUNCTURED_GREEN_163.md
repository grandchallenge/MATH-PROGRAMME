# EXT-015 REACH / 163 — critical mathematical review of punctured Green source lifting

**Verdict: BOUNDED ACCEPT of the exact punctured completed-source construction and finite Wick-jet negative control. The joint corner and universal 150.L remain OPEN.**

## 1. Exact source and logical reviewer identities

| Item | Identity |
| --- | --- |
| [Primary 162](LEGAL_HIDDEN_NONSPECTATOR_GREEN_SOURCE_AUDIT_162.md) | Git blob 20febc0e1196990addf446f0054f5e9e563ba615 |
| Exact [PR 3305](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3305) head | 5ae41e1a20dc304a1e62bc8409286d971f7733d3 |
| [Finite fixture](fixtures/hidden_corner_localization_controls_162.py) | Git blob 3bc21b06ffdebf3d06a3e93429b9767b6e49df20 |
| Native exact-head mathematical review | GitHub review 5892870101, COMMENTED by same account; not a nonauthor APPROVED |
| Scalar heat source 105 and mixed source 108 | a8ce66ff0edec33e2aff299550fca2089d671033 / 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| Full one-retained-slot source homotopy 141 | de6b608c8def91dd0b8b2d98fe410348ac92a17d |
| Green primitive and missing 150.L | 03deca9212a9bea56743e482e5cb79edb46b9d7f |
| Corrected non-spectator 159, critic 160 and ledger 161 | 555088f3da2c87dc02304dcf44b2738510f65062 / c11d08c17b5819a8042cc816520b920ede022ffa / eed5790361f58c6724bfc2c53481b064febdc5d4 |

V163 is a fresh logical **Verifier** pass, which independently reconstructs the positive source transformations. A163 is the **Adversary** pass, which checks source cone exclusions, all-corner indices and the scope of the no-go argument. They share the same ChatGPT/GitHub identity and general model context as the author. They are logically different tasks, **not** separately authenticated people, agents, mathematical peer referees or MATHCERT. The substantive GitHub comment does not supply external certification.

## 2. V163 — the exact prerequisite from the admitted one-slot theorem

The admitted two-slot history $\delta_0(y)\rho(z)\kappa_\epsilon(y-z)$ properly projects by forgetting $y$ to $w_\epsilon(z)=\rho(z)\kappa_\epsilon(z)$, with no Jacobian adjustment. Partial scalar moments and smooth bump reinsertion from 108/150 give the one-slot source $w_\epsilon^\circ=(1-B)w_\epsilon$. Because it has two vanishing affine moments, the *already proved* one-retained-vertex theorem 141 §§4–6 supplies an actual finite completed one-slot source for $H_\epsilon=e*w_\epsilon^\circ$. Its source maps preserve actual equality, fixed cone stages, rapid relations and compatible parameter derivatives. This use of 141 does not invoke the missing two-retained-vertex theorem 150.L.

Smooth singleton reinsertion applies to any fixed smooth compact function $g$, by the same completed graph tensor and zero-added-covector argument as the specific moment bumps in 150 §5. Inserting a singular anchor delta by this rule would be invalid; 162 does not do so.

**V163-A PASS:** complete one-slot provenance and fixed-stage continuity for both $w_\epsilon^\circ$ and $H_\epsilon$.

## 3. V163 — full scalar asymptotics on the strict patches

For the actual Gaussian moments

$$
M_{j,\epsilon}=\int t^j\rho(t)\kappa_\epsilon(t)\,dt
\sim\sum_{n\ge0}
\frac{\epsilon^{2n}}{2^n n!}
\partial_t^{2n}[t^j\rho(t)]\big|_{t=0},
\tag{163.1}
$$

the compact Taylor remainder is uniformly controlled by finitely many $\rho$ and test seminorms under all fixed regulator and parameter differentiations. On the support of $1-\beta(z)$, which is a positive distance from zero, the first part $\rho(z)\kappa_\epsilon(z)$ of $w_\epsilon^\circ$ is exponentially flat in every derivative. The remaining moment-bump terms occupy one fixed even-power regulator index family, saturated by all ordinary nonnegative integer shifts at the full heat faces after the permitted b-map pullback. The flat tail is retained as an actual coefficient.

Away from the anchor in $x$, the Green kernel is affine on the Gaussian core:

$$
e(x-t)=e(x)-\tfrac12\mathrm{sgn}(x)t
\qquad (|t|<|x|).
\tag{163.2}
$$

The complementary Gaussian tail is exponentially flat, even under fixed $x$ and regulator derivatives. Thus $(1-\alpha)H_\epsilon$ is a compact smooth scalar polyhomogeneous family, with coefficients $G(x)M_0-[C_1(x)+\mathrm{sgn}(x)/2]M_1$ and an actual flat remainder. It is not claimed to be scalar-polyhomogeneous across $x=0$. The primary includes **fixed passive-coordinate cutoffs** to make its two-slot scalar representatives compact; without these, the fixed-source assertion would be inadequately specified.

**V163-B PASS:** exact scalar-stage membership on both complementary strict regions, including all-corner integer-shift saturation and finite source seminorm estimates.

## 4. V163 — four legal histories, completed source bounds and exact equality

Let $u=\delta_0-b_0$, $G=e-C_0$, and let $F_{\mathrm{lab}}=G(x)w_\epsilon^\circ(z)$ and $F_{\mathrm{sym}}=[G(x)w_\epsilon^\circ(z)+H_\epsilon(x)u(z)]/2$. Take $\alpha,\beta$ smooth compact, equal to one near zero. The algebraic identity $1-\alpha(x)\beta(z)=(1-\alpha(x))+\alpha(x)(1-\beta(z))$ produces exactly four terms:

| Evaluated summand | Admitted source mechanism |
| --- | --- |
| $(1-\alpha)G\,w_\epsilon^\circ$ | One-slot $w_\epsilon^\circ$ plus smooth compact singleton $(1-\alpha)G$ |
| $(1-\alpha)H_\epsilon\,u$ | Two-slot identity history: scalar stage on the strict face away from the $x$ anchor and R1 with pure $z$ covectors |
| $\alpha G(1-\beta)w_\epsilon^\circ$ | Two-slot identity history: scalar stage on the strict face away from the $z$ anchor and R1 with pure $x$ covectors |
| $\alpha H_\epsilon(1-\beta)u$ | One-slot $H_\epsilon$ plus smooth singleton $-(1-\beta)b_0$ |

In the second and third terms, R1 covectors with only one nonzero coordinate cannot be pure two-slot diagonal conormals. The scalar inputs are in existing 105.5 fixed complete stages; the 108.6 projective tensor product and the normal topology control all requested coefficient derivatives. In the first and fourth terms, the smooth singleton map from 150 §5 and the one-slot map from 141 give a fixed finite source list. No step forms the illegal joint R1 coefficient $G(x)\delta_0(y)$. The cutoffs and density maps are fixed and the geometric/source index lists are independent of relaxed graph orders in all genuine 126 derivative rows.

All four equations hold as **actual positive-scale distribution identities**, before the rapid quotient. Their sum proves the claimed source status of $(1-\alpha\beta)F_{\mathrm{lab}}$ and $(1-\alpha\beta)F_{\mathrm{sym}}$.

**V163-C PASS.** This is a local, cutoff-dependent source lift. It is not an equivariant two-slot global contraction: the cutoff need not be invariant under slot exchange, and the output of $h_y$ is a labelled component in any case.

## 5. A163 — finite Wick-jet repair fails even in weak distributions

The heat semigroup identity $P_\epsilon=e*\kappa_\epsilon$ gives the strong distribution expansion

$$
P_\epsilon-e\sim
\sum_{n\ge1}
\frac{\epsilon^{2n}}{2^n n!}
\delta_0^{(2n-2)}.
\tag{163.3}
$$

For any prescribed finite point-jet bound $J$, choose an even $m>J$ and a *fixed* compact test equal to $x^m/m!$ near the origin. Every counterterm supported on $x=0$ of normal derivative order $\le J$ pairs to zero with that test, regardless of its regulator-dependent spectator distribution coefficient. The first nonzero term from (163.3) occurs at order $\epsilon^{m+2}$; the spectator $w_\epsilon^\circ$ tends to $\rho(0)(\delta_0-b_0)$, which has a nonzero pairing with a suitable fixed spectator test $\psi$. The coefficient equals $\rho(0)\langle\delta_0-b_0,\psi\rangle/[2^{m/2+1}(m/2+1)!]$ and is nonzero. Hence the corrected difference cannot be rapid even in the weakest distributional test sense.

**A163 PASS for the exact quantifiers.** This disproves only the ansatz of *Gaussian Wick replacement plus a fixed finite list of point-supported $x$ jets*. It does not disprove every existing completed scalar coefficient with infinitely many compatible asymptotic orders or every other legal hidden history.

## 6. Hostile limits, finite controls and decision

The cutoff complement $\alpha(x)\beta(z)F$ is **not** represented or excluded; the work does not establish a support theorem for a quotient sheaf. It only shows that every chosen punctured cutoff belongs to the actual source class. The scalar stages proved in §3 explicitly avoid the corresponding absolute anchor and cannot be extended across that anchor by an unargued continuity assertion. The finite Wick-jet no-go cannot be promoted to all finite 108.7 histories. Universal 150.L, residual W acyclicity, original R3, full family recovery126.14, higher weights and M5/R4 remain OPEN.

The committed exact fixture SHA 3bc21b06ffdebf3d06a3e93429b9767b6e49df20 was fetched and executed on the CHAD OS account: capture ID e4547718e3184ebf94c9879b5162a33a, exit zero, 242 inputs, 26,620 paired cutoff identities, 234 nonzero moment projections and 12 finite-jet controls. It is a finite algebra regression, **not** a source-topology or microlocal certificate. This execution is OS_ACCOUNT_ONLY, not independently authenticated review.

**Canonical bounded verdict:** BOUNDED_ACCEPT__PUNCTURED_ACTUAL_SOURCE__FINITE_WICK_POINT_JETS_NOT_RAPID__JOINT_ANCHOR_CUSP_OPEN.

The source-bound critic role is complete. Protected source admission of primary 162, protected admission of this review and ledger 164, and CP187 continuity remain distinct documentary obligations. The next scientific task must address the simultaneous $(x,z)=(0,0)$ corner with a legal complete mixed source or an exhaustive restricted nonmembership invariant.
