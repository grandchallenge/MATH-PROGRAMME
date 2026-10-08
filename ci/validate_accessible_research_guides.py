#!/usr/bin/env python3
"""Syntactic and structural accessible-guide checks, not mathematical peer review.

A guide can pass this gate and still have incomplete mathematical exposition.
The source/claim audit and independent human review remain separate.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES = (
    "docs/domains/YM_001_RESEARCH_GUIDE.md",
    "docs/EUCLID_GCD_E2E_001_RESEARCH_GUIDE.md",
    "docs/POINCARE_RECONSTRUCTION_RESEARCH_GUIDE.md",
    "docs/domains/UC_001_RESEARCH_GUIDE.md",
    "docs/domains/NS_CI_001_RESEARCH_GUIDE.md",
    "docs/domains/HC_001_RESEARCH_GUIDE.md",
    "docs/domains/BSD_001_RESEARCH_GUIDE.md",
    "docs/domains/PNP_001_RESEARCH_GUIDE.md",
    "docs/campaigns/OZ_001_RESEARCH_GUIDE.md",
    "docs/campaigns/VGSE_001_RESEARCH_GUIDE.md",
)
REQUIRED_HEADINGS = (
    "Reader entry and prerequisites",
    "Core bridge and first examples by hand",
    "First computation or fixture",
    "First theorem or local proposition",
    "Challenge ladder",
    "Certification path and continuation graph",
    "Trust quartet",
    "Bibliography and source audit",
)
REQUIRED_TERMS = (
    "Audience:", "Time to first example:", "Time to first fixture:",
    "Required", "Helpful", "Deferred",
    "Exercise", "Exploration", "Fixture", "Lemma candidate", "Open direction",
    "Completion test", "Support route", "Limitation",
    "What", "Open", "External verification", "First executable step",
)
EXAMPLE_PAIR = re.compile(
    r"\*\*(?:Friendly example|Friendly example:|Friendly example\.)"
    r"|\*\*Friendly example\*\*",
    re.IGNORECASE,
)
EDGE_CASE = re.compile(r"\*\*(?:Edge example|Boundary example|Failure example|Obstruction example)\*\*", re.IGNORECASE)
FENCE = re.compile(r"\x60\x60\x60python\s*\n(.*?)\n\x60\x60\x60", re.DOTALL)


def validate_text(text: str, path: str) -> list[str]:
    problems: list[str] = []
    for name in REQUIRED_HEADINGS:
        if not re.search(r"^##\s+" + re.escape(name) + r"\s*$", text, re.MULTILINE):
            problems.append(f"{path}: missing pedagogical section {name}")
    for term in REQUIRED_TERMS:
        if term not in text:
            problems.append(f"{path}: missing guide-contract marker {term}")
    if not re.search(r"\*\*Friendly example:", text):
        problems.append(f"{path}: missing friendly worked example")
    if not EDGE_CASE.search(text):
        problems.append(f"{path}: missing obstruction/boundary worked example")
    snippets = FENCE.findall(text)
    if len(snippets) != 1:
        problems.append(f"{path}: expected exactly one bounded Python teaching fixture, got {len(snippets)}")
    for index, snippet in enumerate(snippets, start=1):
        try:
            ast.parse(snippet, filename=f"{path}:fixture-{index}")
        except SyntaxError as exc:
            problems.append(f"{path}: invalid Python fixture syntax: {exc}")
        if "# Expected" not in snippet:
            problems.append(f"{path}: fixture has no expected output")
    if not re.search(r"^## (?:\\d+\\. )?Claim boundary", text, re.MULTILINE):
        problems.append(f"{path}: missing claim-boundary section")
    return problems


def validate(root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    for file in GUIDES:
        path = root / file
        if not path.is_file():
            problems.append(f"{file}: guide missing")
        else:
            problems.extend(validate_text(path.read_text(encoding="utf-8"), file))
    return problems


if __name__ == "__main__":
    issues = validate()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(f"PASS: {len(GUIDES)} guide structures, examples, fixture syntax and source/debt handoff markers; human content audit still required")
