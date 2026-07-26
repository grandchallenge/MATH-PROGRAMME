# ADR-0011: Require full workflow coverage before publication

## Status

Accepted, 2026-07-26.

## Context

The post-merge audit after PR #94 found four execution and continuity gaps:

1. merged BSD and RH campaign replay scripts existed in the repository but were not reachable from the global `Programme policy checks` workflow;
2. GitHub Pages deployed after a strict MkDocs build without waiting for the programme policy workflow, so publication could proceed despite a campaign, continuity, or certification failure;
3. the RH-WP01/WP02 retained promotion blockers were documented consistently but were not machine-enforced across the public page, catalogue, ledger, promotion register, disposition, and legacy reviews;
4. the Union-Closed handoff and file manifest named `MathCert/` and `MATHCERT/` paths as though they were local, although the authoritative implementation is maintained in the separate `grandchallenge/MATHCERT` repository.

Path-scoped campaign workflows were valuable for fast feedback but did not establish repository-wide reachability. A green general workflow therefore did not necessarily mean every executable campaign contract had run.

## Decision

1. Establish `ci/campaign_replay_registry.json` as the governed list of campaign and archive replay commands.
2. Discover every `campaigns/**/replay.py` and `campaigns/**/validate*.py` file and fail policy when a discovered executable is not registered.
3. Execute all registered BSD, RH, and Poincaré policy and adversarial commands in the global workflow under direct argument arrays and bounded timeouts.
4. Add global Lean replay for the bounded PC-WP04 certificate.
5. Record Union-Closed certification as cross-repository evidence pinned to an exact `grandchallenge/MATHCERT` commit and replay that repository's complete `ci/check_lean.sh` gate from the global workflow.
6. Machine-check the RH-WP01/WP02 retained-blocker state without promoting either artifact.
7. Make Pages deployment depend exclusively on successful completion of a push-triggered global policy run on `main`, and deploy the exact validated commit SHA.
8. Retain path-scoped BSD and Poincaré workflows as supplementary fast feedback rather than substitute policy gates.
9. Require explicit workflow permissions, bounded job timeouts, and non-persistent checkout credentials for every governed workflow.
10. Expose a manual global policy audit but no manual Pages bypass.

## Alternatives considered

### Continue relying on path-scoped workflows

Rejected. They do not run on unrelated changes that can still alter shared schemas, governance, or publication surfaces, and they do not provide one complete publication prerequisite.

### Auto-execute every Python file under `campaigns/`

Rejected. Arbitrary discovery without a registry cannot express arguments, timeouts, scope, or intentional execution boundaries. Discovery is used to detect omissions; the registry remains the command authority.

### Keep Pages on direct push and rely on branch protection

Rejected. Branch protection is repository configuration outside the versioned programme contract and does not guarantee that the deployed workflow waits for every relevant job. Publication must be downstream of the versioned global gate.

### Copy MATHCERT sources into MATH-PROGRAMME

Rejected. It would duplicate formal authority and create source drift. The correct boundary is an exact external commit plus a replayed certification command.

### Treat successful merge and CI as RH-WP01/WP02 promotion

Rejected. The legacy reviews explicitly retain `promotion_recommended: false` and blocking Referee findings. Workflow coverage preserves, rather than erases, that distinction.

## Consequences

- Every currently discovered campaign replay or validator is executed on every pull request and every push to `main`.
- A new campaign replay file cannot silently enter the tree without registration.
- The published site corresponds to a commit that passed campaign, documentation, continuity, formal-fixture, and external-evidence gates.
- Union-Closed formal evidence has one explicit cross-repository identity rather than nonexistent local paths.
- RH implementation facts and promotion blockers are both machine-enforced.
- Global policy runtime increases because PC-WP04 and external MATHCERT Lean gates now run universally; this cost is accepted as the price of a meaningful repository-wide green state.
- Path-scoped workflows may provide earlier feedback but cannot weaken the global gate.

## Affected artifacts

- `.github/workflows/ci.yml`
- `.github/workflows/pages.yml`
- `.github/workflows/bsd-wp03-substrate.yml`
- `.github/workflows/bsd-wp04-target.yml`
- `.github/workflows/pc-wp04.yml`
- `.github/workflows/pc-wp05.yml`
- `ci/campaign_replay_registry.json`
- `ci/validate_campaign_replays.py`
- `ci/test_campaign_replays.py`
- `ci/validate_workflow_coverage.py`
- `ci/test_workflow_coverage.py`
- `ci/validate_rh_continuity.py`
- `ci/test_rh_continuity.py`
- `evidence/UC-WP02-MATHCERT.json`
- `schemas/campaign_replay_registry.schema.json`
- `schemas/cross_repository_evidence.schema.json`
- `WP02_UNION_CLOSED_LEAN_HANDOFF.md`
- `FILE_MANIFEST.md`
- `docs/WORKFLOW_COVERAGE.md`
- governance and reference indexes

## Claim boundary

This decision governs execution coverage, external evidence identity, deployment order, and continuity. It does not prove Frankl's conjecture, promote RH-WP01 or RH-WP02, strengthen the PC-WP04 imported mathematical relations, certify a new theorem, or make a novelty claim.

## Review provenance

- Trigger: user-requested loose-end and full-workflow audit after PR #94.
- Base commit: `fe5a8c63d7b2f27927f27d7d9e2e203e19330398`.
- External MATHCERT evidence inspected at `d59173899dcd1a67dbe8f31de0b9f0917cd1459a`.
- Promotion and publication boundaries checked against ADR-0007 through ADR-0010.

## Supersession

This decision extends ADR-0007's CI-scope discipline, ADR-0008 and ADR-0009's semantic documentation coverage, and ADR-0010's publication authority. It does not supersede their mathematical or documentary claim boundaries.
