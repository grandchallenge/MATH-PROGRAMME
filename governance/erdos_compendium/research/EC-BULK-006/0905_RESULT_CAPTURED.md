RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0905-S01
PROBLEM_ID: 905
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For every simple undirected graph on n vertices and m edges with STRICT 4m>n², some actual edge xy belongs to >=n/6 distinct triangles; equivalently 6*|N(x)∩N(y)|>=n with xy in E(G). Counts triangles containing ONE COMMON EDGE (booksize), not just total triangles. Distinguish > n²/4 from >= floor(n²/4) because balanced complete bipartite graph achieves floor(n²/4) edges and has ZERO triangles, so strict threshold indispensable. Integer interpretation uses exact inequalities and no floor rounding.

## Dated status and primary evidence
Original Bollobás–Erdős conjecture in Erdős 1975 graph survey, [Er82e,p71], [Er93,p344] per maintained https://www.erdosproblems.com/905. Maintained #905 edited April7 2026 marks PROVED (LEAN). Independent papers C. S. Edwards (1977 UNPUBLISHED), and N. G. Khadzhiivanov and S. V. Nikiforov 'Solution of a problem of P. Erdős about the maximum number of triangles with a common edge in a graph', C. R. Acad. Bulgare Sci. (1979) pp1315–1318, source metadata https://www.erdosproblems.com/latex/905. Full 1979 primary proof not independently obtained, so imported mathematical proof boundary. Jacob Fox & Po-Shen Loh 'On the Erdős–Rothschild problem' arXiv:1106.0290 secondary refereed primary excerpt https://www.math.cmu.edu/~ploh/docs/research/20110821-erdos-rothschild.pdf cites Edwards and Khadzhiivanov–Nikiforov n/6 result, and explains below-quarter threshold behavior. April7 2026 comment claims online Aristotle/GPT-5.4 typecheck. Public upstream Google DeepMind FormalConjectures/ErdosProblems/905.lean https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/905.lean contains an upstream theorem body 'sorry' with metadata link external v4.29.1 proof https://github.com/plby/lean-proofs/blob/main/src/v4.29.1/ErdosProblems/Erdos905.lean. External proof not GCL kernel built or axiom checked; PROVED(LEAN) does not imply protected local cert.

## Strongest verified interface
For actual undirected edge xy, each common neighbor z yields exactly ONE triangle xyz containing xy, and conversely, so b_G(xy)=popcount(N(x)&N(y)). Source theorem integer version 4m>n² implies exists xy edge 6*b_G(xy)>=n, avoiding numerical approximation. Independently executable CHAD finite_905.py/json exhaustively enumerates ALL 33,866 labelled simple graphs orders n2..6. Every graph exceeding threshold passes; n2 none eligible, n3 exactly1 eligible, n4 exactly7 eligible, n5 exactly176 eligible, n6 exactly4944 eligible; observed minimum over eligible graphs of maximum edge booksize for n3=1,n4=2,n5=2,n6=2. Also checks balanced K_floor(n/2),ceil(n/2) for n2..8 has floor(n²/4) edges and zero triangles. Exact finite certificate not general proof.

## Proposed bounded successor task
Prove triangle-book cardinality = common neighborhood intersection for all simple graphs and edges; exact integer translation of strict threshold and conclusion; derive/source-check full theorem if pursuing beyond finite range. Acceptance complete elementary paper proof or pinned no-placeholder Lean theorem with actual axiom report, byte-identical finite fixture JSON rerun for all 33866 graphs including strict-boundary bipartite examples; falsify via missed shared-edge triangle, any exact counterexample with m>n²/4, or wrong >= threshold. Second successor retrieve full 1979 original proof, reconstruct general n argument, pin/compile independent v4.29.1 external Lean with exact theorem semantics and printed axioms before mathematical certification.

## Prerequisites and blocker
Full 1979 source article and 1975 historical pages not directly obtained/replayed. External v4.29.1 formal proof not GCL compiled and upstream has sorry. Cannot claim independently proved all-n theorem or protected review/main merge.

## Reuse and claim boundary
Uses published Khadzhiivanov–Nikiforov/Edwards solved result, Fox–Loh secondary source, independently derived exact finite predicate and full small graph enumeration. No novel general proof, trusted Lean certification, protected merger, public live MathJax or V2 admission.
