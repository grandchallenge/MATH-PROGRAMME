# Post-Pilot Operating Plan — Agent-Cadence Revision

**Plan ID:** `MP-OPERATING-PLAN-2026-08-POST-PILOT-001-R2`

**Plan window:** half-open interval `[T0, T0 + P9D)`

**Source:** *Full-System Follow-up Report: Post-Pilot Transition and Operating Consolidation*, reporting cut-off 2026-08-12 18:04 PDT

**Status:** Council-review candidate; activates only after the reserved exact-revision Human Steward disposition and protected merge

**Primary coordinating repository:** `grandchallenge/MATH-PROGRAMME`

## 1. Operating outcome

Over nine days, Grand Challenge should convert the report's seven recommendations into three observable outcomes:

1. the factor-`0.1` maintenance regime completes an ordinary, predeclared observation window without bespoke recovery;
2. every required post-merge transition can be shown as processed, skipped for a governed reason, or still outstanding from a durable high-water mark; and
3. one externally legible flagship produces an independently usable or reproducible evidence packet.

CMDG, odd-zeta, PRVSR, and visual pedagogy continue as bounded workstreams. Their purpose in this plan is to produce exact research or operator value, not to expand the institution's authority surface.

The deadline transform is exactly `0.1` of the predecessor plan as frozen in `governance/agent_cadence_operating_plan_transform.json` and checked by `ci/validate_agent_cadence_operating_plan.py`. Evidence, review, claim, protection, and authority requirements are not compressed away. Where the shorter window cannot produce terminal evidence, the correct output is an exact blocker, negative result, or owned continuation packet.

## 2. Baseline and revalidation rule

The source report observed MATH-PROGRAMME `main` at `4f99b64482fb6d67d918d0e4a8d919584236177f`, the merge of PR #488.

