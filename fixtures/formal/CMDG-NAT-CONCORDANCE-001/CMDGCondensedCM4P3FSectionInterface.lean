import CMDGCondensedCM4P2EPointProbe

/-!
# CMDG CM4-P3-F test-object section interface

This auxiliary fixture packages the exact test-object description of the P2-D internal dual.
For a module `A` and compact Hausdorff test object `T`, a section at `T` of
`underline Hom(A_disc, R_disc)` is identified with an `R`-linear family
`A → LocallyConstant T R`.

The construction is basis-free. The forward map evaluates the enriched end at the identity
object over `T` and then on constant `A`-sections. The inverse reconstructs every slice by the
pointwise formula `h ↦ (y ↦ L (h y) (k y))`. The reverse triangle is certified by the same
constant-map point-probe geometry used in the protected P2-E rank-one bridge.
-/

namespace CMDG.CondensedCM4P3F.SectionInterface

universe u

open CategoryTheory Limits Opposite
open CategoryTheory.Enriched.FunctorCategory
open scoped CategoryTheory.MonoidalClosed

abbrev R := CMDG.CondensedCM4P2D.R.{u}
abbrev PresheafModule := CMDG.CondensedCM4P2D.PresheafModule.{u}

noncomputable abbrev coefficientPresheaf : PresheafModule :=
  CMDG.CondensedCM4P2D.coefficientPresheaf

noncomputable local instance : MonoidalClosed PresheafModule :=
  MonoidalClosed.FunctorCategory.monoidalClosed

noncomputable abbrev discretePresheaf (A : ModuleCat.{u + 1} R) : PresheafModule :=
  (CondensedMod.LocallyConstant.functorToPresheaves R).obj A

noncomputable def internalDualPresheaf (A : ModuleCat.{u + 1} R) : PresheafModule :=
  (MonoidalClosed.internalHom.obj (op (discretePresheaf A))).obj coefficientPresheaf

lemma internalDualPresheaf_eq_functorEnrichedHom (A : ModuleCat.{u + 1} R) :
    internalDualPresheaf A =
      functorEnrichedHom (ModuleCat.{u + 1} R) (discretePresheaf A) coefficientPresheaf := rfl

noncomputable abbrev coefficientAt (T : CompHaus.{u}) : ModuleCat.{u + 1} R :=
  coefficientPresheaf.obj (op T)

noncomputable abbrev familyModule (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) :
    ModuleCat.{u + 1} R :=
  ModuleCat.of R (A →ₗ[R] LocallyConstant T R)

noncomputable def identityProjection
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) :=
  enrichedHomπ
    (ModuleCat.{u + 1} R)
    (Under.forget (op T) ⋙ discretePresheaf A)
    (Under.forget (op T) ⋙ coefficientPresheaf)
    (Under.mk (𝟙 (op T)))

noncomputable def projectionLinearMap
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    (k : Under (op T)) (φ : internalDualPresheaf A |>.obj (op T)) :
    (discretePresheaf A).obj k.right ⟶ coefficientPresheaf.obj k.right := by
  exact show
    (Under.forget (op T) ⋙ discretePresheaf A).obj k ⟶
      (Under.forget (op T) ⋙ coefficientPresheaf).obj k from
    (enrichedHomπ
      (ModuleCat.{u + 1} R)
      (Under.forget (op T) ⋙ discretePresheaf A)
      (Under.forget (op T) ⋙ coefficientPresheaf)
      k) φ

/-- Evaluate an enriched-end section on constant `A`-sections at the identity object over `T`. -/
noncomputable def evaluationFamily
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    (φ : (internalDualPresheaf A).obj (op T)) :
    A →ₗ[R] LocallyConstant T R :=
  (projectionLinearMap A T (Under.mk (𝟙 (op T))) φ).hom.comp
    (LocallyConstant.constₗ R)

