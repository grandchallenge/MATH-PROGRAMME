"""Hostile, offline regression tests for editorial freshness without claim promotion."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from erdos_compendium_evidence_freshness import audit

class FreshnessTests(unittest.TestCase):
    def setUp(self):
        self.registry = {"issues": [{"problem_id": i} for i in range(1, 1222)]}
        self.admissions = {"admissions": [], "batches": []}
        self.routes = {"routes": [{
            "route_id": "MC-ROUTE-ERDOS-579-DISPROOF-001",
            "campaign_id": "ERDOS-579-DISPROOF-001",
            "intake_status": "certified",
            "cert_output": {
                "repository": "grandchallenge/MATHCERT",
                "path": "certificates/formal_sources/MC-ERDOS-579-LEVEL5-001.json",
                "digest": "9edadf6c23810612b44c8ac0e7a0d3ad37a782b5",
            },
        }]}
    def test_missing_article_detected(self):
        x = audit(self.registry, self.admissions, self.routes, set())
        self.assertEqual(1, x["unreconciled_certified_results"])
        self.assertFalse(x["review_candidates"][0]["publication_authorized_by_this_record"])
    def test_draft_is_not_admission(self):
        x = audit(self.registry, self.admissions, self.routes, {"0579.md"})
        self.assertEqual(1, x["unreconciled_certified_results"])
        self.assertTrue(x["review_candidates"][0]["manuscript_exists"])
        self.assertFalse(x["review_candidates"][0]["editorial_admitted"])
    def test_actual_admission_clears_only_tracked_drift(self):
        self.admissions["batches"] = [{"entries": [{"problem_id": 579}]}]
        x = audit(self.registry, self.admissions, self.routes, {"0579.md"})
        self.assertEqual([], x["review_candidates"])
        self.assertFalse(x["automatic_publication"])
    def test_pending_is_not_certified(self):
        self.routes["routes"][0]["intake_status"] = "pending"
        self.assertEqual([], audit(self.registry, self.admissions, self.routes, set())["review_candidates"])
    def test_malformed_certificate_fails_closed(self):
        self.routes["routes"][0]["cert_output"] = None
        with self.assertRaises(ValueError):
            audit(self.registry, self.admissions, self.routes, set())
    def test_duplicate_identity_fails_closed(self):
        self.routes["routes"].append(dict(self.routes["routes"][0]))
        with self.assertRaises(ValueError):
            audit(self.registry, self.admissions, self.routes, set())
    def test_catalogue_id_drift_fails_closed(self):
        self.routes["routes"][0]["campaign_id"] = "ERDOS-1222-DISPROOF-001"
        with self.assertRaises(ValueError):
            audit(self.registry, self.admissions, self.routes, set())
if __name__ == "__main__":
    unittest.main()
