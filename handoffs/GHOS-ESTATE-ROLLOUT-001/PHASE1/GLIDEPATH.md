# GHOS-ESTATE-ROLLOUT-001 — Phase 1 execution glidepath

Read `HANDOFF.md` and `STATE.json` first. Live protected GitHub state wins over this glidepath.

## 0. Cold-start reconstruction

Before modifying a repository:

1. re-fetch MATH-PROGRAMME protected `main`, umbrella issue #724, and this handoff pack;
2. re-fetch the shared `.github` gate at commit `ef1cce6029233a68cf46063cea2384772fcae613` and verify SHA-256 `fc0a9a4d20de72e9fbc04c8cd54cffc3a6e4657fb09e7978b360616bd5e94a17`;
3. re-fetch MATH-PROGRAMME routing ruleset `21969152`; it is a separate control from Programme profile `17137629`;
4. re-fetch all Phase-1 trackers and the current target repository's protected `main`, rulesets, workflows, and open PRs;
5. search for already-protected or in-flight work before creating a new branch.

Head movement invalidates prior evidence only when it changes the material routing/control closure. Do not discard valid byte-derived evidence, review, or checks solely because an unrelated protected commit moved `main`.

## 1. Current immediate operation — complete INTELLECT admission

Tracker: `grandchallenge/INTELLECT#73`.

Protected routing implementation is already merged through PR #79. Current protected `main` is `565ed31f413b4698f400a260fc4a8ea65e7e1255`.

The implementation uses candidate-independent protected-base execution and GitHub's virtual merge ref `refs/pull/<number>/merge`, so an unchanged stale branch can be evaluated against current protected-base routing semantics without rebasing.

The remaining material gap is live protection:

- checked-in MATH-PROGRAMME Release Trust contract expects INTELLECT `routing-enforcement` plus the existing four contexts;
- expected strictness is `false`;
- current live INTELLECT ruleset `19964077` is non-strict and zero-bypass but does not yet require `routing-enforcement`.

Therefore:

1. read back INTELLECT `main`, ruleset `19964077`, and the protected enforcement/registry bytes;
2. confirm the checked-in admitted Release Trust contract still requires `routing-enforcement` and non-strict policy;
3. apply the admitted ruleset contract through the available authorized administration path;
4. read the complete ruleset back independently;
5. verify all existing required contexts remain and `routing-enforcement` is now mandatory;
6. verify strictness remains false and bypass actors remain empty;
7. bind the already-successful hostile/probe routing evidence to the protected implementation material closure;
8. record terminal readback on INTELLECT #73 and close it only if the terminal state is internally consistent;
9. update MATH-PROGRAMME #724 before mutating MATHFORGE.

Do not rerun or redesign the routing implementation merely because the protection application remained outstanding. Do not update the INTELLECT branch just to make it numerically current.

## 2. Common implementation pattern for MATHFORGE, MATHSOLVE, MATHCERT

### Stage A — install candidate-independent routing under existing protection

1. snapshot the target repository's protected material state, rulesets, required contexts, bypass actors, and direct workflow inventory;
2. enumerate all direct workflows and derive feature vectors from their bytes with the exact shared-gate semantics;
3. create `.ghos-routing/workflows.json` with exact repository identity, admitted controller catalog, exact workflow coverage, exact features/topology, and false claim/authority boundaries;
4. add `.github/workflows/ghos-routing-enforcement.yml` using protected-base `pull_request_target`, read-only permissions, no candidate execution, immutable external-gate identity, and digest verification;
5. adapt dependency installation to the repository rather than copying a nonexistent MATH-PROGRAMME requirements path; `PyYAML==6.0.3` is the established compatible pin unless fresh governed evidence changes it;
6. add only focused local reproducibility tests that preserve the shared classifier semantics;
7. open the implementation PR;
8. run the affected repository policy/security/routing checks selected by current policy;
9. obtain specialist review only if the material change crosses a reserved security/provenance/certification boundary; routine implementation uses standing delegated disposition;
10. merge through existing protection when the candidate is mergeable and affected evidence is green;
11. read protected `main` back and verify exact registry/enforcement bytes.

Do not invalidate checks/review because unrelated protected-main commits appeared. Renew evidence only when the material routing/security object changed.