/-- The forward linear map from test-object sections to `R`-linear locally constant families. -/
noncomputable def sectionToFamily
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) :
    (internalDualPresheaf A).obj (op T) ⟶ familyModule A T :=
  ModuleCat.ofHom
    { toFun := evaluationFamily A T
      map_add' := by
        intro φ ψ
        apply LinearMap.ext
        intro a
        apply LocallyConstant.ext
        intro t
        have hp := map_add (identityProjection A T).hom φ ψ
        have ha := congrArg
          (fun q => (ModuleCat.Hom.hom q) (LocallyConstant.const T a)) hp
        have ht := congrArg
          (fun q : coefficientPresheaf.obj (op T) =>
            (show LocallyConstant T R from q) t) ha
        simpa [evaluationFamily, projectionLinearMap, identityProjection] using ht
      map_smul' := by
        intro r φ
        apply LinearMap.ext
        intro a
        apply LocallyConstant.ext
        intro t
        have hp := map_smul (identityProjection A T).hom r φ
        have ha := congrArg
          (fun q => (ModuleCat.Hom.hom q) (LocallyConstant.const T a)) hp
        have ht := congrArg
          (fun q : coefficientPresheaf.obj (op T) =>
            (show LocallyConstant T R from q) t) ha
        simpa [evaluationFamily, projectionLinearMap, identityProjection] using ht }

