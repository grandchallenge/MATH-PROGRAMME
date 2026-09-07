# GH-OS routing control runbook

## Purpose

This runbook governs maintenance of MATH-PROGRAMME's mandatory execution-routing control. The control is self-policing, not self-authorizing: it detects coverage, capability, topology, controller, identity, and enforcement drift.

Routine workflow maintenance follows the standing delegated execution model. A legitimate routine change does not require fresh Human Steward or generic independent approval merely because its commit is new. Security-sensitive weakening, external gate authority changes, controller capability expansion, or temporary removal of protected enforcement remains a reserved control-plane boundary and receives the specialist or Human Steward authority required by that exact action.

This runbook grants no certification, mathematical-claim, publication, external-claim, or protected-bypass authority.

## Control surface

| Surface | Purpose |
| --- | --- |
| `.ghos-routing/workflows.json` | Complete workflow inventory, derived features, topology, controller, and fixed authority boundaries |
| `ci/ghos_execution_routing.py` | Repository-local deterministic validator |
| `schemas/ghos_execution_routing.schema.json` | Closed routing-record schema |
| `tests/test_ghos_execution_routing.py` | Core hostile semantic tests plus effective-candidate, base-advance, and enforcement-contract regressions |
| `.github/workflows/ghos-routing-enforcement.yml` | Protected-base candidate-independent enforcement and protected-base revalidation dispatcher |
| `grandchallenge/.github/scripts/ghos_execution_routing_gate.py` | External governed gate whose bytes are SHA-256 pinned by the enforcement workflow |
| Ruleset `21969152` | Dedicated protected-main requirement for `routing-enforcement` |
| Ruleset `17137629` | Separate Programme profile; not the GH-OS routing ruleset |

The dedicated routing ruleset currently requires `routing-enforcement` with `strict_required_status_checks_policy: false` and no bypass actors. Non-strict status policy is deliberate: it permits concurrent mergeable development without update-branch synchronization solely for freshness. The protected controller supplies freshness by binding the required context to the effective merge candidate and revalidating open pull requests after protected-main movement.

## Routine workflow maintenance

When adding, deleting, renaming, or changing a workflow:

1. Run `python ci/ghos_execution_routing.py`.
2. Update exactly one corresponding entry in `.ghos-routing/workflows.json`, or remove the stale entry when deleting a workflow.
3. Use the exact feature list and topology derived from workflow bytes. Do not weaken or over-declare them manually; the shared gate requires equality with its byte-derived result.
4. For any non-`BOUNDED_ATOMIC` workflow, use the exact admitted controller and confirm that all derived features are supported. Otherwise decompose the operation into independently recoverable bounded workflows.
5. Run the focused routing/semantic tests needed by the changed control. Current policy impact routing will select the additional protected shards actually affected.
6. Require `routing-enforcement` on changed workflow bytes and the affected policy/security checks selected by current policy. Do not require repository-wide, campaign-wide, formal, or computational replay when their material inputs are unchanged.
7. Merge through protected controls under standing delegated authority when the change is routine, mergeable, and does not weaken or expand the protected control boundary.

The expected maintenance burden is one routing-entry update per workflow change plus affected validation. The gate supplies the authoritative diagnostic when the entry drifts.

## Candidate-independent enforcement and concurrency

The enforcement workflow executes protected controller logic from protected `main` under `pull_request_target` or a protected `workflow_dispatch`. Candidate content is inert data and must never be executed under the privileged controller.

For each pull request targeting `main`, the controller:

1. checks out current protected `main` with credentials disabled;
2. reads the current pull-request identity through the GitHub API;
3. fetches `refs/pull/<number>/head` and `refs/pull/<number>/merge` as data;
4. accepts the merge ref only when its two parents are exactly the current protected-main commit followed by the current pull-request head commit, and the API-reported test-merge identity equals the fetched merge identity;
5. fails closed after a bounded retry when GitHub cannot supply that exact effective candidate;
6. materializes the verified merge tree without executing any candidate-controlled program, action, hook, script, dependency declaration, or workflow;
7. compares the effective candidate's enforcement-workflow bytes with the protected-base enforcement workflow and rejects ordinary self-modification;
8. verifies the content-addressed external gate and runs that gate only against the inert effective-candidate tree;
9. re-fetches protected `main` before admitting the gate result and fails if the protected base moved during evaluation; and
10. publishes the required `routing-enforcement` status to the verified effective merge commit, not to a stale head-only snapshot.

The controller job is deliberately not named `routing-enforcement`. The dedicated required context is the commit status emitted only for the verified effective merge commit. Therefore a successful routing result attached only to a pull-request head cannot stand in for evaluation of a materially different current effective merge candidate.

Protected-main movement does not require update-branch synchronization. On each push to `main`, the protected workflow dispatches a fresh effective-candidate evaluation for every open pull request targeting `main`. GitHub may regenerate the virtual merge candidate; the controller accepts it only after the exact-parent checks above. A disjoint protected-base change should therefore produce a fresh passing effective-candidate result without mutating the pull-request branch. A relevant protected-base routing change is necessarily present in the effective tree and can invalidate the gate result.

If protected-main movement occurs while a controller evaluation is in flight, the protected-base recheck fails that attempt rather than publishing success for a stale base. The subsequent protected-main dispatch supplies the fresh evaluation. If GitHub cannot generate the current merge candidate or cannot dispatch the revalidation, the current effective candidate lacks a passing required context and remains blocked; absence of evidence is not success.

Do not evaluate the routing contract against raw stale branch snapshots where the protected control requires the effective merge candidate.

## External gate and digest rotation

An external gate semantic change is a control-plane upgrade rather than ordinary workflow maintenance.

