# Erdős #41: joint shell-pattern exclusions and limits of range packing

**Status:** bounded combinatorial theorem and adversarial no-go result. The genuine M3 finite-window valley remains open. These are necessary conditions for M3, not a solution to #41.

## 1. Simultaneous shell-pattern packing

Partition the positive integers into dyadic shells $I_j=[2^j,2^{j+1})$. Suppose A satisfies M3: unordered three-element multisets supported in A have distinct sums. Set $m_j=|A\cap I_j|$.

A shell pattern p is a three-element multiset of nonnegative shell indices. Write $c_j(p)$ for the number of times j occurs; its multiplicities sum to three. Exactly

$$
w(p)=\prod_{j:c_j(p)>0}\binom{m_j+c_j(p)-1}{c_j(p)}
$$

triples of elements have pattern p. Their sums lie in the integer interval

$$
J(p)=\left[\sum_jc_j(p)2^j,\ \sum_jc_j(p)2^{j+1}-3\right]\cap\mathbb Z.
$$

For any finite collection P of distinct shell patterns, every represented triple sum is different under M3, even across different patterns. Its sum is in the indicated interval. Consequently

$$
\boxed{\sum_{p\in P}w(p)\le\left|\bigcup_{p\in P}J(p)\right|.}\tag{HALL}
$$

This is direct injective counting, not an invocation of the perfect-matching theorem. The union range is counted once and includes patterns with repeated shell labels. A shell-pattern occupancy vector satisfying this inequality is not necessarily realized by an M3 set: the actual arithmetic positions inside the shells are forgotten.

## 2. Strict improvement for two adjacent shells

Let $X=A\cap[L,2L)$ and $Y=A\cap[2L,4L)$, with L a positive power of two and $x=|X|$, $y=|Y|$.

The XXY pattern has $\binom{x+1}{2}y$ triples in $[4L,8L-3]$, an interval of $4L-2$ integers. The XYY pattern has $x\binom{y+1}{2}$ triples in $[5L,10L-3]$, containing $5L-2$ integers. They overlap, and their union is $[4L,10L-3]$, with only $6L-2$ integers. Therefore

$$
\boxed{\binom{x+1}{2}y+x\binom{y+1}{2}
=\frac{xy(x+y+2)}2\le6L-2.}\tag{MIX2}
$$

At $L=64,\ x=y=7$, each pattern individually fits: $196\le254$ and $196\le318$. Even unrestricted packing of all triples from 14 points into the full possible range fits, $\binom{16}{3}=560\le574=9L-2$. But together the two mixed patterns require $392>382=6L-2$ sum positions. Thus this *hypothetical* occupancy vector is excluded by genuine joint cross-pattern counting, although the isolated and global volume tests pass.

## 3. A universal obstruction to all shell-pattern range bounds

We construct a genuine infinite integer set F whose shell occupancy profile obeys **every** (HALL) condition for every finite family of patterns, and even the sharp M3 cubic counting bound, but violates the shell-energy deficit. F is deliberately **not claimed to be M3**.

Put

$$
G=\bigcup_{n\ge2}\{n^4,n^4+1,\dots,n^4+n\}.
$$

For each j outside G, choose the first

$$
m_j=\left\lfloor\frac{2^{\lfloor j/3\rfloor}}{16}\right\rfloor
$$

positive integers in shell j; for j in G choose none. This defines F. Its first nonempty shell has index 12.

**All finite Hall families pass.** Fix any nonempty family P of shell patterns and let K be the largest index appearing in P. Denote the number of selected elements in shells 0 through K by $T_K=\sum_{j=0}^{K}m_j$. Since the geometric ratio $2^{-1/3}<4/5$,

$$
T_K\le\frac{2^{K/3}}{16}\sum_{r\ge0}2^{-r/3}
<\frac5{16}\,2^{K/3}.
$$

For K below 12, all selected occupancies are zero and so is the weight sum. For K at least 12, $2^{K/3}\ge16$; hence

$$
T_K+2\le\left(\frac5{16}+\frac18\right)2^{K/3}
=\frac7{16}2^{K/3}.
$$

Every represented triple with a pattern in P draws three terms from at most $T_K$ selected elements. Thus, using multiset counting,

$$
\sum_{p\in P}w(p)\le\binom{T_K+2}{3}
\le\frac{(T_K+2)^3}{6}<2^K.
$$

At least one interval J(p) in the union includes the largest shell index K. Its interval contains exactly $\sum_jc_j(p)2^j-2\ge2^K$ integer positions, since each of the other two summands contributes at least one. Consequently the union contains at least $2^K$ integers, proving (HALL) for **every** P. The argument does not depend on any chosen positions within the shells.

The **sharp global cubic counting necessary bound** also holds for this F: if N lies in shell K, then

$$
F(N)\le T_K < \frac5{16}2^{K/3}\le\frac5{16}N^{1/3},
$$

and in particular $F(N)^3\le18N$. For K below 12 the count is zero, so there is no edge case.

### An even stronger ungapped counterprofile

Define F0 using the **same** occupancies but without excluding any shells: for every j, take the first $b_j=\lfloor 2^{\lfloor j/3\rfloor}/16\rfloor$ integers of shell j. Its occupancy bound $b_j\le2^{j/3}/16$ is identical, so the preceding argument proves **every** (HALL) inequality, for every finite pattern family, and the sharp cubic counting bound $F0(N)^3\le18N$.

