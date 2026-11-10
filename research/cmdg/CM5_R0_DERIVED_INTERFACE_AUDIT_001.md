# CMDG CM5-R0 — pinned derived-interface audit 001

**Status:** SOURCE-AND-INTERFACE AUDIT, NO THEOREM. **Parent:** `research/cmdg/CM5_FRONTIER_001.md`. **Protected baseline examined:** `b67152169f6dc589a9f0260e2f78fedc383d32f5`. **Formal pin:** Lean `62eed1db4d67327ec8120be05f1a1b0847d74561`, mathlib `79d0395a1825a6264ad5d269e35e60537518955e`.

## Exact restricted input

`CMDG.CondensedCM4.cm4Target_via_pointFunctional : CM4Target` in `fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4Blocker.lean` at protected blob `8ab0051746507099f7321460fe091e56a84b57bb` establishes the **module-level** assertion for all `S : Profinite.{u}` with `ZLift = ULift.{u + 1} ℤ`. The exact `CondensedMod.IsSolid` predicate is the one used by pinned mathlib, not an already constructed derived-solid subcategory.

The earlier formal interface probe `fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P3Audit.lean` (blob `52f4f15fc3f01a353c105ef3ac138de73e4910df`) checks general Ext, enough injectives/projectives, sheaf abelian and cohomology/Čech APIs and a condensed discrete-module interface. It **explicitly proves no P3 vanishing**. Its earlier `governance/cmdg_condensed_cm4_p3_001.json` (blob `949ea8cc3abd06dfe8da87f6baca0a200a35a300`) is a *historical characterized blocker*: its underived proof status was superseded by the subsequently protected Point-functional route. It remains valid as scoped evidence of which generic interfaces were examined; it is not a fresh exhaustive audit of all current mathlib derived solids.

## Five exact comparison gates

| Gate | Evidence actually observed | Classification and missing bridge |
| --- | --- | --- |
| R0-A: ambient category | `CategoryTheory.sheafIsAbelian` from `Mathlib/CategoryTheory/Sites/Abelian.lean`, pinned blob `d5250edfc56c2d79c7dae942fe0ab1e8a93ac707`; CM3 protected interface | Generic abelian sheaf machinery observed; exact derived-category instance for the chosen `CondensedAb` with universe and smallness profile **not yet established** |
| R0-B: derived construction | `CategoryTheory.HasExt` in `Mathlib/Algebra/Homology/DerivedCategory/Ext/Basic.lean` blob `2ee4d31030b25e6886bf6884046b33727385e0d3`; enough-injectives/projectives interfaces in pinned derived Ext modules | Generic Ext/derived infrastructure observed; `A_S[0]` and exact coherent derived CondensedAb category have **not been constructed in CM5** |
| R0-C: derived-solid definition | Protected `CondensedMod.IsSolid` via `Mathlib/Condensed/Solid.lean` and `CMDGSolidC05.lean` | **Blocking:** no inspected Lean declaration identifying the desired derived-solid/local predicate and its derived `RHom` universal property; no claim of global absence |
| R0-D: source correspondence | CM4 terminal receipt `governance/cmdg_condensed_cm4_terminal_readback_001.json`; original CM4 issue #355 source-locks Scholze Proposition 0.5.7, including module and complex clauses | Source claim includes a complex-level clause, but only the module-level realization is protected; categorical and universe correspondence must be separately reviewed |
| R0-E: transport principle | Module theorem proved by `cm4Target_via_pointFunctional`; old P3 audit records generic Ext and sheaf cohomology | **Blocking:** no inspected theorem showing `IsSolid(A)` induces derived-locality of `A[0]`. Exact derived orthogonality, Ext vanishing/t-exactness or an equivalent bridge is needed |

## Minimum falsifiable next theorem obligation

Before proposing a Lean statement of `A_S[0]` derived-solid, define a formal predicate `DerivedSolid_Z` with a pinned ambient derived category and a derived mapping-out criterion. Then attempt a lemma for the **specific profinite solid object**:

> Given the actual `CondensedMod.IsSolid ZLift A_S` witness and separately established, precisely stated derived-orthogonality/Ext hypotheses for `A_S`, construct `DerivedSolid_Z(A_S[0])`.

This is a **conditional proof target**, not an asserted theorem. The hypotheses cannot be assumed vacuously or substituted with the sought conclusion. First test the simplest potential counterexample to the overly broad rule `IsSolid A → DerivedSolid(A[0])` in any proposed derived-solid definition; audit the categorical t-structure and the comparison with Scholze's complex clause.

## Source-and-proof boundaries

- Never infer derived localization or complex solidity merely from the underived `IsSolid` field.
- Generic `Ext` APIs or a type-checking `#check` do not prove profinite acyclicity, a derived Hom comparison or a liquid tensor theorem.
- A source citation does not certify a Lean definition's exact semantic identity.
- Do not infer arbitrary-ring, cardinality-bounded source concordance, C06, CM5 completion or `GRAPH_CERTIFIED`.
- This audit does not select the R1 Liquid-Tensor capstone.

**Result:** `R0_EXACT_INTERFACE_CHARACTERIZED_BLOCKER` for the specifically missing derived-solid predicate, precise ambient derived category and transport/Ext bridge. The next constructive act is a pinned declaration inventory and minimal Lean scaffold for gates R0-A–C; mathematical proof R0-E is still open.
