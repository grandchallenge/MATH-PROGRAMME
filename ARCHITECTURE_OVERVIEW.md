# Architecture Overview

## The missing middle

The earlier two-part split, MATHFORGE plus MATHCERT, was logically clean but structurally incomplete. It separated exploration from certification, yet omitted the long middle process where Grand Challenge work actually happens. The Chaidez-style Work Packages did not merely discover problems or certify final theorems. They built mathematical campaigns: normal forms, restricted theorem targets, proof attempts, compact residual reductions, exact screens, interval scaffolds, failure ledgers, and plain-language companions.

That middle is now named **MATHSOLVE**.

```text
MATHFORGE  ->  MATHSOLVE  ->  MATHCERT
discover       attack         certify
```

A more faithful picture is:

```text
raw mathematical signal
  -> reconstructed source context
  -> problem card
  -> status spine
  -> theorem spine
  -> work-package campaign
  -> claim ledger
  -> certification handoff
  -> checked artifact or rejected claim
```

The architecture exists to prevent each stage from pretending to be the next one.

## Three-pillar doctrine

### MATHFORGE

MATHFORGE is the exploratory foundry. It ingests open-problem corpora, source papers, surveys, repository data, examples, counterexamples, computational searches, and speculative conjectures. Its output is not mathematical authority. Its output is candidate ore.

Its governing question is:

> What is worth carrying into a disciplined campaign?

### MATHSOLVE

MATHSOLVE is the campaign room. It turns promising ore into disciplined mathematical form: status spines, theorem candidates, reductions, exact computations, Work Packages, failed attempts, lay explanations, and certification handoffs. MATHSOLVE is allowed to be incomplete, but it must be honest.

Its governing question is:

> What exact mathematical obligation have we clarified?

### MATHCERT

MATHCERT is the assay office. It checks, rejects, certifies, or records the exact status of claims. It is Lean-first but not Lean-only. It also admits exact rational computation, interval arithmetic, SAT/SMT proof artifacts, theorem prover alternatives, and independently replayable certificate ledgers.

Its governing question is:

> What has crossed a trusted proof or replay boundary?

## The promotion path

```text
Candidate problem card
  -> Status audit
  -> Work Package 01: problem spine
  -> Work Package 02: definitions and reductions
  -> Work Package 03+: restricted results, exact screens, failure analysis
  -> MATHCERT handoff
  -> formal statement / checked lemma / exact certificate / interval certificate
  -> public claim
```

No artifact is promoted merely because it sounds mathematical. Promotion requires a claim type, support type, source trail, and certification route.

## Why three pillars instead of one repo

The three functions have different failure modes.

- MATHFORGE fails by hallucinating promise, over-selecting fashionable problems, or producing noisy conjectures.
- MATHSOLVE fails by writing impressive prose without theorem-grade obligations, hiding dead ends, or confusing evidence with proof.
- MATHCERT fails by becoming a technical shrine disconnected from mathematical understanding, or by formalizing statements that nobody has explained.

Separating the pillars allows each to check the others.

## Cross-pillar lanes

Some workflows cut across all three pillars. These are called lanes. A lane is a reusable route from discovery to tactic to certification.

The first explicit lane is the algebraic witness-to-certificate route:

```text
MATHFORGE: external CAS or exact symbolic search emits a witness
MATHSOLVE: recognizes the algebraic subproblem and routes the tactic
MATHCERT: replays or Lean-checks the certificate before promotion
```

The lane doctrine lives in `docs/CROSS_PILLAR_LANES.md`.

## Classification and discovery layer

The three-pillar workflow shares a fourth, programme-owned information layer:

```text
MSC2020-SKOS          -> versioned subject mappings
external discovery    -> reviewed evidence records
internal graph        -> programme concepts, relations, and state
```

MSC2020-SKOS is the stable classification spine. It does not define mathematical
dependencies or programme meaning. Those belong to the versioned internal
knowledge graph.

MATHFORGE queries zbMATH Open for mathematics-specific literature, OpenAlex for
semantic and citation discovery, and arXiv for current-awareness intake. Results
remain discovery evidence until a human review promotes a normalized record into
an audited mapping or graph assertion. OntoMathPRO may inform graph design but is
not a runtime or governance dependency.

## Naming note

MATHSMELT remains a useful internal term for the refinement phase inside MATHSOLVE, but it is not the public pillar. MATHSOLVE is clearer and more institutional. It does not mean that the system magically solves mathematics. It means the system organizes the struggle.

## Binding maxim

> No theorem without a spine. No computation without a ledger. No conjecture without a map. No proof without a reader.
