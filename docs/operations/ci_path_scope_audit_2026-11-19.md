# GCL — MATH-PROGRAMME path-scoping audit, 19 November 2026

**Scope:** Read-only comparative audit of exact PR #3541 and its native merge group, followed by a bounded candidate-side *impact-identity* correction. **No change to protected required checks, native merge queue, full merge-group policy, schedule sentinel, Pages/push rules or authority.**

**Issue class:** CI false-positive invalidation caused by a stale candidate head relative to active protected main. Related, but separate: intentionally exhaustive nine-shard merge-group replay.

## Evidence lock

- Protected rulesets: [Programme profile — main](https://github.com/grandchallenge/MATH-PROGRAMME/rules/17137629) (required `validate-json`, `formal-validation / formal-validation`, `policy / policy`, `security / action-policy`); [GH-OS universal execution routing](https://github.com/grandchallenge/MATH-PROGRAMME/rules/21969152) (mandatory native merge queue, `routing-enforcement` check).
- Exact PR: [#3541](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3541), candidate `8e24fded3b6fd8ed096ce2ff8ef26bafc5dd2fb6`, native protected merge `ed711bd3ea4b49c954880f429eb9ad409a0aecf7`; committed on 2026-11-19 UTC.
- **Actual PR file list:** exactly five files, all in `experiments/erdos249_full_series_phase/` and the registered test `tests/test_erdos249_full_series_phase.py`. Existing governed component [erdos249_full_series_phase.json](../../governance/policy_components/erdos249_full_series_phase.json) owns them and routes `contracts`, `docs`, `repository-regression`, plus mandatory `core`.
- **Observed PR #3541 impact classifier** in [candidate workflow run 44499075920](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/44499075920): six reported paths, including the **unrelated** `fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P3DerivedCM5R0SplitFreeCechDegreeThree.lean`. The classifier consequently selected `core`, `fixtures`, `cmdg`, `contracts`, `docs`, `repository-regression`. `unknown_count=0` does **not** mean the selected paths all originated from this PR.
- The candidate base/head comparison was divergent (10 commits ahead, 3 behind in GitHub's comparison at the inspected current base), whereas GitHub's PR changed-files API enumerated only the five research files. The stale two-tree diff included an unrelated main-side formal fixture **in reverse**, and the then-current code used `git diff base head` rather than a verified merge result.
- **Observed native merge-group workflow** [run 44499681977](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/44499681977), exact merge `ed711bd3ea4b49c954880f429eb9ad409a0aecf7`: nine shards plus queue-cutover, impact classification and `validate-json`; all succeeded. This full fanout is explicitly returned by `classify_paths(...,event_name="merge_group")` and required by the current control tests.

## Measured cost — source data, not conjectural reduction

The two job sets below were obtained from the native GitHub Actions jobs API, using each completed job's `started_at` and `completed_at` timestamps. They are *runner elapsed seconds*, not billable-minute invoices or additive critical-path latency.

| Policy shard | Candidate PR #3541 (s) | Native merge group (s) |
| --- | ---: | ---: |
| core | 18 | 13 |
| fixtures | **16** | 15 |
| cmdg | **143** | 87 |
| oz | not run | 39 |
| administrative | not run | 18 |
| campaigns | not run | 34 |
| contracts | 76 | 71 |
| docs | 38 | 46 |
| repository-regression | 55 | 71 |
| **Total shard runner seconds** | **346** | **394** |

**Confirmed avoidable candidate work:** fixtures 16 + CMDG 143 = **159 runner-seconds = 2.65 runner-minutes** for this exact PR, roughly **46% of candidate shard runner time**. Because shards run concurrently, the candidate's critical path was approximately 143 seconds (CMDG) after classification; the remaining longest relevant shard took 76 seconds. Thus the observed job timings suggest, but do **not** guarantee, a potential **67-second reduction in candidate critical-path time** when this same divergence pattern recurs. Network queuing, setup overhead and concurrency can change wall-clock realization.

**Still intentionally required:** merge-group 394 shard runner-seconds, including every formerly unrelated shard, because the current protected control expressly requires full merge-group coverage. The present change does not remove any of that work.

## Root cause and safe candidate correction

The previous event path function extracted `pull_request.base.sha` and `pull_request.head.sha` and ran `git diff --name-only base head`. In a stale-head/concurrently advancing-main case, comparing those two **trees** lists both candidate changes and protected-main-only changes, the latter in reverse. Such false-positive paths trigger unrelated invalidations. The PR's effective synthetic merge commit, when available, has exactly two parents: the event's protected base SHA and candidate head SHA. Comparing that verified merge's tree to its first parent reports the **real changes introduced by the candidate on that protected base**.

The bounded correction:

1. Reads GitHub event `pull_request.merge_commit_sha` only for `pull_request` classification.
2. Uses `git rev-list --parents -n 1 <merge>` and accepts the merge only if its identity and ordered parents are **exactly** `[merge_sha, base_sha, head_sha]`.
3. On success, derives changed paths from `git diff --name-only base_sha merge_sha`.
4. On a missing, unavailable, one-parent, stale-parent or otherwise invalid merge, **falls back to the original broad** `git diff base head`. It never treats missing evidence as a no-op.
5. Uses the **same selected exact tree transition** for the mathematical Markdown source gate and newly added test-route registration check. This avoids inconsistent paths being classified, source-checked and registered.
6. Does not modify `classify_paths` shard ownership, unknown-path `FULL_FANOUT`, control-plane full invalidation, any protected rule, the `merge_group` full fanout, main-push Pages building, or full-policy sentinel.

The exact-merge choice is conservative with respect to the changes that would land on protected base: its diff is the complete tree change relative to its first parent, rather than a heuristic name filter. On identity drift, the safer broad behavior is retained.

## Hostile acceptance and non-regression

The updated `ci/test_policy_impact.py` constructs a **real temporary Git DAG** with a feature branch adding an Erdős research file, then a concurrently advancing main branch adding an unrelated CMDG formal fixture, followed by an exact two-parent synthetic merge. Its assertions cover:

- The old two-tree comparison incorrectly includes both the Erdős and CMDG paths.
- The verified exact merge includes **only** the genuine Erdős material path, selecting `core`, `contracts`, `docs`, `repository-regression` with zero unknown paths.
- Missing merge, one-parent substituted head and unresolvable merge SHA all revert to the original broad comparison, never to an empty/no-op path set.
- Full nine-shard `merge_group` routing and full fanout on changed classifier/control-plane source remain enforced.
- All original policy-routing and mutation-hostile controls remain exercised.

**Independent local bounded replay:** exact candidate source `ci/policy_impact.py` and `ci/test_policy_impact.py` passed `python3 ci/test_policy_impact.py` and `python3 ci/policy_impact.py validate` in an isolated CHAD workspace after hydrating pinned source dependencies. No production workflow or protected setting has been changed by that replay. Fresh protected CI and native merge-group validation remain the admission mechanism.

## Residual risks, no-op paths and follow-on options

- **Risk 1 — GitHub merge-ref staleness or absence:** The identity check will reject it and use broad fallback. The control does not optimize such an event, but preserves coverage. The separate GH-OS effective-candidate controller and native merge group still enforce exact current-state admission.
- **Risk 2 — real cross-programme source changes:** Correctly selected; no source change is omitted when its exact merged tree differs from base. The existing policy manifest dependency closure remains active.
- **Risk 3 — unregistered new tests or unknown material:** The new-test route guard and `FULL_FANOUT` remain; protection fails rather than silently accepting an unregistered test route.
- **Risk 4 — unconditional full merge group:** It is the largest structural remaining expense. Any eventual selective merge-group policy would require a separately governed proof of equivalent coverage, replay of hostile drift and dependency cases, preservation of `validate-json` and matching required rulesets. **Not authorized or attempted here.**
- **Risk 5 — runner/package setup duplication:** A separate source-locked timing study could assess dependency caching or immutable environment reuse, but no external mutable cache trust boundary is introduced in this work package.

**Rollback:** Revert only the `verified_pull_request_transition` helper and its uses in `changed_paths_from_event` and the two source/registration checks. The original `git diff base head` conservative comparison and all required workflows then operate as before. There are no secrets, branch settings, third-party deployment targets or site artifacts to roll back.

**Disposition:** Candidate-side PR impact identity defect addressed, **without reducing governance**. Native required protected checks must still pass at the current exact head and full merge-group replay must still succeed before protected admission. The full nine-shard merge-group cost is documented as a genuine governance-boundary trade-off, not silently called a bug.
