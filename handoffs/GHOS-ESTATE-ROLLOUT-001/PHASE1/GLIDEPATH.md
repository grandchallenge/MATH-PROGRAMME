# GHOS-ESTATE-ROLLOUT-001 — Phase 1 execution glidepath

This is the ordered execution procedure for a replacement agent starting with no useful transcript. Read `HANDOFF.md` and `STATE.json` first.

## 0. Cold-start reconstruction

Before modifying any repository:

1. Re-fetch `grandchallenge/MATH-PROGRAMME/main`, umbrella issue `#724`, and this handoff pack from protected `main`.
2. Re-fetch `grandchallenge/.github/main`, ruleset `17137624`, `.ghos-routing/control.json`, and the shared gate at exact commit `ef1cce6029233a68cf46063cea2384772fcae613`.
3. Verify the gate blob is `f9f85937713046eacdc79c532046c676cbb4550c` and SHA-256 is `fc0a9a4d20de72e9fbc04c8cd54cffc3a6e4657fb09e7978b360616bd5e94a17`.
4. Re-fetch `gcl-standards/main` and ruleset `19962512` as a second protected reference implementation.
5. Re-fetch MATH-PROGRAMME dedicated routing ruleset `21969152`. Treat ruleset `17137629` as a separate Programme profile.
6. Confirm `.github#67` remains closed completed as `GHOS_ROUTING_ENFORCED`.
7. Re-fetch all four Phase-1 trackers and protected heads. Any head movement invalidates byte-derived inventory and feature evidence from this handoff.
8. Search for already-open Phase-1 implementation or hostile PRs before creating branches. Adopt valid durable work rather than duplicating it.

Do not start from a candidate branch remembered from chat.

## 1. Common Phase-1 bootstrap pattern

For each repository, use a two-stage protection sequence.

### Stage A — install the control under existing protection

1. Snapshot protected `main`, every applicable ruleset, required contexts, bypass actors, and direct workflow inventory.
2. Enumerate all `.github/workflows/*.yml` and `.yaml` files at that exact head.
3. Derive each workflow's feature vector with the exact shared-gate semantics. Do not infer features from filenames.
4. Create `.ghos-routing/workflows.json`:
   - `record_type`: `GHOS_EXECUTION_ROUTING_REGISTRY`;
   - `schema_version`: `1.0.0`;
   - exact repository identity;
   - exact admitted `GITHUB_ACTIONS` controller catalog;
   - lexicographically exact complete workflow path coverage;
   - exact byte-derived feature arrays and topology;
   - controller only where topology is non-bounded;
   - all authority/claim boundaries false.
5. Add `.github/workflows/ghos-routing-enforcement.yml` using the Phase-0 candidate-independent pattern.
6. Do not copy the MATH-PROGRAMME dependency line. The Phase-1 targets lack `requirements/policy.txt` at the handoff baselines. Use an explicit reviewed dependency install; `python -m pip install PyYAML==6.0.3` is the established shared-gate-compatible pin from protected `.github` tests.
7. Enforcement requirements:
   - `pull_request_target` only for PR inspection;
   - `permissions: contents: read`;
   - protected-base and candidate checkouts read-only with `persist-credentials: false`;
   - candidate workflow/scripts never executed;
   - externally governed gate checkout pinned to `ef1cce6029233a68cf46063cea2384772fcae613`;
   - SHA-256 verified before gate execution;
   - exact `GITHUB_REPOSITORY` passed as repository identity.
8. Add focused local tests only where useful for reproducibility. Do not fork or weaken classifier semantics.
9. Open the implementation PR against the exact protected base. Request independent review immediately.
10. Require all existing repository checks plus a passing routing-enforcement result on the exact candidate. Because routing is not yet a required context in Phase 1, this pre-admission run is evidence, not yet structural protection.
11. Re-read PR head, protected base, reviews, threads, and checks immediately before merge. If head moved, invalidate stale evidence.
12. Merge only the exact reviewed candidate through existing protected controls.
13. Read protected `main` back and verify exact parentage and exact registry/enforcement bytes.

### Stage B — make routing structurally mandatory

1. Snapshot the complete ruleset pre-state immediately before administration.
2. Add `routing-enforcement` without removing existing required contexts or adding bypass actors.
3. Preserve existing strictness for INTELLECT, MATHFORGE, and MATHSOLVE.
4. For MATHCERT, default to a new dedicated active strict zero-bypass ruleset requiring only `routing-enforcement`; leave ruleset `17137628` unchanged unless an explicit policy decision authorizes changing Cert-profile strictness.
5. Independently read the complete post-state. A settings UI success message is not sufficient evidence.
6. If a mutation response is ambiguous, read live state before retrying.
7. Do not proceed to hostile proof until routing is demonstrably mandatory.

### Stage C — repository-specific hostile proof

1. Branch from the exact protected post-installation head.
2. Add one inert workflow under `.github/workflows/` that is deliberately absent from `.ghos-routing/workflows.json` and is structurally scheduled and/or write-capable.
3. The fixture must not perform a real mutation. It exists only to create an unregistered execution surface.
4. Open a PR marked clearly `HOSTILE PROOF — MUST NEVER MERGE`.
5. Observe `routing-enforcement` fail at the protected-base gate with `workflow routing coverage mismatch`, or another equally specific governed fail-closed class if the hostile profile intentionally tests a different invariant.
6. Bind repository, PR number, exact hostile head, protected base, workflow run, job/check, first failure class, and ruleset state.
7. Verify the required routing context makes protected integration unavailable. Do not over-interpret GitHub's raw `mergeable` Boolean; it describes Git mergeability, not ruleset authorization.
8. Close the hostile PR unmerged.
9. Record the hostile proof on the repository tracker.

