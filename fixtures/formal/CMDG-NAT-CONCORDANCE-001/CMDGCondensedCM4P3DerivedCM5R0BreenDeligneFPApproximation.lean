import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFPClosure

/-! Approximate resolution lemma with explicit degree accounting.
Cycles, boundaries and homology are the actual categorical objects. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits HomologicalComplex
open scoped ZeroObject
open CMDG.CondensedCM5R0.BreenDeligneFP
open CMDG.CondensedCM5R0.BreenDeligneFPClosure
namespace CMDG.CondensedCM5R0.BreenDeligneFPApproximation

universe v u
variable {C : Type u} [Category.{v} C] [Abelian C]

def kernelMonoCompIso {P X Y : C} (f : P ⟶ X) (g : X ⟶ Y) [Mono g] :
    kernel (f ≫ g) ≅ kernel f where
  hom := kernel.lift f (kernel.ι (f ≫ g)) (by
    apply (cancel_mono g).mp
    simp)
  inv := kernel.lift (f ≫ g) (kernel.ι f) (by simp)
  hom_inv_id := by apply (cancel_mono (kernel.ι (f ≫ g))).mp; simp
  inv_hom_id := by apply (cancel_mono (kernel.ι f)).mp; simp

variable (K : ChainComplex C ℕ)
abbrev B (j : ℕ) := kernel (K.homologyπ (j+1))

def boundaryCover (j : ℕ) : K.X (j+2) ⟶ B K j :=
  kernel.lift _ (K.toCycles (j+2) (j+1)) (K.toCycles_comp_homologyπ _ _)

theorem boundaryCover_epi (j : ℕ) : Epi (boundaryCover K j) := by
  let S := ShortComplex.mk (K.toCycles (j+2) (j+1)) (K.homologyπ (j+1))
    (K.toCycles_comp_homologyπ _ _)
  have hS : S.Exact := ShortComplex.exact_of_g_is_cokernel _
    (K.homologyIsCokernel (j+2) (j+1) ((ComplexShape.down ℕ).prev_eq' (by rfl)))
  exact (S.exact_iff_epi_kernel_lift).mp hS

def cycleKernelIso (j : ℕ) : K.cycles (j+1) ≅ kernel (K.d (j+1) j) :=
  (K.cyclesIsKernel (j+1) j ((ComplexShape.down ℕ).next_eq' (by rfl))).conePointUniqueUpToIso (limit.isLimit _)

def boundaryKernelIso (j : ℕ) : kernel (boundaryCover K j) ≅ K.cycles (j+2) := by
  let f := boundaryCover K j
  let g := kernel.ι (K.homologyπ (j+1)) ≫ K.iCycles (j+1)
  have he : f ≫ g = K.d (j+2) (j+1) := by
    unfold f g boundaryCover
    rw [← Category.assoc,kernel.lift_ι,K.toCycles_i]
  exact (kernelMonoCompIso f g).symm ≪≫ eqToIso (congrArg (fun a : K.X (j+2) ⟶ K.X (j+1) => kernel a) he) ≪≫
    (cycleKernelIso K (j+1)).symm

def homologySequence (j : ℕ) : ShortComplex C := ShortComplex.kernelSequence (K.homologyπ (j+1))
theorem homologySequence_exact (j : ℕ) : (homologySequence K j).ShortExact := {
  exact := ShortComplex.kernelSequence_exact _
  mono_f := by change Mono (kernel.ι _); infer_instance
  epi_g := by change Epi (K.homologyπ (j+1)); infer_instance }

def boundarySequence (j : ℕ) : ShortComplex C := ShortComplex.kernelSequence (boundaryCover K j)
theorem boundarySequence_exact (j : ℕ) : (boundarySequence K j).ShortExact := {
  exact := ShortComplex.kernelSequence_exact _
  mono_f := by change Mono (kernel.ι _); infer_instance
  epi_g := boundaryCover_epi K j }

variable (D : FiniteClass C)

theorem cycles_fp (r j : ℕ)
    (ht : ∀ i ≤ r, FP D (r-i) (K.X (j+i+2)))
    (hh : ∀ i ≤ r, FP D (r-i) (K.homology (j+i+1))) :
    FP D r (K.cycles (j+1)) := by
  induction r generalizing j with
  | zero =>
    letI := boundaryCover_epi K j
    have hB : FP D 0 (B K j) := fp0_epi D (boundaryCover K j) (by simpa using ht 0 (by omega))
    have hH : FP D 0 (K.homology (j+1)) := by simpa using hh 0 (by omega)
    exact fp_extension D 0 (homologySequence K j) (homologySequence_exact K j) hB hH
  | succ r ih =>
    have hnext : FP D r (K.cycles (j+2)) := by
      apply ih (j+1)
      · intro i hi
        have h := ht (i+1) (by omega)
        rwa [show r+1-(i+1)=r-i by omega,show j+(i+1)+2=j+1+i+2 by omega] at h
      · intro i hi
        have h := hh (i+1) (by omega)
        rwa [show r+1-(i+1)=r-i by omega,show j+(i+1)+1=j+1+i+1 by omega] at h
    have hB : FP D (r+1) (B K j) :=
      fp_cokernel D r (boundarySequence K j) (boundarySequence_exact K j)
        (fp_iso D (boundaryKernelIso K j).symm hnext) (by change FP D (r+1) (K.X (j+2)); simpa using ht 0 (by omega))
    have hH : FP D (r+1) (K.homology (j+1)) := by simpa using hh 0 (by omega)
    exact fp_extension D (r+1) (homologySequence K j) (homologySequence_exact K j) hB hH

theorem approximate (r : ℕ) (ha : Epi (K.d 1 0))
    (h0 : FP D (r+1) (K.X 1))
    (ht : ∀ i ≤ r, FP D (r-i) (K.X (i+2)))
    (hh : ∀ i ≤ r, FP D (r-i) (K.homology (i+1))) :
    FP D (r+1) (K.X 0) := by
  let S := ShortComplex.kernelSequence (K.d 1 0)
  have hS : S.ShortExact := {
    exact := ShortComplex.kernelSequence_exact _
    mono_f := by change Mono (kernel.ι _); infer_instance
    epi_g := ha }
  exact fp_cokernel D r S hS
    (fp_iso D (cycleKernelIso K 0) (cycles_fp K D r 0
      (by simpa using ht) (by simpa using hh))) h0

#print axioms cycles_fp
#print axioms approximate
end CMDG.CondensedCM5R0.BreenDeligneFPApproximation
