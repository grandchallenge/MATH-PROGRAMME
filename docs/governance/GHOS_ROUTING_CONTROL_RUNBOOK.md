# GH-OS routing control runbook

## Purpose

This runbook governs MATH-PROGRAMME's mandatory execution-routing control. The control is self-policing, not self-authorizing. It detects coverage, capability, topology, controller, identity, and enforcement drift.

Routine workflow maintenance follows the standing delegated execution model. A legitimate routine change does not require fresh Human Steward or generic independent approval merely because its commit is new. Security-sensitive weakening, external gate authority changes, controller capability expansion, merge-queue admission changes, or temporary removal of protected enforcement remains a reserved control-plane boundary and receives the specialist or Human Steward authority required by that exact action.

This runbook grants no certification, mathematical-claim, publication, external-claim, or protected-bypass authority.

## Control surface

| Surface | Purpose |
| --- | --- |
| `.ghos-routing/workflows.json` | Complete workflow inventory, derived features, topology, controller, and fixed authority boundaries |
| `ci/ghos_execution_routing.py` | Repository-local deterministic validator |
| `schemas/ghos_execution_routing.schema.json` | Closed routing-record schema |
| `tests/test_ghos_execution_routing.py` | Core hostile semantic tests plus pre-queue, merge-group, base-advance, and enforcement-contract regressions |
| `.github/workflows/ghos-routing-enforcement.yml` | Protected pre-queue controller, native merge-group admission controller, and protected-base revalidation dispatcher |
| `grandchallenge/.github/scripts/ghos_execution_routing_gate.py` | External governed gate whose bytes are SHA-256 pinned by the enforcement workflow |
| Ruleset `21969152` | Dedicated protected-main requirement for `routing-enforcement` and mandatory native merge queue |
| Ruleset `17137629` | Separate Programme profile; not the GH-OS routing ruleset |

The dedicated routing ruleset requires `routing-enforcement` with `strict_required_status_checks_policy: false`, zero bypass actors, and a mandatory native merge queue. Non-strict status policy remains deliberate. Freshness is supplied by the merge queue's queue-owned candidate rather than update-branch synchronization.

The same required context has two distinct stages:

1. **Pre-queue eligibility.** The protected `pull_request_target` controller validates the current effective PR candidate and publishes `routing-enforcement` to the PR head. This status permits queue entry only. It is not final merge authority.
2. **Final protected admission.** GitHub creates a `merge_group` candidate against the current target state. The merge-group controller evaluates that exact queue-owned SHA and publishes `routing-enforcement` to it. The mandatory merge queue may merge only after the required checks pass on that merge group.

A head-bound routing success is safe only while the merge queue remains mandatory. Never treat a head-bound status as permission for direct protected merge.

## Exact self-protection boundary

Ordinary candidates cannot modify `.github/workflows/ghos-routing-enforcement.yml`. The protected pre-queue controller compares that workflow's bytes in the effective candidate with the bytes on current protected `main` and rejects any ordinary candidate difference.

This is deliberately narrower than a blanket ban on `.github/workflows/`. Other workflow files may be added, changed, renamed, or removed through ordinary governed development. Such changes must still satisfy complete routing inventory coverage, byte-derived feature equality, topology, controller compatibility, authority boundaries, and all materially affected protected checks.

Do not describe this control as making every workflow immutable.

## Routine workflow maintenance

When adding, deleting, renaming, or changing a workflow:

1. Run `python ci/ghos_execution_routing.py`.
2. Update exactly one corresponding entry in `.ghos-routing/workflows.json`, or remove the stale entry when deleting a workflow.
3. Use the exact feature list and topology derived from workflow bytes. Do not weaken or over-declare them manually; the shared gate requires equality with its byte-derived result.
4. For any non-`BOUNDED_ATOMIC` workflow, use the exact admitted controller and confirm that all derived features are supported. Otherwise decompose the operation into independently recoverable bounded workflows.
5. Run the focused routing and semantic tests needed by the changed control. Current policy impact routing selects the additional protected shards actually affected.
6. Required workflows that participate in protected merge admission must report their required checks on `merge_group` candidates. Do not add a required check that cannot execute on merge groups.
7. Merge through protected controls under standing delegated authority when the change is routine, queue-admissible, and does not weaken or expand the protected control boundary.

The expected maintenance burden is one routing-entry update per workflow change plus affected validation. The gate supplies the authoritative diagnostic when the entry drifts.

## Pre-queue candidate-independent enforcement

The pre-queue enforcement workflow executes protected controller logic from protected `main` under `pull_request_target` or protected `workflow_dispatch`. Candidate content is inert data and must never be executed under the privileged controller.

For each pull request targeting `main`, the controller:

