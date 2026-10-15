#!/usr/bin/env python3
"""Validate EXT-015A/B handoff packaging, not mathematics or active dispatch."""
from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SHA = "1f28f95d7c0e4059685830391ba4dfe37760d043"
QUESTION = "Can an extension carry genuinely global analytic information that no compact-support stage can capture?"
DOCS = {"EXT-015A": (2653, "EXT-015A.md"), "EXT-015B": (2654, "EXT-015B.md")}


def fail(message: str) -> None:
    raise SystemExit("HANDOFF VALIDATION FAIL: " + message)


def check_math_markdown(src: str, name: str) -> None:
    lines = src.splitlines()
    in_display = False
    for idx, line in enumerate(lines):
        raw = line.strip()
        if raw == "$$":
            if not in_display and idx > 0 and lines[idx-1].strip():
                fail(f"{name}:{idx+1}: display must follow blank line")
            if in_display and idx + 1 < len(lines) and lines[idx+1].strip():
                fail(f"{name}:{idx+1}: display must precede blank line")
            in_display = not in_display
            continue
        if "\\operatorname" in line:
            fail(f"{name}:{idx+1}: unsupported LaTex operator")
        if in_display:
            continue
        positions = [match.start() for match in re.finditer(r"(?<!\\)(?<!\$)\$(?!\$)", line)]
        if len(positions) % 2:
            fail(f"{name}:{idx+1}: unpaired inline math dollar")
        for start, end in zip(positions[::2], positions[1::2]):
            if ((start and re.search(r"[\w-]", line[start-1])) or
                    (end+1 < len(line) and re.search(r"[\w-]", line[end+1]))):
                fail(f"{name}:{idx+1}: inline math touches prose")
    if in_display:
        fail(f"{name}: unclosed display")


def main() -> None:
    manifest = json.loads((BASE / "HANDOFF_INDEX.json").read_text(encoding="utf8"))
    assert manifest["record_type"] == "GCL_RESEARCH_HANDOFF_CANDIDATES"
    assert manifest["source_protected_head"] == SHA
    assert re.fullmatch(r"[0-9a-f]{40}", manifest["source_protected_head"])
    assert manifest["state"] == "PREPARED_NOT_DISPATCHED"
    for flag in ("authorizes_execution", "authorizes_result_comment",
                 "project_queue_activation", "controller_generated_dispatch"):
        assert manifest[flag] is False, flag
    assert manifest["question"] == QUESTION
    handoffs = manifest["handoffs"]
    assert len(handoffs) == 2
    assert set(entry["id"] for entry in handoffs) == set(DOCS)
    for entry in handoffs:
        ident = entry["id"]
        issue, filename = DOCS[ident]
        assert entry["issue"] == issue and entry["worker"] == "UNASSIGNED"
        assert entry["protected_dispatch"] == "NOT_CREATED"
        assert entry["return_state"] == "NO_RETURN"
        assert entry["candidate_path"].endswith("/" + filename)
        content = (BASE / filename).read_text(encoding="utf8")
        for snippet in (QUESTION, SHA, "#" + str(issue), "NOT DISPATCHED"):
            if snippet not in content:
                fail(f"{filename}: missing {snippet}")
        check_math_markdown(content, filename)
    readiness = (BASE / "READINESS.md").read_text(encoding="utf8")
    if QUESTION not in readiness or "PREPARED; NOT DISPATCHED" not in readiness:
        fail("READINESS.md: no question or launch boundary")
    check_math_markdown(readiness, "READINESS.md")
    print("EXT-015 AB HANDOFF VALIDATION PASS: two issue-bound handoffs, frozen source, no dispatch claims")


if __name__ == "__main__":
    main()
