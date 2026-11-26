import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneAdditiveNextMap
import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberNatural

/-! Free interval cylinder of a simplicial integer module. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
namespace CMDG.CondensedCM5R0.BreenDeligneInterval

abbrev I (a : Δ) := a.unop ⟶ SimplexCategory.mk 1
def vertex (a : Δ) (v : Fin 2) : I a :=
  SimplexCategory.const a.unop (SimplexCategory.mk 1) v

def cylinderBi (X : SimplicialObject ZMod) : Bi where
  obj a := ∐ fun _ : I a.1 => X.obj a.2
  map {a b} f := Sigma.desc (fun t : I a.1 =>
    X.map f.2 ≫ Sigma.ι (fun _ : I b.1 => X.obj b.2) (f.1.unop ≫ t))
  map_id a := by
    apply Sigma.hom_ext
    intro t
    rw [Sigma.ι_desc]
    change X.map (𝟙 a.2) ≫ Sigma.ι (fun _ : I a.1 => X.obj a.2) ((𝟙 a.1).unop ≫ t) = _
    simp
  map_comp {a b e} f g := by
    apply Sigma.hom_ext
    intro t
    rw [Sigma.ι_desc,← Category.assoc,Sigma.ι_desc,Category.assoc,Sigma.ι_desc]
    change X.map (f.2 ≫ g.2) ≫ Sigma.ι (fun _ : I e.1 => X.obj e.2) ((f.1 ≫ g.1).unop ≫ t) =
      X.map f.2 ≫ X.map g.2 ≫ Sigma.ι (fun _ : I e.1 => X.obj e.2) (g.1.unop ≫ f.1.unop ≫ t)
    rw [Functor.map_comp,Category.assoc,unop_comp,Category.assoc]

abbrev cyl (X : SimplicialObject ZMod) := diagonal (cylinderBi X)

def inj (X : SimplicialObject ZMod) (a b : Δ) (t : I a) :
    X.obj b ⟶ (cylinderBi X).obj (a,b) :=
  Sigma.ι (fun _ : I a => X.obj b) t

@[reassoc]
theorem inj_map (X : SimplicialObject ZMod) {a b a' b' : Δ} (f : a ⟶ a') (g : b ⟶ b')
    (t : I a) :
    inj X a b t ≫ (cylinderBi X).map (f ×ₘ g) =
      X.map g ≫ inj X a' b' (f.unop ≫ t) :=
  by exact Sigma.ι_desc _ _

theorem vertex_comp {a b : Δ} (f : a ⟶ b) (v : Fin 2) :
    f.unop ≫ vertex a v = vertex b v := by
  apply SimplexCategory.Hom.ext
  apply OrderHom.ext
  funext j
  rfl

def endpoint (X : SimplicialObject ZMod) (v : Fin 2) : X ⟶ cyl X where
  app a := inj X a a (vertex a v)
  naturality {a b} f := by
    change X.map f ≫ inj X b b (vertex b v) =
      inj X a a (vertex a v) ≫ (cylinderBi X).map (f ×ₘ f)
    rw [inj_map,vertex_comp]

def lastValue {p : ℕ} (t : I (d p)) : Fin 2 := t.toOrderHom (Fin.last p)
def firstValue {p : ℕ} (t : I (d p)) : Fin 2 := t.toOrderHom 0

theorem one_const_or_id (t : I (d 1)) : t = vertex (d 1) 0 ∨
    t = vertex (d 1) 1 ∨ t = 𝟙 (SimplexCategory.mk 1) := by
  have h := t.toOrderHom.monotone (show (0 : Fin 2) ≤ 1 by decide)
  rcases Fin.eq_zero_or_eq_succ (t.toOrderHom 0) with h₀ | ⟨i,hi⟩
  · rcases Fin.eq_zero_or_eq_succ (t.toOrderHom 1) with h₁ | ⟨i,hi⟩
    · left
      apply SimplexCategory.Hom.ext
      apply OrderHom.ext
      funext j
      fin_cases j <;> assumption
    · have hi' : i=0 := Subsingleton.elim _ _
      subst i
      right; right
      apply SimplexCategory.Hom.ext
      apply OrderHom.ext
      funext j
      fin_cases j <;> assumption
  · have hi' : i=0 := Subsingleton.elim _ _
    subst i
    have h₁ : t.toOrderHom 1=1 := by
      rw [hi] at h
      exact le_antisymm (Fin.le_last _) h
    right; left
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    fin_cases j <;> assumption

#print axioms cylinderBi
#print axioms endpoint
#print axioms one_const_or_id
end CMDG.CondensedCM5R0.BreenDeligneInterval
