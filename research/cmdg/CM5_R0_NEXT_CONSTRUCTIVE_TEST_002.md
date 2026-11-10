# CMDG CM5-R0 — next constructive test and falsification gate 002

**Status:** SOURCE-PINNED RESEARCH WORK PACKAGE, NO DERIVED THEOREM. **Parent:** `CM5_R0_DERIVED_INTERFACE_AUDIT_001.md`. **Target:** the proposed derived/complex assertion for `A_S[0]` with `A_S = (Condensed.profiniteSolid ZLift).obj S`. The underived CM4 theorem remains closed and is an input only.

## Exact inspected interfaces, not inferred instances

The earlier compiled CM4-P3 audit (`CMDGCondensedCM4P3Audit.lean`, blob `52f4f15fc3f01a353c105ef3ac138de73e4910df`) has `#check CategoryTheory.HasExt` and `#check CategoryTheory.sheafIsAbelian`. The inspected pinned mathlib file `Mathlib/Algebra/Homology/DerivedCategory/Ext/Basic.lean` (blob `2ee4d31030b25e6886bf6884046b33727385e0d3`) defines `CategoryTheory.HasExt` for a category already equipped with `[Abelian C]` and describes derived zero-degree objects via `CategoryTheory.DerivedCategory.singleFunctor`. These are generic library interfaces, **not** instances or derived-solid predicates for `CondensedAb`.

The inspected `Mathlib/Condensed/Solid.lean` (blob `f5214433f91ee87fc8fbe7e2746e0bd227faed2a`) supplies `Condensed.profiniteSolid`, `Condensed.profiniteSolidification` and **underived** `CondensedMod.IsSolid`, with its `isIso_solidification_map` property. None of those declarations is a displayed derived-locality definition.

| Gate | Next mechanical check | Current result |
| --- | --- | --- |
| R0-A: ambient abelian category | Check exact Lean type and universe of `CondensedMod.{u} ZLift` / intended `CondensedAb`; resolve actual `[Abelian C]` and derived-category instance | No selected exact derived ambient category |
| R0-B: degree-zero object | Type-check `(singleFunctor C 0).obj A_S` with the chosen `C` and functor's universe constraints; extract declaration closure | Only generic `HasExt` and `singleFunctor` APIs inspected |
| R0-C: derived solid | Identify/define noncircular local objects by explicit derived `RHom` or localization property and source-concordant probe generators | Missing semantic and Lean predicate |
| R0-D: source concordance | Compare chosen `A_S[0]` definition with Scholze Proposition 0.5.7 **complex** clause and its quantifier/boundary | Not reviewed |
| R0-E: bridge | Prove conditional derived-orthogonality or a pointwise comparison of derived localization with a heart localization | No transport theorem |

## Precise conditional bridge to attempt

Let `C` be a chosen abelian category with derived category `D(C)`. Let `L_D` be a specified localization endofunctor of `D(C)`, and `L_C` a specified localization of `C`. Suppose **independently** that:

1. `A` is `L_C`-local, with an explicit witnessed isomorphism `L_C(A) ≅ A`;
2. a natural comparison isomorphism `L_D(A[0]) ≅ (L_C(A))[0]` exists, in the exact chosen category;
3. the meaning of `L_D`-local is independently defined and proved equivalent to the required **derived-solid** criterion, including higher-degree mapping tests.

Then one can transport the first isomorphism through degree zero to show `L_D(A[0]) ≅ A[0]`, and use the third assumption to conclude the desired derived locality. This is a **conditional proof strategy, not a solution**: assumptions 2 and 3 carry the difficult mathematical work and are not available for CM5 in the inspected sources. In particular, no step may simply assume `A_S[0]` is derived-solid or package the conclusion into an unexamined instance.

The smallest falsification target is the unqualified implication `CondensedMod.IsSolid A → DerivedSolid(A[0])`. Try to exhibit a localization for which the heart-local property does not commute with derived localization; if no example is found, this still does not prove the implication. Any adversarial test must use the *same* intended derived-solid definition rather than a convenient unrelated notion of locality.

## Runnable probe design and acceptance

A candidate Lean source `CMDGCondensedCM5R0Interface.lean` should first import the exact protected CM4 wrapper and pinned derived-category modules and **only** check the available declarations. Next, explicitly choose and type-check a category `C`, the zero-degree embedding and the object `A_S[0]`. Record actual elaborated types, declaration and axiom dependencies, toolchain and mathlib hashes. A `#check` success is an **interface result** only.

- **GREEN_INTERFACE:** source-pinned `A_S[0]` elaborates, with no new axioms/sorries and correct universe checks; still no CM5 theorem.
- **CHARACTERIZED_BLOCKER:** a precise failing declaration, missing instance, universe constraint or derived-solid predicate is attached to the actual compiler diagnostics.
- **PROOF_CANDIDATE:** only after R0-C/D/E are resolved by independent evidence should the source-normalized theorem be stated and attacked.
- **REJECTED:** any reinterpretation of underived `IsSolid` as derived locality, arbitrary-ring strengthening, source-number substitution, or fabricated universal derived vanishing.

For resource routing use the protected `.agents/skills/gcl-lean-colab/SKILL.md` workflow: source-lock the worker and register a suitable job in `governance/lean_colab/JOBS.json` before remote execution. Existing registered jobs must not be repurposed to run arbitrary new code. Prefer CPU Colab for the bounded interface probe; reserve a protected successor for a one-shot failed job.

**Result of this increment:** a testable logical bridge and exact first compiler obligations; `CM5-R0` remains `R0_EXACT_INTERFACE_CHARACTERIZED_BLOCKER`. No derived solidity, liquid-tensor result, `GRAPH_CERTIFIED`, independent specialist adjudication or CM5 closure is claimed.
