from pathlib import Path
import math
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


def get_representations_erdos(n: int, max_exp: int = 20) -> list[tuple[int, int, int]]:
    """Returns all representations of n as p + 2^k + 2^l with p prime, 0 <= k <= l."""
    reps = []
    for k in range(max_exp):
        if 2**k >= n:
            break
        for l in range(k, max_exp):
            sum_powers = 2**k + 2**l
            if sum_powers >= n:
                break
            p = n - sum_powers
            if is_prime(p):
                reps.append((p, k, l))
    return reps


def get_representations_crocker(n: int, max_exp: int = 20) -> list[tuple[int, int, int]]:
    """Returns representations under Crocker's strict positive condition: 1 <= k <= l."""
    reps = []
    for k in range(1, max_exp):
        if 2**k >= n:
            break
        for l in range(k, max_exp):
            sum_powers = 2**k + 2**l
            if sum_powers >= n:
                break
            p = n - sum_powers
            if is_prime(p):
                reps.append((p, k, l))
    return reps


class ErdosCatalogue0009AuditTests(unittest.TestCase):
    def test_parity_decomposition_cases(self):
        """Verifies that every representation of an odd n partitions into three disjoint parity branches:

        1. k = l = 0 -> p = n - 2 (odd prime)
        2. k >= 1 and l >= 1 -> p is an odd prime >= 3
        3. Exactly one exponent is 0 -> p = 2 and n = 3 + 2^j (j >= 1).
        """
        for n in range(5, 1000, 2):
            reps = get_representations_erdos(n)
            for p, k, l in reps:
                if k == 0 and l == 0:
                    self.assertEqual(p, n - 2)
                    self.assertEqual(p % 2, 1)
                    self.assertTrue(is_prime(p))
                elif k >= 1 and l >= 1:
                    self.assertEqual(p % 2, 1)
                    self.assertGreaterEqual(p, 3)
                    self.assertTrue(is_prime(p))
                else:
                    # Exactly one exponent is 0
                    self.assertEqual(min(k, l), 0)
                    self.assertGreater(max(k, l), 0)
                    self.assertEqual(p, 2)
                    j = max(k, l)
                    self.assertEqual(n, 3 + 2**j)

    def test_crocker_vs_erdos_zero_exponent_divergence(self):
        """Verifies that n=5 is representable under Erdős (k, l >= 0) but exceptional under Crocker (k, l >= 1),

        and that 1 and 3 are exceptional under both definitions.
        """
        # Under Erdős 9:
        self.assertEqual(get_representations_erdos(1), [])
        self.assertEqual(get_representations_erdos(3), [])
        reps_erdos_5 = get_representations_erdos(5)
        self.assertIn((3, 0, 0), reps_erdos_5)

        # Under Crocker (1971):
        self.assertEqual(get_representations_crocker(1), [])
        self.assertEqual(get_representations_crocker(3), [])
        self.assertEqual(get_representations_crocker(5), [])

    def test_small_odd_representations_fixtures(self):
        """Verifies the small integer representations cited in editorial/0009.md."""
        # 5 = 3 + 2^0 + 2^0
        self.assertIn((3, 0, 0), get_representations_erdos(5))

        # 11 = 2 + 2^0 + 2^3
        self.assertIn((2, 0, 3), get_representations_erdos(11))

        # 17 = 13 + 2^1 + 2^1
        self.assertIn((13, 1, 1), get_representations_erdos(17))

    def test_pan_lower_bound_sublinear_density_zero(self):
        """Verifies that Pan (2011) lower bound X * exp(-C log X log4 X / log3 X) divided by X

        tends to zero, and therefore does not establish positive upper density.
        """
        # For sufficiently large X, ratio = exp(-C log X * log4 X / log3 X)
        # As X -> infty, log X * log4 X / log3 X -> infty, so ratio -> 0.
        def bound_ratio(x: float, c: float = 1.0) -> float:
            log1 = math.log(x)
            log2 = math.log(log1)
            log3 = math.log(log2)
            log4 = math.log(log3)
            exponent = -c * (log1 * log4) / log3
            return math.exp(exponent)

        # Compute for large X values
        x1 = 1e15
        x2 = 1e30
        x3 = 1e60
        r1 = bound_ratio(x1)
        r2 = bound_ratio(x2)
        r3 = bound_ratio(x3)

        self.assertGreater(r1, r2)
        self.assertGreater(r2, r3)
        self.assertLess(r3, 1e-10)

    def test_math_markdown_gate_on_editorial_0009(self):
        """Verifies that governance/erdos_compendium/editorial/0009.md passes the math markdown gate."""
        doc_path = ROOT / "governance" / "erdos_compendium" / "editorial" / "0009.md"
        self.assertTrue(doc_path.exists(), f"Missing file: {doc_path}")

        gate_script = ROOT / "ci" / "math_markdown_gate.py"
        result = subprocess.run(
            [sys.executable, str(gate_script), "--file", str(doc_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"math_markdown_gate failed on {doc_path}:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}",
        )
        self.assertIn("mathematical Markdown source gate: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
