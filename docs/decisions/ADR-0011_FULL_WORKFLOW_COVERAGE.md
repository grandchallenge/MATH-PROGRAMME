# ADR-0011: Require full workflow coverage before publication

## Status

Accepted, 2026-07-26; implementation findings and retired-path continuity integrated 2026-07-26.

## Context

The post-merge audit after PR #94 found four execution and continuity gaps:

1. merged BSD and RH campaign replay scripts existed in the repository but were not reachable from the global `Programme policy checks` workflow;
2. GitHub Pages deployed after a strict MkDocs build without waiting for the programme policy workflow, so publication could proceed despite a campaign, continuity, or certification failure;
3. the RH-WP01/WP02 retained promotion blockers were documented consistently but were not machine-enforced across the public page, catalogue, ledger, promotion register, disposition, and legacy reviews;
4. the Union-Closed handoff and file manifest named `MathCert/` and `MATHCERT/` paths as though they were local, although the authoritative implementation is maintained in the separate `grandchallenge/MATHCERT` repository.

The first complete execution pass exposed further latent defects that narrower workflows had not made visible:

- the BSD WP01/WP02 validator used a brittle lexical condition inconsistent with its own noncomposable theorem-interface records;
- the PC-WP04 Lake package identifier used a hyphenated name rejected by current Lake before compilation;
- the PC-WP04 policy checked file presence but not package-name and toolchain/manifest concordance;
- several Lean jobs treated a cache/setup wrapper outcome as the certification fact instead of requiring the actual pinned `lake build`;
- workflow review provenance, action immutability, external-checkout coordinates, and Pages credential scope were not fully governed.

During remediation, PR #96 removed the mislabelled `DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md`. Current authority records, version-history provenance, the archival alias register, and frozen pre-renumbering reviews then required an explicit continuity contract rather than silent rewriting or stale current-path claims.

Path-scoped campaign workflows remain valuable for fast feedback but do not establish repository-wide reachability. A green general workflow must mean that every declared executable, formal, continuity, external-evidence, and publication control has run for the exact commit.

## Decision

1. Establish `ci/campaign_replay_registry.json` as the governed list of campaign and archive replay commands.
2. Discover every `campaigns/**/replay.py`, `campaigns/**/validate*.py`, and `campaigns/**/test*.py` file and fail policy when a discovered executable is not registered.
3. Execute all registered BSD, RH, and Poincaré policy and adversarial commands in the global workflow under direct argument arrays and bounded timeouts.
4. Replace brittle BSD lexical inference with explicit theorem-interface, source-locator, dependency-debt, and closed-gate checks, with adversarial mutations.
5. Require the PC-WP04 policy to validate its Lake package identifier, Lean toolchain, mathlib revision, manifest identity, declarations, sources, and replay bindings before kernel compilation.
6. Add global direct Lean replay for the bounded PC-WP04 certificate and retain direct LOG-GCD Lean replay.
7. Record Union-Closed certification as cross-repository evidence pinned to an exact `grandchallenge/MATHCERT` commit and replay that repository's complete `ci/check_lean.sh` gate from the global workflow.
8. Keep the external checkout repository and commit literal in the workflow and require exact agreement with the audited evidence record; pull-request-controlled data may not redirect the checkout.
9. Machine-check the RH-WP01/WP02 retained-blocker state without promoting either artifact.
10. Make Pages deployment depend exclusively on successful completion of a push-triggered global policy run on `main`, deploy the exact validated commit SHA, and scope Pages/OIDC credentials to the jobs that require them.
11. Retain path-scoped BSD and Poincaré workflows as supplementary fast feedback rather than substitute policy gates.
12. Require explicit least-privilege permissions, concurrency controls, bounded job timeouts, non-persistent checkout credentials, and immutable full-commit action references for every governed workflow.
13. Govern the removed Poincaré Domain 04 alias through `ci/validate_retired_paths.py` and `reviews/poincare/HISTORICAL_IDENTITY_CROSSWALK.yaml`: the path remains absent, Domain 05 remains canonical, current claim provenance uses an exact version-history locator, and frozen reviews preserve their original identity only as enumerated provenance.
14. Expose a manual global policy audit but no manual Pages bypass.

## Alternatives considered

### Continue relying on path-scoped workflows

Rejected. They do not run on unrelated changes that can still alter shared schemas, governance, or publication surfaces, and they do not provide one complete publication prerequisite.

### Auto-execute every Python file under `campaigns/`

