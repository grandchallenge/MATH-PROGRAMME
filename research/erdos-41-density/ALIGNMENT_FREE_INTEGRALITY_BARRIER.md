# Erdős #41 — Arbitrary-centre collision capacity and the all-scale fractional barrier

**17 October 2026. Status: exact finite and analytic theorems proved below. The original persistent-density question remains OPEN.** This note is a bounded successor to the extension-capacity work in PR #2739. It does not assert that a full B3 set exists at positive critical lower density, and it does not claim independent mathematical certification.

## Executive research finding

The equally spaced-centre assumption **can be removed** from the block-interaction theorem: every family of actual occupied intervals obeys an exact *sliding-window* capacity inequality for all near-coincident sums of their arbitrary starting positions. Also, the within-block difference spectra are globally disjoint, regardless of the block locations.

**However these two supplies of first-moment arithmetic capacity do not produce a universal critical-density dip by themselves.** A single explicit fractional Bernoulli profile, \(p_n=\tfrac14 n^{-2/3}\), has positive critical expected mass at every prefix, while satisfying **every individual pair-difference and repeated-summand triple-sum expected packing inequality simultaneously, at every scale**. This gives a rigorous all-resolution obstruction to any argument that only rearranges those first-moment inequalities. It is NOT a genuine B3 construction.

The remaining mathematical target is an **integral collision/rounding loss** on actual 0-1 sets or a genuinely stronger, dependent-cohort condition (e.g. reciprocal signed-code incompatibility), not another equality of coarse sum indices.

## 1. No alignment assumption: exact moving-window triple capacity

Let A be a genuine repeated-summand B3 set. Fix an integer width R>=1, and let I_i=[b_i,b_i+R-1] be **pairwise disjoint** integer intervals with completely arbitrary integer starts b_i (not necessarily equally spaced). Put A_i=A∩I_i and m_i=|A_i|. For every unordered index triple i<=j<=k define its actual number of repeated-summand selections

$$
w(i,j,k)=
\begin{cases}
m_i m_j m_k,&i<j<k,\\
\binom{m_i+1}{2}m_k,&i=j<k,\\
m_i\binom{m_j+1}{2},&i<j=k,\\
\binom{m_i+2}{3},&i=j=k.
\end{cases}
$$

Here indices are ordered by the order of the intervals, and empty bins have zero occupancy. The contribution of this pattern consists of w(i,j,k) distinct *actual* B3 triples; its sums lie in the short interval

$$
[b_i+b_j+b_k,\ b_i+b_j+b_k+3R-3].
$$

**Theorem A (arbitrary-centre sliding-window Hall inequality).** For every pair of integers S and D>=0,

$$
\boxed{
\sum_{\substack{i\le j\le k\\
 S\le b_i+b_j+b_k\le S+D}}
w(i,j,k)\ \le\ D+3R-2.
}\tag{MOVING-TRIPLE-HALL}
$$

**Proof.** Distinct index patterns cannot represent the same unordered triple of actual elements, because the intervals are disjoint. Within each pattern, the stated combinatorial weight counts exactly the distinct selected unordered triples, including repetitions. The B3 property assigns distinct integer sums to ALL of them. Every counted sum is inside [S,S+D+3R-3], which has D+3R-2 integer positions. Thus the inequality follows without assumptions on the starts or on the locations of points within their bins. QED.

**Corollary (robust approximate B3[g] centres).** Suppose a subfamily of bins is m-heavy, meaning each has at least m>=c R^(1/3) genuine points for some c>0. Let \(\mathcal N_{S,D}\) count **distinct three-bin patterns i<j<k** from the heavy subfamily whose base-sum starts belong to [S,S+D]. Then

$$
\boxed{
\mathcal N_{S,D}\le
\frac{D+3R-2}{m^3}
\le\frac{D/R+3}{c^3}.
}\tag{APPROXIMATE-B3-G}
$$

