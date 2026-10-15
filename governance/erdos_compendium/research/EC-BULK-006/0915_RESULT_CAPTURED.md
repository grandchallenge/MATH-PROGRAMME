RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0915-S01
PROBLEM_ID: 915
DISPOSITION: STATUS_CONFLICT
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Bollobás–Erdős original: any simple graph G with v=1+t(m-1) vertices and at least e=1+t*binomial(m,2) edges contains two distinct vertices connected by m 'disjoint' paths? Integers m>=2,t>=1. WORD DISJOINT ambiguous. Vertex-disjoint means INTERNAL vertices disjoint (shared endpoints), vs EDGE-disjoint means shared edges prohibited but internal vertices may overlap. Both notions coincide for certain small m but the conjecture is FALSE for internal vertex disjoint when m>=5, TRUE for edge-disjoint with stronger Mader bound. Maintained https://www.erdosproblems.com/915 labels SOLVED not uniformly proved/disproved. Source fidelity requires keeping both semantics explicit.

## Dated status and primary evidence
Original Béla Bollobás and Paul Erdős 'Extremal problems in graph theory', Mat. Lapok (1962)143–152 [BoEr62], and Erdős [Er67b,p4], all referenced at https://www.erdosproblems.com/latex/915 and https://www.erdosproblems.com/915. Vertex-disjoint target k_m(v) minimum host edges forcing pair with >=m internally vertex-disjoint paths: small cases Bártfai1960 k3(2t)=3t-1,k3(2t+1)=3t+1; Bollobás1966 k4(v)=2v-1. John Leonard 'On a conjecture of Bollobás and Erdős', Periodica Math Hungar (1973)281–284 gives EXPLICIT m5 counterexample v57 e141 =1+14*binom(5,2), lacking any pair with 5 internally vertex-disjoint paths; full labelled edge list NOT independently reconstructed GCL. Sørensen–Thomassen 'On k-rails in graphs', J Combin Theory B (1974)143–159 gives k5(v)=floor(8v/3)-3 v>=13 and validity of original bound for 3-connected targets; Walter Mader 'Ein Extremalproblem des Zusammenhangs von Graphen', Math Z (1973)223–231 disproves general vertex branch for all m>=6 and proves STRONGER edge-disjoint result: ell_m(v)=floor(m*(v-1)/2+1) for m>=2, hence edge version affirmative. Exact main catalog source bibliography https://www.erdosproblems.com/latex/915. Publication proofs not independently replayed GCL, so status source-grounded SPLIT, not a single negative theorem for edges.

## Strongest verified interface
Clique bouquet of t copies of K_m with exactly one common central vertex and otherwise disjoint has v=1+t(m-1), e=t*binom(m,2), exactly ONE edge short of conjectured threshold. Any pair in same K_m has at most m-1 internally vertex-disjoint or edge-disjoint paths because its degree is m-1 unless center endpoint, and any pair in different cliques shares cut center, so also cannot have m. This proves lower-bound sharpness at E-1 for both interpretations, not the positive threshold. GCL exact finite_914_915.py/json enumerates all relevant labelled simple graphs orders n3..6 for m2,m3 original threshold, **28661 graph-parameter tests** using Menger vertex-separator enumeration, with special handling if endpoints adjacent: count direct edge plus paths after removal of that edge. All pass; no 57-vertex Leonard graph and no all-m Mader theorem proved by these finite tests. Fixture also checks bouquet counts m2..8, t1,2,3,5. For edge-disjoint branch separate maximum-flow/min-edge-cut verification remains future work.

## Proposed bounded successor task
Formalize bouquet exact vertex/edge counts and absence of m disjoint paths under BOTH semantics, and Menger adjacent-endpoint correction; replay 28661 finite cases with exact stored JSON and no-placeholder Lean with axiom readback. Independently reconstruct original Leonard1973 57-vertex141-edge graph and run exact all-pairs minimum vertex separator <=4 certificate; source-check all m>=6 Mader constructions. Separately independently source-review Mader edge-disjoint degree-sensitive theorem with correct strict inequality/rounding before any local universal proof certification. Source audit original 1962 vs 1967 texts for whether 'disjoint' meant internally vertex or edge disjoint.

## Prerequisites and blocker
Original 1962/1967 disjoint wording unresolved, Leonard explicit 57-vertex graph not independently encoded, Mader1973 general edge theorem not reconstructed, no GCL Lean or mathematical protected review. Finite small data not proof general cases.

## Reuse and claim boundary
Uses classical Bollobás–Erdős, Leonard, Mader, Sørensen–Thomassen results, exact independent clique bouquet counting and finite Menger regression. BOTH answers must remain disambiguated. No independently verified Leonard certificate, new theorem, protected merge, public live MathJax or V2 admission.
