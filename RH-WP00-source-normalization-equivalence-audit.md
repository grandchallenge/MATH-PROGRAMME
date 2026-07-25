# RH-WP00 — Source, Normalization, and Equivalence Audit

**Artifact ID:** `RH-WP00-source-normalization-equivalence-audit`  
**Challenge:** Riemann Hypothesis  
**Campaign:** `RH-001`  
**Programme lane:** MATHSOLVE  
**Status:** `INTERNAL REVIEW COMPLETE — REPOSITORY REVIEW REQUIRED`  
**Version:** 0.1.0  
**Audit date:** 2026-07-25  
**Promotion authority:** Referee  
**Claim class:** `SOURCE-NORMALIZED / NON-SOLUTION ARTIFACT`

---

## 0. Executive disposition

This Work Package fixes the canonical Riemann Hypothesis statement, analytic normalization, zero taxonomy, symmetry and multiplicity conventions, exact equivalence routes, non-equivalence boundaries, false-proof seeds, theorem spine, proof debt, and certification boundary.

The binding companion artifacts are:

- `campaigns/riemann_hypothesis/WP00_SOURCE_NORMALIZATION_EQUIVALENCE/00_CHARTER.md`;
- `campaigns/riemann_hypothesis/WP00_SOURCE_NORMALIZATION_EQUIVALENCE/02_FUNCTION_AND_ZERO_LOCK.md`.

This artifact does **not** claim:

- a proof or disproof of the Riemann Hypothesis;
- a new zero-free region or zero-density estimate;
- a new proportion of zeros on the critical line;
- a new prime-counting error bound;
- a new equivalent criterion;
- a Hilbert-Polya operator;
- a newly certified zero computation;
- a novelty result.

It is eligible for repository review as a source, statement, and equivalence-control dossier only.

---

## 1. Result-status box

| Field | Value |
|---|---|
| Result status | `WP00 DRAFT COMPLETE / OPEN PROBLEM` |
| Conditions | Classical Riemann zeta function; standard meromorphic continuation; nontrivial zeros counted with multiplicity |
| Strongest supported claim | The canonical target, analytic objects, zero symmetries, exact core equivalences, non-equivalence boundaries, and certification obligations are normalized |
| Not claimed | RH, GRH, simplicity, a new verified height, a new equivalent criterion, a spectral realization, or a prime-distribution theorem |
| Support-route class | `PRIMARY_SOURCE_AUDIT`, `SEMANTIC_CORRESPONDENCE_AUDIT`, `LITERATURE_DERIVED`, `NEGATIVE_RESULT` |
| Computation class | `NONE` |
| Certification state | Human semantic and source audit prepared; repository review and CI outstanding; no theorem-prover certification of analytic continuation or zero theory |
| First executable step | Run adversarial review on the twenty false-proof seeds and promote them into `RH-WP01`; build the theorem-by-theorem known-results ledger in `RH-WP02` |

## 2. Lay executive companion

The zeta function begins as a weighted sum of the positive integers:

```math
1+2^{-s}+3^{-s}+4^{-s}+\cdots.
```

For complex `s` with real part greater than one, this sum converges and can also be written as a product over primes. Analytic continuation extends the function to almost the whole complex plane. Its zeros then become a compressed record of how the primes depart from their average distribution.

Some zeros occur for transparent algebraic reasons at the negative even integers. The remaining zeros occupy a vertical strip between real parts zero and one and occur in symmetric families. The Riemann Hypothesis says that every one of them sits exactly on the strip's centre line.

The symmetry is suggestive but not decisive. A mirror-symmetric flock need not fly on the mirror: points may occur in reflected quartets away from the centre. Numerical verification is similarly bounded. It can show that every zero up to a certified height lies on the line, but the conjecture quantifies over an infinite set.

A useful reformulation can move the problem into prime-counting errors, positivity of coefficients, approximation in a Hilbert space, arithmetic inequalities, or a spectral problem. Each move transfers the burden rather than erasing it. The purpose of `RH-WP00` is to record exactly what must survive each transfer.

## 3. Canonical statement

For `Re(s)>1`,

```math
\zeta(s)=\sum_{n=1}^{\infty}\frac{1}{n^s}
        =\prod_p(1-p^{-s})^{-1}.
```

The Dirichlet series has a unique meromorphic continuation to `C`, with one simple pole at `s=1`. Define

```math
\xi(s)=\frac12s(s-1)\pi^{-s/2}\Gamma\!\left(\frac{s}{2}\right)\zeta(s).
```

Then `xi` is entire and

```math
\xi(s)=\xi(1-s).
```

The canonical target is

```math
\boxed{
\forall \rho\in\mathbb C,
\quad
\xi(\rho)=0
\Longrightarrow
\operatorname{Re}(\rho)=\frac12.
}
```

Equivalently, for

```math
\Xi(t)=\xi\!\left(\frac12+it\right),
```

every zero of `Xi` is real.

A terminal refutation is one rigorously certified `rho` such that

