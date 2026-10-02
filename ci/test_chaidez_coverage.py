import copy
import json
import unittest
from validate_chaidez_coverage import LEDGER, ROOT, errors

class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(LEDGER.read_text())

    def test_inventory(self):
        self.assertEqual(errors(self.data), [])

    def test_every_requirement_is_required(self):
        for index in range(len(self.data["requirements"])):
            data = copy.deepcopy(self.data)
            del data["requirements"][index]
            self.assertTrue(errors(data))

    def test_duplicate_requirement_rejected(self):
        self.data["requirements"].append(self.data["requirements"][0])
        self.assertTrue(errors(self.data))

    def test_zero_production_not_exercised(self):
        self.data["requirements"][0]["coverage"] = "PRODUCTION_EXERCISED"
        self.assertTrue(errors(self.data))

    def test_close_requires_receipt(self):
        self.data["phase"] = "CLOSED"
        self.data["integration_receipt"] = None
        self.assertTrue(errors(self.data))

    def test_enforced_requires_each_evidence_pin(self):
        row = self.data["requirements"][0]
        row["coverage"] = "SCHEMA_ENFORCED"
        for field in ("validator", "positive_test", "negative_test"):
            row[field] = copy.deepcopy(row["documentation"])
        self.assertEqual(errors(self.data), [])
        for field in ("validator", "positive_test", "negative_test"):
            case = copy.deepcopy(self.data)
            case["requirements"][0][field] = None
            self.assertTrue(errors(case))

    def test_compatibility_cannot_expand_scope(self):
        base = json.loads((ROOT / "pedagogy/chaidez_v1_v2_compatibility.json").read_text())
        for field, value in (("scope", "ALL_COMPUTATION"), ("historical_rewrite", True),
                             ("resource_ledger_rename", True), ("claim_upgrade", True),
                             ("field_renames", {}), ("exposition_stage_mapping", {})):
            case = copy.deepcopy(base)
            case[field] = value
            self.assertTrue(errors(self.data, case))

if __name__ == "__main__":
    unittest.main()
