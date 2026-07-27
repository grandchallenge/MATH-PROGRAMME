# Proofs and classified computations

## Proofs reconstructed in the monograph

1. The union of all members of a finite nonempty union-closed family belongs to the family.
2. The powerset half-threshold is sharp by a fixed-point-free toggle involution.
3. A singleton member yields an abundant element by an injective union map.
4. Complementation translates union closure to intersection closure under a fixed universe.

These are pedagogical reconstructions and do not approach the universal open step.

## Imported formal results

The source lock imports, without duplicating their proofs:

- powerset sharpness and elementary support lemmas;
- singleton and two-element-member cases;
- exact `n <= 4` replay;
- the checked finite-lattice spine through `UC-WP05-L016`;
- hybrid package `UC-WP05-C015`.

## Classified computation

| Item | Arithmetic mode | Class | Supported claim |
|---|---|---|---|
| PDF byte length and SHA-256 | exact bytes / SHA-256 | `REGRESSION_AUDIT` | release identity |
| TeX byte length and SHA-256 | exact bytes / SHA-256 | `REGRESSION_AUDIT` | release identity |
| Source-bundle byte length and SHA-256 | exact bytes / SHA-256 | `REGRESSION_AUDIT` | release identity |
| Union-closed `n <= 4` certificate | finite Boolean/integer | `EXACT_FINITE_VERIFICATION` | bounded nonexistence of counterexamples |

No floating-point output is used as theorem-grade support.