Rejected. Arbitrary discovery without a registry cannot express arguments, timeouts, scope, or intentional execution boundaries. Discovery is used to detect omissions; the registry remains the command authority.

### Keep Pages on direct push and rely on branch protection

Rejected. Branch protection is repository configuration outside the versioned programme contract and does not guarantee that the deployed workflow waits for every relevant job. Publication must be downstream of the versioned global gate.

### Copy MATHCERT sources into MATH-PROGRAMME

Rejected. It would duplicate formal authority and create source drift. The correct boundary is an exact external commit plus a replayed certification command.

### Derive external checkout coordinates from the evidence file

Rejected. A pull request could change both the evidence record and the dynamic checkout coordinates before the validation job completed. The workflow pin and evidence record must be independent controls that agree exactly.

### Treat successful merge and CI as RH-WP01/WP02 promotion

Rejected. The legacy reviews explicitly retain `promotion_recommended: false` and blocking Referee findings. Workflow coverage preserves, rather than erases, that distinction.

### Rewrite frozen Poincaré reviews to Domain 05

Rejected. Those records reviewed the pre-renumbering artifact identity. The correct repair is a current canonical Domain 05 authority plus a governed historical-identity crosswalk, not retrospective alteration of review provenance.

## Consequences

- Every currently discovered campaign replay, validator, or campaign adversarial test is executed on every pull request and every push to `main`.
- A new campaign executable cannot silently enter the tree without registration.
- The published site corresponds to a commit that passed campaign, documentation, continuity, formal-fixture, external-evidence, retired-path, and publication gates.
- Union-Closed formal evidence has one explicit cross-repository identity rather than nonexistent local paths or a PR-redirectable checkout.
- RH implementation facts and promotion blockers are both machine-enforced.
- The PC-WP04 package now reaches actual kernel compilation with a policy-checked Lake/toolchain contract.
- The removed Poincaré alias is absent from current authority while its exact historical review and claim provenance remain recoverable and bounded.
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
- `ci/validate_retired_paths.py`
- `ci/test_retired_paths.py`
- `campaigns/birch_swinnerton_dyer/validate_wp01_wp02.py`
- `campaigns/birch_swinnerton_dyer/test_validate_wp01_wp02.py`
- `fixtures/formal/PC-WP04/lakefile.toml`
- `fixtures/formal/PC-WP04/lake-manifest.json`
- `ci/validate_pc_wp04_fixture.py`
- `ci/test_pc_wp04_fixture.py`
- `evidence/UC-WP02-MATHCERT.json`
- `reviews/poincare/HISTORICAL_IDENTITY_CROSSWALK.yaml`
- `schemas/campaign_replay_registry.schema.json`
- `schemas/cross_repository_evidence.schema.json`
- `WP02_UNION_CLOSED_LEAN_HANDOFF.md`
- `DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md`
- `campaigns/poincare_reconstruction/WP00_SOURCE_EQUIVALENCE/10_CLAIM_LEDGER.yaml`
- `campaigns/poincare_reconstruction/WP05_INTEGRATED_CLOSURE/09_ARCHIVAL_MANIFEST.json`
- `FILE_MANIFEST.md`
- `docs/REPOSITORY_DOCS.md`
- `docs/WORKFLOW_COVERAGE.md`
- governance and reference indexes

## Claim boundary

This decision governs execution coverage, external evidence identity, deployment order, historical identity, and continuity. It does not prove Frankl's conjecture, promote RH-WP01 or RH-WP02, strengthen the PC-WP04 imported mathematical relations, certify a new theorem, or make a novelty claim.

## Review provenance

- Trigger: user-requested loose-end and full-workflow audit after PR #94.
- Original base commit: `fe5a8c63d7b2f27927f27d7d9e2e203e19330398`.
- Integrated upstream retirement commit: `99f66fdb0e2d5cd99c2d6e4f716d77d56cd3ea35` from PR #96.
- External MATHCERT evidence inspected at `d59173899dcd1a67dbe8f31de0b9f0917cd1459a`.
- Promotion, historical-identity, and publication boundaries checked against ADR-0006 through ADR-0010 and the schema-bound `WORKFLOW-COVERAGE-001` review.

## Supersession

This decision extends ADR-0007's CI-scope discipline, ADR-0008 and ADR-0009's semantic documentation coverage, ADR-0010's publication authority, and ADR-0006's Poincaré identity decision. It does not supersede their mathematical or documentary claim boundaries.
