"""Erdos 41: exact reciprocal fourth-order overlap barrier.

This checks genuine B3 carriers, the full pair-sum difference decomposition,
and mixed 4-sum collision certificates. No infinite density theorem claimed.
"""
from itertools import combinations_with_replacement
import unittest


A=[1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
   3098,4048,5298,6704,7839,10987,12332,15465,19144,
   24546,28974,34406,37769,45864,50877]


def b3(s):
    words=[sum(a) for a in combinations_with_replacement(sorted(s),3)]
    return len(words)==len(set(words))


def q(s):
    return {a+b for a,b in combinations_with_replacement(sorted(s),2)}


def t(s):
    return {a+b-c for a,b in combinations_with_replacement(sorted(s),2)
                  for c in s}


def positives(s):
    return {a-b for a in s for b in s if a>b}


def decomp(p,y):
    short=positives(q(p)) | positives({a+b for a in p for b in y}) | positives(q(y))
    u={b-c for b in y for c in t(p)}
    v={c-a for c in t(y) for a in p}
    far={b-a for b in q(y) for a in q(p)}
    baseline={b-a for b in y for a in p}
    return short,u,v,far,baseline


def certificate(p,y,d):
    lefts=[]
    rights=[]
    for a,b in combinations_with_replacement(sorted(p),2):
        for c in p:
            for z in y:
                if z-(a+b-c)==d:
                    for xx,yy in combinations_with_replacement(sorted(y),2):
                        for zz in y:
                            for cp in p:
                                if (xx+yy-zz)-cp==d:
                                    left=tuple(sorted((z,zz,c,cp)))
                                    right=tuple(sorted((xx,yy,a,b)))
                                    if left!=right:
                                        return left,right
    return None


class ReciprocalFourSumOverlapTests(unittest.TestCase):
    def test_exact_full_difference_partition_on_separated_actual_b3(self):
        for n,m in ((3,3),(4,4),(5,5),(7,7),(10,10)):
            p=A[:n]
            raw=A[n:n+m]
            R=max(max(p),max(raw)-min(raw)+1)
            shift=10*R
            y=[shift+a for a in raw]
            with self.subTest(n=n,m=m):
                self.assertGreater(min(y),5*R)
                self.assertTrue(b3(p+y))
                short,u,v,far,baseline=decomp(p,y)
                self.assertFalse(short & (u|v|far))
                self.assertFalse((u|v)&far)
                actual=positives(q(p+y))
                self.assertEqual(actual,short|u|v|far)
                self.assertTrue(baseline.issubset(u&v))
                self.assertEqual(len(baseline),len(p)*len(y))
                self.assertEqual(len(u|v),len(u)+len(v)-len(u&v))

    def test_nontrivial_four_sum_defect_on_genuine_eight_element_carrier(self):
        p=[1,2,5,14]
        y=[1033,1072,1125,1219]
        R=187
        self.assertGreater(min(y),5*R)
        self.assertTrue(b3(p+y))
        short,u,v,far,baseline=decomp(p,y)
        extra=(u&v)-baseline
        self.assertEqual((len(short),len(u),len(v),
                          len(u&v),len(baseline),len(extra),
                          len(u|v),len(far)),
                         (112,111,110,27,16,11,194,97))
        self.assertEqual(len(positives(q(p+y))),403)
        self.assertEqual(positives(q(p+y)),short|u|v|far)
        for d in sorted(extra):
            witness=certificate(p,y,d)
            self.assertIsNotNone(witness)
            left,right=witness
            self.assertNotEqual(left,right)
            self.assertEqual(sum(left),sum(right))
            # Canceling any common term would be an illegal 3-sum collision.
            self.assertFalse(set(left)&set(right))
            self.assertEqual(sum(a in p for a in left),2)
            self.assertEqual(sum(a in p for a in right),2)

    def test_extra_four_sum_defect_is_translation_invariant(self):
        p=[1,2,5,14]
        raw=[33,72,125,219]
        values=[]
        for shift in (1000,10000,100000):
            y=[shift+a for a in raw]
            _,u,v,_,baseline=decomp(p,y)
            values.append((
                len(u),len(v),len(u&v),len((u&v)-baseline),
                len(u|v)
            ))
            self.assertTrue(b3(p+y))
        self.assertEqual(len(set(values)),1)
        self.assertEqual(values[0][-2],11)

    def test_four_sum_collision_is_allowed_by_b3_but_not_b4(self):
        p=[1,2,5,14]
        y=[1033,1072,1125,1219]
        self.assertTrue(b3(p+y))
        four=[sum(z) for z in combinations_with_replacement(sorted(p+y),4)]
        self.assertLess(len(set(four)),len(four))
        _,u,v,_,base=decomp(p,y)
        self.assertGreater(len((u&v)-base),0)


if __name__=="__main__":
    unittest.main()
