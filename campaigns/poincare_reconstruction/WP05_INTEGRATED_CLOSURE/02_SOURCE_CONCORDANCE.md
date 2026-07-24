# PC-WP05 — source-concordance audit

## Audit question

Do the campaign-critical interfaces used by the finite-extinction Poincaré route agree in theorem role and logical direction across Perelman’s primary preprints, Kleiner–Lott’s detailed notes, and Morgan–Tian’s complete reconstruction?

## Editions fixed

| Key | Source | Edition used |
|---|---|---|
| `P-I` | Perelman, *The entropy formula for the Ricci flow and its geometric applications* | arXiv `math/0211159`, v1 |
| `P-II` | Perelman, *Ricci flow with surgery on three-manifolds* | arXiv `math/0303109`, v1 |
| `P-III` | Perelman, *Finite extinction time for the solutions to the Ricci flow on certain three-manifolds* | arXiv `math/0307245`, v1 |
| `KL` | Kleiner–Lott, *Notes on Perelman's Papers* | arXiv `math/0605667`, v5 / Geometry & Topology 12 |
| `MT` | Morgan–Tian, *Ricci Flow and the Poincaré Conjecture* | Clay Mathematics Monographs 3 (2007) |

## Critical crosswalk

| Campaign interface | Perelman | Kleiner–Lott | Morgan–Tian | Disposition |
|---|---|---|---|---|
| entropy/reduced geometry and no local collapsing | `P-I`, especially §§3–10 | detailed reconstruction following `P-I` numbering | Parts 1–2, especially Chapters 6–8 | concordant in role; exact proof-step concordance retained |
| ancient limits and canonical neighbourhoods | `P-I` §§11–12 | detailed reconstruction of `P-I` | Chapters 9–11 and Appendix | concordant in role and consumer chain |
| surgery construction and restart | `P-II` | detailed reconstruction of `P-II` | Chapters 12–17 | concordant in role; parameter-level equivalence retained |
| no accumulation / all-time surgery | `P-II` | Claim 3.4 and detailed construction | Theorem 0.3; Theorem 15.9; Chapter 17 | concordant for campaign use |
| topology change across surgery | `P-II` surgery description | overview Claims 3.2–3.3 and reverse-surgery description | Theorem 0.3; Proposition 15.3 | concordant; MT is governing exact topology interface |
| finite extinction hypothesis | `P-III`, Theorem 1.1: closed oriented, no aspherical prime factors | Claim 3.5 and references to finite-extinction results | Theorem 0.4 / Chapter 18 | concordant after the WP02 prime-decomposition/group-hypothesis bridge |
| extinction-to-factor classification | implicit combination of `P-II` topology and `P-III` extinction | overview: finite extinction plus reverse surgery yields standard factors | Corollary 15.4; Introduction Theorem 0.1 and Corollary 0.5 | concordant; MT governs the campaign terminal statement |
| simply connected terminal conclusion | primary route consequence | overview invokes van Kampen after standard factor expression | Corollary 0.2 and Corollary 15.4(2) | concordant and non-circular when factor expression precedes discharge |

## Perelman II correction discipline

The introduction to `P-II` explicitly excludes two assertions from `P-I` §13:

1. the graph-manifold conclusion for local lower-curvature collapse is deferred to separate work;
2. a maximal-horn volume lower bound and eventual smoothness assertion is identified as unjustified and irrelevant to the remaining conclusions.

Campaign disposition:

- neither assertion is used in the finite-extinction Poincaré route;
- no WP02 theorem interface may cite either assertion as established by `P-II`;
- the stronger geometrization route remains separately gated;
- `P-II` supersedes any unqualified use of the affected `P-I` sketch claims.

## Finite-extinction normalization

`P-III` states finite extinction for a closed oriented 3-manifold whose prime decomposition has no aspherical factors. `MT` states an equivalent campaign-facing hypothesis using a fundamental group that is a free product of finite groups and infinite cyclic groups and records the topological equivalence in its introduction. The campaign uses the implication chain:

```text
pi1(M)=1
  -> M orientable
  -> prime decomposition has no aspherical factor
  -> P-III finite-extinction hypothesis.
```

The bridge is a separate topology import. It is not part of Perelman’s analytic estimate and is not proved by extinction.

## Governing-source policy

1. Primary attribution belongs to Perelman.
2. For detailed finite-time extinction and terminal topology in this archive, Morgan–Tian is the governing reconstruction source.
3. Kleiner–Lott is the governing detailed cross-check for Perelman I and II, but it does not replace the campaign’s Morgan–Tian source for the expanded proof of Perelman III.
4. Where formulations differ, the archive records a one-way implication or hypothesis bridge instead of declaring literal identity.
5. Exact quotation claims require a locator and edition; semantic theorem-interface summaries do not masquerade as quotations.

## Closed concordance obligations

The following are closed for archival publication:

- identity and ordering of the three Perelman primary sources;
- exclusion of the two `P-II`-identified unsupported/deferred assertions;
- role of `P-I` in noncollapsing and canonical-neighbourhood preparation;
- role of `P-II` in surgery and all-time continuation;
- role of `P-III` in finite extinction;
- Morgan–Tian’s explicit topology-event and terminal-reconstruction statements;
- Kleiner–Lott’s detailed coverage boundary: Perelman I/II plus finite-extinction handoff.

## Retained concordance debt

The following remain open but nonblocking for a qualified archive:

- sentence-by-sentence concordance of all nineteen WP02 interfaces;
- full correspondence of every surgery parameter and normalization across `P-II`, `KL`, and `MT`;
- quotation-level locator verification for every analytic sublemma;
- independent rechecking of all reconstructed analytic proofs;
- reconciliation with every alternative complete exposition.

These debts block the labels “source-complete line-by-line reconstruction,” “independently verified proof,” and “full formal proof certificate.” They do not block publication of the explicitly bounded archive.