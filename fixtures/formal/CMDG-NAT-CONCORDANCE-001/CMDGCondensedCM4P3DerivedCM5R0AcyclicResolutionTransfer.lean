import CMDGCondensedCM4P3DerivedCM5R0CoproductExt

/-! Actual all-degree acyclic-resolution comparison using Yoneda
dimension shifting. No spectral sequence API, projectivity of the
terms, or exchange of inverse limits with homology is assumed. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.AcyclicResolution

structure Resolution where
  target : Ambient.{u}
  term : ℕ → Ambient.{u}
  aug : term 0 ⟶ target
  d : (n : ℕ) → term (n+1) ⟶ term n
  aug_zero : d 0 ≫ aug = 0
  sq_zero : ∀ n, d (n+1) ≫ d n = 0
  aug_epi : Epi aug
  aug_exact : (ShortComplex.mk (d 0) aug aug_zero).Exact
  exact : ∀ n, (ShortComplex.mk (d (n+1)) (d n) (sq_zero n)).Exact

variable (R : Resolution.{u})

def syzygy : ℕ → Ambient.{u}
  | 0 => kernel R.aug
  | n+1 => kernel (R.d n)

def inclusion : (n : ℕ) → syzygy R n ⟶ R.term n
  | 0 => kernel.ι R.aug
  | n+1 => kernel.ι (R.d n)

def cover : (n : ℕ) → R.term (n+1) ⟶ syzygy R n
  | 0 => kernel.lift R.aug (R.d 0) R.aug_zero
  | n+1 => kernel.lift (R.d n) (R.d (n+1)) (R.sq_zero n)

theorem cover_inclusion (n : ℕ) : cover R n ≫ inclusion R n = R.d n := by
  cases n <;> exact kernel.lift_ι _ _ _

theorem inclusion_mono (n : ℕ) : Mono (inclusion R n) := by
  cases n with
  | zero => change Mono (kernel.ι R.aug); infer_instance
  | succ n => change Mono (kernel.ι (R.d n)); infer_instance

theorem cover_epi (n : ℕ) : Epi (cover R n) := by
  cases n with
  | zero => exact ((ShortComplex.mk (R.d 0) R.aug R.aug_zero).exact_iff_epi_kernel_lift).mp R.aug_exact
  | succ n => exact ((ShortComplex.mk (R.d (n+1)) (R.d n) (R.sq_zero n)).exact_iff_epi_kernel_lift).mp (R.exact n)

theorem inclusion_cover_zero (n : ℕ) : inclusion R (n+1) ≫ cover R n = 0 := by
  letI := inclusion_mono R n
  apply (cancel_mono (inclusion R n)).1
  rw [Category.assoc,cover_inclusion,zero_comp]
  exact kernel.condition (R.d n)

theorem syzygy_shortExact (n : ℕ) :
    (ShortComplex.mk (inclusion R (n+1)) (cover R n)
      (inclusion_cover_zero R n)).ShortExact := by
  letI := cover_epi R n
  letI := inclusion_mono R n
  letI := inclusion_mono R (n+1)
  have hlim : IsLimit (KernelFork.ofι (inclusion R (n+1))
      (inclusion_cover_zero R n)) :=
    isKernelOfComp (f:=cover R n) (inclusion R n) (R.d n)
      (kernelIsKernel (R.d n)) (inclusion_cover_zero R n) (cover_inclusion R n)
  exact ⟨(ShortComplex.mk (inclusion R (n+1)) (cover R n)
    (inclusion_cover_zero R n)).exact_of_f_is_kernel hlim⟩

theorem aug_shortExact :
    (ShortComplex.mk (inclusion R 0) R.aug (kernel.condition R.aug)).ShortExact := by
  letI := R.aug_epi
  change (ShortComplex.mk (kernel.ι R.aug) R.aug (kernel.condition R.aug)).ShortExact
  exact ⟨ShortComplex.exact_kernel R.aug⟩

variable (G : Ambient.{u})

def HomExact : Prop :=
  ∀ (n : ℕ) (f : R.term (n+1) ⟶ G), R.d (n+1) ≫ f = 0 →
    ∃ g : R.term n ⟶ G, R.d n ≫ g = f

def TermAcyclic : Prop :=
  ∀ (n q : ℕ) (e : Abelian.Ext (R.term n) G (q+1)), e=0

theorem syzygy_hom_extends (h : HomExact R G) (n : ℕ)
    (f : syzygy R n ⟶ G) :
    ∃ g : R.term n ⟶ G, inclusion R n ≫ g = f := by
  letI := cover_epi R n
  have hz : R.d (n+1) ≫ cover R n = 0 := by
    letI := inclusion_mono R n
    apply (cancel_mono (inclusion R n)).1
    rw [Category.assoc,cover_inclusion,zero_comp]
    exact R.sq_zero n
  have hc : R.d (n+1) ≫ (cover R n ≫ f) = 0 := by
    rw [← Category.assoc,hz,zero_comp]
  obtain ⟨g,hg⟩ := h n (cover R n ≫ f) hc
  refine ⟨g,(cancel_epi (cover R n)).1 ?_⟩
  rw [← Category.assoc,cover_inclusion,hg]

theorem syzygy_extZero (ht : TermAcyclic R G) (hh : HomExact R G) (q : ℕ) :
    ∀ (n : ℕ) (e : Abelian.Ext (syzygy R n) G (q+1)), e=0 := by
  induction q with
  | zero =>
    intro n
    exact shortExact_extOne_right_zero_of_hom_extensions _
      (syzygy_shortExact R n) G (ht (n+1) 0) (syzygy_hom_extends R G hh (n+1))
  | succ q ih =>
    intro n
    exact shortExact_extSucc_right_zero _ (syzygy_shortExact R n) G q
      (ih (n+1)) (ht (n+1) (q+1))

/-- Every positive Ext class out of the genuine augmented target
vanishes under term acyclicity and positive Hom exactness. -/
theorem target_extZero (ht : TermAcyclic R G) (hh : HomExact R G) (q : ℕ) :
    ∀ e : Abelian.Ext R.target G (q+1), e=0 := by
  cases q with
  | zero =>
    exact shortExact_extOne_right_zero_of_hom_extensions _
      (aug_shortExact R) G (ht 0 0) (syzygy_hom_extends R G hh 0)
  | succ q =>
    exact shortExact_extSucc_right_zero _ (aug_shortExact R) G q
      (syzygy_extZero R G ht hh q 0) (ht 0 (q+1))

#print axioms syzygy_shortExact
#print axioms target_extZero
end CMDG.CondensedCM5R0.AcyclicResolution
