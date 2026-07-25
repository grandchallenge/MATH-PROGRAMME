# RH-WP00 — Function and Zero Lock

**Artifact ID:** `RH-WP00-02-FUNCTION-ZERO-LOCK`  
**Campaign:** `RH-001`  
**Challenge:** Riemann Hypothesis  
**Work Package:** `RH-WP00`  
**Status:** `LOCKED FOR WP00`  
**Version:** 0.1.0  
**Audit date:** 2026-07-25  
**Claim class:** `ANALYTIC-NORMALIZATION / NON-SOLUTION ARTIFACT`

---

## 1. Purpose

This file fixes the analytic objects, zero conventions, branch rules, counting functions, symmetry operations, and computational certificate boundary used throughout the Riemann Hypothesis campaign.

Its purpose is defensive. Many invalid arguments begin with a correct identity in one region and then use it outside that region, confuse two completed functions, discard a pole, count only detected critical-line zeros, or treat floating-point output as an exact zero statement.

## 2. Base complex conventions

Write

```math
s=\sigma+it,
\qquad
\sigma=\operatorname{Re}(s),
\qquad
t=\operatorname{Im}(s).
```

The symbol `i` denotes the square root of `-1` with positive imaginary orientation.

For a positive integer `n`,

```math
n^{-s}=\exp(-s\log n),
```

where `log n` is the ordinary real logarithm. There is no branch ambiguity in `n^{-s}`.

A complex logarithm `Log f(s)` is never used globally unless a branch has been constructed on a specified zero-free simply connected domain. The logarithmic derivative `f'/f` may be meromorphic even when no global logarithm exists.

## 3. The zeta function

### 3.1 Dirichlet-series definition

For `sigma>1`,

```math
\zeta(s)=\sum_{n=1}^{\infty}\frac{1}{n^s}.
```

The series converges absolutely and locally uniformly in this half-plane. Termwise differentiation is authorized only on compact subsets of an admitted uniform-convergence domain.

### 3.2 Euler product

For `sigma>1`,

```math
\zeta(s)=\prod_p(1-p^{-s})^{-1}.
```

The product and its logarithm are not authorized inside the critical strip by formal continuation of their factors. The meromorphic continuation of `zeta` is not the termwise continuation of the Euler product.

The Euler product gives zero-freeness for `sigma>1`. Zero-freeness on `sigma=1` is a separate theorem, not a consequence of absolute convergence.

### 3.3 Meromorphic continuation

The symbol `zeta(s)` outside `sigma>1` means the unique meromorphic continuation of the Dirichlet series. Its only pole is a simple pole at `s=1` with residue `1`.

Any representation used to continue `zeta` must carry its own domain, contour, remainder, and endpoint conditions. Equality by analytic continuation is authorized only after both sides are shown meromorphic on a connected domain and equal on a nonempty open subset.

## 4. Completed functions

### 4.1 Symmetric meromorphic completion

Define

```math
\Lambda(s)=\pi^{-s/2}\Gamma\!\left(\frac{s}{2}\right)\zeta(s).
```

This function is meromorphic and satisfies

```math
\Lambda(s)=\Lambda(1-s).
```

It has poles at `s=0` and `s=1`. It is not entire.

### 4.2 Riemann's entire completion

Define

```math
\xi(s)=\frac12 s(s-1)\Lambda(s)
      =\frac12 s(s-1)\pi^{-s/2}\Gamma\!\left(\frac{s}{2}\right)\zeta(s).
```

The factors `s(s-1)` remove the poles of `Lambda`. The resulting function is entire and satisfies

```math
\xi(s)=\xi(1-s).
```

The values at `s=0` and `s=1` are obtained by removable continuation; neither point is a zero of `xi`.

### 4.3 Critical-line reparametrization

Define

```math
\Xi(t)=\xi\!\left(\frac12+it\right).
```

`Xi` is an entire function of the complex variable `t`. The functional equation gives

```math
\Xi(-t)=\Xi(t).
```

Conjugation gives `Xi(t)` real for real `t`.

The programme reserves:

- `xi(s)` for the entire function in the `s`-plane;
- `Xi(t)` for the entire function in the `t`-plane.

### 4.4 Hardy's function

For real `t`, Hardy's function is conventionally written

```math
Z(t)=e^{i\vartheta(t)}\zeta\!\left(\frac12+it\right),
```

with a phase `vartheta(t)` chosen so that `Z(t)` is real.

`Z(t)` and `Xi(t)` are not the same function. Their real zeros correspond to zeros of `zeta` on the critical line, but sign changes detect only odd-order real zeros unless supplemented by multiplicity and zero-count information.

## 5. Gamma-factor and trivial-zero accounting

The functional equation may be written