```math
\zeta(\rho)=0,
\qquad
0<\operatorname{Re}(\rho)<1,
\qquad
\operatorname{Re}(\rho)\ne\frac12.
```

## 4. Binding source ledger

| ID | Source | Role | Binding use | Audit state |
|---|---|---|---|---|
| `SRC-RH-00` | Enrico Bombieri, *Problems of the Millennium: the Riemann Hypothesis*, <https://www.claymath.org/wp-content/uploads/2022/05/riemann.pdf> | Normative theorem statement | Definition, completion, functional equation, canonical RH statement, prime-error equivalence, explicit-formula and evidence boundaries | `CHECKED` |
| `SRC-RH-01` | Clay Mathematics Institute, *Riemann Hypothesis*, <https://www.claymath.org/millennium/Riemann-Hypothesis/> | Current institutional status | Open-problem status and official resource routing | `CHECKED_2026-07-25` |
| `SRC-RH-02` | B. Riemann, *On the Number of Primes Less Than a Given Magnitude* (1859), Clay manuscript collection, <https://www.claymath.org/library/historical/riemann/> | Historical primary source | Original real-zero formulation and historical notation concordance | `CHECKED_IN_TRANSLATION` |
| `SRC-RH-03` | NIST DLMF §25.2, <https://dlmf.nist.gov/25.2> | Reference normalization | Dirichlet series, continuation, pole, Euler product | `CHECKED` |
| `SRC-RH-04` | NIST DLMF §25.4, <https://dlmf.nist.gov/25.4> | Reference normalization | Functional equation and `xi(s)` normalization | `CHECKED` |
| `SRC-RH-05` | NIST DLMF §25.10, <https://dlmf.nist.gov/25.10> | Reference normalization | Trivial zeros, critical strip, critical line, Hardy `Z` conventions | `CHECKED` |
| `SRC-RH-06` | E. C. Titchmarsh, revised by D. R. Heath-Brown, *The Theory of the Riemann Zeta-Function*, 2nd ed. | Analytic reference | Zero counting, explicit formulae, equivalent growth estimates, contour conventions | `BIBLIOGRAPHICALLY_FIXED / LOCATORS_DEFERRED_TO_WP02` |
| `SRC-RH-07` | X.-J. Li, “The Positivity of a Sequence of Numbers and the Riemann Hypothesis,” *J. Number Theory* 65 (1997), 325-333, DOI `10.1006/jnth.1997.2137` | Exact equivalence | Li-coefficient criterion | `STATEMENT_CHECKED` |
| `SRC-RH-08` | E. Bombieri and J. C. Lagarias, “Complements to Li's Criterion for the Riemann Hypothesis,” *J. Number Theory* 77 (1999), 274-287, DOI `10.1006/jnth.1999.2392` | Criterion clarification | Positivity criterion and zero-multiset formulation | `STATEMENT_CHECKED` |
| `SRC-RH-09` | G. Robin, “Grandes valeurs de la fonction somme des diviseurs et hypothese de Riemann,” *J. Math. Pures Appl.* 63 (1984), 187-213 | Exact arithmetic equivalence | Robin inequality | `STATEMENT_CHECKED / PRIMARY PDF LOCATOR DEBT` |
| `SRC-RH-10` | J. C. Lagarias, “An Elementary Problem Equivalent to the Riemann Hypothesis,” *Amer. Math. Monthly* 109 (2002), 534-543, DOI `10.1080/00029890.2002.11919883` | Exact arithmetic equivalence | Harmonic-number divisor-sum criterion | `CHECKED` |
| `SRC-RH-11` | L. Baez-Duarte, “A strengthening of the Nyman-Beurling criterion for the Riemann hypothesis,” *Rend. Mat. Acc. Lincei* 14 (2003), 5-11; arXiv `math/0202141` | Exact Hilbert-space equivalence | Integer-dilation Nyman-Beurling criterion | `STATEMENT_CHECKED / NORMALIZATION AUDIT OPEN` |
| `SRC-RH-12` | A. Weil, “Sur les formules explicites de la theorie des nombres premiers” (1952) | Positivity route | Explicit-formula positivity criterion | `SOURCE IDENTIFIED / EXACT TEST CLASS DEBT` |
| `SRC-RH-13` | L. Baez-Duarte, “A sequential Riesz-like criterion for the Riemann hypothesis,” *Int. J. Math. Math. Sci.* 2005, 3527-3537, DOI `10.1155/IJMMS.2005.3527` | Sequence criterion | Sequential Riesz-like equivalence and simplicity-strengthening boundary | `STATEMENT CHECKED / DEFERRED` |

### 4.1 Source hierarchy

1. `SRC-RH-00` fixes the official challenge.
2. `SRC-RH-02` fixes historical intent and notation provenance.
3. `SRC-RH-03` through `SRC-RH-05` fix standard analytic normalization.
4. `SRC-RH-07` through `SRC-RH-13` govern particular equivalence lanes.
5. Later literature may improve partial results but may not silently alter definitions, quantifiers, or equivalence hypotheses.

### 4.2 Temporal status rule

