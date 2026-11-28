import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteInduction
import CMDGCondensedCM4P3DerivedCM5R0BarGroupMoore

/-! Transfer the rank-one base to the genuine additive bar model
by Dold–Kan full faithfulness. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarObject
open CMDG.CondensedCM5R0.BreenDeligneReducedNext
open CMDG.CondensedCM5R0.BreenDeligneFiniteBar
open CMDG.CondensedCM5R0.BreenDeligneFiniteInduction
open CMDG.CondensedCM5R0.BreenDeligneAdditiveBarTotal
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneRankOneBar

def barEMIso (A : AGrp) : bar A ≅ (em 1).obj A :=
  BreenDeligneAdditiveBarTotal.DK.unitIso.app (bar A) ≪≫ BreenDeligneAdditiveBarTotal.DK.inverse.mapIso (BarGroupMoore.groupMooreIso A)

def barReducedIso (A : AGrp) : RC (bar A) ≅ reducedChainsZ A 1 :=
  BreenDeligneMooreHomotopyTransport.ZK.mapIso
    (BreenDeligneMooreHomotopyTransport.reducedFunctor.mapIso (barEMIso A)) ≪≫
    reducedEMChainIso A 1

theorem finite_from_bar (A : AGrp)
    (h : ∀ j, Module.Finite ℤ ((RC (bar A)).homology j)) (n j : ℕ) :
    Module.Finite ℤ ((reducedChainsZ A (n+1)).homology j) := by
  apply finite_positive A (fun i => ?_) n j
  letI := h i
  exact finiteOfIso (HomologicalComplex.homologyMapIso (barReducedIso A) i).symm

#print axioms barEMIso
#print axioms finite_from_bar
end CMDG.CondensedCM5R0.BreenDeligneRankOneBar
