# CSM-00/G0 — primary-statement audit and negative-novelty decisions

**Programme:** CSM-001. **Audit date:** 2026-11-23. **Status:** PARTIAL G0: four original primary-paper statement surfaces inspected; primary-document binary hashing, publication-vs-preprint line-by-line concordance, exhaustive prior-art search, and independent source-proof replay remain open. **Tracker:** [CSM-001 issue #3136](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3136). This record must not be used as a complete source lock or novelty certificate.

## Observed primary versions and exact theorem interfaces

| Key | Version examined, with primary link | Grounded numbered result | What the result permits; what it does not |
| --- | --- | --- | --- |
| S01 | [Fritz, arXiv:1908.07021v8](https://arxiv.org/pdf/1908.07021v8), front matter 31 May 2020; *Advances in Mathematics* 370 (2020) 107239 | Definition 2.1: Markov category is symmetric monoidal with coherent copy/delete comonoids and natural deletion. Example 2.5: finite stochastic matrices are a Markov category | Normalized finite kernels permit deleting any output without changing total probability. **Full weighted nonnegative matrices are not automatically Markov:** deleting the output multiplies an input by its column sum. |
| S02 | [Baez, Lynch, Moeller, arXiv:2111.10315](https://arxiv.org/pdf/2111.10315), PDF front matter says v2, 10 February 2023; *Journal of Mathematical Physics* 64 (2023) 023304 | Lemmas 27, 39 and Theorem 40: the entropy construction is a lax symmetric monoidal functor from convex relations to sets, supplying an operad algebra of thermostatic systems | Operadic entropy optimization under convex constraints is established; this **does not** assert that arbitrary positive factor-network marginalization preserves interaction locality. |
| S03 | [Sergeant-Perthuis, arXiv:2403.16104](https://arxiv.org/pdf/2403.16104), PDF v1, 24 March 2024 | Definition 3: compatible proper specification kernels. Definition 4: Gibbs measures consistent with a specification. Theorem 1: kernels of specifications form the appropriate poset representation. Theorem 2: Gibbs marginals are compatible sections | Categorical specification/invariance and phases have prior art. Weighted finite diagrams need a precise normalization and limit bridge before they can be identified with DLR specifications. |
| S04 | [van Enter, Fernández, Sokal, hep-lat/9210032](https://arxiv.org/pdf/hep-lat/9210032), source front matter 22 October 1992; *Journal of Statistical Physics* 72 (1993) | Theorem 4.1: for zero-field two-dimensional nearest-neighbour Ising at coupling exceeding the paper's explicit large-coupling threshold (approximately 0.764285), spacing-2 decimation produces an image measure with no quasilocal specification | The non-Gibbsian RG obstruction is already rigorous. The theorem is **not** an assertion that every finite marginal or every RG map is non-Gibbsian. The source also treats other dimensions and transformations with different conditions. |

**Provenance precision:** The version numbers above are printed in the inspected originals, not inferred from current bibliography headings. The user-facing source URLs are retrieval locators. A canonical SHA-256 of the PDF bytes is **not** recorded; the review environment could read source text but could not acquire those bytes for a repeatable digest. Consequently this is a versioned theorem-interface audit, not complete source-lock G0.

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

## Deliberate negative novelty verdicts

- **Not novel:** Markov categories of finite stochastic matrices; operadic entropy maximization; categorical Gibbs specification and phase-invariance; non-Gibbsian decimation examples; the fact that positive one-dimensional hidden Markov images have exponentially continuous conditionals and Gibbs representations.
- **Not yet established:** a new theorem characterizing *necessary and sufficient categorical compatibility* of weighted gluing, stochastic normalization, physical locality, and infinite-volume DLR reconstruction for a previously untreated class.
- **Scientific pivot:** Build a fully explicit finite-state, machine-checkable **positive-control certificate** for one-dimensional channel pushforward with exponential continuity and a precise proof. Use its failure modes to identify which *higher-dimensional*, *nonuniform positivity*, or *nonlocal-gluing* regimes could carry new content. A certificate implementation itself is not a novel theorem.
- **Source-lock gap:** retain exact retrieved binary digests, verify edition agreement with published versions, audit the full S05 and S06 theorem spines and quantitative predecessors, then repeat the novelty comparison before promoting a G2 research candidate.

## Substantive G0 status

The four original source **statement interfaces** and the two newly necessary predecessor classes are recorded. The stronger version of G0 demanding full paper proofs, source-byte digests, complete novelty matrix and source-semantic agreement is **OPEN**, with no MATHCERT authority.
