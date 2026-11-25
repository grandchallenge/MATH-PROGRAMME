import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBarTotal
import Mathlib.CategoryTheory.Functor.Currying
import Mathlib.AlgebraicTopology.DoldKan.HomotopyEquivalence

/-! Alexander–Whitney and shuffle degree maps on the actual
alternating diagonal and total complexes of a bisimplicial integer module.
The chain identities are separate from the definition of these maps. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
namespace CMDG.CondensedCM5R0.EilenbergZilberMaps
abbrev Δ := SimplexCategoryᵒᵖ
abbrev Bi := Δ × Δ ⥤ ZMod
abbrev d (n : ℕ) : Δ := op (SimplexCategory.mk n)

def diagonal (B : Bi) : SimplicialObject ZMod := CategoryTheory.Functor.diag Δ ⋙ B
def diagChains (B : Bi) : Ch := (alternatingFaceMapComplex ZMod).obj (diagonal B)
def double (B : Bi) : HomologicalComplex₂ ZMod c c :=
  (alternatingFaceMapComplex Ch).obj
    (CategoryTheory.Functor.curry.obj B ⋙ alternatingFaceMapComplex ZMod)
def total (B : Bi) : Ch := (double B).total c

def front (p q : ℕ) : SimplexCategory.mk p ⟶ SimplexCategory.mk (p+q) :=
  SimplexCategory.subinterval 0 p (by omega)
def back (p q : ℕ) : SimplexCategory.mk q ⟶ SimplexCategory.mk (p+q) :=
  SimplexCategory.subinterval p q (by omega)

/-- Restrict the first direction to the initial interval and the second
to the terminal interval, with the cut vertex shared. -/
def awPart (B : Bi) (p q : ℕ) :
    (diagChains B).X (p+q) ⟶ ((double B).X p).X q :=
  B.map ((front p q).op ×ₘ (back p q).op)

def awTerm (B : Bi) (n : ℕ) (i : Fin (n+1)) :
    (diagChains B).X n ⟶ (total B).X n :=
  B.map ((SimplexCategory.subinterval 0 i.val (by omega : 0+i.val ≤ n)).op ×ₘ
         (SimplexCategory.subinterval i.val (n-i.val) (by omega : i.val+(n-i.val) ≤ n)).op) ≫
    (double B).ιTotal c i.val (n-i.val) n (by change i.val+(n-i.val)=n; omega)

def awDegree (B : Bi) (n : ℕ) : (diagChains B).X n ⟶ (total B).X n :=
  ∑ i : Fin (n+1), awTerm B n i

/-- A lattice path from (0,0) to (p,q), one unit step at a time.
Rank equals the vertex number; monotonicity supplies the step direction. -/
abbrev Path (p q : ℕ) :=
  {f : (Fin (p+q+1) →o Fin (p+1)) × (Fin (p+q+1) →o Fin (q+1)) //
    ∀ i, (f.1 i).val + (f.2 i).val = i.val}

instance (p q : ℕ) : Finite (Path p q) :=
  Finite.of_injective (fun u : Path p q => ((u.val.1 : Fin (p+q+1) → Fin (p+1)), (u.val.2 : Fin (p+q+1) → Fin (q+1)))) (by
    intro u v h
    apply Subtype.ext
    apply Prod.ext <;> apply DFunLike.coe_injective
    · exact congrArg Prod.fst h
    · exact congrArg Prod.snd h)
noncomputable instance (p q : ℕ) : Fintype (Path p q) := Fintype.ofFinite _

def pathSign {p q : ℕ} (u : Path p q) : ℤ :=
  (-1) ^ (∑ i : Fin (p+q),
    if u.val.1 i.castSucc < u.val.1 i.succ then (u.val.2 i.castSucc).val else 0)

def shufflePart (B : Bi) (p q : ℕ) :
    ((double B).X p).X q ⟶ (diagChains B).X (p+q) :=
  ∑ u : Path p q, pathSign u •
    B.map ((SimplexCategory.mkHom u.val.1).op ×ₘ
           (SimplexCategory.mkHom u.val.2).op)

def shuffleDegree (B : Bi) (n : ℕ) : (total B).X n ⟶ (diagChains B).X n :=
  (double B).toGradedObject.descMapObj (ComplexShape.π c c c)
    (fun i h => shufflePart B i.1 i.2 ≫
      eqToHom (by change i.1+i.2 = n at h; rw [h]))

set_option backward.isDefEq.respectTransparency false in
theorem shuffleDegree_summand (B : Bi) (p q : ℕ) :
    (double B).ιTotal c p q (p+q) rfl ≫ shuffleDegree B (p+q) =
      shufflePart B p q := by
  unfold shuffleDegree HomologicalComplex₂.ιTotal
  rw [GradedObject.ι_descMapObj]
  simp

#print axioms awDegree
#print axioms shuffleDegree
#print axioms shuffleDegree_summand
end CMDG.CondensedCM5R0.EilenbergZilberMaps
