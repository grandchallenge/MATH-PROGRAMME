RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0897-S01
PROBLEM_ID: 897
DISPOSITION: SOURCE_LOCK_READY
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let additive f:positive integers->real have f(ab)=f(a)+f(b) for gcd(a,b)=1, f(1)=0. Assume unbounded normalized prime-power limsup limsup_{p PRIME,k>=1} f(p^k)/log(p^k)=+infinity. Erdős–Wirsing ask whether (A) limsup_{n->inf}(f(n+1)-f(n))/log n=+infinity and/or (B) limsup_{n->inf}f(n+1)/f(n)=+infinity. Ratios require f(n)!=0 eventually, or precise extended-real convention; source proof must lock this. Both purported implications FALSE in literature, the normalized difference limsup may equal 0. No claim that a zero limsup is possible for the ratio, which is a distinct quantity and may be positive.

## Dated status and primary evidence
Original Er72 p85 (not directly page-image inspected). E. Wirsing, 'A characterization of log n as an additive arithmetic function', Symposia Mathematica (1970), pp45–57, proves bounded consecutive differences imply f(n)=c log n + O(1). E. Wirsing, 'Additive and completely additive functions with restricted growth', Recent Progress in Analytic Number Theory, vol2 (Durham1979 proceedings published 1981), pp231–280, primary HISTORICAL counterexample; catalogue https://www.erdosproblems.com/897 states Wirsing credits its insight to Erdős, and describes prime-power weights f(q)=g(q)log q for SUFFICIENTLY slowly growing g. The full Wirsing 1981 50-page argument and allowed g not independently reproduced in GCL. Maintained #897 edited Apr1 2026 labels DISPROVED (LEAN) both parts. Public upstream Google DeepMind Formal Conjectures FormalConjectures/ErdosProblems/897.lean metadata links external L. Wu/Aristotle Lean4 v4.24.0 reconstruction https://github.com/plby/lean-proofs/blob/main/src/v4.24.0/ErdosProblems/Erdos897.lean and Archivara 2025 rediscovery; upstream theorem bodies themselves contain sorry. The link is NOT an internally compiled GCL proof and no independent kernel/axiom audit occurred. Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 DISPROVED, formal status reported externally, not protected GCL proof.

## Strongest verified interface
For arbitrary real weights w(p,e) assigned to prime powers with e>=1, define f(1)=0 and f(n)=sum_{p^e || n}w(p,e). Unique factorization means coprime a,b have disjoint prime-power contributions, so f(ab)=f(a)+f(b); no assumption w(p,e) linear in e (do not confuse with complete additivity). Concrete toy w(p,e)=e(e+1) yields f(2^k)=k(k+1), hence f(2^k)/log(2^k)=(k+1)/log2->infinity, satisfying original premise. CHAD finite_896_897.py/json independently checks f(ab)=f(a)+f(b) for EVERY coprime a,b in [1,150], growth formula k=1..32, adjacent differences n=2..2000 range -102..104. Critically this toy DOES NOT counterexample (A) or (B): no global neighboring-bound argument. The external Wirsing slow-growth function, not toy, is necessary for disproof.

## Proposed bounded successor task
First formalize prime-power extension w->additive f, f(1)=0, with exact positive exponent support and unique factorization. Acceptance elementary reviewed proof or pinned no-sorry Lean compile with literal axiom report and exact finite coprime matrix 150x150 and prime-power k<=32. Falsify by coprime pair failing additivity or wrong support/exponent. Second obtain original Wirsing 1981 page and exact g construction, rederive limit control for ALL sufficiently large neighbors and map each to upstream Aristotle/L. Wu precise statement, denominator f(n) restrictions and pinned Mathlib dependencies; independently run lean build and literal axioms. STOP without claiming external reported Lean result independently checked or ratio limsup zero.

## Prerequisites and blocker
Primary Er72 p85 and Wirsing 1981 detailed g lemma not source-page reviewed; external Lean proof not downloaded, built, or axiom-replayed in CHAD. Main upstream theorem marked sorry despite external formal_proof metadata. Historic (A) negative and (B) negative credited to Wirsing, but no new GCL solution or independent review.

## Reuse and claim boundary
Used historical Wirsing bibliographic metadata, current maintained statement and external Lean source, independently proved elementary unique-factorization extension, exact bounded integer verification. No claim a toy f disproves #897, no new asymptotic counterexample, protected main merge, Lean certificate, live deployed browser MathJax or V2 editorial admission.
