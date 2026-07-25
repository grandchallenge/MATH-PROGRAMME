# Programme Status Taxonomy

<p class="page-deck">Three vocabularies govern different objects. They may be compared, but they must not be collapsed.</p>

## Claim and support status

This vocabulary applies to mathematical statements and the support routes attached to them.

| Level | Meaning | Permitted reliance |
|---|---|---|
| Lead | A direction worth reconstructing | Exploration only |
| Heuristic | An organizing intuition | Cautious reasoning, not theorem reliance |
| Exact evidence | A finite or computational fact under stated assumptions | Reliance on the bounded fact only |
| Proved locally | A theorem inside an explicit dependency boundary | Reliance within that boundary |
| Certification-ready | A precise statement with dependencies and replay route | Audit of the handoff |
| Certified | A checked proof or independently replayed certificate | Reliance on the declared checked statement |
| Rejected or superseded | A claim or route that failed, drifted, or was replaced | Historical and adversarial use only |

The compact labels used on visual entry pages—conjectural, computed, provisional, certified, and rejected—are reader-facing summaries. This table and the [Claim Boundary Doctrine](CLAIM_BOUNDARY_DOCTRINE.md) govern their interpretation.

## Artifact lifecycle status

This vocabulary applies to governed documents and artifacts, not directly to theorem truth.

`draft`, `active`, `blocked`, `ready_for_next_stage`, `ready_for_certification`, `certified`, `completed`, `selected`, `published`, `archived`

An artifact may be `completed` while its target conjecture remains open. A publication may be `published` while explicitly making no novelty claim.

## Campaign disposition

Disposition is a human-readable campaign qualification, such as:

- `referee_promoted_conditional`;
- `selected_unproved`;
- `qualified solved-problem archive`;
- `WP02/MATHCERT handoff discharged`.

Disposition records why or how an artifact occupies its lifecycle state. It does not create a new machine lifecycle token and does not strengthen the mathematical claim.

## Programme structure

The programme has three mathematical execution pillars:

`MATHFORGE -> MATHSOLVE -> MATHCERT`

`MATH-PROGRAMME` is the governance, integration, publication, and archival layer. It is represented as a schema pillar where those artifacts require a named owner, but it is not a fourth mathematical proof stage.

## Reading rule

Before relying on a status word, ask:

1. Does it describe a mathematical claim, an artifact lifecycle, or a campaign disposition?
2. Which support route or review record governs it?
3. What nearby stronger statement is explicitly excluded?