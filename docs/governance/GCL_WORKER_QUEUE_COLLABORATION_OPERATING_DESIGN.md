# GCL Worker Queue and Collaboration Operating Design

**Policy ID:** GCL-WORKER-QUEUE-001  
**Version:** 1.0.0  
**Status:** active bounded operating design on protected admission  
**Owner:** MATH-PROGRAMME  
**Implementation target:** MATHSOLVE

## Purpose

GCL-WORKER-QUEUE-001 defines a governed worker-discovery and collaboration layer for bounded mathematical work. It removes manual prompt copy/paste from worker pickup while preserving the authority, provenance, and claim boundaries of the existing dispatch, lease, launch, RESULT/1, intake, adjudication, and certification machinery.

The queue is an operational surface. It is not a proof stage, approval mechanism, claim ledger, or certification route.

## Governing doctrine

This operating design is subordinate to the current protected MATH-PROGRAMME doctrine, including:

- `docs/MATH_PROGRAMME_AGENT_COUNCIL.md`;
- `docs/AGENT_COUNCIL_GOVERNANCE.md`;
- `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`;
- `docs/governance/STREAMLINED_EXECUTION_AMENDMENT.md`;
- `GCL-AGENT-STAFFING-001@1.0.0`;
- `GCL-AGENT-CONTINUITY-001@1.0.0`.

This design creates no new mathematical, certification, publication, protected-bypass, Human Steward, Referee, Council, or external-claim authority.

## Architectural rule

The worker queue sits above the existing execution contract:

```text
worker discovery / reservation
            |
            v
protected dispatch + protected execution lease
            |
            v
immutable launch artifact
            |
            v
worker RESULT/1
            |
            v
controlled intake -> protected evidence -> adjudication
```

A worker reservation and a protected execution lease are distinct objects.

- The protected execution lease answers: **may this dispatch execute?**
- The worker reservation answers: **which authenticated worker is currently working on it?**

A reservation MUST NOT create, extend, revive, or widen execution authority. A dispatch is self-claimable only when protected repository state explicitly opts it into the queue.

## Worker-facing pickup contract

A self-claimable dispatch is exposed through a GitHub-native queue surface. The minimum worker protocol is:

1. open the worker queue;
2. select an AVAILABLE job;
3. post exactly `/claim` on the bound GitHub issue;
4. execute the immutable launch artifact returned by the persistent controller;
5. post the required RESULT/1 on the same bound issue;
6. post `/release` only when abandoning the reservation before a result.

No worker is required to copy a bootstrap prompt into another session. The bound issue and immutable launch artifact remain the complete pickup route.

GitHub Projects may provide a table or board view over these issues, but Project state is a projection only. The Project MUST NOT become the authority source for execution, mathematical status, or certification.

## Dispatch modes

Existing dispatch-level `concurrency_mode` remains authoritative. Version 1 recognizes:

- `independent_blind`: the worker must not inspect or use sibling returns before the governing blind cohort closes;
- `cooperative_claimed`: the worker may inspect and explicitly build on the protected evidence listed by the dispatch;
- `adversarial_replay`: the worker attacks or replays disclosed material and must not be represented as an independent blind return.

The queue does not rewrite a dispatch mode.

## Cohort collaboration modes

Cohort orchestration may declare one of:

- `INDEPENDENT_BLIND`;
- `COOPERATIVE`;
- `STAGED_DISCLOSURE`;
- `LEAD_SUPPORT`.

### INDEPENDENT_BLIND

Sibling-use is forbidden until protected closure/reconciliation. Public GitHub visibility is not an access-control guarantee; independence is a governed epistemic contract unless a stronger private transport is separately established.

### COOPERATIVE

Sibling-use is allowed. Dispatches SHOULD identify the protected upstream evidence that participants are expected to inspect and reuse.

### STAGED_DISCLOSURE

The initial phase is independent blind collection. After the required returns are preserved and the blind cohort is explicitly closed, a disclosure receipt may authorize a new cooperative successor cohort.

A blind dispatch MUST NOT be reclassified in place as cooperative. Historical independence is preserved by closing the predecessor cohort and creating successor dispatches.

### LEAD_SUPPORT

A lead dispatch may integrate work from specialized support dispatches. Visibility and dependency permissions must be explicit in each dispatch. A later independent or adversarial lane remains a separate dispatch with its own epistemic class.

