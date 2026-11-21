import Mathlib.GroupTheory.FreeAbelianGroup

/-!
# CMDG CM5: actual finite-free Breen–Deligne first three terms and doubling homotopy

Reconstruct the source's low-degree polynomial free-group resolution,
functorial for every abelian group A, with F0 = Z[A], F1 = Z[A²],
F2 = Z[A³] ⊕ Z[A²]. These are **genuine** free abelian groups with
explicit finite universal formulas, not merely an untyped schematic complex.

The augmenting d1 has vanishing composite, d1 d2 = 0, augmentation
is surjective, and h0/h1 provide an explicit (2 id - [2]) homotopy
through homological degree one, including full-object not just basis
identities. Differential and homotopy operations are natural under
all abelian-group homomorphisms.

This does not prove exactness at F1 or continuation in degree 3+, nor
construct the associated condensed free modules / derived real-circle
comparison. Those require subsequent categorical and stable-homotopy
work. The displayed ingredients are the low-degree part of Scholze
Theorem 4.5 and Proposition 4.17, May 2026 notes pp. 25, 30–32.
-/
import Mathlib.Tactic.Abel

noncomputable section
universe u
namespace CMDG.CondensedCM5R0.BreenDeligne

variable (A : Type u) [AddCommGroup A]

abbrev F0 := FreeAbelianGroup A
abbrev F1 := FreeAbelianGroup (A × A)
abbrev F2 := FreeAbelianGroup (Sum (A × (A × A)) (A × A))

def d1 : F1 A →+ F0 A :=
  FreeAbelianGroup.lift fun p =>
    FreeAbelianGroup.of (p.1 + p.2) -
    FreeAbelianGroup.of p.1 - FreeAbelianGroup.of p.2

def d2 : F2 A →+ F1 A :=
  FreeAbelianGroup.lift fun s =>
    match s with
    | .inl p =>
        FreeAbelianGroup.of (p.2.1, p.2.2) -
        FreeAbelianGroup.of (p.1 + p.2.1, p.2.2) +
        FreeAbelianGroup.of (p.1, p.2.1 + p.2.2) -
        FreeAbelianGroup.of (p.1, p.2.1)
    | .inr p =>
        FreeAbelianGroup.of p - FreeAbelianGroup.of (p.2, p.1)

def h0 : F0 A →+ F1 A :=
  FreeAbelianGroup.lift fun a => -FreeAbelianGroup.of (a, a)

def h1 : F1 A →+ F2 A :=
  FreeAbelianGroup.lift fun p =>
    FreeAbelianGroup.of (Sum.inl (p.1,(p.1,p.2+p.2))) -
    FreeAbelianGroup.of (Sum.inl (p.1,(p.2,p.2))) -
    FreeAbelianGroup.of (Sum.inl (p.1,(p.2,p.1+p.2))) -
    FreeAbelianGroup.of (Sum.inr (p.1+p.2,p.2))

def double0 : F0 A →+ F0 A :=
  FreeAbelianGroup.map fun a : A => a + a

def double1 : F1 A →+ F1 A :=
  FreeAbelianGroup.map fun p : A × A => (p.1+p.1,p.2+p.2)

theorem d1d2_zero : (d1 A).comp (d2 A) = 0 := by
  apply FreeAbelianGroup.lift_ext
  intro x
  cases x with
  | inl p =>
    rcases p with ⟨a, ⟨b,c⟩⟩
    simp [d1,d2,add_assoc]
    abel
  | inr p =>
    rcases p with ⟨a,b⟩
    simp [d1,d2]
    abel

theorem homotopy0 (a : A) :
    d1 A (h0 A (FreeAbelianGroup.of a)) =
      FreeAbelianGroup.of a + FreeAbelianGroup.of a -
      double0 A (FreeAbelianGroup.of a) := by
  simp [d1,h0,double0]
  abel

theorem homotopy1 (a b : A) :
    d2 A (h1 A (FreeAbelianGroup.of (a,b))) +
    h0 A (d1 A (FreeAbelianGroup.of (a,b))) =
      FreeAbelianGroup.of (a,b) + FreeAbelianGroup.of (a,b) -
      double1 A (FreeAbelianGroup.of (a,b)) := by
  simp [d1,d2,h0,h1,double1,add_assoc]
  abel