1. Change and test the gate in `grandchallenge/.github` through its protected path.
2. Record the merged gate commit, exact script blob, SHA-256, test evidence, compatibility statement, and affected repositories.
3. Prefer a versioned successor path while the prior pinned path remains available when consumers require staged migration.
4. Prepare the smallest consumer update containing the justified pin/path change and necessarily synchronized local validator, schema, tests, controller catalog, registry, or documentation.
5. Obtain specialist non-author review when the change alters security-sensitive enforcement semantics, controller authority, or another reserved boundary. A pure content-addressed repin to already-admitted equivalent semantics does not acquire a generic reviewer gate merely because the digest changed.
6. Follow the protected self-modification procedure only if the active self-protection makes ordinary protected admission impossible.
7. After a material enforcement upgrade, run focused hostile proof that candidate-controlled local validation cannot bypass the protected external gate.

A digest mismatch is an expected fail-closed condition. Never solve it by removing the digest check, following an unpinned branch, or executing candidate code.

## Protected self-modification procedure

The active enforcement workflow rejects candidate modification of itself. A legitimate successor that therefore requires temporary relaxation of the dedicated routing rule crosses a security-sensitive protection boundary and is not routine delegation.

1. Freeze only the affected workflow-control mutation while preparing the bootstrap; unrelated bounded read-only or disjoint work may continue.
2. Record protected-main identity, dedicated routing ruleset `21969152`, required context, bypass actors, enforcement-workflow blob, external gate identity/digest, and separate Programme ruleset `17137629`.
3. Obtain the reserved authorization required for the exact temporary weakening and successor control bytes. Do not add a bypass actor or weaken unrelated rules.
4. Remove or disable only the routing requirement necessary for the bootstrap. Preserve every other applicable protected rule.
5. Merge only the authorized material successor after all other affected checks and specialist review required by the security boundary pass.
6. Immediately restore ruleset `21969152` active with `routing-enforcement`, `strict_required_status_checks_policy: false`, and zero bypass actors. Do not restore obsolete strict/up-to-date synchronization semantics.
7. Read back the complete ruleset, protected merge, enforcement blob, registry, validator, external digest, and post-merge checks.
8. Execute focused hostile proof before declaring the control restored.
9. Record before/after protection identity and the material authorization in the governing issue or protected evidence record.

If the successor identity, reserved authorization, ruleset snapshot, or restoration route is unavailable, stop. Do not leave the routing requirement disabled while diagnosing an unrelated failure.

## Admitted-controller changes

The controller catalog is code-governed in both local and external gates. Adding or changing a controller requires evidence for its durable wake mechanism, state store, supported feature classes, repository identity, and failure/recovery behavior.

Controller capability expansion is a material control-plane change. Update the external gate, local validator, schema if necessary, registry, hostile tests, and affected workflow entries together. Demonstrate agent replacement, stale evidence rejection, interrupted execution recovery, and unauthorized-transition failure before admission. Controller capability never supplies authority.

## Ruleset care

After routing administration or a material control upgrade:

1. Read dedicated routing ruleset `21969152` from GitHub.
2. Confirm it is active on `refs/heads/main`.
3. Confirm `routing-enforcement` is required with `strict_required_status_checks_policy: false`.
4. Confirm bypass actors remain empty.
5. Confirm the passing required context is bound to the current effective merge commit when a pull request is being admitted; a head-only status is not equivalent.
6. Read Programme profile `17137629` separately so a routing transaction cannot silently weaken unrelated Programme protections.
7. Open a bounded repair immediately on material drift. Pause only the affected unattended transition if enforcement is no longer mandatory.

Do not interpret a passing optional routing check or a stale head-only result as equivalent to the required protected effective-candidate context.

## Emergency diagnosis

Use this order when `routing-enforcement` fails:

1. Bind the failure to repository, pull request, current protected-base SHA, pull-request head SHA, verified effective-merge SHA and parent identities, workflow run, external gate digest, and emitted status context where available.
2. Classify the first exact error: missing registry, coverage mismatch, feature drift, topology drift, controller mismatch, repository mismatch, unavailable/stale merge ref, merge-parent mismatch, protected-base movement during evaluation, self-modification, external digest failure, status-publication failure, revalidation-dispatch failure, dependency failure, or platform outage.
3. For candidate drift, correct the changed candidate registry/workflow and rerun the affected routing check. Do not refresh unrelated review or CI evidence.
4. For a stale or unavailable merge ref, retain the required context and retry through the protected controller; do not fall back to head-only validation.
5. For an external digest mismatch, verify the protected shared script and change history; use the control-upgrade route rather than changing the pin ad hoc.
6. For a platform outage, leave the gate required and recover evidence through the execution-recovery guide. Do not infer success from absence of a result.
7. For unexpected ruleset drift or missing enforcement, pause the affected unattended transition until protected enforcement is restored and proven.

Never solve an emergency by executing untrusted candidate code under `pull_request_target`, granting write credentials to candidate content, removing authority boundaries, or carrying an approval to materially changed security-control bytes.

## Periodic and sentinel evidence

After every material control upgrade, and through the programme's existing scheduled/manual assurance rather than a separate timer, retain or verify as appropriate:

- current protected-main and enforcement-workflow identities;
- successful workflow inventory/coverage validation;
- external gate commit/path/digest;
- dedicated routing ruleset identity, required context, strictness, and bypass actors;
- proof that the required context is attached to the current effective merge candidate rather than only to the pull-request head;
- separate Programme-profile readback where routing administration occurred;
- focused hostile-test results, including relevant and disjoint protected-base movement;
- live or fixture-based fail-closed proof outside candidate control.

Routine periods with no workflow, controller, gate, or ruleset change require verification or protected evidence reuse, not ceremonial regeneration of unchanged records.
