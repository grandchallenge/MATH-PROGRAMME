# PC-WP04: bounded surgery-history certificate

## Result-status box

| Field | Status |
|---|---|
| Object | Finite source-bound surgery-history algebra exported by `PC-WP03` |
| Formal carrier | `FactorAtom`, `FactorCertificate`, `Reconstruction`, `Event`, `EventContract`, `CertifiedEvent`, and `ImportedHistoryRelation` |
| Evaluator | `stepBack` and `runBackward` |
| Kernel-checked obligations | active-set coverage; exact support; no-component-loss extraction; event and history evaluator correctness; source-binding preservation; terminal factor-profile elimination |
| Imported boundary | `ImportedEventRelation` connecting a source-certified topology event to its reconstruction equation |
| Analytic results not formalized | Ricci flow, canonical neighbourhoods, neck detection, cap geometry, surgery existence/continuation, noncollapsing, finite extinction |
| Fixture corpus | two valid and twelve malformed WP03 JSON histories |
| Toolchain | Lean `v4.33.0-rc1`, mathlib `v4.33.0-rc1` |
| Certification state | **CANDIDATE** pending repository-native kernel replay |

## Formal theorem surface

The package exports:

- `eventContract_noComponentLoss`;
- `stepBack_covers`;
- `stepBack_none_outside`;
- `stepBack_exactSupport`;
- `stepBack_correct`;
- `runBackward_covers`;
- `runBackward_correct`;
- `buildCertificate_sources`;
- `all_s3_of_simplyConnectedCompatible`.

The evaluator is total as a function into `Option FactorExpr`: malformed or incomplete records produce `none`. The correctness theorems require an `EventContract` and the explicit `ImportedEventRelation`.

## Trust boundary

`ImportedEventRelation` is not a theorem about Ricci flow. It is the formal interface through which a source-certified real topology event supplies its finite reconstruction equation. The package proves what follows from that event equation and the structural history contract.

No declaration named after Perelman is introduced as an axiom. The Lean source contains neither `sorry` nor local `axiom` declarations.

## Source preservation

Every `Event` contains a `SourceBinding` with provider, theorem identifier, version, locator, and imported assumptions. `buildCertificate_sources` proves definitionally that certificate generation retains the event source list in chronological order.

## JSON replay

The dedicated workflow executes the authoritative WP03 validator against all fourteen fixture cases before running the Lean build. JSON validity does not establish event existence; it establishes only that the finite record satisfies the committed schema and semantic checks.

## Reproduction

From this directory:

```bash
lake update
lake exe cache get
lake build
```

From the repository root:

```bash
python3 campaigns/poincare_reconstruction/WP03_SURGERY_TOPOLOGY/05_ADVERSARIAL_HISTORIES/validate_histories.py
python3 ci/validate_pc_wp04_fixture.py fixtures/formal/PC-WP04
```

## Claim boundary

The strongest permitted statement is:

> PC-WP04 kernel-checks the finite backward evaluator and its structural correctness conditional on explicit source-bound event relations, while repository CI replays the complete WP03 JSON corpus.

It is prohibited to describe this artifact as a formalization of Perelman's analytic proof, a proof of surgery existence, or a new proof of the Poincaré theorem.
