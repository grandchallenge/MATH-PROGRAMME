"""Exact residue-by-residue capacity certificates for the Erdős #41 graph.

Run: python -m unittest discover -s tests -p 'test_erdos41_residue_lp.py' -v
The integer programme is a necessary condition, not a B3 solution.
"""
from collections import Counter
from itertools import combinations_with_replacement, product
import unittest


def pair_sums(u):
    return {x+y for x,y in combinations_with_replacement(sorted(u),2)}


def b3(u):
    triples = [sum(t) for t in combinations_with_replacement(sorted(u),3)]
    return len(set(triples))==len(triples)


def feasible(p, interval, w, q, plus_one=False):
    a=Counter(x%q for x in p)
    b=Counter(x%q for x in w)
    for scale in (1,2) if plus_one else (2,):
        lo=min(p)+scale*min(interval)
        hi=max(p)+scale*max(interval)
        caps=Counter(x%q for x in range(lo,hi+1))
        for t in range(q):
            assigned=sum(a[r]*b[s] for r in range(q) for s in range(q)
                         if (r+scale*s)%q==t)
            if assigned>caps[t]:
                return False
    return True


def residue_integer_programme(p, interval, q):
    per_class=Counter(v%q for v in interval)
    best=0
    for b in product(*(range(per_class[s]+1) for s in range(q))):
        if sum(b)<=best:
            continue
        class_counts=[s for s in range(q) for _ in range(b[s])]
        if feasible(p,interval,class_counts,q):
            best=sum(b)
    return best


def independent(p,w):
    return len({v+2*z for v in p for z in w})==len(p)*len(w)


class ResidueCapacityTests(unittest.TestCase):
    def test_short_finite_graph_exact_alpha_and_lp(self):
        u=[1,2,5]
        self.assertTrue(b3(u))
        p=pair_sums(u)
        interval=list(range(20,29))
        D=max(u)-min(u); L=max(interval)-min(interval)
        self.assertEqual((2*D+2*L+1)//len(p),4)
        bounds={q:residue_integer_programme(p,interval,q)
                for q in (2,3,4,5,7)}
        self.assertEqual(bounds[2],3)
        exact=0
        for mask in range(1<<len(interval)):
            w=[interval[j] for j in range(len(interval)) if (mask>>j)&1]
            if not independent(p,w):
                continue
            exact=max(exact,len(w))
            for q,bound in bounds.items():
                with self.subTest(mask=mask,q=q):
                    self.assertLessEqual(len(w),bound)
                    self.assertTrue(feasible(p,interval,w,q))
                    if w and b3(u+w):
                        self.assertTrue(feasible(p,interval,w,q,plus_one=True))
        self.assertEqual(exact,2)

    def test_parity_bound_is_strictly_stronger_than_triple_capacity(self):
        u=[1,5,33]
        self.assertTrue(b3(u))
        p=pair_sums(u)
        self.assertTrue(all(v%2==0 for v in p))
        D=max(u)-min(u); L=32
        q=len(p)
        global_bound=(2*D+2*L+1)//q
        triple_bound=(2*D+L+1)//q
        parity_bound=(D+L+1)//q
        self.assertEqual((global_bound,triple_bound,parity_bound),(21,16,10))
        I=list(range(100,133))
        even_positions=sum(v%2==0 for v in range(min(p)+2*min(I),
                                                   max(p)+2*max(I)+1))
        self.assertEqual(even_positions,D+L+1)

    def test_hostile_nondirect_sum_rejected(self):
        p={0,2,4}
        interval=list(range(1,7))
        w=[1,2]
        self.assertFalse(independent(p,w))
        # Never infer feasibility of exact injection from mere class totals.
        self.assertGreaterEqual(residue_integer_programme(p,interval,2),1)


if __name__=="__main__":
    unittest.main()
