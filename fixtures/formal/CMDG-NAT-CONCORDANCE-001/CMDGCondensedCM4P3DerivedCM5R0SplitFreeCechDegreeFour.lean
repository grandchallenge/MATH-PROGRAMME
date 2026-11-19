import CMDGCondensedCM4P3DerivedCM5R0GenuineSixfoldCechFaces
import CMDGCondensedCM4P3DerivedCM5R0SplitFreeCechDegreeThree
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat

/-!
# CM5: split-set sixfold Čech degree-four contraction

For every split set map p:X→Y, the true signed free-module
five/sixfold Čech differential at degree four is contracted by
appending the chosen section. This is a SET-LEVEL theorem, not
a claim of condensed sheaf exactness or Ext5 vanishing.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0
variable {X Y : Type (u + 1)}

def splitFreeCechSextuple (p : X → Y) : Type (u + 1) :=
  {q : X × (X × (X × (X × (X × X)))) //
    p q.1 = p q.2.1 ∧
    p q.1 = p q.2.2.1 ∧
    p q.1 = p q.2.2.2.1 ∧
    p q.1 = p q.2.2.2.2.1 ∧
    p q.1 = p q.2.2.2.2.2}

def splitFreeCechSextFace0 (p : X → Y) :
    splitFreeCechSextuple p → splitFreeCechQuintuple p :=
  fun q => ⟨(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,q.val.2.2.2.2.2)))), ⟨(q.property.1.symm.trans q.property.2.1),(q.property.1.symm.trans q.property.2.2.1),(q.property.1.symm.trans q.property.2.2.2.1),(q.property.1.symm.trans q.property.2.2.2.2)⟩⟩

def splitFreeCechSextFace1 (p : X → Y) :
    splitFreeCechSextuple p → splitFreeCechQuintuple p :=
  fun q => ⟨(q.val.1,(q.val.2.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,q.val.2.2.2.2.2)))), ⟨q.property.2.1,q.property.2.2.1,q.property.2.2.2.1,q.property.2.2.2.2⟩⟩

def splitFreeCechSextFace2 (p : X → Y) :
    splitFreeCechSextuple p → splitFreeCechQuintuple p :=
  fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,q.val.2.2.2.2.2)))), ⟨q.property.1,q.property.2.2.1,q.property.2.2.2.1,q.property.2.2.2.2⟩⟩

def splitFreeCechSextFace3 (p : X → Y) :
    splitFreeCechSextuple p → splitFreeCechQuintuple p :=
  fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.2.1,q.val.2.2.2.2.2)))), ⟨q.property.1,q.property.2.1,q.property.2.2.2.1,q.property.2.2.2.2⟩⟩

def splitFreeCechSextFace4 (p : X → Y) :
    splitFreeCechSextuple p → splitFreeCechQuintuple p :=
  fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,q.val.2.2.2.2.2)))), ⟨q.property.1,q.property.2.1,q.property.2.2.1,q.property.2.2.2.2⟩⟩

def splitFreeCechSextFace5 (p : X → Y) :
    splitFreeCechSextuple p → splitFreeCechQuintuple p :=
  fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,q.val.2.2.2.2.1)))), ⟨q.property.1,q.property.2.1,q.property.2.2.1,q.property.2.2.2.1⟩⟩

noncomputable def splitFreeCechD5 (p : X → Y) :
    (ModuleCat.free Coeff).obj (splitFreeCechSextuple p) ⟶
    (ModuleCat.free Coeff).obj (splitFreeCechQuintuple p) :=
  (ModuleCat.free Coeff).map (↾(splitFreeCechSextFace0 p))
  - (ModuleCat.free Coeff).map (↾(splitFreeCechSextFace1 p))
  + (ModuleCat.free Coeff).map (↾(splitFreeCechSextFace2 p))
  - (ModuleCat.free Coeff).map (↾(splitFreeCechSextFace3 p))
  + (ModuleCat.free Coeff).map (↾(splitFreeCechSextFace4 p))
  - (ModuleCat.free Coeff).map (↾(splitFreeCechSextFace5 p))

def splitFreeCechContractSext
    (p : X → Y) (sect : Y → X) (hs : ∀ y, p (sect y) = y)
    (q : splitFreeCechQuintuple p) : splitFreeCechSextuple p :=
  ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,
      (q.val.2.2.2.1,(q.val.2.2.2.2,sect (p q.val.1)))))),
    ⟨q.property.1,q.property.2.1,q.property.2.2.1,
      q.property.2.2.2,(hs (p q.val.1)).symm⟩⟩

noncomputable def splitFreeCechH4
    (p : X → Y) (sect : Y → X) (hs : ∀ y, p (sect y) = y) :
    (ModuleCat.free Coeff).obj (splitFreeCechQuintuple p) ⟶
    (ModuleCat.free Coeff).obj (splitFreeCechSextuple p) :=
  (ModuleCat.free Coeff).map (↾(splitFreeCechContractSext p sect hs))

