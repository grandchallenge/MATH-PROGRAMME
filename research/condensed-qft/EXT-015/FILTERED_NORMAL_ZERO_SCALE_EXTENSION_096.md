# EXT-015 REACH / 096 — filtered normal specialization and the mixed-corner obligation

**Disposition: positive local liquid theorem; global M2 contract unresolved.** This is the single bounded M2 attempt under [090](REACH_CONDENSED_RENORMALIZATION_PLAN_090.md), after protected M1. It constructs an actual enlarged one-chart liquid domain, a nonzero full-profile boundary and physical finite evaluation. It also constructs the full finite collision resolution and the geometric R1 pullback. It does not prove that the entire mixed distributional model and all legal source pushforwards descend to one liquid boundary. M3 is suspended on that unproved step; original R3 is independent and remains open.

## 1. Frozen inputs, category and recovery target

Work in real liquid modules with parameter $p$ for fixed $0<p\le1$, in the admitted condensed universe and ZFC. Physical spacetime remains the line with its interval basis. Relative-coordinate dimension is bookkeeping for vertex configurations, not a change of spacetime.

| Input | Git blob |
| --- | --- |
| Full protocol090 | 6b642bf10c3328bb64d37474e290810fb45cbca1 |
| Liquid profile/record bridge091 | c517fe1ae46bcaa9f4a3fc0e64381ae8096bfe27 |
| Non-author critic092 | 3eafe7ec909fe315db71dc7c2942c08e17eb9ba2 |
| Bridge ledger093 | ee6d1c089847f3d5b482e1624d9923a6277ddbe0 |
| Actual subtraction087 | 452c494bcdc94ba94e52ae50c7b4d1eb3240ca83 |
| Consistent-host ledger089 | 600a269ffd47b84b1bc9c671125aea3bf61a2f80 |

M1 was protected in PR2897 at 48e07f1fe64084c9200b1ca8cadcea895c944811; its eleven changed blobs, exact reviewed second parent and five native required checks were read back before M2 construction. Independent R3 audit094/095 was protected in PR2898 at 7d8b396beef5aa21452c60d21d9337964ebb8ce4 and did not solve its equation. Current protected policy cut for this attempt is 4e2a362ffb7b679fe91815fddbe90561cb1541ae. Its intervening changes affect recovery policy and unrelated documentary/ERDOS machinery, not the scientific inputs above. The existing checkpoint owns operational custody.

The recovery target is an actual positive-regulator family with additional filtered normal information. Equal actual families must have equal boundary data; graph presentations cannot distinguish them. Full normal Taylor profiles are stronger observations than physical distributional Laurent coefficients. Finite physical evaluation is a separate, weaker map. The local theorem proves this identification; the corresponding global mixed-domain comparison is explicitly left as an equation in section8.

The parent authored this report, using preliminary local-profile and geometric observations from the existing R2 role. That delegated draft stopped at a usage limit before writing files. This is the same primary attempt, not a restarted attempt or independent review. A distinct critic097 and ledger098 remain separate requirements.

## 2. Actual local liquid domain

Fix $e_0>0$ and put

$$
P_d=C^\infty([0,e_0],\mathcal S(\mathbb R^d)),\qquad
V_d=\underline{\mathcal S(\mathbb R^d)},\qquad
V_0=R=\mathbb R_{<p}.
\tag{96.1}
$$

Use all seminorms $\sup_{0\le\epsilon\le e_0}q_N(\partial_\epsilon^k F(\epsilon))$, where $q_N$ is an increasing defining Schwartz family. Thus regulator derivatives and Schwartz tails are uniform, separately from scalar testwise smoothness. For $d=0$ this is scalar smoothness. This is a complete nuclear Fréchet space: the usual compact-interval smooth seminorms and rapid Hermite coefficients give a cofinal countable Hilbert tower with summable inclusions, as in091. Its condensed realization is liquid. More generally, completeness of a Hausdorff locally convex space suffices for the measure-extension criterion: integrate a continuous profinite plot by finite clopen step approximations, Cauchy in every seminorm; bounded variation bounds the approximations uniformly. Restriction to every measure object of exponent $q$ for $q<p$ gives the required unique extension. No projectivity or Hom exactness follows.

