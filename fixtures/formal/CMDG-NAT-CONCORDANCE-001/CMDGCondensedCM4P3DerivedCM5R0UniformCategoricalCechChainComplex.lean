import CMDGCondensedCM4P3DerivedCM5R0UniformCategoricalCechHom

/-!
# Genuine categorical Čech chain complex and its Stonean augmentation

This module proves that the ACTUAL free-condensed relation face maps
satisfy the simplicial identities, their alternating categorical
boundary squares to zero in all degrees, and hence they form an
honest chain complex. The real augmentation to F(T) kills the first
boundary, and for the protected canonical Stonean presentation the
augmentation is a genuine epimorphism.

**Not claimed:** exactness at all augmented internal chain terms,
a projective resolution, all-degree Ext vanishing, or derived solidity.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem uniformRelationFace_comp_swap
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (i : Fin (n + 2)) (j : Fin (n + 3)) :
    (uniformRelationFace P T p (n + 1) j) ≫
      (uniformRelationFace P T p n i) =
    (uniformRelationFace P T p (n + 1) (j.succAbove i)) ≫
      (uniformRelationFace P T p n (i.predAbove j)) := by
  ext xs
  apply Subtype.ext
  change i.removeNth (j.removeNth xs.val) =
      (i.predAbove j).removeNth
        ((j.succAbove i).removeNth xs.val)
  exact Fin.removeNth_removeNth_eq_swap xs.val i j

