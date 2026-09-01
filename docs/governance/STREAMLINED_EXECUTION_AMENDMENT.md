# Streamlined execution amendment

**Control:** `MP-STREAMLINED-EXECUTION-001`  
**Authority:** Human Steward directive, 2026-09-01  
**Status:** binding on protected merge; supersedes contrary routine-process requirements  

## Purpose

Remove administrative blockers that do not protect a material mathematical, certification, security, provenance, or authority boundary. This amendment is deliberately narrow. It does not create a new control plane.

## 1. Delegated execution replaces routine approval ceremony

For bounded administrative, documentation, engineering, workflow, maintenance, routing, synchronization, and campaign-execution changes within already-authorized scope, standing delegated authority is sufficient to execute the transaction through protected merge and readback.

Routine work does **not** require a fresh Human Steward approval or a fresh independent-review approval merely because a new commit, synchronization commit, or protected-main commit exists.

Where separation of duties is materially required, the review function may be performed by an appropriately skilled non-author delegated agent. This is a delegated operating role, not a per-transition Human Steward approval gate. A Human Steward disposition is required only where authority is expressly reserved and cannot be delegated by the governing instrument.

Independent specialist review remains appropriate for substantive mathematical certification, source-semantic adjudication, constitutional authority expansion, security-sensitive protection weakening, or external claim promotion. Such review is attached to the material object under review; it is not invalidated by unrelated repository activity.

## 2. Evidence-closure identity

Governed evidence binds to a **material evidence closure**, not indiscriminately to the whole repository head.

The closure consists of:

- the governed changed bytes;
- directly consumed protected artifacts and their content identities;
- validators, schemas, workflows, toolchain pins, and policy bytes that can affect the conclusion;
- the declared authority and claim scope.

A later commit invalidates prior evidence only when it changes that closure, creates a merge conflict affecting it, or changes the authority/claim boundary relevant to the transaction.

Unrelated movement of `main`, unrelated documentation, independent campaigns, or byte-identical synchronization merges do **not** invalidate checks, delegated dispositions, or specialist review. No rebase, synchronization merge, rerun, or re-approval is required solely to make a branch numerically current with `main`.

The existing administrative-maintenance distinction between repository head and material artifact identity is controlling for concurrent development.

## 3. Concurrent development rule

Protected branches may advance concurrently. A candidate may merge from an older base when all of the following hold:

1. GitHub reports the candidate mergeable without a material conflict;
2. required checks for the candidate's material closure pass;
3. no relevant protected dependency in that closure changed since validation;
4. the candidate does not widen its governed scope or authority.

If protected `main` advances only in disjoint material closures, the candidate remains valid. Agents must not manufacture synchronization commits merely to refresh the base SHA.

## 4. CI proportionality

Pull-request CI must be impact-routed.

- Cheap classification and syntax/schema checks may run on every candidate.
- A substantive shard runs only when its governed inputs or validator dependencies changed.
- Lean replays, external repository replays, full-estate conformance, publication builds, and other expensive checks do not run on unrelated changes.
- A required status context for an unaffected expensive lane may complete by a cheap content-identity/impact determination that records `UNCHANGED_ATTESTATION_REUSED` or equivalent.
- Full sentinel/replay runs belong on relevant material changes, explicit dispatch, or low-frequency scheduled assurance, not on every tiny PR.
- Unknown impact fails closed into the smallest defensible affected set; it does not automatically imply a full-estate replay unless the classifier itself or its dependency map is affected.

New required CI must identify its trigger set and expected marginal cost. A new routine check should replace, subsume, or demonstrably justify existing cost rather than simply accumulate.

## 5. Merge and readback

Routine bounded execution sequence is:

`classify material closure -> run affected checks -> exercise delegated disposition -> protected merge -> protected readback`.

There is no generic independent-approval stage and no generic Human Steward approval stage.

A protected readback establishes the merged result. It does not trigger a second approval cycle.

## 6. Supersession

For routine bounded work, this amendment supersedes contrary requirements in earlier maintenance plans, handoff packs, runbooks, issue templates, PR prose, or design documents that require:

- fresh independent approval on every exact commit;
- fresh Human Steward approval where standing delegation already covers the action;
- invalidation solely because protected `main` advanced;
- synchronization solely to make a base current;
- full or expensive CI for an unaffected material closure.

Historical records remain historically accurate; they need not be rewritten. Active automation and current operating documentation should be reconciled mechanically when encountered.

## 7. Non-expansion boundary

This amendment reduces ceremony; it does not promote mathematics, certify a theorem, alter source provenance, widen a campaign claim, weaken security controls, or authorize external claims. Delegation cannot be used to manufacture substantive mathematical independence where the same actor produced and certifies the same mathematical claim.
