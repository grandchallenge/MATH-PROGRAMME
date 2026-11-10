# CMDG CM4 — four-layer evidence seed and semantic-edge review queue

**Operation:** CMDG-GRAPH-ROOT-CM4-001, bounded evidence increment 2026-11-09. **Disposition:** SOURCE-OBSERVED SEED; no production graph certification. This increment does not reopen the internally closed CM4 theorem.

## Artifact and exact identity

Machine-readable observations: `fixtures/cmdg/cm4_graph_root_001/observed_layer_seed_001.json`. They are **not** a `cmdg_graph_certification_manifest`, validator output, reviewed semantic-edge file, or `GRAPH_CERTIFIED` receipt. The existing candidate manifest `fixtures/cmdg/cm4_graph_root_001/manifest.json` remains authoritative for open graph obligations and is not silently promoted.

The observed wrapper is `fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4Blocker.lean`, protected Git blob `8ab0051746507099f7321460fe091e56a84b57bb`. Its explicit direct Lean proof invokes `CMDG.CondensedCM4P3M.KernelPointBridge.profiniteSolid_isSolid_via_pointFunctional S`; the wrapper returns `CMDG.CondensedCM4.CM4Target`. The proof-bearing imported module has protected blob `d3ef22a2ad2d9c0af6982773d0a24b715e61f5a7`.

The pinned environment is Lean `62eed1db4d67327ec8120be05f1a1b0847d74561` and mathlib `79d0395a1825a6264ad5d269e35e60537518955e`. The pinned `Mathlib/Condensed/Solid.lean` blob is `f5214433f91ee87fc8fbe7e2746e0bd227faed2a`. A previous operator replay and the protected terminal receipt record `[propext, Classical.choice, Quot.sound]`, without `sorryAx`; this document does not assert a new compiler run.

## Four distinct observations

| Layer | Observed evidence | What is deliberately not inferred |
| --- | --- | --- |
| `G_proof` | Root theorem body calls the named Point-functional terminal theorem | A complete kernel-extracted transitive dependency graph |
| `G_implementation` | Root file directly imports `Mathlib.Condensed.Solid`, `Mathlib.Topology.Category.Profinite.Nobeling.Induction`, `Mathlib.Algebra.Ring.ULift`, and `CMDGCondensedCM4P3GPointFunctional` | That an import implies an immediate mathematical dependency |
| `G_provenance` | Protected CM4 terminal readback, source-facing mathematical note and independent replay protocol; external issue #1222 still open | External specialist signoff |
| `G_semantic` | Candidate root and three **unreviewed** definition dependencies proposed below | Any `REVIEWED_DIRECT` edge or complete dependency path |

## Immediate semantic-edge proposals for separate critical review

These are **proposed**, not admitted, edges. Each requires exact semantic classification and a logically distinct source/meaning review before encoding as `REVIEWED_DIRECT`.

1. Root theorem to `CondensedMod.IsSolid`: candidate `REQUIRES_DEFINITION`. Verify that the pinned class's `isIso_solidification_map` field captures exactly the claimed **module-level** statement at `ZLift`; do not identify it with the more general correct solid-module notion mentioned in the mathlib TODO.
2. Root theorem to `Condensed.profiniteSolid`: candidate `REQUIRES_DEFINITION`. Verify the right-Kan-extension construction and all variance, universe and coefficient conditions before treating the symbol as a source-equivalent solid free group.
3. Root theorem to `CMDG.CondensedCM4.ZLift`: candidate `REQUIRES_DEFINITION`. Verify this is the explicit universe lift of the integers, not a general coefficient-ring theorem.

**Adversarial objections:** (a) the root type may syntactically mention a declaration without implying that declaration is the unique or minimal semantic dependency; (b) a source-to-formal name match is not itself a `REALIZES_AS` proof; (c) direct proof dependencies and source-history dependencies can disagree; (d) neither `#print axioms` nor CI green certifies the semantic graph. The proposed edges therefore remain quarantined in the seed, not placed into the production manifest.

## Next evidence-producing acts

1. Extract and archive the exact transitive **declaration-level** proof dependency graph at the pinned root; compare the direct call recorded above with the transitive closure. Preserve file/blob/Lean/mathlib pins and fail on drift.
2. Produce explicit semantic-node records and `REALIZES_AS` candidates for each root prerequisite, with proof of scope correspondence rather than matching text alone. Obtain the separate semantic critic disposition before making any edge `REVIEWED_DIRECT`.
3. Produce a four-layer difference ledger: `PROOF_ONLY`, `IMPLEMENTATION_ONLY`, `SEMANTIC_ONLY`, `PROVENANCE_ONLY`, `RECONCILED`; keep every unsupported transitive step open.
4. Run the registered C06 hostile suite and clean external replay on **materially matching** exact source identities, then build a graph runtime package with the updated candidate manifest's Git blob SHA. A runtime `VALIDATOR_ACCEPTED_PRECONDITIONS` status remains short of `GRAPH_CERTIFIED`.
5. Leave the independent external CM4 review outside this internal graph boundary; it cannot be counted as completed and does not block ordinary evidence preparation.

**Current unresolved in-boundary graph obligations:** direct semantic review, formal realization bindings, four-layer reconciliation, C06 adversarial clean replay. There is no certified full spine.