```math
\zeta(s)
=
2^s\pi^{s-1}\sin\!\left(\frac{\pi s}{2}\right)
\Gamma(1-s)\zeta(1-s),
```

where both sides are interpreted meromorphically.

The factor `sin(pi s/2)` vanishes at the even integers. At the negative even integers

```math
s=-2,-4,-6,\ldots,
```

these zeros yield the trivial zeros of `zeta` after the remaining factors are accounted for.

A proof may not infer zeros merely by identifying a vanishing factor in a product that also contains poles. Orders must be added algebraically after local Laurent expansions or a valid divisor calculation.

## 6. Zero taxonomy

### 6.1 Trivial zeros

The trivial zeros are

```math
-2,-4,-6,\ldots.
```

They are excluded from the Riemann Hypothesis target.

### 6.2 Nontrivial zeros

A nontrivial zero is any zero of `zeta` not in the trivial-zero list. Equivalently, it is a zero of `xi`.

The classical location theorem states that every nontrivial zero lies in

```math
0<\operatorname{Re}(s)<1.
```

This uses more than the Euler product: zero-freeness on `Re(s)=1` is a theorem of Hadamard and de la Vallee Poussin, and the opposite boundary follows through the functional equation and trivial-zero analysis.

### 6.3 Multiplicity

For a holomorphic function `f`, a zero `rho` has multiplicity `m` when

```math
f(s)=(s-\rho)^m g(s)
```

near `rho`, with `g(rho) != 0`.

All zero sums and counts must state whether multiplicity is included. The default for this campaign is **with multiplicity**.

RH does not assert that the zeros are simple.

## 7. Zero symmetries

### 7.1 Conjugation symmetry

Because the Dirichlet series has real coefficients for `sigma>1` and the identity extends meromorphically,

```math
\zeta(\overline{s})=\overline{\zeta(s)}.
```

Thus

```math
\rho\mapsto\overline{\rho}
```

preserves the nontrivial-zero multiset and multiplicity.

### 7.2 Functional-equation symmetry

The equation

```math
\xi(s)=\xi(1-s)
```

implies

```math
\rho\mapsto1-\rho
```

preserves the zero multiset and multiplicity.

### 7.3 Quartet structure

Combining the two symmetries gives

```math
\rho,
\quad\overline{\rho},
\quad1-\rho,
\quad1-\overline{\rho}.
```

These may collapse to fewer distinct points when a zero lies on the real axis or critical line.

Symmetry about a line does not imply that every point lies on that line. The quartet structure is compatible with off-line zeros.

## 8. Counting conventions

Let `rho=beta+i gamma` range over nontrivial zeros with multiplicity.

For `T>0` not equal to a zero ordinate, define

```math
N(T)=\#\{\rho:0<\gamma<T\}.
```

Define

```math
N_0(T)=\#\{\rho:0<\gamma<T,\ \beta=1/2\}.
```

Alternative endpoint conventions such as `0<gamma<=T` are admissible only when stated and used consistently. At a boundary ordinate, half-weight or limiting conventions must be explicit.

Under the locked definitions,

```math
\mathrm{RH}
\iff
N_0(T)=N(T)
\quad\text{for every admissible }T>0.
```

A statement such as `N_0(T)/N(T) -> 1` is strictly weaker: a zero-density exceptional set may still contain infinitely many off-line zeros.

## 9. Logarithmic derivative and explicit-formula hygiene

For `sigma>1`, absolute convergence gives

```math
-\frac{\zeta'}{\zeta}(s)
=
\sum_{n=1}^{\infty}\frac{\Lambda(n)}{n^s},
```

where `Lambda(n)` is the von Mangoldt function.

After meromorphic continuation, `-zeta'/zeta` has singularities induced by:

- the pole of `zeta` at `s=1`;
- every zero of `zeta`, with residue equal to minus its multiplicity under this sign convention;
- gamma and completion terms when one rewrites the completed logarithmic derivative.

An explicit formula is not a formal equality of divergent sums. Every version must specify:

1. the test-function class;
2. transform convention;
3. contour and orientation;
4. truncation or symmetric summation of zeros;
5. treatment of the pole and trivial zeros;
6. endpoint values at prime powers;
7. convergence mode; and
8. whether zeros are counted with multiplicity.

## 10. Prime-counting notation

The following functions are not interchangeable:

```math
\pi(x)=\#\{p\le x:p\text{ prime}\},
```

```math
\vartheta(x)=\sum_{p\le x}\log p,
```

```math
\psi(x)=\sum_{n\le x}\Lambda(n),
```

and weighted prime-power counting functions customarily denoted `J(x)` or `Pi(x)`.

The logarithmic integral must carry its convention. For the prime-number theorem and RH-equivalent estimate, one may use the offset form

```math
\operatorname{Li}(x)=\operatorname{PV}\int_0^x\frac{dt}{\log t}
```

