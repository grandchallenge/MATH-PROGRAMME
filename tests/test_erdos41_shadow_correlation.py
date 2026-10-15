"""Exact autocorrelation spectrum and cross-pair forbidden-difference tests.

The universal mathematical proofs are in SHADOW_CORRELATION_SPECTRUM.md.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement as multi
from random import Random
import unittest


def is_b3(A):
    sums = [sum(t) for t in multi(A, 3)]
    return len(sums) == len(set(sums))


def pair_sums(X):
    return {a+b for a,b in multi(X,2)}


def autocorrelations(X):
    P=pair_sums(X)
    return Counter(p-q for p in P for q in P)


def difference(A):
    return {a-b for a in A for b in A}


class CorrelationSpectrumTests(unittest.TestCase):
    A=(1,2,5,14,33,72,125,219,376,573,745,1209,1557,
       2442,3098,4048,5298,6704,7839,10987,12332,15465,
       19144,24546,28974,34406,37769,45864,50877)

    def test_complete_selector_on_genuine_b3_across_many_subsets(self):
        self.assertTrue(is_b3(self.A))
        rng=Random(41)
        choices=[tuple(),(self.A[0],),self.A[:2],self.A[:3],
                 self.A[:7],self.A[-6:],self.A]
        choices.extend(tuple(rng.sample(self.A,n)) for n in (1,2,3,5,8,13,18))
        for X in choices:
            n=len(X); R=autocorrelations(X)
            self.assertEqual(R[0],n*(n+1)//2)
            for a in self.A:
                for b in self.A:
                    if a==b: continue
                    self.assertEqual(R[a-b],n if a in X and b in X else 0,
                                     (len(X),a,b))
            self.assertEqual(sum(R[d] for d in difference(self.A) if d),
                             n*n*(n-1))
            self.assertEqual(sum(R[d]==0 for d in difference(self.A) if d),
                             len(self.A)*(len(self.A)-1)-n*(n-1))

    def test_cross_pair_spectra_exclude_every_A_difference(self):
        rng=Random(593)
        for _ in range(35):
            A=list(self.A)
            rng.shuffle(A)
            n=rng.randrange(1,14)
            k=rng.randrange(1,14)
            X=tuple(A[:n]); Y=tuple(A[n:n+k])
            cross={p-q for p in pair_sums(X) for q in pair_sums(Y)}
            self.assertFalse(cross.intersection(difference(self.A)))
            self.assertGreaterEqual(len(cross),
                                    len(pair_sums(X))+len(pair_sums(Y))-1)

    def test_gram_quadratic_form_and_all_eigenvalues(self):
        rng=Random(138)
        A=self.A[:12]
        for n in range(1,13):
            X=A[:n]; R=autocorrelations(X)
            q=n*(n+1)//2
            self.assertEqual((q-n),n*(n-1)//2)
            self.assertEqual(q+n*(n-1),n*(3*n-1)//2)
            for _ in range(7):
                z={a:rng.randrange(-5,6) for a in A}
                lhs=sum(R[a-b]*z[a]*z[b] for a in A for b in A)
                rhs=(q-n)*sum(z[a]**2 for a in X)+n*sum(z[a] for a in X)**2
                rhs+=q*sum(z[a]**2 for a in A if a not in X)
                self.assertEqual(lhs,rhs)
                self.assertGreaterEqual(rhs,0)

    def test_naive_cross_pair_spectrum_disjointness_is_false(self):
        A=self.A[:12]
        blocks=[A[i:i+3] for i in range(0,len(A),3)]
        P=[pair_sums(X) for X in blocks]
        by_diff={}
        found=None
        for i in range(len(P)):
            for j in range(len(P)):
                if i==j: continue
                for a in P[i]:
                    for b in P[j]:
                        d=a-b
                        if d in by_diff and by_diff[d][:2]!=(i,j):
                            found=(by_diff[d],(i,j,a,b))
                            break
                        by_diff[d]=(i,j,a,b)
                    if found:break
                if found:break
            if found:break
        self.assertIsNotNone(found)
        (i,j,a,b),(k,l,c,d)=found
        self.assertEqual(a-b,c-d)

    def test_arbitrary_blocks_orthogonal_translation_features(self):
        A=self.A[:12]
        for size in (1,2,3,4,6):
            blocks=[A[i:i+size] for i in range(0,len(A),size)]
            P=[pair_sums(X) for X in blocks]
            k=len(blocks);m=len(A)
            for i in range(k):
                for j in range(i+1,k):
                    for a in A:
                        for b in A:
                            self.assertTrue({p+a for p in P[i]}.isdisjoint(
                                            {q+b for q in P[j]}))
            left=min(2*min(X)+min(A) for X in blocks)
            right=max(2*max(X)+max(A) for X in blocks)
            self.assertLessEqual(k*m,right-left+1)
            self.assertLessEqual(k*m,3*(max(A)-min(A))+1)

    def test_non_b3_cluster_violates_selector(self):
        A=(1,2,3,100)
        X=(1,2,3)
        self.assertFalse(is_b3(A))
        R=autocorrelations(X)
        self.assertEqual(R[1-2],4)
        self.assertNotEqual(R[1-2],len(X))


if __name__ == '__main__':
    unittest.main()
