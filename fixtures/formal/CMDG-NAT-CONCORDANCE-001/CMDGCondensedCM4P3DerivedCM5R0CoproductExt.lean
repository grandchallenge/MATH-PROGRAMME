import CMDGCondensedCM4P3DerivedCM5R0AmbientProjectiveGenerators
import Mathlib.Condensed.AB
import Mathlib.CategoryTheory.Abelian.GrothendieckAxioms.Colim

/-! Ext restriction to every summand jointly detects classes in
arbitrary small coproducts. Proof by actual projective presentations
and the natural long exact sequence, with AB4 at the correct size. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

variable {J : Type u}

local instance : AB4OfSize.{u} Ambient.{u} := AB4OfSize_shrink.{u,u+1} _

def coproductSequence (S : J → ShortComplex Ambient.{u}) :
    ShortComplex Ambient.{u} :=
  ShortComplex.mk (Limits.Sigma.map fun j => (S j).f)
    (Limits.Sigma.map fun j => (S j).g) (by
      apply Sigma.hom_ext
      intro j
      rw [← Category.assoc,Sigma.ι_map,Category.assoc,Sigma.ι_map,
        ← Category.assoc,(S j).zero,zero_comp,comp_zero])

theorem coproductSequence_shortExact (S : J → ShortComplex Ambient.{u})
    (hS : ∀ j, (S j).ShortExact) : (coproductSequence S).ShortExact := by
  let D : ShortComplex (Discrete J ⥤ Ambient.{u}) :=
    ShortComplex.mk
      (Discrete.natTrans (F:=Discrete.functor fun j => (S j).X₁)
        (G:=Discrete.functor fun j => (S j).X₂) fun j => (S j.as).f)
      (Discrete.natTrans (F:=Discrete.functor fun j => (S j).X₂)
        (G:=Discrete.functor fun j => (S j).X₃) fun j => (S j.as).g)
      (by apply NatTrans.ext; funext j; exact (S j.as).zero)
  letI : ∀ j, Mono (D.f.app j) := fun j => (hS j.as).mono_f
  letI : ∀ j, Epi (D.g.app j) := fun j => (hS j.as).epi_g
  haveI : Mono D.f := NatTrans.mono_of_mono_app _
  haveI : Epi D.g := NatTrans.epi_of_epi_app _
  have hd : D.ShortExact := ⟨functorShortComplex_exact_of_pointwise D
    (fun j => (hS j.as).exact)⟩
  let F : (Discrete J ⥤ Ambient.{u}) ⥤ Ambient.{u} := colim
  haveI : Mono (F.map D.f) := by
    letI : PreservesFiniteLimits F := inferInstance
    exact F.map_mono D.f
  haveI : Epi (F.map D.g) := by dsimp [F]; infer_instance
  have hh := hd.map F
  exact hh

def coproductSequenceInclusion (S : J → ShortComplex Ambient.{u}) (j : J) :
    S j ⟶ coproductSequence S where
  τ₁ := Sigma.ι (fun k => (S k).X₁) j
  τ₂ := Sigma.ι (fun k => (S k).X₂) j
  τ₃ := Sigma.ι (fun k => (S k).X₃) j
  comm₁₂ := by exact Sigma.ι_map (fun k => (S k).f) j
  comm₂₃ := by exact Sigma.ι_map (fun k => (S k).g) j

def presentationSequence {X : Ambient.{u}} (P : ProjectivePresentation X) :
    ShortComplex Ambient.{u} :=
  ShortComplex.mk (kernel.ι P.f) P.f (kernel.condition P.f)

theorem presentationSequence_shortExact {X : Ambient.{u}} (P : ProjectivePresentation X) :
    (presentationSequence P).ShortExact := by
  change (ShortComplex.mk (kernel.ι P.f) P.f (kernel.condition P.f)).ShortExact
  exact ⟨ShortComplex.exact_kernel P.f⟩

