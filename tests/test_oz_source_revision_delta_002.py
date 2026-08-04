from __future__ import annotations

import copy
import json
import unittest

from campaigns.odd_zeta.OZ_SOURCE_REVISION_DELTA_002.validate import (
    RECORD_PATH,
    validation_errors,
)

BASE = json.loads(RECORD_PATH.read_text(encoding="utf-8"))


class SourceRevisionDeltaMutationTests(unittest.TestCase):
    def assertRejected(self, mutate) -> None:
        candidate = copy.deepcopy(BASE)
        mutate(candidate)
        self.assertTrue(validation_errors(candidate))

    def test_baseline_accepts(self) -> None:
        self.assertEqual(validation_errors(copy.deepcopy(BASE)), [])

    def test_rejects_source_head_drift(self) -> None:
        self.assertRejected(
            lambda x: x["authority"].__setitem__(
                "candidate_source_head", x["authority"]["protected_source_pin"]
            )
        )

    def test_rejects_premature_archive_binding(self) -> None:
        def mutate(x):
            x["authority"]["archive_sha256"] = "0" * 64
        self.assertRejected(mutate)

    def test_rejects_t3_promotion(self) -> None:
        self.assertRejected(lambda x: x["boundaries"].__setitem__("t3_proved", True))

    def test_rejects_depth_promotion(self) -> None:
        self.assertRejected(
            lambda x: x["depth_impact"].__setitem__("programme_state", "CERTIFIED")
        )

    def test_rejects_rank_drift(self) -> None:
        self.assertRejected(lambda x: x["depth_impact"].__setitem__("joint_rank", 323))

    def test_rejects_silent_t1_t3_equivalence(self) -> None:
        self.assertRejected(
            lambda x: x["t1_top_t3_concordance"].__setitem__(
                "relation", "IDENTICAL"
            )
        )

    def test_rejects_missing_conjectural_class(self) -> None:
        def mutate(x):
            for claim in x["claim_register"]:
                if claim["classification"] == "CONJECTURAL":
                    claim["classification"] = "PROVED_SOURCE_CLAIM_PENDING_INDEPENDENT_REPLAY"
        self.assertRejected(mutate)

    def test_rejects_duplicate_claim_id(self) -> None:
        self.assertRejected(
            lambda x: x["claim_register"][1].__setitem__(
                "id", x["claim_register"][0]["id"]
            )
        )

    def test_rejects_sharp12_route_opening(self) -> None:
        def mutate(x):
            for route in x["route_recommendations"]:
                if route["id"] == "OZ-ROUTE-R004":
                    route["state"] = "READY"
        self.assertRejected(mutate)


if __name__ == "__main__":
    unittest.main()
