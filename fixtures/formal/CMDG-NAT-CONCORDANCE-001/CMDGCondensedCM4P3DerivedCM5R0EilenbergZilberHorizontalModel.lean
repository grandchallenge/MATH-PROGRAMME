import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberTotalHomotopy

/-! Contract the horizontal direction of a free bisimplicial representable,
in the category of vertical simplicial sets, then linearize. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberModels
open CMDG.CondensedCM5R0.EilenbergZilberNatural
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
namespace CMDG.CondensedCM5R0.EilenbergZilberHorizontalModel

abbrev SS := SimplicialObject Type

def rowSet (a b : ℕ) : SimplicialObject SS :=
  Functor.curry.obj (coyoneda.obj (op (pair a b)))

def simplex (b : ℕ) : SS := coyoneda.obj (op (d b))

def forgetFirst (a b : ℕ) (p : Δ) : (rowSet a b).obj p ⟶ simplex b where
  app q := ↾fun x => x.2
  naturality := by intros; rfl

def rowAug (a b : ℕ) : SimplicialObject.Augmented SS where
  left := rowSet a b
  right := simplex b
  hom := {
    app := forgetFirst a b
    naturality := by
      intro p p' f
      apply NatTrans.ext
      funext q
      apply ConcreteCategory.hom_ext
      intro x
      change x.2 ≫ 𝟙 q = x.2
      simp }

def initialFirst (a b : ℕ) : simplex b ⟶ (rowSet a b).obj (d 0) where
  app q := ↾fun x => ((SimplexCategory.const (SimplexCategory.mk 0) (SimplexCategory.mk a) 0).op,x)
  naturality := by intros; rfl

def prependFirst (a b n : ℕ) : (rowSet a b).obj (d n) ⟶ (rowSet a b).obj (d (n+1)) where
  app q := ↾fun x => ((shift x.1.unop).op,x.2)
  naturality := by intros; rfl

def rowExtra (a b : ℕ) : SimplicialObject.Augmented.ExtraDegeneracy (rowAug a b) where
  s' := initialFirst a b
  s := prependFirst a b
  s'_comp_ε := by rfl
  s₀_comp_δ₁ := by
    apply NatTrans.ext
    funext q
    apply ConcreteCategory.hom_ext
    intro x
    apply Prod.ext
    · apply congrArg Quiver.Hom.op
      apply SimplexCategory.Hom.ext
      apply OrderHom.ext
      funext i
      fin_cases i
      rfl
    · change x.2 ≫ 𝟙 q = x.2; simp
  s_comp_δ₀ n := by
    apply NatTrans.ext
    funext q
    apply ConcreteCategory.hom_ext
    intro x
    apply Prod.ext
    · apply congrArg Quiver.Hom.op
      apply SimplexCategory.Hom.ext
      apply OrderHom.ext
      funext i
      rfl
    · change x.2 ≫ 𝟙 q = x.2; simp
  s_comp_δ n i := by
    apply NatTrans.ext
    funext q
    apply ConcreteCategory.hom_ext
    intro x
    apply Prod.ext
    · exact congrArg Quiver.Hom.op (shift_face x.1.unop i)
    · rfl
  s_comp_σ n i := by
    apply NatTrans.ext
    funext q
    apply ConcreteCategory.hom_ext
    intro x
    apply Prod.ext
    · exact congrArg Quiver.Hom.op (shift_degeneracy x.1.unop i)
    · rfl

def chainsF : SS ⥤ Ch :=
  (SimplicialObject.whiskering Type ZMod).obj freeZ ⋙ alternatingFaceMapComplex ZMod

def verticalModel (b : ℕ) : Ch := chainsF.obj (simplex b)

def horizontalModelEquiv (a b : ℕ) :
    HomotopyEquiv (double (model a b)) ((ChainComplex.single₀ Ch).obj (verticalModel b)) :=
  ((rowExtra a b).map chainsF).homotopyEquiv

#print axioms rowExtra
#print axioms horizontalModelEquiv
end CMDG.CondensedCM5R0.EilenbergZilberHorizontalModel
