# Programme Atlas

## The landscape

MATH-PROGRAMME is a map of mathematical work as a sequence of transformations.

```text
raw question
  -> source-reconstructed problem
  -> status-audited problem card
  -> theorem spine
  -> Work Package sequence
  -> exact computation or proof attempt
  -> claim ledger
  -> certification handoff
  -> checked artifact or rejected claim
```

Each transformation changes the status of the material. The programme exists to make those status changes explicit.

## Three rooms

### The foundry: MATHFORGE

The foundry is noisy by design. It collects ore: problems, examples, failures, small computations, apparent patterns, source trails, and first formulations.

MATHFORGE is allowed to be generative. It is not allowed to be authoritative.

### The campaign room: MATHSOLVE

The campaign room turns ore into mathematical obligations. It builds definitions, normal forms, reductions, diagrams, Work Packages, exact screens, failed-attempt ledgers, and next-target statements.

MATHSOLVE is allowed to be incomplete. It is not allowed to be vague.

### The assay office: MATHCERT

The assay office checks claims against a proof boundary. It accepts Lean/equivalent formalization, exact replay, interval certificates, SAT/SMT artifacts, and other auditable proof-producing routes.

MATHCERT is allowed to reject. It is not allowed to be impressed.

## Artifact ladder

| Stage | Artifact | Owner | Promotion condition |
| --- | --- | --- | --- |
| Curiosity | Lead note | MATHFORGE | Source can be reconstructed |
| Candidate | Problem card | MATHFORGE | Status and risks recorded |
| Campaign | Work Package | MATHSOLVE | Claim ledger and next target present |
| Local result | Lemma/proposition/screen | MATHSOLVE | Support route identified |
| Handoff | Certification packet | MATHSOLVE + MATHCERT | Formal statement and dependencies clear |
| Certification | Checked artifact | MATHCERT | Proof/replay passes the gate |
| Publication | Public claim | Programme | Claim boundary visible to reader |

## First domain: Union-Closed Sets

The first domain is intentionally modest. The programme does not begin by claiming progress on Frankl's conjecture. It begins by building reusable infrastructure:

- definitions;
- small exact enumerations;
- status spines;
- Lean-friendly statements;
- local lemmas;
- claim ledgers;
- certification handoffs.

This establishes the method before attempting ambitious theorem production.

## Cross-pillar obligations

MATHFORGE must give MATHSOLVE enough context to avoid attacking a mirage.

MATHSOLVE must give MATHCERT claims precise enough to check or reject.

MATHCERT must give MATHFORGE and MATHSOLVE feedback about missing definitions, unsupported assumptions, and proof gaps.

The system improves when each pillar makes the others harder to fool.