### Stage D — terminalize repository

1. Re-read protected `main` after hostile closure.
2. Re-read registry, enforcement workflow, external gate pin/digest, ruleset, required contexts, bypass actors, and relevant post-merge checks.
3. Confirm no authority boundary was enlarged.
4. Record terminal `GHOS_ROUTING_ENFORCED` on the repository tracker.
5. Close the tracker `completed` only after the terminal record is internally consistent.
6. Update `MATH-PROGRAMME#724` and the estate ledger before advancing to the next repository.

## 2. INTELLECT first

Tracker: `grandchallenge/INTELLECT#73`.
Handoff baseline: `08a3044e0363fa932012fa642ea15d9153ba876b`.
Known surface: 8 direct workflows.
Known ruleset: `19964077`, active, strict, zero-bypass.
Existing required contexts: `test (3.11.14)`, `test (3.12.13)`, `policy / policy`, `security / action-policy`.

Special boundary: no constitutional authority enlargement. The routing registry and enforcement workflow are observational/control-plane artifacts only.

Acceptance: implementation protected; routing mandatory without weakening Constitutional profile; hostile proof fails closed; terminal readback recorded.

## 3. MATHFORGE second

Tracker: `grandchallenge/MATHFORGE#117`.
Handoff baseline: `ed8a65410336489ea5646808265c44f5387bebb8`.
Known surface: 7 direct workflows.
Known ruleset: `17137626`, active, strict, zero-bypass.
Existing required contexts: `reconnaissance`, `policy / policy`, `security / action-policy`.

Special boundary: no source/provenance authority enlargement. Routing classification does not validate source truth or promote provenance claims.

Acceptance: implementation protected; routing mandatory without weakening Forge profile; hostile proof fails closed; terminal readback recorded.

## 4. MATHSOLVE third

Tracker: `grandchallenge/MATHSOLVE#131`.
Handoff baseline: `07814c1e28855ff0314737d3666642217da095a1`.
Known surface: 11 direct workflows.
Known ruleset: `17137627`, active, strict, zero-bypass.
Existing required contexts: `ledgers`, `policy / policy`, `security / action-policy`.

Special boundary: no mathematical-production, proof-promotion, or campaign-authority enlargement. Routing says where/how execution may run, not what mathematics is valid.

Acceptance: implementation protected; routing mandatory without weakening Solve profile; hostile proof fails closed; terminal readback recorded.

## 5. MATHCERT fourth

Tracker: `grandchallenge/MATHCERT#232`.
Handoff baseline: `bb9b88a03f379fc0ea9776a672a098cb73096f0a`.
Known surface: large certification workflow set. Enumerate the full directory afresh; do not rely on a stale count.
Known ruleset: `17137628`, active, zero-bypass, but `strict_required_status_checks_policy: false`.
Existing required contexts: `certify`, `policy / policy`, `security / action-policy`.

Special boundary: certification authority is reserved. Routing installation must not alter adjudication semantics, certification eligibility, claim promotion, or publication authority.

Default protection strategy: create a dedicated strict zero-bypass routing ruleset requiring `routing-enforcement`, while leaving Cert profile `17137628` unchanged. This isolates routing strictness from certification-profile policy. Any decision to tighten `17137628` itself is a separate policy/control-plan change and requires explicit treatment.

Because the workflow surface is large, use the shared gate as the exact classifier and generate the registry mechanically. Spot checking is insufficient.

Acceptance: complete exact inventory; implementation protected; dedicated strict routing requirement active; hostile proof fails closed; terminal readback recorded.

## 6. Phase-1 closure

Phase 1 is complete only when all four trackers are closed completed with `GHOS_ROUTING_ENFORCED` or another explicitly justified allowed terminal disposition.

Then:

1. update `governance/ghos_estate_conformance_ledger.json` with all four terminal receipts;
2. add an umbrella Phase-1 checkpoint to `MATH-PROGRAMME#724` with exact protected heads, rulesets, hostile proof IDs, and any named deviations;
3. reconcile the campaign handoff state to `PHASE_1_COMPLETE__PHASE_2_READY` through protected review;
4. begin Phase 2 at `grandchallenge/AETHER#61` only after re-fetching AETHER from protected state;
5. do **not** assume AETHER itself is an admitted persistent controller. Prove durable wake/state/recovery semantics independently if such a controller transition is proposed.

## 7. Immediate stop conditions

Stop and surface the exact boundary rather than improvising when any of these occurs:

- protected head changes materially during byte-derived classification;
- a review/check is invalidated by changed bytes and the new result changes the security argument;
- a ruleset cannot be restored/read back exactly;
- a workflow requires a feature not supported by the admitted controller catalog;
- a new controller is required;
- candidate-independent enforcement cannot be achieved without executing candidate code or granting it credentials;
- a proposed change alters constitutional, source/provenance, mathematical-production, certification, publication, production, commercial, or claim-promotion authority;
- an external gate/digest mismatch cannot be explained by an admitted shared-gate upgrade;
- a classifier defect prevents exact feature/topology derivation.

Routine fresh reads, review requests, reruns, ordinary exact-head merges, readbacks, and tracker updates are not stop conditions.
