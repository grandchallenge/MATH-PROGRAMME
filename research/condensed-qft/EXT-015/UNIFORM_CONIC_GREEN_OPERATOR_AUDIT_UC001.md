# EXT-015 REACH / UC-OP-001 — the heat-normal rank gate for a uniform conic Green source operator

**Primary mathematical disposition: BOUNDED MICROLLOCAL RANK CRITERION AND AN ACTUAL PARTITION-STRATUM COUNTEREXAMPLE.** A fixed conic Fourier component is smoothed at every positive regulator, with continuous finite polynomial Sobolev estimates, whenever the Gaussian heat directions are jointly elliptic on its frequency cone. A legal nonidentity partition-inclusion source exhibits an explicit forbidden conormal annihilated by a single chosen heat direction, and thus refutes a naive universal one-edge promotion of the successful first Green conic split. These assertions concern positive-interior smoothing and the original moderate distribution envelope. They do **not** prove fixed105 polyhomogeneous all-corner source membership, an operator on the full completed108 image, universal150.L, residual W acyclicity or original R3.

## 1. Frozen original contracts and the bounded question

The immutable existing source contracts are original105 Gaussian/Wick full collision scalar stages (Git blob a8ce66ff0edec33e2aff299550fca2089d671033), original108 complete mixed coefficient histories, legal partition inclusions and finite-order uniform rapid subobject (blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6), and original126 source-controlled parameter rows (blob 5b05c6147d237ca1d22e4dcbce9262b0f038c163). The particular positive conic first-core construction [JOINT_DEFECT_SOURCE_AUDIT_195.md](JOINT_DEFECT_SOURCE_AUDIT_195.md), protected Git blob fc0fddb678f0cc0c1b9764bb449ab6d9150b33d0, and corrected critical review [AGENT_CRITICAL_REVIEW_JOINT_DEFECT_196.md](AGENT_CRITICAL_REVIEW_JOINT_DEFECT_196.md), protected blob 6c9607eb3db55153e999587e6546931244ef2150, are native-merged in PR3371 at 1d741353367997f51d0789ad7049ded1c0712c9e. The new programme custody checkpoint CP222 is proposed separately in PR3375 and is not presumed protected here.

The corrected conic195 decomposes the one singular ambient distribution $e(r)\delta_0(t)$ in two relative coordinates, absorbs the directions forbidden for the original R1 coefficient into a partially heat-smoothed scalar, proves its complete105 all-corner stage, and thereby produces a legal finite source for that specific first core. The new obligation is to test the **uniform microlocal applicability gate** before inferring any analogous construction on a general legal finite original108.7 history, especially nonidentity partition inclusions and tangent R1 covectors.

We first prove the gate in standard real Sobolev distribution spaces, without silently promoting ambient moderation to a fixed original105 scalar-stage estimate.

## 2. An exact finite-rank ellipticity test

Let $X=\mathbb R^m$ with Fourier variable $\zeta\in X^*$. Fix directions $v_1,\ldots,v_J\in X$, positive constants $a_j$, and the nonnegative heat quadratic form

$$
E(\zeta)=\sum_{j=1}^J a_j(v_j\cdot\zeta)^2,
\qquad
L\zeta=(\sqrt{a_j}\,v_j\cdot\zeta)_{j=1}^J.
\tag{UC1.1}
$$

The corresponding evaluated Gaussian smoothing is the Fourier multiplier $\exp[-\epsilon^2E(\zeta)/2]$, i.e. a finite product of **convolutional** heat operators in the listed directions. This is not an assertion that every original105 Gaussian *multiplication* edge or every mixed108 history factorizes in this form.

Let $C\subset X^*\setminus\{0\}$ be a fixed closed conic set whose unit-sphere section is compact. Let $q$ be a fixed bounded smooth symbol of order zero, vanishing near frequency zero and with its high-frequency support in $C$. Set

$$
\mathcal H_\epsilon^qT
=\mathcal F^{-1}\left[
q(\zeta)e^{-\epsilon^2E(\zeta)/2}\widehat T(\zeta)\right].
\tag{UC1.2}
$$

**Proposition UC1.1 (heat-normal rank criterion).** The two conditions are equivalent:

1. $C\cap\ker L=\varnothing$.
2. There is a constant $c>0$ with $E(\zeta)\ge c|\zeta|^2$ for every $\zeta\in C$.

Here the first condition is interpreted on the punctured cone, equivalently $C\cap\ker L\cap S^{m-1}=\varnothing$.

**Proof.** The nonnegative continuous function $E$ on the compact set $C\cap S^{m-1}$ has a strictly positive minimum precisely when it has no zero there. But $E(\zeta)=0$ if and only if $L\zeta=0$. Its degree-two homogeneity extends the minimum to the cone. The empty cone is trivial. $\square$

