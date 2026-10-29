# GCL cross-project authenticated operation recovery

**Scope:** Every GCL repository, controller, scheduled worker, council role and connected execution surface. This is an implementation profile of the protected [operation-scoped recovery policy](OPERATION_SCOPED_RECOVERY_POLICY.md), not permission to bypass a denial. Inherit higher-priority platform constraints and repository protection.

## Mandatory operation contract

Before a consequential external operation, record: task/work-item identity; repository and protected source SHA; operation kind (READ, DISPATCH, WRITE, REVIEW, MERGE); exact inputs, target, idempotency key where available; preconditions; authorized actor and surface; expected observable remote result. For long-horizon jobs, persist this in existing continuity artifacts rather than creating a new registry.

For every invocation distinguish **request sent**, **local tool execution**, **remote effect observed**, **provider acknowledgment delivered**, **protected admission**, and **scientific/certification validity**. A command exit code alone proves none of the later stages. When available, correlate operation ID, GCL CONTROL run ID, provider request/run ID, receipt digest, and delivery acknowledgment; label unavailable dimensions UNKNOWN.

## Shared recovery state machine

1. **SUCCESS + readback:** verify exact remote identity (run/PR/commit/artifact/scheduler state), reconcile durable record and advance work. Do not replay.
2. **TRANSIENT / UNAVAILABLE / TIMEOUT / MALFORMED / ambiguous transport failure:** bounded health probe and retry on an independently confirmed healthy path. Before replaying any potentially mutating operation, query authoritative remote state using its identifying parameters and reconcile ambiguous outcomes. If readback is unavailable, keep mutation **UNCERTAIN**, do not redispatch, and continue unrelated permitted work.
3. **Explicit policy or platform DENIAL:** put the *exact rejected invocation* on hold. Do not retry, repackage, translate, or reroute that denied action through another transport. Carry on only genuinely independent authorized operations.
4. **Authority, mathematical, security, or protected-gate blocker:** retain the relevant hold; use existing review and governance routes rather than weakening controls.
5. **Repeated service defect:** aggregate evidence into one classified incident per defect (operation, time, correlation, tool error, remote outcome); do not create duplicate tickets or presume cause without evidence.

Fallback between authenticated transports is allowed **only for technical availability failures**, not explicit denials; the replacement must have the correct delegated authority and be auditable. GitHub connector may read/write GitHub within its capabilities when CHAD/GCL CONTROL transport is unavailable; never assert it repaired CHAD itself. Prefer narrowly scoped connector operations to relying on a single generic shell interface.

## Concurrency, idempotency and resumption

At the start of each worker iteration, rebind live protected policy, current main SHA, active/completed runs and protected evidence ledger. Derive work eligibility from **both** admitted artifacts and in-flight dispatches, not an agent's previous message. Cap concurrency at the campaign's protected limit. An uncertain submission occupies its slot until resolved. An operation must be uniquely associated with immutable target parameters; repeat only after proving absence of the first remote effect. Use exact-head merge and protected readback. Preserve failures and retry disposition in the existing work-item/issue record.

For recurring tasks, a failed iteration does not retire its schedule; use [recurring task continuity](RECURRING_TASK_CONTINUITY_CONTRACT.md). Do not infer worker health from schedule enablement, or scheduler delivery from a GCL local execution receipt. A separate heartbeat/readback observer is required where available.

## Agent reporting and acceptance tests

Report separately: completed and remotely verified work, requested/in-flight work, uncertain mutations, held invocations, remaining substantive obligations and next authorized action. Never advertise a technical fallback as independent mathematical review.

Test these scenarios for every campaign-specific controller: lost response after successful dispatch (no duplicate), transient read failure with alternate healthy connector, explicit denial (no alternate path to same denied mutation), replay of a completed operation (no effect), concurrency-slot exhaustion, expired/stale evidence against moved main, and failed scheduled run (schedule preserved).

**Rollout:** Every GCL worker prompt and controller implementing external mutations must incorporate this contract on its next governed revision. Existing workers must follow it immediately through umbrella policy; repositories may specialize without weakening its denial, idempotency, readback or protected-admission boundaries. Integration evidence must cite actual runnable tests or live receipts, not merely a policy file.