theorem coproduct_ext_detect (n : ℕ) (X : J → Ambient.{u}) (Y : Ambient.{u})
    (e : Abelian.Ext (∐ X) Y n)
    (h : ∀ j, (Abelian.Ext.mk₀ (Sigma.ι X j)).comp e (zero_add n) = 0) :
    e = 0 := by
  induction n generalizing X with
  | zero =>
    apply Abelian.Ext.addEquiv₀.injective
    rw [map_zero]
    apply Sigma.hom_ext
    intro j
    rw [comp_zero]
    have hj := h j
    rw [← Abelian.Ext.mk₀_addEquiv₀_apply e, Abelian.Ext.mk₀_comp_mk₀] at hj
    exact Abelian.Ext.addEquiv₀.symm.injective (by
      rw [Abelian.Ext.addEquiv₀_symm_apply,Abelian.Ext.addEquiv₀_symm_apply,
        Abelian.Ext.mk₀_zero]; exact hj)
  | succ n ih =>
    letI : EnoughProjectives Ambient.{u} := ambientEnoughProjectives
    let P (j : J) : ProjectivePresentation (X j) := Classical.arbitrary _
    let S (j : J) := presentationSequence (P j)
    have hS (j : J) : (S j).ShortExact := presentationSequence_shortExact (P j)
    let T := coproductSequence S
    have hT : T.ShortExact := coproductSequence_shortExact S hS
    haveI : Projective T.X₂ := projective_coproduct (fun j => (S j).X₂)
      (fun j => (P j).projective)
    have hz : (Abelian.Ext.mk₀ T.g).comp e (zero_add (n+1)) = 0 :=
      Abelian.Ext.eq_zero_of_projective _
    obtain ⟨x,hx⟩ := Abelian.Ext.contravariant_sequence_exact₃ hT Y e hz
      (by omega : 1+n=n+1)
    have localLift (j : J) :
        ∃ y : Abelian.Ext (S j).X₂ Y n,
          (Abelian.Ext.mk₀ (S j).f).comp y (zero_add n) =
            (Abelian.Ext.mk₀ (Sigma.ι (fun k => (S k).X₁) j)).comp x (zero_add n) := by
      let i := coproductSequenceInclusion S j
      have hn := ShortComplex.ShortExact.extClass_naturality (hS j) hT i
      have hzero : (hS j).extClass.comp
          ((Abelian.Ext.mk₀ i.τ₁).comp x (zero_add n)) (by omega : 1+n=n+1) = 0 := by
        rw [← Abelian.Ext.comp_assoc,hn,Abelian.Ext.comp_assoc,hx]
        exact h j
        all_goals omega
      exact Abelian.Ext.contravariant_sequence_exact₁ (hS j) Y _ _ hzero
    cases n with
    | zero =>
      choose y hy using localLift
      let g : T.X₂ ⟶ Y := Sigma.desc fun j => Abelian.Ext.addEquiv₀ (y j)
      have hg : (Abelian.Ext.mk₀ T.f).comp (Abelian.Ext.mk₀ g) (zero_add 0) = x := by
        apply Abelian.Ext.addEquiv₀.injective
        rw [Abelian.Ext.mk₀_comp_mk₀,← Abelian.Ext.addEquiv₀_symm_apply,AddEquiv.apply_symm_apply]
        change T.f ≫ g = Abelian.Ext.addEquiv₀ x
        apply Sigma.hom_ext
        intro j
        have hj := hy j
        rw [← Abelian.Ext.mk₀_addEquiv₀_apply (y j),
          ← Abelian.Ext.mk₀_addEquiv₀_apply x,Abelian.Ext.mk₀_comp_mk₀,
          Abelian.Ext.mk₀_comp_mk₀] at hj
        have heq := Abelian.Ext.addEquiv₀.symm.injective
          (show Abelian.Ext.addEquiv₀.symm ((S j).f ≫ Abelian.Ext.addEquiv₀ (y j)) =
            Abelian.Ext.addEquiv₀.symm (Sigma.ι (fun k => (S k).X₁) j ≫
              Abelian.Ext.addEquiv₀ x) from hj)
        change Sigma.ι (fun k => (S k).X₁) j ≫
          Limits.Sigma.map (fun k => (S k).f) ≫ g = _
        rw [Sigma.ι_map_assoc]
        unfold g
        rw [Sigma.ι_desc]
        exact heq
      rw [← hx, ← hg, ← Abelian.Ext.comp_assoc,hT.extClass_comp,Abelian.Ext.zero_comp] <;> omega
    | succ n =>
      have hlocal (j : J) :
          (Abelian.Ext.mk₀ (Sigma.ι (fun k => (S k).X₁) j)).comp x
            (zero_add (n+1)) = 0 := by
        obtain ⟨y,hy⟩ := localLift j
        letI : Projective (S j).X₂ := (P j).projective
        rw [Abelian.Ext.eq_zero_of_projective y,Abelian.Ext.comp_zero] at hy
        exact hy.symm
      have hx0 := ih (fun j => (S j).X₁) x hlocal
      rw [← hx,hx0,Abelian.Ext.comp_zero]

theorem coproduct_extPositive_zero (X : J → Ambient.{u}) (Y : Ambient.{u}) (q : ℕ)
    (h : ∀ j (e : Abelian.Ext (X j) Y (q+1)), e=0)
    (e : Abelian.Ext (∐ X) Y (q+1)) : e=0 :=
  coproduct_ext_detect (q+1) X Y e (fun j => h j _)

#print axioms coproductSequence_shortExact
#print axioms coproduct_ext_detect
#print axioms coproduct_extPositive_zero
end CMDG.CondensedCM5R0
