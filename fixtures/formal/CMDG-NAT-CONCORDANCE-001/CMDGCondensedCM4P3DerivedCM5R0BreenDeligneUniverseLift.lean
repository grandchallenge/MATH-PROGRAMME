import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCoherentResolution
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneLatticeComplex

/-! Explicit scalar/universe transport, including the actual lifted
finite free lattice skeleton. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneProbe
namespace CMDG.CondensedCM5R0.BreenDeligneUniverseLift
abbrev ZMod := BreenDeligneTensorSupport.ZMod
abbrev Small := BreenDeligneLatticeProjectives.Latt
abbrev Big := UniversalExtension.Latt.{u}
abbrev LC := BreenDeligneLatticeFP.LC
abbrev BC := Big.{u} ⥤ Mod.{u}

def bigLinear {M N : Mod.{u}} (f : M →+ N) : M ⟶ N :=
  ConcreteCategory.ofHom (C:=Mod.{u}) (X:=M) (Y:=N) {
    toFun := f
    map_add' := map_add f
    map_smul' := by
      intro r x
      obtain ⟨r⟩ := r
      letI : Module Coeff.{u} M := M.isModule
      letI : Module Coeff.{u} N := N.isModule
      rw [RingHom.id_apply, show (ULift.up r : Coeff.{u}) = (r : Coeff.{u}) from rfl]
      simp only [Int.cast_smul_eq_zsmul, map_zsmul] }

def bigIso {M N : Mod.{u}} (e : M ≃+ N) : M ≅ N where
  hom := bigLinear e.toAddMonoidHom
  inv := bigLinear e.symm.toAddMonoidHom
  hom_inv_id := by
    apply ConcreteCategory.hom_ext
    exact e.left_inv
  inv_hom_id := by
    apply ConcreteCategory.hom_ext
    exact e.right_inv

def liftObj (M : ZMod) : Mod.{u} :=
  @ModuleCat.of Coeff.{u} _ (ULift.{u+1} M) inferInstance
    (Module.compHom (ULift.{u+1} M) (ULift.ringEquiv : Coeff.{u} ≃+* ℤ).toRingHom)

def liftAdd (M : ZMod) : M ≃+ liftObj.{u} M where
  toFun := ULift.up
  invFun := ULift.down
  left_inv _ := rfl
  right_inv _ := rfl
  map_add' _ _ := rfl

def lift : ZMod ⥤ Mod.{u} where
  obj := liftObj
  map {M N} f := bigLinear ((liftAdd N).toAddMonoidHom.comp
    (f.hom.toAddMonoidHom.comp (liftAdd M).symm.toAddMonoidHom))
  map_id _ := by apply ConcreteCategory.hom_ext; intro x; rfl
  map_comp _ _ := by apply ConcreteCategory.hom_ext; intro x; rfl

instance : lift.{u}.Additive where
  map_add := by intros; apply ConcreteCategory.hom_ext; intro x; rfl

theorem lift_apply {M N : ZMod} (f : M ⟶ N) (x : M) :
    lift.{u}.map f (liftAdd M x) = liftAdd N (f x) := rfl

theorem lift_exact (S : ShortComplex ZMod) (h : S.Exact) :
    (S.map lift.{u}).Exact := by
  apply (ShortComplex.moduleCat_exact_iff _).mpr
  intro x hx
  obtain ⟨y,hy⟩ := (liftAdd S.X₂).surjective x
  subst x
  change lift.map S.g (liftAdd S.X₂ y) = 0 at hx
  rw [lift_apply,← map_zero (liftAdd S.X₃)] at hx
  obtain ⟨z,hz⟩ := (ShortComplex.moduleCat_exact_iff _).mp h y
    ((liftAdd S.X₃).injective hx)
  exact ⟨liftAdd S.X₁ z, by change lift.map S.f (liftAdd S.X₁ z) = _; rw [lift_apply,hz]⟩

