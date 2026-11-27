import CMDGCondensedCM4P3DerivedCM5R0CompactCoverGeometry

/-! The genuine compact-cover free-condensed Čech complex,
with all internal terms exact. The target of the cover is an
arbitrary compact Hausdorff object, not a profinite surrogate. -/
noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0.CompactCover

def compactFreeRelationBoundary
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    (Condensed.profiniteFree Coeff).obj
      (compactRelationProfinite P T p (n + 1)) ⟶
    (Condensed.profiniteFree Coeff).obj
      (compactRelationProfinite P T p n) :=
  ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    (Condensed.profiniteFree Coeff).map
      (compactRelationFace P T p n k)

theorem compactRelationFace_comp_swap
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ)
    (i : Fin (n + 2)) (j : Fin (n + 3)) :
    (compactRelationFace P T p (n + 1) j) ≫
      (compactRelationFace P T p n i) =
    (compactRelationFace P T p (n + 1) (j.succAbove i)) ≫
      (compactRelationFace P T p n (i.predAbove j)) := by
  ext xs
  apply Subtype.ext
  change i.removeNth (j.removeNth xs.val) =
      (i.predAbove j).removeNth
        ((j.succAbove i).removeNth xs.val)
  exact Fin.removeNth_removeNth_eq_swap xs.val i j

/-- The actual all-degree categorical free-condensed Čech
boundary squares to ZERO as a morphism of condensed modules, not
merely after applying a selected coefficient Hom functor. -/
theorem compactFreeRelationBoundary_sq_zero
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    compactFreeRelationBoundary P T p (n + 1) ≫
      compactFreeRelationBoundary P T p n = 0 := by
  dsimp [compactFreeRelationBoundary]
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
    · have hface := compactRelationFace_comp_swap P T p n i j
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
def compactFreeRelationChainComplex
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    ChainComplex Ambient ℕ :=
  ChainComplex.of
    (fun n => (Condensed.profiniteFree Coeff).obj
      (compactRelationProfinite P T p n))
    (compactFreeRelationBoundary P T p)
    (compactFreeRelationBoundary_sq_zero P T p)

def compactPresheafRelationBoundary
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    freeCompHausModulePresheaf (compactRelationProfinite P T p (n + 1)) ⟶
      freeCompHausModulePresheaf (compactRelationProfinite P T p n) :=
  ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    freeCompHausModulePresheafFunctor.map
      (compactRelationFace P T p n k)

theorem compactPresheafRelationBoundary_sq_zero
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    compactPresheafRelationBoundary P T p (n + 1) ≫
      compactPresheafRelationBoundary P T p n = 0 := by
  dsimp [compactPresheafRelationBoundary]
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
    · have hface := compactRelationFace_comp_swap P T p n i j
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
          (compactRelationFace P T p (n + 1) j) ≫
          freeCompHausModulePresheafFunctor.map
            (compactRelationFace P T p n i) =
        freeCompHausModulePresheafFunctor.map
          (compactRelationFace P T p (n + 1) i.succ) ≫
          freeCompHausModulePresheafFunctor.map
            (compactRelationFace P T p n
              (Fin.castLT j (lt_of_le_of_lt hjval (Fin.is_lt i))))
      simpa only [Functor.map_comp] using hmap


/-- Sheafification of the true degree-n CompHaus free
presheaf Čech boundary IS the genuine categorical condensed
free-module boundary, for every n without a degree cap. -/
theorem compactPresheafRelationBoundary_sheafify
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    moduleSheafification.map (compactPresheafRelationBoundary P T p n) =
      compactFreeRelationBoundary P T p n := by
  unfold compactPresheafRelationBoundary compactFreeRelationBoundary
  rw [Functor.map_sum]
  simp only [Functor.map_zsmul]
  congr 1

