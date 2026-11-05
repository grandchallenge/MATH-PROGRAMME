# CMDG CM4 — first semantic and realization candidates

**Operation:** CMDG-GRAPH-ROOT-CM4-002. **Status:** PROPOSED only; this is not semantic-edge review or graph certification.

## Exact formal evidence

The protected formal file `fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4Blocker.lean`, blob `8ab0051746507099f7321460fe091e56a84b57bb`, declares:

- `CM4Target : Prop` as the universal `CondensedMod.IsSolid ZLift ((Condensed.profiniteSolid ZLift).obj S)`;
- `cm4Target_via_pointFunctional : CM4Target`, invoking `KernelPointBridge.profiniteSolid_isSolid_via_pointFunctional S`.

The protected CM4 terminal receipt gives the restricted module-level result, axiom footprint and proof-state authority. This is evidence for *proposing* two immediate semantic dependencies, not evidence that those are the complete semantic edge set.

## Distinct node/edge proposals

1. `CMDG:E:CM4-REQUIRES-SOLID-PREDICATE`: CM4 theorem root to the semantic definition of `CondensedMod.IsSolid`.
2. `CMDG:E:CM4-REQUIRES-PROFINITE-SOLID`: root to the `Condensed.profiniteSolid` construction with the integer-lifted coefficient.
3. `CMDG:E:CM4-ROOT-LEAN-REALIZATION`: explicit proposed `REALIZES_AS` binding from the semantic theorem root to the exact formal `cm4Target_via_pointFunctional` declaration.

The two semantic proposals reside as `PROPOSED` edges in `package.json.additional_edges`, not as `REVIEWED_DIRECT` edges in the manifest. The realization is likewise `PROPOSED`. Their inclusion in the validator package must **not** make them traversable authoritative semantic dependencies.

## Logical critic's bounded assessment

The root's formal proposition explicitly mentions both named objects, supporting their relevance. That alone does **not** establish that every occurrence is a material **immediate** semantic dependency, nor that no intermediate node is needed. An authorial candidate is not a reviewed-direct edge. The root statement and proof are restricted to `ULift ℤ`, so the mapping cannot imply a general-ring or derived/complex theorem. The proof import list is a software graph and cannot be relabeled as semantic authority. The Point-functional kernel theorem is a formal proof dependency, not automatically a direct semantic prerequisite.

**Disposition:** three bounded proposals retained for separate semantic review; zero new reviewed-direct semantic edges admitted; `GRAPH_CERTIFIED` remains false.

## Exact next review

Review source/type granularity: `CondensedMod.IsSolid` and `Condensed.profiniteSolid` may need their formal construction/definition nodes separated from the semantic layer. Review the Point-functional proof spine and direct-edge completeness against the pinned formal file, source Proposition 0.5.7 and protected C05/CM4 receipts. Either admit each edge with exact evidence and distinct role-scoped review, or reject/modify it. Then record the direct edges in the manifest and re-pin the runtime package to its new Git blob; replay the validator and C06 mutations before production intent.

No step here asserts that the CM5 derived comparison is proved.
