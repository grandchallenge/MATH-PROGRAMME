RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0900-S01
PROBLEM_ID: 900
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For fixed real c>1/2, sample uniformly from all simple labelled graphs G(n,m) on n vertices with EXACTLY m=floor(c*n) edges (valid for n sufficiently large). Erdős asks for a function f:(1/2,infinity)->(0,1) such that with probability 1-o(1) graph has a SIMPLE path with at least f(c)*n edges (or vertices, differing by one), and f(c)->0 as c↓1/2 and f(c)->1 as c->infinity. Random G(n,m), NOT deterministic all graphs with >=cn edges, and NOT directly the independent-edge G(n,p) model. Distinguish undirected edge threshold (1+epsilon)n/2 from directed (1+epsilon)n in AKS abstract.

## Dated status and primary evidence
Original Erdős [Er78,p32] and [Er82e] per maintained https://www.erdosproblems.com/900, marks PROVED; original Er78 printed p32 not independently read in this execution. Primary paper Miklós Ajtai, János Komlós, Endre Szemerédi, 'The longest path in a random graph', Combinatorica 1(1) (March 1981), pp1-12 DOI10.1007/BF02579172. Original publisher/university publication abstract https://www.researchwithrutgers.org/en/publications/the-longest-path-in-a-random-graph/ confirms that an undirected random graph with (1+epsilon)n/2 edges contains a path of length c*n, and a random DIRECTED graph with (1+epsilon)n directed edges contains long directed path, solving Erdős conjecture. Open-access version of record archived by Rutgers https://scholarship.libraries.rutgers.edu/esploro/outputs/journalArticle/The-longest-path-in-a-random/991031550002004646; full 12-page published proof NOT independently reconstructed on CHAD. Maintained page last edited March7 2026 records f(c) limit conditions and original Erdős vs Szemerédi historical disagreement, reported as historical not contemporary unresolved controversy. No public formalization/protected Lean certificate.

## Strongest verified interface
Finite theorem: L(G)=maximum number of DISTINCT vertices in any simple undirected path, so path edge-length L(G)-1; adding an edge cannot reduce L(G) because existing paths remain. In G(n,m) each graph selected with uniform probability 1/binomial(binomial(n,2),m). CHAD exact finite_900_902.py/json exhaustively enumerates all labelled simple graphs for n=3,4,5 (2^3+2^6+2^10=1096 total), calculates L(G) with exact subset-and-endpoint DP, groups by m with counts binomial(binomial(n,2),m), verifies edge-monotonicity for every graph plus every missing edge. Deterministic counterexample: an n-vertex STAR graph has n−1 edges (for n>2 exceeds n/2) but longest path only 3 vertices, so cannot transfer whp claim to all graphs. This bounded computation does NOT imply any asymptotic random graph theorem or f(c) limits.

## Proposed bounded successor task
Formalize exact longest simple path dynamic programming interface with distinct vertices, graph-edge monotonicity and G(n,m) uniform edge subset count for finite n,m. Acceptance complete mathematical proof or pinned no-sorry Lean kernel build with literal axiom readback, replay all 1096 labelled graphs and binomial counts, and validate star counterexample. Falsify by a repeated path vertex counted as simple, DP missing actual path, nonuniform G(n,m) counting or edge-addition decreasing L. Separate deep source task: fully inspect and reconstruct AKS81 probability argument with directed/undirected and edge/vertex path conventions and both limiting f(c) requirements. Do not treat finite fixtures as theorem replay.

## Prerequisites and blocker
Er78 original page and entire AKS81 proof not source-page independently replayed. Primary university-authored abstract and DOI secured, maintained f(c) limits imported. GCL no Lean proof, independent asymptotic mathematical adjudication, protected admission or public browser check.

## Reuse and claim boundary
Reused AKS81 published primary theorem and maintained solved status, independently constructed and executed exact finite graph DP plus monotonicity and model-count test. No novel asymptotic result or proof priority, no protected main merge, Lean certification or V2 editorial admission claimed.
