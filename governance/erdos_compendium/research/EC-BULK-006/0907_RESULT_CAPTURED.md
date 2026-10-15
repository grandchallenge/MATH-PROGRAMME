RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0907-S01
PROBLEM_ID: 907
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For f:R->R arbitrary WITHOUT assuming measurable or continuous, suppose for every positive real t>0 the translation difference Delta_t f(x)=f(x+t)-f(x) is continuous as a function of x over all R. Show f=g+H for some continuous g and additive H(x+y)=H(x)+H(y) on ALL real arguments. Positive-only condition is equivalent to for all real translations: Delta_{-t}f(x)=-Delta_t f(x-t) for t>0, Delta_0=0. Additive does NOT imply continuous; uniqueness only modulo continuous linear map x->cx. Not same as #908 measurable differences with a residual almost-invariant term.

## Dated status and primary evidence
Original Erdős early-1950s conjecture cited [Er81b,p31] [Er82e]. FULL PRIMARY N.G. de Bruijn, 'Functions whose differences belong to a given class', Nieuw Archief voor Wiskunde, ser2 vol23 (1951)194–218, publisher PDF university https://pure.tue.nl/ws/files/4316577/597498.pdf, university record https://research.tue.nl/en/publications/functions-whose-differences-belong-to-a-given-class/. Original printed page194 Theorem 1.1 visually independently checked Oct15 2026: if Delta_h f is continuous for EACH h, then f=g+H continuous g/additive H; paper explicitly credits Erdős conjecture, discusses earlier Mary L Boas/R P Boas Jr bounded-on-positive-measure theorem. Printed pp196–197 also inspected: key bounded-additivity stability Theorem1.2, periodic-case reduction Lemma1.1 and interval variant Theorem1.3, should NOT merge hypotheses. Maintained https://www.erdosproblems.com/907 Apr7 2026 labels PROVED (LEAN) and report Aristotle formalization from Pietro Monticone, yet same catalogue external field 'Formalised statement? No', exact Lean build/axioms not independently rechecked GCL. This is mathematical PROVED by full primary 1951 paper regardless newer Lean metadata inconsistency. Frozen teorth/erdosproblems source was PROVED (current source confirms).

## Strongest verified interface
Elementary positive->all-translation lemma above, and uniqueness: if f=g+H=g'+H', then H-H'=g'-g simultaneously continuous and additive, so equals cx for a real c. Exact noncontinuous example: define on Q(sqrt2) H(a+b sqrt2)=b rational, H(1)=0,H(sqrt2)=1 so not scalar identity; extend Q-basis of Q(sqrt2) to Hamel basis of R to obtain additive noncontinuous H. Let g(x)=x² and f=g+H, then Delta_t f(x)=2tx+t²+H(t) for every real t, continuous in x while f discontinuous. CHAD finite_906_907.py/json checks 392 exact difference identities and 1568 commuting mixed-difference identities on rational quadratic field, no floats; also checks H(1)=0/H(sqrt2)=1. Tests are proof regressions for example, not independent full 1951 de Bruijn proof or kernel replay.

## Proposed bounded successor task
First formalize exact positive->negative translation reduction and two-decomposition uniqueness modulo continuous linear maps on R, using standard continuous-Cauchy lemma; inputs arbitrary f and additive H, no measurable assumptions. Acceptance complete independent paper proofs or pinned no-sorry Lean4 compile plus literal axiom report, 392+1568 exact finite reproductions. Falsify with negative-shift formula mismatch, unwarranted continuity assumption on H, or distinct decompositions not related by cx. Then independent original de Bruijn 1951 §2 reconstruction including periodic lemma, no assumption on f measurability, exact semantic match of April2026 external Aristotle formal proof, pinned Lean deps and axioms. Stop before falsely claiming a GCL independently certified full theorem.

## Prerequisites and blocker
Full 1951 de Bruijn 25-page proof not reconstructed line by line; inspected original printed pp194–197 Theorem1.1, not all 25 pages. Historical Er81b/Er82e images not individually checked; modern April2026 Aristotle link and exact source not independently compiled. No GCL Lean certificate or independent mathematical review/admission.

## Reuse and claim boundary
Primary de Bruijn published theorem and university publisher PDF visually checked, maintained catalogue, independent elementary translation/uniqueness proof, exact Hamel-basis example and finite arithmetic fixture. No novel universal proof, not #908, no protected main merge, public browser verification or V2 admission.
