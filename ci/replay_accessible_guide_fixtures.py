#!/usr/bin/env python3
"""Replay the ten bounded teaching snippets with exact, scope-limited expected output.

This is neither a mathematical proof of any campaign target nor a substitute
for independent certificate verification. The examples are deliberately tiny.
A narrow syntax/import gate precedes running the maintained snippets; only
reviewed repository changes should be admitted to the protected workflow.
"""
from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    "docs/domains/YM_001_RESEARCH_GUIDE.md": "1 1\n2 1/2\n5 1/5\n10 1/10",
    "docs/EUCLID_GCD_E2E_001_RESEARCH_GUIDE.md":
        "[(252, 105, 2, 42), (105, 42, 2, 21), (42, 21, 2, 0)]\n21 21 21",
    "docs/POINCARE_RECONSTRUCTION_RESEARCH_GUIDE.md":
        "[('3-sphere', True, True), ('Poincare-homology-sphere', True, False)]",
    "docs/domains/UC_001_RESEARCH_GUIDE.md": "True {1: 2, 2: 2} True",
    "docs/domains/NS_CI_001_RESEARCH_GUIDE.md": "2 2/3 finite\n4 4/3 divergent",
    "docs/domains/HC_001_RESEARCH_GUIDE.md": "1 []\n2 []\n3 []\n4 [2]",
    "docs/domains/BSD_001_RESEARCH_GUIDE.md":
        "[(0, 0), (1, 0), (2, 1), (2, 4), (3, 2), (3, 3), (4, 0)]\naffine 7 projective 8",
    "docs/domains/PNP_001_RESEARCH_GUIDE.md": "2\n0",
    "docs/campaigns/OZ_001_RESEARCH_GUIDE.md": "[1, 5, 73]",
    "docs/campaigns/VGSE_001_RESEARCH_GUIDE.md": "1\n0",
}
FENCE = re.compile(r"\x60\x60\x60python\s*\n(.*?)\n\x60\x60\x60", re.DOTALL)
ALLOWED_MODULES = {"math", "fractions", "itertools"}
DISALLOWED_CALLS = {"open", "input", "eval", "exec", "compile", "__import__",
                    "breakpoint", "getattr", "setattr", "delattr"}


def replay(root: Path = ROOT) -> list[str]:
    errors = []
    for path, expected in OUTPUTS.items():
        source = (root / path).read_text(encoding="utf-8")
        blocks = FENCE.findall(source)
        if len(blocks) != 1:
            errors.append(f"{path}: expected one Python example")
            continue
        code = blocks[0]
        tree = ast.parse(code, filename=path)
        forbidden = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                forbidden |= any(alias.name not in ALLOWED_MODULES for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                forbidden |= node.module not in ALLOWED_MODULES or node.level != 0
            elif isinstance(node, ast.Attribute):
                forbidden |= node.attr.startswith("__")
            elif isinstance(node, ast.Name):
                forbidden |= node.id.startswith("__")
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                forbidden |= node.func.id in DISALLOWED_CALLS
        if forbidden:
            errors.append(f"{path}: teaching fixture outside supported reviewed subset")
            continue
        try:
            result = subprocess.run([sys.executable, "-I", "-c", code], cwd=root,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, timeout=5, check=False)
        except subprocess.TimeoutExpired:
            errors.append(f"{path}: teaching fixture timed out")
            continue
        if result.returncode or result.stdout.strip() != expected:
            errors.append(
                f"{path}: teaching fixture mismatch: expected={expected!r}, "
                f"actual={result.stdout.strip()!r}, stderr={result.stderr!r}"
            )
    return errors


if __name__ == "__main__":
    problems = replay()
    if problems:
        print("\n".join(problems))
        raise SystemExit(1)
    print(f"PASS: all {len(OUTPUTS)} limited educational Python fixtures replay exactly")
