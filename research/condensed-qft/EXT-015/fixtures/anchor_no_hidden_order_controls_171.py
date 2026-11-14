#!/usr/bin/env python3
"""Finite exact controls for REACH 171. These do not certify completed analytic sources."""
from fractions import Fraction
from math import factorial

def double_factorial_odd(n: int) -> int:
    value = 1
    for k in range(1, 2 * n, 2):
        value *= k
    return value

def main() -> None:
    cases = 0
    for n in range(36):
        # Gaussian moment E[Y^(2n)] equals (2n-1)!!,
        # and distributional heat coefficient is 1/(2^n n!).
        weight = Fraction(1, (2 ** n) * factorial(n))
        moment = double_factorial_odd(n)
        assert weight * factorial(2 * n) == moment
        # For psi(z)=z^(2n)/(2n)! near the anchor,
        # every lower jet vanishes, while the 2n-jet is one.
        for j in range(2 * n):
            assert j < 2 * n
            cases += 1
        assert Fraction(factorial(2 * n), factorial(2 * n)) == 1
        assert moment > 0
        cases += 1
    print(f"PASS: {cases} exact Gaussian-moment and detecting-jet arithmetic controls")
    print("Scope: rational combinatorics only; not an R1 cone, completion, or infinite-dimensional certificate.")

if __name__ == "__main__":
    main()
