import CMDGCondensedCM4P2EFiniteMeasureTransport
import CMDGCondensedCM4P2EAlgebraic

/-!
# CMDG CM4-P2-E finite free-presheaf transport

This auxiliary fixture starts the free-side closure of E1. It identifies the canonical finite
coefficient-family presheaf with the locally-constant presheaf of the small finite free module.
The comparison uses only the canonical finite `Pi`/`Finsupp` equivalence and records its action
on the canonical delta generators.

No sheaf-level finite comparison or global P2-E equivalence is asserted here.
-/

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
attribute [local instance] FintypeCat.fintype

abbrev R := CMDG.CondensedCM4P2D.R.{u}

/-- The small finite free modules, realized as locally-constant module presheaves. -/
noncomputable abbrev finiteSmallFreePresheafFunctor :
    FintypeCat.{u} ⥤ (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R) :=
  CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule ⋙
    CondensedMod.LocallyConstant.functorToPresheaves R

/-- At a fixed finite set, the canonical coefficient family is the locally-constant presheaf of
the small finite free module. -/
noncomputable def finiteCoefficientFamilyFreeIso (X : FintypeCat.{u}) :
    CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X ≅
      finiteSmallFreePresheafFunctor.obj X :=
  (CMDG.CondensedCM4P2E.FiniteTransport.finiteFunctionPresheafFamilyIso X).symm ≪≫
    (CondensedMod.LocallyConstant.functorToPresheaves R).mapIso
      ((Finsupp.linearEquivFunOnFinite R R X.obj).symm.toModuleIso)

/-- The canonical free-module delta inclusion at a finite point. -/
noncomputable def finiteSmallFreeCoordinateModuleMap
    (X : FintypeCat.{u}) (x : X.obj) :
    ModuleCat.of R R ⟶ CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule.obj X :=
  ModuleCat.ofHom (Finsupp.lsingle x)

/-- The corresponding delta inclusion after passage to locally-constant presheaves. -/
noncomputable def finiteSmallFreeCoordinateInclusion
    (X : FintypeCat.{u}) (x : X.obj) :
    CMDG.CondensedCM4P2D.coefficientPresheaf ⟶ finiteSmallFreePresheafFunctor.obj X :=
  (CondensedMod.LocallyConstant.functorToPresheaves R).map
    (finiteSmallFreeCoordinateModuleMap X x)

/-- The family/free comparison sends the canonical coordinate inclusion to `Finsupp.single`. -/
lemma finiteCoordinateInclusion_freeIso
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteCoordinateInclusion X x ≫ (finiteCoefficientFamilyFreeIso X).hom =
      finiteSmallFreeCoordinateInclusion X x := by
  classical
  ext S h
  apply LocallyConstant.ext
  intro s
  apply Finsupp.ext
  intro y
  change (if y = x then h s else 0) = (Finsupp.single x (h s)) y
  by_cases hy : y = x
  · subst y
    simp
  · simp [hy]

#check finiteSmallFreePresheafFunctor
#check finiteCoefficientFamilyFreeIso
#check finiteSmallFreeCoordinateModuleMap
#check finiteSmallFreeCoordinateInclusion
#check finiteCoordinateInclusion_freeIso

#print axioms finiteCoefficientFamilyFreeIso
#print axioms finiteSmallFreeCoordinateModuleMap
#print axioms finiteSmallFreeCoordinateInclusion
#print axioms finiteCoordinateInclusion_freeIso

end CMDG.CondensedCM4P2E.FiniteDualTransport
