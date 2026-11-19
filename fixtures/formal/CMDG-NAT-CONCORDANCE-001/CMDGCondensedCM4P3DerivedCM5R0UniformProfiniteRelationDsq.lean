import CMDGCondensedCM4P3DerivedCM5R0UniformProfiniteRelationComplex

/-!
# Genuine profinite relation differential squares to zero

The all-arity continuous face maps form a cochain complex, not merely
an exactness assertion on a pair of formal arrows. Prove this via
ambient tuple extension and naturality of restriction to closed R_k.
-/

noncomputable section
universe u
open Set CategoryTheory Limits
namespace CMDG.CondensedCM5R0

def uniformProfiniteAmbientFaceMap
    (P : Profinite.{u}) (n : ℕ) (k : Fin (n + 2)) :
    C(Fin (n + 2) → P, Fin (n + 1) → P) :=
  ⟨fun xs => xs ∘ k.succAbove,
    by
      apply continuous_pi
      intro j
      exact continuous_apply (k.succAbove j)⟩

def uniformProfiniteAmbientDifferential
    (P : Profinite.{u}) (n : ℕ) :
    LocallyConstant (Fin (n + 1) → P) ℤ →
    LocallyConstant (Fin (n + 2) → P) ℤ :=
  fun c => ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    c.comap (uniformProfiniteAmbientFaceMap P n k)

theorem uniformProfiniteAmbientDifferential_apply
    (P : Profinite.{u}) (n : ℕ)
    (c : LocallyConstant (Fin (n + 1) → P) ℤ)
    (xs : Fin (n + 2) → P) :
    (uniformProfiniteAmbientDifferential P n c) xs =
      scalarCechDifferential n (fun τ => c τ) xs := by
  change (LocallyConstant.evalₗ ℤ xs)
    (∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
      c.comap (uniformProfiniteAmbientFaceMap P n k)) =
    ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) *
      c (k.removeNth xs)
  simp only [map_sum, map_smul, LocallyConstant.evalₗ_apply, smul_eq_mul]
  rfl

theorem uniformProfiniteAmbientDifferential_sq_zero
    (P : Profinite.{u}) (n : ℕ)
    (c : LocallyConstant (Fin (n + 1) → P) ℤ) :
    uniformProfiniteAmbientDifferential P (n + 1)
      (uniformProfiniteAmbientDifferential P n c) = 0 := by
  apply DFunLike.ext
  intro xs
  rw [uniformProfiniteAmbientDifferential_apply]
  have hs := congrFun (scalarCechDifferential_sq_zero n
    (fun τ : Fin (n + 1) → P => c τ)) xs
  have hs' : scalarCechDifferential (n + 1)
      (scalarCechDifferential n (fun τ => c τ)) xs = 0 := by
    simpa using hs
  change scalarCechDifferential (n + 1)
    (fun τ => (uniformProfiniteAmbientDifferential P n c) τ) xs = 0
  convert hs' using 1
  congr 1
  funext τ
  exact uniformProfiniteAmbientDifferential_apply P n c τ

/-- Ambient restriction to the genuine equal-image relation, of an
ambient tuple cochain, at every degree. -/
def uniformProfiniteRelationRestrict
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (C : LocallyConstant (Fin (n + 1) → P) ℤ) :
    LocallyConstant (↥(profiniteCechArityRelatedSet n P T p)) ℤ :=
  C.comap ⟨Subtype.val, continuous_subtype_val⟩

theorem uniformProfiniteRelationDifferential_restrict
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (C : LocallyConstant (Fin (n + 1) → P) ℤ) :
    uniformProfiniteRelationDifferential P T p n
      (uniformProfiniteRelationRestrict P T p n C) =
    uniformProfiniteRelationRestrict P T p (n + 1)
      (uniformProfiniteAmbientDifferential P n C) := by
  apply DFunLike.ext
  intro xs
  rw [uniformProfiniteRelationDifferential_apply]
  change (∑ k : Fin (n + 2),
    (-1 : ℤ) ^ (k : ℕ) * C (xs.val ∘ k.succAbove)) =
    (uniformProfiniteAmbientDifferential P n C) xs.val
  rw [uniformProfiniteAmbientDifferential_apply]
  rfl

theorem uniformProfiniteRelationDifferential_sq_zero
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (c : LocallyConstant (↥(profiniteCechArityRelatedSet n P T p)) ℤ) :
    uniformProfiniteRelationDifferential P T p (n + 1)
      (uniformProfiniteRelationDifferential P T p n c) = 0 := by
  obtain ⟨C,hC⟩ :=
    integerCechArityRelated_locallyConstant_extends n P T p c
  have hrestrict :
      uniformProfiniteRelationRestrict P T p n C = c := by
    apply DFunLike.ext
    intro xs
    exact hC xs
  rw [← hrestrict]
  rw [uniformProfiniteRelationDifferential_restrict]
  rw [uniformProfiniteRelationDifferential_restrict]
  rw [uniformProfiniteAmbientDifferential_sq_zero]
  rfl

#print axioms uniformProfiniteRelationDifferential_sq_zero
end CMDG.CondensedCM5R0
