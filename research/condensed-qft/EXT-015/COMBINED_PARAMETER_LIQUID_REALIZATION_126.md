# EXT-015 REACH / 126 — a combined smooth-parameter and liquid-source realization

**Disposition: positive construction candidate on the actual whole-source graph rule; unreviewed.** This constructs a sheaf with values in the fixed real liquid heart. At a profinite coefficient point it recovers123's retained manifold-family sheaf; at a manifold parameter point it recovers108/111's liquid object on every profinite test. The new analytic step is a finite-loss lifting lemma for a Fréchet quotient. It supplies genuine finite-order coefficient lifts from the admitted whole-source jet witnesses, without assuming a smooth section of a quotient or injectivity of completed tensor transition maps. Pointwise membership in the analytic image is not enough and is not the domain here. Review127 and ledger128 remain separate.

## 1. Frozen category, two tests and exact scope

Work in $\mathcal A=\mathrm{Liq}_p(\mathbb R)$ for fixed $0<p\le1$, in ZFC, with the same one-dimensional physical model and interval basis. CP097 binds this construction from28971a49b7ce775306d1ca1ffab29088a53cf8d7 on `research/reach-combined-input-frozen-20261101`. The expanded same-cut input manifest has56 exact scientific sources and SHA256 `a4b8ee2d034ded4f6fac4f7a728fb0ef83af2fbc4b102e1fe5a15ea565754729`. Its critical construction inputs are:

| Input | Exact Git blob |
| --- | --- |
| Source/profile realization091 |c517fe1ae46bcaa9f4a3fc0e64381ae8096bfe27 |
| Scalar heat stages105 |a8ce66ff0edec33e2aff299550fca2089d671033 |
| Mixed source and rapid quotient108 |587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| Quantum record theorem111 |b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| Unit comparison114 |ee4bfb46c5565b90d6f9015765edc8a773b0997a |
| R1 joint-source comparison117 |e95b1155ebb2018a80d2dc559560730fd7ea6594 |
| Parameter obstruction120 |89f910e1d04d82da3f45d00c4ac7bb3ad0fbad13 |
| Retained module-sheaf theorem123 |c5195a38414e3b45dbf75bb89b0db055ce01a5a2 |
| Its exact-source review124 |e68ed185d489cf75c97207e8f28e136f098078b8 |
| Retained-family acceptance125 |5386a13c92d607145d7fb32fb4a2b48d47c5186c |

There are two different variables in the conclusion: $M$ is a smooth finite-dimensional parameter manifold, and $S$ is a profinite coefficient test. For each physical open $U$ the construction gives a liquid-valued parameter sheaf $\mathbf F_U$, and thus a two-variable sheaf $\mathbf F_U(M)(S)$. Its required recoveries are

$$
\mathbf F_U(M)(*)\cong\mathfrak F^J(M;U),
\qquad
\mathbf F_U(*)(S)\cong\widehat{\mathcal O}_{\mathcal Z}(U)(S).
\tag{126.1}
$$

The first star is a profinite coefficient point; the second formula fixes the manifold parameter at a point. This does not make manifold point evaluation faithful.120's ghost is retained.

Use the module-sheaf differentiable convention explicitly audited in123, not the stronger inherited concrete convention. The construction supplies actual liquid-valued scalar, connection, quantum and comparison maps. It does not assert a universal liquid-to-DVS functor, a derived internal-Hom formula, current pro-category lifting axioms or extended target Weiss descent.

## 2. Whole analytic histories and the family rule being realized

Fix a finite analytic history $h$ from108.7: a finite list of compact supports, admissible R1 cones, scalar stages, partition inclusions, finite normal derivatives and proper physical projections. Normal/parity and finite permutation data are included. At one Sobolev refinement write its complete coefficient source as a finite sum

$$
H_{h,s}=
\bigoplus_{\nu\in h}
\left(E_{s_\nu,K_\nu,\Gamma_\nu}
\mathbin{\widehat\otimes}_{\pi}S_{\lambda_\nu}\right).
\tag{126.2}
$$

The scalar stages $S_{\lambda_\nu}$ and finite geometric histories are fixed. The order vector $s$ may be relaxed. The continuous history evaluation

