# EC-BULK-007 — Mandatory critical sample #1135: Collatz

**Disposition:** `PRIMARY_SOURCE_REVIEW_AND_INDEPENDENT_CRITICAL_APPROVAL_PENDING`. This is an unaccepted editorial draft, **not** a Collatz proof, a certified Lean proof, or a completed critical sample.

## Source and identity

- Canonical maintained statement: https://www.erdosproblems.com/1135
- Historical source and original attribution: https://www.erdosproblems.com/latex/1135
- Original issue RESULT/1: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2406#issuecomment-6180930562
- Draft: governance/erdos_compendium/editorial/1135.md
- Frozen formal representation: google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020/FormalConjectures/ErdosProblems/1135.lean, open theorem with local sorry, no kernel proof.
- Historical background sources: Lagarias [La85],[La10],[La16], as indexed at canonical catalogue.

## Exact statement to review

For positive integers n:
- f(n)=n/2 if n is even;
- f(n)=(3n+1)/2 if n is odd.

Conjecture: for **every m>=1 there exists k>=1** such that the k-fold iterate of f maps m to exactly 1.

The k>=1 condition matters for seed 1: f(1)=2, f²(1)=1. Count steps of this normalized map, not the uncompressed odd 3n+1 map. Require arbitrary precision integer arithmetic to avoid overflow for large seeds.

## Existing finite, exact evidence

The deterministic program ci/erdos_compendium_007_phase15_checks.py tests ALL m=1..10000, reaches one for each, and finds maximum positive first-hit time 165 at seed m=6171, with seed 1 returning in two steps. Receipt: governance/erdos_compendium/batches/EC-BULK-007_FINITE_CHECKS_PHASE15.json.

**These finite tests cannot prove the universal conjecture and must not be called a counterexample search that settles an infinite problem.**

## Mandatory independent review obligations

1. Source-lock Lagarias original 1985, 2010 and 2016 papers and identify Collatz/Erdős historical attribution and the conversational \$500 valuation rather than an unverified offered prize.
2. Verify the exact Tao published logarithmic-density almost-all result including normalization, quantifier, density and actual conclusion; show explicitly why it does not prove termination for every m.
3. Independently implement or audit the finite sweep, exact step count, positive k, and any overflow/cycle assumptions. Require a separate reproducible test of m=1 and m=6171.
4. Confirm frozen Lean theorem's `sorry` status, distinguish statement formalization from proof or kernel certificate, and audit proof dependency chain if newer formal artifacts appear.
5. Have an independent non-author mathematical critic review historical precision, claimed finite evidence and open status; record APPROVE/REVISE with original source pages and reviewer identity.
6. Update the deterministic 20-sample completion count only after completed independent critical review, not because a draft or finite fixture exists.

**State at this checkpoint: 0/20 completed deterministic critical reviews, no source-fidelity acceptance, no protected publication.**