RH remains institutionally listed as unsolved on the audit date. Any later claimed resolution requires a fresh acceptance audit. A preprint title, repository claim, numerical experiment, or unrefereed manuscript does not change programme status.

## 5. Analytic normalization lock

The following distinctions are binding:

| Object | Domain/status | Hazard |
|---|---|---|
| `sum n^{-s}` | Absolutely convergent for `Re(s)>1` | Illegal use inside the strip |
| Euler product | Absolutely convergent for `Re(s)>1` | Termwise continuation is invalid |
| `zeta(s)` | Meromorphic on `C`, simple pole at `1` | Pole omitted or treated as zero |
| `Lambda(s)=pi^{-s/2}Gamma(s/2)zeta(s)` | Meromorphic, poles at `0,1` | Incorrectly called entire |
| `xi(s)=1/2 s(s-1)Lambda(s)` | Entire | Normalization collision |
| `Xi(t)=xi(1/2+it)` | Entire in complex `t`, even, real on real axis | Confused with Hardy `Z` |
| `Z(t)` | Real-valued for real `t` under phase convention | Sign changes miss even multiplicity |
| `Log zeta(s)` | Local branch only on declared zero-free domain | Global branch assumed |
| `-zeta'/zeta` | Meromorphic | Residues and pole signs lost |

The full lock is in `02_FUNCTION_AND_ZERO_LOCK.md`.

## 6. Zero symmetry and location ledger

For every nontrivial zero `rho`, the zero multiset is invariant under

```math
\rho\mapsto\overline{\rho}
```

and

```math
\rho\mapsto1-\rho.
```

Hence a generic off-line zero occurs in the quartet

```math
\rho,
\quad\overline{\rho},
\quad1-\rho,
\quad1-\overline{\rho}.
```

The symmetries preserve multiplicity. They do not imply that `rho` is fixed by either map.

The classical location theorem places nontrivial zeros in

```math
0<\operatorname{Re}(s)<1.
```

Its ingredients are separated:

- the Euler product excludes zeros for `Re(s)>1`;
- zero-freeness on `Re(s)=1` is a separate prime-number-theorem theorem;
- the functional equation reflects the result across `Re(s)=1/2`;
- gamma-factor accounting identifies the negative even trivial zeros.

## 7. Theorem spine

```text
RH-D000  Complex variable, real/imaginary part, branch conventions
RH-D001  Dirichlet-series zeta on Re(s)>1
RH-D002  Euler product on Re(s)>1
RH-T003  Meromorphic continuation and simple pole at s=1 [LITERATURE]
RH-D004  Gamma factor and Lambda(s)
RH-D005  Entire completion xi(s)
RH-T006  Functional equation xi(s)=xi(1-s) [LITERATURE]
RH-L007  Conjugation symmetry
RH-L008  Functional-equation zero symmetry
RH-K009  Trivial-zero divisor calculation
RH-K010  Nontrivial zeros lie in 0<Re(s)<1 [LITERATURE]
RH-D011  Xi(t), Hardy Z(t), and counting functions
RH-B012  RH <-> all zeros of Xi are real
RH-B013  RH <-> N0(T)=N(T) for every admissible T
RH-B014  RH <-> prime-counting square-root error
RH-B015  RH <-> Chebyshev square-root error
RH-B016  RH <-> Li coefficient nonnegativity
RH-B017  RH <-> Nyman-Beurling closure criterion
RH-B018  RH <-> Robin divisor-sum inequality
RH-B019  RH <-> Lagarias harmonic-number inequality
RH-B020  RH <-> Mertens epsilon-family bound
RH-B021  Weil positivity criterion [NORMALIZATION DEBT]
RH-O022  Finite-height verification obstruction
RH-O023  Symmetry-not-location obstruction
RH-O024  Conditional-convergence and contour obstruction
RH-O025  Positivity test-class obstruction
RH-O026  Symmetric-versus-self-adjoint spectral obstruction
RH-O027  Density-one-versus-all-zeros obstruction
RH-O028  Equivalent-criterion quantifier drift
RH-T029  Classical Riemann Hypothesis [OPEN]
RH-R030  First restricted theorem target [UNSELECTED]
```

### 7.1 Dependency architecture

```text
D000 -> D001 -> T003 -> D004 -> D005 -> T006
          |        |                |       |
          v        v                v       v
         D002     K009             L007    L008
                                             |
                                             v
                                           K010
                                             |
                 D011 -----------------------+
                   |                          |
                   +-> B012 -> T029           |
                   +-> B013 -> T029           |

T003 + T006 + explicit formula -> B014/B015/B020 -> T029
D005 + zero product theory     -> B016 -> T029
Mellin/Hilbert-space theory    -> B017 -> T029
Prime estimates                -> B018/B019 -> T029
Explicit formula + test class  -> B021 -> T029

O022..O028 constrain every route into T029.
WP00 -> WP01 false-proof atlas + WP02 theorem ledger.
WP00 + WP01 + WP02 + prior-art audit -> R030 selection gate.
```

