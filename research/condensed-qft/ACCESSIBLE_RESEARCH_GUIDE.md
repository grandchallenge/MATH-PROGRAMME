# QFT-COND-001 — Condensed Functional Analysis and Quantum Observables

**Status:** exploratory research guide; no novel theorem certified.  
**Audience:** graduate reader, mathematical physicist, condensed-mathematics researcher, research agent.  
**Research tracker:** [QFT-COND-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2596).  
**Foundational predecessor:** [CMDG CM4](../../docs/CMDG_CM4.md), strictly at its integer-coefficient, module-level boundary.  
**Support route:** elementary proof and exact finite fixtures first; source-concordant theorem research and later formal certification separately.  
**First runnable fixture:** Python 3 standard library only, below.

> **Completed restricted mathematics (TK-1 through TK-4):** [Analytic-condensed tensor/kernel note](ANALYTIC_TENSOR_KERNEL_001.md). It proves an all-Schwartz **scalar-Hom-level** kernel comparison, Scholze-backed Banach completed-tensor comparison for the $L^2$ massive free field, a finite-free derived liquid comparison, and explicit infrared/ordinary-solidification no-go boundaries. The **infinite-dimensional derived Schwartz object-level comparison remains open**; these results are not a novel QFT theorem.

> **Derived comparison resolved (QFT-COND-002):** [Derived Schwartz tensor theorem](DERIVED_SCHWARTZ_TENSOR_002.md) establishes the **object-level** tensor equivalence in the derived category of real $p$ -liquid vector spaces for all finite-dimensional Euclidean Schwartz test-function spaces. Higher Tor vanishes by nuclear Fréchet liquid flatness (Clausen–Scholze, Theorem 4.11 and Remark 4.12). This is an established source-backed application, **not** a new theorem about QFT. Free BV observables and factorization descent remain unproved.

> **QFT-COND-003 — compact-support localization:** [Research note and proofs](COMPACT_SUPPORT_FACTORISATION_003.md) constructs liquid compact-support test objects as filtered colimits of nuclear Fréchet support stages, gives a restricted classical and polynomial free quantum BV Weiss-descent construction, and records a rigorous failure of the naive completed **projective LF** tensor substitution. The completion/infinite-product boundary remains unresolved; no interacting-field theorem is claimed.

> **Quantum completion boundary (QW-001):** [Quantum-weight pro-completion and Weiss obstruction](QUANTUM_WEIGHT_PRO_COMPLETION_004.md) distinguishes a *tower of finite-weight free quantum BV factorization algebras* (each has Weiss descent) from its **ordinary liquid-category inverse limit** (which fails Weiss descent on an explicit disconnected open). The quantum weight is $w=r+2k$ for field degree $r$ and $\hbar$ power $k$; the BV differential preserves it. The proper pro-category Čech comparison and a corrected descent-compatible completion remain open.

> **PRO-001 — the pro-valued locality test:** [Pro-valued Weiss no-go](PRO_VALUED_WEISS_NO_GO_005.md) demonstrates that a **tower of quantum-weight finite-stage factorization algebras** is *not necessarily* a factorization algebra **valued in the pro-category**. A compatible family of local quantum BV moments on a genuine Weiss cover requires unbounded weight cutoffs; every global pro-morphism into a constant object has a bounded cutoff. This identifies a further completion/locality obstruction without any arbitrary singular-product or renormalization claim.

> **CF-001: completed filtered free quantum observables.** [Proof and Costello–Gwilliam comparison](COMPLETE_FILTERED_LIQUID_WEISS_006.md) constructs split complete p-liquid quantum-weight objects with completed tensor and Cech colimits, proves Weiss descent in that target and reconciles the earlier ordinary-product and pro-category no-go results. Full enriched comparison to differentiable pro-cochain complexes remains open.

> **FC-007 — beyond the split-weight category:** [Triangular filtered dg comparison](TRIANGULAR_FILTERED_COMPARISON_007.md) proves two finite counterexamples to a full Costello–Gwilliam equivalence: filtered maps may mix weights, and filtered differentials may raise weight. The same note proves an exact finite-dimensional triangular-matrix equivalence and a finite-filtered Weiss descent propagation theorem that tolerates filtration-raising differentials. Infinite-dimensional differentiable enrichment remains open.

> **LFO-010 — strict LF output and infinite-jet boundary:** [Underived smooth multilinear maps to compact-support outputs and the infinite-jet non-splitting obstruction](STRICT_LF_OUTPUT_DERIVED_BOUNDARY_010.md) provides the mixed source-support inverse-limit/target-support filtered-colimit formula, a proof that no *uniform* output compact support can be imposed, and the nonzero strict Fréchet extension for the full Borel jet map. At the time of LFO-010, the unrestricted fixed-source-stage liquid LF-output Hom comparison was **open**; this has now been resolved by LFO-013. The smooth **derived** pro-cochain equivalence remains **open**. [Original verification ledger](RUN_MATRIX_010.md).

> **LFO-013 — underived LFO3 is resolved:** [Strict LF liquid realization and the LFO3 surjectivity theorem](LFO3_SURJECTIVITY_THEOREM_013.md) proves the fixed-source Fréchet to strict-LF-output Hom bijection using scalar probes, Baire category and profinite-plot factorization; the liquid filtered colimit agrees with the strict LF condensed realization for the actual test-function filtration. The stagewise output support may still depend on the source stage. Higher derived Hom and the Costello–Gwilliam differentiable pro-cochain comparison remain open. [Verification matrix](RUN_MATRIX_013.md).