theorem homotopy0_all (x : F0 A) :
    d1 A (h0 A x) = x + x - double0 A x := by
  have heq :
      (d1 A).comp (h0 A) =
      (AddMonoidHom.id (F0 A) + AddMonoidHom.id (F0 A) - double0 A) := by
    apply FreeAbelianGroup.lift_ext
    intro a
    simpa [AddMonoidHom.comp_apply, AddMonoidHom.add_apply,
      AddMonoidHom.sub_apply] using homotopy0 A a
  have h := congrArg (fun f : F0 A →+ F0 A => f x) heq
  simpa [AddMonoidHom.comp_apply, AddMonoidHom.add_apply,
      AddMonoidHom.sub_apply] using h

theorem homotopy1_all (x : F1 A) :
    d2 A (h1 A x) + h0 A (d1 A x) =
      x + x - double1 A x := by
  have heq :
      (d2 A).comp (h1 A) + (h0 A).comp (d1 A) =
      (AddMonoidHom.id (F1 A) + AddMonoidHom.id (F1 A) - double1 A) := by
    apply FreeAbelianGroup.lift_ext
    rintro ⟨a,b⟩
    simpa [AddMonoidHom.comp_apply, AddMonoidHom.add_apply,
      AddMonoidHom.sub_apply] using homotopy1 A a b
  have h := congrArg (fun f : F1 A →+ F1 A => f x) heq
  simpa [AddMonoidHom.comp_apply, AddMonoidHom.add_apply,
      AddMonoidHom.sub_apply] using h

#print axioms homotopy0_all
#print axioms homotopy1_all

/-- Universal augmentation of the first free term to the abelian group. -/
def augmentation : F0 A →+ A :=
  FreeAbelianGroup.lift id

theorem augmentation_of (a : A) :
    augmentation A (FreeAbelianGroup.of a) = a := by
  simp [augmentation]

theorem augmentation_surjective : Function.Surjective (augmentation A) := by
  intro a
  exact ⟨FreeAbelianGroup.of a, augmentation_of A a⟩

theorem augmentation_comp_d1_zero :
    (augmentation A).comp (d1 A) = 0 := by
  apply FreeAbelianGroup.lift_ext
  rintro ⟨a,b⟩
  simp [augmentation,d1]

/-- The polynomial first free terms are natural under any homomorphism. -/
def map0 {B : Type*} [AddCommGroup B] (f : A →+ B) :
    F0 A →+ F0 B := FreeAbelianGroup.map f

def map1 {B : Type*} [AddCommGroup B] (f : A →+ B) :
    F1 A →+ F1 B :=
  FreeAbelianGroup.map (fun p : A × A => (f p.1, f p.2))

def map2 {B : Type*} [AddCommGroup B] (f : A →+ B) :
    F2 A →+ F2 B :=
  FreeAbelianGroup.map (fun s =>
    match s with
    | .inl p => Sum.inl (f p.1,(f p.2.1,f p.2.2))
    | .inr p => Sum.inr (f p.1,f p.2))

theorem d1_natural {B : Type*} [AddCommGroup B] (f : A →+ B) :
    (d1 B).comp (map1 A f) = (map0 A f).comp (d1 A) := by
  apply FreeAbelianGroup.lift_ext
  rintro ⟨a,b⟩
  simp [map0,map1,d1, f.map_add]

theorem h0_natural {B : Type*} [AddCommGroup B] (f : A →+ B) :
    (h0 B).comp (map0 A f) = (map1 A f).comp (h0 A) := by
  apply FreeAbelianGroup.lift_ext
  intro a
  simp [map0,map1,h0]

theorem d2_natural {B : Type*} [AddCommGroup B] (f : A →+ B) :
    (d2 B).comp (map2 A f) = (map1 A f).comp (d2 A) := by
  apply FreeAbelianGroup.lift_ext
  intro z
  cases z with
  | inl p =>
      rcases p with ⟨a,⟨b,c⟩⟩
      simp [map1,map2,d2, f.map_add]
  | inr p =>
      rcases p with ⟨a,b⟩
      simp [map1,map2,d2]

theorem h1_natural {B : Type*} [AddCommGroup B] (f : A →+ B) :
    (h1 B).comp (map1 A f) = (map2 A f).comp (h1 A) := by
  apply FreeAbelianGroup.lift_ext
  rintro ⟨a,b⟩
  simp [map1,map2,h1, f.map_add]

#print axioms augmentation_comp_d1_zero
#print axioms augmentation_surjective
#print axioms d1_natural
#print axioms d2_natural
#print axioms h1_natural

#print axioms d1d2_zero
#print axioms homotopy0
#print axioms homotopy1
end CMDG.CondensedCM5R0.BreenDeligne
