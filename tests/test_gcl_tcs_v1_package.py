import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from ci.gcl_tcs_v1_package import PACKAGE, errors


class CandidatePackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name) / "package"
        shutil.copytree(PACKAGE, self.package)

    def test_candidate_package(self):
        self.assertEqual(errors(self.package), [])

    def test_payload_tamper_rejected(self):
        with (self.package / "GCL-TCS-00.md").open("a") as stream:
            stream.write("\nUnreviewed change\n")
        self.assertTrue(any("payload drift" in e for e in errors(self.package)))

    def test_unlisted_payload_rejected(self):
        (self.package / "extra.txt").write_text("orphan")
        self.assertIn("inventory mismatch", errors(self.package))

    def test_false_promotion_rejected(self):
        path = self.package / "manifest.json"
        manifest = json.loads(path.read_text())
        manifest.update(authority_status="authoritative", g8="PASS", g9="PASS")
        path.write_text(json.dumps(manifest))
        self.assertEqual(sum("candidate boundary" in e for e in errors(self.package)), 3)

    def test_traversal_rejected(self):
        path = self.package / "manifest.json"
        manifest = json.loads(path.read_text())
        manifest["files"][0]["path"] = "../outside"
        path.write_text(json.dumps(manifest))
        self.assertTrue(any("unsafe path" in e for e in errors(self.package)))

    def test_old_declaration_identity_is_not_silently_admitted(self):
        schema = json.loads((self.package / "schemas/gcl-tcs-conformance.schema.json").read_text())
        record = yaml.safe_load((self.package / "templates/GCL-TCS-00.conformance.template.yaml").read_text())
        record["standard"]["version"] = "0.1.0"
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(record)))

    def test_normative_delta_is_only_documented_identity_changes(self):
        root = Path(__file__).resolve().parents[1]
        parts = sorted((root / "council_submissions/GCL-TCS-00/parts").glob("*.md"))
        self.assertEqual(len(parts), 7)
        expected = "".join(p.read_text(encoding="utf-8") for p in parts)
        expected = expected.replace("0.1.0", "1.0.0").replace("2026-07-27", "2026-09-05")
        expected = expected.replace("| Supersedes | None |", "| Supersedes | No effective supersession before G9; predecessor GCL-TCS-00@0.1.0 |")
        self.assertEqual((self.package / "GCL-TCS-00.md").read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
