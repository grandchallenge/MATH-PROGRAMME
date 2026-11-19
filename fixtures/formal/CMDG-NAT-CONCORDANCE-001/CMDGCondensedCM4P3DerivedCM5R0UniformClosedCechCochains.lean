import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverGluing
import Mathlib.Data.Fin.Tuple.Basic

/-!
# CM5: degree-uniform finite closed-intersection cochain interfaces

For any cochain degree, all tuples (including repetitions) of a finite closed
family have closed intersections, and every tuple-indexed collection of
locally constant integer functions on the genuine intersections can be
represented by ambient locally constant functions. The representation
does not assume that the closed family is clopen.

This is an actual all-degree extension statement, not a claim of cocycle
acyclicity, differential exactness, or derived solidity.
-/

noncomputable section
universe u v w
open Set
namespace CMDG.CondensedCM5R0

/-- Genuine intersection associated with an ordered tuple, including repeated indices. -/
def uniformClosedCechIntersection (X : Profinite.{u}) {I : Type v} (E : I → Set X) (n : ℕ) (σ : Fin (n + 1) → I) : Set X :=
  ⋂ j, E (σ j)

/-- Arbitrary-length intersections of closed subsets are closed. -/
theorem uniformClosedCechIntersection_isClosed
    (X : Profinite.{u}) {I : Type v} (E : I → Set X)
    (hclosed : ∀ i, IsClosed (E i))
    (n : ℕ) (σ : Fin (n + 1) → I) :
    IsClosed (uniformClosedCechIntersection X E n σ) := by
  exact isClosed_iInter (fun j => hclosed (σ j))

/-- The true intersection-local, all-tuples scalar cochain term at degree n. -/
abbrev uniformClosedCechLocalCochain (X : Profinite.{u}) {I : Type v}
    (E : I → Set X) (n : ℕ) : Type _ :=
  ∀ σ : Fin (n + 1) → I,
    LocallyConstant (uniformClosedCechIntersection X E n σ) ℤ

/-- The ambient scalar cochains with the same tuple indexing. -/
abbrev uniformClosedCechAmbientCochain (X : Profinite.{u}) (I : Type v) (n : ℕ) : Type _ :=
  (Fin (n + 1) → I) → LocallyConstant X ℤ

/-- Deleting a coordinate enlarges the intersection. This holds for
arbitrary tuple lengths, including tuples with repeated indices. -/
theorem uniformClosedCechIntersection_face_subset
    (X : Profinite.{u}) {I : Type v} (E : I → Set X)
    (n : ℕ) (σ : Fin (n + 2) → I) (j : Fin (n + 2)) :
    uniformClosedCechIntersection X E (n + 1) σ ⊆
      uniformClosedCechIntersection X E n (σ ∘ j.succAbove) := by
  intro x hx
  simp only [uniformClosedCechIntersection, Set.mem_iInter] at hx ⊢
  intro k
  exact hx (j.succAbove k)

/-- Actual continuous face-inclusion map on genuine closed intersections. -/
def uniformClosedCechFaceMap
    (X : Profinite.{u}) {I : Type v} (E : I → Set X)
    (n : ℕ) (σ : Fin (n + 2) → I) (j : Fin (n + 2)) :
    C(uniformClosedCechIntersection X E (n + 1) σ,
      uniformClosedCechIntersection X E n (σ ∘ j.succAbove)) :=
  ⟨fun x => ⟨x.val,
      uniformClosedCechIntersection_face_subset X E n σ j x.property⟩,
    Continuous.subtype_mk continuous_subtype_val _⟩

/-- Pull scalar cochains back along the genuine closed-intersection face. -/
def uniformClosedCechFaceRestrict
    (X : Profinite.{u}) {I : Type v} (E : I → Set X)
    (n : ℕ) (σ : Fin (n + 2) → I) (j : Fin (n + 2))
    (f : LocallyConstant
      (uniformClosedCechIntersection X E n (σ ∘ j.succAbove)) ℤ) :
    LocallyConstant (uniformClosedCechIntersection X E (n + 1) σ) ℤ :=
  f.comap (uniformClosedCechFaceMap X E n σ j)

/-- The face map really evaluates the original cochain at the same
point in the smaller closed intersection. -/
theorem uniformClosedCechFaceRestrict_apply
    (X : Profinite.{u}) {I : Type v} (E : I → Set X)
    (n : ℕ) (σ : Fin (n + 2) → I) (j : Fin (n + 2))
    (f : LocallyConstant
      (uniformClosedCechIntersection X E n (σ ∘ j.succAbove)) ℤ)
    (x : uniformClosedCechIntersection X E (n + 1) σ) :
    uniformClosedCechFaceRestrict X E n σ j f x =
      f (uniformClosedCechFaceMap X E n σ j x) := rfl

