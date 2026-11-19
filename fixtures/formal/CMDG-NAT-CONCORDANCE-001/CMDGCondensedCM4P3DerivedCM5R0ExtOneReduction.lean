import CMDGCondensedCM4P3DerivedCM5R0ExtOneEquivalence

/-!
# CM5 E3 — transport of degree-one Ext comparison to negative shifted Hom

The E1 naturality square and E2 vertical equivalences reduce bijectivity
of the negative-one shifted comparison to bijectivity of the *actual*
solidification-induced Ext¹ comparison, for arbitrary profinite probes.

This is an exact reduction, NOT a proof of infinite-profinite Ext¹
bijectivity or vanishing. Those are the remaining research obligations.
-/

noncomputable section

universe u

open CategoryTheory Pretriangulated

namespace CMDG.CondensedCM5R0

/-- In a commuting square with bijective vertical maps, the upper
horizontal map is bijective exactly when the lower horizontal map is. -/
private theorem bijective_iff_of_commuting_vertical_bijections
    {A B C D : Type*}
    (f : A → B) (g : C → D) (u : A → C) (v : B → D)
    (hu : Function.Bijective u) (hv : Function.Bijective v)
    (h : ∀ a, v (f a) = g (u a)) :
    Function.Bijective f ↔ Function.Bijective g := by
  constructor
  · intro hf
    constructor
    · intro c c' hcc
      obtain ⟨a, rfl⟩ := hu.2 c
      obtain ⟨a', rfl⟩ := hu.2 c'
      apply congrArg u
      apply hf.1
      apply hv.1
      calc
        v (f a) = g (u a) := h a
        _ = g (u a') := hcc
        _ = v (f a') := (h a').symm
    · intro d
      obtain ⟨b, rfl⟩ := hv.2 d
      obtain ⟨a, rfl⟩ := hf.2 b
      exact ⟨u a, (h a).symm⟩
  · intro hg
    constructor
    · intro a a' haa
      apply hu.1
      apply hg.1
      calc
        g (u a) = v (f a) := (h a).symm
        _ = v (f a') := by rw [haa]
        _ = g (u a') := h a'
    · intro b
      obtain ⟨c, hc⟩ := hg.2 (v b)
      obtain ⟨a, ha⟩ := hu.2 c
      refine ⟨a, hv.1 ?_⟩
      calc
        v (f a) = g (u a) := h a
        _ = g c := by rw [ha]
        _ = v b := hc

/-- Exact E3 reduction for arbitrary profinite probes:
the negative-one shifted comparison is bijective if and only if
the ordinary Ext¹ pullback along solidification is bijective.
No finite-to-infinite inference or vanishing is used. -/
theorem comparisonAtShift_neg_one_bijective_iff_extOneComparison
    (S T : Profinite.{u}) :
    Function.Bijective (comparisonAtShift S T (-1)) ↔
      Function.Bijective (extOneComparison S T) := by
  symm
  exact bijective_iff_of_commuting_vertical_bijections
    (extOneComparison S T)
    (comparisonAtShift S T (-1))
    (extOneToNegativeHom (X := (Condensed.profiniteSolid Coeff).obj T)
      (Y := underivedObject S))
    (extOneToNegativeHom (X := (Condensed.profiniteFree Coeff).obj T)
      (Y := underivedObject S))
    (extOneToNegativeHom_bijective _ _)
    (extOneToNegativeHom_bijective _ _)
    (extOneComparison_negative_commutes S T)

#print axioms comparisonAtShift_neg_one_bijective_iff_extOneComparison

/-- Once both degree-one Ext groups are shown to vanish (expressed here
as subsingleton instances), the actual negative-shift comparison follows.
The instances are *hypotheses*, not established for infinite profinite
probes by this theorem. -/
theorem comparisonAtShift_neg_one_bijective_of_extOne_subsingleton
    (S T : Profinite.{u})
    [Subsingleton (Abelian.Ext ((Condensed.profiniteSolid Coeff).obj T)
      (underivedObject S) 1)]
    [Subsingleton (Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      (underivedObject S) 1)] :
    Function.Bijective (comparisonAtShift S T (-1)) := by
  rw [comparisonAtShift_neg_one_bijective_iff_extOneComparison]
  constructor
  · intro _ _ _
    exact Subsingleton.elim _ _
  · intro y
    refine ⟨0, ?_⟩
    exact Subsingleton.elim _ _

#print axioms comparisonAtShift_neg_one_bijective_of_extOne_subsingleton

end CMDG.CondensedCM5R0
