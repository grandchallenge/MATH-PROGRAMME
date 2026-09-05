"""Validate candidate packaging only; never emit a promotion decision."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "council_submissions/GCL-TCS-00/releases/1.0.0"


def errors(package: Path = PACKAGE) -> list[str]:
    problems = []
    manifest = json.loads((package / "manifest.json").read_text())
    for key, expected in {"artifact_id": "GCL-TCS-00", "version": "1.0.0",
                          "authority_status": "candidate", "promotion_status": "registered",
                          "g8": "DEFERRED", "g9": "DEFERRED"}.items():
        if manifest.get(key) != expected:
            problems.append(f"candidate boundary: {key}")
    listed = []
    for item in manifest["files"]:
        name = item["path"]
        original = package / name
        path = original.resolve()
        if not path.is_relative_to(package.resolve()) or original.is_symlink():
            problems.append(f"unsafe path: {name}")
            continue
        listed.append(name)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            problems.append(f"payload drift: {name}")
    actual = {p.relative_to(package).as_posix() for p in package.rglob("*")
              if p.is_file() and p != package / "manifest.json"}
    if set(listed) != actual or len(listed) != len(set(listed)):
        problems.append("inventory mismatch")
    schema = json.loads((package / "schemas/gcl-tcs-conformance.schema.json").read_text())
    records = json.loads((package / "schemas/gcl-tcs-record-contracts.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(records)
    template = yaml.safe_load((package / "templates/GCL-TCS-00.conformance.template.yaml").read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    problems.extend(f"template: {e.message}" for e in validator.iter_errors(template))
    policy = yaml.safe_load((package / "GCL-TCS-00.policy.yaml").read_text())
    if policy["standard"]["version"] != "1.0.0" or policy["standard"]["status"] != "candidate":
        problems.append("policy identity mismatch")
    if "| Version | 1.0.0 |" not in (package / "GCL-TCS-00.md").read_text():
        problems.append("normative identity mismatch")
    return problems
