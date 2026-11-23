import Mathlib.Algebra.Homology.ShortComplex.Basic
import Mathlib.Topology.Algebra.Group.Basic
import Mathlib.Condensed.TopComparison
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.Category.TopCat.Yoneda
import Mathlib.Topology.Category.CompHausLike.Limits
import Mathlib.Topology.Category.Stonean.Limits
import Mathlib.Algebra.Category.ModuleCat.Limits
import Mathlib.Condensed.Explicit
import Mathlib.Condensed.Module
import Mathlib.Topology.ContinuousMap.Algebra
import Mathlib.Topology.Category.Stonean.Basic

/-!
# CMDG CM5: genuine CondensedAb real/circle product complex

For arbitrary index type I, construct actual integer, real and circle
product objects in CondensedAb via the ModuleCat-valued Stonean
finite-product sheaf and Mathlib's Stonean–CompHaus equivalence.

Construct continuous additive topological maps I→ℤ to I→ℝ and
I→ℝ to I→UnitAddCircle, lift to natural transformations of
Stonean module presheaves and sheaves, then transfer their
morphisms to genuine CondensedAb. Prove the categorical composition
is exactly zero, yielding a genuine CondensedAb ShortComplex.

This is NOT yet a ShortExact proof in CondensedAb. A separately
Lean-proved all-index Stonean ModuleCat short exact sequence
exists in parent PR #3640. Transfer of categorical exactness,
circle-to-integers derived calculation, and canonical solidification
unit remain open. No artificial axiom or assumed comparison.
-/

noncomputable section
universe u
open CategoryTheory
namespace CMDG.CondensedCM5R0.RealCircleStoneanPresheaf

variable (M : Type (u+1)) [TopologicalSpace M] [AddCommGroup M] [IsTopologicalAddGroup M]

def probePullback {X Y : Stonean.{u}} (f : X ⟶ Y) :
    C(Y,M) →ₗ[ULift.{u+1} ℤ] C(X,M) where
  toFun g := g.comp ⟨f.hom.hom, f.hom.hom.continuous⟩
  map_add' g h := by
    ext x
    rfl
  map_smul' r g := by
    ext x
    rfl

def probePresheaf :
    Stonean.{u}ᵒᵖ ⥤ ModuleCat.{u+1} (ULift.{u+1} ℤ) where
  obj X := ModuleCat.of _ (C(X.unop,M))
  map f := ModuleCat.ofHom (probePullback M f.unop)
  map_id X := by
    ext g x
    rfl
  map_comp f g := by
    ext h x
    rfl

example : (probePresheaf M ⋙ CategoryTheory.forget (ModuleCat (ULift.{u+1} ℤ))) =
    ContinuousMap.yonedaPresheaf
      (CompHausLike.compHausLikeToTop (fun X : TopCat.{u} => ExtremallyDisconnected X))
      M := by
  rfl

noncomputable instance : CategoryTheory.Limits.PreservesFiniteProducts
    ((probePresheaf M) ⋙ CategoryTheory.forget (ModuleCat (ULift.{u+1} ℤ))) := by
  change CategoryTheory.Limits.PreservesFiniteProducts
    (ContinuousMap.yonedaPresheaf
      (CompHausLike.compHausLikeToTop (fun X : TopCat.{u} => ExtremallyDisconnected X))
      M)
  infer_instance

noncomputable def condensedTopologicalGroup : CondensedAb.{u} :=
  haveI : CategoryTheory.Limits.HasLimitsOfSize.{u,u+1}
      (ModuleCat.{u+1} (ULift.{u+1} ℤ)) :=
    CategoryTheory.Limits.hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  Condensed.ofSheafForgetStonean (probePresheaf M)

def postcomposeAddHom {N : Type (u+1)}
    [TopologicalSpace N] [AddCommGroup N] [IsTopologicalAddGroup N]
    (f : M →+ N) (hf : Continuous (f : M → N))
    (X : Stonean.{u}) : C(X,M) →+ C(X,N) where
  toFun g := ⟨fun x => f (g x), hf.comp g.continuous⟩
  map_zero' := by
    ext x
    simp
  map_add' g h := by
    ext x
    simp

def postcomposeNatTrans {N : Type (u+1)}
    [TopologicalSpace N] [AddCommGroup N] [IsTopologicalAddGroup N]
    (f : M →+ N) (hf : Continuous (f : M → N)) :
    probePresheaf M ⟶ probePresheaf N where
  app X := ModuleCat.ofHom
    ((postcomposeAddHom M f hf X.unop).toIntLinearMap)
  naturality := by
    intros X Y h
    ext g x
    rfl


