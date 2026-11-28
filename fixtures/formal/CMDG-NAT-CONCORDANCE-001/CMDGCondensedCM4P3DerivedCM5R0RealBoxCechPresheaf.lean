import CMDGCondensedCM4P3DerivedCM5R0RealBoxCechGeometry

noncomputable section
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.RealProductProjection
open RealProductCondensedColimit RealProductCompactExhaustion CompactCover
variable (S : Profinite.{u}) (I : Type u)

def intersectionFace (T : CompHaus.{u}) (n : ℕ) (k : Fin (n+2))
    (z : intersectionSections S I T (n+1)) : intersectionSections S I T n :=
  ⟨k.removeNth z.1,⟨z.2.down ≫ radiusInclusion S I (homOfLE (intersection_face_le I n k z.1))⟩⟩

theorem intersection_face_relation (T : CompHaus.{u}) (n : ℕ) (k : Fin (n+2))
    (z : intersectionSections S I T (n+1)) :
    intersectionToRelation S I T n (intersectionFace S I T n k z) =
      splitCechFace _ _ (liftImage S I T) n k (intersectionToRelation S I T (n+1) z) := by
  apply Subtype.ext
  funext j
  apply Sigma.ext
  · rfl
  · apply heq_of_eq
    apply ULift.ext
    apply ConcreteCategory.hom_ext
    intro t
    apply Prod.ext
    · rfl
    · funext i
      apply Subtype.ext
      rfl

def intersectionEquiv (T : CompHaus.{u}) (n : ℕ) :
    intersectionSections S I T n ≃ relationSections S I T n :=
  ⟨intersectionToRelation S I T n,relationToIntersection S I T n,
    intersectionToRelation_left S I T n,intersectionToRelation_right S I T n⟩

abbrev SetPsh := CompHaus.{u}ᵒᵖ ⥤ Type (u+1)
abbrev ModPsh := CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u+1} Coeff

def intersectionPresheaf (n : ℕ) : SetPsh.{u} where
  obj T := intersectionSections S I T.unop n
  map f := ↾fun z => ⟨z.1,⟨f.unop ≫ z.2.down⟩⟩
  map_id T := by
    apply ConcreteCategory.hom_ext
    intro z
    rcases z with ⟨r,⟨g⟩⟩
    change (⟨r,⟨𝟙 T.unop ≫ g⟩⟩ : intersectionSections S I T.unop n) = ⟨r,⟨g⟩⟩
    rw [Category.id_comp]
  map_comp f g := by
    apply ConcreteCategory.hom_ext
    intro z
    rcases z with ⟨r,⟨a⟩⟩
    change (⟨r,⟨(g.unop ≫ f.unop) ≫ a⟩⟩ : intersectionSections S I _ n) =
      ⟨r,⟨g.unop ≫ f.unop ≫ a⟩⟩
    rw [Category.assoc]

def intersectionFaceNat (n : ℕ) (k : Fin (n+2)) :
    intersectionPresheaf S I (n+1) ⟶ intersectionPresheaf S I n where
  app T := ↾intersectionFace S I T.unop n k
  naturality := by
    intro X Y f
    apply ConcreteCategory.hom_ext
    intro z
    rcases z with ⟨r,⟨a⟩⟩
    change (⟨k.removeNth r,⟨(f.unop ≫ a) ≫ radiusInclusion S I
      (homOfLE (intersection_face_le I n k r))⟩⟩ : intersectionSections S I _ n) =
      ⟨k.removeNth r,⟨f.unop ≫ a ≫ radiusInclusion S I
      (homOfLE (intersection_face_le I n k r))⟩⟩
    rw [Category.assoc]

abbrev freePsh : SetPsh.{u} ⥤ ModPsh.{u} :=
  (Functor.whiskeringRight _ _ _).obj (ModuleCat.free Coeff)

abbrev boxCechPsh (n : ℕ) := freePsh.obj (intersectionPresheaf S I n)
abbrev boxCechPshFace (n : ℕ) (k : Fin (n+2)) :=
  freePsh.map (intersectionFaceNat S I n k)

def boxCechPshD (n : ℕ) : boxCechPsh S I (n+1) ⟶ boxCechPsh S I n :=
  ∑ k : Fin (n+2), (-1 : ℤ)^(k : ℕ) • boxCechPshFace S I n k

def intersectionAug (T : CompHaus.{u}) (z : intersectionSections S I T 0) :
    realSections S I T :=
  liftImage S I T ⟨intersectionRadius I 0 z.1,z.2⟩

def intersectionAugNat : intersectionPresheaf S I 0 ⟶ (probeRealSet S I).obj where
  app T := ↾intersectionAug S I T.unop
  naturality := by
    intro X Y f
    apply ConcreteCategory.hom_ext
    intro z
    rfl

abbrev boxCechPshAug := freePsh.map (intersectionAugNat S I)

def boxCechEvalIso (T : CompHaus.{u}) (n : ℕ) :
    (boxCechPsh S I n).obj (op T) ≅
      (ModuleCat.free Coeff).obj (relationSections S I T n) :=
  (ModuleCat.free Coeff).mapIso (equivEquivIso (intersectionEquiv S I T n))

theorem boxCechEvalFace (T : CompHaus.{u}) (n : ℕ) (k : Fin (n+2)) :
    (boxCechPshFace S I n k).app (op T) ≫ (boxCechEvalIso S I T n).hom =
      (boxCechEvalIso S I T (n+1)).hom ≫
        (ModuleCat.free Coeff).map (↾splitCechFace _ _ (liftImage S I T) n k) := by
  change (ModuleCat.free Coeff).map (↾intersectionFace S I T n k) ≫
    (ModuleCat.free Coeff).map (↾intersectionToRelation S I T n) =
    (ModuleCat.free Coeff).map (↾intersectionToRelation S I T (n+1)) ≫
    (ModuleCat.free Coeff).map (↾splitCechFace _ _ (liftImage S I T) n k)
  rw [← Functor.map_comp,← Functor.map_comp]
  congr 1

theorem boxCechEvalD (T : CompHaus.{u}) (n : ℕ) :
    (boxCechPshD S I n).app (op T) ≫ (boxCechEvalIso S I T n).hom =
      (boxCechEvalIso S I T (n+1)).hom ≫
        splitBarD _ _ (liftImage S I T) n := by
  unfold boxCechPshD splitBarD
  rw [NatTrans.app_sum]
  simp only [NatTrans.app_zsmul,Preadditive.sum_comp,Preadditive.comp_sum,
    Preadditive.zsmul_comp,Preadditive.comp_zsmul,boxCechEvalFace]

theorem boxCechEvalAug (T : CompHaus.{u}) :
    (boxCechPshAug S I).app (op T) =
      (boxCechEvalIso S I T 0).hom ≫ splitBarBaseMap _ _ (liftImage S I T) := by
  change (ModuleCat.free Coeff).map (↾intersectionAug S I T) =
    (ModuleCat.free Coeff).map (↾intersectionToRelation S I T 0) ≫
      (ModuleCat.free Coeff).map (↾splitCechBaseProjection _ _ (liftImage S I T))
  rw [← Functor.map_comp]
  rfl

#print axioms boxCechEvalD
#print axioms boxCechEvalAug
end CMDG.CondensedCM5R0.RealProductProjection
