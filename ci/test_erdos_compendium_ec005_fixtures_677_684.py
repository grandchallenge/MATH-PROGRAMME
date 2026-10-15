"""Exact bounded regression fixtures for EC-BULK-005 Erdős #677-684.
Not proofs of asymptotic conjectures, full source fidelity or editorial admission.
"""
import math
import itertools
import unittest


def lcm_interval(n, k):
    v = 1
    for i in range(1, k + 1):
        v = math.lcm(v, n + i)
    return v


def factors(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def prime(n):
    return n >= 2 and not any(n % i == 0 for i in range(2, math.isqrt(n) + 1))


def smallest_factor(n):
    fs = factors(n)
    return min(fs) if fs else 1


def small_part(n,k):
    return math.prod(p**e for p,e in factors(math.comb(n,k)).items() if p <= k)


class EC005Fixtures(unittest.TestCase):
    def test_677_equal_lcm_varying_length_only(self):
        self.assertEqual(lcm_interval(4,3), 210)
        self.assertEqual(lcm_interval(13,2), 210)
        self.assertEqual(lcm_interval(3,4), 420)
        self.assertEqual(lcm_interval(19,2), 420)
        self.assertGreater(lcm_interval(6,7), lcm_interval(8,7))
        # This is a bounded falsification harness, not a proof of #677.
        for k in range(1, 7):
            for n in range(0, 60):
                a = lcm_interval(n,k)
                for m in range(n+k, 90):
                    self.assertNotEqual(a,lcm_interval(m,k))

    def test_678_cambie_selfridge_witness(self):
        self.assertEqual(lcm_interval(96,7), 8321670749700)
        self.assertEqual(lcm_interval(104,8), 3803928503760)
        self.assertGreater(lcm_interval(96,7), lcm_interval(104,8))
        self.assertGreater(lcm_interval(52,7), lcm_interval(62,8))
        self.assertGreaterEqual(104,96+7)

    def test_679_omega_vs_big_omega(self):
        self.assertEqual(len(factors(30)),3)
        self.assertEqual(len(factors(24)),2)
        self.assertEqual(sum(factors(24).values()),4)

    def test_680_prime_and_composite_qualify(self):
        self.assertTrue(prime(11))
        self.assertGreater(smallest_factor(11),1*1+1)
        self.assertFalse(prime(9))
        self.assertGreater(smallest_factor(9),1*1+1)

    def test_681_composite_required(self):
        self.assertFalse(prime(9))
        self.assertGreater(smallest_factor(9),1*1)
        self.assertTrue(prime(11))

    def test_682_gap_boundary_and_conditional_template(self):
        self.assertTrue(prime(7) and prime(11) and prime(13))
        self.assertFalse(any(prime(i) for i in range(8, 11)))
        self.assertTrue(all(smallest_factor(i)<4 for i in range(8,11)))
        self.assertEqual(smallest_factor(12),2)
        self.assertFalse(prime(2183))
        self.assertFalse(prime(2201))
        self.assertTrue(all(smallest_factor(i)<18 for i in range(2184,2201)))

    def test_683_strict_lean_target_falsified(self):
        for a in range(2,10):
            n=2**a
            k=n-1
            largest=max(factors(math.comb(n,k)))
            self.assertEqual(largest,2)
            # For every c>0, min(n-k+1,k**(1+c))=2.
            for c in [0.1, 0.5, 1.0]:
                rhs=min(n-k+1,k**(1+c))
                self.assertEqual(rhs,2)
                self.assertFalse(largest>rhs)
                self.assertTrue(largest>=rhs)
        self.assertEqual(math.comb(8,8),1)
        self.assertEqual(factors(1),{})

    def test_684_small_index_partial_function(self):
        self.assertEqual(math.comb(10,7),120)
        self.assertEqual(small_part(10,7),120)
        self.assertEqual(next(k for k in range(11) if small_part(10,k)>100),7)
        vals=[small_part(20,k) for k in range(21)]
        self.assertEqual(max(vals),240)
        self.assertLess(max(vals),400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
