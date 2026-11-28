import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCircleRealization

/-! Every Ext class of the actual transported circle resolution has
finite-coordinate support. The augmentation inherits this property
in all degrees by the exact syzygy transfer. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection CompactCover CompactCover.CircleContinuity AcyclicResolution

theorem pb_iso_injective {X Z : Ambient.{u}} (iso : X ≅ Z) (q : ℕ) :
    Function.Injective (pb discreteIntegerCoeff iso.hom q) := by
  intro a b h
  have hh := congrArg (pb discreteIntegerCoeff iso.inv q) h
  rw [pb_comp,pb_comp,Iso.inv_hom_id] at hh
  simpa [pb,Abelian.Ext.mk₀_id_comp] using hh

theorem finiteCoproduct_pb_detect {k : ℕ} (X : Fin k → Ambient.{u}) (q : ℕ)
    (a b : Abelian.Ext (∐ X) discreteIntegerCoeff q)
    (h : ∀ j, pb discreteIntegerCoeff (Sigma.ι X j) q a =
      pb discreteIntegerCoeff (Sigma.ι X j) q b) : a=b := by
  let L (j : ULift.{u} (Fin k)) : Ambient.{u} := X j.down
  let iso : (∐ L) ≅ (∐ X) :=
    Sigma.whiskerEquiv (f := L) (g := X) (Equiv.ulift : ULift.{u} (Fin k) ≃ Fin k)
      (fun _ => Iso.refl _)
  apply pb_iso_injective iso q
  apply sub_eq_zero.mp
  apply coproduct_ext_detect q L discreteIntegerCoeff
  intro j
  change pb discreteIntegerCoeff (Sigma.ι L j) q
    (pb discreteIntegerCoeff iso.hom q a - pb discreteIntegerCoeff iso.hom q b) = 0
  rw [map_sub,pb_comp,pb_comp]
  have hj : Sigma.ι L j ≫ iso.hom = Sigma.ι X j.down := by
    change Sigma.ι L j ≫ Limits.Sigma.map' (Equiv.ulift : ULift.{u} (Fin k) ≃ Fin k)
      (fun j => (Iso.refl (L j)).inv) = _
    rw [Sigma.ι_comp_map',Iso.refl_inv,Category.id_comp]
    rfl
  rw [hj,h j.down,sub_self]

variable (I : Type u) (S : Profinite.{u}) {k : ℕ} (arity : Fin k → ℕ)

theorem powerTrunc_projection {F G : Finset I} (h : F ⊆ G) (j : Fin k) :
    powerTrunc I S arity G j ≫ circleProjection S I (arity j) F =
      circleProjection S I (arity j) F := by
  classical
  apply ConcreteCategory.hom_ext
  intro z
  apply Prod.ext
  · rfl
  · funext a i
    change (if hG : i.val ∈ G then z.2 a i.val else 0) = z.2 a i.val
    rw [dif_pos (h i.property)]

theorem circleTerm_finiteSupport (s : S) (q : ℕ)
    (e : Abelian.Ext ((transport (probeSet S) (circlePsh I)).obj (polynomial arity))
      discreteIntegerCoeff q) :
    ∃ F : Finset I,
      pb discreteIntegerCoeff (changeInput (probeSet S) (circleTrunc I F) (polynomial arity)) q e = e := by
  classical
  let iso := circleTermIso I S arity
  let X := circleFamilyFree I S arity
  let a := pb discreteIntegerCoeff iso.hom q e
  let ej (j : Fin k) := pb discreteIntegerCoeff (Sigma.ι X j) q a
  choose F b hb using fun j : Fin k => circlePower_ext_finiteSupport S I (arity j) s q (ej j)
  let G := Finset.univ.biUnion F
  have hsub (j : Fin k) : F j ⊆ G := by
    intro i hi
    exact Finset.mem_biUnion.mpr ⟨j,Finset.mem_univ _,hi⟩
  have fixed (j : Fin k) :
      pb discreteIntegerCoeff (compactFreeFunctor.map (powerTrunc I S arity G j)) q (ej j) = ej j := by
    rw [← hb j]
    change pb discreteIntegerCoeff (compactFreeFunctor.map (powerTrunc I S arity G j)) q
      (pb discreteIntegerCoeff (compactFreeFunctor.map (circleProjection S I (arity j) (F j))) q (b j)) = _
    rw [pb_comp,← Functor.map_comp,powerTrunc_projection I S arity (hsub j)]
  refine ⟨G,?_⟩
  apply pb_iso_injective iso q
  rw [pb_comp]
  change pb discreteIntegerCoeff ((circleTermIso I S arity).hom ≫
    changeInput (probeSet S) (circleTrunc I G) (polynomial arity)) q e = a
  rw [circleTermIso_trunc,← pb_comp]
  apply finiteCoproduct_pb_detect X q
  intro j
  rw [pb_comp]
  change pb discreteIntegerCoeff (Sigma.ι X j ≫
    Limits.Sigma.map (fun j => compactFreeFunctor.map (powerTrunc I S arity G j))) q a = ej j
  rw [Sigma.ι_map,← pb_comp]
  exact fixed j

theorem circleResolution_termFinite (s : S) (B : UniversalBD.{u}) :
    (circleTruncations I S B).termFinite discreteIntegerCoeff := by
  intro n q e
  exact circleTerm_finiteSupport I S (B.arity n) s q e

abbrev relativeCircle (I : Type u) (S : Profinite.{u}) : Ambient.{u} :=
  moduleSheafification.obj (indexedSum (probeSet S) (circlePsh I))

abbrev relativeCircleRestrict (F : Finset I) : relativeCircle I S ⟶ relativeCircle (↥F) S :=
  (relativeSheafify (probeSet S)).map (circleRestrict I F)
abbrev relativeCircleExtend (F : Finset I) : relativeCircle (↥F) S ⟶ relativeCircle I S :=
  (relativeSheafify (probeSet S)).map (circleExtend I F)

theorem relativeCircleExtend_restrict (F : Finset I) :
    relativeCircleExtend I S F ≫ relativeCircleRestrict I S F = 𝟙 _ := by
  change (relativeSheafify (probeSet S)).map (circleExtend I F) ≫
    (relativeSheafify (probeSet S)).map (circleRestrict I F) = _
  rw [← Functor.map_comp,circleExtend_restrict]
  exact (relativeSheafify (probeSet S)).map_id _

theorem relativeCircle_ext_finiteSupport (s : S) (B : UniversalBD.{u}) (q : ℕ)
    (e : Abelian.Ext (relativeCircle I S) discreteIntegerCoeff q) :
    ∃ F : Finset I, ∃ b : Abelian.Ext (relativeCircle (↥F) S) discreteIntegerCoeff q,
      pb discreteIntegerCoeff (relativeCircleRestrict I S F) q b = e := by
  obtain ⟨F,hF⟩ := (circleTruncations I S B).target_finiteSupport discreteIntegerCoeff
    (circleResolution_termFinite I S s B) q e
  refine ⟨F,pb discreteIntegerCoeff (relativeCircleExtend I S F) q e,?_⟩
  rw [pb_comp]
  change pb discreteIntegerCoeff ((relativeSheafify (probeSet S)).map (circleRestrict I F) ≫
    (relativeSheafify (probeSet S)).map (circleExtend I F)) q e = e
  rw [← Functor.map_comp]
  exact hF

theorem relativeCircle_ext_pull_injective (F : Finset I) (q : ℕ) :
    Function.Injective (pb discreteIntegerCoeff (relativeCircleRestrict I S F) q) := by
  intro a b h
  have hh := congrArg (pb discreteIntegerCoeff (relativeCircleExtend I S F) q) h
  rw [pb_comp,pb_comp,relativeCircleExtend_restrict] at hh
  simpa [pb,Abelian.Ext.mk₀_id_comp] using hh

#print axioms relativeCircle_ext_finiteSupport
#print axioms relativeCircle_ext_pull_injective
end CMDG.CondensedCM5R0.BreenDeligneProbe
