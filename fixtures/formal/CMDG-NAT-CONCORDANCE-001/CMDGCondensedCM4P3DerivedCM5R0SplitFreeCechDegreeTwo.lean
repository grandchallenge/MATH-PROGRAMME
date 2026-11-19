import CMDGCondensedCM4P3DerivedCM5R0SplitFreeCechDegreeOne
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat

/-!
# CMDG CM5 — exact split-set free Čech complex in degree two

For any map of sets p:X→Y with specified section s:Y→X, define the
actual compatible quadruple set and its four face maps to triples.
Define the free Coeff-module alternating fourth boundary d₃ with
the same orientation as the genuine categorical fourfold boundary
and prove d₃≫d₂=0.

Construct the explicit section-based contraction by appending
s(p(x)) to each compatible triple. The resulting identity is
h₂≫d₃ = -(d₂≫h₁) - id in the pinned chain sign convention.
For any c with d₂(c)=0, the element -h₂(c) has d₃-boundary c.
Therefore the split-set Čech complex is exact at the triple term.

This theorem holds for all split maps of sets, not just finite maps.
It DOES NOT assert global splitness of arbitrary profinite T,
identify probe evaluation with un-sheafified free modules, prove
global fourth-to-third relation epimorphism, or establish Ext³
vanishing. Those transports remain independent obligations.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0
variable {X Y : Type (u + 1)}

/-- Actual compatible quadruples for a set presentation. -/
def splitFreeCechQuadruple (p : X → Y) : Type (u + 1) :=
  {xyzw : X × (X × (X × X)) //
    p xyzw.1 = p xyzw.2.1 ∧
    p xyzw.1 = p xyzw.2.2.1 ∧
    p xyzw.1 = p xyzw.2.2.2}

/-- The four face projections from compatible quadruples to triples. -/
def splitFreeCechQuadYZW (p : X → Y) :
    splitFreeCechQuadruple p → splitFreeCechTriple p := by
  intro t
  refine ⟨(t.val.2.1, (t.val.2.2.1, t.val.2.2.2)), ?_⟩
  exact ⟨t.property.1.symm.trans t.property.2.1,
    t.property.1.symm.trans t.property.2.2⟩

def splitFreeCechQuadXZW (p : X → Y) :
    splitFreeCechQuadruple p → splitFreeCechTriple p :=
  fun t => ⟨(t.val.1, (t.val.2.2.1, t.val.2.2.2)),
    ⟨t.property.2.1, t.property.2.2⟩⟩

def splitFreeCechQuadXYW (p : X → Y) :
    splitFreeCechQuadruple p → splitFreeCechTriple p :=
  fun t => ⟨(t.val.1, (t.val.2.1, t.val.2.2.2)),
    ⟨t.property.1, t.property.2.2⟩⟩

def splitFreeCechQuadXYZ (p : X → Y) :
    splitFreeCechQuadruple p → splitFreeCechTriple p :=
  fun t => ⟨(t.val.1, (t.val.2.1, t.val.2.2.1)),
    ⟨t.property.1, t.property.2.1⟩⟩

/-- The genuine free-module fourth differential on a split set map. -/
noncomputable def splitFreeCechD3 (p : X → Y) :
    (ModuleCat.free Coeff).obj (splitFreeCechQuadruple p) ⟶
    (ModuleCat.free Coeff).obj (splitFreeCechTriple p) :=
  (ModuleCat.free Coeff).map (↾(splitFreeCechQuadYZW p)) -
    (ModuleCat.free Coeff).map (↾(splitFreeCechQuadXZW p)) +
    (ModuleCat.free Coeff).map (↾(splitFreeCechQuadXYW p)) -
    (ModuleCat.free Coeff).map (↾(splitFreeCechQuadXYZ p))

