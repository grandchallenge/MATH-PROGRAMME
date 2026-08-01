# Administrative Maintenance Terminology Registry

**Registry extension:** `MP-ADMIN-TERMS-001`  
**Parent registry:** `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`  
**Decision:** ADR-0016  
**Status:** Accepted for protected-merge activation

This controlled extension registers terms introduced by `MP-ADMIN-MAINT-001`. Where a term conflicts with the parent registry, the parent registry controls unless ADR-0016 explicitly narrows the maintenance meaning.

| Term | Canonical meaning | Boundary and exclusions |
|---|---|---|
| Core Clarity | The condition in which authority, exact identity, current state, validating workflow, exact-head evidence, permitted next action, and prohibited claims are explicit without inference. | Does not assert that the governed mathematics is correct or complete. |
| Material change | A change that alters authority, lifecycle, route, claim, promotion, accepted evidence, prohibited use, consumed provider content, required workflow, or branch-protection semantics. | Repository-head movement alone is not material when every consumed artifact blob is unchanged. |
| Nonmaterial change | A change that preserves protected semantics and every consumed material artifact identity, such as a mirror refresh, typographic repair, or unrelated provider-head movement. | Classification requires evidence; uncertainty fails closed. |
| Event-triggered synchronization | Immediate cross-repository repair and validation required after a material governed change. | Periodic cadence cannot delay this obligation. |
| Accelerated maintenance time scale | The Human Steward rule multiplying every proposed maintenance duration and cadence interval by `0.1`. | Does not delay immediate event-triggered obligations or change mathematical time assumptions. |
| Accelerated pilot | The nine-day operating period beginning at the protected merge timestamp of PR #184. | A pilot is operative governance evidence collection, not provisional mathematical authority. |
| Workflow coverage | The recorded combination of capability, trigger, required-check state, exact-head execution, success and failure evidence, owner, repair route, and last verified identity. | A workflow file or historical green run alone is insufficient. |
| Canonical tracker | The designated issue or navigation surface that points to protected authority, current lifecycle and route state, next obligation, claim boundary, and review trigger. | It cannot create protected state. |
| Issue mirror | A mutable issue, pull request body, or comment that explains or navigates protected authority. | It cannot change lifecycle, route, certification, or claim state. |
| Tracker refresh clock | The binding `PT7H12M` interval after a protected material transition for updating the canonical tracker. | A documented interruption may pause only this mirror clock; protected state remains unchanged. |
| Administrative waiver | A typed, scoped, expiring exception with owner, evidence, approver, prohibited uses, repair obligation, and renewal count. | It cannot authorize claim promotion. Cross-repository, provenance, certification, and required-check waivers require Council authority. |
| Emergency override | A temporary control used only to restore availability, respond to a security incident, or restore CI operability. | It cannot promote, admit, adjudicate certification, weaken branch protection, or delete evidence. It expires after `PT7H12M`. |
| Maintenance-burden circuit breaker | The fail-closed mechanism that freezes affected campaigns or new admissions when critical coverage, required-check evidence, repair latency, or repeated-review thresholds are breached. | It is an administrative containment action, not a judgment on mathematical merit. |
| Campaign-level fail closed | Immediate suspension of promotion for the affected campaign when a critical required capability is missing or stale. | Does not automatically suspend unrelated campaigns unless the portfolio circuit-breaker threshold is met. |
| Portfolio admission freeze | The prohibition on new campaign admission when two active campaigns or more than 20 percent of the active portfolio are incomplete, whichever threshold is stricter, or another D7 trigger applies. | Existing mathematical blockers and records remain preserved. |
| INTELLECT Phase A buy-in | Constitutional acceptance of the authority split, acceleration rule, stale-contract rejection, claim boundaries, and obligation to exact-pin the future protected Programme merge. | It is not the final content-addressed adoption. |
| INTELLECT Phase B protected adoption | The protected INTELLECT record pinning the exact MATH-PROGRAMME merge and Git blob identities of the maintenance control, decision, and mirror policy, with fail-closed tests and exact-head CI. | Final administrative closure is prohibited before this state. |
| Protected-merge activation | The rule that an approved artifact becomes operative only when merged to the protected branch after required review and checks. | Draft branches, issues, comments, and PR approval alone do not activate it. |
| Final cross-repository closure | The state after Programme protected merge, INTELLECT Phase B protected adoption, exact-head validation, and external attestation. | Does not promote any mathematical or external claim. |

## Change control

A term in this extension may change only through a decision record that names the affected control, consistency checks, review evidence, supersession boundary, and claim boundary.
