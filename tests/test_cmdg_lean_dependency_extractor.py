from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci" / "extract_cmdg_lean_dependencies.py"
spec = importlib.util.spec_from_file_location("cmdg_lean_extractor", MODULE_PATH)
assert spec is not None and spec.loader is not None
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)

BASE_CONFIG = {
    "schema_version": "1.0.0",
    "fixture_id": "TEST-FIXTURE",
    "project_dir": "fixtures/formal/LOG-GCD-001",
    "module": "LogGcd",
    "roots": ["logGcd_posSemidef"],
    "expected_toolchain_git_blob_sha1": "0" * 40,
    "expected_lake_manifest_git_blob_sha1": "0" * 40,
    "expected_axioms": {"logGcd_posSemidef": ["Classical.choice"]},
    "claim_boundary": {
        "semantic_authority_conferred": False,
        "realizes_as_conferred": False,
        "foundational_concordance_conferred": False,
        "graph_certified_conferred": False,
        "dependency_minimality_claim": False,
    },
}


class CMDGLeanDependencyExtractorTests(unittest.TestCase):
    def assert_code(self, code: str, fn, *args):
        with self.assertRaises(extractor.ExtractionError) as caught:
            fn(*args)
        self.assertEqual(code, caught.exception.code)

    def write_config(self, value: dict) -> Path:
        handle = tempfile.NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8", delete=False)
        json.dump(value, handle)
        handle.close()
        self.addCleanup(Path(handle.name).unlink, missing_ok=True)
        return Path(handle.name)

    def test_claim_boundary_promotion_rejected(self):
        config = copy.deepcopy(BASE_CONFIG)
        config["claim_boundary"]["graph_certified_conferred"] = True
        self.assert_code("PROHIBITED_AUTHORITY_PROMOTION", extractor.load_config, self.write_config(config))

    def test_duplicate_requested_root_rejected(self):
        config = copy.deepcopy(BASE_CONFIG)
        config["roots"] = ["logGcd_posSemidef", "logGcd_posSemidef"]
        self.assert_code("DUPLICATE_REQUESTED_ROOT", extractor.load_config, self.write_config(config))

    def test_malformed_declaration_name_rejected(self):
        config = copy.deepcopy(BASE_CONFIG)
        config["roots"] = ["not a Lean name"]
        self.assert_code("MALFORMED_DECLARATION_NAME", extractor.load_config, self.write_config(config))

    def test_stale_toolchain_pin_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "lean-toolchain").write_text("leanprover/lean4:test\n", encoding="utf-8")
            (project / "lake-manifest.json").write_text("{}\n", encoding="utf-8")
            config = copy.deepcopy(BASE_CONFIG)
            config["expected_toolchain_git_blob_sha1"] = "f" * 40
            config["expected_lake_manifest_git_blob_sha1"] = extractor.git_blob_sha1(project / "lake-manifest.json")
            self.assert_code("STALE_TOOLCHAIN_PIN", extractor.validate_pins, config, project)

    def test_probe_order_is_canonicalized(self):
        stdout = "\n".join([
            "CMDG|ROOT|T.r",
            "CMDG|KIND|theorem",
            "CMDG|MODULE|T",
            "CMDG|DIRECT|z",
            "CMDG|DIRECT|a",
            "CMDG|AXIOM|propext",
            "CMDG|IMPORT|T.Base",
            "CMDG|SEMANTIC_AUTHORITY|false",
            "CMDG|GRAPH_CERTIFIED|false",
        ])
        parsed = extractor.parse_probe(stdout, "")
        self.assertEqual(["a", "z"], parsed["direct"])
        self.assertEqual(["propext"], parsed["axioms"])
        self.assertEqual(["T.Base"], parsed["imports"])

    def test_duplicate_scalar_rejected(self):
        stdout = "\n".join([
            "CMDG|ROOT|T.r",
            "CMDG|ROOT|T.s",
            "CMDG|KIND|theorem",
            "CMDG|MODULE|T",
            "CMDG|SEMANTIC_AUTHORITY|false",
            "CMDG|GRAPH_CERTIFIED|false",
        ])
        self.assert_code("PROBE_OUTPUT_DUPLICATE_SCALAR", extractor.parse_probe, stdout, "")

    def test_probe_authority_promotion_rejected(self):
        stdout = "\n".join([
            "CMDG|ROOT|T.r",
            "CMDG|KIND|theorem",
            "CMDG|MODULE|T",
            "CMDG|SEMANTIC_AUTHORITY|true",
            "CMDG|GRAPH_CERTIFIED|false",
        ])
        self.assert_code("PROHIBITED_AUTHORITY_PROMOTION", extractor.parse_probe, stdout, "")

    def test_observed_edges_remain_proof_only(self):
        probe = {
            "root": "T.r",
            "kind": "theorem",
            "module": "T",
            "direct_signature": [],
            "direct_body": ["T.helper"],
            "direct": ["T.helper"],
            "local_declarations": [{"declaration": "T.helper", "kind": "theorem", "module": "T"}],
            "edges": [{"source": "T.r", "target": "T.helper", "target_module": "T"}],
            "frontier": [],
            "axioms": [],
            "imports": ["Mathlib"],
            "semantic_authority": "false",
            "graph_certified": "false",
        }
        report = extractor.build_root_report("T.r", probe)
        edge = report["observed_direct_proof_edges"][0]
        self.assertEqual("G_proof", edge["layer"])
        self.assertEqual("PROOF_USES_DECLARATION", edge["relation"])
        self.assertEqual("OBSERVED", edge["authority_state"])
        self.assertFalse(edge["semantic_authority"])
        self.assertEqual(["T.helper"], report["derived_local_transitive_closure"])
        self.assertEqual(["T.helper"], report["direct_dependencies"])

    def test_expected_axiom_mismatch_rejected(self):
        config = copy.deepcopy(BASE_CONFIG)
        roots = [{"declaration": "logGcd_posSemidef", "axiom_footprint": {"axioms": ["propext"]}}]
        self.assert_code("AXIOM_FOOTPRINT_MISMATCH", extractor.validate_expected_axioms, config, roots)

    def test_canonical_digest_stable(self):
        a = {"b": [2, 1], "a": {"x": True}}
        b = {"a": {"x": True}, "b": [2, 1]}
        self.assertEqual(extractor.sha256_json(a), extractor.sha256_json(b))
        expected = hashlib.sha256(extractor.canonical_bytes(a)).hexdigest()
        self.assertEqual(expected, extractor.sha256_json(a))


if __name__ == "__main__":
    unittest.main()
