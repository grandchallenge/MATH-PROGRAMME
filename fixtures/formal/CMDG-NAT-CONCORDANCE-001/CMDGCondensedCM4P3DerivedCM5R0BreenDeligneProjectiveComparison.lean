import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCoefficientPresentation
import Mathlib.Algebra.Homology.ShortComplex.ShortExact
import Mathlib.CategoryTheory.Abelian.Basic

/-! Schanuel comparison in the actual abelian category. No finite
generation or pseudocoherence closure properties are assumed. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits CategoryTheory.Preadditive
namespace CMDG.CondensedCM5R0.BreenDeligneProjectiveComparison

universe v u
variable {C : Type u} [Category.{v} C] [Abelian C]

def kernelCompIso {P X Y : C} (f : P ⟶ X) (e : X ≅ Y) :
    kernel (f ≫ e.hom) ≅ kernel f where
  hom := kernel.lift f (kernel.ι (f ≫ e.hom)) (by
    apply (cancel_mono e.hom).mp
    simp)
  inv := kernel.lift (f ≫ e.hom) (kernel.ι f) (by simp)
  hom_inv_id := by
    apply (cancel_mono (kernel.ι (f ≫ e.hom))).mp
    simp
  inv_hom_id := by
    apply (cancel_mono (kernel.ι f)).mp
    simp

def splitKernelIso {P X : C} (f : P ⟶ X) [Epi f] [Projective X] :
    P ≅ kernel f ⊞ X := by
  have hS : (ShortComplex.kernelSequence f).ShortExact := {
    exact := ShortComplex.kernelSequence_exact f
    mono_f := by change Mono (kernel.ι f); infer_instance
    epi_g := by change Epi f; infer_instance }
  letI : Projective (ShortComplex.kernelSequence f).X₃ := by change Projective X; infer_instance
  exact hS.splittingOfProjective.isoBinaryBiproduct

def fstKernelIso {P Q X : C} (f : P ⟶ X) (g : Q ⟶ X) :
    kernel (pullback.fst f g) ≅ kernel g where
  hom := kernel.lift g (kernel.ι (pullback.fst f g) ≫ pullback.snd f g) (by
    rw [Category.assoc,← pullback.condition,← Category.assoc,kernel.condition,zero_comp])
  inv := kernel.lift (pullback.fst f g)
    (pullback.lift 0 (kernel.ι g) (by simp)) (by simp)
  hom_inv_id := by
    apply (cancel_mono (kernel.ι (pullback.fst f g))).mp
    apply pullback.hom_ext
    · simp
    · simp
  inv_hom_id := by
    apply (cancel_mono (kernel.ι g)).mp
    simp

def sndKernelIso {P Q X : C} (f : P ⟶ X) (g : Q ⟶ X) :
    kernel (pullback.snd f g) ≅ kernel f where
  hom := kernel.lift f (kernel.ι (pullback.snd f g) ≫ pullback.fst f g) (by
    rw [Category.assoc,pullback.condition,← Category.assoc,kernel.condition,zero_comp])
  inv := kernel.lift (pullback.snd f g)
    (pullback.lift (kernel.ι f) 0 (by simp)) (by simp)
  hom_inv_id := by
    apply (cancel_mono (kernel.ι (pullback.snd f g))).mp
    apply pullback.hom_ext
    · simp
    · simp
  inv_hom_id := by
    apply (cancel_mono (kernel.ι f)).mp
    simp

def schanuel {P Q X : C} (f : P ⟶ X) (g : Q ⟶ X)
    [Projective P] [Projective Q] [Epi f] [Epi g] :
    kernel f ⊞ Q ≅ kernel g ⊞ P :=
  (biprod.mapIso (sndKernelIso f g) (Iso.refl Q)).symm ≪≫
    (splitKernelIso (pullback.snd f g)).symm ≪≫
    splitKernelIso (pullback.fst f g) ≪≫
    biprod.mapIso (fstKernelIso f g) (Iso.refl P)

def kernelSumIso {P Q X Y : C} (f : P ⟶ X) (g : Q ⟶ Y) :
    kernel (biprod.map f g) ≅ kernel f ⊞ kernel g where
  hom := biprod.lift
    (kernel.lift f (kernel.ι (biprod.map f g) ≫ biprod.fst) (by
      rw [Category.assoc,← biprod.map_fst,← Category.assoc,kernel.condition,zero_comp]))
    (kernel.lift g (kernel.ι (biprod.map f g) ≫ biprod.snd) (by
      rw [Category.assoc,← biprod.map_snd,← Category.assoc,kernel.condition,zero_comp]))
  inv := kernel.lift (biprod.map f g) (biprod.map (kernel.ι f) (kernel.ι g)) (by
    apply biprod.hom_ext
    · simp
    · simp)
  hom_inv_id := by
    apply (cancel_mono (kernel.ι (biprod.map f g))).mp
    apply biprod.hom_ext
    · simp
    · simp
  inv_hom_id := by
    apply biprod.hom_ext
    · apply (cancel_mono (kernel.ι f)).mp
      simp
    · apply (cancel_mono (kernel.ι g)).mp
      simp

#print axioms schanuel
#print axioms kernelSumIso
end CMDG.CondensedCM5R0.BreenDeligneProjectiveComparison
