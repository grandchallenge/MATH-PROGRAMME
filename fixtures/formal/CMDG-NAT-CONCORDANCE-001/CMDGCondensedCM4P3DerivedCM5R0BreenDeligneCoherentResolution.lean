import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneLatticePseudocoherence

/-! Extract one infinite resolution from all finite partial resolutions.
The choice of each cover is independent of the requested future length,
because Schanuel comparison preserves all FP degrees of its kernel. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneFP
open CMDG.CondensedCM5R0.BreenDeligneFPApproximation
namespace CMDG.CondensedCM5R0.BreenDeligneCoherentResolution
universe v u
variable {C : Type u} [Category.{v} C] [Abelian C]
variable (D : FiniteClass C)

def AllFP (X : C) : Prop := ∀ k, FP D k X

structure Cover (X : C) where
  P : C
  finite : D.finite P
  e : P ⟶ X
  epi : Epi e

def chooseCover {X : C} (h : AllFP D X) : Cover D X :=
  Classical.choice (show Nonempty (Cover D X) from by
    obtain ⟨P,hP,e,he⟩ := h 0
    exact ⟨⟨P,hP,e,he⟩⟩)

theorem cover_kernel_all {X : C} (h : AllFP D X) :
    AllFP D (kernel (chooseCover D h).e) := by
  letI := (chooseCover D h).epi
  intro k
  exact fp_cover_kernel D _ (chooseCover D h).finite (h (k+1))

def stage (X : C) (h : AllFP D X) : ℕ → {Y : C // AllFP D Y}
  | 0 => ⟨X,h⟩
  | n+1 => ⟨kernel (chooseCover D (stage X h n).property).e,
      cover_kernel_all D (stage X h n).property⟩

variable {X : C} (h : AllFP D X)
abbrev term (n : ℕ) : C := (chooseCover D (stage D X h n).property).P
abbrev cover (n : ℕ) : term D h n ⟶ (stage D X h n).val :=
  (chooseCover D (stage D X h n).property).e

instance cover_epi (n : ℕ) : Epi (cover D h n) :=
  (chooseCover D (stage D X h n).property).epi

def aug : term D h 0 ⟶ X := cover D h 0
def d (n : ℕ) : term D h (n+1) ⟶ term D h n :=
  cover D h (n+1) ≫ kernel.ι (cover D h n)

theorem aug_zero : d D h 0 ≫ aug D h = 0 := by
  unfold d aug
  simp

theorem sq_zero (n : ℕ) : d D h (n+1) ≫ d D h n = 0 := by
  unfold d
  rw [Category.assoc, ← Category.assoc (kernel.ι (cover D h (n+1)))]
  simp

theorem aug_exact : (ShortComplex.mk (d D h 0) (aug D h) (aug_zero D h)).Exact := by
  apply (ShortComplex.exact_iff_epi_kernel_lift _).mpr
  have he : kernel.lift (aug D h) (d D h 0) (aug_zero D h) = cover D h 1 := by
    apply (cancel_mono (kernel.ι (aug D h))).mp
    simp [d,aug]
  rw [he]
  infer_instance

theorem exact (n : ℕ) :
    (ShortComplex.mk (d D h (n+1)) (d D h n) (sq_zero D h n)).Exact := by
  apply (ShortComplex.exact_iff_epi_kernel_lift _).mpr
  let e := kernelMonoCompIso (cover D h (n+1)) (kernel.ι (cover D h n))
  have he : kernel.lift (d D h n) (d D h (n+1)) (sq_zero D h n) ≫ e.hom =
      cover D h (n+2) := by
    apply (cancel_mono (kernel.ι (cover D h (n+1)))).mp
    simp [e,kernelMonoCompIso,d]
  haveI : Epi (kernel.lift (d D h n) (d D h (n+1)) (sq_zero D h n) ≫ e.hom) := by rw [he]; infer_instance
  exact (epi_comp_iff_of_isIso (kernel.lift (d D h n) (d D h (n+1)) (sq_zero D h n)) e.hom).mp inferInstance

open CMDG.CondensedCM5R0.BreenDeligneLatticeFP
open CMDG.CondensedCM5R0.BreenDeligneLatticePseudocoherence

theorem ordinary_finite (n : ℕ) : FinitePoly (term latFinite identity_fp n) :=
  (chooseCover latFinite (stage latFinite V identity_fp n).property).finite

#print axioms aug_exact
#print axioms exact
#print axioms ordinary_finite
end CMDG.CondensedCM5R0.BreenDeligneCoherentResolution
