# GHOS-ESTATE-ROLLOUT-001 — Phase 0 → Phase 1 handoff

This file is the human-readable entry point for a completely independent successor agent. It is intentionally sufficient to resume the campaign without conversational history.

## Recovery rule

Never trust this handoff over live protected GitHub state. On every new session, first re-fetch the protected default branch, relevant rulesets, tracker, current PRs, and exact-head checks before acting. If live state differs, live protected state wins and this handoff becomes historical evidence to reconcile.

Source-of-truth order:

1. live protected GitHub refs, rulesets, PR/review/check state;
2. protected repository artifacts and durable tracker comments;
3. `STATE.json` in this handoff pack;
4. campaign manifest/ledger/documentation;
5. chat history, which is never authoritative.

## Campaign identity and purpose

Campaign: `GHOS-ESTATE-ROLLOUT-001`.
Umbrella tracker: `grandchallenge/MATH-PROGRAMME#724`.
Campaign admission: merged PR `grandchallenge/MATH-PROGRAMME#726`, exact candidate `d7888766a01d9e20153376a3c7f3cc4635911610`, protected merge `06fdcda8c18f395403dc544274fb98fee36ef6ea`.

Objective: every active repository must terminate as exactly one of:

- `GHOS_ROUTING_ENFORCED`;
- `GHOS_GOVERNED_NON_APPLICABLE`;
- `GHOS_BLOCKED_WITH_NAMED_DEFECT`.

Estate success is only `GHOS_ESTATE_CONFORMANCE_GREEN` after all repositories have terminal evidence. Repository-local success must never be inflated into estate-wide conformance.

The central invariant is:

`workflow bytes -> derived features -> derived topology -> compatible admitted controller -> candidate-independent routing enforcement -> protected ruleset -> hostile proof -> protected readback`.

## Phase 0 is closed

Phase-0 shared-control tracker `grandchallenge/.github#67` is closed `completed` with terminal disposition `GHOS_ROUTING_ENFORCED`.

Binding Phase-0 control state:

- final protected `.github/main`: `6a3693fe5a9c6ee6bb420a429f9421801e35457f`;
- final protected `.github/.ghos-routing/control.json` blob: `21d04288a32321af09b3ee503e9cf4c9f6af5fee`;
- shared gate commit: `ef1cce6029233a68cf46063cea2384772fcae613`;
- shared gate path: `scripts/ghos_execution_routing_gate.py`;
- shared gate blob: `f9f85937713046eacdc79c532046c676cbb4550c`;
- shared gate SHA-256: `fc0a9a4d20de72e9fbc04c8cd54cffc3a6e4657fb09e7978b360616bd5e94a17`;
- classifier defect `GHOS-CLASSIFIER-PROJECT-MUTATION-001` is closed; `gh project item-add` is classified `WRITE_CAPABLE`;
- `.github` ruleset `17137624` is active, strict, zero-bypass, and requires `policy / policy`, `security / action-policy`, and `routing-enforcement`;
- `gcl-standards` protected head at handoff: `4467622415530d1abc56784a4d02c1cd1278b836`; ruleset `19962512` is active, strict, zero-bypass, and requires `routing-enforcement` in addition to existing Standards checks;
- MATH-PROGRAMME Phase-0 successor consumer admission was protected at `d9560df959d4b00eebe69b61a6f8890c50e97e14`; current protected MATH-PROGRAMME head at handoff is `4b09c2b471f378a4161357c836945296cff15434` after unrelated bounded administrative merges;
- MATH-PROGRAMME routing is supplied by dedicated ruleset `21969152`, active, strict, zero-bypass, requiring only `routing-enforcement` on `main`;
- Programme ruleset `17137629` is a separate pre-existing profile and is not the routing ruleset.

Successor-era hostile proofs all failed closed on workflow routing coverage and were closed unmerged:

- `.github#72`: head `56c52449cefea143f8c391c291cdac4b52659f0f`, run `33503173626`, job `99840986069`;
- `gcl-standards#74`: head `825694986aa68ac13feb62e1ec6c04ff6e3d79dd`, run `33503195001`, job `99841052245`;
- `MATH-PROGRAMME#749`: head `05eb2aa0042f2a5dbd2c239168776d6e5a6df533`, run `33503211601`, job `99841106633`.

Failure class: `FAIL_CLOSED_WORKFLOW_ROUTING_COVERAGE_MISMATCH`.

Umbrella Phase-0 checkpoint: `MATH-PROGRAMME#724` comment `5493507033`.
Binding `.github#67` terminal-disposition comment: `5493437493`.

Do not reopen Phase 0 unless a fresh protected read reveals a material contradiction or enforcement regression.

## Phase 1 scope

