import CMDGCondensedCM4P3DerivedCM5R0CompHausCechPullbackComparison
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat
import Mathlib.CategoryTheory.Preadditive.AdditiveFunctor

/-!
# CM5 — algebraic degree-one contraction on a split set Čech presentation

For an arbitrary map p : X → Y with a chosen right inverse, the
free Coeff-module complex of its actual set-theoretic kernel
pairs and triples is exact in degree one. The argument constructs
a degree-zero and degree-one contraction and proves the exact
identity d₂ h₁ = h₀ d₁ - id at the level of genuine free-module
morphisms. The full degree-one exactness follows by a concrete
preimage for any d₁-cycle.

This theorem is for a split map of SETS; it does not claim a global
section of the profinite presentation, nor does it identify a
sheaf evaluation with an unsheafified free module. The protected
CompHaus-site pair/triple comparisons will be used to transport
this to each genuine Stonean-restricted presheaf evaluation.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

variable {X Y : Type (u + 1)}

/-- Actual compatible pairs for a map of sets. -/
def splitFreeCechPair (p : X → Y) : Type (u + 1) :=
  {xy : X × X // p xy.1 = p xy.2}

/-- Actual compatible triples with all three endpoints in
one p-fiber, represented by a right-associated triple. -/
def splitFreeCechTriple (p : X → Y) : Type (u + 1) :=
  {xyz : X × (X × X) //
    p xyz.1 = p xyz.2.1 ∧ p xyz.1 = p xyz.2.2}

def splitFreeCechPairFst (p : X → Y) :
    splitFreeCechPair p → X := fun xy => xy.1.1

def splitFreeCechPairSnd (p : X → Y) :
    splitFreeCechPair p → X := fun xy => xy.1.2

def splitFreeCechTripleXY (p : X → Y) :
    splitFreeCechTriple p → splitFreeCechPair p :=
  fun xyz => ⟨(xyz.1.1, xyz.1.2.1), xyz.2.1⟩

def splitFreeCechTripleXZ (p : X → Y) :
    splitFreeCechTriple p → splitFreeCechPair p :=
  fun xyz => ⟨(xyz.1.1, xyz.1.2.2), xyz.2.2⟩

def splitFreeCechTripleYZ (p : X → Y) :
    splitFreeCechTriple p → splitFreeCechPair p :=
  fun xyz => ⟨(xyz.1.2.1, xyz.1.2.2),
    (xyz.2.1).symm.trans xyz.2.2⟩

/-- The authentic degree-one difference [x,y] ↦ [x]-[y]. -/
noncomputable def splitFreeCechD1 (p : X → Y) :
    (ModuleCat.free Coeff).obj (splitFreeCechPair p) ⟶
      (ModuleCat.free Coeff).obj X :=
  (ModuleCat.free Coeff).map (↾(splitFreeCechPairFst p)) -
    (ModuleCat.free Coeff).map (↾(splitFreeCechPairSnd p))

/-- The sign-correct degree-two differential
[x,y,z] ↦ [x,z]-[x,y]-[y,z]. -/
noncomputable def splitFreeCechD2 (p : X → Y) :
    (ModuleCat.free Coeff).obj (splitFreeCechTriple p) ⟶
      (ModuleCat.free Coeff).obj (splitFreeCechPair p) :=
  (ModuleCat.free Coeff).map (↾(splitFreeCechTripleXZ p)) -
    (ModuleCat.free Coeff).map (↾(splitFreeCechTripleXY p)) -
    (ModuleCat.free Coeff).map (↾(splitFreeCechTripleYZ p))

/-- The *actual* split Čech free-module differentials compose to zero. -/
theorem splitFreeCechD2_comp_D1_zero (p : X → Y) :
    splitFreeCechD2 p ≫ splitFreeCechD1 p = 0 := by
  have hxf :
      (↾(splitFreeCechTripleXZ p) :
        splitFreeCechTriple p ⟶ splitFreeCechPair p) ≫
        (↾(splitFreeCechPairFst p)) =
      (↾(splitFreeCechTripleXY p)) ≫
        (↾(splitFreeCechPairFst p)) := by
    ext xyz; rfl
  have hys :
      (↾(splitFreeCechTripleYZ p) :
        splitFreeCechTriple p ⟶ splitFreeCechPair p) ≫
        (↾(splitFreeCechPairSnd p)) =
      (↾(splitFreeCechTripleXZ p)) ≫
        (↾(splitFreeCechPairSnd p)) := by
    ext xyz; rfl
  have hmid :
      (↾(splitFreeCechTripleXY p) :
        splitFreeCechTriple p ⟶ splitFreeCechPair p) ≫
        (↾(splitFreeCechPairSnd p)) =
      (↾(splitFreeCechTripleYZ p)) ≫
        (↾(splitFreeCechPairFst p)) := by
    ext xyz; rfl
  unfold splitFreeCechD2 splitFreeCechD1
  simp only [Preadditive.sub_comp, Preadditive.comp_sub,
    ← Functor.map_comp]
  rw [hxf, ← hys, hmid]
  abel

/-- Section-based pair contraction [x] ↦ [x,s(px)]. -/
def splitFreeCechContractPair
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y)
    (x : X) : splitFreeCechPair p :=
  ⟨(x, s (p x)), (hs (p x)).symm⟩

