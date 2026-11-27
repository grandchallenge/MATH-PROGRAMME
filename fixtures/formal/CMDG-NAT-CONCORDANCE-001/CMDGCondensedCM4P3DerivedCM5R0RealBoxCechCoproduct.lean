import CMDGCondensedCM4P3DerivedCM5R0RealBoxCechExact

/-! The actual sheafified relation terms are coproducts of the
genuine compact-box free modules. The inclusions intertwine the
face maps with the actual enlargements. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.RealProductProjection
open CompactCover CompactCover.Dyadic RealProductCondensedColimit
variable (S : Profinite.{u}) (I : Type u)

abbrev boxSetPsh (n : ℕ) (r : labels I n) : SetPsh.{u} :=
  (compHausToCondensed.obj (radiusBox S I (intersectionRadius I n r))).obj

def intersectionLeg (n : ℕ) (r : labels I n) :
    boxSetPsh S I n r ⟶ intersectionPresheaf S I n where
  app T := ↾fun z => ⟨r,z⟩
  naturality := by intros; rfl

def intersectionCofan (n : ℕ) : Cofan (boxSetPsh S I n) :=
  Cofan.mk (intersectionPresheaf S I n) (intersectionLeg S I n)

def intersectionCofanIsColimit (n : ℕ) : IsColimit (intersectionCofan S I n) := by
  apply evaluationJointlyReflectsColimits
  intro T
  refine { desc := fun c => ↾fun z => c.ι.app ⟨z.1⟩ z.2
           fac := ?_
           uniq := ?_ }
  · intro c j
    apply ConcreteCategory.hom_ext
    intro z
    rfl
  · intro c m hm
    apply ConcreteCategory.hom_ext
    intro z
    obtain ⟨r,g⟩ := z
    exact congrArg (fun f => f g) (hm ⟨r⟩)

abbrev boxFamily (n : ℕ) (r : labels I n) : Ambient.{u} :=
  compactFreeFunctor.obj (radiusBox S I (intersectionRadius I n r))

abbrev boxCechLeg (n : ℕ) (r : labels I n) :
    boxFamily S I n r ⟶ boxCechTerm S I n :=
  moduleSheafification.map (freePsh.map (intersectionLeg S I n r))

def boxCechCofan (n : ℕ) : Cofan (boxFamily S I n) :=
  Cofan.mk (boxCechTerm S I n) (boxCechLeg S I n)

def boxCechCofanIsColimit (n : ℕ) : IsColimit (boxCechCofan S I n) := by
  letI := (ModuleCat.adj Coeff).isLeftAdjoint
  let F := freePsh.{u} ⋙ moduleSheafification
  exact (Cofan.isColimitMapCoconeEquiv F _ (intersectionCofan S I n))
    (isColimitOfPreserves F (intersectionCofanIsColimit S I n))

def boxCechCoproductIso (n : ℕ) :
    (∐ boxFamily S I n) ≅ boxCechTerm S I n :=
  IsColimit.coconePointUniqueUpToIso (colimit.isColimit _) (boxCechCofanIsColimit S I n)

theorem boxCechTerm_extZero (n q : ℕ)
    (e : Abelian.Ext (boxCechTerm S I n) discreteIntegerCoeff (q+1)) : e=0 := by
  let iso := boxCechCoproductIso S I n
  exact ext_zero_of_retract iso.inv iso.hom iso.inv_hom_id q
    (coproduct_extPositive_zero (boxFamily S I n) discreteIntegerCoeff q
      (fun r => radiusExtZero S I (intersectionRadius I n r) q)) e

theorem intersectionLeg_face (n : ℕ) (k : Fin (n+2)) (r : labels I (n+1)) :
    intersectionLeg S I (n+1) r ≫ intersectionFaceNat S I n k =
      (forgetSheaf.map (compHausToCondensed.map (radiusInclusion S I
        (homOfLE (intersection_face_le I n k r))))) ≫
        intersectionLeg S I n (k.removeNth r) := by
  apply NatTrans.ext
  funext T
  rfl

theorem boxCechLeg_face (n : ℕ) (k : Fin (n+2)) (r : labels I (n+1)) :
    boxCechLeg S I (n+1) r ≫
      moduleSheafification.map (boxCechPshFace S I n k) =
        compactFreeFunctor.map (radiusInclusion S I (homOfLE (intersection_face_le I n k r))) ≫
          boxCechLeg S I n (k.removeNth r) := by
  let F := freePsh.{u} ⋙ moduleSheafification
  change F.map (intersectionLeg S I (n+1) r) ≫ F.map (intersectionFaceNat S I n k) =
    F.map (forgetSheaf.map (compHausToCondensed.map (radiusInclusion S I
      (homOfLE (intersection_face_le I n k r))))) ≫
      F.map (intersectionLeg S I n (k.removeNth r))
  rw [← Functor.map_comp,← Functor.map_comp,intersectionLeg_face]

#print axioms boxCechCofanIsColimit
#print axioms boxCechTerm_extZero
#print axioms boxCechLeg_face
end CMDG.CondensedCM5R0.RealProductProjection
