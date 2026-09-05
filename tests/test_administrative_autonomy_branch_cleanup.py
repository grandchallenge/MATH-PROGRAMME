from pathlib import Path
import sys
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ci"))
from autonomy_github import AutonomyError, delete_branch


class BranchCleanupTests(unittest.TestCase):
    repo = "grandchallenge/MATH-PROGRAMME"
    branch = "automation/maintenance/receipt-example"
    encoded = "automation%2Fmaintenance%2Freceipt-example"

    def missing(self):
        client = Mock()
        client.delete.side_effect = AutonomyError(
            f'DELETE /repos/{self.repo}/git/refs/heads/{self.encoded} '
            'failed: 422 {"message":"Reference does not exist"}'
        )
        return client

    def test_success_does_not_need_absence_recovery(self):
        client = Mock()
        delete_branch(client, self.repo, self.branch)
        client.get.assert_not_called()

    def test_auto_deleted_branch_requires_exact_absence_readback(self):
        client = self.missing()
        client.get.side_effect = AutonomyError("GET ref failed: 404 Not Found")
        delete_branch(client, self.repo, self.branch)
        client.get.assert_called_once_with(
            f"/repos/{self.repo}/git/ref/heads/{self.encoded}"
        )

    def test_recreated_branch_fails_closed(self):
        client = self.missing()
        client.get.return_value = {"object": {"sha": "a" * 40}}
        with self.assertRaisesRegex(AutonomyError, "absence readback failed"):
            delete_branch(client, self.repo, self.branch)

    def test_other_422_and_malformed_errors_remain_errors(self):
        for body in ('{"message":"Cannot delete protected branch"}', 'not-json', '[]', 'null'):
            with self.subTest(body=body):
                client = self.missing()
                client.delete.side_effect = AutonomyError(
                    f"DELETE /repos/{self.repo}/git/refs/heads/{self.encoded} failed: 422 {body}"
                )
                with self.assertRaises(AutonomyError):
                    delete_branch(client, self.repo, self.branch)
                client.get.assert_not_called()

    def test_absence_readback_auth_or_server_error_is_not_success(self):
        for status in (403, 429, 500):
            with self.subTest(status=status):
                client = self.missing()
                client.get.side_effect = AutonomyError(f"GET ref failed: {status} error")
                with self.assertRaises(AutonomyError):
                    delete_branch(client, self.repo, self.branch)

    def test_existing_404_cleanup_contract_is_preserved(self):
        client = Mock()
        client.delete.side_effect = AutonomyError("DELETE ref failed: 404 Not Found")
        delete_branch(client, self.repo, self.branch)
        client.get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
