import CMDGCondensedCM4P3DerivedCM5R0ExtOne
import Mathlib.CategoryTheory.Shift.ShiftedHom

/-!
# CMDG CM5-R0: Ext¹ naturality for the first negative source shift

The degree-one Ext comparison in the first (contravariant) argument is
related to the actual derived-category comparison at source shift -1 by
canonical shift isomorphisms.  This file builds the map explicitly and
proves its naturality against the specific solidification morphism.

The canonical map to negative-shift morphisms is not yet shown to be a
bijection in this module.  Neither Ext¹ vanishing for arbitrary profinite
probes nor the full derived-solid theorem is assumed or proved.

No new axiom or sorry.
-/

noncomputable section

universe u

open CategoryTheory Pretriangulated

namespace CMDG.CondensedCM5R0

private noncomputable instance : HasDerivedCategory Ambient :=
  HasDerivedCategory.standard Ambient

private noncomputable instance : HasExt.{u + 2} Ambient.{u} :=
  HasExt.standard Ambient.{u}

/-- Ext¹ pullback agrees with composition on its standard
positive-target-shift derived-Hom realization. -/
private theorem extOne_precomp_hom_natural
    {X Y A : Ambient} (f : X ⟶ Y) (e : Abelian.Ext Y A 1) :
    (((Abelian.Ext.mk₀ f).precomp A (Nat.zero_add 1)) e).hom =
      (DerivedCategory.singleFunctor Ambient 0).map f ≫ e.hom := by
  change ((Abelian.Ext.mk₀ f).comp e (Nat.zero_add 1)).hom = _
  rw [Abelian.Ext.comp_hom, Abelian.Ext.mk₀_hom]
  simpa using
    (ShiftedHom.mk₀_comp (0 : ℤ) (by rfl)
      ((DerivedCategory.singleFunctor Ambient 0).map f) e.hom)

/-- Canonical realization of Ext¹(X,Y) as a morphism X[-1] → Y
in the standard derived category. The two displayed shifts are
converted using the structural shift-sum and shift-zero isomorphisms. -/
noncomputable def extOneToNegativeHom {X Y : Ambient} (e : Abelian.Ext X Y 1) :
    ((shiftFunctor (DerivedCategory Ambient) (-1 : ℤ)).obj
      ((DerivedCategory.singleFunctor Ambient 0).obj X)) ⟶
      ((DerivedCategory.singleFunctor Ambient 0).obj Y) :=
  ((shiftFunctor (DerivedCategory Ambient) (-1 : ℤ)).map e.hom) ≫
    ((shiftFunctorAdd' (DerivedCategory Ambient) (1 : ℤ) (-1 : ℤ) 0 (by omega)).inv.app
      ((DerivedCategory.singleFunctor Ambient 0).obj Y)) ≫
    ((shiftFunctorZero (DerivedCategory Ambient) ℤ).hom.app
      ((DerivedCategory.singleFunctor Ambient 0).obj Y))

/-- The degree-one Ext comparison commutes with the negative-source
shift realization for any arrow in the ambient abelian category. -/
private theorem extOne_negative_natural
    {X Y A : Ambient} (f : X ⟶ Y) (e : Abelian.Ext Y A 1) :
    extOneToNegativeHom (((Abelian.Ext.mk₀ f).precomp A (Nat.zero_add 1)) e) =
      (shiftFunctor (DerivedCategory Ambient) (-1 : ℤ)).map
        ((DerivedCategory.singleFunctor Ambient 0).map f) ≫
        extOneToNegativeHom e := by
  dsimp only [extOneToNegativeHom]
  rw [extOne_precomp_hom_natural]
  simp only [Functor.map_comp, Category.assoc]

/-- The exact GCL Ext¹ comparison and the previously protected
n=-1 derived comparison form a commuting square at every profinite test T,
including infinite T. No bijectivity is inferred from commutativity. -/
theorem extOneComparison_negative_commutes (S T : Profinite.{u})
    (e : Abelian.Ext ((Condensed.profiniteSolid Coeff).obj T)
      (underivedObject S) 1) :
    extOneToNegativeHom (extOneComparison S T e) =
      comparisonAtShift S T (-1) (extOneToNegativeHom e) := by
  unfold extOneComparison comparisonAtShift solidificationAtZero
  exact extOne_negative_natural
    ((Condensed.profiniteSolidification Coeff).app T) e

#print axioms extOneComparison_negative_commutes

end CMDG.CondensedCM5R0