private theorem splitFreeCechContractSext_face0
    (p : X → Y) (sect : Y → X) (hs : ∀ y, p (sect y) = y) :
    (↾(splitFreeCechContractSext p sect hs) :
      splitFreeCechQuintuple p ⟶ splitFreeCechSextuple p) ≫
      (↾(splitFreeCechSextFace0 p)) =
      (↾(splitFreeCechQuintFace0 p)) ≫
        (↾(splitFreeCechContractQuint p sect hs)) := by
  ext q
  apply Subtype.ext
  apply Prod.ext
  · rfl
  · apply Prod.ext
    · rfl
    · apply Prod.ext
      · rfl
      · apply Prod.ext
        · rfl
        · exact congrArg sect q.property.1

private theorem splitFreeCechContractSext_face1
    (p : X → Y) (sect : Y → X) (hs : ∀ y, p (sect y) = y) :
    (↾(splitFreeCechContractSext p sect hs) :
      splitFreeCechQuintuple p ⟶ splitFreeCechSextuple p) ≫
      (↾(splitFreeCechSextFace1 p)) =
      (↾(splitFreeCechQuintFace1 p)) ≫
        (↾(splitFreeCechContractQuint p sect hs)) := by
  ext q
  apply Subtype.ext
  rfl

private theorem splitFreeCechContractSext_face2
    (p : X → Y) (sect : Y → X) (hs : ∀ y, p (sect y) = y) :
    (↾(splitFreeCechContractSext p sect hs) :
      splitFreeCechQuintuple p ⟶ splitFreeCechSextuple p) ≫
      (↾(splitFreeCechSextFace2 p)) =
      (↾(splitFreeCechQuintFace2 p)) ≫
        (↾(splitFreeCechContractQuint p sect hs)) := by
  ext q
  apply Subtype.ext
  rfl

private theorem splitFreeCechContractSext_face3
    (p : X → Y) (sect : Y → X) (hs : ∀ y, p (sect y) = y) :
    (↾(splitFreeCechContractSext p sect hs) :
      splitFreeCechQuintuple p ⟶ splitFreeCechSextuple p) ≫
      (↾(splitFreeCechSextFace3 p)) =
      (↾(splitFreeCechQuintFace3 p)) ≫
        (↾(splitFreeCechContractQuint p sect hs)) := by
  ext q
  apply Subtype.ext
  rfl

private theorem splitFreeCechContractSext_face4
    (p : X → Y) (sect : Y → X) (hs : ∀ y, p (sect y) = y) :
    (↾(splitFreeCechContractSext p sect hs) :
      splitFreeCechQuintuple p ⟶ splitFreeCechSextuple p) ≫
      (↾(splitFreeCechSextFace4 p)) =
      (↾(splitFreeCechQuintFace4 p)) ≫
        (↾(splitFreeCechContractQuint p sect hs)) := by
  ext q
  apply Subtype.ext
  rfl

private theorem splitFreeCechContractSext_face5
    (p : X → Y) (sect : Y → X) (hs : ∀ y, p (sect y) = y) :
    (↾(splitFreeCechContractSext p sect hs) :
      splitFreeCechQuintuple p ⟶ splitFreeCechSextuple p) ≫
      (↾(splitFreeCechSextFace5 p)) =
      𝟙 (splitFreeCechQuintuple p) := by
  ext q
  apply Subtype.ext
  rfl

/-- Sixth-face contracting homotopy, with NEGATIVE last face:
H4*d5 = d4*H3 - id. -/
theorem splitFreeCech_degreeFour_contraction
    (p : X → Y) (sect : Y → X) (hs : ∀ y, p (sect y) = y) :
    splitFreeCechH4 p sect hs ≫ splitFreeCechD5 p =
      splitFreeCechD4 p ≫ splitFreeCechH3 p sect hs - 𝟙 _ := by
  unfold splitFreeCechH4 splitFreeCechD5
    splitFreeCechD4 splitFreeCechH3
  simp only [Preadditive.comp_sub, Preadditive.comp_add,
    Preadditive.sub_comp, Preadditive.add_comp, ← Functor.map_comp]
  rw [splitFreeCechContractSext_face0 p sect hs,
    splitFreeCechContractSext_face1 p sect hs,
    splitFreeCechContractSext_face2 p sect hs,
    splitFreeCechContractSext_face3 p sect hs,
    splitFreeCechContractSext_face4 p sect hs,
    splitFreeCechContractSext_face5 p sect hs,
    (ModuleCat.free Coeff).map_id]

