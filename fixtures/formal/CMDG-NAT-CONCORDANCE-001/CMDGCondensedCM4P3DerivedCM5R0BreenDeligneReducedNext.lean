import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneMooreHomotopyTransport
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneDiagonalSuspension

/-! The actual comparison maps are inverse up to reduced-chain homotopy. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneAdditiveNextMap
open CMDG.CondensedCM5R0.BreenDeligneMooreHomotopyTransport
open CMDG.CondensedCM5R0.BreenDeligneDiagonalSuspension
open CMDG.CondensedCM5R0.BreenDeligneFirstColumnInclusion
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneReducedNext

abbrev RC (X : SimplicialObject AGrp) : Ch := ZK.obj (reducedFunctor.obj X)
abbrev RCMap {X Y : SimplicialObject AGrp} (f : X ⟶ Y) : RC X ⟶ RC Y :=
  ZK.map (reducedFunctor.map f)

def mooreHomInv (A : AGrp) (n : ℕ) :
    Homotopy (N.map (nextMap A n ≫ nextInverse A n))
      (N.map (𝟙 (barDiagonal ((EilenbergMacLaneModel.em n).obj A)))) := by
  rw [N.map_comp,N.map_id,nextMap_normalized,nextInverse_normalized]
  exact (ordinaryMooreEquiv A n).homotopyHomInvId

def mooreInvHom (A : AGrp) (n : ℕ) :
    Homotopy (N.map (nextInverse A n ≫ nextMap A n))
      (N.map (𝟙 ((EilenbergMacLaneModel.em (n+1)).obj A))) := by
  rw [N.map_comp,N.map_id,nextMap_normalized,nextInverse_normalized]
  exact (ordinaryMooreEquiv A n).homotopyInvHomId

def reducedNextEquiv (A : AGrp) (n : ℕ) :
    HomotopyEquiv (RC (barDiagonal ((EilenbergMacLaneModel.em n).obj A)))
      (RC ((EilenbergMacLaneModel.em (n+1)).obj A)) where
  hom := RCMap (nextMap A n)
  inv := RCMap (nextInverse A n)
  homotopyHomInvId := by
    rw [← ZK.map_comp,← reducedFunctor.map_comp,
      ← ZK.map_id,← reducedFunctor.map_id]
    exact reducedFromMoore (mooreHomInv A n)
  homotopyInvHomId := by
    rw [← ZK.map_comp,← reducedFunctor.map_comp,
      ← ZK.map_id,← reducedFunctor.map_id]
    exact reducedFromMoore (mooreInvHom A n)

def reducedEMChainIso (A : AGrp) (n : ℕ) :
    RC ((EilenbergMacLaneModel.em n).obj A) ≅ reducedChainsZ A n := by
  apply eqToIso
  exact (congrArg (fun F => F.obj (((EilenbergMacLaneModel.em n).obj A) ⋙ reducedFree))
    (AlgebraicTopology.map_alternatingFaceMapComplex toZModule)).symm

def fullSuspensionMap (A : AGrp) (n : ℕ) :
    suspendedReduced A n ⟶ reducedChainsZ A (n+1) :=
  diagonalSuspensionMap A n ≫ (reducedNextEquiv A n).hom ≫ (reducedEMChainIso A (n+1)).hom

set_option backward.isDefEq.respectTransparency false in
theorem fullSuspension_isIso (A : AGrp) (n j : ℕ) (hj : j<2*n+1) :
    IsIso (homologyMap (fullSuspensionMap A n) j) := by
  letI := diagonalSuspension_isIso A n j hj
  haveI : IsIso (homologyMap (reducedNextEquiv A n).hom j) :=
    (show IsIso ((reducedNextEquiv A n).toHomologyIso j).hom from inferInstance)
  haveI : IsIso (homologyMap (reducedEMChainIso A (n+1)).hom j) :=
    (show IsIso (homologyMapIso (reducedEMChainIso A (n+1)) j).hom from inferInstance)
  unfold fullSuspensionMap
  rw [homologyMap_comp,homologyMap_comp]
  infer_instance

def fullSuspensionIso (A : AGrp) (n j : ℕ) (hj : j<2*n+1) :
    (suspendedReduced A n).homology j ≅ (reducedChainsZ A (n+1)).homology j :=
  letI := fullSuspension_isIso A n j hj
  asIso (homologyMap (fullSuspensionMap A n) j)

#print axioms reducedNextEquiv
#print axioms fullSuspension_isIso
end CMDG.CondensedCM5R0.BreenDeligneReducedNext
