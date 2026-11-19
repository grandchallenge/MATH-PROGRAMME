# ERDOS-249-S-WP06 — source-critical, adversarial noncertifying review

**Role:** non-authoring logical Adversary/Referee pass by the same authenticated agent as mathematical author; **not** independently authenticated, not independent human mathematical review, not Lean-checked and not MATHCERT certification.  
**Bounded issue:** [MATH-PROGRAMME #3495](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3495).  
**Exact reviewed manuscript SHA-256:** 202af20ee1c06ab33e744020388f84f9184f0d2ee5c5f2733ae515aca6180489.  
**Exact source module SHA-256:** 07f9f0a2c27e162355b422eb920464581a0cbb34d00833881fd6e9a5df5c2367.  
**Exact hostile tests SHA-256:** 8b1dac2909a7514a75f0553ccac01375791704b6dbc9a2251d3dcae0ce82bbcd.  
**Execution candidate source head:** 07ec2bfbbfae14b90d4d80c95d992d53b5718a9a.  
**Observed tests:** 11/11 PASS, exact stdout SHA-256 cf0553e2c15bd9d95f49e1f7f3e77ced151a2430c0b49b85e39369109ea6c1a4.  
**Mathematical Markdown:** PASS, log SHA-256 d4e8fa67794c1c864f92783e049a32dc4a554a844b44e191677da8ccc910e1cc.

## A. Can the constructed series remain rational with infinitely many support changes?

Yes. The source identity is exact for *any* binary sequence $b$ with $b_0=0$:

$$
\sum_{n=1}^{N}\frac{2b_{n-1}-b_n}{2^n}
=-\frac{b_N}{2^N}.
$$

The right-hand side tends to zero because $|b_N|\le1$. No eventual periodicity, density limit, conditional rearrangement, or finite-support assumption is used. The independently derived base generating value is $8/255$. This is a genuine **infinite** rational control rather than a finite rational polynomial matched to one observation.

## B. Can the sparse prime support contaminate an earlier pulse?

The construction selects each new prime larger than the predecessor by over $4\max\mathcal H+8$. The support locations are $p_j+4h-1$ and all congruent to two modulo four. Thus no supported location is $p_j$ or $p_j+4h$, both congruent to three modulo four. Earlier support locations lie below $p_j-1$, and later support locations lie above it. Therefore $b_{p_j-1}=0$ and $b_{p_j+4h-1}=1$ for every selected $h$; the congruence difference is exactly two modulo four. Arbitrarily large cofinal prime positions follow from the elementary infinitude of primes three modulo four, not from finite machine search.

## C. Are coefficient bounds valid at support transitions?

For $n<8$ the support is empty and the baseline is zero. For $n\ge8$, $4\lfloor n/8\rfloor$ is between four and $n/2$, while $2b_{n-1}-b_n$ lies between minus one and two. Thus every coefficient is at least three and at most $n/2+2\le n$; all coefficients are integral. The exact test verifies representative numerous sparse-prime windows but is not the proof of the universal bound.

## D. Does the two-scale theorem confuse an upper with a lower bound?

No. It shows that the **particular standard analytic upper bound** is larger than one when $L\le K$, because $2^K\mid\varphi(N+L)$ forces $N+L\ge2^K$. This is a necessary-depth obstruction to that bound's usefulness, **not** a claim that the true omitted tail is large or nonzero. It leaves open sharper analytic methods, different residue certificates, and all statements about the original irrationality conjecture.

## E. Does this rational control refute Cook 6.70 or 6.71?

No. Cook's source uses a universal quantified exclusion of candidate *full infinite shifted tails*, substantially stronger than the modulo-four pulses alone. The rational control does not satisfy that exclusion; otherwise Cook's condition would contradict its verified rational value. This negative model establishes that the local pulse plus positivity/linear coefficient bound is insufficient. It makes **no claim** to refute Cook's actual theorems.

## F. Novelty and external certification

The dyadic coboundary is an elementary telescoping identity, and Cook's paper already discusses nontrivial rational countercontrols to several naive strategies. No priority or novelty assertion is justified without comprehensive theorem-level comparison. This same-agent logical adversarial review is not a substitute for independent mathematical certification. The original Erdős #249 irrationality problem remains **OPEN**.

**Critical disposition:** ACCEPT_WITH_SCOPE for two bounded manuscript theorems, exact fixture evidence, rational-model falsification of an unsupported implication, and explicit successor condition. Do not promote to general totient separation or certification. The next mathematical producer must prove a totient-specific cofinal finite-residue distance lower bound at genuine analytic depth $L>K$ under all candidate rational periods.
