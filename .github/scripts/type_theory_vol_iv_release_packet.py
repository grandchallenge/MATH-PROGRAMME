#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import subprocess
from pathlib import Path

SOURCE_SHA = "9e7d817daf388e020ceb2b4d83bb7543d8c57f12"
GATE7_RUN = 34170916991
GATE7_ARTIFACT_ID = 10035704745
GATE7_ARTIFACT_DIGEST = "920541f9df897460bca1ef066a4ac9dbf4c30f08e95b1d676f186cbb2fafc86d"
SOURCE_ARCHIVE_SHA = "48e2d1f32b1cbf8349ddd3a0f5a807781c6e75b50a411fba8a8f8f038302508e"
SOURCE_ARCHIVE_SIZE = 123466
MAIN_SHA = "bb1c4ef217f7487a8e4a9f93fb2f1e7e7ecce3fef3f426485e7e8f2d5c1a12b7"
SOLUTIONS_SHA = "d5a1bfa752c57f90a3461ea24d663523dc35c7bb9a127116d32e4d05ae57cdd4"
PLATES_SHA = "6e5fb07bc67f88230895fca2a4e60354ec452d7e4dec9871dd47c806b3c84fe0"
ROOT = Path("monographs/type-theory/volume-iv-protocol")
RELEASE = ROOT / "releases" / "RC1"


def git_blob_sha(text: str) -> str:
    data = text.encode("ascii")
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def main() -> None:
    observed = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    if observed != SOURCE_SHA:
        raise SystemExit(f"source drift: {observed} != {SOURCE_SHA}")
    if subprocess.check_output(["git", "status", "--porcelain"], text=True).strip():
        raise SystemExit("source working tree is not clean")

    RELEASE.mkdir(parents=True, exist_ok=True)
    archive = Path("/tmp/GCL_Type_Theory_Volume_IV_PROTOCOL_RC1_Source.zip")
    subprocess.run(
        [
            "git",
            "archive",
            "--format=zip",
            "--prefix=volume-iv-protocol/",
            "-o",
            str(archive),
            f"HEAD:{ROOT.as_posix()}",
        ],
        check=True,
    )
    raw = archive.read_bytes()
    observed_archive_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != SOURCE_ARCHIVE_SIZE or observed_archive_sha != SOURCE_ARCHIVE_SHA:
        raise SystemExit(
            f"source archive identity mismatch: bytes={len(raw)} sha256={observed_archive_sha}"
        )

    encoded = base64.b64encode(raw).decode("ascii")
    parts = [encoded[i : i + 8000] for i in range(0, len(encoded), 8000)]
    ordered_parts = []
    for i, part in enumerate(parts, start=1):
        name = f"source.zip.b64.part{i:02d}"
        (RELEASE / name).write_text(part, encoding="ascii")
        ordered_parts.append(
            {"file": name, "chars": len(part), "git_blob_sha": git_blob_sha(part)}
        )

    manifest = {
        "schema_version": "1.0.0",
        "encoding": "base64",
        "ordered_parts": ordered_parts,
        "base64_length": len(encoded),
        "decoded_filename": "GCL_Type_Theory_Volume_IV_PROTOCOL_RC1_Source.zip",
        "decoded_size": len(raw),
        "decoded_sha256": SOURCE_ARCHIVE_SHA,
        "built_source_commit": SOURCE_SHA,
        "reconstruction": "Concatenate ordered parts byte-for-byte with no separators or newline insertion, Base64-decode with validation, then verify size and SHA-256.",
    }
    (RELEASE / "SOURCE_TRANSPORT_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    reconstruct = '''#!/usr/bin/env python3
"""Reconstruct and verify the exact Volume IV PROTOCOL RC1 source archive."""
from __future__ import annotations
import base64, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "SOURCE_TRANSPORT_MANIFEST.json").read_text(encoding="utf-8"))
chunks = []
for part in manifest["ordered_parts"]:
    p = ROOT / part["file"]
    data = p.read_text(encoding="ascii")
    if len(data) != part["chars"]:
        raise SystemExit(f"length mismatch: {p.name}: {len(data)} != {part['chars']}")
    chunks.append(data)
