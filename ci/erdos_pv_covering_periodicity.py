#!/usr/bin/env python3
"""Exact bounded finite-period coverage certificates (not an analytic theorem prover).

The general periodicity lemma is proved in the companion mathematical note.
This evaluates specific finite fixtures; oversized lcm => UNCHECKED, not false.
"""
from __future__ import annotations
import argparse
from itertools import product
import json
from math import lcm

HOUGH_SIX = ((0, 2), (0, 3), (1, 4), (3, 8), (7, 12), (23, 24))


def finite_certificate(classes, *, max_period=100_000):
    """Compute exact covered residues and earliest witnessing class, within cap."""
    if type(max_period) is not int or max_period < 1:
        raise ValueError("max_period must be positive integer")
    classes = tuple(classes)
    for row in classes:
        if (not isinstance(row, (tuple, list)) or len(row) != 2
                or any(type(n) is not int for n in row) or row[1] <= 1):
            raise ValueError("each class must be two integers (a,m), m>1")
    moduli = [m for _, m in classes]
    period = lcm(*moduli)  # lcm(empty)=1; empty family covers nothing
    if period > max_period:
        raise ValueError("PERIOD_EXCEEDS_RESOURCE_CAP: no mathematical verdict")
    witness = [-1] * period
    for i, (a, m) in enumerate(classes):
        for r in range(a % m, period, m):
            if witness[r] < 0:
                witness[r] = i
    return {
        "period": period,
        "distinct_moduli": len(set(moduli)) == len(moduli),
        "covers_all_integers": -1 not in witness,
        "uncovered_residues": [r for r, v in enumerate(witness) if v < 0],
        "first_witness_index_by_residue": witness,
    }


def direct_covered(classes, integer):
    """Independent comparator: no use of a period or the witness table."""
    return any((integer - a) % m == 0 for a, m in classes)


def verify_certificate(classes, certificate):
    """Reject a false finite certificate by independent direct scanning."""
    rows = tuple(classes)
    period = lcm(*(m for _, m in rows))
    witnesses = certificate["first_witness_index_by_residue"]
    if certificate["period"] != period or len(witnesses) != period:
        raise ValueError("wrong exact period or incomplete residue table")
    distinct = len({m for _, m in rows}) == len(rows)
    if certificate["distinct_moduli"] != distinct:
        raise ValueError("distinctness incorrectly certified")
    missing = []
    for r in range(period):
        # Exhaustive direct predicate, independent of modular-progression fill.
        expected = next((i for i, (a, m) in enumerate(rows)
                         if (r - a) % m == 0), -1)
        if witnesses[r] != expected:
            raise ValueError("invalid exact witness or false uncovered residue")
        if expected == -1:
            missing.append(r)
    if (certificate["uncovered_residues"] != missing or
            certificate["covers_all_integers"] != (not missing)):
        raise ValueError("coverage metadata contradicts direct certificate")
    return True


def fixture_payload():
    original = finite_certificate(HOUGH_SIX)
    mutated = finite_certificate(HOUGH_SIX[:-1] + ((24, 24),))
    repeated = finite_certificate(((0, 2), (1, 2)))
    for rows, cert in ((HOUGH_SIX, original),
                       (HOUGH_SIX[:-1] + ((24, 24),), mutated),
                       (((0, 2), (1, 2)), repeated)):
        verify_certificate(rows, cert)
    checks = 0
    for values in product(range(2), range(3), range(4), range(6)):
        rows = tuple(zip(values, (2, 3, 4, 6)))
        result = finite_certificate(rows)
        period = result["period"]
        for x in range(-2 * period, 2 * period + 1):
            assert direct_covered(rows, x) == (
                result["first_witness_index_by_residue"][x % period] != -1
            )
        checks += 1
    assert checks == 144
    assert original["period"] == 24 and original["covers_all_integers"]
    assert original["distinct_moduli"] and not original["uncovered_residues"]
    assert mutated["uncovered_residues"] == [23]
    assert not mutated["covers_all_integers"] and mutated["distinct_moduli"]
    assert repeated["covers_all_integers"] and not repeated["distinct_moduli"]
    return {
        "record_type": "ERDOS_PV_0002_B_FINITE_PERIODICITY_FIXTURES/1",
        "source_issue_body_sha256": (
            "65e4ef993de9e9c69ac5ca9f21c9d784f5553f79fafed42cf197f38a3295e54d"
        ),
        "claim": "BOUNDED_FINITE_PERIODICITY_ONLY__NOT_HOUGH_BBMST_REPROOF",
        "class_list_original": [list(v) for v in HOUGH_SIX],
        "original": original,
        "hostile_last_class_mutation": mutated,
        "repeated_modulus_control": repeated,
        "exhaustive_small_distinct_assignments_checked": checks,
        "independent_comparator": "direct integer congruence on [-2L,2L]",
        "lean_kernel_replayed": False,
        "mathcert_certified": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", action="store_true")
    args = parser.parse_args()
    if not args.fixtures:
        parser.error("Use --fixtures for deterministic bounded evidence")
    print(json.dumps(fixture_payload(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
