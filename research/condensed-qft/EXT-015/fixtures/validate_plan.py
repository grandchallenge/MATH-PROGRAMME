#!/usr/bin/env python3
"""Format and contract smoke checks for the EXT-015 research plan.

Does not verify mathematics, derived Ext, GitHub approvals, or live queue state.
Run from any working directory after the branch is checked out.
"""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
FILES = (
    "SPEC.md",
    "WORK_PACKAGES.md",
    "EXTENSION_DOCKET.md",
    "RUN_MATRIX.md",
)
QUESTION = "Can an extension carry genuinely global analytic information that no compact-support stage can capture?"
REQUIRED_IDS = ("EXT-015A", "EXT-015B", "EXT-015C", "EXT-015D")


def check(path: Path) -> list[str]:
    s = path.read_text(encoding="utf-8")
    issues = []
    if not s.startswith("# QFT-COND-005 / EXT-015"):
        issues.append("unexpected heading")
    if QUESTION not in s:
        issues.append("missing guiding question")
    if len(re.findall(r"^\s*\$\$\s*$", s, re.M)) % 2:
        issues.append("unbalanced display math")
    if "\\operatorname" in s:
        issues.append("unsupported math operator")
    # Inline math must not collide with a word or hyphen.
    for n, line in enumerate(s.splitlines(), 1):
        if line.strip() == "$$":
            continue
        positions = [m.start() for m in re.finditer(r"(?<!\\)(?<!\$)\$(?!\$)", line)]
        for a, b in zip(positions[::2], positions[1::2]):
            if (a > 0 and re.match(r"[\w-]", line[a-1])) or (
                b+1 < len(line) and re.match(r"[\w-]", line[b+1])
            ):
                issues.append("inline math adjacency on line " + str(n))
    return issues


def main() -> None:
    failures = {}
    for relative in FILES:
        path = BASE / relative
        if not path.is_file():
            failures[relative] = ["missing"]
        else:
            issues = check(path)
            if issues:
                failures[relative] = issues
    work = (BASE / "WORK_PACKAGES.md").read_text(encoding="utf-8")
    for work_id in REQUIRED_IDS:
        if work_id not in work:
            failures.setdefault("WORK_PACKAGES.md", []).append(
                "missing " + work_id
            )
    if failures:
        raise SystemExit("EXT-015 PLAN CONTRACT FAIL: " + repr(failures))
    print("EXT-015 PLAN CONTRACT PASS: 4 docs, 4 package IDs, math delimiters")


if __name__ == "__main__":
    main()
