import CMDGCondensedCM4P3DerivedCM5R0GenuineFifthCechBoundary
import CMDGCondensedCM4P3DerivedCM5R0SplitFreeCechDegreeTwo
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat

/-!
# CM5: genuine set-level split fivefold Čech degree-three contraction

For any split set map p:X→Y, build the compatible five-vertex
set and full signed free-module d4. Prove the section-appending
contracting homotopy. This does not establish its transfer to
the actual condensed-module sheaf until probe and sheafification
comparisons are proved.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0
variable {X Y : Type (u + 1)}

def splitFreeCechQuintuple (p : X → Y) : Type (u + 1) :=
  {q : X × (X × (X × (X × X))) //
    p q.1 = p q.2.1 ∧
    p q.1 = p q.2.2.1 ∧
    p q.1 = p q.2.2.2.1 ∧
    p q.1 = p q.2.2.2.2}

def splitFreeCechQuintFace0 (p : X → Y) :
    splitFreeCechQuintuple p → splitFreeCechQuadruple p := by
  intro q
  exact ⟨(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,q.val.2.2.2.2))),
    ⟨q.property.1.symm.trans q.property.2.1,
     q.property.1.symm.trans q.property.2.2.1,
     q.property.1.symm.trans q.property.2.2.2⟩⟩

def splitFreeCechQuintFace1 (p : X → Y) :
    splitFreeCechQuintuple p → splitFreeCechQuadruple p :=
  fun q => ⟨(q.val.1,(q.val.2.2.1,(q.val.2.2.2.1,q.val.2.2.2.2))),
    ⟨q.property.2.1,q.property.2.2.1,q.property.2.2.2⟩⟩

def splitFreeCechQuintFace2 (p : X → Y) :
    splitFreeCechQuintuple p → splitFreeCechQuadruple p :=
  fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.2.1,q.val.2.2.2.2))),
    ⟨q.property.1,q.property.2.2.1,q.property.2.2.2⟩⟩

def splitFreeCechQuintFace3 (p : X → Y) :
    splitFreeCechQuintuple p → splitFreeCechQuadruple p :=
  fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,q.val.2.2.2.2))),
    ⟨q.property.1,q.property.2.1,q.property.2.2.2⟩⟩

def splitFreeCechQuintFace4 (p : X → Y) :
    splitFreeCechQuintuple p → splitFreeCechQuadruple p :=
  fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,q.val.2.2.2.1))),
    ⟨q.property.1,q.property.2.1,q.property.2.2.1⟩⟩

noncomputable def splitFreeCechD4 (p : X → Y) :
    (ModuleCat.free Coeff).obj (splitFreeCechQuintuple p) ⟶
    (ModuleCat.free Coeff).obj (splitFreeCechQuadruple p) :=
  (ModuleCat.free Coeff).map (↾(splitFreeCechQuintFace0 p)) -
  (ModuleCat.free Coeff).map (↾(splitFreeCechQuintFace1 p)) +
  (ModuleCat.free Coeff).map (↾(splitFreeCechQuintFace2 p)) -
  (ModuleCat.free Coeff).map (↾(splitFreeCechQuintFace3 p)) +
  (ModuleCat.free Coeff).map (↾(splitFreeCechQuintFace4 p))

/-- Appending a chosen section at the fifth vertex of a quadruple. -/
def splitFreeCechContractQuint
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y)
    (q : splitFreeCechQuadruple p) : splitFreeCechQuintuple p :=
  ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,
      (q.val.2.2.2,s (p q.val.1))))),
    ⟨q.property.1,q.property.2.1,q.property.2.2,
      (hs (p q.val.1)).symm⟩⟩

noncomputable def splitFreeCechH3
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y) :
    (ModuleCat.free Coeff).obj (splitFreeCechQuadruple p) ⟶
    (ModuleCat.free Coeff).obj (splitFreeCechQuintuple p) :=
  (ModuleCat.free Coeff).map (↾(splitFreeCechContractQuint p s hs))


