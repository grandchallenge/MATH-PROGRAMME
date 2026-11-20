import CMDGCondensedCM4P3DerivedCM5R0UniformCategoricalCechChainComplex
import CMDGCondensedCM4P3DerivedCM5R0DenseExactnessTransfer

/-!
# General all-degree genuine presheaf relation Čech complex

Construct exact face/sign comparison for the genuine free CompHaus
module presheaf in all degrees and record a source-independent
Stonean restriction exactness transfer. The missing external
objectwise Stonean-bar comparison is separately exposed rather
than assumed or circumvented.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

/-- The actual finite-arity CompHaus free-representable
presheaf boundary (before sheafification). -/
def uniformPresheafRelationBoundary
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    freeCompHausModulePresheaf (uniformRelationProfinite P T p (n + 1)) ⟶
      freeCompHausModulePresheaf (uniformRelationProfinite P T p n) :=
  ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    freeCompHausModulePresheafFunctor.map
      (uniformRelationFace P T p n k)

theorem uniformPresheafRelationBoundary_sq_zero
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    uniformPresheafRelationBoundary P T p (n + 1) ≫
      uniformPresheafRelationBoundary P T p n = 0 := by
  dsimp [uniformPresheafRelationBoundary]
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
      simp only [φ]
      have hjval : (j : ℕ) ≤ (i : ℕ) :=
        (Finset.mem_filter.mp hij).2
      have hjle : j ≤ i.castSucc := Fin.le_iff_val_le_val.mpr hjval
      have hidx : i.predAbove j =
          Fin.castLT j (lt_of_le_of_lt hjval (Fin.is_lt i)) := by
        rw [Fin.predAbove_of_le_castSucc i j hjle]
        apply Fin.ext
        rfl
      have hidx' : j.succAbove i = i.succ :=
        Fin.succAbove_of_le_castSucc j i hjle
      rw [hidx, hidx'] at hface
      have hmap := congrArg
        (fun m => freeCompHausModulePresheafFunctor.map m) hface
      change freeCompHausModulePresheafFunctor.map
          (uniformRelationFace P T p (n + 1) j) ≫
          freeCompHausModulePresheafFunctor.map
            (uniformRelationFace P T p n i) =
        freeCompHausModulePresheafFunctor.map
          (uniformRelationFace P T p (n + 1) i.succ) ≫
          freeCompHausModulePresheafFunctor.map
            (uniformRelationFace P T p n
              (Fin.castLT j (lt_of_le_of_lt hjval (Fin.is_lt i))))
      simpa only [Functor.map_comp] using hmap


/-- Sheafification of the true degree-n CompHaus free
presheaf Čech boundary IS the genuine categorical condensed
free-module boundary, for every n without a degree cap. -/
theorem uniformPresheafRelationBoundary_sheafify
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    moduleSheafification.map (uniformPresheafRelationBoundary P T p n) =
      uniformFreeRelationBoundary P T p n := by
  unfold uniformPresheafRelationBoundary uniformFreeRelationBoundary
  rw [Functor.map_sum]
  simp only [Functor.map_zsmul]
  congr 1

/-- The actual degree-n short complex of free CompHaus-site
representable presheaves, with genuine face maps. -/
def uniformPresheafRelationShortComplex
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    ShortComplex (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (uniformPresheafRelationBoundary P T p (n + 1))
    (uniformPresheafRelationBoundary P T p n)
    (uniformPresheafRelationBoundary_sq_zero P T p n)

/-- Exact Stonean-restricted free-representable presheaf short
complex transfers via exact Stonean sheafification and the
natural dense-site equivalence to the genuine categorical free
condensed Čech complex. Assumption is precisely source-level
Stonean presheaf exactness; not a coefficient-Hom surrogate. -/
theorem uniformRelationShortExact_of_stoneanPresheafExact
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (h : ((uniformPresheafRelationShortComplex P T p n).map
      stoneanPresheafRestriction).Exact) :
    (ShortComplex.mk
      (uniformFreeRelationBoundary P T p (n + 1))
      (uniformFreeRelationBoundary P T p n)
      (uniformFreeRelationBoundary_sq_zero P T p n)).Exact := by
  let S := uniformPresheafRelationShortComplex P T p n
  let R := stoneanPresheafRestriction
  let A := stoneanModuleSheafification
  let E := (Condensed.StoneanCompHaus.equivalence
    (ModuleCat Coeff)).inverse
  haveI : PreservesFiniteLimits A := by
    change PreservesFiniteLimits
      (presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff))
    infer_instance
  haveI : PreservesFiniteColimits A := by
    change PreservesFiniteColimits
      (presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff))
    infer_instance
  have hStonean : ((S.map R).map A).Exact := h.map A
  have hStonean' : (S.map (R ⋙ A)).Exact := by
    simpa only [ShortComplex.map_comp] using hStonean
  have hTransport :
      (S.map (moduleSheafification ⋙ E)).Exact :=
    ShortComplex.exact_of_iso
      (S.mapNatIso stoneanCompHausSheafificationCompatibility)
      hStonean'
  have hTransport' :
      ((S.map moduleSheafification).map E).Exact := by
    simpa only [ShortComplex.map_comp] using hTransport
  have hComp : (S.map moduleSheafification).Exact :=
    E.reflects_exact_of_faithful _ hTransport'
  have hZero :
      kernel.ι ((S.map moduleSheafification).g) ≫
      cokernel.π ((S.map moduleSheafification).f) = 0 :=
    ((S.map moduleSheafification).exact_iff_kernel_ι_comp_cokernel_π_zero).1 hComp
  have hZero' :
      kernel.ι (uniformFreeRelationBoundary P T p n) ≫
      cokernel.π (uniformFreeRelationBoundary P T p (n + 1)) = 0 := by
    rw [← uniformPresheafRelationBoundary_sheafify P T p n,
      ← uniformPresheafRelationBoundary_sheafify P T p (n + 1)]
    exact hZero
  exact ((ShortComplex.mk
    (uniformFreeRelationBoundary P T p (n + 1))
    (uniformFreeRelationBoundary P T p n)
    (uniformFreeRelationBoundary_sq_zero P T p n)).exact_iff_kernel_ι_comp_cokernel_π_zero).2 hZero'

#print axioms uniformPresheafRelationBoundary_sq_zero
#print axioms uniformPresheafRelationBoundary_sheafify
#print axioms uniformRelationShortExact_of_stoneanPresheafExact
end CMDG.CondensedCM5R0
