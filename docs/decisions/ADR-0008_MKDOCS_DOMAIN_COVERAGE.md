# ADR-0008: Govern MkDocs domain coverage and public authority

## Status

Accepted, 2026-07-24.

## Context

The public MkDocs site remained mechanically valid while its information architecture lagged behind the governed repository. It presented Union-Closed Sets as the only current demonstration domain, exposed active campaigns mainly through decision records, retained a stale June integration audit as if it were current doctrine, linked two materially different pedagogy standards, and used claim, lifecycle, and campaign-disposition vocabularies without an explicit mapping.

A successful documentation build could not detect these semantic omissions because every configured page existed and every link was syntactically valid.

## Decision

1. Treat `DOMAIN_REGISTRY.yaml` as the canonical machine-readable catalogue of programme domains.
2. Require every canonical domain to record a stable programme number, campaign ID, canonical repository entry, public MkDocs page, governance references, claim boundary, foundational profile, and next review date.
3. Require every canonical domain to have one concise public landing page under `docs/domains/` and one entry in the MkDocs Domains navigation.
4. Preserve theorem-level authority in master plans, Work Packages, claim ledgers, proof artifacts, source records, reviews, and certification routes. Public landing pages remain orientation artifacts.
5. Separate claim/support status, artifact lifecycle, and campaign disposition in public documentation through `docs/STATUS_TAXONOMY.md`.
6. Describe MATHFORGE, MATHSOLVE, and MATHCERT as the three mathematical execution pillars, with MATH-PROGRAMME as the governance, integration, publication, and archival layer rather than a fourth proof stage.
7. Replace duplicate root-level doctrine bodies with canonical pointers when a rendered `docs/` artifact is authoritative.
8. Preserve dated audits as historical records with explicit snapshot notices and current dispositions.
9. Make documentation coverage enforceable in `ci/validate_docs.py`, including domain-page presence, canonical-entry resolution, ADR resolution, navigation coverage, authority pointers, edition agreement, and historical notices.
10. Maintain `FILE_MANIFEST.md` as a curated governed inventory rather than a stale exhaustive listing.

## Alternatives considered

### Keep the public site intentionally minimal

Rejected. A minimal front door is useful only when it accurately routes readers to the current governed portfolio. Omitting active domains while displaying their ADRs creates a misleading information hierarchy.

### Copy complete campaign dossiers into `docs/`

Rejected. This would duplicate theorem-level authority, increase drift, and blur the distinction between public orientation and canonical research artifacts.

### Rely on strict MkDocs builds alone

Rejected. Build validity detects missing files and malformed links, not stale claims, absent domains, competing standards, or status-taxonomy drift.

### Generate all pages automatically from the registry

Deferred. The registry now supplies enforceable identity and coverage fields, but domain landing pages remain deliberately edited for claim-boundary clarity and pedagogy. Generation may be reconsidered when the domain schema stabilizes further.

## Consequences

- Domains 01–05 receive public landing pages and a shared catalogue.
- The MkDocs navigation is reorganized around Programme, Domains, Governance, Doctrine, Routes, Results, Intake, Reference, and History.
- Public entry pages no longer describe Union-Closed as the only current domain.
- The root pedagogy standard becomes a compatibility pointer to the canonical rendered standard.
- The June integration audit remains available without presenting superseded findings as current.
- Documentation CI rejects future canonical domains that lack public coverage or authoritative links.
- This decision changes documentation and governance only. It makes no mathematical, novelty, certification, or theorem-strengthening claim.

## Affected artifacts

- `DOMAIN_REGISTRY.yaml`
- `schemas/domain_registry.schema.json`
- `mkdocs.yml`
- `docs/index.md`
- `docs/SHOWCASE.md`
- `docs/PROGRAMME_ATLAS.md`
- `docs/GRAND_CHALLENGE_READER_GUIDE.md`
- `docs/CLAIM_BOUNDARY_DOCTRINE.md`
- `docs/STATUS_TAXONOMY.md`
- `docs/domains/`
- `docs/REPOSITORY_DOCS.md`
- `docs/GLOSSARY.md`
- `docs/INTEGRATION_AUDIT_2026_06_21.md`
- `GRAND_CHALLENGE_PEDAGOGY_STANDARD.md`
- `FILE_MANIFEST.md`
- `ci/validate_docs.py`
- `ci/test_validate_docs.py`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`

## Review provenance

- Trigger: post-merge MkDocs consistency and coverage audit, 2026-07-24.
- Governing review offices: Cartographer, Steward, Grammarian, Amanuensis, Adversary, and Referee.
- Validation route: schema parsing, documentation contract tests, strict MkDocs build, navigation coverage, and branch-to-main comparison.

## Supersession

This decision does not supersede ADR-0001 through ADR-0007. It extends ADR-0007's cross-document consistency and lifecycle normalization into the public documentation and domain-coverage layer.