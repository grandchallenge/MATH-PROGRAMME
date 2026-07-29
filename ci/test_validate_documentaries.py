#!/usr/bin/env python3
"""Adversarial rejection tests for admitted and pre-admission documentary contracts."""

from __future__ import annotations

import copy

from validate_documentaries import (
    ROOT,
    SHARED_CSS,
    SHARED_JS,
    candidate_semantic_errors,
    collection_discovery_errors,
    discovered_asset_directories,
    discovered_candidate_locks,
    discovered_documentary_assets,
    discovered_edition_records,
    discovered_source_records,
    discovered_web_pages,
    documentary_contract_errors,
    load_json,
    manifest_semantic_errors,
    schema_errors,
    web_edition_errors,
)


def volume_by_slug(manifest: dict, slug: str) -> dict:
    return next(volume for volume in manifest["volumes"] if volume["slug"] == slug)


def synthetic_candidate_from_admitted(volume: dict) -> dict:
    """Construct a valid pre-admission-shaped fixture from an admitted volume."""
    return {
        "slug": volume["slug"],
        "domain_id": volume["domain_id"],
        "campaign_id": volume["campaign_id"],
        "scope_relation": volume["scope_relation"],
        "proposed_documentary_tier": volume["documentary_tier"],
        "title": volume["title"],
        "topic": volume["topic"],
        "claim_status": volume["claim_status"],
        "problem_class": volume["problem_class"],
        "display_status": volume["display_status"],
        "claim_authority": volume["claim_authority"],
        "source_record": (
            "campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK/"
            "artifacts/the_element_in_half_the_worlds.tex"
        ),
        "source_lock": volume["source_lock"],
        "review_record": "reviews/union_closed/UC-DOC-WP00.agent_review.yaml",
        "admission_state": "source_locked_web_admission_pending",
        "manifest_member": False,
        "public_copy_policy": "metadata_public_source_record_repository_only",
        "admission_obligations": ["synthetic pre-admission obligation"],
        "release_artifacts": {
            "rendered_pdf": volume["rendered_pdf"],
            "latex_source": volume["latex_source"],
            "authoritative_source_bundle": volume["authoritative_source_bundle"],
        },
    }


