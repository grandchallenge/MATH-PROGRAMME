# M3 multiscale candidate: a quantified shell-energy deficit

**Research status: OPEN CONJECTURAL LEMMA.** This note identifies a strong, falsifiable sufficient condition for the current repetition-allowed Erdős #41 conjecture. It does not claim to prove that condition. Its implication to the Erdős conclusion is elementary and established below.

## 2026-10-13 adversarial status update

The audited follow-up [SHELL_HARDY_AUDIT.md](SHELL_HARDY_AUDIT.md) proves that the proposed shell-energy deficit is equivalent to logarithmic Cesàro decay of cubed normalized counting density. It is **strictly stronger than the original density-dip conclusion at the level of general counting profiles even when the ordinary cubic packing bound holds**. This is not a counterexample among M3 sets. The proposed shell-energy deficit remains OPEN and is not assumed true. The follow-up supplies the *finite-window valley criterion* (V), exactly equivalent to the original M3 Erdős conjecture, as the better primary multiscale target.

## A rigorous packing baseline

Suppose A is an M3 subset of the positive integers and m is the number of its elements in the interval [1,N]. The number of size-three multisets supported in these m elements is

$$
\binom{m+2}{3}.
$$

All their sums are distinct and lie between 3 and 3N. Consequently

$$
\binom{m+2}{3}\leq 3N-2,
\qquad m^3 \leq 18N,
\qquad m\leq 3N^{1/3}.
$$

This is a standard-order cubic bound, not yet an asymptotic density dip. More generally, for three pairwise disjoint intervals with integer lengths L1,L2,L3 (upper minus lower endpoints), and respective M3 occupancies m1,m2,m3, the m1*m2*m3 cross-block sums are all distinct, implying

$$
m_1m_2m_3\leq L_1+L_2+L_3+1.
$$

These inequalities are the established packing baseline that any sharper multiscale estimate must improve.

## A concrete sufficient lemma, not an established theorem

Define the dyadic shell occupancy

$$
m_j=|A\cap[2^j,2^{j+1})|,
\qquad j=0,1,2,\ldots.
$$

The following is a proposed **multiscale shell-energy deficit**:

$$
\boxed{\liminf_{J\to\infty}\frac1J
\sum_{j=0}^{J-1}\frac{m_j^3}{2^j}=0\quad\text{for every infinite M3 set }A.}
$$

This condition is intentionally much more specific than simply restating the counting-function conjecture. It asserts sublinear cumulative cubic shell occupancy, a potentially falsifiable structural restriction beyond the standard termwise packing estimate. Its truth is currently **UNPROVED**, and it may be false. It is not a claimed new result.

## Exact implication from proposed lemma to Erdős #41

Suppose contrary to the Erdős conclusion that there exist c>0 and N0 such that A(N) is at least c times N to the one-third power for every N at least N0. Write

$$
X_j=|A\cap[1,2^{j+1})|=\sum_{i=0}^j m_i.
$$

For all large j, the persistent-density hypothesis gives

$$
X_j\ge c2^{j/3}.
$$

Our proven standard cubic packing bound gives, for any nonnegative integer L,

$$
X_{j-L}\le3\cdot2^{(j-L+1)/3}.
$$

Choose a fixed L sufficiently large that 3 times 2 to the power (1-L)/3 is less than c/2. Then all sufficiently late blocks of L successive shells obey

$$
\sum_{i=j-L+1}^{j}m_i\ge\frac{c}{2}2^{j/3}.
$$

At least one shell index i in each such block satisfies

$$
\frac{m_i^3}{2^i}\ge\left(\frac{c}{2L}\right)^3.
$$

Partition the late shell indices into disjoint blocks of length L. Consequently the averages of the nonnegative shell-energy terms are bounded below by a positive constant in the limit (for instance, c cubed divided by 8 times L to the fourth power, up to negligible end effects). Their liminf cannot equal zero. This contradicts the **proposed** shell-energy deficit.

Thus proving the boxed lemma would solve modern M3 Erdős #41. This implication is rigorous. **The boxed lemma itself remains open**, and requires independent adversarial work; ordinary M3 triple-sum counting alone gives only a bounded shell-energy term and cannot establish the required average decay.

## Bounded next research experiment

For finite M3 fixtures across a range of scales, compute the dyadic shell counts and their cumulative normalized cubic energy. Include constructive B3 sequences, randomized greedily extended sequences, and adversarial families selected for unusually dense consecutive shells. Search specifically for evidence *against* the boxed lemma. Do not infer its truth from limited runs or from the superlacunary finite witnesses in the source-fidelity audit.

Separate the results clearly: **proved elementary packing**, **proved conditional implication**, **unproved shell deficit**. No MATHCERT or solution-state promotion is authorized by this docket.