## Disclosure transition

A staged-disclosure transition has this form:

```text
blind cohort
    -> protected evidence complete / reconciled
    -> GCL-DISCLOSURE-RECEIPT/1
    -> cooperative successor cohort
```

The disclosure receipt must bind:

- predecessor cohort identity;
- protected return identities;
- closure/reconciliation evidence;
- successor collaboration mode;
- permitted upstream evidence;
- claim boundary.

Opening disclosure does not adjudicate the protected returns and does not promote any mathematical claim.

## Epistemic provenance

Intake or adjudication records SHOULD preserve one of the following provenance classes when applicable:

- `INDEPENDENT_BLIND`;
- `COOPERATIVE`;
- `ADVERSARIAL_REPLAY`;
- `SYNTHESIZED`.

These labels describe evidence provenance. They do not by themselves determine mathematical correctness or certification strength.

## Reservation state

A self-claimable dispatch may specify:

```json
{
  "worker_reservation": {
    "self_claimable": true,
    "role": "RECONNAISSANCE",
    "reservation_ttl_minutes": 65,
    "collaboration_mode": "STAGED_DISCLOSURE",
    "visibility_phase": "BLIND_COLLECTION",
    "sibling_use_policy": "FORBIDDEN"
  }
}
```

The operational controller may represent current reservation state using GitHub issue labels, authenticated comments, and assignee metadata. Those mutable surfaces are operational evidence only. They cannot override the protected dispatch.

A stale reservation may expire or be released without changing mathematical state. Late or duplicate RESULT/1 handling remains controlled by the existing intake contract.

## Persistent-controller requirement

Claim, release, queue initialization, label mutation, or other unattended write-capable queue operations must run through an admitted persistent controller under the repository's GH-OS routing registry. A conversational executor may prepare and protect the workflow, but it is not the persistent controller for future issue-comment events.

Competing claims on the same issue must be serialized. Exactly one live reservation may exist for one dispatch.

## Council responsibility map

This design is governed proportionally:

- **Mechanist:** implementation, race handling, GitHub event semantics, and recovery behavior;
- **Adversary:** authority inflation, duplicate claim, stale reservation, blind-cohort contamination, and mutable-UI attacks;
- **Amanuensis:** policy/implementation consistency, durable references, and protected readback;
- **Referee or security specialist:** required only if an implementation materially weakens protected enforcement, expands constitutional authority, or crosses another reserved boundary.

An authoring system may conduct Mechanist and Adversary logical audit passes only under the staffing doctrine. An authoring-system Adversary pass is non-authoring/read-only and cannot manufacture substantive mathematical independence.

## Immediate implementation profile

The first implementation SHALL:

1. provide a repository-native queue entrypoint;
2. provide `/claim` and `/release`;
3. serialize competing claims per issue;
4. verify protected dispatch eligibility before reservation;
5. keep protected execution lease distinct from reservation state;
6. register the write-capable workflow in GH-OS routing;
7. preserve collaboration mode and sibling-use policy in the claim response;
8. leave RESULT/1 grammar unchanged;
9. pilot on the existing ERDOS first reconnaissance tranche without changing its mathematical assignments, launch bytes, cohort membership, or blind evidence contract;
10. permit a later staged-disclosure successor cohort only through a separate protected transition.

The existing OPENMATH job-board semantics are not changed by this policy. Campaigns that prohibit self-claim remain non-self-claimable until separately opted in.

## Acceptance criteria

The implementation is acceptable only if tests or protected review establish that:

- simultaneous claims serialize and exactly one succeeds;
- non-queue issues cannot be claimed;
- inactive or unauthorized dispatches cannot be claimed;
- an existing protected result prevents a new reservation;
- unauthorized release is rejected;
- expired reservations can be reclaimed without reviving execution authority;
- queue/UI mutation cannot manufacture protected authority;
- blind pickup explicitly preserves sibling-use prohibition;
- cooperative pickup explicitly states sibling-use permission;
- blind dispatches are not converted in place to cooperative dispatches;
- disclosure requires protected predecessor closure;
- queue operations have `mathematical_effect = false` and `certification_effect = false`.

## Claim boundary

GCL-WORKER-QUEUE-001 governs discovery, reservation, collaboration provenance, and disclosure routing. It does not establish mathematical truth, novelty, priority, source equivalence, campaign completion, publication authority, or MATHCERT certification.
