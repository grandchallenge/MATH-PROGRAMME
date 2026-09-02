# Execution Recovery operating guide

## Purpose

This guide defines the MATH-PROGRAMME recovery procedure for an already authorized bounded operation when an ordinary diagnostic, logging, CI, connector, compiler, environment, or replay surface fails.

It does not enlarge authority. It distinguishes recoverable execution failure from a genuine stopping boundary so that fail-closed governance is not misapplied as abandonment of authorized diagnostic work.

The governing issue for this guide is `MP-EXECUTION-RECOVERY-001`. Routine recovery is additionally governed by `MP-STREAMLINED-EXECUTION-001`: exact identities are used where they describe the failing evidence, while unrelated repository-head movement does not invalidate a materially unchanged closure.

## Authority and precedence

MATH-PROGRAMME owns mathematics-specific operating policy subject to the INTELLECT Constitution, effective amendments, admitted cross-programme standards actually adopted by the programme, protected programme policy, and MATHCERT's separate certification authority.

`GCL-GHOS-00` `0.2.0` is current authority for the bounded MATH-PROGRAMME pilot. Its standards-layer and programme adoption records remain protected evidence. This guide stands on existing authority and must remain compatible with superior controls.

## Continuity rule

For an already authorized bounded MATH operation, a recoverable infrastructure, connector, logging, check-surface, compiler-diagnostic, environment, CI, or tooling failure is not by itself a stopping condition.

The operator continues through the applicable recovery ladder until:

1. the authorized objective is completed; or
2. a genuine boundary is reached and named precisely.

Fail closed on mathematical claims, certification, promotion, publication, unauthorized protected-state mutation, materially stale evidence, and authority. Do not fail closed merely on the mechanics of obtaining the evidence needed to decide those matters.

## Mandatory workflow routing

All direct repository workflows are enumerated in `.ghos-routing/workflows.json`. The protected routing control derives each workflow's autonomous-wake, external-wait, opaque-execution, credential, and write-capability features from its bytes, derives the minimum execution topology, and requires an admitted compatible controller whenever the workflow is not bounded atomic work.

The current admitted persistent controller is repository-bound GitHub Actions. Its event queue and exact run/job records survive the conversational executor. This controller supplies persistence and observation only; it supplies no merge, certification, promotion, publication, or mathematical authority.

The independently required `routing-enforcement` check runs from the protected base, treats pull-request content as untrusted data, verifies the externally governed gate digest, and rejects routing/control drift outside the admitted contract.

Routine care, external gate upgrades, digest rotation, protected self-modification, ruleset recovery, controller changes, and hostile proof are governed by [`GH-OS routing control runbook`](GHOS_ROUTING_CONTROL_RUNBOOK.md).

## Material-identity binding

Before recovery or repair, bind the operation to every exact identity that is material to the failing evidence route. Depending on the operation, this includes:

- repository and relevant protected predecessor or dependency;
- issue or work-package identifier;
- pull request and branch;
- candidate commit whose bytes produced the diagnostic;
- workflow run ID;
- exact job ID and job head SHA;
- artifact digest or file/blob identity;
- pinned dependency/toolchain identities;
- exact theorem, module, check, or failing step.

A diagnostic becomes stale when the repaired bytes, relevant dependency, governed scope, toolchain, authority boundary, or other material input it describes changes. A numerically newer protected `main` is not by itself evidence staleness when that movement is outside the material closure.

## Durable checkpoint and session restart

Only a multi-session governed campaign explicitly admitted in
`governance/bounded_operation_checkpoint_registry.json` carries this checkpoint.
Routine pull requests, ordinary CI waits, bounded repairs, and ordinary drafting
are excluded and continue under the streamlined execution policy. Merely taking
more than one session or waiting for CI does not admit work to this registry.

The checkpoint is the durable operational resume surface. Before substantial
continuation, a new agent/session must:

1. read the registered checkpoint;
2. read the authoritative issue/PR/policy sources named by the checkpoint;
3. verify that exact material identities still match;
   mechanically run the recorded `freshness.verification_command` and fail
   closed on a head, base, PR-state, or settled-result mismatch;
4. execute only a permitted action, normally the single recorded `next_action`;
5. update the checkpoint after a material transition changes phase, exact head,
   external-evidence state, next action, or genuine boundary.

A conforming live checkpoint sets `resume.fresh_session_safe=true` and
`resume.requires_chat_history=false`. A chat transcript, conversational summary,
or operator promise is never an authoritative prerequisite for resume.

When external CI, review, or evidence is pending, record the exact run, job,
review, artifact, or source identity and the exact status/evidence query to
perform next. `wait`, `wait for CI`, and equivalent indefinite instructions are
not valid next actions.

An interaction/session/resource interruption does not create a governance or
authority boundary. If interruption occurs after a material transition, commit
or update the durable checkpoint before relying on later conversational
continuity. If interruption occurs before a transition is durably recorded, the
next session re-reads authoritative state and records a fresh checkpoint rather
than assuming that an unrecorded transition occurred.

Checkpoint shape and cross-state semantics are enforced by
`ci/validate_bounded_operation_continuity.py`. A checkpoint carries no approval,
merge, certification, publication, protected-bypass, or claim authority.

Mandatory routing and checkpoints have different jobs. Routing selects an
admitted persistent controller when workflow topology requires one. A checkpoint
stores reconstructible transaction state only for an explicitly admitted
multi-session campaign. A registry entry is therefore a deliberate governance
decision, not a universal paperwork requirement.

