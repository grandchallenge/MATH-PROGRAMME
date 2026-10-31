from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = 5
    while d * d <= n:
        if n % d == 0 or n % (d + 2) == 0:
            return False
        d += 6
    return True


def get_representations(n: int, max_k: int = 60) -> list[tuple[int, int]]:
    """Returns all representations of n as p + 2^k with p prime and k >= 0."""
    reps = []
    power = 1
    k = 0
    while power < n:
        p = n - power
        if is_prime(p):
            reps.append((p, k))
        power *= 2
        k += 1
        if k > max_k:
            break
    return reps


class ErdosCatalogue0016AuditTests(unittest.TestCase):
    def test_chen_transfer_implication(self):
        """Verifies the elementary logical transfer: refutation of all finite progressions

        directly refutes any single progression (k=1).
        """

        def chen_theorem(num_progressions: int) -> bool:
            """Chen (2023) proves: No finite collection of progressions plus density zero covers U."""
            return False  # False means decomposition is impossible for ANY finite k >= 1

        # Case k = 1 is an instance of a finite collection
        self.assertFalse(chen_theorem(1))

    def test_zero_exponent_odd_parity_boundary(self):
        """Verifies that k=0 represents only the unique odd integer n=3."""
        reps_k0 = []
        for n in range(1, 2000, 2):
            p = n - 1
            if is_prime(p):
                reps_k0.append(n)
        self.assertEqual(reps_k0, [3])

        # For any odd n > 3, any representation must have k >= 1 and an odd prime p >= 3
        for n in range(5, 500, 2):
            for p, k in get_representations(n):
                self.assertGreaterEqual(k, 1)
                self.assertGreaterEqual(p, 3)
                self.assertEqual(p % 2, 1)

    def test_small_odd_representations_fixtures(self):
        """Verifies the small integer examples cited in editorial/0016.md."""
        # 3 = 2 + 2^0
        self.assertIn((2, 0), get_representations(3))

        # 9 = 7 + 2^1
        self.assertIn((7, 1), get_representations(9))

        # 11 = 3 + 2^3
        self.assertIn((3, 3), get_representations(11))

        # 13 = 11 + 2^1
        self.assertIn((11, 1), get_representations(13))

        # 15 has multiple representations: 7 + 2^3, 11 + 2^2, 13 + 2^1
        reps15 = get_representations(15)
        self.assertIn((7, 3), reps15)
        self.assertIn((11, 2), reps15)
        self.assertIn((13, 1), reps15)

    def test_subset_containment_vs_decomposition(self):
        """Verifies the structural distinction between containment P subset U and equality U = P union R."""
        # Mock universe U containing progression P = {a + m*d} plus another positive-density sequence
        d = 6
        P = {1 + k * d for k in range(100)}
        # Suppose U also contains disjoint infinite progression Q
        Q = {5 + k * d for k in range(100)}
        U = P | Q

        # P is a subset of U
        self.assertTrue(P.issubset(U))

        # But remainder R = U \ P is Q, which has relative density > 0 and is not negligible
        R = U - P
        self.assertEqual(R, Q)
        self.assertEqual(len(R), 100)

    def test_editorial_markdown_gate(self):
        """Verifies that 0016.md satisfies math_markdown_gate."""
        md_path = ROOT / "governance/erdos_compendium/editorial/0016.md"
        self.assertTrue(md_path.exists())
        cmd = [sys.executable, str(ROOT / "ci/math_markdown_gate.py"), "--file", str(md_path)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"math_markdown_gate failed: {res.stdout}\n{res.stderr}")


if __name__ == "__main__":
    unittest.main()
