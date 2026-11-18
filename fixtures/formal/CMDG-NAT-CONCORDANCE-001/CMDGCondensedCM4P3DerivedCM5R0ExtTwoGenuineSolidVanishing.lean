import CMDGCondensedCM4P3DerivedCM5R0FourthPointRelationBoundary
import CMDGCondensedCM4P3DerivedCM5R0DiscreteExtOneClosure
import CMDGCondensedCM4P3DerivedCM5R0StoneanCechDegreeOneClosure
import CMDGCondensedCM4P3DerivedCM5R0GSCondensedProduct
import CMDGCondensedCM4P3DerivedCM5R0GSCechSecondRelation

/-!
# CMDG CM5 — unconditional Ext²(F_T,G_S) vanishing

For *arbitrary* profinite T,S, F_T is the genuine free condensed
Coeff-module and G_S the genuine free-solid coefficient object.
This source closes the second-relation extension criterion, and then
uses the protected dimension-shifting Ext² equivalence.

The exact four-point scalar cochain condition is proved (not assumed)
for every map L_T→Z_disc: the genuine alternating four-point point-map
boundary vanishes in L_T by the preceding module. This identity
transports through the actual free-module/discrete-integer Hom
equivalence. The protected categorical scalar H² boundary primitive
and its arbitrary-product extension supply a lift along d₂:F_Q→F_R
for every map induced from L_T into the protected coefficient product
presentation of G_S. Finally the protected *unconditional* Epi(F_Q→L_T)
and Mono(L_T→F_R) identify this lift with the required extension
of f:L_T→G_S, and the pinned long exact Ext sequence criterion
proves Ext²(F_T,G_S)=0.

No unbounded higher Ext vanishing, derived solidity in all shifts,
unrelated coefficient targets, or independent source-semantic
certification is asserted.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

private theorem scalar_eval_cm5SingletonPointMap
    (X : Profinite.{u}) (x : X)
    (h : ((Condensed.profiniteFree Coeff).obj X) ⟶
      discreteIntegerCoeff) :
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (Profinite.of PUnit.{u + 1})
        ((Condensed.profiniteFree Coeff).map (cm5SingletonPointMap X x) ≫ h))
      PUnit.unit =
    (freeProfiniteDiscreteIntegerHomScalarEquiv X h) x := by
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]
  rfl

private theorem scalar_eval_zero :
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (Profinite.of PUnit.{u + 1})
        (0 : ((Condensed.profiniteFree Coeff).obj
          (Profinite.of PUnit.{u + 1})) ⟶ discreteIntegerCoeff))
      PUnit.unit = 0 := by
  rfl


/-- Every scalar cochain induced by an actual morphism out of
L_T satisfies the genuine alternating four-point cocycle identity.
No separate cocycle axiom is assumed. -/
theorem secondRelation_discreteInteger_cocycle
    (T : Profinite.{u})
    (f : stoneanCechSecondRelationKernel T ⟶
      discreteIntegerCoeff) :
    integerCechTwoCocycleCondition T
      (stoneanCechTripleToSecondRelation T ≫ f) := by
  intro x y z w hxy hyz hzw
  let U := Profinite.of PUnit.{u + 1}
  let Q := stoneanPresentationCechTriples T
  let h := stoneanCechTripleToSecondRelation T ≫ f
  let m := fourthPointAlternatingFreeMap T x y z w hxy hyz hzw
  have hzero : m ≫ h = 0 := by
    change m ≫ (stoneanCechTripleToSecondRelation T ≫ f) = 0
    rw [← Category.assoc,
      fourthPointAlternatingFreeMap_comp_secondRelation_zero, zero_comp]
  have h4 :
      (((Condensed.profiniteFree Coeff).map
          (cm5SingletonPointMap Q (stoneanCechTripleOfRelated T y z w hyz hzw)) ≫ h) -
        ((Condensed.profiniteFree Coeff).map
          (cm5SingletonPointMap Q (stoneanCechTripleOfRelated T x z w
            (hxy.trans hyz) hzw)) ≫ h)) +
        ((Condensed.profiniteFree Coeff).map
          (cm5SingletonPointMap Q (stoneanCechTripleOfRelated T x y w
            hxy (hyz.trans hzw))) ≫ h) -
        ((Condensed.profiniteFree Coeff).map
          (cm5SingletonPointMap Q (stoneanCechTripleOfRelated T x y z hxy hyz)) ≫ h)
        = 0 := by
    simpa only [m, fourthPointAlternatingFreeMap,
      Preadditive.sub_comp, Preadditive.add_comp] using hzero
  let F := freeProfiniteDiscreteIntegerHomScalarEquiv U
  have hs := congrArg (fun g : (Condensed.profiniteFree Coeff).obj U ⟶
      discreteIntegerCoeff => (F g) PUnit.unit) h4
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_sub U,
    freeProfiniteDiscreteIntegerHomScalarEquiv_add U,
    freeProfiniteDiscreteIntegerHomScalarEquiv_sub U] at hs
  change
    (F ((Condensed.profiniteFree Coeff).map
        (cm5SingletonPointMap Q (stoneanCechTripleOfRelated T y z w hyz hzw)) ≫ h))
        PUnit.unit -
    (F ((Condensed.profiniteFree Coeff).map
        (cm5SingletonPointMap Q (stoneanCechTripleOfRelated T x z w
          (hxy.trans hyz) hzw)) ≫ h)) PUnit.unit +
    (F ((Condensed.profiniteFree Coeff).map
        (cm5SingletonPointMap Q (stoneanCechTripleOfRelated T x y w
          hxy (hyz.trans hzw))) ≫ h)) PUnit.unit -
    (F ((Condensed.profiniteFree Coeff).map
        (cm5SingletonPointMap Q (stoneanCechTripleOfRelated T x y z hxy hyz)) ≫ h))
        PUnit.unit = 0 at hs
  rw [scalar_eval_cm5SingletonPointMap Q,
    scalar_eval_cm5SingletonPointMap Q,
    scalar_eval_cm5SingletonPointMap Q,
    scalar_eval_cm5SingletonPointMap Q] at hs
  exact hs

