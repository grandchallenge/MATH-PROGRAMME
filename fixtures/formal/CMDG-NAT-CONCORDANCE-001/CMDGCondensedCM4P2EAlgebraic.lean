import CMDGCondensedCM4P2E

/-!
# CMDG CM4-P2-E finite algebraic naturality

This auxiliary fixture isolates the remaining algebraic naturality layer from the certified
P2-E comparison fixture. It proves no sheaf-level internal-Hom comparison.
-/

namespace CMDG.CondensedCM4P2E.Algebraic

universe u

open CategoryTheory
open scoped BigOperators

attribute [local instance] FintypeCat.fintype

abbrev R := CMDG.CondensedCM4P2E.R.{u}

/-- Pullback of finite functions along a map of finite sets. -/
noncomputable def finiteFunctionPullback {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    (Y → R.{u}) →ₗ[R.{u}] (X → R.{u}) where
  toFun h := fun x => h (f x)
  map_add' h k := by
    funext x
    rfl
  map_smul' c h := by
    funext x
    rfl

/-- The algebraic dual of finite function modules with its canonical covariant functoriality. -/
noncomputable def finiteFunctionDualModule :
    FintypeCat.{u} ⥤ ModuleCat.{u + 1} R.{u} where
  obj X := ModuleCat.of R.{u} ((X → R.{u}) →ₗ[R.{u}] R.{u})
  map f := ModuleCat.ofHom
    { toFun := fun φ => φ.comp (finiteFunctionPullback f)
      map_add' := by
        intro φ ψ
        ext h
        rfl
      map_smul' := by
        intro c φ
        ext h
        rfl }
  map_id X := by
    apply ModuleCat.hom_ext
    ext φ h
    rfl
  map_comp f g := by
    apply ModuleCat.hom_ext
    ext φ h
    rfl

/-- Small-universe finite free modules, with morphisms given by pushforward of generators. -/
noncomputable def finiteSmallFreeModule :
    FintypeCat.{u} ⥤ ModuleCat.{u + 1} R.{u} where
  obj X := ModuleCat.of R.{u} (X →₀ R.{u})
  map f := ModuleCat.ofHom (Finsupp.lmapDomain R.{u} R.{u} (fun x => f x))
  map_id X := by
    apply ModuleCat.hom_ext
    ext a x
    simp [Finsupp.lmapDomain_apply]
  map_comp f g := by
    apply ModuleCat.hom_ext
    ext a z
    simp [Finsupp.lmapDomain_apply]

/-- Explicit formula for the inverse finite dual/free equivalence. -/
lemma finiteFunctionDualFreeEquiv_symm_apply
    (X : FintypeCat.{u}) (a : X →₀ R.{u}) (h : X → R.{u}) :
    ((CMDG.CondensedCM4P2E.finiteFunctionDualFreeEquiv.{u, u} X).symm a) h =
      ∑ x, h x * a x := by
  rfl

/-- The inverse finite duality map is natural on free generators. -/
noncomputable def finiteSmallFreeDualNatIso :
    finiteSmallFreeModule ≅ finiteFunctionDualModule :=
  NatIso.ofComponents
    (fun X =>
      (CMDG.CondensedCM4P2E.finiteFunctionDualFreeEquiv.{u, u} X).symm.toModuleIso)
    (by
      intro X Y f
      apply ModuleCat.hom_ext
      apply Finsupp.lhom_ext
      intro x r
      apply LinearMap.ext
      intro h
      change
        ((CMDG.CondensedCM4P2E.finiteFunctionDualFreeEquiv.{u, u} Y).symm
          (Finsupp.lmapDomain R.{u} R.{u} (fun x => f x) (Finsupp.single x r))) h =
        ((CMDG.CondensedCM4P2E.finiteFunctionDualFreeEquiv.{u, u} X).symm
          (Finsupp.single x r)) (fun y => h (f y))
      simp [finiteFunctionDualFreeEquiv_symm_apply, Finsupp.lmapDomain_apply])

/-- Canonical natural algebraic dual/free comparison on finite sets. -/
noncomputable def finiteFunctionDualFreeNatIso :
    finiteFunctionDualModule ≅ finiteSmallFreeModule :=
  finiteSmallFreeDualNatIso.symm

#check finiteFunctionPullback
#check finiteFunctionDualModule
#check finiteSmallFreeModule
#check finiteFunctionDualFreeEquiv_symm_apply
#check finiteSmallFreeDualNatIso
#check finiteFunctionDualFreeNatIso

#print axioms finiteFunctionPullback
#print axioms finiteFunctionDualModule
#print axioms finiteSmallFreeModule
#print axioms finiteFunctionDualFreeEquiv_symm_apply
#print axioms finiteSmallFreeDualNatIso
#print axioms finiteFunctionDualFreeNatIso

end CMDG.CondensedCM4P2E.Algebraic
