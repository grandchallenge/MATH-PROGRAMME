# Canonical GCL Handoff Takeover Prompt

Use this prompt to start any substantial GCL work-set takeover. Replace only the placeholders in the opening lines unless a domain-specific handoff explicitly requires additional material context.

```text
Take over `<WORKSET-ID>` in `<OWNER/REPOSITORY>`, tracked by `<ISSUE/PR/WORKSET POINTER IF APPLICABLE>`.

Treat this prompt only as a pointer. Do not rely on conversational history or stale handoff state.

Re-fetch protected live repository state first, then start at:

`handoffs/<WORKSET-ID>/README.md`

Before mutation, read and inherit the canonical operating contract at:

`handoffs/README.md`

The following controls govern this work unless an exact domain-specific instrument materially overrides them:

- `MP-STREAMLINED-EXECUTION-001`
- `MP-SUBSTANCE-FIRST-EXECUTION-001`

Do not reproduce those controls into the domain handoff. The domain handoff is intentionally thin and contains only work-set-specific state, acceptance criteria, authoritative pointers, dependencies, and exact stop conditions.

First produce the mandatory canonical preflight:

LIVE PROTECTED HEAD
CONTROLLING DOCTRINE REVISIONS
PRIMARY DELIVERABLE
MATERIAL ACCEPTANCE CRITERIA
CURRENT SUBSTANTIVE STATE
SMALLEST SAFE EXECUTABLE TRANCHE
MATERIAL CLOSURE
MINIMUM REQUIRED CONTROL PATH
AFFECTED CHECKS
PROCESS ARTIFACTS PROPOSED
PROCESS NECESSITY TEST: pass / fail
DRIFT TRIPWIRES ACTIVE: none / list
AUTHORITY REQUIRED: delegated / reserved

Then immediately effectuate the `SMALLEST SAFE EXECUTABLE TRANCHE`.

Execution rules:

- Keep the `PRIMARY DELIVERABLE` as the object of optimization.
- Treat governance, CI, provenance, release engineering, synchronization, evidence, and repository mechanics as subordinate controls.
- Do not create a process artifact or additional control step unless its `PROCESS NECESSITY TEST` passes.
- Do not use machine evidence as a proxy for substantive mathematical, scientific, technical, editorial, or product quality beyond what the evidence actually tests.
- Distinguish substantive progress, substantive verification/review, required governance state, and incidental process state in every continuation.
- If two consecutive continuations occur without material advancement of the primary artifact, re-plan before continuing.
- If supporting machinery fails, determine whether it actually blocks a material acceptance criterion or reserved authority boundary before repairing or expanding it.
- Do not reproduce historical ceremony that is no longer a live material dependency.
- Prefer terminal completion of a meaningful substantive unit over accumulation of branches, manifests, evidence packets, gates, or intermediate state.
- Proceed autonomously through routine bounded work under standing delegated authority.
- Do not request Human Steward, Referee, Council, or other approval unless an exact governing instrument materially reserves the transition. If authority is `reserved`, cite the exact instrument and transition.
- Stop only for a genuine material blocker, material scope/control-plan change, exact reserved authority boundary, substantive contradiction/failure requiring escalation, or completed material closure.

If the existing `handoffs/<WORKSET-ID>/README.md` materially conflicts with the canonical handoff contract by duplicating obsolete ceremony or process, preserve historical evidence but follow the live canonical controls and identify the shortest safe path back to substantive execution.

For any new handoff material created during this work, use:

`handoffs/_TEMPLATE/README.md`

Do not invent a new handoff structure or operating doctrine.
```

## Usage

Normally replace only:

- `<WORKSET-ID>`
- `<OWNER/REPOSITORY>`
- `<ISSUE/PR/WORKSET POINTER IF APPLICABLE>`

Everything after the opening pointer should remain stable. Domain-specific execution detail belongs in `handoffs/<WORKSET-ID>/README.md`, not in a rewritten takeover prompt.
