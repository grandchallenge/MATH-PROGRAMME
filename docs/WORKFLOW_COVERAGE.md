# Programme Workflow Coverage

## Purpose

The programme workflow is a claim-boundary control. A green documentation build alone is insufficient: governed campaign replays, formal fixtures, cross-repository certification evidence, continuity records, and publication gates must all remain reachable from the repository-wide policy workflow.

## Global policy gate

`.github/workflows/ci.yml` is the global `Programme policy checks` workflow. It runs on:

- every pull request;
- every push to `main`;
- explicit manual audit through `workflow_dispatch`.

The workflow uses read-only repository permissions, bounded job timeouts, non-persistent checkout credentials, and pull-request concurrency cancellation.

Its required jobs are:

| Job | Controlled obligation |
|---|---|
| `validate-json` | Schemas, fixtures, documentary policy, programme contracts, documentation, workflow coverage, RH retained blockers, and every registered campaign replay |
| `log-gcd-lean` | Pinned Lean replay of the published LOG-GCD formal fixture |
| `pc-wp04-lean` | Pinned Lean replay and policy validation of the bounded Poincaré certificate |
| `union-closed-mathcert` | Exact checkout and replay of the evidence-pinned external `grandchallenge/MATHCERT` certification gate |

A successful workflow establishes only the recorded integration, replay, policy, or bounded-certification facts. It does not promote an open mathematical claim.

## Campaign replay discovery

`ci/campaign_replay_registry.json` is the governed replay registry. `ci/validate_campaign_replays.py` discovers every file matching:

```text
campaigns/**/replay.py
campaigns/**/validate*.py
campaigns/**/test_validate*.py
```

A discovered executable that is absent from the registry fails policy. Registry entries use direct argument arrays rather than shell strings, have unique IDs and script paths, and run under explicit timeouts. This prevents a newly merged campaign validator or its adversarial rejection suite from existing in the tree without being executed by the global gate.

Path-scoped BSD and Poincaré workflows remain as fast feedback. They do not replace the global replay gate.

## External MATHCERT evidence

Union-Closed Lean definitions and bounded certificates are maintained in the separate `grandchallenge/MATHCERT` repository. `evidence/UC-WP02-MATHCERT.json` records:

- the repository;
- an exact 40-character commit SHA;
- the formal and certificate paths;
- the complete certification command;
- the claim boundary.

The global policy checks out that exact commit and runs `bash ci/check_lean.sh`. A moving branch name is not accepted as evidence. Updating the external dependency requires updating the evidence record and passing the full programme policy again.

## RH retained-blocker continuity

`ci/validate_rh_continuity.py` requires the RH public page, catalogue, artifact ledger, promotion register, disposition record, and legacy review records to agree that:

- RH-WP01 and RH-WP02 are implemented, merged, and CI-passed;
- they are not formally promoted;
- `promotion_recommended` remains false;
- the blocking Referee findings remain active.

The adversarial tests reject any silent conversion of repository integration into mathematical or artifact promotion.

## Publication gate

`.github/workflows/pages.yml` no longer deploys directly from a push. It runs only after `Programme policy checks` completes and only when all of the following hold:

1. the policy conclusion is `success`;
2. the validated branch is `main`;
3. the originating event was a push;
4. the Pages build checks out the exact validated `head_sha`.

A manual Pages bypass is not provided. Manual audits run the policy workflow but do not publish.

## Workflow inventory

The current governed workflow set is:

- `ci.yml` — global policy;
- `pages.yml` — downstream publication;
- `bsd-wp03-substrate.yml` — BSD-WP03 fast replay;
- `bsd-wp04-target.yml` — BSD-WP04 fast replay;
- `pc-wp04.yml` — PC-WP04 fast certificate replay;
- `pc-wp05.yml` — PC-WP05 archival fast replay.

`ci/validate_workflow_coverage.py` rejects an unregistered workflow, a missing governed workflow, absent least-privilege permissions, missing job timeouts, persistent checkout credentials, missing global jobs, a direct Pages push trigger, or an unpinned external evidence commit.

## Maintenance rule

A change to a campaign replay, workflow file, external certification dependency, publication gate, or retained-blocker contract must update its governing registry or evidence record and pass the global policy workflow. Merge state, workflow success, and publication visibility remain separate from theorem support and formal artifact promotion.
