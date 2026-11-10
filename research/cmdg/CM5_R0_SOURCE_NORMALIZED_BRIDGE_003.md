# CMDG CM5-R0 — source-normalized derived-solidity bridge, tranche 003

**Status:** SOURCE-OBSERVED RESEARCH SPECIFICATION; NOT LEAN-PROVED; NOT SOURCE-SEMANTIC CERTIFIED.  
**Parent:** `research/cmdg/CM5_R0_DERIVED_INTERFACE_AUDIT_001.md` and `research/cmdg/CM5_R0_NEXT_CONSTRUCTIVE_TEST_002.md`.  
**Formal interface candidate:** `fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P3DerivedCM5R0Interface.lean` (PR #3184, initially a candidate).

## Source and identity

Peter Scholze, *Lectures on Condensed Mathematics*, [public source PDF](https://people.mpim-bonn.mpg.de/scholze/Condensed.pdf), Lecture V, printed pages **33–36**, and Lecture VI, printed page **39**. Source locators are mathematical/section locators, **not** a pinned PDF-byte digest. Obtain and retain a local source digest before any GCL SOURCE-SEMANTIC certification.

- Definition 5.1(ii) distinguishes the ordinary extension-property definition of solid abelian groups.
- Definition 5.1(iii) defines a solid complex by a derived mapping comparison for **every** profinite test set.
- Remark 5.2 explicitly warns that ordinary solidity `A` to derived solidity `A[0]` is not an immediate formal consequence; the converse relationship is proved later.
- Proposition 5.7 on printed page 35 directly proves that the source free solid abelian group on a profinite space is solid **both as an abelian group and as a complex**.
- Theorem 5.8(ii), stated on page 36 and proved beginning on page 39, characterizes solid complexes by their solid cohomology objects. In particular, it supplies the *general mathematical* direction from ordinary solidity of an abelian group to derived solidity of its degree-zero complex. Its proof proceeds through the source's general abstract Lemma 5.9 rather than by a definitional unfolding.

**Numbering caution:** These are locators in Scholze's *Lectures* (5.7 and 5.8). Existing GCL notes mentioning a “Proposition 0.5.7” may refer to a differently numbered source. Do not assert identical source identity from numerical resemblance; establish the actual cited edition and text first.

## Mathematical specification of the narrow bridge

Fix a profinite space `S` and `A_S := (Condensed.profiniteSolid ZLift).obj S`, with `ZLift := ULift.{u+1} ℤ` as in the protected CM4 theorem.

The **known GCL-internal result** is the underived predicate `CondensedMod.IsSolid ZLift A_S`. The desired **CM5-R0 formal target** is the source-compatible derived-local condition for the degree-zero object `A_S[0]` of an explicitly chosen derived category of condensed abelian groups.

For every profinite `T`, the source-compatible target requires an isomorphism of derived mapping objects from the free solid abelian group on `T` to `A_S[0]`, compared to the analogous derived mapping object from the ordinary free condensed abelian group on `T`. This is stronger than merely comparing degree-zero hom sets. The precise variance, universes, `ULift` equivalence, and source-to-mathlib realization require explicit proofs; a common name is not an equivalence.

## Two logically distinct formalization routes

### Route N — direct and narrow (preferred)

Mirror the source strategy for Proposition 5.7: identify the free solid object with the compatible integer measure/dual model, use freeness of locally constant integer functions, and establish the required derived comparison for **this one family of target objects**.

The source reduces the derived calculation using the integral dual structure and higher-Ext information. The crucial missing GCL formal interfaces are:

1. **R0-C:** definition of a correctly typed *derived* mapping comparison, or an equivalent derived-local predicate with explicit universal tests;
2. **R0-D:** comparison of the source free condensed/solid objects with mathlib's `profiniteFree`/`profiniteSolid` at the lifted coefficient type;
3. **R0-E-N1:** a chain of derived functor and Ext statements computing the higher-degree part of that comparison, not just its degree-zero part;
4. **R0-E-N2:** a source-compatible derived biduality or acyclicity statement under the correct hypotheses.

A machine-checked underived mapping-out comparison, or `#synth Abelian`, does not discharge N1 or N2.

### Route G — general categorical bridge (fallback)

Formalize the abstract content of Theorem 5.8 or its Lemma 5.9 in an appropriate abelian/derived setting: a complex is derived-solid precisely when the cohomology objects satisfy ordinary solidity, under the verified source hypotheses. Apply it to `A_S[0]` and the protected CM4 theorem.

This would give a reusable general theorem but requires substantially more infrastructure: an identified solid subcategory, derived categories, a localization and fully faithful derived inclusion, and control over unbounded complexes/t-structure. Do not assert generic heart-to-derived locality without the source hypotheses.

## Resolution of the earlier ambiguity

There is **no mathematical open conjecture** that the source free solid abelian group is derived-solid: the cited lectures already prove this. The unresolved GCL work is *reproducing and identifying the statement in its exact formal environment*. A generic counterexample to “heart-local implies derived-local” for some unrelated localization would not refute the source proposition or Theorem 5.8. Such an example is useful only to reject an unjustified generic shortcut.

The first concrete compiled gate is **R0-A/B**: `CondensedMod.{u} ZLift` is an abelian category, and `A_S` has a degree-zero image in the corresponding derived category. PR #3184 contains a pinned Lean interface test for this gate; success establishes only `GREEN_INTERFACE`, not derived locality.

## Adversarial source-to-formal checklist

- Keep `CondensedMod.IsSolid` and the source complex criterion distinct; do not rename the former `DerivedSolid`.
- Show that source `Z[S]^solid` is realized by the exact right-Kan-extension object in mathlib, rather than assuming the notation is self-explanatory.
- Specify a **natural** derived comparison at all profinite `T`, and prove higher-degree consequences, not just `Hom` in degree zero.
- State whether the transported source criterion uses derived `RHom` of global morphisms, internal derived Hom, or both; do not conflate them.
- Require pinned mathematical source evidence, compiler diagnostics and exact-source replay before any formal theorem or semantic-edge admission.
- Keep CM4 theorem closure, CM5 theorem status, graph certification and external specialist #1222 as separate claims.

## Next executable unit after R0-A/B

Create a bounded **R0-C/D comparison-interface** module: formalize the underived map between `profiniteFree` and `profiniteSolid`, embed its components by `singleFunctor`, and state the exact derived mapping comparison as a *definition* (not an axiom or assumed theorem). Then separately attack higher Ext through Route N. Record a minimal failing declaration if the current pinned mathlib API cannot express the derived map.

**Disposition:** `R0_SOURCE_SPEC_IDENTIFIED__FORMAL_DERIVED_BRIDGE_OPEN`. No theorem, derived-solidity certification, graph certification, upstream acceptance, or independent mathematical review is conferred by this note.
