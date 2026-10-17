# EC-BULK-004 — #473 reported-solution source exception review

Receipt: EC-BULK-004-SOURCE-EXCEPTION-015  
Observed: 2026-10-14  
Accountable authenticated identity: fyremael  
Authority: documentary adversarial source check, not independent human review, Lean proof certification, or protected editorial admission.

## Primary-statement consistency

Erdős–Graham (1980), printed p.94, PDF p.89 (zero-based), explicitly states three DIFFERENT questions: (A) existence of an infinite permutation of all positive integers with every adjacent sum prime, reported solved by Odlyzko; (B) whether Watts's greedy sequence a₁=1, a_(n+1)=least unused positive x with a_n+x prime covers every positive integer; and (C) whether all primes occur among this greedy sequence's adjacent sums.

A second archival primary historical text, P. Erdős, R. Freud and N. Hegyvári, “Some results in combinatorial number theory,” *Colloq. Math. Soc. János Bolyai* 34 (1981 conference), archival PDF https://renyi.hu/~p_erdos/1984-23.pdf p.4, repeats attribution to Odlyzko. It cites the earlier 1980 monograph, **not Odlyzko's original proof**. Maintained https://www.erdosproblems.com/473 marks only (A) PROVED and reports (C) refuted by omitted primes 197 and 199. The one-sided-versus-two-sided distinction in Li–Shang–Zhang 2025 is preserved.

## Independent mathematical critical check

Under the greedy rule there is ALWAYS some possible next value: choose an arbitrarily large prime p and set x=p−a_n. With finitely many values already used, sufficiently large p ensures x>0 and unused. This only proves **infinite length**, not that all integers appear.

Using independent exact trial-division primality at all steps, the first 100 greedy values begin 1,2,3,4,7,6,5,8,9,10,13,16,15,14,17,12,11,18,19,22,21,20,23,24,29. The first 99 terms form exactly the set {1,…,99}; a₉₉=89 and a₁₀₀=102. For each 1≤k≤99, the exact adjacent sum a_k+a_(k+1) is prime and differs from 197 and 199. For all k≥100 both terms are unused positive integers ≥100, hence their sum is ≥200. This establishes **without an unbounded computation** that the greedy sequence NEVER has adjacent sum 197 or 199. The arithmetic obstruction (C) is therefore fully explained, but (B) remains unresolved.

The committed test tests/test_erdos_compendium_0473_prime_sums.py independently replays every greedy MINIMAL x, prime sum and unique-use claim; it checks the full-coverage cutoff and the 197/199 exclusion and has three successful exact finite tests. A four-element prime-sum permutation [1,4,3,2] gives a separate small illustration but no all-n theorem.

## Evidence and decision

Authenticated issue-bound source audit: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1743#issuecomment-6167157265, author fyremael, SHA-256 of LF-normalized comment body dad526e005d04b59ee1901d61e9ec7c9a9c753d1864662cd381d507986bce0e1, disposition PARTIAL.

Original Odlyzko construction/proof is not located. Therefore **no source-locked manuscript or certified proof of (A)** follows from this record. A scholarly compendium article may be produced later after original-source recovery or explicitly labelled historical-proof secondary evidence, with these ambiguities preserved.

Disposition: SOURCE_EXCEPTION_REVIEWED_PROOF_PROVENANCE_OPEN. No MathCert, protected production merge, deterministic final sample substitution, new theorem priority, live-browser rendering, or V2 editorial admission.