/-- Section-based triple contraction [x,y] ↦ [x,y,s(px)]. -/
def splitFreeCechContractTriple
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y)
    (xy : splitFreeCechPair p) : splitFreeCechTriple p :=
  ⟨(xy.1.1, (xy.1.2, s (p xy.1.1))),
    ⟨xy.2, (hs (p xy.1.1)).symm⟩⟩

noncomputable def splitFreeCechH0
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y) :
    (ModuleCat.free Coeff).obj X ⟶
      (ModuleCat.free Coeff).obj (splitFreeCechPair p) :=
  (ModuleCat.free Coeff).map (↾(splitFreeCechContractPair p s hs))

noncomputable def splitFreeCechH1
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y) :
    (ModuleCat.free Coeff).obj (splitFreeCechPair p) ⟶
      (ModuleCat.free Coeff).obj (splitFreeCechTriple p) :=
  (ModuleCat.free Coeff).map (↾(splitFreeCechContractTriple p s hs))

/-- The actual degree-one contraction identity, with signs fixed to
the existing CM5 differential: h₁ ≫ d₂ = d₁ ≫ h₀ - id. -/
theorem splitFreeCech_contraction
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y) :
    splitFreeCechH1 p s hs ≫ splitFreeCechD2 p =
      splitFreeCechD1 p ≫ splitFreeCechH0 p s hs - 𝟙 _ := by
  have hxz :
      (↾(splitFreeCechContractTriple p s hs) :
        splitFreeCechPair p ⟶ splitFreeCechTriple p) ≫
        (↾(splitFreeCechTripleXZ p)) =
      (↾(splitFreeCechPairFst p)) ≫
        (↾(splitFreeCechContractPair p s hs)) := by
    ext xy; rfl
  have hxy :
      (↾(splitFreeCechContractTriple p s hs) :
        splitFreeCechPair p ⟶ splitFreeCechTriple p) ≫
        (↾(splitFreeCechTripleXY p)) =
      𝟙 (splitFreeCechPair p) := by
    ext xy; rfl
  have hyz :
      (↾(splitFreeCechContractTriple p s hs) :
        splitFreeCechPair p ⟶ splitFreeCechTriple p) ≫
        (↾(splitFreeCechTripleYZ p)) =
      (↾(splitFreeCechPairSnd p)) ≫
        (↾(splitFreeCechContractPair p s hs)) := by
    ext xy
    apply Subtype.ext
    apply Prod.ext
    · rfl
    · exact congrArg s xy.2
  unfold splitFreeCechH1 splitFreeCechD2
    splitFreeCechD1 splitFreeCechH0
  simp only [Preadditive.comp_sub, Preadditive.sub_comp,
    ← Functor.map_comp]
  rw [hxz, hxy, hyz, (ModuleCat.free Coeff).map_id]
  abel

/-- The actual split-Čech two-step complex. -/
noncomputable def splitFreeCechDegreeOneComplex (p : X → Y) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (splitFreeCechD2 p) (splitFreeCechD1 p)
    (splitFreeCechD2_comp_D1_zero p)

/-- A split set presentation has a degree-one exact free-module
Čech complex: explicit preimage of any d₁-cycle is -h₁(c). -/
theorem splitFreeCechDegreeOne_exact
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y) :
    (splitFreeCechDegreeOneComplex p).Exact := by
  rw [ShortComplex.moduleCat_exact_iff]
  change ∀ (c : (ModuleCat.free Coeff).obj (splitFreeCechPair p)),
    (splitFreeCechD1 p) c = 0 →
      ∃ z : (ModuleCat.free Coeff).obj (splitFreeCechTriple p),
        (splitFreeCechD2 p) z = c
  intro c hc
  refine ⟨-(splitFreeCechH1 p s hs c), ?_⟩
  have hcon := congrArg
    (fun f : (ModuleCat.free Coeff).obj (splitFreeCechPair p) ⟶
      (ModuleCat.free Coeff).obj (splitFreeCechPair p) => f c)
    (splitFreeCech_contraction p s hs)
  have hcalc :
      (splitFreeCechD2 p) ((splitFreeCechH1 p s hs) c) =
        (splitFreeCechH0 p s hs) ((splitFreeCechD1 p) c) - c := by
    simpa only [ModuleCat.comp_apply, ModuleCat.hom_sub,
      LinearMap.sub_apply, ModuleCat.id_apply] using hcon
  change (splitFreeCechD2 p) (-(splitFreeCechH1 p s hs c)) = c
  rw [map_neg, hcalc, hc, map_zero]
  abel

#print axioms splitFreeCechD2_comp_D1_zero
#print axioms splitFreeCech_contraction
#print axioms splitFreeCechDegreeOne_exact

end CMDG.CondensedCM5R0
