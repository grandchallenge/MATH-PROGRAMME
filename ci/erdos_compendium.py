#!/usr/bin/env python3
"""Deterministic, source-qualified, 1,221-entry Erdős MkDocs reference builder.

No network, worker comments, GitHub API, or unreviewed theorem promotion.
The registry is a pinned *catalogue snapshot*, not current theorem authority.
Curated source-reviewed essays live outside docs/ and are copied as authored.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance/erdos_catalogue/REGISTRY.json"
EDITORIAL = ROOT / "governance/erdos_compendium/editorial"
GENERATED = ROOT / "docs/erdos/generated"
EXPECTED_COUNT = 1221
REQUIRED_EDITORIAL_HEADINGS = (
    "## The question in plain language",
    "## A small example",
    "## What is known",
    "## GCL's current state",
    "## What remains",
    "## Sources and claim boundaries",
)


def clean_cell(value: object) -> str:
    """Treat registry strings as *data*, never Markdown/HTML authority."""
    s = str(value)
    return re.sub(r"([\\`|\[\]<>*_{!}])", r"\\\1", s.replace("\n", " ").replace("\r", " "))[:160]


def load_registry(path: Path = REGISTRY) -> tuple[dict, list[dict]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("record_type") != "ERDOS_CATALOGUE_REGISTRY":
        raise ValueError("Erdős catalogue registry identity mismatch")
    if data.get("source", {}).get("source_commit") != "536408716724a2402bdfa7c1d764bf83d64a8c89":
        raise ValueError("Erdős source lock changed: audit and update generator explicitly")
    rows = data.get("issues")
    if not isinstance(rows, list) or len(rows) != EXPECTED_COUNT:
        raise ValueError(f"expected {EXPECTED_COUNT} protected entries, found {len(rows) if isinstance(rows, list) else 'invalid'}")
    ids = [row.get("problem_id") for row in rows]
    numbers = [row.get("issue_number") for row in rows]
    if (any(not isinstance(n, int) or isinstance(n, bool) or n < 1 for n in ids + numbers)
            or len(set(ids)) != len(ids) or len(set(numbers)) != len(numbers)):
        raise ValueError("duplicate or malformed catalogue problem/issue IDs")
    for row in rows:
        if (not isinstance(row.get("catalogue_status"), str)
                or not isinstance(row.get("triage_class"), str)
                or not isinstance(row.get("topics"), list)
                or any(not isinstance(t, str) for t in row["topics"])):
            raise ValueError(f"invalid catalogue metadata: {row.get('problem_id')}")
    return data, sorted(rows, key=lambda x: x["problem_id"])


def manuscript(problem_id: int, base: Path = EDITORIAL) -> str | None:
    source = base / f"{problem_id:04d}.md"
    if not source.exists():
        return None
    text = source.read_text(encoding="utf-8").strip()
    missing = [head for head in REQUIRED_EDITORIAL_HEADINGS if head not in text]
    if missing or re.search(r"(?m)^# ", text):
        raise ValueError(f"editorial manuscript {source} has missing sections {missing} or a duplicate H1")
    return text


def reader_card(row: dict, curated: str | None, commit: str) -> str:
    n = row["problem_id"]
    issue = row["issue_number"]
    topics = ", ".join(clean_cell(x) for x in row["topics"]) or "not classified"
    status = clean_cell(row["catalogue_status"])
    triage = clean_cell(row["triage_class"])
    provider = ("A provider statement was included in the pinned snapshot"
                if row.get("protected_fc_present") is True else
                "No statement was confirmed in GCL's pinned formal-provider snapshot")
    link = f"https://github.com/grandchallenge/MATH-PROGRAMME/issues/{issue}"
    source = f"https://www.erdosproblems.com/{n}"
    body = [
        f"# Erdős Problem #{n}",
        "",
        f"**Editorial depth:** {'Reviewed explanatory draft' if curated else 'Reference entry — substantive explanation pending source review'}.  ",
        f"**Snapshot classification:** {status} (not automatically the live result).  ",
        f"**Subject areas:** {topics}.",
        "",
        "!!! info \"Read this status correctly\"",
        "    The status above is reproduced from GCL's immutable external-catalogue snapshot. "
        "It is **not** a new claim of current mathematical resolution, a source-semantic review, "
        "an independent proof check, or GCL certification. A published proof and a GCL replay "
        "are separate events.",
        "",
    ]
    if curated:
        body.extend([curated, ""])
    else:
        body.extend([
            "## The question in plain language",
            "",
            "The precise mathematical question has **not yet been editorially paraphrased or reviewed for this entry**. "
            f"Read the [original question and its references]({source}) rather than rely on an invented synopsis.",
            "",
            "## A small example",
            "",
            "A checked illustrative example has not yet been prepared.",
            "",
            "## What is known",
            "",
            f"The pinned catalogue records **{status}**. This label must be reconciled against the dated primary literature "
            "before it is treated as a current mathematical conclusion.",
            "",
            "## GCL's current state",
            "",
            f"GCL classifies this item as **{triage}**. Its "
            f"[protected source-audit task]({link}) is the current research-evidence entry point. "
            "An available task is not proof that an independent agent has begun work.",
            "",
            "## What remains",
            "",
            "Capture the exact theorem statement, a readable worked example, the strongest dated source result, "
            "a falsifiable mathematical boundary, and an independently checked account of GCL progress. "
            "Until those steps are done, this is an indexed source reference, **not** a completed explainer.",
            "",
            "## Sources and claim boundaries",
            "",
            f"- [Original problem and primary references]({source})",
            f"- [GCL source-audit record]({link})",
            "",
        ])
    body.extend([
        "## Catalogue and evidence provenance",
        "",
        f"- **Pinned catalogue source:** [teorth/erdosproblems at `{commit[:12]}`]"
        f"(https://github.com/teorth/erdosproblems/blob/{commit}/data/problems.yaml).",
        f"- **GCL issue:** [#{issue}]({link}) — protected issue/assignment identity; "
        "its labels and results are live, not reproduced automatically here.",
        f"- **GCL triage:** {triage}.",
        f"- **Formal-statement coverage:** {provider}. Presence does not mean the statement or proof has been checked.",
        f"- **External mathematical status:** [consult current problem page]({source}) and its dated bibliography.",
        "",
        f"[Back to catalogue](../catalogue/index.md) · [Compendium introduction](../index.md)",
        "",
    ])
    return "\n".join(body)


def build(*, registry: Path = REGISTRY, editorial: Path = EDITORIAL,
          output: Path = GENERATED) -> dict:
    data, rows = load_registry(registry)
    if output.exists():
        shutil.rmtree(output)
    problems = output / "problems"
    catalogue = output / "catalogue"
    problems.mkdir(parents=True)
    catalogue.mkdir(parents=True)
    commit = data["source"]["source_commit"]
    curated_ids: list[int] = []
    for row in rows:
        n = row["problem_id"]
        article = manuscript(n, editorial)
        if article:
            curated_ids.append(n)
        (problems / f"{n:04d}.md").write_text(reader_card(row, article, commit), encoding="utf-8")

    buckets: dict[int, list[dict]] = {}
    for row in rows:
        bucket = (row["problem_id"] - 1) // 100
        buckets.setdefault(bucket, []).append(row)

    ranges = []
    for bucket in sorted(buckets):
        group = buckets[bucket]
        a, b = bucket * 100 + 1, (bucket + 1) * 100
        name = f"{a:04d}-{b:04d}"
        ranges.append((name, len(group)))
        lines = [
            f"# Erdős catalogue #{a}–#{b}",
            "",
            f"{len(group)} registered problems in this number range. "
            "These are source-qualified references, not 100 independently reviewed explanations.",
            "",
            "| Problem | Pinned status | Editorial treatment | Topics |",
            "| --- | --- | --- | --- |",
        ]
        for row in group:
            n = row["problem_id"]
            treatment = "Explanatory article" if n in curated_ids else "Reference entry"
            lines.append(
                f"| [#{n}](../problems/{n:04d}.md) | "
                f"{clean_cell(row['catalogue_status'])} | {treatment} | "
                f"{', '.join(clean_cell(t) for t in row['topics'])} |"
            )
        lines.extend(["", "[All catalogue ranges](index.md)", ""])
        (catalogue / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")

    status_counts = Counter(row["catalogue_status"] for row in rows)
    index = [
        "# All registered Erdős problems",
        "",
        f"**{len(rows):,} indexed reference entries; {len(curated_ids)} authored explanatory articles.** "
        "The two counts are deliberately different.",
        "",
        "The frozen status labels are **not live mathematical facts**. "
        "Read individual source histories before claiming that any problem has been proved or disproved.",
        "",
        "## Browse by number",
        "",
        "| Range | Registered problems |",
        "| --- | ---: |",
    ]
    index.extend(
        f"| [#{name.replace('-', '–#')} ]({name}.md) | {count} |"
        for name, count in ranges
    )
    index.extend(["", "## Editorially developed entries", ""])
    if curated_ids:
        index.extend(f"- [Erdős #{n}](../problems/{n:04d}.md)" for n in curated_ids)
    else:
        index.append("No explanatory articles are admitted.")
    index.extend([
        "", "## Snapshot labels, not a live scoreboard", "",
        "These totals come from the GCL-pinned source snapshot:",
        "",
        "| Source status | Count |", "| --- | ---: |",
    ])
    index.extend(f"| {clean_cell(label)} | {count} |" for label, count in sorted(status_counts.items()))
    index.extend([
        "", "No status line certifies a theorem, a solved problem, or independent external work.",
        "", "[Compendium overview](../index.md)", "",
    ])
    (catalogue / "index.md").write_text("\n".join(index), encoding="utf-8")
    expected = len(rows) + len(ranges) + 1
    written = len(list(output.rglob("*.md")))
    if written != expected:
        raise ValueError(f"compendium generation incomplete: expected {expected}, got {written}")
    return {"problems": len(rows), "editorial": len(curated_ids),
            "ranges": len(ranges), "pages": written, "statuses": dict(status_counts)}


def clean(output: Path = GENERATED) -> None:
    if output.exists():
        shutil.rmtree(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="Validate complete deterministic generation, then remove the build-only source")
    args = parser.parse_args()
    result = build()
    print(json.dumps(result, sort_keys=True))
    if args.check:
        clean()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
