# EC-BULK-004 — Erdős #536–537 source-fidelity and exact-fixture review

Observed 2026-10-16 UTC; authenticated actor fyremael. SAME-OPERATOR source and exact finite mathematics QA, NOT independently approved research, GCL Lean kernel receipt or protected editorial admission.

## #536 — OPEN LCM triangle positive-density question

Original Erdős *On a Problem in Elementary Number Theory and a Combinatorial Problem*, Math. Comput. 18 (1964) 644–646, complete original PDF https://www.renyi.hu/~p_erdos/1964-10.pdf downloaded CHAD /tmp/ec004-er1964-0534-0535.pdf, p646 directly read. Erdős 1973, *Problems and Results on Combinatorial Number Theory*, A Survey of Combinatorial Theory Chapter12 p124, original https://www.renyi.hu/~p_erdos/1973-21.pdf#page=8 downloaded and read CHAD /tmp/ec004-er1973-0534-0535.pdf index7. For N, f(N)=largest |A|⊆[1,N] avoiding three DISTINCT a,b,c with lcm(a,b)=lcm(a,c)=lcm(b,c), ask f(N)=o(N). Four-element variant can have linear-size avoiding families; Ruzsa's disproof of stronger #537 DOES NOT negate weaker #536.

For prime p, max(v_p(a),v_p(b))=max(v_p(a),v_p(c))=max(v_p(b),v_p(c)) iff maximum of three valuations occurs at least twice. This exact equivalence characterizes an LCM triangle prime by prime. (6,10,15) bad (all LCM30), (6,10,14) allowed (LCM30,42,70); latter is gcd-bad for distinct #535. Disjoint prime-bin products with exactly one prime per bin cannot make a triangle of DISTINCT integers, but a finite family is NOT positive density evidence.

Maintained https://www.erdosproblems.com/536 and /history/536 OPEN, Abbott–Gardner (1967) f(N)≥(1−o(1))N loglogN/logN and community Desmond Weisenberg 2025-12-21 upper (221/225+o(1))N and enhanced lower involving N(loglogN)^ω/logN. Those latter community proof claims have NOT been independently reconstructed and are not treated as peer-reviewed new formal results. Protected FC-GDM-85F86371 FormalConjectures/ErdosProblems/536.lean blob 2934181f7d8a7167b7d0540ee8d4c55ec6e234ed directly inspected, statement includes # {a,b,c}=3, research open; answer(sorry) and theorem by sorry, NO kernel proof.

tests/test_erdos_compendium_0536_lcm_triangles.py FOUR PASS: exhaustive all unordered distinct triples from 1..100 valuation / gcd identities and exact LCM, good/bad examples, two independent algorithms for finite maximum avoiding size n≤12, and disjoint prime-bin construction. These checks do not imply f(N)=o(N). Authenticated source issue https://github.com/grandchallenge/MATH-PROGRAMME/issues/1807#issuecomment-6227941976 BOUNDED_TASK_DESIGNED, preserved OPEN.

## #537 — DISPROVED by Ruzsa positive-density separated-prime construction

Original Erdős 1973 printed p124 (same direct source above) **already** attributes to teenage Imre Ruzsa the dense construction refuting whether every positive-density A⊆[1,N] yields m=p1a1=p2a2=p3a3 with distinct primes p_i. Let B consist of squarefree a=∏q_i with q_(i+1)>2q_i. Erdős states B has positive natural density (separate analytical input). Set A_N=B∩(N/2,N]; therefore |A_N|≫N for all large N. If p_i a_i=m with all p_i different and a_i∈A_N, reorder a2>a3 and p2<p3. Then 1<p3/p2=a2/a3<2. But p2,p3 both divide a1∈B, so p3/p2>2, contradiction. This proves at most TWO prime-multiple representations for any m and every finite N; positivity of density is not proved by enumeration. Modern maintained https://www.erdosproblems.com/537 and pinned teorth@536408716724a2402bdfa7c1d764bf83d64a8c89 classify DISPROVED (LEAN). Feb7 2026 forum cites external Aristotle Lean proof via Boris Alexeev, NOT acquired/compiled exact-head by GCL. Protected FC-GDM-85F86371 has no 537.lean, NO local Lean kernel certification or invented primary Ruzsa journal attribution.

Logical distinction: (12,20,15) has equal pairwise LCM60 but quotients {5,3,4} contain composite4, so a generic LCM triangle does NOT provide three distinct prime multiples. Ruzsa refutes stronger #537 without settling #536.

tests/test_erdos_compendium_0537_ruzsa_prime_gaps.py FOUR PASS: squarefree/gap predicates, all admissible A_N for N=50,100,200,400, prime-multiple collision checks up to prime cutoff500 by two algorithms, pairwise ratio constraints, and LCM vs prime-quotient logical example. Test initially contained incorrect example claim 2·5·11 fails gap (it actually passes), corrected to 2·5·7; initial composite-quotient example corrected to (12,20,15). Reran both focused suites, eight PASS. Finite bounded prime cutoff does not certify positive density or all prime multipliers, whose general contradiction is separately explained.

Authenticated source issue https://github.com/grandchallenge/MATH-PROGRAMME/issues/1808#issuecomment-6227942142 SOURCE_LOCK_READY, preserved DISPROVED.

## Admission and provenance boundary

Both articles six substantive sections, UNACCEPTED_DRAFT. Original source comments must be read back with SHA256 and manuscript raw/stripped hashes recorded in canonical 200-slot manifest. Full cohort test suite, strict MkDocs, real local Chromium MathJax and exact remote branch SHA verification precede closure. No independent proof acceptance, novel theorem, external Lean kernel replay, protected main merge, or public deployed render claimed.
