# ADR-0012: Make workflow coverage self-authenticating and reproducible

## Status

Accepted, 2026-07-26.

Final-head workflow evidence is recorded in the governing pull-request history rather than embedded self-referentially in this decision.

## Context

ADR-0011 made the global programme workflow authoritative before publication. A second pass over the merged implementation found four residual weaknesses in how that authority was established:

1. `ci/campaign_replay_registry.json` supplied its own discovery globs, so the registry could narrow the boundary that was meant to audit it;
2. executable `ci/*.py` validators and adversarial tests had no repository-wide reachability proof;
3. some workflow obligations were checked by searching raw YAML text, which could be satisfied by comments or harmless echo statements rather than operative steps;
4. Python packages and `ubuntu-latest` remained mutable, and a Pages run could deploy an older validated commit after `main` advanced.

These are execution-governance defects. They do not alter any mathematical claim, but they weaken what a green workflow and a published site can be said to represent.

## Decision

1. Campaign executable discovery is owned by validator code, not by the replay registry. Every Python file under `campaigns/` with a shebang or `__main__` guard is discovered independently of its filename.
2. The campaign registry remains the command authority for direct argument arrays, scope, and timeout. An executable must be registered or carry a governed exemption with an explicit rationale; registration and exemption may not overlap.
3. Every executable `ci/*.py` file must be reachable from an actual Python command in a governed workflow or replay registry, directly or through a statically parsed local import path.
4. Workflow names, runners, Python selectors, dependency-install routes, policy commands, Pages conditions, checkout references, and publication-freshness checks are validated from parsed YAML structures and operative `run` lines rather than raw-file marker presence.
5. All governed workflows use `ubuntu-24.04` rather than `ubuntu-latest`.
6. Every `actions/setup-python` step uses the governed `3.12` minor line. Patch-level movement within that line is accepted and must not be described as an exact runtime pin.
7. Policy and documentation dependencies are pinned in `requirements/policy.txt` and `requirements/docs.txt`. Ad hoc workflow `pip install` commands are rejected.
8. Pages cancels stale in-progress publication runs and verifies that the policy-validated SHA is still the current `main` tip immediately before building.
9. The stronger controls are adversarially tested against narrowed discovery, hidden executables, command-marker spoofing, duplicate workflow names, mutable runners, unconstrained Python selectors, unpinned installation, stale publication, and missing workflow roots.

## Alternatives considered

### Keep discovery globs in the replay registry

Rejected. A control cannot provide fail-closed evidence when the audited object can silently redefine the search space.

### Register every CI script manually

Rejected. A second manually curated list would recreate the omission problem. Executability is discovered by content and reachability is derived from workflow roots and the local import graph.

### Execute every Python file indiscriminately

Rejected. Helper modules are not commands and some scripts require arguments. Discovery determines which files require a route; workflows and replay records remain responsible for correct invocation.

### Rely on successful historical dependency resolution

Rejected. A later policy or Pages run could resolve different packages. Checked-in exact top-level pins stabilize the declared package layer, although they are not represented as a complete transitive hash lock.

### Present Python `3.12` as an exact runtime pin

Rejected. The minor-line selector permits patch-level movement. The declared environment must state that boundary explicitly unless a later supply-chain decision introduces an exact patch and stronger lock discipline.

### Publish every successful historical `main` run

Rejected. Publication should represent the current repository tip. A successful policy run for a superseded commit is archival execution evidence, not current publication authority.

## Consequences

- Campaign and CI coverage boundaries can no longer be narrowed by editing their registries or using unexpected executable filenames.
- Comments and echo statements cannot satisfy operative workflow-command obligations.
- All six governed workflows share a fixed runner family, a governed Python minor line, and checked-in top-level dependency declarations.
- A newer `main` commit supersedes any older Pages build before publication.
- The policy remains bounded: Python patch-level drift is accepted, exact top-level dependency pins do not constitute a full transitive hash lock, and static import reachability does not prove semantic correctness of the imported code.
- Runtime and maintenance cost increase modestly because workflow structure and dependency files are now governed artifacts.

## Affected artifacts

- `.github/workflows/ci.yml`
- `.github/workflows/pages.yml`
- `.github/workflows/bsd-wp03-substrate.yml`
- `.github/workflows/bsd-wp04-target.yml`
- `.github/workflows/pc-wp04.yml`
- `.github/workflows/pc-wp05.yml`
- `requirements/policy.txt`
- `requirements/docs.txt`
- `ci/campaign_replay_registry.json`
- `schemas/campaign_replay_registry.schema.json`
- `ci/validate_campaign_replays.py`
- `ci/test_campaign_replays.py`
- `ci/validate_policy_reachability.py`
- `ci/test_policy_reachability.py`
- `ci/validate_workflow_semantics.py`
- `ci/test_workflow_semantics.py`
- `docs/WORKFLOW_COVERAGE.md`
- `reviews/governance/WORKFLOW-COVERAGE.agent_review.yaml`
- continuity and inventory records

## Claim boundary

This decision establishes stronger evidence about repository execution, the declared Python minor line, top-level dependencies, workflow structure, and publication freshness. It does not establish an exact Python patch, a complete operating-system image identity, a transitive dependency hash lock, theorem certification, stronger imported mathematical relations, RH-WP01 or RH-WP02 promotion, novelty, or priority.

## Review provenance

- Trigger: user-requested second-pass coverage and consistency audit after merge of PR #95.
- Base commit: `bc70f10327f7f12505ad1c3a456be3e82455978c`.
- Dependency versions checked against official PyPI records on 2026-07-26.
- Initial comprehensive run confirmed the existing campaign executable set was fully registered and exposed one adversarial-test diagnostic mismatch, which was repaired without weakening discovery.

## Supersession

This decision extends ADR-0011. It does not supersede ADR-0011's global policy authority, ADR-0010's documentary authority, ADR-0006's Poincaré identity boundary, or any mathematical claim ledger.
