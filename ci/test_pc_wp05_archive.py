#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path.cwd()
SOURCE = ROOT / "campaigns/poincare_reconstruction/WP05_INTEGRATED_CLOSURE"
VALIDATOR = ROOT / "ci/validate_pc_wp05_archive.py"


def run_case(name: str, mutate) -> None:
    with tempfile.TemporaryDirectory(prefix=f"pc-wp05-{name}-") as tmp:
        target = Path(tmp) / "WP05"
        shutil.copytree(SOURCE, target)
        mutate(target)
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR), str(target)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            raise SystemExit(f"adversarial case {name} was incorrectly accepted")
        print(f"rejected as expected: {name}")


def mutate_json(path: Path, edit) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    edit(data)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    baseline = subprocess.run(
        [sys.executable, str(VALIDATOR), str(SOURCE)], cwd=ROOT, check=False
    )
    if baseline.returncode != 0:
        raise SystemExit("baseline PC-WP05 archive is invalid")

    run_case(
        "missing-disclosure",
        lambda p: mutate_json(
            p / "09_ARCHIVAL_MANIFEST.json",
            lambda d: d["mandatory_disclosures"].pop(),
        ),
    )
    run_case(
        "fake-line-concordance",
        lambda p: mutate_json(
            p / "06_DEPENDENCY_CLOSURE.json",
            lambda d: d["closure"].__setitem__("line_by_line_source_concordance_closed", True),
        ),
    )
    run_case(
        "fake-analytic-formalization",
        lambda p: mutate_json(
            p / "06_DEPENDENCY_CLOSURE.json",
            lambda d: d["closure"].__setitem__("full_analytic_formalization", True),
        ),
    )

    def remove_claim(p: Path) -> None:
        path = p / "03_CLAIM_TRUST_MATRIX.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["claims"] = data["claims"][:-1]
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    run_case("missing-claim", remove_claim)
    run_case(
        "new-proof-gate-open",
        lambda p: mutate_json(
            p / "08_PROOF_DEBT.json",
            lambda d: d["publication_gate"].__setitem__("new_proof_claim", "pass"),
        ),
    )
    print("PC-WP05 adversarial archive tests passed")


if __name__ == "__main__":
    main()
