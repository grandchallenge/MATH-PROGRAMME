# EXT-015 REACH / 192 — zero-energy weighted means and a genuine disconnected Wick source

**Disposition: bounded mechanism and obstruction audit; full first-core membership remains OPEN.** A Gaussian hidden mean preserves the effective R1 cone only after removing a uniformly rapid tail. A static-target regularity argument makes that weaker result sufficient for an exact terminal-source obstruction, without requiring a graph limit at regulator zero. A different, actual disconnected Wick history has the same weak limit as the target and a nonrapid joint-corner defect. Thus a proposed invariant based only on the leading physical coefficient fails on an admitted source. Neither result decides all histories or equality modulo rapid.

## 1. Frozen source, category and scope

CP207 assigns this primary at input `c999e3090f2483b5ee85a63dfaf35f09aa9cc290`, preserved on `research/reach-zero-energy192-input-frozen-20261115`. The parent records180 scientific sources in the external `zero-energy192-science-manifest.json`, SHA256 `864fc9d30d27939c7fa09b49e6aaaf3d6d55070182b2badc7a9bde8de64f25c1`. Work in ZFC, real liquid modules for fixed $0<p\le1$, the physical interval basis, original [105](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md)/[108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) and source-controlled [126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md). This is one primary for distinct source-locked review193 and draft ledger194. Shared same-system mathematical work is not external certification, protected admission or programme completion.

The actual sources read include protocol090, 105/108/126, first core165, matched second arm168, bridge174 and critic175, terminal177 and critic178, mixed widths180 and critic181, polynomial183 and critic184, actual [NONPOLYNOMIAL_GAUSSIAN_SOURCE_AUDIT_186.md](NONPOLYNOMIAL_GAUSSIAN_SOURCE_AUDIT_186.md) and critic187, and energy189 and critic190. The separately named [DOUBLE_GAUSSIAN_HIDDEN_MEAN_SOURCE_186.md](DOUBLE_GAUSSIAN_HIDDEN_MEAN_SOURCE_186.md) is also present at this input. Its number does not identify it with the actual nonpolynomial186. Its two-edge identity and counterexample are acknowledged explicitly below; they are not claimed as new results of192.

Keep the target and normalization of165:

$$
e(t)=|t|/2,\qquad f(x)=\chi(x)e(x),\qquad
K(t)=(2\pi)^{-1/2}e^{-t^2/2},\qquad
\kappa_\sigma(t)=\sigma^{-1}K(t/\sigma),\qquad
A_\epsilon(x,z)=f(x)\rho(z)\kappa_\epsilon(z).
\tag{192.1}
$$

Here $\chi=1$ near zero, the cutoffs are fixed compact smooth functions, and $\rho(0)\ne0$. Every rapid assertion means108.3/126.8: one finite negative Sobolev order for each mixed derivative, independent of the requested power. No lockfile, Python runtime or numerical experiment is used to establish the arguments below.

## 2. Actual hidden-mean elimination and its limited cone statement

Consider genuine identity-partition108.7 histories on $(x,y,h)$, with retained $(x,z)$, of the form

$$
S_\epsilon(x,z)=\rho(z)\iint
\kappa_{a\epsilon}(z-y)\kappa_{b\epsilon}(z-h)
F_\epsilon(x,y,h)\,dy\,dh,\qquad a,b>0.
\tag{192.2}
$$

The widths, compact physical support, original permitted closed R1 cone $\Gamma$ and scalar indices are fixed. The coefficient $F$ is evaluated from one complete source $E_{s,K,\Gamma}\widehat\otimes_\pi S_\lambda$ or a finite sum thereof. Its scalar factor may be any actual105 fixed stage, including singular heat-front behavior; it is independent of retained $z$. This last condition is necessary for the displayed terminal factorization. We assume the original scalar pullbacks, R1 products and whole-source126 rows, rather than inferring them from an untyped positive-regulator function. There is no nonidentity partition insertion in this theorem.

Put

$$
d=(a^2+b^2)^{1/2},\quad c=ab/d,\quad
\alpha=a^2/d^2,\quad\beta=b^2/d^2,\quad
u=\beta y+\alpha h,\quad v=y-h.
\tag{192.3}
$$