/-- Genuine split free Čech d5·d4 = 0, by 15 exact simplicial face pairs. -/
theorem splitFreeCechD5_comp_D4_zero (p : X → Y) :
    splitFreeCechD5 p ≫ splitFreeCechD4 p = 0 := by
  unfold splitFreeCechD5 splitFreeCechD4
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.comp_add, Preadditive.comp_sub, ← Functor.map_comp]
  have h01 :
      (↾(splitFreeCechSextFace0 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace0 p)) =
      (↾(splitFreeCechSextFace1 p)) ≫
        (↾(splitFreeCechQuintFace0 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h02 :
      (↾(splitFreeCechSextFace0 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace1 p)) =
      (↾(splitFreeCechSextFace2 p)) ≫
        (↾(splitFreeCechQuintFace0 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h03 :
      (↾(splitFreeCechSextFace0 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace2 p)) =
      (↾(splitFreeCechSextFace3 p)) ≫
        (↾(splitFreeCechQuintFace0 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h04 :
      (↾(splitFreeCechSextFace0 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace3 p)) =
      (↾(splitFreeCechSextFace4 p)) ≫
        (↾(splitFreeCechQuintFace0 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h05 :
      (↾(splitFreeCechSextFace0 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace4 p)) =
      (↾(splitFreeCechSextFace5 p)) ≫
        (↾(splitFreeCechQuintFace0 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h12 :
      (↾(splitFreeCechSextFace1 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace1 p)) =
      (↾(splitFreeCechSextFace2 p)) ≫
        (↾(splitFreeCechQuintFace1 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h13 :
      (↾(splitFreeCechSextFace1 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace2 p)) =
      (↾(splitFreeCechSextFace3 p)) ≫
        (↾(splitFreeCechQuintFace1 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h14 :
      (↾(splitFreeCechSextFace1 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace3 p)) =
      (↾(splitFreeCechSextFace4 p)) ≫
        (↾(splitFreeCechQuintFace1 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h15 :
      (↾(splitFreeCechSextFace1 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace4 p)) =
      (↾(splitFreeCechSextFace5 p)) ≫
        (↾(splitFreeCechQuintFace1 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h23 :
      (↾(splitFreeCechSextFace2 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace2 p)) =
      (↾(splitFreeCechSextFace3 p)) ≫
        (↾(splitFreeCechQuintFace2 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h24 :
      (↾(splitFreeCechSextFace2 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace3 p)) =
      (↾(splitFreeCechSextFace4 p)) ≫
        (↾(splitFreeCechQuintFace2 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h25 :
      (↾(splitFreeCechSextFace2 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace4 p)) =
      (↾(splitFreeCechSextFace5 p)) ≫
        (↾(splitFreeCechQuintFace2 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h34 :
      (↾(splitFreeCechSextFace3 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace3 p)) =
      (↾(splitFreeCechSextFace4 p)) ≫
        (↾(splitFreeCechQuintFace3 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h35 :
      (↾(splitFreeCechSextFace3 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace4 p)) =
      (↾(splitFreeCechSextFace5 p)) ≫
        (↾(splitFreeCechQuintFace3 p)) := by
    ext q
    apply Subtype.ext
    rfl
  have h45 :
      (↾(splitFreeCechSextFace4 p) :
        splitFreeCechSextuple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace4 p)) =
      (↾(splitFreeCechSextFace5 p)) ≫
        (↾(splitFreeCechQuintFace4 p)) := by
    ext q
    apply Subtype.ext
    rfl
  rw [h01, h02, h03, h04, h05, h12, h13, h14, h15, h23, h24, h25, h34, h35, h45]
  abel

noncomputable def splitFreeCechDegreeFourComplex (p : X → Y) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (splitFreeCechD5 p) (splitFreeCechD4 p)
    (splitFreeCechD5_comp_D4_zero p)

/-- Every split-set degree-four cycle is an actual sixfold boundary. -/
theorem splitFreeCechDegreeFour_exact
    (p : X → Y) (sect : Y → X) (hs : ∀ y, p (sect y) = y) :
    (splitFreeCechDegreeFourComplex p).Exact := by
  rw [ShortComplex.moduleCat_exact_iff]
  change ∀ (c : (ModuleCat.free Coeff).obj (splitFreeCechQuintuple p)),
    (splitFreeCechD4 p) c = 0 →
      ∃ z : (ModuleCat.free Coeff).obj (splitFreeCechSextuple p),
        (splitFreeCechD5 p) z = c
  intro c hc
  refine ⟨-(splitFreeCechH4 p sect hs c), ?_⟩
  have h := congrArg (fun f :
      (ModuleCat.free Coeff).obj (splitFreeCechQuintuple p) ⟶
      (ModuleCat.free Coeff).obj (splitFreeCechQuintuple p) => f c)
    (splitFreeCech_degreeFour_contraction p sect hs)
  have hh :
      (splitFreeCechD5 p) ((splitFreeCechH4 p sect hs) c) =
      (splitFreeCechH3 p sect hs) ((splitFreeCechD4 p) c) - c := by
    simpa only [ModuleCat.comp_apply, ModuleCat.hom_sub,
      LinearMap.sub_apply, ModuleCat.id_apply] using h
  change (splitFreeCechD5 p) (-(splitFreeCechH4 p sect hs c)) = c
  rw [map_neg, hh, hc, map_zero, zero_sub, neg_neg]

#print axioms splitFreeCechD5_comp_D4_zero
#print axioms splitFreeCechDegreeFour_exact

#print axioms splitFreeCech_degreeFour_contraction
end CMDG.CondensedCM5R0