theorem lift_epi {M N : ZMod} (f : M ⟶ N) [Epi f] : Epi (lift.{u}.map f) := by
  apply (ModuleCat.epi_iff_surjective _).mpr
  intro x
  obtain ⟨y,hy⟩ := (liftAdd N).surjective x
  obtain ⟨z,hz⟩ := (ModuleCat.epi_iff_surjective f).mp inferInstance y
  exact ⟨liftAdd M z,by rw [lift_apply,hz,hy]⟩

def rankCoords (n : ℕ) :
    UniversalExtension.rank.{u} n ≃+ (Fin n → ℤ) :=
  (Finsupp.domCongr (Equiv.ulift : ULift.{u+1} (Fin n) ≃ Fin n)).trans
    ((Finsupp.linearEquivFunOnFinite Coeff.{u} Coeff.{u} (Fin n)).toAddEquiv.trans
      (AddEquiv.piCongrRight fun _ : Fin n => (ULift.ringEquiv : Coeff.{u} ≃+* ℤ).toAddEquiv))

def shrink : Big.{u} ⥤ Small where
  obj n := n
  map {r s} f := InducedCategory.homMk (AddCommGrpCat.ofHom
    ((rankCoords.{u} s).toAddMonoidHom.comp
      ((UniversalExtension.incl.map f).hom.toAddMonoidHom.comp (rankCoords.{u} r).symm.toAddMonoidHom)))
  map_id r := by
    apply (InducedCategory.homEquiv).injective
    apply AddCommGrpCat.hom_ext
    ext x
    exact (rankCoords.{u} r).apply_symm_apply x
  map_comp {r s t} f g := by
    apply (InducedCategory.homEquiv).injective
    apply AddCommGrpCat.hom_ext
    ext x
    change rankCoords.{u} t (UniversalExtension.incl.map g (UniversalExtension.incl.map f
      ((rankCoords.{u} r).symm x))) = rankCoords.{u} t (UniversalExtension.incl.map g
        ((rankCoords.{u} s).symm (rankCoords.{u} s (UniversalExtension.incl.map f ((rankCoords.{u} r).symm x)))))
    rw [AddEquiv.symm_apply_apply]

abbrev transport : LC ⥤ BC.{u} :=
  (Functor.whiskeringLeft Big.{u} Small ZMod).obj shrink ⋙
    (Functor.whiskeringRight Big.{u} ZMod Mod.{u}).obj lift

def identityIso : transport.{u}.obj BreenDeligneLatticeFP.V ≅ UniversalExtension.incl.{u} :=
  NatIso.ofComponents
    (fun r => bigIso ((liftAdd (BreenDeligneLatticeFP.V.obj (shrink.obj r))).symm.trans (rankCoords.{u} r).symm))
    (fun {r s} f => by
      apply ConcreteCategory.hom_ext
      intro x
      change (rankCoords.{u} s).symm (rankCoords.{u} s (UniversalExtension.incl.map f
        ((rankCoords.{u} r).symm ((liftAdd (BreenDeligneLatticeFP.V.obj (shrink.obj r))).symm x)))) = _
      rw [AddEquiv.symm_apply_apply]
      rfl)

theorem transport_exact (S : ShortComplex LC) (h : S.Exact) :
    (S.map transport.{u}).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro r
  exact lift_exact (S.map ((evaluation Small ZMod).obj (shrink.obj r)))
    (h.map ((evaluation Small ZMod).obj (shrink.obj r)))

theorem transport_epi {F G : LC} (f : F ⟶ G) [Epi f] :
    Epi (transport.{u}.map f) := by
  apply (NatTrans.epi_iff_epi_app _).mpr
  intro r
  letI := (NatTrans.epi_iff_epi_app f).mp inferInstance (shrink.obj r)
  exact lift_epi (f.app (shrink.obj r))

#print axioms identityIso
#print axioms transport_exact
end CMDG.CondensedCM5R0.BreenDeligneUniverseLift
