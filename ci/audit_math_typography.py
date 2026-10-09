#!/usr/bin/env python3
"""Audit GitHub math syntax across Markdown and built MkDocs Arithmatex HTML.

A source-compatibility audit is not a substitute for a live GitHub KaTeX
render, and an HTML wrapper check is not a JavaScript/browser visual test.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".venv", "site", "node_modules", ".lake", "build", "dist"}
INLINE = re.compile(r"(?<!\\)(?<!\$)\$(?!\$)([^\n$]+?)(?<!\\)(?<!\$)\$(?!\$)")
DISPLAY = re.compile(r"(?<!\\)\$\$([\s\S]*?)(?<!\\)\$\$")
CODE = re.compile(r"(\x60+)(.*?)\1")
FENCE = re.compile(r"^\s{0,3}(\x60{3,}|~{3,})")
ADJACENT = re.compile(r"[\w-]")
MATHLIKE = re.compile(r"\\[A-Za-z]+|[_^{}=<>+\-]")

def source_lines(text: str):
    """Yield line number, content outside code, and raw-HTML classification."""
    fence_char = None
    script = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        match = FENCE.match(raw)
        if match:
            marker = match.group(1)
            if fence_char is None:
                fence_char = (marker[0], len(marker))
            elif marker[0] == fence_char[0] and len(marker) >= fence_char[1]:
                fence_char = None
            continue
        if fence_char is not None:
            continue
        if re.search(r"<(?:script|style)\b", raw, re.I):
            script = True
        if script:
            if re.search(r"</(?:script|style)>", raw, re.I):
                script = False
            continue
        yield lineno, CODE.sub("", raw), raw.lstrip().startswith("<")

def source_issues(path: Path, root: Path = ROOT):
    text = path.read_text(encoding="utf-8")
    label = path.relative_to(root).as_posix()
    issues = []
    kept = list(source_lines(text))
    public = label.startswith("docs/")
    for lineno, line, html in kept:
        if not line.strip():
            continue
        context = "html" if html else "markdown"
        for name, pattern in (
            ("legacy-inline-delimiter", r"\\\("),
            ("legacy-display-delimiter", r"\\\["),
        ):
            if re.search(pattern, line):
                issues.append({"path": label, "line": lineno, "kind": name,
                               "context": context, "sample": line.strip()[:160]})
        if re.search(r"\\operatorname\b", line):
            issues.append({"path": label, "line": lineno,
                           "kind": "github-unsupported-operatorname",
                           "context": context, "sample": line.strip()[:160]})
        for match in INLINE.finditer(line):
            left = line[match.start()-1] if match.start() else ""
            right = line[match.end()] if match.end() < len(line) else ""
            if ADJACENT.search(left) or ADJACENT.search(right):
                issues.append({"path": label, "line": lineno, "kind": "math-prose-adjacency",
                               "context": context, "sample": line.strip()[:160]})
        if public and not html:
            without_display = re.sub(r"(?<!\\)\$\$.*?(?<!\\)\$\$", "", line)
            single = re.sub(r"(?<!\\)\$\$", "", without_display)
            singles = list(re.finditer(r"(?<!\\)\$(?!\$)", single))
            if len(singles) % 2 and MATHLIKE.search(single):
                issues.append({"path": label, "line": lineno,
                               "kind": "unpaired-inline-dollar", "context": context,
                               "sample": line.strip()[:160]})
    ordinary = "\n".join(line for _, line, html in kept if not html)
    if len(re.findall(r"(?<!\\)\$\$", ordinary)) % 2:
        issues.append({"path": label, "line": 0, "kind": "unpaired-display-dollar",
                       "context": "markdown", "sample": "$$ display delimiters unbalanced"})
    return issues

def source_math_count(path: Path) -> int:
    ordinary = "\n".join(line for _, line, html in source_lines(
        path.read_text(encoding="utf-8")) if not html)
    blocks = list(DISPLAY.finditer(ordinary))
    return len(blocks) + len(INLINE.findall(DISPLAY.sub("", ordinary)))

def rendered_issues(root: Path, site: Path):
    findings = []
    checked = 0
    for path in sorted((root / "docs").rglob("*.md")):
        if any(part in SKIP for part in path.relative_to(root).parts):
            continue
        # Documentary editions hand-author HTML and load their own pinned
        # MathJax. Their math never passes through Arithmatex; instead, check
        # their explicitly separate script path in the built HTML.
        documentary = path.read_text(encoding="utf-8")
        if "documentary-mathjax.js" in documentary:
            rel = path.relative_to(root / "docs").with_suffix("")
            html_path = site / rel / "index.html"
            if path.name == "index.md":
                html_path = site / rel.parent / "index.html"
            if not html_path.is_file():
                findings.append({"path": path.relative_to(root).as_posix(),
                                 "kind": "documentary-page-missing"})
                continue
            html = html_path.read_text(encoding="utf-8")
            checked += 1
            if ("documentary-mathjax.js" not in html
                    or "mathjax@3.2.2" not in html):
                findings.append({"path": path.relative_to(root).as_posix(),
                                 "kind": "documentary-mathjax-loader-missing"})
            continue
        expected = source_math_count(path)
        if not expected:
            continue
        rel = path.relative_to(root / "docs").with_suffix("")
        html_path = site / rel / "index.html"
        if path.name == "index.md":
            html_path = site / rel.parent / "index.html"
        if not html_path.is_file():
            findings.append({"path": path.relative_to(root).as_posix(),
                             "kind": "built-page-missing", "expected": expected})
            continue
        html = html_path.read_text(encoding="utf-8")
        actual = len(re.findall(r'class=["\x27]arithmatex["\x27]', html))
        checked += 1
        if actual < expected:
            findings.append({"path": path.relative_to(root).as_posix(),
                             "kind": "arithmatex-wrapper-shortfall",
                             "expected": expected, "actual": actual})
    return checked, findings

def github_render_probe(root: Path):
    """Render two public flagship pages through GitHub's real GFM HTML API.

    This observes the server renderer, not JavaScript MathJax in a browser.
    Network failures are reported explicitly, not counted as passes.
    """
    records = []
    for rel in ("docs/CMDG_CM4_MATHEMATICAL_NOTE.md",
                "docs/CONDENSED_MATHEMATICS_FOR_THE_PERPLEXED.md"):
        source = (root / rel).read_text(encoding="utf-8")
        payload = json.dumps({"text": source, "mode": "gfm",
                              "context": "grandchallenge/MATH-PROGRAMME"}).encode("utf-8")
        request = urllib.request.Request(
            "https://api.github.com/markdown", data=payload,
            headers={"Accept": "text/html", "Content-Type": "application/json",
                     "User-Agent": "GCL-typography-audit",
                     "X-GitHub-Api-Version": "2026-03-10"}, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                html = response.read().decode("utf-8")
            has_math = bool(re.search(r"math-inline|math-display|class=.math\b|katex", html, re.I))
            records.append({"path": rel, "status": "ok" if has_math else "no-math-markers",
                            "html_bytes": len(html), "math_markup_observed": has_math})
        except (OSError, UnicodeError, ValueError) as exc:
            records.append({"path": rel, "status": "unavailable",
                            "reason": f"{type(exc).__name__}: {exc}"[:160]})
    return records

def audit(root: Path = ROOT, site: Path | None = None, github_live: bool = False):
    paths = sorted(p for p in root.rglob("*.md")
                   if not any(part in SKIP for part in p.relative_to(root).parts))
    issues = []
    for path in paths:
        issues.extend(source_issues(path, root))
    report = {
        "schema": "GCL-MATH-TYPOGRAPHY-AUDIT/1",
        "scanned_markdown_files": len(paths),
        "scanned_public_markdown_files": sum(p.is_relative_to(root / "docs") for p in paths),
        "findings": issues,
    }
    report["findings_by_kind_and_context"] = dict(Counter(
        f["kind"] + ":" + f["context"] for f in issues
    ))
    report["top_markdown_paths"] = Counter(
        f["path"] for f in issues if f["context"] == "markdown"
    ).most_common(20)
    if github_live:
        report["github_render_probe"] = github_render_probe(root)
    if site is not None:
        checked, rendered = rendered_issues(root, site)
        report["rendered_math_pages_checked"] = checked
        report["rendered_findings"] = rendered
    return report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--site-dir", type=Path)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--github-live", action="store_true",
                    help="Use GitHub Markdown API for two flagship notes")
    ap.add_argument("--gate", action="store_true",
                    help="Fail on mathematical typography defects in the two CM4 flagship pages")
    args = ap.parse_args()
    root = args.root.resolve()
    report = audit(root, args.site_dir, github_live=args.github_live)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
    summary = {}
    for finding in report["findings"] + report.get("rendered_findings", []):
        summary[finding["kind"]] = summary.get(finding["kind"], 0) + 1
    print(f"mathematical typography: {report['scanned_markdown_files']} repository Markdown "
          f"files; {report['scanned_public_markdown_files']} public pages; "
          f"findings={json.dumps(summary, sort_keys=True)}")
    if "rendered_math_pages_checked" in report:
        print(f"MkDocs rendered math pages checked: {report['rendered_math_pages_checked']}")
    if args.gate:
        targets = {"docs/CMDG_CM4_MATHEMATICAL_NOTE.md",
                   "docs/CONDENSED_MATHEMATICS_FOR_THE_PERPLEXED.md"}
        errors = [f for f in report["findings"] + report.get("rendered_findings", [])
                  if f["path"] in targets and f.get("context", "markdown") == "markdown"]
        if errors:
            for issue in errors:
                print(f"ERROR {issue['path']}:{issue.get('line', 0)} {issue['kind']}")
            return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
