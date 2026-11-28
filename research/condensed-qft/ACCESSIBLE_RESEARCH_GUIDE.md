# QFT-COND-001 — Condensed Functional Analysis and Quantum Observables

**Status:** audited teaching guide through the explicit REACH overlap model, UC119.

**Audience:** the REACH overview is for a mathematically curious reader. The worked background sections are for graduate readers and researchers.

**Research tracker:** [QFT-COND-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2596).

**Foundational predecessor:** [CMDG CM4](../../docs/CMDG_CM4.md), strictly at its integer-coefficient, module-level boundary.

**Support route:** hand examples, exact finite fixtures, and source-linked mathematical proofs with reviewed scopes.

**First example:** count fifteen products from two sets of three collision relations below. The runnable fixtures use the Python 3 standard library.

## REACH in plain language

**Current through UC119, 28 November 2026.** The proofs cover the declared one-dimensional Gaussian/Wick free scalar and its controlled families of singular kernels. The original comparison of support stages has a separate qualified verdict. The Gaussian covariance example farther down is an elementary benchmark that introduces the wider programme.

### The field and the collision problem

A scalar field associates a single quantity with each position. In the quantum description, an observable tests the field against a smooth function supported in a region. This is a carefully chosen average of the field. Combining several tests creates kernels with several positions, called slots. When slots meet, a kernel can be singular along the set where their positions coincide. The renormalization problem is to subtract these singular parts in a way that still lets us differentiate and compose the resulting observables. Each quantum contraction contributes one power of $\hbar$. The separate regulator controls the approach to a collision. Total weight counts one for each field slot and two for each power of $\hbar$.

The construction keeps a subtraction record with coefficients describing how the kernel approaches the collision. The finite physical answer is a separate readout. For two slots at positions $x_1,x_2$, use their midpoint $c$ and separation $z=x_1-x_2$. The three pair-collision tests are $1$, $c$, and $x_1x_2=c^2-z^2/4$. The last test sees the second derivative in the separation direction. This explains why keeping only midpoint data would lose information even in the first collision case. [Renormalized quantum structure](EXT-015/RENORMALIZED_QUANTUM_STRUCTURE_111.md) · [Three pair moments and the normal derivative](EXT-015/COLLISION_LIQUID_WEIGHT_TWO_UC092.md)

### What the liquid description contributes

The liquid category gives a common setting for continuous parameter families, their coefficient spaces and derived composition. The model also keeps genuine smooth parameter derivatives through the specified quotient by rapidly vanishing regulator errors. In the resulting description each group of coincident slots has its own polynomial moment coordinates. A finite-weight term uses finitely many components. Completion holds the terms of all weights together, so successive weights may visit different components of an open region. [Parameter families](EXT-015/COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) · [Collision coordinates at all weights](EXT-015/COLLISION_LIQUID_ALL_WEIGHTS_UC093.md) · [All opens and completed gluing](EXT-015/COLLISION_LIQUID_WEISS_UC096.md) · [Why the order of completion matters](EXT-015/JOINT_LIQUID_FILTERED_COMPLETION_UC099.md)

Separated regions combine over one common vacuum, including the empty region. The completed derived product also works for two general coefficient inputs. For example, when both inputs are the vacuum with $\hbar$ set to zero, their derived product keeps a class recording the common relation $\hbar=0$ in weight two and degree minus one. [Shared vacuum and disjoint Wick product](EXT-015/COMPLETED_FILTERED_VACUUM_PRODUCTS_UC102.md) · [Derived product for general inputs](EXT-015/AMBIENT_COMPLETED_LIQUID_TENSOR_UC105.md)

### What the affine readout forgets

On an interval, the simple field tests use an affine function $a+bx$, specified by its intercept and slope. Its square has three quadratic coefficients. The affine readout replaces the three independent pair-collision measurements by those quadratic expressions in singleton measurements. The three differences are independent relations that vanish under the readout. Comparing two copies of that readout over the richer collision algebra records each such relation in degree minus one. On a larger interval containing two previously separate intervals, the two triples map to one by addition in the common moment basis. The differences between the two copies disappear there. A product of singletons from the two intervals stays in degree zero. [Derived readout relations and interval merger](EXT-015/AFFINE_READOUT_DERIVED_RELATIONS_UC108.md)

