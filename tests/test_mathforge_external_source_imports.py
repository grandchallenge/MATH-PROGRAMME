import copy
import json
import unittest

from ci.validate_mathforge_external_source_imports import REGISTRY_PATH, import_errors


class ExternalSourceImportTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_committed_registry(self):
        self.assertEqual(import_errors(self.registry), [])

    def test_rejects_provider_commit_drift(self):
        mutated = copy.deepcopy(self.registry)
        mutated["provider_commit"] = "0" * 40
        self.assertTrue(import_errors(mutated))

    def test_rejects_admission_inflation(self):
        mutated = copy.deepcopy(self.registry)
        mutated["sources"][0]["programme_disposition"] = "ADMITTED_PROVIDER_EVIDENCE"
        self.assertTrue(import_errors(mutated))

    def test_rejects_artifact_identity_drift(self):
        mutated = copy.deepcopy(self.registry)
        mutated["sources"][0]["artifacts"][0]["git_blob_sha1"] = "0" * 40
        self.assertTrue(import_errors(mutated))


if __name__ == "__main__":
    unittest.main()
