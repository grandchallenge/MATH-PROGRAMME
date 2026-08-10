import CMDGCondensedCM4P2E

/-!
# CMDG CM4-P2-E finite algebraic naturality

This auxiliary fixture isolates the remaining algebraic naturality layer from the certified
P2-E comparison fixture. It proves no sheaf-level internal-Hom comparison.
-/

namespace CMDG.CondensedCM4P2E.Algebraic

universe u

open CategoryTheory

attribute [local instance] FintypeCat.fintype

abbrev R := CMDG.CondensedCM4P2E.R.{u}

/-- Pullback of finite functions along a map of finite sets. -/
noncomputable def finiteFunctionPullback {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    (Y → R) →ₗ[R] (X → R) where
  toFun h := fun x => h (f x)
  map_add' h k := by
    funext x
    rfl
  map_smul' c h := by
    funext x
    rfl

/-- The algebraic dual of finite function modules with its canonical covariant functoriality. -/
noncomputable def finiteFunctionDualModule :
    FintypeCat.{u} ⥤ ModuleCat.{u + 1} R where
  obj X := ModuleCat.of R ((X → R) →ₗ[R] R)
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
    FintypeCat.{u} ⥤ ModuleCat.{u + 1} R where
  obj X := ModuleCat.of R (X →₀ R)
  map f := ModuleCat.ofHom (Finsupp.lmapDomain R R f)
  map_id X := by
    apply ModuleCat.hom_ext
    ext a x
    simp [Finsupp.lmapDomain_apply]
  map_comp f g := by
    apply ModuleCat.hom_ext
    ext a z
    simp [Finsupp.lmapDomain_apply]

/-- The inverse finite duality map is natural on free generators. -/
noncomputable def finiteSmallFreeDualNatIso :
    finiteSmallFreeModule ≅ finiteFunctionDualModule :=
  NatIso.ofComponents
    (fun X => (CMDG.CondensedCM4P2E.finiteFunctionDualFreeEquiv X).symm.toModuleIso)
    (by
      intro X Y f
      apply ModuleCat.hom_ext
      apply Finsupp.lhom_ext
      intro x r
      apply LinearMap.ext
      intro h
      simp [finiteSmallFreeModule, finiteFunctionDualModule, finiteFunctionPullback,
        CMDG.CondensedCM4P2E.finiteFunctionDualFreeEquiv,
        CMDG.CondensedCM4P2E.finiteFunctionDualEquiv])

/-- Canonical natural algebraic dual/free comparison on finite sets. -/
noncomputable def finiteFunctionDualFreeNatIso :
    finiteFunctionDualModule ≅ finiteSmallFreeModule :=
  finiteSmallFreeDualNatIso.symm

#check finiteFunctionPullback
#check finiteFunctionDualModule
#check finiteSmallFreeModule
#check finiteSmallFreeDualNatIso
#check finiteFunctionDualFreeNatIso

#print axioms finiteFunctionPullback
#print axioms finiteFunctionDualModule
#print axioms finiteSmallFreeModule
#print axioms finiteSmallFreeDualNatIso
#print axioms finiteFunctionDualFreeNatIso

end CMDG.CondensedCM4P2E.Algebraic
