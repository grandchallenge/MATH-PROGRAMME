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

/-- The finite internal duals form a covariant functor of finite sets. -/
noncomputable def finiteFamilyInternalHomFunctor :
    FintypeCat.{u} ⥤
      (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) where
  obj X := finiteFamilyInternalHom X
  map f := finiteFamilyInternalHomMap f
  map_id X := by
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
  map_comp f g := by
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

/-- The coefficient-family objects equipped with the covariant action transported through the
certified fixed-finite-set internal-dual isomorphisms. This is not yet identified with canonical
finite-free pushforward. -/
noncomputable def finiteCoefficientFamilyCovariantFunctor :
    FintypeCat.{u} ⥤
      (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) where
  obj X := CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X
  map {X Y} f :=
    (finiteFamilyInternalHomIso X).inv ≫
      finiteFamilyInternalHomFunctor.map f ≫
      (finiteFamilyInternalHomIso Y).hom
  map_id X := by
    change
      (finiteFamilyInternalHomIso X).inv ≫
          𝟙 (finiteFamilyInternalHomFunctor.obj X) ≫
          (finiteFamilyInternalHomIso X).hom =
        𝟙 (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X)
    rw [Category.comp_id]
    exact (finiteFamilyInternalHomIso X).inv_hom_id
  map_comp f g := by
    change
      (finiteFamilyInternalHomIso _).inv ≫
          finiteFamilyInternalHomFunctor.map (f ≫ g) ≫
          (finiteFamilyInternalHomIso _).hom =
        ((finiteFamilyInternalHomIso _).inv ≫
            finiteFamilyInternalHomFunctor.map f ≫
            (finiteFamilyInternalHomIso _).hom) ≫
          (finiteFamilyInternalHomIso _).inv ≫
            finiteFamilyInternalHomFunctor.map g ≫
            (finiteFamilyInternalHomIso _).hom
    rw [finiteFamilyInternalHomFunctor.map_comp]
    simp only [Category.assoc, Iso.hom_inv_id_assoc]

/-- Naturality package for the certified fixed-finite-set internal-dual isomorphisms. -/
noncomputable def finiteFamilyInternalHomNatIso :
    finiteFamilyInternalHomFunctor ≅ finiteCoefficientFamilyCovariantFunctor :=
  NatIso.ofComponents
    (fun X => finiteFamilyInternalHomIso X)
    (by
      intro X Y f
      change
        finiteFamilyInternalHomFunctor.map f ≫ (finiteFamilyInternalHomIso Y).hom =
          (finiteFamilyInternalHomIso X).hom ≫
            (finiteFamilyInternalHomIso X).inv ≫
              finiteFamilyInternalHomFunctor.map f ≫
                (finiteFamilyInternalHomIso Y).hom
      simp only [Iso.hom_inv_id_assoc])

#check finiteFamilyInternalHomMap
#check finiteFamilyInternalHomFunctor
#check finiteCoefficientFamilyCovariantFunctor
#check finiteFamilyInternalHomNatIso

#print axioms finiteFamilyInternalHomMap
#print axioms finiteFamilyInternalHomFunctor
#print axioms finiteCoefficientFamilyCovariantFunctor
#print axioms finiteFamilyInternalHomNatIso

end CMDG.CondensedCM4P2E.FiniteDualTransport
