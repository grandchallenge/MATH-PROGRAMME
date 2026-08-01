# GCL GitHub-Native Institutional Truth Spine

## Status

`CANDIDATE_PENDING_INDEPENDENT_REVIEW`

This document defines the candidate authority model for `GCL-TRUTH-SPINE-WP00`.
It does not become binding merely because it appears on a branch or in a pull
request. Binding adoption requires protected merge, exact-head validation,
non-author Referee review, and Human Steward release.

## Purpose

GCL must remain fully operable through Git and the GitHub ecosystem while
AETHER develops as a separate semantic-kernel and design-partner programme.

The truth spine standardizes the records that answer four questions:

1. What is the current governed state?
2. Which repository has authority to state it?
3. Which exact evidence supports it?
4. How can the state be reconstructed without dashboards, projections, or a
   future coordination service?

The truth spine is not a new central database. It is a contract over protected,
versioned records distributed across the existing repositories.

## Core rule

> Protected normative records define current institutional state. Evidence,
> reviews, generated reports, and issue mirrors may support or explain that
> state, but they cannot silently replace it.

## Authority precedence

| Rank | Authority class | May define current state? | Conflict treatment |
|---:|---|:---:|---|
| 1 | Protected normative record | Yes | Fail closed and escalate |
| 2 | Immutable subject-bound evidence | No | Evidence cannot override normative state |
| 3 | Review and decision record | No | Stale or out-of-scope review fails closed |
| 4 | Generated projection or report | No | Regenerate from canonical inputs |
| 5 | Mutable issue or discussion mirror | No | Ignore as authority and open an administrative defect |

A workflow run can prove that a check passed for an exact commit. It cannot by
itself change campaign lifecycle. A review can authorize a transition only
when protected policy grants that jurisdiction, and only for its exact subject.
An issue can point to current state. Editing the issue cannot create that state.

## Canonical record classes

The registry defines eleven classes:

| Record class | Primary authority | Function |
|---|---|---|
| `campaign_manifest` | MATH-PROGRAMME | Campaign admission, lifecycle, and routing identity |
| `provider_manifest` | MATHFORGE | Source identity, provenance, and source revision |
| `solve_manifest` | MATHSOLVE | Work-package lineage and producer state |
| `cert_route` | MATHCERT | Certification route, adjudication, output, and scope |
| `handoff_packet` | MATHSOLVE | Producer readiness for Cert intake without adjudication authority |
| `claim_ledger` | MATH-PROGRAMME | Programme-level mathematical and external claim status |
| `review_record` | Policy-defined office | Exact-subject office, Council, Referee, and Human dispositions |
| `promotion_record` | MATH-PROGRAMME | Admission, promotion, rejection, release, and closure |
| `waiver_record` | Programme under Human/Council policy | Typed, expiring exceptions and emergencies |
| `evidence_manifest` | Producing repository | Exact-subject workflow, certificate, release, and artifact evidence |
| `negative_knowledge_record` | Producing research repository | Failure, obstruction, counterexample, exhaustion, and reopening state |

Each class defines identity fields, permitted producers, consumers, current and
historical rules, supersession semantics, review and CI requirements,
retention, and a fail-closed disposition.

## Repository jurisdictions

**MATH-PROGRAMME** owns portfolio authority, campaign lifecycle, programme
routing, programme-level claim status, promotion, closure, and administrative
policy. It does not own source provenance, Solve producer state, or Cert
adjudication.

**MATHFORGE** owns source identity, provider provenance, and source revisions.
It does not admit campaigns, adjudicate certificates, or promote programme
claims.

**MATHSOLVE** owns mathematical work-package lineage, producer evidence,
bounded claim production, and handoff readiness. A ready handoff is not a Cert
adjudication.

**MATHCERT** owns certification routes, subject intake, adjudication,
certificate outputs, and certificate scope. A certificate cannot widen its
subject or programme claim.

**INTELLECT** owns its constitutional provider contracts, routing eligibility,
consumer projections, and stale-contract rejection. A consumer projection
cannot override provider authority.

## Current, historical, and superseded records

A protected record is not current merely because it exists on `main`. Every
record class must distinguish current, historical, superseded, revoked,
terminal, and candidate state where applicable.

Historical records remain immutable. A successor must preserve lineage and
identify the prior record. A repository-head change is not automatically a
material authority change. When a consumed artifact blob and its semantics are
unchanged, consumers should preserve the material identity rather than perform
a ceremonial repin.

## Conflict resolution

When records appear to disagree:

1. identify their record classes;
2. verify repository, path, commit, blob, schema, and subject identities;
3. determine current, historical, candidate, expired, or superseded state;
4. apply repository jurisdiction and authority precedence;
5. fail closed if ambiguity remains;
6. correct protected records rather than resolving the conflict in issue text.

Generated summaries and trackers must be repaired after authority is corrected.
They must not rewrite authority retrospectively.

## Evidence and review binding

Promotion-critical evidence should identify its repository, subject commit and
tree, artifact digest, producer workflow/run/attempt, schema version,
qualification identity where applicable, and expiry state.

Reviews must identify exact subject and jurisdiction. A review of one commit
does not transfer automatically to a changed head.

## GitHub-only operation

Every canonical record and validator must work from a normal source checkout.
A live AETHER service is not permitted as a correctness dependency.

The ordinary operating path is:

1. read protected records;
2. validate schemas and semantics locally;
3. verify exact identities and retained evidence;
4. obtain review through pull requests and governed review records;
5. materialize decisions through protected merge.

Dashboards or future semantic projections may improve visibility. Their absence
must not prevent reconstruction, validation, review, or promotion.

## AETHER boundary

`AETHER-GH-BRIDGE-WP00` is
`ON_HOLD_PENDING_RESOURCE_AVAILABILITY`.

Under this package:

- AETHER has no GCL institutional authority;
- AETHER is not required for GCL operation;
- no exclusive institutional fact may exist only in AETHER;
- records should remain suitable for later optional ingestion;
- no bridge implementation is authorized.

AETHER may continue under its own controlled design-partner and release gates.
This boundary does not reject its semantic-kernel thesis.

## Promotion and claim boundary

The registry and matrix remain nonbinding: `effective: false`, Referee review
incomplete, Human release incomplete, and `may_promote_now: false`.

This administrative package does not prove a mathematical target, issue a
certificate, establish novelty, priority, or patentability, or authorize
mechanical, manufacturing, or commercial claims.
