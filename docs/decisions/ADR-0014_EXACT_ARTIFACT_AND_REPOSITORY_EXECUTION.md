# ADR-0014: Bind publication to the exact policy artifact and govern repository tests

## Status

Accepted, 2026-07-26.

## Context

ADR-0011 and ADR-0012 established repository-wide policy authority, self-authenticating workflow discovery, declared environments, and current-tip publication. A third pass found two residual consistency gaps:

1. the Pages workflow rebuilt the site after policy success instead of deploying the exact site bytes that passed the strict policy build;
2. repository Python surfaces under `tests/` and `experiments/` were outside both campaign-executable discovery and CI-script reachability.

The second defect was made concrete by the pending NS-CI-WP06 draft, which contained a valid-looking test and bounded fixture that the universal policy did not execute.

## Decision

1. The global policy packages the strict MkDocs output for successful pushes to `main` and uploads it as the short-lived `validated-site` workflow artifact.
2. The package contains a deterministic site archive and an inner SHA-256 record.
3. The downstream Pages workflow downloads only the `validated-site` artifact from the exact triggering policy run, verifies GitHub’s artifact digest and the inner archive digest, and deploys the extracted site without rebuilding it.
4. Pages continues to require that the validated SHA is still the current `main` tip before publication.
5. The Pages build job receives `actions: read` solely to retrieve the triggering run’s artifact; publication credentials remain separated from the policy workflow.
6. `ci/validate_repository_execution.py` discovers all `tests/test_*.py` modules and all non-package Python modules under `experiments/`.
7. Every discovered test module must expose actual `unittest.TestCase` methods, and the global policy must execute the entire test tree through standard-library discovery.
8. Every experiment module must be library-only and reachable from the discovered tests, directly or through the local experiment import graph.
9. Hidden, standalone, syntactically invalid, or untested experiment modules fail policy.
10. The existing campaign and CI execution controls remain authoritative for their own directories; this decision closes the separate repository-test and experiment surface.

## Alternatives considered

### Rebuild the site in Pages

Rejected. A second build can differ from the policy-validated output through environment, dependency, or toolchain movement. Current-tip identity alone does not prove byte-level publication identity.

### Upload the Pages artifact directly from the policy workflow

Rejected. Keeping deployment in the downstream workflow preserves separation between read-only policy execution and Pages/OIDC publication credentials.

### Add pytest as a new dependency

Rejected for the current bounded test surface. Standard-library `unittest` provides complete discovery without expanding the package dependency graph.

### Require manual registration of every test

Rejected. Full-tree unit-test discovery is a stronger omission control than another curated registry.

### Permit executable experiment scripts

Rejected at this stage. Executable experiments require an explicit command contract and should be promoted into a governed campaign replay rather than bypassing test-based evidence.

## Consequences

- Published site bytes are the bytes produced by the successful global policy run.
- A successful policy run without its expected artifact cannot publish.
- Artifact selection is scoped to the triggering workflow run, preventing cross-run name collisions.
- Repository experiments cannot enter the tree without test reachability.
- Test success establishes software behaviour only; it does not strengthen mathematical claims.
- Pages no longer resolves documentation dependencies or rebuilds MkDocs output.

## Affected artifacts

- `.github/workflows/ci.yml`
- `.github/workflows/pages.yml`
- `ci/validate_repository_execution.py`
- `ci/test_repository_execution.py`
- `ci/validate_workflow_coverage.py`
- `ci/test_workflow_coverage.py`
- `ci/validate_workflow_semantics.py`
- `ci/test_workflow_semantics.py`
- `docs/WORKFLOW_COVERAGE.md`
- `reviews/governance/WORKFLOW-COVERAGE.agent_review.yaml`
- continuity, terminology, inventory, and navigation records

## Claim boundary

This decision strengthens repository execution and publication evidence only. It does not establish deterministic builds across independent runs, a complete transitive supply-chain lock, theorem support, or mathematical promotion.

## Supersession

This decision extends ADR-0011 and ADR-0012. It does not supersede their claim boundaries or any campaign-specific mathematical decision.
