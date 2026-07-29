#!/usr/bin/env python3
"""Adversarial tests for the Groebner application manifest."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from validate_grobner_manifest import MANIFEST, ManifestError, validate


def source() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def rejected(mutator) -> None:
    manifest = source()
    mutator(manifest)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "manifest.json"
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        try:
            validate(path)
        except ManifestError:
            return
    raise AssertionError("invalid application manifest was accepted")


def main() -> int:
    validate()
    rejected(lambda manifest: manifest["lanes"].pop())
    rejected(lambda manifest: manifest["lanes"].append(manifest["lanes"][0]))
    rejected(lambda manifest: manifest["lanes"][0].update(excluded_inference=""))
    rejected(lambda manifest: manifest["lanes"][1].update(status="queued"))
    rejected(lambda manifest: manifest["lanes"][2].update(status="next_fixture"))
    rejected(lambda manifest: manifest.update(next_fixture_lane="APP-SDK-05"))
    rejected(lambda manifest: manifest["foundation_fixtures"].pop())
    rejected(lambda manifest: manifest["lanes"][3].update(certificate_route=[]))
    rejected(
        lambda manifest: manifest["lanes"][4].update(
            excluded_inference=manifest["lanes"][4]["local_obligation"]
        )
    )
    rejected(lambda manifest: manifest["lanes"][0].pop("resource_budget"))
    rejected(
        lambda manifest: manifest["lanes"][1]["resource_budget"].update(
            max_runtime_seconds=0
        )
    )
    rejected(lambda manifest: manifest["lanes"][2].pop("run_ledger"))
    rejected(
        lambda manifest: manifest["lanes"][3]["run_ledger"].update(
            execution_status="failed",
            termination_status="timeout",
            failure_status="timeout",
            failure_record=None,
            recorded_at="2026-07-28T00:00:00Z",
        )
    )
    rejected(
        lambda manifest: manifest["lanes"][4]["run_ledger"].update(
            execution_status="completed",
            termination_status="success",
            result_artifact=None,
            recorded_at="2026-07-28T00:00:00Z",
        )
    )
    print("adversarial application manifest tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