## 8. Exact equivalence catalogue

An entry is marked `BINDING` only when the statement, quantifiers, normalization, and both directions are sufficiently fixed for programme use. `SOURCE-BOUND` means the equivalence is accepted from the cited theorem but its proof and every technical convention remain to be reconstructed in `RH-WP02`. `DEFERRED` means it may not yet be used as a programme bridge.

### 8.1 Core zero formulation

| ID | Statement | Relation | State |
|---|---|---|---|
| `RH-EQ-00` | Every nontrivial zero of `zeta` has real part `1/2` | Canonical | `BINDING` |
| `RH-EQ-01` | Every zero of `xi(s)` has real part `1/2` | Exact | `BINDING` |
| `RH-EQ-02` | Every zero of `Xi(t)=xi(1/2+it)` is real | Exact | `BINDING` |
| `RH-EQ-03` | `N_0(T)=N(T)` for every admissible `T>0`, with identical ranges and multiplicity conventions | Exact | `BINDING` |

The map in `RH-EQ-02` is

```math
t=-i\left(s-\frac12\right).
```

A zero `s=rho` lies on the critical line exactly when the corresponding `t` is real.

`RH-EQ-03` is global. Equality at one height or along an unbounded sequence of heights does not suffice unless those equalities jointly cover every zero ordinate.

### 8.2 Prime-distribution formulations

Let

```math
\psi(x)=\sum_{n\le x}\Lambda(n).
```

The following classical estimates are source-bound exact equivalents:

```math
\mathrm{RH}
\iff
\pi(x)=\operatorname{Li}(x)+O(\sqrt{x}\log x),
```

and

```math
\mathrm{RH}
\iff
\psi(x)=x+O(\sqrt{x}\log^2 x).
```

| ID | Obligation | State |
|---|---|---|
| `RH-EQ-04A` | Fix the `Li` convention and range of `x` | `DISCHARGED FOR BIG-O USE` |
| `RH-EQ-04B` | `RH -> pi` estimate via explicit formula | `SOURCE-BOUND` |
| `RH-EQ-04C` | `pi` estimate -> zero-free half-plane `Re(s)>1/2` and symmetry -> RH | `SOURCE-BOUND` |
| `RH-EQ-05A` | `RH -> psi` estimate | `SOURCE-BOUND` |
| `RH-EQ-05B` | `psi` estimate -> analytic continuation/nonvanishing of `-zeta'/zeta` to `Re(s)>1/2` -> RH | `SOURCE-BOUND` |

Hazards:

- replacing `O(sqrt(x) log x)` by a visually similar but weaker error;
- proving the estimate only on sampled `x`;
- allowing the implied constant to depend on `x`;
- confusing `pi`, `theta`, `psi`, or a smoothed counting function;
- dropping prime-power and endpoint corrections in exact formulae.

### 8.3 Li coefficient criterion

Define, for positive integers `n`,

```math
\lambda_n
=
\left.
\frac{1}{(n-1)!}
\frac{d^n}{ds^n}
\left[s^{n-1}\log\xi(s)\right]
\right|_{s=1},
```

where the logarithm is the local analytic branch near `s=1`, since `xi(1) != 0`.

The source-bound criterion is

```math
\mathrm{RH}
\iff
\lambda_n\ge 0
\quad\text{for every }n\ge1.
```

| ID | Obligation | State |
|---|---|---|
| `RH-EQ-06A` | Fix `xi` normalization | `DISCHARGED` |
| `RH-EQ-06B` | Prove derivative definition equals the regularized zero sum | `SOURCE-BOUND` |
| `RH-EQ-06C` | RH implies nonnegativity | `SOURCE-BOUND` |
| `RH-EQ-06D` | Nonnegativity for every `n` excludes off-line zeros | `SOURCE-BOUND` |
| `RH-EQ-06E` | Strict versus non-strict positivity variants | `LOCATOR DEBT` |

Computing `lambda_1,...,lambda_N` as positive for finite `N` is not a proof.

### 8.4 Nyman-Beurling-Baez-Duarte criterion

Let

```math
\rho(x)=x-\lfloor x\rfloor,
\qquad
\rho_a(x)=\rho\!\left(\frac{1}{ax}\right),
\qquad
\chi=\mathbf 1_{(0,1)}.
```

In `L^2(0,infinity)`, let `B` be the span of `rho_a` for real `a>=1`. The source-bound Nyman-Beurling criterion is

```math
\mathrm{RH}
\iff
\chi\in\overline{B}^{L^2}.
```

Baez-Duarte's strengthening permits the span generated by positive integer `a`.

| ID | Obligation | State |
|---|---|---|
| `RH-EQ-07A` | Confirm interval endpoint convention for `chi` | `NON-MATERIAL IN L2 / RECORD REQUIRED` |
| `RH-EQ-07B` | Confirm parameter convention `a>=1` versus reciprocal parameterizations | `OPEN NORMALIZATION AUDIT` |
| `RH-EQ-07C` | Fix complex or real linear span | `OPEN NORMALIZATION AUDIT` |
| `RH-EQ-07D` | Prove Mellin-transform bridge and both implications | `SOURCE-BOUND` |
| `RH-EQ-07E` | Integer-dilation strengthening | `SOURCE-BOUND` |