theorem postcomposeNatTrans_comp_zero {N K : Type (u+1)}
    [TopologicalSpace N] [AddCommGroup N] [IsTopologicalAddGroup N]
    [TopologicalSpace K] [AddCommGroup K] [IsTopologicalAddGroup K]
    (f : M →+ N) (hf : Continuous (f : M → N))
    (g : N →+ K) (hg : Continuous (g : N → K))
    (h : g.comp f = 0) :
    postcomposeNatTrans M f hf ≫ postcomposeNatTrans N g hg = 0 := by
  ext S k
  change C(S.unop, M) at k
  change (postcomposeAddHom N g hg S.unop)
    ((postcomposeAddHom M f hf S.unop) k) = 0
  apply ContinuousMap.ext
  intro x
  change g (f (k x)) = 0
  have hh := congrArg (fun t : M →+ K => t (k x)) h
  simpa only [AddMonoidHom.comp_apply, AddMonoidHom.zero_apply] using hh

#print axioms postcomposeNatTrans_comp_zero

noncomputable def stoneanModuleSheaf :
    CategoryTheory.Sheaf
      (coherentTopology Stonean.{u})
      (ModuleCat.{u+1} (ULift.{u+1} ℤ)) := by
  letI : CategoryTheory.Limits.HasLimitsOfSize.{u,u+1}
      (ModuleCat.{u+1} (ULift.{u+1} ℤ)) :=
    CategoryTheory.Limits.hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  exact {
    obj := probePresheaf M
    property := by
      apply CategoryTheory.Presheaf.isSheaf_coherent_of_projective_of_comp
        (probePresheaf M) (CategoryTheory.forget (ModuleCat (ULift.{u+1} ℤ)))
      rw [CategoryTheory.Presheaf.isSheaf_iff_preservesFiniteProducts_of_projective]
      exact ⟨fun _ => inferInstance⟩
  }

noncomputable def condensedTopologicalGroupViaSheaf : CondensedAb.{u} := by
  letI : CategoryTheory.Limits.HasLimitsOfSize.{u,u+1}
      (ModuleCat.{u+1} (ULift.{u+1} ℤ)) :=
    CategoryTheory.Limits.hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  exact (Condensed.StoneanCompHaus.equivalence
    (ModuleCat.{u+1} (ULift.{u+1} ℤ))).functor.obj (stoneanModuleSheaf M)


def stoneanSheafMap {N : Type (u+1)}
    [TopologicalSpace N] [AddCommGroup N] [IsTopologicalAddGroup N]
    (f : M →+ N) (hf : Continuous (f : M → N)) :
    stoneanModuleSheaf M ⟶ stoneanModuleSheaf N :=
  ⟨postcomposeNatTrans M f hf⟩

noncomputable def condensedGroupMap {N : Type (u+1)}
    [TopologicalSpace N] [AddCommGroup N] [IsTopologicalAddGroup N]
    (f : M →+ N) (hf : Continuous (f : M → N)) :
    condensedTopologicalGroupViaSheaf M ⟶
      condensedTopologicalGroupViaSheaf N := by
  letI : CategoryTheory.Limits.HasLimitsOfSize.{u,u+1}
      (ModuleCat.{u+1} (ULift.{u+1} ℤ)) :=
    CategoryTheory.Limits.hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  exact (Condensed.StoneanCompHaus.equivalence
    (ModuleCat.{u+1} (ULift.{u+1} ℤ))).functor.map
      (stoneanSheafMap M f hf)


theorem stoneanSheafMap_comp_zero {N K : Type (u+1)}
    [TopologicalSpace N] [AddCommGroup N] [IsTopologicalAddGroup N]
    [TopologicalSpace K] [AddCommGroup K] [IsTopologicalAddGroup K]
    (f : M →+ N) (hf : Continuous (f : M → N))
    (g : N →+ K) (hg : Continuous (g : N → K))
    (h : g.comp f = 0) :
    stoneanSheafMap M f hf ≫ stoneanSheafMap N g hg = 0 := by
  apply CategoryTheory.Sheaf.hom_ext
  exact postcomposeNatTrans_comp_zero M f hf g hg h

theorem condensedGroupMap_comp_zero {N K : Type (u+1)}
    [TopologicalSpace N] [AddCommGroup N] [IsTopologicalAddGroup N]
    [TopologicalSpace K] [AddCommGroup K] [IsTopologicalAddGroup K]
    (f : M →+ N) (hf : Continuous (f : M → N))
    (g : N →+ K) (hg : Continuous (g : N → K))
    (h : g.comp f = 0) :
    condensedGroupMap M f hf ≫ condensedGroupMap N g hg = 0 := by
  letI : CategoryTheory.Limits.HasLimitsOfSize.{u,u+1}
      (ModuleCat.{u+1} (ULift.{u+1} ℤ)) :=
    CategoryTheory.Limits.hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  change ((Condensed.StoneanCompHaus.equivalence
    (ModuleCat.{u+1} (ULift.{u+1} ℤ))).functor).map
      (stoneanSheafMap M f hf) ≫
    ((Condensed.StoneanCompHaus.equivalence
      (ModuleCat.{u+1} (ULift.{u+1} ℤ))).functor).map
      (stoneanSheafMap N g hg) = 0
  rw [← Functor.map_comp, stoneanSheafMap_comp_zero M f hf g hg h]
  simp

