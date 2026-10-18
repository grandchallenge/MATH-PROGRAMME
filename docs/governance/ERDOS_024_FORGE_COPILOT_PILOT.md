# Erdős-024: unattended Forge mathematical critique canary

**Transaction:** ERDOS-024-FORGE-COPILOT-PILOT-001. **Mode:** bounded production controller canary, evidence-only; no research claim or permission expansion. **Subject:** Problem #41 finite semantic difference. **Protected cohort:** `governance/erdos_catalogue/ROLLING_RESEARCH_024.json`.

## Existing authority

- MATHFORGE is responsible for authentic source/premise reconstruction and semantic review. The programme's source critic docket is [#2536](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2536); its exact [source return](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1310#issuecomment-6104193801) is **unadjudicated**.
- MATHSOLVE alone hosts separately protected, reservation-controlled mathematical execution assignments and their capture/replay/adjudication chain.
- MATHCERT alone may certify mathematical claims, under its existing substantive independence controls.
- Source critical reviews are **not** accepted mathematical claims; routine protected engineering should not invoke a new Human Steward approval ceremony.

## Executable canary

The already registered persistent `.github/workflows/erdos-catalogue-queue-projection.yml` retains Project #2 reconciliation and gains two **separately permission-scoped jobs** after protected-main push. No other workflow or controller is created.

1. **Preparation/read-only model job:** First require a successfully reconciled production queue, with review issue #2536 carrying both authenticated direct-editorial availability labels AND authoritative `GCL State=AVAILABLE`. Confirm the protected 24-slot roster, exact catalogue issue #1310, result comment ID 6104193801 and content hash, and the Formal Conjectures upstream pinned commit and Git blob. If any assertion fails, preserve the exact blocker **without spending AI credits**.
2. **Isolated model execution:** If ready, launch a fresh Github Copilot CLI process authenticated using the one-run `GITHUB_TOKEN` and `copilot-requests: write`. No personal credential, API key or GitHub Models endpoint. Pin CLI version 1.0.66, model selection `gpt-5.4`, read-only tool allowance, no MCP servers, and refuse shell, URL and write permissions. Timeout 420 seconds. One model call per protected-main changed-substrate event, **no scheduled Copilot retry**, and a soft maximum of 30 GitHub AI Credits per call (about \$0.30 before any soft-limit overshoot); organization usage policy/budget may deny execution. Exact CLI version and evidence input/output are retained as run artifacts. Newer models/runtimes require a separate protected revision.
3. **Separate trusted evidence publisher:** A different Actions job, without `copilot-requests: write`, validates the output schema and exact source result hash, checks live claim/queue/custody again, and publishes only `GCL-FORGE-CRITIQUE-CANDIDATE/1` to issue #2536. The model's role is **a critical mathematical evidence generator, not source acceptance**. Only the trusted publisher holds issue write permission. If the model fails, times out, exceeds its soft credit cap, or returns malformed content, an artifact records the failure; it cannot manufacture acceptance. Duplicate reviews are never re-billed/published after a successful candidate receipt.

## Mathematical target and safeguards

Independently assess the finite-set discrepancy identified in the candidate: for B={1,2,3}, the 3-element FINSET uniqueness predicate holds vacuously but the triples (1,1,3) and (1,2,2) have the same sum 5. The deterministic code independently verifies the **finite witness only**. The actual historical interpretation of repetitions is not established by the witness; original problem research status, source-semantic acceptance, the infinite Erdős conjecture, and upstream Lean build/certification stay unresolved.

All authority-effect booleans are false. A second AI call, different workflow run, separate short-lived token, or an automated reviewer verdict is NOT proof of the substantive specialist independence required for a promoted source theorem or MATHCERT. More stringent review remains routed to the domain specialist. If the worker cannot access the organization Copilot quota/policy, record `COPILOT_EXECUTION_UNAVAILABLE` rather than impersonating an independent agent.

## Gates, continuation and acceptance

- **Gate A:** 24 original source returns, reviewed critical issues and protected roster are already admitted; do not reopen authorship.
- **Gate B:** Queue publisher has populated issue #2536 in Project #2, with correct Issue Field and status; fail closed if absent.
- **Gate C:** Actual Copilot Actions run reports available organizational quota and produces a bounded read-only result.
- **Gate D:** A separate trusted job validates and posts the full unadjudicated reviewer candidate once, with workflow provenance; read back original comment and source hash.
- **Gate E (NOT PART OF THIS CANARY):** MATHFORGE independently adjudicates source semantics, after which a separately authorized immutable MATHSOLVE work package can be admitted and captured/replayed. Any proof-grade claim goes through MATHCERT. Refill is by protected controller transaction only.

The pilot is **not completed** by green PR checks or an Actions job reporting success without a posted, externally inspectable evidence receipt and exact field/label readback. Do not scale to 24 AI executions or activate any automatically claimable Solve dispatch before the protected end-to-end results for #41 are observed and reviewed.

## Recovery

Re-read protected Programme `main`, the target issue's Issue Field and comments, the exact Actions run and artifact, and `ci/erdos_forge_copilot_pilot.py`. Address a missing field, Copilot authorization denial, or missing model before attempting any publication. Never assume the model had privileges or treat an empty output artifact as mathematical review. The model and publication jobs do not self-authorize a follow-up Forge→Solve→Cert transition.