/-- Appending the chosen presentation section gives a quadruple. -/
def splitFreeCechContractQuad
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y)
    (t : splitFreeCechTriple p) : splitFreeCechQuadruple p :=
  ⟨(t.val.1, (t.val.2.1, (t.val.2.2, s (p t.val.1)))),
    ⟨t.property.1, t.property.2, (hs (p t.val.1)).symm⟩⟩

noncomputable def splitFreeCechH2
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y) :
    (ModuleCat.free Coeff).obj (splitFreeCechTriple p) ⟶
    (ModuleCat.free Coeff).obj (splitFreeCechQuadruple p) :=
  (ModuleCat.free Coeff).map (↾(splitFreeCechContractQuad p s hs))

/-- Fourfold/threefold signed boundary compatibility. -/
theorem splitFreeCechD3_comp_D2_zero (p : X → Y) :
    splitFreeCechD3 p ≫ splitFreeCechD2 p = 0 := by
  unfold splitFreeCechD3 splitFreeCechD2
  simp only [Preadditive.sub_comp, Preadditive.add_comp,
    Preadditive.comp_sub, ← Functor.map_comp]
  -- Equalities of all repeated faces are definitional modulo subtype proof irrelevance.
  have h₁ :
    (↾(splitFreeCechQuadYZW p) : splitFreeCechQuadruple p ⟶ splitFreeCechTriple p) ≫
      (↾(splitFreeCechTripleXZ p)) =
    (↾(splitFreeCechQuadXYW p)) ≫
      (↾(splitFreeCechTripleYZ p)) := by
    ext t; apply Subtype.ext; rfl
  have h₂ :
    (↾(splitFreeCechQuadYZW p) : splitFreeCechQuadruple p ⟶ splitFreeCechTriple p) ≫
      (↾(splitFreeCechTripleXY p)) =
    (↾(splitFreeCechQuadXYZ p)) ≫
      (↾(splitFreeCechTripleYZ p)) := by
    ext t; apply Subtype.ext; rfl
  have h₃ :
    (↾(splitFreeCechQuadXZW p) : splitFreeCechQuadruple p ⟶ splitFreeCechTriple p) ≫
      (↾(splitFreeCechTripleXY p)) =
    (↾(splitFreeCechQuadXYZ p)) ≫
      (↾(splitFreeCechTripleXZ p)) := by
    ext t; apply Subtype.ext; rfl
  have h₄ :
    (↾(splitFreeCechQuadXYW p) : splitFreeCechQuadruple p ⟶ splitFreeCechTriple p) ≫
      (↾(splitFreeCechTripleXY p)) =
    (↾(splitFreeCechQuadXYZ p)) ≫
      (↾(splitFreeCechTripleXY p)) := by
    ext t; apply Subtype.ext; rfl
  have h₅ :
    (↾(splitFreeCechQuadYZW p) : splitFreeCechQuadruple p ⟶ splitFreeCechTriple p) ≫
      (↾(splitFreeCechTripleYZ p)) =
    (↾(splitFreeCechQuadXZW p)) ≫
      (↾(splitFreeCechTripleYZ p)) := by
    ext t; apply Subtype.ext; rfl
  have h₆ :
    (↾(splitFreeCechQuadXYW p) : splitFreeCechQuadruple p ⟶ splitFreeCechTriple p) ≫
      (↾(splitFreeCechTripleXZ p)) =
    (↾(splitFreeCechQuadXZW p)) ≫
      (↾(splitFreeCechTripleXZ p)) := by
    ext t; apply Subtype.ext; rfl
  rw [h₁, h₂, h₃, h₄, h₅, h₆]
  abel


