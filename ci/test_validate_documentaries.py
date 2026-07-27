#!/usr/bin/env python3
"""Adversarial rejection tests for Documentary Library contracts."""

from __future__ import annotations

import copy

from validate_documentaries import (
    ROOT,
    collection_discovery_errors,
    discovered_edition_records,
    documentary_contract_errors,
    load_json,
    manifest_semantic_errors,
    schema_errors,
    web_edition_errors,
)


def volume_by_slug(manifest: dict, slug: str) -> dict:
    return next(volume for volume in manifest["volumes"] if volume["slug"] == slug)


def run_rejection_tests() -> None:
    manifest = load_json(ROOT / "docs/documentaries/ARTIFACT_MANIFEST.json")
    manifest_schema = load_json(ROOT / "schemas/documentary_manifest.schema.json")
    discovered = discovered_edition_records()

    assert not documentary_contract_errors()

    duplicate_slug = copy.deepcopy(manifest)
    duplicate_slug["volumes"][1]["slug"] = duplicate_slug["volumes"][0]["slug"]
    assert any(
        "duplicate slug" in error
        for error in manifest_semantic_errors(duplicate_slug)
    )

    omitted_volume = copy.deepcopy(manifest)
    omitted_volume["volumes"] = [
        volume for volume in omitted_volume["volumes"] if volume["slug"] != "riemann"
    ]
    assert any(
        "orphaned edition record" in error
        for error in collection_discovery_errors(
            omitted_volume,
            discovered_records=discovered,
        )
    )

    orphaned_record = set(discovered)
    orphaned_record.add("unregistered.edition.json")
    assert any(
        "orphaned edition record" in error
        for error in collection_discovery_errors(
            manifest,
            discovered_records=orphaned_record,
        )
    )

    incomplete_discovery = set(discovered)
    incomplete_discovery.remove("hodge.edition.json")
    assert any(
        "manifest edition record is missing" in error
        for error in collection_discovery_errors(
            manifest,
            discovered_records=incomplete_discovery,
        )
    )

    topic_drift = copy.deepcopy(manifest)
    volume_by_slug(topic_drift, "hodge")["topic"] = "Integral Hodge Conjecture"
    assert any(
        "source record subject" in error and "does not match manifest" in error
        for error in manifest_semantic_errors(topic_drift)
    )

    invalid_scope = copy.deepcopy(manifest)
    volume_by_slug(invalid_scope, "poincare")["scope_relation"] = "campaign_documentary"
    assert any(
        "incompatible with scope relation" in error
        or "requires an ACTIVE domain" in error
        for error in manifest_semantic_errors(invalid_scope)
    )

    authority_mismatch = copy.deepcopy(manifest)
    volume_by_slug(authority_mismatch, "hodge")[
        "claim_authority"
    ] = "RH-WP00-source-normalization-equivalence-audit.md"
    assert any(
        "does not match expected authority" in error
        for error in manifest_semantic_errors(authority_mismatch)
    )

    false_publication = copy.deepcopy(manifest)
    volume_by_slug(false_publication, "poincare")["rendered_pdf"][
        "availability"
    ] = "published_release"
    assert any(
        "release_locator" in error
        for error in schema_errors(false_publication, manifest_schema, "manifest")
    )

    bsd_volume = volume_by_slug(manifest, "bsd")
    bsd_edition = load_json(
        ROOT / "docs/documentaries" / bsd_volume["edition_record"]
    )
    bsd_page = (
        ROOT / "docs/documentaries" / bsd_volume["web_page"]
    ).read_text(encoding="utf-8")

    duplicate_plate_id = copy.deepcopy(bsd_edition)
    duplicate_plate_id["plates"][1]["id"] = duplicate_plate_id["plates"][0]["id"]
    assert any(
        "duplicate plate id" in error
        for error in web_edition_errors(
            bsd_volume,
            duplicate_plate_id,
            bsd_page,
        )
    )

    duplicate_plate_asset = copy.deepcopy(bsd_edition)
    duplicate_plate_asset["plates"][1]["asset"] = duplicate_plate_asset["plates"][0][
        "asset"
    ]
    assert any(
        "duplicate plate asset" in error
        for error in web_edition_errors(
            bsd_volume,
            duplicate_plate_asset,
            bsd_page,
        )
    )

    missing_asset = copy.deepcopy(bsd_edition)
    missing_asset["plates"][0][
        "asset"
    ] = "assets/documentaries/bsd/missing.svg"
    assert any(
        "missing plate asset" in error
        for error in web_edition_errors(
            bsd_volume,
            missing_asset,
            bsd_page,
        )
    )

    nested_main = bsd_page.replace(
        '<article class="monograph-body"',
        '<main class="monograph-body"',
        1,
    )
    assert any(
        "nested main landmark" in error
        for error in web_edition_errors(
            bsd_volume,
            bsd_edition,
            nested_main,
        )
    )

    unfocusable_skip = bsd_page.replace(
        ' id="monograph-start" tabindex="-1"',
        ' id="monograph-start"',
        1,
    )
    assert any(
        "required marker" in error and "tabindex" in error
        for error in web_edition_errors(
            bsd_volume,
            bsd_edition,
            unfocusable_skip,
        )
    )

    unpinned_math = bsd_page.replace('crossorigin="anonymous"', "", 1)
    assert any(
        "MathJax policy attribute missing" in error
        for error in web_edition_errors(
            bsd_volume,
            bsd_edition,
            unpinned_math,
        )
    )


def main() -> int:
    run_rejection_tests()
    print("documentary validator rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
