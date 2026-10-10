# Erdős catalogue processing

The 1,221 `ERDOS-CATALOGUE-####-S01` issues in MATH-PROGRAMME are source/status
audits and bounded-work-design tasks. The protected registry binds each exact
issue number and issue-body SHA-256. Existing Solve dispatches retain their own
reservation, disclosure, intake and execution contracts.

## Intake and disposition

`ci/erdos_catalogue_programme_intake.py` captures authenticated `RESULT/1`
comments from exactly these issues. It checks the issue source lock, repository,
pickup labels, assignment/problem pairing and required report grammar. It
preserves raw text, actor metadata, content hashes, edit revisions and deletion
tombstones. It never executes worker text or follows worker-supplied URLs.

The admitted GitHub Actions controller runs on created/edited/deleted comments,
explicit dispatch and a six-hour reconciliation schedule. Reconciliation scans
repository-wide comments once and fetches only matching catalogue issues.
Captured events, raw versions, receipts and a complete disposition index are
retained as run artifacts for 90 days. Reports are operational evidence;
workflow artifact custody is not protected repository admission.

| Worker-reported disposition | Required next review |
| --- | --- |
| `SOURCE_LOCK_READY` | Source and statement review |
| `BOUNDED_TASK_DESIGNED` | Scope, acceptance test and work-design review |
| `STATUS_CONFLICT` | Status/semantic reconciliation |
| `EXACT_BLOCKER` | Check the precise reported blocker and recovery route |
| `PARTIAL` | Review the partial result and bounded next action |

Structural validity never sets source acceptance, Solve readiness, mathematical
truth, certification or publication. A deleted, malformed, source-mismatched or
conflicting revision remains explicitly review-required. Multiple cooperative
contributors remain visible; the reservation-controlled Solve first-result
lock is not imported into this direct-editorial lane. Context independence is
unverified even when a worker declares `ZERO_CONTEXT`.

Bounded canonical intake must preserve the captured artifact and exact hashes
in an ordinary protected evidence PR before treating custody as canonical.
Source-semantic disposition and a concrete Solve package remain separate
governed transitions. No new general-purpose approval ceremony is created for
routine custody, engineering or metadata work.

## First processing batch

`governance/erdos_catalogue/BATCH-001.json` publishes 32 distinct issue IDs in
eight disjoint cooperative subject slots for authenticated **self-pickup**.
Live activation control: [pilot issue #2503](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2503).
At activation readback on 2026-10-10, 31 pilot assignments had AVAILABLE labels;
Problem 4 ([#1273](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1273))
had a genuine returned `RESULT/1`, routed to [critical source review #2504](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2504).
These are observations, not assumed permanent counts. Runtime owners and
GitHub actors remain null until an independently verifiable authenticated worker
actually begins work. Queue publication does **not** launch eight agents and
must never be used to manufacture runtime identities, lease evidence, or returns.
Workers follow [WORKERS.md](https://github.com/grandchallenge/MATHSOLVE/blob/main/WORKERS.md),
select an AVAILABLE issue, perform its bounded source audit, and return `RESULT/1`
on that issue without `/claim`. Coordinate one worker per task before execution,
particularly when multiple sessions share an authenticated actor.

The batch contains:

- eight original reconnaissance problems, for reuse/reconciliation of protected
  evidence before any new work;
- sixteen additional protected-source open problems;
- four resolved-problem method/provenance audits;
- four informal-open/formal-solution status conflicts.

The existing 593 pinned-kernel/axiom/fidelity residual and 470 historical
generator/format/coverage residual are carried forward by exact protected Solve
reference. No duplicate dispatch, replay, source acceptance or parent-problem
closure is implied. Reconcile current authoritative artifacts before execution.

Prioritize accepted, source-grounded work designs with a small explicit target,
falsification hook, reproducible method and stopping condition. Track source
locks, admissible work packages, checked partial results, eliminated approaches
and cost per accepted result separately from raw issue/comment throughput.

## Operator commands

```sh
python -m unittest tests.test_administrative_erdos_catalogue_intake
python ci/erdos_catalogue_programme_intake.py --live-snapshot --output catalogue-intake
python ci/erdos_catalogue_programme_intake.py --events catalogue-intake/CAPTURED_EVENTS.json --output catalogue-replay
```

For historical edits/deletions, replay the concatenated event streams from the
retained event artifacts. A current GitHub comment snapshot alone cannot recover
a previously deleted body or reconstruct a lost historical revision. Retain
qualified evidence through canonical intake before the artifact expires.

The collector writes local/report artifacts only. It does not change Project
state, close issues, accept a source claim, grant a Solve lease, or certify a
theorem. There is no self-promotion from a worker's return into an accepted
mathematical result.

## Restart and successor gate · 10 October 2026

Initial priority is source/reuse reconciliation for Erdős 99, 101, 138, 241,
470, 593, 595 and 1052. The existing protected MATHSOLVE
`ERDOS-SUCCESSOR-003-ADJUDICATION-001` is authoritative for the 593 kernel
replay and 470 historical generator/coverage residuals. Do not treat catalogue
source-audit offers as duplicate mathematical successor dispatches. The status
of 470 and 593 is **not solved or certified** by this activation.

A current structurally valid worker return is only `CAPTURED_UNADJUDICATED`;
its source evidence, theorem-to-statement semantics, bounded successor and
replay tests require a separate critical disposition. Source-approved bounded
successors enter MATHSOLVE only under its protected packet, dispatch and
execution-lease authority. MATHFORGE and MATHCERT remain separately controlled.
Expansion requires readback of genuine attributable returns, independently
reviewed primary sources, replay/falsification quality and duplicate-work cost.
No fixed calendar date or fabricated throughput condition authorizes expansion.
