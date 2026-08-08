#!/usr/bin/env python3
"""Fail-closed validator for EUCLID-ELEMENTS-BOOK-VII-MICRO-001."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAGE = DOCS / "documentaries" / "euclid_book_vii_micro.md"
SOURCE = DOCS / "documentaries" / "sources" / "euclid_book_vii_micro.source.json"
EDITION = DOCS / "documentaries" / "euclid_book_vii_micro.edition.json"
SCHEMA = DOCS / "documentaries" / "euclid_book_vii_micro.edition.schema.json"
MANIFEST = DOCS / "documentaries" / "ARTIFACT_MANIFEST.json"
ADMISSION = ROOT / "governance" / "euclid_book_vii_micro_edition_admission.json"
MKDOCS = ROOT / "mkdocs.yml"
CSS = DOCS / "stylesheets" / "euclid-book-vii.css"
PLATES = [
    DOCS / "assets" / "documentaries" / "euclid_book_vii" / "plate_anthyphairesis.svg",
    DOCS / "assets" / "documentaries" / "euclid_book_vii" / "plate_concordance.svg",
]

LOCI = ["VII.def.1", "VII.def.2", "VII.def.3", "VII.def.5", "VII.def.12", "VII.def.14", "VII.1", "VII.2"]
SOURCE_LOCK = "49071febcacd9c84fe4ff268d4e11d7e0c4ff0e5"
TRANSCRIPTION_BLOB = "778718006a60e780ad996e72189bc413c92dc48c"
TRANSCRIPTION_SHA256 = "66d3d62cb75cccc0d705fa06c8845f3d9c2c61952f9994862d54c7679517e6d0"
CONCORDANCE_BLOB = "287126ea40b30cdbb66bd2e489bde6076a51bcf7"
PROVIDER_BLOB = "d3f3a36177cef3962fc8b320302e8cea6bb5bd86"
STAGE1 = "183ff2a0adfbe5bd0ffd5f2e638089b94b868c54"
STAGE2 = "6dd51c29b8bcbac812bcf7a4e803b693ac8be69c"
CERT1 = "78b69e6a3461a83f4893d61c421b1570c08a9ba6"
CERT2 = "cd69013cf55d4ee96539d28ee27eadef64cca06f"

EXACT_STATEMENTS = {
    "VII.def.1": "An unit is that by virtue of which each of the things that exist is called one.",
    "VII.def.2": "A number is a multitude composed of units.",
    "VII.def.3": "A number is a part of a number, the less of the greater, when it measures the greater;",
    "VII.def.5": "The greater number is a multiple of the less when it is measured by the less.",
    "VII.def.12": "Numbers prime to one another are those which are measured by an unit alone as a common measure.",
    "VII.def.14": "Numbers composite to one another are those which are measured by some number as a common measure.",
    "VII.1": "Two unequal numbers being set out, and the less being continually subtracted in turn from the greater, if the number which is left never measures the one before it until an unit is left, the original numbers will be prime to one another.",
    "VII.2": "Given two numbers not prime to one another, to find their greatest common measure.",
}
PORISM = "From this it is manifest that, if a number measure two numbers, it will also measure their greatest common measure."


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors() -> list[str]:
    errors: list[str] = []
    required = [PAGE, SOURCE, EDITION, SCHEMA, MANIFEST, ADMISSION, MKDOCS, CSS, *PLATES]
    for path in required:
        if not path.is_file():
            errors.append(f"missing atomic member: {path.relative_to(ROOT)}")
    if errors:
        return errors

    edition = load(EDITION)
    schema = load(SCHEMA)
    errors.extend(
        f"{e.json_path}: {e.message}"
        for e in sorted(Draft202012Validator(schema).iter_errors(edition), key=lambda e: list(e.path))
    )
    source = load(SOURCE)
    admission = load(ADMISSION)
    manifest = load(MANIFEST)
    page = PAGE.read_text(encoding="utf-8")
    mkdocs = MKDOCS.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")

    if source.get("source_lock_merge") != SOURCE_LOCK:
        errors.append("source-lock merge drift")
    transcription = source.get("transcription", {})
    if transcription.get("git_blob_sha1") != TRANSCRIPTION_BLOB or transcription.get("sha256") != TRANSCRIPTION_SHA256:
        errors.append("transcription identity drift")
    if source.get("concordance", {}).get("git_blob_sha1") != CONCORDANCE_BLOB:
        errors.append("concordance identity drift")
    if source.get("provider_manifest_git_blob_sha1") != PROVIDER_BLOB:
        errors.append("provider-manifest identity drift")
    if source.get("admitted_loci") != LOCI:
        errors.append("source-reference locus membership or order drift")
    if source.get("attached_material") != {"VII.2": ["VII.2.porism"]}:
        errors.append("VII.2 porism binding drift")
    if source.get("historical_modern_equivalence") is not False or source.get("proof_body_transcribed") is not False:
        errors.append("source-reference authority inflation")

    pa = edition.get("protected_authority", {})
    expected = {
        "forge_source_lock_merge": SOURCE_LOCK,
        "source_transcription_blob": TRANSCRIPTION_BLOB,
        "source_transcription_sha256": TRANSCRIPTION_SHA256,
        "source_concordance_blob": CONCORDANCE_BLOB,
        "provider_manifest_blob": PROVIDER_BLOB,
        "stage1_programme_closeout": STAGE1,
        "stage2_programme_closeout": STAGE2,
        "stage1_cert_merge": CERT1,
        "stage2_cert_merge": CERT2,
    }
    for key, value in expected.items():
        if pa.get(key) != value:
            errors.append(f"edition protected authority drift: {key}")
    if edition.get("admitted_loci") != LOCI:
        errors.append("edition locus membership or order drift")
    if any(plate.get("authority") != "pedagogical_orientation_only" for plate in edition.get("plates", [])):
        errors.append("plate authority inflation")
    if any(value is not False for value in edition.get("authority_flags", {}).values()):
        errors.append("edition nonclaim boundary inflation")

    for locus, statement in EXACT_STATEMENTS.items():
        if statement not in page:
            errors.append(f"historical statement missing or mutated: {locus}")
    if PORISM not in page:
        errors.append("VII.2 porism missing or mutated")
    for token in (
        "252 - 105 = 147", "147 - 105 = 42", "105 - 42 = 63", "63 - 42 = 21", "42 - 21 = 21",
        "252 = 2 * 105 + 42", "105 = 2 * 42 + 21", "42 = 2 * 21 + 0",
        "later_algorithmic_normalization", "not_verbatim_in_admitted_loci",
        "21 = -2 * 252 + 5 * 105", "pedagogical_orientation_only",
        SOURCE_LOCK, TRANSCRIPTION_BLOB, TRANSCRIPTION_SHA256, CONCORDANCE_BLOB, PROVIDER_BLOB, STAGE1, STAGE2, CERT1, CERT2,
        "does not establish historical-modern equivalence",
    ):
        if token not in page:
            errors.append(f"reader missing required boundary/evidence token: {token}")

    atomic = admission.get("atomic_members", [])
    for path in (
        "docs/documentaries/euclid_book_vii_micro.md",
        "docs/documentaries/sources/euclid_book_vii_micro.source.json",
        "docs/documentaries/euclid_book_vii_micro.edition.json",
        "docs/documentaries/euclid_book_vii_micro.edition.schema.json",
        "docs/assets/documentaries/euclid_book_vii/plate_anthyphairesis.svg",
        "docs/assets/documentaries/euclid_book_vii/plate_concordance.svg",
        "docs/stylesheets/euclid-book-vii.css",
        "docs/documentaries/ARTIFACT_MANIFEST.json",
        "mkdocs.yml",
        "tests/euclid_book_vii_micro.py",
        "tests/test_euclid_book_vii_micro.py",
    ):
        if path not in atomic:
            errors.append(f"atomic admission member missing: {path}")
    if admission.get("admitted_loci") != LOCI or admission.get("attached_porism") != "VII.2.porism":
        errors.append("admission historical scope drift")
    for key in ("historical_modern_equivalence", "new_mathematical_theorem", "mathsolve_authority_created", "mathcert_authority_created", "novelty_claim", "priority_claim", "first_formalization_claim"):
        if admission.get(key) is not False:
            errors.append(f"admission authority inflation: {key}")
    if admission.get("plates_authority") != "pedagogical_orientation_only":
        errors.append("admission plate authority drift")

    volumes = manifest.get("volumes", [])
    euclid = [v for v in volumes if isinstance(v, dict) and v.get("slug") == "euclid_book_vii_micro"]
    if len(euclid) != 1:
        errors.append("documentary manifest must contain exactly one Euclid Book VII micro-edition member")
    else:
        v = euclid[0]
        if v.get("campaign_id") != "EUCLID-ELEMENTS-BOOK-VII-MICRO-001":
            errors.append("documentary manifest campaign drift")
        if v.get("web_page") != "euclid_book_vii_micro.md" or v.get("edition_record") != "euclid_book_vii_micro.edition.json":
            errors.append("documentary manifest page/edition binding drift")
        if v.get("source_record") != "sources/euclid_book_vii_micro.source.json":
            errors.append("documentary manifest source binding drift")
        if v.get("plates_authority") != "pedagogical_orientation_only":
            errors.append("documentary manifest plate authority inflation")

    if "Euclid, Book VII: Measure and Common Measure: documentaries/euclid_book_vii_micro.md" not in mkdocs:
        errors.append("MkDocs navigation admission missing")
    if "stylesheets/euclid-book-vii.css" not in mkdocs:
        errors.append("Euclid documentary stylesheet not registered")
    for css_token in ("#071A36", "#FAF5E8", "#B78935", "@media print", "max-width: 640px"):
        if css_token not in css:
            errors.append(f"print/mobile/design contract missing: {css_token}")

    for plate in PLATES:
        text = plate.read_text(encoding="utf-8")
        for token in ("<title", "<desc", "pedagogical_orientation_only", "role=\"img\"", "aria-labelledby"):
            if token not in text:
                errors.append(f"plate accessibility/authority contract missing in {plate.name}: {token}")

    return errors


def validate() -> list[str]:
    return semantic_errors()


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(errors))
        print(f"EUCLID-ELEMENTS-BOOK-VII-MICRO-001 failed with {len(errors)} error(s)")
        return 1
    print("validated atomic Book VII micro-edition, exact source identities, eight-locus scope, accessible plates, navigation, and nonclaim boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
