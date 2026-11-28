import CMDGCondensedCM4P3DerivedCM5R0StoneanProjective
import CMDGCondensedCM4P3DerivedCM5R0ProbeRealProductColimit

/-! Actual projective generators, with the universe of the indexing
coproduct made explicit. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u v w
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

section
variable {C : Type u} [Category.{v} C] {J : Type w}
variable (P : J → C) [HasCoproduct P]

theorem projective_coproduct (h : ∀ j, Projective (P j)) :
    Projective (∐ P) where
  factors := by
    intro E X f e he
    letI : Epi e := he
    choose g hg using fun j => (h j).factors (Sigma.ι P j ≫ f) e
    refine ⟨Sigma.desc g, ?_⟩
    apply Sigma.hom_ext
    intro j
    rw [← Category.assoc, Sigma.ι_desc, hg]
end

abbrev generatorIndex (X : Ambient.{u}) :=
  Σ S : Stonean.{u}, ((Condensed.profiniteFree Coeff).obj
    (Stonean.toProfinite.obj S) ⟶ X)

abbrev generatorFamily (X : Ambient.{u}) (j : generatorIndex X) : Ambient.{u} :=
  (Condensed.profiniteFree Coeff).obj (Stonean.toProfinite.obj j.1)

def generatorCover (X : Ambient.{u}) : (∐ generatorFamily X) ⟶ X :=
  Sigma.desc fun j => j.2

theorem generatorCover_epi (X : Ambient.{u}) : Epi (generatorCover X) := by
  rw [CondensedMod.epi_iff_surjective_on_stonean]
  intro S x
  let e := freeProfiniteSectionsEquiv (Stonean.toProfinite.obj S) X
  let f := e.symm x
  let j : generatorIndex X := ⟨S,f⟩
  let g : (Condensed.profiniteFree Coeff).obj (Stonean.toProfinite.obj S) ⟶
      ∐ generatorFamily X := Sigma.ι (generatorFamily X) j
  refine ⟨freeProfiniteSectionsEquiv (Stonean.toProfinite.obj S) _ g, ?_⟩
  have he : g ≫ generatorCover X = f := Sigma.ι_desc _ _
  have hh := freeProfiniteSectionsEquiv_naturality_target (Stonean.toProfinite.obj S)
    g (generatorCover X)
  rw [he] at hh
  exact hh.symm.trans (e.apply_symm_apply x)

theorem ambientEnoughProjectives : EnoughProjectives Ambient.{u} where
  presentation X := by
    letI := projective_coproduct (generatorFamily X) (fun j => freeStonean_projective j.1)
    letI := generatorCover_epi X
    exact ⟨⟨∐ generatorFamily X,generatorCover X⟩⟩

#print axioms projective_coproduct
#print axioms ambientEnoughProjectives
end CMDG.CondensedCM5R0