def run_rejection_tests() -> None:
    manifest = load_json(ROOT / "docs/documentaries/ARTIFACT_MANIFEST.json")
    candidates = load_json(ROOT / "docs/documentaries/DOCUMENTARY_CANDIDATES.json")
    manifest_schema = load_json(ROOT / "schemas/documentary_manifest.schema.json")
    candidate_schema = load_json(
        ROOT / "schemas/documentary_candidate_registry.schema.json"
    )
    discovered_editions = discovered_edition_records()
    discovered_pages = discovered_web_pages()
    discovered_sources = discovered_source_records()
    discovered_assets = discovered_documentary_assets()
    discovered_dirs = discovered_asset_directories()
    discovered_locks = discovered_candidate_locks()

    assert len(manifest["volumes"]) == 8
    assert candidates["candidates"] == []
    assert not schema_errors(candidates, candidate_schema, "candidates")
    assert not documentary_contract_errors()

    duplicate_slug = copy.deepcopy(manifest)
    duplicate_slug["volumes"][1]["slug"] = duplicate_slug["volumes"][0]["slug"]
    assert any(
        "duplicate slug" in error for error in manifest_semantic_errors(duplicate_slug)
    )

    omitted_volume = copy.deepcopy(manifest)
    omitted_volume["volumes"] = [
        volume for volume in omitted_volume["volumes"] if volume["slug"] != "riemann"
    ]
    omitted_errors = collection_discovery_errors(
        omitted_volume,
        candidates=candidates,
        discovered_records=discovered_editions,
        discovered_pages=discovered_pages,
        discovered_sources=discovered_sources,
        discovered_assets=discovered_assets,
        discovered_asset_dirs=discovered_dirs,
    )
    assert any("orphaned edition record" in error for error in omitted_errors)
    assert any("orphaned web page" in error for error in omitted_errors)
    assert any("orphaned admitted source record" in error for error in omitted_errors)
    assert any("orphaned asset directory" in error for error in omitted_errors)

    orphaned_record = set(discovered_editions)
    orphaned_record.add("unregistered.edition.json")
    assert any(
        "orphaned edition record" in error
        for error in collection_discovery_errors(
            manifest, candidates=candidates, discovered_records=orphaned_record
        )
    )

    incomplete_discovery = set(discovered_editions)
    incomplete_discovery.remove("hodge.edition.json")
    assert any(
        "manifest edition record is missing" in error
        for error in collection_discovery_errors(
            manifest, candidates=candidates, discovered_records=incomplete_discovery
        )
    )

    orphaned_page = set(discovered_pages)
    orphaned_page.add("unregistered.md")
    assert any(
        "orphaned web page" in error
        for error in collection_discovery_errors(
            manifest, candidates=candidates, discovered_pages=orphaned_page
        )
    )

    missing_source = set(discovered_sources)
    missing_source.remove("sources/the_geometry_of_hidden_harmony.tex")
    assert any(
        "admitted source record is missing" in error
        for error in collection_discovery_errors(
            manifest, candidates=candidates, discovered_sources=missing_source
        )
    )

    orphaned_source = set(discovered_sources)
    orphaned_source.add("sources/unregistered.tex")
    assert any(
        "orphaned admitted source record" in error
        for error in collection_discovery_errors(
            manifest, candidates=candidates, discovered_sources=orphaned_source
        )
    )

    orphaned_asset = set(discovered_assets)
    orphaned_asset.add("assets/documentaries/bsd/unregistered.svg")
    assert any(
        "orphaned documentary asset" in error
        for error in collection_discovery_errors(
            manifest, candidates=candidates, discovered_assets=orphaned_asset
        )
    )

    missing_dir = set(discovered_dirs)
    missing_dir.remove("hodge")
    assert any(
        "asset directory is missing" in error
        for error in collection_discovery_errors(
            manifest, candidates=candidates, discovered_asset_dirs=missing_dir
        )
    )

    orphaned_dir = set(discovered_dirs)
    orphaned_dir.add("unregistered")
    assert any(
        "orphaned asset directory" in error
        for error in collection_discovery_errors(
            manifest, candidates=candidates, discovered_asset_dirs=orphaned_dir
        )
    )

    orphaned_lock = set(discovered_locks)
    orphaned_lock.add("campaigns/union_closed/UNKNOWN/artifacts/UNKNOWN_SOURCE_LOCK.json")
    assert any(
        "orphaned source lock" in error
        for error in collection_discovery_errors(
            manifest,
            candidates=candidates,
            discovered_candidate_records=orphaned_lock,
        )
    )

    missing_lock = set(discovered_locks)
    missing_lock.remove(volume_by_slug(manifest, "union_closed")["source_lock"])
    assert any(
        "registered source lock is missing" in error
        for error in collection_discovery_errors(
            manifest,
            candidates=candidates,
            discovered_candidate_records=missing_lock,
        )
    )

    missing_provenance = copy.deepcopy(manifest)
    volume_by_slug(missing_provenance, "union_closed").pop("source_lock")
    assert any(
        "orphaned source lock" in error
        for error in collection_discovery_errors(
            missing_provenance,
            candidates=candidates,
            discovered_candidate_records=discovered_locks,
        )
    )

    drifted_provenance = copy.deepcopy(manifest)
    volume_by_slug(drifted_provenance, "union_closed")["display_status"] = (
        "Different open label"
    )
    assert any(
        "source lock display_status" in error
        for error in manifest_semantic_errors(drifted_provenance)
    )

    assert any(
        "forbidden root static file POINCARE_WEB_EDITION_README.txt" in error
        for error in collection_discovery_errors(
            manifest,
            candidates=candidates,
            root_files={
                "ARTIFACT_MANIFEST.json",
                "DOCUMENTARY_CANDIDATES.json",
                "documentary_web.schema.json",
                "index.md",
                "POINCARE_WEB_EDITION_README.txt",
                *(volume["edition_record"] for volume in manifest["volumes"]),
                *(volume["web_page"] for volume in manifest["volumes"]),
            },
        )
    )

    extra_css = set(SHARED_CSS)
    extra_css.add("docs/stylesheets/documentary-legacy.css")
    assert any(
        "orphaned shared CSS" in error
        for error in collection_discovery_errors(
            manifest,
            candidates=candidates,
            discovered_css=extra_css,
            discovered_js=set(SHARED_JS),
        )
    )

    extra_js = set(SHARED_JS)
    extra_js.add("docs/javascripts/documentary-legacy.js")
    assert any(
        "orphaned shared JavaScript" in error
        for error in collection_discovery_errors(
            manifest,
            candidates=candidates,
            discovered_css=set(SHARED_CSS),
            discovered_js=extra_js,
        )
    )

    topic_drift = copy.deepcopy(manifest)
    volume_by_slug(topic_drift, "hodge")["topic"] = "Integral Hodge Conjecture"
    assert any(
        "source record subject" in error and "does not match manifest" in error
        for error in manifest_semantic_errors(topic_drift)
    )

    invalid_scope = copy.deepcopy(manifest)
    volume_by_slug(invalid_scope, "poincare")["scope_relation"] = (
        "campaign_documentary"
    )
    assert any(
        "incompatible with scope relation" in error or "requires an ACTIVE domain" in error
        for error in manifest_semantic_errors(invalid_scope)
    )

    authority_mismatch = copy.deepcopy(manifest)
    volume_by_slug(authority_mismatch, "hodge")["claim_authority"] = (
        "RH-WP00-source-normalization-equivalence-audit.md"
    )
    assert any(
        "does not match expected authority" in error
        for error in manifest_semantic_errors(authority_mismatch)
    )

    false_publication = copy.deepcopy(manifest)
    volume_by_slug(false_publication, "poincare")["rendered_pdf"]["availability"] = (
        "published_release"
    )
    assert any(
        "release_locator" in error
        for error in schema_errors(false_publication, manifest_schema, "manifest")
    )

    invalid_status_pair = copy.deepcopy(manifest)
    volume_by_slug(invalid_status_pair, "bsd")["problem_class"] = (
        "solved_classical_theorem"
    )
    assert any(
        "problem_class" in error
        for error in schema_errors(invalid_status_pair, manifest_schema, "manifest")
    )

    union_volume = volume_by_slug(manifest, "union_closed")
    candidate_overlap = copy.deepcopy(candidates)
    candidate_overlap["candidates"] = [synthetic_candidate_from_admitted(union_volume)]
    assert not schema_errors(candidate_overlap, candidate_schema, "candidates")
    assert any(
        "already admitted" in error
        for error in candidate_semantic_errors(candidate_overlap, manifest)
    )

    candidate_public_source = copy.deepcopy(candidate_overlap)
    candidate_public_source["candidates"][0]["source_record"] = (
        "docs/documentaries/sources/the_element_in_half_the_worlds.tex"
    )
    assert any(
        "must remain outside docs/" in error
        for error in candidate_semantic_errors(candidate_public_source, manifest)
    )

    candidate_wrong_status = copy.deepcopy(candidate_overlap)
    candidate_wrong_status["candidates"][0]["problem_class"] = (
        "solved_classical_theorem"
    )
    assert any(
        "problem_class" in error
        for error in schema_errors(candidate_wrong_status, candidate_schema, "candidates")
    )

    bsd_volume = volume_by_slug(manifest, "bsd")
    bsd_edition = load_json(ROOT / "docs/documentaries" / bsd_volume["edition_record"])
    bsd_page = (ROOT / "docs/documentaries" / bsd_volume["web_page"]).read_text(
        encoding="utf-8"
    )

    duplicate_plate_id = copy.deepcopy(bsd_edition)
    duplicate_plate_id["plates"][1]["id"] = duplicate_plate_id["plates"][0]["id"]
    assert any(
        "duplicate plate id" in error
        for error in web_edition_errors(bsd_volume, duplicate_plate_id, bsd_page)
    )

    duplicate_plate_asset = copy.deepcopy(bsd_edition)
    duplicate_plate_asset["plates"][1]["asset"] = duplicate_plate_asset["plates"][0][
        "asset"
    ]
    assert any(
        "duplicate plate asset" in error
        for error in web_edition_errors(bsd_volume, duplicate_plate_asset, bsd_page)
    )

    missing_asset = copy.deepcopy(bsd_edition)
    missing_asset["plates"][0]["asset"] = "assets/documentaries/bsd/missing.svg"
    assert any(
        "missing plate asset" in error
        for error in web_edition_errors(bsd_volume, missing_asset, bsd_page)
    )

    nested_main = bsd_page.replace(
        '<article class="monograph-body"', '<main class="monograph-body"', 1
    )
    assert any(
        "nested main landmark" in error
        for error in web_edition_errors(bsd_volume, bsd_edition, nested_main)
    )

    unfocusable_skip = bsd_page.replace(
        ' id="monograph-start" tabindex="-1"', ' id="monograph-start"', 1
    )
    assert any(
        "required marker" in error and "tabindex" in error
        for error in web_edition_errors(bsd_volume, bsd_edition, unfocusable_skip)
    )

    unpinned_math = bsd_page.replace('crossorigin="anonymous"', "", 1)
    assert any(
        "MathJax policy attribute missing" in error
        for error in web_edition_errors(bsd_volume, bsd_edition, unpinned_math)
    )


def main() -> int:
    run_rejection_tests()
    print("documentary validator rejection tests passed for admitted state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