Execute in this order unless a genuine dependency or authority boundary requires otherwise:

1. `grandchallenge/INTELLECT#73`;
2. `grandchallenge/MATHFORGE#117`;
3. `grandchallenge/MATHSOLVE#131`;
4. `grandchallenge/MATHCERT#232`.

Current protected baselines at handoff:

| Repository | Protected main | Direct workflow surface | Registry | Existing main ruleset | Strict | Bypass | Routing required |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `INTELLECT` | `08a3044e0363fa932012fa642ea15d9153ba876b` | 8 workflows | absent | `19964077` Constitutional profile | yes | none | no |
| `MATHFORGE` | `ed8a65410336489ea5646808265c44f5387bebb8` | 7 workflows | absent | `17137626` Forge profile | yes | none | no |
| `MATHSOLVE` | `07814c1e28855ff0314737d3666642217da095a1` | 11 workflows | absent | `17137627` Solve profile | yes | none | no |
| `MATHCERT` | `bb9b88a03f379fc0ea9776a672a098cb73096f0a` | large certification workflow surface; enumerate afresh | absent | `17137628` Cert profile | **no** | none | no |

Required existing contexts:

- INTELLECT: `test (3.11.14)`, `test (3.12.13)`, `policy / policy`, `security / action-policy`;
- MATHFORGE: `reconnaissance`, `policy / policy`, `security / action-policy`;
- MATHSOLVE: `ledgers`, `policy / policy`, `security / action-policy`;
- MATHCERT: `certify`, `policy / policy`, `security / action-policy`.

All four are applicable workflow surfaces. `GHOS_GOVERNED_NON_APPLICABLE` is not available on present evidence.

## Shared implementation contract

The shared gate is exact and deterministic. It derives features from workflow bytes and requires the registry declaration to equal the derived feature list and topology exactly. Do not over-declare features “for safety”; over-declaration is drift and fails the gate.

Admitted features are:

`AUTONOMOUS_WAKE`, `EXTERNAL_REUSABLE_JOB`, `EXTERNAL_WAIT`, `NON_RECONCILABLE_MUTATION`, `OPAQUE_EXECUTION`, `SCHEDULED`, `SECRET_CREDENTIAL`, `UNATTENDED_DISPATCH`, `WRITE_CAPABLE`.

Topology rule:

- any `AUTONOMOUS_WAKE`, `NON_RECONCILABLE_MUTATION`, `OPAQUE_EXECUTION`, `SECRET_CREDENTIAL`, or `WRITE_CAPABLE` => `PERSISTENT_CONTROLLER_REQUIRED`;
- otherwise any `EXTERNAL_REUSABLE_JOB`, `EXTERNAL_WAIT`, or `UNATTENDED_DISPATCH` => `MULTI_SESSION_RESUMABLE`;
- otherwise => `BOUNDED_ATOMIC`.

The admitted controller catalog currently contains repository-bound `GITHUB_ACTIONS`, executor class `PERSISTENT_CONTROLLER`, supporting all admitted features. Controller capability supplies execution topology, never governance authority.

Reference enforcement workflow: `grandchallenge/MATH-PROGRAMME/.github/workflows/ghos-routing-enforcement.yml`.

Important Phase-1 adaptation: none of the four Phase-1 repositories has `requirements/policy.txt` at the recorded protected baseline. Therefore do **not** copy the reference workflow verbatim. The shared gate imports PyYAML; protected `.github` routing tests pin `PyYAML==6.0.3`. Use a repository-appropriate, reviewed dependency step, with `PyYAML==6.0.3` as the established Phase-0 compatible pin unless fresh evidence requires another governed choice.

The enforcement workflow must remain candidate-independent:

- trigger on `pull_request_target`;
- permissions `contents: read` only;
- check out protected base and candidate read-only with `persist-credentials: false`;
- never execute candidate scripts/workflows;
- reject ordinary candidate modification of the enforcement workflow once protected;
- check out the external gate at exact commit `ef1cce6029233a68cf46063cea2384772fcae613`;
- verify SHA-256 `fc0a9a4d20de72e9fbc04c8cd54cffc3a6e4657fb09e7978b360616bd5e94a17` before execution;
- call the gate with the exact target repository identity.

## Repository implementation pattern

For each Phase-1 repository:

