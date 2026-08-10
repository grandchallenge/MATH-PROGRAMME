import CMDGCondensedCM4P2E
import CMDGCondensedCM4P2EAlgebraic
import Mathlib.Algebra.Algebra.Bilinear

/-!
# CMDG CM4-P2-E internal-Hom bridge

This auxiliary fixture isolates the sole remaining E1 construction: comparison of the protected
P2-D sheaf-level internal Hom with the discrete algebraic dual on finite modules.

The current checkpoint develops the canonical evaluation direction and the canonical multiplication
map into the enriched end needed for its inverse. It does not yet assert the rank-one isomorphism or
the final finite comparison.
-/

namespace CMDG.CondensedCM4P2E.InternalHom

universe u

open CategoryTheory Limits Opposite
open CategoryTheory.Enriched.FunctorCategory
open scoped CategoryTheory.MonoidalClosed

abbrev R := CMDG.CondensedCM4P2E.R.{u}
abbrev PresheafModule := CMDG.CondensedCM4P2D.PresheafModule.{u}

noncomputable abbrev coefficientPresheaf : PresheafModule :=
  CMDG.CondensedCM4P2D.coefficientPresheaf

noncomputable local instance : MonoidalClosed PresheafModule :=
  MonoidalClosed.FunctorCategory.monoidalClosed

noncomputable def rankOneInternalHom : PresheafModule :=
  (MonoidalClosed.internalHom.obj (op coefficientPresheaf)).obj coefficientPresheaf

lemma rankOneInternalHom_eq_functorEnrichedHom :
    rankOneInternalHom =
      functorEnrichedHom (ModuleCat.{u + 1} R) coefficientPresheaf coefficientPresheaf := rfl

abbrev RankOneTarget := rankOneInternalHom ≅ coefficientPresheaf

noncomputable abbrev coefficientAt (X : CompHaus.{u}) : ModuleCat.{u + 1} R :=
  coefficientPresheaf.obj (op X)

noncomputable def rankOneIdentityProjection (X : CompHaus.{u}) :=
  CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
    (ModuleCat.{u + 1} R)
    (Under.forget (op X) ⋙ coefficientPresheaf)
    (Under.forget (op X) ⋙ coefficientPresheaf)
    (Under.mk (𝟙 (op X)))

noncomputable def rankOneEndomorphismEvalOne (X : CompHaus.{u}) :
    (ihom (coefficientAt X)).obj (coefficientAt X) ⟶ coefficientAt X :=
  ModuleCat.ofHom
    { toFun := fun φ => φ (show coefficientAt X from LocallyConstant.const X (1 : R))
      map_add' := by
        intro φ ψ
        rfl
      map_smul' := by
        intro c φ
        rfl }

noncomputable def rankOneEvaluationApp (X : CompHaus.{u}) :
    rankOneInternalHom.obj (op X) ⟶ coefficientAt X := by
  exact rankOneIdentityProjection X ≫ rankOneEndomorphismEvalOne X

noncomputable def rankOneSectionMul
    (X : CompHaus.{u}) (k : Under (op X))
    (a : coefficientAt X) (h : coefficientPresheaf.obj k.right) :
    coefficientPresheaf.obj k.right := by
  let Y : CompHaus.{u} := k.right.unop
  let a' : LocallyConstant Y R := coefficientPresheaf.map k.hom a
  let h' : LocallyConstant Y R := h
  exact LinearMap.mul R (LocallyConstant Y R) a' h'

lemma coefficientPullback_triangle
    (X : CompHaus.{u}) {i j : Under (op X)} (f : i ⟶ j) :
    coefficientPresheaf.map i.hom ≫ coefficientPresheaf.map f.right =
      coefficientPresheaf.map j.hom := by
  rw [← coefficientPresheaf.map_comp, Under.w f]