### Stage B — make routing mandatory without reintroducing strict synchronization

1. snapshot complete live ruleset pre-state;
2. add `routing-enforcement` while preserving existing required contexts and zero bypass actors;
3. preserve the repository's existing non-strict required-status policy unless a separate material policy decision expressly changes it;
4. independently read back complete post-state;
5. if an administration response is ambiguous, read live state before retrying;
6. do not proceed to hostile proof until routing is demonstrably mandatory.

Current live main-profile strictness is false for INTELLECT, MATHFORGE, MATHSOLVE, and MATHCERT. The former default of creating a separate **strict** routing ruleset is superseded; routing protection should not force branch synchronization merely to obtain freshness.

### Stage C — repository-specific hostile proof

1. branch from the protected post-installation state;
2. add an inert but structurally unregistered scheduled/write-capable workflow;
3. never perform a real mutation;
4. open a PR clearly marked hostile proof and never merge it;
5. observe candidate-independent `routing-enforcement` fail with the intended governed class;
6. bind repository, hostile PR, hostile head, protected base/material state, workflow run/job/check, first failure class, and ruleset state;
7. verify the mandatory routing context blocks protected integration;
8. close the hostile PR unmerged;
9. record the hostile proof on the repository tracker.

### Stage D — terminalize repository

1. read protected `main` again;
2. read registry, enforcement workflow, external gate pin/digest, ruleset, required contexts, bypass actors, and relevant checks;
3. confirm no repository authority boundary was enlarged;
4. record terminal `GHOS_ROUTING_ENFORCED` or another explicitly justified allowed terminal disposition;
5. close the tracker only after terminal evidence is internally consistent;
6. update the umbrella ledger/checkpoint before advancing.

## 3. MATHFORGE second

Tracker: `grandchallenge/MATHFORGE#117`.

Current live ruleset `17137626` is active, non-strict, zero-bypass, with required contexts:

- `reconnaissance`;
- `policy / policy`;
- `security / action-policy`.

Special boundary: routing must not enlarge source/provenance authority or treat execution conformance as source truth.

## 4. MATHSOLVE third

Tracker: `grandchallenge/MATHSOLVE#131`.

Current live ruleset `17137627` is active, non-strict, zero-bypass, with required contexts:

- `ledgers`;
- `policy / policy`;
- `security / action-policy`.

Special boundary: routing must not enlarge mathematical-production, proof-promotion, or campaign authority.

## 5. MATHCERT fourth

Tracker: `grandchallenge/MATHCERT#232`.

Current live ruleset `17137628` is active, non-strict, zero-bypass, with required contexts:

- `certify`;
- `policy / policy`;
- `security / action-policy`.

Enumerate the large certification workflow surface afresh. Routing installation must not alter adjudication semantics, certification eligibility, claim promotion, or publication authority.

Require routing while preserving non-strict status policy unless a separate certification-policy decision explicitly changes it. Do not introduce a dedicated strict ruleset merely by default.

## 6. Phase-1 closure

Phase 1 completes only when all four trackers have a permitted terminal disposition.

Then:

1. update `governance/ghos_estate_conformance_ledger.json` with the terminal receipts;
2. add a Phase-1 checkpoint to MATH-PROGRAMME #724 with protected material identities, rulesets, hostile proof IDs, and named deviations;
3. reconcile the handoff state to `PHASE_1_COMPLETE__PHASE_2_READY` through protected routine integration;
4. begin Phase 2 only after re-fetching AETHER protected state;
5. do not assume AETHER is an admitted persistent controller without independent controller-capability evidence.

## 7. Stop conditions

Stop and name the exact boundary only when:

- a material protected routing/security object changes and invalidates the current argument;
- protection cannot be restored or read back;
- a new persistent controller or unsupported capability is required;
- candidate-independent enforcement would require executing candidate code or exposing credentials;
- a proposed change enlarges constitutional, provenance, mathematical-production, certification, publication, production, commercial, or external-claim authority;
- an unexplained gate/digest/classifier defect prevents exact routing derivation;
- a genuine authorization boundary is reached.

Routine fresh reads, affected-check reruns, protected merges, readbacks, tracker updates, unrelated `main` movement, and a behind branch are not stop conditions.
