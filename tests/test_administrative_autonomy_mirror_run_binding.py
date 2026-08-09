from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
MODULE_PATH = ROOT / "ci" / "administrative_autonomy_runtime_mirror_sync.py"
SPEC = importlib.util.spec_from_file_location(
    "administrative_autonomy_runtime_mirror_sync",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
mirror_sync = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mirror_sync
SPEC.loader.exec_module(mirror_sync)


OLD_RUN = 31284898458
PRODUCER_RUN = 31284996233
HEAD = "5" * 40
DUE = "2026-08-08T18:09:00Z"


def run(
    run_id: int,
    *,
    status: str = "completed",
    conclusion: str | None = "success",
    created_at: str,
) -> dict[str, object]:
    return {
        "id": run_id,
        "status": status,
        "conclusion": conclusion,
        "created_at": created_at,
    }


class AdministrativeAutonomyMirrorRunBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = {
            "merge_control": {
                "maximum_protected_readback_wait_seconds": 1,
                "poll_interval_seconds": 0,
            },
            "mirrors": [
                {
                    "repository": "grandchallenge/MATH-PROGRAMME",
                    "issue": 182,
                },
                {
                    "repository": "grandchallenge/MATH-PROGRAMME",
                    "issue": 183,
                },
                {
                    "repository": "grandchallenge/INTELLECT",
                    "issue": 21,
                },
            ],
        }

    def test_newer_in_progress_producer_blocks_older_success(self) -> None:
        runs = [
            run(
                PRODUCER_RUN,
                status="in_progress",
                conclusion=None,
                created_at="2026-08-08T23:53:43Z",
            ),
            run(
                OLD_RUN,
                created_at="2026-08-08T23:51:02Z",
            ),
        ]
        self.assertEqual(
            0,
            mirror_sync.authoritative_successful_run_id(runs),
        )

    def test_newer_skipped_trigger_does_not_displace_success(self) -> None:
        runs = [
            run(
                PRODUCER_RUN + 1,
                conclusion="skipped",
                created_at="2026-08-08T23:54:10Z",
            ),
            run(
                PRODUCER_RUN,
                created_at="2026-08-08T23:53:43Z",
            ),
        ]
        self.assertEqual(
            PRODUCER_RUN,
            mirror_sync.authoritative_successful_run_id(runs),
        )

    def test_newer_failure_blocks_older_success(self) -> None:
        runs = [
            run(
                PRODUCER_RUN,
                conclusion="failure",
                created_at="2026-08-08T23:53:43Z",
            ),
            run(
                OLD_RUN,
                created_at="2026-08-08T23:51:02Z",
            ),
        ]
        self.assertEqual(
            0,
            mirror_sync.authoritative_successful_run_id(runs),
        )

    def test_newer_success_is_the_attestation(self) -> None:
        runs = [
            run(
                PRODUCER_RUN,
                created_at="2026-08-08T23:53:43Z",
            ),
            run(
                OLD_RUN,
                created_at="2026-08-08T23:51:02Z",
            ),
        ]
        self.assertEqual(
            PRODUCER_RUN,
            mirror_sync.authoritative_successful_run_id(runs),
        )

    def test_all_cross_repository_mirrors_must_match_exact_head_and_due(self) -> None:
        marker = (
            f"- protected MATH-PROGRAMME head: `{HEAD}`\n"
            f"- `structural_sweep` completed through: `{DUE}`\n"
        )

        class Evidence:
            def get(self, path: str):
                if path.endswith("/issues/21"):
                    return {"body": marker.replace(DUE, "2026-08-08T01:21:00Z")}
                return {"body": marker}

        self.assertFalse(
            mirror_sync._mirrors_current(
                Evidence(),
                HEAD,
                "structural_sweep",
                DUE,
                self.runtime,
            )
        )

    def test_current_mirrors_do_not_admit_older_success_while_producer_runs(self) -> None:
        old_success = run(
            OLD_RUN,
            created_at="2026-08-08T23:51:02Z",
        )
        producer_running = run(
            PRODUCER_RUN,
            status="in_progress",
            conclusion=None,
            created_at="2026-08-08T23:53:43Z",
        )
        producer_success = run(
            PRODUCER_RUN,
            created_at="2026-08-08T23:53:43Z",
        )
        snapshots = [
            [producer_running, old_success],
            [producer_success, old_success],
            [producer_success, old_success],
            [producer_success, old_success],
            [producer_success, old_success],
        ]
        observed_paths: list[str] = []

        class Observability:
            def get(self, path: str):
                observed_paths.append(path)
                value = snapshots.pop(0) if snapshots else [producer_success, old_success]
                return {"workflow_runs": value}

        marker = (
            f"- protected MATH-PROGRAMME head: `{HEAD}`\n"
            f"- `structural_sweep` completed through: `{DUE}`\n"
        )

        class Evidence:
            def get(self, path: str):
                return {"body": marker}

        selected = mirror_sync.wait_mirror_sync(
            Observability(),
            Evidence(),
            "grandchallenge/MATH-PROGRAMME",
            HEAD,
            "structural_sweep",
            DUE,
            self.runtime,
        )
        self.assertEqual(PRODUCER_RUN, selected)
        self.assertTrue(observed_paths)
        self.assertTrue(all(f"head_sha={HEAD}" in path for path in observed_paths))

    def test_runtime_patches_binding_before_execute_import(self) -> None:
        text = (ROOT / "ci" / "administrative_autonomy_runtime.py").read_text(
            encoding="utf-8"
        )
        patch_line = (
            "runtime_github.wait_mirror_sync = provenance_bound_wait_mirror_sync"
        )
        execute_import = "from administrative_autonomy_runtime_behind_sync import"
        self.assertIn(patch_line, text)
        self.assertLess(text.index(patch_line), text.index(execute_import))


if __name__ == "__main__":
    unittest.main()