The inverse is $y=u+\alpha v$, $h=u-\beta v$, with absolute physical Jacobian one. Completing the square gives the previously recorded exact identity

$$
\kappa_{a\epsilon}(z-y)\kappa_{b\epsilon}(z-h)
=\kappa_{c\epsilon}(z-u)\kappa_{d\epsilon}(v),\qquad
V_\epsilon(x,u)=\int\kappa_{d\epsilon}(v)
F_\epsilon(x,u+\alpha v,u-\beta v)\,dv,
\quad S_\epsilon=\rho(z)(\kappa_{c\epsilon}*_{u}V_\epsilon)(x,z).
\tag{192.4}
$$

There is no Gaussian division and no reclassification of a weighted linear mean as physical vertex forgetting. In particular exact R1-cone preservation is false. The historical double-Gaussian186 constructs the legal original coefficient $g(x)\psi(v)\delta(x-u)$ with $v$ bounded away from zero. It evaluates to $C_\epsilon g(x)\delta(x-u)$ under this mean, with $C_\epsilon>0$ for every positive regulator. That coefficient has the forbidden effective diagonal conormal. Its amplitude is uniformly rapid. The next statement treats this distinction rather than repeating the false exact-cone assertion.

**Proposition192.1 (weighted mean near its zero-energy collapse).** Locally at $(x,u)=(0,0)$, there is a decomposition

$$
\psi(x,u)V_\epsilon=W_\epsilon+R_\epsilon
\tag{192.5}
$$

with a fixed cutoff $\psi=1$ near the origin, such that $W$ belongs to one moderate graph stage with a fixed output cone avoiding the diagonal conormal, and $R$ is uniformly rapid in a fixed finite negative order for each regulator derivative. These are continuous evaluated-family maps on the specified complete sources and their given126 rows. The proposition does not assert that $W$ has a presentation as an original completed coefficient $E\widehat\otimes_\pi S$ on the two mean coordinates.

**Proof.** A possible forbidden output covector at $x=u$ has the form $(\tau,-\tau)$, $\tau\ne0$. Its lift through the mean projection and the inverse coordinate change, with zero $v$ covector, is

$$
(\xi_x,\xi_y,\xi_h)=(\tau,-\beta\tau,-\alpha\tau).
\tag{192.6}
$$

At $v=0$ and $x=u$, all three physical coordinates agree, and these covectors sum to zero. They are therefore conormal to the original full three-vertex partition and excluded by $\Gamma$. On a compact base patch and normalized covector sphere, closedness of the fixed cone gives a fixed neighborhood of this collapse and a fixed angular neighborhood of the output forbidden rays whose lifts avoid $\Gamma$. This is a separation in both base and covector variables, not just a test at the single point zero. Shrink $\psi$ and choose a fixed $\theta(v)=1$ near zero, supported inside that neighborhood.

Define $W$ by inserting $\psi\theta$ in the integral192.4, and $R$ by inserting $\psi(1-\theta)$. The wavefront pushforward relation for $W$ now excludes a fixed neighborhood of the forbidden output rays at every output diagonal point in this patch. The corresponding normal graph estimates are uniform: an output off-cone Sobolev seminorm requests finitely many input off-cone seminorms and one finite global negative norm, since its lifted covectors are separated from $\Gamma$. Proper support supplies the compact projection estimate. Multiplication by the Gaussian and the actual scalar factor costs finitely many physical derivatives for each requested seminorm. On the compact positive-regulator source these derivatives have fixed inverse-regulator powers by105/108. Hence $W$ is moderate in a fixed permitted output cone, with order and power allowed to depend on the requested derivative or off-cone seminorm.

For $R$, the remaining support has $|v|\ge\delta>0$. Every finite derivative of its Gaussian multiplier is bounded by a polynomial in $\epsilon^{-1}$ times $\exp(-\delta^2/(4d^2\epsilon^2))$. The evaluated whole coefficient is moderate in one fixed negative order for each derivative by108.2. Smooth multiplier estimates and compact pushforward give $R=O(\epsilon^L)$ in one fixed negative order for every $L$. The order does not depend on $L$.

