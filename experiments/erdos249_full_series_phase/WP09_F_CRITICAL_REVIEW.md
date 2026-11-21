# WP09-F — role-scoped mathematical review and adversarial audit

**Material:** CONDITIONAL_COOK_PHASE_009F.md, conditional_cook_phase.py, and added tests in tests/test_erdos249_full_series_phase.py.  
**Inputs:** the exact primary Cook source (Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, revision 3368d1e69467aec111eb3244843ad3542171ff96); GCL protected WP09-B exact cocycle and WP09-E fixed-prime genuine totient progression identity.  
**Independent review status:** the four passes below are logically separated audits by the same agent, not authenticated independent human specialist certification, not a Lean theorem, not MATHCERT.

## Axiomatist: exact assertion boundary

The claim is for the **complete actual Cook numerator** $D_{h,N,L}$ and exponential $E_{h,N,L}$, with no truncation to a fixed number of shifts or finite-prime surrogate. Parameters h, X, L, and p are positive integers, p is prime not dividing h, and the hypothesis simultaneously requires

$$
L+h+1\le X,\quad
X\ge40p^2\max(3+\mathrm{bitlength}(3X),h+4),\quad
2^L\ge16(2X+h+L+2).
$$

For each of two explicit signed source residue classes, a one-class **exact actual Cook cocycle** real-part bound holds; for the **original Cook phases**, a two-neighbor-class conditional real-part bound holds. A separately conditional one-class bound is **existential** over those two classes; the proof does not choose it in advance.

Uniform fractional savings apply at the **least** Cook-admissible depth only once $L_h(X)>h$; the latter holds for all sufficiently large X at fixed h. Arbitrarily oversized depths retain only the displayed $Q^{-2}$ saving, not a constant relative deficit.

## Verifier: independent arithmetic reconstruction

1. For a modulus m and a residue a, the prefix discrepancy of integer counts relative to length/m has absolute value at most one. Abel summation against the increasing weight N+s yields weighted discrepancy at most $4X$ independent of m. Multiplying by the exact Möbius weight $1/d$ and summing $d\le2X+L+h+1$ costs at most $4X(1+\log(3X))$.
2. Extending the weighted main term over all divisors costs at most $W\sum_{d>M}1/d^2\le X$, because $W\le XM$. These estimates produce **$5XE_X^*$** with no source-statistical assumption.
3. Exactly summing the p-divisibility Euler factors gives $\mu_pW/p^2$ with opposite signs for $N+L+1\equiv0\pmod p$ and $N+L+h+1\equiv0\pmod p$. The $h f$ remainder is positive in the first case and at most $h(X/p+1)$ in the second.
4. The explicit threshold absorbs two weighted-count errors $10XE_X^*$ and the h remainder. It yields the signed full-source bounds $X^2/(2p^2)$ and then, after losing at most one endpoint with $|d|<3X$, the magnitude $X^2/(4p^2)$ on the recurrence-ready source set.
5. Each source class has at most $X/p+1\le2X/p$ elements. Direct Cauchy yields the energy $X^3/(32p^3)$; the square-root and sign are not interchanged in the proof.
6. Reconstruct exactly $D_{N+1}-2D_N=d_h(N+L+1)-2^Ld_h(N+1)$, hence the displayed **one-class cocycle exponential**. With $|d|<3X$ and $Q>32X$, the source is the unique centered rational residue, so chord inequality gives $X^3/(4p^3Q^2)$.
7. For centered representatives $\theta_N\in[-1/2,1/2)$, the true modulo-one recurrence implies $|d|/Q\le|\theta_{N+1}-2\theta_N|$. The deterministic $5$-norm inequality distributes this forcing into the **disjoint neighboring residue classes**. Chord inequality gives the stated two-class full-Cook deficit $X^3/(20p^3Q^2)$.
8. At least one of the two disjoint residue classes carries half this deficit. Its size is at most $2X/p$, so the **normalized existential** gap is $X^2/(80p^2Q^2)$, not an unjustified bound on a prechosen single class.
9. The least-depth inequality $Q<96X$ depends on the explicit condition $L_h(X)>h$; it is **not** true for arbitrary h-dominated minimum depths or for an oversized chosen L. This preserves the cofinal quantifiers.

## Adversary: hostile failure modes

- A mistaken sign in the conditional prime bias would make the entire theorem false. Independent direct integer totient first moments are checked for both residue classes, several p, both odd/even h, and genuine least Cook depths.
- A small p can alias numerous shifts in the **whole** Cook window; this proof never treats the full windows as independent finite shifted coordinates. It uses only the terminal difference plus exact one-step recurrence, so no false WP09-D separated-support assumption is imported.
- Dropping the modulus-centering step reopens the WP09-E unwrapped-winding counterexample. The verifier therefore checks the exact modulo-Q recurrence and centered full phases at **every** tested N; analytic proof explicitly uses the fractional-distance inequality.
- If p divides h, the two signed classes coincide and the main bias vanishes. Composite primes similarly invalidate the Euler factor; producer rejects both.
- Conditioning on N mod p is not the same as conditioning on the **largest prime factor/cofactor** used in Cook's open first bound. No correlation between the p-condition and Cook's good-set is established.
- The pair of classes may overlap with a different pair but within each result the two classes are disjoint. One must not add both r+ and r- deficits without subtracting overlaps.
- The predicted real-part bound is not a bound on the **absolute modulus** of the exponential sum. Uniform phase rotation could change its real part. The exact Cook criterion requires real part, which is the claim here.
- The new global consequence $X/(184320p^3)$ is **far below** $X/10$; the already protected WP09-B global saving can be stronger. This is a localized arithmetic-to-phase result, not Cook's final obstruction or an irrationality proof.
- Numerical floating cosine evaluation is illustrative only; actual arithmetic replay and phase-transfer tests are exact integer identities, while the all-X inequalities depend on the written analytic proof.
- No theorem priority or independent specialist certification is inferred from green CI, self-review, or repository merge.

## Referee: admissibility and next proof obligation

**Conditional result suitable for bounded research admission only**, subject to exact candidate tests, source mathematical Markdown validation, native protected merge queue, merge-group checks, material identity readback and permanent research issue evidence. Do not close source issue #3500, the parent verification programme, or the Erdős #249 open-problem record; do not issue MATHCERT.

**Scientific bottleneck:** the fixed-prime one-step cocycle yields a real first-harmonic deficit but remains insufficient to reach the Cook $9X/10$ target. A further bound must exploit *higher-order conditional correlations of the actual overlapping totient phases*, or Cook's unresolved weighted prime/cofactor conditional sum; sharpening the counting constant in this proof alone cannot bridge the several-orders-of-magnitude gap.

This is a **qualified same-agent logical adversarial review** and is not an independently authenticated theorem audit.
