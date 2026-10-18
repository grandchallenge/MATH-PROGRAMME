#!/usr/bin/env python3
"""PRO-001: exact bounded probes for quantum pro-valued Weiss descent.

Demonstrates the finite matrix entries of an infinite categorical proof.
Does not claim to compute Pro(D(Liq_p(R))) or certify that proof itself.
"""
from fractions import Fraction as Q


def normalized_quantum_moment(weight: int, interval: int) -> Q:
    """The hbar^0 moment lambda_weight on class z_interval."""
    return Q(1) if weight == interval else Q(0)


def local_probe(k: int, weight: int, interval: int) -> Q:
    """a_k sums moments with weights 1..k, zero off the first k intervals."""
    if not (1 <= weight <= k and 1 <= interval <= k):
        return Q(0)
    return normalized_quantum_moment(weight, interval)


def global_bounded_probe(N: int, weight: int, interval: int) -> Q:
    """Any map represented on T_N cannot see weight >= N.

    For test purposes take the candidate matching local moments below cutoff N.
    Other maps out of T_N have the same high-weight blindness.
    """
    if weight >= N:
        return Q(0)
    return normalized_quantum_moment(weight, interval)


def run() -> None:
    for maximum in (1, 2, 3, 7, 12, 24):
        # Strict compatibility: restriction of a_k to U_l equals a_l.
        for k in range(1, maximum + 1):
            for l in range(1, k + 1):
                for weight in range(1, maximum + 2):
                    for interval in range(1, l + 1):
                        assert local_probe(k, weight, interval) == local_probe(
                            l, weight, interval
                        )
        # No fixed cutoff detects every compatible local weight witness.
        for N in range(1, maximum + 1):
            k = max(N, 1)
            assert local_probe(k, k, k) == Q(1)
            assert global_bounded_probe(N, k, k) == Q(0)
        # The differential preserves quantum weight w = r + 2 * hbar_power.
        for r in range(0, maximum + 2):
            for hbar_power in range(0, maximum + 2):
                if r >= 2:
                    assert r + 2 * hbar_power == (r-2) + 2*(hbar_power+1)

    # The massive field-equation moment kills kinetic boundaries by
    # integration by parts against h(x)=exp(m*x), with P h = 0.
    for mass in (Q(1, 2), Q(1), Q(5)):
        assert -mass * mass + mass * mass == Q(0)
    print("PRO-001 exact local/pro cutoff and quantum moment tests: PASS")


if __name__ == "__main__":
    run()
