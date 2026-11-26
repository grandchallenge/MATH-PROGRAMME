# P versus NP from Above

<p class="page-deck">A bounded GCL inquiry into whether quantum verification compression can reveal a classical lower-bound principle.</p>

**Programme:** PNP-ABOVE, under [PNP-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/162)  
**Historical WP00 preflight (closed):** [PNP-ABOVE-WP00](https://github.com/grandchallenge/MATHSOLVE/issues/1136)

**Documentary evidence:** updated through WP38B, 24 November 2026 (local programme date); the 1 November version 0.1 **preprint is archival and unchanged**.

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

## Paths through the research

| Reader | Start here | Coverage |
| --- | --- | --- |
| Educated general reader | [The reader's primer](primer.md) | Verification, interactive proofs, entanglement, compression and concrete examples |
| Complexity researcher | [Technical spine](technical.md) | Theorem 12.1, resource semantics, quantitative compression and the classical transfer theorem |
| Contributor or reviewer | [Evidence and status](evidence.md) | Exact source versions, finite tests, protected artifacts, pending mathematical obligations |
| Documentary auditor | [Full GCL coverage](coverage.md) | Historical WP00–WP17 inventory and later source pointers |
| Preprint reader | [Preprint record](preprint.md) | Abstract, scholarly structure, PDF/source edition status and citation policy |

**Preprint now available:** [Download the seven-page version 0.1 PDF](https://github.com/grandchallenge/MATH-PROGRAMME/releases/download/pnp-above-preprint-v0.1.0-binary-2026-11-01/PNP_ABOVE_Verification_Compression_Preprint_v0_1.pdf) or consult the [versioned release and checksum record](preprint.md). This remains a working, uncertified research exposition, not an arXiv deposit.

The original exploratory [lay manuscript](../research/pnp_above_lay_manuscript.md) remains preserved. This documentary edition incorporates work completed afterward.

**November 2026 research update:** A classical-sampler randomness bound and a constructive SAT-to-perfect-classical-strategy transfer for **explicit finite game tables** have been proved and tested in a bounded WP01 candidate. This does not transfer to succinct quantum compression or P versus NP. A [source erratum and technical update](wp01_erratum.md) also records a factor-of-two discrepancy between the printed Theorem 12.1 and its displayed proof.

**Source-native research result, 18 November 2026:** Protected WP08–WP14 now construct and check an original source-bounded nine-stage reference verifier with fully occupied conditional CL stages. WP15 proves the actual reference game has a perfect deterministic strategy. WP16 proves its shared Alice/Bob sampling yields identical questions. WP17 establishes the general original-game no-advantage theorem: **on any diagonal-supported finite synchronous game with nonempty answers, synchronous, quantum and commuting optimal values coincide**, even if some questions are unwinnable. Consequently merely changing WP14's decision rule cannot produce quantum advantage. This is a rigorous negative design result, not a hard game or P-versus-NP theorem. Read the [exact source/receipt inventory](coverage.md) and [full evidence audit](evidence.md).

**WP18 construction (18 November 2026):** GCL has now formally built the complementary missing sampler: a genuinely **player-asymmetric nine-stage** conditional-linear distribution with positive probability on unequal questions, an executable original source query interface, and a bounded original verifier. However the **old identity decider** remains trivially classically winnable, and original synchronous, quantum and commuting game values still equal 1. A quantum gap requires new question structure and an answer-sensitive decision predicate; merely fixing one component is insufficient. The [complete evidence ledger](evidence.md#wp18-native-asymmetric-nine-stage-cl-sampler-and-second-no-gap-control-18-november-2026) documents the actual verified scope.

**WP19 universal obstruction (19 November 2026):** The next original-source theorem proves the precise 512-pair distribution of WP18: **256 star edges** from a single Alice question and **256 isolated diagonal edges**, each with weight `1/512`. More strongly, it proves that **no synchronous decision predicate whatsoever** can produce a quantum advantage on that source law: the original synchronous, finite-dimensional quantum and commuting optima are *always equal*, even when the common winning probability is less than one. Thus WP18's question sampler itself must be replaced with a richer two-sided law; changing its decider cannot help. The [mathematical proof and evidence](evidence.md#wp19-universal-star-support-no-quantum-advantage-19-november-2026) distinguish the actual source models from an executable hard-game construction, which remained open at WP19.

## The current frontier: finding a solution

The WP19 no-gap obstruction was a design result, not a universal impossibility theorem. WP20–WP22 subsequently establish a bounded executable native Bell-gap verifier. WP27–WP35 develop SAT-dependent native verification, control the numeric index versus binary source length, and prove an exact classical decision equivalence for the restricted valid-index compressed promise (under the stated verifier boundedness hypothesis). That is not a general strategy-synthesis theorem.

WP38A–B now prove the following equivalence of **existence of total polynomial-time native programs**:

- Deciding the restricted valid compressed promise.
- Deciding whether a Boolean formula is satisfiable.
- Finding a satisfying assignment whenever one exists.
- Finding the lexicographically greatest satisfying assignment in the fixed support order.

For the witness programs, only satisfiable formulas require correct outputs; the polynomial runtime bound applies to all inputs. Read the [worked example in the primer](primer.md#from-knowing-that-a-solution-exists-to-finding-it) and [technical statement](technical.md).

**What remains difficult:** finding a representation-independent superpolynomial obstruction against *every* classical witness constructor. Quantum Schmidt rank is not classical time. A semantic proof-width lower bound (WP37) can coexist with a fast algebraic algorithm; a native quadratic charged-copy lower bound (WP36) can arise even with no active variables. Neither closes the unrestricted target.

## A distinct algebraic route: Structural Capacity Calculus

[Read the illustrated SCC research chapter](../scc.md). Its central question is whether a conservation law can distinguish irreducible logical obligations from relationships generated cheaply by compositional reuse. The graded promotion and syzygy transport identities are author-derived results with bounded exact regression, not unrestricted lower bounds.

## What is known, calculated, and open

| Result | Protected evidence | Scope |
| --- | --- | --- |
| Quantum verification compression | External MIP* = RE theorem; [source erratum](wp01_erratum.md) | Quantum resource, not classical time |
| Restricted valid-promise/SAT equivalence | [WP34](https://github.com/grandchallenge/MATHSOLVE/pull/1287), [WP35](https://github.com/grandchallenge/MATHSOLVE/pull/1288) | Native model; exact valid indices |
| Quadratic native charged-copy bound | [WP36B](https://github.com/grandchallenge/MATHSOLVE/pull/1292) | Representation overhead |
| Semantic proof width and affine shortcut | [WP37](https://github.com/grandchallenge/MATHSOLVE/pull/1293) | Restricted proof measure, not all-algorithm time |
| Decision, witness and canonical witness equivalence | [WP38A](https://github.com/grandchallenge/MATHSOLVE/pull/1297), [WP38B](https://github.com/grandchallenge/MATHSOLVE/pull/1298) | 43 checked theorems; native model |
| Unrestricted superpolynomial lower bound and standard machine concordance | [PNP-001 tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/162) | OPEN |

The [evidence ledger](evidence.md) distinguishes protected source results from historical controls and the independent certification route.

## Relation to the existing GCL books

The [P versus NP domain page](../domains/p_vs_np.md), [PNP-001 Research Guide](../domains/PNP_001_RESEARCH_GUIDE.md) and documentary [*The Shape of Computational Truth*](../documentaries/index.md) explain the overarching Millennium problem. PNP-ABOVE is a specific research path within that problem; the earlier books remain authoritative for their own editorial scope.

## Primary literature

Ji et al., [*MIP*=RE*, arXiv:2001.04383v4](https://arxiv.org/pdf/2001.04383v4), especially Definition 5.12, Theorem 12.1, Figure 15 and Table 2. See also their [quantum low-individual-degree soundness paper](https://arxiv.org/abs/2009.12982) for the corrected underpinning.

For precisely what this programme's claims mean, continue to [Evidence and status](evidence.md).