Thus arbitrarily positioned heavy bin starts have bounded multiplicity of near-coincident three-fold sums at resolution R. The equally spaced arithmetic-run theorem is only one special case; the general collision budget does not depend on that alignment.

**Independent second resource (nonzero pair differences):**

$$
\boxed{
\sum_i\binom{m_i}{2}\le R-1.
}\tag{GLOBAL-INTERNAL-DIFFERENCES}
$$

For each i, all positive differences between distinct points in A_i lie in [1,R-1]; B3 implies B2, so no nonzero positive difference may occur twice, even between different bins. This is true at ANY separation of the bins. If h bins have at least m>=2 points, then h<=2(R-1)/(m(m-1)). At critical local occupancy m>=c R^(1/3), this is order c^(-2)R^(1/3). These constraints must be respected simultaneously with the moving triple Hall inequalities. Neither establishes an absolute upper bound on the number of singly occupied bins.

### Theorem A2: a density-sensitive *delocalization* consequence, regardless of block alignment

The globally distinct within-bin B2 differences do more than restrict the number of heavy blocks. Combined with the local B3 upper bound, they prove that **a positive-critical-density B3 prefix cannot place a positive fraction of its elements into short blocks that are themselves critically dense**.

Let A_N=A∩[1,N] be any finite B3 prefix. Partition [1,N] into disjoint consecutive length-R integer bins, extending the last bin beyond N if necessary. Fix an arbitrary real epsilon>0 and call a bin *heavy* when its occupancy m_i satisfies

$
m_i\ge \varepsilon R^{1/3}\quad\text{and}\quad m_i\ge2.
$

Write H_R(A_N) for the total number of actual elements in the union of those heavy bins.

**Theorem A2 (unconditional alignment-free heavy-bin mass bound):**

$
\boxed{
H_R(A_N)\le\frac{4\cdot18^{1/3}}{\varepsilon^2}R^{2/3}.
}\tag{HEAVY-BIN-DELLOCALIZATION}
$

**Proof.** Every actual B3 subset of an integer interval of length R has at most (18R)^(1/3) elements: its binom(m+2,3) different triple sums lie in an interval of 3R-2 integers. For each heavy bin with m_i>=2 we have binom(m_i,2)>=m_i²/4>=epsilon² R^(2/3)/4. By global pair-difference uniqueness, the sum over ALL bins of binom(m_i,2) is at most R−1. Thus at most 4 epsilon^(−2) R^(1/3) bins can be heavy. Multiply by the local (18R)^(1/3) cap. QED.

**Conditional persistent-density corollary.** If hypothetically \(A(N)\ge cN^{1/3}\) for some fixed c>0 at a sequence of N values, then, for any R=R(N) with R>=2 and R=o(N^(1/2)), the proportion of points in bins containing >=epsilon R^(1/3) elements tends to zero:

$
\boxed{
\frac{H_R(A_N)}{A(N)}
\le\frac{4\cdot18^{1/3}}{c\varepsilon^2}
\left(\frac{R^2}{N}\right)^{1/3}
\longrightarrow0.
}\tag{FORCED-LOCAL-DISPERSION}
$

The maximum of each non-heavy bin need not be one; it is simply subcritical compared to epsilon R^(1/3). The result is about the **actual original integer points**, not the fractional profile of section 2.

**Interpretation for the remaining proof.** The former plan to extract multiple densely populated short cohorts at every scale is not forced by critical *global* density; indeed this bound demonstrates that such cohorts must carry asymptotically **negligible** total mass whenever their width R is smaller than the square-root scale of the enclosing horizon N. Any putative critical-density B3 set must instead exhibit **strong local dispersion** over sub-square-root windows. The critical fractional profile n^(−2/3) provides a first-moment *model* of a similarly spread-out configuration, but not a genuine collision-free set. A proof of Erdős #41 must rule out this dispersed **integral** regime, not merely dense arithmetic runs of short blocks.