$$
e_{h,s}:H_{h,s}\longrightarrow\mathcal D'((0,e_0)\times U^n)
\tag{126.3}
$$

is the ENTIRE actual positive-regulator source expression, with its actual physical densities. Its positive-regulator smooth pairings and every regulator derivative are the continuous maps proved in108. No independent value is chosen for each regulator. Relaxing $s$ gives continuous coefficient maps commuting with(126.3); their completed tensor maps are not assumed injective.

These coefficient sources are Fréchet. For a fixed scalar stage105, the finite corner atlas, locally finite index families, integer truncation depths, multi-indices, compact exhaustions and remainder weights give a countable defining family of seminorms. Each recursive face-coefficient request uses the same countable choices and finitely many faces. The completeness proved in105 therefore gives a complete metrizable locally convex space. The graph spaces $E_{s,K,\Gamma}$ are Fréchet by108. Completed projective tensor products and finite sums of Fréchet spaces are Fréchet. This argument uses no nuclearity of a graph or scalar stage and no tensor-injectivity claim.

Here is the exact source-family witness rule used in the recovery proof. Locally on a parameter chart, an admitted joint family has one finite history and fixed scalar stages. Its parameter jets have continuous lifts $c_\alpha(a)$ in whole sources $H_{h,s_\alpha}$, with the prescribed compact-set bounds. Their evaluated ENTIRE source families are the actual parameter derivatives, with distributional compatibility; their regulator jets are the already defined derivatives of(126.3). A finite collection of jet requests can be placed in a common relaxed order stage. This is the actual analytic/source graph-jet rule of108 section8 and117 section7. It is not the statement that an arbitrary smooth output has pointwise values in $\mathcal P_n$. In particular no such arbitrary output is supplied with source lifts by assumption or by the proof below.

For source families given directly by R1 plots and scalar coefficient plots, these witnesses are their actual coefficient jets. Compact parameter images and the finite-order refinement argument117.1 provide the required graph orders. Completed coefficient families are admitted with the same whole-source jet witness rule; they are not replaced by unrelated regulator slices. The proof will allow relations invisible under the full history. It does not require that a tensor representative itself have all derivatives in a single fixed $H_{h,s}$.

## 3. A finite-loss Fréchet lifting lemma

The principal issue is genuine parameter lifting, not completeness of an ambient moderate graph. We use the following elementary lemma.

**Lemma126.1 (finite-loss parameter lift).** Let $q:X\twoheadrightarrow Y$ be a continuous surjective map of Fréchet spaces. On a finite-dimensional parameter chart of dimension $d$, every $C^p$ map into $Y$ has, locally, a $C^r$ lift into $X$ when $p\ge r+d+2$. No linear section or continuous lifting operator on spaces of maps is asserted.

**Proof.** Multiply by a smooth parameter cutoff equal to one on a smaller chart and extend by zero to a torus. It suffices to lift a $C^p$ map $f:\mathbb T^d\to Y$. Complexify and pair conjugate Fourier coefficients to return to the real case. Choose increasing defining seminorms $P_j$ on $X$ and $Q_m$ on $Y$. The Fréchet open mapping theorem gives $m(j)$ and $C_j$ such that each Fourier coefficient $y_k$ has an exact lift with

$$
P_j(x_k)\le2C_jQ_{m(j)}(y_k)+\langle k\rangle^{-p}.
\tag{126.4}
$$

The additive term matters when the quotient seminorm vanishes. Integration by parts in a coordinate with largest frequency gives $Q_m(y_k)\le B_m\langle k\rangle^{-p}$. Choose integers $j(k)\to\infty$ sufficiently slowly that $2C_{j(k)}B_{m(j(k))}+1\le\langle k\rangle^{1/2}$ outside finitely many frequencies. Choose the exact lift at that index. For every fixed $j$ and sufficiently large $k$, monotonicity gives

$$
P_j(x_k)\le\langle k\rangle^{-p+1/2}.
\tag{126.5}
$$

The series $\sum_kx_ke^{ik\cdot a}$ and every derivative through order $r$ converge absolutely in every defining seminorm, since $p-r-1/2>d$. Completeness gives a $C^r$ map into $X$. Its image has the same Fourier series as $f$, hence equals $f$. Choose conjugate-paired lifts to make it real. Restriction to the smaller chart proves the local statement. Choices depend on the given map and on $r$. $\square$