/-- Pointwise reconstruction of a slice map from an `R`-linear family on `T`. -/
noncomputable def reconstructedSection
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    (L : familyModule A T) (k : Under (op T))
    (h : (discretePresheaf A).obj k.right) :
    coefficientPresheaf.obj k.right where
  toFun := fun y =>
    (show LocallyConstant k.right.unop R from
      coefficientPresheaf.map k.hom (L ((show LocallyConstant k.right.unop A from h) y))) y
  isLocallyConstant := by
    rw [IsLocallyConstant.iff_eventually_eq]
    intro y
    have hh := (show LocallyConstant k.right.unop A from h).isLocallyConstant.eventually_eq y
    have hL :=
      (show LocallyConstant k.right.unop R from
        coefficientPresheaf.map k.hom
          (L ((show LocallyConstant k.right.unop A from h) y))).isLocallyConstant.eventually_eq y
    filter_upwards [hh, hL] with y' hy' hLy'
    change
      (show LocallyConstant k.right.unop R from
        coefficientPresheaf.map k.hom
          (L ((show LocallyConstant k.right.unop A from h) y'))) y' =
        (show LocallyConstant k.right.unop R from
          coefficientPresheaf.map k.hom
            (L ((show LocallyConstant k.right.unop A from h) y))) y
    have harg :
        L ((show LocallyConstant k.right.unop A from h) y') =
          L ((show LocallyConstant k.right.unop A from h) y) :=
      congrArg (fun a : A => L a) hy'
    have hpull := congrArg
      (fun s : LocallyConstant T R =>
        (show LocallyConstant k.right.unop R from coefficientPresheaf.map k.hom s)) harg
    have hpullPoint := congrArg
      (fun s : LocallyConstant k.right.unop R => s y') hpull
    exact hpullPoint.trans hLy'

noncomputable def reconstructedLinearMap
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    (L : familyModule A T) (k : Under (op T)) :
    (discretePresheaf A).obj k.right ⟶ coefficientPresheaf.obj k.right :=
  ModuleCat.ofHom
    (show ((discretePresheaf A).obj k.right) →ₗ[R]
        (coefficientPresheaf.obj k.right) from
      { toFun := reconstructedSection A T L k
        map_add' := by
          intro h₁ h₂
          apply LocallyConstant.ext
          intro y
          change
            (show LocallyConstant k.right.unop R from
              coefficientPresheaf.map k.hom
                (L ((show LocallyConstant k.right.unop A from h₁) y +
                  (show LocallyConstant k.right.unop A from h₂) y))) y =
              (show LocallyConstant k.right.unop R from
                (coefficientPresheaf.map k.hom
                  (L ((show LocallyConstant k.right.unop A from h₁) y)) +
                coefficientPresheaf.map k.hom
                  (L ((show LocallyConstant k.right.unop A from h₂) y)))) y
          simp only [map_add, LocallyConstant.add_apply]
        map_smul' := by
          intro r h
          apply LocallyConstant.ext
          intro y
          change
            (show LocallyConstant k.right.unop R from
              coefficientPresheaf.map k.hom
                (L (r • (show LocallyConstant k.right.unop A from h) y))) y =
              (show LocallyConstant k.right.unop R from
                r • coefficientPresheaf.map k.hom
                  (L ((show LocallyConstant k.right.unop A from h) y))) y
          simp only [map_smul, LocallyConstant.smul_apply] })

lemma coefficientPullback_triangle
    (T : CompHaus.{u}) {i j : Under (op T)} (f : i ⟶ j) :
    coefficientPresheaf.map i.hom ≫ coefficientPresheaf.map f.right =
      coefficientPresheaf.map j.hom := by
  rw [← coefficientPresheaf.map_comp, Under.w f]

lemma discretePullback_triangle
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    {i j : Under (op T)} (f : i ⟶ j) :
    (discretePresheaf A).map i.hom ≫ (discretePresheaf A).map f.right =
      (discretePresheaf A).map j.hom := by
  rw [← (discretePresheaf A).map_comp, Under.w f]

/-- The reconstructed slice maps are natural in the under-category variable. -/
lemma reconstructedLinearMap_naturality
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    (L : familyModule A T)
    {i j : Under (op T)} (f : i ⟶ j) :
    reconstructedLinearMap A T L i ≫ coefficientPresheaf.map f.right =
      (discretePresheaf A).map f.right ≫ reconstructedLinearMap A T L j := by
  apply ModuleCat.hom_injective
  ext h
  apply LocallyConstant.ext
  intro y
  change
    (show LocallyConstant j.right.unop R from
      coefficientPresheaf.map f.right
        (reconstructedSection A T L i h)) y =
      (show LocallyConstant j.right.unop R from
        reconstructedSection A T L j ((discretePresheaf A).map f.right h)) y
  change
    (show LocallyConstant j.right.unop R from
      coefficientPresheaf.map f.right
        (reconstructedSection A T L i h)) y =
      (show LocallyConstant j.right.unop R from
        coefficientPresheaf.map j.hom
          (L ((show LocallyConstant j.right.unop A from
            (discretePresheaf A).map f.right h) y))) y
  have hsource :
      ((show LocallyConstant j.right.unop A from
        (discretePresheaf A).map f.right h) y) =
        ((show LocallyConstant i.right.unop A from h) (f.right.unop y)) := rfl
  rw [hsource]
  have htriangle := congrArg
    (fun q : coefficientAt T ⟶ coefficientPresheaf.obj j.right =>
      q (L ((show LocallyConstant i.right.unop A from h) (f.right.unop y))))
    (coefficientPullback_triangle T f)
  have hpoint := congrArg
    (fun q : coefficientPresheaf.obj j.right =>
      (show LocallyConstant j.right.unop R from q) y) htriangle
  exact hpoint

/-- Package a family into the enriched-end cone. -/
noncomputable def reconstructionToIhom
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) (k : Under (op T)) :
    familyModule A T ⟶
      (ihom ((Under.forget (op T) ⋙ discretePresheaf A).obj k)).obj
        ((Under.forget (op T) ⋙ coefficientPresheaf).obj k) :=
  ModuleCat.ofHom
    (show (familyModule A T) →ₗ[R]
        ((ihom ((Under.forget (op T) ⋙ discretePresheaf A).obj k)).obj
          ((Under.forget (op T) ⋙ coefficientPresheaf).obj k)) from
      { toFun := fun L => reconstructedLinearMap A T L k
        map_add' := by
          intro L₁ L₂
          apply ModuleCat.hom_injective
          apply LinearMap.ext
          intro h
          apply LocallyConstant.ext
          intro y
          change
            (show LocallyConstant k.right.unop R from
              coefficientPresheaf.map k.hom
                ((L₁ + L₂) ((show LocallyConstant k.right.unop A from h) y))) y =
              (show LocallyConstant k.right.unop R from
                coefficientPresheaf.map k.hom
                    (L₁ ((show LocallyConstant k.right.unop A from h) y)) +
                  coefficientPresheaf.map k.hom
                    (L₂ ((show LocallyConstant k.right.unop A from h) y))) y
          simp only [LinearMap.add_apply, map_add, LocallyConstant.add_apply]
        map_smul' := by
          intro r L
          apply ModuleCat.hom_injective
          apply LinearMap.ext
          intro h
          apply LocallyConstant.ext
          intro y
          change
            (show LocallyConstant k.right.unop R from
              coefficientPresheaf.map k.hom
                ((r • L) ((show LocallyConstant k.right.unop A from h) y))) y =
              (show LocallyConstant k.right.unop R from
                r • coefficientPresheaf.map k.hom
                  (L ((show LocallyConstant k.right.unop A from h) y))) y
          simp only [LinearMap.smul_apply, map_smul, LocallyConstant.smul_apply] })

set_option backward.isDefEq.respectTransparency false in
lemma reconstructionToIhom_condition
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    {i j : Under (op T)} (f : i ⟶ j) :
    reconstructionToIhom A T i ≫
        (ihom ((Under.forget (op T) ⋙ discretePresheaf A).obj i)).map
          ((Under.forget (op T) ⋙ coefficientPresheaf).map f) =
      reconstructionToIhom A T j ≫
        (MonoidalClosed.pre ((Under.forget (op T) ⋙ discretePresheaf A).map f)).app
          ((Under.forget (op T) ⋙ coefficientPresheaf).obj j) := by
  apply ModuleCat.hom_injective
  apply LinearMap.ext
  intro L
  change
    ((ihom ((Under.forget (op T) ⋙ discretePresheaf A).obj i)).map
      ((Under.forget (op T) ⋙ coefficientPresheaf).map f))
        (reconstructedLinearMap A T L i) =
      ((MonoidalClosed.pre ((Under.forget (op T) ⋙ discretePresheaf A).map f)).app
        ((Under.forget (op T) ⋙ coefficientPresheaf).obj j))
        (reconstructedLinearMap A T L j)
  rw [ModuleCat.ihom_map_apply,
    CMDG.CondensedCM4P2E.InternalHom.monoidalClosed_pre_apply]
  exact reconstructedLinearMap_naturality A T L f

/-- Reconstruct an enriched-end section from an `R`-linear locally constant family. -/
noncomputable def familyToSection
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) :
    familyModule A T ⟶ (internalDualPresheaf A).obj (op T) := by
  change
    familyModule A T ⟶
      enrichedHom
        (ModuleCat.{u + 1} R)
        (Under.forget (op T) ⋙ discretePresheaf A)
        (Under.forget (op T) ⋙ coefficientPresheaf)
  exact end_.lift
    (fun k => reconstructionToIhom A T k)
    (fun i j f => by
      dsimp [CategoryTheory.Enriched.FunctorCategory.diagram, CategoryTheory.eHomFunctor,
        CategoryTheory.Functor.whiskerLeft]
      simpa only [
        MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerLeft,
        MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerRight] using
        reconstructionToIhom_condition A T f)

lemma familyToSection_projection
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) (k : Under (op T)) :
    familyToSection A T ≫
      enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op T) ⋙ discretePresheaf A)
        (Under.forget (op T) ⋙ coefficientPresheaf)
        k =
      reconstructionToIhom A T k := by
  unfold familyToSection
  exact end_.lift_π _ _ k

