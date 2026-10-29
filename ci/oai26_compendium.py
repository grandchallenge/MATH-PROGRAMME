"""Source-locked, noncertifying OAI-26 documentary compendium for MkDocs.

The 372 family pages are generated *only* from protected bibliographic
metadata. An authored six-section manuscript is a DRAFT until an exact
content-hash editorial admission is recorded. No automatic proof verdict.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "governance/oai26_documentary/FAMILY_CATALOGUE.json"
ADMISSIONS = ROOT / "governance/oai26_documentary/EDITORIAL_ADMISSIONS.json"
DOCS = ROOT / "docs/oai26"
EDITORIAL = DOCS / "editorial"
GENERATED = DOCS / "families"
CATALOGUE_PAGE = DOCS / "catalogue.md"
PIN = "1581d4cbdd69a0faf34b2089614fe2a814316a6a"
MARKER = "<!-- GENERATED OAI26 SOURCE-LOCKED NONCERTIFYING PAGE -->"
SECTIONS = (
    "## The question in plain language",
    "## A small example",
    "## What is known",
    "## GCL verification state",
    "## What remains",
    "## Sources and claim boundaries",
)


def load_catalogue(path: Path = CATALOGUE) -> dict:
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("record_type") != "GCL_OAI26_DOCUMENTARY_SOURCE_SNAPSHOT/1":
        raise ValueError("wrong source snapshot schema")
    if record.get("source_lock") != PIN:
        raise ValueError("source revision drift")
    if record.get("source_catalogue_git_blob") != "7a0b00eb9bfdeb59b157a98ee6522fc685580152":
        raise ValueError("source index Git blob identity drift")
    families = record.get("families")
    if not isinstance(families, list) or len(families) != 372:
        raise ValueError("family coverage is not 372")
    identifiers = [f.get("family_id") for f in families]
    expected = [f"{n:03d}" for n in range(1, 373)]
    if identifiers != expected:
        raise ValueError("family identities are duplicated, missing or unordered")
    pdfs = []
    for family in families:
        if not isinstance(family.get("headline"), str) or not family["headline"].strip():
            raise ValueError("missing indexed family headline")
        if not isinstance(family.get("manuscripts"), list) or not family["manuscripts"]:
            raise ValueError("missing indexed family manuscripts")
        for manuscript in family["manuscripts"]:
            path_value = manuscript.get("pdf_path", "")
            if (not isinstance(path_value, str) or
                    not path_value.startswith("preprints/") or
                    not path_value.lower().endswith(".pdf") or
                    ".." in Path(path_value).parts or
                    not manuscript.get("title")):
                raise ValueError(f"unsafe or missing PDF source: {path_value!r}")
            pdfs.append(path_value)
    if len(pdfs) != 719 or len(set(pdfs)) != 719:
        raise ValueError("manuscript coverage not exactly 719 unique paths")
    if record.get("expected_families") != 372 or record.get("expected_manuscript_paths") != 719:
        raise ValueError("snapshot denominators inconsistent")
    return record


def load_admissions(path: Path = ADMISSIONS) -> dict[str, dict]:
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("record_type") != "GCL_OAI26_DOCUMENTARY_EDITORIAL_ADMISSIONS/1":
        raise ValueError("wrong admission schema")
    if record.get("source_lock") != PIN:
        raise ValueError("editorial source revision drift")
    found = {}
    for row in record.get("admissions", []):
        number = row.get("family_id")
        digest = row.get("manuscript_sha256", "")
        if (not isinstance(number, str) or not re.fullmatch(r"\d{3}", number)
                or number in found or
                not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)
                or not row.get("source_audit_url") or not row.get("critic_evidence_url")
                or not row.get("protected_admission_url")):
            raise ValueError("invalid, duplicate or unevidenced editorial admission")
        found[number] = row
    return found


def md_text(value: str) -> str:
    """Display unreviewed publisher text literally, without executing Markdown/math."""
    return html.escape(value, quote=True).replace("$", "&#36;").replace("`", "&#96;").replace("[", "&#91;").replace("]", "&#93;")


def pdf_url(path: str) -> str:
    return "https://github.com/openai/math/blob/" + PIN + "/" + quote(path, safe="/")


def manuscript_text(family: dict) -> str:
    return "\n".join(
        f"- [{md_text(m['title'])}]({pdf_url(m['pdf_path'])}) "
        f"— `{m['pdf_path']}`"
        for m in family["manuscripts"]
    )


def reference_page(family: dict) -> str:
    n = family["family_id"]
    return "\n\n".join((
        f"# OAI-26 family {n}: {md_text(family['headline'])}",
        "**Documentary state: REFERENCE_ONLY.** This is an indexed source record, "
        "not a reviewed explanatory article or a finding about whether the claim is true.",
        SECTIONS[0] + "\n\nThe publisher indexes this family under: "
        + md_text(family["headline"]) +
        "\n\nIts exact theorem statement and all hypotheses have **not** been "
        "reconstructed or independently source-audited in this entry.",
        SECTIONS[1] + "\n\nNo source-checked explanatory example is admitted yet. "
        "An example must be checked against the paper's definitions before publication.",
        SECTIONS[2] + "\n\nThe source collection supplies the manuscripts below. "
        "Their presence in an index does not establish that their conclusions are known "
        "theorems or that a published proof has been independently validated.",
        SECTIONS[3] + "\n\n**SOURCE_INDEXED; FAMILY_SEMANTICS_UNREVIEWED; "
        "EDITORIAL_REFERENCE_ONLY; NO_CERTIFICATION.** A separate corpus-level Lean "
        "compilation/axiom replay cannot be assigned to this family without a witnessed "
        "declaration-to-family bridge.",
        SECTIONS[4] + "\n\nAudit the current manuscript edition, extract its "
        "quantified claim, verify a small example and literature context, establish "
        "any Lean declaration correspondence and record separate source, semantic and "
        "mathematical verdicts. Commission an authored six-section explanation.",
        SECTIONS[5] + "\n\nSource collection: "
        f"[openai/math at pinned revision](https://github.com/openai/math/tree/{PIN}). "
        "GCL source index: "
        "[MATHFORGE protected snapshot](https://github.com/grandchallenge/MATHFORGE/"
        "blob/8c17073e3325a2c8a22f64c0a0edcd853f7f895b/"
        "sources/OPENAI-MATH-2026/MANUSCRIPT_INDEX.json). "
        "Programme: [OAI-26 #2850](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2850)."
        "\n\nIndexed manuscripts (" + str(len(family["manuscripts"])) + "):\n\n"
        + manuscript_text(family) +
        "\n\n**Boundary:** source bibliographic coverage only; no paper-to-Lean "
        "semantic equivalence, mathematical correctness, novelty or MATHCERT asserted.",
    )) + "\n"


def validate_draft(content: str, number: str) -> None:
    if not content.startswith(f"# OAI-26 family {number}"):
        raise ValueError("manuscript header does not match family")
    for heading in SECTIONS:
        if content.count(heading) != 1:
            raise ValueError(f"missing or duplicate authored section: {number} {heading}")
    if "NO_CERTIFICATION" not in content or PIN not in content:
        raise ValueError("draft lacks exact source and certification boundary")


def editorial_page(family: dict, content: str, admitted: bool) -> str:
    status = "EDITORIALLY_ADMITTED" if admitted else "DRAFT_UNACCEPTED"
    qualifier = ("The manuscript has a protected editorial admission, not a theorem certification."
                 if admitted else
                 "This draft has NOT been editorially admitted. Mathematical claims require independent checking.")
    return (f"**Documentary state: {status}.** {qualifier}\n\n"
            + content.rstrip() + "\n\n"
            + "---\n\n**Indexed primary manuscript paths:**\n\n"
            + manuscript_text(family) + "\n")


def build(output_dir: Path = DOCS, catalogue_path: Path = CATALOGUE,
          admissions_path: Path = ADMISSIONS) -> dict:
    record = load_catalogue(catalogue_path)
    admissions = load_admissions(admissions_path)
    folder = output_dir / "families"
    folder.mkdir(parents=True, exist_ok=True)
    if any(folder.iterdir()):
        raise ValueError("generated output is not clean; remove only marked generated pages")
    articles, reviewed = 0, 0
    indices = ["# OAI-26 source catalogue", "",
               "372 families and 719 indexed manuscript PDF paths, source-locked "
               "to [openai/math](" + "https://github.com/openai/math/tree/" + PIN
               + "). **Catalogue presence is not a proof or an editorial review.**", "",
               "[Reader guide](index.md) | "
               "[Programme tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2850)", ""]
    for i, family in enumerate(record["families"]):
        n = family["family_id"]
        if i % 50 == 0:
            indices.extend([f"## Families {i+1:03d}–{min(i+50,372):03d}", ""])
        draft_path = EDITORIAL / f"{n}.md"
        if draft_path.is_file():
            draft = draft_path.read_text(encoding="utf-8")
            validate_draft(draft, n)
            digest = hashlib.sha256(draft.encode("utf-8")).hexdigest()
            accepted = admissions.get(n)
            if accepted and accepted["manuscript_sha256"] != digest:
                raise ValueError(f"stale editorial manuscript hash for family {n}")
            page = editorial_page(family, draft, bool(accepted))
            articles += 1
            reviewed += bool(accepted)
        else:
            if n in admissions:
                raise ValueError("editorial admission without manuscript")
            page = reference_page(family)
        (folder / f"{n}.md").write_text(MARKER + "\n" + page, encoding="utf-8")
        state = "reviewed article" if n in admissions else ("unadmitted draft" if draft_path.is_file() else "reference only")
        indices.append(f"- [Family {n}: {md_text(family['headline'])}](families/{n}.md) "
                       f"({state}; {len(family['manuscripts'])} manuscripts)")
    (output_dir / "catalogue.md").write_text(MARKER + "\n" + "\n".join(indices) + "\n", encoding="utf-8")
    return {"families": 372, "manuscript_paths": 719,
            "editorial_drafts": articles-reviewed, "editorially_admitted": reviewed,
            "reference_only": 372-articles, "generated_pages": 373}


def clean(output_dir: Path = DOCS) -> None:
    paths = [output_dir / "catalogue.md", *(output_dir / "families").glob("*.md")]
    for path in paths:
        if path.exists():
            if not path.read_text(encoding="utf-8").startswith(MARKER):
                raise ValueError("refusing to remove non-generated content: " + str(path))
            path.unlink()
    folder = output_dir / "families"
    if folder.is_dir() and not any(folder.iterdir()):
        folder.rmdir()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("check", "build", "clean"))
    args = parser.parse_args()
    if args.action == "check":
        cat = load_catalogue()
        load_admissions()
        print(json.dumps({"families":len(cat["families"]),
                          "manuscripts":sum(len(f["manuscripts"]) for f in cat["families"])}))
    elif args.action == "build":
        print(json.dumps(build(), sort_keys=True))
    else:
        clean()
