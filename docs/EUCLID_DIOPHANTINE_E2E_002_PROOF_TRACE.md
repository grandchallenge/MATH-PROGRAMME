# Linear Diophantine equations: one witness and one obstruction

## Begin with two concrete tasks

We use the same coefficients in both equations:

1. Find integers `x` and `y` such that `252x + 105y = 84`.
2. Decide whether integers `x` and `y` can satisfy `252x + 105y = 20`.

The first equation has a constructive witness. The second has a checkable obstruction. Neither conclusion depends on a search timeout.

## 1. The object

The object is an integer equation `a*x + b*y = c`. For the admitted modern theorem, `(a,b)` is not `(0,0)`.

## 2. The protected construction

Stage 2 reuses the protected Stage 1 gcd and Bézout spine. It does not define a second gcd procedure.

- `gcd(252,105) = 21`;
- `21 = -2 * 252 + 5 * 105`.

## 3. Constructive witness for target 84

Because `84 = 4 * 21`, multiply the protected Bézout coefficients by four:

- `x = -8`;
- `y = 20`.

Then `84 = -8 * 252 + 20 * 105`.

Thus `(-8,20)` is a directly checkable witness for `252x + 105y = 84`.

## 4. Divisibility obstruction for target 20

Every integer combination of `252` and `105` is divisible by `21`.

Exact division gives `20 = 0 * 21 + 20` with `0 < 20 < 21`.

The nonzero remainder proves that `21` does not divide `20`; therefore no integer pair solves `252x + 105y = 20`. This is an arithmetic obstruction, not a failed search and not a timeout.

## 5. The certified modern theorem

For integers `a`, `b`, and `c`, with a nonzero coefficient pair:

`(∃ x y : ℤ, a * x + b * y = c) ↔ a.gcd b ∣ c.natAbs`.

The Lean declarations include:

- `MathCert.NumberTheory.linearDiophantine_iff_gcdDvdNatAbs`;
- `MathCert.NumberTheory.diophantine25210584`;
- `MathCert.NumberTheory.obstruction25210520`;
- `MathCert.NumberTheory.noDiophantine25210520`;
- `MathCert.NumberTheory.zeroTargetSolvable`.

## 6. Independent certificate checks

The MATHCERT checker does not import or execute the MATHSOLVE producer. It checks exact protected identities, the scaled witness, the quotient-remainder obstruction, strict remainder bounds, signed and zero-target semantics, and the prohibition on timeout-as-unsatisfiability.

The protected certification disposition is `CERTIFIED_LINEAR_DIOPHANTINE_EQUIVALENCE_AND_BOUNDED_EXEMPLARS`.

## 7. Exact authority chain

- MATHFORGE: `af5398a05f17789a061ab0d23c2b47f0cc952fff`;
- MATHSOLVE: `66d54d375ae4dfc148888325b6093818669e7c02`;
- MATHCERT: `cd69013cf55d4ee96539d28ee27eadef64cca06f`;
- protected Stage 1 Programme closeout: `183ff2a0adfbe5bd0ffd5f2e638089b94b868c54`.

## Claim labels

**Theorem.** Solvability of the admitted two-variable integer equation is equivalent to divisibility by the normalized gcd.

**Certified evidence.** `(-8,20)` solves the target-84 instance; the nonzero remainder `20` modulo `21` obstructs the target-20 instance.

**Interpretation.** A constructive witness and a negative obstruction are different certificate forms for the same divisibility criterion.

**Nonclaim.** This does **not** establish completeness for arbitrary Diophantine equations, novelty, priority, first formalization, or verbatim Euclidean attribution.

## Stage 3 boundary

The Book VII micro-edition is not activated by this page. Stage 3 still requires exact historical source acquisition, hashing, licensing or public-domain basis, proposition-level concordance, independent review, and separate Human Steward authority.