-- Easy triangle: reconstructing a family and re-evaluating it returns the original family.
set_option backward.isDefEq.respectTransparency false in
lemma familyToSection_sectionToFamily
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) :
    familyToSection A T ≫ sectionToFamily A T = 𝟙 (familyModule A T) := by
  apply ModuleCat.hom_injective
  apply LinearMap.ext
  intro L
  apply LinearMap.ext
  intro a
  apply LocallyConstant.ext
  intro t
  have hp := ConcreteCategory.congr_hom
    (familyToSection_projection A T (Under.mk (𝟙 (op T)))) L
  have ha := ConcreteCategory.congr_hom hp
    (show (discretePresheaf A).obj (op T) from LocallyConstant.const T a)
  have ht := congrArg
    (fun q : coefficientPresheaf.obj (op T) =>
      (show LocallyConstant T R from q) t) ha
  simpa [sectionToFamily, evaluationFamily, projectionLinearMap,
    reconstructionToIhom, reconstructedLinearMap, reconstructedSection] using ht

-- Enriched-end naturality of every projected slice.
set_option backward.isDefEq.respectTransparency false in
lemma projectionLinearMap_naturality
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    {i j : Under (op T)} (f : i ⟶ j)
    (φ : (internalDualPresheaf A).obj (op T)) :
    projectionLinearMap A T i φ ≫
        (Under.forget (op T) ⋙ coefficientPresheaf).map f =
      (Under.forget (op T) ⋙ discretePresheaf A).map f ≫
        projectionLinearMap A T j φ := by
  have hbase :
      enrichedHomπ
            (ModuleCat.{u + 1} R)
            (Under.forget (op T) ⋙ discretePresheaf A)
            (Under.forget (op T) ⋙ coefficientPresheaf)
            i ≫
          (ihom ((Under.forget (op T) ⋙ discretePresheaf A).obj i)).map
            ((Under.forget (op T) ⋙ coefficientPresheaf).map f) =
        enrichedHomπ
            (ModuleCat.{u + 1} R)
            (Under.forget (op T) ⋙ discretePresheaf A)
            (Under.forget (op T) ⋙ coefficientPresheaf)
            j ≫
          (MonoidalClosed.pre ((Under.forget (op T) ⋙ discretePresheaf A).map f)).app
            ((Under.forget (op T) ⋙ coefficientPresheaf).obj j) := by
    simpa only [
        MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerLeft,
        MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerRight] using
      (enrichedHom_condition
        (ModuleCat.{u + 1} R)
        (Under.forget (op T) ⋙ discretePresheaf A)
        (Under.forget (op T) ⋙ coefficientPresheaf)
        f)
  have hcond := congrArg (fun q => q φ) hbase
  change
    ((ihom ((Under.forget (op T) ⋙ discretePresheaf A).obj i)).map
      ((Under.forget (op T) ⋙ coefficientPresheaf).map f))
        (projectionLinearMap A T i φ) =
      ((MonoidalClosed.pre ((Under.forget (op T) ⋙ discretePresheaf A).map f)).app
        ((Under.forget (op T) ⋙ coefficientPresheaf).obj j))
        (projectionLinearMap A T j φ) at hcond
  rw [ModuleCat.ihom_map_apply,
    CMDG.CondensedCM4P2E.InternalHom.monoidalClosed_pre_apply] at hcond
  exact hcond

