import Init

/-!
Finite, kernel-checked SimpleGraph-like degree-cap enumeration on FOUR
labelled vertices, with the six possible undirected edges enumerated exactly.
No source-level axiom, no sorry/admit, no native_decide. This is a finite
corroboration, not Lovász's general (g,f) factor theorem.
-/
namespace Erdos561FiniteGraph

-- The edges of the labelled K4, in bit order 0..5.
def edgeU (i : Nat) : Nat :=
  if i ≤ 2 then 0 else if i ≤ 4 then 1 else 2

def edgeV (i : Nat) : Nat :=
  if i == 0 then 1 else if i == 1 then 2 else if i == 2 then 3
  else if i == 3 then 2 else 3

def incident (i v : Nat) : Bool := (edgeU i == v) || (edgeV i == v)

-- `mask` selects graph edges; `colour` selects their red subset.
def degreeBy (mask colour v : Nat) : Nat :=
  ((List.range 6).filter fun i =>
    mask.testBit i && colour.testBit i && incident i v).length

def degree (mask v : Nat) : Nat :=
  ((List.range 6).filter fun i => mask.testBit i && incident i v).length

def blueDegree (mask colour v : Nat) : Nat :=
  ((List.range 6).filter fun i =>
    mask.testBit i && !(colour.testBit i) && incident i v).length

def maxDegree (mask : Nat) : Nat :=
  (List.range 4).foldl (fun d v => max d (degree mask v)) 0

def numSaturated (mask D : Nat) : Nat :=
  ((List.range 4).filter fun v => degree mask v == D).length

def canSplit (mask α β : Nat) : Bool :=
  (List.range 64).any fun colour =>
    (List.range 4).all fun v =>
      decide (degreeBy mask colour v ≤ α) &&
      decide (blueDegree mask colour v ≤ β)

def passesCoreTest (mask α : Nat) : Bool :=
  let D := maxDegree mask
  let β := D - α
  if α > 0 && β > 0 && !(canSplit mask α β) then
    decide (D + 1 ≤ numSaturated mask D)
  else true

-- Every finite simple labelled graph on four vertices has the stated
-- degree-saturated vertex bound if an (alpha,beta) degree-cap split fails.
theorem four_vertex_degree_core :
    (List.range 64).all (fun mask =>
      (List.range 4).all (fun α => passesCoreTest mask α)) = true := by decide

-- K3 plus one isolate is an actual D=2 alpha=1 beta=1 obstruction.
def triangleWithIsolate : Nat := 1 + 2 + 8

theorem triangle_has_no_1_1_split :
    canSplit triangleWithIsolate 1 1 = false := by decide

theorem triangle_saturates_three :
    numSaturated triangleWithIsolate 2 = 3 := by decide

#print axioms Erdos561FiniteGraph.four_vertex_degree_core
#print axioms Erdos561FiniteGraph.triangle_has_no_1_1_split
#print axioms Erdos561FiniteGraph.triangle_saturates_three

end Erdos561FiniteGraph
