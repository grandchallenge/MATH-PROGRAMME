# GHOS-ESTATE-ROLLOUT-001 — Phase 1 handoff

This is the human-readable recovery entry point for a replacement agent. Live protected GitHub state always wins over this file.

## Recovery rule

At the start of a session, re-fetch:

1. MATH-PROGRAMME protected `main`, umbrella tracker #724, and this handoff pack;
2. the target repository's protected `main`, current rulesets, tracker, open PRs, and relevant checks;
3. `grandchallenge/.github` shared gate identity;
4. any material provider/control dependency consumed by the target transition.

A protected head change invalidates this handoff only when it changes the material routing/control closure. Do not discard valid evidence or rebase a candidate merely because an unrelated commit advanced `main`.

Source-of-truth order remains:

1. live protected GitHub refs, rulesets, PR/check state, and protected records;
2. protected repository artifacts and durable tracker records;
3. this handoff pack;
4. historical campaign documents;
5. chat history, which is never authoritative.

## Current campaign position

Campaign: `GHOS-ESTATE-ROLLOUT-001`.  
Umbrella: `grandchallenge/MATH-PROGRAMME#724`.  
Phase 0: complete.  
Phase 1: active at `grandchallenge/INTELLECT#73`.

Phase-1 order remains:

1. INTELLECT #73;
2. MATHFORGE #117;
3. MATHSOLVE #131;
4. MATHCERT #232.

Do not advance the mutation sequence past INTELLECT until its live required-routing protection and terminal readback are complete. Read-only preparation of downstream repositories is permitted.

## Shared gate

Current admitted shared gate:

- repository: `grandchallenge/.github`;
- commit: `ef1cce6029233a68cf46063cea2384772fcae613`;
- path: `scripts/ghos_execution_routing_gate.py`;
- blob: `f9f85937713046eacdc79c532046c676cbb4550c`;
- SHA-256: `fc0a9a4d20de72e9fbc04c8cd54cffc3a6e4657fb09e7978b360616bd5e94a17`.

The central invariant is:

`workflow bytes -> derived features -> derived topology -> compatible admitted controller -> candidate-independent routing enforcement -> protected ruleset -> hostile proof -> protected readback`.

The admitted repository-bound GitHub Actions controller supplies persistence and execution topology only. It grants no governance, certification, mathematical, publication, or commercial authority.

## Phase 0 reference state

Phase 0 is closed. Do not reopen it merely because later protected commits advanced a reference repository.

MATH-PROGRAMME routing ruleset `21969152` is currently active and requires `routing-enforcement` with `strict_required_status_checks_policy: false` and zero bypass actors. Programme ruleset `17137629` is separate and also uses non-strict status checks for concurrent development.

The old handoff statement that the MATH-PROGRAMME routing ruleset was strict is superseded.

## INTELLECT current state

Opening Phase-1 baseline was `08a3044e0363fa932012fa642ea15d9153ba876b`. Do not use it as the current implementation head.

Current protected INTELLECT `main` is `565ed31f413b4698f400a260fc4a8ea65e7e1255`, after the GH-OS routing implementation series through PR #79.

Important admitted corrections:

- the routing workflow YAML parse defect was repaired;
- candidate evaluation uses the protected-base `pull_request_target` model without executing candidate code;
- the effective candidate is obtained through GitHub's virtual merge ref `refs/pull/<number>/merge`, not a raw stale branch snapshot;
- this permits current-base routing evaluation without update-branch/rebase ceremony;
- repository-specific probe execution demonstrated successful routing on an unchanged stale branch.

MATH-PROGRAMME's checked-in Release Trust contract now expects INTELLECT required contexts:

- `test (3.11.14)`;
- `test (3.12.13)`;
- `policy / policy`;
- `security / action-policy`;
- `routing-enforcement`;

with `strict_status_checks: false`.

Current live INTELLECT ruleset `19964077` is non-strict and zero-bypass but still lacks `routing-enforcement`. Therefore #73 remains open and INTELLECT is not terminally admitted. The next material action is to apply/read back the admitted protection contract, verify `routing-enforcement` is mandatory, record the terminal readback, and close #73 if all terminal conditions are satisfied.

