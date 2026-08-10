#!/usr/bin/env python3
"""Regression and mutation tests for the Programme-policy execution envelope."""
from __future__ import annotations

import copy
import unittest
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
REPLAY_JOB = "governed-campaign-replay"
VALIDATE_JOB = "validate-json"
REPLAY_COMMANDS = (
    "python3 ci/validate_campaign_replays.py",
    "python3 ci/test_campaign_replays.py",
)


def load_workflow() -> dict[str, Any]:
    data = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    if not isinstance(data, dict):
        raise AssertionError("Programme policy workflow must parse as a mapping")
    return data


def job_run_text(job: dict[str, Any]) -> str:
    return "\n".join(str(step.get("run", "")) for step in job.get("steps", []))


def envelope_errors(workflow: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    jobs = workflow.get("jobs", {})
    replay = jobs.get(REPLAY_JOB)
    validate = jobs.get(VALIDATE_JOB)

    if not isinstance(replay, dict):
        return ["missing governed-campaign-replay job"]
    if not isinstance(validate, dict):
        return ["missing validate-json job"]

    if str(replay.get("runs-on", "")) != "ubuntu-24.04":
        errors.append("replay job runner must remain pinned to ubuntu-24.04")
    if str(replay.get("if", "")) != "github.event_name != 'schedule'":
        errors.append("replay job event boundary drift")

    try:
        timeout = int(str(replay.get("timeout-minutes", "0")))
    except ValueError:
        timeout = 0
    if not 30 <= timeout <= 60:
        errors.append("replay job timeout must remain bounded between 30 and 60 minutes")

    needs = validate.get("needs")
    if isinstance(needs, list):
        dependency_present = REPLAY_JOB in needs
    else:
        dependency_present = str(needs or "") == REPLAY_JOB
    if not dependency_present:
        errors.append("validate-json must depend on governed-campaign-replay")

    replay_runs = job_run_text(replay)
    validate_runs = job_run_text(validate)
    for command in REPLAY_COMMANDS:
        if command not in replay_runs:
            errors.append(f"replay job missing {command}")
        if command in validate_runs:
            errors.append(f"validate-json must not duplicate long replay command {command}")

    setup_python = [
        step
        for step in replay.get("steps", [])
        if str(step.get("uses", "")).startswith("actions/setup-python@")
    ]
    if len(setup_python) != 1 or str(setup_python[0].get("with", {}).get("python-version", "")) != "3.12":
        errors.append("replay job must use exactly one governed Python 3.12 setup")

    if "python -m pip install --requirement requirements/policy.txt" not in replay_runs:
        errors.append("replay job must install governed policy dependencies")

    artifacts = [
        step
        for step in replay.get("steps", [])
        if str(step.get("uses", "")).startswith("actions/upload-artifact@")
        and str(step.get("with", {}).get("name", "")) == "campaign-replay-failure"
    ]
    if len(artifacts) != 1:
        errors.append("replay job must preserve exactly one campaign-replay-failure artifact")
    else:
        condition = str(artifacts[0].get("if", ""))
        if "failure()" not in condition:
            errors.append("campaign replay failure artifact must remain fail-closed")
        if "campaign-replays.log" not in str(artifacts[0].get("with", {}).get("path", "")):
            errors.append("campaign replay failure artifact must retain campaign-replays.log")

    return errors


class ProgrammePolicyExecutionEnvelopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = load_workflow()

    def test_current_workflow_satisfies_envelope(self) -> None:
        self.assertEqual(envelope_errors(self.workflow), [])

    def test_missing_replay_job_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.workflow)
        mutated["jobs"].pop(REPLAY_JOB, None)
        self.assertTrue(envelope_errors(mutated))

    def test_missing_required_dependency_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.workflow)
        mutated["jobs"][VALIDATE_JOB].pop("needs", None)
        self.assertTrue(any("depend" in error for error in envelope_errors(mutated)))

    def test_old_twenty_minute_ceiling_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.workflow)
        mutated["jobs"][REPLAY_JOB]["timeout-minutes"] = "20"
        self.assertTrue(any("timeout" in error for error in envelope_errors(mutated)))

    def test_missing_replay_command_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.workflow)
        for step in mutated["jobs"][REPLAY_JOB]["steps"]:
            run = str(step.get("run", ""))
            if REPLAY_COMMANDS[1] in run:
                step["run"] = run.replace(REPLAY_COMMANDS[1], "echo replay-test-omitted")
                break
        self.assertTrue(any(REPLAY_COMMANDS[1] in error for error in envelope_errors(mutated)))

    def test_failure_artifact_removal_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.workflow)
        mutated["jobs"][REPLAY_JOB]["steps"] = [
            step
            for step in mutated["jobs"][REPLAY_JOB]["steps"]
            if str(step.get("with", {}).get("name", "")) != "campaign-replay-failure"
        ]
        self.assertTrue(any("failure artifact" in error for error in envelope_errors(mutated)))

    def test_long_replay_reintroduced_into_validate_json_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.workflow)
        mutated["jobs"][VALIDATE_JOB]["steps"].append({"run": REPLAY_COMMANDS[0]})
        self.assertTrue(any("must not duplicate" in error for error in envelope_errors(mutated)))


if __name__ == "__main__":
    unittest.main()
