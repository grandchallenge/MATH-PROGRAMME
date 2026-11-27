import CMDGCondensedCM4P3DerivedCM5R0CompactCoverGeometry

/-! Finite-coordinate observations for genuine products of compact
relations. This is the topological continuity input, not a claim
that ordinary sheaf cohomology agrees with condensed Ext. -/
noncomputable section
universe u v w a
open Set CategoryTheory
namespace CMDG.CondensedCM5R0.CompactCover

section FiniteCoordinates

variable {I : Type u} {X : I → Type v}
  [∀ i, TopologicalSpace (X i)] [∀ i, CompactSpace (X i)]
  {A : Type w}

/-- A locally constant function on an arbitrary compact product
has one finite coordinate set controlling its entire value. -/
theorem finiteCoordinateSupport (f : LocallyConstant (∀ i, X i) A) :
    ∃ F : Finset I, ∀ x y : ∀ i, X i,
      (∀ i ∈ F, x i = y i) → f x = f y := by
  classical
  have hlocal (x : ∀ i, X i) :
      ∃ F : Finset I, ∃ U : ∀ i, Set (X i),
        (∀ i, i ∈ F → IsOpen (U i) ∧ x i ∈ U i) ∧
        (F : Set I).pi U ⊆ {y | f y = f x} := by
    apply (isOpen_pi_iff.mp (f.isLocallyConstant.isOpen_fiber (f x))) x
    rfl
  choose F U hU hsub using hlocal
  let V (x : ∀ i, X i) := (F x : Set I).pi (U x)
  have ho (x : ∀ i, X i) : IsOpen (V x) :=
    isOpen_set_pi (F x).finite_toSet (fun i hi => (hU x i hi).1)
  have hcover : (Set.univ : Set (∀ i, X i)) ⊆ ⋃ x, V x := by
    intro x _
    apply Set.mem_iUnion.mpr
    exact ⟨x, fun i hi => (hU x i hi).2⟩
  obtain ⟨s,hs⟩ := isCompact_univ.elim_finite_subcover V ho hcover
  refine ⟨s.biUnion F, ?_⟩
  intro x y hxy
  have hx : x ∈ ⋃ z ∈ s, V z := hs (Set.mem_univ x)
  simp only [Set.mem_iUnion] at hx
  obtain ⟨z,hzs,hxz⟩ := hx
  have hyz : y ∈ V z := by
    intro i hi
    have hi' : i ∈ s.biUnion F := Finset.mem_biUnion.mpr ⟨z,hzs,hi⟩
    rw [← hxy i hi']
    exact hxz i hi
  exact (hsub z hxz).trans (hsub z hyz).symm

def restrictCoordinates (F : Finset I) : C((∀ i, X i), (∀ i : ↥F, X i.val)) :=
  ⟨fun x i => x i.val, continuous_pi fun i => continuous_apply i.val⟩

def extendCoordinates (F : Finset I) (x₀ : ∀ i, X i) :
    C((∀ i : ↥F, X i.val), (∀ i, X i)) := by
  classical
  refine ⟨fun y i => if h : i ∈ F then y ⟨i,h⟩ else x₀ i, ?_⟩
  apply continuous_pi
  intro i
  by_cases hi : i ∈ F
  · simp only [dif_pos hi]
    exact continuous_apply (⟨i,hi⟩ : ↥F)
  · simp only [dif_neg hi]
    exact continuous_const

theorem extend_restrict_agrees (F : Finset I) (x₀ x : ∀ i, X i)
    (i : I) (hi : i ∈ F) :
    extendCoordinates F x₀ (restrictCoordinates F x) i = x i := by
  classical
  change (if h : i ∈ F then (restrictCoordinates F x) ⟨i,h⟩ else x₀ i) = x i
  rw [dif_pos hi] <;> rfl

/-- Actual locally constant factor, not merely a finite support
predicate. The default point is only used for the omitted factors. -/
theorem finiteCoordinateFactor (f : LocallyConstant (∀ i, X i) A)
    (x₀ : ∀ i, X i) :
    ∃ F : Finset I, ∃ g : LocallyConstant (∀ i : ↥F, X i.val) A,
      g.comap (restrictCoordinates F) = f := by
  obtain ⟨F,hF⟩ := finiteCoordinateSupport f
  refine ⟨F, f.comap (extendCoordinates F x₀), ?_⟩
  ext x
  exact hF _ _ (fun i hi => extend_restrict_agrees F x₀ x i hi)

end FiniteCoordinates

section ProductRelation

variable {I : Type u} {X : I → Type v} {Y : I → Type w}
  [∀ i, TopologicalSpace (X i)]

abbrev tupleRelation {B : Type*} {D : Type*} (p : B → D) (n : ℕ) :=
  {z : Fin (n+1) → B // ∀ i, p (z i)=p (z 0)}

def productMap (p : ∀ i, X i → Y i) (x : ∀ i, X i) : ∀ i, Y i :=
  fun i => p i (x i)

/-- The genuine all-tuple product relation is homeomorphic to the
product of the individual all-tuple relations. This includes
arbitrary index sets and all tuple arities. -/
def productRelationHomeo (p : ∀ i, X i → Y i) (n : ℕ) :
    tupleRelation (productMap p) n ≃ₜ (∀ i, tupleRelation (p i) n) where
  toFun z i := ⟨fun j => z.val j i, fun j => congrFun (z.property j) i⟩
  invFun z := ⟨fun j i => (z i).val j, fun j => funext fun i => (z i).property j⟩
  left_inv z := by apply Subtype.ext; funext j i; rfl
  right_inv z := by funext i; apply Subtype.ext; funext j; rfl
  continuous_toFun := by
    apply continuous_pi
    intro i
    apply Continuous.subtype_mk
    apply continuous_pi
    intro j
    exact (continuous_apply i).comp ((continuous_apply j).comp continuous_subtype_val)
  continuous_invFun := by
    apply Continuous.subtype_mk
    apply continuous_pi
    intro j
    apply continuous_pi
    intro i
    exact (continuous_apply j).comp (continuous_subtype_val.comp (continuous_apply i))

def tupleDeletion {B : Type*} {D : Type*} (p : B → D) (n : ℕ)
    (k : Fin (n+2)) (z : tupleRelation p (n+1)) : tupleRelation p n :=
  ⟨z.val ∘ k.succAbove, fun i =>
    (z.property (k.succAbove i)).trans (z.property (k.succAbove 0)).symm⟩

/-- The homeomorphism identifies the actual deletion faces,
hence the product-coordinate factorization respects signs and
all arities of the Čech differential. -/
theorem productRelationHomeo_face (p : ∀ i, X i → Y i) (n : ℕ)
    (k : Fin (n+2)) (z : tupleRelation (productMap p) (n+1)) :
    productRelationHomeo p n (tupleDeletion (productMap p) n k z) =
      fun i => tupleDeletion (p i) n k (productRelationHomeo p (n+1) z i) := by
  funext i
  apply Subtype.ext
  rfl

end ProductRelation

#print axioms finiteCoordinateSupport
#print axioms finiteCoordinateFactor
#print axioms productRelationHomeo
#print axioms productRelationHomeo_face
end CMDG.CondensedCM5R0.CompactCover
