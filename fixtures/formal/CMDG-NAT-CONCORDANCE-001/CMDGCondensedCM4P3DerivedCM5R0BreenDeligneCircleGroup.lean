import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCircleTransfer
import CMDGCondensedCM4P3DerivedCM5R0RealCircleFiniteCoordinateNaturality

/-! The point-probe continuity theorem is transported to the existing
genuine circle group, with the actual protected coordinate morphism. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection CompactCover AcyclicResolution
open RealCircleStoneanPresheaf RealCircleFiniteCoordinateNaturality

local instance (I : Type u) : IsTopologicalAddGroup (ULift.{u+1,u} (I → UnitAddCircle)) := ⟨⟩

variable (I : Type u)

abbrev circleSet : CondensedSet.{u} :=
  topCatToCondensedSet.obj (TopCat.of (ULift.{u+1,u} (I → UnitAddCircle)))

def circleDirectCondensed : Ambient.{u} := by
  letI : PreservesFiniteProducts (circlePsh I ⋙ CategoryTheory.forget Mod.{u}) := by
    change PreservesFiniteProducts (circleSet I).obj
    infer_instance
  apply Condensed.ofSheafForgetCompHaus (circlePsh I)
  change regularTopology.EqualizerCondition (circleSet I).obj
  exact Condensed.equalizerCondition (circleSet I)

def circleDirectIso : circleDirectCondensed I ≅ circleProductCondensed I := by
  letI : HasLimitsOfSize.{u,u+1} Mod.{u} := hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  let E := Condensed.StoneanCompHaus.equivalence Mod.{u}
  exact (E.counitIso.app (circleDirectCondensed I)).symm

def pointCircleIso : relativeCircle I pointProbe ≅ circleProductCondensed I :=
  moduleSheafification.mapIso (pointIndexedIso (circlePsh I)) ≪≫
    (sheafificationIso (circleDirectCondensed I)).symm ≪≫ circleDirectIso I

theorem pointIndexedIso_natural {A B : Psh.{u}} (f : A ⟶ B) :
    (indexedFunctor (probeSet pointProbe)).map f ≫ (pointIndexedIso B).hom =
      (pointIndexedIso A).hom ≫ f := by
  apply NatTrans.ext
  funext T
  apply Sigma.hom_ext
  intro j
  change Sigma.ι (fun _ : (probeSet pointProbe).obj T => A.obj T) j ≫
      Limits.Sigma.map (fun _ : (probeSet pointProbe).obj T => f.app T) ≫
      Sigma.desc (fun _ : (probeSet pointProbe).obj T => 𝟙 (B.obj T)) =
    Sigma.ι (fun _ : (probeSet pointProbe).obj T => A.obj T) j ≫
      Sigma.desc (fun _ : (probeSet pointProbe).obj T => 𝟙 (A.obj T)) ≫ f.app T
  rw [Sigma.ι_map_assoc,Sigma.ι_desc,Category.comp_id,← Category.assoc,Sigma.ι_desc,Category.id_comp]

variable (F : Finset I)
abbrev circleCoordinate : circleProductCondensed I ⟶ circleProductCondensed (↥F) :=
  circleReindex I (↥F) Subtype.val

def directRestrict : circleDirectCondensed I ⟶ circleDirectCondensed (↥F) :=
  ⟨circleRestrict I F⟩

theorem directRestrict_natural :
    directRestrict I F ≫ (circleDirectIso (↥F)).hom =
      (circleDirectIso I).hom ≫ circleCoordinate I F := by
  letI : HasLimitsOfSize.{u,u+1} Mod.{u} := hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  let E := Condensed.StoneanCompHaus.equivalence Mod.{u}
  change directRestrict I F ≫ (E.counitIso.app (circleDirectCondensed (↥F))).inv =
    (E.counitIso.app (circleDirectCondensed I)).inv ≫
      E.functor.map (stoneanSheafMap (ULift.{u+1,u} (I → UnitAddCircle))
        (reindexTopHom I (↥F) UnitAddCircle Subtype.val)
        (reindexTopHom_continuous I (↥F) UnitAddCircle Subtype.val))
  have h := E.counitIso.inv.naturality (directRestrict I F)
  exact h

theorem pointCircleIso_natural :
    relativeCircleRestrict I pointProbe F ≫ (pointCircleIso (↥F)).hom =
      (pointCircleIso I).hom ≫ circleCoordinate I F := by
  change moduleSheafification.map ((indexedFunctor (probeSet pointProbe)).map (circleRestrict I F)) ≫
    (moduleSheafification.map (pointIndexedIso (circlePsh (↥F))).hom ≫
      (sheafificationIso (circleDirectCondensed (↥F))).inv ≫ (circleDirectIso (↥F)).hom) =
    (moduleSheafification.map (pointIndexedIso (circlePsh I)).hom ≫
      (sheafificationIso (circleDirectCondensed I)).inv ≫ (circleDirectIso I).hom) ≫ circleCoordinate I F
  rw [← Category.assoc,← Functor.map_comp,pointIndexedIso_natural,Functor.map_comp]
  simp only [Category.assoc]
  have h := (sheafificationNatIso (J:=coherentTopology CompHaus.{u}) (D:=Mod.{u})).inv.naturality (directRestrict I F)
  change moduleSheafification.map (circleRestrict I F) ≫
    (sheafificationIso (circleDirectCondensed (↥F))).inv =
    (sheafificationIso (circleDirectCondensed I)).inv ≫ directRestrict I F at h
  rw [← Category.assoc (moduleSheafification.map (circleRestrict I F)),h,Category.assoc,directRestrict_natural]

theorem circleGroup_ext_finiteSupport (B : UniversalBD.{u}) (q : ℕ)
    (e : Abelian.Ext (circleProductCondensed I) discreteIntegerCoeff q) :
    ∃ F : Finset I, ∃ b : Abelian.Ext (circleProductCondensed (↥F)) discreteIntegerCoeff q,
      pb discreteIntegerCoeff (circleCoordinate I F) q b = e := by
  obtain ⟨G,c,hc⟩ := relativeCircle_ext_finiteSupport I pointProbe PUnit.unit B q
    (pb discreteIntegerCoeff (pointCircleIso I).hom q e)
  refine ⟨G,pb discreteIntegerCoeff (pointCircleIso (↥G)).inv q c,?_⟩
  apply pb_iso_injective (pointCircleIso I) q
  rw [pb_comp,← pointCircleIso_natural,pb_comp,Category.assoc,Iso.hom_inv_id,Category.comp_id]
  exact hc


theorem circleGroup_ext_pull_injective (F : Finset I) (q : ℕ) :
    Function.Injective (pb discreteIntegerCoeff (circleCoordinate I F) q) := by
  intro a b h
  apply pb_iso_injective (pointCircleIso (↥F)) q
  apply relativeCircle_ext_pull_injective I pointProbe F q
  rw [pb_comp,pb_comp,pointCircleIso_natural,← pb_comp,← pb_comp,h]

#print axioms circleGroup_ext_finiteSupport
#print axioms circleGroup_ext_pull_injective
end CMDG.CondensedCM5R0.BreenDeligneProbe
