import CMDGCondensedCM4P3DerivedCM5R0FiniteProbes
import Mathlib.Algebra.Homology.DerivedCategory.Ext.Basic
import Mathlib.CategoryTheory.ConcreteCategory.EpiMono

/-!
# CMDG CM5-R0: the degree-one Ext obstruction for arbitrary profinite probes

For an arbitrary profinite test object T, the first negative source shift
of the already protected derived comparison is governed by the contravariant
degree-one Ext map induced by the underived solidification morphism.

This source defines that actual Ext¹ map (as an additive homomorphism) in
mathlib's pinned abelian-category Ext implementation, not a formal placeholder
with a guessed codomain. It independently proves its bijectivity on finite
profinite tests. The infinite-profinite bijectivity and the natural
Ext¹/shifted-Hom comparison square are NOT proved here.

Source-semantic identification, derived solidity, and other negative shifts
remain open. No additional axioms, sorry, or general coefficient change.
-/

noncomputable section

universe u

open CategoryTheory

namespace CMDG.CondensedCM5R0

private noncomputable instance : HasDerivedCategory Ambient :=
  HasDerivedCategory.standard Ambient

private noncomputable instance : HasExt.{u + 2} Ambient.{u} :=
  HasExt.standard Ambient.{u}

/-- The explicit Ext¹ map pulled back along ordinary free-to-solid
solidification for any profinite T, into the existing protected CM4 target.
No claim of injectivity or surjectivity for arbitrary T is made. -/
noncomputable def extOneComparison (S T : Profinite.{u}) :
    Abelian.Ext ((Condensed.profiniteSolid Coeff).obj T) (underivedObject S) 1 →+
      Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) (underivedObject S) 1 :=
  (Abelian.Ext.mk₀ ((Condensed.profiniteSolidification Coeff).app T)).precomp
    (underivedObject S) (Nat.zero_add 1)

/-- The Ext¹ comparison preserves addition, even for infinite profinite tests. -/
theorem extOneComparison_add (S T : Profinite.{u})
    (a b : Abelian.Ext ((Condensed.profiniteSolid Coeff).obj T)
      (underivedObject S) 1) :
    extOneComparison S T (a + b) =
      extOneComparison S T a + extOneComparison S T b :=
  map_add (extOneComparison S T) a b

/-- In the pinned Ext implementation, the map induced by an isomorphism
in the first argument is bijective. -/
private theorem extOne_precomp_bijective_of_isIso
    {X Y A : Ambient} (f : X ⟶ Y) [IsIso f] :
    Function.Bijective
      ((Abelian.Ext.mk₀ f).precomp A (Nat.zero_add 1)) := by
  let F := Abelian.extFunctor (C := Ambient) 1
  have hf : IsIso ((F.map f.op).app A) := inferInstance
  have hb : Function.Bijective ((F.map f.op).app A) :=
    ConcreteCategory.bijective_of_isIso _
  change Function.Bijective
    ((Abelian.Ext.mk₀ f).precomp A (Nat.zero_add 1)) at hb
  exact hb

/-- For every integer-coefficient free solid CM4 target, the degree-one
Ext map is bijective on finite test objects. The general infinite-profinite
Ext¹ obstruction remains open. -/
theorem extOneComparison_finite_bijective (S : Profinite.{u})
    (X : FintypeCat.{u}) :
    Function.Bijective
      (extOneComparison S (FintypeCat.toProfinite.obj X)) := by
  letI : IsIso ((Condensed.profiniteSolidification Coeff).app
      (FintypeCat.toProfinite.obj X)) :=
    solidification_isIso_finite X
  exact extOne_precomp_bijective_of_isIso
    ((Condensed.profiniteSolidification Coeff).app
      (FintypeCat.toProfinite.obj X))

#print axioms extOneComparison_add
#print axioms extOneComparison_finite_bijective

end CMDG.CondensedCM5R0
