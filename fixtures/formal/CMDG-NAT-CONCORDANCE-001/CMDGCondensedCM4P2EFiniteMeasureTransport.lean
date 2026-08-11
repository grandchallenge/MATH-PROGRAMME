import CMDGCondensedCM4P2EFiniteDualPushforward

/-!
# CMDG CM4-P2-E finite measure-presheaf transport

This auxiliary fixture identifies the actual finite restriction of the protected P2-D measure
presheaf functor with the already-certified finite internal-dual functor. The comparison is induced
solely by the natural finite source decomposition
`finiteDiscreteContinuousPresheafFamilyNatIso` and contravariance of closed internal Hom in its
first argument.

No finite-free condensed-module comparison is asserted here, so E1 remains open.
-/

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
open scoped CategoryTheory.MonoidalClosed

noncomputable local instance : MonoidalClosed
    (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :=
  MonoidalClosed.FunctorCategory.monoidalClosed

/-- The actual finite restriction of the protected P2-D measure presheaf functor. -/
noncomputable abbrev finiteMeasurePresheafFunctor :
    FintypeCat.{u} ⥤
      (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :=
  FintypeCat.toProfinite ⋙ CMDG.CondensedCM4P2D.measurePresheafFunctor

/-- The accepted finite source-family comparison at a fixed finite set. -/
noncomputable abbrev finiteMeasureSourceFamilyIso (X : FintypeCat.{u}) :=
  CMDG.CondensedCM4P2E.FiniteTransport.finiteDiscreteContinuousPresheafFamilyNatIso.app (op X)

/-- The raw source-presheaf morphism induced by a finite map after promotion to profinite spaces. -/
noncomputable def finiteMeasureSourcePresheafMap
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    CMDG.CondensedCM4P2D.discreteContinuousPresheaf.obj
        (op (FintypeCat.toProfinite.obj Y)) ⟶
      CMDG.CondensedCM4P2D.discreteContinuousPresheaf.obj
        (op (FintypeCat.toProfinite.obj X)) :=
  CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map
    (FintypeCat.toProfinite.map f).op

/-- The raw morphism of the actual finite P2-D measure-presheaf restriction. -/
noncomputable def finiteMeasurePresheafMap
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    finiteMeasurePresheafFunctor.obj X ⟶ finiteMeasurePresheafFunctor.obj Y :=
  (MonoidalClosed.pre (finiteMeasureSourcePresheafMap f)).app
    CMDG.CondensedCM4P2D.coefficientPresheaf

lemma finiteMeasurePresheafFunctor_map_eq
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    finiteMeasurePresheafFunctor.map f = finiteMeasurePresheafMap f := by
  rfl

/-- Forward closed-Hom transport through the inverse finite source comparison. -/
noncomputable def finiteMeasurePresheafFamilyHom (X : FintypeCat.{u}) :
    finiteMeasurePresheafFunctor.obj X ⟶ finiteFamilyInternalHomFunctor.obj X :=
  (MonoidalClosed.pre (finiteMeasureSourceFamilyIso X).inv).app
    CMDG.CondensedCM4P2D.coefficientPresheaf

/-- Inverse closed-Hom transport through the forward finite source comparison. -/
noncomputable def finiteMeasurePresheafFamilyInv (X : FintypeCat.{u}) :
    finiteFamilyInternalHomFunctor.obj X ⟶ finiteMeasurePresheafFunctor.obj X :=
  (MonoidalClosed.pre (finiteMeasureSourceFamilyIso X).hom).app
    CMDG.CondensedCM4P2D.coefficientPresheaf

/-- For a fixed finite set, transport the P2-D internal dual through the canonical finite source
family decomposition. Contravariance of `pre` means the inverse source isomorphism gives the
forward dual map. -/
noncomputable def finiteMeasurePresheafFamilyIso (X : FintypeCat.{u}) :
    finiteMeasurePresheafFunctor.obj X ≅ finiteFamilyInternalHomFunctor.obj X := by
  let i := finiteMeasureSourceFamilyIso X
  refine
    { hom := finiteMeasurePresheafFamilyHom X
      inv := finiteMeasurePresheafFamilyInv X
      hom_inv_id := ?_
      inv_hom_id := ?_ }
  · change
      (MonoidalClosed.pre i.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf ≫
          (MonoidalClosed.pre i.hom).app CMDG.CondensedCM4P2D.coefficientPresheaf =
        𝟙 _
    have hpre := congrArg
      (fun η => η.app CMDG.CondensedCM4P2D.coefficientPresheaf)
      (MonoidalClosed.pre_map i.hom i.inv)
    calc
      (MonoidalClosed.pre i.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf ≫
          (MonoidalClosed.pre i.hom).app CMDG.CondensedCM4P2D.coefficientPresheaf =
        (MonoidalClosed.pre (i.hom ≫ i.inv)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf := by
            simpa only [NatTrans.comp_app] using hpre.symm
      _ = (MonoidalClosed.pre (𝟙 _)).app CMDG.CondensedCM4P2D.coefficientPresheaf := by
            rw [i.hom_inv_id]
      _ = 𝟙 _ := by simp
  · change
      (MonoidalClosed.pre i.hom).app CMDG.CondensedCM4P2D.coefficientPresheaf ≫
          (MonoidalClosed.pre i.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf =
        𝟙 _
    have hpre := congrArg
      (fun η => η.app CMDG.CondensedCM4P2D.coefficientPresheaf)
      (MonoidalClosed.pre_map i.inv i.hom)
    calc
      (MonoidalClosed.pre i.hom).app CMDG.CondensedCM4P2D.coefficientPresheaf ≫
          (MonoidalClosed.pre i.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf =
        (MonoidalClosed.pre (i.inv ≫ i.hom)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf := by
            simpa only [NatTrans.comp_app] using hpre.symm
      _ = (MonoidalClosed.pre (𝟙 _)).app CMDG.CondensedCM4P2D.coefficientPresheaf := by
            rw [i.inv_hom_id]
      _ = 𝟙 _ := by simp

lemma finiteMeasurePresheafFamilyIso_hom (X : FintypeCat.{u}) :
    (finiteMeasurePresheafFamilyIso X).hom = finiteMeasurePresheafFamilyHom X := by
  rfl

lemma finiteFamilyInternalHomFunctor_map_eq
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    finiteFamilyInternalHomFunctor.map f = finiteFamilyInternalHomMap f := by
  rfl

/-- The coefficient-family composite functor map is definitionally the named pullback map. -/
lemma finiteCoefficientFamilyPresheafFunctor_map_eq
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafFunctor.map f.op =
      CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op := by
  rfl

/-- The finite P2-D source composite functor map is definitionally the named promoted source map. -/
lemma finiteDiscreteContinuousPresheafFunctor_map_eq
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    CMDG.CondensedCM4P2E.FiniteTransport.finiteDiscreteContinuousPresheafFunctor.map f.op =
      finiteMeasureSourcePresheafMap f := by
  rfl

/-- Raw naturality of the accepted finite source-family inverse, expressed against the actual
P2-D source-presheaf map. -/
lemma finiteMeasureSourceFamilyInv_naturality
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op ≫
        (finiteMeasureSourceFamilyIso X).inv =
      (finiteMeasureSourceFamilyIso Y).inv ≫ finiteMeasureSourcePresheafMap f := by
  have h :=
    CMDG.CondensedCM4P2E.FiniteTransport.finiteDiscreteContinuousPresheafFamilyNatIso.inv.naturality
      f.op
  rw [finiteCoefficientFamilyPresheafFunctor_map_eq f,
    finiteDiscreteContinuousPresheafFunctor_map_eq f] at h
  exact h

/-- Raw naturality of the forward finite measure/source-family transport. Keeping this statement
at the morphism level avoids expensive reduction of the two composite functor presentations. -/
lemma finiteMeasurePresheafFamilyHom_naturality
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    finiteMeasurePresheafMap f ≫ finiteMeasurePresheafFamilyHom Y =
      finiteMeasurePresheafFamilyHom X ≫ finiteFamilyInternalHomMap f := by
  let iX := finiteMeasureSourceFamilyIso X
  let iY := finiteMeasureSourceFamilyIso Y
  have hnat :
      CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op ≫
          iX.inv =
        iY.inv ≫ finiteMeasureSourcePresheafMap f := by
    exact finiteMeasureSourceFamilyInv_naturality f
  have hleft := congrArg
    (fun η => η.app CMDG.CondensedCM4P2D.coefficientPresheaf)
    (MonoidalClosed.pre_map iY.inv (finiteMeasureSourcePresheafMap f))
  have hright := congrArg
    (fun η => η.app CMDG.CondensedCM4P2D.coefficientPresheaf)
    (MonoidalClosed.pre_map
      (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op)
      iX.inv)
  change
    (MonoidalClosed.pre (finiteMeasureSourcePresheafMap f)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre iY.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf =
      (MonoidalClosed.pre iX.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre
          (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op)).app
            CMDG.CondensedCM4P2D.coefficientPresheaf
  calc
    (MonoidalClosed.pre (finiteMeasureSourcePresheafMap f)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre iY.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf =
      (MonoidalClosed.pre (iY.inv ≫ finiteMeasureSourcePresheafMap f)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf := by
            simpa only [NatTrans.comp_app] using hleft.symm
    _ = (MonoidalClosed.pre
          (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op ≫
            iX.inv)).app CMDG.CondensedCM4P2D.coefficientPresheaf := by
          exact congrArg
            (fun k => (MonoidalClosed.pre k).app CMDG.CondensedCM4P2D.coefficientPresheaf)
            hnat.symm
    _ = (MonoidalClosed.pre iX.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf ≫
          (MonoidalClosed.pre
            (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op)).app
              CMDG.CondensedCM4P2D.coefficientPresheaf := by
            simpa only [NatTrans.comp_app] using hright

/-- The fixed-finite-set comparison is natural in finite maps. -/
noncomputable def finiteMeasurePresheafFamilyNatIso :
    finiteMeasurePresheafFunctor ≅ finiteFamilyInternalHomFunctor :=
  NatIso.ofComponents
    (fun X => finiteMeasurePresheafFamilyIso X)
    (by
      intro X Y f
      rw [finiteMeasurePresheafFunctor_map_eq,
        finiteMeasurePresheafFamilyIso_hom,
        finiteMeasurePresheafFamilyIso_hom,
        finiteFamilyInternalHomFunctor_map_eq]
      exact finiteMeasurePresheafFamilyHom_naturality f)

#check finiteMeasurePresheafFunctor
#check finiteMeasureSourceFamilyIso
#check finiteMeasureSourcePresheafMap
#check finiteMeasurePresheafMap
#check finiteMeasurePresheafFunctor_map_eq
#check finiteMeasurePresheafFamilyHom
#check finiteMeasurePresheafFamilyInv
#check finiteMeasurePresheafFamilyIso
#check finiteMeasurePresheafFamilyIso_hom
#check finiteFamilyInternalHomFunctor_map_eq
#check finiteCoefficientFamilyPresheafFunctor_map_eq
#check finiteDiscreteContinuousPresheafFunctor_map_eq
#check finiteMeasureSourceFamilyInv_naturality
#check finiteMeasurePresheafFamilyHom_naturality
#check finiteMeasurePresheafFamilyNatIso

#print axioms finiteMeasureSourcePresheafMap
#print axioms finiteMeasurePresheafMap
#print axioms finiteMeasurePresheafFunctor_map_eq
#print axioms finiteMeasurePresheafFamilyHom
#print axioms finiteMeasurePresheafFamilyInv
#print axioms finiteMeasurePresheafFamilyIso
#print axioms finiteMeasurePresheafFamilyIso_hom
#print axioms finiteFamilyInternalHomFunctor_map_eq
#print axioms finiteCoefficientFamilyPresheafFunctor_map_eq
#print axioms finiteDiscreteContinuousPresheafFunctor_map_eq
#print axioms finiteMeasureSourceFamilyInv_naturality
#print axioms finiteMeasurePresheafFamilyHom_naturality
#print axioms finiteMeasurePresheafFamilyNatIso

end CMDG.CondensedCM4P2E.FiniteDualTransport
