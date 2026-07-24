# BSD-WP00 — Statement lattice and equivalence boundary

## 1. Purpose

The phrase “the Birch–Swinnerton-Dyer conjecture” is routinely used for several related statements. This artifact fixes their logical identities and prevents a theorem about one component from being reported as a theorem about the whole bundle.

Throughout, let `E/Q` be an elliptic curve, let

```math
r_{\mathrm{alg}}=\operatorname{rank}_{\mathbb Z}E(\mathbb Q),
\qquad r_{\mathrm{an}}=\operatorname{ord}_{s=1}L(E,s),
```

and let `p` be a prime.

## 2. Canonical nodes

### `R` — rank BSD

```math
r_{\mathrm{alg}}=r_{\mathrm{an}}.
```

### `F` — finiteness of the Tate–Shafarevich group

```math
\#\Sha(E/\mathbb Q)<\infty.
```

### `L` — strong complex leading-term formula

With the normalization in `07_NORMALIZATION_REGISTRY.yaml`,

```math
\frac{L^{(r)}(E,1)}{r!}
=
\frac{\Omega_E\operatorname{Reg}_E\#\Sha(E/\mathbb Q)\prod_\ell c_\ell}
{\#E(\mathbb Q)_{\mathrm{tors}}^2},
\qquad r=r_{\mathrm{alg}}=r_{\mathrm{an}}.
```

The formula includes `R` and presupposes the finite arithmetic quantity in `F`. A source that calls this “BSD” must be tagged `BSD-LEAD-Q`, not merely `BSD-RANK-Q`.

### `S_p` — p-primary Selmer corank statement

```math
\operatorname{corank}_{\mathbb Z_p}\operatorname{Sel}_{p^\infty}(E/\mathbb Q)=r_{\mathrm{an}}.
```

The exact sequence

```math
0\to E(\mathbb Q)\otimes\mathbb Q_p/\mathbb Z_p
\to\operatorname{Sel}_{p^\infty}(E/\mathbb Q)
\to\Sha(E/\mathbb Q)[p^\infty]\to0
```

gives

```math
S_p
\iff
r_{\mathrm{alg}}+\operatorname{corank}_{\mathbb Z_p}\Sha(E/\mathbb Q)[p^\infty]=r_{\mathrm{an}}.
```

Thus `S_p` is not textually identical to `R`.

### `F_p` — finite p-primary Tate–Shafarevich part

```math
\#\Sha(E/\mathbb Q)[p^\infty]<\infty.
```

Equivalently, its `Z_p`-corank vanishes.

### `P_p` — p-Selmer parity

```math
(-1)^{\operatorname{corank}_{\mathbb Z_p}\operatorname{Sel}_{p^\infty}(E/\mathbb Q)}=w(E),
```

where `w(E)` is the global root number. Via the functional equation,

```math
(-1)^{r_{\mathrm{an}}}=w(E).
```

This identifies parity only. It does not determine either rank exactly.

### `L_p` — a p-part or p-adic leading-term theorem

This symbol is not a single universal statement. Every use must specify:

- complex or `p`-adic `L`-function;
- ordinary, split multiplicative, or supersingular reduction;
- cyclotomic, anticyclotomic, or multivariable setting;
- primitive or imprimitive Euler factors;
- exceptional-zero correction;
- valuation identity, characteristic ideal, or exact leading coefficient;
- residual and local hypotheses.

An unqualified node `L_p` is inadmissible in a promoted proof graph.

## 3. Valid implication records

The following are formal or theorem-conditioned implications.

```text
L  ->  R and F
S_p + F_p  ->  R
R + F_p  ->  S_p
F  ->  F_p for every p
R  ->  parity(r_alg) = parity(r_an)
functional equation  ->  parity(r_an) determined by w(E)
P_p + F_p  ->  parity(r_alg) = parity(r_an)
```

The first line means that the full strong formula entails the equality of the order used in the formula with the Mordell–Weil rank and contains a finite `Sha` factor under the adopted formulation. It does not mean that every paper proving a valuation identity has proved `L`.

## 4. Forbidden automatic implications

None of the following arrows may appear without an explicit additional theorem:

```text
P_p  -/->  R
functional-equation sign  -/->  exact analytic rank
S_p  -/->  R
R  -/->  F
R + F  -/->  L
one-prime p-part  -/->  L
p-adic order of vanishing  -/->  complex order of vanishing
infinitely many twists  -/->  every elliptic curve
positive density  -/->  universal statement
finite conductor verification  -/->  universal statement
analytic rank <= 1 theorem  -/->  higher-rank theorem
```

## 5. Low-rank theorem lane

The admitted operational low-rank interface is:

```text
r_an = 0  ->  r_alg = 0 and Sha finite
r_an = 1  ->  r_alg = 1 and Sha finite
```

for elliptic curves over `Q`, using modularity together with the Gross–Zagier–Kolyvagin theorem chain and its rank-zero companions. WP02 must replace this compressed interface with exact source statements, hypotheses, and theorem-number concordance.

The converse direction is not globally admitted as a theorem node. Restricted `p`-converse results receive separate records with their full hypotheses.

## 6. Quantifier lattice

Results must carry one of the following scopes:

```text
INDIVIDUAL_CURVE
FINITE_DATABASE
PARAMETRIC_FAMILY
INFINITE_TWIST_SUBFAMILY
POSITIVE_PROPORTION
DENSITY_ONE
ALL_CURVES_IN_A_RESTRICTED_CLASS
ALL_ELLIPTIC_CURVES_OVER_Q
```

Moving upward in this list is never automatic. In particular, cardinal infinity is not a substitute for universality.

## 7. Promotion rule

A future claim may use the unqualified label “BSD proved” only when its artifact identifies which of `R`, `F`, and `L` is established, states the domain and quantifier, and discharges every imported interface. Otherwise the claim must use the exact lane identifier.
