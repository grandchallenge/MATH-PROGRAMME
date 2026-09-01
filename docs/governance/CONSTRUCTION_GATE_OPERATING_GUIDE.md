# Construction Gate operating guide

## Purpose

The Construction Gate preserves the identity of agent-prepared work as it moves
from ordinary construction into formal review. It creates a one-way,
tamper-resistant path from an authorized starting point to one exact review
candidate.

The Gate does not decide whether the work is correct. It does not approve or
merge a pull request, prove or certify mathematics, authorize publication, or
authorize an external claim.

## The user does not need Gate vocabulary

Users should request the outcome they want in ordinary language. The agent is
responsible for recognizing when the Gate applies, explaining the proposed
transition, finding the exact commit, and operating the technical workflow.

| Ordinary request | Agent interpretation |
| --- | --- |
| "Start work on X" or "continue revising X" | Work on an ordinary branch. Do not invoke the Gate merely because work is underway. |
| "Run the checks" or "tell me whether X is ready" | Observe and validate only. Do not move or freeze a governed reference. |
| "Prepare this exact version for governed review" | Consider admitting the exact prepared commit to the governed development reference. Confirm that X is a registered target and that the protected scope permits the change. |
| "This is the final review version", "lock this candidate", or "submit this exact version for formal review" | Attempt to freeze the exact governed development head as the immutable candidate. If the wording does not clearly establish finality, ask before freezing. |
| "Address the review changes" after a candidate is frozen | Do not alter the frozen candidate. Prepare a new authorized target or revision path. |
| "Approve this", "merge this", "certify this", or "publish this" | Use the separate process and authority for that outcome. A Gate operation supplies none of those authorities. |

The technical workflow uses three operation names:

- `CREATE_DEVELOPMENT` creates the governed development reference at the exact
  predecessor authorized by protected `main`.
- `UPDATE_DEVELOPMENT` moves that reference to one exact prepared commit within
  the authorized path scope. This admission is sometimes described as
  **advancing** the target.
- `FREEZE_CANDIDATE` creates the immutable candidate reference at exactly the
  governed development head. This is **freezing** the candidate.

These are implementation terms, not words the user must use.

## Where ordinary revision happens

Ordinary drafting, repairs, rebases, and exploratory review happen before Gate
admission on a normal working branch. The governed development reference is not
intended to replace that working branch.

The active policy denies a governed development update when exact-head evidence
already exists for its current version. Once a candidate reference exists, the
development reference is frozen as well. Consequently, an agent must not
describe the governed development reference as indefinitely editable or assume
that earlier review evidence survives changed bytes.

The practical sequence is:

1. Draft and revise on an ordinary branch.
2. Identify the exact prepared commit and run the relevant checks.
3. Ensure protected `main` contains a target row authorizing the predecessor,
   lifecycle, governed references, and path scope.
4. Create the governed development reference if it does not exist.
5. Admit the exact prepared commit with `UPDATE_DEVELOPMENT` when preflight
   permits it.
6. Freeze that exact development head with `FREEZE_CANDIDATE` when the user has
   clearly requested the final review candidate.
7. Conduct human review, disposition, and any protected merge through their
   separate authority paths.

If a repair is required after freezing, preserve the frozen candidate as
historical evidence. Do not force-update, delete, or replace it in place. A new
target or another protected-main-authorized revision path is required.

## When the Gate applies

The Gate applies only to targets registered in the
[`construction_integrity_contract.json`](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/construction_integrity_contract.json)
and only to mutations of their `gcl/dev/*` and `gcl/candidate/*` references.
It is not automatically invoked by every commit, branch, pull request, test
run, approval, or merge request.

If the requested real target is not registered, the agent must stop before any
governed mutation and explain that a protected-main change is needed to define:

- the target identifier;
- the authorized predecessor;
- the allowed and forbidden path scope;
- the development and candidate references; and
- the lifecycle policy.

Registration is a governance change. The operator cannot supply substitute
authority at workflow-dispatch time.

## Agent decision rule

Before a Gate mutation, the agent must:

1. Translate the user's ordinary-language outcome into the proposed Gate
   transition and state that translation plainly.
2. Read the active contract from protected `main`; do not rely on a feature
   branch copy or chat memory.
3. Verify the target registration, current lifecycle, exact predecessor,
   current governed heads, proposed exact commit, and changed-path scope.
4. Use the
   [Construction Gate runtime workflow](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/.github/workflows/construction-gate-runtime.yml)
   rather than directly pushing to a governed namespace.
5. Report the allow or denial and the exact resulting references. A denial is a
   safe outcome and must not be bypassed.

Clear outcome language can authorize the corresponding attempt. For example,
"prepare this exact version for governed review" can authorize admission if all
preconditions are already satisfied, and "lock this exact version as the formal
review candidate" can authorize freezing. Ambiguous requests such as "looks
good" or "get it ready" do not by themselves establish irreversible finality.

## Authority boundaries

A successful Gate operation establishes only that the exact reference mutation
was allowed by the protected construction contract and performed by the
separate Gate identity.

It does not establish:

- substantive correctness or mathematical proof;
- campaign admission;
- human approval or disposition;
- permission to merge to protected `main`;
- certificate issuance;
- publication permission; or
- permission to make an external claim.

Those decisions remain with their existing checks, reviewers, Human Steward,
Council, protected-branch, and certification processes as applicable.
