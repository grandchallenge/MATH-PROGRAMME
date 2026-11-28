import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntegerOrbitHomology

/-! Identify the orbit complex with the unreduced free chains of the
actual bar, and use the canonical reduced-free retract. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneIntegerOrbits
open CMDG.CondensedCM5R0.BreenDeligneIntegerOrbitHomology
open CMDG.CondensedCM5R0.BreenDeligneBarObject
open CMDG.CondensedCM5R0.BreenDeligneRankOneBar
open CMDG.CondensedCM5R0.BreenDeligneReducedNext
open CMDG.CondensedCM5R0.BreenDeligneFiniteBar
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneIntegerReducedHomology

def freeIso (A : AddCommGrpCat.{0}) :
    (forgetFree ⋙ toZModule).obj A ≅ (CategoryTheory.forget AddCommGrpCat.{0} ⋙ ModuleCat.free ℤ).obj A :=
  (FreeAbelianGroup.equivFinsupp A).toIntLinearEquiv.toModuleIso

theorem freeIso_gen (A : AddCommGrpCat.{0}) (x : A) :
    (freeIso A).hom (FreeAbelianGroup.of x) = ModuleCat.freeMk x :=
  FreeAbelianGroup.toFinsupp_of x

def freeNatIso : forgetFree ⋙ toZModule ≅ CategoryTheory.forget AddCommGrpCat.{0} ⋙ ModuleCat.free ℤ :=
  NatIso.ofComponents freeIso (by
    intro A B f
    apply ConcreteCategory.hom_ext
    intro x
    change (freeIso B).hom (FreeAbelianGroup.map f x) =
      (ModuleCat.free ℤ).map ((CategoryTheory.forget AddCommGrpCat.{0}).map f) ((freeIso A).hom x)
    induction x using FreeAbelianGroup.induction_on with
    | zero => rw [map_zero,map_zero,map_zero,map_zero]
    | of x =>
      have he : FreeAbelianGroup.map (fun a : A => f a) (FreeAbelianGroup.of x) =
          FreeAbelianGroup.of (f x) := by
        change FreeAbelianGroup.lift (fun a : A => FreeAbelianGroup.of (f a)) (FreeAbelianGroup.of x) = _
        exact FreeAbelianGroup.lift_apply_of _ _
      rw [he,freeIso_gen,freeIso_gen,ModuleCat.free_map_apply]
      rfl
    | neg x hx => rw [map_neg,map_neg,map_neg,map_neg,hx]
    | add x y hx hy => rw [map_add,map_add,map_add,map_add,hx,hy])

abbrev U := bar BreenDeligneIntegerOrbits.Z ⋙ forgetFree ⋙ toZModule
abbrev C := (alternatingFaceMapComplex ZMod).obj U
abbrev L := RC (bar BreenDeligneIntegerOrbits.Z)

def rawIso : C ≅ K :=
  (alternatingFaceMapComplex ZMod).mapIso
    (Functor.isoWhiskerLeft (bar BreenDeligneIntegerOrbits.Z) freeNatIso) ≪≫
  eqToIso (by rfl)

def inclS : bar BreenDeligneIntegerOrbits.Z ⋙ reducedFree ⋙ toZModule ⟶ U :=
  Functor.whiskerLeft (bar BreenDeligneIntegerOrbits.Z)
    (Functor.whiskerRight reducedInclusion toZModule)
def projS : U ⟶ bar BreenDeligneIntegerOrbits.Z ⋙ reducedFree ⋙ toZModule :=
  Functor.whiskerLeft (bar BreenDeligneIntegerOrbits.Z)
    (Functor.whiskerRight reducedProjection toZModule)

theorem splitS : inclS ≫ projS = 𝟙 _ := by
  apply NatTrans.ext
  funext Δ
  change toZModule.map (reducedInclusion.app _) ≫ toZModule.map (reducedProjection.app _) = 𝟙 _
  rw [← Functor.map_comp]
  have he := NatTrans.congr_app reducedRetract_eq ((bar BreenDeligneIntegerOrbits.Z).obj Δ)
  rw [show reducedInclusion.app _ ≫ reducedProjection.app _ = 𝟙 _ from he]
  exact toZModule.map_id _

def incl : L ⟶ K :=
  (alternatingFaceMapComplex ZMod).map inclS ≫ rawIso.hom
def proj : K ⟶ L :=
  rawIso.inv ≫ (alternatingFaceMapComplex ZMod).map projS

theorem split : incl ≫ proj = 𝟙 L := by
  unfold incl proj
  rw [Category.assoc, Iso.hom_inv_id_assoc,← Functor.map_comp,splitS]
  exact (alternatingFaceMapComplex ZMod).map_id _

theorem reduced_finite (n : ℕ) : Module.Finite ℤ (L.homology n) := by
  letI := finite_all n
  apply Module.Finite.of_surjective (homologyMap proj n).hom
  intro x
  refine ⟨homologyMap incl n x,?_⟩
  have h := congrArg (fun f => homologyMap f n) split
  rw [homologyMap_comp,homologyMap_id] at h
  exact CategoryTheory.congr_fun h x

theorem integer_em_finite (n j : ℕ) :
    Module.Finite ℤ ((reducedChainsZ BreenDeligneIntegerOrbits.Z (n+1)).homology j) :=
  finite_from_bar BreenDeligneIntegerOrbits.Z reduced_finite n j

#print axioms reduced_finite
#print axioms integer_em_finite
end CMDG.CondensedCM5R0.BreenDeligneIntegerReducedHomology
