#!/usr/bin/env python3
"""Mathematically check the RAD-NIL-002 radical-membership fixture."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from check_algebraic_fixture import (
    FixtureError,
    Polynomial,
    add,
    load_json,
    multiply,
    parse_polynomial,
    require,
    sha256,
)


def power(polynomial: Polynomial, exponent: int, variable_count: int) -> Polynomial:
    require(isinstance(exponent, int) and exponent > 0, "radical exponent must be a positive integer")
    result: Polynomial = {(0,) * variable_count: Fraction(1)}
    factor = polynomial
    remaining = exponent
    while remaining:
        if remaining % 2:
            result = multiply(result, factor)
        remaining //= 2
        if remaining:
            factor = multiply(factor, factor)
    return result


def check_claim_ledger(root: Path, certificate_hash: str) -> None:
    ledger = load_json(root / "claim_ledger.json")
    claims = ledger.get("claims")
    require(isinstance(claims, list), "claim_ledger.json: claims must be a list")
    by_id = {claim.get("claim_id"): claim for claim in claims if isinstance(claim, dict)}
    require(len(by_id) == len(claims), "claim_ledger.json: claim IDs must be unique")

    required = {
        "RAD-NIL-002-C001",
        "RAD-NIL-002-C002",
        "RAD-NIL-002-C003",
        "RAD-NIL-002-C004",
    }
    require(set(by_id) == required, "claim_ledger.json: radical fixture claim set changed")

    semantic = by_id["RAD-NIL-002-C001"]
    identity = by_id["RAD-NIL-002-C002"]
    theorem = by_id["RAD-NIL-002-C003"]
    rejected = by_id["RAD-NIL-002-C004"]

    require(
        (semantic.get("claim_class"), semantic.get("support_type"), semantic.get("status"))
        == ("PROVED_IN_PACKAGE", "HUMAN_PROOF", "AUDITED"),
        "field semantic bridge must remain an audited human proof",
    )
    require(
        (identity.get("claim_class"), identity.get("support_type"), identity.get("status"))
        == ("COMPUTED_EXACTLY", "EXACT_RATIONAL_COMPUTATION", "CHECKED"),
        "radical identity must remain an exactly computed checked claim",
    )
    require(
        identity.get("artifact_hashes", {}).get("certificate.json") == certificate_hash,
        "radical identity carries the wrong certificate hash",
    )
    require(
        (theorem.get("claim_class"), theorem.get("support_type"), theorem.get("status"))
        == ("PROVED_IN_PACKAGE", "HUMAN_PROOF", "AUDITED"),
        "field theorem cannot be promoted beyond its human semantic proof",
    )
    require(
        theorem.get("depends_on") == ["RAD-NIL-002-C001", "RAD-NIL-002-C002"],
        "field theorem must depend on semantic and radical identity claims",
    )
    require(
        (rejected.get("claim_class"), rejected.get("status"), rejected.get("certainty"))
        == ("REFUTED", "REJECTED", "FALSE"),
        "arbitrary-ring generalization must remain rejected",
    )
    require(
        rejected.get("countermodel") == "QQ[epsilon]/(epsilon^2), with epsilon^2 = 0 and epsilon != 0.",
        "arbitrary-ring rejection must retain its countermodel",
    )


def check_fixture(root: Path) -> None:
    encoding_path = root / "encoding.json"
    certificate_path = root / "certificate.json"
    encoding = load_json(encoding_path)
    certificate = load_json(certificate_path)

    require(encoding.get("fixture_id") == "RAD-NIL-002", "unexpected fixture ID")
    require(certificate.get("fixture_id") == "RAD-NIL-002", "certificate fixture ID mismatch")
    require(
        encoding.get("coefficient_domain") == {"kind": "rational_field", "characteristic": 0},
        "unsupported coefficient domain",
    )
    require(encoding.get("model_class") == "field_extensions_of_QQ", "model class must remain field extensions")
    require(encoding.get("variables") == ["x"], "fixture variable order must be [x]")
    require(certificate.get("variables") == encoding["variables"], "certificate variable order mismatch")
    require(encoding.get("monomial_order") == "lex", "fixture monomial order must be lex")
    require(certificate.get("monomial_order") == encoding["monomial_order"], "monomial order mismatch")
    require(certificate.get("certificate_kind") == "radical_membership", "wrong certificate kind")
    require(certificate.get("encoding_sha256") == sha256(encoding_path), "encoding hash mismatch")

    excluded = encoding.get("excluded_generalization")
    require(isinstance(excluded, dict), "excluded generalization is required")
    require(excluded.get("model_class") == "commutative_QQ_algebras", "wrong excluded model class")
    require(excluded.get("status") == "refuted", "arbitrary-ring generalization must remain refuted")
    require(
        excluded.get("countermodel") == "QQ[epsilon]/(epsilon^2), where epsilon^2 = 0 but epsilon != 0",
        "countermodel changed or removed",
    )

    equations = encoding.get("compiled_equations")
    require(isinstance(equations, list) and len(equations) == 1, "compiled system must have one equation")
    equation = equations[0]
    require(isinstance(equation, dict) and equation.get("name") == "square_is_zero", "wrong generator")
    generator = parse_polynomial(equation.get("polynomial"), 1, "compiled_equations[0].polynomial")

    target = parse_polynomial(encoding.get("target"), 1, "encoding.target")
    certificate_target = parse_polynomial(certificate.get("target"), 1, "certificate.target")
    require(target == certificate_target, "certificate target differs from encoding target")

    exponent = certificate.get("radical_exponent")
    require(exponent == 2, "fixture radical exponent must be exactly 2")
    powered_target = power(target, exponent, 1)

    witness = certificate.get("generator_coefficients")
    require(isinstance(witness, list) and len(witness) == 1, "witness must cover the generator")
    item = witness[0]
    require(isinstance(item, dict) and item.get("generator") == "square_is_zero", "witness generator mismatch")
    coefficient = parse_polynomial(
        item.get("coefficient_polynomial"), 1, "generator_coefficients[0].coefficient_polynomial"
    )
    reconstructed = add({}, multiply(coefficient, generator))

    require(reconstructed == powered_target, "radical-membership identity is false")
    check_claim_ledger(root, sha256(certificate_path))


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) == 2 else Path("fixtures/algebraic/RAD-NIL-002")
    try:
        check_fixture(root)
    except FixtureError as exc:
        print(f"radical fixture rejected: {exc}", file=sys.stderr)
        return 1
    print(f"radical fixture checked: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