For a finite set of collision partitions $\mathcal P$, let $C_P=N^*\Delta_P$ be each linear partition-diagonal conormal subspace (with the zero covector excluded). The criterion for ellipticity simultaneously on their entire conormal union is the **finite exact rank test**

$$
\operatorname{rank}(L|_{C_P})=\dim C_P
\quad\text{for every }P\in\mathcal P.
\tag{UC1.3}
$$

Testing only one generating vector per partition is insufficient: $L$ must be injective on every linear combination in each conormal subspace. For finite $\mathcal P$, the positive constants from Proposition UC1.1 have a common strictly positive lower bound. This is a necessary algebraic gate on any proposed finite heat-direction cover of those collision conormals, not a source-completion theorem.

## 3. Uniform positive-regulator smoothing on fixed ambient stages

**Theorem UC1.2 (source-stage-compatible polynomial *moderation*, not scalar PHG).** Suppose the rank criterion holds on the support cone of $q$, and let $s\ge0$. For every $T\in H^{-s}_K(X)$ with a fixed compact support $K$, every multi-index $\beta$, regulator derivative order $k\ge0$ and compact output patch $K'$, the actual family UC1.2 is smooth at each $\epsilon>0$ and satisfies

$$
\sup_{x\in K'}
\left|\partial_x^\beta\partial_\epsilon^k
\mathcal H_\epsilon^qT(x)\right|
\le C_{\beta,k,s,K'}\,
\epsilon^{-(s+|\beta|+m/2+k)}
\|T\|_{H^{-s}},
\qquad0<\epsilon\le\epsilon_0\le1.
\tag{UC1.4}
$$

The estimate extends continuously to any bounded set or smooth parameter family in a **fixed** $H^{-s}_K$ stage; parameter derivatives are bounded by the same formula applied to the actual input derivatives. A fixed compact output multiplier preserves the estimates and restores proper output support. It also extends to moderate evaluated source curves with fixed negative-order rows by ordinary finite Leibniz bounds.

**Proof.** Fourier inversion and Cauchy–Schwarz against the defining $H^{-s}$ norm give

$$
\left|\partial_x^\beta\partial_\epsilon^k
\mathcal H_\epsilon^qT(x)\right|
\le C\|T\|_{H^{-s}}
\left(\int
\langle\zeta\rangle^{2s}|\zeta|^{2|\beta|}
|\partial_\epsilon^k e^{-\epsilon^2E(\zeta)/2}|^2
|q(\zeta)|^2\,d\zeta\right)^{1/2}.
\tag{UC1.5}
$$

For any fixed $k$, differentiation of the exponential yields a finite sum of terms $\epsilon^{2j-k}E(\zeta)^j e^{-\epsilon^2E(\zeta)/2}$, where $j$ is bounded by $k$. On the support of $q$, $E(\zeta)\ge c|\zeta|^2$, and the polynomial factors are absorbed into a weaker Gaussian:

$$
|\partial_\epsilon^k e^{-\epsilon^2E/2}|
\le C_k\epsilon^{-k}e^{-\epsilon^2E/4}
\le C_k\epsilon^{-k}e^{-c\epsilon^2|\zeta|^2/4}.
\tag{UC1.6}
$$

The radial weighted integral in UC1.5 is at most a constant times $\epsilon^{-2s-2|\beta|-m-2k}$. Taking its square root proves UC1.4. The compact-support and parameter claims use the same finite continuous seminorm bound. For a moderate input curve, differentiated products involve only finitely many input rows. No inverse heat map or source-stage closure is used. $\square$

This result is **more than a pointwise positive-regulator smoothing observation**: it supplies a finite operator seminorm bound on every fixed $H^{-s}$ stage and for all regulator derivatives. But the original105 scalar space requires **fixed compatible power/logarithmic index families and all differentiated recursive heat-collision corner remainders**, not only these polynomial bounds. Theorem UC1.2 does not supply those additional properties and does not assert an original completed108.6 source map or the full original126.14 family-recovery contract.

## 4. A legal partition input defeats the one-heat-direction universalization

Take $m=3$, coordinates $(r,t,u)$, and **one** heat direction $v_t=(0,1,0)$. Then $E(\xi_r,\eta,\xi_u)=\eta^2$. Consider the partition diagonal $\Delta=\{r=u\}$, whose conormal contains the nonzero rays

$$
\zeta_\tau=(\tau,0,-\tau),\qquad\tau\ne0,
\quad E(\zeta_\tau)=0.
\tag{UC1.7}
$$

Choose nonnegative fixed compact smooth $\chi(r,u)$ that equals one near the origin and $\psi(t)$ nonzero near0. Define the genuine compact distribution

$$
T(r,t,u)=\chi(r,u)\psi(t)\delta_0(r-u).
\tag{UC1.8}
$$

This is not an original R1 coefficient on all three independent vertices: its wavefront **contains** the forbidden $r=u$ conormal. But it is an actual **legal nonidentity partition-inclusion source** of original108.7, with smooth block coefficient, zero insertion derivative and fixed compact physical support. No illegal product of singular R1 factors is invoked.

The heat operator in $t$ has the exact output

$$
\mathcal H_\epsilon^{t}T
=\chi(r,u)\delta_0(r-u)
(\kappa_\epsilon*_t\psi)(t).
\tag{UC1.9}
$$

The multiplier in the $t$ slot is smooth and strictly nonzero near some point on the diagonal, so the output still has conormal wavefront $\zeta_\tau$ **for every $\epsilon>0$**.

Let $q(D)$ be a fixed high-frequency conic cutoff equal to one on a neighborhood of these two conormal rays, as would be required to remove them from a proposed R1 “good” part. Then $(1-q(D))T$ is smooth microlocally at those rays, and convolution in $t$ does not introduce their conormal singularities. Because fixed Fourier multipliers commute,

$$
q(D)\mathcal H_\epsilon^t T
=\mathcal H_\epsilon^tT
-\mathcal H_\epsilon^t(1-q(D))T
\tag{UC1.10}
$$

still has the nonzero $r=u$ conormal. It therefore **cannot** be an interior-smooth scalar105 heat coefficient. The complementary “good” distribution cannot retain the same forbidden conormal and simultaneously qualify as an original R1 coefficient.

**Proposition UC1.3 (one-edge obstruction).** A blanket operation that splits arbitrary original108 partition-inclusion sources into a permitted original R1 coefficient plus an interior-smooth scalar by applying a fixed conic cutoff and only the one hidden heat direction $t$ is impossible. The counterexample UC1.8 is itself a legal partition source. The no-go is for this attempted **uniform source transformation**, not for source membership of the input, which is already admitted.

In the protected conic195 example there are only two relative variables $(r,t)$; the bad R1 rays are $(\tau,-\tau)$, and the $t$ heat direction has nonzero pairing with every such ray. The heat-normal rank gate is therefore passed on its specific bad conic support. In the three-variable example the heat direction misses a valid partition conormal. This is an exact structural distinction, not a contradiction between the positive195 and the new negative result.

## 5. Consequences for a full mixed source operator and exact-rank verification

A proposed heat-direction family can only smooth a chosen collection of partition conormals uniformly when it passes UC1.3 on **each entire conormal subspace**. The finite rank gate is checkable by exact rational linear algebra. The included control fixture [conic_heat_rank_gate_uc001.py](fixtures/conic_heat_rank_gate_uc001.py) verifies the two-coordinate positive case, the three-coordinate degeneracy and a higher-dimensional conormal example where testing basis vectors separately gives a false positive. Its PASS result is an exact algebraic regression, not a substitute for Theorem UC1.2 or original105 scalar PHG proof.

Passing the rank gate guarantees finite continuous positive-interior Sobolev estimates **only** for actually factorized convolutional heat histories. A full extension to original108 must still prove: correct factorization after actual scalar multiplication, noncharacteristic R1 restrictions for every nonidentity partition/jet, all complete105 collision corner indices and lower auxiliary weights, fixed supported proper-density pushforward, joint source-stage continuity through completed projective tensor products, and actual source-controlled126 row maps. Each is still an independent proof obligation. A finite collection of rank-passing heat directions is not by itself a source-inverse, a contracting homotopy or an original R3 comparison.

## 6. Scientific decision boundary

| Question | Bounded result |
| --- | --- |
| Finite conormal heat-ellipticity gate | Exact rank equivalence UC1.3 |
| Positive-interior conic Gaussian smoothing on fixed $H^{-s}$ stages | Uniform polynomial bound with all derivatives UC1.4 |
| One heat edge covers every partition conormal in three relative coordinates | FALSE; actual legal partition UC1.8 refutes it |
| Arbitrary Gaussian multiplication source factorizes into directional convolution | NOT ASSUMED and not established |
| Original105 all-corner scalar stages for general conic inputs | OPEN |
| Full original108 mixed Green operator, universal150.L, residual W acyclicity, original R3 and full126.14 | OPEN |

**Next executable scientific condition:** formulate a typed finite heat-direction/partition-conormal incidence matrix for each proposed original108 history; reject histories failing the kernel intersection test before investing in a complete all-corner scalar proof. For rank-passing cases, prove the actual original105 source-stage realization and all collision-corner estimates separately. Source-controlled parameter rows and the original rapid ideal must remain unchanged.

This is a primary scientific candidate for source-locked independent logical critic UC-OP-002, bounded ledger UC-OP-003, exact-head CI and native protected admission. The logical reviewer may share the same model/account but must not be described as an independent external mathematical certification. No programme terminal claim follows.
