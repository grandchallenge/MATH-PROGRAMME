# The solidity of free solid abelian groups: a formal underived argument

*Mathematical exposition for independent scrutiny · CM4 · 8 October 2026*

**Status:** GCL-protected Lean theorem for integer coefficients and the module-level target; independent external mathematical review **open** at [#1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222). This is an explanatory proof map, not a new certificate, journal publication, claim of mathematical novelty, or substitute for reading the Lean source.

## Abstract

For a profinite space \(S\), the free solid condensed abelian group \(\mathbb Z[S]^{\blacksquare}\) is solid. This result is known from Clausen–Scholze's work on condensed mathematics. GCL has formalized the corresponding **module-level** assertion for the exact \`CondensedMod.IsSolid\` predicate and universe-lifted integer coefficients in a pinned Lean 4/mathlib environment. Instead of reconstructing the original derived-\(\mathrm{RHom}\) argument, the formal proof uses the measure/dual model of the free solid object, Nöbeling freeness of locally constant integer-valued functions, a weighted finite-Boolean reconstruction of Point-sections, and a functional-detection argument for coefficient morphisms. This note identifies the principal statements and the interfaces that require external mathematical attention.

## 1. Statement and exact formal boundary

Fix an arbitrary universe \(u\). Let \(S\) be a profinite space at that universe and let \(R=\mathrm{ULift}^{u+1}(\mathbb Z)\). Write \(P(S)\) for the exact mathlib construction \`(Condensed.profiniteSolid R).obj S\`. The proved proposition is

\[
  \forall S:\operatorname{Profinite}_u,\qquad
  \operatorname{CondensedMod.IsSolid}_R(P(S)).
\]

The \`ULift\` is part of the type-correct formal statement, not an extension to arbitrary coefficient rings. The terminal wrapper is literally:

\`\`\`lean
def CM4Target : Prop :=
  ∀ S : Profinite.{u},
    CondensedMod.IsSolid ZLift
      ((Condensed.profiniteSolid ZLift).obj S)

theorem cm4Target_via_pointFunctional : CM4Target := by
  intro S
  exact
    CMDG.CondensedCM4P3M.KernelPointBridge.profiniteSolid_isSolid_via_pointFunctional S
\`\`\`

Source: [the exact terminal Lean file](https://github.com/grandchallenge/MATH-PROGRAMME/blob/7a0f33588aa8d1add4d941c9b4681b6910644bf1/fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4Blocker.lean). The \`#print axioms\` output recorded for the terminal theorem is \`[propext, Classical.choice, Quot.sound]\`, without \`sorryAx\`. The terminal wrapper itself is short: the mathematical work lies in the imported Point-functional proof and earlier reconstructed measure model.

**Not established by this result:** the full derived/complex version of the Clausen–Scholze assertion, arbitrary finite-type integer-algebra coefficients, arbitrary rings, the corrected general-ring notion of solidity, C06, CM5, or a global condensed-mathematics library.

## 2. Why this theorem is not tautological

The notation “free *solid* object” might suggest solidity is immediate by definition. It is not: in the pinned mathlib development, the construction \`Condensed.profiniteSolid\` and the predicate \`CondensedMod.IsSolid\` exist as distinct interfaces, and the former was not already known to satisfy the latter for every profinite space. The exact source \`Mathlib/Condensed/Solid.lean\` has described the integer case as a “TODO (hard)”. A proof must construct the relevant mapping-out comparison, not simply unfold a suggestive name.

One way to recognize the obstacle is to consider morphisms from the free profinite condensed module into a discrete coefficient object. To prove the requisite solidity property, the comparison induced by solidification must be strong enough that morphisms cannot be lost. The proof reduces that question to the faithfulness of a concrete integer-valued functional.

### A finite example before the general construction

For a finite discrete profinite space \(S=\{s_1,\ldots,s_n\}\), the integer-valued functions \(C(S,\mathbb Z)\) are \(\mathbb Z^n\). A homomorphism \(\lambda:C(S,\mathbb Z)\to\mathbb Z\) is determined by its values on characteristic functions:

\[
   \lambda(f)=\sum_{j=1}^{n}\lambda(\mathbf 1_{\{s_j\}})\, f(s_j).
\]

The finite example illustrates **detection by coefficients**. It is not a proof that every functional on an infinite profinite space is a finite sum of evaluations, or that an arbitrary condensed morphism is determined by its underlying ordinary set-theoretic points. Those steps require the separate formal reconstruction and faithfulness lemmas below.

For a general profinite \(S\), any continuous map from \(S\) to a discrete target with finite image factors through a finite quotient. The compatible system of finite quotients is therefore a natural way to observe a locally constant function. Nöbeling's theorem supplies freeness for \(C(S,\mathbb Z)\), even when \(S\) is infinite. The argument combines these ingredients without pretending that the finite model is the complete proof.

## 3. The proof spine and its nontrivial joints

Here is the *logical reading order* of the protected formal proof; the headings are explanatory, not independent restatements of the Lean theorems.

### A. From Point sections to scalar data

The relevant internal-Hom/measure construction is evaluated on the one-point profinite object. The following theorems establish successively that suitable Point data can be recovered from projections and integral functionals:

- \`measurePointProjection_zero_reflects\`
- \`measurePointFunctional_zero_reflects\`
- \`measurePointIntegralFunctional_zero_reflects\`

Their proofs appear in \`CMDGCondensedCM4P3GPointFunctional.lean\`. The central issue is *zero reflection*: if the observable functional vanishes, does the original structured Point section vanish? This is not an assertion that an arbitrary presheaf is globally determined by its value at the terminal object.

### B. Reconstruct arbitrary Point-measure sections

The protected \`CM4-P2\` work provides the canonical measure/dual functor together with the right-Kan reconstruction equivalence linking it to \`Condensed.profiniteSolid\`. Nöbeling-type integral coordinates and finite Boolean probes then yield the global reconstruction

\`weightedFiniteBooleanMeasureLimitLift_measurePoint_allTrue\`.

The crucial universal quantifier concerns **arbitrary Point-measure sections**. Checking it only for finite examples or basis vectors would leave the infinite case unresolved. The exact formal proof constructs compatible finite-stage morphisms and passes to the protected limit.

### C. Annihilate the product functional

For a solid-side coefficient morphism \(d\), the formal development defines a product functional on the Nöbeling coordinate vector. The central vanishing statements include

\`kernelProductFunctional_evaluationWeight_eq_zero_of_solidification_kernel\`,
\`basisCombination_kernelProductFunctional_eq_zero_of_solidification_kernel\`, and
\`kernelProductFunctional_eq_zero_of_solidification_kernel\`.

Conceptually, when \(d\) lies in the kernel of precomposition with the relevant solidification map, the scalar functional associated to \(d\) must vanish. The *formal meaning* of the kernel condition and the quantification over test data, not the informal slogan, is what must be checked by an independent referee.

### D. Lift scalar vanishing back to morphism vanishing

The bridge

\`applied_d_point_kernelProductFunctional\`

identifies the scalar functional with evaluation of the actual coefficient morphism on reconstructed Point-measure sections. Together with zero reflection it leads to

\`coefficient_eq_zero_of_solidification_kernel\`.

This is the deepest possible hidden gap from a mathematical-exposition perspective: one must show that Point-level, integer-valued observations detect the right category-theoretic morphism. The formal proof has dedicated extensionality/naturality infrastructure for that purpose. A reviewer should not treat the finite-coordinate heuristic as adequate justification.

### E. Recover the exact solidity predicate

Finally,

\`coefficientMappingOutInjectivity_of_pointFunctional\`
\(\longrightarrow\)
\`coefficientObject_isSolid_via_pointFunctional\`
\(\longrightarrow\)
\`profiniteSolid_isSolid_via_pointFunctional\`

establish the mapping-out criterion for the coefficient object and transports it to the profinite solid object. The wrapper \`cm4Target_via_pointFunctional\` then closes the exact \`CM4Target\` proposition.

The central lemma and terminal wrapper are preserved in two separate files, rather than being hidden in an uninspectable final invocation.

## 4. Relationship to the source proof

Clausen–Scholze's *Lectures on Condensed Mathematics*, Proposition 0.5.7, establishes a stronger statement. The historical proof uses derived Hom, cohomological vanishing, and biduality involving condensed real coefficients. GCL does **not** claim to have reconstructed that derived argument. It establishes the restricted, ordinary module-level statement through a different intermediate detection principle.

This distinction is mathematically informative: higher derived machinery can be necessary for a particular proof or for a stronger derived result without being necessary for the restricted theorem. A source-proof obligation that becomes nonblocking in an alternative route has **not** thereby been proved.

The protected CM4 finalization accordingly leaves its original P4–P6 source-route auxiliaries explicitly unproved.

## 5. Falsification-focused referee agenda

An external reviewer should attempt to identify the first invalid implication, if any, in this sequence:

1. Does zero reflection at the Point component follow from the actual enriched internal-Hom and naturality data, without an unstated conservativity hypothesis?
2. Does weighted finite-Boolean reconstruction apply to *every* Point-section, and do the finite-quotient / right-Kan transitions commute with all intended maps?
3. Is the coefficient product functional's vanishing genuinely forced by the precise solidification-kernel hypothesis?
4. Does the move from an integer-valued functional to a zero condensed-module morphism require any unproved choice of basis or naturality?
5. Does the coefficient-solid criterion correspond exactly to the pinned mathlib \`CondensedMod.IsSolid\` definition?
6. Is the imported dependency closure free of an equivalent target theorem or assumption being used as a premise?

A \`#print axioms\` report is necessary evidence about foundational dependencies but cannot independently settle questions of target identification, upstream provenance, explanatory circularity, or community novelty.

See [the referee checklist](CMDG-CM4-EXTERNAL-MATHEMATICAL-REVIEW.md), with dispositions tracked in [issue #1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222).

## 6. Formal and source provenance

| Item | Exact public referent |
| --- | --- |
| Original mathematics | Clausen–Scholze, *Lectures on Condensed Mathematics*, Proposition 0.5.7 |
| Pin | Lean \`v4.33.0-rc1\`; mathlib commit \`79d0395a1825a6264ad5d269e35e60537518955e\` |
| Protected terminal theorem | [\`CMDGCondensedCM4Blocker.lean\`](https://github.com/grandchallenge/MATH-PROGRAMME/blob/7a0f33588aa8d1add4d941c9b4681b6910644bf1/fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4Blocker.lean) |
| Underived bridge | [\`CMDGCondensedCM4P3GPointFunctional.lean\`](https://github.com/grandchallenge/MATH-PROGRAMME/blob/7a0f33588aa8d1add4d941c9b4681b6910644bf1/fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P3GPointFunctional.lean) |
| Claim authority | [Protected finalization, PR #1218](https://github.com/grandchallenge/MATH-PROGRAMME/pull/1218) |
| External review | [#1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222) |
| Upstream preparation | [#1223](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1223) |

For a source-locked, executable verification sequence see the [reproducibility protocol](CMDG_CM4_REPRODUCIBILITY.md). To understand the candidate mathlib extraction route, see the [upstream readiness assessment](CMDG-CM4-MATHLIB-UPSTREAM-ASSESSMENT.md).

## 7. Scientific disposition

The **result** is historically known; the **Lean formalization** is protected and reproducible in its pinned context; the **underived proof presentation** is a candidate for an independently useful alternative argument. Novelty of the proof architecture and acceptability of the upstream code are external-review questions, not conclusions established by this note.

**First executable review step:** starting from the pinned source, inspect \`measurePointIntegralFunctional_zero_reflects\` and \`weightedFiniteBooleanMeasureLimitLift_measurePoint_allTrue\` and report whether their type signatures and imported premises justify the first two arrows of the proof spine.
