RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0904-S01
PROBLEM_ID: 904
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For integers 2<=r<=n, let t_r(n) be exact integer Turán number max edges in n-vertex K_(r+1)-free simple graph, attained by balanced complete r-partite graph. For EVERY graph G with n vertices and m>=t_r(n) edges, find a clique S of exactly r vertices with sum_{v in S} degree(v) >= 2*r*m/n. Equivalently n*sum degree >=2*r*m using integers. This is EXISTENCE of one clique with large TOTAL degree, not all vertices having degree >=mean and not any clique of different size. The public FC theorem has an extra r=1 case, semantic extension that must be separately checked when formalizing.

## Dated status and primary evidence
Original Bollobás and Erdős 'Unsolved Problems', Fifth British Combinatorial Conference 1975 pp678-680, Erdős 1975 'Some recent progress on extremal problems in graph theory', Congressus Numerantium pp3–14 special r=3 with n²/3 edge hypothesis. Maintained https://www.erdosproblems.com/904 PROVED (LEAN), last edited Apr3 2026. Edwards 1978 proved r2..8 for n>=r², Faudree 1992 full r with n>(r-1)r²/4. Full published solution B. Bollobás & V. Nikiforov, 'The Sum of Degrees in Cliques', Electronic Journal of Combinatorics 12 (2005) N21 DOI10.37236/1988, journal primary https://www.combinatorics.org/ojs/index.php/eljc/article/view/v12i1n21, published Nov7 2005. Its original abstract directly states m>=t_r(n) => Delta_r(n,m)>=2rm/n for all r>=2, and separate near-threshold stability estimate. Public Google DeepMind Formal Conjectures main FormConjectures/ErdosProblems/904.lean https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/904.lean contains upstream theorem with sorry and metadata pointing to external proof https://github.com/plby/lean-proofs/blob/main/src/v4.29.1/ErdosProblems/Erdos904.lean. GCL has NOT independently built this external Lean4 proof nor axiom audited. Do not equate catalog solved(LEAN) with GCL protected proof certification. Source journal publisher primary abstract directly verified; full published proof not independently replayed.

## Strongest verified interface
Exact balanced complete r-partite Turán construction: q=floor(n/r), h=n-r*q; h parts size q+1, r-h size q, with exact t_r(n)=(n² - [h(q+1)²+(r-h)q²])/2 integer. In ANY graph the target check is n*max_{r-clique S} sum degrees >=2*r*m, avoiding floats. Independent CHAD finite_903_904.py/json exhaustively enumerates all simple graphs n2..6, total 2^1+2^3+2^6+2^10+2^15=33866 labelled graphs, checks every r=2..n against exact Turán threshold and all r-cliques, and verifies the inequality wherever hypothesis applies. K3,3 has n6,r2,m9=t2(6), each cross edge degree sum6 exactly 2*r*m/n=6, proving equality/sharpness in this case. These are exact finite checks, not general BN05 proof.

## Proposed bounded successor task
Prove exact Turán edge-number formula for balanced part sizes with combinatorial pair counting and source-normalized m>=t_r. Prove full finite inequality for n<=6 using independent exhaustive integer graph enumeration and retain sharp K3,3 witness; acceptance complete paper proof or pinned no-sorry Lean with literal axiom report, byte-identical finite result JSON and all 33866 graphs checked. Falsify by counterexample with m>=t_r or mismatched graph/edge/clique count. Separately replay published 2005 proof for ALL n,r and check semantic and version comparison with external Lean r>=1 theorem and its pinned deps/axioms; no claim general proof GCL-certified until successful.

## Prerequisites and blocker
Full 2005 technical proof not independently reconstructed; original 1975 exact page image not inspected; external Aristotle Lean at plby v4.29.1 not compiled by GCL, upstream FC body sorry. No independent protected reviewer/Lean kernel certification.

## Reuse and claim boundary
Used primary 2005 published solution, maintained history, independently derived exact finite extremal graph verification and equality case. This is researched editorial evidence for published theorem, not a novel theorem or independent analytic/formal proof, protected main merge, deployed browser rendering or V2 admission.