For each integer $h\ge0$, define the actual stage map

$$
L_{d,h}(F)_\epsilon(y)
=\epsilon^{-d-h}F(\epsilon,y/\epsilon),\qquad \epsilon>0.
\tag{96.2}
$$

It is monic on every profinite test. Indeed the evaluated distribution determines the smooth function at each positive $\epsilon$; changing variables $y=\epsilon u$ recovers $F(\epsilon,u)$. Positive values determine the closed-interval smooth coefficient, including every one-sided derivative at zero. For a continuous profinite plot this argument applies pointwise in its concrete Fréchet source, so the entire plot is zero.

Identify the transition from stage $h$ to $h+1$ with $F\mapsto\epsilon F$. It is a monomorphism of liquid modules and preserves the actual family. Write

$$
\mathcal C_d=\underset{h\ge0}{\mathop{\mathrm{colim}}}\,
L_{d,h}(\underline P_d).
\tag{96.3}
$$

This is an actual evaluated-family image with finite pole order, not a new presentation label. As proved in Lemma91.2, the free liquid object on every profinite test is compact in the abelian heart. Consequently every section of this filtered union lifts to one $h$ with continuous $P_d$ coefficients. Evaluation into the ordinary internal-Hom envelope of091 remains monic: every tested section has such a lift. No ambient subspace topology is substituted.

The old finite-homogeneity module $\Phi_d$ maps monically into (96.3): for a finite sum $\sum_m\epsilon^m f_m$ choose $h$ with $h+m\ge0$ and use $F(\epsilon)=\sum_m\epsilon^{h+m}f_m$. Changing $h$ is exactly the specified transition. A nonzero scalar-unit family is included at $d=0$.

## 3. Full-profile boundary and uniform Borel lifting

Use a formal symbol $z$, recording the regulator Taylor degree; do not set an invertible physical regulator equal to zero. Define

$$
\mathcal N_d
=\underset{h\ge0}{\mathop{\mathrm{colim}}}\,
z^{-h}\prod_{j\ge0}V_dz^j,\qquad
J_{d,h}(F)=z^{-h}\sum_{j\ge0}\frac{\partial_\epsilon^jF(0)}{j!}z^j .
\tag{96.4}
$$

Products and colimits are in the liquid heart. The transition multiplies the Taylor series by $z$ and changes its displayed weight to $h+1$, so (96.4) is independent of the representative. The symbol $z$ remains part of the boundary; tensoring the Laurent algebra with its alleged quotient by $\epsilon$ would instead give zero.

**Theorem96.1.** The map $J_d:\mathcal C_d\to\mathcal N_d$ is an epimorphism on every profinite test. Its kernel consists exactly of regulator-flat normalized profiles. The boundary is nonzero and retains all actual Schwartz profiles, including profiles whose every physical moment is zero.

**Proof.** At a fixed stage, a target profinite plot is a sequence of continuous maps $T\to\mathcal S$, denoted $f_j(t)$. Compactness bounds every $q_N(f_j(t))$ uniformly in $t$ for each fixed $j,N$. Choose a scalar cutoff $\eta=1$ near zero. Form

$$
F(t,\epsilon)=\sum_{j\ge0}\eta(\epsilon/\delta_j)\epsilon^jf_j(t).
\tag{96.5}
$$

Keep finitely many low terms separately. For each large $j$, choose $\delta_j\downarrow0$ so that the term in (96.5) has norm at most $2^{-j}$ in all seminorms $q_N\partial_\epsilon^k$ with $N,k\le j/2$. This is possible because differentiation gives a bound $C_{j,k}\delta_j^{\,j-k}\sup_tq_N(f_j(t))$, and $j-k>0$. For every fixed seminorm the tail then converges uniformly in $t$ and $\epsilon$. Its terms are continuous into $P_d$, hence the limit is a continuous map $T\to P_d$. Its Taylor coefficient of order $j$ is $f_j(t)$, since the cutoff is constant near zero. This proves a genuine family lift, not merely scalar Borel surjectivity. The choices may depend on the compact family; no continuous linear Borel section is claimed.