#print axioms condensedGroupMap_comp_zero

variable (I : Type u)

noncomputable abbrev realProductCondensed : CondensedAb.{u} :=
  condensedTopologicalGroup.{u} (ULift.{u+1,u} (I → ℝ))

noncomputable abbrev circleProductCondensed : CondensedAb.{u} := by
  letI : IsTopologicalAddGroup
      (ULift.{u+1,u} (I → UnitAddCircle)) := ⟨⟩
  exact condensedTopologicalGroup.{u}
    (ULift.{u+1,u} (I → UnitAddCircle))

noncomputable abbrev integerProductCondensed : CondensedAb.{u} :=
  condensedTopologicalGroup.{u} (ULift.{u+1,u} (I → ℤ))

local instance (I : Type u) :
    IsTopologicalAddGroup (ULift.{u+1,u} (I → UnitAddCircle)) := ⟨⟩

def realProductTopHom (I : Type u) :
    ULift.{u+1,u} (I → ℝ) →+ ULift.{u+1,u} (I → UnitAddCircle) where
  toFun x := ⟨fun i => ((x.down i : ℝ) : UnitAddCircle)⟩
  map_zero' := by
    ext i
    rfl
  map_add' x y := by
    ext i
    rfl

theorem realProductTopHom_continuous (I : Type u) :
    Continuous (realProductTopHom I :
      ULift.{u+1,u} (I → ℝ) → ULift.{u+1,u} (I → UnitAddCircle)) := by
  apply continuous_uliftUp.comp
  apply continuous_pi
  intro i
  exact (AddCircle.continuous_mk' (1 : ℝ)).comp
    ((continuous_apply i).comp continuous_uliftDown)

def intProductTopHom (I : Type u) :
    ULift.{u+1,u} (I → ℤ) →+ ULift.{u+1,u} (I → ℝ) where
  toFun x := ⟨fun i => (x.down i : ℝ)⟩
  map_zero' := by
    ext i
    simp
  map_add' x y := by
    ext i
    simp

theorem intProductTopHom_continuous (I : Type u) :
    Continuous (intProductTopHom I :
      ULift.{u+1,u} (I → ℤ) → ULift.{u+1,u} (I → ℝ)) := by
  apply continuous_uliftUp.comp
  apply continuous_pi
  intro i
  exact continuous_of_discreteTopology.comp
    ((continuous_apply i).comp continuous_uliftDown)

theorem realProductTopHom_comp_intProductTopHom (I : Type u) :
    (realProductTopHom I).comp (intProductTopHom I) = 0 := by
  apply AddMonoidHom.ext
  intro x
  apply ULift.ext
  funext i
  change (((x.down i : ℤ) : ℝ) : UnitAddCircle) = 0
  rw [AddCircle.coe_eq_zero_iff]
  exact ⟨x.down i, by simp [zsmul_eq_mul]⟩

noncomputable def condensedIntegerToReal (I : Type u) :
    condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (I → ℤ)) ⟶
    condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (I → ℝ)) :=
  condensedGroupMap (ULift.{u+1,u} (I → ℤ))
    (intProductTopHom I) (intProductTopHom_continuous I)

noncomputable def condensedRealToCircle (I : Type u) :
    condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (I → ℝ)) ⟶
    condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (I → UnitAddCircle)) :=
  condensedGroupMap (ULift.{u+1,u} (I → ℝ))
    (realProductTopHom I) (realProductTopHom_continuous I)

noncomputable def realCircleCondensedSequence (I : Type u) :
    CategoryTheory.ShortComplex CondensedAb.{u} :=
  CategoryTheory.ShortComplex.mk
    (condensedIntegerToReal I)
    (condensedRealToCircle I)
    (condensedGroupMap_comp_zero
      (ULift.{u+1,u} (I → ℤ))
      (intProductTopHom I) (intProductTopHom_continuous I)
      (realProductTopHom I) (realProductTopHom_continuous I)
      (realProductTopHom_comp_intProductTopHom I))

#print axioms realCircleCondensedSequence
#print axioms condensedGroupMap_comp_zero
#print axioms realProductTopHom_comp_intProductTopHom

#print axioms realProductTopHom_comp_intProductTopHom



end CMDG.CondensedCM5R0.RealCircleStoneanPresheaf