/-- The actual all-degree categorical free-condensed Čech
boundary squares to ZERO as a morphism of condensed modules, not
merely after applying a selected coefficient Hom functor. -/
theorem uniformFreeRelationBoundary_sq_zero
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    uniformFreeRelationBoundary P T p (n + 1) ≫
      uniformFreeRelationBoundary P T p n = 0 := by
  dsimp [uniformFreeRelationBoundary]
  simp only [Preadditive.comp_sum, Preadditive.sum_comp,
    ← Finset.sum_product']
  let IJ := Fin (n + 2) × Fin (n + 3)
  let S : Finset IJ := {ij : IJ | (ij.2 : ℕ) ≤ (ij.1 : ℕ)}
  rw [Finset.univ_product_univ, ← Finset.sum_add_sum_compl S,
    ← eq_neg_iff_add_eq_zero, ← Finset.sum_neg_distrib]
  let φ : ∀ ij : IJ, ij ∈ S → IJ := fun ij hij =>
    (Fin.castLT ij.2
      (lt_of_le_of_lt (Finset.mem_filter.mp hij).right
        (Fin.is_lt ij.1)), ij.1.succ)
  apply Finset.sum_bij φ
  · intro ij hij
    simp_rw [S, φ, Finset.compl_filter, Finset.mem_filter_univ,
      Fin.val_succ, Fin.val_castLT] at hij ⊢
    lia
  · rintro ⟨i, j⟩ hij ⟨i', j'⟩ hij' h
    rw [Prod.mk_inj]
    exact ⟨by simpa [φ] using! congr_arg Prod.snd h,
      by simpa [φ, Fin.castSucc_castLT] using!
        congr_arg Fin.castSucc (congr_arg Prod.fst h)⟩
  · rintro ⟨i', j'⟩ hij'
    simp_rw [S, Finset.compl_filter, Finset.mem_filter_univ, not_le] at hij'
    refine ⟨(j'.pred <| ?_, Fin.castSucc i'), ?_, ?_⟩
    · rintro rfl
      simp only [Fin.val_zero, not_lt_zero] at hij'
    · simpa [S] using! Nat.le_sub_one_of_lt hij'
    · simp only [φ, Fin.castLT_castSucc, Fin.succ_pred]
  · rintro ⟨i, j⟩ hij
    dsimp
    simp only [Preadditive.zsmul_comp, Preadditive.comp_zsmul,
      smul_smul, ← neg_smul]
    congr 1
    · simp only [φ, Fin.val_succ, pow_add, pow_one, mul_neg,
        neg_neg, mul_one]
      apply mul_comm
    · have hface := uniformRelationFace_comp_swap P T p n i j
      simp only [← Functor.map_comp] at ⊢
      simp only [φ]
      rw [hface]
      have hjval : (j : ℕ) ≤ (i : ℕ) :=
        (Finset.mem_filter.mp hij).2
      have hjle : j ≤ i.castSucc := Fin.le_iff_val_le_val.mpr hjval
      rw [Fin.predAbove_of_le_castSucc i j hjle,
        Fin.succAbove_of_le_castSucc j i hjle]
      rfl

/-- The genuine all-degree Čech complex of free condensed modules
attached to any profinite morphism p:P→T. No surrogate indices or
conditional square-zero hypotheses. -/
def uniformFreeRelationChainComplex
    (P T : Profinite.{u}) (p : P ⟶ T) :
    ChainComplex Ambient ℕ :=
  ChainComplex.of
    (fun n => (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p n))
    (uniformFreeRelationBoundary P T p)
    (uniformFreeRelationBoundary_sq_zero P T p)

/-- The genuine 0-th relation object (singletons) projects to P. -/
def uniformRelationProjection0
    (P T : Profinite.{u}) (p : P ⟶ T) :
    uniformRelationProfinite P T p 0 ⟶ P := by
  letI : CompactSpace (↥(profiniteCechArityRelatedSet 0 P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechArityRelatedSet_isClosed 0 P T p).isCompact
  exact CompHausLike.ofHom _
    (⟨fun xs => xs.val 0, by
      change Continuous
        (fun xs : ↥(profiniteCechArityRelatedSet 0 P T p) =>
          xs.val 0)
      exact (continuous_apply (0 : Fin 1)).comp
        continuous_subtype_val⟩)

def uniformFreeRelationAugmentation
    (P T : Profinite.{u}) (p : P ⟶ T) :
    (Condensed.profiniteFree Coeff).obj
      (uniformRelationProfinite P T p 0) ⟶
        (Condensed.profiniteFree Coeff).obj T :=
  (Condensed.profiniteFree Coeff).map
    (uniformRelationProjection0 P T p ≫ p)

theorem uniformRelationAugmentation_faces_agree
    (P T : Profinite.{u}) (p : P ⟶ T) :
    (uniformRelationFace P T p 0 (0 : Fin 2)) ≫
      (uniformRelationProjection0 P T p ≫ p) =
    (uniformRelationFace P T p 0 (1 : Fin 2)) ≫
      (uniformRelationProjection0 P T p ≫ p) := by
  ext xs
  have hp := xs.property (1 : Fin 2)
  simp only [ConcreteCategory.comp_apply]
  change p.hom.hom (xs.val 1) = p.hom.hom (xs.val 0)
  exact hp

/-- The genuine augmentation of the actual condensed-module Čech
chain complex kills the first boundary: no formal assumption of
augmentation exactness or epi is hidden here. -/
theorem uniformFreeRelationAugmentation_comp_boundary_zero
    (P T : Profinite.{u}) (p : P ⟶ T) :
    uniformFreeRelationBoundary P T p 0 ≫
      uniformFreeRelationAugmentation P T p = 0 := by
  unfold uniformFreeRelationBoundary uniformFreeRelationAugmentation
  rw [Fin.sum_univ_two]
  simp only [Fin.val_zero, pow_zero, one_smul, Fin.val_one,
    pow_one, neg_smul]
  rw [← sub_eq_add_neg]
  rw [Preadditive.sub_comp]
  simp only [← Functor.map_comp]
  rw [uniformRelationAugmentation_faces_agree]
  exact sub_self _

/-- The unique coordinate of the zero-th Čech relation gives
an inverse to the genuine singleton-coordinate projection. -/
def uniformRelationSingleton
    (P T : Profinite.{u}) (p : P ⟶ T) :
    P ⟶ uniformRelationProfinite P T p 0 := by
  letI : CompactSpace (↥(profiniteCechArityRelatedSet 0 P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechArityRelatedSet_isClosed 0 P T p).isCompact
  let f : C(P, ↥(profiniteCechArityRelatedSet 0 P T p)) :=
    ⟨fun x => ⟨fun _ : Fin 1 => x, by
        intro i
        rfl⟩, by
      apply Continuous.subtype_mk
      apply continuous_pi
      intro i
      exact continuous_id⟩
  exact CompHausLike.ofHom _ f

theorem uniformRelationSingleton_projection
    (P T : Profinite.{u}) (p : P ⟶ T) :
    uniformRelationSingleton P T p ≫
      uniformRelationProjection0 P T p = 𝟙 P := by
  ext x
  simp only [ConcreteCategory.comp_apply, ConcreteCategory.id_apply]
  rfl

theorem uniformRelationProjection_singleton
    (P T : Profinite.{u}) (p : P ⟶ T) :
    uniformRelationProjection0 P T p ≫
      uniformRelationSingleton P T p =
        𝟙 (uniformRelationProfinite P T p 0) := by
  ext xs
  simp only [ConcreteCategory.comp_apply, ConcreteCategory.id_apply]
  apply Subtype.ext
  funext i
  fin_cases i
  rfl

def uniformRelationProjection0Iso
    (P T : Profinite.{u}) (p : P ⟶ T) :
    uniformRelationProfinite P T p 0 ≅ P where
  hom := uniformRelationProjection0 P T p
  inv := uniformRelationSingleton P T p
  hom_inv_id := uniformRelationProjection_singleton P T p
  inv_hom_id := uniformRelationSingleton_projection P T p

/-- Whenever the original free-module map F(P)→F(T) is epi,
the genuine degree-zero Čech augmentation is epi. -/
theorem uniformFreeRelationAugmentation_epi_of_freeMap_epi
    (P T : Profinite.{u}) (p : P ⟶ T)
    [Epi ((Condensed.profiniteFree Coeff).map p)] :
    Epi (uniformFreeRelationAugmentation P T p) := by
  haveI : IsIso (uniformRelationProjection0 P T p) :=
    (uniformRelationProjection0Iso P T p).isIso_hom
  unfold uniformFreeRelationAugmentation
  rw [Functor.map_comp]
  infer_instance

/-- The augmented free-condensed relation chain complex for the
canonical Stonean presentation begins with a genuine epi to F(T).
This is a *first-stage* exactness result, not higher exactness. -/
theorem uniformFreeStoneanRelationAugmentation_epi
    (T : Profinite.{u}) :
    Epi (uniformFreeRelationAugmentation
      (Stonean.toProfinite.obj T.presentation) T
        (Profinite.presentation.π T)) := by
  letI : Epi ((Condensed.profiniteFree Coeff).map
      (Profinite.presentation.π T)) :=
    freeStoneanPresentationMap_epi T
  exact uniformFreeRelationAugmentation_epi_of_freeMap_epi
    (Stonean.toProfinite.obj T.presentation) T
    (Profinite.presentation.π T)

#print axioms uniformFreeStoneanRelationAugmentation_epi

#print axioms uniformRelationProjection0Iso

#print axioms uniformFreeRelationAugmentation_comp_boundary_zero

#print axioms uniformRelationAugmentation_faces_agree

#print axioms uniformFreeRelationChainComplex

#print axioms uniformFreeRelationBoundary_sq_zero

#print axioms uniformRelationFace_comp_swap
end CMDG.CondensedCM5R0
