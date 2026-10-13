#!/usr/bin/env python3
"""Deterministic EC-BULK-003 documentary production gate.

A strict pass checks a *complete* batch. An incomplete pass checks the
source and manuscript contracts without converting missing work to success.
This never provides mathematical certification or admission authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "governance/erdos_compendium/batches/EC-BULK-003.json"
REGISTRY = ROOT / "governance/erdos_catalogue/REGISTRY.json"
ACCEPTED = ROOT / "governance/erdos_compendium/EDITORIAL_ADMISSIONS.json"
SECTIONS = [
    "## The question in plain language",
    "## A small example",
    "## What is known",
    "## GCL's current state",
    "## What remains",
    "## Sources and claim boundaries",
]
VALID_STATES = {"RESULT_PRESENT_UNADJUDICATED", "NO_RESULT_AT_READBACK"}
REPO = "grandchallenge/MATH-PROGRAMME"



# Reject common missing backslashes within $...$ or $$...$$ mathematics.
BARE_MATH = re.compile(
    r"(?<!\\)\b(?:mathbb|mathcal|frac|sqrt|quad|qquad|cdot|leq|geq|"
    r"subseteq|infty|alpha|beta|gamma|limsup|lfloor|rfloor|ldots|operatorname)\b"
    r"|(?<!\\)\b[A-Za-z](?:geq|leq|subseteq)(?=\d|\b)|(?<!\\)\bsum_"
)

def check_math_commands(text: str, problem_id: int) -> None:
    for match in re.finditer(r"(?s)\$\$(.*?)\$\$|\$([^$\n]+)\$", text):
        math = match.group(1) if match.group(1) is not None else match.group(2)
        bad = BARE_MATH.search(math)
        assert bad is None, f"Bare TeX command in #{problem_id}: {bad.group(0)}"


def git_blob_sha(raw: bytes) -> str:
    payload = b"blob " + str(len(raw)).encode() + b"\0" + raw
    return hashlib.sha1(payload).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def qa_ids(manifest: dict) -> tuple[str, list[int]]:
    seed = "EC-BULK-003|" + manifest["source_registry_blob"] + "|200|EDITORIAL-QA"
    rng = random.Random(int(hashlib.sha256(seed.encode("utf-8")).hexdigest(), 16))
    return seed, sorted(rng.sample([x["problem_id"] for x in manifest["items"]], 20))


def verify(strict: bool = False) -> dict:
    m, registry, ledger = load(MANIFEST), load(REGISTRY), load(ACCEPTED)
    assert m["cohort_id"] == "EC-BULK-003"
    assert m["record_type"] == "ERDOS_COMPENDIUM_BULK_INTAKE/1"
    assert m["source_registry_blob"] == git_blob_sha(REGISTRY.read_bytes())
    assert m["target_count"] == 200 and len(m["items"]) == 200
    expected = set(range(246, 447)) - {390}
    mapping = {int(i["problem_id"]): i for i in registry["issues"]}
    nums = [x["problem_id"] for x in m["items"]]
    assert len(nums) == len(set(nums)) and set(nums) == expected
    others = load(ROOT / "governance/erdos_compendium/batches/EC-BULK-002.json")
    assert not expected.intersection(x["problem_id"] for x in others["items"])
    admitted = [e["problem_id"] for b in ledger["batches"] for e in b["entries"]]
    admitted += [e["problem_id"] for e in ledger.get("admissions", [])]
    assert not expected.intersection(admitted), "Already admitted problem in EC-BULK-003"

    returns = 0
    articles = 0
    exceptions = []
    returned_urls = []
    for x in m["items"]:
        n = x["problem_id"]
        source = mapping[n]
        assert x["audit_issue"] == source["issue_number"], n
        assert x["assignment_id"] == f"ERDOS-CATALOGUE-{n:04d}-S01", n
        assert x["registry_issue_body_sha256"] == source["issue_body_sha256"], n
        assert x["registry_status"] == source["catalogue_status"], n
        assert x["evidence_state"] in VALID_STATES, n
        url = x.get("source_return")
        if url is None:
            assert x["evidence_state"] == "NO_RESULT_AT_READBACK", n
        else:
            assert x["evidence_state"] == "RESULT_PRESENT_UNADJUDICATED", n
            assert re.fullmatch(
                rf"https://github\.com/{REPO}/issues/{x['audit_issue']}#issuecomment-[0-9]+",
                url), n
            returns += 1
            returned_urls.append(url)
        flagged = bool(x.get("exception_review_required")) or bool(x.get("exceptions"))
        if flagged:
            exceptions.append(n)
        path = ROOT / f"governance/erdos_compendium/editorial/{n:04d}.md"
        if path.is_file():
            assert url, f"Article #{n} lacks authenticated original audit"
            assert x.get("article_path") == str(path.relative_to(ROOT)), n
            text = path.read_text(encoding="utf-8")
            headings = re.findall(r"^## .+$", text, flags=re.MULTILINE)
            assert headings == SECTIONS, f"Bad six-section structure for #{n}: {headings}"
            assert url in text, f"Article #{n} has no original source comment URL"
            assert text.count("$$") % 2 == 0, f"Unpaired display math in #{n}"
            check_math_commands(text, n)
            assert not re.search(r"\\\[|\\\]|\\\(|\\\)", text), n
            assert len(text.split()) >= 350, f"Insufficient substantive article #{n}"
            digest = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
            raw_digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if x.get("manuscript_raw_file_sha256_pre_admission"):
                assert x["manuscript_raw_file_sha256_pre_admission"] == raw_digest, n
            if x.get("manuscript_sha256_pre_admission"):
                assert x["manuscript_sha256_pre_admission"] == digest, n
            assert x.get("article_status") == "UNACCEPTED_DRAFT", n
            articles += 1
        else:
            assert not x.get("article_path"), f"Missing article file #{n}"
    assert len(returned_urls) == len(set(returned_urls)), "Duplicate issue comment URLs"

    seed, sampled = qa_ids(m)
    qa_file = ROOT / "governance/erdos_compendium/batches/EC-BULK-003_QA.json"
    qa = load(qa_file) if qa_file.exists() else None
    checked = set()
    if qa:
        assert qa["cohort_id"] == m["cohort_id"]
        assert qa["sample_seed"] == seed
        assert qa["sample_problem_ids"] == sampled
        for row in qa.get("reviewed", []):
            n = row["problem_id"]
            assert n in expected
            assert n not in checked, f"Duplicate QA review receipt for #{n}"
            item = m["items"][nums.index(n)]
            assert row.get("source_return") == item["source_return"], n
            assert item.get("article_path"), f"QA review of missing article #{n}"
            assert row.get("article_sha256") == item.get("manuscript_sha256_pre_admission"), (
                f"Stale QA article digest for #{n}; re-review changes before admission"
            )
            assert row.get("editorial_check") in (
                "SOURCE_BOUNDED_PASS_WITH_DISCLOSED_LIMITS",
                "MATERIAL_DEFECT_CORRECTED",
                "SOURCE_EXCEPTION_DOCUMENTED",
                "REVIEW_PENDING_RESOLUTION",
            )
            checked.add(n)
    if strict:
        assert returns == articles == 200, f"Incomplete: {returns} source, {articles} articles"
        assert qa, "Missing editorial QA receipt"
        assert set(sampled) <= checked, "Unreviewed deterministic sample"
        assert set(exceptions) <= checked, "Unreviewed source/material exceptions"
        assert all(x.get("editorial_check") != "REVIEW_PENDING_RESOLUTION"
                   for x in qa["reviewed"]), "Unresolved material review"
    return {
        "cohort": m["cohort_id"],
        "phase": "complete" if strict else "checkpoint",
        "target": 200,
        "source_returns": returns,
        "articles": articles,
        "missing_returns": 200 - returns,
        "missing_articles": 200 - articles,
        "risk_exception_problem_count": len(exceptions),
        "sample_problem_ids": sampled,
        "reviewed_unique": len(checked),
        "strict_ready": returns == articles == 200 and set(sampled) <= checked
                        and set(exceptions) <= checked,
        "claim_boundary": "DOCUMENTARY_ONLY_NOT_MATHEMATICAL_CERTIFICATION",
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    print(json.dumps(verify(a.strict), sort_keys=True))
