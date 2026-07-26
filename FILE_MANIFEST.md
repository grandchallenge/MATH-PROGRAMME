# File Manifest

**Status:** Current governed inventory, edition 2026.07.

This is a curated map of authoritative entry points, not an exhaustive recursive file listing. Exact repository contents remain available through version control. New campaign or publication files do not become authoritative merely by appearing in the tree; authority is established by the domain registry, Agent Council artifact ledger, decision records, claim ledgers, promotion register, schema-bound reviews, executable replay registry, and certification routes.

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
- `docs/CAMPAIGN_PROMOTION_REGISTER.md`
- `docs/decisions/ADR-0001_*.md` through `ADR-0010_*.md`
- `schemas/agent_review.schema.json`
- `templates/agent_review.yaml`
- `reviews/documentation/MKDOCS-COVERAGE.agent_review.yaml`
- `reviews/documentation/DOCUMENTARY-LIBRARY.agent_review.yaml`

## Canonical domains

- `DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md`
- `DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md`
- `DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md`
- `DOMAIN_04_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md`
- `DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md`
- `YM-WP00-source-normalization-equivalence-audit.md`
- `PNP-WP00-source-definition-equivalence-audit.md`
- `RH-WP00-source-normalization-equivalence-audit.md`
- `docs/domains/index.md`
- `docs/domains/union_closed.md`
- `docs/domains/navier_stokes.md`
- `docs/domains/hodge.md`
- `docs/domains/birch_swinnerton_dyer.md`
- `docs/domains/poincare_reconstruction.md`
- `docs/domains/yang_mills.md`
- `docs/domains/p_vs_np.md`
- `docs/domains/riemann_hypothesis.md`

Historical filenames retained under decision control:

- `DOMAIN_03_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md`
- `DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md`

## Campaign stacks

- `campaigns/navier_stokes_critical_integrability/`
- `campaigns/hodge_conjecture/`
- `campaigns/birch_swinnerton_dyer/`
- `campaigns/poincare_reconstruction/`
- `campaigns/p_vs_np/`
- `campaigns/riemann_hypothesis/`
- `reviews/union_closed/`
- `reviews/navier_stokes/`
- `reviews/hodge_conjecture/`
- `reviews/birch_swinnerton_dyer/`
- `reviews/poincare/`
- `reviews/riemann_hypothesis/`

Yang–Mills currently uses its integrated root WP00 dossier as the complete campaign stack entry.

Riemann Hypothesis post-WP00 continuity entry points:

- `RH-WP01-WP02-post-WP00-integration.md`
- `campaigns/riemann_hypothesis/WP01_FALSE_PROOF_ATLAS/`
- `campaigns/riemann_hypothesis/WP02_THEOREM_LEDGER/`
- `campaigns/riemann_hypothesis/RH_WP01_WP02_POST_MERGE_DISPOSITION.md`

RH-WP01 and RH-WP02 are implemented, merged, and CI-passed but not formally promoted while their retained review blockers remain open.

## Documentary Library

- `docs/documentaries/index.md`
- `docs/documentaries/ARTIFACT_MANIFEST.json`
- `docs/documentaries/sources/README.md`
- `docs/documentaries/sources/*.tex` — source records, not complete compilable projects
- `docs/documentaries/documentary_web.schema.json`
- `docs/documentaries/poincare.edition.json`
- `docs/documentaries/poincare.md`
- `docs/documentaries/bsd.md`
- `docs/documentaries/hodge.md`
- `docs/documentaries/navier_stokes.md`
- `docs/documentaries/yang_mills.md`
- `docs/documentaries/p_vs_np.md`
- `docs/documentaries/riemann.md`
- `docs/stylesheets/documentary.css`
- `docs/javascripts/documentary.js`
- `docs/javascripts/documentary-mathjax.js`
- `docs/assets/documentaries/poincare/`
- `schemas/documentary_manifest.schema.json`
- `ci/validate_documentaries.py`
- `ci/test_validate_documentaries.py`

