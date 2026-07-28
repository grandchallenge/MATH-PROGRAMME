# File Manifest

**Status:** Current governed inventory, edition 2026.07.

This is a curated map of authoritative entry points, not an exhaustive recursive listing. Files become authoritative through the domain registry, artifact ledger, decisions, canonical claim-ledger and review registries, promotion records, governed execution routes, documentary discovery authorities, and certification controls—not merely by appearing in the tree.

## Programme architecture

- `README.md`
- `ARCHITECTURE_OVERVIEW.md`
- `MATHFORGE_SPEC.md`
- `MATHSOLVE_SPEC.md`
- `MATHCERT_SPEC.md`
- `PROGRAMME_CHARTER.md` through `docs/PROGRAMME_CHARTER.md`
- `DOMAIN_REGISTRY.yaml`
- `mkdocs.yml`

## Governing standards

- `GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md`
- `GRAND_CHALLENGE_PEDAGOGY_STANDARD.md`
- `docs/GRAND_CHALLENGE_PEDAGOGY_STANDARD.md`
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
- `docs/decisions/ADR-0001_*.md` through `ADR-0014_*.md`
- `schemas/agent_review.schema.json`
- `templates/agent_review.yaml`
- `reviews/union_closed/UC-WP01.agent_review.yaml`
- `reviews/union_closed/UC-DOC-WP00.agent_review.yaml`
- `reviews/documentation/MKDOCS-COVERAGE.agent_review.yaml`
- `reviews/documentation/DOCUMENTARY-LIBRARY.agent_review.yaml`
- `reviews/governance/WORKFLOW-COVERAGE.agent_review.yaml`
- `reviews/navier_stokes/NS-CI-WP06.agent_review.yaml`

The programme validator maintains an explicit schema-bound review registry and adversarially discovers schema-valid records under governed review roots. A discovered review omitted from the registry and a registered review missing from the repository both fail policy.

## Canonical claim ledgers

- `CLAIM_LEDGER_STANDARD.md`
- `schemas/claim_ledger.schema.json`
- `templates/claim_ledger_template.yaml`
- `templates/union_closed_claim_ledger_wp01.yaml`
- `campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK/10_CLAIM_LEDGER.yaml`

Canonical ledgers carry `ledger_contract: canonical_claim_ledger`, conform to schema version 1.1.0, and are explicitly registered. Discovery and registration are bidirectional; legacy claim lists remain historical evidence until migrated.

## Canonical domains

- `DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md`
- `DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md`
- `DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md`
- `DOMAIN_04_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md`
- `DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md`
- `YM-WP00-source-normalization-equivalence-audit.md`
- `PNP-WP00-source-definition-equivalence-audit.md`
- `RH-WP00-source-normalization-equivalence-audit.md`
- `docs/domains/`

The historical BSD Domain 03 filename remains under decision control. The mislabelled `DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md` was removed in PR #96; `DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md` is canonical and frozen provenance is governed by `reviews/poincare/HISTORICAL_IDENTITY_CROSSWALK.yaml`.

## Campaign stacks

- `campaigns/union_closed/`
- `campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK/`
- `campaigns/navier_stokes_critical_integrability/`
- `campaigns/navier_stokes_critical_integrability/WP06_UNDECIDABILITY_REDUCTION_LANE/`
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

UC-DOC-WP00 is a completed documentary source lock. Its candidate metadata are public, its source pointer remains repository-only, and its page, edition record, assets, public source record, navigation, and manifest admission remain deferred to one atomic UC-DOC-WP01 change.

NS-CI-WP06 is a non-blocking, non-probative computability lane. Its literature, risk, obligation, and bounded fixture artifacts do not alter the WP01/WP02 analytic mainline or any WP00–WP05 result state.

Yang–Mills currently uses its integrated root WP00 dossier as the complete campaign stack entry.

Riemann Hypothesis post-WP00 continuity entries remain implemented and CI-passed but formally unpromoted while retained blockers remain open.

## Repository tests and bounded experiments

- `tests/test_ns_wp06_halting_gate_fixture.py`
- `tests/test_documentary_web_editions.py`
- `tests/test_documentary_wave_one.py`
- `tests/test_uc_doc_source_lock.py`
- `experiments/__init__.py`
- `experiments/ns_wp06_undec/__init__.py`
- `experiments/ns_wp06_undec/halting_gate_fixture.py`
- `ci/validate_repository_execution.py`
- `ci/test_repository_execution.py`

Experiment modules are library-only and must be reachable from discovered standard-library unit tests. Passing tests establish bounded software behaviour only. Documentary repository tests retain problem-specific mathematical spines; shared discovery, authority, accessibility, release, plate, section, rendering, candidate, and orphan invariants belong to `ci/validate_documentaries.py`.

## Documentary Library