/-- The fifth-face contracting identity for every split set map.
Positive last face makes H3≫D4 = D3≫H2 + id. -/
theorem splitFreeCech_degreeThree_contraction
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y) :
    splitFreeCechH3 p s hs ≫ splitFreeCechD4 p =
      splitFreeCechD3 p ≫ splitFreeCechH2 p s hs + 𝟙 _ := by
  have h0 :
      (↾(splitFreeCechContractQuint p s hs) :
        splitFreeCechQuadruple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace0 p)) =
      (↾(splitFreeCechQuadYZW p)) ≫
        (↾(splitFreeCechContractQuad p s hs)) := by
    ext q
    apply Subtype.ext
    apply Prod.ext
    · rfl
    · apply Prod.ext
      · rfl
      · apply Prod.ext
        · rfl
        · exact congrArg s q.property.1
  have h1 :
      (↾(splitFreeCechContractQuint p s hs) :
        splitFreeCechQuadruple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace1 p)) =
      (↾(splitFreeCechQuadXZW p)) ≫
        (↾(splitFreeCechContractQuad p s hs)) := by
    ext q; apply Subtype.ext; rfl
  have h2 :
      (↾(splitFreeCechContractQuint p s hs) :
        splitFreeCechQuadruple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace2 p)) =
      (↾(splitFreeCechQuadXYW p)) ≫
        (↾(splitFreeCechContractQuad p s hs)) := by
    ext q; apply Subtype.ext; rfl
  have h3 :
      (↾(splitFreeCechContractQuint p s hs) :
        splitFreeCechQuadruple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace3 p)) =
      (↾(splitFreeCechQuadXYZ p)) ≫
        (↾(splitFreeCechContractQuad p s hs)) := by
    ext q; apply Subtype.ext; rfl
  have h4 :
      (↾(splitFreeCechContractQuint p s hs) :
        splitFreeCechQuadruple p ⟶ splitFreeCechQuintuple p) ≫
        (↾(splitFreeCechQuintFace4 p)) =
          𝟙 (splitFreeCechQuadruple p) := by
    ext q; apply Subtype.ext; rfl
  unfold splitFreeCechH3 splitFreeCechD4
    splitFreeCechD3 splitFreeCechH2
  simp only [Preadditive.comp_sub, Preadditive.comp_add,
    Preadditive.sub_comp, Preadditive.add_comp, ← Functor.map_comp]
  rw [h0,h1,h2,h3,h4,(ModuleCat.free Coeff).map_id]


