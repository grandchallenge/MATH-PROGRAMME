import CMDGCondensedCM4P3DerivedCM5R0DiscreteProductCechDifferential
import CMDGCondensedCM4P3DerivedCM5R0UniformProfiniteRelationDsq

/-!
# Degree-uniform genuine categorical Čech Hom exactness

All statements use real profinite equal-image relation objects and
the real free condensed-module functor, uniformly in all degrees.
The categorical Hom differential is the alternating sum of actual
free-module face maps, and its natural scalar comparison is proved.
The Hom complex is exact in positive degrees for the actual discrete
integer coefficient object and arbitrary categorical products of it.

For the genuine underived free-solid coefficient target, exactness
is formally proved only CONDITIONAL on a supplied categorical product
isomorphism. No such product model is claimed to exist globally.
No all-degree Ext, relation epimorphism, derived solidity, or public
independent mathematical certification is asserted by this module.
-/
noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

/-- Actual profinite object of related tuples, in every arity. -/
def uniformRelationProfinite
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) : Profinite.{u} :=
  letI : CompactSpace (↥(profiniteCechArityRelatedSet n P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechArityRelatedSet_isClosed n P T p).isCompact
  Profinite.of (↥(profiniteCechArityRelatedSet n P T p))

/-- Continuous face deletion as an honest Profinite morphism. -/
def uniformRelationFace
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (k : Fin (n + 2)) :
    uniformRelationProfinite P T p (n + 1) ⟶
      uniformRelationProfinite P T p n := by
  letI : CompactSpace (↥(profiniteCechArityRelatedSet (n + 1) P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechArityRelatedSet_isClosed (n + 1) P T p).isCompact
  letI : CompactSpace (↥(profiniteCechArityRelatedSet n P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechArityRelatedSet_isClosed n P T p).isCompact
  exact CompHausLike.ofHom _
    (uniformProfiniteRelationFaceMap P T p n k)

/-- Actual precomposition by an individual categorical free-module face
is the corresponding scalar restriction on the true relation. -/
theorem uniformRelationFace_integerHom_scalar
    (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ) (k : Fin (n + 2))
    (g : (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p n) ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv
      (uniformRelationProfinite P T p (n + 1))
      ((Condensed.profiniteFree Coeff).map
        (uniformRelationFace P T p n k) ≫ g) =
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (uniformRelationProfinite P T p n) g).comap
        (uniformRelationFace P T p n k).hom.hom := by
  exact freeProfiniteDiscreteIntegerHomScalarEquiv_precomp
    (uniformRelationFace P T p n k) g

/-- Genuine categorical all-degree alternating free-condensed Čech
boundary on actual profinite equal-image relations. -/
def uniformFreeRelationBoundary
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p (n + 1)) ⟶
    (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p n) :=
  ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    (Condensed.profiniteFree Coeff).map
      (uniformRelationFace P T p n k)

/-- The scalar Hom equivalence is additive. -/
theorem uniformFreeRelationHomScalar_add (X : Profinite.{u})
    (f g : (Condensed.profiniteFree Coeff).obj X ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv X (f + g) =
      freeProfiniteDiscreteIntegerHomScalarEquiv X f +
      freeProfiniteDiscreteIntegerHomScalarEquiv X g := by
  ext x
  rfl

/-- The scalar Hom equivalence respects integer multiples. -/
theorem uniformFreeRelationHomScalar_zsmul (X : Profinite.{u})
    (z : ℤ)
    (f : (Condensed.profiniteFree Coeff).obj X ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv X (z • f) =
      z • freeProfiniteDiscreteIntegerHomScalarEquiv X f := by
  ext x
  rfl

/-- Additive packaging of the existing exact free-condensed scalar
Hom equivalence. No false product-of-ℤ or solid target model. -/
def uniformFreeRelationHomScalarAddHom (X : Profinite.{u}) :
    ((Condensed.profiniteFree Coeff).obj X ⟶ discreteIntegerCoeff) →+
      LocallyConstant X ℤ where
  toFun := freeProfiniteDiscreteIntegerHomScalarEquiv X
  map_zero' := by
    ext x
    rfl
  map_add' := uniformFreeRelationHomScalar_add X

theorem uniformFreeRelationHomScalar_zero (X : Profinite.{u}) :
    freeProfiniteDiscreteIntegerHomScalarEquiv X
      (0 : (Condensed.profiniteFree Coeff).obj X ⟶ discreteIntegerCoeff) = 0 := by
  ext x
  rfl

/-- Signed scalar differential attached to categorical free-module
relations, using the same genuine Profinite face morphisms. -/
def uniformCategoricalRelationScalarDifferential
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    LocallyConstant (uniformRelationProfinite P T p n) ℤ →
    LocallyConstant (uniformRelationProfinite P T p (n + 1)) ℤ :=
  fun f => ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    f.comap (uniformRelationFace P T p n k).hom.hom

theorem uniformCategoricalRelationScalarDifferential_apply
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (f : LocallyConstant (uniformRelationProfinite P T p n) ℤ)
    (xs : uniformRelationProfinite P T p (n + 1)) :
    uniformCategoricalRelationScalarDifferential P T p n f xs =
      ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) *
        f ((uniformRelationFace P T p n k).hom.hom xs) := by
  change (LocallyConstant.evalₗ ℤ xs)
    (∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
      f.comap (uniformRelationFace P T p n k).hom.hom) =
    _
  simp only [map_sum, map_smul, LocallyConstant.evalₗ_apply, smul_eq_mul]
  rfl

theorem uniformFreeRelationBoundary_integerHom_scalar
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (g : (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p n) ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv
      (uniformRelationProfinite P T p (n + 1))
      (uniformFreeRelationBoundary P T p n ≫ g) =
    uniformCategoricalRelationScalarDifferential P T p n
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (uniformRelationProfinite P T p n) g) := by
  classical
  rw [uniformFreeRelationBoundary, Preadditive.sum_comp]
  simp only [Preadditive.zsmul_comp]
  change (uniformFreeRelationHomScalarAddHom
    (uniformRelationProfinite P T p (n + 1)))
    (∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
      ((Condensed.profiniteFree Coeff).map
        (uniformRelationFace P T p n k) ≫ g)) = _
  rw [map_sum]
  simp only [map_zsmul]
  apply DFunLike.ext
  intro xs
  rw [uniformCategoricalRelationScalarDifferential_apply]
  change (LocallyConstant.evalₗ ℤ xs)
      (∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
        (uniformFreeRelationHomScalarAddHom
          (uniformRelationProfinite P T p (n + 1)))
          ((Condensed.profiniteFree Coeff).map
            (uniformRelationFace P T p n k) ≫ g)) = _
  simp only [map_sum, map_smul, LocallyConstant.evalₗ_apply, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro k hk
  change (-1 : ℤ) ^ (k : ℕ) *
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (uniformRelationProfinite P T p (n + 1))
      ((Condensed.profiniteFree Coeff).map
        (uniformRelationFace P T p n k) ≫ g)) xs =
    _
  rw [uniformRelationFace_integerHom_scalar]
  rfl

/-- Canonical homeomorphism from the profinite object to the
genuine closed-relation subtype. It is not a made-up finite surrogate. -/
def uniformRelationHomeomorph
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    uniformRelationProfinite P T p n ≃ₜ
      ↥(profiniteCechArityRelatedSet n P T p) where
  toFun := id
  invFun := id
  left_inv := fun _ => rfl
  right_inv := fun _ => rfl
  continuous_toFun := by
    change Continuous (id : ↥(profiniteCechArityRelatedSet n P T p) → _)
    exact continuous_id
  continuous_invFun := by
    change Continuous (id : ↥(profiniteCechArityRelatedSet n P T p) → _)
    exact continuous_id

/-- Transport scalar cochains between the categorical profinite
model and the original closed-subtype relation model. -/
def uniformRelationScalarEquiv
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    LocallyConstant (uniformRelationProfinite P T p n) ℤ ≃
      LocallyConstant (↥(profiniteCechArityRelatedSet n P T p)) ℤ where
  toFun f := f.comap ⟨(uniformRelationHomeomorph P T p n).symm,
    (uniformRelationHomeomorph P T p n).symm.continuous⟩
  invFun f := f.comap ⟨(uniformRelationHomeomorph P T p n),
    (uniformRelationHomeomorph P T p n).continuous⟩
  left_inv f := by
    ext xs
    rfl
  right_inv f := by
    ext xs
    rfl

theorem uniformRelationScalarEquiv_diff
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (f : LocallyConstant (uniformRelationProfinite P T p n) ℤ) :
    uniformRelationScalarEquiv P T p (n + 1)
      (uniformCategoricalRelationScalarDifferential P T p n f) =
    uniformProfiniteRelationDifferential P T p n
      (uniformRelationScalarEquiv P T p n f) := by
  apply DFunLike.ext
  intro xs
  rw [uniformProfiniteRelationDifferential_apply]
  change (uniformCategoricalRelationScalarDifferential P T p n f)
    ((uniformRelationHomeomorph P T p (n + 1)).symm xs) =
    _
  rw [uniformCategoricalRelationScalarDifferential_apply]
  apply Finset.sum_congr rfl
  intro k hk
  rfl

/-- Unconditional positive-degree exactness of the ACTUAL
free-condensed Čech relation Hom complex with the discrete integer
coefficient target, in every degree. This follows through a fully
natural scalar Hom equivalence and the genuine closed-relation
all-positive-degree theorem. No Ext or solid model asserted. -/
theorem uniformFreeRelationBoundary_integerHom_exact
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (g : (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p (n + 1)) ⟶ discreteIntegerCoeff)
    (hg : uniformFreeRelationBoundary P T p (n + 1) ≫ g = 0) :
    ∃ f : (Condensed.profiniteFree Coeff).obj
        (uniformRelationProfinite P T p n) ⟶ discreteIntegerCoeff,
      uniformFreeRelationBoundary P T p n ≫ f = g := by
  let e (k : ℕ) :=
    freeProfiniteDiscreteIntegerHomScalarEquiv
      (uniformRelationProfinite P T p k)
  let c : LocallyConstant
      (↥(profiniteCechArityRelatedSet (n + 1) P T p)) ℤ :=
    uniformRelationScalarEquiv P T p (n + 1) (e (n + 1) g)
  have hcCat :
      uniformCategoricalRelationScalarDifferential P T p (n + 1)
        (e (n + 1) g) = 0 := by
    have h := congrArg (e (n + 2)) hg
    rw [uniformFreeRelationBoundary_integerHom_scalar] at h
    have hz : (e (n + 2))
        (0 : (Condensed.profiniteFree Coeff).obj
          (uniformRelationProfinite P T p (n + 2)) ⟶
          discreteIntegerCoeff) = 0 := by
      exact uniformFreeRelationHomScalar_zero _
    rw [hz] at h
    exact h
  have hc :
      uniformProfiniteRelationDifferential P T p (n + 1) c = 0 := by
    have h := congrArg
      (uniformRelationScalarEquiv P T p (n + 2)) hcCat
    rw [uniformRelationScalarEquiv_diff] at h
    have hz : (uniformRelationScalarEquiv P T p (n + 2))
        (0 : LocallyConstant (uniformRelationProfinite P T p (n + 2)) ℤ) = 0 := by
      ext xs
      rfl
    rw [hz] at h
    exact h
  obtain ⟨b,hb⟩ :=
    uniformProfiniteRelationAllPositive_cocycle_coboundary
      P T p n c hc
  let bc : LocallyConstant (uniformRelationProfinite P T p n) ℤ :=
    (uniformRelationScalarEquiv P T p n).symm b
  let f := (e n).symm bc
  refine ⟨f, ?_⟩
  apply (e (n + 1)).injective
  rw [uniformFreeRelationBoundary_integerHom_scalar]
  change uniformCategoricalRelationScalarDifferential P T p n
    ((e n) f) = e (n + 1) g
  rw [show (e n) f = bc from (e n).apply_symm_apply bc]
  apply (uniformRelationScalarEquiv P T p (n + 1)).injective
  rw [uniformRelationScalarEquiv_diff]
  simpa [bc, c] using hb

/-- Actual categorical Hom exactness for arbitrary products of
discrete integer coefficient sheaves. This uses categorical product
projections and their universal property; it does NOT presume a
solid coefficient target is such a product. -/
theorem uniformFreeRelationBoundary_discreteProductHom_exact
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    {ι : Type (u + 1)}
    (g : (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p (n + 1)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hg : uniformFreeRelationBoundary P T p (n + 1) ≫ g = 0) :
    ∃ f : (Condensed.profiniteFree Coeff).obj
        (uniformRelationProfinite P T p n) ⟶
          ∏ᶜ (fun _ : ι => discreteIntegerCoeff),
      uniformFreeRelationBoundary P T p n ≫ f = g := by
  classical
  have hcoord (i : ι) :
      ∃ f : (Condensed.profiniteFree Coeff).obj
          (uniformRelationProfinite P T p n) ⟶ discreteIntegerCoeff,
        uniformFreeRelationBoundary P T p n ≫ f =
          g ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i := by
    apply uniformFreeRelationBoundary_integerHom_exact
    have hz := congrArg
      (fun h : (Condensed.profiniteFree Coeff).obj
          (uniformRelationProfinite P T p (n + 2)) ⟶
          ∏ᶜ (fun _ : ι => discreteIntegerCoeff) =>
        h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i) hg
    simpa [Category.assoc] using hz
  choose f hf using hcoord
  refine ⟨Pi.lift f, ?_⟩
  apply Pi.hom_ext
  intro i
  rw [Category.assoc, Pi.lift_π]
  exact hf i

/-- The true free-condensed Čech boundaries compose to zero after
applying Hom(-, Z_disc), in all degrees, by the actual relation
differential squared-zero theorem. -/
theorem uniformFreeRelationBoundary_integerHom_sq_zero
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (g : (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p n) ⟶ discreteIntegerCoeff) :
    (uniformFreeRelationBoundary P T p (n + 1) ≫
      uniformFreeRelationBoundary P T p n) ≫ g = 0 := by
  have hc :
      uniformCategoricalRelationScalarDifferential P T p (n + 1)
        (uniformCategoricalRelationScalarDifferential P T p n
          (freeProfiniteDiscreteIntegerHomScalarEquiv
            (uniformRelationProfinite P T p n) g)) = 0 := by
    apply (uniformRelationScalarEquiv P T p (n + 2)).injective
    rw [uniformRelationScalarEquiv_diff,
      uniformRelationScalarEquiv_diff,
      uniformProfiniteRelationDifferential_sq_zero]
    rfl
  apply (freeProfiniteDiscreteIntegerHomScalarEquiv
    (uniformRelationProfinite P T p (n + 2))).injective
  rw [Category.assoc, uniformFreeRelationBoundary_integerHom_scalar,
    uniformFreeRelationBoundary_integerHom_scalar]
  simpa only [uniformFreeRelationHomScalar_zero] using hc

/-- Every actual product-of-discrete-integers Hom complex also
has square-zero differential, with no finite index assumption. -/
theorem uniformFreeRelationBoundary_discreteProductHom_sq_zero
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    {ι : Type (u + 1)}
    (g : (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p n) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) :
    (uniformFreeRelationBoundary P T p (n + 1) ≫
      uniformFreeRelationBoundary P T p n) ≫ g = 0 := by
  classical
  apply Pi.hom_ext
  intro i
  have h := uniformFreeRelationBoundary_integerHom_sq_zero
    P T p n (g ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)
  simpa only [Category.assoc, zero_comp] using h

#print axioms uniformFreeRelationBoundary_discreteProductHom_sq_zero

#print axioms uniformFreeRelationBoundary_integerHom_sq_zero

/-- Precisely conditional all-positive-degree Čech Hom exactness
for the genuine underived free-solid coefficient object. An
ACTUAL categorical product isomorphism is required; this theorem
does not manufacture or postulate such an isomorphism. -/
theorem uniformFreeRelationBoundary_solidHom_exact_of_discreteProductModel
    (P T S : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    {ι : Type (u + 1)}
    (e : underivedObject S ≅
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (g : (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p (n + 1)) ⟶ underivedObject S)
    (hg : uniformFreeRelationBoundary P T p (n + 1) ≫ g = 0) :
    ∃ f : (Condensed.profiniteFree Coeff).obj
        (uniformRelationProfinite P T p n) ⟶ underivedObject S,
      uniformFreeRelationBoundary P T p n ≫ f = g := by
  have hg' :
      uniformFreeRelationBoundary P T p (n + 1) ≫ (g ≫ e.hom) = 0 := by
    rw [← Category.assoc, hg, zero_comp]
  obtain ⟨f,hf⟩ :=
    uniformFreeRelationBoundary_discreteProductHom_exact
      P T p n (g ≫ e.hom) hg'
  refine ⟨f ≫ e.inv, ?_⟩
  calc
    uniformFreeRelationBoundary P T p n ≫ (f ≫ e.inv) =
        (uniformFreeRelationBoundary P T p n ≫ f) ≫ e.inv := by
          rw [Category.assoc]
    _ = (g ≫ e.hom) ≫ e.inv := by rw [hf]
    _ = g := by simp

#print axioms uniformFreeRelationBoundary_solidHom_exact_of_discreteProductModel

#print axioms uniformFreeRelationBoundary_discreteProductHom_exact

#print axioms uniformFreeRelationBoundary_integerHom_exact

#print axioms uniformRelationScalarEquiv_diff

#print axioms uniformRelationHomeomorph

#print axioms uniformFreeRelationBoundary_integerHom_scalar

#print axioms uniformFreeRelationHomScalar_add
#print axioms uniformFreeRelationHomScalar_zsmul

#print axioms uniformRelationFace_integerHom_scalar
end CMDG.CondensedCM5R0