- `docs/documentaries/index.md`
- `docs/documentaries/ARTIFACT_MANIFEST.json` — sole machine discovery authority for admitted public editions
- `docs/documentaries/DOCUMENTARY_CANDIDATES.json` — public metadata authority for pre-admission source locks
- `docs/documentaries/sources/README.md`
- `docs/documentaries/sources/*.tex` — admitted public source records only
- `docs/documentaries/documentary_web.schema.json`
- `docs/documentaries/*.edition.json`
- admitted documentary `docs/documentaries/*.md`
- `docs/stylesheets/documentary.css`
- `docs/stylesheets/documentary-status.css`
- `docs/javascripts/documentary.js`
- `docs/javascripts/documentary-mathjax.js`
- `docs/assets/documentaries/poincare/`
- `docs/assets/documentaries/bsd/`
- `docs/assets/documentaries/hodge/`
- `docs/assets/documentaries/navier_stokes/`
- `docs/assets/documentaries/yang_mills/`
- `docs/assets/documentaries/p_vs_np/`
- `docs/assets/documentaries/riemann/`
- `schemas/documentary_manifest.schema.json`
- `schemas/documentary_candidate_registry.schema.json`
- `ci/validate_documentaries.py`
- `ci/test_validate_documentaries.py`
- `tests/test_documentary_web_editions.py`
- `tests/test_documentary_wave_one.py`
- `tests/test_uc_doc_source_lock.py`

The manifest names every admitted source record, web page, edition record, claim authority, scope relation, documentary tier, machine claim status, problem class, and display status. The candidate registry records source-locked but unadmitted projects without conferring collection membership. Candidate source pointers remain under their governing campaign and outside `docs/` until atomic admission.

The complete illustrated source bundle is the authoritative documentary source artifact; the checksum-locked PDF is the rendered edition. Current release-class entries and candidates are `metadata_only` and do not assert stable public locators.

The tier vocabulary is expository rather than mathematical: Poincaré is the reference tier, BSD is the full tier, and Hodge, Navier–Stokes, Yang–Mills, P versus NP, and Riemann are orientation tier.

## Union-Closed formal and exact baseline

The implementation and bounded replay are maintained in external `grandchallenge/MATHCERT` rather than local `MathCert/` or `MATHCERT/` paths.

- `WP01_UNION_CLOSED_STATUS_SPINE.md`
- `WP02_UNION_CLOSED_LEAN_HANDOFF.md`
- `evidence/UC-WP02-MATHCERT.json`
- `schemas/cross_repository_evidence.schema.json`
- external `grandchallenge/MATHCERT/MathCert/Domains/UnionClosed/`
- external `grandchallenge/MATHCERT/certificates/exact/union_closed_n_le_4.json`
- external `grandchallenge/MATHCERT/ci/check_lean.sh`

The global policy checks out the evidence-pinned commit and runs the complete gate. Bounded replay and checked local lemmas do not prove Frankl's conjecture.

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
- `schemas/documentary_candidate_registry.schema.json`
- `schemas/campaign_replay_registry.schema.json`
- `schemas/cross_repository_evidence.schema.json`
- `requirements/policy.txt`
- `requirements/docs.txt`
- `ci/campaign_replay_registry.json`
- `ci/validate_campaign_replays.py`
- `ci/test_campaign_replays.py`
- `ci/validate_policy_reachability.py`
- `ci/test_policy_reachability.py`
- `ci/validate_repository_execution.py`
- `ci/test_repository_execution.py`
- `ci/validate_workflow_semantics.py`
- `ci/test_workflow_semantics.py`
- `ci/validate_workflow_coverage.py`
- `ci/test_workflow_coverage.py`
- `ci/validate_rh_continuity.py`
- `ci/test_rh_continuity.py`
- `ci/validate_retired_paths.py`
- `ci/test_retired_paths.py`
- `ci/validate_programme.py`
- `ci/test_validate_programme.py`
- `ci/validate_docs.py`
- `ci/test_validate_docs.py`
- `ci/validate_documentaries.py`
- `ci/test_validate_documentaries.py`

## Workflow coverage

- `.github/workflows/ci.yml` — global policy, repository tests, strict site producer, formal gates, external evidence, and continuity controls.
- `.github/workflows/pages.yml` — retrieves and verifies the exact run-scoped `validated-site` artifact, refuses stale `main`, and deploys without rebuilding.
- `.github/workflows/bsd-wp03-substrate.yml` — BSD-WP03 fast feedback.
- `.github/workflows/bsd-wp04-target.yml` — BSD-WP04 fast feedback.
- `.github/workflows/pc-wp04.yml` — bounded certificate replay.
- `.github/workflows/pc-wp05.yml` — archival and bounded-certificate replay.

Workflow identity, permissions, immutable actions, environment declarations, executable reachability, repository tests, experiment imports, exact workflow-artifact and inner archive digests, external evidence, and current-tip deployment are machine-checked. Exact top-level pins remain short of a complete transitive hash lock.