set_option backward.isDefEq.respectTransparency false in
lemma projectionLinearMap_naturality_apply
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    {i j : Under (op T)} (f : i ⟶ j)
    (φ : (internalDualPresheaf A).obj (op T))
    (h : (Under.forget (op T) ⋙ discretePresheaf A).obj i) :
    ((Under.forget (op T) ⋙ coefficientPresheaf).map f
        (projectionLinearMap A T i φ h)) =
      projectionLinearMap A T j φ
        (((Under.forget (op T) ⋙ discretePresheaf A).map f) h) := by
  change
    (projectionLinearMap A T i φ ≫
      (Under.forget (op T) ⋙ coefficientPresheaf).map f) h =
    ((Under.forget (op T) ⋙ discretePresheaf A).map f ≫
      projectionLinearMap A T j φ) h
  exact ConcreteCategory.congr_hom (projectionLinearMap_naturality A T f φ) h

noncomputable abbrev pointProbeObject
    (T : CompHaus.{u}) (k : Under (op T)) (y : k.right.unop) : Under (op T) :=
  CMDG.CondensedCM4P2E.InternalHom.rankOnePointProbeObject T k y

noncomputable abbrev pointProbeFrom
    (T : CompHaus.{u}) (k : Under (op T)) (y : k.right.unop) :
    k ⟶ pointProbeObject T k y :=
  CMDG.CondensedCM4P2E.InternalHom.rankOnePointProbeFrom T k y

