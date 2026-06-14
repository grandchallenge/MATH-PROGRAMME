#!/usr/bin/env python3
"""Adversarial rejection tests for the exact algebraic fixture."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from check_algebraic_fixture import FixtureError, check_fixture

SOURCE = Path(__file__).resolve().parents[1] / "fixtures" / "algebraic" / "UF-INV-001"


def load(name: str) -> dict:
    return json.loads((SOURCE / name).read_text(encoding="utf-8"))


def write(root: Path, name: str, value: dict) -> None:
    (root / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def materialize(root: Path, encoding: dict, certificate: dict, ledger: dict) -> None:
    root.mkdir()
    write(root, "encoding.json", encoding)
    write(root, "certificate.json", certificate)
    write(root, "claim_ledger.json", ledger)
    (root / "README.md").write_text((SOURCE / "README.md").read_text(encoding="utf-8"), encoding="utf-8")


def rejected(mutator) -> None:
    encoding = load("encoding.json")
    certificate = load("certificate.json")
    ledger = load("claim_ledger.json")
    mutator(encoding, certificate, ledger)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "fixture"
        materialize(root, encoding, certificate, ledger)
        try:
            check_fixture(root)
        except FixtureError:
            return
    raise AssertionError("adversarial fixture was accepted")


def main() -> int:
    check_fixture(SOURCE)

    rejected(
        lambda _e, c, _l: c["generator_coefficients"][0]["coefficient_polynomial"][0].update(
            coefficient=[2, 1]
        )
    )
    rejected(lambda e, _c, _l: e.update(variables=["t", "x"]))
    rejected(
        lambda e, _c, _l: e["target"].append(copy.deepcopy(e["target"][0]))
    )
    rejected(lambda e, _c, _l: e["compiled_equations"].pop())
    rejected(lambda _e, c, _l: c.update(encoding_sha256="0" * 64))
    rejected(lambda _e, _c, l: l["claims"][2].update(status="CERTIFIED"))

    print("adversarial fixture tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
