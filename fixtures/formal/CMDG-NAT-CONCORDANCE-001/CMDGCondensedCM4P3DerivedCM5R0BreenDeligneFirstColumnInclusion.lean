import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBarTotal

/-! The actual first-column suspension map into the reduced bar total.
No assertion of its stable-range homology isomorphism is made here. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
namespace CMDG.CondensedCM5R0.BreenDeligneFirstColumnInclusion

def firstColumnOnly (X : SimplicialObject AGrp) : HomologicalComplex₂ ZMod c c :=
  (HomologicalComplex.single Ch c 1).obj ((barDouble X).X 1)

def firstColumnMap (X : SimplicialObject AGrp) : firstColumnOnly X ⟶ barDouble X :=
  HomologicalComplex.mkHomFromSingle (𝟙 _) (by
    intro k hk
    have h : k = 0 := by
      change k + 1 = 1 at hk
      omega
    subst k
    rw [Category.id_comp]
    apply HomologicalComplex.Hom.ext
    funext q
    exact (zeroColumn X q).eq_of_tgt _ _)

theorem firstColumnMap_f_one (X : SimplicialObject AGrp) :
    (firstColumnMap X).f 1 =
      (HomologicalComplex.singleObjXSelf c 1 ((barDouble X).X 1)).hom := by
  rw [firstColumnMap, HomologicalComplex.mkHomFromSingle_f, Category.comp_id]

def suspendedFirst (X : SimplicialObject AGrp) : Ch :=
  (firstColumnOnly X).total c

def suspensionInclusion (X : SimplicialObject AGrp) : suspendedFirst X ⟶ barTotal X :=
  HomologicalComplex₂.total.map (firstColumnMap X) c

set_option backward.isDefEq.respectTransparency false in
theorem suspensionInclusion_on_summand (X : SimplicialObject AGrp) (q j : ℕ)
    (h : ComplexShape.π c c c (1, q) = j) :
    (firstColumnOnly X).ιTotal c 1 q j h ≫ (suspensionInclusion X).f j =
      ((HomologicalComplex.singleObjXSelf c 1 ((barDouble X).X 1)).hom).f q ≫
        (barDouble X).ιTotal c 1 q j h := by
  change _ ≫ (HomologicalComplex₂.total.map (firstColumnMap X) c).f j = _
  rw [HomologicalComplex₂.ιTotal_map, firstColumnMap_f_one]

def suspendedReduced (A : AGrp) (n : ℕ) : Ch :=
  HomologicalComplex₂.total ((HomologicalComplex.single Ch c 1).obj (reducedChainsZ A n)) c

/-- The comparison begins with the verified reduced Dold–Kan complex. -/
def reducedSuspensionMap (A : AGrp) (n : ℕ) :
    suspendedReduced A n ⟶ barTotal ((EilenbergMacLaneModel.em n).obj A) :=
  HomologicalComplex₂.total.map
    ((HomologicalComplex.single Ch c 1).map (totalFirstColumn A n).inv) c ≫
    suspensionInclusion ((EilenbergMacLaneModel.em n).obj A)

#print axioms firstColumnMap_f_one
#print axioms suspensionInclusion_on_summand
#print axioms reducedSuspensionMap
end CMDG.CondensedCM5R0.BreenDeligneFirstColumnInclusion
