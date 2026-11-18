# Erdős #249 — exact rational-denominator exclusion at depth 65,536

**Disposition: substantive finite exclusion for the full original series; not an irrationality proof.** The original question whether the full series is irrational remains **OPEN**. This packet does not alter the closed auxiliary lacunary-T verification #3205 or claim a new Lean theorem, MATHCERT disposition, separate human review, or mathematical-priority discovery.

## Source and prior work

The series is

$$
S=\sum_{n=1}^{\infty}\frac{\varphi(n)}{2^n}.
$$

Will Cook, *The Binary Totient Series*, July 2026, revised 1 October 2026, already developed exact interval/Farey exclusions and reported a depth-240 exclusion through a cutoff of approximately $7.96\times10^{34}$. [Published short paper and detailed record](https://wcook04.github.io/practical-formal-verification/maths/papers/erdos-249-binary-totient-series.html), [long research record](https://wcook04.github.io/practical-formal-verification/maths/papers/erdos249-totient-reasoning-surface--chapter-f5a03d171ab5.html). **The method is not newly invented by GCL.** This work extends the *finite verified depth and explicit bound*, and provides an independently replayable, exact-integer minimum-denominator certificate for its chosen enclosure.

## Theorem: exact exclusion for all denominators below an explicit 9,862-digit bound

Put

$$
A_N=\sum_{n=1}^{N}\varphi(n)2^{N-n}.
$$

Since $0<\varphi(n)\le n$ for $n\ge1$, with strict inequality for $n>2$, the full positive tail satisfies the strict rational enclosure

$$
\frac{A_N}{2^N}<S<\frac{A_N+N+2}{2^N}.
$$

**Proposition (Farey lower bound).** Let $Q=2^N$, $D=N+2$ and $x=A_N/Q$, $y=(A_N+D)/Q$. Suppose four nonnegative integers $a,b,c,d$ (with $b\ge1$, $d\ge0$) satisfy

$$
bc-ad=1,\qquad
\frac ab\le x<y\le\frac cd,
$$

where $1/0$ denotes positive infinity when $d=0$. Suppose also that the mediant $(a+c)/(b+d)$ belongs strictly to $(x,y)$. Then **every reduced rational** $p/q\in(x,y)$ has

$$
q\ge b+d.
$$

Moreover the reduced mediant has denominator exactly $b+d$, so this is the **best possible denominator bound for that particular rational enclosure**.

**Proof.** Since $x< p/q<y$ and the Farey neighbors bracket the full interval,

$$
bp-aq\ge1,\qquad cq-dp\ge1.
$$

Their integer expressions are positive. The unimodularity identity gives the exact Bézout-like decomposition

$$
q=d(bp-aq)+b(cq-dp)\ge b+d.
$$

The mediant is in the enclosure by hypothesis and is in lowest terms because $bc-ad=1$. This proves both minimality and attainability **within the enclosure**. It does not assert that the actual unknown value S equals this mediant.

### Exact computation and independently checkable certificate

A totient sieve builds each $\varphi(n)$ through $N$ and the integer recurrence $A_0=0$, $A_n=2A_{n-1}+\varphi(n)$. The code runs an accelerated Stern–Brocot search. Rather than trusting its search, \`validate_receipt\` independently checks the integer endpoint comparisons, $bc-ad=1$, mediant inclusion and the denominator identity. Therefore even a faulty search could not pass validation with a false bound.

Three permanent witness instances are source-locked:

| Truncation depth N | Digits in the **least compatible** rational denominator | Search iterations |
| ---: | ---: | ---: |
| 240 | 35 | 69 |
| 4,096 | 615 | 1,200 |
| **65,536** | **9,862** | **19,184** |

At depth 240 the least compatible denominator is exactly

$$
93265863992885066276123916030240921.
$$

This is consistent with (and slightly sharper for this particular enclosure than) Cook's published approximately $7.96\times10^{34}$ *proven cutoff*. The large-depth machine witness retains the full 9,862-digit denominator and its adjacent Farey neighbors, rather than relying only on a decimal approximation.

**Exact proved conclusion at N=65,536:** If $S=p/q$ is rational in lowest terms with $q\ge1$, then $q\ge Q_{65536}$, where $Q_{65536}$ is the exact integer recorded in \`K65536.json\`. Because this integer has 9,862 decimal digits,

$$
S\notin\left\{\frac pq:
p\in\mathbb Z,\;1\le q<10^{9861}\right\}.
$$

**This is a finite exclusion.** It is not a proof that rationality is impossible; a denominator larger than the reported bound is not excluded. Every larger finite cutoff can in principle be investigated by increasing N, but no theorem in this packet proves that the cutoff must tend to infinity.

## Reproducibility and falsification

Governed, importable library: \`farey_interval.py\`; no executable main guard or external package dependency. Test entry: \`tests/test_erdos249_farey_interval.py\`, registered in the existing versioned \`erdos249_full_series_phase\` policy component and discoverable by the repository-regression shard. Machine witnesses: \`K240.json\`, \`K4096.json\`, \`K65536.json\`.

Run from the repository root:

\`\`\`bash
python3 -m unittest discover -s tests -p 'test_erdos249_farey_interval.py' -v
python3 -c 'from experiments.erdos249_full_series_phase.farey_interval import compute,validate_receipt; r=compute(65536);validate_receipt(r);print(r["minimal_denominator_digits"])'
\`\`\`

The **eight adversarial test cases** check the sieve against independent gcd-counting through 512, the integer prefix against direct weighted sums, exact brute-force minimum denominators at smaller depths, the source-locked Farey inequality certificates at depths 240/4096/65536, deliberate witness mutation rejection, independent regeneration of the 65,536-term totient prefix, monotonicity of the nested interval cutoffs, and the exact rational $4/3$ comparator. The comparator is a positive, linearly bounded integer-coefficient series whose rational value lies in corresponding elementary tail intervals. This prevents promoting an interval-exclusion routine into a general irrationality detector.

The calculations use only exact integer/rational operations; decimal digit counts are derived from the stored integer. No floating-point phase inference, stochastic simulation or external numerical oracle is involved.

## Evidentiary and mathematical boundary

- **Unconditional:** All denominator exclusions strictly below the stated $10^{9861}$ bound for the *full* totient series, after exact prefix arithmetic, certificate checks and repository admission.
- **Not established:** Irrationality of S; unbounded/cofinal rational-denominator exclusion; Cook's sufficient arithmetic hypotheses; novelty or priority beyond this finite computational extension.
- **No independent human or Lean formal review:** The proof is a complete manuscript argument, checked by executable exact-integer tests. Neither is a proof of the open statement.
- **Next necessary mathematical step:** Obtain a cofinal, arithmetic (not computational-range-limited) lower bound on the least compatible denominator $Q_N$ along an unbounded sequence N, or prove one of Cook's source-locked cofinal residue/cancellation hypotheses for the actual totient sequence. The latter remains the direct preferred route; enlarging N again has diminishing scientific value.

The certificate format is deliberately compact in logic: only two bracketing fractions, their determinant 1, a strict mediant inequality and the correct prefix are needed to verify the exclusion.