/-- The fourth-face contraction on compatible triples is exact,
with the chosen sign convention d₂=[xz]-[xy]-[yz]. -/
theorem splitFreeCech_degreeTwo_contraction
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y) :
    splitFreeCechH2 p s hs ≫ splitFreeCechD3 p =
      -(splitFreeCechD2 p ≫ splitFreeCechH1 p s hs) -
      𝟙 _ := by
  have hyzw :
      (↾(splitFreeCechContractQuad p s hs) :
        splitFreeCechTriple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadYZW p)) =
      (↾(splitFreeCechTripleYZ p)) ≫
        (↾(splitFreeCechContractTriple p s hs)) := by
    ext t
    apply Subtype.ext
    apply Prod.ext
    · rfl
    · apply Prod.ext
      · rfl
      · exact congrArg s t.property.1
  have hxzw :
      (↾(splitFreeCechContractQuad p s hs) :
        splitFreeCechTriple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXZW p)) =
      (↾(splitFreeCechTripleXZ p)) ≫
        (↾(splitFreeCechContractTriple p s hs)) := by
    ext t
    apply Subtype.ext
    rfl
  have hxyw :
      (↾(splitFreeCechContractQuad p s hs) :
        splitFreeCechTriple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXYW p)) =
      (↾(splitFreeCechTripleXY p)) ≫
        (↾(splitFreeCechContractTriple p s hs)) := by
    ext t
    apply Subtype.ext
    rfl
  have hxyz :
      (↾(splitFreeCechContractQuad p s hs) :
        splitFreeCechTriple p ⟶ splitFreeCechQuadruple p) ≫
        (↾(splitFreeCechQuadXYZ p)) =
      𝟙 (splitFreeCechTriple p) := by
    ext t
    apply Subtype.ext
    rfl
  unfold splitFreeCechH2 splitFreeCechD3
    splitFreeCechD2 splitFreeCechH1
  simp only [Preadditive.comp_sub, Preadditive.comp_add,
    Preadditive.sub_comp, ← Functor.map_comp]
  rw [hyzw, hxzw, hxyw, hxyz,
    (ModuleCat.free Coeff).map_id]
  abel

/-- Two-step split Čech complex at the triple term. -/
noncomputable def splitFreeCechDegreeTwoComplex (p : X → Y) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (splitFreeCechD3 p) (splitFreeCechD2 p)
    (splitFreeCechD3_comp_D2_zero p)

/-- Split presentations are exact in degree two, not only degree one. -/
theorem splitFreeCechDegreeTwo_exact
    (p : X → Y) (s : Y → X) (hs : ∀ y, p (s y) = y) :
    (splitFreeCechDegreeTwoComplex p).Exact := by
  rw [ShortComplex.moduleCat_exact_iff]
  change ∀ (c : (ModuleCat.free Coeff).obj (splitFreeCechTriple p)),
    (splitFreeCechD2 p) c = 0 →
      ∃ z : (ModuleCat.free Coeff).obj (splitFreeCechQuadruple p),
        (splitFreeCechD3 p) z = c
  intro c hc
  refine ⟨-(splitFreeCechH2 p s hs c), ?_⟩
  have hcon := congrArg
    (fun f : (ModuleCat.free Coeff).obj (splitFreeCechTriple p) ⟶
      (ModuleCat.free Coeff).obj (splitFreeCechTriple p) => f c)
    (splitFreeCech_degreeTwo_contraction p s hs)
  have hcalc :
      (splitFreeCechD3 p) ((splitFreeCechH2 p s hs) c) =
        -((splitFreeCechH1 p s hs) ((splitFreeCechD2 p) c)) - c := by
    simpa only [ModuleCat.comp_apply, ModuleCat.hom_sub,
      ModuleCat.hom_neg, LinearMap.sub_apply, LinearMap.neg_apply,
      ModuleCat.id_apply] using hcon
  change (splitFreeCechD3 p) (-(splitFreeCechH2 p s hs c)) = c
  rw [map_neg, hcalc, hc, map_zero]
  abel

#print axioms splitFreeCechD3_comp_D2_zero
#print axioms splitFreeCech_degreeTwo_contraction
#print axioms splitFreeCechDegreeTwo_exact

end CMDG.CondensedCM5R0
