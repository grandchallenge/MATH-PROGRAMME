#!/usr/bin/env python3
import validate_workflow_coverage_v3 as v3

v3.legacy.EXPECTED_WORKFLOWS = set(v3.legacy.EXPECTED_WORKFLOWS) | {
    "aether-controls-admin.yml",
    "cmdg-nat-concordance.yml",
    "cmdg-euclid-bridge.yml",
    "cmdg-vertical-spine-v0.yml",
    "cmdg-condensed-cm1.yml",
    "cmdg-condensed-cm2.yml",
    "cmdg-condensed-cm3.yml",
    "cmdg-solid-c05.yml",
    "cmdg-condensed-cm4.yml",
    "cmdg-condensed-cm4-p2.yml",
    "cmdg-condensed-cm4-p2-d.yml",
    "cmdg-condensed-cm4-p2-e.yml",
}

ROOT = v3.ROOT
workflow_coverage_errors = v3.workflow_coverage_errors
main = v3.main

__all__ = ["ROOT", "workflow_coverage_errors", "main"]

if __name__ == "__main__":
    raise SystemExit(main())