or the equivalent integral from `2` plus a fixed constant. Big-O statements are unaffected by the constant, but exact formulae are not.

## 11. Branch and contour lock

Every contour argument must record:

- an oriented contour with no zero or pole on its boundary;
- the branch of every logarithm used along the contour;
- indentation or limiting rules near singularities;
- horizontal and vertical boundary estimates;
- the order in which limits are taken;
- whether an infinite rectangle is approached through admissible heights;
- the residues of the pole, trivial zeros, and nontrivial zeros;
- any cancellation that depends on symmetric truncation.

Moving a contour across a zero or pole changes the expression by its residue. A deformation is not valid merely because the endpoints remain fixed.

## 12. Equivalent-criterion lock

A claimed RH equivalence must be represented as two separate implications:

```text
RH -> criterion
criterion -> RH
```

Each implication must record:

- exact quantifiers;
- constants and their allowed dependence;
- endpoint and exceptional-set conventions;
- function spaces and norm;
- closure topology;
- convergence or summability convention;
- zero multiplicity convention;
- source and theorem locator;
- whether the proof uses an intermediate equivalence.

The phrase `equivalent to RH` is prohibited when only one implication has been checked.

## 13. Computational certificate lock

### 13.1 Non-certifying evidence

The following are exploratory unless enclosed in a rigorous error analysis:

- a floating-point value of `zeta(s)` close to zero;
- Newton or secant convergence;
- a plot of `Z(t)` or `Xi(t)`;
- a sign-change scan;
- agreement with tabulated ordinates;
- positive values of finitely many Li coefficients;
- a numerical prime-counting inequality over a finite range.

### 13.2 Certified zero enclosure

A theorem-grade zero enclosure must provide a region `D` and a proof, for example through the argument principle or Rouche's theorem, of the exact number of zeros in `D`, counted with multiplicity.

The certificate must include:

- interval or ball arithmetic with outward rounding;
- a boundary on which the relevant function is certified nonzero;
- a winding-number or comparison-function proof;
- exact treatment of poles;
- a reproducible precision and subdivision policy;
- a check that the region lies in the intended strip; and
- for a refutation candidate, a certified positive distance from `Re(s)=1/2`.

### 13.3 Finite-height verification

To certify RH through height `T`, one must show both:

1. the detected critical-line zeros are genuine, with multiplicity; and
2. their total count equals an independently certified count of **all** nontrivial zeros in the region.

Sign changes alone can miss even-multiplicity zeros. A total zero count without locating them on the line can miss off-line pairs.

No finite `T` proves the global hypothesis.

## 14. Notation registry

| Symbol | Locked meaning |
|---|---|
| `s=sigma+it` | Complex zeta variable |
| `rho=beta+i gamma` | Nontrivial zero, normally counted with multiplicity |
| `zeta(s)` | Meromorphic continuation of the Dirichlet series |
| `Lambda(s)` | `pi^{-s/2} Gamma(s/2) zeta(s)` |
| `xi(s)` | Entire completed function `1/2 s(s-1)Lambda(s)` |
| `Xi(t)` | `xi(1/2+it)` |
| `Z(t)` | Hardy's real-valued critical-line function |
| `Lambda(n)` | Von Mangoldt function; distinguished by integer argument |
| `N(T)` | All nontrivial zeros in the stated ordinate range |
| `N_0(T)` | Critical-line zeros in the same range |
| `pi(x)` | Prime-counting function |
| `theta(x)` | Sum of `log p` over primes up to `x` |
| `psi(x)` | Sum of von Mangoldt weights up to `x` |
| `Li(x)` | Logarithmic integral with declared convention |

## 15. Adversarial rejection tests

A submission fails this lock if it:

1. uses the Dirichlet series where it does not converge;
2. uses the Euler product inside the critical strip without a new proved representation;
3. calls `Lambda(s)` entire;
4. identifies `xi(s)`, `Xi(t)`, and `Z(t)`;
5. treats `s=1` as a zero;
6. counts trivial zeros as counterexamples;
7. infers the critical line from quartet symmetry;
8. ignores multiplicities;
9. equates sign changes with the total zero count;
10. continues `Log zeta` through a zero;
11. deforms a contour across singularities without residues;
12. interchanges infinite sums, products, derivatives, or integrals without a convergence theorem;
13. replaces a universal criterion by a finite check;
14. reports an approximate root as a certified zero;
15. imports GRH or simplicity under the name RH; or
16. claims a spectral proof from symmetry rather than self-adjointness and exact spectral correspondence.

## 16. Claim boundary

This lock establishes notation and admissibility rules only. It does not prove a new property of `zeta`, improve a zero-free region, verify a new height, establish an equivalent criterion, or advance the truth status of RH.