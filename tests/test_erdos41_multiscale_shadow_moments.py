"""Exact-rational positive and hostile tests of arbitrary-block cubic-shadow moments.

The complete universal mathematical proof is in CROSS_SCALE_SHADOW_MOMENTS.md.
The simulated critical-density block profiles are NOT B3 sets.
"""
from itertools import combinations, combinations_with_replacement as cwr
from fractions import Fraction
from random import Random
import unittest

def is_b3(X):
    sums=[sum(t) for t in cwr(X,3)]
    return len(sums)==len(set(sums))

def shadow(X):
    return {a+b-c for a,b in cwr(X,2) for c in X}

def stats(X):
    n=len(X)
    f=n*(n*n-n+2)//2
    s=sum(X);q=sum(x*x for x in X)
    mu=Fraction(s,n)
    v=Fraction(q,n)-mu*mu
    lam=Fraction(3*n*n+3*n+2,n*n-n+2)
    return f,mu,v,lam

def moment_slack(Z):
    n=len(Z)
    return 12*(n*sum(x*x for x in Z)-sum(Z)**2)-n*n*(n*n-1)

def cross_slack(blocks):
    v=[stats(X) for X in blocks]
    F=sum(t[0] for t in v)
    within=F*sum((f*lam*variance for f,mu,variance,lam in v),Fraction(0))
    between=sum((f*g*(mu-nu)**2
                 for i,(f,mu,_,_) in enumerate(v)
                 for g,nu,_,_ in v[i+1:]),Fraction(0))
    return 12*(within+between)-F*F*(F*F-1)

def union_interval_length(blocks):
    intervals=sorted((2*min(X)-max(X),2*max(X)-min(X)) for X in blocks)
    size=0;right=-10**100
    for lo,hi in intervals:
        if hi>right:
            size+=hi-max(lo,right+1)+1
            right=hi
    return size

class CrossScaleShadowTests(unittest.TestCase):
    def test_exact_shadow_moments_exhaustive_small_b3(self):
        seen=0
        for n in range(1,6):
            for X in combinations(range(1,18),n):
                if not is_b3(X):continue
                seen+=1
                f,mu,v,lam=stats(X)
                T=shadow(X)
                self.assertEqual(len(T),f)
                self.assertEqual(sum(T),f*mu)
                self.assertEqual(sum(t*t for t in T),f*(mu*mu+lam*v))
        self.assertGreater(seen,100)

    def test_arbitrary_many_blocks_of_genuine_m3_set(self):
        A=(1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,3098,
           4048,5298,6704,7839,10987,12332,15465,19144,24546,28974,
           34406,37769,45864,50877)
        self.assertTrue(is_b3(A))
        rng=Random(41)
        for split_size in (1,2,3,4,5,7,11):
            blocks=[A[i:i+split_size] for i in range(0,len(A),split_size)]
            self._verify(blocks)
        for _ in range(35):
            shuffled=list(A)
            rng.shuffle(shuffled)
            blocks=[tuple(shuffled[i:i+3]) for i in range(0,len(A),3)]
            self._verify(blocks)

    def _verify(self,blocks):
        Ts=[shadow(X) for X in blocks]
        union=set().union(*Ts)
        F=sum(map(len,Ts))
        self.assertEqual(F,len(union))
        self.assertEqual(sum(stats(X)[0] for X in blocks),F)
        self.assertGreaterEqual(cross_slack(blocks),0)
        self.assertEqual(cross_slack(blocks),moment_slack(union))
        self.assertLessEqual(F,union_interval_length(blocks))

    def test_variance_sensitive_b3_spacing_and_hostile_cluster(self):
        for n in range(1,5):
            for X in combinations(range(1,17),n):
                if not is_b3(X):continue
                f,mu,v,lam=stats(X)
                self.assertGreaterEqual(v, Fraction(f*f-1,12)/lam)
        clustered=(1,2,3)
        self.assertFalse(is_b3(clustered))
        f,mu,v,lam=stats(clustered)
        self.assertLess(v, Fraction(f*f-1,12)/lam)

    def test_parity_wall_translation_covariance_and_failed_anchor(self):
        X=(1,2,5)
        self.assertTrue(is_b3(X))
        for h in (-121,-1,0,1,1000):
            self.assertEqual(shadow(tuple(x+h for x in X)),
                             {t+h for t in shadow(X)})
        self.assertEqual(1+5-2*2,2+2-2*1)
        self.assertNotEqual((1,5,2),(2,2,1))

    def test_abstract_critical_scale_model_moments_do_not_force_collision(self):
        # AP blocks deliberately not M3; this tests only the NECESSARY
        # summary constraints (CROSS) and (RANGE), not realizability.
        for K in (8,10,12,14):
            blocks=[]
            for j in range(6,K+1):
                L=8**j
                n=max(2,2**j//32)
                step=(7*L-1)//(n+1)
                blocks.append(tuple(L+k*step for k in range(1,n+1)))
            self.assertGreaterEqual(cross_slack(blocks),0)
            self.assertLessEqual(sum(stats(X)[0] for X in blocks),
                                 union_interval_length(blocks))
            self.assertFalse(is_b3(blocks[-1]))
