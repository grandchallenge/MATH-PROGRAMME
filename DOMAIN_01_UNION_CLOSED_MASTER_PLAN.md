# DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md

## Domain

**Domain 01: Union-Closed Sets / Frankl's Conjecture**

This is the first Lean-friendly Grand Challenge domain for the MATHFORGE -> MATHSOLVE -> MATHCERT platform.

## Problem statement

A finite family `F` of sets is union-closed if whenever `A` and `B` are in `F`, the union `A ∪ B` is also in `F`. Frankl's union-closed sets conjecture states that every finite nontrivial union-closed family has an element appearing in at least half of the sets in the family.

The conjecture remains open. Recent breakthroughs beginning with Gilmer established the first dimension-free constant lower bound, followed by rapid improvements around the constant `(3 - sqrt(5))/2 ≈ 0.38197` and slightly beyond in subsequent work.

## Why this is the first domain

Union-Closed Sets is an ideal first test case because it is:

1. **Easy to state** but difficult to prove.
2. **Finite and combinatorial**, hence Lean-friendly.
3. **Rich in equivalent formulations**, including lattice and intersection-closed dual forms.
4. **Well suited to exact finite computation**.
5. **Dangerous enough to require discipline**, since it has attracted many false proofs.
6. **Pedagogically strong**, because small examples expose much of the difficulty.

## Programme posture

The programme does not begin by trying to prove Frankl's conjecture outright. It begins by building a certified research environment around it.

The first objectives are:

- reconstruct the problem and literature status;
- formalize definitions in Lean;
- build exact small-universe ledgers;
- identify known special cases and formalization targets;
- create reusable finite-family certificate machinery;
- select tractable restricted theorem targets.

## Three-pillar domain split

### MATHFORGE tasks

```text
- Ingest and normalize source descriptions.
- Enumerate union-closed families for small universes.
- Generate example families and frequency profiles.
- Search for extremal low-frequency families.
- Produce candidate reductions and restricted regimes.
- Record failed heuristics and false-proof traps.
```

### MATHSOLVE tasks

```text
- WP01 status spine.
- WP02 Lean handoff.
- WP03 primary-source audit and known-bounds synthesis.
- WP04 checked special cases and exact finite replay.
- WP05 restricted-target selection after external formalization audit.
- WP06 restricted theorem target selection.
```

### MATHCERT tasks

```text
- Define finite set families in Lean.
- Define union-closure, support, frequency, abundance.
- State Frankl's conjecture.
- Prove elementary lemmas: singleton case, powerset sharpness, top-union membership.
- Replay small finite certificates independently.
- Formalize selected known special cases where infrastructure permits.
```

## Work Package sequence

### WP01: Status spine

Goal: establish the problem, known terrain, partial bounds, false-proof risk, and certification opportunities.

Deliverables:

- lay companion;
- formal problem statement;
- literature map;
- claim ledger;
- first exact enumeration ledger;
- next-target list.

### WP02: Lean handoff

Goal: translate the problem into Lean-ready definitions and theorem statements.

Deliverables:

- informal-to-formal dictionary;
- Lean file plan;
- theorem statement scaffold;
- first local lemmas;
- missing mathlib inventory;
- exact certificate schema.

### WP03: Known bounds synthesis

Goal: explain the information-theoretic method and recent constant-bound progress without overclaiming.

Deliverables:

- Gilmer method exposition;
- improved constant-bound map;
- coupling/entropy formulation notes;
- formalization feasibility assessment.

### WP04: Special cases and finite certificates

Goal: identify special cases that are approachable in Lean or exact computation.

Deliverables:

- Lean-checked singleton and two-element-member cases;
- independently replayed small-universe certification;
- families with bounded universe/cardinality;
- exact certificate verifier.

### WP05: Restricted theorem target

Goal: select a genuine restricted theorem target that is useful, checkable, and not merely a toy.

Candidates:

- closure-generated families with constrained generator rank;
- separating families under compression operations;
- low-height or chain-constrained families;
- certificate-verifiable finite lattice classes.

## Claim boundary

No Work Package in this domain may state or imply that Frankl's conjecture is close to solved unless it has an actual theorem-grade route. Computations over small universes validate definitions and tooling, not the general conjecture.

## Completed baseline

WP02 and the first WP04 restricted result now provide checked definitions and local lemmas:

1. support membership is well-defined for finite families;
2. powerset families satisfy the half bound sharply;
3. singleton-containing union-closed families satisfy Frankl for that singleton.
4. a union-closed family containing `{a, b}` satisfies Frankl for at least one of `a` or `b`;
5. independent exact replay finds no nontrivial violations for universes `n <= 4`.

## First concrete next target

Reconstruct Bouchard's lattice-minimal-counterexample conditions in a theorem
spine and nominate the smallest Lean-ready condition as `UC-WP05-L001`. The
ideal-family branch is deferred because a public Lean development already
exists and should be reused through a translation layer if activated.

## Source notes

Useful context sources include:

- Wikipedia overview of the union-closed sets conjecture.
- Stijn Cambie, *Progress on the union-closed conjecture and offsprings in winter 2022-2023*, arXiv:2306.12351.
- Lei Yu, *Dimension-Free Bounds for the Union-Closed Sets Conjecture*, arXiv:2212.00658.
- Jingbo Liu, *Improving the Lower Bound for the Union-closed Sets Conjecture via Conditionally IID Coupling*, arXiv:2306.08824.
- Antoine Bouchard, *Frankl's Union-Closed Conjecture in the Lattice Formulation*, arXiv:2503.00277.
- Masahiro Hachimori and Kenji Kashiwabara, *On the Averaging Problem of Ideal Families*, arXiv:2504.13454.
