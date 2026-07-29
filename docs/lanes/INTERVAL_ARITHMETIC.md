# Interval Arithmetic to Certified Bound

## Obligation

Use this lane for an explicit enclosure or inequality on a declared domain. The expression, variables, domain, precision, outward-rounding mode, backend, and subdivision policy must be fixed.

## MATHFORGE

MATHFORGE identifies a suitable enclosure problem, locates singularities and excluded regions, tests subdivisions, and emits an interval trace with backend provenance.

## MATHSOLVE

MATHSOLVE checks that the enclosure implies the intended local mathematical step. It chooses the domain decomposition and rejects sampled extrema or unsupported monotonicity arguments.

## MATHCERT

MATHCERT replays outward-rounded arithmetic, checks domain coverage and subdivision joins, and verifies that the final enclosure implies the named bound.

## Allowed statuses

`configured`, `enclosed`, `subdivision_required`, `ready_for_mathcert`, `rejected`.

## Rejection policy

Reject missing precision or rounding information, hidden singularities, incomplete domain coverage, and floating-point samples presented as interval certificates.

## Package

The package root is `lanes/interval_arithmetic`. Its toy fixture encloses `x^2` by `[0,1]` on `x in [0,1]`.

## Claim boundary

A replayed interval computation proves only the stated enclosure on the stated domain under the exact arithmetic contract.
