# CMDG — first production-root graph certification workset (candidate)

**Operation:** CMDG-GRAPH-ROOT-CM4-001. **Status:** candidate graph workset; production `GRAPH_CERTIFIED` **NOT CONFERRED**. Charter §§7–14, 24–29 and CMDG-C06 govern.

## Root

`CMDG.CondensedCM4.cm4Target_via_pointFunctional : CM4Target` is the protected, Lean-checked, module-level integer-coefficient theorem. Source authority: `governance/cmdg_condensed_cm4_terminal_readback_001.json`, reviewed reconciliation PR #1216, terminal theorem merge `442dbc15b0cc7d4b068d6cbf73ae3be8f96f0dc6`, formal fixture `fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4Blocker.lean`. Axiom readback `[propext, Classical.choice, Quot.sound]`; no `sorryAx`. This **theorem-level** evidence is not yet a graph-certified dependency path.

## Actual versioned candidate manifest

See `fixtures/cmdg/cm4_graph_root_001/manifest.json`. It uses the existing `cmdg_graph_certification_manifest.schema.json`, a real theorem/root reference and the exact pinned Lean/mathlib baseline, **not** the synthetic schema demo's claimed reviewer identities. Its proposed direct semantic edges are deliberately empty pending semantic classification, and its missing in-boundary obligations are explicit. The resulting candidate cannot validly assert production `GRAPH_CERTIFIED`.

## Route to admissible graph package

1. Populate graph nodes for the actual CM4 theorem, `CondensedMod.IsSolid`, `profiniteSolid`, coefficient object, Point functional, measure reconstruction, C05 and relevant foundation boundaries. Do not use source-file imports as semantic edges.
2. For **each immediate dependency**, produce a proposed typed `G_semantic` edge, exact source/proof evidence and a distinct reviewed-direct disposition. Compute transitive closure only from the admitted direct edges. Record the four-layer discrepancy reconciliation.
3. Add explicit `REALIZES_AS` cross-layer edges mapping semantic nodes to pinned Lean declarations with named correspondence scope. Record limitations; never infer semantic equivalence from matching names.
4. Extract declaration-level proof and axiom dependencies from the **actual pinned root**, with implementation and provenance graphs separate. Ensure the formal proof environment hashes and archived replay artifacts match all sources.
5. Replace the in-boundary obligations in the manifest only when their evidence is protected and replayed; bind the manifest Git blob SHA to the runtime validation package. Execute `python3 ci/validate_cmdg_graph_package.py` against that exact package and preserve its report.
6. Exercise C06 adversarial cases: hidden classicality, proof/import laundering, equivalence and alias laundering, boundary inflation, transitive-edge omission, universe/source/pin drift, and failed clean replay.
7. Review mathematical semantic edges with a logically distinct critic, inspect exact CI and replay, and complete protected admission/readback. A passing existing validator currently emits `VALIDATOR_ACCEPTED_PRECONDITIONS`, not `GRAPH_CERTIFIED`: an **additional governed production certification disposition** is required before the latter status is claimed.

**Acceptance for this workset:** real candidate manifest created; unresolved evidence gaps precisely recorded; implementation and review route executable. **Not accepted:** review of uninspected semantic edges, C06 closure, production graph certification or V0/V1/V2 certified-spine promotion.

The CM4 root is deliberately a *root-first thin certified-path candidate*, not an assertion that the original V0 demonstration's full educational route is the unique, minimal, or proved semantic dependency chain.
