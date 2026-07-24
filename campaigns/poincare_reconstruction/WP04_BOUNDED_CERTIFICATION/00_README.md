# PC-WP04 — Bounded certification substrate

## Metadata

- Campaign: `PC-001`
- Work Package: `PC-WP04`
- Tracker: `MATH-PROGRAMME#77`
- Input: Referee-promoted conditional topology certificate `PC-WP03`
- Formal fixture: `fixtures/formal/PC-WP04`
- State: `KERNEL_CHECKED_BOUNDED_EVALUATOR_CERTIFICATE`
- Claim boundary: finite expression-level certification conditional on explicit imported event relations

## Result-status box

| Field | Value |
|---|---|
| Strongest certified result | The finite backward evaluator preserves active-set coverage, exact support, event equations, history equations, and source bindings under the explicit `EventContract` and `ImportedEventRelation` |
| Kernel | Lean 4 `v4.33.0-rc1` with mathlib pinned to commit `79d0395a1825a6264ad5d269e35e60537518955e` |
| JSON replay | Two valid and twelve malformed WP03 histories replay with expected outcomes |
| Not certified | Event existence, geometric neck/cap validity, Ricci-flow analysis, surgery continuation, noncollapsing, finite extinction, or manifold-level connected-sum semantics |
| No placeholders | Lean source contains neither `sorry` nor local axioms |
| Evidence | Dedicated workflow run `30094600807` passed all policy, mutation, placeholder, dependency, and Lean kernel checks |

## What was formalized

The formal carrier includes:

- `FactorAtom` and source-level `FactorCertificate`;
- normalization of `RP^3#RP^3` into two nontrivial spherical atoms;
- finite component identifiers and reconstruction equations;
- source-bearing `Event` records;
- structural `EventContract` and `NoComponentLoss` obligation;
- optional finite valuations and total backward evaluation;
- event- and history-level imported semantic relations;
- certificate generation with retained source bindings;
- a bounded Boolean terminal factor-profile discharge.

## The formal trust boundary

`ImportedEventRelation` is the only semantic bridge used by evaluator correctness. It states that a source-certified event's pre-event factor expression equals the recorded expression built from post-event components and emitted factors.

It does not assert that a Ricci flow produces such an event. In particular, the formal project does not contain an opaque theorem or axiom named after Perelman.

## Certified theorem surface

```text
PC04-L001  normalizeCertificate / normalizeCertificates
PC04-L002  evalChildren_exact
PC04-L003  evalReconstruction_exact
PC04-T004  eventContract_noComponentLoss
PC04-T005  stepBack_covers
PC04-T006  stepBack_none_outside
PC04-T007  stepBack_exactSupport
PC04-T008  stepBack_correct
PC04-T009  runBackward_covers
PC04-T010  runBackward_correct
PC04-T011  buildCertificate_sources
PC04-T012  all_s3_of_simplyConnectedCompatible
PC04-C013  bounded evaluator certificate
```

## Active-set and loss discipline

`stepBack_covers` proves that every pre-event component receives a value when every post-event component has one and the event contract supplies a reconstruction for each changed pre-component.

`stepBack_none_outside` proves that the evaluator assigns no value outside the declared pre-event active set. Together these give `stepBack_exactSupport`.

`eventContract_noComponentLoss` exposes the no-loss witness required of every certified event. This is a contract-level obligation, checked against the WP03 JSON history by the semantic validator; it is not inferred from geometry.

## Correctness

`stepBack_correct` proves that one evaluator step encodes the source-declared pre-event semantic valuation when the post-event valuation is correctly encoded.

`runBackward_correct` composes this statement through a finite `ImportedHistoryRelation`. Termination is structural recursion on the finite event list.

## Source preservation

Every event carries:

```text
provider
theoremId
version
locator
importedAssumptions
```

`buildCertificate_sources` is definitional evidence that certificate generation preserves the chronological source list.

The certificate manifest binds the WP03 schema, fixture corpus, and validator by Git blob SHA.

## Validation gates

The dedicated workflow performs, in order:

1. certificate-manifest and source-binding validation;
2. complete WP03 history replay;
3. three adversarial policy mutations;
4. rejection of `sorry` and local axioms;
5. pinned Lean/mathlib setup;
6. kernel compilation of the formal fixture.

The general programme workflow independently checks repository contracts and documentation.

## Claim boundary

Permitted:

> A kernel-checked finite backward evaluator for the PC-WP03 surgery-history language, correct conditional on explicit source-bound event equations, with repository-native replay of the complete fixture corpus.

Prohibited:

- “formalized Perelman's proof”;
- “formalized Ricci flow with surgery”;
- “proved surgery events exist”;
- “machine-checked Poincaré proof”;
- “new proof of Poincaré.”
