from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ci.gcl_tcs_cross_surface_orphans import (
    ROOT,
    governed_root_orphan_errors,
    has_strong_governance_identity,
    raw_references,
    reference_errors,
    resolve_reference,
    scratch_boundary_errors,
    cross_surface_orphan_errors,
)


class GclTcsCrossSurfaceOrphanTests(unittest.TestCase):
    def fixture(self):
        return TemporaryDirectory()

    def test_live_repository_cross_surface_passes(self):
        self.assertEqual(cross_surface_orphan_errors(ROOT), [])

    def test_markdown_reference_discovery(self):
        with self.fixture() as directory:
            root = Path(directory)
            target = root / "docs/target.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Target\n", encoding="utf-8")
            source = root / "docs/index.md"
            source.write_text("[Target](target.md)\n", encoding="utf-8")
            self.assertIn("target.md", raw_references(source))
            self.assertEqual(reference_errors([source], root), [])

    def test_html_web_reference_discovery(self):
        with self.fixture() as directory:
            root = Path(directory)
            asset = root / "web/assets/figure.svg"
            asset.parent.mkdir(parents=True)
            asset.write_text("<svg></svg>", encoding="utf-8")
            page = root / "web/page.html"
            page.write_text('<img src="assets/figure.svg">', encoding="utf-8")
            self.assertIn("assets/figure.svg", raw_references(page))
            self.assertEqual(reference_errors([page], root), [])

    def test_tex_source_and_asset_reference_discovery(self):
        with self.fixture() as directory:
            root = Path(directory)
            source_dir = root / "tex"
            source_dir.mkdir()
            (source_dir / "section.tex").write_text("Text", encoding="utf-8")
            (source_dir / "figure.png").write_bytes(b"png")
            main = source_dir / "main.tex"
            main.write_text(
                r"\input{section}" "\n" r"\includegraphics{figure}",
                encoding="utf-8",
            )
            self.assertEqual(reference_errors([main], root), [])

    def test_json_source_record_reference_discovery(self):
        with self.fixture() as directory:
            root = Path(directory)
            (root / "sources").mkdir()
            (root / "sources/source.tex").write_text("source", encoding="utf-8")
            record = root / "record.json"
            record.write_text(json.dumps({"source_record": "sources/source.tex"}), encoding="utf-8")
            self.assertIn("sources/source.tex", raw_references(record))
            self.assertEqual(reference_errors([record], root), [])

    def test_json_candidate_record_reference_discovery(self):
        with self.fixture() as directory:
            root = Path(directory)
            (root / "candidates").mkdir()
            (root / "candidates/CANDIDATE.json").write_text("{}", encoding="utf-8")
            record = root / "registry.json"
            record.write_text(
                json.dumps({"candidate_record": "candidates/CANDIDATE.json"}), encoding="utf-8"
            )
            self.assertEqual(reference_errors([record], root), [])

    def test_static_text_reference_discovery(self):
        with self.fixture() as directory:
            root = Path(directory)
            (root / "records").mkdir()
            (root / "records/receipt.json").write_text("{}", encoding="utf-8")
            note = root / "STATUS.txt"
            note.write_text("source: records/receipt.json\n", encoding="utf-8")
            self.assertIn("records/receipt.json", raw_references(note))
            self.assertEqual(reference_errors([note], root), [])

    def test_governed_directory_registration(self):
        with self.fixture() as directory:
            root = Path(directory)
            governed = root / "governed"
            package = governed / "PACKAGE-001"
            package.mkdir(parents=True)
            (package / "record.json").write_text('{"record_id":"R-1"}', encoding="utf-8")
            index = root / "INDEX.md"
            index.write_text("[Package](governed/PACKAGE-001)\n", encoding="utf-8")
            self.assertEqual(governed_root_orphan_errors(governed, [index], root), [])

    def test_definite_governed_directory_orphan_fails_closed(self):
        with self.fixture() as directory:
            root = Path(directory)
            governed = root / "governed"
            (governed / "PACKAGE-001").mkdir(parents=True)
            index = root / "INDEX.md"
            index.write_text("# No registration\n", encoding="utf-8")
            errors = governed_root_orphan_errors(governed, [index], root)
            self.assertTrue(any("definite governed orphan" in error for error in errors))

    def test_missing_reference_target_fails_closed(self):
        with self.fixture() as directory:
            root = Path(directory)
            source = root / "index.md"
            source.write_text("[Missing](records/missing.json)\n", encoding="utf-8")
            errors = reference_errors([source], root)
            self.assertTrue(any("missing repository reference target" in error for error in errors))

    def test_repository_escape_fails_closed(self):
        with self.fixture() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            source = docs / "index.md"
            source.write_text("[Escape](../../outside.md)\n", encoding="utf-8")
            _, error = resolve_reference(source, "../../outside.md", root)
            self.assertIsNotNone(error)
            self.assertIn("escapes root", error or "")

    def test_plain_scratch_is_not_promoted_or_rejected(self):
        with self.fixture() as directory:
            root = Path(directory)
            scratch = root / "scratch"
            scratch.mkdir()
            (scratch / "notes.txt").write_text("unregistered working note\n", encoding="utf-8")
            self.assertEqual(scratch_boundary_errors(root), [])

    def test_governed_identity_hidden_in_scratch_fails_closed(self):
        with self.fixture() as directory:
            root = Path(directory)
            scratch = root / "scratch"
            scratch.mkdir()
            record = scratch / "record.json"
            record.write_text('{"record_id":"GOV-001","authority_status":"approved"}', encoding="utf-8")
            self.assertTrue(has_strong_governance_identity(record))
            errors = scratch_boundary_errors(root)
            self.assertTrue(any("scratch path contains governed identity markers" in error for error in errors))

    def test_yaml_governed_identity_hidden_in_scratch_fails_closed(self):
        with self.fixture() as directory:
            root = Path(directory)
            scratch = root / "_scratch"
            scratch.mkdir()
            record = scratch / "record.yaml"
            record.write_text("operation_id: OP-001\npromotion_status: candidate\n", encoding="utf-8")
            errors = scratch_boundary_errors(root)
            self.assertTrue(any("scratch path contains governed identity markers" in error for error in errors))

    def test_external_links_are_not_claimed_as_repository_authority(self):
        with self.fixture() as directory:
            root = Path(directory)
            source = root / "index.md"
            source.write_text("[External](https://example.com/x)\n", encoding="utf-8")
            self.assertEqual(reference_errors([source], root), [])

    def test_existing_documentary_authority_remains_manifest_driven(self):
        programme = (ROOT / "ci/validate_programme.py").read_text(encoding="utf-8")
        documentary = (ROOT / "ci/validate_documentary_library.py").read_text(encoding="utf-8")
        legacy = (ROOT / "ci/validate_documentaries.py").read_text(encoding="utf-8")
        self.assertIn("from validate_documentary_library import documentary_contract_errors", programme)
        self.assertIn("errors.extend(documentary_contract_errors())", programme)
        self.assertIn("legacy.collection_discovery_errors", documentary)
        for marker in (
            "discovered_web_pages",
            "discovered_source_records",
            "discovered_documentary_assets",
            "discovered_asset_directories",
            "discovered_candidate_locks",
        ):
            self.assertIn(marker, legacy)

    def test_documentary_authority_is_reachable_from_governed_contract_shard(self):
        registry = json.loads((ROOT / "governance/policy_shard_registry.json").read_text(encoding="utf-8"))
        commands = registry["shards"]["contracts"]
        self.assertIn(["python", "ci/validate_programme.py"], commands)

    def test_control_creates_no_parallel_inventory_file(self):
        module = (ROOT / "ci/gcl_tcs_cross_surface_orphans.py").read_text(encoding="utf-8")
        self.assertNotIn("AUTHORITY_REGISTRY", module)
        self.assertNotIn("ORPHAN_REGISTRY", module)
        self.assertIn("registered_by_text", module)


if __name__ == "__main__":
    unittest.main()
