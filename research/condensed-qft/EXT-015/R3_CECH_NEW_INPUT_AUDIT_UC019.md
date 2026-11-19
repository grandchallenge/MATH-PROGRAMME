# EXT-015 REACH / R3 / UC019 — relevance of the new scalar Čech H² input

**Disposition: new, substantive scalar input; insufficient input to reopen an opposed original-R3 construction cycle. Original R3 remains OPEN.** The new sources prove a locally constant integer H² potential on the genuine categorical Čech triple, and now transport it to actual module/product boundaries conditional on the four-point law. The newer degree-one closure proves an actual second-relation epimorphism in condensed integer modules. Their combination has a useful restricted consequence: second-relation maps into products of discrete integers extend, by a sign-exact argument given below. That consequence does not apply to the original real-liquid coefficients. In fact, every additive morphism from a real-liquid object to such a discrete-integer product is zero. Neither a real-liquid replacement mechanism nor the global finite-coordinate normalization of (84.19) is supplied.

This is one bounded primary relevance audit under CP249, materially refreshed under CP250 before the new input was consumed, not a new positive/negative construction cycle. The primary is a fresh logical role within the same Codex system/account and uses shared frozen sources. It does not supply external independence, mathematical certification, publication authority, or acceptance of its new source-semantic deductions. Distinct UC020 criticism and UC021 disposition remain required. The parent handles administrative admission; it did not coauthor the mathematical arguments below. Only this file is authored by this pass.

## 1. Frozen custody and execution boundary

The initial scientific input was frozen commit `d5d6ee79c1210bfd71976672b418d18ac45e8f53`, persistent ref `research/reach-r3-cech-uc019-input-frozen-20261118`. The ordinary authoring branch is `research/reach-r3-cech-uc019-20261118`; its initial head was the prior-bound CP249 commit `38c38780ef09abf96bae9672c7fb05719973716d`. During primary drafting, new material PR #3465 merged. Dependent finalization paused. The parent bound CP250 at `85f7ad4a7cbe1b8e2fddaa3c0e2f1261be68ab16` before the new module was read. The operative refreshed scientific input is `d365bc625dfbe42be9539085912b206c0b2d07d3`, persistent ref `research/reach-r3-cech-uc019-refreshed-input-frozen-20261118`. All 268 original scientific blobs are unchanged; the formal input manifest now has 132 sources. The external evidence directory is `F:\_codex\MATH\_evidence\reach-liquid-route-20261029`.

- `r3-cech-uc019-input-manifest.json`: 268 original scientific input blobs at the frozen commit.
- `r3-cech-uc019-formal-inputs.json`: 132 CMDG formal input blobs at the refreshed commit.
- `r3-cech-uc019-cmdg-provenance.json`, `r3-cech-uc019-cmdg-degree-one-provenance.json` and their exact formal-run logs: source admission and prior compiler evidence acquired by the parent and inspected here.

Working-copy hashes of the following consumed sources were checked against the frozen manifests. Source IDs in the rest of this note refer to these exact versions. Scientific paths are relative to this directory; formal suffixes expand under `fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P3DerivedCM5R0`.

