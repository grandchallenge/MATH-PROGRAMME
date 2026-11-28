import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneProbeFree
import CMDGCondensedCM4P3DerivedCM5R0RealCircleCondensedComplex

/-! Actual sections of the real-group presheaf and finite-power
coordinates on the genuine relative product. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
open scoped ZeroObject
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection CompactCover

variable (I : Type u)

def realPsh : Psh.{u} where
  obj T := ModuleCat.of Coeff (C(T.unop, ULift.{u+1,u} (I → ℝ)))
  map f := ModuleCat.ofHom
    { toFun := fun g => g.comp f.unop.hom.hom
      map_add' := by intros; rfl
      map_smul' := by intros; rfl }
  map_id T := by ext g t; rfl
  map_comp f g := by ext h t; rfl

variable (S : Profinite.{u})
abbrev probeSet : SetPsh.{u} :=
  (compHausToCondensed.obj (profiniteToCompHaus.obj S)).obj

def realToProbe (J : Type u) : (probeRealSet S J).obj ⟶ probeSet S where
  app T := ↾fun (x : C(T.unop, ULift.{u+1,u} (S × (J → ℝ)))) => ⟨CompHausLike.ofHom _
    (⟨fun t => (x t).down.1,continuous_fst.comp (continuous_uliftDown.comp x.continuous)⟩ :
      C(T.unop,S))⟩
  naturality := by intros; rfl

variable {k : ℕ} (arity : Fin k → ℕ)
abbrev realGeneratorPsh := realPsh I ⋙ tupleSet arity
abbrev zeroGeneratorPsh := zeroPsh.{u} ⋙ tupleSet arity

def realLeg (j : Fin k) :
    (probeRealSet S (Fin (arity j) × I)).obj ⟶
      productSet (probeSet S) (realGeneratorPsh I arity) where
  app T := ↾fun (x : C(T.unop,ULift.{u+1,u} (S × ((Fin (arity j) × I) → ℝ)))) =>
    ((realToProbe S (Fin (arity j) × I)).app T x,
      ⟨j,fun a => (⟨fun t => ⟨fun i => (x t).down.2 (a,i)⟩,
        continuous_uliftUp.comp (continuous_pi fun i =>
          (continuous_apply (a,i)).comp
            (continuous_snd.comp (continuous_uliftDown.comp x.continuous)))⟩ :
        C(T.unop,ULift.{u+1,u} (I → ℝ)))⟩)
  naturality := by intros; rfl

def assembleReal (T : CompHaus.{u}ᵒᵖ) (j : Fin k)
    (p : (probeSet S).obj T)
    (g : Fin (arity j) → C(T.unop,ULift.{u+1,u} (I → ℝ))) :
    (probeRealSet S (Fin (arity j) × I)).obj.obj T :=
  ⟨fun t => ⟨(p.down.hom.hom t,fun a => (g a.1 t).down a.2)⟩,
    continuous_uliftUp.comp (p.down.hom.hom.continuous.prodMk
      (continuous_pi fun a =>
        (continuous_apply a.2).comp (continuous_uliftDown.comp (g a.1).continuous)))⟩

def realLegEquiv (T : CompHaus.{u}ᵒᵖ) :
    (Σ j : Fin k, (probeRealSet S (Fin (arity j) × I)).obj.obj T) ≃
      (productSet (probeSet S) (realGeneratorPsh I arity)).obj T where
  toFun z := (realLeg I S arity z.1).app T z.2
  invFun z := ⟨z.2.1,assembleReal I S arity T z.2.1 z.1 z.2.2⟩
  left_inv := by
    rintro ⟨j,x⟩
    apply Sigma.ext
    · rfl
    · apply heq_of_eq
      apply ContinuousMap.ext
      intro t
      apply ULift.ext
      apply Prod.ext
      · rfl
      · funext a
        cases a
        rfl
  right_inv := by
    rintro ⟨p,⟨j,g⟩⟩
    apply Prod.ext
    · apply ULift.ext
      apply ConcreteCategory.hom_ext
      intro t
      rfl
    · apply Sigma.ext
      · rfl
      · apply heq_of_eq
        funext a
        apply ContinuousMap.ext
        intro t
        rfl

def zeroLeg (j : Fin k) : probeSet S ⟶ productSet (probeSet S) (zeroGeneratorPsh arity) where
  app T := ↾fun p => (p,⟨j,fun _ => 0⟩)
  naturality := by
    intro T U f
    apply ConcreteCategory.hom_ext
    intro p
    apply Prod.ext
    · rfl
    · apply Sigma.ext
      · rfl
      · apply heq_of_eq
        funext a
        change (0 : (0 : Mod.{u})) = _
        rfl

def zeroLegEquiv (T : CompHaus.{u}ᵒᵖ) :
    (Σ _ : Fin k, (probeSet S).obj T) ≃
      (productSet (probeSet S) (zeroGeneratorPsh arity)).obj T where
  toFun z := (zeroLeg S arity z.1).app T z.2
  invFun z := ⟨z.2.1,z.1⟩
  left_inv := by rintro ⟨j,p⟩; rfl
  right_inv := by
    rintro ⟨p,⟨j,g⟩⟩
    apply Prod.ext
    · rfl
    · apply Sigma.ext
      · rfl
      · apply heq_of_eq
        funext a
        change (_ : (0 : Mod.{u})) = _
        letI : Subsingleton (0 : Mod.{u}) := ModuleCat.subsingleton_of_isZero (isZero_zero Mod.{u})
        exact Subsingleton.elim _ _

def realGeneratorProjection : realGeneratorPsh I arity ⟶ zeroGeneratorPsh arity :=
  Functor.whiskerRight (pZero (realPsh I)) (tupleSet arity)

theorem realLeg_projection (j : Fin k) :
    realLeg I S arity j ≫ productMap (probeSet S) (realGeneratorProjection I arity) =
      realToProbe S (Fin (arity j) × I) ≫ zeroLeg S arity j := by
  apply NatTrans.ext
  funext T
  apply ConcreteCategory.hom_ext
  intro x
  apply Prod.ext
  · rfl
  · apply Sigma.ext
    · rfl
    · apply heq_of_eq
      funext a
      change (_ : (0 : Mod.{u})) = _
      letI : Subsingleton (0 : Mod.{u}) := ModuleCat.subsingleton_of_isZero (isZero_zero Mod.{u})
      exact Subsingleton.elim _ _

#print axioms realLegEquiv
#print axioms zeroLegEquiv
#print axioms realLeg_projection
end CMDG.CondensedCM5R0.BreenDeligneProbe