Every plot into $\mathcal N_d$ has one finite pole bound by profinite compactness, so the same construction proves the statement for the colimit. Vanishing of every Taylor coefficient is exactly regulator flatness at each actual stage; finite changes of weight preserve that condition. A constant nonzero $f\in\mathcal S$ gives the nonzero boundary $f$. In particular a real even Fourier bump supported away from the origin gives a nonzero $f$ with all physical moments zero, as in091. Its boundary still equals $f$, although its physical distributional Laurent series vanishes. $\square$

This quotient removes regulator-flat dependence, not moment-flat spatial profiles. Finite-order differential operations and polynomial regulator growth preserve the former kernel on these uniformly Schwartz stages. It does not license arbitrary exponentially growing insertions.

### Why the first leading-profile candidate was corrected

The primary associated-graded proposal keeps only $F(0)$ in each degree. It is nonzero, but it cannot determine the required finite physical value. At $h=1$, compare $F=f$ and $F=f+\epsilon g$ with $\int g\ne0$. Their leading profiles agree; their physical finite values differ by $(\int g)\delta$. This is already a scalar-unit counterexample at $d=0$ with $g\ne0$.

The one correction pass therefore retains the full series (96.4), rather than claiming a finite-evaluation map on the leading associated graded. Further global difficulties below are reported as unresolved, not repaired by an endless sequence of new candidates. This corrects a new trial construction, not an accepted historical theorem.

## 4. Physical subtraction, cutoffs and operations that are proved

Write $F_j=\partial_\epsilon^jF(0)/j!$ and $\mu_\alpha(f)=\int u^\alpha f(u)\,du$. The strong physical expansion has coefficients

$$
a_n(F,h)=
\sum_{\substack{j\ge0,\ \alpha\ge0\\j+|\alpha|-h=n}}
\frac{(-1)^{|\alpha|}}{\alpha!}\mu_\alpha(F_j)\,
\partial^\alpha\delta .
\tag{96.6}
$$

Each coefficient uses finitely many $j,\alpha$. Taylor expansion in $\epsilon$ in $P_d$, followed by Taylor expansion of the test $\phi(\epsilon u)$, proves (96.6) uniformly on compact profinite coefficient families and bounded Schwartz test sets. The remainders are bounded by finitely many Schwartz moments of bounded profile derivatives and bounded test derivatives. Taking sufficiently many terms gives any requested strong remainder order; the same argument applies to fixed regulator and parameter derivatives.

The principal part is $\sum_{n<0}\epsilon^n a_n$, and

$$
\mathrm{CT}_{\mathrm{phys}}J_{d,h}(F)
=\sum_{j+|\alpha|=h}
\frac{(-1)^{|\alpha|}}{\alpha!}\mu_\alpha(F_j)\partial^\alpha\delta .
\tag{96.7}
$$

These are real-linear liquid maps at every stage, hence on the compatible colimit. At $d=0$ the only multi-index is zero and (96.7) selects $F_h$. On the embedded $\Phi_d$ this is exactly087's whole-family finite normalization. Reconstruction by addition of principal part and actual remainder still takes place at positive scale. Equation(96.7) does not identify finite physical outputs with $\mathcal N_d$, or make finite evaluation multiplicative.

For a fixed physical $\chi\in C_c^\infty(\mathbb R^d)$, multiplication replaces $F(\epsilon,u)$ by $\chi(\epsilon u)F(\epsilon,u)$. Every mixed derivative is a finite sum of polynomial factors in $u$, bounded cutoff derivatives and Schwartz derivatives of $F$; dominated seminorm estimates prove continuity into $P_d$. If $\chi=1$ near zero, the difference is regulator-flat in $P_d$: its support has $|u|\ge c/\epsilon$, and arbitrarily high Schwartz tails absorb every regulator derivative and seminorm power. Thus compact physical localization is actually included, although generally absent from the finite regulator-independent class of091.