| Source ID | File or formal suffix | Git blob |
| --- | --- | --- |
| S018 | [FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md) | `81018f669afc062127877a3984e915f1fbea6f39` |
| S019 | [FIXED_SOURCE_EXT1_ISOMORPHISM_019.md](FIXED_SOURCE_EXT1_ISOMORPHISM_019.md) | `6b0fb373b8bde1434b3b443f16274c626e0d954c` |
| S037 | [R3_ALL_SINGLETON_LINEAR_RELATIONS_037.md](R3_ALL_SINGLETON_LINEAR_RELATIONS_037.md) | `68b92dfca0bdd51707f409ff79f2770a310fc4e0` |
| S067 | [R3_EVALUATED_RELATION_COVER_067.md](R3_EVALUATED_RELATION_COVER_067.md) | `7069938ce1e75f946e2f4ff70fcabb2f073065e9` |
| S084 | [R3_POSITIVE_SUPPORT_ATTEMPT_084.md](R3_POSITIVE_SUPPORT_ATTEMPT_084.md) | `932be6cc3445182a8423b23cc4840fe7ad685ced` |
| S085 | [R3_COUNTEREXAMPLE_ATTEMPT_085.md](R3_COUNTEREXAMPLE_ATTEMPT_085.md) | `9f4463bc17cb723043f27965ebfbbef0bf2f657a` |
| S090 | [REACH_CONDENSED_RENORMALIZATION_PLAN_090.md](REACH_CONDENSED_RENORMALIZATION_PLAN_090.md) | `6b642bf10c3328bb64d37474e290810fb45cbca1` |
| S094 | [R3_NEW_INPUT_AUDIT_094.md](R3_NEW_INPUT_AUDIT_094.md) | `f0732cb96a27f540a2209a54d43ced97abb94503` |
| F-ambient | `Interface.lean` | `bca9f2cfd28fbd876042a3de6f6b4e43ac3e9423` |
| F-H2 | `CategoricalScalarH2Potential.lean` | `9aaab0ed255cc5eaeb6101c2b96535211208e3c8` |
| F-iso | `CategoricalTripleRelationIso.lean` | `fe2408d79cc481f565bb79c0de4ae6007f82dac0` |
| F-productH2 | `ScalarCechH2AmbientPotential.lean` | `af47121560a5dcb4a216db3f6a7ad0ed4ac4cac1` |
| F-closedH2 | `ScalarCechH2ClosedRelation.lean` | `560d7a622087d7806fabc97546e82c4abd9b243c` |
| F-epi | `StoneanCechDegreeOneClosure.lean` | `40f47f19a57ca012016d808f6db1355237d7e692` |
| F-probe | `CompHausProbeTrueDegreeOneExact.lean` | `fca2f3b05fad21645d02512d2b267f6728393bd2` |
| F-sections | `DiscreteCoefficientCechBridge.lean` | `d7a3d87c0ea9534facad67f1e7bac1d59e824580` |
| F-products | `DiscreteProductSections.lean` | `dc49a08bb5a73f617395dd25a45e8b1282876652` |
| F-second | `GSCechSecondRelation.lean` | `9973384b8f46c62e22178d9cd121f16afd1c2e4a` |
| F-boundary | `GSCechTripleBoundary.lean` | `014d6ad9b8d9eaa817cee32374087db3e7359898` |
| F-moduleH2 | `ScalarCechH2ModuleBoundary.lean` | `afed16806c96abeb3571333931b937cc445c4327` |
| F-GSproduct | `GSCondensedProduct.lean` | `b13893342bdd5fa3a918bf84eac902ee447c47a0` |

Supporting source inspection includes `StoneanCechTripleCocycle`, `CechTriplePointGeometry`, `TripleClopenBoxFactorization`, `FiniteClosedCoverH2CocycleInduction`, `CechRelationEpi`, `DenseExactnessTransfer`, `CompHausProbeActualTriple`, and `StoneanSolidTargetExtension`. Their exact blobs remain in the formal manifest. Predecessor file headers sometimes describe obligations subsequently resolved by successor files; declarations, imports and exact hypotheses determine the present scope.

### Prior formal replay, with its actual scope

