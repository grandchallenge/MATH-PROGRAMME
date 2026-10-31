from itertools import combinations
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def is_forbidden_triple_free(A: set[int] | list[int]) -> tuple[bool, str]:
    """Checks whether A satisfies: for all a < min(b, c) in A, a does not divide b + c.

    Note that repetitions b = c are permitted in the quantifier.
    """
    sorted_A = sorted(A)
    n = len(sorted_A)
    for i in range(n):
        a = sorted_A[i]
        for j in range(i + 1, n):
            b = sorted_A[j]
            for k in range(j, n):
                c = sorted_A[k]
                if (b + c) % a == 0:
                    return False, f"Violation: {a} divides {b} + {c} = {b + c}"
    return True, "Forbidden-triple-free"


def tail_construction(N: int) -> set[int]:
    """Returns the tail construction {floor(2N/3) + 1, ..., N}."""
    return set(range(2 * N // 3 + 1, N + 1))


class ErdosCatalogue0013AuditTests(unittest.TestCase):
    def test_tail_construction_admissibility(self):
        """Verifies that the tail construction is forbidden-triple-free for all N in [1, 50]."""
        for N in range(1, 51):
            A = tail_construction(N)
            is_free, msg = is_forbidden_triple_free(A)
            self.assertTrue(is_free, f"N={N} failed: {msg}")

            # Verify size matches ceil(N / 3) = N - floor(2N / 3)
            expected_size = N - (2 * N // 3)
            self.assertEqual(len(A), expected_size)

            # Analytic check: for every a < min(b, c) in A:
            # 2a < b + c <= 2N < 3a since a > 2N/3
            sorted_A = sorted(A)
            for i in range(len(sorted_A)):
                a = sorted_A[i]
                self.assertGreater(a, 2 * N / 3)
                self.assertGreater(3 * a, 2 * N)
                for j in range(i + 1, len(sorted_A)):
                    b = sorted_A[j]
                    for k in range(j, len(sorted_A)):
                        c = sorted_A[k]
                        self.assertGreater(b + c, 2 * a)
                        self.assertLessEqual(b + c, 2 * N)
                        self.assertLess(b + c, 3 * a)

    def test_concrete_n9_fixture(self):
        """Verifies the concrete fixture N=9, A={7, 8, 9} from editorial/0013.md."""
        A = {7, 8, 9}
        self.assertEqual(A, tail_construction(9))
        is_free, msg = is_forbidden_triple_free(A)
        self.assertTrue(is_free, msg)
        self.assertEqual(len(A), 3)

        # Divisibility checks for a=7:
        # b=c=8 -> 16 % 7 == 2 != 0
        # b=8, c=9 -> 17 % 7 == 3 != 0
        # b=c=9 -> 18 % 7 == 4 != 0
        self.assertNotEqual(16 % 7, 0)
        self.assertNotEqual(17 % 7, 0)
        self.assertNotEqual(18 % 7, 0)

    def test_exhaustive_maximality_small_n(self):
        """Verifies that for N in [1, 10], tail construction attains the exact maximum size."""
        for N in range(1, 11):
            tail_size = len(tail_construction(N))
            # Find maximum size by searching combinations from N down
            max_size = 0
            for k in range(N, 0, -1):
                found = False
                for comb in combinations(range(1, N + 1), k):
                    if is_forbidden_triple_free(comb)[0]:
                        max_size = k
                        found = True
                        break
                if found:
                    break
            self.assertEqual(tail_size, max_size, f"Tail not maximal at N={N}")
            # Bedert's bound: max_size <= floor(N/3) + 1
            self.assertLessEqual(max_size, N // 3 + 1)

    def test_adversarial_hostile_violations(self):
        """Verifies rejection of violating sets."""
        # Case 1: Repeated summand violation: A = {2, 3}. a=2, b=c=3 -> 2 divides 6
        is_free, msg = is_forbidden_triple_free({2, 3})
        self.assertFalse(is_free)
        self.assertIn("2 divides 3 + 3 = 6", msg)

        # Case 2: Small element added to N=9 tail: A = {1, 7, 8, 9}. 1 divides 7+7=14
        is_free, msg = is_forbidden_triple_free({1, 7, 8, 9})
        self.assertFalse(is_free)
        self.assertIn("1 divides", msg)

        # Case 3: A = {2, 7, 8, 9}. 2 divides 7+7=14
        is_free, msg = is_forbidden_triple_free({2, 7, 8, 9})
        self.assertFalse(is_free)
        self.assertIn("2 divides 7 + 7 = 14", msg)

        # Case 4: A = {4, 7, 8, 9}. 4 divides 7+9=16
        is_free, msg = is_forbidden_triple_free({4, 7, 8, 9})
        self.assertFalse(is_free)
        self.assertIn("4 divides 7 + 9 = 16", msg)

    def test_editorial_markdown_gate(self):
        """Verifies that 0013.md satisfies math_markdown_gate."""
        md_path = ROOT / "governance/erdos_compendium/editorial/0013.md"
        self.assertTrue(md_path.exists())
        cmd = [sys.executable, str(ROOT / "ci/math_markdown_gate.py"), "--file", str(md_path)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"math_markdown_gate failed: {res.stdout}\n{res.stderr}")


if __name__ == "__main__":
    unittest.main()
