# MP-PROGRAMME-POLICY-EXECUTION-ENVELOPE-REPAIR-001

Status: AUTHORIZED_IMPLEMENTATION_IN_PROGRESS

Governing issue: #393
Human Steward authorization comment: 5239566619
Protected implementation base: `6796e55749d6a89f0aadf68274d80c74863d4a54`
Triggering Programme-policy run: `31373604594`
Affected T3 development head: `9e27685771d3e38472f2682bca6f64725bf7d3b5`

## Diagnosis

The `validate-json` job in `.github/workflows/ci.yml` is bounded by `timeout-minutes: 20`. On Programme-policy run `31373604594`, all steps through repository unit tests, structural-sweep validation, and candidate campaign admission succeeded. The governed-campaign replay then continued until the job reached the 20-minute ceiling and GitHub cancelled the operation. No T3 assertion failure was demonstrated.

## Authorized repair

The preferred implementation separates governed-campaign replay into a distinct bounded job with its own runtime envelope. The existing `validate-json` required-check surface remains fail closed by depending on successful completion of that replay job.

The repair must preserve:

- exact-head execution;
- full governed-campaign replay coverage;
- failure artifact preservation;
- required-check failure on replay failure or cancellation;
- current policy and documentation checks;
- all T3 mathematical nonclaims.

## Nonclaims

`residual_sum_zero_proved: false`

`proof_effect: NONE`

`promotion_effect: NONE`

`t3_status: OPEN_WITH_CHARACTERIZED_BLOCKER`

This operation does not modify PR #373 mathematics, the locked Brown–Zudilin recurrence, the pole-free coefficient object, protected-shell semantics, MATHCERT authority, GRAPH_CERTIFIED authority, or global CMDG claims.
