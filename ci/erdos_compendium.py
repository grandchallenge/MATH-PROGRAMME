"""Deterministic, source-qualified, 1,221-entry Erdős MkDocs reference builder.

No network, worker comments, GitHub API, or unreviewed theorem promotion.
The registry is a pinned *catalogue snapshot*, not current theorem authority.
Curated source-reviewed essays live outside docs/ and are copied as authored.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance/erdos_catalogue/REGISTRY.json"
EDITORIAL = ROOT / "governance/erdos_compendium/editorial"
ACCEPTANCE = ROOT / "governance/erdos_compendium/EDITORIAL_ADMISSIONS.json"
# Existing published exemplars #1–#3 predate this acceptance ledger. They are
# preserved only as clearly qualified LEGACY articles, not reviewed admissions.
LEGACY_EXEMPLARS = frozenset({1, 2, 3})
# Older #4 also predates cross-renderer delimiter enforcement; remediate separately.
MATH_DELIMITER_LEGACY = frozenset({1, 2, 3, 4})
GENERATED = ROOT / "docs/erdos"
EXPECTED_COUNT = 1221
REQUIRED_EDITORIAL_HEADINGS = (
    "## The question in plain language",
    "## A small example",
    "## What is known",
    "## GCL's current state",
    "## What remains",
    "## Sources and claim boundaries",
)


def load_admissions(path: Path = ACCEPTANCE) -> dict[int, dict]:
    """A reviewed publication needs exact-source, protected, and rendered evidence.

    The manifest is a proposed editorial decision, not proof certification.
    Publication still requires normal protected PR review and site checks.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(data, dict)
            or set(data) != {"record_type", "admissions"}
            or data["record_type"] != "ERDOS_COMPENDIUM_EDITORIAL_ADMISSIONS/1"
            or not isinstance(data["admissions"], list)):
        raise ValueError("Invalid editorial admission manifest")
    required = {"problem_id", "source_sha256", "source_check",
                "critical_review", "protected_admission",
                "mkdocs_run", "public_html_readback"}
    link_patterns = {
        "source_check": r"https://github[.]com/grandchallenge/MATH-PROGRAMME/issues/\d+#issuecomment-\d+",
        "critical_review": r"https://github[.]com/grandchallenge/MATH-PROGRAMME/(issues|pull)/\d+#issuecomment-\d+",
        "protected_admission": r"https://github[.]com/grandchallenge/MATH-PROGRAMME/pull/\d+",
        "mkdocs_run": r"https://github[.]com/grandchallenge/MATH-PROGRAMME/actions/runs/\d+",
        "public_html_readback": r"https://github[.]com/grandchallenge/MATH-PROGRAMME/issues/\d+#issuecomment-\d+",
    }
    accepted = {}
    for row in data["admissions"]:
        if not isinstance(row, dict) or set(row) != required:
            raise ValueError("Incomplete or unexpected editorial admission fields")
        n = row["problem_id"]
        if (type(n) is not int or n <= 0 or n in LEGACY_EXEMPLARS
                or n in accepted or not re.fullmatch(r"[0-9a-f]{64}", row["source_sha256"])):
            raise ValueError("Invalid, duplicated, or legacy editorial admission identity")
        for key, pattern in link_patterns.items():
            if not isinstance(row[key], str) or not re.fullmatch(pattern, row[key]):
                raise ValueError(f"Invalid {key} evidence link for editorial #{n}")
        accepted[n] = row
    # V2 batch extension is parsed below; V1 remains backward compatible.
    return accepted


