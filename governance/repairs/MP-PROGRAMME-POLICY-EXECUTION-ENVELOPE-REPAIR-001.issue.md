# Governing issue draft

Operation: `MP-PROGRAMME-POLICY-EXECUTION-ENVELOPE-REPAIR-001`

## Diagnosis

Programme policy run `31373604594` for PR #373 at exact head `9e27685771d3e38472f2682bca6f64725bf7d3b5` completed all steps through repository unit tests, administrative structural-sweep validation, and candidate campaign admission. The `Validate and replay governed campaigns` step was cancelled at the `validate-json` job's 20-minute runtime ceiling. No T3 assertion failure was demonstrated.

## Scope

Repair only the Programme-policy execution envelope. Preferred implementation: move governed-campaign replay into a distinct bounded required job with its own sufficient runtime envelope. A simple timeout increase is fallback only if splitting is technically unsuitable.

## Required invariants

- preserve fail-closed execution;
- preserve exact-head binding and branch-protection semantics;
- preserve complete governed-campaign replay coverage;
- preserve failure-artifact behavior;
- do not convert cancellation or failure into success;
- do not modify T3-009 mathematics, recurrence, coefficient object, or shell semantics;
- do not expand administrative autonomy or mathematical/certification authority.

## Acceptance criteria

1. The repair is implemented from exact protected base `6796e55749d6a89f0aadf68274d80c74863d4a54`.
2. Governed-campaign replay remains required and fail closed.
3. The long replay is independently bounded from the ordinary `validate-json` policy job, unless the documented fallback is necessary.
4. Validation demonstrates no governed replay lane is silently omitted.
5. Required checks pass at the final exact repair head.
6. Independent review is recorded before protected merge.
7. Post-merge readback binds the exact protected merge.

## Claim boundary

`residual_sum_zero_proved: false`

`proof_effect: NONE`

`promotion_effect: NONE`

`t3_status: OPEN_WITH_CHARACTERIZED_BLOCKER`
