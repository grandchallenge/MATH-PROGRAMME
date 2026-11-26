import CMDGCondensedCM4P3DerivedCM5R0RealCircleCondensedComplex
import Mathlib.Condensed.Discrete.Module
import Mathlib.Condensed.Limits

/-! Identify the actual Stonean topological integer product with the
categorical product of discrete integer sheaves, via probe maps. -/
noncomputable section
universe u
open CategoryTheory CategoryTheory.Limits Opposite
open CMDG.CondensedCM5R0.RealCircleStoneanPresheaf
namespace CMDG.CondensedCM5R0.IntegerProductBridge

abbrev R := ULift.{u+1} ℤ
abbrev Mod := ModuleCat.{u+1} R.{u}
abbrev Sh := Sheaf (coherentTopology Stonean.{u}) Mod.{u}

local instance : HasLimitsOfSize.{u,u+1} Mod.{u} :=
  hasLimitsOfSizeShrink.{u,u+1,u+1,u} _

abbrev E : Sh.{u} ≌ CondensedAb.{u} := Condensed.StoneanCompHaus.equivalence Mod.{u}
abbrev Zdisc : CondensedAb.{u} :=
  (CondensedMod.LocallyConstant.functor R.{u}).obj (ModuleCat.of R.{u} R.{u})
abbrev Zst : Sh.{u} := E.{u}.inverse.obj Zdisc.{u}

def lcAt (X : Stonean.{u}ᵒᵖ) (v : Zst.{u}.obj.obj X) :
    LocallyConstant X.unop R.{u} := v

def coord (I : Type u) (i : I) :
    stoneanModuleSheaf.{u} (ULift.{u+1,u} (I → ℤ)) ⟶ Zst.{u} :=
  ⟨{
      app := fun X => ModuleCat.ofHom {
        toFun := fun g => ⟨fun x => ⟨(g x).down i⟩,
          (IsLocallyConstant.iff_continuous _).mpr
            (continuous_uliftUp.comp ((continuous_apply i).comp
              (continuous_uliftDown.comp g.continuous)))⟩
        map_add' := by intro a b; ext x; rfl
        map_smul' := by intro a b; ext x; rfl }
      naturality := by intros X Y f; ext g x; rfl }⟩

def stFan (I : Type u) : Fan (fun _ : I => Zst.{u}) :=
  Fan.mk _ (coord.{u} I)

def assemble (I : Type u) (s : Fan (fun _ : I => Zst.{u})) :
    s.pt ⟶ stoneanModuleSheaf.{u} (ULift.{u+1,u} (I → ℤ)) :=
  ⟨{
      app := fun X => ModuleCat.ofHom {
        toFun := fun a => ⟨fun x => ⟨fun i =>
          (lcAt X ((s.proj i).hom.app X a) x).down⟩,
          continuous_uliftUp.comp (continuous_pi fun i =>
            continuous_uliftDown.comp ((lcAt X ((s.proj i).hom.app X a)).continuous))⟩
        map_add' := by
          intro a b; apply ContinuousMap.ext; intro x; apply ULift.ext; funext i
          change (lcAt X ((s.proj i).hom.app X (a+b)) x).down =
            (lcAt X ((s.proj i).hom.app X a) x).down + (lcAt X ((s.proj i).hom.app X b) x).down
          rw [map_add]; rfl
        map_smul' := by
          intro a b; apply ContinuousMap.ext; intro x; apply ULift.ext; funext i
          rw [ContinuousMap.smul_apply]
          simp only [RingHom.id_apply]
          have hh := ((s.proj i).hom.app X).hom.map_smul a b
          have h := congrArg (fun z => (lcAt X z x).down) hh
          exact h }
      naturality := by
        intro X Y f
        ext a
        apply ContinuousMap.ext; intro x; apply ULift.ext; funext i
        have h := congrArg (fun k => (lcAt Y (k a) x).down) ((s.proj i).hom.naturality f)
        exact h }⟩

def stFanIsLimit (I : Type u) : IsLimit (stFan.{u} I) :=
  Fan.IsLimit.mk _ (assemble I)
    (by
      intro s i
      apply Sheaf.hom_ext
      ext X a
      change (LocallyConstant.mk _ _) = _
      ext x
      rfl)
    (by
      intro s m hm
      apply Sheaf.hom_ext
      ext X a
      change (m.hom.app X a : C(X.unop, ULift.{u+1,u} (I → ℤ))) = _
      apply ContinuousMap.ext; intro x; apply ULift.ext; funext i
      have h := congrArg (fun k => (lcAt X (k.hom.app X a) x).down) (hm i)
      exact h)

def equivFanLimit {C : Type*} [Category C] {D : Type*} [Category D]
    (e : C ≌ D) {I : Type*} {X : I → C} (c : Fan X) (h : IsLimit c) :
    IsLimit (Fan.mk (e.functor.obj c.pt) (fun i => e.functor.map (c.proj i))) :=
  (Fan.isLimitMapConeEquiv e.functor X c).toFun (isLimitOfPreserves e.functor h)

def changeFanLimit {C : Type*} [Category C] {I : Type*} {X Y : I → C}
    (c : Fan X) (h : IsLimit c) (e : ∀ i, X i ≅ Y i) :
    IsLimit (Fan.mk c.pt (fun i => c.proj i ≫ (e i).hom)) := by
  refine Fan.IsLimit.mk _ (fun s => h.lift (Fan.mk s.pt (fun i => s.proj i ≫ (e i).inv))) ?_ ?_
  · intro s i
    change h.lift _ ≫ (c.proj i ≫ (e i).hom) = _
    rw [← Category.assoc]
    have hh := h.fac (Fan.mk s.pt (fun i => s.proj i ≫ (e i).inv)) (Discrete.mk i)
    change h.lift (Fan.mk s.pt (fun i => s.proj i ≫ (e i).inv)) ≫ c.proj i = s.proj i ≫ (e i).inv at hh
    rw [hh]
    simp
  · intro s m hm
    apply h.hom_ext
    intro j
    have hj := hm j.as
    change m ≫ (c.proj j.as ≫ (e j.as).hom) = _ at hj
    rw [← Category.assoc] at hj
    have h' := congrArg (fun f => f ≫ (e j.as).inv) hj
    have hh := h.fac (Fan.mk s.pt (fun i => s.proj i ≫ (e i).inv)) j
    rw [hh]
    change m ≫ c.proj j.as = s.proj j.as ≫ (e j.as).inv
    simpa [Category.assoc] using h'

def integerFan (I : Type u) : Fan (fun _ : I => Zdisc.{u}) :=
  Fan.mk (realCircleCondensedSequence.{u} I).X₁
    (fun i => E.{u}.functor.map (coord.{u} I i) ≫ E.{u}.counitIso.hom.app Zdisc.{u})

def integerFanIsLimit (I : Type u) : IsLimit (integerFan.{u} I) := by
  let e : Sh.{u} ≌ CondensedAb.{u} := E.{u}
  exact changeFanLimit _ (equivFanLimit e (stFan.{u} I) (stFanIsLimit.{u} I))
    (fun _ : I => e.counitIso.app Zdisc.{u})

#print axioms integerFanIsLimit
end CMDG.CondensedCM5R0.IntegerProductBridge
