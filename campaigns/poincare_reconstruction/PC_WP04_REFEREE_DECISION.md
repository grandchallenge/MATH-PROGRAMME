# PC-001 — PC-WP04 Referee decision

## Decision

Promote `PC-WP04` as:

```text
KERNEL_CHECKED_BOUNDED_EVALUATOR_CERTIFICATE
```

Authorize `PC-WP05` only as an integrated closure and source-concordance audit.

## Findings

1. The formal carrier is finite and total.
2. Active-set coverage and exact support are kernel checked.
3. No-component-loss remains an explicit certified event-contract obligation.
4. Event and finite-history evaluator correctness are kernel checked conditional on `ImportedEventRelation`.
5. Certificate generation preserves source bindings.
6. The full WP03 fixture corpus and policy mutations replay in repository CI.
7. No `sorry`, local axioms, or opaque Perelman premise occurs.

## Evidence

- Dedicated certificate workflow: `30094600807` — success.
- Programme policy workflow: `30094600804` — success.
- Certified source commit: `3aee596c674c2b7f403c73de0709f5ea0e14e209`.

## Boundary

The promoted statement concerns expression-level finite bookkeeping. It does not include:

- analytic event existence;
- manifold-level connected-sum semantics;
- formal van Kampen theory;
- formalization of finite extinction;
- a machine-checked proof of Poincaré.

## Debt disposition

The remaining debts are retained in `09_PROOF_DEBT.json`. None blocks the bounded evaluator certificate; several block any full-proof certificate.
