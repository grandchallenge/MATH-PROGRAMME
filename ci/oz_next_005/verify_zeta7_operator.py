#!/usr/bin/env python3
"""Verify the submitted zeta(7) recurrence against the exact locked q_n terms.

This checker does not reconstruct the operator. The source reconstruction script needs
fleet_*.txt inputs that are absent from the pinned repository.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()

    root = args.source.resolve()
    recurrence_path = root / "worthiness" / "zeta7_q_recurrence.json"
    terms_path = root / "worthiness" / "zeta7_lc_terms.txt"
    reconstruction_inputs = list((root / "worthiness").glob("fleet_*.txt"))

    recurrence = json.loads(recurrence_path.read_text(encoding="utf-8"))
    order = int(recurrence["order"])
    degree = int(recurrence["deg"])
    polys = recurrence["Cpoly"]
    if order != 4 or degree != 19 or len(polys) != order + 1:
        raise SystemExit("unexpected submitted operator shape")

    terms: dict[int, int] = {}
    pattern = re.compile(r"q_(\d+)\s*=\s*(\d+)")
    for line in terms_path.read_text(encoding="utf-8").splitlines():
        match = pattern.fullmatch(line.strip())
        if match:
            terms[int(match.group(1))] = int(match.group(2))

    n_terms = 0
    while n_terms in terms:
        n_terms += 1
    if n_terms < order + 1:
        raise SystemExit("insufficient exact terms")

    def coefficient(poly: list[int], n: int) -> int:
        return sum(int(value) * n**power for power, value in enumerate(poly))

    failures: list[tuple[int, int]] = []
    for n in range(n_terms - order):
        residual = sum(coefficient(polys[k], n) * terms[n + k] for k in range(order + 1))
        if residual != 0:
            failures.append((n, residual))

    print(f"operator_order={order}")
    print(f"operator_degree={degree}")
    print(f"exact_terms={n_terms}")
    print(f"tested_residuals={n_terms - order}")
    print(f"reconstruction_inputs={len(reconstruction_inputs)}")
    print(f"submitted_certified_flag={recurrence.get('certified')}")
    print(f"submitted_ntested={recurrence.get('ntested')}")
    print(f"failures={len(failures)}")
    if failures:
        for n, residual in failures[:5]:
            print(f"failure n={n} residual={residual}")
        return 1
    if reconstruction_inputs:
        print("reconstruction_status=inputs_present")
    else:
        print("reconstruction_status=blocked_missing_fleet_inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
