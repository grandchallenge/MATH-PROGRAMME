import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealTransfer

/-! Relative indexing by the actual sections of a probe. This is
the presheaf construction underlying tensoring with its free
condensed module; it preserves exactness and epimorphisms. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection

abbrev Mod := ModuleCat.{u+1} Coeff.{u}
abbrev Psh := CompHaus.{u}ᵒᵖ ⥤ Mod.{u}

def indexedSum (P : SetPsh.{u}) (A : Psh.{u}) : Psh.{u} where
  obj T := ∐ (fun _ : P.obj T => A.obj T)
  map f := Limits.Sigma.map' (P.map f) (fun _ => A.map f)
  map_id T := by
    apply Sigma.hom_ext
    intro j
    rw [Sigma.ι_comp_map',Category.comp_id,P.map_id,A.map_id,Category.id_comp]
    rfl
  map_comp f g := by
    apply Sigma.hom_ext
    intro j
    rw [Sigma.ι_comp_map',Sigma.ι_comp_map'_assoc,Sigma.ι_comp_map',P.map_comp,A.map_comp,Category.assoc]
    rfl

def indexedMap (P : SetPsh.{u}) {A B : Psh.{u}} (f : A ⟶ B) :
    indexedSum P A ⟶ indexedSum P B where
  app T := Limits.Sigma.map (fun _ : P.obj T => f.app T)
  naturality := by
    intro T U g
    apply Sigma.hom_ext
    intro j
    change Sigma.ι (fun _ : P.obj T => A.obj T) j ≫
      Limits.Sigma.map' (P.map g) (fun _ => A.map g) ≫
      Limits.Sigma.map (fun _ : P.obj U => f.app U) =
      Sigma.ι (fun _ : P.obj T => A.obj T) j ≫
      Limits.Sigma.map (fun _ : P.obj T => f.app T) ≫
      Limits.Sigma.map' (P.map g) (fun _ => B.map g)
    rw [Sigma.ι_comp_map'_assoc,Sigma.ι_map_assoc,Sigma.ι_map,Sigma.ι_comp_map',
      ← Category.assoc,← Category.assoc,f.naturality]

def indexedFunctor (P : SetPsh.{u}) : Psh.{u} ⥤ Psh.{u} where
  obj := indexedSum P
  map := indexedMap P
  map_id A := by
    apply NatTrans.ext
    funext T
    exact Sigma.map_id (f:=fun _ : P.obj T => A.obj T)
  map_comp f g := by
    apply NatTrans.ext
    funext T
    exact (Sigma.map_comp_map (fun _ : P.obj T => f.app T) (fun _ : P.obj T => g.app T)).symm

instance (P : SetPsh.{u}) : (indexedFunctor P).PreservesZeroMorphisms where
  map_zero A B := by
    apply NatTrans.ext
    funext T
    apply Sigma.hom_ext
    intro j
    change Sigma.ι _ j ≫ Limits.Sigma.map (fun _ : P.obj T => (0 : A.obj T ⟶ B.obj T)) = _
    change _ = Sigma.ι (fun _ : P.obj T => A.obj T) j ≫ (0 : _ ⟶ ∐ (fun _ : P.obj T => B.obj T))
    rw [Sigma.ι_map,zero_comp,comp_zero]

theorem indexedFunctor_exact (P : SetPsh.{u}) (Q : ShortComplex Psh.{u})
    (h : Q.Exact) : (Q.map (indexedFunctor P)).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro T
  let F (X : Mod.{u}) : Discrete (P.obj T) ⥤ Mod.{u} :=
    Discrete.functor (fun _ : P.obj T => X)
  let f : F (Q.X₁.obj T) ⟶ F (Q.X₂.obj T) :=
    Discrete.natTrans (fun _ => Q.f.app T)
  let g : F (Q.X₂.obj T) ⟶ F (Q.X₃.obj T) :=
    Discrete.natTrans (fun _ => Q.g.app T)
  have hz : f ≫ g = 0 := by
    apply NatTrans.ext
    funext j
    change Q.f.app T ≫ Q.g.app T = 0
    exact NatTrans.congr_app Q.zero T
  let D := ShortComplex.mk f g hz
  have hd : D.Exact := by
    apply functorShortComplex_exact_of_pointwise
    intro j
    exact h.map ((evaluation CompHausᵒᵖ Mod.{u}).obj T)
  have hh := hd.map (colim : (Discrete (P.obj T) ⥤ Mod.{u}) ⥤ Mod.{u})
  exact hh

theorem indexedFunctor_epi (P : SetPsh.{u}) {A B : Psh.{u}} (f : A ⟶ B)
    [Epi f] : Epi ((indexedFunctor P).map f) := by
  apply (NatTrans.epi_iff_epi_app _).2
  intro T
  change Epi (Limits.Sigma.map (fun _ : P.obj T => f.app T))
  letI : Epi (f.app T) := (NatTrans.epi_iff_epi_app f).1 inferInstance T
  infer_instance

#print axioms indexedFunctor_exact
#print axioms indexedFunctor_epi
end CMDG.CondensedCM5R0.BreenDeligneProbe