#print axioms secondRelation_discreteInteger_cocycle



/-- Every map from the true second relation L_T to genuine G_S extends
through the true inclusion L_T→F_R, for arbitrary profinite T,S.
This uses the existing canonical product presentation of G_S; there
is no chosen section of the profinite presentation. -/
theorem genuineSecondRelationHom_extends
    (T S : Profinite.{u})
    (f : stoneanCechSecondRelationKernel T ⟶
      (Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechPairs T)) ⟶
      (Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S,
      kernel.ι (stoneanCechRelationToKernel T) ≫ g = f := by
  let E := stoneanCechTripleToSecondRelation T
  let i := kernel.ι (stoneanCechRelationToKernel T)
  let iso := gsFreeSolidToCoefficientProductIso S
  let h := E ≫ f ≫ iso.hom
  have hc :
      ∀ k : LiftedSourceBasisIndex S,
      integerCechTwoCocycleCondition T
        (h ≫ Pi.π (fun _ : LiftedSourceBasisIndex S =>
          discreteIntegerCoeff) k) := by
    intro k
    change integerCechTwoCocycleCondition T
      (E ≫ (f ≫ iso.hom ≫
        Pi.π (fun _ : LiftedSourceBasisIndex S =>
          discreteIntegerCoeff) k))
    exact secondRelation_discreteInteger_cocycle T _
  obtain ⟨gprod, hgprod⟩ :=
    stoneanCechSecondBoundary_integerProductCocycle_hasPotential
      T h hc
  let g := gprod ≫ iso.inv
  have hmap : stoneanCechTripleBoundary T ≫ g = E ≫ f := by
    calc
      stoneanCechTripleBoundary T ≫ g =
          (stoneanCechTripleBoundary T ≫ gprod) ≫ iso.inv :=
            (Category.assoc _ _ _).symm
      _ = h ≫ iso.inv := by rw [hgprod]
      _ = E ≫ f := by
        dsimp [h]
        simp
  refine ⟨g, ?_⟩
  haveI : Epi E := stoneanCechTripleToSecondRelation_epi_unconditional T
  apply (cancel_epi E).1
  calc
    E ≫ (i ≫ g) = (E ≫ i) ≫ g :=
      (Category.assoc _ _ _).symm
    _ = stoneanCechTripleBoundary T ≫ g := by
      rw [stoneanCechTripleToSecondRelation_comp_ι]
    _ = E ≫ f := hmap

/-- Unconditional degree-two Ext vanishing for the genuine free
profinite module and genuine free-solid coefficient target. -/
theorem freeSolid_extTwo_vanishes_unconditional
    (T S : Profinite.{u}) :
    ∀ e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T)
      ((Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S) 2,
      e = 0 := by
  apply (freeSolid_extTwo_vanishes_iff_secondRelation_hom_extends
    T S).2
  intro f
  exact genuineSecondRelationHom_extends T S f

#print axioms genuineSecondRelationHom_extends
#print axioms freeSolid_extTwo_vanishes_unconditional
#print axioms secondRelation_discreteInteger_cocycle
#print axioms genuineSecondRelationHom_extends

end CMDG.CondensedCM5R0
