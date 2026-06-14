# RAD-NIL-002: Radical membership and model-class boundary

## Source claim

For every field extension `K` of `QQ`:

```text
x^2 = 0  implies  x = 0.
```

This fixture tests a different certificate level from `UF-INV-001`. The target
`x` is not in the ideal `(x^2)`, but it is in its radical.

## Exact certificate

The radical-membership witness is:

```text
x^N = 1 * (x^2), where N = 2.
```

The exponent is part of the proof object. Reclassifying this as ordinary ideal
membership would make a stronger and false algebraic claim.

`ci/check_radical_fixture.py` independently computes the target power and
checks it against the exact generator combination over rational coefficients.

## Semantic boundary

The source theorem is valid over fields because fields are integral domains and
have no nonzero nilpotents.

It is false over arbitrary commutative `QQ`-algebras. In:

```text
QQ[epsilon]/(epsilon^2)
```

the class of `epsilon` is nonzero but its square is zero.

The fixture therefore records both:

- the field-level theorem as `AUDITED`; and
- the arbitrary-ring generalization as `REFUTED`.

## Adversarial tests

The suite rejects:

- a missing or zero radical exponent;
- exponent `N = 1`;
- reclassification as ordinary ideal membership;
- a broadened model class;
- an altered target;
- a false certificate hash;
- promotion of the source theorem to `CERTIFIED`;
- removal of the refuted arbitrary-ring boundary.
