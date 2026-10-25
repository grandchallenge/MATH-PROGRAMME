# The Element in Half the Worlds

**Source status:** Open conjecture · UC-DOC-WP01 · No proof claimed.

> **GitHub equation reader; automatically generated from the original manuscript.**
> The [illustrated documentary](../union_closed.md) has the canonical layout, figures and reader controls.
> This is not independent mathematical or publication certification.

A note to the reader

## Wonder first; the universal quantifier always visible

A finite family of sets can obey one simple closure law and still resist a universal abundance theorem. Frankl’s conjecture says that some element belongs to at least half of the sets in every

**nontrivial**

finite union-closed family, meaning here a finite union-closed family with nonempty support. The empty-only family $\mathcal F=\{\varnothing\}$ is an essential excluded edge case: its support is empty, so no such element exists. It is an

**Open conjecture**

.

The plates are mnemonic maps, not proof diagrams. Definitions, exact quantifiers, theorem labels, finite-certificate scopes, source links, and the claim ledger govern the mathematics.

**Edition status:**

Open conjecture; full-tier documentary exposition; no proof claim.

**Open conjecture · Frankl**

Let $\mathcal F$ be a finite union-closed family with $\mathop{\mathrm{supp}}(\mathcal F)\ne\varnothing$. Then there is an element $x\in\mathop{\mathrm{supp}}(\mathcal F)$ such that $2\mathop{\mathrm{freq}}_{\mathcal F}(x)\ge |\mathcal F|$.

**Claim boundary**

This is a source-normalized illustrated documentary. It does not prove Frankl's conjecture, establish a new universal frequency bound, certify unreviewed proof claims, or make a novelty, priority, or public-release claim.

> **Plate I.** Plate I The Garden That Closes Pairwise union is local. The conjectured abundant element is a global witness. [Illustration](../../assets/documentaries/union_closed/plate_garden.svg). *Alt text:* A branching garden of finite sets flows upward to their pairwise unions, contrasting local closure with the global search for an abundant element.

Chapter I

## The garden that closes under union

A family $\mathcal F$ is union-closed when $A,B\in\mathcal F$ implies $A\cup B\in\mathcal F$.

**Definition**

The support is $\mathop{\mathrm{supp}}(\mathcal F)=\bigcup_{A\in\mathcal F}A$. The frequency of $x$ is $\mathop{\mathrm{freq}}_{\mathcal F}(x)=|\{A\in\mathcal F:x\in A\}|$.

Closure describes what happens after choosing two members. Frankl’s statement asks for a single coordinate whose incidence count reaches half the entire family. The top union belongs to every finite nonempty union-closed family, but that alone does not identify an abundant element.

> **Plate II.** Plate II The Half-Way Balance The threshold is sharp: powersets attain equality for every element. [Illustration](../../assets/documentaries/union_closed/plate_frequency.svg). *Alt text:* A brass balance compares one element’s frequency with half the number of sets, above the incidence-counting identity linking all frequencies to total set size.

Chapter II

## The half-way balance

In the powerset $\mathcal P(U)$, each element occurs in exactly half the subsets. Thus no universal theorem can demand more than one half. Double-counting incidences gives

$$
\sum_x\mathop{\mathrm{freq}}_{\mathcal F}(x)=\sum_{A\in\mathcal F}|A|.
$$

**Established elementary terrain**

Powersets attain the threshold sharply. A union-closed family containing a singleton $\{x\}$ satisfies Frankl for $x$ through the injection $A\mapsto A\cup\{x\}$ from sets missing $x$ to sets containing it.

The identity controls an average. It does not force the maximum frequency to reach one half unless additional structure supplies the missing bridge.

Chapter III

## Small worlds, exact ledgers

For a universe of size $n$, exact enumeration can test union closure and every frequency profile. The programme’s independently replayed certificate finds no nontrivial counterexample for universes $n\le4$.

**Exact bounded result**

The $n\le4$ statement is exact finite verification for those universes.

**Bounded-computation guardrail**

Finite replay validates definitions, software, and bounded claims. It does not prove the conjecture for arbitrary finite universes.

> **Plate IV.** Plate IV The Lattice Cathedral Set-family and lattice formulations require an explicit correspondence. [Illustration](../../assets/documentaries/union_closed/plate_lattice.svg). *Alt text:* A finite join-semilattice rises from bottom to top through atoms, joins, and irreducible elements, illustrating the lattice formulation and deletion routes.

Chapter IV

## Mirrors, intersections, and lattices

Taking complements turns unions into intersections. Inclusion turns a union-closed family into a finite join-semilattice with $A\vee B=A\cup B$. These viewpoints reveal atoms, irreducibles, upper cones, deletion operations, and minimal-counterexample constraints.

**Formal bounded terrain**

