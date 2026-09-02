# GCL GitHub-Native Institutional Truth Spine

## Status

`COMPLETED_PROTECTED_ACTIVATION`

`GCL-TRUTH-SPINE-WP00` completed through PR #194. The protected merge is `50a2d20a21caa20570042a021842580d31d6d2d4`; the protected promotion record became effective when its stated merge/readback condition was satisfied.

The original registry and authority-matrix semantic blobs were deliberately preserved byte-identical from the approved substantive subject. Consequently, candidate-era fields such as `status: CANDIDATE_PENDING_INDEPENDENT_REVIEW` and `effective: false` inside `governance/gcl_truth_spine_registry.json` are historical pre-activation fields of that preserved semantic object, not the current institutional disposition. Current activation is established by the protected promotion/release/review records and protected merge history.

Historical admission evidence includes the approved substantive subject `d2a78b0b25497da192f23045d35869cd483ea15c`, final PR head `c2209148df625859e012bc2bfa330f16c3494f10`, successful Programme policy run `30680478155`, successful GCL conformance run `30680478316`, Human Steward release, delegated Referee review, protected merge, and post-merge activation attestation. Those identities remain provenance; they do not impose the former exact-head approval ceremony on current routine administration.

## Purpose

GCL remains fully operable through Git and the GitHub ecosystem while AETHER develops as a separate semantic-kernel and design-partner programme.

The truth spine standardizes the records that answer four questions:

1. What is the current governed state?
2. Which repository has authority to state it?
3. Which material evidence supports it?
4. How can the state be reconstructed without dashboards, projections, or a future coordination service?

The truth spine is not a new central database. It is a contract over protected, versioned records distributed across the existing repositories.

## Core rule

> Protected normative records define current institutional state. Evidence, reviews, generated reports, and issue mirrors may support or explain that state, but they cannot silently replace it.

## Authority precedence

| Rank | Authority class | May define current state? | Conflict treatment |
|---:|---|:---:|---|
| 1 | Protected normative record | Yes | Fail closed on material ambiguity |
| 2 | Immutable subject-bound evidence | No | Evidence cannot override normative state |
| 3 | Review and decision record | No | Out-of-scope or materially stale review cannot authorize a changed subject |
| 4 | Generated projection or report | No | Regenerate from canonical inputs |
| 5 | Mutable issue or discussion mirror | No | Ignore as authority and repair the mirror |

A workflow run can establish that a check passed for the material object it executed. It cannot by itself change campaign lifecycle. A review can authorize a transition only when protected policy grants that jurisdiction and the reviewed material subject is unchanged. An issue can point to current state; editing the issue cannot create that state.

## Canonical record classes

The protected registry defines eleven record classes:

| Record class | Primary authority | Function |
|---|---|---|
| `campaign_manifest` | MATH-PROGRAMME | Campaign admission, lifecycle, and routing identity |
| `provider_manifest` | MATHFORGE | Source identity, provenance, and source revision |
| `solve_manifest` | MATHSOLVE | Work-package lineage and producer state |
| `cert_route` | MATHCERT | Certification route, adjudication, output, and scope |
| `handoff_packet` | MATHSOLVE | Producer readiness for Cert intake without adjudication authority |
| `claim_ledger` | MATH-PROGRAMME | Programme-level mathematical and external claim status |
| `review_record` | Policy-defined office | Subject-bound office, Council, Referee, and Human dispositions where applicable |
| `promotion_record` | MATH-PROGRAMME | Admission, promotion, rejection, release, and closure |
| `waiver_record` | Programme under reserved authority policy | Typed, expiring exceptions and emergencies |
| `evidence_manifest` | Producing repository | Workflow, certificate, release, and artifact evidence |
| `negative_knowledge_record` | Producing research repository | Failure, obstruction, counterexample, exhaustion, and reopening state |

Each class defines identity fields, permitted producers, consumers, current/historical rules, supersession semantics, review and CI requirements, retention, and a fail-closed disposition.

## Repository jurisdictions

**MATH-PROGRAMME** owns portfolio authority, campaign lifecycle, programme routing, programme-level claim status, promotion, closure, and administrative policy. It does not own source provenance, Solve producer state, or Cert adjudication.

**MATHFORGE** owns source identity, provider provenance, and source revisions. It does not admit campaigns, adjudicate certificates, or promote programme claims.

**MATHSOLVE** owns mathematical work-package lineage, producer evidence, bounded claim production, and handoff readiness. A ready handoff is not a Cert adjudication.

**MATHCERT** owns certification routes, subject intake, adjudication, certificate outputs, and certificate scope. A certificate cannot widen its subject or programme claim.

**INTELLECT** owns its constitutional provider contracts, routing eligibility, consumer projections, and stale-contract rejection. A consumer projection cannot override provider authority.

## Current, historical, and superseded records

A protected record is not current merely because it exists on `main`. Record classes distinguish current, historical, superseded, revoked, terminal, and candidate state where applicable.

Historical records remain historical. A successor preserves lineage and identifies its predecessor. Repository-head movement is not automatically a material authority change. When a consumed artifact and its semantics are unchanged, consumers preserve that material identity rather than perform a ceremonial repin.

## Conflict resolution

When records appear to disagree:

1. identify their record classes;
2. verify repository, path, material blob/digest, schema, and subject identities;
3. determine current, historical, candidate, expired, or superseded state;
4. apply repository jurisdiction and authority precedence;
5. fail closed if a material ambiguity remains;
6. correct protected records rather than resolving the conflict only in issue text.

Generated summaries and trackers are repaired after authority is corrected. They do not rewrite authority retrospectively.

## Evidence and review binding

Promotion-critical evidence identifies the material subject, artifact identity, producer workflow/run where applicable, schema/toolchain identity, and expiry state required by its route.

Reviews bind to their material subject and jurisdiction. A materially changed theorem, source, authority boundary, security control, or external claim requires renewed specialist review where that boundary demands it. Unrelated protected-main movement, byte-identical synchronization, or disjoint campaign activity does not invalidate a review.

Routine bounded administration uses standing delegated authority under `MP-STREAMLINED-EXECUTION-001`; it does not acquire a generic Referee or Human Steward gate.

## GitHub-only operation

Every canonical record and validator must work from a normal source checkout. A live AETHER service is not permitted as a correctness dependency.

The ordinary routine operating path is:

1. read protected records and identify the material closure;
2. validate affected schemas and semantics;
3. verify material identities and retained evidence;
4. obtain specialist review only where the substantive boundary requires it;
5. merge through protected controls under delegated or reserved authority as applicable;
6. read back protected state.

Dashboards or future semantic projections may improve visibility. Their absence must not prevent reconstruction, validation, review, or promotion.

## AETHER boundary

`AETHER-GH-BRIDGE-WP00` remains `ON_HOLD_PENDING_RESOURCE_AVAILABILITY` unless separately changed by its own governed record.

Under the truth spine:

- AETHER has no GCL institutional authority merely by holding a projection;
- AETHER is not required for GCL operation;
- no exclusive institutional fact may exist only in AETHER;
- records should remain suitable for later optional ingestion;
- no bridge implementation is authorized by this doctrine alone.

## Promotion and claim boundary

The truth spine itself is protected and active. That activation is administrative; it does not prove a mathematical target, issue a certificate, establish novelty, priority, or patentability, or authorize mechanical, manufacturing, or commercial claims.
