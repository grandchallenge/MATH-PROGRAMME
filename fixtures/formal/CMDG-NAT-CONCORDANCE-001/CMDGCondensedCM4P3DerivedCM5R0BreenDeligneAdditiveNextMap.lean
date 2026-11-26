import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneAdditiveBarShift
import Mathlib.Algebra.Category.Grp.ZModuleEquivalence

/-! Transport the ordinary chain comparison to normalized abelian-group
chains, and lift its actual maps by Dold–Kan full faithfulness. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneAdditiveBarTotal
open CMDG.CondensedCM5R0.BreenDeligneAdditiveBarShift
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneAdditiveNextMap

abbrev U : ZMod ⥤ AGrp := forget₂ ZMod AGrp

def forgetToZIso : toZModule ⋙ U ≅ 𝟭 AGrp :=
  NatIso.ofComponents (fun A => Iso.refl A) (fun f => by
    apply ConcreteCategory.hom_ext
    intro x
    rfl)

def forgetAdditiveChainsIso (X : SimplicialObject AGrp) :
    (U.mapHomologicalComplex c).obj (additiveChains X) ≅
      (alternatingFaceMapComplex AGrp).obj X := by
  refine eqToIso (congrArg (fun F => F.obj (X ⋙ toZModule))
    (AlgebraicTopology.map_alternatingFaceMapComplex U)) ≪≫ ?_
  exact (alternatingFaceMapComplex AGrp).mapIso (Functor.isoWhiskerLeft X forgetToZIso)

def ordinaryAlternatingEquiv (A : AGrp) (n : ℕ) :
    HomotopyEquiv ((alternatingFaceMapComplex AGrp).obj (barDiagonal ((EilenbergMacLaneModel.em n).obj A)))
      ((alternatingFaceMapComplex AGrp).obj ((EilenbergMacLaneModel.em (n+1)).obj A)) :=
  (HomotopyEquiv.ofIso (forgetAdditiveChainsIso _).symm).trans
    ((U.mapHomotopyEquiv (additiveNextEquiv A n)).trans
      (HomotopyEquiv.ofIso (forgetAdditiveChainsIso _)))

def ordinaryMooreEquiv (A : AGrp) (n : ℕ) :
    HomotopyEquiv ((normalizedMooreComplex AGrp).obj (barDiagonal ((EilenbergMacLaneModel.em n).obj A)))
      ((normalizedMooreComplex AGrp).obj ((EilenbergMacLaneModel.em (n+1)).obj A)) :=
  (AlgebraicTopology.DoldKan.homotopyEquivNormalizedMooreComplexAlternatingFaceMapComplex).trans
    ((ordinaryAlternatingEquiv A n).trans
      (AlgebraicTopology.DoldKan.homotopyEquivNormalizedMooreComplexAlternatingFaceMapComplex).symm)

def nextMap (A : AGrp) (n : ℕ) :
    barDiagonal ((EilenbergMacLaneModel.em n).obj A) ⟶ ((EilenbergMacLaneModel.em (n+1)).obj A) :=
  BreenDeligneAdditiveBarTotal.DK.functor.preimage (ordinaryMooreEquiv A n).hom

def nextInverse (A : AGrp) (n : ℕ) :
    ((EilenbergMacLaneModel.em (n+1)).obj A) ⟶ barDiagonal ((EilenbergMacLaneModel.em n).obj A) :=
  BreenDeligneAdditiveBarTotal.DK.functor.preimage (ordinaryMooreEquiv A n).inv

theorem nextMap_normalized (A : AGrp) (n : ℕ) :
    (normalizedMooreComplex AGrp).map (nextMap A n) = (ordinaryMooreEquiv A n).hom :=
  BreenDeligneAdditiveBarTotal.DK.functor.map_preimage _

theorem nextInverse_normalized (A : AGrp) (n : ℕ) :
    (normalizedMooreComplex AGrp).map (nextInverse A n) = (ordinaryMooreEquiv A n).inv :=
  BreenDeligneAdditiveBarTotal.DK.functor.map_preimage _

theorem nextMap_homology_isIso (A : AGrp) (n j : ℕ) :
    IsIso (homologyMap ((normalizedMooreComplex AGrp).map (nextMap A n)) j) := by
  rw [nextMap_normalized]
  change IsIso ((ordinaryMooreEquiv A n).toHomologyIso j).hom
  infer_instance

#print axioms ordinaryMooreEquiv
#print axioms nextMap_normalized
#print axioms nextMap_homology_isIso
end CMDG.CondensedCM5R0.BreenDeligneAdditiveNextMap