The programme records Lean-checked lattice theorems and hybrid packages through the governed Union-Closed theorem spine. Each result retains its precise hypotheses and certificate boundary.

**Correspondence guardrail**

Order duality, complement duality, ideal-family averaging, and set-family frequency are related but not interchangeable without a complete translation theorem.

Chapter V

## The average-size door

Reimer’s theorem gives a lower bound on the average size of members of a union-closed family. Combined with incidence double-counting, it guarantees some element with nontrivial frequency, but the support-size denominator prevents the argument from reaching the universal half threshold.

**Imported established theorem · Reimer**

The exact source statement controls this edition. The theorem is a major structural constraint, not a proof of Frankl’s conjecture.

> **Plate III.** Plate III The Entropy Bridge Dimension-free positive constants are breakthroughs; they remain below one half. [Illustration](../../assets/documentaries/union_closed/plate_entropy.svg). *Alt text:* A uniform random set passes through coordinate entropies and coupled unions to a dimension-free constant lower bound that still falls short of one half.

Chapter VI

## Entropy enters the garden

Choose a uniform random member $A\in\mathcal F$ and write its membership indicators as coordinates. Entropy decomposes the uncertainty of the random set, while coupled copies and union closure create inequalities among the coordinate marginals.

**Imported theorem terrain**

Gilmer established the first dimension-free positive constant; Sawin, Yu, Cambie, Alweiss–Huang–Sellke, Liu, and others refined the entropy and coupling landscape. Exact constants and assumptions remain source-specific.

**Entropy guardrail**

A positive constant below one half, a numerically optimized coupling, or a barrier for one entropy ansatz does not settle the universal conjecture.

> **Plate VI.** Plate VI Islands of Theorem The frontier advances without erasing the open boundary. [Illustration](../../assets/documentaries/union_closed/plate_frontier.svg). *Alt text:* Islands representing special families, rigorous constant bounds, and formal lattice results approach but do not reach the open one-half threshold.

Chapter VII

## The theorem frontier

Known terrain includes elementary families, bounded exact verification, average-size inequalities, rigorous dimension-free constants, structural restrictions on minimal counterexamples, and formalized lattice results.

**Still open universally**

No admitted result proves that every nontrivial finite union-closed family (one with nonempty support) has an element in at least half its sets.

Recent posted proof claims remain current-awareness entries until their theorem statements, dependencies, and complete proofs are independently audited. Repository merge, citation count, or public attention does not change mathematical status.

> **Plate V.** Plate V The Certificate Forge A certificate proves only the claim encoded by its contract. [Illustration](../../assets/documentaries/union_closed/plate_certificate.svg). *Alt text:* A formal forge separates exact finite replay, Lean theorems, imported results, hybrid packages, source audits, and the universal conjecture’s claim boundary.

Chapter VIII

## The certificate forge

The programme separates human proof, imported theorem, Lean theorem, exact finite replay, numerical evidence, and hybrid certificate. A hybrid package may combine a formal transfer theorem with an independently replayed finite fact, but its public claim must expose both components.

**Certification discipline**

Lean checks encoded terms under explicit imports. Exact replay checks a declared finite search space. Neither silently verifies source correspondence or an unbounded theorem.

**No promotion by proximity**

Many correct restricted results surrounding an open conjecture do not add up to a proof unless a complete logical bridge is supplied.

Technical appendix A

## Precise definitions and normalizations

For finite $\mathcal F\subseteq\mathcal P(U)$, define $\mathop{\mathrm{supp}}(\mathcal F)=\bigcup\mathcal F$.

The frequency is $\mathop{\mathrm{freq}}_{\mathcal F}(x)=|\{A\in\mathcal F:x\in A\}|$.

An element is abundant when $2\mathop{\mathrm{freq}}_{\mathcal F}(x)\ge|\mathcal F|$. The canonical target requires nonempty support and reduces the ground set to the support. It excludes both the empty family and the family $\{\varnothing\}$: in either case no support element exists.

Technical appendix B

## Elementary proof spine

The top union belongs to the family by finite repeated closure. Powerset sharpness follows by toggling a chosen coordinate. The singleton theorem uses the injective map $A\mapsto A\cup\{x\}$. These are complete arguments within their scopes and suitable for direct formalization.

Technical appendix C

## Entropy method skeleton

For membership indicators $(X_x)_x$, $H(A)=H((X_x)_x)\le\sum_x H(X_x)$. Coupled copies are combined through union closure. Assuming all marginals lie below a selected threshold, one seeks an entropy contradiction. The coupling, concavity estimates, and optimization domain are theorem-bearing details.

Technical appendix D

## Lattice correspondence notes

Inclusion supplies a finite join-semilattice. Upper cones and irreducible elements can encode frequency-like data. Translation obligations include separation, the ground-set representation, internal versus ambient lattices, and the exact relation between lattice elements and set coordinates.

