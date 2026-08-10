import CMDGCondensedCM4P2EFiniteDualFamilyIso

/-!
# CMDG CM4-P2-E finite dual naturality

This auxiliary fixture upgrades the certified fixed-finite-set internal-dual isomorphisms to
functorial data. The internal dual is covariant in finite sets because the finite coefficient
family is contravariant and internal Hom is contravariant in its first argument.

The coefficient-family covariant action below is deliberately defined by transport through the
certified internal-dual isomorphism. A later checkpoint must identify that transported action with
the canonical finite-free pushforward before E1 can close.
-/

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
open scoped CategoryTheory.MonoidalClosed BigOperators
attribute [local instance] FintypeCat.fintype

noncomputable local instance : MonoidalClosed
    (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :=
  MonoidalClosed.FunctorCategory.monoidalClosed

/-- Covariant action on finite internal duals, obtained by applying `pre` to the contravariant
coefficient-family pullback. -/
noncomputable def finiteFamilyInternalHomMap
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    finiteFamilyInternalHom X ⟶ finiteFamilyInternalHom Y :=
  (MonoidalClosed.pre
      (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op)).app
    CMDG.CondensedCM4P2D.coefficientPresheaf

lemma finiteFamilyInternalHomMap_id (X : FintypeCat.{u}) :
    finiteFamilyInternalHomMap (𝟙 X) = 𝟙 (finiteFamilyInternalHom X) := by
  change
    (MonoidalClosed.pre
        (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap
          (𝟙 X).op)).app CMDG.CondensedCM4P2D.coefficientPresheaf =
      𝟙 (finiteFamilyInternalHom X)
  have h :
      CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap
          (𝟙 X).op =
        𝟙 (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X) := by
    ext S a x s
    rfl
  rw [h, MonoidalClosed.pre_id]
  rfl

lemma finiteFamilyInternalHomMap_comp
    {X Y Z : FintypeCat.{u}} (f : X ⟶ Y) (g : Y ⟶ Z) :
    finiteFamilyInternalHomMap (f ≫ g) =
      finiteFamilyInternalHomMap f ≫ finiteFamilyInternalHomMap g := by
  change
    (MonoidalClosed.pre
        (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap
          (f ≫ g).op)).app CMDG.CondensedCM4P2D.coefficientPresheaf =
      finiteFamilyInternalHomMap f ≫ finiteFamilyInternalHomMap g
  have h :
      CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap
          (f ≫ g).op =
        CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap g.op ≫
          CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op := by
    ext S a z s
    rfl
  rw [h, MonoidalClosed.pre_map]
  rfl

/-- The finite internal duals form a covariant functor of finite sets. -/
noncomputable def finiteFamilyInternalHomFunctor :
    FintypeCat.{u} ⥤
      (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) where
  obj X := finiteFamilyInternalHom X
  map f := finiteFamilyInternalHomMap f
  map_id X := finiteFamilyInternalHomMap_id X
  map_comp f g := finiteFamilyInternalHomMap_comp f g

/-- Reassociated form of the certified family evaluation/extension triangle. -/
lemma finiteFamilyEvaluation_extension_assoc
    (X : FintypeCat.{u})
    {Z : CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}}
    (h : finiteFamilyInternalHom X ⟶ Z) :
    finiteFamilyEvaluation X ≫ finiteFamilyExtension X ≫ h = h := by
  rw [← Category.assoc, finiteFamilyEvaluation_extension, Category.id_comp]

/-- The coefficient-family objects equipped with the covariant action transported through the
certified fixed-finite-set internal-dual isomorphisms. This is not yet identified with canonical
finite-free pushforward. -/
noncomputable def finiteCoefficientFamilyCovariantFunctor :
    FintypeCat.{u} ⥤
      (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) where
  obj X := CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X
  map {X Y} f :=
    finiteFamilyExtension X ≫ finiteFamilyInternalHomMap f ≫ finiteFamilyEvaluation Y
  map_id X := by
    change
      finiteFamilyExtension X ≫ finiteFamilyInternalHomMap (𝟙 X) ≫ finiteFamilyEvaluation X =
        𝟙 (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X)
    rw [finiteFamilyInternalHomMap_id, Category.id_comp]
    exact finiteFamilyExtension_evaluation X
  map_comp f g := by
    change
      finiteFamilyExtension _ ≫ finiteFamilyInternalHomMap (f ≫ g) ≫ finiteFamilyEvaluation _ =
        (finiteFamilyExtension _ ≫ finiteFamilyInternalHomMap f ≫ finiteFamilyEvaluation _) ≫
          finiteFamilyExtension _ ≫ finiteFamilyInternalHomMap g ≫ finiteFamilyEvaluation _
    rw [finiteFamilyInternalHomMap_comp]
    rw [finiteFamilyEvaluation_extension_assoc]

/-- Naturality package for the certified fixed-finite-set internal-dual isomorphisms. -/
noncomputable def finiteFamilyInternalHomNatIso :
    finiteFamilyInternalHomFunctor ≅ finiteCoefficientFamilyCovariantFunctor :=
  NatIso.ofComponents
    (fun X => finiteFamilyInternalHomIso X)
    (by
      intro X Y f
      change
        finiteFamilyInternalHomMap f ≫ finiteFamilyEvaluation Y =
          finiteFamilyEvaluation X ≫
            finiteFamilyExtension X ≫ finiteFamilyInternalHomMap f ≫ finiteFamilyEvaluation Y
      rw [← Category.assoc, finiteFamilyEvaluation_extension, Category.id_comp])

#check finiteFamilyInternalHomMap
#check finiteFamilyInternalHomMap_id
#check finiteFamilyInternalHomMap_comp
#check finiteFamilyInternalHomFunctor
#check finiteFamilyEvaluation_extension_assoc
#check finiteCoefficientFamilyCovariantFunctor
#check finiteFamilyInternalHomNatIso

#print axioms finiteFamilyInternalHomMap
#print axioms finiteFamilyInternalHomMap_id
#print axioms finiteFamilyInternalHomMap_comp
#print axioms finiteFamilyInternalHomFunctor
#print axioms finiteFamilyEvaluation_extension_assoc
#print axioms finiteCoefficientFamilyCovariantFunctor
#print axioms finiteFamilyInternalHomNatIso

end CMDG.CondensedCM4P2E.FiniteDualTransport
