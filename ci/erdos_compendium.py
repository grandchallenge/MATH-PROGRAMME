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
RENDER_AMENDMENTS = ROOT / "governance/erdos_compendium/EDITORIAL_RENDER_AMENDMENTS.json"
STATUS_AMENDMENTS = ROOT / "governance/erdos_compendium/EDITORIAL_STATUS_AMENDMENTS.json"
EC005_TYPOGRAPHY_AMENDMENTS = ROOT / "governance/erdos_compendium/EDITORIAL_TYPOGRAPHY_AMENDMENTS_EC005.json"
LEGACY25_TYPOGRAPHY_AMENDMENTS = ROOT / "governance/erdos_compendium/EDITORIAL_TYPOGRAPHY_AMENDMENTS_LEGACY25.json"
FOUR_DISPLAY_AMENDMENTS = ROOT / "governance/erdos_compendium/EDITORIAL_DISPLAY_MATH_AMENDMENTS_FOUR.json"
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
    # Preserve historical V2 source hashes and evidence on their original batches.
    # A protected, source-bound rendering amendment replaces only the effective
    # manuscript digest; the original admission remains auditable and immutable.
    if Path(path).resolve() == ACCEPTANCE.resolve() and RENDER_AMENDMENTS.exists():
        doc = json.loads(RENDER_AMENDMENTS.read_text(encoding="utf-8"))
        if (set(doc) != {"record_type", "revision_id", "source_issue",
                         "scope", "protected_admission", "browser_readback",
                         "entries"}
                or doc["record_type"] != "ERDOS_COMPENDIUM_EDITORIAL_RENDER_AMENDMENTS/1"
                or doc["revision_id"] != "EC-MATHJAX-20261014-A"
                or doc["scope"] != "TYPOGRAPHY_ONLY_NO_MATHEMATICAL_CERTIFICATION"
                or doc["source_issue"] !=
                   "https://github.com/grandchallenge/MATH-PROGRAMME/issues/2637"
                or not re.fullmatch(r"https://github[.]com/grandchallenge/MATH-PROGRAMME/pull/[0-9]+",
                                    doc["protected_admission"])
                or not re.fullmatch(r"https://github[.]com/grandchallenge/MATH-PROGRAMME/issues/2637#issuecomment-[0-9]+",
                                    doc["browser_readback"])):
            raise ValueError("Invalid rendering amendment authority and receipts")
        corrected = set()
        for row in doc["entries"]:
            if set(row) != {"problem_id", "batch_id", "previous_sha256",
                            "corrected_sha256", "source_check"}:
                raise ValueError("Invalid rendering amendment fields")
            n = row["problem_id"]
            if (type(n) is not int or n in corrected or n not in accepted
                    or n not in {301, 311, 326, 346, 400}
                    or row["batch_id"] != "EC-BULK-003"
                    or row["batch_id"] != accepted[n]["batch_id"]
                    or row["previous_sha256"] != accepted[n]["source_sha256"]
                    or row["source_check"] != accepted[n]["source_check"]
                    or not isinstance(row["corrected_sha256"], str)
                    or not re.fullmatch(r"[0-9a-f]{64}", row["corrected_sha256"])
                    or row["previous_sha256"] == row["corrected_sha256"]):
                raise ValueError(f"Invalid or stale rendering amendment #{n}")
            corrected.add(n)
            accepted[n] = {**accepted[n],
                           "source_sha256": row["corrected_sha256"],
                           "render_amendment_id": doc["revision_id"],
                           "render_amendment_authority": doc["protected_admission"],
                           "render_preview_receipt": doc["browser_readback"]}
        if corrected != {301, 311, 326, 346, 400}:
            raise ValueError("Incomplete 5-article rendering correction batch")
    # Editorial-state text updates after protected admission must not rewrite
    # the historically reviewed V2 batch entries. Enforce an exact protected,
    # source-bound two-entry overlay with immutable old hashes and no theorem
    # certification or change to original source review disposition.
    if Path(path).resolve() == ACCEPTANCE.resolve() and STATUS_AMENDMENTS.exists():
        doc = json.loads(STATUS_AMENDMENTS.read_text(encoding="utf-8"))
        expected = {"record_type", "revision_id", "scope", "source_issue",
                    "pre_fix_public_failure", "protected_patch", "entries"}
        prefix = "https://github.com/grandchallenge/MATH-PROGRAMME/"
        if (not isinstance(doc, dict) or set(doc) != expected
                or doc["record_type"] != "ERDOS_COMPENDIUM_EDITORIAL_STATUS_AMENDMENTS/1"
                or doc["revision_id"] != "EC005-R3-STATUS-20261015-A"
                or doc["scope"] != "EDITORIAL_STATUS_TEXT_ONLY_NO_THEOREM_CERTIFICATION"
                or doc["source_issue"] != prefix + "issues/2552"
                or doc["pre_fix_public_failure"] != prefix + "issues/2552#issuecomment-6185743558"
                or not isinstance(doc["protected_patch"], str)
                or not re.fullmatch(r"https://github[.]com/grandchallenge/MATH-PROGRAMME/pull/[1-9][0-9]*",
                                    doc["protected_patch"])
                or not isinstance(doc["entries"], list)
                or len(doc["entries"]) != 2):
            raise ValueError("Invalid EC005-R3 protected status amendment evidence")
        corrected = set()
        for row in doc["entries"]:
            required = {"problem_id", "batch_id", "previous_sha256",
                        "corrected_sha256", "source_check"}
            if not isinstance(row, dict) or set(row) != required:
                raise ValueError("Invalid EC005-R3 amendment fields")
            n = row["problem_id"]
            if (type(n) is not int or n not in {765, 772} or n in corrected
                    or n not in accepted or accepted[n]["batch_id"] != "EC-BULK-005-R3"
                    or row["batch_id"] != "EC-BULK-005-R3"
                    or row["previous_sha256"] != accepted[n]["source_sha256"]
                    or row["source_check"] != accepted[n]["source_check"]
                    or not isinstance(row["corrected_sha256"], str)
                    or not re.fullmatch(r"[0-9a-f]{64}", row["corrected_sha256"])
                    or row["corrected_sha256"] == row["previous_sha256"]
                    or (hashlib.sha256(manuscript(n).encode("utf-8")).hexdigest()
                        != row["corrected_sha256"]
                        and not (n == 765 and Path(path).resolve() == ACCEPTANCE.resolve()
                                 and EC005_TYPOGRAPHY_AMENDMENTS.exists()))):
                raise ValueError(f"Invalid or stale EC005-R3 status amendment #{n}")
            corrected.add(n)
            accepted[n] = {**accepted[n],
                           "source_sha256": row["corrected_sha256"],
                           "status_amendment_id": doc["revision_id"],
                           "status_amendment_authority": doc["protected_patch"],
                           "pre_fix_status_failure": doc["pre_fix_public_failure"]}
        if corrected != {765, 772}:
            raise ValueError("Incomplete EC005-R3 two-article status correction")
    # R2 is strictly sequential after historical V2 admission and R3 status
    # amendment. Never rewrite the historical ledger or accept an unbound hash.
    if Path(path).resolve() == ACCEPTANCE.resolve() and EC005_TYPOGRAPHY_AMENDMENTS.exists():
        doc = json.loads(EC005_TYPOGRAPHY_AMENDMENTS.read_text(encoding="utf-8"))
        expected = {"record_type", "revision_id", "scope", "source_issue",
                    "protected_patch", "browser_readback", "entries"}
        root_url = "https://github.com/grandchallenge/MATH-PROGRAMME/"
        if (not isinstance(doc, dict) or set(doc) != expected
                or doc["record_type"] != "ERDOS_COMPENDIUM_EDITORIAL_TYPOGRAPHY_AMENDMENTS/1"
                or doc["revision_id"] != "EC005-TYPOGRAPHY-R2-20261015"
                or doc["scope"] != "MATHEMATICAL_TYPOGRAPHY_ONLY_NO_THEOREM_CERTIFICATION"
                or doc["source_issue"] != root_url + "issues/2643"
                or doc["protected_patch"] != root_url + "pull/2677"
                or not re.fullmatch(
                    r"https://github[.]com/grandchallenge/MATH-PROGRAMME/"
                    r"issues/2643#issuecomment-[1-9][0-9]*",
                    doc["browser_readback"])
                or not isinstance(doc["entries"], list)
                or len(doc["entries"]) != 2):
            raise ValueError("Invalid EC005 R2 rendering-correction authority")
        amended = set()
        for row in doc["entries"]:
            required = {"problem_id", "batch_id", "previous_sha256",
                        "corrected_sha256", "source_check"}
            if not isinstance(row, dict) or set(row) != required:
                raise ValueError("Invalid EC005 R2 entry fields")
            n = row["problem_id"]
            if (type(n) is not int or n not in {765, 836}
                    or n in amended or n not in accepted
                    or row["batch_id"] != accepted[n]["batch_id"]
                    or row["batch_id"] != ("EC-BULK-005-R3" if n == 765 else "EC-BULK-005-R5")
                    or row["previous_sha256"] != accepted[n]["source_sha256"]
                    or row["source_check"] != accepted[n]["source_check"]
                    or not isinstance(row["corrected_sha256"], str)
                    or not re.fullmatch(r"[a-f0-9]{64}", row["corrected_sha256"])
                    or row["corrected_sha256"] == row["previous_sha256"]
                    or hashlib.sha256(manuscript(n).encode("utf-8")).hexdigest()
                       != row["corrected_sha256"]):
                raise ValueError(f"Invalid or stale EC005 R2 rendering amendment #{n}")
            amended.add(n)
            accepted[n] = {
                **accepted[n],
                "source_sha256": row["corrected_sha256"],
                "typography_amendment_id": doc["revision_id"],
                "typography_amendment_authority": doc["protected_patch"],
                "typography_preview_receipt": doc["browser_readback"],
            }
        if amended != {765, 836}:
            raise ValueError("Incomplete EC005 R2 amended article pair")
    # The 25-item historical-compendium correction is applied AFTER all older
    # source- and status-bound protected overlays. It may not alter legacy
    # admissions or assert anything about mathematical truth/proof status.
    if Path(path).resolve() == ACCEPTANCE.resolve() and LEGACY25_TYPOGRAPHY_AMENDMENTS.exists():
        doc = json.loads(LEGACY25_TYPOGRAPHY_AMENDMENTS.read_text(encoding="utf-8"))
        required_doc = {"record_type", "revision_id", "scope", "source_issue",
                        "protected_patch", "browser_receipt", "base_main_sha", "entries"}
        expected_ids = {7, 59, 399, 670, 671, 672, 673, 674, 675, 676,
                        780, 781, 803, 804, 806, 807, 808, 809, 811, 816,
                        818, 823, 828, 833, 841}
        root_url = "https://github.com/grandchallenge/MATH-PROGRAMME/"
        if (not isinstance(doc, dict) or set(doc) != required_doc
                or doc["record_type"] != "ERDOS_COMPENDIUM_ADMITTED_TYPOGRAPHY_AMENDMENTS/1"
                or doc["revision_id"] != "EC-LEGACY-25-TEX-20261015"
                or doc["scope"] != "WHITESPACE_AND_MATH_DELIMITERS_ONLY_NO_MATHEMATICAL_CERTIFICATION"
                or doc["source_issue"] != root_url + "issues/2690"
                or doc["base_main_sha"] != "0077c03b06915ebb08bd35a89846ceaaf881e2de"
                or doc["protected_patch"] != root_url + "pull/2694"
                or doc["browser_receipt"] != root_url + "issues/2690#issuecomment-6203116883"
                or not isinstance(doc["entries"], list)
                or len(doc["entries"]) != len(expected_ids)):
            raise ValueError("Invalid legacy25 typography amendment authority")
        amended = set()
        required_entry = {"problem_id", "batch_id", "source_check", "previous_sha256",
                          "corrected_sha256", "previous_raw_sha256", "corrected_raw_sha256",
                          "nonwhitespace_sha256"}
        for row in doc["entries"]:
            if not isinstance(row, dict) or set(row) != required_entry:
                raise ValueError("Invalid legacy25 typography amendment entry schema")
            n = row["problem_id"]
            src = EDITORIAL / f"{n:04d}.md" if type(n) is int else None
            if (type(n) is not int or n not in expected_ids or n in amended
                    or n not in accepted or src is None or not src.is_file()
                    or row["batch_id"] != accepted[n]["batch_id"]
                    or row["source_check"] != accepted[n]["source_check"]
                    or row["previous_sha256"] != accepted[n]["source_sha256"]
                    or any(not isinstance(row[k], str)
                           or not re.fullmatch(r"[a-f0-9]{64}", row[k])
                           for k in ("previous_sha256", "corrected_sha256",
                                     "previous_raw_sha256", "corrected_raw_sha256",
                                     "nonwhitespace_sha256"))
                    or hashlib.sha256(
                        "".join(src.read_text(encoding="utf-8").split()).encode("utf-8")
                    ).hexdigest() != row["nonwhitespace_sha256"]
                    or row["previous_sha256"] == row["corrected_sha256"]
                    or row["previous_raw_sha256"] == row["corrected_raw_sha256"]
                    or hashlib.sha256(src.read_bytes()).hexdigest()
                       != row["corrected_raw_sha256"]
                    or hashlib.sha256(manuscript(n).encode("utf-8")).hexdigest()
                       != row["corrected_sha256"]):
                raise ValueError(f"Invalid/stale legacy25 typography source #{n}")
            amended.add(n)
            accepted[n] = {**accepted[n],
                           "source_sha256": row["corrected_sha256"],
                           "legacy25_typography_id": doc["revision_id"],
                           "legacy25_authority": doc["protected_patch"],
                           "legacy25_browser_receipt": doc["browser_receipt"]}
        if amended != expected_ids:
            raise ValueError("Incomplete legacy25 typography correction")
    # A new typography-only correction layer applies AFTER all previous
    # protected admissions, rendering repairs and status amendments.
    # The historical protected digest remains immutable.
    if Path(path).resolve() == ACCEPTANCE.resolve() and FOUR_DISPLAY_AMENDMENTS.exists():
        doc = json.loads(FOUR_DISPLAY_AMENDMENTS.read_text(encoding="utf-8"))
        fields = {"record_type", "revision_id", "scope", "source_issue",
                  "protected_patch", "browser_receipt", "base_main_sha", "entries"}
        source_url = "https://github.com/grandchallenge/MATH-PROGRAMME/"
        wanted = {665, 669, 776, 777}
        if (not isinstance(doc, dict) or set(doc) != fields
                or doc["record_type"] != "ERDOS_COMPENDIUM_ADMITTED_DISPLAY_MATH_AMENDMENTS/1"
                or doc["revision_id"] != "EC-FOUR-DISPLAY-MATH-20261016"
                or doc["scope"] != "DOCUMENTED_DISPLAY_MATH_AND_NOTATION_PORTABILITY_NO_CERTIFICATION"
                or doc["source_issue"] != source_url + "issues/2698"
                or doc["protected_patch"] != source_url + "pull/2715"
                or doc["browser_receipt"] != source_url + "issues/2698#issuecomment-6227245766"
                or doc["base_main_sha"] != "49d768ed15b2ab77742c34737e172ed53d1ff2db"
                or not isinstance(doc["entries"], list)
                or len(doc["entries"]) != 4):
            raise ValueError("Invalid four-display rendering amendment authority")
        required = {"problem_id", "batch_id", "source_check", "previous_sha256",
                    "corrected_sha256", "previous_raw_sha256", "corrected_raw_sha256",
                    "previous_nonwhitespace_sha256",
                    "corrected_nonwhitespace_sha256", "notation_adjustment"}
        seen = set()
        for row in doc["entries"]:
            if not isinstance(row, dict) or set(row) != required:
                raise ValueError("Invalid four-display rendering amendment schema")
            n = row["problem_id"]
            src = EDITORIAL / f"{n:04d}.md" if type(n) is int else None
            if (type(n) is not int or n not in wanted or n in seen
                    or n not in accepted or src is None or not src.is_file()
                    or row["batch_id"] != accepted[n]["batch_id"]
                    or row["source_check"] != accepted[n]["source_check"]
                    or row["previous_sha256"] != accepted[n]["source_sha256"]
                    or any(not isinstance(row[key], str)
                           or not re.fullmatch(r"[a-f0-9]{64}", row[key])
                           for key in ("previous_sha256", "corrected_sha256",
                                       "previous_raw_sha256", "corrected_raw_sha256",
                                       "previous_nonwhitespace_sha256",
                                       "corrected_nonwhitespace_sha256"))
                    or row["previous_sha256"] == row["corrected_sha256"]
                    or row["previous_raw_sha256"] == row["corrected_raw_sha256"]
                    or hashlib.sha256(src.read_bytes()).hexdigest()
                       != row["corrected_raw_sha256"]
                    or hashlib.sha256(manuscript(n).encode("utf-8")).hexdigest()
                       != row["corrected_sha256"]
                    or hashlib.sha256(
                        "".join(src.read_text(encoding="utf-8").split()).encode("utf-8")
                    ).hexdigest() != row["corrected_nonwhitespace_sha256"]
                    or row["notation_adjustment"] != {
                        665: "WHITESPACE_ONLY",
                        669: "CARDINALITY_AS_SET_SIZE",
                        776: "LINK_TITLE_LITERAL_R",
                        777: "WHITESPACE_ONLY",
                    }[n]
                    or (n in {665, 777} and row["previous_nonwhitespace_sha256"]
                        != row["corrected_nonwhitespace_sha256"])
                    or (n in {669, 776} and row["previous_nonwhitespace_sha256"]
                        == row["corrected_nonwhitespace_sha256"])
                    or (n == 669 and (
                        src.read_text(encoding="utf-8").count(
                            chr(92)+"lvert"+chr(92)+"{") != 5
                        or chr(92)+"#"+chr(92)+"{" in src.read_text(encoding="utf-8")))
                    or (n == 776 and (
                        "multiplicity r on each occurring level" not in
                            src.read_text(encoding="utf-8")
                        or "multiplicity $r$ on each occurring level" in
                            src.read_text(encoding="utf-8")))):
                raise ValueError(f"Invalid or stale four-display correction #{n}")
            seen.add(n)
            accepted[n] = {**accepted[n],
                           "source_sha256": row["corrected_sha256"],
                           "four_display_amendment_id": doc["revision_id"],
                           "four_display_authority": doc["protected_patch"],
                           "four_display_browser_receipt": doc["browser_receipt"]}
        if seen != wanted:
            raise ValueError("Incomplete four-display typography correction")
    # Source-bound explanatory recovery; preserve the historical admission.
    # This role-scoped mathematical review does not confer theorem certification.
    amendment = ROOT / "governance/erdos_compendium/EDITORIAL_EXPOSITION_AMENDMENT_0440.json"
    if Path(path).resolve() == ACCEPTANCE.resolve() and amendment.exists():
        doc = json.loads(amendment.read_text(encoding="utf-8"))
        required = {
            "record_type", "revision_id", "scope", "source_issue",
            "critical_review", "protected_patch", "recovered_source_sha256", "entry"
        }
        root_url = "https://github.com/grandchallenge/MATH-PROGRAMME/"
        if (not isinstance(doc, dict) or set(doc) != required
                or doc["record_type"] != "ERDOS_COMPENDIUM_EDITORIAL_EXPOSITION_AMENDMENT/1"
                or doc["revision_id"] != "EC-440-DYADIC-20261022"
                or doc["scope"] != "ELEMENTARY_BOUNDED_EXPOSITION_NO_THEOREM_CERTIFICATION"
                or doc["source_issue"] != root_url + "issues/1710"
                or doc["critical_review"] != root_url + "issues/1710#issuecomment-6338608455"
                or doc["protected_patch"] != root_url + "pull/2819"
                or doc["recovered_source_sha256"]
                    != "37b93ae66b4791cb15281c3f8b14e89cd22153ea81a59b9ce3caba21a7771159"):
            raise ValueError("Invalid #440 exposition amendment authority or provenance")
        entry = doc["entry"]
        entry_fields = {
            "problem_id", "batch_id", "source_check",
            "previous_sha256", "corrected_sha256"
        }
        old = accepted.get(440)
        if (not isinstance(entry, dict) or set(entry) != entry_fields
                or old is None
                or entry["problem_id"] != 440
                or entry["batch_id"] != "EC-BULK-003"
                or old["batch_id"] != entry["batch_id"]
                or old["source_check"] != entry["source_check"]
                or old["source_sha256"] != entry["previous_sha256"]
                or not isinstance(entry["corrected_sha256"], str)
                or not re.fullmatch(r"[0-9a-f]{64}", entry["corrected_sha256"])
                or entry["previous_sha256"] == entry["corrected_sha256"]
                or hashlib.sha256(manuscript(440).encode("utf-8")).hexdigest()
                    != entry["corrected_sha256"]):
            raise ValueError("Invalid or unreviewed #440 exposition correction")
        accepted[440] = {
            **old,
            "source_sha256": entry["corrected_sha256"],
            "exposition_amendment_id": doc["revision_id"],
            "exposition_review_receipt": doc["critical_review"],
            "exposition_protected_patch": doc["protected_patch"],
        }
    # Source-bound explanatory recovery; preserve the historical admission.
    # This role-scoped mathematical review does not confer theorem certification.
    amendment = ROOT / "governance/erdos_compendium/EDITORIAL_EXPOSITION_AMENDMENT_0436.json"
    if Path(path).resolve() == ACCEPTANCE.resolve() and amendment.exists():
        doc = json.loads(amendment.read_text(encoding="utf-8"))
        required = {
            "record_type", "revision_id", "scope", "source_issue",
            "critical_review", "protected_patch", "recovered_source_sha256", "entry"
        }
        root_url = "https://github.com/grandchallenge/MATH-PROGRAMME/"
        if (not isinstance(doc, dict) or set(doc) != required
                or doc["record_type"] != "ERDOS_COMPENDIUM_EDITORIAL_EXPOSITION_AMENDMENT/1"
                or doc["revision_id"] != "EC-436-QRPAIR-20261022"
                or doc["scope"] != "CLASSICAL_QUADRATIC_RESIDUE_EXPOSITION_NO_THEOREM_CERTIFICATION"
                or doc["source_issue"] != root_url + "issues/1706"
                or doc["critical_review"] != root_url + "issues/1706#issuecomment-6340164126"
                or doc["protected_patch"] != root_url + "pull/2821"
                or doc["recovered_source_sha256"]
                    != "8b73f2be48de4890bba11140c680fb52ba5b5b0094c466c74074816ca1db8eb8"):
            raise ValueError("Invalid #436 exposition amendment authority or provenance")
        entry = doc["entry"]
        entry_fields = {
            "problem_id", "batch_id", "source_check",
            "previous_sha256", "corrected_sha256"
        }
        old = accepted.get(436)
        if (not isinstance(entry, dict) or set(entry) != entry_fields
                or old is None
                or entry["problem_id"] != 436
                or entry["batch_id"] != "EC-BULK-003"
                or old["batch_id"] != entry["batch_id"]
                or old["source_check"] != entry["source_check"]
                or old["source_sha256"] != entry["previous_sha256"]
                or not isinstance(entry["corrected_sha256"], str)
                or not re.fullmatch(r"[0-9a-f]{64}", entry["corrected_sha256"])
                or entry["previous_sha256"] == entry["corrected_sha256"]
                or hashlib.sha256(manuscript(436).encode("utf-8")).hexdigest()
                    != entry["corrected_sha256"]):
            raise ValueError("Invalid or unreviewed #436 exposition correction")
        accepted[436] = {
            **old,
            "source_sha256": entry["corrected_sha256"],
            "exposition_amendment_id": doc["revision_id"],
            "exposition_review_receipt": doc["critical_review"],
            "exposition_protected_patch": doc["protected_patch"],
        }
    # Source-bound explanatory recovery; preserve the historical admission.
    # This role-scoped mathematical review does not confer theorem certification.
    amendment = ROOT / "governance/erdos_compendium/EDITORIAL_EXPOSITION_AMENDMENT_0328.json"
    if Path(path).resolve() == ACCEPTANCE.resolve() and amendment.exists():
        doc = json.loads(amendment.read_text(encoding="utf-8"))
        required = {
            "record_type", "revision_id", "scope", "source_issue",
            "critical_review", "protected_patch", "recovered_source_sha256", "entry"
        }
        root_url = "https://github.com/grandchallenge/MATH-PROGRAMME/"
        if (not isinstance(doc, dict) or set(doc) != required
                or doc["record_type"] != "ERDOS_COMPENDIUM_EDITORIAL_EXPOSITION_AMENDMENT/1"
                or doc["revision_id"] != "EC-328-ORDERED-C2-20261022"
                or doc["scope"] != "ELEMENTARY_ORDERED_C2_OBSTRUCTION_NO_THEOREM_CERTIFICATION"
                or doc["source_issue"] != root_url + "issues/1598"
                or doc["critical_review"] != root_url + "pull/2826#issuecomment-6354908900"
                or doc["protected_patch"] != root_url + "pull/2826"
                or doc["recovered_source_sha256"]
                    != "4c08a3b47c51e1464186c181057117327a1c2bae38ae21ab6c8ccf0fc547441b"):
            raise ValueError("Invalid #328 exposition amendment authority or provenance")
        entry = doc["entry"]
        entry_fields = {
            "problem_id", "batch_id", "source_check",
            "previous_sha256", "corrected_sha256"
        }
        old = accepted.get(328)
        if (not isinstance(entry, dict) or set(entry) != entry_fields
                or old is None
                or entry["problem_id"] != 328
                or entry["batch_id"] != "EC-BULK-003"
                or old["batch_id"] != entry["batch_id"]
                or old["source_check"] != entry["source_check"]
                or old["source_sha256"] != entry["previous_sha256"]
                or not isinstance(entry["corrected_sha256"], str)
                or not re.fullmatch(r"[0-9a-f]{64}", entry["corrected_sha256"])
                or entry["previous_sha256"] == entry["corrected_sha256"]
                or hashlib.sha256(manuscript(328).encode("utf-8")).hexdigest()
                    != entry["corrected_sha256"]):
            raise ValueError("Invalid or unreviewed #328 exposition correction")
        accepted[328] = {
            **old,
            "source_sha256": entry["corrected_sha256"],
            "exposition_amendment_id": doc["revision_id"],
            "exposition_review_receipt": doc["critical_review"],
            "exposition_protected_patch": doc["protected_patch"],
        }
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


