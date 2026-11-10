# CMDG-CM5 — bounded theorem frontier and capstone boundary (candidate)

**Operation:** CMDG-CM5-FRONTIER-001. **Status:** research contract candidate; no mathematical certification or CM5 completion. **Authority:** protected CMDG_CHARTER.md §§12, 14, 20, 24, 29; CM4 terminal receipt governance/cmdg_condensed_cm4_terminal_readback_001.json.

## Scientific target and separation

The charter's **CM5 capstone** is a completely dependency-accounted, manifest-relative route to a substantial Clausen–Scholze Liquid-Tensor-class theorem (or a separately admitted comparably demanding exact target). This is **not** discharged by CM4 and is not yet a frozen terminal theorem. The first bounded mathematical rung is instead the **derived extension audit** below; completion of this rung does not complete CM5.

### CM5-R0 — precise mathematical test

Fix the integer coefficients and a profinite space `S`. Let `A_S = (Condensed.profiniteSolid (ULift ℤ)).obj S` in the exact universe-correct pinned condensed-module category. Define the *candidate* derived-solid assertion:

> For all profinite `S`, the chain complex `A_S[0]`, concentrated in degree zero, belongs to the explicitly defined derived-solid subcategory of the chosen derived category of condensed abelian groups.

This is a **proposed** theorem, not a formal declaration or proved fact. It cannot even be frozen as a Lean theorem until the following exact source-to-formal interfaces are identified: (a) ambient abelian category and universe; (b) construction of `D(CondensedAb)` or equivalent; (c) definition of derived-solid/local objects and their mapping-out criterion; (d) comparison of `A_S` and the source's `ℤ[S]^□`; (e) t-exactness or another bridge needed to transport the module-level `IsSolid` result to complexes.

The source Proposition 0.5.7 (module and complex clauses) is the source audit target. Its derived clause is **not** inferred from `CMDG.CondensedCM4.cm4Target_via_pointFunctional`. The first permissible outcome may be an exact characterized interface blocker, not a false theorem.

### CM5-R1 — choice of actual capstone theorem

After R0, pin a source edition, theorem number, hypotheses, conclusion and universe/cardinality/functional-analytic setting of one Liquid-Tensor-class theorem. Record a source-normalized theorem and a dependency inventory under MATHFORGE; select only after comparing available Lean/mathlib interfaces and foundational concordance. R0 is neither required to imply R1 nor sufficient for R1. Record exact theorem identity before naming any final CM5 target.

## Dependency boundaries

| Dependency | Current scope | Promotion gate |
| --- | --- | --- |
| CM1–CM3, C05 | Protected narrower formal results | Reuse only under recorded original scopes |
| CM4 | Module-level `ULift ℤ` solidity of profiniteSolid, protected | Reuse, no automatic derived functor transport |
| Source Proposition 0.5.7, derived clause | Research target only | Source semantics and exact derived category reconstruction |
| P3 historical Ext/cohomology route, P4–P6 | Unproved source-route auxiliaries | Never silently treated as proved; nonblocking only for CM4's selected underived proof |
| C04, C05 | Restricted formal/presentation and coefficient regime | No arbitrary-ring or cardinality-free-to-source global concordance |
| C06 and `GRAPH_CERTIFIED` | Undischarged | Dedicated graph package, review, mutations and clean replay |
| Liquid-Tensor capstone | Not pinned | Separate protected exact theorem-selection and dependencies |

## Executable obligations

1. MATHFORGE: source-lock Proposition 0.5.7's **complex** assertion and one liquid-tensor capstone candidate, distinguishing module, derived, and analytic hypotheses.
2. MATHSOLVE: exact-tree inventory for the five R0 formal interfaces, with paths, declaration names, blob hashes, universe constraints and sufficiency classifications.
3. Produce either an actual Lean theorem attempt with no `sorry`/new axioms, or a minimal characterized blocker; no theorem is asserted merely by compiling an import.
4. A distinct logical Adversary pass must test the invalid inference `IsSolid A → DerivedSolid (A[0])`, cardinality changes, derived/underived conflation, and arbitrary-ring substitution.
5. Independently review source-semantic correspondence; run affected exact-pin formal replay and document checks. Governed review/merge/readback cannot turn an unproved statement into a result.
6. Select the R1 capstone theorem under a subsequent exact theorem-selection record; do not label R0 completion CM5 completion.

**Acceptance for this bounded contract:** source and proof obligations are exact and falsifiable; next formal step is identified. **Not accepted:** CM5 proved, derived solidity, liquid tensor equivalence, broader C04/C05, production GRAPH_CERTIFIED, global CMDG completion.
