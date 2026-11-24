import Mathlib.Algebra.Category.Grp.Adjunctions
import Mathlib.Algebra.Category.Grp.Abelian
import Mathlib.Algebra.Category.Grp.EpiMono
import Mathlib.CategoryTheory.Adjunction.Whiskering
import Mathlib.CategoryTheory.InducedCategory
import Mathlib.CategoryTheory.Limits.FunctorCategory.EpiMono
import Mathlib.CategoryTheory.Preadditive.Projective.Basic
import Mathlib.CategoryTheory.Limits.Shapes.Products

/-! Free representables in the actual finite-free lattice functor category.
The existence of a finite-type resolution is a separate obligation. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite
namespace CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives

def lattice (n : ℕ) : AddCommGrpCat.{0} := AddCommGrpCat.of (Fin n → ℤ)
abbrev Latt := InducedCategory AddCommGrpCat.{0} lattice
abbrev valueFunctor : Latt ⥤ AddCommGrpCat.{0} := inducedFunctor lattice

def polynomial (n : Latt) : Latt ⥤ AddCommGrpCat.{0} :=
  coyoneda.obj (op n) ⋙ AddCommGrpCat.free

def polynomialHomEquiv (n : Latt) (F : Latt ⥤ AddCommGrpCat.{0}) :
    (polynomial n ⟶ F) ≃ F.obj n :=
  ((AddCommGrpCat.adj.whiskerRight Latt).homEquiv
    (coyoneda.obj (op n)) F).trans coyonedaEquiv

theorem polynomialHomEquiv_comp (n : Latt)
    {F G : Latt ⥤ AddCommGrpCat.{0}}
    (f : polynomial n ⟶ F) (g : F ⟶ G) :
    polynomialHomEquiv n G (f ≫ g) =
      g.app n (polynomialHomEquiv n F f) := by
  let adj := AddCommGrpCat.adj.whiskerRight Latt
  change coyonedaEquiv (adj.homEquiv (coyoneda.obj (op n)) G (f ≫ g)) =
    g.app n (coyonedaEquiv (adj.homEquiv (coyoneda.obj (op n)) F f))
  have h := adj.homEquiv_naturality_right (X := coyoneda.obj (op n)) f g
  exact (congrArg coyonedaEquiv h).trans (coyonedaEquiv_comp _ _)

instance polynomialProjective (n : Latt) : Projective (polynomial n) where
  factors f e he := by
    have hE : Epi (e.app n) := (NatTrans.epi_iff_epi_app e).mp he n
    obtain ⟨x, hx⟩ := (AddCommGrpCat.epi_iff_surjective (e.app n)).mp hE
      (polynomialHomEquiv n _ f)
    refine ⟨(polynomialHomEquiv n _).symm x, ?_⟩
    apply (polynomialHomEquiv n _).injective
    rw [polynomialHomEquiv_comp, Equiv.apply_symm_apply, hx]

abbrev CoverIndex (F : Latt ⥤ AddCommGrpCat.{0}) := Σ n : Latt, F.obj n
def coverFamily (F : Latt ⥤ AddCommGrpCat.{0}) (i : CoverIndex F) :
    Latt ⥤ AddCommGrpCat.{0} := polynomial i.1

def cover (F : Latt ⥤ AddCommGrpCat.{0}) : (∐ (coverFamily F)) ⟶ F :=
  Sigma.desc (fun i => (polynomialHomEquiv i.1 F).symm i.2)

theorem cover_epi (F : Latt ⥤ AddCommGrpCat.{0}) : Epi (cover F) := by
  apply (NatTrans.epi_iff_epi_app _).mpr
  intro n
  apply (AddCommGrpCat.epi_iff_surjective _).mpr
  intro x
  let i : CoverIndex F := ⟨n,x⟩
  let a : polynomial n ⟶ ∐ (coverFamily F) := Sigma.ι (coverFamily F) i
  refine ⟨polynomialHomEquiv n _ a, ?_⟩
  rw [← polynomialHomEquiv_comp]
  change polynomialHomEquiv n F (Sigma.ι (coverFamily F) i ≫ cover F) = x
  have h : Sigma.ι (coverFamily F) i ≫ cover F =
      (polynomialHomEquiv i.1 F).symm i.2 :=
    Sigma.ι_desc (f := coverFamily F)
      (fun j => (polynomialHomEquiv j.1 F).symm j.2) i
  exact (congrArg (polynomialHomEquiv n F) h).trans
    ((polynomialHomEquiv n F).apply_symm_apply x)

instance coverProjective (F : Latt ⥤ AddCommGrpCat.{0}) :
    Projective (∐ (coverFamily F)) := by
  letI (i : CoverIndex F) : Projective (coverFamily F i) := polynomialProjective i.1
  infer_instance

instance latticeFunctorEnoughProjectives :
    EnoughProjectives (Latt ⥤ AddCommGrpCat.{0}) where
  presentation F := by
    letI : Epi (cover F) := cover_epi F
    exact ⟨⟨∐ (coverFamily F), cover F⟩⟩

#print axioms polynomialHomEquiv
#print axioms polynomialProjective
#print axioms cover_epi
#print axioms latticeFunctorEnoughProjectives
end CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives
