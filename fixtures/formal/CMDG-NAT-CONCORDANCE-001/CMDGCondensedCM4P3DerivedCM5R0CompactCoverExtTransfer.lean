import CMDGCondensedCM4P3DerivedCM5R0CompactCoverScalarHom

/-! Dimension shifting for the actual compact-cover resolution.
The only remaining premise is exactness of the actual scalar Čech cochains.
No projectivity assumption on the relation terms. -/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.CompactCover

variable (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)

abbrev term (n : ℕ) : Ambient :=
  (Condensed.profiniteFree Coeff).obj (compactRelationProfinite P T p n)
abbrev d (n : ℕ) : term P T p (n+1) ⟶ term P T p n :=
  compactFreeRelationBoundary P T p n
abbrev aug : term P T p 0 ⟶ compactFreeFunctor.obj T :=
  compactFreeRelationAugmentation P T p

def syzygy : ℕ → Ambient
  | 0 => kernel (aug P T p)
  | n+1 => kernel (d P T p n)

def syzygyι : (n : ℕ) → syzygy P T p n ⟶ term P T p n
  | 0 => kernel.ι (aug P T p)
  | n+1 => kernel.ι (d P T p n)

def syzygyCover : (n : ℕ) → term P T p (n+1) ⟶ syzygy P T p n
  | 0 => kernel.lift (aug P T p) (d P T p 0)
      (compactFreeRelationAugmentation_comp_boundary_zero P T p)
  | n+1 => kernel.lift (d P T p n) (d P T p (n+1))
      (compactFreeRelationBoundary_sq_zero P T p n)

theorem cover_comp_ι (n : ℕ) :
    syzygyCover P T p n ≫ syzygyι P T p n = d P T p n := by
  cases n <;> exact kernel.lift_ι _ _ _

theorem syzygyι_mono (n : ℕ) : Mono (syzygyι P T p n) := by
  cases n with
  | zero => change Mono (kernel.ι (aug P T p)); infer_instance
  | succ n => change Mono (kernel.ι (d P T p n)); infer_instance

variable [Epi p]

theorem cover_epi (n : ℕ) : Epi (syzygyCover P T p n) := by
  cases n with
  | zero =>
    let S := ShortComplex.mk (d P T p 0) (aug P T p)
      (compactFreeRelationAugmentation_comp_boundary_zero P T p)
    exact (S.exact_iff_epi_kernel_lift).mp (compactFreeCechAugmentationExact P T p)
  | succ n =>
    let S := ShortComplex.mk (d P T p (n+1)) (d P T p n)
      (compactFreeRelationBoundary_sq_zero P T p n)
    exact (S.exact_iff_epi_kernel_lift).mp (compactFreeCechInternalExact P T p n)

omit [Epi p] in
theorem ι_comp_cover_zero (n : ℕ) :
    syzygyι P T p (n+1) ≫ syzygyCover P T p n = 0 := by
  letI := syzygyι_mono P T p n
  apply (cancel_mono (syzygyι P T p n)).1
  rw [Category.assoc, cover_comp_ι, zero_comp]
  exact kernel.condition (d P T p n)

theorem syzygy_shortExact (n : ℕ) :
    (ShortComplex.mk (syzygyι P T p (n+1)) (syzygyCover P T p n)
      (ι_comp_cover_zero P T p n)).ShortExact := by
  letI := cover_epi P T p n
  letI := syzygyι_mono P T p n
  letI := syzygyι_mono P T p (n+1)
  have hlim : IsLimit (KernelFork.ofι (syzygyι P T p (n+1))
      (ι_comp_cover_zero P T p n)) :=
    isKernelOfComp (f := syzygyCover P T p n)
      (syzygyι P T p n) (d P T p n) (kernelIsKernel (d P T p n))
      (ι_comp_cover_zero P T p n) (cover_comp_ι P T p n)
  exact ShortComplex.ShortExact.mk
    ((ShortComplex.mk (syzygyι P T p (n+1)) (syzygyCover P T p n)
      (ι_comp_cover_zero P T p n)).exact_of_f_is_kernel hlim)

theorem aug_shortExact :
    (ShortComplex.mk (syzygyι P T p 0) (aug P T p)
      (kernel.condition (aug P T p))).ShortExact := by
  letI := compactFreeCechAugmentationEpi P T p
  change (ShortComplex.mk (kernel.ι (aug P T p)) (aug P T p)
    (kernel.condition (aug P T p))).ShortExact
  exact ShortComplex.ShortExact.mk (ShortComplex.exact_kernel (aug P T p))