For each stated target seminorm the estimates use finitely many defining source seminorms. First prove them on simple tensors, then extend by the projective tensor seminorm bound and completeness. In particular the argument does not assign unrelated bounds separately to infinitely many tensor summands. For126 use the same history, widths, cutoffs, indices and cone in every row; differentiate the continuous maps and use finite Leibniz sums. Entire evaluated row compatibilities are preserved. Profinite plots lift cover-locally through finitely many stages and these actual test-pairing identities descend. This proves precisely the evaluated moderate/rapid assertion. It supplies neither missing coefficient lifts for arbitrary output families nor a new scalar heat stage on the mean space. $\square$

## 3. Why the weaker cone statement still excludes a static effective target

**Lemma192.2 (static target cannot hide forbidden wavefront in a rapid tail).** Let $U$ be a fixed compact distribution and, locally, $U=W_\epsilon+R_\epsilon$. Suppose $W$ has polynomially moderate Sobolev bounds of every order off one fixed cone, and $R$ is rapid in one fixed $H^{-t}$ norm. Then $U$ is smooth off that cone.

**Proof.** Apply a properly supported microlocal cutoff $B$ outside the cone, with compact output support. For each $m$ there are finite $N_m,C_m$ with $\|BW_\epsilon\|_{H^m}\le C_m\epsilon^{-N_m}$. For every $L$, $\|BR_\epsilon\|_{H^{-t}}\le C_L\epsilon^L$. A frequency shell $\Delta_j$ therefore satisfies

$$
\|\Delta_j BU\|_{L^2}
\le C_m2^{-jm}\epsilon^{-N_m}
+C_L2^{jt}\epsilon^L.
\tag{192.7}
$$

Given a desired Sobolev order $q$, choose $m>2q+4$ and a positive $\gamma$ with $\gamma\max(N_m,0)<m/2$. Set $\epsilon=2^{-\gamma j}$ for large $j$, and then choose $L$ with $\gamma L>t+q+2$. Both terms are summable with the $H^q$ shell weight. Thus $BU\in H^q$ for every $q$. Low shells cause no issue. Crucially $t$ is fixed while $L$ increases. This proves the microlocal smoothness assertion. $\square$

**Corollary192.3 (exact two-hidden-mean obstruction without a graph limit).** A finite sum of histories192.2, with fixed positive widths and finitely many terminal derivatives transferred to compact effective inputs, cannot equal $A$ exactly. Arbitrary admitted scalar stages independent of retained $z$ and completed coefficient tensors are included within the hypotheses of Proposition192.1.

**Proof.** Use192.4, transfer terminal derivatives by distributional integration by parts, and group equal terminal widths. Protected180 gives, from an exact output identity, zero non-target-width aggregates and target-width aggregate $V_{1,\epsilon}=f(x)\delta_0(u)$ at every positive regulator. It uses compact effective support and exact Gaussian analytic continuation, not any effective cone. For each target-width summand apply192.5. Finite sums and derivatives retain its permitted-cone moderate part and fixed-order rapid tail; finite joins preserve the absence of the forbidden rays. Lemma192.2 would force the static $f(x)\delta_0(u)$ to exclude its actual nonzero $(\tau,-\tau)$ wavefront at the origin. This is a contradiction. The proof also covers a finite join with ordinary single-bridge histories whose effective permitted-cone estimates follow174.1. No graph limit through zero is required. $\square$

This is an obstruction for an actual weighted hidden projection, beyond the historical graph-regular double-bridge result. It is not an invariant for nonidentity source partitions, essential retained $z$ scalar factors or arbitrary Gaussian networks. An output relation modulo rapid cannot be Gaussian-inverted by this proof: inverse heat amplification is uncontrolled. Nor does192.5 establish membership of $W$ in an original two-coordinate complete scalar/R1 source.

## 4. A disconnected Wick source defeats a leading-coefficient R1 invariant

The preceding exact argument must not be replaced by an assertion that every source has an R1 leading physical coefficient. There is an actual counterexample in the original grammar.

For a fixed $b>0$ define the admitted heat-smoothed relative Green scalar

