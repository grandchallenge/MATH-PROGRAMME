# Atomic Erdős adjudication claim protocol

This protocol prevents two independent hourly workers from posting source-critical adjudications to the same issue. The linearization point is GitHub's atomic **create ref** operation, not an issue comment or a pre-write read. All three queue-reduction automations must use this gate before posting.

## Worker procedure

1. Read current protected AGENTS.md and applicable governance. Inspect issue, Project #2 item, RESULT/1 and **all** comments. Check eligibility and exact immutable source pins.
2. Run `python3 ci/atomic_erdos_adjudication_claim.py acquire ISSUE_NUMBER` from an authenticated checkout of this admitted script. Record `claim_sha`, actor and ref from its JSON response. A nonzero exit, an existing adjudication, or a conflicting ref is a **hard no-write** result for that issue.
3. If ACQUIRED, recheck Project #2 item and the full comment history immediately before writing. Only the holder of the exact claim commit may post the adjudication. Reconcile an ambiguous comment submission by complete comment readback; never blindly replay.
4. Read back the posted comment ID and all comments. Release with `python3 ci/atomic_erdos_adjudication_claim.py release ISSUE_NUMBER --claim-sha SHA` **only** after durable outcome readback or documented cancellation.
5. A crash or lost response leaves the ref held. Inspect it and reconcile the outcome. **Do not automatically steal, delete, or expire claims**. Manual governed recovery must establish whether the holder posted and whether the operation remains in flight before releasing a stranded claim.

## Invariants

- GitHub rejects a second create of the same ref; only one claimant receives ACQUIRED.
- Each claim is a distinct Git commit with actor, issue and nonce in the message; the commit SHA is the ownership token.
- The ref is under `refs/heads/gcl-adjudication-claims/issue-N`. It is **not** a mathematical source branch or a protected-main mutation.
- Failure to fetch all comments, validate the issue, acquire the ref or verify claim ownership prevents posting.
- A release must compare the current ref SHA with the holder's token. Concurrent release and reacquire is still a residual race if an operator bypasses the protocol; do not operate an old token after release.
- This is a *cross-worker exclusion primitive*, not a proof review, Project status update, certification or permission to bypass protected governance.
- No queue automation should attempt this protocol until its code has passed protected PR review and is present on protected main.

## Acceptance tests

Exercise (a) two simultaneous contenders for the same unused issue (exactly one ACQUIRED), (b) a pre-existing adjudication (neither creates a ref), (c) lost create-ref acknowledgment (readback and hold; no blind retry), (d) wrong-SHA release (ref preserved), (e) owner crash (ref remains held), and (f) independent issues (claims do not interfere). Run these on a test repository or disposable test issues, not live research items.