## 2. A simultaneous all-resolution fractional obstruction

Let

$$
\boxed{p_n=\frac14 n^{-2/3}\quad(n=1,2,\dots).}\tag{FRACTIONAL-PROFILE}
$$

These numbers are probabilities strictly between 0 and 1, **not** a B3 indicator. Their total mass at every prefix is critical:

$$
\boxed{
\sum_{n=1}^N p_n\ge\frac14 N^{1/3}.
}\tag{FRACTIONAL-CRITICAL}
$$

For each nonzero positive lag d the pair-difference expectation is bounded independently of d:

$$
\boxed{
D_p(d)=\sum_{n\ge1}p_np_{n+d}
\le\frac1{16}\sum_{n\ge1}n^{-4/3}
\le\frac14.
}\tag{FRACTIONAL-DIFFERENCES}
$$

For each integer s>=3 define the **correct Bernoulli expected count of unordered triple selections allowing repetitions**:

$$
U_p(s)=
\sum_{\substack{1\le a\le b\le c\\a+b+c=s}}
\prod_{v\in\{a,b,c\}}p_v.
$$

IMPORTANT: when a vertex repeats in a triple, it is selected only ONCE by a Bernoulli variable. Its contribution is p_a rather than p_a^3 for a=a=a, and p_a p_b rather than p_a²p_b for a=a!=b. This definition is stronger/more faithful than merely evaluating the cubic convolution \((p*p*p)(s)\).

**Theorem B (all-sum fractional capacity including repetitions).** For every s>=3,

$$
\boxed{
U_p(s)\le
\frac{35}{6\cdot64}+\frac{4}{16}+\frac14
<\frac35<1.
}\tag{FRACTIONAL-TRIPLE-SUMS}
$$

**Proof with explicit constants.** Write a_n=n^(-2/3). The elementary integral comparison \(\sum_{j=1}^M j^{-\beta}\le M^{1-\beta}/(1-\beta)\) for 0<beta<1 yields

$$
(a*a)(s)=\sum_{i=1}^{s-1}i^{-2/3}(s-i)^{-2/3}
\le6\cdot 2^{1/3}s^{-1/3}.
$$

Split the further convolution over i<=s/2 and i>s/2, bounding the longer factor by its smallest permitted value and applying the corresponding power-sum estimates. Then

$$
\boxed{(a*a*a)(s)\le27\cdot2^{1/3}<35.}
$$

The unordered triples with three distinct vertices contribute at most (1/4)^3 times one sixth of the complete ordered convolution, or 35/(6·64).

For exactly two equal vertices, the total contribution is at most

$$
\frac1{16}\sum_{\substack{i,j\ge1\\2i+j=s}}i^{-2/3}j^{-2/3}
\le\frac1{16}\left(\sum_{i\ge1}i^{-4/3}\right)
\le\frac4{16}.
$$

The middle bound is Cauchy--Schwarz on the sequences i^(-2/3) and (s-2i)^(-2/3), each square-sum bounded by \(\sum_{i\ge1}i^{-4/3}\le1+\int_1^\infty x^{-4/3}dx=4\). All-equal triples contribute at most 1/4. Add the three mutually exclusive types and obtain the displayed uniform bound. QED.

Theorem B and (FRACTIONAL-DIFFERENCES) hold **at every exact integer sum and difference**, hence for all sliding sum windows, arbitrary coarse block intervals, and ALL simultaneous resolutions by summing the individual inequalities. A single fractional assignment sustains order N^(1/3) prefix mass while leaving slack in all of these *first-moment* packing constraints. It does not satisfy the actual binary collision clauses, nor does it define a B3 set.

### The continuum fixed point explaining the obstruction

For real x>0, the locally integrable density \(f_\kappa(x)=\kappa x^{-2/3}\) has a scale-invariant third additive convolution:

