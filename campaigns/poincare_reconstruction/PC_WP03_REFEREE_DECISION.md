# PC-001 — WP03 Referee promotion decision

## Decision

Promote `PC-WP03` as:

```text
REFEREE_PROMOTED_CONDITIONAL_TOPOLOGY_CERTIFICATE
```

Authorize `PC-WP04`, the bounded certification substrate.

## Basis

WP03 converts the topology interface imported by WP02 into a finite source-bound event model. It supplies:

- an exact JSON Schema;
- a deterministic semantic validator;
- separating and nonseparating cut equations;
- explicit cap and discard records;
- complete active-set and ancestry tracking;
- the correct local-finiteness plus finite-extinction derivation;
- a finite backward reconstruction proof;
- terminal factor normalization and non-circular group discharge;
- two positive and twelve malformed histories.

## Source alignment

The event algebra is governed by:

- Morgan–Tian Theorem 0.3;
- Morgan–Tian Proposition 15.3;
- Morgan–Tian Corollary 15.4;
- the source-normalized interfaces `PC02-T013`, `PC02-T014`, and `PC02-T016`.

The schema retains the exact exceptional classes `RP3#RP3` and the nonorientable `S^2`-bundle, while the Poincaré profile separately enforces orientability.

## Adversarial findings

The validator rejects:

- missing provenance;
- nonmonotone event order;
- malformed separating and nonseparating cuts;
- duplicate ancestry parents;
- component loss in backward equations;
- unpermitted discards;
- nonorientable factors in the orientable profile;
- finite-history claims derived from discreteness alone;
- nonempty terminal slices;
- nontrivial factors under the simply connected profile;
- incorrect `RP3#RP3` normalization.

## Claim boundary

Promotion certifies only:

```text
valid finite event history
+ imported topology transition contract
=> connected-sum factor reconstruction
=> Poincare terminal discharge in the simply connected orientable profile.
```

It does not certify that Ricci flow produces the history.

## Debt disposition

Quotation-level source crosswalk, proof-assistant formalization, topology-library interfaces, CI integration, and all analytic imports remain explicit nonblocking debt. They block stronger certification claims, not WP03's conditional result.

## Next gate

WP04 may formalize the finite evaluator and terminal algebraic/topological logic. It must preserve source provenance and imported assumptions in every theorem statement.
