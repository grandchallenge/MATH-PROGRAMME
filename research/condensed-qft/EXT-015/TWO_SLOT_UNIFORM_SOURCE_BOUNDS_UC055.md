# EXT-015 REACH / UC055 — rapid-stable obstruction to two-slot family recovery

**Candidate disposition.** On the original real manifold axis with two physical slots, the admissibility conditions of 108 §8, 117 §7 and 123 §2 do not imply the history-quotient bounds needed by UC043, even after a uniform mixed-jet rapid correction. The example has one fixed bounded scalar factor and a fixed four-vertex history. The obstruction tests the entire evaluated family and covers every finite history in 126, including completed coefficients, hidden vertices, alternative presentations and diagonal jets.

## 1. Domain and frozen inputs

Use a nonempty physical interval, one real parameter interval at the coefficient singleton, and the original compact source stages and rapid relation in real liquid modules at the fixed exponent $0<p\leq1$. The example uses even slots and is exchange symmetric. The parameters are observed jointly with the positive regulator. The parameter point values alone lose information.

| Protected input at the CP276 cut | Git blob |
| --- | --- |
| [Heat blowups 096](FILTERED_NORMAL_ZERO_SCALE_EXTENSION_096.md) | ee15ed47d90123bdd958dcb4a93cd51b428c1702 |
| [Scalar heat stages 105](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | a8ce66ff0edec33e2aff299550fca2089d671033 |
| [Mixed sources and graph jets 108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| [Parameter domain 117](R1_WICK_DRESSED_QUANTUM_COMPARISON_117.md) | e95b1155ebb2018a80d2dc559560730fd7ea6594 |
| [Prior retained-family rule 123](RETAINED_FAMILY_DIFFERENTIABLE_LIQUID_AUDIT_123.md) | c5195a38414e3b45dbf75bb89b0db055ce01a5a2 |
| [Coefficient rows and the original recovery assertion 126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [Domain review 127](AGENT_CRITICAL_REVIEW_COMBINED_REALIZATION_127.md) | 74c47f1329d414fdf65f85cb3fdda8712852e65f |
| [Two-slot quotient-bound criterion UC043](TWO_SLOT_FAMILY_RECOVERY_UC043.md) | 56565632c13957190ead129ead0c6ef920ed5330 |

The old rule fixes a finite collection of actual source stages locally, along with uniform finite-order polynomial bounds for the evaluated mixed jets in a fixed spatial graph sector. The scalar stages are the original power/logarithmic stages. The construction below uses a single scalar factor with all of its seminorms constant in the parameter. The estimates of 126 ask in addition for local bounds and continuity of entire-history coefficient lifts. In particular an undifferentiated output jet of such a lift ranges over a bounded set in the complete stage on each compact parameter interval.

## 2. A necessary estimate on every original history

In output coordinates $c=(x+y)/2$ and $t=x-y$, choose a compact smooth centre cutoff $\chi(c)$ and a real even nonzero $\omega\in C_c^\infty(\mathbb R)$ supported where $1<|t|<2$. Define the physical test

$$
p_\epsilon(c,t)=\chi(c)\omega(t/\epsilon)\cos(t/\epsilon^2).
\tag{UC055.1}
$$

Shrink the regulator interval if necessary for these tests to be compactly supported in the physical patch. For each fixed finite order $s$, their physical $H^s$ norms grow at most by a finite power of $\epsilon^{-1}$. Thus pairing with them takes a uniform rapid error to a uniformly rapid scalar, using the fixed-order bound on the undifferentiated jet. The tests are physical test functions at each positive regulator. Their use is only a pairing with that finite-order error estimate.

**Lemma UC055.1.** For every fixed original history $h$, fixed complete graph and scalar stages, and requested power $J$, there is a continuous seminorm $P_{h,J}$ on its complete coefficient source $H_{h,s}$ for which

$$
\big|\langle e_{h,s}b(\epsilon),p_\epsilon\rangle\big|
 \leq \epsilon^J P_{h,J}(b)
\tag{UC055.2}
$$

for all sufficiently small $\epsilon>0$. The threshold can depend on the fixed history. The same bound holds with the quotient seminorm on its entire evaluated image.

**Proof.** First, a scalar stage on a fixed compact heat patch has a fixed $A$ such that every finite spatial derivative satisfies

$$
\sup_w|\partial_w^\alpha f_\epsilon(w)|
 \leq C_\alpha\,\epsilon^{-A-|\alpha|}Q_\alpha(f),
\tag{UC055.3}
$$

with a continuous stage seminorm $Q_\alpha$ and the same $A$ for all $\alpha$. To see the derivative scaling, the one-parameter maps $(\epsilon,w)\mapsto(\epsilon,w+\lambda\epsilon e_j)$ lift smoothly to the ordinary heat blowups. The map fixes the boundary downstairs pointwise, hence preserves each partition centre there. The lift of a smooth family preserving a centre is smooth by writing its normal map as $z\mapsto L(b,z,\lambda)z$ with $L$ invertible near the centre and taking radial and angular coordinates. After each blowup the lift preserves the strict lifts of the remaining centres, which are closures of the unchanged subsets of the old regulator boundary away from the previously blown centres. It also preserves each existing hypersurface. Thus the generator of the lifted family is a smooth b-vector field and equals $\epsilon\partial_{w_j}$ in the interior. This is a local use of ordinary radial blowup on the heat arrangement of 096 and 105. For background on the arrangement construction see [Kottke, Functorial compactification of linear spaces](https://arxiv.org/abs/1712.03902).

By the definition of a fixed stage 105 §8, all finite b-derivatives satisfy a common product of finite lower face weights, with different controlling seminorms for the different derivatives. Strict margin below each leading power absorbs logarithms. On a compact patch each heat hypersurface divides $\epsilon$, whose pullback is a positive unit times a product of positive powers of the incident defining functions. The product lower bounds therefore cost one finite power $\epsilon^{-A}$ independent of the number of b-derivatives. In the interior each $\partial_{w_j}$ costs $\epsilon^{-1}$ because the lifted vector fields leave $\epsilon$ fixed. Finite charts and compact physical cutoffs prove (UC055.3). The same argument applies on each smaller partition space.

Reduce one summand of (108.7) to its old block coordinates $w$. Transfer its finite derivatives and physical projection to the test before applying the partition inclusion. If the two retained slots use one old block, every derivative of the test vanishes there because the test has a positive-scale gap at $t=0$. If the two retained slots use distinct blocks, the retained difference is the linear function $t(w)=w_i-w_j$. Derivatives of the transported test produce finitely many factors with each sign of $\exp(ik t(w))$, where $k=\epsilon^{-2}$. The amplitude includes the scalar factor, the compact physical cutoffs, the actual density, the test centre cutoff and its rescaled annulus factor. Each term satisfies

$$
|\partial_w^\alpha B_\epsilon(w)|\leq
 C_\alpha\epsilon^{-A'-|\alpha|}Q'_\alpha(f)
\tag{UC055.4}
$$

with compact support in the old block variables. This follows from (UC055.3), the finite Leibniz formula and the finite powers $k$ and $\epsilon^{-1}$ already produced when transferring the derivatives. Those powers enlarge the fixed $A'$. Choose the compact support of the localization of the graph coefficient independently of $\epsilon$, equal to one on the shrinking test support for all sufficiently small $\epsilon$.

Write $\nu=dt$ in these coordinates. On the old partial diagonal $w_i=w_j$, both rays $\pm\nu$ are forbidden spatial conormals for the original R1 graph coefficient. By compactness of the physical support and closedness of its fixed cone, choose one narrow fixed tube about this partial diagonal and fixed open frequency cones about the two rays whose closures avoid the component's cone in that tube. Cut the graph coefficient to that fixed tube by a smooth cutoff equal to one on the test support. The localized coefficient $T'$ has an $H^{-s}$ bound and weighted Fourier $L^2$ bounds of every finite positive order on the two smaller frequency cones. These are continuous graph seminorm bounds from (108.1). They can be seen by applying a fixed Fourier cone cutoff after the physical localization. The properly supported order-zero operators localized there give the same estimates, with the smooth remainder controlled by $H^{-s}$. These estimates use the forbidden conormal of the partition joining just the two retained blocks, also at configurations with simultaneous hidden collisions.

For a simple tensor write the pairing as the Fourier integral of $\widehat T'(\xi)$ against $\widehat B_\epsilon(\pm k\nu-\xi)$, with the harmless Fourier convention constant. Split at $|\xi\mp k\nu|=\delta k$ for one small fixed $\delta>0$. On the inner part the frequency lies in the forbidden-ray cone, $|\xi|\asymp k$. The graph bound of order $N$ and the $L^2$ estimate of (UC055.4) bound this contribution by a product of seminorms times $\epsilon^{-A'}k^{-N}$. On the outer part $|\xi\mp k\nu|\gtrsim k+|\xi|$. Derivatives and compact support in (UC055.4) give

$$
|\widehat B_\epsilon(\eta)|\leq
 C_N\epsilon^{-A'-N}(1+|\eta|)^{-N}Q'_N(f).
$$

Pair with the global $H^{-s}$ bound by Cauchy–Schwarz. In old block dimension $d$, the remaining integral gives a factor at most $C_{N,s}k^{\max(s,0)+d/2-N}$ for sufficiently large $N$. With $k=\epsilon^{-2}$ this outer bound is at most a seminorm product times $\epsilon^{N-A'-2\max(s,0)-d}$. The two estimates achieve each $J$ by choosing finite $N$. This derives the distinct-block estimate before any integration over the hidden vertices and so includes arbitrary incident factors and coupled source tensors.

Each bound factors through finitely many seminorms on the respective fixed graph and scalar stages. By taking the projective seminorm and completing, it holds on the completed mixed tensors. Finite histories use finite sums of the bounds, and the actual evaluation kernel is annihilated by the pairing for all positive regulators. Taking the infimum over lifts yields (UC055.2) with the quotient seminorm. $\square$

## 3. A prior admissible family with one fixed scalar factor

Choose two disjoint compactly contained physical patches in the interval, one for the output centre $c$ and one for a hidden centre $d$. Place the output centre at $c_0$. The two forgotten vertices are $d+z/2$ and $d-z/2$. Choose compact cutoffs in the centre variables and differences so both two-vertex configurations stay in their indicated patches. Choose $\gamma(d)\in C_c^\infty$ with integral one. Choose real nonnegative $\rho\in C_c^\infty((1,2))$ with integral one and even $\zeta\in C_c^\infty$ supported where $1/2<|z|<3$, strictly positive on $\mathrm{supp}\rho$. Put

$$
\Lambda(\lambda)=\int\rho(v)\zeta(v/\lambda)\,dv.
$$

This smooth function is supported on a compact subinterval of $(0,\infty)$ and $\Lambda(1)>0$. Take $a_m=2^{-m}$ and disjoint parameter bumps $\beta_m$ supported in $|a-a_m|<a_m/8$ with $\beta_m(a_m)=1$ and $|\beta_m^{(j)}|\le C_j a_m^{-j}$. Let $r_m=r_*2^{-m^2}$ with $r_*>0$ sufficiently small for the physical cutoffs. On the parameter interval about zero define the actual two-slot distribution family

$$
u_{a,\epsilon}(c,t)
 =
 \delta(c-c_0)\,\omega(t/\epsilon)
 \sum_{m\ge1}\beta_m(a)\Lambda(\epsilon/r_m)\cos(t/r_m^2).
\tag{UC055.5}
$$

It is even in $t$. At every positive regulator only finitely many summands can be active, and all vanish near $a=0$ at that regulator. The centre distribution is fixed, so the mixed graph jets are genuinely compatible.

To obtain (UC055.5) from the original sources, use the identity source partition in the four old vertices, one proper projection forgetting the hidden pair, and the single fixed scalar factor $\omega(t/\epsilon)\zeta(z/\epsilon)$ with a compact cutoff equal to one on all the contributing supports. It is the product of two localized smooth compact normal profiles. Each pulls back from its two-vertex heat space by 105.4 and is in a fixed scalar stage by 105 §8. Their product and the compact fixed cutoff are in one fixed stage. In particular every scalar seminorm and every scalar face coefficient is independent of $a$. Use the actual graph coefficient

$$
T_a(c,t,d,z)
 =
 \delta(c-c_0)\gamma(d)\sigma(t)
 \sum_{m\ge1}\beta_m(a)r_m^{-1}\rho(z/r_m)\cos(t/r_m^2),
\tag{UC055.6}
$$

where $\sigma$ is a fixed compact cutoff equal to one on the active retained annuli. For each fixed parameter, including zero, this is a permitted coefficient in one fixed graph sector. It is compactly supported with wavefront only in the centre direction $(1,1,0,0)$. This direction has nonzero total covector sum and so avoids every forbidden partition conormal. Each formal parameter derivative of the expression is likewise a member of the same type of graph source, with $\beta_m$ replaced by the differentiated bump. These are actual source witnesses for each evaluated jet. The ordinary densities in $(c,t)$ and $(d,z)$ are the physical product densities since both absolute Jacobians are one. The substitution $z=r_m v$ makes the proper projection exactly (UC055.5).

For each mixed output jet $\partial_a^j\partial_\epsilon^k$, each fixed spatial derivative order $l$ of its smooth $t$ factor has a bound by a constant times a finite inverse regulator power. On an active term $\epsilon\asymp r_m$, so the parameter derivatives cost $a_m^{-j}\le C_j r_m^{-j}$, regulator derivatives cost at most $C_k r_m^{-k}$, and $l$ spatial derivatives cost at most $C_l r_m^{-2l}$. Taking a finite sum across the Leibniz terms gives one bound per request, uniformly on compact parameter intervals. Since the centre distribution is fixed, the finite Sobolev and corresponding fixed-cone graph estimates for the actual outputs follow from the compact smooth $t$ seminorms and the fixed distribution $\delta(c-c_0)$. Directly, in Fourier coordinates the centre factor has bounded transform, the off-cone region satisfies $|\xi_t|\gtrsim|\xi|$, and arbitrarily high decay in $\xi_t$ comes from finitely many derivatives of the smooth compact $t$ factor. Fixed physical localizations and properly supported off-cone cutoffs have the same estimates, as in 108.1. This checks the output graph-jet conditions with the same cone for all jets. The construction uses no escaping scalar index or support.

Here is a separate check of uniform physical asymptotics, including bounded sets of fixed allowed rescaled scalar multipliers. Such a multiplier and any finite spatial or mixed regulator derivatives have (UC055.3) with one fixed base order for the family of spatial derivative requests. A fixed physical test contributes finitely many derivatives at any stated depth. After taking each requested mixed jet of (UC055.5), pairing with such a multiplier and a physical test reduces to integration in $t$ at $c=c_0$. Each integration by parts in $t$ supplies $r_m^2$ from the oscillation. Derivatives of the remaining amplitude cost at most one inverse regulator power each, in addition to the fixed loss for the original jet and multiplier. On the active support $r_m\asymp\epsilon$. Hence any prescribed decay power follows by using finitely many integrations by parts, uniformly on bounded scalar and fixed test sets. The same check in the rescaled profile coordinate $v=t/\epsilon$ has oscillation frequency $\epsilon/r_m^2\asymp r_m^{-1}$ and gives arbitrarily high powers for fixed smooth normal-profile tests. All these coefficients are zero. Retained diagonal restrictions, when taken at positive scale, give zero with every derivative, by the annulus gap. These tests check the uniform scalar and graph bounds in the prior mixed admissibility rule. In particular the failure below cannot be produced by a fixed allowed scalar multiplier followed by taking a discontinuous finite coefficient, as in the weaker control of UC043 §4.

For each fixed parameter, the entire output vanishes for all sufficiently small regulators. For the joint family the implicit cutoff threshold depends on the parameter. In the prior rule there is no hypothesis of compactness in the bare coefficient graph topology of (UC055.6) before projection. Adding such a hypothesis to the dependence of the completed mixed coefficient is the source condition whose recoverability is at issue. The fixed scalar factor and the actual uniform mixed output estimates have been checked independently of that stronger condition.

## 4. Obstruction after every rapid correction

Use (UC055.1) with $\chi(c_0)=1$ and the same $\omega$. At $a=a_m$ and $\epsilon=r_m$, (UC055.5) gives

$$
\langle u_{a_m,r_m},p_{r_m}\rangle
 =
 r_m\Lambda(1)\int \omega(v)^2\cos^2(v/r_m)\,dv
 =
 C r_m+O(r_m^L)
\tag{UC055.7}
$$

for every chosen $L>1$, with $C=\Lambda(1)\int\omega(v)^2\,dv/2>0$. The second equality uses $\cos^2 b=(1+\cos(2b))/2$ and ordinary integration by parts on the compact smooth square. Hence the pairings are bounded below by a fixed positive multiple of $r_m$ for all large $m$.

Suppose 126.14 held for this family near $a=0$. After shrinking to a compact parameter interval about zero, a source-controlled representative has one continuous zero-order row in a fixed finite collection of complete histories and thus bounded coefficient seminorms there. Lemma UC055.1 gives pairings $O(\epsilon^J)$ for all $J$, uniformly in that interval, for this representative. The difference is a uniform fixed-order rapid error. By the finite-order norm of the tests (UC055.1) its pairings are also $O(\epsilon^J)$ for every $J$. This contradicts (UC055.7). The argument works after every local restriction about zero because it contains a tail of the $a_m$. It excludes every possible history with the same rapid correction rule, even if many terms cancel or a different analytic presentation is used. By (UC055.2) it also excludes the locally bounded history-quotient seminorm hypothesis of UC043 for any corrected representative. It uses the zeroth jet already and so tests the original all-mixed-jet relation without replacing it by a weaker pointwise relation.

This construction disproves local surjectivity on the original two-slot real parameter axis. It leaves the injective source-controlled comparison and the theorems on that source-controlled model in their original scope. No obstruction to an independently constructed larger-source functor or to a different locally defined integrable model is claimed. The original scalar stage, fixed-order negligible relation, and finite history conditions are used throughout. The proof uses explicit analytic bounds and no numerical fixture. Exact-source nonauthor review and protected admission are separate.
