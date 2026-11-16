# ERDOS-PV-DISPATCH-001 — bounded one-shot worker pickup

## Scope and authority

The canonical programme ledger is `governance/erdos_proof_verification/coverage/REGISTRY.json` and its protected cohort packets. The current selection contract is `ci/erdos_pv_queue.py`; the authenticated GitHub ref claim, typed return and protected release contract is `ci/erdos_pv_worker_lease.py`.

`ci/erdos_pv_dispatch_once.py` adds one **bounded controller-call adapter**. It is not a persistent scheduler, independently executing research agent, mathematical referee or Project V2 projection controller. No GH Actions workflow, automation, recurring schedule, or permission is added or changed.

## Calls

Run from a clean checkout whose cohort packet bytes match protected `main`, with authenticated `gh` access:

```bash
python3 ci/erdos_pv_dispatch_once.py inspect --last-served-phase D --scan-limit 5
```

This is live read-only selection. It checks the source-locked per-task identity, existing held claim ref, open/available issue labels, protected cohort blob and prior exact `RESULT/1`. It rotates phases in `A, B, C, D` order after the last **actually serviced** phase; a caller must retain that cursor under its own durable controller state. A held ref is *never* removed or stolen by this adapter. A stale issue projection or already-present result returns `RECONCILIATION_REQUIRED` and blocks further selection during that pass; ambiguous transport failures fail closed.

Only an authorized execution controller with a ready worker should call:

```bash
python3 ci/erdos_pv_dispatch_once.py claim --last-served-phase D --scan-limit 5
```

`claim` re-runs the existing live preflight and creates the native atomic GitHub reservation; a successful exit means only `CLAIMED_HANDOFF_ONLY`. It is not evidence of execution, `RESULT/1` submission, independent review, custody or protected admission. A lost race or uncertain response is `CLAIM_RACE_OR_UNCERTAIN` and must be reconciled against the exact GitHub ref and issue before any repeat. A failed read after attempted claim has `mutation=UNKNOWN_IF_CLAIM_ATTEMPTED`, **not** a proven no-op. Do not retry `claim` blindly.

The same issue represents multiple per-problem tasks; do not close cohort issues when a single task completes. The existing release command requires exact admitted status, evidence, actor, receipt, protected ancestry and unique result before deleting a claim.

## Acceptance boundary and remaining work

The adapter is an engineering increment on [ERDOS-PV-DISPATCH-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3265), not closure of that issue.

Remaining substantive obligations:

- Connect it to the **already authorized persistent controller**, with durable per-stage cursor and fairness across long-held / out-of-window candidates; avoid new schedules and duplicate native GitHub queue machinery.
- Bind selection to exact GCL Project #2 Mathematics item discovery and projection, not only GitHub issue labels. Reconcile stale Project V2 views or label changes before claiming.
- Demonstrate real unattended worker execution, typed `RESULT/1` return, interruption/restart, contested claim, source change, missing source, explicit-denial hold, zero-progress alarm, bounded recovery and exact protected admission/release.
- Read back protected manifest and queue status after the worker's full cycle. Original global theorem adjudication and MATHCERT remain separate.

## Verification record

On the candidate checkout based on protected commit `0f86940c4c318574f0f2fbe98e2ebe5850f598ff`, live **inspect** (no claim) selected `ERDOS-PV-0002-A`, source issue #1271, queue issue #3212, protected cohort blob `e9c6a2dbec8f6b594e0e3d2762a3da00c3fefab5`. GCL_CONTROL capture ID `ebede077c163486c812592d643e5b6af`; this capture attests only local CHAD execution, not unattended execution.

Candidate tests: `python3 ci/test_erdos_pv_dispatch_once.py`, `python3 ci/test_erdos_pv_worker_lease.py`, `python3 ci/test_erdos_pv_queue.py`; full 1,221-problem validator `ci/validate_erdos_pv_full_coverage.py`. These are source and unit checks, not a general live worker acceptance test.