encoded = "".join(chunks)
if len(encoded) != manifest["base64_length"]:
    raise SystemExit(f"base64 length mismatch: {len(encoded)}")
raw = base64.b64decode(encoded, validate=True)
if len(raw) != manifest["decoded_size"]:
    raise SystemExit(f"decoded size mismatch: {len(raw)}")
sha = hashlib.sha256(raw).hexdigest()
if sha != manifest["decoded_sha256"]:
    raise SystemExit(f"sha256 mismatch: {sha}")
out = ROOT / manifest["decoded_filename"]
out.write_bytes(raw)
print(f"verified {out.name} bytes={len(raw)} sha256={sha}")
'''
    (RELEASE / "RECONSTRUCT_SOURCE.py").write_text(reconstruct, encoding="utf-8")

    readme = f'''# Volume IV — PROTOCOL RC1 source admission packet

This directory preserves an exact, content-addressed rebuildable representation of the composition-complete RC1 source archive for **Volume IV — PROTOCOL: Computation as Communication**.

The source archive is the exact built source at `{SOURCE_SHA}` used by Gate-7 run `{GATE7_RUN}`. It is transported as ordered Base64 text chunks. `SOURCE_TRANSPORT_MANIFEST.json` fixes the order, character lengths, Git blob identities, decoded size, and expected SHA-256. Run `python RECONSTRUCT_SOURCE.py` from this directory to reconstruct and verify the archive.

Canonical decoded source identity:

`sha256:{SOURCE_ARCHIVE_SHA}`

This packet is an admission artifact, not a mathematical review or publication-authority record. Until protected merge and protected readback occur, RC1 is composition-complete but not durably admitted. Independent mathematical review remains pending and publication authority is not granted.
'''
    (RELEASE / "README.md").write_text(readme, encoding="utf-8")

    checksums = f'''# Volume IV PROTOCOL RC1 — release identities

{SOURCE_ARCHIVE_SHA}  GCL_Type_Theory_Volume_IV_PROTOCOL_RC1_Source.zip
{MAIN_SHA}  GCL_Type_Theory_Volume_IV_PROTOCOL_RC1.pdf
{SOLUTIONS_SHA}  GCL_Type_Theory_Volume_IV_Solutions_RC1.pdf
{PLATES_SHA}  GCL_Type_Theory_Volume_IV_Plates_01_42_RC1.pdf

State at staging: RC_COMPOSITION_COMPLETE. Durable admission is pending protected merge and readback. Independent mathematical review is pending. Publication authority is not granted.
'''
    (RELEASE / "CHECKSUMS.sha256").write_text(checksums, encoding="utf-8")

    release_record = {
        "schema_version": "1.0.0",
        "series": "TYPE THEORY — The Grand Unified Theory of Computation",
        "volume": "IV",
        "title": "PROTOCOL",
        "subtitle": "Computation as Communication",
        "release": "RC1",
        "composition_status": "RC_COMPOSITION_COMPLETE",
        "durable_admission_status": "PENDING_PROTECTED_MERGE_AND_READBACK",
        "independent_review_status": "PENDING_EXTERNAL_MATHEMATICAL_REVIEW",
        "publication_authority_status": "NOT_GRANTED",
        "source_archive": {
            "filename": "GCL_Type_Theory_Volume_IV_PROTOCOL_RC1_Source.zip",
            "built_source_commit": SOURCE_SHA,
            "size_bytes": SOURCE_ARCHIVE_SIZE,
            "sha256": SOURCE_ARCHIVE_SHA,
            "transport_manifest": "SOURCE_TRANSPORT_MANIFEST.json",
        },
        "distribution_artifacts": {
            "main_pdf_sha256": MAIN_SHA,
            "solutions_pdf_sha256": SOLUTIONS_SHA,
            "plates_pdf_sha256": PLATES_SHA,
        },
        "composition_evidence": {
            "gate7_run_id": GATE7_RUN,
            "gate7_artifact_id": GATE7_ARTIFACT_ID,
            "gate7_artifact_sha256": GATE7_ARTIFACT_DIGEST,
            "main_pages": 77,
            "solutions_pages": 34,
            "plate_folio_pages": 10,
            "canonical_plates": 42,
            "exercises": 168,
            "keyed_solutions_or_rubrics": 168,
            "laboratories": 14,
            "laboratories_passing": 14,
            "index_entries": 58,
            "rendered_page_inspection": "PASS",
            "grayscale_plate_legibility": "PASS",
        },
        "durable_admission": {
            "protected_admission_commit": None,
            "protected_readback_status": "PENDING",
            "source_archive_sha256_readback": None,
        },
        "claim_boundary": "This record identifies the exact RC1 composition source and Gate-7 evidence. It creates no independent mathematical review result, mathematical certification, or publication authority. Durable admission requires protected merge and protected readback.",
    }
    (RELEASE / "RELEASE_RECORD.json").write_text(
        json.dumps(release_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    audit = f'''# Publication Audit RC1 — Composition Complete

