# GCL handoff contract

This directory contains durable takeover packages for governed GCL work.

All new substantial handoffs inherit the following live operating controls unless an exact domain-specific instrument materially overrides them:

1. `docs/governance/STREAMLINED_EXECUTION_AMENDMENT.md` (`MP-STREAMLINED-EXECUTION-001`)
2. `docs/governance/SUBSTANCE_FIRST_EXECUTION_DISCIPLINE.md` (`MP-SUBSTANCE-FIRST-EXECUTION-001`)

The handoff exists to preserve continuity of substantive work. It is not an authority source by itself and must not grow into a second control plane.

## Quick access

Canonical control repository: `grandchallenge/MATH-PROGRAMME`.

To start a substantial GCL takeover, copy `grandchallenge/MATH-PROGRAMME:handoffs/CANONICAL_TAKEOVER_PROMPT.md`. Set its `TARGET WORK REPOSITORY` explicitly; do not assume the substantive work lives in `MATH-PROGRAMME`.

To create a new handoff package, start from `grandchallenge/MATH-PROGRAMME:handoffs/_TEMPLATE/README.md` and keep the domain handoff thin.

Do not rewrite the operating doctrine into either artifact.

## Mandatory first executable preflight

Before mutation, a future execution lead must state:

```text
LIVE PROTECTED HEAD
CONTROLLING DOCTRINE REVISIONS
PRIMARY DELIVERABLE
MATERIAL ACCEPTANCE CRITERIA
CURRENT SUBSTANTIVE STATE
SMALLEST SAFE EXECUTABLE TRANCHE
MATERIAL CLOSURE
MINIMUM REQUIRED CONTROL PATH
AFFECTED CHECKS
PROCESS ARTIFACTS PROPOSED
PROCESS NECESSITY TEST: pass / fail
DRIFT TRIPWIRES ACTIVE: none / list
AUTHORITY REQUIRED: delegated / reserved
```

If `PROCESS NECESSITY TEST` is `fail`, do not create the proposed process artifact or step.

If `AUTHORITY REQUIRED` is `reserved`, cite the exact governing rule and material transition. Importance, polish, or generic template language is not evidence of reserved authority.

## Substance-first inheritance

Each handoff must name the primary deliverable and acceptance criteria before describing workflow mechanics.

Supporting governance, CI, provenance, release, synchronization, evidence, and repository work is permitted only when it directly verifies an acceptance criterion, protects an exact material boundary, or removes a demonstrated blocker.

Every continuation must distinguish:

- substantive progress on the primary artifact;
- verification/review progress;
- required governance state;
- incidental process state.

Two consecutive continuations without material primary-artifact advancement trigger mandatory re-planning under `MP-SUBSTANCE-FIRST-EXECUTION-001`.

A failed supporting mechanism does not automatically authorize a larger mechanism. Apply the remediation-recursion rule before expanding tooling or governance.

## Handoff anti-patterns

Do not:

- optimize for the number of commits, gates, evidence records, manifests, archive parts, or workflow runs;
- reproduce historical ceremony that no live material boundary requires;
- use green CI as a proxy for mathematical, scientific, editorial, or product quality outside the checks' actual scope;
- turn repair of supporting machinery into an independent programme unless separately authorized and materially necessary;
- report procedural motion as substantive completion;
- continue a repeatedly fragmenting execution path without re-planning.

Prefer the shortest path that leaves the primary artifact correct, verified to its actual acceptance criteria, and durably preserved under the required authority boundaries.

## Standard structure for new `handoffs/<WORKSET>/README.md`

All new substantial handoffs must use a **thin domain-handoff structure** under this canonical contract.

The domain handoff exists to supply only work-set-specific information. It must not restate or replace the governing doctrine already inherited from:

1. `docs/governance/STREAMLINED_EXECUTION_AMENDMENT.md` (`MP-STREAMLINED-EXECUTION-001`)
2. `docs/governance/SUBSTANCE_FIRST_EXECUTION_DISCIPLINE.md` (`MP-SUBSTANCE-FIRST-EXECUTION-001`)
3. this canonical handoff contract (`handoffs/README.md`)

### Required outline

Each new `handoffs/<WORKSET>/README.md` must contain only the following sections, in this order:

1. `# <WORKSET-ID> — Handoff`
2. `## Purpose`
3. `## Primary deliverable`
4. `## Material acceptance criteria`
5. `## Current substantive state`
6. `## Authoritative pointers`
7. `## Smallest safe next tranche`
8. `## Material dependencies and boundaries`
9. `## Reserved authority / stop conditions`
10. `## Notes intentionally omitted`

### Structural rules

- Keep the file thin and domain-specific.
- Do not duplicate general operating doctrine.
- Do not reproduce historical ceremony unless it remains a live material dependency.
- Do not embed large status logs, replay transcripts, release packets, or procedural archives.
- Put domain intelligence in the handoff; put operating behavior in the canonical contract.
- If a work set requires additional detail, link to authoritative domain artifacts instead of restating them redundantly.

### `Notes intentionally omitted`

Each handoff should close with a short section stating what is *not* included, for example:

- full operating doctrine, inherited from `handoffs/README.md`;
- historical workflow detail no longer required for execution;
- supporting evidence already preserved elsewhere;
- generic GitHub or governance instructions already controlled by live doctrine.

Use `handoffs/_TEMPLATE/README.md` as the starter form for all new substantial handoffs.