def load_batch_admissions(path: Path = ACCEPTANCE) -> dict[int, dict]:
    """Validate V1 legacy rows plus V2 shared evidence and per-entry hashes.

    This is a fail-closed syntactic and identity gate; a protected editorial
    decision must still verify the *truth* of all linked evidence.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("record_type") != "ERDOS_COMPENDIUM_EDITORIAL_ADMISSIONS/2":
        return load_admissions(path)
    if set(data) != {"record_type", "admissions", "batches"} or not isinstance(data["batches"], list):
        raise ValueError("Invalid batch editorial admission manifest")
    with __import__("tempfile").TemporaryDirectory() as td:
        old = Path(td) / "legacy.json"
        old.write_text(json.dumps({"record_type": "ERDOS_COMPENDIUM_EDITORIAL_ADMISSIONS/1",
                                   "admissions": data["admissions"]}), encoding="utf-8")
        accepted = load_admissions(old)
    link_patterns = {
        "critical_review": r"https://github[.]com/grandchallenge/MATH-PROGRAMME/(issues|pull)/\d+#issuecomment-\d+",
        "protected_admission": r"https://github[.]com/grandchallenge/MATH-PROGRAMME/pull/\d+",
        "mkdocs_run": r"https://github[.]com/grandchallenge/MATH-PROGRAMME/actions/runs/\d+",
        "public_html_readback": r"https://github[.]com/grandchallenge/MATH-PROGRAMME/issues/\d+#issuecomment-\d+",
        "source_check": r"https://github[.]com/grandchallenge/MATH-PROGRAMME/issues/\d+#issuecomment-\d+",
    }
    seen_batches = set()
    for batch in data["batches"]:
        shared = {"batch_id", "critical_review", "protected_admission", "mkdocs_run",
                  "public_html_readback", "entries"}
        if not isinstance(batch, dict) or set(batch) != shared:
            raise ValueError("Invalid batch fields")
        batch_id = batch["batch_id"]
        if (not isinstance(batch_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{4,80}", batch_id)
                or batch_id in seen_batches):
            raise ValueError("Invalid or duplicate editorial batch identity")
        seen_batches.add(batch_id)
        if not isinstance(batch["entries"], list) or not batch["entries"] or len(batch["entries"]) > 250:
            raise ValueError("Invalid editorial batch size")
        for key in ("critical_review", "protected_admission", "mkdocs_run", "public_html_readback"):
            if not isinstance(batch[key], str) or not re.fullmatch(link_patterns[key], batch[key]):
                raise ValueError(f"Invalid batch {key}")
        for entry in batch["entries"]:
            if not isinstance(entry, dict) or set(entry) != {"problem_id", "source_sha256", "source_check"}:
                raise ValueError("Invalid per-article batch evidence")
            n = entry["problem_id"]
            if (type(n) is not int or n <= 0 or n in LEGACY_EXEMPLARS or n in accepted
                    or not isinstance(entry["source_sha256"], str)
                    or not re.fullmatch(r"[0-9a-f]{64}", entry["source_sha256"])):
                raise ValueError("Invalid, duplicated, or legacy batch admission identity")
            if not isinstance(entry["source_check"], str) or not re.fullmatch(link_patterns["source_check"], entry["source_check"]):
                raise ValueError("Invalid batch article source_check")
            accepted[n] = {**entry, **{key: batch[key] for key in
                            ("critical_review", "protected_admission", "mkdocs_run", "public_html_readback")},
                           "batch_id": batch_id}
    return accepted


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
    # Reject accidental C0 control bytes (for example, Python "\\alpha" written
    # in a non-raw literal becomes BEL). They silently corrupt rendered LaTeX.
    # Newlines and ordinary tabs are the only allowed C0 whitespace.
    bad_controls = sorted({ord(char) for char in text if ord(char) < 32 and ord(char) not in (9, 10)})
    if bad_controls:
        raise ValueError(f"nonprinting control characters in editorial manuscript {source}: {bad_controls}")
    missing = [head for head in REQUIRED_EDITORIAL_HEADINGS if head not in text]
    if missing or re.search(r"(?m)^# ", text):
        raise ValueError(f"editorial manuscript {source} has missing sections {missing} or a duplicate H1")
    # GitHub MathJax documents $...$ / $...$ delimiters. Markdown backslash
    # parentheses/brackets are intentionally not accepted for new manuscripts:
    # they work with local Arithmatex but can appear literally on GitHub.
    if problem_id not in MATH_DELIMITER_LEGACY and any(
        delimiter in text for delimiter in (r"\(", r"\)", r"\[", r"\]")
    ):
        raise ValueError(f"nonportable GitHub mathematical delimiters in #{problem_id}")
    return text


def reader_card(row: dict, curated: str | None, commit: str, *, pending: bool = False, legacy: bool = False) -> str:
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
        f"**Editorial depth:** {'Legacy authored exemplar — not separately admitted' if legacy else ('Authored explanatory DRAFT — NOT editorially accepted' if pending else ('Reviewed explanatory article — evidence qualified' if curated else 'Reference entry — substantive explanation pending source review'))}.  ",
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
        if legacy:
            body.extend([
                "!!! warning \"Legacy editorial exemplar\"",
                "    This early authored explanation predates the manuscript-acceptance ledger. "
                "It is provided as a qualified educational exemplar, not a separate "
                "source-verified editorial acceptance or mathematical certification.",
                "",
            ])
        if pending:
            body.extend([
                "!!! warning \"UNACCEPTED DRAFT — mathematical editorial review pending\"",
                "    This material is a provisional, source-qualified manuscript "
                "published for line-by-line scrutiny and real HTML/LaTeX testing. "
                "It has NOT received separate GCL editorial acceptance or "
                "independent mathematical certification. Its presence on this "
                "website is not evidence of a solution, reviewed coverage, or final publication.",
                "",
                f"[Review the underlying draft on GitHub](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/erdos_compendium/editorial/{n:04d}.md).",
                "",
            ])
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
          output: Path = GENERATED, admissions_path: Path = ACCEPTANCE) -> dict:
    data, rows = load_registry(registry)
    admissions = load_batch_admissions(admissions_path)
    problems = output / "problems"
    catalogue = output / "catalogue"
    for directory in (problems, catalogue):
        if directory.exists():
            shutil.rmtree(directory)
    problems.mkdir(parents=True)
    catalogue.mkdir(parents=True)
    commit = data["source"]["source_commit"]
    curated_ids: list[int] = []
    pending_ids: list[int] = []
    reviewed_ids: list[int] = []
    legacy_ids: list[int] = []
    found_ids = set()
    for row in rows:
        n = row["problem_id"]
        article = manuscript(n, editorial)
        if article:
            found_ids.add(n)
        legacy = article is not None and n in LEGACY_EXEMPLARS
        admission = admissions.get(n)
        if admission is not None:
            if article is None:
                raise ValueError(f"Admission without manuscript for #{n}")
            actual_hash = hashlib.sha256(article.encode("utf-8")).hexdigest()
            if admission["source_sha256"] != actual_hash:
                raise ValueError(f"Admitted manuscript changed without re-review: #{n}")
        reviewed = article is not None and admission is not None
        pending = article is not None and not legacy and not reviewed
        # Publish clearly labeled, non-accepted drafts so actual deployed
        # mathematical HTML can be verified before the separate admission.
        # Only the reviewed_ids count is authoritative for accepted coverage.
        curated = article
        if reviewed:
            reviewed_ids.append(n)
        if legacy:
            legacy_ids.append(n)
        if pending:
            pending_ids.append(n)
        if curated:
            curated_ids.append(n)
        (problems / f"{n:04d}.md").write_text(
            reader_card(row, curated, commit, pending=pending, legacy=legacy), encoding="utf-8")
    if set(admissions) - found_ids:
        raise ValueError("Admission references an absent registry manuscript")

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
            treatment = ("Reviewed explainer" if n in reviewed_ids else
                         "Legacy exemplar" if n in legacy_ids else
                         "Manuscript awaiting acceptance" if n in pending_ids else
                         "Reference entry")
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
        f"**{len(rows):,} indexed references; {len(reviewed_ids)} separately admitted explanations; "
        f"{len(legacy_ids)} legacy authored exemplars; {len(pending_ids)} manuscripts pending acceptance.** "
        "A merged draft is not editorial acceptance; legacy exemplars are not counted as reviewed.",
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
    index.extend(["", "## Editorially displayed entries", ""])
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
    written = len(list(problems.rglob("*.md"))) + len(list(catalogue.rglob("*.md")))
    if written != expected:
        raise ValueError(f"compendium generation incomplete: expected {expected}, got {written}")
    return {"problems": len(rows), "editorial": len(curated_ids),
            "reviewed": len(reviewed_ids), "legacy": len(legacy_ids),
            "pending": len(pending_ids), "ranges": len(ranges),
            "pages": written, "statuses": dict(status_counts)}


def clean(output: Path = GENERATED) -> None:
    for directory in (output / "problems", output / "catalogue"):
        if directory.exists():
            shutil.rmtree(directory)