Volume IV — **PROTOCOL: Computation as Communication** has completed the internal camera-ready composition pass for RC1. This audit records internal composition evidence only. It is not Gate 8 independent mathematical review, mathematical certification, or publication authority.

## Gate dispositions

- Gate 0 preflight: PASS.
- Gate 1 minimal executable tranche: PASS_PROTECTED_ADMISSION_AND_READBACK under `WORKSET_STATE.json`.
- Gate 2 formal closure: PASS in `THEOREM_AUDIT.md`; theorem and non-result boundaries remain as recorded there.
- Gate 3 pedagogical closure: PASS; 14 chapters, 168 exercises, 168 keyed solutions/rubrics, and 14 retained laboratory source files.
- Gate 4 visual closure: PASS. The 77-page manuscript, 34-page solutions companion, and 10-page 42-plate folio were rendered and inspected. All page contact sheets were visually inspected; affected and warning-associated pages were checked at full resolution. All 42 canonical plates were inspected in the folio, and grayscale inspection confirmed legibility. No clipping, overlap, broken glyph, or arrow/text collision remained.
- Gate 5 scholarship closure: PASS in `BIBLIOGRAPHY_AUDIT.md`.
- Gate 6 notation/index closure: PASS; the publication build produced 58 index entries.
- Gate 7 camera-ready composition RC: PASS for built source `{SOURCE_SHA}` under exact-head workflow run `{GATE7_RUN}`. The canonical RC validator reports 42 plates, zero errors, and zero warnings. All 14 laboratories pass. Clean indexed LuaLaTeX builds of all three publication targets pass. Final diagnostics report no fatal errors, unresolved references or citations, duplicate labels, missing glyphs, or overfull boxes. The retained 25 warning lines are underfull/package notices and were covered by rendered inspection.
- Gate 7A durable RC admission: PENDING protected merge and protected readback.
- Gate 8 independent mathematical review: PENDING_EXTERNAL_MATHEMATICAL_REVIEW after durable RC admission.
- Gate 9 publication authority: NOT_GRANTED.

## Repair evidence

Gate-7 inspection found and corrected two concrete defects before this disposition: canonical plate labels were added to all 42 plate sources; a duplicate physical inclusion of Plate 22 was removed from Chapter 4. A subsequent visual check corrected the Chapter 4 forward wording so it names canonical Plate 22 rather than exposing chapter-local figure numbering. The final correction changed only manuscript page 29 relative to the previously inspected build; the solutions companion and plate folio were raster-identical. Page 29 was re-inspected at full resolution and passed.

## Distribution build identities

- built source commit: `{SOURCE_SHA}`;
- Gate-7 run: `{GATE7_RUN}`;
- main PDF SHA-256: `{MAIN_SHA}`;
- solutions PDF SHA-256: `{SOLUTIONS_SHA}`;
- plates folio SHA-256: `{PLATES_SHA}`;
- exact source archive SHA-256: `{SOURCE_ARCHIVE_SHA}`.

This evidence record is staged in a later administrative commit than the built source above. Its Gate-7 disposition becomes operative only after the containing exact head receives a fresh clean replay confirming that the evidence/release additions did not alter the publication outputs materially.

## Claim boundary

