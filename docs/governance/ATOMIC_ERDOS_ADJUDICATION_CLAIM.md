# Atomic Erdős adjudication claim protocol

This protocol prevents two independent hourly workers from posting source-critical adjudications to the same issue. The linearization point is GitHub's atomic **create ref** operation, not an issue comment or a pre-write read. All three queue-reduction automations must use this gate before posting.

## Guarded worker lifecycle (`run` and `recover`)

Use the guarded `run` subcommand so claim acquisition, durable custody checkpointing, post-execution comment readback, and own-SHA release execute inside one `try`/`finally` lifecycle rather than relying on caller prompts to remember cleanup:

```bash
python3 ci/atomic_erdos_adjudication_claim.py run ISSUE_NUMBER \
  --checkpoint /path/to/claim-ISSUE_NUMBER.json \
  --worker-id WORKER_INVOCATION_ID \
  -- <worker-command...>
```

1. **Stale-custody hold:** Before calling GitHub, `run` inspects `--checkpoint`. If an unclosed checkpoint exists on disk (`phase != "CLOSED"` or `claim_still_held == true`), `run` fails closed with `STALE_CUSTODY_HOLD` (exit `7`) and does not overwrite custody or steal claims.
2. **Pre-acquire durability:** Before calling `POST git/refs`, `run` writes the newly created claim commit's exact `claim_sha`, `actor`, `worker_id`, and `nonce` to the atomic checkpoint file so even a lost create-ref acknowledgment remains recoverable.
3. **Worker execution:** Once acquired and verified by readback, `run` executes `<worker-command...>` with `GCL_CLAIM_ISSUE`, `GCL_CLAIM_SHA`, `GCL_CLAIM_REF`, `GCL_CLAIM_ACTOR`, `GCL_CLAIM_WORKER_ID`, `GCL_CLAIM_CHECKPOINT`, and optional `GCL_ASSIGNMENT_ID` in the environment, handling `SIGINT`/`SIGTERM` cleanly through `finally`.
4. **Guaranteed `finally` reconciliation and release:** On exit, error, or interruption, `run` re-reads paginated issue comments and records either newly observed adjudication comment IDs or an explicit `abort_reason`. Only after durable readback succeeds does `run` verify `GET git/ref/... == own_claim_sha` and delete its own ref. If readback fails, if the live ref SHA disagrees, or if `DELETE` fails, the checkpoint stays in `HELD_PENDING_RECOVERY` (`claim_still_held == true`) and exits non-zero.
5. **Interrupted-run recovery:** If a host crash (`SIGKILL`) leaves an unclosed checkpoint, run:
   - `python3 ci/atomic_erdos_adjudication_claim.py recover ISSUE_NUMBER --checkpoint PATH` (read-only live ref and comment reconciliation), and
   - `python3 ci/atomic_erdos_adjudication_claim.py recover ISSUE_NUMBER --checkpoint PATH --release-owned --abort-reason "REASON"` to release **only** if the live ref SHA still matches the checkpoint's exact `claim_sha`.

## Outcome classes

Every guarded run records an explicit `outcome_class` in its JSON receipt and durable checkpoint (never equating scheduler completion with substantive completion):

- `SUBSTANTIVE_ADJUDICATION` — claim acquired, worker exited `0`, paginated readback confirmed at least one new adjudication comment for the target issue/assignment, and the worker's own exact `claim_sha` ref was released.
- `READ_ONLY_COMPLETION` — no write occurred (pre-acquire ineligible/already adjudicated, post-acquire `ABORT_EXISTING` with own ref released, or worker exited `0` without posting with explicit `abort_reason` and own ref released).
- `EXCLUSIVE_CLAIM_BLOCK` — concurrent HTTP `422` ref conflict (`NOT_ACQUIRED`, exit `4`); fail-closed with no retry and no ref mutation.
- `FAILED_CLOSURE` — stale-custody hold, worker interruption/non-zero exit, ambiguous create-ref transport failure, readback failure, ref SHA mismatch, or release error.

## Standalone commands (retained for compatibility)

1. Read current protected `AGENTS.md` and applicable governance. Inspect issue, Project #2 item, `RESULT/1`, and **all** comments. Check eligibility and exact immutable source pins.
2. Run `python3 ci/atomic_erdos_adjudication_claim.py acquire ISSUE_NUMBER` from an authenticated checkout of this admitted script. Record `claim_sha`, actor, and ref from its JSON response. A nonzero exit, an existing adjudication, or a conflicting ref is a **hard no-write** result for that issue.
3. If `ACQUIRED`, recheck Project #2 item and the full comment history immediately before writing. Only the holder of the exact claim commit may post the adjudication. Reconcile an ambiguous comment submission by complete comment readback; never blindly replay.
4. Read back the posted comment ID and all comments. Release with `python3 ci/atomic_erdos_adjudication_claim.py release ISSUE_NUMBER --claim-sha SHA` **only** after durable outcome readback or documented cancellation.
5. A crash or lost response leaves the ref held. Inspect it and reconcile the outcome. **Do not automatically steal, delete, or expire claims**. Manual governed recovery must establish whether the holder posted and whether the operation remains in flight before releasing a stranded claim.

