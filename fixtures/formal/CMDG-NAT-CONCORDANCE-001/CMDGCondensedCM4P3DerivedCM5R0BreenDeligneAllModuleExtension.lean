import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteModuleDescent

/-! Any polynomial element on an arbitrary module descends to a
finitely generated submodule, and the inclusion detects equality.
This completes the extension from lattice exactness to UniversalBD. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
open BreenDeligneProbe
variable {A B : Mod.{u}} {k : ℕ} (a : Fin k → ℕ)

theorem tuple_injective (f : A ⟶ B) (hf : Function.Injective f) :
    Function.Injective ((tupleSet a).map f) := by
  rintro ⟨j,x⟩ ⟨l,y⟩ h
  have he := congrArg (fun t : (tupleSet a).obj B => t.1) h
  change j=l at he
  subst l
  apply Sigma.ext
  · rfl
  · apply heq_of_eq
    funext i
    apply hf
    change (⟨j,fun i => f (x i)⟩ : (tupleSet a).obj B) =
      ⟨j,fun i => f (y i)⟩ at h
    exact congrFun (Sigma.mk.inj h).2.eq i

theorem polynomial_injective (f : A ⟶ B) (hf : Function.Injective f) :
    Function.Injective ((polynomial a).map f) :=
  Finsupp.mapDomain_injective (tuple_injective a f hf)

def subObj (V : Submodule Coeff.{u} A) : Mod.{u} :=
  @ModuleCat.of Coeff.{u} _ V V.addCommGroup V.module

def subIncl (V : Submodule Coeff.{u} A) : subObj V ⟶ A :=
  @ModuleCat.ofHom Coeff.{u} _ V A V.addCommGroup V.module A.isAddCommGroup A.isModule V.subtype

theorem finiteSubmodule_support (x : (polynomial a).obj A) :
    ∃ V : Submodule Coeff.{u} A, V.FG ∧
      ∃ y : (polynomial a).obj (subObj V),
        (polynomial a).map (subIncl V) y = x := by
  classical
  let z : (tupleSet a).obj A →₀ Coeff.{u} := x
  let S : Finset A := z.support.biUnion fun t =>
    Finset.univ.image t.2
  let V : Submodule Coeff.{u} A := Submodule.span Coeff.{u} (S : Set A)
  refine ⟨V,Submodule.fg_span S.finite_toSet,?_⟩
  let f : (tupleSet a).obj (subObj V) → (tupleSet a).obj A :=
    (tupleSet a).map (subIncl V)
  have hs : ∀ t ∈ z.support, t ∈ Set.range f := by
    intro t ht
    refine ⟨⟨t.1,fun i => ⟨t.2 i,Submodule.subset_span ?_⟩⟩,?_⟩
    · exact Finset.mem_biUnion.mpr ⟨t,ht,Finset.mem_image.mpr ⟨i,Finset.mem_univ _,rfl⟩⟩
    · rfl
  have hz : z ∈ Finsupp.supported Coeff.{u} Coeff.{u} (Set.range f) :=
    (Finsupp.mem_supported _ _).mpr hs
  have hr := Finsupp.lmapDomain_supported Coeff.{u} Coeff.{u} f Set.univ
  rw [Finsupp.supported_univ,Submodule.map_top,Set.image_univ] at hr
  rw [← hr] at hz
  obtain ⟨y,hy⟩ := hz
  exact ⟨y,hy⟩

namespace PolynomialComplex
variable (C : PolynomialComplex.{u})

theorem row_injective (n : ℕ) (f : A ⟶ B) (hf : Function.Injective f) :
    Function.Injective ((C.row n).map f) := by
  cases n with
  | zero => exact hf
  | succ n => exact polynomial_injective (C.arity n) f hf

theorem exact_all (h : ∀ n : ℕ, C.ExactAt (rank.{u} n))
    (A : Mod.{u}) : C.ExactAt A := by
  refine ⟨C.aug_surj_all (h 1).1 A,?_⟩
  intro n
  apply (ShortComplex.moduleCat_exact_iff _).2
  intro x hx
  obtain ⟨V,hV,y,hy⟩ := finiteSubmodule_support (C.arity n) x
  let M := subObj V
  letI : Module.Finite Coeff.{u} M := Module.Finite.iff_fg.mpr hV
  let f := subIncl V
  have hfin := C.exact_finite h M
  have hzero : (C.vertical n).app M y = 0 := by
    apply C.row_injective n f Subtype.coe_injective
    rw [map_zero]
    have hh := CategoryTheory.congr_fun ((C.vertical n).naturality f) y
    change (C.vertical n).app A ((C.row (n+1)).map f y) =
      (C.row n).map f ((C.vertical n).app M y) at hh
    rw [← hh]
    change (C.vertical n).app A ((polynomial (C.arity n)).map f y) = 0
    rw [show (polynomial (C.arity n)).map f y = x from hy]
    exact hx
  obtain ⟨z,hz⟩ := (ShortComplex.moduleCat_exact_iff _).1 (hfin.2 n) y hzero
  refine ⟨(C.row (n+2)).map f z,?_⟩
  have hh := CategoryTheory.congr_fun ((C.vertical (n+1)).naturality f) z
  change (C.vertical (n+1)).app A ((C.row (n+2)).map f z) =
    (C.row (n+1)).map f ((C.vertical (n+1)).app M z) at hh
  change (C.vertical (n+1)).app A ((C.row (n+2)).map f z) = x
  rw [hh,show (C.vertical (n+1)).app M z = y from hz]
  exact hy

end PolynomialComplex

def LatticeBD.toUniversalBD (B : LatticeBD.{u}) : UniversalBD.{u} where
  count := B.count
  arity := B.arity
  aug := B.extended.aug
  d := B.extended.d
  aug_zero := B.extended.aug_zero
  sq_zero := B.extended.sq_zero
  aug_epi := by
    apply (NatTrans.epi_iff_epi_app _).2
    intro A
    exact (ModuleCat.epi_iff_surjective _).2
      (B.extended.exact_all B.extended_exact A).1
  aug_exact := by
    apply functorShortComplex_exact_of_pointwise
    intro A
    exact (B.extended.exact_all B.extended_exact A).2 0
  exact n := by
    apply functorShortComplex_exact_of_pointwise
    intro A
    exact (B.extended.exact_all B.extended_exact A).2 (n+1)

#print axioms PolynomialComplex.exact_all
#print axioms LatticeBD.toUniversalBD
end CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
