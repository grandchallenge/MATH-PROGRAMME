# Programme Workflow Coverage

## Purpose

The programme workflow is a claim-boundary control. A green documentation build alone is insufficient. Campaign replays, repository tests, executable policy controls, formal fixtures, cross-repository evidence, provider contracts, exact publication artifacts, and repository administration must remain distinct and governed.

## Current audit disposition

The umbrella audit dated 2026-07-29 is recorded in `WORKFLOW_COVERAGE_AUDIT_2026_07_29.md` and `governance/workflow_coverage_audit.json`.

Its determination is:

- CI contract coverage: `COMPLETE`;
- technical umbrella children: `COMPLETE`;
- administrative umbrella children: `COMPLETE`;
- `operational_release_complete: true`;
- remaining blockers: none;
- umbrella issue #6: `CLOSE`.

The admitted administrative evidence is App-backed release-trust run `30450610588`, artifact `8723362498`, and canonical evidence SHA-256 `acd7e9c3ea10e9c03ea5dc81a0b84918d7241fea886426d2304e168b10c936f8`.

## Global policy gate

`.github/workflows/ci.yml` is the global `Programme policy checks` workflow. It runs on pull requests, pushes to `main`, and explicit manual audits.

The workflow uses read-only repository permissions, bounded timeouts, non-persistent checkout credentials, immutable action references, fixed runner families, checked-in dependency pins, and concurrency cancellation.

| Job | Controlled obligation |
|---|---|
| `validate-json` | Schemas, fixtures, campaign replays, repository tests, experiment reachability, documentation, continuity, workflow semantics, and strict MkDocs |
| `log-gcd-lean` | Pinned Lean replay of the LOG-GCD formal fixture |
| `pc-wp04-lean` | Pinned Lean replay and policy validation of the bounded Poincaré certificate |
| `union-closed-mathcert` | Exact checkout and complete replay of pinned external MATHCERT evidence |

A successful workflow records integration, execution, policy, artifact, or bounded-certification facts. It does not promote an open mathematical claim.

## Covered repository surfaces

The global contract covers:

- recursive campaign executable discovery;
- executable CI-control reachability;
- repository tests and experiment reachability;
- symbolic resource budgets and failure ledgers;
- reusable cross-pillar lane packages;
- MATHFORGE provider imports;
- MATHSOLVE routing;
- programme-wide MATHCERT conformance;
- bounded MATHFORGE algebraic witness generation;
- bounded MATHSOLVE algebraic tactic routing;
- formal Lean replays;
- pinned external certification evidence;
- strict documentation construction;
- exact-artifact Pages publication semantics;
- governed fast-path workflows.

## Bounded algebraic provider chain

The algebraic lane now has explicit contracts at each provider boundary.

### MATHFORGE

A governed witness must record local scope, coefficient domain, variable and degree bounds, timeout, basis and term budgets, exact backend identity, observed execution, expected witness, fallback route, failure ledger, and content-addressed registry identity.

MATHFORGE outputs evidence. A `ready_for_mathcert` witness is not certified.

### MATHSOLVE

A governed tactic invocation must identify one local proof obligation, reject global open-problem encoding, declare resource limits and fallback conditions, identify the expected witness, pin its source, and state the exact MATHCERT checking obligation.

Packet readiness and submission are intake states. Only a content-addressed MATHCERT disposition can close the certification boundary.

## Policy-validated site artifact

On a successful push to `main`, the policy job packages the strict MkDocs output as a deterministic validated-site artifact. The Pages workflow deploys only that verified artifact and does not rebuild documentation independently.

Publication proceeds only when the policy run succeeded for a `main` push, the validated SHA remains the current `main` tip, artifact digests verify, safe extraction succeeds, and the site contains its required entry point.

This repository-side publication contract is complete. Issue #7 is closed: the release-trust evidence records the repository homepage, exact-main policy run, Pages deployment, validated-site artifact, and byte-identical public index.

## Protected-branch boundary

Exact-head workflow success alone does not prove that a repository administrator cannot bypass the workflow. Issue #125 is closed because the Release Trust App applied and read back the authoritative ruleset evidence for each mathematics governance repository.

The admitted administration record states:

- ruleset or protection identifier;
- required status-check context;
- strict or up-to-date requirement;
- review requirement;
- bypass actors or explicit absence of bypass;
- effective date and verification method.

## Policy impact gating demonstration

`MP-POLICY-IMPACT-GATING-001` was protected at merge `fad9cff9f8f73b78bfed94fb1aab9763f63d00ab`. Issue #390 requires a post-merge proof-clean pull request to demonstrate the reduced path.

The demonstration is non-authoritative. For a documentation-only transition, the expected policy impact is `core` plus `docs`, with all three formal lanes clean. Each clean formal lane must reuse a fresh protected content-addressed attestation and must skip Lean setup, fixture replay, and protected receipt creation. Inactive policy shards must complete through the governed verified-no-op path. `validate-json` remains the final required aggregator.

Demonstration workflow evidence does not create mathematical, source, certification, external-claim, publication, deployment, product, release, commercial, bypass, emergency, direct-protected-push, or Human Steward authority.

## Closure rule

MATH-PROGRAMME issue #6 may close only when:

1. Pages issue #7 is complete;
2. protected-branch issue #125 is complete;
3. the MATHFORGE and MATHSOLVE technical children remain complete;
4. `remaining_blockers` is empty;
5. `operational_release_complete` is `true`.

Merge state, workflow success, test success, witness identity, certification, publication visibility, and mathematical theorem support remain separate facts.