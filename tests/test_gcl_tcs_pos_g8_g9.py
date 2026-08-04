from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "docs/council/submissions/GCL-TCS-00_GCL-POS-01_AUTHORITY_DECISION.json"
G8 = ROOT / "docs/council/submissions/GCL-POS-01/reviews/REV-GCLPOS-G8-001.yaml"
G9 = ROOT / "docs/council/submissions/GCL-POS-01/reviews/REV-GCLPOS-G9-001.yaml"
INDEX = ROOT / "docs/council/submissions/GCL-POS-01/reviews/REVIEW_INDEX.yaml"
CONFORMANCE = ROOT / "docs/council/submissions/GCL-POS-01/conformance/GCL-POS-01.conformance.yaml"
MANIFEST = ROOT / "docs/council/submissions/SUBMISSION_MANIFEST.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class GclTcsPosAuthorityTests(unittest.TestCase):
    def test_bounded_pilot_authority_decision(self) -> None:
        record = json.loads(read(DECISION))
        self.assertEqual(record["operation_id"], "GCL-TCS-00-GCL-POS-01-G8-G9-001")
        self.assertEqual(record["disposition"], "APPROVE_CANDIDATE_PILOT_RELEASE")
        self.assertIn("protected_merge", record["effective_condition"])

        self.assertEqual(
            record["artifacts"]["GCL-TCS-00"],
            {
                "version": "0.1.0",
                "version_status": "candidate",
                "authority_status": "admitted",
                "promotion_status": "promoted",
                "sha256": "ea750b9b80b53c7d6ed755978fa4bdf59413fad93cec1db81eb3238372ce61c9",
                "authorized_use": "bounded_candidate_pilot",
            },
        )
        self.assertEqual(
            record["artifacts"]["GCL-POS-01"],
            {
                "version": "0.1.0",
                "version_status": "candidate",
                "authority_status": "admitted",
                "promotion_status": "promoted",
                "sha256": "d8be180052a48655a02612b0d6ca883067abe93f0391c4b9c6561a3867ad4d2c",
                "authorized_use": "bounded_institutional_position_accompanying_pilot",
            },
        )
        self.assertEqual(record["g8"]["decision"], "PASS")
        self.assertEqual(record["g8"]["reviewer_kind"], "agent")
        self.assertEqual(record["g9"]["decision"], "PASS")
        self.assertIs(record["g9"]["exact_head_disposition_required"], True)
        self.assertTrue(record["pilot_obligations"])
        self.assertTrue(record["claim_boundaries"])
        self.assertFalse(any(record["claim_boundaries"].values()))

    def test_cross_record_projection_is_closed(self) -> None:
        g8 = read(G8)
        g9 = read(G9)
        index = read(INDEX)
        conformance = read(CONFORMANCE)
        manifest = read(MANIFEST)

        self.assertIn("decision: PASS", g8)
        self.assertIn("disposition: APPROVE_CANDIDATE_PILOT", g8)
        self.assertIn("openai-gpt-5.6-thinking-referee", g8)
        self.assertIn("decision: PASS", g9)
        self.assertIn("APPROVE_CANDIDATE_PILOT_RELEASE", g9)
        self.assertIn("exact-head Human Steward disposition", g9)
        self.assertEqual(index.count("decision: PASS"), 10)
        self.assertIn("authority_status: admitted", conformance)
        self.assertIn("promotion_status: promoted", conformance)
        self.assertIn("automatic replacement", conformance.lower())
        self.assertIn("APPROVED_FOR_BOUNDED_CANDIDATE_PILOT_PENDING_PROTECTED_MERGE", manifest)
        self.assertIn("No formal ASD-STE100 compliance claim", manifest)
        self.assertIn(
            "No mathematical, certification, novelty, priority, deployment, product, manufacturing, or commercial authority",
            manifest,
        )

    def test_mutations_break_expected_invariants(self) -> None:
        record = json.loads(read(DECISION))
        record["claim_boundaries"]["formal_asd_ste100_compliance"] = True
        with tempfile.TemporaryDirectory() as directory:
            mutated = Path(directory) / "mutated.json"
            mutated.write_text(json.dumps(record), encoding="utf-8")
            loaded = json.loads(read(mutated))
            self.assertTrue(any(loaded["claim_boundaries"].values()))

        record = json.loads(read(DECISION))
        record["artifacts"]["GCL-TCS-00"]["version_status"] = "authoritative"
        self.assertNotEqual(record["artifacts"]["GCL-TCS-00"]["version_status"], "candidate")

        record = json.loads(read(DECISION))
        record["g9"]["exact_head_disposition_required"] = False
        self.assertIsNot(record["g9"]["exact_head_disposition_required"], True)


if __name__ == "__main__":
    unittest.main()
