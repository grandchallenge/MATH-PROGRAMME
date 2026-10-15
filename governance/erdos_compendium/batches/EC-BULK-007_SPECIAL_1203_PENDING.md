# EC-BULK-007 — #1203 undefined lower k domain and maximum semantics

Original https://www.erdosproblems.com/1203 ; authenticated return https://github.com/grandchallenge/MATH-PROGRAMME/issues/2474#issuecomment-6188417714.

The printed $F(n)=\max_k\omega(n+k)\log\log k/\log k$ has an undefined $k=1$ term and a negative factor at $k=2$. It must specify $k\ge3$ or other admissible range and whether a **maximum** over all $k$ is known to exist versus only a supremum. Check original Erdős (1980), p.107, and current formalization before source normalization.

Phase24 computes **only partial maxima for $3\le k\le100$** at $n=100,1000,10000$, approximately 1.103, 1.465, 1.811. Those are bounded examples and not proof that $F(n)\to\infty$.

**Source fidelity PENDING; general problem OPEN.**
