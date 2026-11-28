import CMDGCondensedCM4P3DerivedCM5R0ResolutionFiniteSupport
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealGroup

/-! The actual continuous-circle-group presheaf, with its finite
coordinate projection and zero extension. The generator comparison
keeps the profinite probe and every power coordinate. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection CompactCover CompactCover.CircleContinuity

local instance (I : Type u) : IsTopologicalAddGroup (ULift.{u+1,u} (I → UnitAddCircle)) := ⟨⟩

variable (I : Type u)

def circlePsh : Psh.{u} where
  obj T := ModuleCat.of Coeff (C(T.unop, ULift.{u+1,u} (I → UnitAddCircle)))
  map f := ModuleCat.ofHom
    { toFun := fun g => g.comp f.unop.hom.hom
      map_add' := by intros; rfl
      map_smul' := by intros; rfl }
  map_id T := by ext g t; rfl
  map_comp f g := by ext h t; rfl

variable (F : Finset I)
def circleRestrict : circlePsh I ⟶ circlePsh (↥F) where
  app T := ModuleCat.ofHom
    { toFun := fun (g : C(T.unop,ULift.{u+1,u} (I → UnitAddCircle))) =>
        (⟨fun t => ⟨fun i => (g t).down i.val⟩,
          continuous_uliftUp.comp (continuous_pi fun i =>
            (continuous_apply i.val).comp (continuous_uliftDown.comp g.continuous))⟩ :
          C(T.unop,ULift.{u+1,u} (↥F → UnitAddCircle)))
      map_add' := by intros; rfl
      map_smul' := by intros; rfl }
  naturality := by intros; rfl

def circleExtendApp (T : CompHaus.{u}ᵒᵖ) :
    (circlePsh (↥F)).obj T ⟶ (circlePsh I).obj T := by
  classical
  refine ModuleCat.ofHom {
    toFun := fun (g : C(T.unop,ULift.{u+1,u} (↥F → UnitAddCircle))) =>
      (⟨fun t => ⟨extendCoordinates F (fun _ => 0) (g t).down⟩,
        continuous_uliftUp.comp ((extendCoordinates F (fun _ => (0 : UnitAddCircle))).continuous.comp
          (continuous_uliftDown.comp g.continuous))⟩ : C(T.unop,ULift.{u+1,u} (I → UnitAddCircle)))
    map_add' := ?_
    map_smul' := ?_ }
  · intro a b
    apply ContinuousMap.ext
    intro t
    apply ULift.ext
    funext i
    change (if h : i ∈ F then (a t).down ⟨i,h⟩ + (b t).down ⟨i,h⟩ else 0) =
      (if h : i ∈ F then (a t).down ⟨i,h⟩ else 0) + (if h : i ∈ F then (b t).down ⟨i,h⟩ else 0)
    by_cases hi : i ∈ F <;> simp [hi]
  · intro r a
    apply ContinuousMap.ext
    intro t
    apply ULift.ext
    funext i
    change (if h : i ∈ F then r.down • (a t).down ⟨i,h⟩ else 0) =
      r.down • (if h : i ∈ F then (a t).down ⟨i,h⟩ else 0)
    by_cases hi : i ∈ F <;> simp [hi]

def circleExtend : circlePsh (↥F) ⟶ circlePsh I where
  app := circleExtendApp I F
  naturality := by intros; rfl

abbrev circleTrunc := circleRestrict I F ≫ circleExtend I F

theorem circleExtend_restrict : circleExtend I F ≫ circleRestrict I F = 𝟙 _ := by
  classical
  apply NatTrans.ext
  funext T
  apply ConcreteCategory.hom_ext
  intro g
  apply ContinuousMap.ext
  intro t
  apply ULift.ext
  funext i
  change C(T.unop,ULift.{u+1,u} (↥F → UnitAddCircle)) at g
  change (if h : i.val ∈ F then (g t).down ⟨i.val,h⟩ else 0) = (g t).down i
  rw [dif_pos i.property]

theorem circleTrunc_absorb {F G : Finset I} (h : F ⊆ G) :
    circleTrunc I G ≫ circleTrunc I F = circleTrunc I F := by
  classical
  apply NatTrans.ext
  funext T
  apply ConcreteCategory.hom_ext
  intro g
  apply ContinuousMap.ext
  intro t
  apply ULift.ext
  funext i
  change C(T.unop,ULift.{u+1,u} (I → UnitAddCircle)) at g
  change (if hF : i ∈ F then (if hG : i ∈ G then (g t).down i else 0) else 0) =
    (if hF : i ∈ F then (g t).down i else 0)
  by_cases hi : i ∈ F
  · simp [hi,h hi]
  · simp [hi]

variable (S : Profinite.{u}) {k : ℕ} (arity : Fin k → ℕ)
abbrev circleGeneratorPsh := circlePsh I ⋙ tupleSet arity

abbrev circlePowerSet (j : Fin k) : SetPsh.{u} :=
  (compHausToCondensed.obj (circlePowerT S I (arity j))).obj

def circleLeg (j : Fin k) :
    circlePowerSet I S arity j ⟶ productSet (probeSet S) (circleGeneratorPsh I arity) where
  app T := ↾fun x =>
    (⟨CompHausLike.ofHom _ (⟨fun t => (x.down.hom.hom t).1,
      continuous_fst.comp x.down.hom.hom.continuous⟩ : C(T.unop,S))⟩,
     ⟨j,fun a => (⟨fun t => ⟨(x.down.hom.hom t).2 a⟩,
      continuous_uliftUp.comp ((continuous_apply a).comp (continuous_snd.comp x.down.hom.hom.continuous))⟩ :
        C(T.unop,ULift.{u+1,u} (I → UnitAddCircle)))⟩)
  naturality := by intros; rfl

def assembleCircle (T : CompHaus.{u}ᵒᵖ) (j : Fin k)
    (p : (probeSet S).obj T)
    (g : Fin (arity j) → C(T.unop,ULift.{u+1,u} (I → UnitAddCircle))) :
    (circlePowerSet I S arity j).obj T :=
  ⟨CompHausLike.ofHom _ (⟨fun t => (p.down.hom.hom t,fun a => (g a t).down),
    p.down.hom.hom.continuous.prodMk (continuous_pi fun a =>
      continuous_uliftDown.comp (g a).continuous)⟩ :
      C(T.unop,S × (Fin (arity j) → I → UnitAddCircle)))⟩

def circleLegEquiv (T : CompHaus.{u}ᵒᵖ) :
    (Σ j : Fin k, (circlePowerSet I S arity j).obj T) ≃
      (productSet (probeSet S) (circleGeneratorPsh I arity)).obj T where
  toFun z := (circleLeg I S arity z.1).app T z.2
  invFun z := ⟨z.2.1,assembleCircle I S arity T z.2.1 z.1 z.2.2⟩
  left_inv := by
    rintro ⟨j,x⟩
    apply Sigma.ext
    · rfl
    · apply heq_of_eq
      apply ULift.ext
      apply ConcreteCategory.hom_ext
      intro t
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

#print axioms circleTrunc_absorb
#print axioms circleLegEquiv
end CMDG.CondensedCM5R0.BreenDeligneProbe
