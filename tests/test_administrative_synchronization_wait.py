from __future__ import annotations

import sys
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import synchronize_administrative_completion_v3 as synchronization


class FakeClient:
    def __init__(self, runs: list[dict]) -> None:
        self.runs = runs

    def get(self, path: str) -> dict:
        self.path = path
        return {"workflow_runs": self.runs}


class AdministrativeSynchronizationWaitTests(unittest.TestCase):
    def test_single_success_is_not_full_gate(self) -> None:
        client = FakeClient([
            {"id": 1, "name": "Programme policy checks", "status": "completed", "conclusion": "success"},
            {"id": 2, "name": "GCL conformance", "status": "in_progress", "conclusion": None},
        ])
        observed = synchronization.successful_workflows(client, "grandchallenge/MATH-PROGRAMME", "a" * 40)
        self.assertEqual(observed, {"Programme policy checks": 1})
        self.assertEqual(synchronization.REQUIRED - set(observed), {"GCL conformance"})

    def test_both_successes_open_synchronization_gate(self) -> None:
        client = FakeClient([
            {"id": 1, "name": "Programme policy checks", "status": "completed", "conclusion": "success"},
            {"id": 2, "name": "GCL conformance", "status": "completed", "conclusion": "success"},
        ])
        observed = synchronization.successful_workflows(client, "grandchallenge/MATH-PROGRAMME", "a" * 40)
        self.assertEqual(set(observed), synchronization.REQUIRED)


    def test_successful_sync_reuses_one_immutable_workflow_read(self) -> None:
        calls=[]
        class OneReadClient:
            def __init__(self,*args):pass
            def get(self,path):
                calls.append(path)
                if len(calls)>1:
                    raise AssertionError("duplicate Actions workflow read")
                return {"workflow_runs":[
                    {"id":17,"name":"Programme policy checks","status":"completed","conclusion":"success"},
                    {"id":18,"name":"GCL conformance","status":"completed","conclusion":"success"},
                ]}
        original = synchronization.implementation.verify_required_workflows
        def fake_implementation_main(args):
            client=OneReadClient()
            verified=synchronization.implementation.verify_required_workflows(
                client,"grandchallenge/MATH-PROGRAMME","a"*40)
            self.assertEqual(verified, {"Programme policy checks":17,"GCL conformance":18})
            with self.assertRaisesRegex(synchronization.automation.AutomationError, "identity changed"):
                synchronization.implementation.verify_required_workflows(
                    client,"grandchallenge/MATH-PROGRAMME","b"*40)
            return 0
        with mock.patch.dict('os.environ',{'GITHUB_REPOSITORY':'grandchallenge/MATH-PROGRAMME',
                                         'WORKFLOW_RUN_HEAD_SHA':'a'*40, 'GITHUB_TOKEN':'test'}):
            with mock.patch.object(synchronization.implementation,'GitHubClient',OneReadClient), \
                 mock.patch.object(synchronization.implementation,'main',fake_implementation_main):
                self.assertEqual(synchronization.main(['--apply']),0)
        self.assertEqual(len(calls),1)
        self.assertIs(synchronization.implementation.verify_required_workflows,original)

    def test_incomplete_sync_never_calls_mutating_base(self) -> None:
        class IncompleteClient:
            def __init__(self,*args):pass
            def get(self,path):return {"workflow_runs":[
                {"id":17,"name":"Programme policy checks","status":"completed","conclusion":"success"}]}
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            report=Path(temp)/'wait.json'
            with mock.patch.dict('os.environ',{'GITHUB_REPOSITORY':'grandchallenge/MATH-PROGRAMME',
                                             'WORKFLOW_RUN_HEAD_SHA':'c'*40,'GITHUB_TOKEN':'test'}), \
                 mock.patch.object(synchronization.implementation,'GitHubClient',IncompleteClient), \
                 mock.patch.object(synchronization.implementation,'main',side_effect=AssertionError('must not mutate')):
                self.assertEqual(synchronization.main(['--apply','--report',str(report)]),0)
            import json
            result=json.loads(report.read_text())
            self.assertEqual(result['state'],'SYNCHRONIZATION_WAITING_FOR_REQUIRED_WORKFLOWS')
            self.assertFalse(result['authority_boundary']['merge_created'])

if __name__ == "__main__":
    unittest.main()
