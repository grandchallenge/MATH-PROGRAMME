# PC-WP04 — Formal model and interface boundary

## 1. Carrier

`ComponentId` is `Nat`. A factor expression is a finite list of atoms:

```text
S3
SPHERICAL_SPACE_FORM_NONTRIVIAL
S2_BUNDLE_OVER_S1_ORIENTABLE
S2_BUNDLE_OVER_S1_NONORIENTABLE
```

The list order is a canonical evaluator order. The package does not formalize the diffeomorphism quotient making connected sum associative and commutative.

## 2. Source-level certificates

A `FactorCertificate` is either one factor atom or the exceptional source label `RP3#RP3`. Normalization expands the latter to two nontrivial spherical atoms.

## 3. Reconstruction

A reconstruction contains:

- child component identifiers;
- emitted factor certificates.

Its evaluated expression is the concatenation of the child values and normalized emitted factors.

## 4. Event

An `Event` records:

- pre-event active components;
- post-event active components;
- unchanged components;
- a partial reconstruction function for pre-components;
- a complete source binding.

The reconstruction function is partial so malformed or incomplete records evaluate to `none` rather than receiving a fabricated value.

## 5. Event contract

The structural contract records:

- duplicate freedom of the active lists;
- unchanged-component membership in both slices;
- reconstruction existence for changed pre-components;
- child membership in the post slice;
- absence of reconstruction outside the pre slice;
- nonempty source-binding fields;
- no-component-loss ownership.

The no-loss obligation is intentionally explicit. It is part of the certificate supplied by the WP03 validator, not an analytic theorem.

## 6. Imported event relation

For semantic valuations `before` and `after`, `ImportedEventRelation e before after` asserts:

1. unchanged components have identical expressions;
2. every changed pre-component equals the total evaluation of its recorded reconstruction.

This relation is the sole imported semantic premise of `stepBack_correct`.

## 7. History relation

`ImportedHistoryRelation` is an inductive finite chain. Its constructor requires the current event's post slice to be the tail history's initial active slice. This makes chronological compatibility structural rather than a side condition.

## 8. Certificate

A generated certificate contains:

- the backward-evaluated initial valuation;
- the chronological list of source bindings.

The source list is preserved by reduction, proved by `buildCertificate_sources`.
