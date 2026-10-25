# Operation-scoped recovery and uninterrupted research

**Authority:** Human Steward directive, 2026-10-25; proposed programme amendment, binding only after protected admission.

## Principle

An error belongs to the *specific invocation* that produced it. A platform decision about one write is not evidence that the research is unsafe, the entire work package lacks authority, the repository is unavailable, or its other pending operations are prohibited.

Classify each invocation using its exact intended operation, repository, path, expected source identity, arguments, transport, and observed response. Keep a denied operation on hold. Do not elevate that hold to the whole task by default.

## 1. Four operational classes

1. **Successful operation:** reconcile the actual remote result and record its durable identity. Do not confuse a submitted request with successful admission.
2. **Recoverable operational failure:** for timeouts, unavailable services, malformed responses and other nondeterministic tooling problems, use bounded recovery and exact-state reconciliation. A mutation with uncertain outcome requires readback before any repeat.
3. **Explicit platform-denied operation:** record the exact denial and do not automatically retry, disguise, alter its semantics to evade detection, or route that *same denied operation* through another transport. This restriction applies to the invocation, not to all future mathematical work.
4. **Genuine substantive or authority boundary:** stop the affected research claim, protected mutation, certification or external publication until the corresponding mathematical or authority requirement is met. A gateway denial with no reason is not itself proof of a substantive mathematics defect.

The classifier cannot infer that benign material was found harmful merely from an opaque platform error.

## 2. Work-item continuity

After any denial, divide the remaining tasks into: **completed and remotely verified**, **permitted and independently executable**, **locally testable/read-only**, and **operation-held**. Execute the second and third classes without waiting for the held operation. Do not manufacture a blanket research freeze, new Human Steward approval, support ticket, PR, or council ceremony for independently authorized work.

A separately identified operation is independent only if it has a distinct legitimate purpose, not if it merely reproduces the denied mutation with different wording, packaging, identity, or tool. The current user's instructions do not grant permission to override a platform restriction.

## 3. Mathematical editorial corrections and reviews

A one-sentence correction to explanatory mathematics ordinarily requires a source-identity check, exact diff, mathematical source preflight, and applicable reviewer assessment; it does not require an unrelated full-project replay or new scientific certification. The same source-specific standard applies when preparing critique of the corrected text.

If the edit operation itself was explicitly platform-denied, prepare and verify its correction in a separate local workspace **without publishing it**; preserve the pending status and request legitimate clarification/remediation for that exact operation. The local copy and its hashes are evidence, not a protected commit. No alternative publication route may be used to accomplish that denied operation absent a substantive, verified authorization that clears the denial.

If the original operation was only a transient failure, the bounded ordinary recovery ladder applies instead; do not misclassify it as a safety denial.

## 4. Review and admission

Separate three facts: (a) mathematics has been checked; (b) a logically distinct critic role has inspected the exact material; (c) protected GitHub admission and readback succeeded. A file or comment does not certify itself. If a policy amendment touches security-sensitive protections or substantive certification, use the applicable competent delegated specialist role and existing protected PR checks; do not require routine Human Steward review when existing authority suffices.

Protected status must never be inferred from a locally tested copy, a branch commit, the existence of a PR, or an automatic-merge request.

## 5. Service and support

Open one classified incident per material provider defect, deduplicating repeated observations by exact operation and evidence. Support escalation is an **exception** where remediation actually requires the provider; it is not the default for generic connector or CI failure. Suppress repeated complaints about the same unchanged denial. Record specific tool action, remote/nonremote outcome, content identities and any available correlation ID; do not invent a policy cause.

## 6. Acceptance scenarios

- Explicit denial of writing file A; local tests for file A and independent work on file B continue; no rewrite of A via another transport.
- Transient failure during a read; bounded recovery obtains evidence; no Human Steward approval.
- Uncertain write result; inspect remote state first; do not duplicate the mutation.
- Mathematical review succeeds locally while protected PR is pending; report review and admission as separate statuses.
- New exact evidence establishes remediation of the denied operation; a newly authorized exact-head action can be evaluated under current platform and GCL controls, with no automatic replay.
- A user requests a safer process description; technical prompts remain accurate, concise and operation-specific without attempting to change the substance of a denied action.

## Precedence and limits

This amendment interprets GCL operational recovery and streamlined execution consistently with superior standards. It does **not** alter OpenAI platform enforcement, GitHub branch protections, restricted provider actions, MATHCERT authority, security-sensitive gates or the mathematical burden of proof. Historical incident reports and frozen evidence remain unchanged.
