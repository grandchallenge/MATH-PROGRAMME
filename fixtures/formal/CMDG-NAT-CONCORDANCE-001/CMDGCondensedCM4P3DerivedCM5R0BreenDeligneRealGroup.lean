import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealRealization

noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection CompactCover

variable (I : Type u)

abbrev realSet : CondensedSet.{u} :=
  topCatToCondensedSet.obj (TopCat.of (ULift.{u+1,u} (I → ℝ)))

def realDirectCondensed : Ambient.{u} := by
  letI : PreservesFiniteProducts (realPsh I ⋙ CategoryTheory.forget Mod.{u}) := by
    change PreservesFiniteProducts (realSet I).obj
    infer_instance
  apply Condensed.ofSheafForgetCompHaus (realPsh I)
  change regularTopology.EqualizerCondition (realSet I).obj
  exact Condensed.equalizerCondition (realSet I)

def realDirectIso : realDirectCondensed I ≅
    RealCircleStoneanPresheaf.realProductCondensed I := by
  letI : HasLimitsOfSize.{u,u+1} Mod.{u} := hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  let E := Condensed.StoneanCompHaus.equivalence Mod.{u}
  exact (E.counitIso.app (realDirectCondensed I)).symm

abbrev pointProbe : Profinite.{u} := Profinite.of PUnit.{u+1}

def pointSection (T : CompHaus.{u}ᵒᵖ) : (probeSet pointProbe).obj T :=
  ⟨CompHausLike.ofHom _ (ContinuousMap.const _ PUnit.unit)⟩

theorem pointSection_unique (T : CompHaus.{u}ᵒᵖ) (x : (probeSet pointProbe).obj T) :
    x = pointSection T := by
  apply ULift.ext
  apply ConcreteCategory.hom_ext
  intro t
  change (_ : PUnit.{u+1}) = _
  exact Subsingleton.elim _ _

def pointIndexedIsoAt (A : Psh.{u}) (T : CompHaus.{u}ᵒᵖ) :
    (indexedSum (probeSet pointProbe) A).obj T ≅ A.obj T where
  hom := Sigma.desc (fun _ => 𝟙 _)
  inv := Sigma.ι (fun _ : (probeSet pointProbe).obj T => A.obj T) (pointSection T)
  hom_inv_id := by
    apply Sigma.hom_ext
    intro j
    change Sigma.ι (fun _ : (probeSet pointProbe).obj T => A.obj T) j ≫
      (Sigma.desc (fun _ : (probeSet pointProbe).obj T => 𝟙 (A.obj T)) ≫ Sigma.ι (fun _ : (probeSet pointProbe).obj T => A.obj T) (pointSection T)) =
      Sigma.ι (fun _ : (probeSet pointProbe).obj T => A.obj T) j ≫ 𝟙 (∐ fun _ : (probeSet pointProbe).obj T => A.obj T)
    rw [← Category.assoc,Sigma.ι_desc,Category.id_comp,Category.comp_id,pointSection_unique T j]
  inv_hom_id := Sigma.ι_desc _ _

def pointIndexedIso (A : Psh.{u}) : indexedSum (probeSet pointProbe) A ≅ A :=
  NatIso.ofComponents (pointIndexedIsoAt A) (by
    intro T U f
    apply Sigma.hom_ext
    intro j
    change Sigma.ι (fun _ : (probeSet pointProbe).obj T => A.obj T) j ≫
      Limits.Sigma.map' ((probeSet pointProbe).map f) (fun _ => A.map f) ≫
      Sigma.desc (fun _ : (probeSet pointProbe).obj U => 𝟙 (A.obj U)) =
      Sigma.ι (fun _ : (probeSet pointProbe).obj T => A.obj T) j ≫
        (Sigma.desc (fun _ : (probeSet pointProbe).obj T => 𝟙 (A.obj T)) ≫ A.map f)
    rw [Sigma.ι_comp_map'_assoc,Sigma.ι_desc,Category.comp_id,← Category.assoc,Sigma.ι_desc,Category.id_comp])

def pointRealIso : moduleSheafification.obj (indexedSum (probeSet pointProbe) (realPsh I)) ≅
    RealCircleStoneanPresheaf.realProductCondensed I :=
  moduleSheafification.mapIso (pointIndexedIso (realPsh I)) ≪≫
    (sheafificationIso (realDirectCondensed I)).symm ≪≫ realDirectIso I

theorem realGroup_extZero (B : UniversalBD.{u}) (q : ℕ)
    (e : Abelian.Ext (RealCircleStoneanPresheaf.realProductCondensed I)
      discreteIntegerCoeff q) : e = 0 := by
  cases q with
  | zero =>
    apply Abelian.Ext.addEquiv₀.injective
    rw [map_zero]
    apply (cancel_epi (pointRealIso I).hom).1
    rw [comp_zero]
    exact (realBD pointProbe I B).target_homZero _
  | succ q =>
    exact CompactCover.Dyadic.ext_zero_of_retract (pointRealIso I).inv (pointRealIso I).hom
      (pointRealIso I).inv_hom_id q (relativeReal_extZero pointProbe I B (q+1)) e

#print axioms realGroup_extZero
end CMDG.CondensedCM5R0.BreenDeligneProbe
