RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0910-S01
PROBLEM_ID: 910
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
TWO connected Euclidean-subspace questions: (A) must every nondegenerate connected subset M of R^n contain a connected nonpoint N subset M NOT HOMEOMORPHIC to M? (B) for n>=2 must every connected subset of R^n have STRICTLY MORE THAN continuum=2^aleph0 many distinct connected subsets? Maintained https://www.erdosproblems.com/910 DISPROVED for both by M.E. Rudin 1958, importantly CONDITIONAL ON CONTINUUM HYPOTHESIS (CH). This is not an unconditional ZFC resolution; do not collapse proper subset versus different homeomorphism type or nondegenerate versus singleton.

## Dated status and primary evidence
Original P. Erdős 'Some remarks on connected sets' 1944 https://users.renyi.hu/~p_erdos/1944-06.pdf raises proper connected subset not homeomorphic. M. E. Rudin, 'A connected subset of the plane', Fundamenta Mathematicae 46 (1958)15–24 DOI10.4064/fm-46-1-15-24, original journal issue https://www.impan.pl/en/publishing-house/journals-and-series/fundamenta-mathematicae/all/46/1, full first-page theorem quoted verbatim in published abstract at https://celebratio.org/Rudin_Mary/article/236/. Under CH, construct NONDEGENERATE CONNECTED M subset Euclidean plane such that for EVERY nondegenerate connected N subset M, the complement M\N is AT MOST COUNTABLE. Source outline: indecomposable continuum I, transversal meets each composant at most one point, CH transfinite induction. Rudin says this disproves Erdős 1944 conjecture, and current catalogue attributes BOTH negative answers to her. Complete 1958 proof (especially first question homeomorphism classification) NOT independently reproduced GCL and original PDF fetch failed, so do not infer all connected N are homeomorphic from co-countability alone.

## Strongest verified interface
Independent cardinal deduction: for fixed M subset R², |M|<=continuum. Rudin condition maps each nondegenerate connected N injectively to D=M\N, which is countable. |[M]^{<=aleph0}|<=continuum^aleph0=(2^aleph0)^aleph0=continuum by ZFC cardinal exponent rules. Including at most continuum many singleton connected subsets gives at most continuum many connected subsets total; refutes B for M under CH. Count arithmetic itself does NOT require CH, but existence of Rudin M DOES. GCL exact finite_910_911.py/json checks finite complement counting for m2..12 and complement sizes d<=3 matches binomial(m,d). This does not construct topological M. The published abstract's co-countable theorem does NOT logically alone show every N homeomorphic to M: full first-question source proof remains a separate fidelity gate.

## Proposed bounded successor task
Formalize the countable-complement cardinality lemma in ZFC with correct injection, finite versus countably infinite omissions and continuum exponent identity; acceptance complete elementary proof or pinned no-sorry Lean with literal axiom report and exact finite binomial checks. Independently source-review Rudin1958 all printed pp15–24, prove connectivity of transfinite constructed M, track CH exactly, and resolve whether first not-homeomorphic issue follows from further source structure rather than co-countability by itself. Falsify by one purported connected N whose complement is uncountable or failed CH enumeration or unjustified homeomorphism conclusion. Do not claim unconditional construction.

## Prerequisites and blocker
Full 1958 primary PDF proof and Erdős 1944 contextual pages not independently page-by-page replayed, source 1958 article explicitly CH conditional. No GCL kernel build, independent math adjudication, protected main merge or deployed browser MathJax.

## Reuse and claim boundary
Uses Rudin 1958 CH-conditional published theorem and catalogue's interpretation of two Erdős questions, independently proved only cardinal bound and finite counting regression. Neither new topology theorem nor ZFC independence classification is claimed. STATUS: conditional disproof in literature, review exception on direct homeomorphism derivation.
