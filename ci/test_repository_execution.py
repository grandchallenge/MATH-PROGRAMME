#!/usr/bin/env python3
"""Adversarial tests for repository experiment and unit-test reachability."""

from __future__ import annotations

import tempfile
from pathlib import Path

from validate_repository_execution import repository_execution_errors


WORKFLOW = """name: Synthetic policy
on: [pull_request]
jobs:
  validate-json:
    runs-on: ubuntu-24.04
    steps:
      - run: python -m unittest discover -s tests -p 'test_*.py'
      - run: |
          python3 ci/validate_repository_execution.py
          python3 ci/test_repository_execution.py
"""

TEST_MODULE = """import unittest
from experiments.sample import value

class SampleTests(unittest.TestCase):
    def test_value(self):
        self.assertEqual(value(), 1)
"""

EXPERIMENT_MODULE = """def value():
    return 1
"""


def write_valid_root(root: Path) -> None:
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "experiments").mkdir()
    (root / ".github" / "workflows" / "ci.yml").write_text(WORKFLOW, encoding="utf-8")
    (root / "tests" / "test_sample.py").write_text(TEST_MODULE, encoding="utf-8")
    (root / "experiments" / "__init__.py").write_text("", encoding="utf-8")
    (root / "experiments" / "sample.py").write_text(EXPERIMENT_MODULE, encoding="utf-8")


def main() -> int:
    assert not repository_execution_errors()

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        write_valid_root(root)
        assert not repository_execution_errors(root)

        (root / "experiments" / "hidden.py").write_text("def hidden():\n    return 2\n", encoding="utf-8")
        assert any(
            "hidden.py" in error and "unreachable" in error
            for error in repository_execution_errors(root)
        )
        (root / "experiments" / "hidden.py").unlink()

        (root / "experiments" / "sample.py").write_text(
            EXPERIMENT_MODULE + "\nif __name__ == '__main__':\n    print(value())\n",
            encoding="utf-8",
        )
        assert any(
            "library-only" in error for error in repository_execution_errors(root)
        )
        (root / "experiments" / "sample.py").write_text(EXPERIMENT_MODULE, encoding="utf-8")

        workflow_path = root / ".github" / "workflows" / "ci.yml"
        workflow_path.write_text(
            WORKFLOW.replace(
                "python -m unittest discover -s tests -p 'test_*.py'",
                "echo tests skipped",
            ),
            encoding="utf-8",
        )
        assert any(
            "missing repository execution command" in error
            for error in repository_execution_errors(root)
        )
        workflow_path.write_text(WORKFLOW, encoding="utf-8")

        (root / "tests" / "test_sample.py").write_text(
            "from experiments.sample import value\n",
            encoding="utf-8",
        )
        assert any(
            "must define a unittest.TestCase" in error
            for error in repository_execution_errors(root)
        )

    print("repository execution rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
