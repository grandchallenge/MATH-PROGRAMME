"""Exact tests for off-spectrum matching competition between B3 blocks."""
from collections import Counter, defaultdict
from itertools import combinations_with_replacement as pairs
from random import Random
import unittest


A29=(1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
     3098,4048,5298,6704,7839,10987,12332,15465,
     19144,24546,28974,34406,37769,45864,50877)


def b3(A):
    t=[sum(x) for x in pairs(A,3)]
    return len(t)==len(set(t))


def pair_map(A):
    return {a+b:(a,b) for a,b in pairs(A,2)}


def spectrum(X, Ys):
    P=pair_map(X)
    r=Counter(p-q for p in P for q in P)
    cs=[Counter(p-q for p in P for q in pair_map(Y)) for Y in Ys]
    return r,cs


class SpectralMatchingTests(unittest.TestCase):
    def test_pointwise_multiblock_cap_genuine_B3(self):
        self.assertTrue(b3(A29))
        rng=Random(41)
        for n in (1,2,3,5,8,13,19,28):
            for repeat in range(3):
                shuffled=list(A29)
                rng.shuffle(shuffled)
                X=shuffled[:n];Z=shuffled[n:]
                k=1+repeat*2
                Ys=[Z[i::k] for i in range(k)]
                r,cs=spectrum(X,Ys)
                q=len(X)*(len(X)+1)//2
                self.assertEqual(r[0],q)
                self.assertTrue(all(c[0]==0 for c in cs))
                for d in set(r).union(*(set(c) for c in cs)):
                    if d==0: continue
                    self.assertLessEqual(r[d]+sum(c[d] for c in cs),n)
                self.assertEqual(
                    sum(v for d,v in r.items() if d!=0)+
                    sum(sum(c.values()) for c in cs),
                    q*q-q+q*sum(len(Y)*(len(Y)+1)//2 for Y in Ys))

    def test_matching_positive_pair_supports_for_off_A_differences(self):
        A=A29[:14]
        D={a-b for a in A for b in A}
        for n in (2,5,8):
            X=A[:n];Ys=[A[n::2],A[n+1::2]]
            P=pair_map(X)
            groups=defaultdict(list)
            for p,positive in P.items():
                for q in P:
                    if p-q not in D:
                        groups[p-q].append(tuple(positive))
                for Y in Ys:
                    for q in pair_map(Y):
                        groups[p-q].append(tuple(positive))
            for d,positive_pairs in groups.items():
                self.assertNotIn(d,D)
                supports=[set(pair) for pair in positive_pairs]
                self.assertEqual(
                    len(set().union(*supports)),
                    sum(len(s) for s in supports),
                    (n,d,positive_pairs))
                self.assertLessEqual(len(supports),n)

    def test_exact_internal_off_first_mass_and_joint_quadratic(self):
        A=A29
        for n in (1,2,3,5,8,12,20,29):
            X=A[:n]
            Ys=[A[n:]]
            r,cs=spectrum(X,Ys)
            q=n*(n+1)//2
            D={a-b for a in A for b in A}
            off_mass=sum(v for d,v in r.items() if d not in D)
            self.assertEqual(off_mass,
                             n*(n-1)*(n*n-n+2)//4)
            s={d:r[d]+sum(c[d] for c in cs) for d in set(r)|set(cs[0]) if d!=0}
            M=q*q-q+q*len(pair_map(Ys[0]))
            self.assertEqual(sum(s.values()),M)
            self.assertLessEqual(sum(v*v for v in s.values()),n*M)
            H=max(A)-min(A)
            self.assertLessEqual(M,4*n*H)
            support_off=sum(v>0 for d,v in s.items() if d not in D)
            self.assertGreaterEqual(n*support_off,
                                    off_mass+q*len(pair_map(Ys[0])))

    def test_invalid_union_breaks_matching_cap(self):
        X=(1,2,5)
        Y=(3,4,7)
        self.assertTrue(b3(X))
        self.assertTrue(b3(Y))
        self.assertFalse(b3(X+Y))
        D={a-b for a in X+Y for b in X+Y}
        self.assertNotIn(-8,D)
        r,cs=spectrum(X,[Y])
        self.assertEqual((r[-8],cs[0][-8]),(1,3))
        self.assertGreater(r[-8]+cs[0][-8],len(X))

    def test_off_difference_multiplicity_bound_sharp_at_small_n(self):
        for A in ((1,2,5,14),(1,2,5,14,33,72),A29[:10]):
            self.assertTrue(b3(A))
            for n in range(1,len(A)+1):
                X=A[:n]
                D={a-b for a in A for b in A}
                r,_=spectrum(X,[])
                self.assertTrue(all(v<=n for d,v in r.items()
                                    if d not in D))


if __name__ == '__main__':
    unittest.main()
