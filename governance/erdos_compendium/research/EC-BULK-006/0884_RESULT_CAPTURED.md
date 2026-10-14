RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0884-S01
PROBLEM_ID: 884
DISPOSITION: STATUS_CONFLICT
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let 1=d1<...<dt=n be all positive divisors of n. Define T(n)=sum_{1<=i<j<=t} 1/(dj-di), and S(n)=sum_{1<=i<t} 1/(d_{i+1}-di). Exact Erdős claim: exists ABSOLUTE C with T(n)<=C*(1+S(n)) for all n, including additive 1. Tao notes historical 1998 source seemingly uses j<t, while modern formal and maintained statements use j<=t; endpoint equivalence requires explicit comparison, not silent normalization.

## Dated status and primary evidence
Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 last updated July 3 2026 records DISPROVED (LEAN), with formal provider google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 path FormalConjectures/ErdosProblems/884.lean blob 847c8684320fa74c63724fa0a43b54ffe4ad028f. A formal STATEMENT does not certify the proof. Maintained https://www.erdosproblems.com/884 edited Apr 1 2026 identifies unconditional negative resolution. PRIMARY Terence Tao, 'On the Sum of Reciprocals of Gaps Between Divisors', dated Sep 9 2025, https://terrytao.wordpress.com/wp-content/uploads/2025/09/erdos-884.pdf, Theorem 1.1 printed p1 directly visually inspected: ratio T/(1+S) unbounded ASSUMING the qualitative Hardy–Littlewood prime-tuples conjecture. PRIMARY Daniel Larsen, 'A Question of Erdős on Reciprocals of Gaps Between Divisors', https://github.com/Larsen-Daniel/Erdos-884/blob/main/884.pdf, posted Mar 29 2026 and updated Mar 30 after discussion, reports an UNCONDITIONAL proof by repeated scales of the clustered-divisor construction. Maintained https://www.erdosproblems.com/forum/thread/884 records author and Tao comments. Larsen full PDF was not accessible for an independent line-by-line proof audit in this execution. Honicky public source https://github.com/honicky/erdos884 README/NEXT_STEPS.md reports complete formal Larsen proof, Lean v4.31.0/mathlib pin, no sorries, #print axioms = [propext, Classical.choice, Quot.sound], but this was NOT independently compiled/replayed by GCL.

## Strongest verified interface
For t increasing divisors define consecutive gaps g_r=d_{r+1}-d_r>0. Cauchy–Schwarz gives 1/(d_j-d_i)<= (1/(j-i)^2)*sum_{r=i}^{j-1}1/g_r. For fixed distance m=j-i, each gap participates in <=m windows. Summing yields T(n)<=H_(t-1)*S(n), where H_(t-1)=sum_{m=1}^{t-1}1/m. This elementary unconditional bound loses ~log t; it does NOT prove Erdős's absolute constant conjecture. An exact fraction Python fixture finite_883_884.py verifies the formula for all n=2..1200, with maximum observed ratio T/(1+S) in that finite range at n=1080, approximately 2.496309. Finite ratios do not establish unboundedness. Larsen's unconditional disproof is externally sourced and accepted in literature, but its full sieve proof and external Lean theorem are not independently GCL-certified.

## Proposed bounded successor task
Input: any strictly increasing finite positive sequence d1<...<dt, exact reciprocal-gap energies and harmonic factor. First target: prove the inequality T<=H_(t-1)S independently (paper lemma or pinned no-sorry Lean), with exact-rational regression n<=1200. Falsification: a strictly increasing finite sequence violating inequality. Second source task: pin the precise Honicky git commit and Mathlib v4.31.0 manifest, rerun lake build and literal #print axioms Erdos884.erdos_884_disproof, compare quantified big-O definitions to the locked FC provider and historic j<t vs j<=t convention. Acceptance: no placeholder/custom axiom, exact theorem negates uniform T=O(1+S) rather than weaker version T=O(S), and actual compiler/axiom readback. Stop before declaring independent GCL Lean certification until both semantic and build gates pass.

## Prerequisites and blocker
Full Larsen primary proof PDF was inaccessible through the available reader, the original Erdős 1998 chapter p177 not directly inspected, and no independent GCL Lean build or axiom output was produced. Therefore formal proof provenance remains to be independently verified even though the mathematics is DISPROVED in the literature; do not reclassify it as an open conjecture.

## Reuse and claim boundary
Used primary Tao 2025 conditional theorem, Larsen 2026 author/detailed public resolution, Honicky external formal repo and maintained status, plus exact finite fractions and elementary harmonic lemma. Offline six-section editorial article and finite fixture are prepared but NOT yet imported/CHAD-published or protected admitted. This source return does not assert novel disproof, independently replayed formal proof, mathematical priority, protected review, protected merge, or public MathJax.