## Local checkpoint contract (`GCL-ENGINEERING-001`)

- **Owner:** the invoking worker process / scheduled job runtime.
- **Unique purpose:** execution-local atomic custody and interruption-recovery state for one in-flight adjudication claim.
- **Precedence:** GitHub issue comments and the live Git ref remain authoritative for remote truth; the local checkpoint holds only the worker's own `claim_sha` and lifecycle phase for reconciliation.
- **Failure behavior and sunset:** unclosed checkpoints fail closed (`STALE_CUSTODY_HOLD`) until reconciled via `recover`; closed checkpoints (`phase == "CLOSED"`, `claim_still_held == false`) may be archived or pruned after receipt capture.

## Invariants

- GitHub rejects a second create of the same ref; only one claimant receives `ACQUIRED`.
- Each claim is a distinct Git commit with actor, issue, worker ID (in `run`), and nonce in the message; the commit SHA is the ownership token.
- The ref is under `refs/heads/gcl-adjudication-claims/issue-N`. It is **not** a mathematical source branch or a protected-main mutation.
- Failure to fetch all comments, validate the issue, acquire the ref, or verify claim ownership prevents posting.
- A release must compare the current ref SHA with the holder's token. Concurrent release and reacquire is still a residual race if an operator bypasses the protocol; do not operate an old token after release.
- This is a *cross-worker exclusion primitive*, not a proof review, Project status update, certification, or permission to bypass protected governance.
- No queue automation should attempt this protocol until its code has passed protected PR review and is present on protected `main`.

## Acceptance tests

Mocked regression coverage in `ci/test_atomic_erdos_adjudication_claim.py` exercises: (a) successful adjudication readback and own-SHA release (`SUBSTANTIVE_ADJUDICATION`), (b) read-only completion with explicit abort (`READ_ONLY_COMPLETION`), (c) interrupted worker (`KeyboardInterrupt`/`SIGTERM`) before and after posting plus post-crash `recover`, (d) release error and readback error holding custody (`FAILED_CLOSURE` / `HELD_PENDING_RECOVERY`), (e) concurrent HTTP `422` (`EXCLUSIVE_CLAIM_BLOCK`) and ambiguous non-`422` create-ref failure, (f) pre-acquire and post-acquire existing adjudication, and (g) stale-custody hold on unclosed checkpoints and mismatched live ref SHAs (no claim stealing). Live verification on scheduled executions remains a separate operational gate tracked in `#3630`.

## Exact partial-adjudication continuation

A historical partial source audit does not constitute terminal adjudication.
The default acquire/run rules remain unchanged: any existing or ambiguous
adjudication blocks an ordinary worker. No timestamp-based selection or
implicit override is permitted. For a separately admitted corrected return,
use the same issue-wide ref and guarded checkpoint, via:

```bash
python3 ci/atomic_erdos_adjudication_claim.py inspect-continuation 2274 \
  --assignment-id ERDOS-CATALOGUE-1003-S01 \
  --predecessor-adjudication 7079364244 --continue-return 7130850350
python3 ci/atomic_erdos_adjudication_claim.py continue 2274 \
  --assignment-id ERDOS-CATALOGUE-1003-S01 \
  --predecessor-adjudication 7079364244 --continue-return 7130850350 \
  --checkpoint /path/to/new-continuation-2274.json \
  --worker-id WORKER_INVOCATION_ID --adjudication-file /path/to/review.md
```

This initial admission is deliberately restricted to issue #2274 and the
three exact authenticated historical comments in the controller's protected
`CONTINUATIONS` binding. Future cases require a separately reviewed binding;
the caller cannot supply a new hash, actor, issue, or authorized disposition.
The previous partial review and its original return remain unchanged.
The corrected return is validated with the existing source-intake parser
and protected registry. Its predecessor must be the exact typed partial
disposition; any extra return or adjudication, including a terminal
adjudication, blocks continuation. Return arbitration for multiple valid
source returns remains a separate existing mechanism; this route does not
override it.

The review file must contain a completed role-scoped source-critical pass,
with precise mathematical limitations. It is not a generic approval.
The controller generates the terminal source-design header, including the
corrected return ID/hash, superseded partial review ID/hash and exact claim
SHA. The guarded lifecycle persists the expected comment digest before
posting, rechecks the full census and protected code before the sole write,
and only accepts the exact superseding comment from the authorized actor.
The ordinary issue-wide create-ref remains the linearization point. A
competing comment or stale evidence after acquisition holds custody for
reconciliation. Missing or ambiguous write acknowledgment without exact
readback also holds custody. Recovery checks the exact comment, claim
message and owner before release; standalone release cannot release a
continuation claim. Preserve the old checkpoint and use a new path for any
subsequent attempt. The normal release read/compare race remains subject to
the existing cooperating-worker protocol; this is not an adversarial
GitHub administrator exclusion mechanism.

A terminal continuation closes the bounded source/design review only,
not the mathematical conjecture, Lean replay, certification, publication,
or any downstream research dispatch. Applicable issue/Project/Issue Field
closure remains a separate governed custody transaction and requires
readback. Candidate tests are mocked; protected deployment and live
read-only inspection must precede real use.