The following shifts follow directly from (96.2). They are local analytical maps, not a global quantum theorem.

| Operation | New profile and pole index |
| --- | --- |
| Physical $\partial_{y_i}$ | $\partial_{u_i}F$, $h+1$ |
| Multiply by $y^\beta$ | $u^\beta F$, $h-|\beta|$; use a larger nonnegative stage if necessary |
| Multiply by $\epsilon^k$ | $h-k$ |
| Exterior composition in independent dimensions | $F(\epsilon,u)G(\epsilon,v)$, $h+h'$ |
| Same-variable smooth-profile product in dimension $d$ | $FG$, $h+h'+d$ |
| Integrate $r$ normal variables of a Schwartz profile | Integrated profile, dimension drops by $r$, $h$ unchanged |
| Restrict $r$ normal variables to zero | Restricted profile, $h+r$ |

Negative displayed indices are interpreted by the same transition into a nonnegative stage. Schwartz multiplication, restriction and linear integration are continuous; their estimates with all regulator derivatives preserve flatness. The local exterior operation therefore descends to the full-profile boundary. It uses the completed liquid Schwartz tensor before diagonal restriction of the two regulator variables. No new relative derived-tensor equivalence over $C^\infty([0,e_0])$ is asserted.

Scale change $\epsilon\mapsto s\epsilon$ acts, on a suitably smaller interval, by $F(\epsilon,u)\mapsto s^{-d-h}F(s\epsilon,u/s)$. It is semilinear over regulator scalars. The coefficient in (96.6) of physical degree $n$ scales by $s^n$, so the finite coefficient is invariant. Regulator derivative at fixed $y$ has index $h+1$ and profile $-(d+h)F-u\cdot\partial_uF+\epsilon\partial_\epsilon F$. These statements account for the change of normal coordinate, rather than differentiating $F$ alone.

## 5. Full collision geometry and raw Gaussian/Wick lifts

For $n$ labeled physical vertices, let $\Delta_\pi$ range over all nondiscrete partition diagonals, including simultaneous disjoint collisions. On $[0,e_0]\times U^n$, form the iterated real oriented blowup

$$
X_n=\bigl[[0,e_0]\times U^n;\
\{0\}\times\Delta_\pi\text{ in deepest-first order}\bigr],
\qquad \beta_n:X_n\to[0,e_0]\times U^n .
\tag{96.8}
$$

