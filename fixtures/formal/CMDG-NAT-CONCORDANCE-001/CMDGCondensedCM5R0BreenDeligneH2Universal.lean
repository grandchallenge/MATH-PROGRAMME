import Mathlib.Tactic


/-!
# CM5: universal finite degree-two doubling homotopy

Construct the natural 13-term commutativity and 16-term associativity
degree-three lift of 2·id − [2] − h₁d₂. The polynomial identities hold for
EVERY abelian source A and EVERY abelian coefficient group B.
They are proved by ordinary abelian-group calculation in Lean, without
fixing any finite group or merely checking sample inputs.

P/H/S/D are exactly the previously protected pentagon/hexagon/
symmetry/strict-diagonal boundary formulas; h1 is the genuine
degree-one homotopy's polynomial pullback formula.
This is the universal algebraic spine, not by itself derived sheaf-Hom
or a complete finite-type Breen–Deligne resolution.
-/
noncomputable section
universe u v
namespace CMDG.CondensedCM5R0.BreenDeligneH2Universal

variable {A : Type u} [AddCommGroup A]
variable {B : Type v} [AddCommGroup B]

def P (f : A → A → A → B) (a b c d : A) : B :=
  f b c d - f (a+b) c d + f a (b+c) d - f a b (c+d) + f a b c

def H (f : A → A → A → B) (g : A → A → B)
    (a b c : A) : B :=
  f a b c - f b a c + f b c a - g a (b+c) + g a b + g a c

def S (g : A → A → B) (a b : A) : B :=
  g a b + g b a

def D (g : A → A → B) (a : A) : B := g a a

def h1 (f : A → A → A → B) (g : A → A → B)
    (a b : A) : B :=
  f a a (b+b) - f a b b - f a b (a+b) - g (a+b) b

def h2Comm (f : A → A → A → B) (g : A → A → B)
    (a b : A) : B :=
  - P f b b a a +
  H f g b a b -
  H f g (b+b) a a +
  H f g a b b +
  H f g a b (a+b) -
  H f g a a (b+b) -
  S g a b +
  (S g a (b+b) + S g a (b+b)) +
  S g (a+b) b -
  S g (a+b) a -
  S g (a+a) (b+b) -
  D g b + D g a

def h2Assoc (f : A → A → A → B) (g : A → A → B)
    (a b c : A) : B :=
  - P f b (a+b) c c +
  P f a b c (b+c) +
  P f a b c (a+b+c) -
  P f a b b (c+c) -
  P f a b (a+b) (c+c) +
  P f a a (b+b) (c+c) -
  P f (a+b) c b c +
  P f (a+b) b c c +
  H f g c b c +
  H f g b (a+b) c -
  H f g (a+b+c) b c -
  S g b c +
  S g (b+c) c -
  S g (a+b) b +
  S g (a+b+c) b -
  D g c

theorem h2Comm_identity (f : A → A → A → B) (g : A → A → B)
    (a b : A) :
    h2Comm f g a b + h1 f g a b - h1 f g b a =
      g a b + g a b - g (a+a) (b+b) := by
  simp only [h2Comm,P,H,S,D,h1]
  simp only [add_left_comm (G := A), add_comm (G := A)]
  abel

theorem h2Assoc_identity (f : A → A → A → B) (g : A → A → B)
    (a b c : A) :
    h2Assoc f g a b c +
        (h1 f g b c - h1 f g (a+b) c +
         h1 f g a (b+c) - h1 f g a b) =
      f a b c + f a b c - f (a+a) (b+b) (c+c) := by
  simp only [h2Assoc,P,H,S,D,h1]
  simp only [add_left_comm (G := A), add_comm (G := A)]
  abel

/-- The closed-cochain consequence of the explicit degree-two homotopy,
valid over every abelian coefficient group B, without Banach assumptions. -/
theorem h2Assoc_closed_identity
    (f : A → A → A → B) (g : A → A → B)
    (hp : ∀ a b c d, P f a b c d = 0)
    (hh : ∀ a b c, H f g a b c = 0)
    (hs : ∀ a b, S g a b = 0)
    (hd : ∀ a, D g a = 0)
    (a b c : A) :
    h1 f g b c - h1 f g (a+b) c +
      h1 f g a (b+c) - h1 f g a b =
      f a b c + f a b c - f (a+a) (b+b) (c+c) := by
  have h := h2Assoc_identity f g a b c
  have hzero : h2Assoc f g a b c = 0 := by
    simp only [h2Assoc, hp, hh, hs, hd, neg_zero, zero_add,
      sub_zero, add_zero]
  rw [hzero, zero_add] at h
  exact h

theorem h2Comm_closed_identity
    (f : A → A → A → B) (g : A → A → B)
    (hp : ∀ a b c d, P f a b c d = 0)
    (hh : ∀ a b c, H f g a b c = 0)
    (hs : ∀ a b, S g a b = 0)
    (hd : ∀ a, D g a = 0)
    (a b : A) :
    h1 f g a b - h1 f g b a =
      g a b + g a b - g (a+a) (b+b) := by
  have h := h2Comm_identity f g a b
  have hzero : h2Comm f g a b = 0 := by
    simp only [h2Comm, hp, hh, hs, hd, neg_zero, zero_add,
      sub_zero, add_zero]
  rw [hzero,zero_add] at h
  exact h

#print axioms h2Assoc_closed_identity
#print axioms h2Comm_closed_identity

#print axioms h2Comm_identity
#print axioms h2Assoc_identity
end CMDG.CondensedCM5R0.BreenDeligneH2Universal
