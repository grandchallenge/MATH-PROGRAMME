# MATH-PROGRAMME

> **A Grand Challenge mathematics programme for turning curiosity into checked understanding.**
>
> MATHFORGE imagines. MATHSOLVE disciplines. MATHCERT certifies.

This repository is the public front door for the Grand Challenge mathematics stack. It explains the doctrine, standards, and work-package grammar shared by the three sibling pillars:

| Pillar | Role | Output | Failure it guards against |
| --- | --- | --- | --- |
| **MATHFORGE** | Discovery foundry | Problem cards, source maps, reconnaissance runs, candidate witnesses | Mistaking promising ore for refined metal |
| **MATHSOLVE** | Campaign room | Work Packages, theorem spines, reductions, exact screens, failed-attempt ledgers, handoffs | Mistaking elegant exposition for proof |
| **MATHCERT** | Assay office | Lean/equivalent formalizations, exact certificates, interval/SAT/SMT replay, claim ledgers | Mistaking computation or citation for certification |

```text
     questions                 campaigns                  certificates
        │                         │                            │
        ▼                         ▼                            ▼
  ┌────────────┐            ┌────────────┐              ┌────────────┐
  │ MATHFORGE │  ───────▶  │ MATHSOLVE │  ─────────▶  │ MATHCERT  │
  └────────────┘            └────────────┘              └────────────┘
   conjecture ore            theorem spine                proof boundary
   finite screens            reductions                   replay gates
   source maps               failed routes                checked claims
```

The binding maxim is simple:

> **No theorem without a spine. No computation without a ledger. No conjecture without a map. No proof without a reader.**

## What this programme is

MATH-PROGRAMME is not a claim of solved open problems. It is a disciplined apparatus for making open-problem work legible, cumulative, and auditable.

It exists because serious mathematical progress often happens before a final theorem appears. A good programme clarifies definitions, finds normal forms, records obstructions, builds exact screens, eliminates false corridors, writes readable companions, and prepares claims for formal checking. Those acts are not decorative; they are the infrastructure of understanding.

The programme standard therefore treats three things as coequal:

1. **Insight**: the reader must understand what the object is and where the obstruction lives.
2. **Discipline**: every claim must have a status, support route, and promotion condition.
3. **Certification**: anything called proved must have a checkable boundary.

## Reader paths

Choose a path by purpose.

| Reader | Start here | Then read |
| --- | --- | --- |
| New contributor | `docs/GRAND_CHALLENGE_READER_GUIDE.md` | `ARCHITECTURE_OVERVIEW.md`, then the pillar specs |
| Work-package author | `GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md` | `CLAIM_LEDGER_STANDARD.md`, `docs/PEDAGOGICAL_STYLE_GUIDE.md` |
| Formalization lead | `CERTIFICATION_LADDER.md` | `MATHCERT_SPEC.md`, `WP02_UNION_CLOSED_LEAN_HANDOFF.md` |
| Research strategist | `docs/PROGRAMME_ATLAS.md` | `MATHFORGE_SPEC.md`, `MATHSOLVE_SPEC.md` |
| Skeptical reviewer | `CLAIM_LEDGER_STANDARD.md` | `CERTIFICATION_LADDER.md`, `docs/CLAIM_BOUNDARY_DOCTRINE.md` |

## Core documents

The top-level programme pack contains:

- `ARCHITECTURE_OVERVIEW.md`
- `MATHFORGE_SPEC.md`
- `MATHSOLVE_SPEC.md`
- `MATHCERT_SPEC.md`
- `GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md`
- `THURSTONIAN_ETHOS.md`
- `CLAIM_LEDGER_STANDARD.md`
- `CERTIFICATION_LADDER.md`
- `DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md`
- `WP01_UNION_CLOSED_STATUS_SPINE.md`
- `WP02_UNION_CLOSED_LEAN_HANDOFF.md`

Presentation and pedagogy companions:

- `docs/GRAND_CHALLENGE_READER_GUIDE.md`
- `docs/PROGRAMME_ATLAS.md`
- `docs/PEDAGOGICAL_STYLE_GUIDE.md`
- `docs/CLAIM_BOUNDARY_DOCTRINE.md`
- `docs/CROSS_PILLAR_LANES.md`
- `docs/GLOSSARY.md`

Additional supporting files include schemas, templates, exact finite enumerators, small audit outputs, and Lean scaffolding for the Union-Closed domain.

## How to use this pack

1. Read `docs/GRAND_CHALLENGE_READER_GUIDE.md` for orientation.
2. Read `ARCHITECTURE_OVERVIEW.md` to understand the three-pillar split.
3. Read the three pillar specifications.
4. Use `GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md` for every MATHSOLVE Work Package.
5. Treat `CLAIM_LEDGER_STANDARD.md` as binding. No claim should appear without a type, support route, and promotion condition.
6. Treat `CERTIFICATION_LADDER.md` as the promotion gate from mathematical development to certified result.
7. Read `docs/CROSS_PILLAR_LANES.md` when a recurring tactic, witness, or certificate path spans all three pillars.
8. Begin the first domain with `DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md`, `WP01_UNION_CLOSED_STATUS_SPINE.md`, and `WP02_UNION_CLOSED_LEAN_HANDOFF.md`.

## Claim boundary

This package does not claim new mathematical results. The included Union-Closed enumerator is a small exact sanity audit for universes up to size 4. It is useful infrastructure, not progress on Frankl's conjecture.

A source can motivate a claim. A computation can suggest a claim. A Work Package can organize a claim. But MATHCERT determines whether a claim is checkable.

## The Grand Challenge posture

The desired voice is ambitious, lucid, and exact. It should not sound like marketing. It should not obscure uncertainty. It should not confuse ornament with insight. Decoration is allowed only when it helps the reader see the structure.

A good artifact should leave the reader with four things:

- the object in view;
- the obstruction in focus;
- the claim boundary visible;
- the next move unmistakable.
