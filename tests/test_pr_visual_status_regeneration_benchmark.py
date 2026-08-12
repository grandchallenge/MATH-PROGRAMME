from __future__ import annotations

import json
import math
import os
import platform
import statistics
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import pr_visual_status_policy as policy  # noqa: E402


WARMUP_ITERATIONS = 3
MEASURED_ITERATIONS = 30
EXPECTED_CASES = 8
ARCHIVE_ROOT = ROOT / "governance" / "pr_visual_status_archive" / "grandchallenge" / "MATH-PROGRAMME"
RESULT_MARKER = "PRVSR_C10_REGEN_BENCHMARK_JSON="


def p95_nearest_rank(values: list[float]) -> float:
    ordered = sorted(values)
    rank = max(1, math.ceil(0.95 * len(ordered)))
    return ordered[rank - 1]


def regenerate(report_path: Path) -> tuple[str, str, dict]:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    sealed = policy.seal_report(report)
    text = policy.render_text(sealed)
    svg = policy.render_svg(sealed)
    return text, svg, sealed


class TestPRVisualStatusRegenerationBenchmark(unittest.TestCase):
    def test_isolated_regeneration_latency_and_determinism(self) -> None:
        report_paths = sorted(ARCHIVE_ROOT.glob("pr-*/PRVSR-P??-001/report.json"))
        self.assertEqual(len(report_paths), EXPECTED_CASES)

        cases: list[dict] = []
        all_samples: list[float] = []

        for report_path in report_paths:
            original = json.loads(report_path.read_text(encoding="utf-8"))
            expected_text = report_path.with_name("report.txt").read_text(encoding="utf-8")
            expected_svg = report_path.with_name("report.svg").read_text(encoding="utf-8")

            for _ in range(WARMUP_ITERATIONS):
                text, svg, sealed = regenerate(report_path)
                self.assertEqual(sealed, original)
                self.assertEqual(text, expected_text)
                self.assertEqual(svg, expected_svg)

            samples_ms: list[float] = []
            for _ in range(MEASURED_ITERATIONS):
                started = time.perf_counter_ns()
                text, svg, sealed = regenerate(report_path)
                elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
                self.assertEqual(sealed, original)
                self.assertEqual(text, expected_text)
                self.assertEqual(svg, expected_svg)
                samples_ms.append(elapsed_ms)

            all_samples.extend(samples_ms)
            cases.append(
                {
                    "report_id": original["report_id"],
                    "pr_number": original["identity"]["pr_number"],
                    "operative_state": original["derived"]["operative_state"],
                    "median_ms": statistics.median(samples_ms),
                    "p95_ms": p95_nearest_rank(samples_ms),
                    "max_ms": max(samples_ms),
                    "measured_iterations": MEASURED_ITERATIONS,
                    "deterministic_equivalence_failures": 0,
                }
            )

        result = {
            "benchmark_id": "PRVSR-C10-REGEN-BENCH-001",
            "protocol_id": "PRVSR-C10-MEASUREMENT-PROTOCOL-001",
            "scope": "isolated deterministic canonical-report derivation plus text/SVG regeneration",
            "network_latency_included": False,
            "whole_repository_ci_fanout_included": False,
            "warmup_iterations_per_case": WARMUP_ITERATIONS,
            "measured_iterations_per_case": MEASURED_ITERATIONS,
            "p95_method": "nearest_rank",
            "generator_version": policy.GENERATOR_VERSION,
            "report_schema_version": policy.SCHEMA_VERSION,
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "runner": {
                "github_actions": os.environ.get("GITHUB_ACTIONS"),
                "runner_os": os.environ.get("RUNNER_OS"),
                "runner_arch": os.environ.get("RUNNER_ARCH"),
                "runner_name": os.environ.get("RUNNER_NAME"),
                "image_os": os.environ.get("ImageOS"),
                "image_version": os.environ.get("ImageVersion"),
                "github_sha": os.environ.get("GITHUB_SHA"),
                "github_run_id": os.environ.get("GITHUB_RUN_ID"),
                "github_job": os.environ.get("GITHUB_JOB"),
            },
            "cases": cases,
            "aggregate": {
                "sample_count": len(all_samples),
                "median_ms": statistics.median(all_samples),
                "p95_ms": p95_nearest_rank(all_samples),
                "max_ms": max(all_samples),
                "deterministic_equivalence_failures": 0,
            },
        }
        print(RESULT_MARKER + json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    unittest.main()
