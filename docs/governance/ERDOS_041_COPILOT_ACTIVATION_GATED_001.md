# Erdős #41 — queue-first authenticated Colab execution route

**Decision:** Copilot is removed from the active implementation glidepath. The existing Copilot model and publication jobs in `.github/workflows/erdos-catalogue-queue-projection.yml` remain explicitly disabled. They are legacy quarantined code, **not** an execution dependency or fallback. Retire them via a separately protected clean-up diff; do not turn their gates on.

**Status:** PROPOSED / NOT EXECUTED. This review document alone does not grant new credentials or certify mathematical claims.

## Operating contract

1. **Queue authority.** GitHub Project #2 and protected repository work packets remain the durable job registry and lifecycle authority. Workers may retrieve an available item and submit an authenticated claim or RESULT/1 using existing admitted intake. Require exact queue field, label, issue, immutable task/source hash and lease/claim check. No hidden Colab-only queue.
2. **Execution.** The existing GCL GSD/QTR Colab runner is the preferred computational host, subject to validation against its actual source and live environment. Kickoff may be manual (a human or already authorized operator starts a notebook) or automatic (existing authorized controller starts a bounded job). Neither method changes governance standards. Use an available model adapter; **do not require Copilot**. If model access or execution credentials are absent, return a precise blocker rather than pretending execution occurred.
3. **Authentication.** Reuse an already authorized GitHub operator or scoped GitHub App token as allowed by protected policy. Never ask for independent accounts merely because the same system performs Researcher, Verifier, Adversary and Referee roles. Do not put privileged tokens into an untrusted prompt, notebook output, public artifact or model-accessible filesystem. Issue-writing belongs to a distinct trusted publication stage, even when operator identity is shared.
4. **Logical review roles.** Record `reviewer_system_id`, distinct `logical_pass_id`, mode, exact subject hash, criteria, evidence, finding, open obligations. Authoring-system Adversary/Referee passes are `non_authoring_read_only`, cannot repair during that pass and must be restarted after material changes. This is logical audit separation, **not** a claim of an independently authenticated GitHub APPROVED review.
5. **Bounded execution.** Job reservation or lease, explicit per-attempt resource allowance (time, compute, model/API cost if relevant), retry policy, cancellation behavior and duplicate-run handling are required. Manual kickoff is acceptable: the source-lock and lifecycle readback remain mandatory. Do not depend on an automatically recurring paid runner.
6. **Evidence/return.** Capture job ID, invocation mode, operator ID, runner version, environment/dependency lock, model provider/version (if any), run/attempt ID, elapsed time and measured usage when provided; SHA-256 of input source, worker result, produced output and deterministic replay. A trusted authenticated publisher validates schema, exact source binding and duplicate receipt status before posting provisional `GCL-FORGE-CRITIQUE-CANDIDATE/1` or applicable RESULT/1 evidence. Failed jobs return a typed failure and log reference.
7. **Mathematical boundaries.** Forge critique remains provisional. Solve admission uses existing protected dispatch, replay and adjudication. MATHCERT and externally promoted theorem claims retain their stronger substantive independence and protected review. Preserve all reserved credential, protection and publication gates.

## First canary — Erdős #41

- Job: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2536
- Verify live Project #2 status AVAILABLE and label/issue bindings before allocating compute.
- Reproduce finite contrast on `B={1,2,3}`: `1+1+3=1+2+2=5` distinguishes multiset triples; only one three-element subset of B exists. This does **not** settle the infinite Erdős conjecture or its historical repetition convention.
- Execute one source-pinned Colab run, manually or via existing authorized controller, with researcher/verification/adversarial traces and a read-only adversarial pass. Return either replayable provisional evidence or explicit typed blocker.
- Verify capture → replay → adjudication/state readback according to existing admitted roles without fabricating Solve leases or certification.

## Admission / migration boundary

This draft documents the **replacement** of the former Copilot activation proposal, not its activation. Existing workflow hold remains effective. Before live Colab execution, verify the runner's actual repo/version, model adapter, available GitHub credentials and permission scope, resource limits, artifact upload trust, and existing queue issue readback; record exact role-scoped assessments. Any new privileged automated execution or protection-sensitive configuration must follow its own actual protected admission route. A separate physical GitHub reviewer identity is necessary only where a specifically invoked existing contract requires it.

Success is an authenticated queue-to-evidence pilot with reproducible output and zero inappropriate claim authority, regardless of whether kickoff is automatic or manual.
