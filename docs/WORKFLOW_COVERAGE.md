# Programme Workflow Coverage

## Purpose

The programme workflow is a claim-boundary control. A green documentation build alone is insufficient: governed campaign replays, executable policy scripts, formal fixtures, cross-repository certification evidence, continuity records, declared dependencies, and publication gates must all remain reachable from the repository-wide policy workflow.

## Global policy gate

`.github/workflows/ci.yml` is the global `Programme policy checks` workflow. It runs on:

- every pull request;
- every push to `main`;
- explicit manual audit through `workflow_dispatch`.

The workflow uses read-only repository permissions, bounded job timeouts, non-persistent checkout credentials, immutable action references, fixed `ubuntu-24.04` runners, a governed Python `3.12` minor line, checked-in dependency pins, and pull-request concurrency cancellation.

Its required jobs are:

| Job | Controlled obligation |
|---|---|
| `validate-json` | Schemas, fixtures, documentary policy, programme contracts, documentation, semantic workflow coverage, CI-script reachability, RH retained blockers, retired-path continuity, and every governed campaign executable |
| `log-gcd-lean` | Pinned Lean replay of the published LOG-GCD formal fixture |
| `pc-wp04-lean` | Pinned Lean replay and policy validation of the bounded Poincaré certificate |
| `union-closed-mathcert` | Exact checkout and replay of the evidence-pinned external `grandchallenge/MATHCERT` certification gate |

A successful workflow establishes only the recorded integration, replay, policy, dependency, or bounded-certification facts. It does not promote an open mathematical claim.

## Campaign executable discovery

`ci/campaign_replay_registry.json` is the governed command registry, but it does not define its own search boundary. `ci/validate_campaign_replays.py` independently scans every Python file under `campaigns/` and treats a file as executable when it has a shebang or an `if __name__ == "__main__"` guard.

Every discovered executable must be one of:

1. a registered direct Python command with a unique ID, scope, and bounded timeout; or
2. a governed exemption naming the exact path and a substantive rationale.

A script cannot be both registered and exempt. Missing exemption targets, non-executable targets, unexpected executable filenames, and attempts to restore registry-controlled discovery globs fail policy. The registry remains the command authority; validator code owns discovery.

Path-scoped BSD and Poincaré workflows remain fast feedback. They do not replace the global replay gate.

## CI policy reachability

`ci/validate_policy_reachability.py` discovers every executable Python file directly under `ci/`. It then:

- extracts actual Python commands from parsed governed workflows;
- adds direct Python commands from the campaign replay registry;
- builds a local AST import graph among `ci/*.py` modules;
- requires every executable CI script to be reachable from a workflow root, directly or through imports;
- rejects workflow or registry commands that name missing Python files.

This allows helper modules to remain helpers while preventing a new validator or adversarial test from existing in the tree without an execution route.

## Workflow semantic contract

`ci/validate_workflow_semantics.py` validates operative workflow structures rather than relying on raw YAML marker presence. It requires:

- exact and unique workflow names;
- `ubuntu-24.04` for every governed job;
- Python `3.12` for every `setup-python` step;
- exact checked-in dependency declarations;
- requirement-file installation rather than ad hoc `pip install` commands;
- direct execution of the reachability and semantic validators and their adversarial tests;
- exact Pages workflow conditions and checkout reference;
- a current-`main` freshness check before publication.

Adversarial tests reject comments or echo statements that merely contain a required command string, mutable runner labels, or an unconstrained Python selector such as `3.x`.

## Declared Python environment

The governed declaration consists of:

- the fixed `ubuntu-24.04` runner family;
- the Python `3.12` minor line;
- `requirements/policy.txt` for JSON-schema and YAML policy execution;
- `requirements/docs.txt` for strict MkDocs publication.

All governed workflows install from those files. The exact top-level pins stabilize the declared package layer across PR, push, and Pages runs. The Python selector deliberately permits patch-level movement within `3.12`. Neither that minor-line policy nor the top-level package pins is presented as a complete transitive hash lock or an exact operating-system image digest.

## External MATHCERT evidence

Union-Closed Lean definitions and bounded certificates are maintained in the separate `grandchallenge/MATHCERT` repository. `evidence/UC-WP02-MATHCERT.json` records:

- the repository;
- an exact 40-character commit SHA;
- the formal and certificate paths;
- the complete certification command;
- the claim boundary.

The global policy checks out that exact commit and runs `bash ci/check_lean.sh`. A moving branch name is not accepted as evidence. The workflow checkout coordinates are literal and must agree exactly with the audited evidence record; a pull-request edit cannot redirect the external checkout. Updating the dependency requires changing both controls and passing the full programme policy again.

## RH retained-blocker continuity

`ci/validate_rh_continuity.py` requires the RH public page, catalogue, artifact ledger, promotion register, disposition record, and legacy review records to agree that:

- RH-WP01 and RH-WP02 are implemented, merged, and CI-passed;
- they are not formally promoted;
- `promotion_recommended` remains false;
- the blocking Referee findings remain active.

The adversarial tests reject any silent conversion of repository integration into mathematical or artifact promotion.

## Retired-path continuity

`ci/validate_retired_paths.py` governs the removal of the mislabelled Poincaré Domain 04 master-plan alias. It requires:

- the retired filename to be absent from the current tree;
- the canonical Domain 05 master plan to exist;
- current authority records to state that the alias was removed;
- claim provenance to use an exact commit-pinned version-history locator;
- frozen pre-renumbering reviews and the archival alias registry to be enumerated in `reviews/poincare/HISTORICAL_IDENTITY_CROSSWALK.yaml`;
- all other references to the retired filename to fail closed.

This preserves historical review provenance without restoring the retired alias to current authority.

## Publication gate

`.github/workflows/pages.yml` runs only after `Programme policy checks` completes and only when all of the following hold:

1. the policy conclusion is `success`;
2. the validated branch is `main`;
3. the originating event was a push;
4. the Pages build checks out the exact validated `head_sha`;
5. that SHA is still the current `origin/main` tip immediately before the site build.

A newer `main` commit supersedes an older publication run. Pages concurrency cancels stale in-progress publication, and the build itself fails closed if the validated SHA is no longer current. Workflow-level permissions remain read-only. The build job receives only repository read access and the Pages permission needed to configure and upload the site artifact. The deploy job alone receives Pages write and OIDC token permissions. A manual Pages bypass is not provided.

## Workflow inventory

The current governed workflow set is:

- `ci.yml` — global policy;
- `pages.yml` — downstream current-tip publication;
- `bsd-wp03-substrate.yml` — BSD-WP03 fast replay;
- `bsd-wp04-target.yml` — BSD-WP04 fast replay;
- `pc-wp04.yml` — PC-WP04 fast certificate replay;
- `pc-wp05.yml` — PC-WP05 archival fast replay.

`ci/validate_workflow_coverage.py` governs inventory, permissions, action immutability, triggers, required jobs, external evidence, and publication authority. `ci/validate_workflow_semantics.py` adds parsed names, runner pins, Python minor-line governance, dependency routes, operative commands, and current-tip publication checks.

## Maintenance rule

A change to a campaign executable, CI policy script, workflow file, Python minor line, dependency declaration, external certification dependency, publication gate, retained-blocker contract, retired path, or historical-identity crosswalk must update its governing registry, decision, or evidence record and pass the global policy workflow. Merge state, workflow success, declared reproducibility, and publication visibility remain separate from theorem support and formal artifact promotion.
