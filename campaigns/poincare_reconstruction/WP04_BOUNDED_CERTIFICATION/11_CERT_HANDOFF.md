# PC-WP04 — Certificate handoff

## Exported formal surface

The authoritative proof-assistant package is:

```text
fixtures/formal/PC-WP04/
```

Consumers may rely on the named declarations in `certificate_manifest.json`, subject to the imported-boundary statement.

## Required imported assumptions

A consumer seeking a topological interpretation must supply, for each event:

1. a valid source binding;
2. an `EventContract` witness;
3. an `ImportedEventRelation` witness identifying the real event with the finite reconstruction equation;
4. a finite `ImportedHistoryRelation` chain.

The certificate does not manufacture these witnesses from a metric flow.

## Guaranteed outputs

Given those assumptions, the formal package guarantees:

- exact active-set support;
- no missing pre-component valuation;
- finite backward expression evaluation;
- compositional event and history correctness;
- chronological source retention;
- bounded terminal factor-profile filtering.

## Replay contract

The JSON corpus and validator are bound by Git blob SHA in the manifest. A source or fixture change invalidates policy validation until the manifest and review are updated.

## Prohibited use

This handoff may not be used to attach a full-proof badge to the Poincaré campaign. The analytic and manifold-level semantic bridges remain named debt.