## Diagnostic recovery ladder

Use the narrowest available diagnostic surface that is bound to the failing material object. Advance to the next route when the prior route is unavailable, empty, truncated, inconclusive, or demonstrably broken.

### 1. Individual Actions job log

Recover the exact failing job log and verify which candidate/head SHA it actually executed. Prefer the smallest failing job rather than a broad run archive.

### 2. Check annotations and job-step surfaces

If the job log cannot provide the diagnostic, inspect check-run annotations, job steps, check output, and other subject-bound diagnostic surfaces. Recover the actual file/line/column and surrounding compiler or validator message when available.

### 3. Complete workflow-run log archive

If individual surfaces fail, retrieve the complete log archive for the relevant workflow run. Isolate the exact job/step and retain enough surrounding context to distinguish the first substantive error from secondary failures.

### 4. Pinned local replay

If hosted logs remain unavailable or insufficient, replay the relevant candidate bytes using the workflow-declared toolchain, dependency pins, commands, and build order. Narrow the replay to the failing module or step when the workflow contract permits that narrowing; do not silently substitute a different environment or dependency set.

### 5. Authenticated local extraction

When connected diagnostic surfaces remain unavailable but an authenticated operator environment can access GitHub, provide a self-contained `gh`/GitHub API extraction route bound to the relevant repository, PR, candidate, run, and job.

The extraction should attempt, as applicable:

1. individual job logs;
2. check-run annotations;
3. the complete run-log archive;
4. focused searches for the failing file, theorem/check identifier, and `error:`/equivalent diagnostics;
5. sufficient surrounding lines to support a narrow repair.

The script must verify that the run and job correspond to the candidate bytes whose failure is being repaired. If the candidate changed materially, recover evidence for the new candidate before patching. Do not require a branch update merely because the base repository advanced independently.

## Shell safety for operator-provided recovery scripts

A recovery snippet intended to be pasted into an operator's existing shell must not terminate that shell as a side effect of a recoverable diagnostic failure.

Therefore:

- do not use top-level `exit`;
- do not use top-level `set -euo pipefail`;
- isolate strict/error-exit behavior inside a subshell;
- use guarded branches, warnings, and continue/skip behavior for recoverable extraction failures;
- a hard material-identity mismatch must print a clear stop condition and avoid mutation or stale evidence use without terminating the parent shell.

This shell-safety rule does not weaken fail-closed governance. It prevents a diagnostic helper from destroying the operator's working session.

## Repair and replay loop

Once a fresh material diagnostic is recovered:

1. identify the smallest demonstrated failing theorem, statement, module, validator rule, or authorized code surface;
2. repair only that demonstrated failure unless the governing scope explicitly authorizes a broader change;
3. do not stack speculative downstream edits while the current affected replay is unresolved;
4. commit the repair to the governed working branch;
5. rerun the affected protected check, pinned replay, or policy shard required by the repaired material closure;
6. if the replay fails, treat diagnostics from superseded candidate bytes as stale and repeat the recovery ladder against the changed object;
7. continue until the bounded objective is green or a genuine named boundary is reached.

Do not rerun unrelated formal, external, repository-wide, or computational lanes merely to obtain a numerically fresh head. Current policy impact routing decides the required protected checks.

A successful local replay is evidence only for the route it actually exercised. It does not replace a required hosted/protected check or a specialist mathematical, certification, security, or admission gate when such a gate genuinely applies.

## Genuine stopping boundaries

Before stopping, state the boundary by name and identify the rule or condition that makes continuation unauthorized or evidentially unsound.

Recognized categories are:

- **governance boundary** — the governing process requires a new governed decision or registered scope;
- **authority boundary** — the next action requires power not delegated to the current actor or operation;
- **authentication boundary** — the required evidence or mutation cannot be accessed with available authorized credentials and no authorized fallback remains;
- **safety boundary** — continuation would violate an applicable safety control;
- **protected-state boundary** — continuation would require an unauthorized protected mutation, bypass, force update, or equivalent prohibited action;
- **materially changed-state boundary** — a relevant protected dependency, material object, scope, toolchain, authority, or claim boundary changed so that existing evidence or authorization no longer applies;
- **substantive evidentiary boundary** — the required claim/certification evidence does not exist or remains insufficient after authorized evidence routes are exhausted;
- **recovery exhaustion boundary** — all reasonably available authorized diagnostic/recovery routes have actually been attempted and none can recover the evidence needed for the next bounded action.

A broken log endpoint, empty connector response, ordinary compiler error, single failed replay, transient CI failure, behind branch, or unrelated `main` movement is not by itself one of these boundaries.

## Human Steward escalation

Human Steward intervention is requested only where the governing process actually reserves the next decision or authority to the Human Steward. Standing delegation covers routine bounded execution; an operator must not convert implementation inconvenience, numerical head drift, or an ordinary documentation/engineering transition into a synthetic approval gate.

When escalation is genuinely required, provide the material identities, evidence already recovered, routes attempted, unresolved condition, and the specific reserved decision or authority required.

## Claim boundary

This guide authorizes no mathematical claim, MATHCERT disposition, publication, protected-branch bypass, or external representation. It governs how already-authorized bounded execution recovers evidence and repairs within scope. Routine protected merge authority is supplied only by the standing delegation and repository protection, not by this guide itself.