### Worked example with two intervals

Take two disjoint intervals. Write down three pair-relation coordinates on each. The product of two distinct relation coordinates changes sign if their order is reversed, so count each unordered pair once.

| Where the two factors live | Number of products |
| --- | --- |
| Both in the first interval | 3 |
| Both in the second interval | 3 |
| One in each interval | 9 |
| Total on the union | 15 |

A cover that lists only the two intervals supplies six of these fifteen weight-four, degree-minus-two products. Each patch has only one set of coordinates, so the nine mixed products are missing. A cover that puts any two chosen points together in some patch suffices to recover all fifteen. More generally, at weight $w$ and degree $-q$ with $2q\le w$, it suffices that every set of up to $w-q$ points lie in some patch. This is the best uniform guarantee over all opens and covers. A Weiss cover has the joint containment property for every finite set, which gives completed gluing at every weight. [Proof and sharp cover example](EXT-015/AFFINE_RELATIONS_WEISS_DESCENT_UC111.md)

For a hand check, label the coordinates $L_0,L_1,L_2$ and $R_0,R_1,R_2$. List the fifteen pairs and mark the nine with both labels. Then embed the intervals in one larger interval and identify $L_i$ with $R_i$ for each index. Among the nine mixed products, the three with matching indices become a wedge of a coordinate with itself and vanish. For a runnable companion, use the existing exact Python fixtures from the repository root.

~~~text
python research/condensed-qft/EXT-015/fixtures/check_collision_liquid_moments_uc092.py
python research/condensed-qft/EXT-015/fixtures/check_collision_liquid_weiss_uc096.py
~~~

The first checks the collision moment formulas and the separated Wick control. The second checks finite component-cover and boundary calculations. The mixed-product count above is a hand calculation. The infinite-component and completed gluing statements use the mathematical proofs. The [UC113 evidence ledger](EXT-015/AFFINE_RELATIONS_WEISS_ACCEPTANCE_UC113.md) records the exact review and finite controls for the later signed calculation.

### Recovering the full collision model

The affine model alone forgets the three pair differences. Keep its actual derived overlaps, which compare copies of the affine readout over the collision algebra, and the maps between those overlaps. Combining these comparisons recovers what was lost. With the first overlap included, the reconstruction is exact through weight three. Six products of two pair differences on one interval enter at weight four. They are absent from that first stage and are recovered at the next stage. At stage $n$, every weight below $2(n+1)$ is recovered. Taking the compatible sequence of all stages reconstructs the completed collision algebra.

The six quadratic products here use two pair differences on one interval in the collision algebra. The nine mixed products above use one relation from each of two intervals in the derived overlap. [Reconstruction proof and finite stage calculation](EXT-015/AFFINE_COLLISION_RECONSTRUCTION_UC114.md)

### How the overlap maps are built

Label three copies of the affine readout first, second and third. The difference from the first copy to the third is the sum of the two adjacent differences. Identifying two adjacent copies makes their difference zero. The same rule works with any number of copies and gives the actual derived overlap maps.

On one interval, choose one of the three pair measurements for each adjacent difference. This makes nine ordered products at weight four. The three differences between the two orders are boundaries, leaving six symmetric quadratic products, including the squares. These are the six products recovered at the second stage. [Explicit overlap recipe and signed calculation](EXT-015/EXPLICIT_AFFINE_OVERLAP_DIAGRAM_UC117.md)

### The original REACH verdict

The declared renormalized model, its quantum identities and its correctly typed gluing have proofs in the usual ZFC axioms of set theory. The original proposed equivalence between the support-stage and observable diagrams already fails at the vacuum. In the old diagram, a larger stage admits coefficient functions supported outside the smaller interval. In the model's vacuum, all stages have the same scalar algebra and identity transitions. The separate degree-two liquid question asks whether every global extension class is already represented at some bounded support stage. In ZFC the classes represented at bounded stages remain distinct in the global group. The continuum hypothesis gives a global class outside every bounded stage. The partition principle PH1 instead guarantees that every global class has a bounded-stage representative. The CH class survives in the intermediate smooth extension group and vanishes under the actual observable evaluation. The original strong criterion remains unmet. These degree-two classes belong to a different comparison from the degree-minus-one collision relations in the worked example. [Qualified closeout and foundation assumptions](EXT-015/REACH_QUALIFIED_CLOSEOUT_UC088.md) · [Exact comparison diagram](EXT-015/ORIGINAL_TYPED_INTEGRATION_VERDICT_UC085.md)

