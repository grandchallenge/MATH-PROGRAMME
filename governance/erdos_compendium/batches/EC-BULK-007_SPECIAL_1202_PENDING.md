# EC-BULK-007 — #1202 newer sieve counterexample and unused eta

**Primary source proof-fidelity and formal statement binding PENDING.**

Original https://www.erdosproblems.com/1202, authenticated return https://github.com/grandchallenge/MATH-PROGRAMME/issues/2473#issuecomment-6188417185.

The displayed statement quantifies $\epsilon,\eta>0$, yet the conclusion only bounds the survivor count by $\epsilon n$ and never uses $\eta$. Do not silently invent a dependence. It quantifies over EVERY set of $k$ primes and every selection of exactly $(p_i-1)/2$ excluded residues, so a random-sieve heuristic does not prove it.

The maintained 2026 Price/GPT-5.4 Pro counterexample is reported to preserve long arithmetic progressions under excluded interval residues with many prime moduli and survivor proportion near $1/2$. Before certifying DISPROVED as an independently reviewed theorem, verify its exact asymptotic range, epsilon/eta parameters, size of prime families and the long-survivor set. Separately review the previously known large-sieve partial result in a more restricted modulus regime.

The phase24 finite fixture enumerates $1050$ assignments for $n=60$, primes $3,5,7$, and survivor counts $11$–$17$. It cannot disprove a statement with arbitrarily large $k$. **Source review PENDING.**