$$
(f_\kappa*f_\kappa*f_\kappa)(x)
=\kappa^3\frac{\Gamma(1/3)^3}{\Gamma(1)}
=\text{constant},\quad x>0.
$$

The homogeneity 3(1/3)-1=0 exactly balances critical N^(1/3) mass against order-N triple sums. The discrete fractional profile is an elementary arithmetic incarnation of this convolution fixed point; density or convolution inequalities alone cannot force a logarithmic drop.

## 3. Integrality is essential: independent rounding creates linearly many collisions

Let independent Bernoulli variables X_n select the integers n with probability p_n above. In a dyadic interval (N,2N] there are only expected O(N^(1/3)) selected points, but **the expected number of pairs of distinct unordered three-element triples with the same sum and six distinct underlying vertices is Omega(N)**.

**Theorem C (quantified failure of independent rounding).** For every sufficiently large integer N (e.g. N>=200), there are at least N^5/400 distinct unordered pairs of disjoint unordered triples chosen from (N,2N] that have the same sum. Hence the expected number of such pairs after independent Bernoulli selection is at least

$$
\boxed{
\frac{N}{400\cdot 4^6\cdot2^4}
=\frac{N}{26\,214\,400}.
}\tag{ROUNDING-COLLISION-LOWER}
$$

**Proof.** Among the N integers in (N,2N], there are T=N(N-1)(N-2) ordered triples of pairwise distinct entries. Their sums lie in at most 3N integer values. If r(s) counts these ordered triples with sum s, Cauchy gives
\(\sum_s r(s)(r(s)-1)\ge T^2/(3N)-T\).
At most 9N^4 ordered pairs of ordered triples share an entry (choose the two positions of a coincident vertex and the four remaining entries). For N>=200 the remaining number is at least N^5/4. Each unordered pair of disjoint unordered triples is represented exactly 2·(3!)²=72 times, so there are at least N^5/288 such collisions, in particular N^5/400. Each of the six distinct vertices is selected with probability >=(1/4)(2N)^(-2/3); multiply to obtain the bound. QED.

The selection still has expected N^(1/3)-order cardinality, but its expected collision count grows like N. Theorem C is **not** an almost-sure lower bound on deletions or a universal bound for adversarial deterministic rounding. It clarifies the missing input: a density-preserving **collision-hypergraph integrality/repair obstruction**, or some comparably strong dependence-sensitive condition.

## 4. Revised mathematical target

The exact arbitrary-centre theorem has answered the restricted 'must blocks be equally spaced?' question: **NO**. Every actual B3 block family already obeys strong moving-window triple-Hall and globally disjoint internal difference constraints, without any center progression. Those constraints alone do not force a density dip: a single fractional model is feasible at every scale, and even the exact scalar one-resolution model in FORWARD_EXTENSION_SHADOW_CAPACITY.md survives indefinitely many coarse checkpoints.

The decisive next proposed lemma is **not** that arbitrary block centres become aligned. It is:

> For each c>0, show that a genuine 0-1 selection which maintains A(N)>=cN^(1/3) over sufficiently many nested windows cannot simultaneously eliminate ALL pair/triple collision hyperedges while respecting reciprocal future signed-code capacity. Prove a *uniform integrality cost* relative to the feasible critical fractional convolution profile.

An accepted proof must yield an explicit scale-owned discharging or bounded-horizon unsatisfiability certificate, with treatment of repeated summands and no duplicate charging. Neither (MOVING-TRIPLE-HALL), (GLOBAL-INTERNAL-DIFFERENCES), nor the fractional obstruction proves that lemma. Erdős #41 remains OPEN.

**Verification scope:** integer-exact B3 test fixtures for moving-window capacity, equal and arbitrary bin starts, disjoint within-bin differences; analytic power-sum constants; numerical fractional sum bounds; and exact collision-pair counts at moderate N. Source problem: https://www.erdosproblems.com/41, currently OPEN.
