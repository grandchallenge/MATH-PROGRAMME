# LOG-GCD-001 prior-art audit

## Audit status

| Field | Determination |
|---|---|
| Audit date | 2026-07-23 |
| Mathematical novelty | **NOT SUPPORTED** |
| Feature-factorization novelty | **NOT SUPPORTED** |
| Lean-artifact priority | **NOT ESTABLISHED** |
| Permitted description | A GCL-certified Lean formalization and explicit `Finsupp` realization of a classical GCD-matrix positivity criterion |
| Prohibited description | New theorem, novel kernel, first proof, or first formalization |

## Question audited

For positive integers `m,n`, consider

```text
K(m,n) = log(gcd(m,n)).
```

The fixture proves that every finite Gram matrix of `K` is positive
semidefinite and realizes the kernel through divisor coordinates

```text
phi(n)_d = sqrt(Lambda(d)) [d | n].
```

The audit asks whether either the positivity theorem or this feature
factorization supports a mathematical novelty claim.

## Determination

It does not.

The result is an immediate specialization of the established theory of GCD
matrices associated with an arithmetical function `f`. The relevant general
factorization is

```text
[f(gcd(x_i,x_j))] = E diag((f * mu)(d)) E^T,
```

where `E_{i,d} = [d | x_i]`. Consequently, positivity follows whenever the
Möbius transform `f * mu` is nonnegative. Taking `f(n)=log n` gives

```text
(log * mu)(d) = Lambda(d) >= 0,
```

which is exactly the factorization and proof used by `LOG-GCD-001`.

The new Lean module makes the columns of this classical incidence
factorization explicit as a finitely supported feature map. That is a useful
formal artifact, but not a new mathematical mechanism.

## Closest and governing prior art

### 1. Smith's GCD determinant

H. J. S. Smith, “On the value of a certain arithmetical determinant,”
*Proceedings of the London Mathematical Society* 7 (1875/76), 208–212.

Smith's determinant is the historical origin of the divisor-incidence
factorizations underlying GCD matrices. It establishes that this matrix class
is classical rather than newly introduced here.

### 2. Positive definiteness of GCD matrices

Scott Beslin and Steve Ligh, “Greatest common divisor matrices,” *Linear
Algebra and its Applications* 118 (1989), 69–76.
DOI: `10.1016/0024-3795(89)90572-7`.

This work initiated the modern study of finite GCD matrices and established
their positive-definiteness properties. It covers the identity-function kernel
and is foundational background rather than the closest exact specialization.

### 3. Matrices associated with general arithmetical functions

Keith Bourque and Steve Ligh, “Matrices associated with arithmetical
functions,” *Linear and Multilinear Algebra* 34 (1993), 261–267.
DOI: `10.1080/03081089308818225`.

This paper studies matrices with entries `f(gcd(x_i,x_j))` and gives
conditions on `f` guaranteeing positivity. The divisor-incidence/diagonal
factorization used in the present fixture belongs to this established line.

### 4. Explicit Möbius-transform characterization

Mika Mattila and Pentti Haukkanen, “A Notion of Positive Definiteness for
Arithmetical Functions,” in *Matrices, Statistics and Big Data*, Springer
(2019), 61–74. DOI: `10.1007/978-3-030-17519-1_5`.

Their Theorem 4.3 states that an arithmetical function `f` is positive
definite in the GCD-matrix sense if and only if

```text
(f * mu)(k) >= 0
```

for every positive integer `k`. Their proof uses the factorization
`E D E^T`, with `D = diag((f * mu)(k))`. The logarithm case follows by the
standard identity `log * mu = Lambda` and nonnegativity of the von Mangoldt
function.

This result directly subsumes the mathematical theorem in `LOG-GCD-001`.

### 5. Semilattice generalization

Vesa Kaarnioja, Pentti Haukkanen, Pauliina Ilmonen, and Mika Mattila,
“Positive definite functions on semilattices,” arXiv:`1804.03047` (2018).

This work places meet matrices, including GCD matrices, in a general
semilattice framework and derives positivity through incidence-algebra and
`LDL^T` structure. It further confirms that the divisor-feature construction
is an instance of a broader established mechanism.

### 6. Related stronger and adjacent results

Shaofang Hong, “Infinite divisibility of Smith matrices,” *Acta Arithmetica*
134 (2008), 381–386; arXiv:`0808.3550`.

Dominique Guillot and JiaRu Wu, “Total nonnegativity of GCD matrices and
kernels,” *Linear Algebra and its Applications* 578 (2019), 446–461;
arXiv:`1901.01947`.

These works study stronger Hadamard-power and total-nonnegativity properties
of related GCD kernels. They are not needed for the logarithmic-kernel proof,
but delimit the surrounding literature.

## Independent structural derivation

Prime valuations give a second standard route:

```text
log(gcd(m,n)) = sum_p log(p) min(v_p(m), v_p(n)).
```

For each prime `p`, the kernel `min(a,b)` on nonnegative integers is the Gram
kernel of initial-segment indicators. The logarithmic GCD kernel is therefore
a nonnegative weighted sum of classical `min` kernels. This is equivalent to
the divisor/von-Mangoldt representation and supplies no independent novelty
claim.

## Formalization search

The bounded search included:

- exact searches for `logGcd_posSemidef`;
- combinations of “log gcd”, “positive semidefinite”, “Lean”, and
  “von Mangoldt”;
- GitHub and public web indexing;
- inspection of the relevant mathlib number-theory support.

The only exact public Lean artifact located was the upstream source already
credited by this fixture:

```text
irregular-rhomboid/log-gcd-lean
```

This negative search result is not proof of first formalization. Repository
indexing is incomplete, private developments are invisible, and equivalent
formal statements may use different names. Therefore the programme records
only:

```text
No earlier public Lean formalization was located in the bounded audit.
Priority remains NOT ESTABLISHED.
```

## Claim policy after audit

The following statements are supported:

- the mathematical theorem is a classical corollary of the general
  GCD-matrix Möbius-transform criterion;
- the GCL artifact supplies a checked Lean proof and an explicit finitely
  supported feature-map declaration;
- the repository preserves provenance, claim boundaries, and replay evidence.

The following statements remain prohibited:

- “new positive-definite kernel”;
- “novel proof of positivity”;
- “first feature representation”;
- “first Lean formalization”;
- any priority assertion without a substantially broader specialist audit.

## Audit conclusion

`LOG-GCD-001` should be presented as a formalization and certification result,
not as a mathematical discovery. The prior-art obligation is discharged by a
negative novelty determination, not by permission to make a novelty claim.
