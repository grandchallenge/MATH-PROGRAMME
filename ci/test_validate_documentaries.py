#!/usr/bin/env python3
"""Adversarial rejection tests for Documentary Library contracts."""
from __future__ import annotations

import copy

from validate_documentaries import (
    ROOT,
    documentary_contract_errors,
    load_json,
    manifest_semantic_errors,
    schema_errors,
    web_edition_errors,
)


def run_rejection_tests() -> None:
    manifest = load_json(ROOT / "docs/documentaries/ARTIFACT_MANIFEST.json")
    manifest_schema = load_json(ROOT / "schemas/documentary_manifest.schema.json")
    edition = load_json(ROOT / "docs/documentaries/poincare.edition.json")
    page_text = (ROOT / "docs/documentaries/poincare.md").read_text(encoding="utf-8")

    assert not documentary_contract_errors()

    duplicate_slug = copy.deepcopy(manifest)
    duplicate_slug["volumes"][1]["slug"] = duplicate_slug["volumes"][0]["slug"]
    assert any("duplicate slug" in error for error in manifest_semantic_errors(duplicate_slug))

    wrong_campaign = copy.deepcopy(manifest)
    wrong_campaign["volumes"][0]["campaign_id"] = "PC-WRONG"
    assert any("does not match domain PC campaign" in error for error in manifest_semantic_errors(wrong_campaign))

    missing_source_record = copy.deepcopy(manifest)
    missing_source_record["volumes"][0]["source_record"] = "sources/missing.tex"
    assert any("source record is missing" in error for error in manifest_semantic_errors(missing_source_record))

    mismatched_hash = copy.deepcopy(manifest)
    mismatched_hash["volumes"][0]["latex_source"]["sha256"] = "0" * 64
    assert any("latex_sha256" in error and "does not match manifest" in error for error in manifest_semantic_errors(mismatched_hash))

    false_publication = copy.deepcopy(manifest)
    false_publication["volumes"][0]["rendered_pdf"]["availability"] = "published_release"
    assert any("release_locator" in error for error in schema_errors(false_publication, manifest_schema, "manifest"))

    bad_asset = copy.deepcopy(edition)
    bad_asset["plates"][0]["asset"] = "assets/documentaries/poincare/missing.svg"
    assert any("missing plate asset" in error for error in web_edition_errors(bad_asset, page_text))

    nested_main = page_text.replace('<article class="monograph-body"', '<main class="monograph-body"', 1)
    assert any("nested main landmark" in error for error in web_edition_errors(edition, nested_main))

    unfocusable_skip = page_text.replace(' id="monograph-start" tabindex="-1"', ' id="monograph-start"', 1)
    assert any("skip target must be programmatically focusable" in error for error in web_edition_errors(edition, unfocusable_skip))

    unpinned_math = page_text.replace('crossorigin="anonymous"', '', 1)
    assert any("MathJax policy attribute missing" in error for error in web_edition_errors(edition, unpinned_math))

    misleading_authority = page_text + "\n<p>Authoritative LaTeX</p>\n"
    assert any("misleading documentary source label" in error for error in web_edition_errors(edition, misleading_authority))


def main() -> int:
    run_rejection_tests()
    print("documentary validator rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
