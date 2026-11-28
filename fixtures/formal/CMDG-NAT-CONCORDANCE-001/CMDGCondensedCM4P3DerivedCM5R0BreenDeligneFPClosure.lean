import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFP

/-! All-degree extension and cokernel closure for partial finite
projective resolutions. The horseshoe step uses an actual pullback
of the right cover, split by projectivity. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits CategoryTheory.Preadditive
open scoped ZeroObject
open CMDG.CondensedCM5R0.BreenDeligneProjectiveComparison
open CMDG.CondensedCM5R0.BreenDeligneFP
namespace CMDG.CondensedCM5R0.BreenDeligneFPClosure

universe v u
variable {C : Type u} [Category.{v} C] [Abelian C]

def compKernelIso {P X Y : C} (f : P ⟶ X) (g : X ⟶ Y) :
    kernel (f ≫ g) ≅ pullback f (kernel.ι g) where
  hom := pullback.lift (kernel.ι (f ≫ g))
    (kernel.lift g (kernel.ι (f ≫ g) ≫ f) (by simp)) (by simp)
  inv := kernel.lift (f ≫ g) (pullback.fst f (kernel.ι g)) (by
    rw [← Category.assoc,pullback.condition,Category.assoc,kernel.condition,comp_zero])
  hom_inv_id := by
    apply (cancel_mono (kernel.ι (f ≫ g))).mp
    simp
  inv_hom_id := by
    apply pullback.hom_ext
    · simp
    · apply (cancel_mono (kernel.ι g)).mp
      simp [pullback.condition]

def exactKernelIso (S : ShortComplex C) (hS : S.ShortExact) :
    S.X₁ ≅ kernel S.g :=
  hS.fIsKernel.conePointUniqueUpToIso (limit.isLimit _)

def pullbackShort (S : ShortComplex C) (hS : S.ShortExact) {Q : C}
    (q : Q ⟶ S.X₃) [Projective Q] :
    pullback S.g q ≅ S.X₁ ⊞ Q := by
  letI := hS.epi_g
  exact splitKernelIso (pullback.snd S.g q) ≪≫
    biprod.mapIso (sndKernelIso S.g q ≪≫ (exactKernelIso S hS).symm) (Iso.refl Q)

variable (D : FiniteClass C)

theorem fp_extension (n : ℕ) (S : ShortComplex C) (hS : S.ShortExact)
    (h₁ : FP D n S.X₁) (h₃ : FP D n S.X₃) : FP D n S.X₂ := by
  induction n generalizing S with
  | zero =>
    obtain ⟨P,hP,p,hp⟩ := h₁
    obtain ⟨Q,hQ,q,hq⟩ := h₃
    letI := hp
    letI := hq
    letI := D.projective Q hQ
    let e := pullbackShort S hS q
    exact ⟨P ⊞ Q,D.sum P Q hP hQ,
      biprod.map p (𝟙 Q) ≫ e.inv ≫ pullback.fst S.g q,inferInstance⟩
  | succ n ih =>
    obtain ⟨P,hP,p,hp,hK⟩ := h₁
    obtain ⟨Q,hQ,q,hq,hL⟩ := h₃
    letI := hp
    letI := hq
    letI := D.projective Q hQ
    let e := pullbackShort S hS q
    let f : P ⊞ Q ⟶ pullback S.g q := biprod.map p (𝟙 Q) ≫ e.inv
    let g := pullback.fst S.g q
    letI : Epi f := by dsimp [f]; infer_instance
    letI : Epi g := by dsimp [g]; infer_instance
    have hZ : FP D n (kernel (𝟙 Q)) :=
      fp_iso D (isZero_kernel_of_mono (𝟙 Q)).isoZero.symm (fp_of_finite D n D.zero)
    have hf : FP D n (kernel f) :=
      fp_iso D ((kernelSumIso p (𝟙 Q)).symm ≪≫ (kernelCompIso (biprod.map p (𝟙 Q)) e.symm).symm)
        ((fp_sum_iff D n _ _).mpr ⟨hK,hZ⟩)
    have hg : FP D n (kernel g) := fp_iso D (fstKernelIso S.g q).symm hL
    let T := ShortComplex.kernelSequence (pullback.snd f (kernel.ι g))
    have hT : T.ShortExact := {
      exact := ShortComplex.kernelSequence_exact _
      mono_f := by change Mono (kernel.ι _); infer_instance
      epi_g := by change Epi (pullback.snd f (kernel.ι g)); infer_instance }
    have hT1 : FP D n T.X₁ := fp_iso D (sndKernelIso f (kernel.ι g)).symm hf
    have hT3 : FP D n T.X₃ := hg
    have hM := ih T hT hT1 hT3
    exact ⟨P ⊞ Q,D.sum P Q hP hQ,f ≫ g,inferInstance,
      fp_iso D (compKernelIso f g).symm hM⟩

theorem fp_cokernel (n : ℕ) (S : ShortComplex C) (hS : S.ShortExact)
    (h₁ : FP D n S.X₁) (h₂ : FP D (n+1) S.X₂) : FP D (n+1) S.X₃ := by
  obtain ⟨P,hP,p,hp,hK⟩ := h₂
  letI := hp
  letI := hS.epi_g
  let T := ShortComplex.kernelSequence (pullback.snd p (kernel.ι S.g))
  have hT : T.ShortExact := {
    exact := ShortComplex.kernelSequence_exact _
    mono_f := by change Mono (kernel.ι _); infer_instance
    epi_g := by change Epi (pullback.snd p (kernel.ι S.g)); infer_instance }
  have hT1 : FP D n T.X₁ := fp_iso D (sndKernelIso p (kernel.ι S.g)).symm hK
  have hT3 : FP D n T.X₃ := fp_iso D (exactKernelIso S hS) h₁
  exact ⟨P,hP,p ≫ S.g,inferInstance,fp_iso D (compKernelIso p S.g).symm
    (fp_extension D n T hT hT1 hT3)⟩

#print axioms fp_extension
#print axioms fp_cokernel
end CMDG.CondensedCM5R0.BreenDeligneFPClosure
