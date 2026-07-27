"""Disposable end-to-end attestation for PR #97's merge publication chain.

This test is intentionally confined to an unmerged audit branch. It queries only
public GitHub and GitHub Pages endpoints and emits one machine-readable evidence
line for external inspection.
"""

from __future__ import annotations

import json
import re
import unittest
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any


REPOSITORY = "grandchallenge/MATH-PROGRAMME"
TARGET_SHA = "ebb73aa1b2c025e52b741cce9756cb0e268e17ef"
API_ROOT = f"https://api.github.com/repos/{REPOSITORY}"
USER_AGENT = "MATH-PROGRAMME-post-merge-pages-attestation"


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


class PostMergePagesAttestationTests(unittest.TestCase):
    def test_exact_policy_artifact_reached_live_pages(self) -> None:
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
        self.assertTrue(policy_runs, f"no main-push policy run for {TARGET_SHA}")
        policy_run = max(
            policy_runs,
            key=lambda run: run.get("run_started_at") or run.get("created_at") or "",
        )
        self.assertEqual(policy_run.get("event"), "push")
        self.assertEqual(policy_run.get("head_branch"), "main")
        self.assertEqual(policy_run.get("status"), "completed")
        self.assertEqual(policy_run.get("conclusion"), "success")
        policy_run_id = int(policy_run["id"])

        artifact_listing = _request_json(
            f"/actions/runs/{policy_run_id}/artifacts?per_page=100"
        )
        artifacts = [
            artifact
            for artifact in artifact_listing.get("artifacts", [])
            if artifact.get("name") == "validated-site"
            and not artifact.get("expired")
        ]
        self.assertEqual(
            len(artifacts),
            1,
            f"expected one live validated-site artifact, found {len(artifacts)}",
        )
        artifact = artifacts[0]
        artifact_id = int(artifact["id"])
        artifact_digest = str(artifact.get("digest", ""))
        self.assertRegex(artifact_digest, r"^sha256:[0-9a-f]{64}$")

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
        self.assertTrue(
            deployment_runs, f"no Pages workflow_run found for {TARGET_SHA}"
        )
        deployment_run = max(
            deployment_runs,
            key=lambda run: run.get("run_started_at") or run.get("created_at") or "",
        )
        self.assertEqual(deployment_run.get("event"), "workflow_run")
        self.assertEqual(deployment_run.get("status"), "completed")
        self.assertEqual(deployment_run.get("conclusion"), "success")
        deployment_run_id = int(deployment_run["id"])

        jobs_listing = _request_json(
            f"/actions/runs/{deployment_run_id}/jobs?per_page=100"
        )
        jobs = {job["name"]: job for job in jobs_listing.get("jobs", [])}
        self.assertEqual(jobs.get("build", {}).get("conclusion"), "success")
        self.assertEqual(jobs.get("deploy", {}).get("conclusion"), "success")

        build_job_id = int(jobs["build"]["id"])
        build_log = _download(f"/actions/jobs/{build_job_id}/logs").decode(
            "utf-8", errors="replace"
        )
        digest_match = re.search(
            r"verified policy artifact (\d+) from run (\d+): "
            r"artifact sha256=([0-9a-f]{64}), site archive sha256=([0-9a-f]{64})",
            build_log,
        )
        self.assertIsNotNone(
            digest_match, "Pages build log lacks the exact digest attestation"
        )
        assert digest_match is not None
        logged_artifact_id = int(digest_match.group(1))
        logged_policy_run_id = int(digest_match.group(2))
        outer_digest = digest_match.group(3)
        inner_digest = digest_match.group(4)
        self.assertEqual(logged_artifact_id, artifact_id)
        self.assertEqual(logged_policy_run_id, policy_run_id)
        self.assertEqual(artifact_digest, f"sha256:{outer_digest}")

        deployment_query = urllib.parse.urlencode(
            {
                "sha": TARGET_SHA,
                "environment": "github-pages",
                "per_page": 100,
            }
        )
        deployments = _request_json(f"/deployments?{deployment_query}")
        self.assertTrue(deployments, f"no github-pages deployment for {TARGET_SHA}")
        deployment_id: int | None = None
        deployment_status_url: str | None = None
        for deployment in deployments:
            statuses = _request_json(
                f"/deployments/{int(deployment['id'])}/statuses?per_page=100"
            )
            successful = next(
                (status for status in statuses if status.get("state") == "success"),
                None,
            )
            if successful is not None:
                deployment_id = int(deployment["id"])
                deployment_status_url = successful.get("environment_url")
                break
        self.assertIsNotNone(
            deployment_id, "no successful github-pages deployment status found"
        )

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
            self.assertEqual(status_code, 200, url)
            self.assertIn(marker, html, url)
            live_results.append(
                {"url": url, "status": status_code, "marker": marker}
            )

        evidence = {
            "attested_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "target_sha": TARGET_SHA,
            "policy_run": {
                "id": policy_run_id,
                "number": policy_run["run_number"],
                "url": policy_run["html_url"],
                "conclusion": policy_run["conclusion"],
            },
            "validated_site_artifact": {
                "id": artifact_id,
                "metadata_digest": artifact_digest,
                "verified_outer_digest": f"sha256:{outer_digest}",
                "verified_inner_archive_digest": f"sha256:{inner_digest}",
            },
            "pages_workflow_run": {
                "id": deployment_run_id,
                "number": deployment_run["run_number"],
                "url": deployment_run["html_url"],
                "conclusion": deployment_run["conclusion"],
                "build_job": "success",
                "deploy_job": "success",
            },
            "deployment": {
                "id": deployment_id,
                "state": "success",
                "environment_url": deployment_status_url,
            },
            "live_pages": live_results,
        }
        print("ATTESTATION_JSON=" + json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
