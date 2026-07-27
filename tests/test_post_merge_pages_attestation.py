"""Disposable end-to-end attestation for PR #97's publication chain.

The test always terminates the disposable audit run after writing either a PASS
record or a complete failure record to ``campaign-replays.log``. The existing
policy workflow then preserves that file through its governed failure-artifact
route. This branch and PR must never be merged.
"""

from __future__ import annotations

import json
import re
import unittest
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPOSITORY = "grandchallenge/MATH-PROGRAMME"
TARGET_SHA = "ebb73aa1b2c025e52b741cce9756cb0e268e17ef"
API_ROOT = f"https://api.github.com/repos/{REPOSITORY}"
USER_AGENT = "MATH-PROGRAMME-post-merge-pages-attestation"
EVIDENCE_PATH = Path("campaign-replays.log")


def _request_json(path: str) -> Any:
    request = urllib.request.Request(
        f"{API_ROOT}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def _download(path: str) -> bytes:
    request = urllib.request.Request(
        f"{API_ROOT}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def _fetch_live(url: str) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.status, response.read().decode("utf-8", errors="replace")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class PostMergePagesAttestationTests(unittest.TestCase):
    def test_capture_exact_policy_artifact_and_pages_evidence(self) -> None:
        evidence: dict[str, Any] = {
            "attested_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "target_sha": TARGET_SHA,
            "status": "IN_PROGRESS",
            "stages": [],
        }

        try:
            run_query = urllib.parse.urlencode(
                {"branch": "main", "event": "push", "per_page": 100}
            )
            run_listing = _request_json(f"/actions/runs?{run_query}")
            policy_runs = [
                run
                for run in run_listing.get("workflow_runs", [])
                if run.get("head_sha") == TARGET_SHA
                and run.get("name") == "Programme policy checks"
            ]
            _require(bool(policy_runs), f"no main-push policy run for {TARGET_SHA}")
            policy_run = max(
                policy_runs,
                key=lambda run: run.get("run_started_at")
                or run.get("created_at")
                or "",
            )
            evidence["policy_run"] = {
                "id": int(policy_run["id"]),
                "number": policy_run["run_number"],
                "url": policy_run["html_url"],
                "event": policy_run.get("event"),
                "head_branch": policy_run.get("head_branch"),
                "status": policy_run.get("status"),
                "conclusion": policy_run.get("conclusion"),
            }
            _require(policy_run.get("event") == "push", "policy run is not push-triggered")
            _require(policy_run.get("head_branch") == "main", "policy run is not on main")
            _require(policy_run.get("status") == "completed", "policy run is incomplete")
            _require(policy_run.get("conclusion") == "success", "policy run failed")
            policy_run_id = int(policy_run["id"])
            evidence["stages"].append("main_push_policy_success")

            artifact_listing = _request_json(
                f"/actions/runs/{policy_run_id}/artifacts?per_page=100"
            )
            artifacts = [
                artifact
                for artifact in artifact_listing.get("artifacts", [])
                if artifact.get("name") == "validated-site"
                and not artifact.get("expired")
            ]
            _require(
                len(artifacts) == 1,
                f"expected one live validated-site artifact, found {len(artifacts)}",
            )
            artifact = artifacts[0]
            artifact_id = int(artifact["id"])
            artifact_digest = str(artifact.get("digest", ""))
            _require(
                re.fullmatch(r"sha256:[0-9a-f]{64}", artifact_digest) is not None,
                f"invalid artifact digest: {artifact_digest!r}",
            )
            evidence["validated_site_artifact"] = {
                "id": artifact_id,
                "metadata_digest": artifact_digest,
                "expired": bool(artifact.get("expired")),
            }
            evidence["stages"].append("validated_site_artifact_present")

            deployment_run_query = urllib.parse.urlencode(
                {"event": "workflow_run", "per_page": 100}
            )
            deployment_run_listing = _request_json(
                f"/actions/runs?{deployment_run_query}"
            )
            deployment_runs = [
                run
                for run in deployment_run_listing.get("workflow_runs", [])
                if run.get("head_sha") == TARGET_SHA
                and run.get("name") == "Deploy documentation site"
            ]
            _require(
                bool(deployment_runs),
                f"no Deploy documentation site workflow_run for {TARGET_SHA}",
            )
            deployment_run = max(
                deployment_runs,
                key=lambda run: run.get("run_started_at")
                or run.get("created_at")
                or "",
            )
            evidence["pages_workflow_run"] = {
                "id": int(deployment_run["id"]),
                "number": deployment_run["run_number"],
                "url": deployment_run["html_url"],
                "event": deployment_run.get("event"),
                "status": deployment_run.get("status"),
                "conclusion": deployment_run.get("conclusion"),
            }
            _require(deployment_run.get("event") == "workflow_run", "wrong Pages event")
            _require(deployment_run.get("status") == "completed", "Pages run is incomplete")
            _require(deployment_run.get("conclusion") == "success", "Pages run failed")
            deployment_run_id = int(deployment_run["id"])
            evidence["stages"].append("pages_workflow_success")

            jobs_listing = _request_json(
                f"/actions/runs/{deployment_run_id}/jobs?per_page=100"
            )
            jobs = {job["name"]: job for job in jobs_listing.get("jobs", [])}
            evidence["pages_jobs"] = {
                name: {
                    "id": int(job["id"]),
                    "status": job.get("status"),
                    "conclusion": job.get("conclusion"),
                }
                for name, job in jobs.items()
            }
            _require(jobs.get("build", {}).get("conclusion") == "success", "Pages build job failed")
            _require(jobs.get("deploy", {}).get("conclusion") == "success", "Pages deploy job failed")
            evidence["stages"].append("pages_jobs_success")

            build_job_id = int(jobs["build"]["id"])
            build_log = _download(f"/actions/jobs/{build_job_id}/logs").decode(
                "utf-8", errors="replace"
            )
            digest_match = re.search(
                r"verified policy artifact (\d+) from run (\d+): "
                r"artifact sha256=([0-9a-f]{64}), site archive sha256=([0-9a-f]{64})",
                build_log,
            )
            _require(
                digest_match is not None,
                "Pages build log lacks the exact digest attestation line",
            )
            assert digest_match is not None
            logged_artifact_id = int(digest_match.group(1))
            logged_policy_run_id = int(digest_match.group(2))
            outer_digest = digest_match.group(3)
            inner_digest = digest_match.group(4)
            _require(logged_artifact_id == artifact_id, "artifact ID mismatch")
            _require(logged_policy_run_id == policy_run_id, "policy run ID mismatch")
            _require(
                artifact_digest == f"sha256:{outer_digest}",
                "outer artifact digest mismatch",
            )
            evidence["validated_site_artifact"].update(
                {
                    "verified_outer_digest": f"sha256:{outer_digest}",
                    "verified_inner_archive_digest": f"sha256:{inner_digest}",
                }
            )
            evidence["stages"].append("outer_and_inner_digests_verified")

            deployment_query = urllib.parse.urlencode(
                {
                    "sha": TARGET_SHA,
                    "environment": "github-pages",
                    "per_page": 100,
                }
            )
            deployments = _request_json(f"/deployments?{deployment_query}")
            _require(bool(deployments), f"no github-pages deployment for {TARGET_SHA}")
            successful_deployment: dict[str, Any] | None = None
            for deployment in deployments:
                statuses = _request_json(
                    f"/deployments/{int(deployment['id'])}/statuses?per_page=100"
                )
                successful_status = next(
                    (status for status in statuses if status.get("state") == "success"),
                    None,
                )
                if successful_status is not None:
                    successful_deployment = {
                        "id": int(deployment["id"]),
                        "state": successful_status["state"],
                        "environment_url": successful_status.get("environment_url"),
                        "created_at": successful_status.get("created_at"),
                    }
                    break
            _require(
                successful_deployment is not None,
                "no successful github-pages deployment status found",
            )
            evidence["deployment"] = successful_deployment
            evidence["stages"].append("github_pages_deployment_success")

            live_checks = [
                (
                    "https://grandchallenge.github.io/MATH-PROGRAMME/decisions/ADR-0014_EXACT_ARTIFACT_AND_REPOSITORY_EXECUTION/",
                    "Exact Artifact and Repository Execution",
                ),
                (
                    "https://grandchallenge.github.io/MATH-PROGRAMME/domains/navier_stokes/",
                    "NS-CI-WP06",
                ),
            ]
            live_results: list[dict[str, Any]] = []
            for url, marker in live_checks:
                status_code, html = _fetch_live(url)
                _require(status_code == 200, f"live page returned HTTP {status_code}: {url}")
                _require(marker in html, f"live page lacks marker {marker!r}: {url}")
                live_results.append(
                    {"url": url, "status": status_code, "marker": marker}
                )
            evidence["live_pages"] = live_results
            evidence["stages"].append("live_pages_verified")
            evidence["status"] = "PASS"
        except Exception as exc:  # evidence must survive every failure mode
            evidence["status"] = "FAIL"
            evidence["error_type"] = type(exc).__name__
            evidence["error"] = str(exc)

        EVIDENCE_PATH.write_text(
            "ATTESTATION_JSON=" + json.dumps(evidence, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        self.fail(
            "Disposable attestation completed; inspect the preserved "
            "campaign-replay-failure artifact for PASS/FAIL evidence."
        )


if __name__ == "__main__":
    unittest.main()
