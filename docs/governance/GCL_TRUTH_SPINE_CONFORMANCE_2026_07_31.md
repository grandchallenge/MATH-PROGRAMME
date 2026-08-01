# GCL Truth Spine Initial Conformance Report

## Status

`CANDIDATE_INVENTORY_FOR_GCL-TRUTH-SPINE-WP00`

Date: 2026-07-31  
Parent programme: MATH-PROGRAMME issue #186  
Work package: MATH-PROGRAMME issue #187

## Purpose

This report maps the existing five-repository umbrella onto the candidate
truth-spine record classes. It is a migration and conformance inventory. It
does not rewrite current authority and does not declare the registry effective.

## Existing strengths

The umbrella already contains substantial parts of the required truth spine:

- protected campaign and routing registries;
- source/provider manifests and provenance controls;
- Solve campaign manifests and producer handoffs;
- Cert routes, adjudications, and bounded certificate outputs;
- exact-head workflow and artifact identity controls;
- protected administrative maintenance and issue-mirror policy;
- claim-boundary doctrine and campaign-specific claim states;
- immutable closure, review, and conformance records.

The candidate registry classifies these jurisdictions. It does not replace the
existing artifacts.

## Initial mapping

| Candidate class | Existing surface | Initial disposition |
|---|---|---|
| `campaign_manifest` | Governed campaign registry and manifests | Existing authority; normalize class metadata only |
| `provider_manifest` | MATHFORGE provider and source records | Existing authority; preserve Forge ownership |
| `solve_manifest` | MATHSOLVE campaign and work-package records | Existing authority; preserve producer scope |
| `cert_route` | MATHCERT route, adjudication, and output records | Existing authority; preserve Cert jurisdiction |
| `handoff_packet` | Solve-to-Cert handoffs | Clarify that readiness is not adjudication |
| `claim_ledger` | Programme ledger and campaign claim fields | Reconcile terminology without local claim widening |
| `review_record` | Council, office, Referee, and Steward records | Define common exact-subject identity minimum |
| `promotion_record` | Admission, promotion, merge, and closure records | Define common predecessor and evidence fields |
| `waiver_record` | Administrative waiver and emergency policy | Add universal instance format without weakening policy |
| `evidence_manifest` | Artifact, workflow, and certificate evidence | Standardize identity fields; retain producer-specific schemas |
| `negative_knowledge_record` | False-proof atlases, blockers, and negative results | Universal durable contract remains work for issue #189 |

## Ambiguities requiring controlled reconciliation

### Claim-state vocabulary

Campaign records use several bounded status vocabularies. They must map to the
programme claim ledger without allowing local records to widen programme state.

### Review identity

Review formats vary. The common minimum must bind reviewer, jurisdiction,
exact subject, disposition, and supersession state without erasing
campaign-specific review content.

### Evidence manifests

The common class should standardize identity and retention fields. It should
not force theorem certificates, source archives, numerical runs, and release
packages into one payload schema.

### Waivers

The maintenance control already defines authority, expiry, prohibited uses,
and review. A common record instance format and location remain to be added.

### Negative knowledge

False-proof atlases and blocker records contain valuable material but do not
yet share one durable index with explicit reopening conditions.

## No-rewrite migration rule

WP00 must not mass-rewrite current records merely to match a new schema. The
first migration stage is additive:

1. register the record class;
2. map existing protected authority;
3. identify missing common fields;
4. add adapters or metadata only where evidence shows value;
5. preserve old identities and history;
6. require explicit supersession for normative replacement.

## Fail-closed findings

The candidate validator rejects:

- missing or duplicate canonical record classes;
- a missing member of the five-repository matrix;
- issue mirrors allowed to define current state;
- consumer projections allowed to override providers;
- unknown record-class references;
- absent historical or supersession semantics;
- non-fail-closed dispositions;
- AETHER made a required dependency;
- AETHER-exclusive institutional facts;
- premature promotion or claim authorization.

## Deferred work

- reusable work-package tooling: issue #188;
- negative-knowledge implementation: issue #189;
- portfolio ledger: issue #190;
- cross-programme synthesis: issue #191;
- assurance product lane: issue #192;
- AETHER pilot: `fyremael/AETHER#51`;
- disclosure and IP gates: issue #193;
- AETHER-GitHub bridge: on hold pending resource availability.

## Candidate disposition

The package is suitable for exact-head validation and independent review. It is
not yet suitable for binding institutional promotion.

No mathematical, certification, novelty, priority, patentability, mechanical,
manufacturing, or commercial claim is promoted.
