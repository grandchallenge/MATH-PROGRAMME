import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "governance" / "documentary_visual_pedagogy_pilot_audit.json"
MANIFEST = ROOT / "governance" / "visual_pedagogy" / "propagation_manifest.json"
SCHEMA = ROOT / "schemas" / "visual_pedagogy_propagation_manifest.schema.json"
PAGES = sorted((ROOT / "docs" / "documentaries").glob("*.md"))
BATCH_COUNTS = {"1": 6, "2": 6, "3": 5, "4": 4, "5": 5}


def blob_sha(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def audit_rows(audit):
    out = []
    for family in audit["families"]:
        for row in family["assets"]:
            item = dict(row)
            item["family"] = row["asset"].split("/")[3]
            out.append(item)
    return out


def fanout(path):
    suffix = path.removeprefix("docs/")
    return sum(suffix in page.read_text(encoding="utf-8") for page in PAGES)


class VisualPedagogyPropagationStage0Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.rows = audit_rows(cls.audit)

    def test_source_inventory_and_blob_identities(self):
        self.assertEqual(blob_sha(AUDIT.read_bytes()), self.m["audit_source"]["blob_sha"])
        self.assertEqual(len(self.rows), 45)
        self.assertEqual(len(self.m["assets"]), 45)
        self.assertEqual([r["asset"] for r in self.rows], list(self.m["assets"]))
        for row in self.rows:
            path = row["asset"]
            blob, disposition, evidentiary = self.m["assets"][path]
            self.assertEqual(blob, row["blob_sha"])
            self.assertEqual(disposition, row["disposition"])
            self.assertFalse(evidentiary)
            self.assertEqual(blob_sha((ROOT / path).read_bytes()), blob, path)

    def test_exact_counts_and_scope(self):
        counts = Counter(v[1] for v in self.m["assets"].values())
        self.assertEqual(counts, Counter({"KEEP": 19, "REDRAW": 21, "REPLACE": 5}))
        self.assertEqual(self.m["counts"], {"assets":45,"KEEP":19,"REDRAW":21,"REPLACE":5,"migration":26})
        keep = {p for p, v in self.m["assets"].items() if v[1] == "KEEP"}
        migration = set(self.m["migration"])
        self.assertEqual(len(migration), 26)
        self.assertTrue(keep.isdisjoint(migration))

    def test_batches_complete_unique_and_correct_kind(self):
        paths = [p for batch in self.m["batches"].values() for p in batch]
        self.assertEqual(len(paths), 26)
        self.assertEqual(len(set(paths)), 26)
        self.assertEqual(set(paths), set(self.m["migration"]))
        self.assertEqual(self.m["batch_counts"], BATCH_COUNTS)
        for b, n in BATCH_COUNTS.items():
            self.assertEqual(len(self.m["batches"][b]), n)
        for b in ("1","2","3","4"):
            self.assertTrue(all(self.m["assets"][p][1] == "REDRAW" for p in self.m["batches"][b]))
        self.assertTrue(all(self.m["assets"][p][1] == "REPLACE" for p in self.m["batches"]["5"]))
        self.assertTrue(all(self.m["migration"][p][5] for p in self.m["batches"]["5"]))

    def test_rollback_fanout_and_risk_tuple(self):
        rows = {r["asset"]: r for r in self.rows}
        model = self.m["risk_model"]
        for path, rec in self.m["migration"].items():
            batch, rollback, successor_class, route, review, isolated, declared_fanout, risk = rec
            source = rows[path]
            self.assertEqual(rollback, source["blob_sha"])
            measured = fanout(path)
            self.assertGreaterEqual(measured, 1, path)
            self.assertEqual(declared_fanout, measured, path)
            expected = [
                model["disposition_scores"][source["disposition"]],
                model["domain_sensitivity_scores"][source["family"]],
                model["representation_scores"][source["representation"]],
                model["renderer_provenance_scores"][route],
                model["accessibility_adaptation_proxy_scores"][source["audit_depth"]],
                measured,
                model["audit_uncertainty_scores"][source["audit_depth"]],
                path,
            ]
            self.assertEqual(risk, expected, path)

        def key(path):
            return self.m["migration"][path][7]
        redraw = sorted((p for p in self.m["migration"] if self.m["assets"][p][1] == "REDRAW"), key=key)
        replace = sorted((p for p in self.m["migration"] if self.m["assets"][p][1] == "REPLACE"), key=key)
        expected = [redraw[:6], redraw[6:12], redraw[12:17], redraw[17:21]]
        for i, batch in enumerate(expected, 1):
            self.assertEqual(self.m["batches"][str(i)], batch)
        self.assertEqual(self.m["batches"]["5"], replace)

    def test_authority_remains_closed(self):
        a = self.m["authority"]
        self.assertFalse(a["live_switch"])
        self.assertFalse(a["blanket_rewrite"])
        self.assertFalse(a["visual_is_evidence"])
        self.assertTrue(a["per_batch_hs_exact_head"])
        props = self.schema["properties"]["authority"]["properties"]
        self.assertFalse(props["live_switch"]["const"])
        self.assertFalse(props["blanket_rewrite"]["const"])
        self.assertFalse(props["visual_is_evidence"]["const"])


if __name__ == "__main__":
    unittest.main()