Use the accepted result and its evidence ledger to refresh the affected example and scope here and in the [public reader edition](https://grandchallenge.ai/MATH-PROGRAMME/campaigns/REACH_READER_GUIDE/) when a new REACH milestone is recorded.

## Earlier steps in the programme

The following entries trace the earlier tensor, completion and support results. Each describes the scope of its cited source. The current REACH account is above.

> **Completed restricted mathematics (TK-1 through TK-4):** [Analytic-condensed tensor/kernel note](ANALYTIC_TENSOR_KERNEL_001.md). It proves an all-Schwartz **scalar-Hom-level** kernel comparison, Scholze-backed Banach completed-tensor comparison for the $L^2$ massive free field, a finite-free derived liquid comparison, and explicit infrared/ordinary-solidification no-go boundaries. The object-level Schwartz question was open at this stage and was subsequently resolved in the next note.

> **Derived comparison resolved (QFT-COND-002):** [Derived Schwartz tensor theorem](DERIVED_SCHWARTZ_TENSOR_002.md) establishes the **object-level** tensor equivalence in the derived category of real $p$ -liquid vector spaces for all finite-dimensional Euclidean Schwartz test-function spaces. Higher Tor vanishes by nuclear Fréchet liquid flatness (Clausen–Scholze, Theorem 4.11 and Remark 4.12). This is an established source-backed application, **not** a new theorem about QFT. Free BV observables and descent are treated in later stages below.

> **QFT-COND-003 — compact-support localization:** [Research note and proofs](COMPACT_SUPPORT_FACTORISATION_003.md) constructs liquid compact-support test objects as filtered colimits of nuclear Fréchet support stages, gives a restricted classical and polynomial free quantum BV Weiss-descent construction, and records a rigorous failure of the naive completed **projective LF** tensor substitution. The note left the completion question for the next stages.

> **Quantum completion boundary (QW-001):** [Quantum-weight pro-completion and Weiss obstruction](QUANTUM_WEIGHT_PRO_COMPLETION_004.md) distinguishes a *tower of finite-weight free quantum BV factorization algebras* (each has Weiss descent) from its **ordinary liquid-category inverse limit** (which fails Weiss descent on an explicit disconnected open). The quantum weight is $w=r+2k$ for field degree $r$ and $\hbar$ power $k$; the BV differential preserves it. The next stages test pro-category descent and construct a completed filtered alternative.

> **PRO-001 — the pro-valued locality test:** [Pro-valued Weiss no-go](PRO_VALUED_WEISS_NO_GO_005.md) demonstrates that a **tower of quantum-weight finite-stage factorization algebras** is *not necessarily* a factorization algebra **valued in the pro-category**. A compatible family of local quantum BV moments on a genuine Weiss cover requires unbounded weight cutoffs; every global pro-morphism into a constant object has a bounded cutoff. This identifies a further completion/locality obstruction without any arbitrary singular-product or renormalization claim.

> **CF-001: completed filtered free quantum observables.** [Proof and Costello–Gwilliam comparison](COMPLETE_FILTERED_LIQUID_WEISS_006.md) constructs split complete p-liquid quantum-weight objects with completed tensor and Cech colimits, proves Weiss descent in that target and reconciles the earlier ordinary-product and pro-category no-go results. The later REACH results give a typed comparison for the controlled free scalar.

> **FC-007 — beyond the split-weight category:** [Triangular filtered dg comparison](TRIANGULAR_FILTERED_COMPARISON_007.md) proves two finite counterexamples to a full Costello–Gwilliam equivalence: filtered maps may mix weights, and filtered differentials may raise weight. The same note proves an exact finite-dimensional triangular-matrix equivalence and a finite-filtered Weiss descent propagation theorem that tolerates filtration-raising differentials. This note treats the finite-dimensional comparison. The later REACH work specifies the infinite-dimensional parameter domains it can cover.

> **LFO-010 — strict LF output and infinite-jet boundary:** [Underived smooth multilinear maps to compact-support outputs and the infinite-jet non-splitting obstruction](STRICT_LF_OUTPUT_DERIVED_BOUNDARY_010.md) provides the mixed source-support inverse-limit/target-support filtered-colimit formula, a proof that no *uniform* output compact support can be imposed, and the nonzero strict Fréchet extension for the full Borel jet map. At the time of LFO-010, the unrestricted fixed-source-stage liquid LF-output Hom comparison was **open**; this has now been resolved by LFO-013. The smooth derived question was deferred to the later integration work. [Original verification ledger](RUN_MATRIX_010.md).

> **LFO-013 — underived LFO3 is resolved:** [Strict LF liquid realization and the LFO3 surjectivity theorem](LFO3_SURJECTIVITY_THEOREM_013.md) proves the fixed-source Fréchet to strict-LF-output Hom bijection using scalar probes, Baire category and profinite-plot factorization; the liquid filtered colimit agrees with the strict LF condensed realization for the actual test-function filtration. The stagewise output support may still depend on the source stage. Higher derived Hom and the differentiable comparison require the separate arguments in the later integration work. [Verification matrix](RUN_MATRIX_013.md).

> **DRM-014 — the derived mapping boundary:** [Source-support derived mapping formula, scalar Mittag–Leffler case and explicit higher-Ext counterexample](DERIVED_MAPPING_OBSTRUCTION_014.md) show that mapping out of compact-support liquid sources is a derived inverse limit. Scalar-valued degree-zero restrictions are surjective by Hahn–Banach, but this does not establish higher Ext comparisons. An exact square-zero module counterexample shows why the successful degree-zero LFO-013 comparison cannot automatically be lifted to derived Hom, even for split monomorphic target stages. This result motivates the fixed-source higher Ext and differentiable questions in EXT-015. [Verification matrix](RUN_MATRIX_014.md).

> **EXT-015 — genuine liquid extension programme:** [SPEC and governing question](EXT-015/SPEC.md) define the compact-support stage Ext¹ comparison and the exact goal: can an extension carry genuinely global analytic information that no compact-support stage can capture? [Work packages](EXT-015/WORK_PACKAGES.md) prescribe independent quotient-stage/injectivity, projective-resolution, positive-versus-negative surjectivity, and derived integration tracks. [Extension docket](EXT-015/EXTENSION_DOCKET.md) records hostile controls. [Run matrix](EXT-015/RUN_MATRIX.md) separates plans from verified theorems. The [qualified closeout](EXT-015/REACH_QUALIFIED_CLOSEOUT_UC088.md) records the eventual bounded results, the conditional degree-two verdicts, and the unmet original strong criterion.

> **Historical EXT-015A/B handoff materials:** [A: quotient-stage factorization and Ext¹ injectivity](EXT-015/handoffs/EXT-015A.md) and [B: genuine liquid projective presentations and Borel-jet control](EXT-015/handoffs/EXT-015B.md) are independently executable research candidates with [controller readiness conditions](EXT-015/handoffs/READINESS.md) and a [machine-readable non-executable manifest](EXT-015/handoffs/HANDOFF_INDEX.json). Their exact mathematical source baseline is pinned; neither document creates a worker lease, Issue AVAILABLE state or RESULT/1 authority. Admitted handoff commit readback and actual protected dispatch are separate steps.

## 1. The object and the scientific question

For a free Euclidean scalar field, test functions $f$ do not name individual field values at a point. They name **smeared observables**, $\phi(f)$, because quantum fields are distribution-valued objects. An algebra of observables on an open spacetime region $U$ must also know how observables on disjoint smaller regions combine.

The difficulty is that this construction mixes continuous function spaces, distributions, completed tensor products, chain complexes and higher-coherent locality. The opening REACH account records how condensed mathematics supplies a common setting in the proved free-scalar scope. This background section introduces the original question and an elementary covariance calculation.

**Research question:** Can a carefully delimited analytic-condensed realization of nuclear test-function spaces make derived tensor products and local-to-global reconstruction functorial in a new way, or detect an obstruction invisible to naive algebraic completion?

A translation of the Schwartz kernel theorem into new notation is **not** a new QFT result.

## 2. Required background

| Level | Concepts |
| --- | --- |
| Required | Linear algebra, positive-definite matrices, Gaussian covariance, Schwartz functions, bilinear maps |
| Helpful | Nuclear locally convex spaces, Schwartz kernel theorem, sheaves, symmetric monoidal categories |
| Deferred | Derived condensed analytic modules, BV/BRST, Weiss descent, infinity-categorical factorization |

**Terminological warning.** Clausen–Scholze *condensed mathematics* is not *condensed-matter physics*, nor the older DeWitt *condensed index notation* used in field theory.

## 3. Core bridge: continuous kernels before condensed categories

Let $m>0$ and $E_d=\mathcal S(\mathbb R^d,\mathbb R)$. Write

$$
\widehat f(p)=\int_{\mathbb R^d}e^{-ip\cdot x}f(x)\,dx.
$$

The covariance bilinear form for the massive free Euclidean scalar is

$$
C_m(f,g)
=\int_{\mathbb R^d}
\frac{\widehat f(-p)\widehat g(p)}{|p|^2+m^2}
\frac{dp}{(2\pi)^d}.
$$

By Cauchy–Schwarz and Plancherel,

$$
|C_m(f,g)|\le \frac{1}{m^2}\,\|f\|_{L^2}\|g\|_{L^2}.
$$

For real $f$, we have $\widehat f(-p)=\overline{\widehat f(p)}$, so

$$
C_m(f,f)=
\int_{\mathbb R^d}\frac{|\widehat f(p)|^2}{|p|^2+m^2}
\frac{dp}{(2\pi)^d}\ge0.
$$

Thus the covariance is positive and jointly continuous in the Schwartz topology. These statements are elementary **known** consequences of the Fourier representation, not discoveries.

The Schwartz space is nuclear. The established completed-tensor isomorphism is

$$
\mathcal S(\mathbb R^a)\widehat\otimes_\pi
\mathcal S(\mathbb R^b)
\cong
\mathcal S(\mathbb R^{a+b}).
$$

Therefore the continuous bilinear covariance is represented by a unique tempered distribution on $\mathbb R^{2d}$. This is the known Schwartz kernel theorem in an especially simple setting. It does **not** authorize multiplying singular distributions, restricting arbitrary kernels to diagonals, or asserting renormalized operator products.

## 4. First example by hand: a two-site Gaussian field

Consider a two-dimensional real Gaussian variable $(\phi_1,\phi_2)$ with inverse covariance

$$
A=\begin{pmatrix}3&-1\\-1&3\end{pmatrix}.
$$

The eigenvalues of $A$ are $2$ and $4$, so $A$ is strictly positive and

$$
C=A^{-1}
=\frac18\begin{pmatrix}3&1\\1&3\end{pmatrix}.
$$

Consequently

$$
\mathbb E(\phi_1\phi_2)=\frac18
$$

even though sites $1$ and $2$ are distinct. Gaussian Wick's rule gives

$$
\begin{aligned}
\mathbb E(\phi_1^2\phi_2^2)
&=C_{11}C_{22}+2C_{12}^2\\
&=\frac{11}{64},\\
\mathbb E(\phi_1^2)\mathbb E(\phi_2^2)
&=\frac9{64}.
\end{aligned}
$$

**Lesson:** two separated regions can possess a perfectly valid multiplication of observables without probabilistic independence. Nonzero correlations must not be misdiagnosed as a failure of factorization-algebra locality. Euclidean factorization involves structure maps and descent, not vanishing of all separated correlations.

## 5. Edge example by hand: completion is not automatic

For infinite-dimensional Hilbert spaces such as $\ell^2$, projective and injective completed tensor products need not coincide. In the standard Hilbert-space example, these distinguish trace-class from compact-operator completions, respectively. That distinction is a meaningful analytic datum, not a choice of notation.

Similarly, an indefinite $2\times2$ form such as

$$
C_{\mathrm{bad}}=
\begin{pmatrix}1&0\\0&-1\end{pmatrix}
$$

cannot be a covariance matrix: its second basis vector has negative variance. A proposed analytic-condensed realization must preserve relevant positivity, continuity and completion data rather than merely forget them.

## 6. First reproducible fixture

Execute with a stock Python 3 interpreter:

~~~python
from fractions import Fraction as Q

# Exact inverse of [[3,-1],[-1,3]].
c11, c12, c22 = Q(3, 8), Q(1, 8), Q(3, 8)
wick22 = c11 * c22 + 2 * c12 * c12
independent = c11 * c22

assert wick22 == Q(11, 64)
assert independent == Q(9, 64)
assert wick22 - independent == Q(1, 32)

# Positivity: determinant and diagonal principal minor.
assert c11 > 0 and c11*c22 - c12*c12 > 0

# A negative variance rejects an invalid covariance.
bad_second_variance = Q(-1)
assert bad_second_variance < 0
print("finite covariance and Wick controls: PASS")
~~~

**Input:** the exact rational covariance above.  
**Output:** a PASS message after exact assertions.  
**Support class:** finite symbolic control, not formal proof of any infinite-dimensional condensed equivalence.  
**Failure fixture:** changing $c_{12}$ to zero eliminates the correlation correction, so a test that still reports $11/64$ must fail.

## 7. First local proposition and honest limitation

**Proposition (known benchmark).** For each $d\ge1$ and $m>0$, the displayed $C_m$ extends to a jointly continuous bilinear form on the real Schwartz space and is positive semidefinite.

**Proof.** The multiplier $(|p|^2+m^2)^{-1}$ is bounded by $m^{-2}$. Plancherel and Cauchy–Schwarz give the bound in Section 3, while Fourier conjugacy for real test functions gives positivity. Since Schwartz inclusion into $L^2$ is continuous, so is $C_m$. $\square$

The proposition concerns continuous bilinear maps. The [derived Schwartz comparison](DERIVED_SCHWARTZ_TENSOR_002.md) gives the object-level tensor result for the specified real liquid realization.

## 8. Typing a condensed tensor comparison

Choose explicitly a stable symmetric monoidal analytic-condensed category $\mathcal C_{\mathrm{an}}$, with an appropriately delimited realization $\Phi$ of nuclear locally convex vector spaces. Before defining a tensor comparison, freeze:

1. The site, coefficient ring and category, including which notion of solid/liquid/analytic completion is used.
2. The morphisms represented by $\Phi$: continuous linear maps, with hypotheses.
3. The symmetric monoidal tensor and its derived or completed variant, and the actual unit.
4. Exactness hypotheses and continuous/internal duality.
5. Compatibility with support, colimits and descent, where these are meaningful.

A candidate comparison has the form

$$
\Phi(E)\widehat\otimes^{\mathbb L}_{\mathcal C_{\mathrm{an}}}\Phi(F)
\longrightarrow \Phi(E\widehat\otimes_\pi F)
$$

The first task is to define that arrow and show when it is an equivalence. The tensor symbol on the left is schematic here. For Schwartz inputs the [derived Schwartz comparison](DERIVED_SCHWARTZ_TENSOR_002.md) specifies the derived real liquid tensor and proves the equivalence. Other inputs require their own hypotheses.

**Minimal test family:** $E=\mathcal S(\mathbb R^a)$, $F=\mathcal S(\mathbb R^b)$, including $a=b=0$. Then test relevant compactly supported smooth-function LF spaces, distribution duals and exact sequences individually, without silently transferring a Schwartz-space result to all locally convex spaces.

**Negative result counts.** A rigorously identified failure of the comparison, an obstruction class, or a boundary between two completion choices can be more valuable than forcing a false equivalence.

## 9. Local-to-global and higher-categorical continuation

The actual free-field BV complexes, their completed target and their disjoint structure maps are constructed for the declared free-scalar model. The Weiss theorem then compares the complex of an open region with the completed gluing of its patches. Compare the [original typed integration](EXT-015/ORIGINAL_TYPED_INTEGRATION_VERDICT_UC085.md) with the [later joint liquid descent proof](EXT-015/AFFINE_RELATIONS_WEISS_DESCENT_UC111.md) to see how the precise source and target change.

For quantum observables, check the covariance/Wick operations against the selected analytic completion. Singular coincident-point products and renormalization require independent hypotheses and are **not** solved by the Schwartz kernel theorem.

Later gauge-theory experiments may use derived BRST/BV complexes and their local-to-global obstructions. These are subsequent research targets, not present claims.

In particular, the 2026 analysis of algebraic QFT versus prefactorization algebras reduces, but does not completely settle, a general infinity-categorical equivalence problem. No claim here bypasses that boundary.

## 10. Challenge ladder and completion tests

| Stage | Task | Completion test |
| --- | --- | --- |
| Exercise | Reproduce $A^{-1}$ and Wick's four-point formula | Exact rational results above |
| Fixture | Run the Python control and its altered-covariance negative case | Positive fixture passes; negative case detected |
| Source audit | Pin exact kernel/nuclear/factorization statements in primary literature | Hypotheses and provenance recorded |
| Restricted lemma | Define $\Phi$ and its continuous-Hom comparison on Schwartz spaces | Fully typed statement or specific counterexample |
| Analytic theorem | Analyze $\Phi(E)\widehat\otimes^\mathbb L\Phi(F)$ for a finite test family | Proof with all completion and exactness assumptions |
| Physics comparison | Reproduce the two-interval collision calculation in the opening section | Count six products on the two single-interval patches and nine additional products on their union |
| Novelty gate | Derive a new invariant, obstruction or improved gluing/completion criterion | Not reducible to a cited known theorem |

## 11. Certification path and continuation graph

The teaching sequence and its support are as follows.

~~~text
finite Gaussian and Schwartz covariance benchmark [known, reproducible]
  -> derived real liquid Schwartz tensor [proved for the stated input spaces]
  -> controlled renormalized free scalar [reviewed proof for the declared class]
  -> collision moments, completed product and Weiss descent [reviewed proofs]
  -> affine readout relations and sharp cover bound [reviewed through UC113]
  -> reconstruction from derived affine overlaps [reviewed through UC116]
  -> explicit overlap maps and signed recovery of the six products [reviewed through UC119]

original support-stage equivalence [refuted in ZFC at the vacuum]
  -> separate degree-two support comparison [conditional verdicts in UC088]
~~~

Lean/CMDG CM4 supplies a rigorous **integer module-level** predecessor. It must not be silently used as a theorem about real or complex analytic coefficients, derived condensations, solid tensor completions, or QFT observables. Any formalization beyond that boundary requires a new dependency audit and actual replay.

Repository artifacts must keep mathematical claims, literature-dependent facts, speculative targets, and experimental data separately marked. Admission uses the ordinary protected GCL route with exact-head validation, not an extra per-entry human ritual.

## 12. Bibliography and claim-support audit

| Source | Exact role | Imported claim | Current audit |
| --- | --- | --- | --- |
| Scholze, *Lectures on Condensed Mathematics* (arXiv:2605.03658, 2026) | Condensed/solid foundations | Baseline theory, not a QFT construction | Primary source identified; detailed API audit pending |
| Clausen–Scholze, *Condensed Mathematics and Complex Geometry* (arXiv:2605.11731, 2026) | Analytic-condensed context | Existing complex-analytic methods | Primary source identified; detailed audit pending |
| Costello–Gwilliam, *Factorization Algebra* (arXiv:2310.06137) | Local observables, higher structure | Definitions and known examples | Primary source identified |
| Gwilliam–Rejzner, *Relating Nets and Factorization Algebras of Observables: Free Field Theories*, CMP 373 (2020), 107–174 | Nuclear-space free-field benchmark | Existing free-field comparisons | Primary article identified |
| Benini, Carmona, Grant-Stuart, Schenkel, *On the equivalence of AQFTs and prefactorization algebras*, Lett. Math. Phys. 116 (2026), article 13 | Delimits infinity-categorical comparison | A remaining obstruction/open generality | Primary article identified |
| Barwick, *Factorization algebras in quite a lot of generality* (arXiv:2602.01292, 2026) | Broader geometric generality, novelty check | No condensed-QFT result inferred | Primary preprint identified |

**Support status.** The continuous covariance and Schwartz tensor examples are established benchmarks. The REACH section links the later bounded research results, their review records and the exact claim boundaries.
