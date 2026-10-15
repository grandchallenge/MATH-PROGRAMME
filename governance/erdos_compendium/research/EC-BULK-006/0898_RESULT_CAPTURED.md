RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0898-S01
PROBLEM_ID: 898
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For any nondegenerate planar triangle ABC and P strictly INSIDE the triangle, define PA,PB,PC Euclidean vertex distances; d_A,d_B,d_C are Euclidean distances of P to the LINES supporting opposite sides BC,CA,AB (not necessarily distance to nearest POINT OF SEGMENT, since obtuse triangles can have perpendicular foot off segment). Erdős–Mordell: PA+PB+PC>=2(d_A+d_B+d_C). Equality equilateral ABC and its centre. Historical Er82e,p61 cites 1932 original question and Mordell soon after, while the 1935 American Mathematical Monthly Problem 3740 was published later; distinguish conjecture timing.

## Dated status and primary evidence
Original Erdős 1982 [Er82e,p61] via maintained https://www.erdosproblems.com/898 (catalogue page last edited Jan28 2026) PROVED (LEAN). Historically Paul Erdős American Mathematical Monthly Problem 3740 proposal 1935 and Mordell/Barrow solution 1937, documented https://www.cut-the-knot.org/triangle/ErdosMordell.shtml and Wolfram MathWorld https://mathworld.wolfram.com/Erdos-MordellTheorem.html. A reviewed side-weighted proof in Notes on Euclidean Geometry, section9.4 Theorem9.3, https://people.math.rochester.edu/faculty/dangeba/geom-080399.pdf, uses projection and AM-GM, equality iff equilateral and P centre. Current maintained catalogue labels PROVED (LEAN), Jan28 2026 commenter JoshuaB reports Gemini3 Flash and Aristotle online typecheck, but SAME page external field says 'Formalised statement? No'; no exact Lean source/commit/build/axioms replayed by GCL. Never infer GCL independent formal certification from the catalogue qualifier. Primary historical Er82e p61 page image not independently rechecked.

## Strongest verified interface
Let a=|BC|,b=|CA|,c=|AB|, p=PA,q=PB,r=PC. Standard source-weighted lemmas ap>=b*d_C+c*d_B, bq>=a*d_C+c*d_A, cr>=a*d_B+b*d_A. Divide by a,b,c and sum: p+q+r >= (b/c+c/b)d_A+(c/a+a/c)d_B+(a/b+b/a)d_C >= 2(d_A+d_B+d_C) by AM-GM. For A=(0,0),B=(3,0),C=(0,4),P=(1,1), d_A=d_B=d_C=1 and p+q+r=sqrt2+sqrt5+sqrt10>6. Equilateral side2 centred yields equality both sides 2sqrt3. CHAD exact integer fixture finite_898_899.py/json exhaustively checks squared, denominator-cleared versions of 3 weighted lemmas across 2148 noncollinear integer-coordinate triangles and 27 strictly positive barycentric weight triples per triangle, 173,988 exact tests, min slack0. It checks an algebraic equilateral equality. This is bounded exact verification plus classical paper proof interface, not formal kernel replay for arbitrary real geometry.

## Proposed bounded successor task
Implement side-weighted vertex-to-side distance lemma for all nondegenerate Euclidean triangles and interior P, with supporting-LINE distance, then cyclic inequalities, AM-GM and equality characterization. Acceptance complete independent paper proof or pinned no-sorry Lean theorem with literal axiom report and exact semantic comparison to catalogue statement, 173988 finite integer fixture replay and right-triangle/equilateral regressions. Falsify by one legitimate interior P violating weighted lemma, incorrect orientation of distance-to-line, or incomplete equality conditions. Independently resolve historical 1932 vs 1935 citation and catalog Lean status/metadata mismatch.

## Prerequisites and blocker
Full historical Er82e original page not visually inspected; formal commenter submission URL, exact Lean dependency pins and kernel/axiom output not independently obtained; exact equality characterization relies on standard sourced proof. Do not confuse finite checks and reported upstream Lean label with GCL kernel certification.

## Reuse and claim boundary
Uses recognized Mordell/Barrow classical result, geometrical side-weighted proof, independently replayed exact finite fixture. No new general mathematical result, independent formal Lean build, protected review/merge, live public MathJax verification or V2 admission claimed.