lemma rankOneSectionMul_naturality
    (X : CompHaus.{u}) {i j : Under (op X)} (f : i ⟶ j)
    (a : coefficientAt X) (h : coefficientPresheaf.obj i.right) :
    coefficientPresheaf.map f.right (rankOneSectionMul X i a h) =
      rankOneSectionMul X j a (coefficientPresheaf.map f.right h) := by
  let Yi : CompHaus.{u} := i.right.unop
  let Yj : CompHaus.{u} := j.right.unop
  let pull : LocallyConstant Yi R →ₗ[R] LocallyConstant Yj R :=
    (coefficientPresheaf.map f.right).hom
  have haBundled :
      coefficientPresheaf.map f.right (coefficientPresheaf.map i.hom a) =
        coefficientPresheaf.map j.hom a := by
    have htriangle := congrArg
      (fun q : coefficientAt X ⟶ coefficientPresheaf.obj j.right => q a)
      (coefficientPullback_triangle X f)
    simpa only [ModuleCat.comp_apply] using htriangle
  have ha :
      pull (show LocallyConstant Yi R from coefficientPresheaf.map i.hom a) =
        (show LocallyConstant Yj R from coefficientPresheaf.map j.hom a) := by
    exact haBundled
  have hmul (x y : LocallyConstant Yi R) :
      pull (x * y) = pull x * pull y := by
    rfl
  change
    pull
        ((show LocallyConstant Yi R from coefficientPresheaf.map i.hom a) *
          (show LocallyConstant Yi R from h)) =
      (show LocallyConstant Yj R from coefficientPresheaf.map j.hom a) *
        pull (show LocallyConstant Yi R from h)
  rw [hmul, ha]

noncomputable def rankOneMultiplicationToEndomorphism
    (X : CompHaus.{u}) (k : Under (op X)) :
    coefficientAt X ⟶
      (ihom (coefficientPresheaf.obj k.right)).obj (coefficientPresheaf.obj k.right) := by
  let Y : CompHaus.{u} := k.right.unop
  let A := LocallyConstant Y R
  let pull : coefficientAt X →ₗ[R] A := (coefficientPresheaf.map k.hom).hom
  let mul : A →ₗ[R] A →ₗ[R] A := LinearMap.mul R A
  let pack : (A →ₗ[R] A) →ₗ[R]
      (coefficientPresheaf.obj k.right ⟶ coefficientPresheaf.obj k.right) :=
    { toFun := fun f => ModuleCat.ofHom f
      map_add' := by
        intro f g
        rfl
      map_smul' := by
        intro r f
        apply ModuleCat.hom_injective
        rfl }
  exact ModuleCat.ofHom (pack.comp (mul.comp pull))

lemma rankOneMultiplicationToEndomorphism_apply
    (X : CompHaus.{u}) (k : Under (op X))
    (a : coefficientAt X) (h : coefficientPresheaf.obj k.right) :
    (show coefficientPresheaf.obj k.right ⟶ coefficientPresheaf.obj k.right from
      rankOneMultiplicationToEndomorphism X k a).hom h = rankOneSectionMul X k a h := by
  rfl

lemma monoidalClosed_pre_apply
    {M N P : ModuleCat.{u + 1} R} (f : N ⟶ M) (g : M ⟶ P) :
    ((MonoidalClosed.pre f).app P) g = f ≫ g := by
  rw [ModuleCat.monoidalClosed_pre_app]
  rfl

lemma rankOneMultiplication_condition
    (X : CompHaus.{u}) {i j : Under (op X)} (f : i ⟶ j) :
    rankOneMultiplicationToEndomorphism X i ≫
        (ihom (coefficientPresheaf.obj i.right)).map (coefficientPresheaf.map f.right) =
      rankOneMultiplicationToEndomorphism X j ≫
        (MonoidalClosed.pre (coefficientPresheaf.map f.right)).app
          (coefficientPresheaf.obj j.right) := by
  apply ModuleCat.hom_injective
  ext a
  let gi : coefficientPresheaf.obj i.right ⟶ coefficientPresheaf.obj i.right :=
    show coefficientPresheaf.obj i.right ⟶ coefficientPresheaf.obj i.right from
      rankOneMultiplicationToEndomorphism X i a
  let gj : coefficientPresheaf.obj j.right ⟶ coefficientPresheaf.obj j.right :=
    show coefficientPresheaf.obj j.right ⟶ coefficientPresheaf.obj j.right from
      rankOneMultiplicationToEndomorphism X j a
  change
    ((ihom (coefficientPresheaf.obj i.right)).map
      (coefficientPresheaf.map f.right)) gi =
      ((MonoidalClosed.pre (coefficientPresheaf.map f.right)).app
        (coefficientPresheaf.obj j.right)) gj
  rw [ModuleCat.ihom_map_apply, monoidalClosed_pre_apply]
  apply ModuleCat.hom_injective
  ext h
  change
    (coefficientPresheaf.map f.right).hom (gi.hom h) =
      gj.hom ((coefficientPresheaf.map f.right).hom h)
  simpa only [gi, gj, rankOneMultiplicationToEndomorphism_apply] using
    rankOneSectionMul_naturality X f a h