/-- Restrict ambient cochains to the actual closed intersection of each tuple. -/
def uniformClosedCechRestrict (X : Profinite.{u}) {I : Type v}
    (E : I → Set X) (n : ℕ) :
    uniformClosedCechAmbientCochain X I n →
      uniformClosedCechLocalCochain X E n :=
  fun C σ =>
    (C σ).comap (⟨Subtype.val, continuous_subtype_val⟩ :
      C(uniformClosedCechIntersection X E n σ, X))


/-- Ambient restriction commutes with every actual face-deletion map.
This is the degree-uniform naturality needed for an alternating differential. -/
theorem uniformClosedCechFaceRestrict_ambient
    (X : Profinite.{u}) {I : Type v} (E : I → Set X)
    (n : ℕ) (j : Fin (n + 2))
    (C : uniformClosedCechAmbientCochain X I n)
    (σ : Fin (n + 2) → I) :
    uniformClosedCechFaceRestrict X E n σ j
      ((uniformClosedCechRestrict X E n C) (σ ∘ j.succAbove)) =
    (uniformClosedCechRestrict X E (n + 1)
      (fun τ : Fin (n + 2) → I => C (τ ∘ j.succAbove))) σ := by
  apply DFunLike.ext
  intro x
  rfl


/-- General simplicial identity behind the closed-intersection complex. -/
def scalarCechDifferential {I : Type u} (n : ℕ)
    (c : (Fin (n + 1) → I) → ℤ) : (Fin (n + 2) → I) → ℤ :=
  fun σ => ∑ i : Fin (n + 2), (-1 : ℤ) ^ (i : ℕ) * c (i.removeNth σ)

