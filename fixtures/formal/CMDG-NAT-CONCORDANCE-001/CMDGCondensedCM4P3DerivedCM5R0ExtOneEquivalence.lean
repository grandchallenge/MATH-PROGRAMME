import CMDGCondensedCM4P3DerivedCM5R0ExtOneNaturality

/-!
# CM5 E2 — Ext¹ to negative-source-shift equivalence

The positive-target-shift realization is already an equivalence in pinned mathlib,
via `Abelian.Ext.homEquiv`.  Shifting both objects by -1 is fully faithful,
and the canonical shift-sum/zero morphism is an isomorphism.  This module
composes these three equivalences and identifies their underlying function
with the E1 realization.  No Ext¹ vanishing or arbitrary-profinite comparison
bijectivity is inferred.
-/

noncomputable section

universe u

open CategoryTheory Pretriangulated

namespace CMDG.CondensedCM5R0

private noncomputable instance : HasDerivedCategory Ambient :=
  HasDerivedCategory.standard Ambient

private noncomputable instance : HasExt.{u + 2} Ambient.{u} :=
  HasExt.standard Ambient.{u}

/-- The E1 realization is bijective for arbitrary ambient objects.
This is a categorical transport statement, not an Ext-vanishing theorem. -/
theorem extOneToNegativeHom_bijective (X Y : Ambient) :
    Function.Bijective
      (extOneToNegativeHom (X := X) (Y := Y)) := by
  let A := (DerivedCategory.singleFunctor Ambient 0).obj X
  let B := (DerivedCategory.singleFunctor Ambient 0).obj Y
  let F := shiftFunctor (DerivedCategory Ambient) (-1 : ℤ)
  let i : F.obj (B⟦(1 : ℤ)⟧) ≅ B :=
    ((shiftFunctorAdd' (DerivedCategory Ambient) (1 : ℤ) (-1 : ℤ) 0
      (by omega)).symm.app B) ≪≫
      ((shiftFunctorZero (DerivedCategory Ambient) ℤ).app B)
  let eqv : Abelian.Ext X Y 1 ≃ (F.obj A ⟶ B) :=
    (Abelian.Ext.homEquiv (X := X) (Y := Y) (n := 1)).trans
      (((Functor.FullyFaithful.ofFullyFaithful F).homEquiv A
        (B⟦(1 : ℤ)⟧)).trans i.homToEquiv)
  have heq : eqv = extOneToNegativeHom (X := X) (Y := Y) := by
    funext e
    rfl
  rw [← heq]
  exact eqv.bijective

#print axioms extOneToNegativeHom_bijective

end CMDG.CondensedCM5R0
