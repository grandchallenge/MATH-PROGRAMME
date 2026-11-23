# CSM-00/G0 — primary-statement audit and negative-novelty decisions

**Programme:** CSM-001. **Audit date:** 2026-11-23. **Status:** PARTIAL G0: four original primary arXiv PDFs acquired with recorded exact SHA-256 and numbered theorem interfaces inspected; publisher/preprint concordance, exhaustive prior-art search, and independent source-proof replay remain open. **Tracker:** [CSM-001 issue #3136](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3136). This record must not be used as a complete source lock or novelty certificate.

## Observed primary versions and exact theorem interfaces

| Key | Version examined, with primary link | Grounded numbered result | What the result permits; what it does not |
| --- | --- | --- | --- |
| S01 | [Fritz, arXiv:1908.07021v8](https://arxiv.org/pdf/1908.07021v8), front matter 31 May 2020; *Advances in Mathematics* 370 (2020) 107239 | Definition 2.1: Markov category is symmetric monoidal with coherent copy/delete comonoids and natural deletion. Example 2.5: finite stochastic matrices are a Markov category | Normalized finite kernels permit deleting any output without changing total probability. **Full weighted nonnegative matrices are not automatically Markov:** deleting the output multiplies an input by its column sum. |
| S02 | [Baez, Lynch, Moeller, arXiv:2111.10315](https://arxiv.org/pdf/2111.10315), PDF front matter says v2, 10 February 2023; *Journal of Mathematical Physics* 64 (2023) 023304 | Lemmas 27, 39 and Theorem 40: the entropy construction is a lax symmetric monoidal functor from convex relations to sets, supplying an operad algebra of thermostatic systems | Operadic entropy optimization under convex constraints is established; this **does not** assert that arbitrary positive factor-network marginalization preserves interaction locality. |
| S03 | [Sergeant-Perthuis, arXiv:2403.16104](https://arxiv.org/pdf/2403.16104), PDF v1, 24 March 2024 | Definition 3: compatible proper specification kernels. Definition 4: Gibbs measures consistent with a specification. Theorem 1: kernels of specifications form the appropriate poset representation. Theorem 2: Gibbs marginals are compatible sections | Categorical specification/invariance and phases have prior art. Weighted finite diagrams need a precise normalization and limit bridge before they can be identified with DLR specifications. |
| S04 | [van Enter, Fernández, Sokal, hep-lat/9210032](https://arxiv.org/pdf/hep-lat/9210032), source front matter 22 October 1992; *Journal of Statistical Physics* 72 (1993) | Theorem 4.1: for zero-field two-dimensional nearest-neighbour Ising at coupling exceeding the paper's explicit large-coupling threshold (approximately 0.764285), spacing-2 decimation produces an image measure with no quasilocal specification | The non-Gibbsian RG obstruction is already rigorous. The theorem is **not** an assertion that every finite marginal or every RG map is non-Gibbsian. The source also treats other dimensions and transformations with different conditions. |

**Source-byte acquisition and exact identity (2026-11-23):** An authenticated CHAD OS shell streamed each pinned arXiv PDF, verified its `%PDF-` header, measured its length and computed its SHA-256. The hashes identify **retrieved bytes**, not proof validity, content immutability or publication-edition equivalence.

| ID | Exact PDF locator | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| S01 | https://arxiv.org/pdf/1908.07021v8 | 1040967 | `99ee420f2e620a1e40e23d7dd8b3608c01f9f07bb32850703d33b9e03d48cb4e` |
| S02 | https://arxiv.org/pdf/2111.10315v2 | 318105 | `b1aca85a2ec860a232a72c3e132230ef1d23e5f6f362610d631b0543707abe4d` |
| S03 | https://arxiv.org/pdf/2403.16104v1 | 326888 | `1d7e429904e88c5ec45e35c3d1fc8134f75f73efc38705096cb7611e37e902b4` |
| S04 | https://arxiv.org/pdf/hep-lat/9210032 | 1562458 | `d7ba5ff8d006863871898b6cec7995087e8846649ebd58e94b795201e45d3c9b` |

**Acquisition receipt:** `GCL_CONTROL_BASH_RESULT/1` id `9db9142ceb604e6280aea42d37d98b32`; command digest `014779556501ed3a82eac111a59d25a74c216305df021b945b330735ad44e37d`; output digest `29f100fc057a527033a1a86c708fc6a0f450d7d7986c77f317de70d3ffbd105e`; private CHAD capture `execution-captures/9db9142ceb604e6280aea42d37d98b32.json`. Receipt explicitly states `execution_origin=LOCAL_OS_ONLY_NOT_INDEPENDENTLY_AUTHENTICATED`, `independent_execution_attested=false`. These identities also appear in [tracker issue #3136, source acquisition comment](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3136#issuecomment-7097110230).

**Remaining source-identity obligations:** Re-fetch and compare retained bytes in an independent replay environment where policy requires it; acquire/check published editions; then compare theorem statements and hypotheses version by version. This G0 record is **partial**, not source-proof certification.

## Finite-to-probability semantics bridge: exact boundary

Let an unnormalized kernel be a nonnegative matrix $A:Y\times X\to\mathbb{R}_{\geq0}$. Its source-dependent total mass is

$$
m_A(x)=\sum_y A(y,x).
$$

If each $m_A(x)>0$, column normalization produces the stochastic kernel

$$
\overline A(y\mid x)=A(y,x)/m_A(x).
$$

However, pointwise normalization is generally **not** a functor preserving unrestricted weighted composition. The missing mass factors depend on the intermediate variables: in general,

$$
\overline{B A}\ne\overline B\,\overline A.
$$

Counterexample: let the input have one point, the intermediate state have two points, and the output one point. Take $A=(1,1)^\mathsf{T}$ and $B=(1,2)$. The composite weight is $3$, whereas normalizing $A$ and $B$ separately gives a stochastic map of total mass $1$ and loses the factor $3$. The mismatch is in weights and their partition function; in this scalar-output example the normalized *probabilities* are necessarily identical, so the example witnesses **normalization-factor loss**, not unequal stochastic composites. A genuinely unequal-probability example must have a nontrivial output: take $A=(1,1)^\mathsf{T}$ and $B=\mathrm{diag}(1,2)$, giving $\overline{BA}=(1/3,2/3)^\mathsf{T}$ but $\overline B\,\overline A=(1/2,1/2)^\mathsf{T}$.

The CSM-01 matrices and their partition-function scalars belong to a weighted category. Only explicit normalization, with all necessary mass factors accounted for, gives stochastic channels suitable for the S01 Markov-category and S03 DLR language. This distinction persists in hidden-state elimination.

## Two indispensable additional prior-art controls

1. **S05: Jean-René Chazottes and Edgardo Ugalde**, [On the preservation of Gibbsianness under symbol amalgamation](https://doi.org/10.1017/CBO9780511819407.003), Cambridge chapter, 2011. The publicly accessible abstract expressly includes a Hölder-potential/Gibbs representation for hidden Markov chains arising from Markov-measure symbol amalgamation. Full theorem hypotheses and proof have **not** been independently retrieved and audited. Any assertion that positive finite hidden Markov images are Gibbsian is **KNOWN**, not a CSM original.
2. **S06: Roberto Fernández and Gregory Maillard**, [Chains with complete connections and one-dimensional Gibbs measures](https://arxiv.org/abs/math/0305025). The accessible full-text source identifies Theorems 4.12 (chain to specification), 4.16 (reverse), 4.18 (continuity), and 4.19 (equivalence at exponential continuity), with hereditary uniqueness and good-future conditions distinguished in the paper. Whether each precise hypothesis is met by an intended CSM example must be checked rather than assumed.

Existing high-level results subsume unqualified claims that finite-state positive Markov observations admit smooth one-sided conditionals or Gibbs reconstructions. Birkhoff/Hopf projective contraction for positive matrices is also prior mathematics, not a new CSM lemma. See [positive-matrix projective contraction](https://doi.org/10.1016/j.laa.2003.11.005) as a literature entry point; verify bibliographic identity before source locking.

### S07: higher-dimensional preservation already has a substantial prior theorem

Christof Külske and Alex A. Opoku, [*The Posterior Metric and the Goodness of Gibbsianness for Transforms of Gibbs Measures*](https://arxiv.org/abs/0711.3764), *Electronic Journal of Probability* 13 (2008), 1307–1344, gives a two-layer conditional continuity treatment for local transformations using Dobrushin uniqueness and a posterior metric. This directly undercuts any generic claim that **uniform conditional first-layer Dobrushin uniqueness implies Gibbsianity of the observed layer** as a new GCL result. The full numbered theorem and all assumptions remain for source-lock audit; this observation is supported by its primary abstract and publisher metadata, not independent proof replay.

Accordingly a higher-dimensional uniform-Dobrushin preservation statement is a **known positive-control target**, not a candidate for G2 originality. A genuinely novel route must demonstrate a stronger conclusion, weaker hypotheses, new admissible transformation class, or a quantitative bound not implied by this prior source. The negative-novelty filter must be performed before theorem promotion.

### S08: exact XOR overlapping-block result already established; G2 novelty verdict NEGATIVE

**Jarkko Kari and Siamak Taati, [*Statistical Mechanics of Surjective Cellular Automata*, arXiv:1311.2319v2](https://arxiv.org/pdf/1311.2319v2), Section 3.3, Example 32 (XOR map), Proposition 33, Example 34.** Example 32 studies exactly the map $\Phi(x)(i)=x(i)+x(i+1)\pmod 2$ on a binary full shift and a biased Bernoulli source with $0<p<1$. It proves that for $p\ne1/2$ the output is **not a regular Gibbs measure**, using an equilibrium/physical-equivalence argument. The paper further credits van den Berg as an earlier origin of the strongly non-Gibbsian example (see its citation [51], Section 3.2). Proposition 33 generalizes the obstruction to non-injective image maps on invariant macroscopic measures.

**Exact prior-art verdict:** the mathematical conclusion of [G2 XOR overlap reconstruction](G2_XOR_OVERLAP_NONQUASILOCALITY_20261123.md) is **KNOWN; NOT NOVEL**. The GCL contribution is an **independent explicit finite-cylinder proof and exact rational regression fixture**, not a new theorem. The local all-ones essential-discontinuity witness is consistent with, and more concrete than, the global regular-Gibbs obstruction in Example 32; additional comparison to van den Berg is needed before asserting originality even of this proof method.

**Acquired source identity:** $\texttt{CSM-S08}$ at exact URL `https://arxiv.org/pdf/1311.2319v2`, 975832 bytes, SHA-256 `ea79ab911040536b5b3fe02a448a9e78e158a2f8f5716635470b8b1c1fdd6df6`; PDF header verified. Authenticated CHAD local acquisition receipt `GCL_CONTROL_BASH_RESULT/1 3e10f12b20014964bac259f521b6e26c`; output digest `c53517d3a1b81defe22a93939054ecf670b22dbb8ea11ed02183f8183b27177a`; `independent_execution_attested=false`.

## Deliberate negative novelty verdicts

- **Not novel:** Markov categories of finite stochastic matrices; operadic entropy maximization; categorical Gibbs specification and phase-invariance; non-Gibbsian decimation examples; the fact that positive one-dimensional hidden Markov images have exponentially continuous conditionals and Gibbs representations.
- **Not yet established:** a new theorem characterizing *necessary and sufficient categorical compatibility* of weighted gluing, stochastic normalization, physical locality, and infinite-volume DLR reconstruction for a previously untreated class.
- **Scientific pivot:** Build a fully explicit finite-state, machine-checkable **positive-control certificate** for one-dimensional channel pushforward with exponential continuity and a precise proof. Use its failure modes to identify which *higher-dimensional*, *nonuniform positivity*, or *nonlocal-gluing* regimes could carry new content. A certificate implementation itself is not a novel theorem.
- **Source-lock gap:** four pinned originals acquired and SHA-256 identified. Verify publisher-edition concordance, the full S05–S07 theorem spines, quantitative predecessors, and reproducible independent replay before promoting a G2 research candidate.

## Substantive G0 status

The four original source **statement interfaces** and the two newly necessary predecessor classes are recorded. The stronger version of G0 demanding independently replayed source proofs, publisher-edition concordance, a complete novelty matrix and source-semantic agreement is **OPEN**, with no MATHCERT authority.