noncomputable def rankOneMultiplicationApp (X : CompHaus.{u}) :
    coefficientAt X ⟶ rankOneInternalHom.obj (op X) := by
  exact end_.lift
    (fun k => rankOneMultiplicationToEndomorphism X k)
    (fun i j f => by
      dsimp [CategoryTheory.Enriched.FunctorCategory.diagram, CategoryTheory.eHomFunctor,
        CategoryTheory.Functor.whiskerLeft]
      simpa only [
        MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerLeft,
        MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerRight] using
        rankOneMultiplication_condition X f)

lemma rankOneMultiplicationApp_projection
    (X : CompHaus.{u}) (k : Under (op X)) :
    rankOneMultiplicationApp X ≫
        CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
          (ModuleCat.{u + 1} R)
          (Under.forget (op X) ⋙ coefficientPresheaf)
          (Under.forget (op X) ⋙ coefficientPresheaf)
          k =
      rankOneMultiplicationToEndomorphism X k := by
  unfold rankOneMultiplicationApp
  exact end_.lift_π _ _ k

lemma rankOneMultiplication_identity_evalOne (X : CompHaus.{u}) :
    rankOneMultiplicationToEndomorphism X (Under.mk (𝟙 (op X))) ≫
        rankOneEndomorphismEvalOne X =
      𝟙 (coefficientAt X) := by
  apply ModuleCat.hom_injective
  ext a
  change
    (show coefficientPresheaf.obj (Under.mk (𝟙 (op X))).right ⟶
        coefficientPresheaf.obj (Under.mk (𝟙 (op X))).right from
      rankOneMultiplicationToEndomorphism X (Under.mk (𝟙 (op X))) a).hom
        (show coefficientPresheaf.obj (Under.mk (𝟙 (op X))).right from
          LocallyConstant.const X (1 : R)) =
      (show coefficientPresheaf.obj (Under.mk (𝟙 (op X))).right from a)
  rw [rankOneMultiplicationToEndomorphism_apply]
  change
    (show LocallyConstant X R from coefficientPresheaf.map (𝟙 (op X)) a) *
        LocallyConstant.const X (1 : R) =
      (show LocallyConstant X R from a)
  rw [coefficientPresheaf.map_id]
  simpa using (mul_one (show LocallyConstant X R from a))

lemma rankOneMultiplication_evaluation (X : CompHaus.{u}) :
    rankOneMultiplicationApp X ≫ rankOneEvaluationApp X = 𝟙 (coefficientAt X) := by
  unfold rankOneEvaluationApp
  rw [← Category.assoc, rankOneMultiplicationApp_projection]
  exact rankOneMultiplication_identity_evalOne X

#check rankOneInternalHom
#check rankOneInternalHom_eq_functorEnrichedHom
#check RankOneTarget
#check coefficientAt
#check rankOneIdentityProjection
#check rankOneEndomorphismEvalOne
#check rankOneEvaluationApp
#check rankOneSectionMul
#check coefficientPullback_triangle
#check rankOneSectionMul_naturality
#check rankOneMultiplicationToEndomorphism
#check rankOneMultiplicationToEndomorphism_apply
#check monoidalClosed_pre_apply
#check rankOneMultiplication_condition
#check rankOneMultiplicationApp
#check rankOneMultiplicationApp_projection
#check rankOneMultiplication_identity_evalOne
#check rankOneMultiplication_evaluation
#check Limits.end_.lift
#check Limits.end_.lift_π

#print axioms rankOneInternalHom_eq_functorEnrichedHom
#print axioms rankOneIdentityProjection
#print axioms rankOneEndomorphismEvalOne
#print axioms rankOneEvaluationApp
#print axioms rankOneSectionMul
#print axioms coefficientPullback_triangle
#print axioms rankOneSectionMul_naturality
#print axioms rankOneMultiplicationToEndomorphism
#print axioms rankOneMultiplicationToEndomorphism_apply
#print axioms monoidalClosed_pre_apply
#print axioms rankOneMultiplication_condition
#print axioms rankOneMultiplicationApp
#print axioms rankOneMultiplicationApp_projection
#print axioms rankOneMultiplication_identity_evalOne
#print axioms rankOneMultiplication_evaluation

end CMDG.CondensedCM4P2E.InternalHom
