# GCL-CI-EFF-003 — Formal fanout dependency and shadow replay

**Candidate status:** Guarded narrow correction, subject to protected exact-head CI and merge-queue replay. Not public mathematical certification.

**Source baseline:** protected `main` commit `505bdbbda91ce18892a85e0d9b42995f0cf0f8be` (2026-11-16). The candidate changes to `ci/formal_validation.py` and `governance/formal_validation_registry.json` are themselves full-fanout changes and must undergo the **original complete** 15-lane replay before admission.

## Actual execution graph

The formal validation workflow has an impact classifier, a conditional lane matrix, a fail-closed aggregate job, and the required `formal-validation / formal-validation` status. The matrix contains 15 lanes: twelve CMDG Lean closure jobs, LOG-GCD, PC-WP04 and Union-Closed/MATHCERT. The registry retains its 23 pre-existing full-fanout patterns, shared CMDG triggers, toolchain constraints, and all material-lane patterns. The schedule still runs the three legacy lanes; `workflow_dispatch` still selects all fifteen. The separate protected CMDG full replay remains scheduled.

The executable Python dependency graph starts from the router and **all** lane validator commands, including the twelve `python -m unittest tests.test_cmdg_*` invocations. It follows source imports under `ci/`, `tests/`, `campaigns/`, and `fixtures/`. At baseline, this closure contains **52** Python files. The PC-WP04 fixture also runs a validator from its manifest; the dependency guard resolves that script and verifies its expected Git blob before allowing a reduced lane set. The external MATHCERT checkout and Lean/mathlib setup remain pinned and unchanged.

The guard recomputes these dependencies from the exact candidate checkout. It refuses an exemption if a formal executable imports any contract-only module, if a source is absent or unparseable, if the PC-WP04 script does not match the locked blob, or if a required contract test is not registered in the governed `contracts` shard. Unknown dynamic imports and unreviewed subprocess execution also refuse the exemption. A refusal selects all fifteen lanes.

## Bounded routing correction

Only these six **already registered** non-formal contract files can be exempted from automatic full formal replay, and only when they are the **only** full-fanout hits:

- `ci/validate_workflow_coverage.py`, `ci/validate_workflow_coverage_v2.py`
- `ci/test_workflow_coverage.py`, `ci/test_workflow_coverage_v2.py`
- `ci/validate_workflow_semantics.py`, `ci/test_workflow_semantics.py`

The four existing wildcard/exact patterns remain present in the registry. The exception is an exact filename allowlist checked before their usual full-fanout handling. New filenames such as `ci/validate_workflow_coverage_v3.py` remain full-fanout. A mixed change containing any other full control path also remains full-fanout. Changes to the dependency guard, its tests, the formal router, the workflow, the registry, its schema, toolchains, environment, or the protected release policy all trigger full replay.

If a contract file changes together with a known LOG-GCD, CMDG or PC-WP04 material source, the material lane still executes. Unclassified formal sources remain errors. The required status context still checks that the material classifier succeeded and that the lane matrix was either completed exactly or legitimately skipped. Existing required policy tests validate the workflow contract code separately from Lean compilation.

**Additional correction found during audit:** the old Git diff reader omitted deletions and did not retain the original path of a rename. The candidate uses NUL-delimited name/status records and includes deleted paths and both rename paths. A deleted/renamed managed formal source therefore cannot evade lane classification through an omitted pathname. Real temporary-Git regression tests verify these cases.

## Historical counterfactual replay

Run `python3 tools/formal_fanout_shadow.py --commits 350 --output <path>` from the source worktree. This reads only the Git history and reclassifies 350 first-parent transitions using the original protected registry and the candidate guard; it does **not** launch 350 CI jobs. The full records are stored in CHAD evidence:

`/home/jim/gcl-evidence/ci-efficiency-20261116/formal_shadow_350_candidate.json` — SHA-256 `e996dc978e58fe7eb4e9477492f07979bbc4e82ffcfdf87ce4d4a15219c1f892`.

| Replay disposition | Transitions |
| --- | ---: |
| Exactly unchanged formal lane selection | 347 |
| Old full 15 lanes; candidate safely excludes unrelated formal lanes | 3 |
| Other lane omissions or unresolved classifications | 0 |

The three affected protected merge commits were `2649062eb193…`, `29b6b1507b70…` and `4ede30f1d6fa…`. All three changed contract checks but no other full-fanout control or mathematical material. This is a counterfactual using the **current** registry against historical changes; it is not a claim that every old repository revision used the current policy.

## Measured cost and limitations

Three corresponding historical successful merge-queue runs were read through bounded GitHub REST requests:

| Run | Formal lanes executed | Sum of formal-lane elapsed minutes | All-job elapsed minutes |
| --- | ---: | ---: | ---: |
| [43833734098](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/43833734098) | 15 | 35.935 | 36.468 |
| [43827513479](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/43827513479) | 15 | 37.001 | 37.401 |
| [43818012198](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/43818012198) | 15 | 35.617 | 36.150 |
| **Total** | **45** | **108.553** | **110.019** |

Source receipt: `/home/jim/gcl-evidence/ci-efficiency-20261116/formal_full_fanout_cost_3_runs.json`, SHA-256 `172086c79e741179d72b436f2b8331eac04aa6d1e0abe6be2cf973ed9ae1aac6`.

These minutes are **summed elapsed runtimes across parallel jobs**, not billed GitHub runner minutes or calendar-time savings. Future savings are unknown until post-merge measurement. Exact historical outcomes cannot substitute for candidate protected merge-queue replay.

## Acceptance, rollback and evidence boundaries

- Execute `ci/test_formal_validation.py`, `ci/test_formal_contract_dependency.py` and `tools/formal_fanout_shadow.py` against the candidate exact head. Require full protected CI, all fifteen formal lanes, policy/security checks, and merge-queue replay before admission.
- Hostile tests must fail open to all lanes for unregistered contracts, a changed formal Python dependency, dynamic import, missing policy test, altered PC-WP04 replay input, new formal paths and other full controls.
- After admission, observe a contract-only PR: the impact classifier must succeed; the formal lane matrix must be skipped; the required status must still succeed; policy/coverage tests must run. Observe a mathematical-source PR to verify its lane is not skipped.
- **Rollback:** remove the contract-only exception from `ci/formal_validation.py` (or make its guard return `(False, "REPLAY_ALL")`). The original 23 registry patterns are unchanged, so this restores full replay without changing branch protection or historical evidence.
- Do not claim publication-level certification, provable lower billing costs, or a general safe relaxation of full formal fanout. Only the six exact filenames have an audited non-formal execution separation.
