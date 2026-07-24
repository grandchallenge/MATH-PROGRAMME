# PC-WP04 — Kernel theorem ledger

| ID | Lean declaration | Status | Meaning | Boundary |
|---|---|---|---|---|
| PC04-L001 | `normalizeCertificate` | kernel definition | Expands source factor certificates | Does not prove source classification |
| PC04-L002 | `evalChildren_exact` | kernel checked | Optional child evaluator equals total evaluator when children are encoded | Expression level only |
| PC04-L003 | `evalReconstruction_exact` | kernel checked | Reconstruction evaluator equals total reconstruction expression | Conditional on child encodings |
| PC04-T004 | `eventContract_noComponentLoss` | kernel checked contract extraction | Every certified event carries the no-loss witness | Witness is supplied by the event contract |
| PC04-T005 | `stepBack_covers` | kernel checked | Covered post slice gives covered pre slice | Requires `EventContract` |
| PC04-T006 | `stepBack_none_outside` | kernel checked | No value is produced outside `pre` | Syntactic active-set theorem |
| PC04-T007 | `stepBack_exactSupport` | kernel checked | One backward step has exact declared support | Requires covered post slice |
| PC04-T008 | `stepBack_correct` | kernel checked | One step encodes the imported pre-event valuation | Requires `ImportedEventRelation` |
| PC04-T009 | `runBackward_covers` | kernel checked | Coverage composes through a finite history | Finite inductive history only |
| PC04-T010 | `runBackward_correct` | kernel checked | Correctness composes through a finite history | Expression-level semantics |
| PC04-T011 | `buildCertificate_sources` | kernel checked | Generated certificate retains every source binding in order | Does not validate the external source theorem |
| PC04-T012 | `all_s3_of_simplyConnectedCompatible` | kernel checked | The bounded compatibility predicate permits only `S3` atoms | Boolean group-profile abstraction, not formal van Kampen |
| PC04-C013 | package claim | governed certificate | Bounded evaluator certificate is replayable in CI | Not a full topology or analytic certificate |
