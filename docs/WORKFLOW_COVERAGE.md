# Programme Workflow Coverage

## Purpose

The programme workflow is a claim-boundary control. A green documentation build alone is insufficient: campaign replays, repository tests, executable policy scripts, formal fixtures, cross-repository evidence, continuity records, declared dependencies, and the exact published site artifact must all remain governed.

## Global policy gate

`.github/workflows/ci.yml` is the global `Programme policy checks` workflow. It runs on every pull request, every push to `main`, and explicit manual audit through `workflow_dispatch`.

It uses read-only repository permissions, bounded timeouts, non-persistent checkout credentials, immutable action references, fixed `ubuntu-24.04` runners, the Python `3.12` minor line, checked-in dependency pins, and pull-request concurrency cancellation.

| Job | Controlled obligation |
|---|---|
| `validate-json` | Schemas, fixtures, campaign replays, repository unit tests, experiment reachability, documentation, continuity, workflow semantics, and strict MkDocs |
| `log-gcd-lean` | Pinned Lean replay of the LOG-GCD formal fixture |
| `pc-wp04-lean` | Pinned Lean replay and policy validation of the bounded Poincaré certificate |
| `union-closed-mathcert` | Exact checkout and complete replay of the evidence-pinned external MATHCERT gate |

A successful workflow records integration, execution, policy, artifact, or bounded-certification facts. It does not promote an open mathematical claim.

## Campaign executable discovery

`ci/validate_campaign_replays.py` independently discovers every Python file under `campaigns/` with a shebang or `__main__` guard. Each discovered executable must be a registered direct Python command with a unique ID, scope, and timeout, or an explicit governed exemption with a substantive rationale. The registry cannot redefine the discovery boundary.

## CI policy reachability

`ci/validate_policy_reachability.py` discovers executable `ci/*.py` files, extracts operative Python roots from parsed workflows and the campaign registry, builds a local AST import graph, and requires every executable CI control to be reachable.

## Repository tests and experiment modules

`ci/validate_repository_execution.py` closes the separate `tests/` and `experiments/` surface:

- every `tests/test_*.py` file must contain discoverable `unittest.TestCase` methods;
- the global policy executes the full test tree with `python -m unittest discover`;
- every non-package Python module under `experiments/` must be library-only;
- every experiment module must be reachable from discovered tests, directly or through the local experiment import graph;
- hidden, standalone, syntactically invalid, or untested experiment modules fail policy.

Passing tests establish bounded software behaviour only. They do not establish mathematical truth or numerical evidence for a continuum claim.

## Workflow semantic contract

`ci/validate_workflow_semantics.py` validates operative YAML structures rather than raw marker presence. It requires exact workflow names, fixed runners, Python `3.12`, exact requirement-file routes, real execution of coverage controls, deterministic validated-site packaging, Pages artifact verification, and current-tip publication. Comments or echo statements cannot satisfy command obligations.

## Declared environment

The declared workflow environment consists of the `ubuntu-24.04` runner family, Python `3.12`, `requirements/policy.txt`, and `requirements/docs.txt`. Python patch movement within `3.12`, transitive dependency movement, and runner-image digest movement remain outside the guarantee.

## Formal and external evidence

The global workflow directly compiles LOG-GCD and PC-WP04. Union-Closed formal evidence is maintained in `grandchallenge/MATHCERT`; `evidence/UC-WP02-MATHCERT.json` records the exact repository, commit, paths, command, and claim boundary. Workflow checkout coordinates are literal and must match that evidence.

## Continuity controls

The global policy also enforces:

- RH-WP01/WP02 retained promotion blockers;
- absence and historical provenance of the retired Poincaré Domain 04 alias;
- schema-bound Agent Council reviews;
- documentary authority and availability distinctions;
- decision, ledger, terminology, navigation, and public-domain consistency.

## Policy-validated site artifact

On a successful push to `main`, the policy job packages the strict MkDocs output as a deterministic `validated-site.tar.gz`, writes an inner SHA-256 record, and uploads both files in a run-scoped `validated-site` workflow artifact retained for one day.

This artifact is publication evidence for that workflow run. It is not a permanent documentary release artifact and is unrelated to theorem support.

## Exact artifact publication

`.github/workflows/pages.yml` is triggered only after a completed `Programme policy checks` run. Publication proceeds only when:

1. the policy conclusion is `success`;
2. the validated branch is `main`;
3. the originating event was a push;
4. Pages checks out the exact validated `head_sha`;
5. that SHA is still the current `origin/main` tip;
6. exactly one unexpired `validated-site` artifact exists for the triggering workflow run;
7. GitHub’s artifact SHA-256 digest verifies;
8. the inner site-archive SHA-256 verifies;
9. the safely extracted site contains `index.html`.

Pages does not install documentation dependencies or rebuild MkDocs. It uploads the verified policy-produced site bytes to Pages and then deploys them. A newer `main` commit cancels or invalidates an older publication run.

The build job receives only `actions: read`, `contents: read`, and `pages: write`; the deploy job alone receives Pages write and OIDC token permissions. There is no manual Pages bypass.

## Workflow inventory

- `ci.yml` — global policy and validated-site producer;
- `pages.yml` — exact-artifact verifier and current-tip deployer;
- `bsd-wp03-substrate.yml` — BSD-WP03 fast replay;
- `bsd-wp04-target.yml` — BSD-WP04 fast replay;
- `pc-wp04.yml` — PC-WP04 fast certificate replay;
- `pc-wp05.yml` — PC-WP05 archival fast replay.

## Maintenance rule

A change to campaign executables, CI controls, repository tests, experiment modules, workflows, dependency declarations, external evidence, publication gates, retained blockers, retired paths, or historical crosswalks must update the governing decision or evidence record and pass the global policy. Merge state, workflow success, test success, artifact identity, publication visibility, certification, and theorem support remain distinct.
