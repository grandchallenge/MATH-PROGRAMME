# GCL recurring-task continuity contract

**Status:** implementation candidate for protected admission. This is a bounded MATH-PROGRAMME operating specialization of `GCL-AGENT-CONTINUITY-001`, not a new authority layer, repository controller, or certification requirement.

## Failure cannot retire the recurrence

A task execution and the recurring schedule that launches it have **distinct lifecycles**. The intended GCL queue-reduction schedule is hourly and enabled. An error in one execution (connector failure, rate limit, blocked tool call, permission issue, no eligible work, or even a successful empty run) cannot disable, replace, or delete that schedule. Execution failures create a classified run outcome with a precise next authorized action. They do not confer scheduler-administration authority.

On an explicit platform safety denial, do not retry, disguise, reroute, or otherwise bypass that rejected action. Preserve the schedule and pursue other authorized, non-duplicative work. The next run rebinds to live protected state and must not replay an already completed mutation.

## Scheduler transitions and audit

A disable/retirement proposal requires an authenticated actor plus a verifiable source for either (1) an explicit user instruction or (2) an already protected, governed terminal disposition with readback. Errors, user silence, the assistant's own diagnosis, an unknown actor, or an absence of immediate queue reductions are **not** retirement instructions. A change record retains previous and new state, UTC time, actor identity, authority reference, reason, host result, and independent scheduler readback. If the provider cannot expose actor or source, report **UNKNOWN** rather than inferring either.

A scheduler observation that differs from protected desired state is **DRIFT**, not successful task completion. Alert and investigate. A genuinely authenticated explicit user disable request must not be automatically undone by a watchdog. Re-enablement requires current desired-state authority and provider readback; do not assume a guarded proposal has actually mutated the host.

## Integration and limitations

`governance/recurring_queue_continuity.json` stores the protected desired-state intent. `ci/recurring_task_continuity.py` is a pure fail-closed transition evaluator, and `ci/test_recurring_task_continuity.py` tests hostile and positive cases. They contain no scheduler credentials, perform no scheduler API calls, and cannot prove who previously disabled a hosted task.

**Present limitation:** the ChatGPT-hosted scheduler is not connected to the GCL persistent controller by a supported readback/administration adapter. Until such an adapter is legitimately available, CI can test policy and event decisions but **cannot detect or repair changes to hosted task state in real time**. Do not label the watchdog operational, durable scheduler enforcement complete, or historical attribution verified on the strength of this policy alone.

A future admitted controller integration must (a) read the actual hosted schedule, (b) emit signed or authenticated immutable transition receipts, (c) detect a missed hourly heartbeat and unexpected disablement, (d) reconcile only with explicit authority, and (e) expose the last successful material queue reduction separately from mere runs and comments. Register any new direct workflow in GH-OS routing before admission. Reuse existing bounded-operation checkpoints for enrolled long-horizon campaigns; do not create a parallel checkpoint registry.
