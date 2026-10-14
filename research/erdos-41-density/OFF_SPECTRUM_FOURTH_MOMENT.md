# Erdős #41: an exact off-spectrum fourth-moment identity

**Scope:** rigorous finite B3 additive-energy decomposition and a quantitative lower bound at critical cardinality. This is not an Erdős #41 solution. The finite theorem follows from the exact pair-sum autocorrelation selector in [SHADOW_CORRELATION_SPECTRUM.md](SHADOW_CORRELATION_SPECTRUM.md).

## 1. The fourth-order quantity omitted by the earlier Gram test

Let A be a finite repetition-allowed B3 set of integers, X a nonempty subset of size n and diameter D=max(X)-min(X). Write

$$
P_X=\{x+x':x,x'\in X\},\qquad q=|P_X|=\binom{n+1}{2},
$$

and for integer d set

$$
r_X(d)=|\{(p,p')\in P_X^2:p-p'=d\}|.
$$

The additive energy of P_X is

$$
E(P_X):=|\{(p_1,p_2,p_3,p_4)\in P_X^4:p_1-p_2=p_3-p_4\}|
=\sum_{d\in\mathbb Z}r_X(d)^2.
$$

This is also the fourth Fourier moment of the exponential sum of P_X:

$$
E(P_X)=\int_0^1\left|\sum_{p\in P_X}e^{2\pi i p\theta}\right|^4d\theta.
$$

The Fourier identity follows by expanding the fourth power and integrating integer Fourier characters. It has no assumption of randomness or spectral uniformity.

## 2. Exact restriction to the B3 difference spectrum

Let D(A)=A-A. The previously proved selector law gives r_X(0)=q, r_X(a-b)=n for any distinct a,b in X, and r_X(a-b)=0 for distinct a,b in A with at least one outside X. Since B3 implies B2, the n(n-1) nonzero ordered differences from X are all distinct.

Therefore the contribution to the fourth moment from D(A) is **exactly**

$$
\boxed{
\sum_{d\in D(A)}r_X(d)^2=q^2+n^3(n-1).
}\tag{KNOWN}
$$

The remaining *off-spectrum energy* is

$$
\boxed{
E_{\mathrm{off}}(X;A):=
\sum_{d\notin D(A)}r_X(d)^2
=E(P_X)-q^2-n^3(n-1).
}\tag{OFF}
$$

This identity is completely exact for **every** finite B3 carrier A containing X. There is no claim that E_off vanishes, nor that spectra of two different blocks are disjoint.

## 3. Quantitative lower bound from fourth-moment positivity

The unordered pair-sum set lies in [2min(X),2max(X)], hence all its ordered differences lie in [-2D,2D], an interval containing at most 4D+1 integers.

Because $\sum_d r_X(d)=q^2$, Cauchy–Schwarz gives

$$
q^4=\left(\sum_d r_X(d)\right)^2
\le(4D+1)\sum_d r_X(d)^2
=(4D+1)E(P_X).
$$

Substituting into (OFF) yields the unconditional **off-spectrum energy lower bound**

$$
\boxed{
E_{\mathrm{off}}(X;A)\ge
\max\left\{0,\frac{q^4}{4D+1}-q^2-n^3(n-1)\right\}.
}\tag{LOWER}
$$

For D=0, X is a singleton, the formula still holds with E_off=0 and q=1. For D>0 the integer Cauchy–Schwarz denominator is valid without boundary corrections.

A convenient coarser rational lower bound is

$$
\boxed{
E_{\mathrm{off}}(X;A)\ge
\frac{n^8}{80D}-2n^4,\qquad D\ge1.
}\tag{COARSE}
$$

Indeed q≥n²/2, 4D+1≤5D (so the stronger denominator 80 is safe), and q≤n² gives q²+n³(n-1)≤2n⁴. The cruder constant 80 avoids any delicate asymptotic bookkeeping.

**Critical-scale consequence (conditional on a finite-block hypothesis):** Suppose we have a family of finite B3 blocks X with diameters D tending to infinity and for fixed positive constants c,C the sizes obey

$$
cD^{1/3}\le n\le CD^{1/3}.
$$

Then (COARSE) implies, for sufficiently large D,

$$
\boxed{E_{\mathrm{off}}(X;A)\ge \frac{c^8}{160}D^{5/3}.}\tag{CRITICAL}
$$

Proof: the first term is at least c^8 D^(5/3)/80 while the negative term is at most 2C⁴D^(4/3). For sufficiently large D, the latter is at most half the former. Note that this is only a *conditional statement about finite B3 blocks*, not a proof that an infinite B3 set has critically large blocks at every scale.

The estimate says the off-spectrum set must contain a large **weighted fourth-order correlation reservoir**; its total squared weight has order at least D^(5/3) under a critical block size hypothesis. It does not say that the off-spectrum support occupies a positive proportion of all integer differences.

## 4. Why this does not yet contradict positive lower density

For any genuine B3 set, D(A) comprises exactly |A|(|A|-1)+1 differences. At the critical scale n≈D^(1/3), there are only order D^(2/3) specified nonzero differences from A, among order D available difference locations. The lower bound (CRITICAL) therefore places most pair-sum fourth-moment mass **outside** the prescribed A-A spectrum, but there is ample ambient room for this in principle.

The cross-block forbidden-difference theorem gives (P_X-P_Y)∩D(A)=empty for disjoint X,Y. This does not forbid P_X-P_Y from intersecting the off-spectrum support of r_X. Indeed such intersections may be natural. To exploit (CRITICAL), one would need a *new* inequality saying that every persistent-density B3 configuration necessarily forces excessive overlap, multiplicity or concentration between off-spectrum autocorrelations of blocks and cross-pair spectra. No such theorem has been proved here.

The fourth-moment identity is therefore a **precisely formulated higher-order target**, not a solution. It is stronger information than positive semidefiniteness of the A-indexed Gram matrix, whose spectrum was fixed purely by cardinality. It also identifies the exact missing data: Fourier/additive energy at differences **not** in A-A.

## 5. Verification and boundary

The exact identity (KNOWN/OFF) is established by the earlier B3 multiset-injection theorem, and (LOWER/COARSE/CRITICAL) follows from elementary Cauchy–Schwarz and integer counting. The executable fixtures compare exact Counter-based additive energies against these identities and bounds for genuine B3 sets and negative controls. The Lean file checks only the arithmetic inequalities used in the coarse estimate, not the complete universal B3/Fourier proof.

This result is mathematical synthesis rather than an external novelty claim. Related context includes Helm (1996), *On the Distribution of B3-Sequences*, DOI 10.1006/jnth.1996.0069, and Táfula (2026), *Infinite Sidon-type sets for zero-sum linear forms*, DOI 10.1007/s00605-026-02211-4. The latter proves logarithmic representation bounds for even-order balanced forms and conditional gap estimates for general zero-sum forms, not an unconditional resolution of the odd B3 case.

**Remaining open:** construct a genuine cross-scale inequality constraining the off-spectrum fourth-moment reservoir sufficiently to force the equivalent M3 finite-window valley; or produce a sourced counterexample to the proposed stronger shell-energy deficit. Erdős #41 is OPEN.
