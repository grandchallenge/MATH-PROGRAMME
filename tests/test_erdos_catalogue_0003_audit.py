import unittest
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def count_aps(N, k):
    count = 0
    for a in range(1, N + 1):
        for d in range(1, N):
            if a + (k - 1) * d <= N:
                count += 1
    return count

def solve_max_independent_set(N, k):
    aps = []
    for a in range(1, N + 1):
        for d in range(1, N):
            if a + (k - 1) * d <= N:
                mask = 0
                for m in range(k):
                    mask |= (1 << (a + m * d - 1))
                aps.append(mask)

    max_size = [0]
    maximizers = []

    def search(idx, current_mask, current_size):
        remaining = N - idx
        if current_size + remaining < max_size[0]:
            return
        if idx == N:
            if current_size > max_size[0]:
                max_size[0] = current_size
                maximizers.clear()
                maximizers.append(current_mask)
            elif current_size == max_size[0]:
                maximizers.append(current_mask)
            return

        bit = 1 << idx
        new_mask = current_mask | bit
        valid = True
        for ap in aps:
            if (ap & bit) and ((new_mask & ap) == ap):
                valid = False
                break
        if valid:
            search(idx + 1, new_mask, current_size + 1)

        search(idx + 1, current_mask, current_size)

    search(0, 0, 0)
    return max_size[0], len(maximizers)

class ErdosCatalogue0003AuditTests(unittest.TestCase):
    def test_possible_ap_counts(self):
        self.assertEqual(count_aps(8, 3), 12)
        self.assertEqual(count_aps(8, 4), 7)
        self.assertEqual(count_aps(16, 3), 56)
        self.assertEqual(count_aps(16, 4), 35)

    def test_r_bounds_and_maximizers(self):
        r3_8, count3_8 = solve_max_independent_set(8, 3)
        self.assertEqual(r3_8, 4)
        self.assertEqual(count3_8, 25)

        r4_8, count4_8 = solve_max_independent_set(8, 4)
        self.assertEqual(r4_8, 6)
        self.assertEqual(count4_8, 4)

        r3_16, count3_16 = solve_max_independent_set(16, 3)
        self.assertEqual(r3_16, 8)
        self.assertEqual(count3_16, 14)

        r4_16, count4_16 = solve_max_independent_set(16, 4)
        self.assertEqual(r4_16, 10)
        self.assertEqual(count4_16, 45)

    def test_r4_16_witness_and_hostile_mutation(self):
        witness = {1, 2, 4, 5, 7, 8, 9, 12, 14, 15}
        self.assertEqual(len(witness), 10)

        def has_k_ap(s, k):
            s_set = set(s)
            s_sorted = sorted(s)
            n = len(s_sorted)
            for i in range(n):
                a = s_sorted[i]
                for j in range(i + 1, n):
                    d = s_sorted[j] - a
                    if all((a + m * d) in s_set for m in range(k)):
                        return True
            return False

        self.assertFalse(has_k_ap(witness, 4))
        self.assertTrue(has_k_ap(witness, 3))

        # Adding 3 creates a 4-term progression 1, 2, 3, 4
        self.assertTrue(has_k_ap(witness | {3}, 4))

    def test_editorial_markdown_gate(self):
        md_path = ROOT / "governance/erdos_compendium/editorial/0003.md"
        self.assertTrue(md_path.exists())
        cmd = [sys.executable, str(ROOT / "ci/math_markdown_gate.py"), "--file", str(md_path)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"math_markdown_gate failed: {res.stdout}\n{res.stderr}")

if __name__ == "__main__":
    unittest.main()
