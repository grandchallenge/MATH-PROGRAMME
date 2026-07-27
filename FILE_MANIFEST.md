# File Manifest

**Status:** Current governed inventory, edition 2026.07.

This is a curated map of authoritative entry points, not an exhaustive recursive listing. Files become authoritative through the domain registry, artifact ledger, decisions, claim and promotion records, schema-bound reviews, governed execution routes, and certification controls—not merely by appearing in the tree.

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
- `reviews/documentation/MKDOCS-COVERAGE.agent_review.yaml`
- `reviews/documentation/DOCUMENTARY-LIBRARY.agent_review.yaml`
- `reviews/governance/WORKFLOW-COVERAGE.agent_review.yaml`
- `reviews/navier_stokes/NS-CI-WP06.agent_review.yaml`

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

The historical BSD Domain 03 filename remains under decision control. The mislabelled Poincaré Domain 04 filename was removed in PR #96; Domain 05 is canonical and its frozen provenance is governed by `reviews/poincare/HISTORICAL_IDENTITY_CROSSWALK.yaml`.

## Campaign stacks

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

NS-CI-WP06 is a non-blocking, non-probative computability lane. Its literature, risk, obligation, and bounded fixture artifacts do not alter the WP01/WP02 analytic mainline or any WP00–WP05 result state.

Yang–Mills currently uses its integrated root WP00 dossier as the complete campaign stack entry.

Riemann Hypothesis post-WP00 continuity entries remain implemented and CI-passed but formally unpromoted while retained blockers remain open.

## Repository tests and bounded experiments

- `tests/test_ns_wp06_halting_gate_fixture.py`
- `experiments/__init__.py`
- `experiments/ns_wp06_undec/__init__.py`
- `experiments/ns_wp06_undec/halting_gate_fixture.py`
- `ci/validate_repository_execution.py`
- `ci/test_repository_execution.py`

Experiment modules are library-only and must be reachable from discovered standard-library unit tests. Passing tests establish bounded software behaviour only.

## Documentary Library

- `docs/documentaries/index.md`
- `docs/documentaries/ARTIFACT_MANIFEST.json`
- `docs/documentaries/sources/README.md`
- `docs/documentaries/sources/*.tex`
- `docs/documentaries/documentary_web.schema.json`
- `docs/documentaries/poincare.edition.json`
- `docs/documentaries/*.md`
- `docs/stylesheets/documentary.css`
- `docs/javascripts/documentary.js`
- `docs/javascripts/documentary-mathjax.js`
- `docs/assets/documentaries/poincare/`
- `schemas/documentary_manifest.schema.json`
- `ci/validate_documentaries.py`
- `ci/test_validate_documentaries.py`

The complete illustrated source bundle is the authoritative documentary source artifact; the checksum-locked PDF is the rendered edition. Current release-class entries are `metadata_only` and do not assert stable public locators.

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
