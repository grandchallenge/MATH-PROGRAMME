import CMDGCondensedCM4P3DerivedCM5R0UniformSplitCechBarExact

set_option backward.isDefEq.respectTransparency false
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

def splitCechBaseProjection (A B : Type (u + 1)) (p : A → B) :
    splitCechTuple A B p 0 → B :=
  fun x => p (x.val 0)

def splitCechBaseSection (A B : Type (u + 1)) (p : A → B)
    (s : B → A) : B → splitCechTuple A B p 0 :=
  fun b => ⟨(fun _ : Fin 1 => s b), by
    intro i
    rfl⟩

def splitBarBaseMap (A B : Type (u + 1)) (p : A → B) :
    (ModuleCat.free Coeff).obj (splitCechTuple A B p 0) ⟶
      (ModuleCat.free Coeff).obj B :=
  (ModuleCat.free Coeff).map (↾splitCechBaseProjection A B p)

def splitBarBaseSection (A B : Type (u + 1)) (p : A → B)
    (s : B → A) :
    (ModuleCat.free Coeff).obj B ⟶
      (ModuleCat.free Coeff).obj (splitCechTuple A B p 0) :=
  (ModuleCat.free Coeff).map (↾splitCechBaseSection A B p s)

theorem splitBarZeroBoundary_comp_augmentation
    (A B : Type (u + 1)) (p : A → B) :
    splitBarD A B p 0 ≫ splitBarBaseMap A B p = 0 := by
  unfold splitBarD splitBarBaseMap
  rw [Fin.sum_univ_two]
  simp only [Fin.val_zero, pow_zero, one_smul, Fin.val_one,
    pow_one, neg_smul, sub_eq_add_neg]
  rw [← sub_eq_add_neg, Preadditive.sub_comp]
  simp only [← Functor.map_comp]
  have h : (↾splitCechFace A B p 0 (0 : Fin 2)) ≫
        (↾splitCechBaseProjection A B p) =
      (↾splitCechFace A B p 0 (1 : Fin 2)) ≫
        (↾splitCechBaseProjection A B p) := by
    apply CategoryTheory.ConcreteCategory.hom_ext
    intro x
    change p (x.val 1) = p (x.val 0)
    exact x.property 1
  rw [h]
  exact sub_self _

theorem splitBarZeroContraction (A B : Type (u + 1))
    (p : A → B) (s : B → A) (hs : ∀ b, p (s b) = b) :
    splitBarH A B p s hs 0 ≫ splitBarD A B p 0 +
      splitBarBaseMap A B p ≫ splitBarBaseSection A B p s =
      𝟙 ((ModuleCat.free Coeff).obj (splitCechTuple A B p 0)) := by
  unfold splitBarH splitBarD splitBarBaseMap splitBarBaseSection
  rw [Fin.sum_univ_two]
  simp only [Fin.val_zero, pow_zero, one_smul, Fin.val_one,
    pow_one, neg_smul, ← sub_eq_add_neg,
    Preadditive.comp_sub, ← Functor.map_comp]
  have heq : (↾splitCechExtra A B p s hs 0) ≫
      (↾splitCechFace A B p 0 (0 : Fin 2)) =
      𝟙 (splitCechTuple A B p 0) := by
    ext x
    exact splitCechFace_zero_extra A B p s hs 0 x
  rw [heq]
  have hlast :
      (↾splitCechExtra A B p s hs 0) ≫
        (↾splitCechFace A B p 0 (1 : Fin 2)) =
      (↾splitCechBaseProjection A B p) ≫
        (↾splitCechBaseSection A B p s) := by
    ext x
    apply Subtype.ext
    funext i
    fin_cases i
    rfl
  rw [hlast]
  have hid : (ModuleCat.free Coeff).map (𝟙 (splitCechTuple A B p 0)) =
      𝟙 ((ModuleCat.free Coeff).obj (splitCechTuple A B p 0)) :=
    (ModuleCat.free Coeff).map_id _
  rw [hid]
  abel

def splitBarZeroShortComplex (A B : Type (u + 1))
    (p : A → B) : ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (splitBarD A B p 0) (splitBarBaseMap A B p)
    (splitBarZeroBoundary_comp_augmentation A B p)

theorem splitBarZeroShortExact (A B : Type (u + 1))
    (p : A → B) (s : B → A) (hs : ∀ b, p (s b) = b) :
    (splitBarZeroShortComplex A B p).Exact := by
  apply shortComplex_exact_of_middle_homotopy
    (splitBarZeroShortComplex A B p)
    (splitBarH A B p s hs 0)
    (splitBarBaseSection A B p s)
  exact splitBarZeroContraction A B p s hs

#print axioms splitBarZeroShortExact
end CMDG.CondensedCM5R0