/-- Signed cofaces square to zero for any integer-valued tuple cochain. -/
theorem scalarCechDifferential_sq_zero {I : Type u} (n : ℕ)
    (c : (Fin (n + 1) → I) → ℤ) :
    scalarCechDifferential (n + 1) (scalarCechDifferential n c) = 0 := by
  funext σ
  change (∑ j : Fin (n + 3), (-1 : ℤ) ^ (j : ℕ) *
    ∑ i : Fin (n + 2), (-1 : ℤ) ^ (i : ℕ) *
      c (i.removeNth (j.removeNth σ))) = 0
  simp only [Finset.mul_sum]
  rw [Finset.sum_comm]
  simp only [← Finset.sum_product']
  let P := Fin (n + 2) × Fin (n + 3)
  let S : Finset P := {ij : P | (ij.2 : ℕ) ≤ (ij.1 : ℕ)}
  rw [Finset.univ_product_univ, ← Finset.sum_add_sum_compl S, ← eq_neg_iff_add_eq_zero,
    ← Finset.sum_neg_distrib]
  let φ : ∀ ij : P, ij ∈ S → P := fun ij hij =>
    (Fin.castLT ij.2 (lt_of_le_of_lt (Finset.mem_filter.mp hij).right (Fin.is_lt ij.1)), ij.1.succ)
  apply Finset.sum_bij φ
  · intro ij hij
    simp_rw [S, φ, Finset.compl_filter, Finset.mem_filter_univ, not_le,
      Fin.val_succ, Fin.val_castLT] at hij ⊢
    lia
  · rintro ⟨i, j⟩ hij ⟨i', j'⟩ hij' h
    rw [Prod.mk_inj]
    exact ⟨by simpa [φ] using! congr_arg Prod.snd h,
      by simpa [φ, Fin.castSucc_castLT] using! congr_arg Fin.castSucc (congr_arg Prod.fst h)⟩
  · rintro ⟨i', j'⟩ hij'
    simp_rw [S, Finset.compl_filter, Finset.mem_filter_univ, not_le] at hij'
    refine ⟨(j'.pred <| ?_, Fin.castSucc i'), ?_, ?_⟩
    · rintro rfl
      simp only [Fin.val_zero, not_lt_zero] at hij'
    · simpa [S] using! Nat.le_sub_one_of_lt hij'
    · simp only [φ, Fin.castLT_castSucc, Fin.succ_pred]
  · rintro ⟨i, j⟩ hij
    dsimp
    simp only [φ, Fin.val_succ, pow_add, pow_one, mul_neg, mul_one]
    have hjval : (j : ℕ) ≤ (i : ℕ) :=
      (Finset.mem_filter.mp hij).2
    have hjle : j ≤ i.castSucc := Fin.le_iff_val_le_val.mpr hjval
    rw [Fin.removeNth_removeNth_eq_swap,
      Fin.predAbove_of_le_castSucc i j hjle,
      Fin.succAbove_of_le_castSucc j i hjle]
    simp only [Fin.castPred, Fin.val_castLT]
    ring


/-- The genuine all-tuples closed-intersection Čech differential.
It uses the continuous face maps and signed integer coefficients. -/
def uniformClosedCechDifferential
    (X : Profinite.{u}) {I : Type v} (E : I → Set X) (n : ℕ) :
    uniformClosedCechLocalCochain X E n →
      uniformClosedCechLocalCochain X E (n + 1) :=
  fun c σ => ∑ j : Fin (n + 2),
    (-1 : ℤ) ^ (j : ℕ) •
      uniformClosedCechFaceRestrict X E n σ j (c (σ ∘ j.succAbove))

/-- The corresponding all-tuples ambient signed differential. -/
def uniformClosedCechAmbientDifferential
    (X : Profinite.{u}) (I : Type v) (n : ℕ) :
    uniformClosedCechAmbientCochain X I n →
      uniformClosedCechAmbientCochain X I (n + 1) :=
  fun C σ => ∑ j : Fin (n + 2),
    (-1 : ℤ) ^ (j : ℕ) • C (σ ∘ j.succAbove)


/-- Evaluation of the ambient signed Čech differential is exactly the
integer-valued simplicial differential, in every degree. -/
theorem uniformClosedCechAmbientDifferential_apply
    (X : Profinite.{u}) (I : Type v) (n : ℕ)
    (C : uniformClosedCechAmbientCochain X I n)
    (σ : Fin (n + 2) → I) (x : X) :
    (uniformClosedCechAmbientDifferential X I n C σ) x =
    scalarCechDifferential n (fun τ => C τ x) σ := by
  change (LocallyConstant.evalₗ ℤ x)
    (∑ j : Fin (n + 2), (-1 : ℤ) ^ (j : ℕ) • C (σ ∘ j.succAbove)) =
    ∑ j : Fin (n + 2), (-1 : ℤ) ^ (j : ℕ) * C (σ ∘ j.succAbove) x
  simp only [map_sum, map_smul, LocallyConstant.evalₗ_apply, smul_eq_mul]


/-- The actual ambient all-tuples differential squares to zero in every
degree, by pointwise reduction to the signed simplicial identity. -/
theorem uniformClosedCechAmbientDifferential_sq_zero
    (X : Profinite.{u}) (I : Type v) (n : ℕ)
    (C : uniformClosedCechAmbientCochain X I n) :
    uniformClosedCechAmbientDifferential X I (n + 1)
      (uniformClosedCechAmbientDifferential X I n C) = 0 := by
  funext σ
  apply DFunLike.ext
  intro x
  change (uniformClosedCechAmbientDifferential X I (n + 1)
    (uniformClosedCechAmbientDifferential X I n C) σ) x = 0
  have hcomp :
      (fun τ : Fin (n + 2) → I =>
        (uniformClosedCechAmbientDifferential X I n C τ) x) =
        scalarCechDifferential n (fun τ => C τ x) := by
    funext τ
    exact uniformClosedCechAmbientDifferential_apply X I n C τ x
  calc
    _ = scalarCechDifferential (n + 1)
      (fun τ => (uniformClosedCechAmbientDifferential X I n C τ) x) σ :=
        uniformClosedCechAmbientDifferential_apply X I (n + 1)
          (uniformClosedCechAmbientDifferential X I n C) σ x
    _ = scalarCechDifferential (n + 1)
      (scalarCechDifferential n (fun τ => C τ x)) σ := by rw [hcomp]
    _ = 0 := by
      have hs := congrFun (scalarCechDifferential_sq_zero n (fun τ => C τ x)) σ
      simpa using hs

/-- The local differential agrees with the ambient differential after
restriction to genuine closed intersections, in every degree. -/
theorem uniformClosedCechDifferential_restrict
    (X : Profinite.{u}) {I : Type v} (E : I → Set X)
    (n : ℕ) (C : uniformClosedCechAmbientCochain X I n) :
    uniformClosedCechDifferential X E n
      (uniformClosedCechRestrict X E n C) =
    uniformClosedCechRestrict X E (n + 1)
      (uniformClosedCechAmbientDifferential X I n C) := by
  funext σ
  apply DFunLike.ext
  intro x
  change (LocallyConstant.evalₗ ℤ x)
    (∑ j : Fin (n + 2), (-1 : ℤ) ^ (j : ℕ) •
      uniformClosedCechFaceRestrict X E n σ j
        ((uniformClosedCechRestrict X E n C) (σ ∘ j.succAbove))) =
    (LocallyConstant.evalₗ ℤ x.val)
      (∑ j : Fin (n + 2), (-1 : ℤ) ^ (j : ℕ) •
        C (σ ∘ j.succAbove))
  simp only [map_sum, map_smul, LocallyConstant.evalₗ_apply]
  apply Finset.sum_congr rfl
  intro j hj
  rfl

/-- Every local cochain of any degree has an ambient representative.
No finite-quotient agreement across tuples is assumed. -/
theorem uniformClosedCechRestrict_surjective
    (X : Profinite.{u}) {I : Type v} (E : I → Set X)
    (hclosed : ∀ i, IsClosed (E i)) (n : ℕ) :
    Function.Surjective (uniformClosedCechRestrict X E n) := by
  classical
  intro c
  have hex (σ : Fin (n + 1) → I) :
      ∃ C : LocallyConstant X ℤ,
        ∀ x : uniformClosedCechIntersection X E n σ,
          C x.val = c σ x := by
    exact locallyConstant_extend_closed_subset X
      (uniformClosedCechIntersection X E n σ)
      (uniformClosedCechIntersection_isClosed X E hclosed n σ)
      (c σ)
  choose C hC using hex
  refine ⟨C, ?_⟩
  funext σ
  apply DFunLike.ext
  intro x
  exact hC σ x


/-- Uniform extension holds independently in every coordinate of any product,
without imposing a single common ambient finite observation. -/
theorem uniformClosedCechProduct_hasAmbientRepresentative
    (X : Profinite.{u}) {I : Type v} (E : I → Set X)
    (hclosed : ∀ i, IsClosed (E i)) (n : ℕ)
    {ι : Type w} (c : ι → uniformClosedCechLocalCochain X E n) :
    ∃ C : ι → uniformClosedCechAmbientCochain X I n,
      ∀ k, uniformClosedCechRestrict X E n (C k) = c k := by
  classical
  have h (k : ι) : ∃ C : uniformClosedCechAmbientCochain X I n,
      uniformClosedCechRestrict X E n C = c k :=
    uniformClosedCechRestrict_surjective X E hclosed n (c k)
  choose C hC using h
  exact ⟨C, hC⟩

#print axioms scalarCechDifferential_sq_zero
#print axioms uniformClosedCechAmbientDifferential_apply
#print axioms uniformClosedCechAmbientDifferential_sq_zero
#print axioms uniformClosedCechIntersection_face_subset
#print axioms uniformClosedCechFaceRestrict_apply
#print axioms uniformClosedCechFaceRestrict_ambient
#print axioms uniformClosedCechDifferential_restrict
#print axioms uniformClosedCechProduct_hasAmbientRepresentative


/-- Main degree-uniform structural result: on the genuine closed
intersections of any closed family, the all-tuples signed Čech
differential squares to zero. The proof does not assert acyclicity. -/
theorem uniformClosedCechDifferential_sq_zero
    (X : Profinite.{u}) {I : Type v} (E : I → Set X)
    (hclosed : ∀ i, IsClosed (E i)) (n : ℕ)
    (c : uniformClosedCechLocalCochain X E n) :
    uniformClosedCechDifferential X E (n + 1)
      (uniformClosedCechDifferential X E n c) = 0 := by
  obtain ⟨C, hC⟩ := uniformClosedCechRestrict_surjective X E hclosed n c
  rw [← hC]
  rw [uniformClosedCechDifferential_restrict X E n C]
  rw [uniformClosedCechDifferential_restrict X E (n + 1)
    (uniformClosedCechAmbientDifferential X I n C)]
  rw [uniformClosedCechAmbientDifferential_sq_zero X I n C]
  funext σ
  apply DFunLike.ext
  intro x
  rfl

#print axioms uniformClosedCechDifferential_sq_zero
#print axioms uniformClosedCechIntersection_isClosed
#print axioms uniformClosedCechRestrict_surjective
end CMDG.CondensedCM5R0