/-- Signed fivefold/signed fourfold boundary is a chain complex,
on the actual free modules over compatible split-set simplices. -/
theorem splitFreeCechD4_comp_D3_zero (p : X → Y) :
    splitFreeCechD4 p ≫ splitFreeCechD3 p = 0 := by
  unfold splitFreeCechD4 splitFreeCechD3
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.comp_add, Preadditive.comp_sub, ← Functor.map_comp]
  have h01 :
      (↾(splitFreeCechQuintFace0 p) :
        splitFreeCechQuintuple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadYZW p)) =
      (↾(splitFreeCechQuintFace1 p)) ≫
        (↾(splitFreeCechQuadYZW p)) := by
    ext q; apply Subtype.ext; rfl
  have h02 :
      (↾(splitFreeCechQuintFace0 p) :
        splitFreeCechQuintuple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXZW p)) =
      (↾(splitFreeCechQuintFace2 p)) ≫
        (↾(splitFreeCechQuadYZW p)) := by
    ext q; apply Subtype.ext; rfl
  have h03 :
      (↾(splitFreeCechQuintFace0 p) :
        splitFreeCechQuintuple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXYW p)) =
      (↾(splitFreeCechQuintFace3 p)) ≫
        (↾(splitFreeCechQuadYZW p)) := by
    ext q; apply Subtype.ext; rfl
  have h04 :
      (↾(splitFreeCechQuintFace0 p) :
        splitFreeCechQuintuple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXYZ p)) =
      (↾(splitFreeCechQuintFace4 p)) ≫
        (↾(splitFreeCechQuadYZW p)) := by
    ext q; apply Subtype.ext; rfl
  have h12 :
      (↾(splitFreeCechQuintFace1 p) :
        splitFreeCechQuintuple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXZW p)) =
      (↾(splitFreeCechQuintFace2 p)) ≫
        (↾(splitFreeCechQuadXZW p)) := by
    ext q; apply Subtype.ext; rfl
  have h13 :
      (↾(splitFreeCechQuintFace1 p) :
        splitFreeCechQuintuple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXYW p)) =
      (↾(splitFreeCechQuintFace3 p)) ≫
        (↾(splitFreeCechQuadXZW p)) := by
    ext q; apply Subtype.ext; rfl
  have h14 :
      (↾(splitFreeCechQuintFace1 p) :
        splitFreeCechQuintuple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXYZ p)) =
      (↾(splitFreeCechQuintFace4 p)) ≫
        (↾(splitFreeCechQuadXZW p)) := by
    ext q; apply Subtype.ext; rfl
  have h23 :
      (↾(splitFreeCechQuintFace2 p) :
        splitFreeCechQuintuple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXYW p)) =
      (↾(splitFreeCechQuintFace3 p)) ≫
        (↾(splitFreeCechQuadXYW p)) := by
    ext q; apply Subtype.ext; rfl
  have h24 :
      (↾(splitFreeCechQuintFace2 p) :
        splitFreeCechQuintuple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXYZ p)) =
      (↾(splitFreeCechQuintFace4 p)) ≫
        (↾(splitFreeCechQuadXYW p)) := by
    ext q; apply Subtype.ext; rfl
  have h34 :
      (↾(splitFreeCechQuintFace3 p) :
        splitFreeCechQuintuple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXYZ p)) =
      (↾(splitFreeCechQuintFace4 p)) ≫
        (↾(splitFreeCechQuadXYZ p)) := by
    ext q; apply Subtype.ext; rfl
  rw [h01, h02, h03, h04, h12, h13, h14, h23, h24, h34]
  abel


noncomputable def splitFreeCechDegreeThreeComplex (p : X → Y) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (splitFreeCechD4 p) (splitFreeCechD3 p)
    (splitFreeCechD4_comp_D3_zero p)

/-- Degree-three exactness for every split presentation of sets,
with a concrete section-appending witness for every cycle. -/
theorem splitFreeCechDegreeThree_exact
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y) :
    (splitFreeCechDegreeThreeComplex p).Exact := by
  rw [ShortComplex.moduleCat_exact_iff]
  change ∀ (c : (ModuleCat.free Coeff).obj (splitFreeCechQuadruple p)),
    (splitFreeCechD3 p) c = 0 →
      ∃ z : (ModuleCat.free Coeff).obj (splitFreeCechQuintuple p),
      (splitFreeCechD4 p) z = c
  intro c hc
  refine ⟨(splitFreeCechH3 p s hs) c, ?_⟩
  have h := congrArg (fun f :
      (ModuleCat.free Coeff).obj (splitFreeCechQuadruple p) ⟶
      (ModuleCat.free Coeff).obj (splitFreeCechQuadruple p) => f c)
    (splitFreeCech_degreeThree_contraction p s hs)
  have hh :
      (splitFreeCechD4 p) ((splitFreeCechH3 p s hs) c) =
      (splitFreeCechH2 p s hs) ((splitFreeCechD3 p) c) + c := by
    simpa only [ModuleCat.comp_apply, ModuleCat.hom_add,
      LinearMap.add_apply, ModuleCat.id_apply] using h
  change (splitFreeCechD4 p) ((splitFreeCechH3 p s hs) c) = c
  rw [hh, hc, map_zero, zero_add]

#print axioms splitFreeCechDegreeThree_exact
#print axioms splitFreeCechD4_comp_D3_zero

#print axioms splitFreeCech_degreeThree_contraction
#print axioms splitFreeCechD4
#print axioms splitFreeCechH3
end CMDG.CondensedCM5R0