$$
P_{b\epsilon}(t)=(e*\kappa_{b\epsilon})(t).
\tag{192.8}
$$

On physical $(x,z,y)$ take the identity partition and original R1 coefficient $T=\eta_x(x)\eta_z(z)\eta_y(y)\delta_0(y)$, with fixed compact spectators equal to one on the required retained supports and at $y=0$. Its wavefront has only a $y$ component; no nonzero partition conormal has that property. Use scalar factor $\chi(x)\rho(z)P_{b\epsilon}(x-y)\kappa_\epsilon(z-y)$ and forget $y$. The exact result is

$$
\widetilde A_\epsilon(x,z)
=\chi(x)P_{b\epsilon}(x)\rho(z)\kappa_\epsilon(z)
\in\mathcal P_2.
\tag{192.9}
$$

The delta pairing with $dy$ has coefficient one. This is a finite actual source, not tensoring the nonsmooth cusp with a hidden delta in one R1 input. Its positive Gaussian graph contains the edge joining $z$ to $y$ and an isolated $x$ vertex. The Wick edge $P_{b\epsilon}(x-y)$ connects them as a scalar Green factor, but supplies no positive Gaussian energy gap on $x\ne0$.

For source typing, $P_{b\epsilon}(x-y)$ is a raw105 Gaussian-smoothed $P_0$ edge. Its fixed two-point heat stage can also be verified exactly as168.2: the front chart has $P_{b\epsilon}(\epsilon X)=\epsilon P_b(X)$; on strict charts it is $e(t)$ plus a Gaussian tail, and at their corner that tail is flat with all prescribed b-derivatives. The relative front index begins at1, the strict index at0, with integer saturation, fixed lower auxiliary weights and no logarithms. Fixed $b$ changes no index family. Pull both scalar edges to the three-point heat space by105.4 and multiply by105.6. Their product has the fixed index sum and fixed auxiliary weights supplied by those actual scalar maps. Tensoring this scalar with the fixed pure $y$ graph coefficient gives a simple tensor in the existing complete108.6 source;108.7 gives192.9. There is no absolute anchored scalar being admitted on an unblown relative two-point heat space.

These maps are continuous on the corresponding complete scalar stages and fixed R1 graph stage by the finite seminorm bounds of105/108. Smooth compact parameter variations of the cutoffs give genuine coefficient derivatives in the same stages, hence compatible126 rows; finite sums of such tensors and their completed stage maps are allowed by continuity. This assertion concerns the constructed source and the admitted maps, not recovery of all prior126 families. All fixed finite whole-source derivatives and partition-jet operations remain legal on192.9 by original closure, with every complement derivative retained.

Yet its physical limit is

$$
\widetilde A_\epsilon\longrightarrow
\rho(0)f(x)\delta_0(z),
\tag{192.10}
$$

which contains the forbidden diagonal covectors at the joint origin. This proves that no universal leading-physical-coefficient R1-cone invariant is true for all admitted histories. It already fails before nonidentity source jets and completion. There is no contradiction with192.1: the positive-scale effective coefficient $\chi(x)P_{b\epsilon}(x)\delta_0(y)$ has a permitted cone and polynomial off-cone bounds, but is not the static target and has no permitted R1 graph limit.

## 5. Exact surviving joint-corner defect, including its rapid status

Set $D=\widetilde A-A$. The exact new reduction is

$$
D_\epsilon(x,z)=\chi(x)\bigl[P_{b\epsilon}(x)-e(x)\bigr]
\rho(z)\kappa_\epsilon(z),\qquad
A\in\mathcal P_2\ \Longleftrightarrow\ D\in\mathcal P_2.
\tag{192.11}
$$

The equivalence follows by addition/subtraction of the actual source192.9. It also holds for existence of a source representative modulo the unchanged uniform rapid relation. Neither side of this equivalence is asserted to hold. This differs from168's admitted second arm $\chi(x)Q_\epsilon(x)\delta_0(z)$: both factors and their positive-regulator placement matter.

The heat equation gives the useful exact positive formula

$$
P_\sigma-e=\int_0^{\sigma^2/2}\kappa_{\sqrt{2s}}\,ds,
\qquad
\int_{\mathbb R}(P_\sigma-e)(x)\,dx=\sigma^2/2.
\tag{192.12}
$$

