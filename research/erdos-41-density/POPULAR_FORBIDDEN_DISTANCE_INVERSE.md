# Erdős #41 — Popular forbidden distances and near-tiling inverse boundary

**Date:** 2026-10-16. **Status:** PROVED elementary finite B3 theorems and a quantitative restricted near-tiling inverse. The crucial critical-density independence improvement, arithmetic classification for low packing fraction, and multiscale decrement remain **OPEN**. This is a bounded Stage B successor to DILATION_ENERGY_WINDOW_GATE.md, not a solution or novelty-certification claim.

## 1. Arithmetic definitions and the pointwise matching cap

Let U be a finite repeated-summand B3 set of n>=2 distinct integers, with diameter D=max(U)-min(U)>0. Define the set P of unordered pair sums (repetition allowed), q=|P|=n(n+1)/2, and

$$
r(h)=R_{UU}(2h)=\#\{(p,p')\in P^2:p-p'=2h\},\quad h=1,\ldots,D .
$$

For every nonzero difference d, **r_P(d)<=n**. Proof: if d belongs to A-A for a B3 carrier A containing U, the previously proved exact autocorrelation selector gives r_P(d) either n or 0; if d does not belong to A-A, the positive-pair matching theorem gives r_P(d)<=n. This also holds for A=U. (See SHADOW_CORRELATION_SPECTRUM.md and SPECTRAL_MATCHING_COMPETITION.md.) The weaker universal r_P(d)<=q would lose the crucial cubic scale.

Let q_0 and q_1 be the counts of even and odd elements of P. Then the exact *parity-filtered first mass* is

$$
\boxed{
S:=\sum_{h=1}^D r(h)
=\binom{q_0}{2}+\binom{q_1}{2}
\ge\frac{q(q-2)}4\ge\frac{n^4}{32}.
}\tag{EVEN-MASS}
$$

The first identity simply pairs each two distinct pair sums of equal parity in the unique positive order. Cauchy on q_0+q_1=q proves the first inequality; q=n(n+1)/2, n>=2 gives the last. **No statistical mixing assumption enters.**

## 2. Density-sensitive popular-distance theorem (proved)

Put tau=S/(2D)>0 and define

$$
B_\tau(U)=\{1\le h\le D:r(h)\ge\tau\}.
$$

**Theorem A (popular forbidden-distance supply):**

$$
\boxed{
|B_\tau(U)|\ge\frac{S^2}{2Dn^2}
\ge\frac{n^6}{2048D},
\qquad
\tau\ge\frac{n^4}{64D}.
}\tag{POPULAR}
$$

**Proof.** For nonnegative r(h) with sum S on D positions, Cauchy gives \(\sum_h r(h)^2\ge S^2/D\). Split into r(h)<tau and r(h)>=tau. The contribution to the second moment from the first group is less than tau S=S^2/(2D). In the second group r(h)^2<=n r(h). Consequently

$$
n\sum_{h\in B_\tau}r(h)\ge\frac{S^2}{2D},
\qquad
n^2|B_\tau|\ge\frac{S^2}{2D}.
$$

Insert S>=n^4/32. QED.

**Conditional density specialization.** If a finite block U satisfies n>=c D^(1/3), for some 0<c<=1, then

$$
\boxed{
|B_\tau(U)|\ge\frac{c^6}{2048}D,
\quad r(h)\ge\frac{c^3}{64}n
\quad(h\in B_\tau).
}\tag{DENS-POPULAR}
$$

This is a **positive-density family of popular forbidden distances**, not merely positive density of the support. If U is the complete initial B3 prefix A intersect [1,D_0] under hypothetical persistent density A(t)>=c t^(1/3), then n>=c D_0^(1/3) and its actual diameter D<=D_0: with D>=1, n>=c D^(1/3). Thus the theorem applies to the actual inner prefix, no shell-occupancy model required.

## 3. Arbitrarily short fixed-ratio windows (proved, explicit constants)

Fix an integer k>=1, assume D>=2k and n^2>=32k. Partition [2min(U),2max(U)] into 2k consecutive integer intervals of lengths at most ceil((2D+1)/(2k)). Choose a most-populated interval, and within it retain the more numerous parity class of P; call the resulting pair-sum subset P_0 of size r_0. Then

$$
r_0\ge \frac{q}{4k}\ge\frac{n^2}{8k},
\quad S_0=\binom{r_0}{2}\ge\frac{n^4}{256k^2}.
$$

Since P_0 consists of one parity and lies in one short interval, all nonzero positive half-differences between its members are in [1,H], H=ceil(D/k) (a safe upper bound). For each h let r_0(h) count ordered P_0 pairs with difference 2h. Clearly r_0(h)<=r(h)<=n and sum_{h<=H}r_0(h)=S_0.

Apply Theorem A's Cauchy-and-cap argument to this restricted profile with threshold tau_0=S_0/(2H). We obtain a set B_(k) subset [1,H] satisfying

$$
\boxed{
|B_{(k)}|\ge\frac{n^6}{262144\,k^3D},\qquad
r(h)\ge r_0(h)\ge\frac{n^4}{1024\,kD}
\quad(h\in B_{(k)}).
}\tag{SHORT-POPULAR}
$$

Here H<=2D/k and the displayed constants are deliberately conservative. Under n>=c D^(1/3),

$$
\boxed{
|B_{(k)}|\ge\frac{c^6}{262144 k^3}D,
\quad
r(h)\ge\frac{c^3}{1024 k}n,\quad
1\le h\le\lceil D/k\rceil .
}\tag{SHORT-DENSITY}
$$

