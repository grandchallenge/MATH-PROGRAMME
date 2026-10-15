# EC-BULK-007 — #1204 admissibility source and greedy indexing

Original https://www.erdosproblems.com/1204 ; return https://github.com/grandchallenge/MATH-PROGRAMME/issues/2475#issuecomment-6188418273.

The admissible $k$-tuple must omit at least one residue modulo every prime. Testing only primes $p\le k$ is sufficient, since a $k$-tuple cannot occupy all residue classes when $p>k$. Both $A(k)=\min a_k$ and $B(k)=\min\frac1k\sum a_i$ are separate minima. The source's quoted greedy rule includes $a_{i+1}>a_{i-1}$, which appears to be an indexing typo; verify Erdős's original statement before changing.

Source claims $(1/2+o(1))k\log k\le A(k)\le(1+o(1))k\log k$, and $A(k)\sim k\log k$ remains open. Independently audit the phase24 exact bounded enumeration $k=2..6$ and prime tuple constructions.

**Source fidelity PENDING.**