Apply this to a WHOLE history. The kernel $K_{h,s}=\ker(e_{h,s})$ is closed because the target of(126.3) is Hausdorff, so $Y_{h,s}=H_{h,s}/K_{h,s}$ is Fréchet. It injects continuously into the actual positive-family envelope. For finitely many continuous whole-source jet witnesses placed in one $H_{h,s}$, their classes in $Y_{h,s}$ satisfy the actual derivative identities. They are genuine $C^p$ jets there. To check this without assuming the injection is a topological embedding, integrate the continuous proposed derivative along a coordinate line in the complete Fréchet quotient. Its image satisfies the fundamental theorem after every distributional test, so equals the original evaluated family. Injectivity identifies the two quotient values. Iterate for the finite jet order.

Lemma126.1 now gives genuine $C^r$ coefficient lifts in a finite relaxed $H_{h,s}$, using finitely many higher parameter jets. Different finite orders may require different lifts. Their ENTIRE evaluated histories agree. This proves the lifting step rather than asserting that a smooth map into an image automatically lifts. No injectivity of $E_s\widehat\otimes_\pi S_\lambda\to E_t\widehat\otimes_\pi S_\lambda$ is used.

## 4. Complete compatible coefficient-row stages

On a parameter chart $V\subset\mathbb R^d$, fix a sequence of finite order refinements $s_r$, $r\ge0$, with the same finite history and scalar stages. Define $J_{h,\mathbf s}(V)$ by variables

$$
b_{r,\alpha}\in C^0(V,H_{h,s_r}),
\qquad |\alpha|\le r,
\tag{126.6}
$$

with compact-open source seminorms. Impose two sets of closed compatibility conditions:

1. Within row $r$, $\partial_{a_i}b_{r,\alpha}=b_{r,\alpha+e_i}$ whenever $|\alpha|<r$, as distributions in the parameter with values in $H_{h,s_r}$.
2. Between rows, $e_{h,s_r}(b_{r,\alpha})=e_{h,s_t}(b_{t,\alpha})$ whenever $|\alpha|\le\min(r,t)$, as ENTIRE actual positive-regulator families, distributionally in all variables.

The first condition is coefficient-level compatibility, not just an equality after geometric pushforward. It makes each row a genuine $C^r$ coefficient lift by the vector-valued fundamental theorem. The second respects actual source equality. Tensor representatives in different rows need not agree, and no quotient kernel is assumed smoothly split. Regulator derivatives are supplied by the continuous maps of(126.3), not by independent variables.

**Lemma126.2.** Each $J_{h,\mathbf s}(V)$ is a complete Fréchet space. Its evaluation is an actual joint analytic/source family, with all the prescribed parameter and regulator jets. The corresponding source construction has the same local real families as the rule in section2.

**Proof.** Every $C^0(V,H_{h,s_r})$, with a countable compact exhaustion, is complete Fréchet. Continuous parameter functions have vector-valued distributional derivatives, defined by integration against compact parameter tests in the complete coefficient space. Derivative compatibility is a closed linear condition in a Hausdorff vector-valued distribution space. Actual-history equality is likewise the kernel of a continuous map into ordinary distributions. Thus(126.6) with both conditions is a closed subspace of a countable product of complete Fréchet spaces.

For any requested finite derivative order, use a sufficiently deep row. Its coefficient map is genuinely differentiable to that order, with continuous source jets bounded on compact parameter sets. Continuous whole-history evaluation gives the corresponding derivatives of the actual family. Cross-row equality makes them independent of the row. The fixed source estimates108 give all mixed regulator bounds and retain the complete scalar normal-profile information. These are exactly admitted joint-source families, not arbitrary output-smooth families.

Conversely take the whole-source jet witnesses of section2 on a chart. For row depth $r$, put the finitely many jets through $p=r+d+2$ into one order refinement. The quotient argument following Lemma126.1 makes the actual family $C^p$ into $Y_{h,s}$. With one fixed parameter cutoff on a slightly larger chart, that lemma supplies a $C^r$ coefficient lift on a common smaller chart. Do this for all $r$. Each lift represents the same actual family; differentiating its history gives the cross-row relations. Taking its genuine coefficient derivatives gives(126.6). All rows use the original fixed history and scalar stages; only finite Sobolev refinements change. Countably many choices give one sequence of rows. This proves local recovery in both directions.

