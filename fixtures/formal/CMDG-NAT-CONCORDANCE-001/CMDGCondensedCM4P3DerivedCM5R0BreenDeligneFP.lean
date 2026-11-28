import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneProjectiveComparison

/-! Finite-projective partial resolutions in an arbitrary abelian
category. Schanuel's lemma makes the condition independent of
the choice of finite-projective cover. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits CategoryTheory.Preadditive
open scoped ZeroObject
open CMDG.CondensedCM5R0.BreenDeligneProjectiveComparison
namespace CMDG.CondensedCM5R0.BreenDeligneFP

universe v u
variable {C : Type u} [Category.{v} C] [Abelian C]

structure FiniteClass (C : Type u) [Category.{v} C] [Abelian C] where
  finite : C → Prop
  projective : ∀ X, finite X → Projective X
  zero : finite 0
  sum : ∀ X Y, finite X → finite Y → finite (X ⊞ Y)

variable (D : FiniteClass C)

def FP : ℕ → C → Prop
  | 0, X => ∃ P, D.finite P ∧ ∃ e : P ⟶ X, Epi e
  | n+1, X => ∃ P, D.finite P ∧ ∃ e : P ⟶ X, Epi e ∧ FP n (kernel e)

theorem fp_iso {n : ℕ} {X Y : C} (e : X ≅ Y) (h : FP D n X) :
    FP D n Y := by
  induction n generalizing X Y with
  | zero =>
    obtain ⟨P,hP,f,hf⟩ := h
    letI := hf
    exact ⟨P,hP,f ≫ e.hom,inferInstance⟩
  | succ n ih =>
    obtain ⟨P,hP,f,hf,hK⟩ := h
    letI := hf
    exact ⟨P,hP,f ≫ e.hom,inferInstance,ih (kernelCompIso f e).symm hK⟩

theorem fp_of_finite (n : ℕ) {X : C} (h : D.finite X) : FP D n X := by
  induction n generalizing X with
  | zero => exact ⟨X,h,𝟙 X,inferInstance⟩
  | succ n ih =>
    refine ⟨X,h,𝟙 X,inferInstance,?_⟩
    exact fp_iso D (isZero_kernel_of_mono (𝟙 X)).isoZero.symm (ih D.zero)

theorem fp_zero_of_fp (n : ℕ) {X : C} (h : FP D n X) : FP D 0 X := by
  cases n with
  | zero => exact h
  | succ n =>
    obtain ⟨P,hP,f,hf,_⟩ := h
    exact ⟨P,hP,f,hf⟩

theorem fp0_epi {X Y : C} (e : X ⟶ Y) [Epi e] (h : FP D 0 X) :
    FP D 0 Y := by
  obtain ⟨P,hP,f,hf⟩ := h
  letI := hf
  exact ⟨P,hP,f ≫ e,inferInstance⟩

theorem fp_sum_iff (n : ℕ) (X Y : C) :
    FP D n (X ⊞ Y) ↔ FP D n X ∧ FP D n Y := by
  induction n generalizing X Y with
  | zero =>
    constructor
    · intro h
      exact ⟨fp0_epi D biprod.fst h,fp0_epi D biprod.snd h⟩
    · rintro ⟨⟨P,hP,f,hf⟩,⟨Q,hQ,g,hg⟩⟩
      letI := hf
      letI := hg
      exact ⟨P ⊞ Q,D.sum P Q hP hQ,biprod.map f g,inferInstance⟩
  | succ n ih =>
    have transfer {A P : C} (p : P ⟶ A) (hP : D.finite P) [Epi p]
        (hA : FP D (n+1) A) : FP D n (kernel p) := by
      obtain ⟨Q,hQ,q,hq,hK⟩ := hA
      letI := hq
      letI := D.projective P hP
      letI := D.projective Q hQ
      have h := (ih (kernel q) P).mpr ⟨hK,fp_of_finite D n hP⟩
      exact ((ih (kernel p) Q).mp (fp_iso D (schanuel q p) h)).1
    constructor
    · intro h
      obtain ⟨P,hP,f,hf⟩ := fp0_epi D (biprod.fst : X ⊞ Y ⟶ X) (fp_zero_of_fp D (n+1) h)
      obtain ⟨Q,hQ,g,hg⟩ := fp0_epi D (biprod.snd : X ⊞ Y ⟶ Y) (fp_zero_of_fp D (n+1) h)
      letI := hf
      letI := hg
      have hK := transfer (biprod.map f g) (D.sum P Q hP hQ) h
      obtain ⟨h₁,h₂⟩ := (ih _ _).mp (fp_iso D (kernelSumIso f g) hK)
      exact ⟨⟨P,hP,f,hf,h₁⟩,⟨Q,hQ,g,hg,h₂⟩⟩
    · rintro ⟨⟨P,hP,f,hf,hK⟩,⟨Q,hQ,g,hg,hL⟩⟩
      letI := hf
      letI := hg
      exact ⟨P ⊞ Q,D.sum P Q hP hQ,biprod.map f g,inferInstance,
        fp_iso D (kernelSumIso f g).symm ((ih _ _).mpr ⟨hK,hL⟩)⟩

theorem fp_cover_kernel {n : ℕ} {P X : C} (p : P ⟶ X) [Epi p]
    (hP : D.finite P) (hX : FP D (n+1) X) : FP D n (kernel p) := by
  obtain ⟨Q,hQ,q,hq,hK⟩ := hX
  letI := hq
  letI := D.projective P hP
  letI := D.projective Q hQ
  exact ((fp_sum_iff D n _ _).mp (fp_iso D (schanuel q p)
    ((fp_sum_iff D n _ _).mpr ⟨hK,fp_of_finite D n hP⟩))).1

theorem fp_retract {n : ℕ} {X Y : C} (r : Retract X Y) (h : FP D n Y) :
    FP D n X := by
  letI : Epi r.r := epi_of_epi_fac r.retract
  let S := ShortComplex.kernelSequence r.r
  have hE : S.Exact := ShortComplex.kernelSequence_exact _
  have spl : S.Splitting := ShortComplex.Splitting.ofExactOfSection S hE r.i
    r.retract (by change Mono (kernel.ι r.r); infer_instance)
  exact ((fp_sum_iff D n _ _).mp (fp_iso D spl.isoBinaryBiproduct h)).2

theorem fp_mono_degree (n : ℕ) {X : C} (h : FP D (n+1) X) : FP D n X := by
  induction n generalizing X with
  | zero => exact fp_zero_of_fp D 1 h
  | succ n ih =>
    obtain ⟨P,hP,f,hf,hK⟩ := h
    exact ⟨P,hP,f,hf,ih hK⟩

#print axioms fp_cover_kernel
#print axioms fp_retract
#print axioms fp_mono_degree
end CMDG.CondensedCM5R0.BreenDeligneFP
