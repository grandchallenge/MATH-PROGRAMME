import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneHomologyElements

/-! Stable-range homology of the actual first-column inclusion, using
finite elimination in two adjacent total degrees. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneFirstColumnInclusion
open CMDG.CondensedCM5R0.BreenDeligneFirstColumnRange
open CMDG.CondensedCM5R0.BreenDeligneColumnPower
open CMDG.CondensedCM5R0.BreenDeligneTotalCoordinates
open CMDG.CondensedCM5R0.BreenDeligneColumnElimination
open CMDG.CondensedCM5R0.BreenDeligneHomologyElements
namespace CMDG.CondensedCM5R0.BreenDeligneStableInclusion

theorem first_homology_surj (X : SimplicialObject AGrp) (j : ℕ)
    (hc : ∀ p q : ℕ, p+q=j → 2≤p → IsZero (((barDouble X).X p).homology q)) :
    Function.Surjective (homologyMap (suspensionInclusion X) j) := by
  intro h
  let F := suspensionInclusion X
  obtain ⟨z,hz⟩ := class_surj (barTotal X) j h
  let x := (barTotal X).iCycles j z
  have hd : SupportedThrough (barDouble X) (j-1) 1 ((barTotal X).d j (j-1) x) := by
    rw [cycle_closed (barTotal X) j z]
    intro p q hpq hp
    exact map_zero _
  obtain ⟨y,hy⟩ := reduce_to_first (barDouble X) j x hd hc
  obtain ⟨a,ha⟩ := first_range X j (x-(barTotal X).d (j+1) j y) hy
  have hac : (suspendedFirst X).d j (j-1) a=0 := by
    apply first_injective X (j-1)
    rw [map_zero]
    have he := CategoryTheory.congr_fun (F.comm j (j-1)) a
    change (barTotal X).d j (j-1) (F.f j a) =
      F.f (j-1) ((suspendedFirst X).d j (j-1) a) at he
    change F.f j a = _ at ha
    rw [ha] at he
    have h' := boundary_unchanged (barDouble X) j x y
    change (barTotal X).d j (j-1) (x-(barTotal X).d (j+1) j y) =
      (barTotal X).d j (j-1) x at h'
    rw [h',cycle_closed] at he
    exact he.symm
  let w := cycleOf (suspendedFirst X) j a hac
  refine ⟨(suspendedFirst X).homologyπ j w,?_⟩
  rw [map_class,← hz]
  symm
  apply class_eq_of_boundary_diff (barTotal X) j z (cyclesMap F j w) y
  rw [map_cycle_i,cycleOf_i]
  change _ = x-F.f j a
  change F.f j a = _ at ha
  rw [ha]
  abel

theorem first_homology_ker_zero (X : SimplicialObject AGrp) (j : ℕ)
    (hc : ∀ p q : ℕ, p+q=j+1 → 2≤p → IsZero (((barDouble X).X p).homology q))
    (b : (suspendedFirst X).homology j) (hb : homologyMap (suspensionInclusion X) j b=0) :
    b=0 := by
  let F := suspensionInclusion X
  obtain ⟨z,rfl⟩ := class_surj (suspendedFirst X) j b
  rw [map_class] at hb
  obtain ⟨y,hy⟩ := (class_zero_iff (barTotal X) j (cyclesMap F j z)).mp hb
  rw [map_cycle_i] at hy
  have hd : SupportedThrough (barDouble X) ((j+1)-1) 1
      ((barTotal X).d (j+1) ((j+1)-1) y) := by
    change SupportedThrough (barDouble X) j 1 ((barTotal X).d (j+1) j y)
    rw [hy]
    exact first_supported X j _
  obtain ⟨w,hw⟩ := reduce_to_first (barDouble X) (j+1) y hd hc
  obtain ⟨a,ha⟩ := first_range X (j+1) (y-(barTotal X).d (j+2) (j+1) w) hw
  have he : (suspendedFirst X).d (j+1) j a=(suspendedFirst X).iCycles j z := by
    apply first_injective X j
    have hcomm := CategoryTheory.congr_fun (F.comm (j+1) j) a
    change (barTotal X).d (j+1) j (F.f (j+1) a) =
      F.f j ((suspendedFirst X).d (j+1) j a) at hcomm
    change F.f (j+1) a = _ at ha
    rw [← hcomm,ha]
    have h := boundary_unchanged (barDouble X) (j+1) y w
    change (barTotal X).d (j+1) j (y-(barTotal X).d (j+2) (j+1) w) =
      (barTotal X).d (j+1) j y at h
    rw [h,hy]
  exact (class_zero_iff (suspendedFirst X) j z).mpr ⟨a,he⟩

theorem first_homology_inj (X : SimplicialObject AGrp) (j : ℕ)
    (hc : ∀ p q : ℕ, p+q=j+1 → 2≤p → IsZero (((barDouble X).X p).homology q)) :
    Function.Injective (homologyMap (suspensionInclusion X) j) := by
  intro a b h
  have hz : homologyMap (suspensionInclusion X) j (a-b)=0 := by
    rw [map_sub,h,sub_self]
  exact sub_eq_zero.mp (first_homology_ker_zero X j hc (a-b) hz)

theorem stableInclusion_isIso (A : AGrp) (n j : ℕ) (hj : j<2*n+1) :
    IsIso (homologyMap (suspensionInclusion ((EilenbergMacLaneModel.em n).obj A)) j) := by
  rw [ConcreteCategory.isIso_iff_bijective]
  constructor
  · apply first_homology_inj
    intro p q h hp
    exact higherColumnStableVanish A n p q hp (by omega)
  · apply first_homology_surj
    intro p q h hp
    exact higherColumnStableVanish A n p q hp (by omega)

def stableInclusionIso (A : AGrp) (n j : ℕ) (hj : j<2*n+1) :
    (suspendedFirst ((EilenbergMacLaneModel.em n).obj A)).homology j ≅
      (barTotal ((EilenbergMacLaneModel.em n).obj A)).homology j :=
  letI := stableInclusion_isIso A n j hj
  asIso (homologyMap (suspensionInclusion ((EilenbergMacLaneModel.em n).obj A)) j)

def suspendedReducedIso (A : AGrp) (n : ℕ) :
    suspendedReduced A n ≅ suspendedFirst ((EilenbergMacLaneModel.em n).obj A) :=
  HomologicalComplex₂.total.mapIso
    ((HomologicalComplex.single Ch c 1).mapIso (totalFirstColumn A n).symm) c

set_option backward.isDefEq.respectTransparency false in
theorem reducedSuspension_isIso (A : AGrp) (n j : ℕ) (hj : j<2*n+1) :
    IsIso (homologyMap (reducedSuspensionMap A n) j) := by
  letI := stableInclusion_isIso A n j hj
  change IsIso (homologyMap ((suspendedReducedIso A n).hom ≫
    suspensionInclusion ((EilenbergMacLaneModel.em n).obj A)) j)
  rw [homologyMap_comp]
  letI : IsIso (homologyMap (suspendedReducedIso A n).hom j) := by
    change IsIso (homologyMapIso (suspendedReducedIso A n) j).hom
    infer_instance
  infer_instance

def reducedSuspensionHomologyIso (A : AGrp) (n j : ℕ) (hj : j<2*n+1) :
    (suspendedReduced A n).homology j ≅
      (barTotal ((EilenbergMacLaneModel.em n).obj A)).homology j :=
  letI := reducedSuspension_isIso A n j hj
  asIso (homologyMap (reducedSuspensionMap A n) j)

#print axioms first_homology_surj
#print axioms first_homology_inj
#print axioms stableInclusion_isIso
#print axioms reducedSuspension_isIso
end CMDG.CondensedCM5R0.BreenDeligneStableInclusion