1. checks out current protected `main` with credentials disabled;
2. reads the current pull-request identity through the GitHub API;
3. fetches `refs/pull/<number>/head` and `refs/pull/<number>/merge` as data;
4. accepts the test merge only when its two parents are exactly current protected `main` followed by the current PR head, and the API-reported test-merge identity equals the fetched identity;
5. retries the synthetic merge identity a bounded five times, recording resolution attempts and elapsed time;
6. fails closed when GitHub cannot supply that exact current effective candidate;
7. materializes the verified merge tree without executing candidate-controlled programs, actions, hooks, scripts, dependency declarations, or workflows;
8. compares the effective candidate's GH-OS enforcement workflow bytes with protected `main` and rejects ordinary self-modification;
9. verifies the content-addressed external gate and runs that gate only against the inert effective-candidate tree;
10. re-fetches protected `main` before admitting the gate result and fails if the protected base moved during evaluation; and
11. publishes the required pre-queue `routing-enforcement` status to the PR head.

The head status means only: the current PR head passed protected pre-queue routing evaluation against the then-current effective candidate. Protected-base revalidation refreshes this evidence after `main` movement. A stale head status can at most permit queue entry; it cannot authorize final merge because the merge queue itself is mandatory.

## Native merge-group final admission

GitHub documents `GITHUB_SHA` for `merge_group: checks_requested` as the merge-group SHA and `GITHUB_REF` as the merge-group ref. The final controller uses those queue-owned identities directly.

For each merge-group event, the controller:

1. checks out current protected `main` with credentials disabled;
2. requires `GITHUB_REF` to be under `refs/heads/gh-readonly-queue/main/`;
3. fetches that exact queue ref and requires the fetched SHA to equal `GITHUB_SHA`;
4. requires current protected `main` to be an ancestor of the merge-group SHA;
5. materializes the merge-group candidate as inert data;
6. requires the candidate's GH-OS enforcement workflow bytes to equal current protected `main`;
7. verifies the same pinned external gate and executes it only against the inert merge-group tree;
8. re-fetches protected `main` after evaluation and rejects the result if the protected base moved; and
9. publishes `routing-enforcement` to the exact merge-group SHA.

GitHub, not an external bot, performs the final merge after all required checks pass on the queue candidate. This removes reliance on the ephemeral `refs/pull/<number>/merge` SHA for final admission and closes the post-status/pre-merge freshness gap by making the queue-owned candidate the final unit of admission.

If the merge-group ref, SHA, protected-base ancestry, protected workflow bytes, gate digest, gate result, or post-gate protected-base identity cannot be proven, the required context fails closed.

## Protected-base refresh and telemetry

On every push to protected `main`, the protected workflow enumerates open PRs targeting `main` and dispatches fresh pre-queue evaluation without mutating candidate branches.

The dispatcher records:

- open PR count;
- dispatched revalidation count;
- GitHub API call count; and
- dispatch elapsed time.

The pre-queue identity resolver records:

- bounded resolution attempt count;
- resolution elapsed time;
- protected-base SHA;
- PR-head SHA; and
- resolved synthetic merge SHA, or the final fail-closed identity diagnostic.

This telemetry is evidence for later scalability decisions. Do not introduce naive path-overlap filtering. Any future reduction in revalidation must prove that the protected-base delta cannot affect GH-OS gate inputs or routing semantics.

## Programme required checks on merge groups

Every context required by Programme ruleset `17137629` must also execute on merge-group candidates. The Programme policy workflow therefore accepts `merge_group: checks_requested` and conservatively routes merge-group events to full policy and formal replay closure. `GCL conformance` already accepts `merge_group` events.

Do not optimize merge-group policy impact until the event inputs used for narrowing are themselves governed and tested. A merge-group event with uncertain material delta receives full validation rather than accidental attestation reuse.

## Merge-queue configuration

The initial protected queue configuration is intentionally conservative:

- `grouping_strategy: ALLGREEN`;
- `max_entries_to_build: 1`;
- `max_entries_to_merge: 1`;
- `min_entries_to_merge: 1`;
- `min_entries_to_merge_wait_minutes: 0`;
- `merge_method: MERGE`; and
- `check_response_timeout_minutes: 60`.

One entry per build and one entry per merge keeps the first admitted queue behavior equivalent to a single-candidate control. `ALLGREEN` requires the complete merge-group candidate to pass. The 60-minute timeout exceeds the current longest individual Programme job timeout of 50 minutes while retaining a bounded fail-closed backstop. Increase queue concurrency only from measured telemetry and through governed ruleset change.

## External gate and digest rotation

An external gate semantic change is a control-plane upgrade rather than ordinary workflow maintenance.

1. Change and test the gate in `grandchallenge/.github` through its protected path.
2. Record the merged gate commit, exact script blob, SHA-256, test evidence, compatibility statement, and affected repositories.
3. Prefer a versioned successor path while the prior pinned path remains available when consumers require staged migration.
4. Prepare the smallest consumer update containing the justified pin or path change and necessarily synchronized local validator, schema, tests, controller catalog, registry, or documentation.
5. Obtain specialist non-author review when the change alters security-sensitive enforcement semantics, controller authority, or another reserved boundary.
6. Follow the protected self-modification procedure when active self-protection makes ordinary protected admission impossible.
7. After a material enforcement upgrade, run focused hostile proof that candidate-controlled local validation cannot bypass the protected external gate.

