# P versus NP from Above

<p class="page-deck">A bounded GCL inquiry into whether quantum verification compression can reveal a classical lower-bound principle.</p>

**Programme:** PNP-ABOVE, under [PNP-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/162)  
**Solve research obligation:** [PNP-ABOVE-WP00](https://github.com/grandchallenge/MATHSOLVE/issues/1136)  
**Documentary edition:** 1 November 2026, version 0.1  
**Claim status:** Exploratory. No proof of P = NP or P ≠ NP, no new unrestricted classical lower bound.

!!! warning "Research is not certification"
    The equality MIP* = RE is an established theorem of Ji, Natarajan, Vidick, Wright and Yuen. Its use as an inspiration does not solve P versus NP. GCL's finite models and conditional corollaries are separately scoped; the preprint is not an arXiv submission or mathematical certification.

## The central question

P versus NP asks whether every yes/no problem with efficiently checkable positive certificates can also be decided efficiently. For SAT, checking a proposed satisfying assignment is easy. Whether a deterministic polynomial-time algorithm can decide SAT on all instances remains unknown.

A different verification model allows a fast referee to ask questions of computationally unbounded provers. With entangled quantum provers, the celebrated external result is

$$
\mathsf{MIP}^{*}=\mathsf{RE}.
$$

This does **not** enable an ordinary computer to decide the Halting Problem. It says that an efficient verifier combined with suitably powerful interacting provers can recognize all recursively enumerable languages under the source theorem's completeness and soundness conventions.

Our research question is narrower: can a finite *structural invariant* of this verification machinery survive a reduction to classical computation, yielding an actual lower bound?

## Four paths through the research

| Reader | Start here | Coverage |
| --- | --- | --- |
| Educated general reader | [The reader's primer](primer.md) | Verification, interactive proofs, entanglement, compression and concrete examples |
| Complexity researcher | [Technical spine](technical.md) | Theorem 12.1, resource semantics, quantitative compression and the classical transfer theorem |
| Contributor or reviewer | [Evidence and status](evidence.md) | Exact source versions, finite tests, protected artifacts, pending mathematical obligations |
| Preprint reader | [Preprint record](preprint.md) | Abstract, scholarly structure, PDF/source edition status and citation policy |

The original exploratory [lay manuscript](../research/pnp_above_lay_manuscript.md) remains preserved. This documentary edition incorporates work completed afterward.

## The missing classical bridge

Let $G_n$ be a uniform family of games and let $\mathcal C_{\mathcal A}(G_n)$ be the cost of implementing a precisely specified classical strategy or circuit model $\mathcal A$. A quantum-strategy Schmidt-rank lower bound is not automatically a lower bound on this classical cost.

Even a genuine classical cost lower bound will not settle P versus NP unless an independently proved implication supplies a conflicting upper bound from a hypothetical fast SAT algorithm:

$$
\mathrm{SAT}\in\mathsf P
\quad\Longrightarrow\quad
\mathcal C_{\mathcal A}(G_n)\le n^{O(1)}.
$$

No such general transfer theorem has been established. The programme is designed to test and, where necessary, falsify purported bridges rather than treat their existence as an assumption.

## What is known, calculated, and open

**External mathematics:** Ji et al. proved MIP* = RE and the gap-preserving compression theorem. The latter concerns nine-level normal-form verification and a lower bound on quantum Schmidt rank under stated hypotheses.

**GCL source and finite-model work:** The magic-square calibration, symbolic compression-parameter ledger, explicit nine-level identity input and finite emulator clarify the gap between quantum strategy resources and classical decision complexity.

**Unproved bridge:** No new lower bound for unrestricted classical SAT or circuits; no uniformly controlled SAT-to-strategy reduction; no numerical execution of the entire MIP* compression construction.

| Material | Primary location | Status |
| --- | --- | --- |
| Parent PNP-001 challenge | [Programme tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/162) | Open |
| Magic-square finite calibration | [MATHSOLVE PR #1137](https://github.com/grandchallenge/MATHSOLVE/pull/1137) | Bounded research note |
| Compression theorem interface | [MATHSOLVE PR #1140](https://github.com/grandchallenge/MATHSOLVE/pull/1140) | Source extraction |
| Schmidt-rank transfer audit | [MATHSOLVE PR #1142](https://github.com/grandchallenge/MATHSOLVE/pull/1142) | Resource distinction |
| Three-stage symbolic parameter ledger | [Protected ledger](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_COMPRESSION_PARAMETER_LEDGER.md) | Protected source record |
| Nine-level sampler and finite emulator | [Protected research note](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_NINE_LEVEL_INPUT_AND_TRANSFER.md) | Admitted finite input |
| Exact machine encoding; numerical compression constants; classical transfer | [Solve task #1136](https://github.com/grandchallenge/MATHSOLVE/issues/1136) | Open |

## Relation to the existing GCL books

The [P versus NP domain page](../domains/p_vs_np.md), [PNP-001 Research Guide](../domains/PNP_001_RESEARCH_GUIDE.md) and documentary [*The Shape of Computational Truth*](../documentaries/index.md) explain the overarching Millennium problem. PNP-ABOVE is a specific research path within that problem; the earlier books remain authoritative for their own editorial scope.

## Primary literature

Ji et al., [*MIP*=RE*, arXiv:2001.04383v4](https://arxiv.org/pdf/2001.04383v4), especially Definition 5.12, Theorem 12.1, Figure 15 and Table 2. See also their [quantum low-individual-degree soundness paper](https://arxiv.org/abs/2009.12982) for the corrected underpinning.

For precisely what this programme's claims mean, continue to [Evidence and status](evidence.md).
