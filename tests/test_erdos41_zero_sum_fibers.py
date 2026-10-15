"""Repetition-permitted B3 zero-sum fiber matching, multishell obstruction.

All verification is finite. The infinite B3 density question is not decided.
"""
from collections import defaultdict
from itertools import combinations, combinations_with_replacement
from random import Random
import unittest

A29 = (1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
       3098,4048,5298,6704,7839,10987,12332,15465,
       19144,24546,28974,34406,37769,45864,50877)


def is_b3(A):
    sums = [sum(t) for t in combinations_with_replacement(A,3)]
    return len(sums)==len(set(sums))


def fibers(X):
    result = defaultdict(list)
    for a,b in combinations_with_replacement(X,2):
        for c in X:
            result[a+b-2*c].append((a,b,c))
    return result


class ZeroSumFiberTests(unittest.TestCase):
    def test_exact_matching_multiplicity_all_B3_subblocks(self):
        self.assertTrue(is_b3(A29))
        rng=Random(41)
        blocks=[A29[:n] for n in (1,2,3,4,6,8,12,20,29)]
        blocks.extend(tuple(rng.sample(A29,n)) for n in (2,3,5,9,17))
        for X in blocks:
            n=len(X); R=fibers(X)
            self.assertEqual(len(R[0]),n)
            for d, representations in R.items():
                if d==0:continue
                positive=[{a,b} for a,b,c in representations]
                self.assertEqual(len(set().union(*positive)),
                                 sum(map(len,positive)),(n,d,representations))
                e=sum(a!=b for a,b,c in representations)
                h=len(representations)-e
                self.assertLessEqual(2*e+h,n)
                self.assertLessEqual(h,1)
                self.assertLessEqual(len(representations),(n+1)//2)

    def test_mass_and_weighted_exact_all_prefix_sizes(self):
        for n in range(1,30):
            X=A29[:n]
            R=fibers(X)
            q=n*(n+1)//2
            self.assertEqual(sum(len(v) for v in R.values()),n*q)
            self.assertEqual(len(R[0]),n)
            self.assertEqual(sum(len(v) for d,v in R.items() if d),n*(q-1))
            weighted=sum(sum(2 if a!=b else 1 for a,b,c in values)
                         for d,values in R.items() if d)
            self.assertEqual(weighted,n*(n*n-1))
            D=max(X)-min(X)
            self.assertLessEqual(n*n-1,4*D)
            self.assertTrue(all(-2*D<=d<=2*D for d in R))

    def test_translation_invariance_and_true_B3_shared_lag(self):
        X=(1,2,5,14); Y=(33,72,125,219); A=X+Y
        self.assertTrue(is_b3(A))
        self.assertIn((1,5,2),fibers(X)[2])
        self.assertIn((33,219,125),fibers(Y)[2])
        self.assertIn(2, set(fibers(X)).intersection(fibers(Y)))
        for h in (-193,0,1000):
            XX=tuple(x+h for x in X)
            self.assertEqual({d:len(z) for d,z in fibers(XX).items()},
                             {d:len(z) for d,z in fibers(X).items()})

    def test_multiblock_fixed_lag_combined_matching(self):
        rng=Random(593)
        for _ in range(26):
            shuffled=list(A29);rng.shuffle(shuffled)
            k=rng.choice((2,3,4,5,8,11))
            blocks=[tuple(shuffled[i::k]) for i in range(k)]
            R=[fibers(X) for X in blocks]
            for d in set().union(*(set(r) for r in R)):
                if d==0:continue
                e=sum(sum(a!=b for a,b,c in r.get(d,())) for r in R)
                h=sum(sum(a==b for a,b,c in r.get(d,())) for r in R)
                self.assertLessEqual(2*e+h,len(A29))

    def test_colored_mixed_block_matching_competition(self):
        A=A29[:16]
        R=fibers(A)
        for k in (2,3,4,8):
            color={a:i%k for i,a in enumerate(A)}
            observed_mixed=False
            for d,rep in R.items():
                if d==0:continue
                within=sum(2 if a!=b else 1 for a,b,c in rep
                           if color[a]==color[b]==color[c])
                cross=sum(2 if a!=b else 1 for a,b,c in rep
                          if not(color[a]==color[b]==color[c]))
                self.assertLessEqual(within+cross,len(A))
                observed_mixed |= cross>0
            self.assertTrue(observed_mixed)

    def test_hostile_non_B3_fiber_shared_vertex(self):
        A=(1,2,3)
        self.assertFalse(is_b3(A))
        R=fibers(A)
        self.assertGreater(sum(2 if a!=b else 1 for a,b,c in R[1]),len(A))
        positive=[{a,b} for a,b,c in R[1]]
        self.assertLess(len(set().union(*positive)),sum(map(len,positive)))

    def test_explicit_infinite_formula_prefixes_are_B3(self):
        def block(j):
            t=16**(2*j+2)
            k=16**(2*j+1)
            return t,t+k,t+2*k+1
        for m in (1,2,3,4,5,10,20):
            A=tuple(v for j in range(m) for v in block(j))
            self.assertTrue(is_b3(A),m)
            self.assertEqual(len(A),3*m)
            self.assertEqual(len(fibers(A)[1]),m)
            for j in range(m):
                x,y,z=block(j)
                self.assertEqual(x+z-2*y,1)
                self.assertEqual(x+z-2*y,block(0)[0]+block(0)[2]-2*block(0)[1])
            self.assertEqual(len(set(A)),len(A))

    def test_arbitrarily_many_disjoint_scales_share_lag_one(self):
        blocks=[]
        for j in range(28):
            T=16**(2*j+2)
            k=16**(2*j+1)
            X=(T,T+k,T+2*k+1)
            blocks.append(X)
            self.assertEqual(len(fibers(X)[1]),1)
        self.assertEqual(sum(len(fibers(X)[1]) for X in blocks),28)
        self.assertTrue(all(max(blocks[j])<min(blocks[j+1])
                            for j in range(len(blocks)-1)))
        self.assertTrue(is_b3(tuple(v for X in blocks[:20] for v in X)))
        self.assertTrue(all(4*len(X) >= 2*sum(a!=b for a,b,c in fibers(X)[1])
                            for X in blocks))

    def test_small_exhaustive_genuine_B3_sets(self):
        examined=0
        for n in range(1,5):
            for X in combinations(range(1,15),n):
                if not is_b3(X):continue
                examined+=1
                R=fibers(X)
                self.assertEqual(len(R[0]),n)
                for d,z in R.items():
                    if d==0:continue
                    self.assertLessEqual(sum(2 if a!=b else 1 for a,b,c in z),n)
        self.assertGreater(examined,100)

if __name__ == '__main__':
    unittest.main()