The argument requires the continuous ENTIRE source jet witnesses in section2. It supplies neither witnesses nor recovery for a family admitted only by pointwise membership in the analytic image and polynomial output derivative bounds. $\square$

This row construction also covers finite joins of histories and finite graded invariants. On a general manifold use coordinate charts and local restriction. Smooth parameter pullback and coordinate changes send a $C^r$ row to a $C^r$ row; the chain rule uses finitely many terms at each order. Sheafification below removes the requirement of one global history or one global order sequence on a noncompact manifold.

## 5. Actual liquid images and the uniform rapid quotient

Complete Fréchet graph stages have their admitted real liquid realizations. Let $W_n(V)$ be the coproduct of $\underline{J_{h,\mathbf s}(V)}$ over the allowed finite histories and sequences. Pairing with physical Schwartz tests supplies a map to the ordinary internal Hom envelope

$$
\mathscr E_n(V)=
\underline{\mathrm{Hom}}_{\mathcal A}
\left(\underline{\mathcal S(\mathbb R^n)},
\underline{C^\infty(V\times(0,e_0))}\right).
\tag{126.7}
$$

Each fixed target seminorm requests finitely many parameter and regulator derivatives on a compact set. A corresponding row and108's fixed-source test estimate bound it by finitely many graph seminorms times one physical test seminorm. This gives the actual condensed bilinear pairing and the liquid tensor/internal-Hom adjunction. The internal Hom in(126.7) is ordinary; no derived concentration is asserted. Put $A_n(V)=\mathrm{im}(W_n(V)\to\mathscr E_n(V))$.

Define uniform rapid graph sources separately. For compact physical support $K$ and fixed finite orders $t_{\alpha,k}$, use compatible continuous actual arrays $r_{\alpha,k}(a,\epsilon)\in H^{-t_{\alpha,k}}_K$ whose parameter and regulator derivatives are the next array entries. Require for every compact parameter set $C$ and every integer $L\ge0$

$$
\sup_{a\in C,\,0<\epsilon\le e_0}
\epsilon^{-L}\|r_{\alpha,k}(a,\epsilon)\|_{H^{-t_{\alpha,k}}}<\infty.
\tag{126.8}
$$

The finite orders do not depend on $L$. Weighted continuous-curve products, closed derivative equalities and a countable compact exhaustion make these complete Fréchet graph spaces. Their zeroth entry is one actual entire curve and the other entries are its derivatives. Their liquid image in(126.7) is denoted $R_n(V)$; it is an ambient rapid image, not declared analytic by itself. Define in the liquid heart

$$
N_n(V)=A_n(V)\cap R_n(V),\qquad
Q_n(V)=A_n(V)/N_n(V).
\tag{126.9}
$$

These are actual image, intersection and cokernel objects. Equality in $A_n$ is actual equality of the full evaluated family, not a graph label or coefficient series.

The intersection has concrete complete witnesses. For one analytic graph source and one rapid graph source, impose equality of their actual evaluations. This is a closed condition in a Hausdorff ordinary distribution envelope, so its graph is complete. Its liquid images cover $N_n$: on a profinite test take an extremally disconnected cover lifting both image representatives, use compactness for finitely many stages, and compare their actual test pairings. The continuous source plot lands in that closed equality graph. Descent gives the intersection. This uses no projectivity of an arbitrary profinite test and no point detection on an arbitrary internal Hom. It is the source-level equality argument already used for actual images in099/108.

## 6. Parameter sheafification and the two exact recoveries