A digest mismatch is an expected fail-closed condition. Never solve it by removing the digest check, following an unpinned branch, or executing candidate code.

## Protected self-modification procedure

The active enforcement workflow rejects candidate modification of itself. A legitimate successor that therefore requires temporary relaxation of the dedicated routing rule crosses a security-sensitive protection boundary and is not routine delegation.

1. Freeze only the affected workflow-control mutation while preparing the bootstrap. Unrelated bounded read-only or disjoint work may continue.
2. Record protected-main identity, dedicated routing ruleset `21969152`, required context, merge-queue rule, bypass actors, enforcement-workflow blob, external gate identity and digest, and separate Programme ruleset `17137629`.
3. Obtain the reserved authorization required for the exact temporary weakening, successor control bytes, and ruleset successor. Do not add a bypass actor or weaken unrelated rules.
4. Remove or disable only the routing requirement necessary for the bootstrap. Preserve every other applicable protected rule.
5. Merge only the authorized material successor after all other affected checks and specialist review required by the security boundary pass.
6. Immediately restore ruleset `21969152` active with `routing-enforcement`, `strict_required_status_checks_policy: false`, zero bypass actors, and the exact authorized mandatory merge-queue configuration.
7. Read back the complete ruleset, protected merge, enforcement blob, Programme required workflows, registry, validator, external digest, and post-merge checks.
8. Execute a live merge-group proof and focused hostile proof before declaring the control restored.
9. Re-run the #881 stale-C1 TOCTOU assurance on the native queue path.
10. Record before and after protection identity and the material authorization in the governing issue or protected evidence record.

If the successor identity, reserved authorization, ruleset snapshot, merge-queue configuration, or restoration route is unavailable, stop. Do not leave the routing requirement disabled while diagnosing an unrelated failure.

## Ruleset care

After routing administration or a material control upgrade:

1. Read dedicated routing ruleset `21969152` from GitHub.
2. Confirm it is active on `refs/heads/main`.
3. Confirm `routing-enforcement` is required with `strict_required_status_checks_policy: false`.
4. Confirm the mandatory merge-queue rule matches the protected configuration.
5. Confirm bypass actors remain empty.
6. Confirm pre-queue routing is present on an eligible PR head only as queue-entry evidence.
7. Confirm final routing is present on the exact current merge-group SHA before protected merge.
8. Read Programme profile `17137629` separately so a routing transaction cannot silently weaken unrelated Programme protections.
9. Open a bounded repair immediately on material drift. Pause only the affected unattended transition if enforcement is no longer mandatory.

Never interpret a head-only routing success as final protected admission.

## Emergency diagnosis

Use this order when `routing-enforcement` fails:

1. Identify the stage: pre-queue or merge-group.
2. Bind the failure to repository, protected-base SHA, PR head or merge-group SHA, workflow run, external gate digest, and emitted status context where available.
3. Classify the first exact error: unavailable or stale PR merge ref, merge-parent mismatch, unexpected queue ref, merge-group SHA mismatch, protected-base ancestry failure, protected-base movement during evaluation, self-modification, external digest failure, gate failure, status-publication failure, revalidation-dispatch failure, dependency failure, queue timeout, or platform outage.
4. For a stale or unavailable PR merge ref, retain the required context and retry through the protected pre-queue controller. Do not infer success.
5. For a merge-group failure, allow the native queue to regenerate the candidate after the underlying condition is corrected. Do not copy a status from a PR head or older merge group.
6. For an external digest mismatch, verify the protected shared script and change history; use the control-upgrade route rather than changing the pin ad hoc.
7. For a platform outage, leave the gate and merge queue required. Do not infer success from absence of a result.
8. For unexpected ruleset drift or missing queue enforcement, pause affected protected admission until the control is restored and proven.

Never solve an emergency by executing untrusted candidate code under `pull_request_target`, granting candidate content write credentials, adding a routing bypass actor, removing the merge queue while relying on head-bound routing success, or carrying approval to materially changed security-control bytes.

## Periodic and sentinel evidence

After every material control upgrade, and through existing scheduled or manual assurance rather than a separate timer, retain or verify as appropriate:

- current protected-main and enforcement-workflow identities;
- successful workflow inventory and coverage validation;
- external gate commit, path, and digest;
- dedicated routing ruleset identity, required context, merge-queue configuration, strictness, and bypass actors;
- pre-queue status placement and current effective-candidate identity;
- final merge-group status placement and queue-owned candidate identity;
- separate Programme-profile readback where routing administration occurred;
- focused hostile-test results, including relevant and disjoint protected-base movement;
- synthetic-ref resolution and base-refresh telemetry; and
- live fail-closed proof outside candidate control.

Routine periods with no workflow, controller, gate, or ruleset change require verification or protected evidence reuse, not ceremonial regeneration of unchanged records.