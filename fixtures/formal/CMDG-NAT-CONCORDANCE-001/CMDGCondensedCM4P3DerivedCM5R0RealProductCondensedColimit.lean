import CMDGCondensedCM4P3DerivedCM5R0RealProductCompactExhaustion
import Mathlib.Condensed.TopComparison
import Mathlib.Condensed.Module
import Mathlib.CategoryTheory.Category.Preorder
import Mathlib.CategoryTheory.Limits.Types.Filtered
import Mathlib.CategoryTheory.Limits.FunctorCategory.Basic

/-! The genuine compact-box diagram and its universal property in condensed
sets. All compact probes, not just points, are used to prove the colimit.
The free condensed abelian functor carries this colimit to a colimit.
This does not assume that condensed cohomology is homotopy invariant. -/
noncomputable section
universe u
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.RealProductCompactExhaustion

namespace CMDG.CondensedCM5R0.RealProductCondensedColimit

variable (I : Type u)

abbrev Radius := {b : I → ℝ // ∀ i, 0 ≤ b i}

def liftMap {X Y : Type u} [TopologicalSpace X] [TopologicalSpace Y]
    (f : C(X,Y)) : C(ULift.{u+1,u} X, ULift.{u+1,u} Y) :=
  ⟨fun x => ⟨f x.down⟩, continuous_uliftUp.comp (f.continuous.comp continuous_uliftDown)⟩

def boxDiagramTop : Radius I ⥤ TopCat.{u+1} where
  obj b := TopCat.of (ULift.{u+1,u} (Box b.val))
  map f := TopCat.ofHom (liftMap (enlarge (leOfHom f)))
  map_id b := by
    ext x
    rfl
  map_comp f g := by
    ext x
    rfl

def boxCoconeTop : Cocone (boxDiagramTop I) where
  pt := TopCat.of (ULift.{u+1,u} (I → ℝ))
  ι :=
    { app b := TopCat.ofHom (liftMap (inclusion b.val))
      naturality f := by
        ext x
        rfl }

def boxDiagram : Radius I ⥤ CondensedSet.{u} :=
  boxDiagramTop I ⋙ topCatToCondensedSet

def boxCocone : Cocone (boxDiagram I) :=
  topCatToCondensedSet.mapCocone (boxCoconeTop I)

abbrev forgetSheaf : CondensedSet.{u} ⥤ (CompHaus.{u}ᵒᵖ ⥤ Type (u+1)) :=
  sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u+1))

/-- Actual colimit of the sections at every compact Hausdorff test. -/
def boxCoconeSectionsIsColimit (S : CompHaus.{u}ᵒᵖ) :
    IsColimit (((evaluation CompHaus.{u}ᵒᵖ (Type (u+1))).obj S).mapCocone
      (forgetSheaf.mapCocone (boxCocone I))) := by
  apply Types.FilteredColimit.isColimitOf
  · intro x
    change C(S.unop, ULift.{u+1,u} (I → ℝ)) at x
    obtain ⟨b, hb, g, hg⟩ := liftedCompactProbe_factors x
    let g' : C(S.unop, ULift.{u+1,u} (Box b)) :=
      ⟨fun s => ⟨g s⟩, continuous_uliftUp.comp g.continuous⟩
    refine ⟨⟨b,hb⟩, g', ?_⟩
    apply ContinuousMap.ext
    intro s
    exact hg s
  · intro i j x y h
    obtain ⟨b, hb, hi, hj⟩ := common_box i.val j.val
    refine ⟨⟨b,hb⟩, homOfLE hi, homOfLE hj, ?_⟩
    apply ContinuousMap.ext
    intro s
    apply ULift.ext
    apply inclusion_injective b
    have hs := congrArg
      (fun z : C(S.unop, ULift.{u+1,u} (I → ℝ)) => (z s).down) h
    exact hs

/-- The inclusion of sheaves into presheaves reflects this colimit. -/
def boxCoconeIsColimit : IsColimit (boxCocone I) := by
  apply isColimitOfReflects forgetSheaf
  exact evaluationJointlyReflectsColimits _
    (boxCoconeSectionsIsColimit I)

/-- Free abelian groups on these genuine condensed sets preserve the
colimit via the actual free-forgetful adjunction. -/
def freeBoxCoconeIsColimit :
    IsColimit ((Condensed.freeAb.{u}).mapCocone (boxCocone I)) := by
  letI := (Condensed.setAbAdjunction.{u}).isLeftAdjoint
  exact isColimitOfPreserves _ (boxCoconeIsColimit I)

#print axioms boxCoconeSectionsIsColimit
#print axioms boxCoconeIsColimit
#print axioms freeBoxCoconeIsColimit
end CMDG.CondensedCM5R0.RealProductCondensedColimit
