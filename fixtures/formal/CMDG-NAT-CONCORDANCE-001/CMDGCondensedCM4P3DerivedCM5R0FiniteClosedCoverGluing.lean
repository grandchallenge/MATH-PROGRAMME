import CMDGCondensedCM4P3DerivedCM5R0DiscreteCechExtension
import Mathlib.Topology.LocallyFinite
import Mathlib.Topology.Compactness.Compact

/-!
# CM5: finite closed-cover gluing of scalar locally constant data

This module begins the *constructive*, rather than obstruction-quotient,
route to scalar Čech acyclicity on arbitrary profinite sources.

1. A compatible family of locally constant functions on a **finite
   closed cover** glues to an actual globally locally constant function.
   We do not replace closed covers by clopen covers; that replacement
   is not valid in general.
2. Every locally constant function on an arbitrary closed subset of a
   profinite space extends to the ambient profinite space. This
   specializes the protected injective-profinite extension theorem and
   gives the precise extension operation needed for cocycle induction.
3. An arbitrary integer-valued transition function on the intersection
   of two closed sets is a difference of locally constant potentials
   on the two sets, without any clopen-cover assumption.

The next substantive obligation is a finite-index induction that
pastes the prescribed transitions across *many* closed subsets, then
applies the result to the finite clopen partition of a Stonean source.
This module does not claim that arbitrary condensed sections are
scalar locally constant functions, nor Ext¹ vanishing or derived solidity.
-/

noncomputable section

universe u v w

open CategoryTheory Limits Set

namespace CMDG.CondensedCM5R0

/-- **Finite closed-cover pasting theorem.** Compatible locally
constant maps on an arbitrary finite closed cover glue globally.
The closed sets need not be open or clopen. -/
theorem locallyConstant_glue_finite_closed_cover
    {X : Type u} [TopologicalSpace X]
    {I : Type v} [Finite I] {A : Type w}
    (E : I → Set X)
    (hclosed : ∀ i, IsClosed (E i))
    (hcover : (⋃ i, E i) = Set.univ)
    (f : ∀ i, LocallyConstant (E i) A)
    (hagree : ∀ (i j : I) (x : X)
      (hi : x ∈ E i) (hj : x ∈ E j),
      f i ⟨x, hi⟩ = f j ⟨x, hj⟩) :
    ∃ g : LocallyConstant X A,
      ∀ (i : I) (x : X) (hx : x ∈ E i),
        g x = f i ⟨x, hx⟩ := by
  classical
  letI : TopologicalSpace A := ⊥
  haveI : DiscreteTopology A := ⟨rfl⟩
  let g : X → A :=
    Set.liftCover E (fun i x => f i x) hagree hcover
  have hg (i : I) (x : X) (hx : x ∈ E i) :
      g x = f i ⟨x, hx⟩ := by
    simp only [g, Set.liftCover_of_mem hx]
  have hcont (i : I) : ContinuousOn g (E i) := by
    rw [continuousOn_iff_continuous_restrict]
    have heq : (fun x : E i => g x.val) =
        (fun x : E i => f i x) := by
      funext x
      exact hg i x.val x.property
    rw [heq]
    exact (IsLocallyConstant.iff_continuous _).mp
      (f i).isLocallyConstant
  have hgcont : Continuous g :=
    (locallyFinite_of_finite E).continuous hcover hclosed hcont
  refine ⟨⟨g, (IsLocallyConstant.iff_continuous _).mpr hgcont⟩, ?_⟩
  intro i x hx
  exact hg i x hx

/-- An arbitrary closed subset of a profinite space is again
profinite. Its locally constant functions extend globally by the
protected injective-profinite finite-image theorem. -/
theorem locallyConstant_extend_closed_subset
    (X : Profinite.{u}) (U : Set X) (hU : IsClosed U)
    {A : Type v} [Inhabited A]
    (f : LocallyConstant U A) :
    ∃ g : LocallyConstant X A,
      ∀ x : U, g x.val = f x := by
  letI : CompactSpace U :=
    isCompact_iff_compactSpace.mp hU.isCompact
  let V : Profinite.{u} := Profinite.of U
  let j : V ⟶ X :=
    CompHausLike.ofHom _
      (⟨Subtype.val, continuous_subtype_val⟩ : C(U, X))
  have hj : Function.Injective j.hom.hom := by
    exact Subtype.val_injective
  obtain ⟨g, hg⟩ :=
    locallyConstant_extension_of_injective V X j hj f
  refine ⟨g, ?_⟩
  intro x
  exact hg x

/-- **Two-closed-set scalar H¹ vanishing, constructively.**
Every integer transition cochain on the closed overlap can be
written as a difference of locally constant potentials, including
when neither closed subset is clopen. This is the two-set base case
of the intended finite closed-cover induction. -/
theorem integerTwoClosedSets_transition_is_coboundary
    (X : Profinite.{u})
    (U V : Set X) (hU : IsClosed U) (hV : IsClosed V)
    (c : LocallyConstant (U ∩ V) ℤ) :
    ∃ (a : LocallyConstant U ℤ)
      (b : LocallyConstant V ℤ),
      ∀ (x : X) (hxU : x ∈ U) (hxV : x ∈ V),
        c ⟨x, ⟨hxU, hxV⟩⟩ =
          a ⟨x, hxU⟩ - b ⟨x, hxV⟩ := by
  obtain ⟨g, hg⟩ :=
    locallyConstant_extend_closed_subset X (U ∩ V)
      (hU.inter hV) c
  let ιU : C(U, X) := ⟨Subtype.val, continuous_subtype_val⟩
  refine ⟨g.comap ιU, LocallyConstant.const V 0, ?_⟩
  intro x hxU hxV
  have h := hg (⟨x, ⟨hxU, hxV⟩⟩ : U ∩ V)
  change g x = c ⟨x, ⟨hxU, hxV⟩⟩ at h
  simpa [ιU] using h.symm

#print axioms locallyConstant_glue_finite_closed_cover
#print axioms locallyConstant_extend_closed_subset
#print axioms integerTwoClosedSets_transition_is_coboundary

end CMDG.CondensedCM5R0
