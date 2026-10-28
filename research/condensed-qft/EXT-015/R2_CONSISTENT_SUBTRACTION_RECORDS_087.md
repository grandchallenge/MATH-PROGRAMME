# EXT-015 R2 / 087 — consistent actual-family subtraction records

**Disposition:** positive construction candidate for the separate fixed-model objective [#2890](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2890), under the contract in [089](CONSISTENT_HOST_ACCEPTANCE_089.md). The proof below constructs a representation-independent procedure with retained subtraction records and an intrinsic finite normalization of each source-channel forest. Critical review 088 and protected admission/readback are separate obligations. This is not full REACH completion or a mathematical certificate.

## 1. Exact question, inputs and the chosen normalization

The frozen original input is protected main `eea4b98d7a3d93db44668366eb13699cc17f7d19`. Protocol and the separate registry entry were protected-admitted in PR #2891 at `f348dcccbc6b8d2ffd89551afa7dea1d27c06e11` and exactly read back before construction. The original REACH checkpoint and original success conditions are unchanged.

| Input | Exact Git blob at the frozen cut |
| --- | --- |
| [083, actual-family descent failure](R2_COMMON_DOMAIN_COMPATIBILITY_083.md) | `ad68f27d91372cb88c648867c9f01dcd707992cb` |
| [086, source-bound review](AGENT_CRITICAL_REVIEW_REASSESSMENT_086.md) | `8934ec118e2b6a62a7d4ff5730dc815d7b9f66f8` |
| [086, Schur verifier](fixtures/check_common_domain_schur_086.py) | `9c452602fc0337002b6125114dbc84345057e2b3` |
| [065, exact rational/radical primitives](fixtures/check_nested_gaussian_jet_forest_065.py) | `9e1e58d5df15cdbbeec5c443199d748742d5d45c` |
| [061, normal-jet insertion](R2_FILTERED_NORMAL_JET_INSERTION_061.md) | `c38269ebf92c40c268d33af1b0e1fff3caf05b9f` |
| [071, finite-state obstruction](R2_FINITE_LAURENT_INSERTION_OBSTRUCTION_071.md) | `13d1441dd5a745f7726d6b01843b2129331e4b2d` |

Use the six-vertex host

$$
H=K_4(01,02,03,12,13,23)+04+14+05+15+45,
\qquad G=H\setminus\{45\},\qquad t=x_5-x_4.
\tag{87.1}
$$

The regulator and marked kernel are exactly those of 083:

$$
\kappa_\epsilon(z)=(2\pi)^{-1/2}\epsilon^{-1}e^{-z^2/(2\epsilon^2)},
\qquad P_\epsilon=(|\cdot|/2)*\kappa_\epsilon,
\qquad P_\epsilon''=\kappa_\epsilon.
\tag{87.2}
$$

The inputs are actual smooth vertex-kernel families for every positive regulator, identified by equality of those functions. They include the specified sources, the marked Wick case, finite derivatives, polynomial decorations and finite Laurent scalar factors. A source and complement can carry different allocations of a regulator scalar; their identical evaluated product is one input. No graph label is used to distinguish equal inputs.

We choose one explicit finite normalization: **the finite value of a connected raw family is its whole-family constant Laurent coefficient**. This choice changes some finite contact terms of the old pole-only forest scheme. We compute the new values and corrections; we do not describe them as the old finite normalization. The full regularized remainder is retained for later operations, rather than replaced by its finite value.

## 2. Analytic domain and strong asymptotic theorem

In relative coordinates $y\in\mathbb R^d$, let $\mathscr F_d$ consist of actual families that admit a finite expression

$$
A_\epsilon(y)=\sum_{j=1}^m\epsilon^{-d-h_j}f_j(y/\epsilon),
\qquad h_j\in\mathbb Z,\quad f_j\in\mathcal S(\mathbb R^d).
\tag{87.3}
$$

Different expressions for the same functions are identified. No uniqueness of the profiles or of their decomposition is required. For the studied model, a connected Gaussian backbone makes each fixed profile Schwartz: the remaining marked $P_1$, its derivatives and the polynomial decorations have polynomial growth, dominated by that Gaussian. Removing the marked edge from any bridgeless source containing it preserves a connected Gaussian backbone. Thus every source in the fixed forest family belongs to (87.3). Scalar powers and vertex derivatives merely change the integer and the Schwartz profile. For each external disjoint component use its own relative coordinates; free center coordinates can be paired over a compact test and cause no new singular factor.

**Theorem 87.1.** Every family (87.3) has a unique bounded-below Laurent asymptotic expansion in the strong topology of $\mathcal D'(\mathbb R^d)$. All coefficients are finite local delta jets:

$$
A_\epsilon\sim\sum_{n\ge n_0}\epsilon^n a_n,
\qquad
a_n=\sum_j\ \sum_{|\alpha|=h_j+n}
\frac{(-1)^{|\alpha|}}{\alpha!}
\left(\int u^\alpha f_j(u)\,du\right)\partial^\alpha\delta_0.
\tag{87.4}
$$

A sum with a negative required derivative degree is empty. For every integer $N$, subtracting the coefficients of degree less than $N$ leaves $O(\epsilon^N)$ uniformly on bounded compact smooth test families.

**Proof.** Pair a summand with a test $\phi$ and put $y=\epsilon u$. The result is $\epsilon^{-h_j}\int f_j(u)\phi(\epsilon u)du$. Taylor-expand the test through the required degree. Its global Taylor remainder is bounded by a derivative supremum times $\epsilon^M|u|^M$; every required moment is integrable because $f_j$ is Schwartz. Bounded test families have uniform derivative bounds and a common compact support. This proves the strong estimate. The distributional sign in (87.4) is the sign in pairing $\partial^\alpha\delta$ with a test. If two expressions yield different first coefficients, pairing their difference with a test on which that coefficient is nonzero contradicts the leading-power estimate. Thus the coefficients depend only on the actual family. This proves uniqueness and representation independence. $\square$

Define

$$
\mathrm{PP}A=\sum_{n<0}\epsilon^n a_n,
\qquad \mathrm{CT}A=a_0,
\qquad \mathcal Z(A)=(C_A,R_A)=(\mathrm{PP}A,\ A-\mathrm{PP}A).
\tag{87.5}
$$

The counterterm $C_A$ is a finite Laurent polynomial of local distributions. The remainder satisfies $R_A\to a_0$ strongly. “Regular remainder” means regular in the regulator limit; $R_A$ can still be spatially distributional for positive regulator. This is why its same-variable pointwise product is not taken by itself.

Whenever an admissible actual family already has a strong finite limit, every negative coefficient vanishes, so this procedure reproduces that limit. The same definition also reproduces a constant ordinary smooth family. Locality here is proved for the concentrated model (87.3); no assertion is made that artificial negative regulator powers of a nonlocal ordinary function would require local counterterms.

## 3. The retained state is an actual analytic record

The state space is the image $\mathscr Z_d=\mathcal Z(\mathscr F_d)$ with its displayed two actual distribution-valued entries. The inverse is

$$
\mathcal I(C_A,R_A)=C_A+R_A=A.
\tag{87.6}
$$

The sum is the actual positive-regulator smooth family before any product is formed. It is not a reconstruction from finitely many coefficients, a reconstruction from a formal series alone, or an appeal to graph provenance. In particular, the entire actual regular remainder is retained, including any information invisible to a formal asymptotic expansion.

For a composable actual kernel operation $F$ whose output is in the model class, define the corresponding record operation by

$$
\widehat F(z_1,\ldots,z_k)
=\mathcal Z\big(F(\mathcal I z_1,\ldots,\mathcal I z_k)\big).
\tag{87.7}
$$

This formula has mathematical content because Theorem 87.1 proves the local finite subtraction, strong remainder and uniqueness, while (87.6) explicitly checks the analytic inverse. It does not transport an arbitrary operation on formal graph labels. Any identity between the actual allowed kernel operations is an identity on these records by (87.6)–(87.7).

For same-variable products, reconstruct the two smooth families first. Pointwise products of (87.3) again have this form, since products of Schwartz profiles are Schwartz, with the appropriate combined scalar degree. For insertion from a source into the studied host, reconstruct its smooth source family, pull it along the source-coordinate projection and multiply by the actual smooth complement. The connected Gaussian backbone of the resulting graph proves membership in (87.3). This is the typed insertion domain. It includes the exact source/complement operations used below; it is not a claim about arbitrary products of distributions.

For external disjoint products, $f\otimes g$ is Schwartz in the combined relative coordinates, so the same theorem applies directly. Consequently the induced product is associative and symmetric. Different legal parenthesizations reconstruct the same smooth product and give the same entire record. In particular, moving $\epsilon^2$ from a source factor to its complement gives exactly the same whole-host record, rather than just the same finite output.

**No overlapping singular products occur.** The inverse sum is performed before same-variable multiplication. It would be invalid to expand (87.7) into a product $C_A C_B$ on overlapping collision diagonals. On independent variable sets the exterior tensor products are well-defined, so coefficient convolution is legitimate.

The visible finite map is $\mathrm{ev}_0(C_A,R_A)=\lim R_A=\mathrm{CT}A$. If $A\sim\sum a_n\epsilon^n$ and $B\sim\sum b_n\epsilon^n$, disjoint composition gives

$$
\mathrm{ev}_0(z_A\widehat\boxtimes z_B)
=\sum_n a_n\boxtimes b_{-n}.
\tag{87.8}
$$

Only finitely many terms occur, because both series are bounded below. A direct Taylor estimate on the product Schwartz profiles proves this coefficient formula and its strong remainder. It is generally larger than $a_0\boxtimes b_0$. For example, $A_\epsilon=\epsilon^{-1}\kappa_\epsilon$ on each of two independent lines has zero finite value individually, but their disjoint product has the nonzero constant coefficient $(\delta''\boxtimes\delta+\delta\boxtimes\delta'')/2$. This is a control requiring retention of the record, not a new claim of finite-output multiplicativity. No fixed cutoff works uniformly over all future insertions, consistently with 071.

## 4. Vertex operators and regulator transport

Any continuous linear distributional operator independent of the regulator commutes with coefficient extraction when it preserves the stated domain. In particular actual vertex differentiation and multiplication by a fixed polynomial satisfy

$$
\mathrm{PP}(D A)=D\mathrm{PP}A,
\qquad \mathrm{CT}(D A)=D\mathrm{CT}A.
\tag{87.9}
$$

The proof is application of the operator to the strong remainder estimate, or the moment formula (87.4). Thus these operators act entrywise on the two entries of the record. The same-variable product rule holds on the records because it holds on the reconstructed smooth families.

Regulator scalar multiplication must instead be reprojected: $\epsilon^r a_n\epsilon^n$ can cross the pole/regular boundary. Define its action using (87.7), not by declaring $\epsilon^r C_A$ to remain a principal part. This corrects precisely the faulty commutation of pole projection and regulator allocation in 083.

For $s>0$, put $(Q_s A)_\epsilon=A_{s\epsilon}$. Its coefficients are $s^n a_n$. Therefore

$$
\mathrm{PP}(Q_sA)=Q_s\mathrm{PP}A,
\mathrm{CT}(Q_sA)=\mathrm{CT}A,
\qquad \widehat Q_s\widehat Q_t=\widehat Q_{st}.
\tag{87.10}
$$

An invertible linear change of vertex normal coordinates also commutes with coefficient extraction by its continuous distributional pullback. Coordinate dilations and regulator rescaling commute and retain their actual composition laws on records. This is a regulator/coordinate transport theorem. It is not a new quantum cochain connection or a claim of BV nilpotence.

## 5. Source-intrinsic finite forest normalizations

The canonical actual-family record (87.5) is distinct from a source-channel forest certificate. We now show that the prescribed finite value $N_\gamma=\mathrm{CT}T_\gamma$ can also be realized by a complete intrinsic forest calculation, including all finite normalizations of its proper sources.

In strictly increasing source edge count, define

$$
\begin{aligned}
\overline R_\gamma^N
&=T_\gamma+
\sum_{\substack{S\ne\varnothing\\S\text{ proper spinney}}}
(-1)^{|S|}\left(\prod_{\beta\in S} C_\beta^N\right)
T_{\gamma\setminus S},\\
C_\gamma^N
&=\mathrm{PP}\overline R_\gamma^N
+\mathrm{CT}\overline R_\gamma^N-N_\gamma,
\qquad N_\gamma=\mathrm{CT}T_\gamma,\\
R_\gamma^N&=\overline R_\gamma^N-C_\gamma^N.
\end{aligned}
\tag{87.11}
$$

The constant terms in the second line are actual local distributions, viewed as constant regulator families. The product over a spinney is only over vertex-disjoint sources. Every jet acts on the entire smooth positive-regulator complement through the full normal Leibniz rule. The old rule that inserts only the complement's value is not used.

**Theorem 87.2.** On this finite source family, including its finite decorations, recursion (87.11) is well-founded. Every $C_\gamma^N$ is a finite local pole-plus-finite counterterm calculated from that source channel alone, independently of a containing supergraph. The renormalized source has the strong limit

$$
\lim_{\epsilon\downarrow0}R_{\gamma,\epsilon}^N
=N_\gamma=\mathrm{CT}T_\gamma.
\tag{87.12}
$$

**Proof.** The primitive source case follows from Theorem 87.1. Assume the proper source counterterms already constructed. Their finitely many local normal jets multiply the smooth regulated complement unambiguously. For disjoint sources their normal directions are independent. In scaled source/quotient coordinates, each insertion is a finite sum of delta derivatives in source normals times a rapidly decreasing Gaussian/Wick profile in the quotient. The Gaussian backbone is connected after contraction. Thus the same test Taylor argument, with finitely many additional test derivatives, gives a bounded-below strong Laurent expansion. Its coefficients are supported on the full collision diagonal of the source. This proves that every term in (87.11) is defined, local and finite-order. The finite subtraction $\mathrm{CT}\overline R_\gamma^N-N_\gamma$ is therefore allowed. After removing poles, subtracting this difference leaves precisely the finite value $N_\gamma$, with a strong vanishing remainder. The finite source poset makes the induction well-founded. Only source and subsource data were used. $\square$

For a homogeneous decorated source of effective degree $h$, its pole jets have degree less than $h$, and its possible finite jet has degree $h$. Negative $h$ gives neither a pole nor a finite jet. This is a finite bound for each input, not a uniform bound for every decoration. The general moment convention is $(-1)^{|\alpha|}m_\alpha\partial^\alpha\delta/\alpha!$; odd decorated sources are not assigned an incorrect even-jet sign.

**What is invariant.** Equal evaluated raw families give equal canonical records and equal limits in (87.12). Individual auxiliary source-channel counterterms in (87.11) need not descend when the channel allocation changes. They are a local computational certificate for the invariant finite value. Their prepared remainders are not substituted for the canonical full record in later insertion. This explicitly avoids hiding the old presentation dependence inside an allegedly canonical counterterm operator.

Finite normalization of a proper source can change the pole part of a containing source after insertion. Accordingly every proper counterterm must be recomputed; adding one finite term to the old host calculation while keeping its proper counterterms fixed is not our construction. For the converted host the legal disconnected spinneys are exactly $(023,145)$ and $(123,045)$. Overlapping $F_4$ and $F_5$ remain alternatives and their singular counterterms are never multiplied.

For any old source-channel forest finite value $F_a(T)$, the overall finite correction to the new value is

$$
q_a(T)=\mathrm{CT}T-F_a(T),
\qquad q_a-q_b=F_b-F_a.
\tag{87.13}
$$

It is local on this concentrated model and obeys the three-presentation cocycle identity by cancellation. Thus the 083 allocation discrepancy is cancelled by an explicit finite contact correction. Equation (87.11) separately realizes the same target with every proper source's normalization recomputed.

## 6. Exact repaired values on the actual host

Suppress the common factor $(2\pi)^{-3}$ in the following displayed moments. The reduced determinants are $\tau(G)=96$ and $\tau(H)=192$. The Gaussian variance of $t$ is $1$ on $G$ and $1/2$ on $H$. For tests equal to the named polynomial near the full collision, the finite values are

$$
\begin{array}{c|c|c}
\text{actual family}&\text{test}&(2\pi)^3 N_H\text{ paired with test}\\ \hline
T_H^\kappa&t^6&5\sqrt3/64\\
\epsilon^2T_H^\kappa&t^4&\sqrt3/32\\
P_\epsilon(t)K_{G,\epsilon}&t^4&23\sqrt3/48\\
\epsilon^2P_\epsilon(t)K_{G,\epsilon}&t^2&\sqrt3/8
\end{array}
\tag{87.14}
$$

The second and fourth rows are independent of which edge carries the displayed scalar. All four values are nonzero. The first two follow from ordinary Gaussian sixth/fourth moments and the two determinants. They differ from the old prepared finite values because the finite normalization has been changed explicitly.

**Explicit local subtraction operators.** Let $Q_G$ be the reduced Gaussian Laplacian, $H_G=Q_G^{-1}$ and $L_0=\sum_{i,j}(H_G)_{ij}\partial_i\partial_j$. Put $w=e_5-e_4$. Direct inversion gives $H_Gw=w/2$, so its derivative direction is exactly $D$, and the converted covariance has operator $L_1=L_0-D^2/2$. Set $\nu=(2\pi)^{-3}\sqrt3/12$. On the two principal host families the actual counterterm and finite value are

$$
\begin{aligned}
C_\kappa&=\frac{\nu}{2}\left(\epsilon^{-6}
+\frac{\epsilon^{-4}}2L_1+\frac{\epsilon^{-2}}8L_1^2\right)\delta,
&N_\kappa&=\frac{\nu}{96}L_1^3\delta,\\
C_P&=\nu\left(\epsilon^{-4}
+\epsilon^{-2}\left(\frac12L_0+\frac14D^2\right)\right)\delta,
&N_P&=\nu\left(\frac18L_0^2+\frac18L_0D^2-\frac1{96}D^4\right)\delta.
\end{aligned}
\tag{87.14a}
$$

The corresponding regular remainders are the actual family minus its displayed $C$. Thus these formulas are finite, directly executable subtractions for the original fixed kernels. They do not require evaluating a formal infinite series. For the allocated inputs, reprojecting the actual family gives

$$
N_{\epsilon^2T^\kappa}=\frac{\nu}{16}L_1^2\delta,
\qquad N_{\epsilon^2T^P}=\nu\left(\frac12L_0+\frac14D^2\right)\delta.
\tag{87.14b}
$$

These operators apply to the actual full family, so the edge that carried the scalar is absent from the result. Gaussian conditioning gives the marked coefficients: its moment-generating expression is the Gaussian factor with covariance $H_G$ times $\sqrt{2\pi}P_{\sqrt2}$ evaluated at the tilted mean. Taylor extraction yields the finite operators above. This use is asymptotic on compact smooth tests, not convergence of an infinite delta-jet series.

As a check that proper-source finite terms really propagate, the fully recomputed auxiliary host's finite counterterm, paired with $t^6$ and divided by $(2\pi)^{-3}$, is

$$
\frac{265\sqrt2}{1536}-\frac{70285\sqrt6}{186624}
+\frac{8860\sqrt7}{27783}-\frac{41\sqrt{30}}{810}.
\tag{87.14c}
$$

It is not obtained by retaining the old proper pole-only counterterms and changing just one host coefficient. The raw actual-family counterterms (87.14a) and this auxiliary forest certificate have the distinct roles specified in section 5.

For the marked rows, let $T,Z$ be independent standard normal variables. Then $P_1(T)=\mathbb E(|T-Z|\mid T)/2$. The marked moment is obtained from the joint Gaussian and the absolute moments of $T-Z$. Equivalently, the independently checkable Stein recurrences for $I_n=\sqrt\pi\mathbb E[T^nP_1(T)]$ and $J_n=\sqrt\pi\mathbb E[T^nP_1'(T)]$ give

$$
I_2=3/2,\quad I_4=23/4,\quad I_6=273/8,
\quad I_8=4353/16,\quad J_7=531/16.
\tag{87.15}
$$

More explicitly, integration by parts in the standard normal variable gives $I_{n+1}=nI_{n-1}+J_n$ and $J_{n+1}=nJ_{n-1}+k_n$, with $I_0=1$, $J_0=0$, $k_{2m}=(2m-1)!!/2^{m+1}$ and $k_{2m+1}=0$. The Gaussian backbone contributes the remaining normalized factor $\sqrt3/12$. These formulas prove the marked rows and supply an independent scalar check on the multivariate Schur computation.

## 7. The actual marked derivative identity

Put $D=(\partial_{x_5}-\partial_{x_4})/2$, so $Dt=1$. Direct differentiation of the actual Gaussian complement gives

$$
D^2(P_\epsilon(t)K_{G,\epsilon})
=\kappa_\epsilon(t)K_{G,\epsilon}
-2t\epsilon^{-2}P_\epsilon'(t)K_{G,\epsilon}
+(t^2\epsilon^{-4}-\epsilon^{-2})P_\epsilon(t)K_{G,\epsilon}.
\tag{87.16}
$$

It is the actual tangent derivative, not independent differentiation of a marked edge after forgetting vertex-cycle relations. Apply (87.9) to obtain the same identity on the finite values, and (87.7) for the full record identity. Each term belongs to the stated concentrated model. By (87.12), its finite value is also realized by the finite-normalized source recursion for that decorated channel.

On the test $t^6$, the four terms on the right have respective normalized values

$$
\frac{5\sqrt3}{64},\qquad
-2\frac{177\sqrt3}{64},\qquad
\frac{1451\sqrt3}{64},\qquad
-\frac{91\sqrt3}{32}.
\tag{87.17}
$$

Their sum is $115\sqrt3/8=30(23\sqrt3/48)$, exactly the left side because $D^2t^6=30t^4$. Dropping the mixed terms fails this nonzero check. The same fixture also checks the actual identity $P_\epsilon''=\kappa_\epsilon$ on every proper-source counterterm tensor, using the two different kernel presentations.

## 8. Why the construction answers the bounded question

The procedure is (87.5) with actual operations (87.7) and finite evaluation. Its local counterterms and strong finite limit are proved, its input equivalence is actual kernel equality, and its full record has an explicit analytic inverse. Recursion (87.11) realizes its finite values by source-intrinsic local pole-plus-finite subtractions on the tested forest model. Equations (87.14)–(87.17) give nonzero, quantitative repaired outputs on the old failure and marked Ward controls. There is no appeal to a fitted graph label or to a finite truncation that cannot support future insertion.

This is a consistent subtraction-record procedure for the declared model. It does not make the finite evaluation map multiplicative or define a closed BV algebra on the finite distributions. It does not prove interacting QME, a zero-scale operator on all distributional kernels, liquid degree-two surjectivity or the original GB2/R4 synthesis. Those original objectives remain open.

For comparison only, Brunetti–Fredenhagen's [extension theorems 5.2–5.3](https://arxiv.org/pdf/math-ph/9903028) describe finite local normalization freedom under their finite-scaling-degree hypotheses. The present proof uses explicit regulated profiles and their moments; it does not identify this concentrated regulator problem with an extension of a nonzero off-diagonal distribution or import a general BV compatibility theorem from those results.

## 9. Exact finite evidence and claim boundary

The accompanying [forest fixture 087](fixtures/check_consistent_subtraction_087.py) rebuilds all 277 proper sources with the finite term in (87.11), including both disjoint spinneys. It computes the two delta allocations, the marked Wick case and its allocations, the alternative $P''$ presentation, and all marked tangent terms. It uses exact rational/squarefree-radical arithmetic and Schur integration; separate scalar Stein recurrences check the marked constants. It also retains signed delta-jet, regulator-shift and disjoint cross-contact controls. The [separate operator check](fixtures/check_subtraction_operators_087.py) imports no producer code: it independently inverts the two reduced matrices and verifies the entire constant-coefficient Ward polynomial, rather than one pairing. Finite computations check those algebraic outputs; the strong-limit and record-coherence theorems are the proofs above.

Local execution is CHAD Windows, CPython 3.12.12 in the isolated project evidence environment, with explicit external GCL uv/bytecode caches. There is no admitted root uv lockfile; this is an unpinned mathematical evidence environment. No dependency installation, host-Python shortcut, hosted compute or deployment is used. Exact final fixture/source identities and final replay/critical/editorial disposition belong in acceptance ledger 089 before tracker closure.