/-- The actual degree-n short complex of free CompHaus-site
representable presheaves, with genuine face maps. -/
def compactPresheafRelationShortComplex
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    ShortComplex (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (compactPresheafRelationBoundary P T p (n + 1))
    (compactPresheafRelationBoundary P T p n)
    (compactPresheafRelationBoundary_sq_zero P T p n)

/-- Exact Stonean-restricted free-representable presheaf short
complex transfers via exact Stonean sheafification and the
natural dense-site equivalence to the genuine categorical free
condensed Čech complex. Assumption is precisely source-level
Stonean presheaf exactness; not a coefficient-Hom surrogate. -/
theorem compactRelationShortExact_of_stoneanPresheafExact
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ)
    (h : ((compactPresheafRelationShortComplex P T p n).map
      stoneanPresheafRestriction).Exact) :
    (ShortComplex.mk
      (compactFreeRelationBoundary P T p (n + 1))
      (compactFreeRelationBoundary P T p n)
      (compactFreeRelationBoundary_sq_zero P T p n)).Exact := by
  let S := compactPresheafRelationShortComplex P T p n
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
      kernel.ι (compactFreeRelationBoundary P T p n) ≫
      cokernel.π (compactFreeRelationBoundary P T p (n + 1)) = 0 := by
    rw [← compactPresheafRelationBoundary_sheafify P T p n,
      ← compactPresheafRelationBoundary_sheafify P T p (n + 1)]
    exact hZero
  exact ((ShortComplex.mk
    (compactFreeRelationBoundary P T p (n + 1))
    (compactFreeRelationBoundary P T p n)
    (compactFreeRelationBoundary_sq_zero P T p n)).exact_iff_kernel_ι_comp_cokernel_π_zero).2 hZero'

theorem compactProbePresheafFace_eval
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ) (k : Fin (n + 2)) :
    (freeCompHausModulePresheafFunctor.map
      (compactRelationFace P T p n k)).app
        (Opposite.op U.compHaus) =
    (ModuleCat.free Coeff).map
      (↾compactProbeFace U P T p n k) := by
  rfl

theorem compactStoneanRestrictedPresheafExact
    (P : Profinite.{u}) (T : CompHaus.{u})
    (p : profiniteToCompHaus.obj P ⟶ T) [Epi p] (n : ℕ) :
    ((compactPresheafRelationShortComplex P T p n).map
        stoneanPresheafRestriction).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro U
  let Q := ((compactPresheafRelationShortComplex P T p n).map
      stoneanPresheafRestriction).map
        ((evaluation Stoneanᵒᵖ (ModuleCat Coeff)).obj U)
  let W := compactProbeBarShortComplex U.unop P T p n
  have hf : Q.f = W.f := by
    change (compactPresheafRelationBoundary P T p (n + 1)).app
        (Opposite.op U.unop.compHaus) = compactProbeBarD U.unop P T p (n + 1)
    unfold compactPresheafRelationBoundary compactProbeBarD
    rw [NatTrans.app_sum]
    simp only [NatTrans.app_zsmul]
    apply Finset.sum_congr rfl
    intro k hk
    rw [compactProbePresheafFace_eval U.unop P T p (n + 1) k]
  have hg : Q.g = W.g := by
    change (compactPresheafRelationBoundary P T p n).app
        (Opposite.op U.unop.compHaus) = compactProbeBarD U.unop P T p n
    unfold compactPresheafRelationBoundary compactProbeBarD
    rw [NatTrans.app_sum]
    simp only [NatTrans.app_zsmul]
    apply Finset.sum_congr rfl
    intro k hk
    rw [compactProbePresheafFace_eval U.unop P T p n k]
  have hW : W.Exact := compactProbeBarExact U.unop P T p n
  change Q.Exact
  apply (Q.exact_iff_kernel_ι_comp_cokernel_π_zero).2
  rw [hf, hg]
  exact (W.exact_iff_kernel_ι_comp_cokernel_π_zero).1 hW

theorem compactFreeCechInternalExact (P : Profinite.{u}) (T : CompHaus.{u})
    (p : profiniteToCompHaus.obj P ⟶ T) [Epi p] (n : ℕ) :
    (ShortComplex.mk (compactFreeRelationBoundary P T p (n + 1))
      (compactFreeRelationBoundary P T p n)
      (compactFreeRelationBoundary_sq_zero P T p n)).Exact :=
  compactRelationShortExact_of_stoneanPresheafExact P T p n
    (compactStoneanRestrictedPresheafExact P T p n)

#print axioms compactFreeRelationChainComplex
#print axioms compactFreeCechInternalExact
end CMDG.CondensedCM5R0.CompactCover
