import copy
import json
import unittest

from ci.validate_mathforge_external_source_imports import (
    PROJECTION_PATH,
    PUBLIC_INDEX_PATH,
    REGISTRY_PATH,
    import_errors,
)


class ExternalSourceImportTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        self.projection = json.loads(PROJECTION_PATH.read_text(encoding="utf-8"))
        self.public_index = json.loads(PUBLIC_INDEX_PATH.read_text(encoding="utf-8"))

    def errors(self, registry=None, projection=None, public_index=None):
        return import_errors(
            registry if registry is not None else self.registry,
            projection=projection if projection is not None else self.projection,
            public_index=public_index if public_index is not None else self.public_index,
        )

    def test_committed_registry_projection_and_public_index(self):
        self.assertEqual(self.errors(), [])

    def test_rejects_provider_commit_drift(self):
        mutated = copy.deepcopy(self.registry)
        mutated["source_foundry"]["commit"] = "1" * 40
        self.assertTrue(self.errors(registry=mutated))

    def test_rejects_artifact_identity_drift(self):
        mutated = copy.deepcopy(self.registry)
        mutated["providers"][0]["catalog_shards"][0]["sha256"] = "0" * 64
        self.assertTrue(self.errors(registry=mutated))

    def test_rejects_legacy_authority_inflation(self):
        mutated = copy.deepcopy(self.registry)
        mutated["legacy_registry"]["authority"] = True
        self.assertTrue(self.errors(registry=mutated))

    def test_rejects_claim_ledger_mutation(self):
        mutated = copy.deepcopy(self.projection)
        mutated["canonical_claim_ledger_mutation"] = True
        self.assertTrue(self.errors(projection=mutated))

    def test_rejects_automated_equivalence(self):
        mutated = copy.deepcopy(self.projection)
        mutated["typed_edges"][0]["review_state"] = "AUTOMATED_PROPOSAL"
        mutated["typed_edges"][0]["predicate"] = "same_statement"
        self.assertTrue(self.errors(projection=mutated))

    def test_rejects_restricted_full_text_publication(self):
        mutated = copy.deepcopy(self.public_index)
        entry = next(item for item in mutated["entries"] if item["provider"] == "FC-GDM")
        entry["visibility"] = "full_text"
        entry["title"] = "∀ x, p x → q x"
        self.assertTrue(self.errors(public_index=mutated))

    def test_rejects_unknown_assurance_tier(self):
        mutated = copy.deepcopy(self.public_index)
        mutated["entries"][0]["assurance"] = "CERTIFIED"
        self.assertTrue(self.errors(public_index=mutated))


if __name__ == "__main__":
    unittest.main()