`RC_COMPOSITION_COMPLETE` means that the internal composition/publication gates are closed for this RC1 source. It does not mean that RC1 is durably admitted on protected `main`, independently refereed, mathematically certified as a whole, or publication-authorized. The next permitted transition is Gate 7A exact durable admission and protected readback.
'''
    (ROOT / "PUBLICATION_AUDIT_RC1.md").write_text(audit, encoding="utf-8")

    illustration_path = ROOT / "ILLUSTRATION_REGISTER.md"
    illustration = illustration_path.read_text(encoding="utf-8")
    old_status = (
        "Status: all 42 source plates present in the composition candidate. Plates 1-6 were visually inspected at Gate 1; "
        "plates 7-42 passed standalone new-body rendering. Full 42-plate folio inspection remains a Gate-7 requirement."
    )
    new_status = (
        f"Status: GATE7_VISUAL_CLOSURE_PASS. All 42 canonical plates from built source `{SOURCE_SHA}` were inspected in the final folio; "
        "grayscale inspection also passed. No clipping, overlap, broken glyph, or arrow/text collision remained."
    )
    if old_status not in illustration:
        raise SystemExit("illustration status preimage not found")
    illustration = illustration.replace(old_status, new_status, 1)
    illustration = illustration.replace("GATE1_RENDER_INSPECTED", "GATE7_RENDER_INSPECTED")
    illustration = illustration.replace("SOURCE_COMPLETE__NEW_BODY_RENDERED", "GATE7_RENDER_INSPECTED")
    illustration_path.write_text(illustration, encoding="utf-8")

    state_path = ROOT / "WORKSET_STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["stage"] = "RC_COMPOSITION_COMPLETE"
    state["composition"] = "RC_COMPOSITION_COMPLETE"
    state["gate7"] = {
        "status": "PASS",
        "built_source_commit": SOURCE_SHA,
        "workflow_run_id": GATE7_RUN,
        "artifact_id": GATE7_ARTIFACT_ID,
        "artifact_sha256": GATE7_ARTIFACT_DIGEST,
        "main_pages": 77,
        "solutions_pages": 34,
        "plate_folio_pages": 10,
        "canonical_plates": 42,
        "laboratories_passing": 14,
        "index_entries": 58,
        "rendered_inspection": "PASS",
        "grayscale_plate_legibility": "PASS",
        "source_archive_sha256": SOURCE_ARCHIVE_SHA,
    }
    state["durable_admission"] = "PENDING_GATE7A_PROTECTED_MERGE_AND_READBACK"
    state["independent_review"] = "PENDING_EXTERNAL_MATHEMATICAL_REVIEW_AFTER_DURABLE_RC_ADMISSION"
    state["publication_authority"] = "NOT_GRANTED"
    state["next_action"] = (
        "Run a fresh exact-head Gate-7 confirmation on this evidence/release commit; if clean, admit RC1 through protected Gate 7A merge and readback. "
        "Do not claim Gate 8 review qualification or publication authority."
    )
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    expected = {
        (ROOT / "PUBLICATION_AUDIT_RC1.md").as_posix(),
        (ROOT / "ILLUSTRATION_REGISTER.md").as_posix(),
        (ROOT / "WORKSET_STATE.json").as_posix(),
        (RELEASE / "README.md").as_posix(),
        (RELEASE / "CHECKSUMS.sha256").as_posix(),
        (RELEASE / "RECONSTRUCT_SOURCE.py").as_posix(),
        (RELEASE / "RELEASE_RECORD.json").as_posix(),
        (RELEASE / "SOURCE_TRANSPORT_MANIFEST.json").as_posix(),
    }
    expected.update(
        (RELEASE / f"source.zip.b64.part{i:02d}").as_posix()
        for i in range(1, len(parts) + 1)
    )
    if len(expected) != 29:
        raise SystemExit(f"unexpected release packet path count: {len(expected)}")
    Path("/tmp/expected-release-paths.txt").write_text(
        "\n".join(sorted(expected)) + "\n", encoding="utf-8"
    )
    print(
        f"PACKET_FILES={len(expected)} PARTS={len(parts)} SOURCE_SHA256={SOURCE_ARCHIVE_SHA}"
    )


if __name__ == "__main__":
    main()
