import Init
set_option maxRecDepth 20000
set_option maxHeartbeats 0

/-!
  GCL Erdős #561: kernel-checked arithmetic sublemmas and a bounded
  3x3 joint-residual PARAMETER certificate.
  This module deliberately DOES NOT claim formalization of Ramsey arrowing,
  Lovász's (g,f)-factor theorem, or the 2026 two-component theorem.
  No axioms, sorry, admit, or external decision oracles.
-/
namespace Erdos561

structure Triple where
  a : Nat
  b : Nat
  c : Nat
  deriving DecidableEq, Repr

def triples : List Triple :=
  ((List.range 7).map (· + 1)).flatMap fun a =>
    ((List.range a).map (· + 1)).flatMap fun b =>
      ((List.range b).map (· + 1)).map fun c => ⟨a, b, c⟩

def w3 (n m : Triple) : Nat := max (n.a + m.b - 1) (n.b + m.a - 1)
def w4 (n m : Triple) : Nat :=
  max (n.a + m.c - 1) (max (n.b + m.b - 1) (n.c + m.a - 1))
def w5 (n m : Triple) : Nat := max (n.b + m.c - 1) (n.c + m.b - 1)
def w6 (n m : Triple) : Nat := n.c + m.c - 1

def residualLeft (n m : Triple) : Nat :=
  (n.b + m.a - 1) +
  max (n.b + m.b - 1) (n.c + m.a - 1) +
  max (n.b + m.c - 1) (n.c + m.b - 1) + (n.c + m.c - 1)

def residualRight (n m : Triple) : Nat :=
  (n.a + m.b - 1) +
  max (n.a + m.c - 1) (n.b + m.b - 1) +
  max (n.b + m.c - 1) (n.c + m.b - 1) + (n.c + m.c - 1)

def joint (n m : Triple) : Nat := w3 n m + w4 n m + w5 n m + w6 n m

def switching (n m : Triple) : Nat := joint n m - max (residualLeft n m) (residualRight n m)

def forcedD (n m : Triple) : Nat := w3 n m - 1

def hypotheticalE (n m : Triple) : Nat := joint n m - 1

def requiredOrder (n m : Triple) : Nat :=
  max (n.a + n.b + n.c + 3) (m.a + m.b + m.c + 3)

def boundedRelevant (n m : Triple) : Bool := switching n m > 0 && forcedD n m ≤ 7

def edgeContradiction (n m : Triple) : Bool :=
  hypotheticalE n m < forcedD n m * (forcedD n m + 1) / 2

def vertexContradiction (n m : Triple) : Bool :=
  requiredOrder n m > 2 * hypotheticalE n m - (forcedD n m * forcedD n m) + 1

def boundedGate (n m : Triple) : Bool :=
  if boundedRelevant n m then edgeContradiction n m || vertexContradiction n m else true

def pairs : List (Triple × Triple) :=
  triples.flatMap fun n => triples.map fun m => (n,m)

-- Expected independently generated finite parameter totals:
theorem triple_count : triples.length = 84 := by decide
-- The following certificates check the bounded arithmetic calculation ONLY.
-- Graph-theoretic reduction to this domain is a separate paper proof.
theorem bounded_parameter_gate : pairs.all (fun p => boundedGate p.1 p.2) = true := by decide

-- The bounded domain contains 82 positive-switching candidates of forced
-- degree at most seven. This is independently verified in Python as well.
theorem relevant_candidate_count :
    (pairs.filter (fun p => boundedRelevant p.1 p.2)).length = 82 := by decide

-- Exactly 74 candidates already fail the core edge budget; the remaining
-- eight candidates fail the vertex budget. The edge check gets priority.
theorem edge_exclusions_count :
    (pairs.filter (fun p => boundedRelevant p.1 p.2 &&
      edgeContradiction p.1 p.2)).length = 74 := by decide

theorem vertex_exclusions_count :
    (pairs.filter (fun p => boundedRelevant p.1 p.2 &&
      !edgeContradiction p.1 p.2 && vertexContradiction p.1 p.2)).length = 8 := by decide

#print axioms Erdos561.triple_count
#print axioms Erdos561.bounded_parameter_gate
#print axioms Erdos561.relevant_candidate_count
#print axioms Erdos561.edge_exclusions_count
#print axioms Erdos561.vertex_exclusions_count

end Erdos561