[PR #3464](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3464) protected-merged as `42da96373e691d6f790d014da512d812210d5fd6`, final head `1e115b24fa0003cbecdc99a175a437a4ebf04308`. Its [formal-validation run 44270603087](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/44270603087), job `134686173495`, lane `cmdg-cm4-p3`, contains actual `lake env lean` invocations for F-productH2, F-closedH2, F-iso and F-H2, followed by `FORMAL_VALIDATION_SUCCEEDED`. The F-H2 theorem's printed axioms are exactly `propext`, `Classical.choice`, `Quot.sound`. The saved log SHA256 is `048c657931339a6c0bd837f8bef75c3b6e537de70dcaa3cd347dc066e8ef1e51`.

The frozen F-H2 source SHA256 is `69e05b48c67abe5c0fb7452456f95dc25a8b68bd7fa6c7943cb653d7c5302747`, equal to the source hash in the PR receipt. This is genuine prior compiler evidence, not an inference from a green workflow name. The run's printed local closure does **not** include F-epi or F-probe; their own receipt is distinct.

[PR #3462](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3462), final head `44836ec8e404f35ea7ec998ae0bada656d7c232a`, protected merge `3fd1d27e4d0d3942d2d7fe7f0ec72409f653ad99`, has [formal run 44266732908](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/44266732908), job `134673139305`. Its saved log explicitly compiles F-probe and F-epi, prints the three standard axioms, and ends `FORMAL_VALIDATION_SUCCEEDED`. Frozen SHA256 values match its PR receipt: F-probe `4e9bed54c12d677b0fd8ec29711bb7e002791980870476dc8e4539ba00184b11`; F-epi `35803415fba02ca7fd4597caf3331aee4e64a3345c7b192bec64f8c6e6cecd90`.

[PR #3465](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3465), final head `0ff1e60fdec2ccd3c61191799fcb6d7fc622f18f`, protected merge `306ffbc0132fce89a5bd8210f3de850b19b96fd0`, has [formal run 44277933197](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/44277933197), job `134710973768`. Its own saved log explicitly compiles F-moduleH2, prints both integer and integer-product potential theorem axiom sets as the same three standard axioms, and reports `FORMAL_VALIDATION_SUCCEEDED`. The log SHA256 is `20a3405f8268c7f609fc440f429c9416260062522a33debad8324acab4ed05ce`; the frozen module SHA256 `ab5d83748451b8600aa97385a0b6a6aa1cb46abb2372512434cc1b8bd6d95bad` matches the PR receipt. The evidence is retained in `r3-cech-uc019-cmdg-module-boundary-provenance.json` and `r3-cech-uc019-formal-44277933197.log`.

No Lean compiler is run locally, and the new deductions in this Markdown file are not claimed as compiled Lean results.

## 2. The unchanged original question

Fix the same universe and $0<p\le1$. The original category is the real-liquid abelian category $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$. Retain exactly

$$
\begin{gathered}
H=\underline{\mathcal D_{[-1,1]}(\mathbb R)},\qquad
G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)},\qquad
G=\underline{\mathcal D(\mathbb R)},\\
0\longrightarrow K\longrightarrow P_{\mathrm{red}}\longrightarrow H\longrightarrow0,
\qquad
0\longrightarrow K_1\overset{j}{\longrightarrow}P_1\longrightarrow K\longrightarrow0.
\end{gathered}
\tag{UC19.1}
$$

These are the S037/S067 covers, including the fixed singleton splitting and all retained nonsingleton generators. The objects $K,K_1$ are liquid kernels. Neither is assigned a Fréchet topology. The evaluated relation cover $P_1$ is projective for the admitted extremally disconnected projective-generator reason, not because arbitrary profinite free objects are projective.

The desired assertion, for **every actual liquid morphism** $f:K_1\to G$, is

$$
\exists b,\ f_b:K_1\to G_b,\ \psi:P_1\to G,
\qquad f=\iota_b f_b+\psi j.
\tag{UC19.2}
$$

Under the admitted S018/S019 real strict-LF realization, write $G\simeq E=\bigoplus_{n\ge1}B_n$, with $B_n=\underline s$ and $E_N=\bigoplus_{n\le N}B_n$. The actual stages $G_b$ and finite prefixes $E_N$ factor through one another. S067 proves the stage comparison injective in every degree, not surjective in degree two.

S084/S094 identify the remaining quantifier. For positive rapid weights $r$, let $T_r$ be the actual scaled-measure stages of $H$. In common physical source coordinates,

$$
\begin{gathered}
V_{r,n}=\mathrm{Hom}_{\mathcal A_p}(T_r,B_n)
=\{(a_i)\in s^{\mathbb N}:r_i a_i\longrightarrow0\text{ in every seminorm of }s\},\\
W_n=s^{\mathbb N},\qquad X_{r,n}=W_n/V_{r,n},\qquad X_r=\bigoplus_n X_{r,n}.
\end{gathered}
\tag{UC19.3}
$$

For each quotient Roos 1-cocycle $\alpha$ over the **whole actual weight poset**, one needs a single finite $F\subset\mathbb N$ and $\beta_r\in X_r$, finite-supported separately for each $r$, with

$$
\alpha_{r,t}-(\beta_t|_r-\beta_r)
\in\bigoplus_{n\in F}X_{r,n}
\qquad\text{for every }r\preceq t.
\tag{UC19.4}
$$

This is original (84.19), not a scalar Čech nerve cocycle on one compact profinite presentation. Its weights, quotient coefficients, global finite set and separately finite-supported corrections must all be preserved. No finite quotient of a single compact source supplies those quantifiers.

## 3. What the new declarations actually establish

The CMDG ambient category in F-ambient is $\mathcal C=\mathrm{CondensedMod}(\mathbb Z^{\mathrm{lift}})$. Its target $G_S^{\mathrm{CMDG}}$ is the actual integral free-solid object `(Condensed.profiniteSolid Coeff).obj S`. This notation is deliberately distinguished from original $G$ and $G_b$. There is no declared identification of those targets.

For a profinite $T$, let $P(T)\to T$ be its Stonean presentation, let $R=P(T)\times_TP(T)$ and let $Z=P(T)\times_TP(T)\times_TP(T)$ be the actual categorical fiber products. Write $F_X$ for the free condensed integral module on $X$. The actual first and second relation objects are $K_T=\ker(F_{P(T)}\to F_T)$ and $L_T=\ker(F_R\to K_T)$. Put $i_T:L_T\hookrightarrow F_R$ and $e_T:F_Z\to L_T$.

| Input and exact output | Inference verdict |
| --- | --- |
| F-productH2: a globally locally constant integer function on an arbitrary profinite product triple, satisfying the alternating identity on equal-image quadruples, has a globally locally constant pair potential | Applicable scalar theorem with a genuine hypothesis; neither continuous real coefficients nor arbitrary target objects occur |
| F-closedH2: extend from the closed equal-image triple relation to the product, apply F-productH2, restrict to the pair relation | Removes the ambient-product restriction for integer locally constant cochains; does not transfer coefficients |
| F-iso and F-H2: actual Profinite triple isomorphism and `integerStoneanCechCategoricalTwoCocycle_hasPairPotential` | Resolves the explicit-subspace versus categorical-triple comparison for this scalar statement; the four-point hypothesis remains in the theorem signature |
| F-probe: actual represented CompHaus pair/triple free-module short complex is exact at each Stonean probe, using the correctly lifted Hom sets and the split set-level Čech complex | Genuine objectwise exactness, not a surrogate triple and not a global natural contracting homotopy |
| F-epi plus dense-site/sheafification comparison: the genuine global short complex is exact and `stoneanCechTripleToSecondRelation_epi_unconditional` | Gives $e_T$ epic for arbitrary profinite $T$ in $\mathcal C$; does not split $e_T$ or make $L_T$ projective |
| F-second: the actual second-relation extension criterion for $G_S^{\mathrm{CMDG}}$, using the specified preceding Ext¹ vanishing | An equivalence with the still-needed extension property, not its proof and not an original-R3 theorem |
| F-products: $\mathrm{Hom}(F_X,\prod_I D)\simeq\prod_I\mathrm{LC}(X,\mathbb Z)$, with $D$ the discrete lifted-integer coefficient object | An exact categorical product bridge. Its application to $G_S^{\mathrm{CMDG}}$ requires an explicitly supplied product-model isomorphism. None for original real $G$ is supplied |
| F-moduleH2: `stoneanCechSecondBoundary_integerCocycle_hasPotential` and `stoneanCechSecondBoundary_integerProductCocycle_hasPotential` | Now proves actual free-pair module primitives for integer/product free-triple morphisms satisfying the explicit four-point condition, with sign negation and exhaustive categorical triple points. This conditional scalar-to-module step is achieved; it is not an unresolved bridge in this audit |
| F-GSproduct: `gsFreeSolidToCoefficientProductIso S` | Supplies the actual product model for the integral CMDG target, so it must be credited in the restricted ambient argument. It does not supply a model for original real $G$ |

The finite-observation proof uses that each single locally constant scalar function on a compact profinite triple has a finite clopen observation. Its image-closed sets in the base need not be open; the closed-cover H² induction is the supporting result. For an infinite product of coefficient sheaves, observations may vary with the coefficient index. That is valid product semantics and supplies no common finite output prefix in $E$.

The explicit split contraction in F-boundary assumes a section of the presentation; F-epi later proves an epi without that assumption. The Stonean probe sections may depend on the probe. One may use the actual exactness/naturality/sheafification transfer proved in the successor sources; one may not declare those choices a natural global splitting. The distinction between a Stonean **probe** and an arbitrary profinite **source** is essential.

## 4. A sign-exact restricted consequence and the four-point test

This section supplies a source-semantic deduction, with proof, beyond merely repeating the missing bridge. F-moduleH2 now formalizes the conditional scalar-to-module primitive and the exact sign comparison. What is additionally proved below is the quadruple cancellation for a map on the actual second relation and its combination with the second-relation epi. The universal quadruple morphism identity and resulting extension corollary are not declarations in the inspected formal sources; they are candidates for UC020 scrutiny.

**Lemma UC19.A (epi cancellation).** In any abelian category, let $i:L\to C_1$ be monic, $e:C_2\to L$ epic and $d_2=ie$. If $f:L\to A$ and $b:C_1\to A$ satisfy $fe=bd_2$, then $f=bi$.

**Proof.** Substitution gives $(f-bi)e=0$; cancel the epimorphism $e$. No splitting, projectivity of $L$, or projectivity of $C_2$ is required. The assertion does not construct $b$. $\square$

Here composition is written in the ordinary right-to-left mathematical convention. F-boundary's actual differential is

$$
d_2[x,y,z]=[x,z]-[x,y]-[y,z],\qquad i_Te_T=d_2.
\tag{UC19.5}
$$

Construct the actual profinite quadruple fiber product $Z_3=P(T)^{\times_T4}$ and its four triple projections by the pullback universal property. On the free modules define

$$
\partial_3[x,y,z,w]=[y,z,w]-[x,z,w]+[x,y,w]-[x,y,z].
\tag{UC19.6}
$$

Functoriality of free modules and cancellation of the six pair terms give $d_2\partial_3=0$ as a morphism, not just a numerical test. Since $i_T$ is monic, $e_T\partial_3=0$. Thus for **any actual ambient** $f_L:L_T\to A$, its pullback $f_Le_T$ obeys the four-point identity as a morphism with values in $A$. This proves the semantic identity in that particular actual second-relation diagram; it does not identify $L_T$ with the original $K_1$.

For precision, the cancellation on a related quadruple is

$$
\begin{aligned}
&([y,w]-[y,z]-[z,w])
-([x,w]-[x,z]-[z,w])\\
&\quad+([x,w]-[x,y]-[y,w])
-([x,z]-[x,y]-[y,z])=0.
\end{aligned}
\tag{UC19.7}
$$

It holds as a free-module morphism by the same projection equalities. It does not rely on point evaluations being conservative for arbitrary condensed targets.

**Lemma UC19.B (restricted discrete-product extension).** Assume the exact source declarations of F-epi, F-H2, F-moduleH2 and F-products. For every profinite $T$, every admitted index type $I$, and every actual $f_L:L_T\to\prod_I D$ in $\mathcal C$, there is $b:F_R\to\prod_I D$ such that $f_L=bi_T$.

**Proof.** For each coordinate $a\in I$, apply the free/discrete Hom equivalence to the negative pullback $-\mathrm{pr}_a f_Le_T:F_Z\to D$. It produces an integer locally constant function $c_a$ on the genuine categorical triple. Equation (UC19.6) proves its nonvacuous four-point hypothesis. F-H2 gives a locally constant pair function $b_a$ with

$$
c_a(x,y,z)=b_a(y,z)-b_a(x,z)+b_a(x,y).
\tag{UC19.8}
$$

Transport $b_a$ back through the genuine free/discrete Hom equivalence. Its naturality under pair projections follows directly from the free-forgetful and Yoneda adjunction descriptions in F-sections; F-moduleH2 now proves this sign-compatible comparison explicitly. With the sign in (UC19.5), equation (UC19.8) says precisely $\mathrm{pr}_a f_Le_T=b_a d_2$. Equality of these free-to-discrete morphisms is detected by their locally constant functions on $Z$; F-iso and F-moduleH2 ensure every actual triple is represented by the related-point notation. Assemble the $b_a$ by the categorical product universal property to obtain $b:F_R\to\prod_I D$. Then $f_Le_T=bd_2$, and Lemma UC19.A gives $f_L=bi_T$. Equivalently, apply F-moduleH2 directly to $f_Le_T$ after the quadruple calculation, then cancel $e_T$. No common finite observation across $a$ is asserted or required. $\square$

**Restricted ambient corollary, as an audit candidate.** F-GSproduct actually provides $G_S^{\mathrm{CMDG}}\simeq\prod_I D$, with its specified basis index. Transport Lemma UC19.B across that isomorphism, apply the exact extension criterion in F-second, and obtain degree-two vanishing from $F_T$ into this integral CMDG target, for profinite $T,S$. This is a proved source-semantic implication of the displayed quadruple calculation and the inspected source declarations, submitted for UC020 scrutiny. The actual quadruple identity and this combined corollary are not asserted as existing compiled declarations or independently certified theorems. No universal higher-degree vanishing, full derived solidity or liquid Ext² conclusion follows. Crediting the actual CMDG product model strengthens the bounded result; it does not identify that integral target with original $G$.

**Four-point hostile control.** For the ambient theorem take the two-point profinite $P=\{0,1\}$ over a point and let $c(x,y,z)$ be the indicator of $(0,0,0)$. It is globally locally constant, but on $(1,0,0,0)$ the alternating four-point expression is $1$. Thus the scalar theorem cannot be applied to an arbitrary locally constant triple cochain by dropping its hypothesis. A pair cocycle law for a first-kernel map also has one degree too few. For original $f:K_1\to E$, neither a map to this CMDG $L_T$ nor a scalarization with the necessary differential compatibility is supplied by the new declarations. The four-point proof above applies to $f_L$ in the actual CMDG diagram, not by renaming original $f$.

## 5. The real-liquid coefficient obstruction is explicit

**Lemma UC19.C (no integer-product scalarization of real coefficients).** Let $V$ be any real-liquid object, viewed by restriction of scalars as a condensed integral module. For every admitted index set $I$,

$$
\mathrm{Hom}_{\mathrm{CondensedMod}(\mathbb Z^{\mathrm{lift}})}
\left(V,\prod_I D\right)=0.
\tag{UC19.9}
$$

**Proof.** For every profinite test $S$, $V(S)$ is a real vector space, hence divisible by each positive integer $m$. If $h:V\to\prod_I D$, take a coordinate and a section $v\in V(S)$. Its image is a locally constant integer function $z$ on $S$. For every $m>0$, linearity of $h$ over the integers gives $z=m h_a(v/m)$. Each value of $z$ is therefore divisible by every positive integer, so it is zero. All coordinates of $h(S)$ vanish, for every profinite $S$. Profinite tests determine the condensed morphism, hence $h=0$. Universe lifts do not change divisibility. $\square$

In particular the nonzero original $G,G_b,B_n,E$ cannot be isomorphic, or embed as additive coefficient objects, into any product of these discrete integer sheaves. This rules out using F-products' supplied model as a faithful model for the original real-liquid target. This is an obstruction to that proposed coefficient mechanism, not an obstruction to R3 itself or to other real-valued methods.

Merely extending scalars from the integral theorem is insufficient. An exact comparison would have to identify the actual free/liquid objects and their derived Hom complexes, preserve the relevant boundaries, and represent the real coefficient plots. The scalar theorem's codomain is discrete integers. On an infinite profinite set a continuous real function need not be locally constant: on $\{0,1\}^{\mathbb N}$, the function $x\mapsto\sum_{k\ge1}2x_k3^{-k}$ is continuous and not locally constant. Uniform approximation by finite observations is not an exact primitive in the required coefficient category without a convergence and norm-control theorem. No such new theorem is declared in F-H2.

Even a hypothetical real scalar H² primitive at each fixed profinite presentation would not by itself be new global R3 normalization: S084 already proves coefficient-specific local hypercover acyclicity for these $B_n$ and $E$. Local choices do not control the entire weight-poset cochain or its common output stage. Nuclear tensor flatness concerns a different functor; it does not make Hom exact, split a syzygy, or establish the needed derived-limit additivity.

## 6. Actual projective comparison, higher degrees and both residual channels

An ordinary left adjoint preserving the effective-epi coequalizer justifies the corresponding degree-zero presentation in F-relation sources. It does not justify preserving an entire exact resolution after real base change or liquidification. For original coefficients, S084 uses the distinct derived free-liquid identity, extremally disconnected hypercover levels and controlled coefficient primitives. General profinite pair/triple fiber products need not be extremally disconnected; F-epi does not make their liquid free objects projective. They cannot simply replace the projective $P_1$ in (UC19.1).

There is already a valid conditional projective comparison for the original problem. Extend (UC19.1) to $R_\bullet\to H$ with $R_0=P_{\mathrm{red}}$, $R_1=P_1$, $R_2\twoheadrightarrow K_1$, and write $\widehat f=f\pi_2$. S084 constructs the projective total resolution $D_\bullet\to H$ from the actual weighted stages, with terms summed over weight strings and projective resolutions of those stages. Comparison maps $u:D_\bullet\to R_\bullet$, $v:R_\bullet\to D_\bullet$ and a homotopy $uv-1=dh+hd$ exist because these are actual projective resolutions of the **same** object $H$.

If new input gave a finite-prefix degree-two cocycle $\zeta:D_2\to E_N$ and $\eta:D_1\to E$ with

$$
\widehat f u_2-\iota_N\zeta=\eta d_2^D,
\tag{UC19.10}
$$

then $\zeta v_2$ descends through $\pi_2$ to $f_N:K_1\to E_N$, and S084's homotopy calculation gives

$$
\widehat f-\iota_N f_N\pi_2
=(\eta v_1-\widehat f h_1)d_2^R.
\tag{UC19.11}
$$

Cancel $\pi_2$ and factor $E_N\to G$ through some actual $G_b$ to obtain (UC19.2). Thus an unspecified comparison is not the missing step in this retained route. The missing input is (UC19.4), equivalently the finite-prefix cocycle/boundary data in (UC19.10). The new CMDG nerve resolves a free profinite object $F_T$, not the original $H$ or its weighted total resolution; matching the words “second relation” does not give the required chain map or its hypotheses.

Write $P=\prod_nB_n$ and $Q=P/E$ in the liquid category. The exact two-channel residual remains

$$
\begin{gathered}
\mathrm{Ph}^2
=\ker\left[\mathrm{Ext}^2(H,E)\longrightarrow
\prod_n\mathrm{Ext}^2(H,B_n)\right]
\simeq\frac{\mathrm{Hom}(K,Q)}{\pi\mathrm{Hom}(K,P)},\\
0\longrightarrow\mathrm{Ph}^2\longrightarrow
\mathrm{coker}(\theta_H^2)\longrightarrow
\frac{\mathrm{im}[\mathrm{Ext}^2(H,E)\to\prod_n\mathrm{Ext}^2(H,B_n)]}
{\bigoplus_n\mathrm{Ext}^2(H,B_n)}\longrightarrow0.
\end{gathered}
\tag{UC19.12}
$$

| Original residual | Exact test retained | Contribution of new sources |
| --- | --- | --- |
| Coordinate-invisible | Lift every actual liquid $K\to Q$ compatibly and linearly to $P$, or exhibit an actual nonlifting map | No theorem about these $K,P,Q$; an epi onto the unrelated $L_T$ and integral pair potentials do not perform this lift |
| Infinitely coordinate-visible | Prove global finite support modulo projective boundaries, or construct infinitely many nonzero coordinate Ext² classes whose representatives vanish in all but finitely many coordinates on each actual compact relation plot | No such family or global finite-support theorem. Infinite products of scalar potentials have product semantics and need not satisfy exact plotwise finite support |
| Both together | Prove (UC19.4) for the actual $X_{r,n}$ and transfer by (UC19.10)–(UC19.11), or construct an actual violation of (UC19.2) surviving every allowed correction | Neither supplied |

The original hostile controls remain decisive. S085's support-escaping $f_0=\Psi j$ is one global boundary. Its nonzero quotient ghost $h_K$ has an explicit product lift, and every resulting second-degree class is a boundary. The new scalar result neither removes those lifts nor converts either control into a counterexample. Conversely, independent coordinate primitives give a map into $P$, not necessarily into $E$; the defect is precisely the remaining $K\to Q$ compatibility problem. Rapidly decreasing nonzero scalars preserve which coordinates are exactly nonzero and cannot repair that support condition.

Degree-one exactness of a chain complex identifies an image with a kernel. Ext² needs the next cochain extension/primitive statement with the actual coefficients and source. The new scalar H² theorem genuinely advances that statement for integer locally constant coefficients, as Lemma UC19.B shows, but degree one alone cannot supply it. Nor does coefficient transfer alone provide coherent finite support over all weights. No CH, forcing axiom, independence conclusion or sequential cofinal replacement is introduced; S094's actual weight poset has no countable cofinal subset.

## 7. Decision threshold and deterministic remaining work

**Inference verdict:** the new categorical/ambient H² and genuine-probe sources are relevant mathematical inputs, with an exact restricted extension consequence. They do **not** meet S090's threshold of a genuinely new mechanism sufficient to restart the original-R3 opposed construction. Lemma UC19.C excludes the direct product-of-discrete-integers model for the original real target. The actual four-point identity can be proved in the CMDG second-relation diagram, but no identification with the original arbitrary $f$, admissible real-liquid coefficient mechanism, or global finite-coordinate control is present.

The smallest unfulfilled positive statement in the already verified original route is precisely (UC19.4), on the actual coefficient system (UC19.3), with **one** finite set valid for every weight edge. This is smaller and more definite than a universal derived-solidity theorem. A new input need not solve an unrelated CMDG programme first. To justify reopening rather than merely rephrase the objective, a proposed lemma must supply a concrete uniformization mechanism for those quotient-system cocycles and prove its hypotheses for these weighted null-sequence subspaces. If a Čech route is proposed, it must additionally exhibit a real-liquid cochain comparison and show how its primitives give that single finite set and separately finite-supported corrections. A local real primitive alone would duplicate the existing local step.

The smallest negative alternative is one actual liquid $K\to Q$ without a lift to $P$, or one infinite family meeting both exact plotwise finite-support realizability and coordinate Ext² nonvanishing from S085. A nonzero quotient section or an unbounded representative is below this threshold.

**Deterministic next action after this primary:** freeze this exact file for distinct UC020 criticism of Lemmas UC19.A–C, the four-point/sign calculation, the source/receipt scope, and the no-new-cycle decision; then record UC021's bounded disposition and carry out the already authorized documentary/protected admission steps. In the absence of a critic-identified repair changing the substantive threshold, keep original R3 OPEN and retain (UC19.4) as the named unresolved bridge. Do not start an opposed construction, a new compiler lane, or another source-only relevance loop merely because this audit has returned. A later genuinely new input must be tested against the explicit threshold above.

No R1, M5/R4 integration, full REACH completion, higher-degree surjectivity, certification or institutional-independence claim follows from this bounded audit.

## 8. Validation record

Execution is CHAD Windows PowerShell, not WSL. Python validation uses only the existing isolated `F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe`, with expected CPython 3.12.12. This evidence environment has no admitted project lockfile and is **UNPINNED**. Its spawned process explicitly sets `UV_CACHE_DIR=%LOCALAPPDATA%\GCL\uv` and `PYTHONPYCACHEPREFIX=%LOCALAPPDATA%\GCL\PythonBytecodeCache`; no dependency installation, lock resolution or local Lean execution occurs.

Mathematical Markdown source preflight and path-scoped whitespace checks are run before handing this file to the parent. The first preflight found one delimiter/prose adjacency, repaired editorially. Their final outcome and non-self-referential final blob identity are reported separately. They validate source structure, not mathematical truth or browser glyph rendering. No finite fixture is added: the new proofs are categorical/divisibility arguments, and no finite calculation can settle the original global higher-limit quantifier. This primary uses zero post-freeze mathematical corrections; the permitted single correction remains available only under the governing bounded protocol.