The cardinality bound is integer-valued, so an arbitrarily small positive right side simply forces at least one actual popular difference. No assumption is made that these popular distances intersect *outer* differences.

This is directly relevant to the localized difference reservoir of CROSS_BIN_LOCAL_DIFFERENCE_SUPPLY.md: **both spectra now have rigorously certified, c-dependent positive density at compatible short scales**. Their intersection remains unproved; a comparison of their cardinalities would only force intersection if their total densities exceeded 1, which need not happen for small c.

## 4. Independence-number baseline and the exact proof obstruction

Let I be any integer interval of span L and G_1(U,I) the forbidden-distance graph with edges at differences h where r(h)>0. If W subset I is independent, the map

$$
P\times W\longrightarrow\mathbb Z,\qquad (p,w)\mapsto p+2w
$$

is injective (otherwise p-p'=2(w'-w) with an actual forbidden difference). Since P has diameter 2D and 2W has span at most 2L, this gives

$$
\boxed{
\alpha(G_1(U,I))\le
\left\lfloor\frac{2D+2L+1}{q}\right\rfloor .
}\tag{ALPHA}
$$

This is a **density-sensitive** quantitative upper bound: if n>=cD^(1/3) and L<=D, then

$$
\boxed{
\alpha(G_1(U,I))\le
\left\lfloor\frac{4D+1}{q}\right\rfloor
\le\frac{8D+2}{n^2}
=O(c^{-2}D^{1/3}).
}
$$

**Critical limitation:** for actual B3 outer W disjoint from U, the original sum map p+w is already injective, yielding the even *stronger* ordinary three-sum packing bound \(|W|q\le2D+L+1\). Thus (ALPHA) is **not an improvement over established B3 packing** in the hypothesized critical-density configuration. Even with the popular-distance supply, no density-dip theorem follows. In particular an adversarial modulus/residue construction may keep many candidate outer positions independent despite a positive-density forbidden-distance set.

## 5. Rigorous inverse structure when independence nearly saturates capacity

A truly *near-maximal* independent set does obey a stronger, quantitative structural constraint, beyond its cardinality.

Let U be any finite B3 block and W independent in G_1(U,I), write m=|W|, q=|P|, and take the integer interval containing the complete sumset P+2W of width

$$
M=2D+2\operatorname{diam}(W)+1.
$$

After translating the interval to [0,M-1], let C be the complement of P+2W, so |C|=M-qm. In the cyclic group Z/MZ, define \(\widehat F(\xi)=\sum_{x=0}^{M-1}F(x)e^{-2\pi i\xi x/M}\). All sums P+2W lie in that interval, with no wrap ambiguity.

**Theorem B (near-tiling spectral complementarity):** For every nonzero frequency xi modulo M,

$$
\boxed{
|\widehat{\mathbf1_P}(\xi)\,\widehat{\mathbf1_{2W}}(\xi)|
=|\widehat{\mathbf1_C}(\xi)|
\le M-qm.
}\tag{TILING}
$$

Proof: the disjoint translates make the convolution \(\mathbf1_P*\mathbf1_{2W}\) equal the indicator of P+2W. This is 1−1_C after translating the supporting interval, so at every nonzero character its Fourier transform is minus the transform of 1_C. A common translation introduces only a unit-modulus phase. QED.

If qm >=(1−epsilon)M with epsilon<1, then for every nonzero xi,

$$
\boxed{
\left|\frac{\widehat{\mathbf1_P}(\xi)}q\right|
\left|\frac{\widehat{\mathbf1_{2W}}(\xi)}m\right|
\le\frac{\epsilon}{1-\epsilon}.
}\tag{SPECTRAL-SEPARATION}
$$

Thus any nontrivial frequency with a large normalized Fourier coefficient of P must have a correspondingly small coefficient of 2W. For epsilon=0 their nonzero Fourier supports are exactly complementary, the familiar exact-tiling phenomenon.

**Sharp limitation:** in hypothetical critical-density B3 configurations with arbitrarily small density coefficient c, the packing fraction qm/M can be O(c^3), far from 1. This theorem proves inverse structure only in the **near-tiling** regime. It must not be advertised as the missing general arithmetic classification for unexpectedly large \(O(D^{1/3})\) independent sets.

## 6. Focused next mathematical decision gate

The preceding theorems remove one uncertainty: the actual inner pair-sum spectrum necessarily has **many popular** forbidden distances in the same short magnitude range as the proved outer-difference reservoir. There are now two precisely quantified, adversarially testable scenarios:

1. **Transverse intersection:** Prove under persistent density that the popular inner distance set B_(k) intersects the actual outer difference reservoir in enough h-values, despite arbitrary residue/spacing structure.
2. **Joint structural inverse:** If the two dense-in-a-short-window spectra remain disjoint over nested scales, show that this repeated avoidance forces a growing arithmetic period, exceptional gap concentration, or another specifically defined structure; then prove a lower-density cost using a scale-owned potential.

Neither follows from two positive density estimates alone. For small c, their densities may have sum much less than one. Nor do the finite Turán independence bound or near-tiling theorem resolve the gap. We should prioritize *cross-scale quantitative inverse arithmetic* over any further unconditional block-selector overlap bounds.

**Validation:** exact parity-filtered r-mass, pointwise cap, both popular sets, localized window cutoffs, independence packing, and near-tiling complementarity; adversarial zero-overlap B3, Sidon-digit lifts, and non-B3 hostile test cases. Do not convert numerical fixture success into a proof of the infinite claim.
