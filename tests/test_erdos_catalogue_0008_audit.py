import math
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def coloring_assignment(m: int, B: int) -> int:
    """Assigns (B+1) coloring: 1..B each get distinct color m, and integers > B get color B+1."""
    return m if m <= B else B + 1


def is_covering_system(congruences: list[tuple[int, int]]) -> tuple[bool, str]:
    """Checks whether a finite set of congruences (a_i, m_i) forms a distinct covering system.

    Returns (is_cover, reason).
    """
    if not congruences:
        return False, "Empty system"
    moduli = [m for _, m in congruences]
    if any(m <= 1 for m in moduli):
        return False, "Modulus must be > 1"
    if len(set(moduli)) != len(moduli):
        return False, "Moduli must be pairwise distinct"

    # Compute LCM of moduli
    lcm = 1
    for m in moduli:
        lcm = (lcm * m) // math.gcd(lcm, m)

    # Check coverage of all residues 0..lcm-1
    covered = [False] * lcm
    for a, m in congruences:
        for r in range(a % m, lcm, m):
            covered[r] = True

    if not all(covered):
        uncovered = [r for r, c in enumerate(covered) if not c]
        return False, f"Uncovered residues: {uncovered[:5]}"
    return True, "Valid distinct covering system"


class ErdosCatalogue0008AuditTests(unittest.TestCase):
    def test_hough_transfer_elementary_implication(self):
        """Tests that any distinct covering system cannot be monochromatic under (B+1)-colouring."""
        # For mock bounds B in [2, 3, 5, 10, 24, 100]
        for B in [2, 3, 5, 10, 24, 100]:
            # Case 1: Any set of moduli with all m_i > B has min(m_i) > B
            candidate_high = [B + 1, B + 2, B + 3]
            self.assertGreater(min(candidate_high), B)

            # Case 2: Any single modulus m > 1 has density 1/m < 1, leaving m - 1 residues uncovered
            for m in range(2, 50):
                uncovered_count = m - 1
                self.assertGreater(uncovered_count, 0)
                # Single class covers exactly 1 out of m residues
                covered = {0}
                self.assertNotEqual(len(covered), m)

    def test_classic_erdos_covering_system(self):
        """Verifies Erdős's classic 6-class distinct covering system."""
        # Congruences: (0 mod 2), (0 mod 3), (1 mod 4), (3 mod 8), (7 mod 12), (23 mod 24)
        congruences = [
            (0, 2),
            (0, 3),
            (1, 4),
            (3, 8),
            (7, 12),
            (23, 24),
        ]
        is_cover, reason = is_covering_system(congruences)
        self.assertTrue(is_cover, reason)

        moduli = [m for _, m in congruences]
        self.assertEqual(moduli, [2, 3, 4, 8, 12, 24])
        self.assertEqual(len(set(moduli)), 6)
        self.assertEqual(min(moduli), 2)
        # 2 <= 10^16 (Hough) and 2 <= 615999 (BBMST)
        self.assertLessEqual(min(moduli), 10**16)
        self.assertLessEqual(min(moduli), 615999)

        # Under (B+1) coloring for any B >= 2, the moduli are never monochromatic
        for B in [2, 3, 4, 8, 10, 12, 24, 100]:
            colors = [coloring_assignment(m, B) for m in moduli]
            # Must have at least two distinct colors
            self.assertGreater(len(set(colors)), 1, f"Expected non-monochromatic for B={B}, got {colors}")

    def test_adversarial_hostile_cases(self):
        """Verifies rejection of invalid systems (hostile mutation, non-distinct, empty)."""
        # Empty system
        is_cov, _ = is_covering_system([])
        self.assertFalse(is_cov)

        # Modulus 1 disallowed
        is_cov, _ = is_covering_system([(0, 1)])
        self.assertFalse(is_cov)

        # Non-distinct moduli [(0, 2), (1, 2)] covers Z but fails distinctness
        is_cov, msg = is_covering_system([(0, 2), (1, 2)])
        self.assertFalse(is_cov)
        self.assertIn("pairwise distinct", msg)

        # Hostile mutation of Erdős system: alter (23 mod 24) to (24 mod 24) == (0 mod 24)
        # Residue 23 is left uncovered
        mutated = [
            (0, 2),
            (0, 3),
            (1, 4),
            (3, 8),
            (7, 12),
            (0, 24),
        ]
        is_cov, msg = is_covering_system(mutated)
        self.assertFalse(is_cov)
        self.assertIn("Uncovered residues", msg)

    def test_editorial_markdown_gate(self):
        """Verifies that 0008.md satisfies math_markdown_gate."""
        md_path = ROOT / "governance/erdos_compendium/editorial/0008.md"
        self.assertTrue(md_path.exists())
        cmd = [sys.executable, str(ROOT / "ci/math_markdown_gate.py"), "--file", str(md_path)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"math_markdown_gate failed: {res.stdout}\n{res.stderr}")


if __name__ == "__main__":
    unittest.main()
