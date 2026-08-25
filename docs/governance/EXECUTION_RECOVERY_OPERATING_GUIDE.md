# Execution Recovery operating guide

## Purpose

This guide defines the MATH-PROGRAMME recovery procedure for an already
authorized bounded operation when the ordinary diagnostic, logging, CI,
connector, compiler, environment, or replay surface fails.

It does not enlarge authority. It distinguishes a recoverable execution
problem from a genuine stopping boundary so that fail-closed governance is not
misapplied as premature abandonment of authorized diagnostic work.

The governing issue for this guide is `MP-EXECUTION-RECOVERY-001`.

## Authority and precedence

MATH-PROGRAMME owns mathematics-specific operating policy subject to the
INTELLECT Constitution, effective amendments, admitted cross-programme
standards actually adopted by the programme, protected programme policy, and
MATHCERT's separate certification authority.

The proposed `GCL-GHOS-00` 0.2.0 bounded-execution-continuity successor is a
coordinated candidate, not current authority until protected admission and
programme adoption. This guide stands on existing MATH-PROGRAMME authority and
must remain compatible with superior controls.

## Continuity rule

For an already authorized bounded MATH operation, a recoverable infrastructure,
connector, logging, check-surface, compiler-diagnostic, environment, CI, or
tooling failure is not by itself a stopping condition.

The operator continues through the applicable recovery ladder until:

1. the authorized objective is completed; or
2. a genuine boundary is reached and named precisely.

Fail closed on mathematical claims, certification, promotion, publication,
protected-state mutation, stale evidence, and authority. Do not fail closed
merely on the mechanics of obtaining the evidence needed to decide those
matters.

## Exact-identity binding

Before recovery or repair, bind the operation to every exact identity that is
material to the evidence route. Depending on the operation, this includes:

- repository and protected predecessor;
- issue or work-package identifier;
- pull request and branch;
- exact current PR head SHA;
- workflow run ID;
- exact job ID and job head SHA;
- artifact digest or file/blob identity;
- pinned dependency/toolchain identities;
- exact theorem, module, check, or failing step.

If the current head, run, job, artifact, protected predecessor, or governed
scope has materially changed, earlier diagnostics are stale. Do not patch from
them as though they described the current operation. Rebind and recover fresh
evidence.

## Diagnostic recovery ladder

Use the narrowest available exact-current diagnostic surface first. Advance to
the next route when the prior route is unavailable, empty, truncated,
inconclusive, or demonstrably broken.

### 1. Exact individual Actions job log

Recover the log for the exact failing job and verify that its `head_sha`
matches the current governed PR head. Prefer the smallest failing job rather
than a broad run archive.

### 2. Check annotations and job-step surfaces

If the job log cannot provide the diagnostic, inspect check-run annotations,
job steps, check output, and other exact-head diagnostic surfaces. Recover the
actual file/line/column and surrounding compiler or validator message when
available.

### 3. Complete workflow-run log archive

If individual surfaces fail, retrieve the complete log archive for the exact
workflow run. Isolate the exact job/step and retain enough surrounding context
to distinguish the first substantive error from secondary failures.

### 4. Exact-head pinned replay

If hosted logs remain unavailable or insufficient, replay the exact current
head using the workflow-declared toolchain, dependency pins, commands, and
build order. Narrow the replay to the failing module or step when the workflow
contract permits that narrowing; do not silently substitute a different
environment or dependency set.

### 5. Authenticated local extraction

When connected diagnostic surfaces remain unavailable but an authenticated
operator environment can access GitHub, provide a self-contained `gh`/GitHub
API extraction route bound to the exact repository, PR, head, run, and job.
The extraction should attempt, as applicable:

1. individual job logs;
2. exact-head check-run annotations;
3. the complete run-log archive;
4. focused searches for the failing file, theorem/check identifier, and
   `error:`/equivalent diagnostics;
5. sufficient surrounding lines to support a narrow repair.

The script must first verify that the live PR, run, and job still bind to the
expected exact head. A mismatch is a named stale-identity boundary, not a
license to use old diagnostics.

## Shell safety for operator-provided recovery scripts

A recovery snippet intended to be pasted into an operator's existing shell
must not terminate that shell as a side effect of a recoverable diagnostic
failure.

Therefore:

- do not use top-level `exit`;
- do not use top-level `set -euo pipefail`;
- use guarded branches, subshells, warnings, and continue/skip behavior for
  recoverable extraction failures;
- a hard identity mismatch must print a clear stop condition and avoid mutation
  or stale evidence use without terminating the parent shell.

This shell-safety rule does not weaken fail-closed governance. It prevents a
diagnostic helper from destroying the operator's working session.

## Repair and replay loop

Once a fresh exact-current diagnostic is recovered:

1. identify the smallest demonstrated failing theorem, statement, module,
   validator rule, or authorized code surface;
2. repair only that demonstrated failure unless the governing scope explicitly
   authorizes a broader change;
3. do not stack speculative downstream edits while the current exact replay is
   unresolved;
4. commit the repair to the governed working branch;
5. run a fresh exact-head replay of the applicable pinned workflow;
6. if the replay fails, discard stale prior diagnostics and repeat the recovery
   ladder against the new exact head;
7. continue until the bounded objective is green or a genuine named boundary is
   reached.

A successful local replay is evidence only for the route it actually exercised.
It does not replace a required hosted, protected, independent-review, MATHCERT,
or admission gate.

## Genuine stopping boundaries

Before stopping, state the boundary by name and identify the rule or condition
that makes continuation unauthorized or evidentially unsound.

Recognized categories are:

- **governance boundary** — the governing process requires a new governed
  decision or registered scope;
- **authority boundary** — the next action requires power not delegated to the
  current actor or operation;
- **authentication boundary** — the required evidence or mutation cannot be
  accessed with available authorized credentials and no authorized fallback
  remains;
- **safety boundary** — continuation would violate an applicable safety control;
- **protected-state boundary** — continuation would require an unauthorized
  protected mutation, bypass, force update, or equivalent prohibited action;
- **materially changed-state boundary** — current protected state, exact head,
  scope, dependency identity, or governed plan has changed so that the existing
  authorization no longer applies;
- **substantive evidentiary boundary** — the required claim/certification
  evidence does not exist or remains insufficient after the authorized evidence
  routes are exhausted;
- **recovery exhaustion boundary** — all reasonably available authorized
  diagnostic/recovery routes have actually been attempted and none can recover
  the evidence needed for the next bounded action.

A broken log endpoint, empty connector response, ordinary compiler error,
single failed replay, transient CI failure, or inconvenient environment is not
by itself one of these boundaries.

## Human Steward escalation

Human Steward intervention is requested only where the governing process
actually reserves the next decision or authority to the Human Steward. The
operator must not convert an implementation inconvenience into a synthetic
approval gate.

When escalation is genuinely required, provide the exact current identities,
evidence already recovered, routes attempted, unresolved condition, and the
specific decision or authority required.

## Claim boundary

This guide authorizes no mathematical claim, MATHCERT disposition, merge,
publication, protected-branch bypass, or external representation. It governs
only how already-authorized bounded execution recovers evidence and repairs
within scope.