noncomputable abbrev pointProbeFromIdentity
    (T : CompHaus.{u}) (k : Under (op T)) (y : k.right.unop) :
    Under.mk (𝟙 (op T)) ⟶ pointProbeObject T k y :=
  CMDG.CondensedCM4P2E.InternalHom.rankOnePointProbeFromIdentity T k y

lemma discretePullback_pointProbe
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    (k : Under (op T)) (y : k.right.unop)
    (h : (discretePresheaf A).obj k.right) :
    (discretePresheaf A).map (pointProbeFrom T k y).right h =
      (show (discretePresheaf A).obj (pointProbeObject T k y).right from
        LocallyConstant.const (pointProbeObject T k y).right.unop
          ((show LocallyConstant k.right.unop A from h) y)) := by
  change
    LocallyConstant.comap (pointProbeFrom T k y).right.unop.hom.hom
        (show LocallyConstant k.right.unop A from h) = _
  exact congrArg
    (fun q => q (show LocallyConstant k.right.unop A from h))
    (LocallyConstant.comap_const
      (pointProbeFrom T k y).right.unop.hom.hom y (fun _ => rfl))

lemma discretePullback_pointProbeFromIdentity
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    (k : Under (op T)) (y : k.right.unop) (a : A) :
    (discretePresheaf A).map (pointProbeFromIdentity T k y).right
        (show (discretePresheaf A).obj (op T) from LocallyConstant.const T a) =
      (show (discretePresheaf A).obj (pointProbeObject T k y).right from
        LocallyConstant.const (pointProbeObject T k y).right.unop a) := by
  rfl

/- Point-probe recovery: every slice value is determined by identity-slice evaluation
on the pointwise value of the source section. -/
set_option backward.isDefEq.respectTransparency false in
lemma projection_point_value
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    (k : Under (op T)) (φ : (internalDualPresheaf A).obj (op T))
    (h : (discretePresheaf A).obj k.right) (y : k.right.unop) :
    (show LocallyConstant k.right.unop R from projectionLinearMap A T k φ h) y =
      evaluationFamily A T φ ((show LocallyConstant k.right.unop A from h) y)
        (k.hom.unop y) := by
  let P := pointProbeObject T k y
  let a : A := (show LocallyConstant k.right.unop A from h) y
  have hk := projectionLinearMap_naturality_apply A T (pointProbeFrom T k y) φ h
  change
    coefficientPresheaf.map (pointProbeFrom T k y).right
        (projectionLinearMap A T k φ h) =
      projectionLinearMap A T P φ
        ((discretePresheaf A).map (pointProbeFrom T k y).right h) at hk
  rw [CMDG.CondensedCM4P2E.InternalHom.coefficientPullback_pointProbe T k y,
    discretePullback_pointProbe A T k y h] at hk
  have hid := projectionLinearMap_naturality_apply A T
    (pointProbeFromIdentity T k y) φ
    (show (discretePresheaf A).obj (op T) from LocallyConstant.const T a)
  change
    coefficientPresheaf.map (pointProbeFromIdentity T k y).right
        (projectionLinearMap A T (Under.mk (𝟙 (op T))) φ
          (show (discretePresheaf A).obj (op T) from LocallyConstant.const T a)) =
      projectionLinearMap A T P φ
        ((discretePresheaf A).map (pointProbeFromIdentity T k y).right
          (show (discretePresheaf A).obj (op T) from LocallyConstant.const T a)) at hid
  rw [CMDG.CondensedCM4P2E.InternalHom.coefficientPullback_pointProbeFromIdentity T k y,
    discretePullback_pointProbeFromIdentity A T k y a] at hid
  rw [← hid] at hk
  have hv := congrArg
    (fun q : coefficientPresheaf.obj P.right =>
      (show LocallyConstant P.right.unop R from q) y) hk
  exact hv

set_option backward.isDefEq.respectTransparency false in
lemma projection_recovery
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u})
    (k : Under (op T)) (φ : (internalDualPresheaf A).obj (op T)) :
    projectionLinearMap A T k φ =
      reconstructedLinearMap A T (evaluationFamily A T φ) k := by
  apply ModuleCat.hom_injective
  apply LinearMap.ext
  intro h
  apply LocallyConstant.ext
  intro y
  simpa [reconstructedLinearMap, reconstructedSection] using
    projection_point_value A T k φ h y