No finite-dimensional approximation, however accurate, establishes membership in the closure unless accompanied by a theorem controlling the limiting distance.

### 8.5 Robin criterion

Let

```math
\sigma(n)=\sum_{d\mid n}d
```

and let `gamma` be the Euler-Mascheroni constant. Robin's theorem gives

```math
\mathrm{RH}
\iff
\sigma(n)<e^\gamma n\log\log n
\quad\text{for every integer }n>5040.
```

The threshold, strict inequality, and universal quantifier are part of the theorem. Verifying the inequality for a large finite range is not a proof.

### 8.6 Lagarias criterion

Let

```math
H_n=\sum_{k=1}^n\frac1k.
```

Lagarias gives the exact arithmetic equivalent

```math
\mathrm{RH}
\iff
\sigma(n)
\le
H_n+e^{H_n}\log H_n
\quad\text{for every }n\ge1,
```

with equality only for `n=1`.

The statement is elementary in vocabulary, not elementary in proof burden. It packages the analytic difficulty into a universal divisor-sum inequality.

### 8.7 Mertens-function criterion

Let

```math
M(x)=\sum_{n\le x}\mu(n).
```

A classical source-bound equivalence is

```math
\mathrm{RH}
\iff
\forall\varepsilon>0,
\quad
M(x)=O_\varepsilon\!\left(x^{1/2+\varepsilon}\right).
```

The epsilon quantifier is structural. The stronger statement `M(x)=O(sqrt(x))` is not the criterion and is known to be too rigid as a naive replacement. A proof for one fixed epsilon does not imply RH.

### 8.8 Weil positivity criterion

The explicit formula can be arranged as a quadratic or linear positivity condition on a declared test-function class. With the correct class and transform conventions, positivity for every admissible test function is equivalent to RH.

This lane is **not yet binding** because the following remain open in this package:

- the exact Weil test class selected for the programme;
- Mellin/Fourier transform normalization;
- involution and convolution conventions;
- prime, archimedean, pole, and zero terms;
- sign convention for the quadratic form;
- density and closure requirements.

Status: `DEFERRED TO RH-WP02`. A proposal may not cite “Weil positivity” without instantiating this contract.

### 8.9 Deferred criteria

The following are recognized but not normalized for use in WP00:

- Riesz and Hardy-Littlewood criteria;
- Baez-Duarte sequential coefficients;
- Franel-Landau Farey-sequence criteria;
- Redheffer-matrix determinant criteria;
- de Bruijn-Newman constant formulations;
- Laguerre-Polya entire-function criteria;
- local-extrema sign criteria for `Xi`;
- Beurling generalized-prime analogues.

They enter `RH-WP02` only after exact statement and source reconstruction.

## 9. One-way implications, stronger statements, and neighboring claims

| Statement | Correct relation to RH |
|---|---|
| Prime number theorem | Consequence of a zero-free line `Re(s)=1`; much weaker than RH |
| Lindelof hypothesis for `zeta(1/2+it)` | Consequence of RH; converse not known |
| Every nontrivial zero is simple | Separate conjecture; does not place zeros on the line |
| RH plus simplicity | Strictly stronger package than RH alone |
| A positive proportion of zeros lie on the line | Known partial direction; far weaker than RH |
| `N_0(T)/N(T) -> 1` | Still weaker than RH; permits a density-zero exceptional set |
| Montgomery pair correlation | Statistical statement; commonly conditioned on RH or restricted to line zeros; not a substitute |
| GUE spacing statistics | Heuristic/statistical evidence, not a zero-location theorem |
| GRH for all Dirichlet `L`-functions | Stronger family statement; contains classical RH as one case |
| Weil conjectures over finite fields | Proved geometric analogue, not a proof of classical RH |
| A symmetric operator with matching-looking eigenvalues | Insufficient; symmetry is not self-adjointness and resemblance is not spectral equality |
| A self-adjoint operator whose complete spectrum is exactly the zero ordinates | Sufficient Hilbert-Polya route if every analytic and spectral bridge is proved |
| Verification through finite height | Finite theorem only; never the global statement |
| Positivity of finitely many Li coefficients | Finite evidence only |
| Robin or Lagarias inequality through finite `n` | Finite evidence only |

## 10. Hilbert-Polya route contract

A spectral proposal must provide:

1. a Hilbert space with inner product;
2. a densely defined operator `H` and exact domain;
3. closedness or a proved closure;
4. self-adjointness, not merely formal symmetry;
5. a spectral theorem applicable to `H`;
6. discreteness or an exact treatment of continuous/residual spectrum;
7. a proved correspondence

```math
\operatorname{Spec}(H)
=
\{\gamma:\zeta(1/2+i\gamma)=0\}
```