Do not redesign or rerun the already-protected routing implementation merely because this ruleset application remains outstanding.

## Remaining Phase-1 ruleset baselines

Current live repository profiles are non-strict:

| Repository | Ruleset | Required contexts before routing admission | Strict | Bypass |
|---|---|---|:---:|---|
| INTELLECT | `19964077` | two Python test contexts; policy; security | no | none |
| MATHFORGE | `17137626` | reconnaissance; policy; security | no | none |
| MATHSOLVE | `17137627` | ledgers; policy; security | no | none |
| MATHCERT | `17137628` | certify; policy; security | no | none |

The earlier handoff's `strict: true` values for INTELLECT, MATHFORGE, and MATHSOLVE are superseded by the current concurrent-development policy.

Routing rollout must preserve this non-strict posture unless a separate material policy decision justifies changing it. Do not create a dedicated strict routing ruleset merely as a default; require routing without reintroducing forced branch synchronization.

## Repository implementation pattern

For each unresolved repository after INTELLECT:

1. re-fetch protected material state and workflow inventory;
2. derive every direct workflow's exact feature vector from bytes using the shared gate semantics;
3. create the repository-local routing registry with exact repository identity, workflow coverage, feature arrays, topology, admitted controller binding, and false claim/authority boundaries;
4. add candidate-independent `ghos-routing-enforcement` adapted to the repository's dependency layout;
5. use the pinned shared gate and verify its digest before execution;
6. never execute candidate scripts/workflows or expose credentials to candidate content;
7. run affected repository checks and focused routing/security evidence only; do not launch unrelated mathematical or full-estate CI;
8. obtain specialist review only when the material security/provenance/certification boundary requires it; routine implementation uses standing delegated authority;
9. merge through existing protected controls and read back exact protected routing bytes;
10. make `routing-enforcement` mandatory while preserving existing non-strict status policy and unrelated required contexts;
11. read the complete live ruleset back;
12. execute the repository-specific hostile proof only after routing is structurally mandatory;
13. close the hostile PR unmerged and record its exact fail-closed evidence;
14. record terminal repository disposition and update the umbrella checkpoint.

## Review and concurrency rule

The former generic sequence “fresh exact-head independent review after every head change” is superseded for routine work.

- Review/check evidence binds to the material object it actually covers.
- Unrelated protected-main movement does not invalidate it.
- A materially changed enforcement workflow, external gate, controller authority, security boundary, or substantive provenance/certification control requires renewed scrutiny for that changed object.
- Routine bounded implementation, readback, tracker maintenance, and protected merge proceed under standing delegated authority once affected checks pass.
- Do not manufacture an approval or represent the author as an independent mathematical/security reviewer where genuine independence is required.

## Ruleset administration

If the connected interface cannot mutate rulesets, use the authorized GitHub UI or authenticated local administration route. Snapshot exact pre-state; make the smallest settings delta; read back full post-state before retrying an ambiguous mutation; never add a bypass actor; never weaken unrelated required contexts.

Applying an already-admitted non-strict required-context contract is routine administration. Removing a required control, introducing bypass, or weakening security is not.

## Stop conditions

Stop only for a real boundary:

- material scope/control-plan change;
- materially changed security argument requiring new specialist review;
- inability to restore/read back protection;
- new persistent-controller or capability transition;
- constitutional, mathematical, certification, provenance, publication, production, commercial, or external-claim authority enlargement;
- unresolved classifier/control defect;
- genuine authorization boundary.

Fresh reads, ordinary affected-check reruns, routine protected merge, readback, and tracker updates are not stop conditions. A behind branch is not a stop condition by itself.

## Terminal condition

A repository reaches `GHOS_ROUTING_ENFORCED` only after protected implementation, mandatory candidate-independent routing protection, hostile proof where required, protected readback, and terminal tracker evidence agree.

Phase 1 completes only after all four repositories have a permitted terminal disposition. Estate-wide success remains `GHOS_ESTATE_CONFORMANCE_GREEN`; repository-local success must not be inflated into estate conformance.