1. Re-fetch protected `main`, rulesets, tracker, direct workflow directory, current PRs, and existing checks. If the head differs from this handoff, bind the new head and discard stale byte-derived evidence.
2. Enumerate every `.github/workflows/*.yml` and `*.yaml` path from protected bytes.
3. Mechanically derive each workflow's exact feature list using the admitted gate semantics.
4. Produce `.ghos-routing/workflows.json` with exact repository identity, admitted controller catalog, exact sorted workflow coverage, exact feature lists/topologies, and all claim boundaries false.
5. Add candidate-independent `.github/workflows/ghos-routing-enforcement.yml` adapted for the repository dependency layout.
6. Add only the minimum local tests or deterministic helper needed to reproduce the gate locally. Do not create a divergent classifier.
7. Open a governed PR; request independent exact-head review immediately. Do not treat stale review/checks as transferable after any head change.
8. Before routing becomes mandatory, prove the candidate implementation passes the external gate against its exact head.
9. Merge the reviewed implementation under existing protected controls. At this initial Phase-1 bootstrap, `routing-enforcement` is not yet required, so installation of the new enforcement workflow does not require weakening an existing routing rule.
10. Read back protected main and the exact enforcement/registry bytes.
11. Add `routing-enforcement` to protected integration without removing or weakening existing rules. Prefer preserving the existing profile and adding only the required context when clean. For MATHCERT, do not silently change Cert-profile strictness: use a dedicated strict, zero-bypass routing ruleset unless an explicit repository-policy decision authorizes a broader Cert-profile change.
12. Read the complete ruleset back and confirm intended strictness, existing required contexts preserved, and no unexpected bypass actor.
13. Only after routing is mandatory, open a repository-specific hostile PR containing an inert but structurally unregistered scheduled/write-capable workflow. The hostile candidate must never merge.
14. Bind the failed `routing-enforcement` run/job and first governed failure class; close the hostile PR unmerged.
15. Record exact protected head, registry/enforcement identities, ruleset state, hostile proof, independent review/check binding, and terminal `GHOS_ROUTING_ENFORCED` disposition on the repository tracker.
16. Close the repository tracker only after its durable protected readback is internally consistent.
17. Update the umbrella ledger/checkpoint before moving to the next repository.

## Ruleset administration boundary

The connected GitHub interface used during Phase 0 could read rulesets but did not expose a ruleset mutation action. If that remains true, ruleset activation is a bounded administrator/Human transaction through GitHub UI or an authorized local `gh api` path.

Ruleset administration rules:

- snapshot exact pre-state first;
- make the smallest settings delta;
- never add a bypass actor as a substitute for the routing context;
- never weaken unrelated required checks;
- read back the complete post-state independently;
- if a mutation may have succeeded but post-validation failed, read live state before retrying;
- do not leave a required context temporarily removed while diagnosing an unrelated failure.

Future modifications to an already-protected enforcement workflow are self-modifications and must follow the bounded bootstrap procedure in `docs/governance/GHOS_ROUTING_CONTROL_RUNBOOK.md`.

## Authority and review

This campaign is control-plane governance, not mathematical/certification promotion. Every claim boundary in routing registries remains false.

Independent review is real, not simulated. Never fabricate an approval or treat the author as an independent reviewer.

The established streamlined operating policy permits routine exact-head progression when required checks/review are satisfied and no reserved-authority boundary is crossed. Exact-head invariance, independent review, protected rules, and self-modification procedures remain mandatory.

Stop for:

- a material scope/control-plan change;
- a non-mechanical stale-head or review invalidation that changes the security argument;
- inability to restore or verify a protection setting;
- a genuine capability transition requiring a new persistent controller;
- any requested constitutional, mathematical, certification, publication, production, or commercial authority enlargement;
- an unresolved classifier/control defect that prevents exact routing derivation;
- a platform/tool limitation that is a true authorization boundary rather than mere inconvenience.

Do not stop merely because a routine gate requires a fresh read, review request, rerun, merge, readback, or tracker update.

## Known traps

- `mergeable: true` is Git-level mergeability, not proof that protected rules permit integration.
- A passing optional `routing-enforcement` check is not equivalent to a required ruleset context.
- `pull_request_target` is safe here only because candidate content is data and is never executed or given credentials.
- Feature declarations must equal the shared gate output exactly.
- Repository identity is part of the gate. Never reuse another repository's registry with only cosmetic edits.
- MATHCERT's existing Cert profile is non-strict. Do not silently tighten or rely on it for strict routing; separate routing protection is the default handoff recommendation.
- The older campaign files contained stale `CANDIDATE_AWAITING_PROTECTED_ADMISSION` and Phase-0-pending projections. This handoff candidate reconciles those projections; if this candidate is not protected, treat the stale files as known documentary drift and use live trackers instead.
- MATH-PROGRAMME routing ruleset is `21969152`; `17137629` is a separate Programme profile.

## Completion condition for this handoff

This handoff is considered operationally admitted only after its PR receives independent exact-head approval, required exact-head checks pass, it is merged to protected `main`, and protected readback confirms `HANDOFF.md`, `STATE.json`, `GLIDEPATH.md`, and the reconciled campaign projections.
