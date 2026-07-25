# LOG-GCD prior-art audit

## Determination

| Question | Finding |
|---|---|
| Is positivity of `log(gcd(m,n))` mathematically novel? | **No. Novelty is not supported.** |
| Is the divisor-indicator feature factorization novel? | **No. It is the classical GCD-matrix incidence factorization.** |
| Is this the first Lean formalization? | **Not established.** |
| What may GCL claim? | A checked Lean formalization and explicit `Finsupp` realization of a classical result. |

## Governing criterion

For an arithmetical function `f`, the associated GCD matrix has entries

```text
f(gcd(x_i,x_j)).
```

Classical GCD-matrix theory factors this matrix through divisor incidence:

```text
[f(gcd(x_i,x_j))] = E diag((f * μ)(d)) Eᵀ,
```

where `E_{i,d}` records whether `d` divides `x_i`. A standard positivity
criterion is therefore

```text
(f * μ)(d) ≥ 0 for every d.
```

For `f(n)=log n`, Möbius inversion gives

```text
(log * μ)(d) = Λ(d) ≥ 0.
```

This is exactly the mechanism used by `LOG-GCD-001`. The Lean feature vector

```text
φ(n)_d = sqrt(Λ(d)) [d | n]
```

makes the columns of the classical incidence factorization explicit.

## Governing literature

The audit records the following line of prior work:

- H. J. S. Smith, “On the value of a certain arithmetical determinant,”
  *Proceedings of the London Mathematical Society* 7 (1875/76), 208–212.
- Scott Beslin and Steve Ligh, “Greatest common divisor matrices,” *Linear
  Algebra and its Applications* 118 (1989), 69–76.
- Keith Bourque and Steve Ligh, “Matrices associated with arithmetical
  functions,” *Linear and Multilinear Algebra* 34 (1993), 261–267.
- Mika Mattila and Pentti Haukkanen, “A Notion of Positive Definiteness for
  Arithmetical Functions,” in *Matrices, Statistics and Big Data*, Springer
  (2019), 61–74.
- Vesa Kaarnioja, Pentti Haukkanen, Pauliina Ilmonen, and Mika Mattila,
  “Positive definite functions on semilattices,” arXiv:1804.03047 (2018).

Mattila and Haukkanen give the explicit if-and-only-if characterization by
nonnegativity of `f * μ`; this directly subsumes the logarithm case.

## Formalization-priority boundary

A bounded public search located the upstream Lean repository already credited
by the fixture and did not locate an earlier exact public artifact. This does
not establish first-formalization priority. Public indexing is incomplete,
private work is invisible, and equivalent declarations may use different
names.

Accordingly, the following descriptions are prohibited:

- new theorem;
- novel positive-definite kernel;
- first proof;
- first feature representation;
- first Lean formalization.

## Programme conclusion

The mathematical result belongs to prior art. The programme contribution is a
governed, replayable formal artifact with explicit provenance, a first-class
finitely supported feature map, and machine-enforced limits on what may be
claimed.

The full audit and machine-readable record live with fixture `LOG-GCD-001` as
`PRIOR_ART_AUDIT.md` and `prior_art_audit.json`.