with multiplicities;
8. completeness: no missing zeros and no extraneous eigenvalues;
9. a trace or determinant formula with regularization justified;
10. compatibility with the explicit formula and archimedean factors.

A numerical fit of eigenvalue spacings, a PT-symmetric Hamiltonian, or a formally Hermitian differential expression does not discharge these obligations.

## 11. False-proof seed registry

| ID | Invalid move | Exact failure | Required repair |
|---|---|---|---|
| `RH-F001` | Verify many zeros and conclude RH | Universal quantifier replaced by finite range | Global theorem or explicit terminal certificate |
| `RH-F002` | Show almost all zeros lie on the line | Density-zero exceptions remain possible | Exclude every exception |
| `RH-F003` | Use quartet symmetry to force the line | Symmetric sets may contain off-line quartets | Add a coercive location mechanism |
| `RH-F004` | Continue the Euler product into the strip termwise | Product does not converge there | New valid representation with convergence proof |
| `RH-F005` | Rearrange a conditionally convergent zero sum | Value may depend on summation order | Symmetric truncation or absolute convergence theorem |
| `RH-F006` | Use a global `Log zeta` | Zeros obstruct a global branch | Declare zero-free simply connected domain |
| `RH-F007` | Move a contour across zeros or the pole silently | Missing residues change the identity | Residue ledger and admissible limiting contour |
| `RH-F008` | Interchange sum, integral, derivative, or limit formally | No domination or uniform convergence | Supply a named convergence theorem and hypotheses |
| `RH-F009` | Prove positivity on a sampled test family | Criterion requires all functions in a class or dense closure | Density theorem plus continuity of the form |
| `RH-F010` | Treat a symmetric operator as self-adjoint | Domain and deficiency indices may differ | Prove self-adjointness or essential self-adjointness |
| `RH-F011` | Match part of a spectrum to zero ordinates | Missing/extraneous spectrum not excluded | Exact complete spectral correspondence |
| `RH-F012` | Compute finitely many positive Li coefficients | Criterion is universal in `n` | Uniform analytic proof for all `n` |
| `RH-F013` | Use the wrong prime error term | Near-looking estimates need not exclude off-line zeros | Exact exponent, logarithm, uniformity, and converse |
| `RH-F014` | Prove `M(x)=O(x^{1/2+epsilon_0})` for one epsilon | Criterion quantifies over every positive epsilon | Uniform family indexed by arbitrary epsilon |
| `RH-F015` | Substitute GRH evidence or a finite-field theorem | Different `L`-function or category | Explicit specialization theorem to classical `zeta` |
| `RH-F016` | Assume all zeros are simple | Simplicity is unproved and separate | Multiplicity-safe argument |
| `RH-F017` | Let a zero-free region approach `1/2` asymptotically | A region near `1` does not squeeze all zeros to the line | Uniform exclusion of every `beta>1/2` |
| `RH-F018` | Invoke Rouche without a boundary lower bound | Comparison may fail on the contour | Certified nonvanishing and strict inequality on boundary |
| `RH-F019` | Report a floating-point root off the line | Approximation and cancellation do not certify a zero | Interval enclosure plus exact zero count and line separation |
| `RH-F020` | Infer trivial or nontrivial zeros from one factor | Other factors may have poles or zeros | Local order calculation of the complete product |

Each seed is to become an executable semantic fixture in `RH-WP01`.

## 12. Claim ledger

| Claim ID | Claim | Status | Support | Promotion condition |
|---|---|---|---|---|
| `RH-C000` | Canonical RH is the critical-line statement for every nontrivial zero | `LITERATURE_DERIVED` | `SRC-RH-00` | Source concordance retained |
| `RH-C001` | `xi(s)` normalization is entire and symmetric | `LITERATURE_DERIVED` | `SRC-RH-04` | Analytic continuation interface imported explicitly |
| `RH-C002` | Nontrivial zeros correspond exactly to zeros of `xi` | `PROVED_IN_PACKAGE` conditional on standard continuation and gamma facts | Local factor accounting | Formal or textbook reconstruction |
| `RH-C003` | `Xi` real-zero formulation is equivalent to RH | `PROVED_IN_PACKAGE` | Linear change of variables | Notation lock retained |
| `RH-C004` | Counting equality for all heights is equivalent to RH | `PROVED_IN_PACKAGE` | Definitions of `N,N0` | Boundary and multiplicity conventions retained |
| `RH-C005` | Prime-counting square-root error is equivalent to RH | `LITERATURE_DERIVED` | `SRC-RH-00`, `SRC-RH-06` | Both directions reconstructed in WP02 |
| `RH-C006` | Li nonnegativity is equivalent to RH | `LITERATURE_DERIVED` | `SRC-RH-07`, `SRC-RH-08` | Strict/non-strict normalization locator resolved |
| `RH-C007` | Nyman-Beurling closure is equivalent to RH | `LITERATURE_DERIVED` | `SRC-RH-11` | Parameterization and span conventions resolved |
| `RH-C008` | Robin inequality is equivalent to RH | `LITERATURE_DERIVED` | `SRC-RH-09` | Primary theorem locator attached |
| `RH-C009` | Lagarias inequality is equivalent to RH | `LITERATURE_DERIVED` | `SRC-RH-10` | Full theorem reconstruction |
| `RH-C010` | Mertens epsilon-family estimate is equivalent to RH | `LITERATURE_DERIVED` | `SRC-RH-06` | Exact theorem locator and proof reconstructed |
| `RH-C011` | Weil positivity is equivalent to RH | `NEEDS_AUDIT` | `SRC-RH-00`, `SRC-RH-12` | Test class, transform, form, and both directions fixed |
| `RH-C012` | Finite computation cannot prove the global statement | `PROVED_IN_PACKAGE` | Quantifier analysis | None |