lemma internalDualPresheaf_obj_eq_enrichedHom
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) :
    (internalDualPresheaf A).obj (op T) =
      enrichedHom
        (ModuleCat.{u + 1} R)
        (Under.forget (op T) ⋙ discretePresheaf A)
        (Under.forget (op T) ⋙ coefficientPresheaf) := by
  rfl

noncomputable def internalDualAtIso
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) :
    (internalDualPresheaf A).obj (op T) ≅
      enrichedHom
        (ModuleCat.{u + 1} R)
        (Under.forget (op T) ⋙ discretePresheaf A)
        (Under.forget (op T) ⋙ coefficientPresheaf) :=
  eqToIso (internalDualPresheaf_obj_eq_enrichedHom A T)

lemma internalDualAtIso_hom_projection
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) (k : Under (op T)) :
    (internalDualAtIso A T).hom ≫
      enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op T) ⋙ discretePresheaf A)
        (Under.forget (op T) ⋙ coefficientPresheaf)
        k =
      enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op T) ⋙ discretePresheaf A)
        (Under.forget (op T) ⋙ coefficientPresheaf)
        k := by
  rfl

/-- Hard triangle, reduced to point-probe recovery on every enriched-end projection. -/
lemma sectionToFamily_familyToSection
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) :
    sectionToFamily A T ≫ familyToSection A T =
      𝟙 ((internalDualPresheaf A).obj (op T)) := by
  rw [← cancel_mono (internalDualAtIso A T).hom]
  apply end_.hom_ext
  intro k
  change
    ((sectionToFamily A T ≫ familyToSection A T) ≫
        (internalDualAtIso A T).hom) ≫
        enrichedHomπ
          (ModuleCat.{u + 1} R)
          (Under.forget (op T) ⋙ discretePresheaf A)
          (Under.forget (op T) ⋙ coefficientPresheaf)
          k =
      ((𝟙 ((internalDualPresheaf A).obj (op T))) ≫
        (internalDualAtIso A T).hom) ≫
        enrichedHomπ
          (ModuleCat.{u + 1} R)
          (Under.forget (op T) ⋙ discretePresheaf A)
          (Under.forget (op T) ⋙ coefficientPresheaf)
          k
  simp only [Category.assoc, Category.id_comp,
    internalDualAtIso_hom_projection,
    familyToSection_projection]
  apply ModuleCat.hom_injective
  ext φ
  change
    reconstructedLinearMap A T (evaluationFamily A T φ) k =
      projectionLinearMap A T k φ
  exact (projection_recovery A T k φ).symm

/-- Exact test-object equivalence for the internal dual of a discrete module. -/
noncomputable def sectionFamilyIso
    (A : ModuleCat.{u + 1} R) (T : CompHaus.{u}) :
    (internalDualPresheaf A).obj (op T) ≅ familyModule A T where
  hom := sectionToFamily A T
  inv := familyToSection A T
  hom_inv_id := sectionToFamily_familyToSection A T
  inv_hom_id := familyToSection_sectionToFamily A T

/-- Specialization to the P2-D measure presheaf: a `T`-section is exactly an `R`-linear family
`C(X,R) → LocallyConstant T R`. -/
noncomputable def measureSectionFamilyIso
    (X : Profinite.{u}) (T : CompHaus.{u}) :
    (CMDG.CondensedCM4P2D.measurePresheafObj X).obj (op T) ≅
      familyModule (CMDG.CondensedCM4P2D.continuousFunctions.obj (op X)) T := by
  change
    (internalDualPresheaf (CMDG.CondensedCM4P2D.continuousFunctions.obj (op X))).obj (op T) ≅ _
  exact sectionFamilyIso _ T

#check sectionFamilyIso
#check measureSectionFamilyIso

#print axioms sectionToFamily_familyToSection
#print axioms familyToSection_sectionToFamily
#print axioms sectionFamilyIso
#print axioms measureSectionFamilyIso

end CMDG.CondensedCM4P3F.SectionInterface
