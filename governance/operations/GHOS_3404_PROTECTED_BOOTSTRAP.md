# GH-OS #3404 — Protected self-modification bootstrap and restoration

**Record:** `GCL-GHOS-3404-PROTECTED-BOOTSTRAP/1`  
**Date:** 2026-11-16 UTC  
**Status:** successor protected-admitted and routing ruleset restored. This receipt PR is the independently required *post-restoration live native merge-group proof*; do not treat the document's own admission as proof until its exact checks and readback are recorded.

## Authority and exact identity

The Human Steward authorized a one-time, narrowly scoped relaxation of only the GH-OS `routing-enforcement` required-status condition to install the tested protected self-modifying workflow successor. Authorization was recorded in [issue #3401](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3401). This authorization did not permit ordinary enforcement bypass, changing unrelated policy, a direct main push, or mathematical certification.

- Successor [PR #3404](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3404), candidate `5c52b71bb6c30f2c6782b3bce9494ebcd0190643`.
- Protected merge via mandatory native merge queue: `c2ff24fa7cca29978042f1c4c7e719b324f6d240`, admitted 2026-11-16 12:54:49 UTC.
- Exact merge-group candidate and protected merge: `c2ff24fa7cca29978042f1c4c7e719b324f6d240`.
- GH-OS pinned external gate: `grandchallenge/.github` commit `ef1cce6029233a68cf46063cea2384772fcae613`, source SHA-256 `fc0a9a4d20de72e9fbc04c8cd54cffc3a6e4657fb09e7978b360616bd5e94a17`.
- Candidate external pinned routing gate and 31 local GH-OS positive/hostile tests passed. Separate structural adversarial code audit SHA-256 `5fa3cd5e104f6c16f839d3257ea877b7c1afeb4a771c0eff1b2fd7bf2c8ffce7` (internal technical evidence, **not** an external reviewer identity).

## Scoped ruleset transition and restoration

Before changing protection, GitHub's GH-OS ruleset `21969152` was snapshotted. Its enforcement was active on protected `main`, requiring `routing-enforcement`, with no bypass actors and a mandatory one-entry `ALLGREEN` merge queue. Programme ruleset `17137629` remained active with `validate-json`, `formal-validation / formal-validation`, `policy / policy`, and `security / action-policy` required.

The authenticated REST update removed only the GH-OS required-status rule, retaining its mandatory merge queue unchanged and not adding bypass actors. A separate CHAD restoration watchdog was running before that change. PR #3404 entered the native merge queue; all four Programme required statuses succeeded on the exact queue candidate. The GH-OS workflow's self-modification check deliberately failed while it was temporarily non-required. The GitHub-native queue, not a direct protected push, admitted the successor.

Immediately after admission, the original GH-OS required-status rule was restored by authenticated REST and independently read back. GitHub reordered the `merge_queue` and `required_status_checks` entries in its REST response; a strict ordered JSON comparison initially reported a mismatch **after GitHub had already restored the rules**. A second full readback verified semantic equality and the verification code was corrected to compare rule sets independent of their returned ordering. Dedicated ruleset `21969152` is active with required `routing-enforcement`, `strict_required_status_checks_policy=false`, zero bypass actors, and the same one-entry mandatory `ALLGREEN` queue. The independent Programme ruleset remains active with its original four required contexts. The restoration watchdog was disarmed after this readback.

Original ruleset canonical SHA-256 (order-sensitive): `1674dd932061b2710d0d6509bef77e86541f69e2dc019f3d53dbebc750ebdb89`. The byte order of the restored rule-array is different; compare rules by type and parameters, not by array ordering. No temporary weakening remains.

## Actual postmerge behavior and qualification

The protected push on the self-modification commit triggered GH-OS base-refresh [run 43870857611](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/43870857611), SUCCESS. Since the push *introduced the new classifier*, its previous-parent tree did not contain every pinned control input; the classifier correctly failed open and performed the old full refresh (13 open PRs dispatched, 14 GitHub API requests). The first full refresh is not evidence of savings and is not a defect. Subsequent unrelated protected changes are eligible for suppression only after exact control-input tree/blob equality, current live protected-head identity, ancestry and no symlinks have been proven.

The protected source checked out after restoration passes 31 GH-OS routing and refresh hostile tests, including merge-group SHA/ref binding, protected-base ancestry, stale pull-request merge identity, and changed-control/missing-evidence fail-open behavior. `ci/ghos_execution_routing.py` passes. The required live post-restoration proof is a separate genuine documentary PR for this custody receipt, not a dummy commit. Its success requires:

1. A `routing-enforcement` **success** on the PR's exact current head under the fully restored ruleset.
2. An authenticated native merge-group SHA/ref proof, `routing-enforcement` **success** on that exact group SHA, and all other required statuses green.
3. Protected `main` readback with this receipt admitted via the queue.
4. The resulting protected push's GH-OS base-refresh to report `CONTROL_INPUT_BYTES_IDENTICAL`, skip the dispatch job, and make no redundant per-open-PR revalidation calls. If the protected base changes materially before the push, use the truthful fail-open result rather than claiming a saving.

Only after those runtime observations is the control rollout fully qualified. Any missing live evidence remains an explicit qualification boundary, not presumed completion.
