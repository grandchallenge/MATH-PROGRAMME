import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneDiagramComparison
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneAdditiveBarMoore
import Mathlib.AlgebraicTopology.DoldKan.Equivalence
import Mathlib.Algebra.Homology.TotalComplexSymmetry

/-! Compare the ordinary additive diagonal bar chains with a double
single complex.  This does not yet transport reduced free chains. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarObject
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneDiagramNormalization
open CMDG.CondensedCM5R0.BreenDeligneDiagramComparison
open CMDG.CondensedCM5R0.BreenDeligneAdditiveBarMoore
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
namespace CMDG.CondensedCM5R0.BreenDeligneAdditiveBarTotal

set_option backward.isDefEq.respectTransparency false in
local instance : TotalComplexShapeSymmetry c c c where
  symm p q := Nat.add_comm q p
  σ p q := (-1 : ℤˣ)^(p*q)
  σ_ε₁ := by
    intro p p' hp q
    change p'+1=p at hp
    subst p
    apply Units.ext
    change (-1 : ℤ)^((p'+1)*q)*1 = (-1)^q * (-1)^(p'*q)
    rw [Nat.add_mul,Nat.one_mul,pow_add,mul_one,mul_comm]
  σ_ε₂ := by
    intro p q q' hq
    change q'+1=q at hq
    subst q
    apply Units.ext
    change (-1 : ℤ)^(p*(q'+1)) * (-1)^p = 1 * (-1)^(p*q')
    rw [Nat.mul_add,Nat.mul_one,pow_add,mul_assoc,one_mul,← pow_add]
    have h : (-1 : ℤ)^(p+p) = 1 := by
      rw [← two_mul,pow_mul]
      norm_num
    rw [h,mul_one]

abbrev singleZ (n : ℕ) := HomologicalComplex.single ZMod c n
abbrev S1 := singleZ 1
def additiveChains (X : SimplicialObject AGrp) : Ch :=
  (alternatingFaceMapComplex ZMod).obj (X ⋙ toZModule)

def mooreSingleZ : horizontalMooreZ barFunctor ≅ toZModule ⋙ S1 :=
  Functor.isoWhiskerRight mooreSingleNatIso (toZModule.mapHomologicalComplex c) ≪≫
    HomologicalComplex.singleMapHomologicalComplex toZModule c 1

def singleRows (K : Ch) : BC := (S1.mapHomologicalComplex c).obj K

def singleRowsIso (X : SimplicialObject AGrp) :
    (normDouble barFunctor X).flip ≅ singleRows (additiveChains X) := by
  refine (alternatingFaceMapComplex Ch).mapIso
    (Functor.isoWhiskerLeft X mooreSingleZ) ≪≫ ?_
  apply eqToIso
  exact (congrArg (fun F => F.obj (X ⋙ toZModule))
    (AlgebraicTopology.map_alternatingFaceMapComplex S1)).symm

def additiveDiagIso (X : SimplicialObject AGrp) :
    barDiagonal X ⋙ toZModule ≅ diagonal (barBi barFunctor X) :=
  NatIso.ofComponents (fun _ => Iso.refl _) (fun {a b} f => by
    change toZModule.map ((barNat (X.map f)).app a ≫ (bar (X.obj b)).map f) ≫ 𝟙 _ =
      𝟙 _ ≫ (toZModule.map ((barNat (X.map f)).app a) ≫
        toZModule.map ((bar (X.obj b)).map f))
    rw [Category.comp_id,Category.id_comp,Functor.map_comp])

def additiveDiagonalEquiv (X : SimplicialObject AGrp) :
    HomotopyEquiv (additiveChains (barDiagonal X)) ((singleRows (additiveChains X)).total c) :=
  (HomotopyEquiv.ofIso ((alternatingFaceMapComplex ZMod).mapIso (additiveDiagIso X))).trans
    ((diagonalComparison barFunctor X).trans
      (HomotopyEquiv.ofIso (((normDouble barFunctor X).totalFlipIso c).symm ≪≫
        HomologicalComplex₂.total.mapIso (singleRowsIso X) c)))

def totalizeEquiv {K L : BC} (e : HomotopyEquiv K L) :
    HomotopyEquiv (K.total c) (L.total c) where
  hom := HomologicalComplex₂.total.map e.hom c
  inv := HomologicalComplex₂.total.map e.inv c
  homotopyHomInvId := by
    rw [← HomologicalComplex₂.total.map_comp,← HomologicalComplex₂.total.map_id K c]
    exact liftHomotopy e.homotopyHomInvId
  homotopyInvHomId := by
    rw [← HomologicalComplex₂.total.map_comp,← HomologicalComplex₂.total.map_id L c]
    exact liftHomotopy e.homotopyInvHomId

def singleRowsEquiv {K L : Ch} (e : HomotopyEquiv K L) :
    HomotopyEquiv ((singleRows K).total c) ((singleRows L).total c) :=
  totalizeEquiv (S1.mapHomotopyEquiv e)

abbrev DK := (CategoryTheory.Abelian.DoldKan.equivalence :
  SimplicialObject AGrp ≌ ChainComplex AGrp ℕ)

def emMooreIso (A : AGrp) (n : ℕ) :
    (normalizedMooreComplex AGrp).obj ((em n).obj A) ≅ (singleDegree n).obj A :=
  DK.counitIso.app ((singleDegree n).obj A)

def additiveEMEquiv (A : AGrp) (n : ℕ) :
    HomotopyEquiv (additiveChains ((em n).obj A)) ((singleZ n).obj (toZModule.obj A)) := by
  let X := (em n).obj A
  refine (HomotopyEquiv.ofIso (eqToIso ?_)).trans
    ((toZModule.mapHomotopyEquiv
      (AlgebraicTopology.DoldKan.homotopyEquivNormalizedMooreComplexAlternatingFaceMapComplex (Y:=X)).symm).trans
      (HomotopyEquiv.ofIso ((toZModule.mapHomologicalComplex c).mapIso (emMooreIso A n) ≪≫
        (HomologicalComplex.singleMapHomologicalComplex toZModule c n).app A)))
  exact (congrArg (fun F => F.obj X)
    (AlgebraicTopology.map_alternatingFaceMapComplex toZModule)).symm

def additiveBarDoubleSingleEquiv (A : AGrp) (n : ℕ) :
    HomotopyEquiv (additiveChains (barDiagonal ((em n).obj A)))
      ((singleRows ((singleZ n).obj (toZModule.obj A))).total c) :=
  (additiveDiagonalEquiv ((em n).obj A)).trans (singleRowsEquiv (additiveEMEquiv A n))

#print axioms additiveDiagonalEquiv
#print axioms additiveEMEquiv
#print axioms additiveBarDoubleSingleEquiv
end CMDG.CondensedCM5R0.BreenDeligneAdditiveBarTotal
