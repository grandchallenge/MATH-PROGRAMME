import CMDGCondensedCM4P3DerivedCM5R0CompactProductAllDegrees
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Data.Finset.Option

/-! Finite circle-coordinate descent with the probe retained and
the same finite coordinate set used in all factors of a finite power. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.CompactCover.CircleContinuity
open CompactCover ProductContinuity
variable (S : Profinite.{u}) (I : Type u) (m : ℕ)

def circlePowerT : CompHaus.{u} :=
  CompHaus.of (S × (Fin m → I → UnitAddCircle))

def circleFamily : Option (Fin m × I) → CompHaus.{u}
  | none => profiniteToCompHaus.obj S
  | some _ => CompHaus.of (ULift.{u} UnitAddCircle)

def pack (z : circlePowerT S I m) (i : Option (Fin m × I)) :
    circleFamily S I m i :=
  match i with
  | none => z.1
  | some a => ⟨z.2 a.1 a.2⟩

def unpack (z : ∀ i, circleFamily S I m i) : circlePowerT S I m :=
  (z none,fun a i => (z (some (a,i))).down)

def packHomeo : circlePowerT S I m ≃ₜ prodT (circleFamily S I m) where
  toFun := pack S I m
  invFun := unpack S I m
  left_inv z := rfl
  right_inv z := by
    funext i
    cases i <;> rfl
  continuous_toFun := by
    apply continuous_pi
    intro i
    cases i with
    | none => exact continuous_fst
    | some a => exact continuous_uliftUp.comp ((continuous_apply a.2).comp ((continuous_apply a.1).comp continuous_snd))
  continuous_invFun := by
    apply Continuous.prodMk
    · exact continuous_apply none
    · apply continuous_pi
      intro a
      apply continuous_pi
      intro i
      exact continuous_uliftDown.comp (continuous_apply (some (a,i)))

def packIso : circlePowerT S I m ≅ prodT (circleFamily S I m) :=
  CompHausLike.isoOfHomeo (packHomeo S I m)

variable (F : Finset I)
def circleProjection : circlePowerT S I m ⟶ circlePowerT S (↥F) m :=
  CompHausLike.ofHom _ (⟨fun z => (z.1,fun a i => z.2 a i.val),
    continuous_fst.prodMk (continuous_pi fun a => continuous_pi fun i =>
      (continuous_apply i.val).comp ((continuous_apply a).comp continuous_snd))⟩ :
      C((S × (Fin m → I → UnitAddCircle)),(S × (Fin m → ↥F → UnitAddCircle))))

def circleSection : circlePowerT S (↥F) m ⟶ circlePowerT S I m := by
  classical
  exact CompHausLike.ofHom _ (⟨fun z => (z.1,fun a => extendCoordinates F (fun _ => 0) (z.2 a)),
    continuous_fst.prodMk (continuous_pi fun a =>
      (extendCoordinates F (fun _ => (0 : UnitAddCircle))).continuous.comp
        ((continuous_apply a).comp continuous_snd))⟩ :
      C((S × (Fin m → ↥F → UnitAddCircle)),(S × (Fin m → I → UnitAddCircle))))

theorem circleSection_projection : circleSection S I m F ≫ circleProjection S I m F = 𝟙 _ := by
  apply ConcreteCategory.hom_ext
  intro z
  apply Prod.ext
  · rfl
  · funext a i
    classical
    change (if h : i.val ∈ F then z.2 a ⟨i.val,h⟩ else 0) = z.2 a i
    rw [dif_pos i.property]

abbrev circlePull (r : ℕ) :
    Abelian.Ext (compactFreeFunctor.obj (circlePowerT S (↥F) m)) discreteIntegerCoeff r →+
      Abelian.Ext (compactFreeFunctor.obj (circlePowerT S I m)) discreteIntegerCoeff r :=
  (Abelian.Ext.mk₀ (compactFreeFunctor.map (circleProjection S I m F))).precomp _ (zero_add r)

theorem circlePull_injective (r : ℕ) : Function.Injective (circlePull S I m F r) := by
  intro a b h
  have hh := congrArg (fun e => (Abelian.Ext.mk₀ (compactFreeFunctor.map (circleSection S I m F))).comp e (zero_add r)) h
  change (Abelian.Ext.mk₀ (compactFreeFunctor.map (circleSection S I m F))).comp
    ((Abelian.Ext.mk₀ (compactFreeFunctor.map (circleProjection S I m F))).comp a (zero_add r)) (zero_add r) =
    (Abelian.Ext.mk₀ (compactFreeFunctor.map (circleSection S I m F))).comp
    ((Abelian.Ext.mk₀ (compactFreeFunctor.map (circleProjection S I m F))).comp b (zero_add r)) (zero_add r) at hh
  simpa only [← Abelian.Ext.comp_assoc_of_second_deg_zero,Abelian.Ext.mk₀_comp_mk₀,
    ← Functor.map_comp,circleSection_projection,compactFreeFunctor.map_id,Abelian.Ext.mk₀_id_comp] using hh