Work over compact physical supports and include all partition intersections, not only graph-divergent sources. The centers are linear in interval coordinates, cleanly intersect and are closed under intersection. They are p-submanifolds of the initial boundary. [Kottke, Theorem3.2 and Corollary3.5, version3](https://arxiv.org/html/1712.03902v3) therefore apply to this finite collection. Alternatively its size-order proof applies directly: after the intersection of incomparable centers has been blown up, their proper transforms are disjoint; nested centers retain product coordinates. This proves existence, independence of the chosen size order and the canonical chart identifications. It does not prove a pushforward theorem.

Each ideal $(\epsilon,x_i-x_j)$ becomes locally principal. Before its pair center is blown up, a blowup of a contained linear center factors its ideal by one radial coordinate and leaves the ideal of its strict transform. In a complementary projective chart that transform is absent and the residual ideal is the unit ideal. Incomparable transforms are already disjoint. Blowing up the pair center makes the residual ideal principal, and later blowups preserve this property. Hence locally

$$
\epsilon=\rho_{ij}a,\qquad x_i-x_j=\rho_{ij}b,\qquad (a,b)\ne(0,0),
\tag{96.9}
$$

where $\rho_{ij}$ is a boundary monomial times a nonvanishing smooth factor and $a\ge0$.

The exact lifted Gaussian is $\rho_{ij}^{-1}(2\pi)^{-1/2}a^{-1}\exp(-b^2/(2a^2))$. At $a=0$ one has $b\ne0$, so its angular coefficient and every derivative extend by zero, flatly. For the Wick kernel the coefficient is $\rho_{ij}aP_1(b/a)$. For $a>0$ it is smooth. At $a=0,b\ne0$ the exact Gaussian convolution formula gives $aP_1(b/a)=|b|/2$ plus a Gaussian-decaying tail with all derivatives. Since $b$ is nonzero there, $|b|$ is smooth locally. The tail is only used away from its origin; $P_1(u)-|u|/2$ is not claimed to be a Schwartz function on the whole line.

Thus every fixed finite product of Gaussian/Wick edges, vertex derivatives, polynomial decorations, Laurent scalar factors and physical cutoffs has a weighted smooth lift in (96.8). This covers disconnected Gaussian backbones and Wick bridges as raw functions, without pretending their profiles are globally Schwartz. Each such lift is uniquely determined by the interior family after its weights are specified: weighted smooth sections that agree on the dense positive-scale interior agree at the boundary. Chart transitions agree by the same uniqueness. Additional weights can be chosen for each fixed finite decoration; no uniform bound over all decorations is claimed.

On a normal chart dominated by $\epsilon$, (96.9) recovers the original $y=\epsilon u$ normalization and its full profiles. Schwartz tails give flat matching into charts where $|y|/\epsilon$ tends to infinity. The eleven-edge host, its277 proper sources and both legal disjoint spinneys remain the finite combinatorial inputs of087–089. Their values and recursions are unchanged. Overlapping sources remain alternatives; the resolution is not permission to multiply their counterterms.

## 6. An actual regular R1 map in its proved category

For the admitted R1 locally normal sector, let $T$ have compact support and fixed closed wavefront cone avoiding every nonzero partial-diagonal conormal, including simultaneous collisions. Regard $T$ as independent of $\epsilon$.

**Proposition96.2.** Spatial blowdown pulls $T$ back to a distribution on $X_n$ with well-defined compatible restrictions to every boundary face and corner. On fixed compact cone sectors these are continuous normal-topology maps and preserve the admitted locally normal smooth plots. The interior map is the original $T$, so it is injective. This is an actual geometric/DVS map; the full mixed liquid comparison in section8 is separate.

**Proof.** At a point of $X_n$ over a collision partition $\pi$, the image of the spatial derivative of blowdown contains $T\Delta_\pi$. Locally translate each block of $\pi$ independently, keeping the separated blocks separated. These translations preserve all nearby centers, lift through every blowup and act tangentially on all the relevant faces. Their derivatives span $T\Delta_\pi$. The same containment therefore holds after restricting blowdown to any face or corner through the point. Any covector annihilated by that derivative is conormal to $\Delta_\pi$, and is excluded from the fixed R1 cone. This proves the noncharacteristic condition for blowdown and for every face-restricted blowdown.

Apply the same noncharacteristic pullback theorem already used in035, in local smooth collar extensions. Compactness gives a fixed compatible output cone on each chart. Functoriality of transversal pullback identifies a restriction of the lifted distribution with pullback by the corresponding face map; it identifies all iterated corner restrictions and overlap maps. Different collar extensions give the same one-sided germ and jets. The normal-topology continuity theorem gives the asserted fixed-sector continuity; the locally normal plot definition then gives smoothness. On positive scale blowdown is the identity in physical variables, proving injectivity. $\square$

A nonzero compact smooth R1 kernel constant near a collision has leading rescaled value constant in $u$ there, which is not Schwartz on the whole normal space. This is why the separate regular sector is essential. Proposition96.2 does not identify that sector with $\mathcal C_d$ or give every mixed distribution a nuclear Fréchet realization.

## 7. Local jets and legal source operations: proved controls

In a fixed split normal chart $(z,y)$, include finite collision-normal jets $g_\alpha(z)\partial_y^\alpha\delta(y)$. Their actual evaluation is

$$
\left\langle g_\alpha(z)\partial_y^\alpha\delta(y),\phi(z,y)\right\rangle
=(-1)^{|\alpha|}\left\langle g_\alpha,\partial_y^\alpha\phi(z,0)\right\rangle .
\tag{96.10}
$$

Here $g_\alpha$ may be smooth Schwartz tangential data, or an admitted fixed-cone tangential distribution when the indicated pullbacks are transversal. The normalization in $r$ normal dimensions is $\epsilon^{r+|\alpha|}\partial_y^\alpha\delta(\epsilon u)=\partial_u^\alpha\delta(u)$. This retains the normal jet; it does not replace it by its integrated scalar.

For a smooth complement $g$, or the transversal distribution-valued version, the exact product rule is

$$
g(z,y)\partial_y^\alpha\delta(y)
=\sum_{\beta\le\alpha}(-1)^{|\beta|}
{\alpha\choose\beta}(\partial_y^\beta g)(z,0)
\partial_y^{\alpha-\beta}\delta(y).
\tag{96.11}
$$

Pairing with a test and differentiating $g\phi$ proves every term and sign. Disjoint normal blocks tensor and their derivative orders add. Nested insertion is successive application of (96.10) to the complement, using the full chain rule; it is not the product of dependent delta distributions. Normal projection, integration and change of variables must include their actual density/Jacobian factors. On the Schwartz local stages their continuity and finite power shifts were proved in section4. Arbitrary global mixed source pushforwards are the unresolved part below.

For the studied host use $t=x_5-x_4$ and $D=(\partial_5-\partial_4)/2$, so $Dt=1$. The actual identity is

$$
D^2(P_\epsilon(t)G)
=\kappa_\epsilon(t)G+2P_\epsilon'(t)DG+
P_\epsilon(t)D^2G .
\tag{96.12}
$$

The two complement terms cannot be dropped. Inserting (96.11) retains all the normal derivatives of those terms. This is consistent with the marked $P_\epsilon''=\kappa_\epsilon$ conversion and087; it is not a zero-scale BV identity.

A regulator-flat normalized Schwartz profile stays flat after the operations proved in section4, including fixed polynomially bounded $P_1$ multipliers. Nonzero even-rank finite terms of087 remain controls; no parity cancellation is used to justify this extension.

## 8. The attempted global model and the exact remaining equations

The global candidate is the union of finite-weight, compact-support distributional sections on $X_n$ which, after multiplication by the prescribed boundary monomials, are smooth in boundary variables with distributional tangential coefficients in fixed normal cones avoiding face conormals. Use local Schwartz conditions on concentrated normal charts and the separate sector of Proposition96.2; include the finite normal jets (96.10). Overlaps must agree as actual weighted distributions. Interior evaluation is injective for these traceable sections: zero interior implies zero continuous distribution-valued coefficients and every boundary jet. Thus the candidate is not a graph-labeled family.

This defines a geometric sheaf of sections and its restricted smooth plots. It has not yet been identified, with these exact mixed plots and uniform corner bounds, as a filtered liquid object. Calling its liquid reflection a realization without proving its evaluation/jet comparison would omit a necessary inference.

Here is a precise categorical test. Let $\mathscr P_n$ be its condensed sheaf of locally finite-stage profinite plots, $L\mathscr P_n$ its liquid reflection, and let $\mathscr E_n$ be the ordinary test-pairing envelope on compact physical charts. Liquidify the compatible formal face-jet target to a module $\mathscr B_n$. Extend evaluation and the jet map by adjunction. For the actual evaluated liquid image to carry a well-defined boundary, one must prove

$$
\ker\!\left(L\mathscr P_n\longrightarrow\mathscr E_n\right)
\ \subset\
\ker\!\left(L\mathscr P_n\longrightarrow\mathscr B_n\right).
\tag{96.13}
$$

The local theorem proves this on $\mathcal C_d$. Uniqueness on the original geometric sections proves it before liquid reflection. Neither alone proves (96.13) on all reflected profinite sections. Proving completeness/liquidness of appropriately specified mixed fixed stages, or an explicit profinite lift theorem, could supply the missing step. An image of the pair (evaluation, jets) is not a substitute unless its projection to the evaluated image is proved monic.

The second, independent remaining inference is pushforward through mixed corners. For each actual source contraction/forgetful map $q$ and its correctly shifted density, construct a lift or a proved alternative and establish

$$
q_*(\mathscr P_n)\subset\mathscr P_m,\qquad
q_*(\mathscr P_n^{\mathrm{flat}})\subset
\mathscr P_m^{\mathrm{flat}},
\tag{96.14}
$$

with continuous uniform bounds in every chosen output stage and all normal/regulator derivatives. Here flat means every retained normalized face jet vanishes, not merely weak physical convergence. These assertions must cover proper compact localization, disconnected backbones, Wick bridges, all legal nested/disjoint source insertions and their changes of chart. Local normal Schwartz integration proves only its own restricted case.

A possible mechanism is a corner pushforward theorem after proving that the resolved forgetful maps are b-fibrations with the required density orders and integrability. [Kottke, Theorem4.1 and Theorem5.3](https://arxiv.org/html/1712.03902v3) provide actual b-fibrations for admissible quotient maps of *many-body compactifications at infinity*. For relative vertex coordinates with a retained anchor, the partition-diagonal systems satisfy the linear admissibility tests: preimages of output diagonals are source diagonals and every output partition is the restriction of a source partition. This supports the normal front-face model. It does not by itself identify all of (96.8), including mixed physical/normal corners, with that compactification or verify the lifted source projections. That additional step is unproved here. Likewise the geometric renormalization paper0908.0633 supplies neither the required Gaussian concentration theorem nor these family-uniform mixed bounds.

Without (96.14), a physical constant coefficient has been proved on the local domain (96.7), not on the entire proposed mixed extension. Without (96.13), that geometric candidate has not supplied the requested common liquid domain even if its pointwise chart formulas look correct. These are the exact failures of the attempted proof, not demonstrated counterexamples to the possibility of M2.

## 9. Controls, limitations and next theorem

| Control | Actual result |
| --- | --- |
| Scalar unit and localization trap | $d=0$ explicit; full-profile boundary nonzero; no fibre of already localized $A$ |
| Full Taylor data versus leading profile | Explicit finite-contact discrepancy; repaired once by(96.4) |
| Moment-zero nonzero Schwartz profile | Retained nontrivially in $\mathcal N_d$ |
| Physical cutoffs and regulator derivatives | Included with uniform Schwartz bounds; constant-near-zero cutoff changes the local profile by a regulator-flat term |
| Escaping homogeneity/ambient plots | Finite-pole profinite stage retained; no ambient-family topology identification |
| Regular physical kernels | Actual R1 geometric/DVS map, not a false all-normal-Schwartz inclusion |
| Wick bridges/disconnected backbones | Weighted smooth raw lifts on full resolution, not a closure theorem for mixed pushforwards |
| Normal derivatives, mixed tangent terms | Exact(96.10)–(96.12); overlapping singular counterterms never multiplied |
| Host277 sources, both spinneys and even-rank finite values | Existing087–089 source-locked evidence unchanged; no unnecessary expensive replay |
| Quantum weight, signs and descent | No new $Q_{\mathrm{ren}}$, BV/QME, extended factorization or Weiss theorem asserted |
| Original R3 | Unchanged equation;094/095 supplies no sufficient new mechanism |

The concrete next theorem is **liquid mixed-corner realization and flat-kernel-preserving source pushforward**, equations(96.13)–(96.14), on explicitly completed fixed stages of (96.8). Its dependencies are the admitted local bridge, the local uniform full-profile theorem above, the actual R1 noncharacteristic map and verified geometry/density conditions for every required projection. The partial front-face comparison with Kottke is a documented mechanism to investigate, not permission to assert those conditions.

The single bounded attempt has produced the proved local theorem and geometric controls, while failing to prove the global mixed contract after its one correction. Freeze this report for critic097. Further construction requires a documented mechanism addressing the two equations; fresh context alone is insufficient. M2 is not complete, so dependent M3 and final M5 integration are suspended. R4 may add only the arrows actually proved here after their own protected admission. Original R2/R3/R4 and both parent objectives remain incomplete.

Local verification uses the existing isolated Windows evidence environment with external GCL caches. No root lockfile is admitted, so that environment is unpinned. Finite symbolic checks test coefficient algebra only; none proves the family, categorical or mixed-corner assertions.