At plan drafting, remote `main` was observed at `898e83fb35d9ef6418e70317678df4b244853552`, the merge of [PR #490](https://github.com/grandchallenge/MATH-PROGRAMME/pull/490). Consequently, the PRVSR operator surface is no longer merely an implementation candidate. This plan starts that workstream at measured evaluation and bounded hardening.

Other live observations at drafting were:

- [PR #478](https://github.com/grandchallenge/MATH-PROGRAMME/pull/478) is merged, so selective post-merge dispatch is the active starting point;
- the current CMDG dispatch contract still records `missed_intermediate_merge_replay: false`;
- [PR #465](https://github.com/grandchallenge/MATH-PROGRAMME/pull/465) is open and behind `main`;
- [PR #482](https://github.com/grandchallenge/MATH-PROGRAMME/pull/482) is an open draft; and
- [issue #474](https://github.com/grandchallenge/MATH-PROGRAMME/issues/474) remains the open coefficient-object-solidity tracker.

These are observations, not permanent plan assumptions. `OPS-00` must refresh them before execution begins. Every later decision packet must bind the then-current protected heads and exact evidence. A green workflow, branch tip, dashboard state, or issue description alone is not completion evidence.

### 2.1 Non-retrospective activation clock

`T0` is the timestamp written by the successful protected-main activation readback after all of the following have completed:

1. Council review of one exact plan candidate;
2. one authenticated Human Steward disposition binding that exact candidate;
3. successful required checks at the authorized candidate head;
4. ordinary protected merge without bypass; and
5. readback proving the protected plan bytes and merge identity.

The protected merge timestamp is evidence but is not `T0`. No deadline begins retrospectively. Events between merge and activation readback remain governed by the pre-existing rules. A failed or missing readback leaves the candidate inactive.

## 3. Non-negotiable boundaries

The plan inherits the authority model in the [Administrative Maintenance Plan](governance/ADMINISTRATIVE_MAINTENANCE_PLAN.md), the active [steady-state contract](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/administrative_maintenance_steady_state_0_1.json), and the [PRVSR decision](decisions/ADR-0019_PR_VISUAL_STATUS_REPORTING.md).

- Do not expand autonomous authority during this plan window.
- Automation may assemble, validate, dispatch, measure, and publish advisory evidence. It may not approve, merge, ratify, certify, promote, or activate.
- Candidate, Referee, Human Steward, merge executor, and protected-main readback remain distinct where the governing contract requires them.
- Unknown or unclassified scope fails closed or invokes conservative fanout.
- Historical lateness, failures, superseded candidates, and recovery attempts remain visible.
- PRVSR remains advisory and non-authoritative; it does not become a required merge gate under this plan.
- Every migrated visual retains `visual_is_evidence: false` and requires a separate live-switch gate.
- Mathematical reductions do not imply CM4, T3, dependency-graph completion, certification, novelty, publication, product, or commercial claims.
- Any alternative mathematical route receives its own bounded candidate and is not silently mixed into an existing route.

### 3.1 Human-action budget

Routine plan execution has a required human-action budget of zero. Agents prepare candidates, dispatch work, validate evidence, perform independent office or Referee review, reconcile exact heads, publish receipts, and maintain mirrors within already granted authority.

Human participation is reserved to:

1. one authenticated exact-revision Human Steward disposition after Council review, if the Human Steward chooses to activate this plan; and
2. a later Human Steward, Council, constitutional, production, certification, publication, or commercial decision only if a terminal packet actually requests an authority change reserved to that office.

Silence is not approval. If the activation disposition is absent, current rules remain effective and the candidate does not activate. Routine status, scheduling, dispatch, retry, no-op classification, evidence collation, and non-authoritative reporting must not be routed to a human.

The scorecard records these categories separately:

- `reserved_human_steward_actions`: target `1` for activation;
- `routine_human_operating_actions`: target `0`;
- `human_merge_executor_actions`: `0` when ordinary automation merges, otherwise observed separately and never represented as routine programme review;
- `external_human_participant_actions`: target `0`; independent agent exercise is sufficient unless a separately authorized external commitment requires a human; and
- `terminal_reserved_human_actions`: target `0` unless the terminal packet requests a reserved authority change.

## 4. Delivery model

### 4.1 Phases

All deadlines are measured from the protected activation time `T0`. The phase offsets are the exact `0.1` transform of the predecessor 90-day plan.

| Phase | Deadline from `T0` | Purpose | Exit condition |
|---|---|---|---|
| 0 — Rebaseline | `T0 + PT4H48M` | Bind the plan to live protected state and assign accountable agent roles | `OPS-A` passes; `OPS-B` ledger is active |
| 1 — Stabilize and specify | `T0 + P2DT12H` | Observe steady-state maintenance, specify high-water semantics, freeze bounded research work, and baseline PRVSR usability | `ADM-A`, `HWM-A`, `CMDG-A`, `OZ-A`, `PRV-A`, and `EXT-A` pass or carry explicit blockers |
| 2 — Deliver bounded increments | `T0 + P5DT9H36M` | Implement high-water recovery, admit bounded research results, migrate one reviewed visual tranche, and build the selected flagship packet | `HWM-B`, `HWM-C`, `CMDG-B`, `OZ-B`, `PRV-B`, `VIS-A`, and `EXT-B` pass or carry explicit blockers |
| 3 — Independent use and disposition | `T0 + P9D` | Close the observation set, exercise recovery, conduct independent reproduction/use, and decide continuation, repair, consolidation, or retirement | `ADM-B`, `PRV-C`, `VIS-B`, and `EXT-C` have terminal records; the nine-day review preserves every blocker and residual |

`OPS-A` is a hard predecessor. No downstream implementation, migration, or experiment may begin before `OPS-A`; only evidence gathering needed to construct and verify `OPS-00` is permitted.

### 4.2 Work-in-progress controls

These are management controls, not governance authority:

- no more than two simultaneous control-plane implementation candidates;
- no more than one active candidate on each of the CMDG and odd-zeta routes;
- one visual migration tranche in review at a time;
- after flagship selection, at least one delivery lane is always externally legible rather than purely infrastructural;
- a blocked candidate is either given an owned next experiment or parked; it does not remain nominally active without a bounded next action.

### 4.3 Operating cadence

- Automation publishes an exact-head status digest after every material transition and at least every `PT2H24M` while work is active.
- A `PT16H48M` operating review is compiled asynchronously from canonical evidence and covers only exceptions, blockers, metric movement, and next gates. No synchronous meeting is required.
- Research lanes use asynchronous exact-revision packets; meetings are scheduled only when a mathematical choice or authority decision cannot be resolved from the packet.
- Council or Human Steward attention is requested only for an actual reserved decision, control-plane authority change, exception, waiver, or terminal disposition.
- Every `P2DT19H12M`, agents retire duplicate trackers, stale branches, redundant workflows, and reports whose history is already preserved canonically.

## 5. Workstream register

| ID | Workstream | Accountable role | Independent role | 90-day result |
|---|---|---|---|---|
| `OPS` | Portfolio control | Programme Operations Lead | non-author operating reviewer | One exact plan ledger, current owners, current heads, and no contradictory status mirrors |
| `ADM` | Steady-state reliability | Administrative Maintenance Owner | non-author Referee where control semantics change | Ordinary factor-`0.1` evidence window completed or an exact failure-and-repair record retained |
| `HWM` | Durable post-merge high-water mark | Policy/CI Maintainer | independent adversarial reviewer | Missed intermediate transitions are detected and recoverable without irrelevant replay |
| `CMDG` | Coefficient-object residue | CMDG Mathematical Lead | independent mathematical/formal reviewer | One or more exact residual steps admitted without claiming CM4 prematurely |
| `OZ` | Bounded odd-zeta/T3 search | Odd-Zeta Campaign Lead | independent mathematical reviewer | At least one predeclared finite class receives an exact, replayable disposition |
| `PRV` | PRVSR operator evaluation | Operator Surface Maintainer | reviewer not involved in implementation | Measured advisory utility with no false authority signal |
| `VIS` | Reviewed visual migration | Documentary/Visualization Lead | domain-sensitive semantic reviewer | One additional tranche reaches a separate, reversible live-switch decision |
| `EXT` | External-value flagship | named human sponsor | independent user or reproducer | One externally legible packet is exercised outside its original authoring path |

Named people may fill these roles, but a role must never be inferred from automation identity.

## 6. Work packages and acceptance gates

### 6.1 `OPS` — portfolio control

#### `OPS-00` — exact baseline packet

Due: end of Phase 0.

Record:

- protected heads for MATH-PROGRAMME, MATHFORGE, MATHSOLVE, MATHCERT, and INTELLECT;
- the exact active maintenance, policy-shard, CMDG-dispatch, PRVSR, and visual-migration contracts;
- open candidates, their exact heads, mergeability, required checks, review state, and blockers;
- the current owner and evidence path for every workstream in this plan;
- contradictions, missing evidence, and unknown metrics without coercing them to zero.

**Gate `OPS-A`:** a non-author reviewer can reproduce the baseline from canonical protected records and live GitHub state. Any mismatch remains `UNKNOWN` or `BLOCKED`, not favorable.

#### `OPS-01` — single operating ledger

Maintain one compact ledger with these states only:

`NOT_STARTED`, `CANDIDATE`, `EXECUTING`, `EVIDENCE_READY`, `INDEPENDENTLY_REVIEWED`, `PROTECTED`, `EXTERNALLY_EXERCISED`, `BLOCKED`, `PARKED`.

The ledger links to canonical evidence; it does not replace it. Update it after material transitions and at the weekly review.

**Gate `OPS-B`:** no plan item is marked complete unless its acceptance gate and exact evidence are linked.

### 6.2 `ADM` — prove ordinary steady-state reliability

#### `ADM-01` — instrument the occurrence ledger

For every scheduled occurrence, capture:

- occurrence key, cadence, due time, delivery time, and scheduler variance;
- candidate-prepared time and candidate exact head;
- first valid review time;
- protected merge time and merge SHA;
- receipt publication time and receipt identity;
- mirror/readback completion time and protected identity;
- stale-head reconciliations and their outcome;
- control-plane interventions, including whether they were ordinary, recovery, or bespoke.

Derive, rather than manually type, due-time reliability and each latency interval.

#### `ADM-02` — run the predeclared observation window

Use `[T0, T0 + P8DT4H48M)` as the primary due-occurrence observation interval while preserving the existing maintenance cadence anchor. Do not reset the cadence anchor or erase a failed occurrence. The interval evaluates every occurrence whose due time falls inside the half-open interval; it does not manufacture additional authoritative occurrences merely to increase sample size. The remaining `PT19H12M` is reserved for terminal receipts, readback, reconciliation, and compilation.

**Gate `ADM-A`:** by the stability gate, every occurrence already due has a current exact state and no occurrence is silently absent.

**Gate `ADM-B`:** by `T0 + P9D`, every occurrence due in the primary observation interval has either a terminal exact receipt/readback or an explicit `PENDING_AT_CUTOFF`/`FAILED_AT_CUTOFF` record with owner, last proven state, and continuation route. The window records whether bespoke recovery occurred and never weakens exact-head, review, protected-merge, or readback requirements.

If `ADM-B` fails, preserve the failure, repair it through a separately reviewed change, and predeclare one new `P9D` confirmation window. Eventual success does not rewrite the primary-window result.

#### `ADM-03` — dispose the reliability evidence

At the end of the observation window, issue one of:

- `ORDINARY_STEADY_STATE_WINDOW_CONFIRMED`;
- `STEADY_STATE_OPERATIONAL_WITH_OWNED_RELIABILITY_RESIDUALS`; or
- `STEADY_STATE_REQUIRES_CONTROL_PLANE_REVIEW`.

No disposition expands authority.

### 6.3 `HWM` — durable post-merge processing

#### `HWM-01` — specify the state machine

The design must persist at least:

- repository and protected branch;
- durable `processed_through_sha`;
- ordered observed transition set from that point to the current protected head;
- per-transition scope-classifier version and digest;
- terminal state: `PROCESSED`, `VERIFIED_NOOP`, `PENDING`, `FAILED`, or `SUPERSEDED_BY_REPLAY`;
- exact workflow/run and receipt identities;
- retry count and last error;
- atomic checkpoint update rule.

`VERIFIED_NOOP` is permitted only for a recognized, governed classifier result. Unknown scope invokes conservative processing.

**Gate `HWM-A`:** the specification proves that observing the newest head cannot conceal an unprocessed intermediate transition.

#### `HWM-02` — implement idempotent recovery

Required adversarial cases:

1. two or more protected merges arrive while the dispatcher is unavailable;
2. the latest head is already processed but an intermediate receipt is missing;
3. duplicate delivery occurs;
4. the classifier version changes;
5. history is shallow or ancestry cannot be proven;
6. a transition is clearly unrelated;
7. scope is unknown or malformed;
8. processing succeeds but checkpoint publication fails;
9. the protected head moves during recovery; and
10. a replayed transition produces a different terminal digest.

The system must be idempotent, preserve failures, and avoid replay of a transition already covered by a valid exact receipt.

**Gate `HWM-B`:** a fixture with missed intermediate merges is recovered in order, produces exact receipts, and advances the checkpoint only after terminal evidence is durable.

**Gate `HWM-C`:** ordinary unrelated transitions remain verified no-ops; unknown transitions fan out; protected required-check identities and authority boundaries remain unchanged.

### 6.4 `CMDG` — preserve and advance the exact mathematical boundary

#### `CMDG-01` — select one active route

Reconcile the protected baseline with PR #465, draft PR #482, issue #474, and any newer successors. Choose one primary candidate for the next exact step. Park or supersede competing candidates explicitly; do not combine unreviewed results across branches.

#### `CMDG-02` — stage the residue

Use the following dependency order unless a separately governed alternative route is opened:

1. lower-Hom identification;
2. finite-quotient factorization;
3. surjectivity;
4. mapping-out or acyclicity residue;
5. injectivity;
6. coefficient residual theorem; and
7. P3 discharge.

Each candidate states the strongest proved result and lists every later item as not claimed.

**Gate `CMDG-A`:** the selected candidate builds and replays against pinned dependencies, and a non-author reviewer agrees with the exact claim boundary.

**Gate `CMDG-B`:** at least one next dependency step receives a protected positive result or an exact blocker packet that makes the remaining theorem narrower. A blocker is a valid result; CM4 is not claimed unless every required bridge is actually admitted.

### 6.5 `OZ` — bounded odd-zeta execution

#### `OZ-01` — preregister the next finite class

Before computation, record:

- the mathematical reason for expanding or changing the ansatz;
- the exact finite candidate class;
- coefficient field, normalization, symmetry, and rank conditions;
- search bounds and resource limits;
- verifier and dependency identities;
- the result types that count as terminal evidence.

#### `OZ-02` — execute once, replay independently

Allowed terminal outcomes are:

- exact positive certificate;
- exact negative result for the bounded class;
- rank obstruction;
- new invariant;
- reduction to a smaller class; or
- exact characterization of a missing proof mechanism.

**Gate `OZ-A`:** the class is frozen before execution and cannot be enlarged after seeing the result without opening a new candidate.

**Gate `OZ-B`:** an independent replay reproduces the exact terminal result. No bounded negative result is represented as evidence against T3 itself, and no positive bounded result is promoted beyond its certified scope.

### 6.6 `PRV` — measure the merged operator surface

#### `PRV-01` — controlled operator exercise

Use a small retained evaluation set containing at least:

- one protected-complete PR;
- one stale-head PR;
- one blocked or residual-bearing PR;
- one PR requiring Human Steward state to be distinguished from ordinary review; and
- one archive or source/render inconsistency.

For each case, measure:

- time to identify operative state;
- exact-head accuracy;
- stale-state detection;
- blocker and residual-obligation detection;
- whether canonical evidence was consulted when required;
- source/render disagreement; and
- accessibility/textual-equivalence failures.

**Gate `PRV-A`:** no evaluation case is falsely labeled ready, protected, approved, or complete.

**Gate `PRV-B`:** all stale and blocker-bearing cases are identified, and every displayed positive state can be traced to canonical evidence.

Time measurements are operational observations, not generalized human-performance claims.

#### `PRV-02` — bounded hardening

Repair deterministic, provenance, accessibility, or stale-state defects found by `PRV-01`. Do not introduce a new required check, mandatory rollout, Projects mutation, or merge authority.

**Gate `PRV-C`:** the repaired surface passes the retained adversarial set and preserves its advisory boundary. Any proposal for wider propagation is a separate later decision.

### 6.7 `VIS` — reviewed visual migration

#### `VIS-01` — freeze one tranche

Select a bounded set of related plates whose source records and mathematical reviewers are available. For every plate retain:

- predecessor identity;
- successor representation class;
- source identity and renderer;
- deterministic derivative digest;
- independent semantic review;
- accessibility text;
- rollback identity;
- `visual_is_evidence: false`; and
- a separate live-switch decision.

#### `VIS-02` — review before activation

Render and inspect the entire tranche together. Reject a semantically weak representation even if its files and manifests validate.

**Gate `VIS-A`:** every candidate passes deterministic regeneration, schema validation, accessibility review, and independent domain-sensitive semantic review.

**Gate `VIS-B`:** live activation is a separate exact-revision change with verified rollback. A tranche may finish as `REDRAW` or `PARKED` without being forced live.

### 6.8 `EXT` — concentrate on one external-value flagship

#### `EXT-01` — select, do not preselect

By the end of Phase 1, a named accountable sponsor selects one flagship using a compact comparison of:

- external legibility;
- independent reproducibility;
- value if the main theorem remains open;
- credible completion within the plan window;
- dependence on unresolved mathematics;
- maintenance burden;
- accessibility to a non-institutional user; and
- a specific outside user or reproducer who can exercise it.

Candidate lanes include an end-to-end mathematical exemplar, a formal-mathematics explanation surface, a visible certified CMDG path, a reproducible positive/negative research packet, or governed research infrastructure an outside group will actually use.

**Gate `EXT-A`:** one lane is selected with an accountable sponsor, intended outside user, bounded output, nonclaims, and stop conditions. The sponsor may be an authorized agent unless external commitment, expenditure, publication, production, or commercial authority requires a human. Selection does not certify market demand or commercial readiness.

#### `EXT-02` — build the minimum independent-use packet

The packet must contain:

- a one-page statement of the problem and value;
- exact source and protected artifact identities;
- a clean-room reproduction or use procedure;
- machine-checkable evidence where applicable;
- expected outputs and known failure modes;
- claim boundaries and unresolved dependencies;
- an accessible explanation surface; and
- a feedback/defect route.

**Gate `EXT-B`:** an independent actor outside the original authoring path can run or use the packet without private oral context. The actor may be an agent; a human is required only for a separately reserved external commitment.

#### `EXT-03` — preserve the external result

Record whether the exercise produced:

- independent reproduction;
- useful adoption;
- partial use with owned defects;
- failure to reproduce; or
- no evidence of external value.

**Gate `EXT-C`:** the result, including a negative result, is retained without being converted into a publication, product, revenue, or scientific-completion claim.

## 7. Integrated milestone gates

| Gate | Target from `T0` | Required evidence | Decision |
|---|---|---|---|
| A — Live baseline | `PT4H48M` | exact heads, active contracts, workstream owners, open residuals | start, repair baseline, or block affected lane |
| B — Stability and design | `P2DT12H` | maintenance-window ledger, high-water specification, frozen CMDG/OZ candidates, PRVSR evaluation baseline | continue, repair, narrow, or pause |
| C — Bounded delivery | `P5DT9H36M` | high-water recovery fixtures, one CMDG/OZ exact result, one visual tranche disposition, flagship packet | admit bounded results or preserve blockers |
| D — External exercise | `P8DT4H48M` | independent-use/reproduction record and defects | continue, revise, park, or retire flagship |
| E — Nine-day disposition | `P9D` | consolidated exact evidence, adverse history, residuals, burden measures, next decision packet | no automatic authority expansion |

Missing evidence at a gate is `UNKNOWN` or `BLOCKED`; it is never scored as zero risk or successful completion.

## 8. Scorecard

| Objective | Measure | Gate rule |
|---|---|---|
| Ordinary maintenance | due occurrences with terminal records / due occurrences | `100%` for `ADM-A`; any absence blocks |
| No bespoke recovery | occurrences requiring bespoke recovery | `0` for `ADM-B`; failures remain recorded |
| Scheduler reliability | delivery time minus due time | report distribution and outliers; do not hide late recovery |
| Merge-to-receipt/readback | protected merge to durable receipt and readback | report each interval and missing identity |
| Durable post-merge coverage | required transitions terminally accounted for / required transitions observed | `100%`, including governed no-ops |
| Recovery correctness | missed-transition adversarial fixtures recovered in order | all required fixtures pass with exact receipts |
| CMDG precision | newly admitted exact step plus explicitly retained residue | no claim crosses the admitted dependency frontier |
| Odd-zeta boundedness | preregistered classes with exact independent disposition | every executed class has one terminal record |
| PRVSR safety | false-ready or false-complete classifications | `0` in the evaluation set |
| PRVSR legibility | correct stale/blocker/authority identification | all evaluation cases correct; time retained as observation |
| Visual migration | activated plates with complete review and rollback bundle | `100%`; otherwise do not switch live |
| External value | independently exercised flagship packets | at least `1`; outcome may be positive or negative |

## 9. Risk and escalation rules

| Risk | Early signal | Response |
|---|---|---|
| exact-head churn invalidates review | candidate behind or reviewed SHA differs from live head | reconcile deterministically; obtain review on the new exact head |
| selective checking skips required work | unknown path or classifier disagreement | conservative full fanout; open a classifier defect |
| high-water checkpoint overstates coverage | newest head present but an intermediate receipt is absent | stop checkpoint advancement; recover from last proven point |
| governance becomes the main output | control-plane WIP grows while no external packet advances | enforce WIP limits and prioritize `EXT` gate work |
| CMDG scope expands without discharge | new graph branches appear before the active residue narrows | park new branches; retain one active route |
| odd-zeta search proliferates | next class lacks a mathematical reason or frozen bound | do not execute; return to route selection |
| PRVSR becomes de facto authority | operator acts on dashboard without canonical evidence | label unknown/stale states visibly; correct training and UI |
| visual validation masks weak pedagogy | manifest passes but reviewer cannot recover intended semantics | reject or redraw before live switch |
| external exercise is performative | reproducer needs private intervention or is an original author | repeat with a genuinely independent user and record the failure |

P0/P1 defects follow the active maintenance response rules immediately. P2 defects must have an owner and next applicable review. P3 work is batched and cannot displace Gates A–D.

## 10. Terminal review packet

The nine-day review should fit in one compact exact-revision packet with appendices generated from canonical evidence. It must contain:

1. baseline and final protected heads;
2. every milestone disposition;
3. maintenance occurrence and latency summary;
4. high-water recovery proof and remaining gaps;
5. exact CMDG and odd-zeta results and nonclaims;
6. PRVSR safety/usability observations;
7. visual tranche disposition and rollback identities;
8. external exercise result;
9. failures, late events, superseded candidates, and unknowns;
10. operating burden, including human actions and control-plane interventions; and
11. one recommended next action per workstream: continue, repair, narrow, park, consolidate, retire, or seek a separately authorized expansion.

The terminal packet may recommend a later Council or Human Steward decision. It does not itself approve, ratify, merge, certify, activate, publish, deploy, or commercially promote anything.

## 11. Immediate first `PT16H48M`

1. Complete `OPS-00` and assign named accountable roles.
2. Start the occurrence ledger before the next scheduled maintenance locus.
3. Freeze the `HWM-01` state-machine contract and adversarial fixture list.
4. Reconcile PR #465, draft PR #482, issue #474, and any successors into one active CMDG route.
5. Preregister the next odd-zeta finite class or explicitly park the lane.
6. Run the first PRVSR operator evaluation against the merged #490 surface.
7. Nominate no more than three external-value candidates and identify a real independent user for each.
8. Choose the next visual tranche only if its source records and semantic reviewer are available.

If these actions cannot be completed within `PT16H48M`, preserve the reasons in the operating ledger and narrow the plan rather than creating more parallel work.
