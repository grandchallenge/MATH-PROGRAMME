# File Manifest

**Status:** Current governed inventory, edition 2026.07.

This is a curated map of authoritative entry points, not an exhaustive recursive file listing. Exact repository contents remain available through version control. New campaign files do not become authoritative merely by appearing in the tree; authority is established by the domain registry, Agent Council artifact ledger, decision records, claim ledgers, and certification routes.

## Programme architecture

- `README.md`
- `ARCHITECTURE_OVERVIEW.md`
- `MATHFORGE_SPEC.md`
- `MATHSOLVE_SPEC.md`
- `MATHCERT_SPEC.md`
- `PROGRAMME_CHARTER.md` through the rendered `docs/PROGRAMME_CHARTER.md`
- `DOMAIN_REGISTRY.yaml`
- `mkdocs.yml`

## Governing standards

- `GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md`
- `GRAND_CHALLENGE_PEDAGOGY_STANDARD.md` — compatibility pointer
- `docs/GRAND_CHALLENGE_PEDAGOGY_STANDARD.md` — canonical pedagogy standard
- `CLAIM_LEDGER_STANDARD.md`
- `CERTIFICATION_LADDER.md`
- `CLASSIFICATION_DISCOVERY_STANDARD.md`
- `HANDOFF_STANDARD.md`
- `GOVERNANCE.md`
- `THURSTONIAN_ETHOS.md`

## Agent Council and continuity

- `docs/MATH_PROGRAMME_AGENT_COUNCIL.md`
- `docs/AGENT_COUNCIL_GOVERNANCE.md`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `docs/AGENT_COUNCIL_DECISION_RECORDS.md`
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`
- `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`
- `docs/decisions/ADR-0001_*.md` through `ADR-0007_*.md`
- `schemas/agent_review.schema.json`
- `templates/agent_review.yaml`

## Canonical domains

- `DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md`
- `DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md`
- `DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md`
- `DOMAIN_04_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md`
- `DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md`
- `docs/domains/index.md`
- `docs/domains/union_closed.md`
- `docs/domains/navier_stokes.md`
- `docs/domains/hodge.md`
- `docs/domains/birch_swinnerton_dyer.md`
- `docs/domains/poincare_reconstruction.md`

Historical filenames retained under decision control:

- `DOMAIN_03_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md`
- `DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md`

## Campaign stacks

- `campaigns/navier_stokes_critical_integrability/`
- `campaigns/hodge_conjecture/`
- `campaigns/birch_swinnerton_dyer/`
- `campaigns/poincare_reconstruction/`
- `reviews/union_closed/`
- `reviews/navier_stokes/`
- `reviews/hodge_conjecture/`
- `reviews/birch_swinnerton_dyer/`
- `reviews/poincare/`

## Union-Closed formal and exact baseline

- `WP01_UNION_CLOSED_STATUS_SPINE.md`
- `WP02_UNION_CLOSED_LEAN_HANDOFF.md`
- `MathCert/Domains/UnionClosed/`
- `MATHCERT/ci/replay_certificates.py`
- `templates/union_closed_claim_ledger_wp01.yaml`

## Certified fixtures and publications

- `fixtures/algebraic/UF-INV-001/`
- `fixtures/algebraic/RAD-NIL-002/`
- `fixtures/formal/LOG-GCD-001/`
- `docs/LOG_GCD_PUBLICATION.md`
- `docs/POINCARE_RECONSTRUCTION_ARCHIVE.md`

## Classification and machine contracts

- `classification/source_registry.json`
- `classification/mappings/union_closed.json`
- `knowledge_graph/union_closed.json`
- `schemas/domain_registry.schema.json`
- `schemas/foundational_profile.schema.json`
- `schemas/claim_ledger.schema.json`
- `ci/validate_programme.py`
- `ci/test_validate_programme.py`
- `ci/validate_docs.py`
- `ci/test_validate_docs.py`

## Maintenance rule

This manifest is updated when a canonical domain, governance contract, public result, or certification entry point changes. Routine internal files remain discoverable through the repository tree and need not be duplicated here.