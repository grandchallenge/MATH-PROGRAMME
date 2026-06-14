#!/usr/bin/env python3
"""Adversarial rejection tests for RAD-NIL-002."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from check_algebraic_fixture import FixtureError
from check_radical_fixture import check_fixture

SOURCE = Path(__file__).resolve().parents[1] / "fixtures" / "algebraic" / "RAD-NIL-002"


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
    raise AssertionError("adversarial radical fixture was accepted")


def main() -> int:
    check_fixture(SOURCE)

    rejected(lambda _e, c, _l: c.update(radical_exponent=0))
    rejected(lambda _e, c, _l: c.update(radical_exponent=1))
    rejected(lambda _e, c, _l: c.update(certificate_kind="ideal_membership"))
    rejected(lambda e, _c, _l: e.update(model_class="commutative_QQ_algebras"))
    rejected(lambda e, _c, _l: e.update(target=[{"coefficient": [1, 1], "exponents": [2]}]))
    rejected(lambda _e, c, _l: c.update(encoding_sha256="0" * 64))
    rejected(lambda _e, _c, l: l["claims"][2].update(status="CERTIFIED"))
    rejected(lambda _e, _c, l: l["claims"].pop())
    rejected(
        lambda e, _c, _l: e["excluded_generalization"].update(
            countermodel="removed"
        )
    )

    print("adversarial radical fixture tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