def scalarExact : Prop :=
  ∀ (n : ℕ) (c : LocallyConstant (compactRelationProfinite P T p (n+1)) ℤ),
    compactCategoricalRelationScalarDifferential P T p (n+1) c = 0 →
    ∃ b : LocallyConstant (compactRelationProfinite P T p n) ℤ,
      compactCategoricalRelationScalarDifferential P T p n b = c

omit [Epi p] in
theorem hom_exact_of_scalarExact (h : scalarExact P T p)
    (n : ℕ) (f : term P T p (n+1) ⟶ discreteIntegerCoeff)
    (hf : d P T p (n+1) ≫ f = 0) :
    ∃ g : term P T p n ⟶ discreteIntegerCoeff, d P T p n ≫ g = f := by
  let E := freeProfiniteDiscreteIntegerHomScalarEquiv
      (compactRelationProfinite P T p (n+1))
  have hc : compactCategoricalRelationScalarDifferential P T p (n+1) (E f) = 0 := by
    rw [← compactFreeRelationBoundary_integerHom_scalar, hf]
    exact map_zero (uniformFreeRelationHomScalarAddHom _)
  obtain ⟨b,hb⟩ := h n (E f) hc
  obtain ⟨g,hg⟩ := (freeProfiniteDiscreteIntegerHomScalarEquiv
      (compactRelationProfinite P T p n)).surjective b
  refine ⟨g,E.injective ?_⟩
  change freeProfiniteDiscreteIntegerHomScalarEquiv _ (d P T p n ≫ g) = E f
  rw [compactFreeRelationBoundary_integerHom_scalar, hg, hb]

theorem syzygy_hom_extends (h : scalarExact P T p) (n : ℕ)
    (f : syzygy P T p n ⟶ discreteIntegerCoeff) :
    ∃ g : term P T p n ⟶ discreteIntegerCoeff, syzygyι P T p n ≫ g = f := by
  letI := cover_epi P T p n
  have hz : d P T p (n+1) ≫ syzygyCover P T p n = 0 := by
    letI := syzygyι_mono P T p n
    apply (cancel_mono (syzygyι P T p n)).1
    rw [Category.assoc, cover_comp_ι, zero_comp]
    exact compactFreeRelationBoundary_sq_zero P T p n
  have hc : d P T p (n+1) ≫ (syzygyCover P T p n ≫ f) = 0 := by
    rw [← Category.assoc, hz, zero_comp]
  obtain ⟨g,hg⟩ := hom_exact_of_scalarExact P T p h n
    (syzygyCover P T p n ≫ f) hc
  refine ⟨g,(cancel_epi (syzygyCover P T p n)).1 ?_⟩
  rw [← Category.assoc, cover_comp_ι, hg]

theorem syzygy_extPositive_zero_of_scalarExact (h : scalarExact P T p) (q : ℕ) :
    ∀ (n : ℕ) (e : Abelian.Ext (syzygy P T p n) discreteIntegerCoeff (q+1)), e = 0 := by
  induction q with
  | zero =>
    intro n
    apply shortExact_extOne_right_zero_of_hom_extensions _ (syzygy_shortExact P T p n)
    · exact freeProfinite_extPositive_scalar_zero _ 0
    · exact syzygy_hom_extends P T p h (n+1)
  | succ q ih =>
    intro n
    apply shortExact_extSucc_right_zero _ (syzygy_shortExact P T p n) _ q
    · exact ih (n+1)
    · exact freeProfinite_extPositive_scalar_zero _ (q+1)

theorem compactFree_extPositive_zero_of_scalarExact (h : scalarExact P T p) (q : ℕ) :
    ∀ e : Abelian.Ext (compactFreeFunctor.obj T) discreteIntegerCoeff (q+1), e = 0 := by
  cases q with
  | zero =>
    apply shortExact_extOne_right_zero_of_hom_extensions _ (aug_shortExact P T p)
    · exact freeProfinite_extPositive_scalar_zero _ 0
    · exact syzygy_hom_extends P T p h 0
  | succ q =>
    apply shortExact_extSucc_right_zero _ (aug_shortExact P T p) _ q
    · exact syzygy_extPositive_zero_of_scalarExact P T p h q 0
    · exact freeProfinite_extPositive_scalar_zero _ (q+1)

#print axioms hom_exact_of_scalarExact
#print axioms syzygy_shortExact
#print axioms compactFree_extPositive_zero_of_scalarExact
end CMDG.CondensedCM5R0.CompactCover