> **DRM-014 — the derived mapping boundary:** [Source-support derived mapping formula, scalar Mittag–Leffler case and explicit higher-Ext counterexample](DERIVED_MAPPING_OBSTRUCTION_014.md) show that mapping out of compact-support liquid sources is a derived inverse limit. Scalar-valued degree-zero restrictions are surjective by Hahn–Banach, but this does not establish higher Ext comparisons. An exact square-zero module counterexample shows why the successful degree-zero LFO-013 comparison cannot automatically be lifted to derived Hom, even for split monomorphic target stages. **Actual liquid target-stage higher Ext and the Costello–Gwilliam smooth pro-cochain comparison remain open.** [Verification matrix](RUN_MATRIX_014.md).

> **EXT-015 — genuine liquid extension programme:** [SPEC and governing question](EXT-015/SPEC.md) define the compact-support stage Ext¹ comparison and the exact goal: can an extension carry genuinely global analytic information that no compact-support stage can capture? [Work packages](EXT-015/WORK_PACKAGES.md) prescribe independent quotient-stage/injectivity, projective-resolution, positive-versus-negative surjectivity, and derived integration tracks. [Extension docket](EXT-015/EXTENSION_DOCKET.md) records hostile controls. [Run matrix](EXT-015/RUN_MATRIX.md) separates plans from verified theorems. This is a **research plan**, not yet a solution to the genuine liquid Ext problem.

## 1. The object and the scientific question

For a free Euclidean scalar field, test functions $f$ do not name individual field values at a point. They name **smeared observables**, $\phi(f)$, because quantum fields are distribution-valued objects. An algebra of observables on an open spacetime region $U$ must also know how observables on disjoint smaller regions combine.

The difficulty is that this construction mixes continuous function spaces, distributions, completed tensor products, chain complexes and higher-coherent locality. Condensed mathematics might provide a common analytic and homological language for these operations. The claim is **conditional**: until the analytic realization and its completed tensor product are defined and shown to preserve the relevant structure, there is no condensed-QFT theorem.

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

The proof establishes no derived statement. The genuinely open step is to define an analytic-condensed coefficient category and compare this continuous bilinear map with its internal-Hom/tensor presentation there.

## 8. Proposed condensed comparison (research target, NOT a theorem)

Choose explicitly a stable symmetric monoidal analytic-condensed category $\mathcal C_{\mathrm{an}}$, with an appropriately delimited realization $\Phi$ of nuclear locally convex vector spaces. Before defining a tensor comparison, freeze:

1. The site, coefficient ring and category, including which notion of solid/liquid/analytic completion is used.
2. The morphisms represented by $\Phi$: continuous linear maps, with hypotheses.
3. The symmetric monoidal tensor and its derived or completed variant, and the actual unit.
4. Exactness hypotheses and continuous/internal duality.
5. Compatibility with support, colimits and descent, where these are meaningful.

Only then ask if the comparison map

$$
\Phi(E)\widehat\otimes^{\mathbb L}_{\mathcal C_{\mathrm{an}}}\Phi(F)
\longrightarrow \Phi(E\widehat\otimes_\pi F)
$$

is defined canonically and is an equivalence for specified nuclear test spaces. The tensor notation on the **left is a placeholder**, not an asserted construction. Its typing and variance are part of the obligation.

**Minimal test family:** $E=\mathcal S(\mathbb R^a)$, $F=\mathcal S(\mathbb R^b)$, including $a=b=0$. Then test relevant compactly supported smooth-function LF spaces, distribution duals and exact sequences individually, without silently transferring a Schwartz-space result to all locally convex spaces.

**Negative result counts.** A rigorously identified failure of the comparison, an obstruction class, or a boundary between two completion choices can be more valuable than forcing a false equivalence.

## 9. Local-to-global and higher-categorical continuation

After the analytic comparison passes its own tests, construct the **actual** free-field BV/observable complex associated to each suitable open $U$. Name its symmetric monoidal target and weak equivalences. Verify disjoint-open multiplication and higher coherence, then independently prove or refute descent for the specified Weiss covers. The condensed realization must be tested for preservation of each feature, not assumed to have inherited it.

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
| Physics comparison | Free BV observables on a specified spacetime and cover family | Disjoint structure, descent and analyticity separately checked |
| Novelty gate | Derive a new invariant, obstruction or improved gluing/completion criterion | Not reducible to a cited known theorem |

## 11. Certification path and continuation graph

Current status:

~~~text
finite Gaussian control [known, reproducible]
  -> Schwartz covariance/kernel benchmark [known, mathematical proof]
  -> analytic-condensed realization + typed tensor [OPEN]
  -> restricted comparison or counterexample [OPEN]
  -> free field factorization/descent transport [OPEN]
  -> novel obstruction/theorem or negative novelty audit [OPEN]
  -> independent mathematical review and certification [LATER]
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

**Novelty status:** **NOT YET ESTABLISHED.** A proof that only reconstructs the standard continuous kernel and tensor product belongs in the validation layer, not the discovery layer.