The first identity follows distributionally by differentiating $e*\kappa_{\sqrt{2s}}$ in $s$, using $e''=\delta_0$, and integrating from0. The second follows by Gaussian mass one and positivity. On a fixed compact set away from zero all derivatives of the difference have Gaussian-tail bounds. Choose a fixed smooth test $\phi(x)\zeta(z)$ equal to one near the origin, with supports where the cutoffs apply. Tail estimates in192.12 and Gaussian moment Taylor expansion then give

$$
\langle D_\epsilon,\phi\boxtimes\zeta\rangle
=\frac{b^2}{2}\rho(0)\epsilon^2+O(\epsilon^4).
\tag{192.13}
$$

Thus $D$ is not uniformly rapid in any fixed negative Sobolev order. A weakly zero error is not a rapid error. More precisely the exact joint-normal profile is

$$
D_\epsilon(\epsilon X,\epsilon Z)
=\chi(\epsilon X)\rho(\epsilon Z)
\bigl[P_b(X)-e(X)\bigr]K(Z).
\tag{192.14}
$$

It is nonzero, decays at large $|X|$, and retains a cusp at $X=0$ because $P_b$ is smooth while $e$ is not. It is not a smooth Schwartz profile. The expansion in fixed physical test pairings begins with $(b^2/2)\rho(0)\epsilon^2\delta_0(x)\delta_0(z)$. In the $x$ factor alone the full formal distributional expansion is

$$
P_{b\epsilon}-e\ \sim
\sum_{j\ge1}\frac{(b^2\epsilon^2/2)^j}{j!}
\delta_0^{(2j-2)}.
\tag{192.15}
$$

Each fixed truncation follows from192.12 and Gaussian test Taylor estimates. It is not an infinite admitted source sum. In particular108's physical coefficient expansion does not prove that the whole joint profile192.14 has an existing complete source. Matching finitely many local counterterms leaves a finite-order error, and formal all-order cancellation supplies neither one original complete stage nor fixed-order rapidness. The profile has the same positive-regulator cusp/anchor difficulty which was removed from the legal smoothed source192.9.

## 6. Acceptance boundary and precise remaining inference

| Question |192 primary result |
| --- | --- |
| Gaussian mean equals a physical vertex projection with automatically preserved exact R1 cone | False; the historical double-Gaussian186 counterexample already refutes it. |
| Actual weighted mean on fixed complete sources near zero energy | Permitted-cone moderate part plus a fixed-order uniformly rapid tail, Proposition192.1. |
| Exact target-width effective coefficient can be the static cusp/delta despite that decomposition | Excluded by Lemma192.2; yields Corollary192.3 for the stated actual terminal class. |
| All admitted histories have permitted R1 leading physical coefficient | False on the explicit legal disconnected Wick source192.9. |
| Disconnected Wick history supplies the original core modulo rapid | It supplies a smoothed core with explicit nonrapid defect192.11–192.14. |
| Original source status of the full cusp core | Equivalent to source status of this explicit defect; remains OPEN. |
| Arbitrary retained-output scalar dependence, nonidentity partition histories, general Wick/PHG networks and cancellations | Not exhausted by the terminal argument. |
| Output equality modulo rapid implies rapidly equivalent Gaussian-deconvolved coefficients | Unproved and not used. |
| Universal150.L, residual $W$ acyclicity, originalR3, full126.14, higher weights, lifting and final REACH integration | OPEN. |

The concrete remaining problem is full-profile source membership of192.14, or an invariant covering that profile and every allowed history, including nonidentity partitions and complete scalar stages. Its first physical coefficient is already realized by an admitted disconnected history and cannot be the invariant. The weighted-mean proof supplies a valid exact terminal obstruction, but its evaluated moderate output is not automatically a new108 complete coefficient stage, and an output rapid defect cannot be inverted through a Gaussian by fiat.

No source or rapid ideal is enlarged. No exhaustive all-history verdict, external certification or protected-state action is asserted. The single author correction remains available for a substantive source-locked review193 request; acceptance194 remains a draft until that review.
