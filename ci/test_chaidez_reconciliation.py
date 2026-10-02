"""Exact-object boundary tests; never production evidence or remote mutations."""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from reconcile_chaidez_conformance import (
    REPOSITORIES, ROOT, artifact, git, hashes, protected_commit,
    reconcile, safe_path, validate_receipt, validate_shape,
    account_source_entries, require_empty_registry,
)


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="chaidez-reconcile-test.")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        git(self.root, "init", "-q", "--initial-branch=main")
        git(self.root, "config", "user.name", "Non-authoritative fixture")
        git(self.root, "config", "user.email", "fixture@example.invalid")
        git(self.root, "config", "commit.gpgsign", "false")
        git(self.root, "remote", "add", "origin", "https://github.com/grandchallenge/MATHSOLVE.git")
        (self.root / "evidence.json").write_bytes(b'{"claim":"not certified"}\n')
        git(self.root, "add", "evidence.json")
        git(self.root, "commit", "-qm", "Synthetic fixture only")
        self.commit = git(self.root, "rev-parse", "HEAD").decode().strip()
        git(self.root, "update-ref", "refs/remotes/origin/main", self.commit)
        self.ref = {"path": "evidence.json", **hashes((self.root / "evidence.json").read_bytes())}
        self.manifest = {"schema_version": "2.0.0", "operation_id": "CHAIDEZ-V2-HARDENING-001",
                         "repositories": {r: self.commit for r in REPOSITORIES}}
        refs = [{"repository": "grandchallenge/" + r, "commit": self.commit, **self.ref} for r in REPOSITORIES]
        refs.sort(key=lambda r: (r["repository"], r["commit"], r["path"]))
        self.receipt = {"schema_version": "2.0.0", "operation_id": self.manifest["operation_id"],
                        "chain_kind": "POLICY_AND_CANARY_NOT_PRODUCTION", "protected_inputs": self.manifest["repositories"],
                        "artifact_count": 4, "artifacts": refs, "catalog_entry_count": 17288,
                        "production_promotion_count": 0, "production_certification_intake_count": 0,
                        "production_exercised": False, "ordinary_catalog_dossiers": 0,
                        "generic_handoffs_unchanged": 11, "wp06_claim_ledger_unchanged": True}

    def test_exact_protected_blob_and_sha256(self):
        raw = artifact(self.root, "MATHSOLVE", self.commit, self.ref)
        self.assertEqual(hashes(raw), {k: self.ref[k] for k in ("git_blob_sha1", "sha256")})
        self.assertEqual(self.ref["git_blob_sha1"], git(self.root, "rev-parse", "HEAD:evidence.json").decode().strip())
        self.assertEqual(artifact(self.root, "MATHSOLVE", self.commit, self.ref), raw)

    def test_worktree_cannot_replace_protected_bytes(self):
        original = artifact(self.root, "MATHSOLVE", self.commit, self.ref)
        (self.root / "evidence.json").write_text("inflated claim")
        self.assertEqual(artifact(self.root, "MATHSOLVE", self.commit, self.ref), original)

    def test_mutable_missing_and_unprotected_commits(self):
        for value in ("HEAD", "main", "0" * 40):
            with self.subTest(value=value), self.assertRaises((ValueError, subprocess.CalledProcessError)):
                protected_commit(self.root, "MATHSOLVE", value)
        git(self.root, "commit", "--allow-empty", "-qm", "Not admitted")
        candidate = git(self.root, "rev-parse", "HEAD").decode().strip()
        with self.assertRaises(subprocess.CalledProcessError):
            protected_commit(self.root, "MATHSOLVE", candidate)

    def test_wrong_repository_root_or_origin(self):
        with self.assertRaises(ValueError):
            protected_commit(self.root, "MATHCERT", self.commit)
        git(self.root, "remote", "set-url", "origin", "https://example.invalid/grandchallenge/MATHSOLVE")
        with self.assertRaises(ValueError):
            protected_commit(self.root, "MATHSOLVE", self.commit)

    def test_both_digests_are_required_and_independent(self):
        for key, size in (("git_blob_sha1", 40), ("sha256", 64)):
            for missing in (False, True):
                ref = copy.deepcopy(self.ref)
                if missing:
                    del ref[key]
                else:
                    ref[key] = "0" * size
                with self.subTest(key=key, missing=missing), self.assertRaises(ValueError):
                    artifact(self.root, "MATHSOLVE", self.commit, ref)

    def test_unsafe_paths(self):
        for path in (None, "", "/tmp/file", "../file", "a/../b", "a//b", "./a", ".git/config", "a\\b", "C:/file"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                safe_path(path)

    def test_absent_untracked_and_symlink_artifacts(self):
        (self.root / "untracked").write_text("not admitted")
        (self.root / "link").symlink_to("evidence.json")
        git(self.root, "add", "link")
        git(self.root, "commit", "-qm", "Symlink fixture")
        candidate = git(self.root, "rev-parse", "HEAD").decode().strip()
        git(self.root, "update-ref", "refs/remotes/origin/main", candidate)
        for path in ("absent", "untracked", "link"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                artifact(self.root, "MATHSOLVE", candidate, {**self.ref, "path": path})

    def test_all_explicit_roots_and_immutable_manifest_members_required(self):
        for repo in REPOSITORIES:
            manifest = copy.deepcopy(self.manifest)
            del manifest["repositories"][repo]
            with self.assertRaises(ValueError):
                reconcile({}, manifest)
            manifest = copy.deepcopy(self.manifest)
            manifest["repositories"][repo] = "main"
            with self.assertRaises(ValueError):
                validate_shape(manifest, "chaidez_reconciliation_manifest.schema.json")
        with self.assertRaises(ValueError):
            reconcile({}, self.manifest)
        result = subprocess.run(["python3", str(ROOT / "ci/reconcile_chaidez_conformance.py")], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"--programme-root", result.stderr)

    def test_receipt_required_fields_and_inventory(self):
        validate_receipt(self.receipt, self.manifest)
        for key in self.receipt:
            receipt = copy.deepcopy(self.receipt)
            del receipt[key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_receipt(receipt, self.manifest)
        for change in (lambda r: r.update(artifact_count=5),
                       lambda r: r["artifacts"].reverse(),
                       lambda r: r["artifacts"].__setitem__(0, r["artifacts"][1]),
                       lambda r: r["artifacts"][0].update(path="../outside"),
                       lambda r: r["artifacts"][0].update(commit="0" * 40)):
            receipt = copy.deepcopy(self.receipt)
            change(receipt)
            with self.assertRaises(ValueError):
                validate_receipt(receipt, self.manifest)

    def test_receipt_cannot_assert_production_or_mutate_preservation(self):
        for field, value in (("production_exercised", True), ("production_promotion_count", 1),
                             ("production_certification_intake_count", 1), ("ordinary_catalog_dossiers", 1),
                             ("generic_handoffs_unchanged", 10), ("wp06_claim_ledger_unchanged", False),
                             ("catalog_entry_count", 17287), ("chain_kind", "CERTIFIED")):
            receipt = copy.deepcopy(self.receipt)
            receipt[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_receipt(receipt, self.manifest)

    def test_source_inventory_prohibits_dossiers_and_wrong_provider(self):
        provider = {"provider_id": "CANARY", "snapshot_id": "SNAPSHOT-CANARY"}
        entry = {**provider, "catalog_id": "GCL-CAT-CANARY"}
        ids = set()
        self.assertEqual(account_source_entries(json.dumps(entry).encode(), provider, ids), 1)
        self.assertEqual(ids, {entry["catalog_id"]})
        with self.assertRaises(ValueError):
            account_source_entries(json.dumps(entry).encode(), provider, ids)
        for key, value in (("provider_id", "OTHER"), ("snapshot_id", "OTHER"),
                           ("chaidez_dossier", {}), ("promotion_dossier", None),
                           ("promotion_state", "PROMOTED"), ("required_artifacts", {})):
            changed = {**entry, key: value}
            with self.subTest(key=key), self.assertRaises(ValueError):
                account_source_entries(json.dumps(changed).encode(), provider, set())

    def test_explicit_zero_production_registry_is_not_a_canary_registry(self):
        for registry_id, count, records in (("MS-EXTERNAL-CATALOG-PROMOTIONS", "promotion_count", "promotions"),
                                            ("MC-EXTERNAL-CATALOG-INTAKES", "intake_count", "intakes")):
            registry = {"schema_version": "2.0.0", "registry_id": registry_id, count: 0, records: []}
            require_empty_registry(registry, registry_id, count, records)
            for key, value in ((count, 1), (count, False), (records, [{"id": "CANARY"}]),
                               ("schema_version", "1.0.0"), ("registry_id", "OTHER"), ("automatic", True)):
                with self.subTest(key=key), self.assertRaises(ValueError):
                    require_empty_registry({**registry, key: value}, registry_id, count, records)


if __name__ == "__main__":
    unittest.main()