The checksum-locked complete illustrated source bundle is the authoritative documentary source artifact. The checksum-locked PDF is the rendered edition. Current release-class entries are `metadata_only` and do not assert stable public release locators.

## Union-Closed formal and exact baseline

The implementation and bounded replay are maintained in the external [`grandchallenge/MATHCERT`](https://github.com/grandchallenge/MATHCERT) repository rather than under local `MathCert/` or `MATHCERT/` paths.

- `WP01_UNION_CLOSED_STATUS_SPINE.md`
- `WP02_UNION_CLOSED_LEAN_HANDOFF.md`
- `evidence/UC-WP02-MATHCERT.json` — exact external repository, commit, paths, command, and claim boundary
- `schemas/cross_repository_evidence.schema.json`
- external `grandchallenge/MATHCERT/MathCert/Domains/UnionClosed/`
- external `grandchallenge/MATHCERT/certificates/exact/union_closed_n_le_4.json`
- external `grandchallenge/MATHCERT/ci/replay_certificates.py`
- external `grandchallenge/MATHCERT/ci/check_lean.sh`
- `templates/union_closed_claim_ledger_wp01.yaml`

The global programme policy checks out the evidence-pinned MATHCERT commit and executes its complete certification gate. Bounded replay and checked local lemmas do not prove Frankl's conjecture.

## Certified fixtures and publications

- `fixtures/algebraic/UF-INV-001/`
- `fixtures/algebraic/RAD-NIL-002/`
- `fixtures/formal/LOG-GCD-001/`
- `fixtures/formal/PC-WP04/`
- `docs/LOG_GCD_PUBLICATION.md`
- `docs/POINCARE_RECONSTRUCTION_ARCHIVE.md`

## Classification and machine contracts

- `classification/source_registry.json`
- `classification/mappings/union_closed.json`
- `knowledge_graph/union_closed.json`
- `schemas/domain_registry.schema.json`
- `schemas/foundational_profile.schema.json`
- `schemas/claim_ledger.schema.json`
- `schemas/documentary_manifest.schema.json`
- `schemas/campaign_replay_registry.schema.json`
- `schemas/cross_repository_evidence.schema.json`
- `ci/campaign_replay_registry.json`
- `ci/validate_campaign_replays.py`
- `ci/test_campaign_replays.py`
- `ci/validate_rh_continuity.py`
- `ci/test_rh_continuity.py`
- `ci/validate_workflow_coverage.py`
- `ci/test_workflow_coverage.py`
- `ci/validate_programme.py`
- `ci/test_validate_programme.py`
- `ci/validate_docs.py`
- `ci/test_validate_docs.py`
- `ci/validate_documentaries.py`
- `ci/test_validate_documentaries.py`

## Workflow coverage

- `.github/workflows/ci.yml` — global policy on every pull request, every push to `main`, and manual audit; includes all registered campaign replays, LOG-GCD Lean, PC-WP04 Lean, and pinned external MATHCERT replay.
- `.github/workflows/pages.yml` — deploys only the exact `main` commit from a successful push-triggered global policy run.
- `.github/workflows/bsd-wp03-substrate.yml` — path-scoped fast feedback for BSD-WP03.
- `.github/workflows/bsd-wp04-target.yml` — path-scoped fast feedback for BSD-WP04.
- `.github/workflows/pc-wp04.yml` — path-scoped bounded certificate replay.
- `.github/workflows/pc-wp05.yml` — path-scoped archival and bounded-certificate replay.

Workflow inventory, checkout credential handling, job timeouts, policy triggers, deployment gating, replay discovery, and external evidence are machine-checked. A new campaign `replay.py` or `validate*.py` file fails closed until registered.

## Maintenance rule

This manifest is updated when a canonical domain, governance contract, public result, documentary authority, campaign promotion or retained-blocker record, release-class artifact policy, executable replay, workflow role, cross-repository certification dependency, or certification entry point changes. Routine internal files remain discoverable through version control and need not be duplicated here.
