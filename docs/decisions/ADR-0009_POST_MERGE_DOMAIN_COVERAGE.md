# ADR-0009: Close the documentation audit and register governed WP00 campaigns

## Status

Accepted, 2026-07-25.

## Context

PR #87 established public domain coverage and semantic MkDocs validation for Domains 01 through 05. A post-merge audit found four residual inconsistencies:

1. the schema-bound documentation review and artifact ledger still described the repair as merge-pending after PR #87 had merged;
2. `FILE_MANIFEST.md` stopped its ADR range at ADR-0007 although ADR-0008 was canonical;
3. the validator hard-coded the five registered domain IDs and therefore could certify an incomplete catalogue;
4. governed root WP00 dossiers for Yang–Mills, P versus NP, and the Riemann Hypothesis were merged but absent from the registry, public catalogue, and MkDocs navigation.

The third finding is structural. A fixed expected-ID set verifies only that an old list remains unchanged; it does not detect a newly merged governed campaign that never entered the list.

## Decision

1. Register Yang–Mills, P versus NP, and the Riemann Hypothesis as Domains 06, 07, and 08.
2. Use their integrated root WP00 dossiers as the initial canonical entries until a later governed master plan explicitly supersedes them.
3. Add concise public landing pages and MkDocs routes for all three domains.
4. Change documentation coverage validation from a fixed five-ID assertion to a governed-root-campaign discovery check: every root `*-WP00-*.md` source-normalized campaign dossier must appear as a canonical registry entry.
5. Retain contiguous programme-number, unique identity, canonical-entry, public-page, ADR, navigation, claim-boundary, and review-date checks.
6. Close `DOCS-PUBLIC-001` as completed after merge and record the final successful policy run.
7. Correct the ADR inventory and all public five-domain language to the current eight-domain portfolio.
8. Treat this as documentation, governance, temporal-status, and validation maintenance only. No theorem, novelty, certification, or mechanism claim is strengthened.

## Alternatives considered

### Leave the three WP00 dossiers outside the public catalogue

Rejected. They are governed integrated campaign artifacts and their omission recreates the semantic coverage failure that ADR-0008 was intended to prevent.

### Add the domains but keep the fixed expected-ID set

Rejected. This would repair the present list without repairing the failure mode.

### Require a full domain master plan before public registration

Rejected for initial WP00 campaigns. The source-normalized integrated WP00 dossier is a sufficient canonical entry for orientation, provided the landing page states its non-solution boundary and a later master plan may supersede it explicitly.

### Promote mathematical status because repository review and CI passed

Rejected. Merge and CI close documentary promotion conditions only. The underlying Yang–Mills, P versus NP, and Riemann Hypothesis problems remain open.

## Consequences

- The public portfolio contains eight governed domains.
- Future governed root WP00 dossiers cannot silently bypass the domain registry and public navigation.
- `DOCS-PUBLIC-001` no longer carries a stale merge-pending disposition.
- The original three WP00 files remain authoritative campaign dossiers and retain their exact theorem exclusions.
- Domain-specific knowledge graphs and classification mappings remain nonblocking debt.

## Affected artifacts

- `DOMAIN_REGISTRY.yaml`
- `docs/domains/`
- `mkdocs.yml`
- `docs/index.md`
- `docs/SHOWCASE.md`
- `docs/PROGRAMME_ATLAS.md`
- `docs/REPOSITORY_DOCS.md`
- `FILE_MANIFEST.md`
- `ci/validate_docs.py`
- `ci/test_validate_docs.py`
- `reviews/documentation/MKDOCS-COVERAGE.agent_review.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `docs/AGENT_COUNCIL_DECISION_RECORDS.md`
- `YM-WP00-source-normalization-equivalence-audit.md`
- `PNP-WP00-source-definition-equivalence-audit.md`
- `RH-WP00-source-normalization-equivalence-audit.md`

## Review provenance

- Trigger: user-requested full second-pass audit after PR #87.
- Merge evidence: PR #87 merge commit `5de21a98fbfca436a29e83f9fb578c0060f19e14`.
- Final PR-head policy evidence: workflow run 380 on `39de10ddb66ee681612546d3b1ab7010f7ef5863`, all jobs successful.
- Subsequent campaign merges inspected: PR #86, PR #88, and PR #89.

## Supersession

This decision does not supersede ADR-0008. It closes its post-merge state and repairs the campaign-discovery gap in its original validator design.
