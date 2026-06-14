#!/usr/bin/env python3
"""Mathematically check the UF-INV-001 exact algebraic fixture."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]


class FixtureError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FixtureError(f"{path}: cannot load JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise FixtureError(f"{path}: top-level value must be an object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_polynomial(value: Any, variable_count: int, label: str) -> Polynomial:
    if not isinstance(value, list):
        raise FixtureError(f"{label}: polynomial must be a list")

    result: Polynomial = {}
    previous: Monomial | None = None
    for index, term in enumerate(value):
        if not isinstance(term, dict) or set(term) != {"coefficient", "exponents"}:
            raise FixtureError(f"{label}[{index}]: malformed term")

        coefficient = term["coefficient"]
        exponents = term["exponents"]
        if (
            not isinstance(coefficient, list)
            or len(coefficient) != 2
            or not all(isinstance(item, int) for item in coefficient)
            or coefficient[1] <= 0
        ):
            raise FixtureError(f"{label}[{index}]: coefficient must be [integer, positive denominator]")
        fraction = Fraction(coefficient[0], coefficient[1])
        if fraction == 0:
            raise FixtureError(f"{label}[{index}]: zero terms are not canonical")
        if [fraction.numerator, fraction.denominator] != coefficient:
            raise FixtureError(f"{label}[{index}]: coefficient is not reduced")

        if (
            not isinstance(exponents, list)
            or len(exponents) != variable_count
            or not all(isinstance(item, int) and item >= 0 for item in exponents)
        ):
            raise FixtureError(f"{label}[{index}]: invalid exponent vector")
        monomial = tuple(exponents)
        if monomial in result:
            raise FixtureError(f"{label}: duplicate monomial {monomial}")
        if previous is not None and monomial >= previous:
            raise FixtureError(f"{label}: terms must be in descending lexicographic order")
        previous = monomial
        result[monomial] = fraction
    return result


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction()) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            result[monomial] = result.get(monomial, Fraction()) + left_coefficient * right_coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FixtureError(message)


def check_claim_ledger(root: Path, certificate_hash: str) -> None:
    ledger = load_json(root / "claim_ledger.json")
    claims = ledger.get("claims")
    require(isinstance(claims, list), "claim_ledger.json: claims must be a list")
    by_id = {claim.get("claim_id"): claim for claim in claims if isinstance(claim, dict)}
    require(len(by_id) == len(claims), "claim_ledger.json: claim IDs must be unique")

    required = {"UF-INV-001-C001", "UF-INV-001-C002", "UF-INV-001-C003"}
    require(set(by_id) == required, "claim_ledger.json: fixture claim set changed")

    semantic = by_id["UF-INV-001-C001"]
    identity = by_id["UF-INV-001-C002"]
    theorem = by_id["UF-INV-001-C003"]

    require(
        (semantic.get("claim_class"), semantic.get("support_type"), semantic.get("status"))
        == ("PROVED_IN_PACKAGE", "HUMAN_PROOF", "AUDITED"),
        "semantic correspondence must remain an audited human proof",
    )
    require(
        (identity.get("claim_class"), identity.get("support_type"), identity.get("status"))
        == ("COMPUTED_EXACTLY", "EXACT_RATIONAL_COMPUTATION", "CHECKED"),
        "identity claim must be an exactly computed checked claim",
    )
    require(
        identity.get("artifact_hashes", {}).get("certificate.json") == certificate_hash,
        "identity claim carries the wrong certificate hash",
    )
    require(
        (theorem.get("claim_class"), theorem.get("support_type"), theorem.get("status"))
        == ("PROVED_IN_PACKAGE", "HUMAN_PROOF", "AUDITED"),
        "source implication cannot be promoted beyond its human semantic proof",
    )
    require(
        theorem.get("depends_on") == ["UF-INV-001-C001", "UF-INV-001-C002"],
        "source implication must depend on semantic and exact identity claims",
    )


def check_fixture(root: Path) -> None:
    encoding_path = root / "encoding.json"
    certificate_path = root / "certificate.json"
    encoding = load_json(encoding_path)
    certificate = load_json(certificate_path)

    require(encoding.get("fixture_id") == "UF-INV-001", "unexpected fixture ID")
    require(certificate.get("fixture_id") == "UF-INV-001", "certificate fixture ID mismatch")
    require(
        encoding.get("coefficient_domain") == {"kind": "rational_field", "characteristic": 0},
        "unsupported coefficient domain",
    )
    require(encoding.get("model_class") == "field_extensions_of_QQ", "unsupported model class")
    require(encoding.get("variables") == ["x", "t"], "fixture variable order must be [x, t]")
    require(certificate.get("variables") == encoding["variables"], "certificate variable order mismatch")
    require(encoding.get("monomial_order") == "lex", "fixture monomial order must be lex")
    require(certificate.get("monomial_order") == encoding["monomial_order"], "monomial order mismatch")
    require(certificate.get("certificate_kind") == "ideal_membership", "wrong certificate kind")
    require(certificate.get("encoding_sha256") == sha256(encoding_path), "encoding hash mismatch")

    equations = encoding.get("compiled_equations")
    require(isinstance(equations, list) and len(equations) == 2, "compiled system must have two equations")
    generators: dict[str, Polynomial] = {}
    for index, equation in enumerate(equations):
        require(isinstance(equation, dict), f"compiled_equations[{index}] must be an object")
        name = equation.get("name")
        require(isinstance(name, str) and name not in generators, "compiled generator names must be unique")
        generators[name] = parse_polynomial(
            equation.get("polynomial"), 2, f"compiled_equations[{index}].polynomial"
        )
    require(
        list(generators) == ["square_is_one", "inverse_for_x_plus_one"],
        "compiled generator order or names changed",
    )

    target = parse_polynomial(encoding.get("target"), 2, "encoding.target")
    certificate_target = parse_polynomial(certificate.get("target"), 2, "certificate.target")
    require(target == certificate_target, "certificate target differs from encoding target")

    witness = certificate.get("generator_coefficients")
    require(isinstance(witness, list) and len(witness) == len(generators), "witness must cover each generator")
    reconstructed: Polynomial = {}
    for index, item in enumerate(witness):
        require(isinstance(item, dict), f"generator_coefficients[{index}] must be an object")
        generator_name = item.get("generator")
        require(generator_name == list(generators)[index], "witness generator order or name mismatch")
        coefficient = parse_polynomial(
            item.get("coefficient_polynomial"), 2, f"generator_coefficients[{index}].coefficient_polynomial"
        )
        reconstructed = add(reconstructed, multiply(coefficient, generators[generator_name]))

    require(reconstructed == target, "ideal-membership identity is false")
    check_claim_ledger(root, sha256(certificate_path))


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) == 2 else Path("fixtures/algebraic/UF-INV-001")
    try:
        check_fixture(root)
    except FixtureError as exc:
        print(f"fixture rejected: {exc}", file=sys.stderr)
        return 1
    print(f"fixture checked: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
