import CMDGCondensedCM4P3DerivedCM5R0UniformClosedCechCochains

noncomputable section
universe u v
namespace CMDG.CondensedCM5R0

def uniformScalarCechD {I : Type v} (n : ℕ)
    (c : (Fin (n + 1) → I) → ℤ) :
    (Fin (n + 2) → I) → ℤ :=
  fun σ => ∑ j : Fin (n + 2), (-1 : ℤ) ^ (j : ℕ) * c (σ ∘ j.succAbove)

def uniformScalarCechCone {I : Type v} (i : I) (n : ℕ)
    (c : (Fin (n + 2) → I) → ℤ) :
    (Fin (n + 1) → I) → ℤ :=
  fun σ => c (Fin.cons i σ)

theorem uniformFinCons_face_zero
    {I : Type v} (i : I) (n : ℕ) (σ : Fin (n + 2) → I) :
    (Fin.cons i σ) ∘ (Fin.succAbove (0 : Fin (n + 3))) = σ := by
  funext k
  simp

theorem uniformFinCons_face_succ
    {I : Type v} (i : I) (n : ℕ)
    (σ : Fin (n + 2) → I) (j : Fin (n + 2)) :
    (Fin.cons i σ) ∘ ((j.succ : Fin (n + 3)).succAbove) =
      Fin.cons i (σ ∘ j.succAbove) := by
  funext k
  refine Fin.cases ?_ ?_ k
  · simp only [Function.comp_apply, Fin.succ_succAbove_zero, Fin.cons_zero]
  · intro l
    simp only [Function.comp_apply, Fin.succ_succAbove_succ, Fin.cons_succ]

theorem uniformScalarCechCone_identity
    {I : Type v} (i : I) (n : ℕ)
    (c : (Fin (n + 2) → I) → ℤ)
    (σ : Fin (n + 2) → I) :
    uniformScalarCechD n (uniformScalarCechCone i n c) σ +
      uniformScalarCechCone i (n + 1) (uniformScalarCechD (n + 1) c) σ =
    c σ := by
  dsimp [uniformScalarCechD, uniformScalarCechCone]
  conv_lhs => rhs; rw [Fin.sum_univ_succ]
  simp only [Fin.val_zero, pow_zero, one_mul, Fin.val_succ, pow_succ]
  rw [uniformFinCons_face_zero i n σ]
  simp_rw [uniformFinCons_face_succ i n σ]
  simp only [mul_neg, mul_one, neg_mul, Finset.sum_neg_distrib]
  abel


/-- Contracting homotopy of the *ambient* unrestricted-tuple complex at
an arbitrary fixed vertex i. This is pointwise, in every degree. -/
def uniformClosedCechAmbientCone
    (X : Profinite.{u}) (I : Type v) (i : I) (n : ℕ)
    (C : uniformClosedCechAmbientCochain X I (n + 1)) :
    uniformClosedCechAmbientCochain X I n :=
  fun σ => C (Fin.cons i σ)

theorem uniformClosedCechAmbientCone_identity
    (X : Profinite.{u}) (I : Type v) (i : I) (n : ℕ)
    (C : uniformClosedCechAmbientCochain X I (n + 1))
    (σ : Fin (n + 2) → I) (x : X) :
    (uniformClosedCechAmbientDifferential X I n
      (uniformClosedCechAmbientCone X I i n C) σ) x +
    (uniformClosedCechAmbientCone X I i (n + 1)
      (uniformClosedCechAmbientDifferential X I (n + 1) C) σ) x =
      C σ x := by
  rw [uniformClosedCechAmbientDifferential_apply X I n
    (uniformClosedCechAmbientCone X I i n C) σ x]
  change uniformScalarCechD n
    (uniformScalarCechCone i n (fun τ => C τ x)) σ +
    (uniformClosedCechAmbientDifferential X I (n + 1) C
      (Fin.cons i σ)) x = C σ x
  rw [uniformClosedCechAmbientDifferential_apply]
  exact uniformScalarCechCone_identity i n (fun τ => C τ x) σ

/-- Local cone correction in every positive cochain degree.

For an actual closed-intersection cocycle, choosing any closed-family
vertex i yields a primitive on all tuples *at points also in E i*.
It does not claim a global primitive: that requires gluing the
different vertexwise corrections across a finite closed family. -/
theorem uniformClosedCechLocalCocycle_cone_on_vertex
    (X : Profinite.{u}) {I : Type v}
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (i : I) (n : ℕ)
    (c : uniformClosedCechLocalCochain X E (n + 1))
    (hc : uniformClosedCechDifferential X E (n + 1) c = 0) :
    ∃ b : uniformClosedCechLocalCochain X E n,
      ∀ (σ : Fin (n + 2) → I) (x : X)
          (_hi : x ∈ E i)
          (hσ : x ∈ uniformClosedCechIntersection X E (n + 1) σ),
        (uniformClosedCechDifferential X E n b σ) ⟨x,hσ⟩ =
          c σ ⟨x,hσ⟩ := by
  classical
  obtain ⟨C, rfl⟩ :=
    uniformClosedCechRestrict_surjective X E hclosed (n + 1) c
  refine ⟨uniformClosedCechRestrict X E n
    (uniformClosedCechAmbientCone X I i n C), ?_⟩
  intro σ x hi hσ
  have hcons :
      x ∈ uniformClosedCechIntersection X E (n + 2) (Fin.cons i σ) := by
    simp only [uniformClosedCechIntersection, Set.mem_iInter] at hσ ⊢
    intro j
    refine Fin.cases ?_ ?_ j
    · simpa only [Fin.cons_zero] using hi
    · intro k
      simpa only [Fin.cons_succ] using hσ k
  have hCoc := hc
  rw [uniformClosedCechDifferential_restrict X E (n + 1) C] at hCoc
  have hzero :
      (uniformClosedCechAmbientDifferential X I (n + 1) C
        (Fin.cons i σ)) x = 0 := by
    have h := congrArg
      (fun q : uniformClosedCechLocalCochain X E (n + 2) =>
        q (Fin.cons i σ) ⟨x,hcons⟩) hCoc
    exact h
  rw [uniformClosedCechDifferential_restrict]
  change (uniformClosedCechAmbientDifferential X I n
    (uniformClosedCechAmbientCone X I i n C) σ) x = C σ x
  have h := uniformClosedCechAmbientCone_identity X I i n C σ x
  simp only [uniformClosedCechAmbientCone] at h
  omega

#print axioms uniformClosedCechLocalCocycle_cone_on_vertex

#print axioms uniformScalarCechCone_identity
#print axioms uniformClosedCechAmbientCone_identity
end CMDG.CondensedCM5R0
