#!/usr/bin/env python3
"""PR source-first mathematical Markdown gate.

Inspect every newly added or modified Markdown file against its protected-base
version; reject *new* source defects and grandfather unchanged historical ones.
Use this before accepting a new mathematical source, not as a post-publication fix.

The gate checks GFM/MkDocs-compatible source structure. It is not a substitute
for rendered HTML checks or a real browser's MathJax/KaTeX paint pass.
"""
from __future__ import annotations

import argparse
from collections import Counter
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^\s{0,3}(\x60{3,}|~{3,})")
CODE = re.compile(r"(\x60+).*?\1")
DOLLAR = re.compile(r"(?<!\\)(?<!\$)\$(?!\$)")
DOUBLE = re.compile(r"(?<!\\)\$\$")
LEGACY = ((r"\\\(", "legacy-inline-delimiter"),
          (r"\\\[", "legacy-display-delimiter"))
ADJACENT = re.compile(r"[\w-]")


def issues(source: str) -> list[tuple[str, str, int]]:
    """Return (kind, stable context fingerprint, 1-based line) for source defects."""
    lines = source.splitlines()
    out: list[tuple[str, str, int]] = []

    def add(kind: str, context: str, line: int) -> None:
        out.append((kind, context.strip()[:220], line))

    fence = None
    script = False
    in_display = False
    opened = 0
    display_has_body = False

    for index, raw in enumerate(lines):
        n = index + 1
        marker = FENCE.match(raw)
        if marker:
            text = marker.group(1)
            if fence is None:
                fence = (text[0], len(text))
            elif fence[0] == text[0] and len(text) >= fence[1]:
                fence = None
            continue
        if fence is not None:
            continue
        if re.search(r"<(?:script|style)\b", raw, re.I):
            script = True
        if script:
            if re.search(r"</(?:script|style)>", raw, re.I):
                script = False
            continue

        line = CODE.sub("", raw)
        stripped = line.strip()
        if stripped == "$$":
            if not in_display:
                opened = n
                display_has_body = False
                if index > 0 and lines[index-1].strip():
                    add("display-opening-needs-blank-line", lines[index-1], n)
                in_display = True
            else:
                if not display_has_body:
                    add("empty-display", lines[opened-1] if opened else "$$", n)
                if index+1 < len(lines) and lines[index+1].strip():
                    add("display-closing-needs-blank-line", lines[index+1], n)
                in_display = False
            continue

        if re.search(r"\\operatorname\b", line):
            add("unsupported-operatorname", line, n)
        for pattern, kind in LEGACY:
            if re.search(pattern, line):
                add(kind, line, n)

        if in_display:
            display_has_body |= bool(stripped)
            if DOUBLE.search(line):
                add("inline-double-dollar-within-display", line, n)
            continue

        if DOUBLE.search(line):
            add("display-delimiter-not-on-own-line", line, n)

        dollar_positions = [match.start() for match in DOLLAR.finditer(line)]
        if len(dollar_positions) % 2:
            add("unpaired-inline-dollar", line, n)
        for start, end in zip(dollar_positions[::2], dollar_positions[1::2]):
            if start+1 == end:
                add("empty-inline-math", line, n)
            left = line[start-1] if start else ""
            right = line[end+1] if end+1 < len(line) else ""
            if ADJACENT.search(left) or ADJACENT.search(right):
                add("inline-math-touching-prose", line, n)
    if in_display:
        add("unclosed-display", lines[opened-2] if opened >= 2 else "$$", opened)
    return out


def newly_introduced(base: str, current: str) -> list[tuple[str, str, int]]:
    """Compare stable (kind, context) fingerprints, not drifting line numbers."""
    old = Counter((kind, ctx) for kind, ctx, _ in issues(base))
    new = issues(current)
    additions: list[tuple[str, str, int]] = []
    for finding in new:
        key = finding[:2]
        if old[key]:
            old[key] -= 1
        else:
            additions.append(finding)
    return additions


def git_text(repo: Path, rev: str, path: str) -> str | None:
    run = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=repo,
                         text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if run.returncode != 0:
        return None
    return run.stdout


def git_changed(repo: Path, base: str, head: str) -> list[str]:
    run = subprocess.run(["git", "diff", "--name-only", "--diff-filter=ACMR",
                          base, head, "--"], cwd=repo, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if run.returncode:
        raise RuntimeError(f"cannot inspect material diff: {run.stderr.strip()}")
    return sorted(p for p in run.stdout.splitlines() if p.endswith(".md"))


def check_transition(repo: Path, base: str, head: str,
                     paths: list[str] | None = None) -> list[str]:
    errors: list[str] = []
    if paths is None:
        paths = git_changed(repo, base, head)
    for path in paths:
        # All mathematical Markdown, including research outside docs/.
        if not path.endswith(".md"):
            continue
        if Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError(f"unsafe candidate path: {path}")
        now = git_text(repo, head, path)
        if now is None:  # deleted or renamed-away path
            continue
        former = git_text(repo, base, path) or ""
        for kind, context, line in newly_introduced(former, now):
            errors.append(f"{path}:{line}: {kind}: {context[:125]}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--file", action="append", default=[])
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    problems: list[str] = []
    if args.file:
        for path in args.file:
            contents = Path(path).read_text(encoding="utf-8")
            for kind, context, line in issues(contents):
                problems.append(f"{path}:{line}: {kind}: {context[:125]}")
    else:
        if not args.base or not args.head:
            parser.error("use --file or both --base and --head")
        problems = check_transition(args.root, args.base, args.head)
    if problems:
        for error in problems:
            print(error, file=sys.stderr)
        print(f"mathematical Markdown source gate: FAIL ({len(problems)} new defects)",
              file=sys.stderr)
        return 1
    print("mathematical Markdown source gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
