RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0925-S01
PROBLEM_ID: 925
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For a finite simple graph G on n vertices, say G is NOT 2-edge-Ramsey for K3 if SOME red-blue colouring of edges E(G) avoids monochromatic triangles in BOTH colors. Erdős [Er69b] asks whether there exists ONE absolute real delta>0 and positive c such that EVERY such n-vertex G for ALL sufficiently large n has INDEPENDENCE alpha(G)>=c*n^(1/3+delta)? NO. This is about G's ordinary independent VERTEX set, not edges in one particular color or a host absent all triangles. The optimal polynomial exponent is 1/3 up to polylog factors, disproved by Alon–Rödl 2005.

## Dated status and primary evidence
Maintained https://www.erdosproblems.com/925 DISPROVED, credited Alon–Rödl [AlRo05] and notes Sudakov's improved loglog upper. Original Erdős 'Problems and results in chromatic graph theory', Proof Techniques in Graph Theory (1969)pp27–35 [Er69b], historical author pdf https://www.renyi.hu/~p_erdos/1969-13.pdf not separately page-image replayed this run. Noga Alon and Vojtěch Rödl, PRIMARY *Sharp bounds for some multicolor Ramsey numbers*, Combinatorica 25(2)(2005)125–141 DOI10.1007/s00493-005-0011-9; author's FINAL source manuscript https://web.math.princeton.edu/~nalon/PDFS/arodl4.pdf, independently visually inspected p1 (title, abstract) and pp2,3 (definitions/background) with full PDF text including Theorem3.2 p6, detailed proof p7. Exact 3-color Ramsey R(3,3,m)=r(K3,K3,Km) defined as minimum N forcing RED K3, BLUE K3 or GREEN Km in every 3-coloring of complete graph K_N. Theorem3.2, k=2 first two colors forbidden triangles: for every positive eps, for all sufficiently large m,
  c_eps*m^3/(log m)^(4+eps) <= R(3,3,m) <= C*m^3*loglog m/(log m)^2.
Source paper itself credits B. Sudakov removing loglog from upper bound (author manuscript p8). The original source contains the deep probabilistic spectral construction, random shifts, pseudorandom regular graphs and independent-set estimates; no GCL independent replay of all asymptotics.

## Strongest verified interface
Finite exact equivalence: For each n and ANY pair (G, red-blue coloring of E(G)), produce coloring of ALL edges of K_n with RED/BLUE colors on E(G), and GREEN on nonedges of G. Then absence red/blue monochrom triangle means first two color classes triangle-free; G's independent vertex subsets are EXACTLY green complete subgraphs. Reversible map yields 3-color Ramsey statement. Thus a universal alpha lower for all nonRamsey G iff 3color R(3,3,m) upper appropriately reparameterized. Exact finite_924_925.py/json preexisted this current run and independently replayed unchanged from Python in read-only form. Across all n1..5, enumerate all 3color K_n edge patterns with red/blue each trianglefree, **29769** valid patterns; alpha(red+blue graph) computed independent brute vertex-subsets equals max green clique size for EACH. All 32768 red-blue K6 colorings checked and none avoids mono K3 while K5 admits red C5, blue complementary C5. Finite data is ONLY proof regression not Alon–Rödl asymptotic construction.

Asymptotic transfer independent algebra: lower Ramsey R(3,3,m)>=c_eps m^3/(log m)^(4+eps) supplies arbitrarily large n with tri-free red/blue color classes and no green Km, hence nonRamsey G with alpha<m ≲ n^(1/3)(log n)^((4+eps)/3). Every n^delta eventually dominates any (log n)^C, so NO universal positive-power delta. Conversely upper R(3,3,m)<=C m^3 loglog m/(log m)^2 implies all sufficiently large n-vertex nonRamsey G have alpha >= order n^(1/3)(log n)^(2/3)/(loglog n)^(1/3); the upper bound on R gives lower bound for alpha, lower bound on R gives counterexample alpha UPPER. Do not invert this direction. Theoretical R(3,3,m) cubic polynomial exponent is sharply shown, not an exact leading asymptotic constant.

## Proposed bounded successor task
Formalize reversible complete-graph 3color edge encoding (red/blue for real G edges, green for missing) and alpha(G)=max green clique, equivalence of G nonRamsey to absence of first two mono triangles. Acceptance elementary proof or pinned no-placeholder Lean with literal axioms and exact 29769/32768 tests. Then formalize Ramsey lower-bound inversion and nonexistence of universal n^(1/3+delta) guarantee, quantify for every delta>0 and sufficiently large n/subsequence as appropriate, correct log exponent and all integer rounding. Falsify by reversing Ramsey upper/lower, confusing G's nonedges and green edges, or assuming a fixed small graph proves an asymptotic negation. Full mathematical successor independently source-audit Alon–Rödl Theorem3.2 lower spectral/pseudorandom construction and Sudakov loglog improvement, do not claim finite evidence certifies construction.

## Prerequisites and blocker
Alon–Rödl proof source full 15 pages accessible but not independently mathematically reconstructed or formalized; original Erdős1969 page not independently verified this turn. No GCL Lean, independent protected specialist mathematical adjudication, protected main merge, public browser math rendering or V2.

## Reuse and claim boundary
Published classical DISPROOF from Alon–Rödl2005, imported precise published theorem with independently proved elementary three-color encoding and algebraic exponent transfer, bounded exact color enumerations; no novel infinite construction, priority/novelty claim, certified formal proof or protected admission.
