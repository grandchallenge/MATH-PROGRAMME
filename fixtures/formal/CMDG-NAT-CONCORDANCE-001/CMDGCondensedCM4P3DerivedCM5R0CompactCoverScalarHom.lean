import CMDGCondensedCM4P3DerivedCM5R0CompactCoverScalarAcyclic

/-! The scalar Hom complex for genuine compact-cover relation objects.
The alternating differential uses actual face morphisms, without any
assumption of acyclicity of the compact target. -/
noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0.CompactCover

/-- Actual precomposition by an individual categorical free-module face
is the corresponding scalar restriction on the true relation. -/
theorem compactRelationFace_integerHom_scalar
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ) (k : Fin (n + 2))
    (g : (Condensed.profiniteFree Coeff).obj
      (compactRelationProfinite P T p n) ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv
      (compactRelationProfinite P T p (n + 1))
      ((Condensed.profiniteFree Coeff).map
        (compactRelationFace P T p n k) ≫ g) =
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (compactRelationProfinite P T p n) g).comap
        (compactRelationFace P T p n k).hom.hom := by
  exact freeProfiniteDiscreteIntegerHomScalarEquiv_precomp
    (compactRelationFace P T p n k) g

/-- Signed scalar differential attached to categorical free-module
relations, using the same genuine Profinite face morphisms. -/
def compactCategoricalRelationScalarDifferential
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    LocallyConstant (compactRelationProfinite P T p n) ℤ →
    LocallyConstant (compactRelationProfinite P T p (n + 1)) ℤ :=
  fun f => ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    f.comap (compactRelationFace P T p n k).hom.hom

theorem compactCategoricalRelationScalarDifferential_apply
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ)
    (f : LocallyConstant (compactRelationProfinite P T p n) ℤ)
    (xs : compactRelationProfinite P T p (n + 1)) :
    compactCategoricalRelationScalarDifferential P T p n f xs =
      ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) *
        f ((compactRelationFace P T p n k).hom.hom xs) := by
  change (LocallyConstant.evalₗ ℤ xs)
    (∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
      f.comap (compactRelationFace P T p n k).hom.hom) =
    _
  simp only [map_sum, map_smul, LocallyConstant.evalₗ_apply, smul_eq_mul]
  rfl

theorem compactFreeRelationBoundary_integerHom_scalar
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ)
    (g : (Condensed.profiniteFree Coeff).obj
      (compactRelationProfinite P T p n) ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv
      (compactRelationProfinite P T p (n + 1))
      (compactFreeRelationBoundary P T p n ≫ g) =
    compactCategoricalRelationScalarDifferential P T p n
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (compactRelationProfinite P T p n) g) := by
  classical
  rw [compactFreeRelationBoundary, Preadditive.sum_comp]
  simp only [Preadditive.zsmul_comp]
  change (uniformFreeRelationHomScalarAddHom
    (compactRelationProfinite P T p (n + 1)))
    (∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
      ((Condensed.profiniteFree Coeff).map
        (compactRelationFace P T p n k) ≫ g)) = _
  rw [map_sum]
  simp only [map_zsmul]
  apply DFunLike.ext
  intro xs
  rw [compactCategoricalRelationScalarDifferential_apply]
  change (LocallyConstant.evalₗ ℤ xs)
      (∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
        (uniformFreeRelationHomScalarAddHom
          (compactRelationProfinite P T p (n + 1)))
          ((Condensed.profiniteFree Coeff).map
            (compactRelationFace P T p n k) ≫ g)) = _
  simp only [map_sum, map_smul, LocallyConstant.evalₗ_apply, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro k hk
  change (-1 : ℤ) ^ (k : ℕ) *
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (compactRelationProfinite P T p (n + 1))
      ((Condensed.profiniteFree Coeff).map
        (compactRelationFace P T p n k) ≫ g)) xs =
    _
  rw [compactRelationFace_integerHom_scalar]
  rfl

/-- Canonical homeomorphism from the profinite object to the
genuine closed-relation subtype. It is not a made-up finite surrogate. -/
def compactRelationHomeomorph
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    compactRelationProfinite P T p n ≃ₜ
      ↥(compactCechArityRelatedSet n P T p) where
  toFun := id
  invFun := id
  left_inv := fun _ => rfl
  right_inv := fun _ => rfl
  continuous_toFun := by
    change Continuous (id : ↥(compactCechArityRelatedSet n P T p) → _)
    exact continuous_id
  continuous_invFun := by
    change Continuous (id : ↥(compactCechArityRelatedSet n P T p) → _)
    exact continuous_id

/-- Transport scalar cochains between the categorical profinite
model and the original closed-subtype relation model. -/
def compactRelationScalarEquiv
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    LocallyConstant (compactRelationProfinite P T p n) ℤ ≃
      LocallyConstant (↥(compactCechArityRelatedSet n P T p)) ℤ where
  toFun f := f.comap ⟨(compactRelationHomeomorph P T p n).symm,
    (compactRelationHomeomorph P T p n).symm.continuous⟩
  invFun f := f.comap ⟨(compactRelationHomeomorph P T p n),
    (compactRelationHomeomorph P T p n).continuous⟩
  left_inv f := by
    ext xs
    rfl
  right_inv f := by
    ext xs
    rfl


#print axioms compactRelationFace_integerHom_scalar
#print axioms compactFreeRelationBoundary_integerHom_scalar
#print axioms compactRelationHomeomorph
end CMDG.CondensedCM5R0.CompactCover
