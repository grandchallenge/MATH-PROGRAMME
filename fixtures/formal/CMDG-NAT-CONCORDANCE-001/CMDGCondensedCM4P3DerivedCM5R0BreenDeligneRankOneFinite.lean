import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntegerReducedHomology
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBottomInjectivity
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneStableLattice
import Mathlib.Algebra.Homology.ShortComplex.PreservesHomology

/-! The rank-one base and the finite stable homology input for the
lattice pseudocoherence induction. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneIntegerReducedHomology
open CMDG.CondensedCM5R0.BreenDeligneIntegerOrbitHomology
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBottomInjectivity
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneFiniteBar
open CMDG.CondensedCM5R0.BreenDeligneStableAdditive
open CMDG.CondensedCM5R0.BreenDeligneStableLattice
namespace CMDG.CondensedCM5R0.BreenDeligneRankOneFinite

local instance toZ_equivalence : toZModule.IsEquivalence := by
  let U := BreenDeligneAdditiveNextMap.U
  haveI : U.IsEquivalence := inferInstance
  haveI : (toZModule ⋙ U).IsEquivalence :=
    (Functor.isEquivalence_iff_of_iso BreenDeligneAdditiveNextMap.forgetToZIso).mpr inferInstance
  exact Functor.isEquivalence_of_comp_right toZModule U

def homologyZIso (A : AGrp) (n j : ℕ) :
    (reducedChainsZ A n).homology j ≅
      toZModule.obj (((reducedEMChains n).obj A).homology j) :=
  (((reducedEMChains n).obj A).sc j).mapHomologyIso toZModule

def bottomZIso (A : AGrp) (n : ℕ) :
    (reducedChainsZ A (n+1)).homology (n+1) ≅ toZModule.obj A :=
  homologyZIso A (n+1) (n+1) ≪≫
    toZModule.mapIso ((bottomHomologyNaturalIso n).app A)

theorem reduced_high_zero (n : ℕ) (x : L.homology (n+2)) : x = 0 := by
  have h' := congrArg (fun f => homologyMap f (n+2)) split
  rw [homologyMap_comp,homologyMap_id] at h'
  have hx := CategoryTheory.congr_fun h' x
  change homologyMap proj (n+2) (homologyMap incl (n+2) x) = x at hx
  rw [high_zero n (homologyMap incl (n+2) x),map_zero] at hx
  exact hx.symm

theorem integer_em_one_high (n : ℕ) :
    IsZero ((reducedChainsZ BreenDeligneIntegerOrbits.Z 1).homology (n+2)) := by
  let e := homologyMapIso (BreenDeligneRankOneBar.barReducedIso BreenDeligneIntegerOrbits.Z) (n+2)
  apply IsZero.of_iso _ e.symm
  apply (IsZero.iff_id_eq_zero _).mpr
  apply ConcreteCategory.hom_ext
  exact reduced_high_zero n

theorem integer_em_one_zero :
    IsZero ((reducedChainsZ BreenDeligneIntegerOrbits.Z 1).homology 0) :=
  ShortComplex.isZero_homology_of_isZero_X₂ _ (reducedChains_supported _ 1 0 (by decide))

def integer_em_one_one :
    (reducedChainsZ BreenDeligneIntegerOrbits.Z 1).homology 1 ≅ ModuleCat.of ℤ ℤ :=
  bottomZIso BreenDeligneIntegerOrbits.Z 0

theorem stable_rank_one_finite (n k : ℕ) (hn : 0 < n) :
    Module.Finite ℤ ((stableFunctor n k).obj BreenDeligneStableLattice.Z) := by
  have he : n-1+1=n := by omega
  haveI := integer_em_finite (n-1) (n+k)
  rw [he] at this
  exact finiteOfIso (homologyMapIso
    (BreenDeligneReducedNext.reducedEMChainIso BreenDeligneStableLattice.Z n) (n+k))

#print axioms integer_em_one_high
#print axioms integer_em_one_one
#print axioms stable_rank_one_finite
end CMDG.CondensedCM5R0.BreenDeligneRankOneFinite
