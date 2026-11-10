import CMDGCondensedCM4P3DerivedCM5R0Comparison
import Mathlib.Algebra.Homology.DerivedCategory.FullyFaithful

/-!
# CMDG CM5-R0: unshifted derived Hom comparison from CM4

The proof transfers the underived Yoneda comparison supplied by the
protected CM4 theorem through the fully faithful degree-zero embedding.

This proves only the *unshifted* Hom comparison. Identifying it with the
n = 0 shifted comparison and controlling all nonzero shifts, which involves
higher Ext data, are separate CM5 obligations.
-/

noncomputable section

universe u

open CategoryTheory

namespace CMDG.CondensedCM5R0

private noncomputable instance : HasDerivedCategory Ambient :=
  HasDerivedCategory.standard Ambient

/-- Transport a Hom-precomposition bijection along any full and faithful functor. -/
private theorem precomposition_bijective_of_full_faithful
    {C D : Type*} [Category* C] [Category* D]
    (F : C ⥤ D) [F.Full] [F.Faithful]
    {X Y A : C} (f : X ⟶ Y)
    (hf : Function.Bijective (fun g : Y ⟶ A => f ≫ g)) :
    Function.Bijective (fun g : F.obj Y ⟶ F.obj A => F.map f ≫ g) := by
  constructor
  · intro g h heq
    obtain ⟨g₀, rfl⟩ := F.map_surjective g
    obtain ⟨h₀, rfl⟩ := F.map_surjective h
    have heq₀ : f ≫ g₀ = f ≫ h₀ :=
      F.map_injective (by simpa only [Functor.map_comp] using heq)
    exact congrArg F.map (hf.1 heq₀)
  · intro q
    obtain ⟨q₀, rfl⟩ := F.map_surjective q
    obtain ⟨g, hg⟩ := hf.2 q₀
    refine ⟨F.map g, ?_⟩
    simpa only [← Functor.map_comp] using congrArg F.map hg

/-- CM4 yields the ordinary Hom-level solidification comparison on these
particular free solid targets. -/
theorem underivedPrecomposition_bijective (S T : Profinite.{u}) :
    Function.Bijective
      (fun g : ((Condensed.profiniteSolid Coeff).obj T ⟶ underivedObject S) =>
        (Condensed.profiniteSolidification Coeff).app T ≫ g) := by
  have h : IsIso ((yoneda.obj (underivedObject S)).map
      ((Condensed.profiniteSolidification Coeff).app T).op) :=
    (underivedObject_isSolid S).isIso_solidification_map T
  have hb := (CategoryTheory.isIso_iff_bijective _).mp h
  change Function.Bijective
    (fun g : ((Condensed.profiniteSolid Coeff).obj T ⟶ underivedObject S) =>
      (Condensed.profiniteSolidification Coeff).app T ≫ g) at hb
  exact hb

/-- The degree-zero derived Hom comparison follows from the protected CM4
theorem and the fully faithful degree-zero embedding. This does *not*
assert derived solidity at arbitrary shifts. -/
theorem unshiftedDerivedPrecomposition_bijective (S T : Profinite.{u}) :
    Function.Bijective
      (fun g : degreeZeroObject T ⟶ degreeZeroObject S =>
        solidificationAtZero T ≫ g) := by
  simpa only [degreeZeroObject, solidificationAtZero, underivedObject] using
    (precomposition_bijective_of_full_faithful
      (DerivedCategory.singleFunctor Ambient 0)
      ((Condensed.profiniteSolidification Coeff).app T)
      (underivedPrecomposition_bijective S T))

#print axioms underivedPrecomposition_bijective
#print axioms unshiftedDerivedPrecomposition_bijective

end CMDG.CondensedCM5R0