def supportCoordinates (G : Finset (Option (Fin m × I))) : Finset I := by
  classical
  exact G.eraseNone.image Prod.snd

theorem supportCoordinates_mem (G : Finset (Option (Fin m × I))) (a : Fin m) (i : I)
    (h : some (a,i) ∈ G) : i ∈ supportCoordinates I m G := by
  classical
  exact Finset.mem_image.mpr ⟨(a,i),Finset.mem_eraseNone.mpr h,rfl⟩

def factorAt (G : Finset (Option (Fin m × I))) (i : ↥G)
    (z : circlePowerT S (↥(supportCoordinates I m G)) m) : circleFamily S I m i.val :=
  match h : i.val with
  | none => z.1
  | some a => ⟨z.2 a.1 ⟨a.2,supportCoordinates_mem I m G a.1 a.2 (h ▸ i.property)⟩⟩

def factorMap (G : Finset (Option (Fin m × I))) :
    circlePowerT S (↥(supportCoordinates I m G)) m ⟶
      prodT (subT (circleFamily S I m) G) := by
  refine CompHausLike.ofHom _ ⟨fun z i => factorAt S I m G i z,?_⟩
  apply continuous_pi
  intro i
  rcases i with ⟨_ | a,hi⟩
  · exact continuous_fst
  · exact continuous_uliftUp.comp ((continuous_apply (⟨a.2,supportCoordinates_mem I m G a.1 a.2 hi⟩ : ↥(supportCoordinates I m G))).comp
      ((continuous_apply a.1).comp continuous_snd))

theorem factorMap_square (G : Finset (Option (Fin m × I))) :
    circleProjection S I m (supportCoordinates I m G) ≫ factorMap S I m G =
      (packIso S I m).hom ≫ coordinateProjection (circleFamily S I m) G := by
  apply ConcreteCategory.hom_ext
  intro z
  funext i
  rcases i with ⟨_ | a,hi⟩ <;> rfl

theorem circlePower_ext_finiteSupport (s : S) (r : ℕ)
    (e : Abelian.Ext (compactFreeFunctor.obj (circlePowerT S I m)) discreteIntegerCoeff r) :
    ∃ F : Finset I, ∃ b, circlePull S I m F r b = e := by
  let iso := compactFreeFunctor.mapIso (packIso S I m)
  let e' := (Abelian.Ext.mk₀ iso.inv).comp e (zero_add r)
  let x : ∀ i, circleFamily S I m i := fun i => match i with
    | none => s
    | some _ => ⟨0⟩
  obtain ⟨G,c,hc⟩ := compactProduct_ext_finiteSupport (circleFamily S I m) x r e'
  refine ⟨supportCoordinates I m G,
    (Abelian.Ext.mk₀ (compactFreeFunctor.map (factorMap S I m G))).comp c (zero_add r),?_⟩
  change (Abelian.Ext.mk₀ (compactFreeFunctor.map (circleProjection S I m (supportCoordinates I m G)))).comp
    ((Abelian.Ext.mk₀ (compactFreeFunctor.map (factorMap S I m G))).comp c (zero_add r)) (zero_add r) = e
  rw [← Abelian.Ext.comp_assoc_of_second_deg_zero,Abelian.Ext.mk₀_comp_mk₀,← Functor.map_comp,
    factorMap_square,Functor.map_comp,← Abelian.Ext.mk₀_comp_mk₀,Abelian.Ext.comp_assoc_of_second_deg_zero]
  change (Abelian.Ext.mk₀ iso.hom).comp (coordinatePull (circleFamily S I m) G r c) (zero_add r) = e
  rw [hc]
  change (Abelian.Ext.mk₀ iso.hom).comp ((Abelian.Ext.mk₀ iso.inv).comp e (zero_add r)) (zero_add r) = e
  rw [← Abelian.Ext.comp_assoc_of_second_deg_zero,Abelian.Ext.mk₀_comp_mk₀,Iso.hom_inv_id,Abelian.Ext.mk₀_id_comp]

#print axioms circlePower_ext_finiteSupport
#print axioms circlePull_injective
end CMDG.CondensedCM5R0.CompactCover.CircleContinuity
