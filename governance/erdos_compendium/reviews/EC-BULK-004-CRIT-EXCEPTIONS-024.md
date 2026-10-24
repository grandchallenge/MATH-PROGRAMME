# EC-BULK-004 — Erdős #488 special-status source and mathematics review

Date: 2026-10-14. Authenticated editorial author/reviewer fyremael. Separate same-identity critical pass, NOT independent-person mathematical peer review. Disposition: **CORRECTED_MULTIPLES_FALSIFIABLE_STATUS_PRESERVED; LITERAL_COMPLEMENT_DISPROVED; FINITE_QA_PASS; PROTECTED_ADMISSION_PENDING**.

## Primary source adjudication

VISUALLY READ Erdős 1961, *Some unsolved problems*, I.27 p.236, https://users.renyi.hu/~p_erdos/1961-22.pdf#page=16: B comprises numbers **not** divisible by any selected a. VISUALLY READ Erdős 1966 Hungarian *Remarks on number theory V*, item 6 printed p.150, https://users.renyi.hu/~p_erdos/1966-20.pdf#page=16: 'melyek legalább egy a-nak többszörösei' means multiples of **at least one** generator. VISUALLY READ Erdős 1980, *A survey of problems in combinatorial number theory*, printed p.112, https://renyi.hu/~p_erdos/1980-03.pdf#page=24: repeats complement wording. The catalogue refers to the 1961 typo but does not establish that 1980 had switched to multiples. The chosen corrected status refers to the **1966 multiples** formulation, NOT to the distinct 1961/1980 text.

## Exact logic and refutation boundary

The corrected conjecture quantifies over finite nonempty positive A and n,m with m>n>=max A; B is the union of multiple sets. Finite n,m,A give a computable integer test  n*F_A(m)<2*m*F_A(n). Hence its global failure would have a finite verifiable counterexample (a Sigma-1 existential arithmetic statement), while its universal truth is a Pi-1 assertion under standard encoding. This does not decide which is true or establish independence from PA/ZFC. The maintained label **FALSIFIABLE** is NOT DISPROVED.

For the literal complement wording take A={2,3,5,7}, n=10, m=20. Exactly one integer <=10 avoids all four divisors (1); five <=20 do (1,11,13,17,19). Therefore 5/20 > 2*(1/10) and the original complement strict inequality is false. In the corrected multiples case the counts are 9 and 15 respectively: 15/20<2*9/10. The false result cannot be transferred to the modern conjecture.

## Constructive arithmetic checks

For A={a}, F_A(x)=floor(x/a). If k=floor(n/a)>=1 and n>=(a), then n<(k+1)a<=2ka, hence F_A(n)/n>1/(2a); F_A(m)/m<=1/a, proving the corrected strict inequality. Taking n=2a-1,m=2a gives density ratio (2a-1)/a→2, demonstrating sharpness of the proposed factor.

Inclusion-exclusion: F_A(x)=sum_{empty != S subseteq A} (-1)^{|S|+1} floor(x/lcm(S)). Exact arithmetic test tests/test_erdos_compendium_0488_falsifiable_boundary.py verifies membership vs inclusion-exclusion on all primitive cores with maximum <=12 at x<=80, compares the corrected inequality on 427167 (A,n,m) cases with max(A)<=n<=40 and n<m<=80, and checks complement-versus-multiple boundary plus redundant-generator and unit cases. All four tests PASSED. The bounded sweep does NOT prove the universal conjecture.

## Formal and editorial boundary

Pinned google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 488.lean, blob d32dda9c6eee99ed0e2e5602deb4a32d61cc7d6d, selects the corrected union-of-multiples definition, nonempty finite A, excludes 0 and 1, exact rational comparison, and theorem by sorry. Excluding 1 is valid as a reduction for a set containing 1 because then B contains all positive integers, so inequality 1<2. 0 is excluded to keep strictly positive divisors. Statement capture is not a proof.

Article governance/erdos_compendium/editorial/0488.md preserves status FALSIFIABLE and UNACCEPTED_DRAFT, with six required sections and three historically different primary wordings. Authenticated issue-bound RESULT/1 https://github.com/grandchallenge/MATH-PROGRAMME/issues/1759#issuecomment-6181186135 has STATUS_CONFLICT disposition to make the competing definitions explicit. No independent mathematical certification, unbounded theorem proof, counterexample to the corrected conjecture, protected admission or public deployed MathJax verification is claimed.

## Bounded successor

Retain two named sets B_A (multiples) and C_A (avoids multiples) and separately type-check their exact counting functions. Prove inclusion-exclusion and the singleton case in the chosen formal environment. Use finite certificate searches solely as falsification attempts; record exact (A,n,m) if a corrected counterexample ever occurs. Never promote a literal historical typo counterexample to DISPROVED of the corrected mathematical statement.
