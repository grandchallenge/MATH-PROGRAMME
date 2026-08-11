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

/-- For a fixed finite set, transport the P2-D internal dual through the canonical finite source
family decomposition. Contravariance of `pre` means the inverse source isomorphism gives the
forward dual map. -/
noncomputable def finiteMeasurePresheafFamilyIso (X : FintypeCat.{u}) :
    finiteMeasurePresheafFunctor.obj X ≅ finiteFamilyInternalHomFunctor.obj X := by
  let i := CMDG.CondensedCM4P2E.FiniteTransport.finiteDiscreteContinuousPresheafFamilyNatIso.app
    (op X)
  refine
    { hom := (MonoidalClosed.pre i.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf
      inv := (MonoidalClosed.pre i.hom).app CMDG.CondensedCM4P2D.coefficientPresheaf
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

/-- The fixed-finite-set comparison is natural in finite maps. This is the exact transport from
actual P2-D finite measure morphisms to the finite internal-dual morphisms already certified in
the preceding checkpoints. -/
noncomputable def finiteMeasurePresheafFamilyNatIso :
    finiteMeasurePresheafFunctor ≅ finiteFamilyInternalHomFunctor :=
  NatIso.ofComponents
    (fun X => finiteMeasurePresheafFamilyIso X)
    (by
      intro X Y f
      let iX :=
        CMDG.CondensedCM4P2E.FiniteTransport.finiteDiscreteContinuousPresheafFamilyNatIso.app
          (op X)
      let iY :=
        CMDG.CondensedCM4P2E.FiniteTransport.finiteDiscreteContinuousPresheafFamilyNatIso.app
          (op Y)
      change
        (MonoidalClosed.pre
            (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op)).app
              CMDG.CondensedCM4P2D.coefficientPresheaf ≫
            (MonoidalClosed.pre iY.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf =
          (MonoidalClosed.pre iX.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf ≫
            (MonoidalClosed.pre
              (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op)).app
                CMDG.CondensedCM4P2D.coefficientPresheaf
      have hnat :=
        CMDG.CondensedCM4P2E.FiniteTransport.finiteDiscreteContinuousPresheafFamilyNatIso.inv.naturality
          f.op
      change
        CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op ≫
            iX.inv =
          iY.inv ≫ CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op at hnat
      have hleft := congrArg
        (fun η => η.app CMDG.CondensedCM4P2D.coefficientPresheaf)
        (MonoidalClosed.pre_map iY.inv
          (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op))
      have hright := congrArg
        (fun η => η.app CMDG.CondensedCM4P2D.coefficientPresheaf)
        (MonoidalClosed.pre_map
          (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op)
          iX.inv)
      calc
        (MonoidalClosed.pre
            (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op)).app
              CMDG.CondensedCM4P2D.coefficientPresheaf ≫
            (MonoidalClosed.pre iY.inv).app CMDG.CondensedCM4P2D.coefficientPresheaf =
          (MonoidalClosed.pre
            (iY.inv ≫ CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op)).app
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
                simpa only [NatTrans.comp_app] using hright)

#check finiteMeasurePresheafFunctor
#check finiteMeasurePresheafFamilyIso
#check finiteMeasurePresheafFamilyNatIso

#print axioms finiteMeasurePresheafFamilyIso
#print axioms finiteMeasurePresheafFamilyNatIso

end CMDG.CondensedCM4P2E.FiniteDualTransport
