RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0880-S01
PROBLEM_ID: 880
DISPOSITION: SOURCE_LOCK_READY
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
An infinite A of nonnegative integers is an additive basis of order h if every sufficiently large natural number is representable as the sum of AT MOST h members, repeated entries permitted. Let B_h(A) be sums of AT MOST h PAIRWISE DISTINCT members. Burr–Erdős ask whether B_h(A) must have BOUNDED eventual consecutive gaps. The at-most versus exactly h distinction and the distinction between repeated and restricted sums are substantive; these are not ordinary sum-free predicates.

## Dated status and primary evidence
Hegyvári, Hennecart and Plagne, 'Answer to a Question by Burr and Erdős on Restricted Addition, and Related Results', Combinatorics Probability and Computing 16 (2007) 747–756, DOI 10.1017/S0963548306008224, original author PDF https://www.cmls.polytechnique.fr/perso/plagne/Erdos-Burr.pdf. Theorem 1 on printed p2 and proof pp4–5 visually inspected October 14, 2026. Part (i) proves that for every additive basis of order 2 the restricted at-most-two sums eventually have gaps at most 2. Part (ii) supplies an explicit order-h basis for EACH h>=3 for which the gaps between successive restricted at-most-h sums are unbounded. Thus the conjectured universal bounded-gap assertion is TRUE at order 2 and FALSE for all orders >=3. Maintained https://www.erdosproblems.com/880 labels PROVED as a decided question, not universal YES; frozen teorth catalogue @536408716724a2402bdfa7c1d764bf83d64a8c89 likewise PROVED. No GCL Lean kernel replay.

## Strongest verified interface
An odd m cannot have a repeated representation m=2a. Therefore if an additive order-two basis represents every sufficiently large odd m as a+b, that representation has a!=b, so every sufficiently large odd number belongs to B_2(A). Such restricted sums have gaps <=2 eventually. Independent exact finite fixture checks this parity implication for each of 512 subsets of [1,9]. For h3 and h4, direct finite tests of the first block of the primary 2007 construction give complete ordinary h-fold representation on [3,54) and [4,192), respectively, but no restricted values in [45,53] and [144,191] respectively. These are stage-specific checks, NOT the infinite proof; primary paper's recursive growth shows gaps unbounded across all stages.

## Proposed bounded successor task
Input h=2 finite parity representation predicate, plus explicit first-block formula from Hegyvári–Hennecart–Plagne and recorded fixture. Target: formalize the universal odd-target order-two lemma and check its equivalence to restricted at-most-two sums. Separately source-lock induction connecting the first h>=3 block and all subsequent blocks, including interval endpoints and overlap cases. Acceptance: reviewed finite proof or no-sorry Lean kernel build for parity lemma, 512-case exact regression, and independent source-check of infinite recursion; falsify with a large odd target whose only two-summand representations repeat an element, or a false first-stage coverage assertion. Stop before claiming the full published infinite negative result independently proved.

## Prerequisites and blocker
The complete 2007 recursive proof was read but not independently formalized. No protected source-provider Lean artifact, proof-replay receipt or independent adjudication, and this source audit does not authorize an independent Solve campaign.

## Reuse and claim boundary
Reused the primary 2007 theorem with explicit order-dependent split and source-tested finite construction. No original novelty, formal certification, protected editorial review/merge, or live deployed MathJax check claimed.