## 13. Trust quartet

### What is proved in this package?

- the equivalence between the `s`-plane critical-line statement and the real-zero statement for `Xi`;
- the equivalence between RH and equality of complete and critical-line zero counts for every admissible height under locked definitions;
- the logical insufficiency of finite verification, density-one results, symmetry alone, and partial positivity checks;
- the distinction between symmetric and self-adjoint operators;
- the required local factor accounting that separates `Lambda`, `xi`, the pole, and trivial zeros.

### What is source-checked?

- the official Bombieri statement and current Clay status;
- DLMF definitions, functional equation, and zero taxonomy;
- the prime-counting error equivalence as stated by Bombieri;
- the Li, Robin, Lagarias, Nyman-Beurling-Baez-Duarte, and sequential Riesz-like source statements;
- the existence of Weil's explicit-formula positivity lane.

### What remains open?

- RH itself;
- simplicity of zeros;
- all mechanism-generation routes;
- a Hilbert-Polya operator;
- all unproved positivity, approximation, arithmetic, or spectral bridges.

### What requires external verification or reconstruction?

- exact theorem locators and proof reconstruction for every literature-derived equivalence;
- the strict versus non-strict Li criterion convention;
- the selected Weil test class and sign convention;
- Nyman-Beurling parameterization and span normalization;
- the primary digital locator for Robin's paper;
- formal-library coverage for complex analysis, gamma, meromorphic continuation, zero counting, and explicit formulae.

## 14. Proof-debt register

| Debt ID | Class | Blocked node | Debt | Discharge condition |
|---|---|---|---|---|
| `RH-DT001` | `EXTERNAL_SOURCE` | `B014/B015` | Prime and Chebyshev error equivalence proof locators | Reconstruct both directions with endpoint conventions |
| `RH-DT002` | `SEMANTIC_CORRESPONDENCE` | `B016` | Li strict/non-strict and zero-sum regularization | Fix canonical theorem statement and derive coefficient identity |
| `RH-DT003` | `SEMANTIC_CORRESPONDENCE` | `B017` | Nyman-Beurling parameter and closure conventions | Match original and Baez-Duarte formulations explicitly |
| `RH-DT004` | `EXTERNAL_SOURCE` | `B018` | Robin primary theorem locator | Attach stable source and theorem statement |
| `RH-DT005` | `ANALYTIC_ESTIMATE` | `B020` | Mertens criterion converse details | Reconstruct Mellin/Perron bridge and epsilon quantifiers |
| `RH-DT006` | `SEMANTIC_CORRESPONDENCE` | `B021` | Weil test class, transform, and quadratic form | Produce exact formula and prove equivalence |
| `RH-DT007` | `FORMALIZATION_BLOCKER` | `T003/T006` | Meromorphic continuation and gamma infrastructure | Identify or build formal library interfaces |
| `RH-DT008` | `FORMALIZATION_BLOCKER` | `D011/B013` | Argument principle and multiplicity-aware zero counting | Formalize contour count under boundary nonvanishing |
| `RH-DT009` | `COMPUTATIONAL_REPLAY` | `O022` | Certified zero-enclosure schema | Specify interval arithmetic and winding certificate format |
| `RH-DT010` | `EXTERNAL_SOURCE` | `R030` | Current known-results and prior-art survey | Complete WP02 before target selection |

Unresolved debt is nonblocking for a source-normalization package only because it is explicit. It blocks use of the affected bridge as a proved programme theorem.

## 15. MATHCERT handoff

### 15.1 Candidate formal definitions

- meromorphic and entire functions on `C`;
- order of a zero or pole;
- zero multiset with multiplicity;
- affine critical-line map `t <-> 1/2+it`;
- conjugation and reflection actions;
- finite-region argument-principle certificate;
- abstract zero-count equality criterion;
- claim and source schemas for equivalence records.

### 15.2 Immediately formalizable lemmas

1. If an entire `xi` obeys `xi(s)=xi(1-s)` and conjugation symmetry, its zero multiset is invariant under the quartet maps.
2. Under the definition `Xi(t)=xi(1/2+it)`, zeros of `xi` on `Re(s)=1/2` correspond exactly to real zeros of `Xi`.
3. If `N(T)` counts all zeros and `N0(T)` counts the line subset with the same multiplicity and range, equality for every admissible `T` is equivalent to every zero lying on the line.
4. Finite equality `N0(T)=N(T)` implies only a bounded-height theorem.
5. A symmetric operator need not be self-adjoint; spectral promotion requires an explicit self-adjointness obligation.

