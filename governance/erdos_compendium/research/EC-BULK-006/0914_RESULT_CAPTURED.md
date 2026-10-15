RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0914-S01
PROBLEM_ID: 914
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For r>=2, m>=1, every finite simple graph G with exactly n=rm vertices and minimum degree at least m(r-1) contains m PAIRWISE VERTEX-DISJOINT r-cliques, partitioning all vertices. Equivalent: complement graph H has maximum degree <=m-1 and an equitable proper vertex colouring with exactly m color classes each of size exactly r. Degree identity deg_H(v)=rm-1-deg_G(v); disjoint r-cliques partition iff complement color classes independent. Published Hajnal–Szemerédi theorem PROVED. Distinguish minimum degree in G from maximum degree in complement, and r-cliques vs m colors.

## Dated status and primary evidence
Maintained https://www.erdosproblems.com/914 PROVED (LEAN), source [Er67b], last edited Apr15 2026. Corrádi–Hajnal, 'On the maximal number of independent circuits in a graph', Acta Math Acad Sci Hungar14 (1963)423–439 solved r3. Hajnal and Szemerédi 'Proof of a conjecture of P. Erdős' in Combinatorial Theory and Its Applications vol II, Colloq Math Soc Janos Bolyai 4 (1970)601–623 solves general r>=4. Kierstead and Kostochka 'A Short Proof of the Hajnal-Szemerédi Theorem on Equitable Colouring', Combinatorics Probability and Computing 17 (2008)265–270 DOI10.1017/S0963548307008619; ORIGINAL publisher abstract at https://www.cambridge.org/core/journals/combinatorics-probability-and-computing/article/abs/short-proof-of-the-hajnalszemeredi-theorem-on-equitable-colouring/5530A5AACBD8246D6B0D7E9A85810FD2 gives stronger form any maximum degree Delta admits equitable Delta+1 coloring and polynomial-time algorithm. Apr15 2026 catalogue comment reports Aristotle completed formalization of Kierstead–Kostochka after prolonged execution. Public external Lean code https://github.com/Woett/Lean-files/blob/main/ErdosProblem914.lean ~3375 lines and https://github.com/plby/lean-proofs/blob/main/src/v4.29.1/ErdosProblems/Erdos914.lean linked from https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/914.lean; upstream FC theorem body has sorry, so NO GCL independent pinned Lean build or axiom certification. Maintained metadata 'Formalised statement? No' inconsistent with PROVED(LEAN) label; needs source lock.

## Strongest verified interface
Exact elementary equivalence: min deg_G>=m(r-1) iff complement max degree<=m-1 (because n=rm). Disjoint clique-partition into m K_r iff complement has equitable m-coloring with m independent color classes size r. For n6 r3 m2 the graph K3,3 has min-degree3, one less than required4, and NO triangles, so lowering degree bound universally fails. GCL exact executable finite_914_915.py/json enumerates ALL labelled simple graphs orders n2..6, every factorization n=rm, filters min degree threshold, and exact-covers each by m vertex-disjoint r-cliques. **1949 qualifying graph-parameter cases**, no failures, and K3,3 boundary checked. This does not independently prove arbitrary n theorem or compile external Lean.

## Proposed bounded successor task
Formally prove graph complement degree identity and clique partition/equitable coloring equivalence, n=rm and constraints, with complete proof or pinned no-sorry Lean and literal axiom report plus 1949 finite cases replay. Independently reconstruct 2008 Kierstead–Kostochka combinatorial recoloring algorithm/invariants and theorem, then pin Woett/plby source commit, Mathlib and Lean toolchain and verify no hidden sorry/admitted axioms and exact formal hypotheses before GCL certification. Falsify via any eligible n<=6 graph without exact clique cover or incorrect coloring complement.

## Prerequisites and blocker
Full 1970 and 2008 proofs not reconstructed GCL; external Lean sources not independently built. Although classical theorem published and catalogue says PROVED(LEAN), this source return is draft evidence not verified GCL theorem or protected admission.

## Reuse and claim boundary
Uses classical Corrádi–Hajnal, Hajnal–Szemerédi and Kierstead–Kostochka results and exact GCL bounded graph enumeration. No novel theorem, independent Lean kernel certificate, protected main merge, deployed public MathJax verification or V2 admission.
