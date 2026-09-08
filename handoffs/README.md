# GCL handoff contract

This directory contains durable takeover packages for governed GCL work. It is a continuity and execution surface, not a constitutional authority source and not a second control plane.

## Authority and repository roles

The governing hierarchy is external to this directory and must be resolved before mutation:

1. `grandchallenge/INTELLECT:CONSTITUTION.md` is the supreme constitutional law of the Grand Intellect.
2. Effective INTELLECT amendments and `governance/constitutional_authority_schedule.json` define the live constitutional schedule, staffing model, office obligations, and reserved authority.
3. `grandchallenge/gcl-standards` registers and publishes admitted cross-programme operating standards as a subordinate layer.
4. Each target repository acts only within its delegated domain authority and exact adopted controls.
5. GitHub surfaces provide authoring, review, integration, execution, indexing, publication, and evidence; they do not create constitutional, certification, or production-semantic authority by themselves.

Specific boundaries remain intact:

- `grandchallenge/MATHCERT` alone renders bounded mathematical certification dispositions through accepted routes.
- `grandchallenge/AETHER` owns the production semantic authority assigned by INTELLECT Article IX.
- `grandchallenge/MATH-PROGRAMME` retains mathematics-specific policy, integration, publication, archival, and related delegated authority. Its custody of this handoff contract does not make it the constitutional control repository for GCL.

When authorities appear to conflict, resolve them through the live INTELLECT authority chain and the exact target-domain instrument. A lower-layer handoff, programme rule, repository setting, workflow, or projection may not enlarge its own authority.

Within their compatible delegated scope, handoffs may use these MATH-PROGRAMME execution disciplines:

1. `docs/governance/STREAMLINED_EXECUTION_AMENDMENT.md` (`MP-STREAMLINED-EXECUTION-001`)
2. `docs/governance/SUBSTANCE_FIRST_EXECUTION_DISCIPLINE.md` (`MP-SUBSTANCE-FIRST-EXECUTION-001`)

These disciplines control execution behavior only. They cannot waive INTELLECT phase gates or office obligations, transfer MATH-PROGRAMME authority to another repository, manufacture mathematical independence, alter AETHER semantic authority, or override an exact target-domain boundary.

## Quick access

Constitutional authority repository: `grandchallenge/INTELLECT`.

Handoff contract repository: `grandchallenge/MATH-PROGRAMME`.

To start a substantial GCL takeover, copy `grandchallenge/MATH-PROGRAMME:handoffs/CANONICAL_TAKEOVER_PROMPT.md`. Set its `TARGET WORK REPOSITORY` explicitly; do not assume the substantive work lives in `MATH-PROGRAMME`.

To create a new handoff package, start from `grandchallenge/MATH-PROGRAMME:handoffs/_TEMPLATE/README.md` and keep the domain handoff thin.

Do not rewrite constitutional or operating doctrine into either artifact.

## INTELLECT lifecycle reconciliation

A handoff does not create a lifecycle phase. If the work is an INTELLECT-governed work package, the execution lead must identify the current lawful phase from:

`Charter -> Generation -> Specification -> Realization -> Confrontation -> Judgment -> Integration -> Disposal -> Complete`

The handoff primarily serves continuity and inheritance. It may support work in any phase, but it does not itself advance a phase, declare completion, or replace a required office finding.

The following INTELLECT constraints remain controlling when applicable:

- purpose, scope, claims, evaluation contract, and acceptance criteria are inherited from the governed work package and must not be silently redefined during realization;
- phase transitions must satisfy the substantive conditions and office obligations in the live Constitution and authority schedule;
- reviews bind an exact subject and must record the applicable role, logical pass, mode, criteria, evidence, finding, and residual uncertainty;
- under the live streamlined staffing schedule, one system may staff multiple non-reserved roles through distinct logical passes where allowed;
- an authoring system acting as Adversary or Referee must use `non_authoring_read_only` mode; mutation invalidates that pass;
- Human Steward authority must not be inferred or manufactured; exact reserved powers remain reserved.

## Mandatory first executable preflight

Before mutation, a future execution lead must state:

```text
CONSTITUTIONAL AUTHORITY HEAD
TARGET WORK REPOSITORY
TARGET PROTECTED HEAD
INTELLECT WORK-PACKAGE PHASE: <phase / not applicable>
CONTROLLING DOCTRINE REVISIONS
TARGET DOMAIN AUTHORITY
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

Two consecutive continuations without material primary-artifact advancement trigger mandatory re-planning under `MP-SUBSTANCE-FIRST-EXECUTION-001` where that discipline applies.

A failed supporting mechanism does not automatically authorize a larger mechanism. Apply the remediation-recursion rule before expanding tooling or governance.

## Handoff anti-patterns

Do not:

- optimize for the number of commits, gates, evidence records, manifests, archive parts, or workflow runs;
- reproduce historical ceremony that no live material boundary requires;
- use green CI as a proxy for mathematical, scientific, editorial, or product quality outside the checks' actual scope;
- turn repair of supporting machinery into an independent programme unless separately authorized and materially necessary;
- report procedural motion as substantive completion;
- continue a repeatedly fragmenting execution path without re-planning;
- treat the handoff repository as authority over the target repository merely because it stores the handoff;
- use handoff terminology to create a second lifecycle alongside INTELLECT.

Prefer the shortest path that leaves the primary artifact correct, verified to its actual acceptance criteria, and durably preserved under the required authority boundaries.

## Standard structure for new `handoffs/<WORKSET>/README.md`

All new substantial handoffs using this contract must use a **thin domain-handoff structure**.

The domain handoff exists to supply only work-set-specific information. It must not restate or replace constitutional law, the live authority schedule, target-domain authority, or the governing execution disciplines.

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
- Identify the target work repository explicitly.
- Identify the current INTELLECT work-package phase when applicable; otherwise state `not applicable`.
- Do not duplicate constitutional or general operating doctrine.
- Do not reproduce historical ceremony unless it remains a live material dependency.
- Do not embed large status logs, replay transcripts, release packets, or procedural archives.
- Put domain intelligence in the handoff; keep authority in the authoritative repository that owns it.
- `Authoritative pointers` should link to the live INTELLECT authority surfaces, target-repository controls, and domain instruments that materially govern the work rather than restating their text.
- If a work set requires additional detail, link to authoritative domain artifacts instead of restating them redundantly.
- Location under `grandchallenge/MATH-PROGRAMME:handoffs/` conveys custody and continuity only; it does not transfer jurisdiction.

### `Notes intentionally omitted`

Each handoff should close with a short section stating what is *not* included, for example:

- constitutional law and authority schedules, inherited by reference from INTELLECT;
- general execution doctrine already inherited by reference;
- historical workflow detail no longer required for execution;
- supporting evidence already preserved elsewhere;
- generic GitHub or governance instructions already controlled by live doctrine.

Use `handoffs/_TEMPLATE/README.md` as the starter form for all new substantial handoffs using this contract.