### 15.3 Prohibited certification shortcut

MATHCERT may not postulate analytic continuation, the functional equation, all explicit-formula identities, or a positivity criterion as axioms and report the resulting conditional theorem as a proof of RH. Imported interfaces must remain visibly conditional and provenance-bearing.

## 16. Work Package sequence

### `RH-WP00` — source, normalization, and equivalence audit

Status: `repository review required`.

Required outputs now present:

- canonical charter;
- function-and-zero lock;
- source ledger;
- notation registry;
- symmetry and location ledger;
- exact equivalence catalogue;
- implication/non-implication matrix;
- theorem spine and dependency architecture;
- false-proof seeds;
- claim ledger;
- proof-debt register;
- MATHCERT boundary.

### `RH-WP01` — false-proof atlas

Status: closed until WP00 promotion.

Each seed `RH-F001` through `RH-F020` must become a minimal fixture containing:

- the tempting argument;
- the first invalid inference;
- an exact countermodel or failed hypothesis;
- the narrowest repair;
- what the failure does and does not rule out.

### `RH-WP02` — source-normalized theorem and barrier ledger

Status: closed until WP00 promotion.

It must reconstruct, rather than list:

- zero-free regions;
- zero-density estimates;
- critical-line proportion theorems;
- zero-counting and Turing methods;
- mean values and moments;
- mollifier results;
- explicit formulae;
- Li, Weil, Nyman-Beurling, Robin, Lagarias, Mertens, Riesz, and related criteria;
- Hilbert-Polya and trace-formula obligations;
- computational verification records and their exact certification class.

### `RH-WP03` — certified computational substrate

Status: closed.

Permitted later role:

- interval evaluation of `zeta`, `xi`, and derivatives;
- argument-principle counts;
- Turing-style completeness certificates;
- falsification of universal intermediate inequalities;
- reproducible counterexample search.

Finite computation remains nonterminal for a proof.

### `RH-WP04` — route and restricted-target selection

Status: closed.

A route may be selected only after WP01, WP02, and prior-art audit. It must name one exact bridge node, the missing theorem, its support route, known barriers, and a falsification plan.

## 17. Internal review record

The present pass applies the following office checks without claiming independent external review:

| Office | Finding |
|---|---|
| Axiomatist | Canonical function, domain, pole, zero taxonomy, multiplicity, and quantifiers are explicit |
| Cartographer | The theorem spine distinguishes definitions, imported theorems, equivalences, obstructions, and open target |
| Grammarian | `xi`, `Xi`, `Z`, `Lambda(s)`, and von Mangoldt `Lambda(n)` collisions are controlled |
| Verifier | Both directions are separately represented for each binding or source-bound equivalence |
| Adversary | Twenty recurrent false-proof modes are registered |
| Formalist | Conditional formalization boundary and first abstract lemmas are stated |
| Amanuensis | Source IDs, claim IDs, debt IDs, and companion artifacts are cross-referenced |
| Referee | Promotion remains withheld pending repository review, CI, and resolution or explicit acceptance of locator debt |

## 18. Exit gate

- [x] Official canonical target recorded.
- [x] `zeta`, `Lambda`, `xi`, `Xi`, and `Z` separated.
- [x] Pole, trivial zeros, nontrivial zeros, and multiplicity conventions fixed.
- [x] Symmetry maps proved or source-bound.
- [x] Core exact equivalences represented in both directions.
- [x] Neighboring statements and one-way implications separated.
- [x] Finite computation segregated from global proof.
- [x] False-proof seeds created.
- [x] Theorem spine, claim ledger, and proof debt created.
- [x] MATHCERT handoff boundary created.
- [ ] Repository review complete.
- [ ] CI and documentation checks complete.
- [ ] Referee promotion recorded.

## 19. Next controlled stage

After WP00 promotion, the only automatically authorized packages are:

- `RH-WP01`: false-proof atlas;
- `RH-WP02`: source-normalized theorem, criterion, computation, and barrier ledger.

They may proceed in parallel.

The following remain closed:

- mechanism generation detached from a selected bridge theorem;
- broad numerical searches without a falsification target;
- Hilbert-Polya construction claims;
- restricted-target selection;
- novelty claims;
- claimed-proof promotion.

## 20. First executable step

**Input:** false-proof seeds `RH-F001` through `RH-F020`.  
**Operation:** instantiate each as a minimal adversarial fixture and test it against the charter and function-and-zero lock.  
**Output:** `RH-WP01` fixture ledger with exact failing premise, countermodel or domain violation, and repair obligation.  
**Completion test:** every seed fails closed; no fixture can be mistaken for evidence against a valid route outside its stated scope.  
**Spine nodes advanced:** `RH-O022` through `RH-O028`.  
**Debt discharged:** none automatically; fixtures expose and classify debt rather than solve the open problem.