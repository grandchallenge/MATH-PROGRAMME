#!/usr/bin/env python3
"""Read-only exact-object reconciliation from four explicit authenticated roots."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES = ("MATH-PROGRAMME", "MATHFORGE", "MATHSOLVE", "MATHCERT")
MANIFEST = ROOT / "governance/chaidez_reconciliation_manifest.json"


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def hashes(raw):
    return {"git_blob_sha1": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
            "sha256": hashlib.sha256(raw).hexdigest()}


def safe_path(path):
    if not isinstance(path, str) or not re.fullmatch(r"[A-Za-z0-9_.\-/]+", path) or path.startswith("/") or any(p in ("", ".", "..", ".git") for p in path.split("/")):
        raise ValueError("unsafe repository path")
    return path


def protected_commit(root, repository, commit):
    if repository not in REPOSITORIES or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("unknown repository or mutable commit")
    remote = git(root, "remote", "get-url", "origin").decode().strip().removesuffix(".git")
    expected = "grandchallenge/" + repository
    if remote not in ("https://github.com/" + expected, "git@github.com:" + expected):
        raise ValueError("repository root/origin mismatch")
    git(root, "merge-base", "--is-ancestor", commit, "refs/remotes/origin/main")


def artifact(root, repository, commit, ref):
    protected_commit(root, repository, commit)
    path = safe_path(ref["path"])
    if not git(root, "ls-tree", commit, "--", path).startswith((b"100644 blob ", b"100755 blob ")):
        raise ValueError("artifact must be a regular protected Git blob")
    raw = git(root, "show", f"{commit}:{path}")
    actual = hashes(raw)
    if any(ref.get(k) != v for k, v in actual.items()):
        raise ValueError("Git blob or SHA-256 receipt drift: " + path)
    return raw


def validate_shape(value, schema_name):
    schema = json.loads((ROOT / "schemas" / schema_name).read_text())
    failures = sorted((e.message for e in Draft202012Validator(schema).iter_errors(value)))
    if failures:
        raise ValueError("; ".join(failures))


def account_source_entries(raw, provider, ids):
    count = 0
    for line in raw.splitlines():
        entry = json.loads(line)
        if entry["catalog_id"] in ids or entry["snapshot_id"] != provider["snapshot_id"] or entry["provider_id"] != provider["provider_id"]:
            raise ValueError("duplicate entry or wrong provider snapshot")
        if any(k in entry for k in ("chaidez_dossier", "promotion_dossier", "promotion_state", "required_artifacts")):
            raise ValueError("ordinary catalog entry acquired a promotion dossier")
        ids.add(entry["catalog_id"])
        count += 1
    return count


def require_empty_registry(data, registry_id, count_key, records_key):
    if type(data.get(count_key)) is not int or data != {"schema_version": "2.0.0", "registry_id": registry_id, count_key: 0, records_key: []}:
        raise ValueError("initial release requires an explicit empty production registry")


def validate_receipt(receipt, manifest):
    validate_shape(manifest, "chaidez_reconciliation_manifest.schema.json")
    validate_shape(receipt, "chaidez_reconciliation_receipt.schema.json")
    if receipt["protected_inputs"] != manifest["repositories"]:
        raise ValueError("receipt input commits differ from manifest")
    artifacts = receipt["artifacts"]
    identities = [(r["repository"], r["commit"], safe_path(r["path"])) for r in artifacts]
    if receipt["artifact_count"] != len(artifacts) or len(set(identities)) != len(identities):
        raise ValueError("receipt artifact inventory/count mismatch")
    if identities != sorted(identities):
        raise ValueError("receipt artifacts must have deterministic order")
    for repo, commit in manifest["repositories"].items():
        if not any(r["repository"] == "grandchallenge/" + repo and r["commit"] == commit for r in artifacts):
            raise ValueError("receipt omits a selected repository snapshot")


def reconcile(roots, manifest, coverage=None):
    validate_shape(manifest, "chaidez_reconciliation_manifest.schema.json")
    if set(roots) != set(REPOSITORIES) or set(manifest["repositories"]) != set(REPOSITORIES):
        raise ValueError("all four repository roots and exact pinned commits are required")
    commits = manifest["repositories"]
    for repo, commit in commits.items():
        protected_commit(roots[repo], repo, commit)
    if manifest["schema_version"] != "2.0.0" or manifest["operation_id"] != "CHAIDEZ-V2-HARDENING-001":
        raise ValueError("unknown reconciliation manifest")
    seen = {}
    def read(repo, path, commit=None, ref=None):
        commit = commit or commits[repo]
        safe_path(path)
        if ref is None:
            raw = git(roots[repo], "show", f"{commit}:{path}")
            ref = {"path": path, **hashes(raw)}
        raw = artifact(roots[repo], repo, commit, ref)
        seen[(repo, commit, path)] = {"repository": "grandchallenge/" + repo, "commit": commit, "path": path, **hashes(raw)}
        return raw
    def obj(repo, path, commit=None, ref=None):
        return json.loads(read(repo, path, commit, ref))
    def verify_ref(ref):
        repo = ref["repository"].removeprefix("grandchallenge/")
        if repo not in roots or ref["repository"] != "grandchallenge/" + repo:
            raise ValueError("unexpected repository in provenance")
        return read(repo, ref["path"], ref["commit"], ref)

    contract = obj("MATH-PROGRAMME", "pedagogy/chaidez_protocol_contract.json")
    if contract["schema_version"] != "2.0.0" or contract["external_catalog_promotion"]["full_dossier_trigger"] != "REVIEWED_PROMOTION_TO_MATHSOLVE":
        raise ValueError("Chaidez v2 governing posture drift")
    imported = obj("MATH-PROGRAMME", "governance/mathforge_external_source_imports.json")
    if imported["registry_id"] != "MATHFORGE-EXTERNAL-SOURCE-IMPORTS" or imported["schema_version"] != "2.0.0":
        raise ValueError("unknown Programme import registry")
    foundry = imported["source_foundry"]
    if foundry["repository"] != "grandchallenge/MATHFORGE":
        raise ValueError("unknown source foundry")
    ids = set()
    for provider in imported["providers"]:
        count = 0
        for shard in provider["catalog_shards"]:
            raw = read("MATHFORGE", shard["path"], foundry["commit"], shard)
            count += account_source_entries(raw, provider, ids)
        if count != provider["inventory_count"]:
            raise ValueError("provider inventory mismatch")
    if len(ids) != imported["catalog_release"]["entry_count"] or len(ids) != 17288:
        raise ValueError("approved two-provider inventory changed")
    def forge_refs(value):
        if isinstance(value, dict):
            if {"path", "git_blob_sha1", "sha256"} <= value.keys():
                read("MATHFORGE", value["path"], foundry["commit"], value)
                # Documentation may advance main without advancing admitted catalog bytes.
                read("MATHFORGE", value["path"], commits["MATHFORGE"], value)
            else:
                for child in value.values():
                    forge_refs(child)
        elif isinstance(value, list):
            for child in value:
                forge_refs(child)
    forge_refs(imported)

    solve = obj("MATHSOLVE", "governance/external_semantic_catalog_intake.json")
    for key in ("programme_authority", "chaidez_authority"):
        ref = solve[key]
        raw = git(roots["MATH-PROGRAMME"], "show", ref["commit"] + ":" + ref["path"])
        if hashes(raw)["git_blob_sha1"] != ref["git_blob_sha1"]:
            raise ValueError("Solve authority blob drift")
        read("MATH-PROGRAMME", ref["path"], ref["commit"], {**ref, "sha256": hashes(raw)["sha256"]})
        if raw != read("MATH-PROGRAMME", ref["path"]):
            raise ValueError("Solve authority differs from the selected Programme snapshot")
    registry = obj("MATHSOLVE", "governance/external_catalog_promotion_registry.json")
    require_empty_registry(registry, "MS-EXTERNAL-CATALOG-PROMOTIONS", "promotion_count", "promotions")
    if git(roots["MATHSOLVE"], "ls-tree", "-r", "--name-only", commits["MATHSOLVE"], "--", "promotions/external_catalog").strip():
        raise ValueError("unregistered production dossier exists")
    if obj("MATHSOLVE", "schemas/external_catalog_promotion_dossier.schema.json")["properties"]["schema_version"]["const"] != "2.0.0":
        raise ValueError("provisional dossier schema is still operative")
    legacy = obj("MATHSOLVE", "governance/external_catalog_legacy_migration.json")
    if legacy["classification"] != "LEGACY_PRE_CATALOG_ROUTE" or legacy["catalog_disposition"] != "NOT_A_CATALOG_PROMOTION" or legacy["inherited_campaign_authority"] or legacy["inherited_certification_authority"]:
        raise ValueError("legacy route acquired promotion authority")
    read("MATHSOLVE", legacy["preserved_artifact"]["path"], ref=legacy["preserved_artifact"])
    handoffs = obj("MATHSOLVE", "contracts/chaidez/generic_handoff_baseline.json")
    if handoffs["handoff_count"] != 11:
        raise ValueError("generic handoff baseline changed")
    for ref in handoffs["artifacts"]:
        read("MATHSOLVE", ref["path"], ref=ref)
        read("MATHSOLVE", ref["path"], handoffs["baseline_commit"], ref)
    wp06 = obj("MATHSOLVE", "domains/union_closed/WP06_ideal_family_bridge/chaidez_v2_conformance.json")
    if wp06["disposition"] != "ACTIVE_REFERENCE_PACKAGE_NOT_CATALOG_PROMOTION" or wp06["result_status"]["support_route_class"] != "FORMAL_PROOF":
        raise ValueError("WP06 reference boundary changed")
    for ref in wp06["required_artifacts"].values():
        read("MATHSOLVE", ref["path"], ref=ref)
    for key in ("baseline_claim_ledger", "certification_reference"):
        reference = wp06[key]
        verify_ref({"repository": reference["repository"], "commit": reference["commit"], **reference["artifact"]})
    if wp06["required_artifacts"]["CLAIM_LEDGER"] != wp06["baseline_claim_ledger"]["artifact"]:
        raise ValueError("WP06 claim ledger changed")

    received = obj("MATHCERT", "governance/external_catalog_certification_intakes.json")
    require_empty_registry(received, "MC-EXTERNAL-CATALOG-INTAKES", "intake_count", "intakes")
    if git(roots["MATHCERT"], "ls-tree", "-r", "--name-only", commits["MATHCERT"], "--", "intakes/external_catalog").strip():
        raise ValueError("unregistered production certification intake exists")
    cert_source = obj("MATHCERT", "governance/external_catalog_solve_contract.json")
    if cert_source["repository"] != "grandchallenge/MATHSOLVE" or cert_source["commit"] != commits["MATHSOLVE"]:
        raise ValueError("Cert does not consume the selected protected Solve gate")
    for ref in cert_source["files"]:
        raw = read("MATHSOLVE", ref["path"], cert_source["commit"], ref)
        if raw != read("MATHCERT", "contracts/chaidez_solve/" + ref["path"]):
            raise ValueError("Cert's vendored Solve gate differs from protected source")
    obj("MATHCERT", "schemas/external_catalog_certification_intake.schema.json")
    read("MATHCERT", "ci/validate_external_catalog_certification_intake.py")
    read("MATHCERT", "ci/test_external_catalog_certification_intake.py")
    read("MATHCERT", "ci/check_ledgers.py")
    read("MATHFORGE", "catalog/README.md")
    read("MATHSOLVE", "ci/test_external_catalog_promotion_dossiers.py")
    lane = obj("MATHCERT", "governance/certification_platform_lane.json")
    control_paths = ["ci/check_ledgers.py", "ci/validate_external_catalog_certification_intake.py",
                     "ci/test_external_catalog_certification_intake.py",
                     "schemas/external_catalog_certification_intake.schema.json",
                     "governance/external_catalog_certification_intakes.json",
                     "governance/external_catalog_solve_contract.json",
                     "docs/EXTERNAL_CATALOG_CERTIFICATION_INTAKE.md"]
    control_paths += ["contracts/chaidez_solve/" + r["path"] for r in cert_source["files"]]
    if not set(control_paths) <= set(lane["shared_platform_paths"]) or lane["rules"]["platform_changes_require_full_estate"] is not True:
        raise ValueError("receiving controls are not protected FULL_ESTATE platform paths")
    # Optional closed-ledger readback is separate from the receipt to avoid a
    # self-referential commit hash. It never changes this deterministic output.
    if coverage is not None:
        from validate_chaidez_coverage import errors
        failures = errors(coverage)
        if failures:
            raise ValueError("; ".join(failures))
        for row in coverage["requirements"]:
            for key in ("documentation", "validator", "positive_test", "negative_test"):
                ref = row[key]
                if ref is not None:
                    repo = ref["repository"].removeprefix("grandchallenge/")
                    artifact(roots[repo], repo, ref["commit"], ref)
        if coverage["integration_receipt"]:
            ref = coverage["integration_receipt"]
            repo = ref["repository"].removeprefix("grandchallenge/")
            pinned_receipt = json.loads(artifact(roots[repo], repo, ref["commit"], ref))
            validate_receipt(pinned_receipt, manifest)
    artifacts = [seen[key] for key in sorted(seen)]
    result = {"schema_version": "2.0.0", "operation_id": manifest["operation_id"],
            "chain_kind": "POLICY_AND_CANARY_NOT_PRODUCTION", "protected_inputs": commits,
            "artifact_count": len(artifacts), "artifacts": artifacts, "catalog_entry_count": len(ids),
            "production_promotion_count": 0, "production_certification_intake_count": 0,
            "production_exercised": False, "ordinary_catalog_dossiers": 0,
            "generic_handoffs_unchanged": 11, "wp06_claim_ledger_unchanged": True}
    validate_receipt(result, manifest)
    if coverage is not None and coverage["integration_receipt"] and pinned_receipt != result:
        raise ValueError("closed coverage receipt differs from replay")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("programme", "forge", "solve", "cert"):
        parser.add_argument("--" + flag + "-root", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--check-receipt", type=Path)
    parser.add_argument("--coverage-ledger", type=Path)
    args = parser.parse_args()
    roots = dict(zip(REPOSITORIES, (args.programme_root, args.forge_root, args.solve_root, args.cert_root)))
    coverage = json.loads(args.coverage_ledger.read_text()) if args.coverage_ledger else None
    result = reconcile(roots, json.loads(args.manifest.read_text()), coverage)
    if args.check_receipt and json.loads(args.check_receipt.read_text()) != result:
        raise SystemExit("deterministic reconciliation receipt mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