Unlike the gapped profile, **F0 violates the conclusion of Erdős #41**. For any $K\ge13$ and $2^K\le N<2^{K+1}$, the previous shell alone contributes at least

$$
F0(N)\ge b_{K-1}
=2^{\lfloor(K-1)/3\rfloor-4}
\ge2^{K/3-5}.
$$

Consequently

$$
rac{F0(N)}{N^{1/3}}\ge2^{-16/3}>0
\quad	ext{for all }N\ge2^{13}.
$$

So **even the entire family of shell-pattern interval-volume inequalities does not imply the original finite-window valley criterion**. This closes the possibility of proving #41 from those inequalities alone, regardless of how many shell patterns are combined. F0 is not an M3 set. Explicitly, shell 21 contains the three consecutive integers $a=2^{21},a+1,a+2$; then $a+a+(a+2)=a+(a+1)+(a+1)$ is a nontrivial M3 collision. That same collision also occurs in the gapped F, since shell 21 is not excluded.

**Nevertheless its logarithmic shell energy does not vanish.** Outside G and for j at least 12, the occupancy is exactly $2^{\lfloor j/3\rfloor-4}$. According to j modulo three, the energy $m_j^3/2^j$ equals $1/4096,\ 1/8192,\ 1/16384$. The excluded j occupy zero asymptotic proportion of indices: at most $O(\sqrt J)$ of them occur below J. Hence

$$
\lim_{J\to\infty}\frac1J
\sum_{j<J}\frac{m_j^3}{2^j}
=\frac{1+1/2+1/4}{3\cdot4096}
=\frac7{49152}>0.
$$

At the end of the n-th deleted block, j equals $n^4+n$. Every selected element before that gap lies in a shell earlier than $n^4$, and the geometric count estimate is $O(2^{n^4/3})$. With $N=2^{n^4+n+1}-1$, the normalized count is $O(2^{-n/3})$, tending to zero. Thus F has the original Erdős density dips, respects the *sharp* elementary counting bound, and passes all shell-range Hall inequalities, but its shell-energy Cesàro average has a positive limit.

**No-go interpretation:** an argument using only shell cardinalities and enclosing three-sum intervals, no matter how many patterns are packed simultaneously, cannot establish the stronger M3 shell-energy deficit. The actual sumsets and their internal additive structure must be used.

Neither F nor F0 is an M3 set; both have the explicit shell-21 triple collision above. Their occupancy profiles are countermodels to *range-counting proof methods*, not counterexamples to the underlying M3 conjecture.

## 4. A finite realizability gap with explicit collision certificates

The Hall inequalities are not sufficient even at a *single scale*. For $L=2$, take no elements in the first shell $X=[2,4)$, and request $y=3$ elements from $Y=[4,8)=\{4,5,6,7\}$. There are $\binom{5}{3}=10$ possible three-term multisets from the requested three elements, while the allowed sum interval $[12,21]$ contains exactly 10 integers. Every shell-pattern Hall condition is satisfied, but there is **no** three-element M3 subset of Y. All four possible choices have explicit collisions:

- $\{4,5,6\}$: $4+4+6=4+5+5$.
- $\{4,5,7\}$: $4+4+7=5+5+5$.
- $\{4,6,7\}$: $4+7+7=6+6+6$.
- $\{5,6,7\}$: $5+5+7=5+6+6$.

Thus this tiny example proves directly that shell-range volume can be saturated while *every actual placement* violates M3.

A second computationally verified case uses $L=8,\ x=y=3$. All 15 nonempty combinations of its four possible shell-pattern intervals obey (HALL), but exhaustive search checks each of $\binom83\binom{16}3=31,360$ placements without finding an M3 set. The exact deterministic enumerator is in the cross-pattern regression test module; this second result is a **finite computational certificate**, not a new infinite theorem. The first four-case certificate is a complete elementary proof.

## 5. Next exact boundary

The finite-window valley criterion (V) proved in [SHELL_HARDY_AUDIT.md](SHELL_HARDY_AUDIT.md) remains the preferable *equivalent* target. Joint shell-pattern packing (HALL) and (MIX2) yield finite exclusions, but the ungapped F0 proves that **all** range-packing inequalities are consistent with a failure of the original density conclusion; the gapped F also shows that they are consistent with density dips and positive average shell energy. A proof of the original M3 theorem requires joint arithmetic restrictions beyond range volumes: an additive-difference/sumset interaction, a cross-pattern variance bound, or an obstruction specific to extending one M3 set indefinitely.

A bounded next test should distinguish the Hall-feasible occupancy polytope from actual realizability by M3 integers, by exact search over small intervals. Every unsatisfiable finite occupancy target must come with a verifiable collision certificate, not a claim about infinite sequences.

The assertions (HALL), (MIX2), and the universal range-packing no-go are elementary written proofs, not a claim of complete Lean formalization or new published mathematical priority. Erdős #41 remains OPEN.

## Source context

- Martin Helm, *On the Distribution of B3-Sequences* (1996), https://www.sciencedirect.com/science/article/pii/S0022314X96900694, defines repeated-summand B3 sequences and supplies existing global distribution restrictions.
- Javier Cilleruelo, *New Upper Bounds for Finite Bh Sequences* (2001), https://www.sciencedirect.com/science/article/pii/S0001870800919613, is relevant finite extremal context. The elementary Hall counting constraints here are not claimed as previously unknown results.
- GCL's earlier [SHELL_HARDY_AUDIT.md](SHELL_HARDY_AUDIT.md) establishes the exact valley criterion and the weaker gapped packing-only example.