Sheafify $Q_n$ in the smooth manifold variable, with values in $\mathcal A$, and denote the result by $\mathbf F_n$. The liquid heart has the needed limits, coproducts and cokernels, with compact projective free generators on extremally disconnected profinite sets. These are the precise properties of the accepted real-liquid category, as in [Scholze, Theorem6.5](https://arxiv.org/pdf/2605.03655). Complete graph-stage liquid realization is the accepted complete-locally-convex criterion096/108. No blanket assertion that every profinite free object is projective is used.

Here is a useful explicit sheafification check. The usual plus construction uses products and equalizers of matching families and the filtered colimit over cover refinements. Evaluation on an extremally disconnected compact projective test commutes with these limits and filtered colimits. It therefore turns this object-valued plus construction into the ordinary real-vector-valued plus construction. Apply it twice. The compact projective generators detect the resulting sheaf identities and the usual universal property. This supplies the liquid-valued sheafification. For any profinite $S$, evaluation preserves limits, so the resulting $\mathbf F_n(M)(S)$ satisfies manifold descent. It also satisfies profinite descent because $\mathbf F_n(M)$ is liquid. Thus it is a sheaf on the product site generated by manifold open covers and profinite covers. Exactness of arbitrary profinite evaluation was not required.

**Theorem126.3 (both axes).** On the source-family rule of section2,

$$
\mathbf F_n(M)(*)\cong\mathfrak F_n^J(M;U),
\qquad
\mathbf F_n(* )\cong\mathcal Z_n(U)
\quad\text{in }\mathcal A.
\tag{126.10}
$$

The second identity holds on every profinite test, not only at ordinary points.

**Proof.** First fix the manifold parameter at a point. There are no parameter derivatives. Projecting a compatible row graph to its zeroth row factors its entire evaluated image through an original coefficient source $H_{h,s_0}$. Conversely every original whole coefficient source maps to a constant row graph, with the same order at all rows and identical entries. Therefore the categorical actual image is exactly $\mathcal P_n$, on every profinite test. At a parameter point(126.8) is exactly108's rapid curve rule. Its liquid image is $\mathcal I_n^{\mathrm{rap}}$. Thus the intersection and quotient in(126.9) are exactly $\mathcal P_n\cap\mathcal I_n^{\mathrm{rap}}$ and $\mathcal Z_n$. This is equality of actual images through explicit source maps in both directions, not a conclusion from their ordinary points. A smooth cover of a point is split, so manifold sheafification changes no value there.

Next evaluate the profinite coefficient variable at the singleton. This evaluation preserves limits, is exact on the liquid heart and commutes with the filtered colimits in the plus construction, since the singleton is an extremally disconnected compact projective test. Thus $Q_n(V)(*)$ is the actual quotient of whole-source graph families by their actual uniform rapid intersection. Singleton image sections have actual representatives after an extremally disconnected image cover; pullback along a point of that nonempty cover supplies the representative at the singleton. Lemma126.2 identifies these local whole-source families with the admitted joint families of117. Equation(126.8) identifies their denominator exactly with the all-mixed-jet rapid rule, with no parameter pointwise replacement. The same argument applies to equality and to the rapid intersection, so the local identification is injective as well as surjective. Evaluation at the singleton commutes with the plus construction by the preceding limit/filtered-colimit facts. Sheafifying this local identification gives precisely $\mathfrak F_n^J(M;U)$ for every $M$. $\square$

For a general profinite coefficient test, image and quotient representatives are local on extremally disconnected covers. On each such cover compactness gives finitely many whole graph stages; manifold sheafification supplies local parameter representatives. Equality is still actual source equality followed by the uniform mixed rapid relation. No global lift on an arbitrary profinite test is claimed. In particular this construction is not $\mathrm{Map}(M,\mathcal Z_n(S))$ and does not erase120's evaluation kernel.

## 7. Liquid-valued scalars, pullbacks, connection and quantum rules

Let $C_M=\underline{C^\infty(M)}$. Multiplication of a $C^r$ coefficient row by a smooth parameter scalar is a $C^r$ row, and its jets obey the finite Leibniz rule. On fixed graph stages these bilinear maps have finite product-seminorm bounds; they give condensed bilinear maps and therefore liquid maps by the liquid tensor adjunction. The resulting $C_M$ action descends to the actual image, preserves(126.8), and extends over parameter sheafification. Pullback by a smooth parameter map is handled locally by the same finite row chain rule. Neither assertion requires a tensor identity for spaces of sections.

Differentiation uses row $r+1$ to supply the derivatives in row $r$, with the shifted order sequence. It is an actual continuous source graph map. It preserves source equality, and the rapid graph rule is derivative-stable by definition. Hence it defines a liquid-valued parameter connection on $\mathbf F_n$.

Its global target is precisely

$$
\underline{\Omega^1(M)}\otimes_{C_M}\mathbf F_n(M).
\tag{126.11}
$$

As in123, a finite Euclidean embedding and a smooth metric make $\Omega^1(M)$ a finite idempotent summand of $C^\infty(M)^N$. Realize that same idempotent in the liquid heart and apply it to $\mathbf F_n(M)^N$. Local coordinate derivative formulas glue into this finite summand. This is ordinary relative liquid tensor with a finite projective module, not a derived-Hom identification. The actual Leibniz and chain rules and commuting derivatives prove naturality and flatness in the liquid-valued sheaf.

The physical differentials and Gaussian/Wick contractions of108/111 act on these sources. At a fixed finite history they are continuous finite sums of coefficient maps and fixed geometric source operations. A $C^r$ coefficient row is carried to a $C^r$ row in a finite target refinement; scalar index/history changes are those already computed in108. No finite-separable description of a completed coefficient is assumed. Cross-row equality persists because the operation is on actual families. For a negligible input use its actual intersection witnesses from section5. The finite source estimates and microlocal saturation108.1, applied after each requested parameter derivative, make its output rapid in fixed finite orders. They act on the entire distribution and preserve summed cancellations. Therefore the operators induce liquid maps on(126.9) and the sheafification.

Consequently at fixed positive scale the cochain identities of111 hold in $\mathbf F$, and the parameter connection commutes with the quantum differential. The legal disjoint maps are liquid multilinear maps with their actual finite joint bounds. Matching Wick maps use the typed finite contraction diagrams; matching ordinary maps use117's independent Gaussian cross-difference estimate. The scale connection and transport are the actual retained-family formulas of117/123, now liquid-valued on the combined source construction. Overlaps of singular counterterms are not multiplied.

Apply the construction per finite arity/parity and then per total weight $w=n+2k$. Products over weights are limits in the liquid heart and commute with evaluation on a profinite test. Each fixed output weight uses finitely many input weights and contraction terms. Thus the componentwise weight completion has both recoveries(126.1), its actual flat connection and its split formal tail/truncation tower. This is not an invocation of unverified current pro-category or completed Weiss theorems.

## 8. R1 and physical comparison targets

The comparison maps need actual combined targets and sources, not just vector spaces at points. For R1 use the same parameter-row construction with coefficient source $E_{s,K,\Gamma}$, identity geometric history and no regulator scalar. At a parameter point its liquid source is117's actual $\mathcal C_n^{R1}$ on every profinite test. At a coefficient point its real manifold families are exactly the original locally normal R1 plots. To see the converse direction explicitly, on a compact parameter set finitely many derivatives of a Bastiani normal plot have bounded order. The117 Sobolev/Rellich refinement makes them continuous into one sufficiently weak graph stage. The vector-valued fundamental theorem makes the plot $C^r$ into that stage for the requested finite $r$. Conversely all finite rows give all derivatives continuously in the original complete normal sector, hence a locally normal plot. Denote this liquid-valued parameter source by $\mathbf C_{R1}$.

For the physical classical distributional target use coefficient sources $H^{-s}_K$ with no cone restriction, no regulator and identity history. Let $\mathbf D_n^{\mathrm{cl}}$ be their compatible-row actual-image construction and parameter sheafification. At a parameter point it is the full compact-distribution liquid object on every profinite test: a continuous compact profinite distribution family has common compact support and bounded order, and the same finite Sobolev loss makes its lift continuous. At a coefficient point it has exactly the028 plot rule, continuous linear maps $C^\infty(U^n)\to C^\infty(M)$, locally with common support. A fixed compact parameter set bounds finitely many derivatives of those pairings by a finite physical test seminorm. Shrink the parameter neighborhood to obtain common physical support from the zeroth bound; higher derivative supports remain in it. Sobolev embedding and a further compact loss give the required continuous finite-order derivatives and their genuine finite rows. Conversely those row estimates give exactly continuity into every $C^\infty(M)$ seminorm. This proves the target typing, rather than assuming a quotient formula for $C^\infty(M,E)$.

The actual maps then give

$$
\mathbf J_s:
(\widehat{\mathbf C}_{R1},Q_{R1})\longrightarrow
(\widehat{\mathbf F},Q_s),
\qquad
\mathbf F_{q,s}=\mathrm{CT}_{\mathrm{phys}}W_s^{-1}:
(\widehat{\mathbf F},Q_s)\longrightarrow
(\widehat{\mathbf D}^{\mathrm{cl}},d).
\tag{126.12}
$$

For $\mathbf J_s$ use the genuine fixed-sector source bounds of117 and its typed source/target Wick composition. For the physical map use108's uniform mixed coefficient estimates and123.6b. Each fixed finite derivative request has a finite physical distribution order and a finite source bound, so its coefficient maps define rows of the stated distributional target. Rapid mixed jets have zero physical coefficients. These maps are therefore actual liquid morphisms through source image, intersection, quotient and sheafification, not merely pointwise formulas. They are compatible with the parameter connections, physical supports, interval inclusions and the stated quantum differentials. Their two recoveries are exactly117's liquid map and123's retained module-sheaf maps. The triangle is

$$
\mathbf F_{q,s}\mathbf J_s
=\iota_{\mathrm{dist}}W_0^{-1}.
\tag{126.13}
$$

It follows by actual typed cancellation and finite extraction of the constant R1 family, on the source stages and hence in the combined sheaf. The physical map is not promoted to a factorization morphism:111's Laurent cross-coefficient defect remains. No weightwise quasi-isomorphism follows;114's nonzero unit cone remains at both point variables.

## 9. Hostile controls and the exact acceptance boundary

The two point variables must not be conflated. Evaluating the profinite coefficient variable gives all retained joint $M$ sections, including120's nonzero zero-evaluation ghost and its quantum primitive123. Evaluating the manifold at a point gives the full liquid coefficient object on every profinite test. Neither recovery replaces a retained section by its manifold point values.

The analytic source is still105/108's declared full normal-profile class. Moment-flat spatial profiles are retained because the image envelope tests actual positive families, not physical Laurent coefficients. Uniform rapidness uses one finite Sobolev order for each mixed derivative independently of the requested decay power. Scalar indices and finite geometric histories remain fixed locally, and regulator jets are derivatives of whole source expressions. Arbitrary fixed finite decorations, all277 sources, both legal disjoint spinneys and the087 normalization remain admitted. No raw finite Gaussian-polynomial-only assertion is substituted for that declared class.

The finite-loss lifting lemma is used only to recover real manifold families at the coefficient singleton. It does not choose a natural lifting operator or lift every continuously profinite-parametrized quotient family. General profinite sections instead have the actual cover-local image/quotient semantics. No arbitrary-profinite projectivity, tensor injectivity, nuclearity of $S_\lambda$, universal liquid/DVS functor or ordinary/derived Hom substitution occurs.

The source-rule boundary is essential: the theorem realizes the joint analytic/source families with continuous ENTIRE source jet witnesses in section2. It proves their local conversion to genuine coefficient rows. It does not admit an arbitrary family solely because each regulator slice or each parameter point lies in the analytic image. Such a larger rule would require a different lifting theorem and is not claimed here.

Subject to source-bound critical review, this supplies the missing all-manifold/profinite realization on that exact rule. It is not the full M5 verdict. Current pro-category lifting conditions, support/comparison cones beyond the proved arrows and completed extended target Weiss descent still require their actual theorems or obstructions. Original R3's distinct degree-two support equation receives no new inference. R0/R1/R2 and separate087–089 retain their completed reviewed scopes; R3, full M5/R4 and both parents remain open.

This is one primary construction jointly reasoned by the parent and the delegated construction context. The new finite-loss Fourier lifting mechanism, exact source-rule audit, closed row stages and two-axis recovery require distinct non-author127 scrutiny before acceptance. The parent supplied primary categorical-source checks and the source-kernel cautions; the construction role supplied the explicit finite-loss lift and row realization. No numerical fixture, Python, Git, tracker or external mutation was used to prepare this draft. Exact freeze, one correction, current gates, protected admission/readback and documentary/tracker reconciliation remain separate.