Technical appendix E

## Formal and computational inventory

| Artifact class | Supports | Does not support |
| --- | --- | --- |
| Lean theorem | Encoded theorem under imports | Unencoded source correspondence |
| Exact finite certificate | Declared finite search | Arbitrary universes |
| Hybrid package | Explicit components and bridge | A stronger unstated theorem |
| Numerical optimization | Candidates and diagnostics | Rigorous universal bounds |

Technical appendix F

## Source audit ledger

Reimer’s theorem and the post-2022 entropy results are literature-derived imports. Programme lattice claims are governed by Domain 01 and their individual formal or hybrid records. Recent proof claims remain

`NEEDS_AUDIT`

until complete independent review.

**Imported-source discipline**

A bibliography identifies provenance. It does not replace theorem-body verification, normalization checks, or proof.

Technical appendix G

## Claim-level trust matrix

| Claim | Trust class | Qualification |
| --- | --- | --- |
| Frankl’s half-frequency statement | open | no admitted proof |
| Top union, powerset, singleton injection | established | elementary proofs |
| No nontrivial counterexample for $n\le4$ | exact finite verification | bounded universe |
| Reimer average-size theorem | imported established | source statement governs |
| Dimension-free constant bounds | imported established | constants and hypotheses are source-specific |
| Programme lattice results | formal or hybrid bounded | individual records govern |
| 2026 posted proof claims | needs audit | not promoted here |
| SVG plates | pedagogical | never proof authority |

**Final claim boundary**

This web edition changes presentation and collection membership, not theorem strength. Frankl’s conjecture remains open, and no interaction, plate, bounded replay, or formal special case supplies the missing universal proof.

Sources and programme crosswalk

## Governing literature and campaign record

David Reimer, [“An Average Set Size Theorem”](https://doi.org/10.1017/S0963548302005230).

Justin Gilmer, [“A constant lower bound for the union-closed sets conjecture”](https://arxiv.org/abs/2211.09055).

Will Sawin, [“An improved lower bound for the union-closed set conjecture”](https://arxiv.org/abs/2211.11504).

Lei Yu, [“Dimension-Free Bounds for the Union-Closed Sets Conjecture”](https://arxiv.org/abs/2212.00658).

Stijn Cambie, [“Better bounds … using the entropy approach”](https://arxiv.org/abs/2212.12500).

Ryan Alweiss, Bo’az Huang, and Mark Sellke, [“Improved Lower Bound for Frankl’s Union-Closed Sets Conjecture”](https://doi.org/10.37236/12232).

Jingbo Liu, [“Improving the Lower Bound … via Conditionally IID Coupling”](https://arxiv.org/abs/2306.08824).

Antoine Bouchard, [lattice formulation work](https://arxiv.org/abs/2503.00277).

Masahiro Hachimori and Kenji Kashiwabara, [ideal-family work with Lean 4 formal proof](https://arxiv.org/abs/2504.13454).

Programme links: [Domain 01](../../domains/union_closed/) · [canonical master plan](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md) · [UC-DOC-WP00 source lock](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK) · [UC-DOC-WP01 admission](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/union_closed/UC_DOC_WP01_WEB_ADMISSION) · [review records](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/reviews/union_closed)

## Edition record

This is the first Wave Two admission and the first non-Millennium full-tier edition. It exercises the shared reader against finite combinatorics, exact enumeration, formal proof artifacts, hybrid certificates, and active source-audit obligations.

The web edition is derivative. The committed pointer is a source record; the checksum-locked complete illustrated source bundle is the authoritative source artifact. MathJax 3.2.2 is a version-pinned network enhancement, and the source TeX remains present when it is unavailable.

**Web claim boundary:** This is a source-normalized illustrated documentary. It does not prove Frankl's conjecture, establish a new universal frequency bound, certify unreviewed proof claims, or make a novelty, priority, or public-release claim.

[Web-edition data](../union_closed.edition.json)[Reusable schema](../documentary_web.schema.json)[Source record](../sources/the_element_in_half_the_worlds.tex)[Artifact manifest](../ARTIFACT_MANIFEST.json)

Rendered PDF

3,343,773 bytes ·

`6ea03bef444f19ae8013e80c76a5112fda9c6b740d61387c2bfeea5921ac71dc`

·

`metadata_only`

Complete LaTeX source

50,548 bytes ·

`e889079fc77163e57b0c239e8f25ae29a3ded640b32120f65d1f3708c05dfdde`

·

`metadata_only`

Authoritative complete illustrated source bundle

3,100,936 bytes ·

`3a1fcf16dee92c6bbf5fd8285702e31c828aa6d1666e5605e8981346f4bd2daf`

·

`metadata_only`
