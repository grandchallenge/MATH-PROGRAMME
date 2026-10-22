"""Exact deterministic containers for B3 future batches.

The theorem counts all legal k-batches in arbitrary future intervals.
It does not prove an Erdős 41 density valley.
"""
from itertools import combinations, combinations_with_replacement
from math import ceil, comb, log
import unittest


A=[1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
   3098,4048,5298,6704,7839,10987,12332,15465,19144,
   24546,28974,34406,37769,45864,50877]


def is_b3(xs):
    sums=[sum(z) for z in combinations_with_replacement(sorted(xs),3)]
    return len(sums)==len(set(sums))


def pair_sums(xs):
    return {a+b for a,b in combinations_with_replacement(sorted(xs),2)}


def difference_graph(p,positions):
    Q=pair_sums(p)
    differences={a-b for a in Q for b in Q if a!=b}
    return {x:{y for y in positions if y!=x and (x-y) in differences}
            for x in positions}


def edges_induced(G,U):
    U=set(U)
    return sum(len(G[v]&U) for v in U)//2


def density_params(p,R,c=None):
    n=len(p)
    q=comb(n+1,2)
    if c is None:
        delta=q*q/(12*R*n)
    else:
        delta=c**3/48
    s=min(R,ceil(6*R/q))
    t=ceil(max(0,log(R/s))/(-log(1-2*delta))) if s<R else 0
    return delta,s,t


def encode_independent(G,I,s,t):
    """Canonical fingerprint: selected ITERATIONS plus residual vertices."""
    I=set(I)
    assert all(b not in G[a] for a,b in combinations(sorted(I),2))
    U=set(G)
    marked=[]
    iteration=0
    chosen=0
    while len(U)>s and chosen<t:
        iteration+=1
        v=min(U,key=lambda w:(-len(G[w]&U),w))
        if v in I:
            marked.append(iteration)
            chosen+=1
            U.difference_update(G[v]|{v})
        else:
            U.remove(v)
    assert len(U)<=s
    assert I.issuperset(I&U)
    return tuple(marked),tuple(sorted(I&U))


def decode_fingerprint(G,code,s,t):
    marked,remainder=code
    markers=set(marked)
    U=set(G)
    selected=[]
    iteration=0
    while len(U)>s and len(selected)<t:
        iteration+=1
        v=min(U,key=lambda w:(-len(G[w]&U),w))
        if iteration in markers:
            selected.append(v)
            U.difference_update(G[v]|{v})
        else:
            U.remove(v)
    assert tuple(sorted(U&set(remainder)))==remainder
    return tuple(sorted(selected+list(remainder)))


class IntegralFutureContainerTests(unittest.TestCase):
    def test_prefix_pair_sums_are_unique(self):
        for n in (4,5,8,12,20,29):
            p=A[:n]
            self.assertTrue(is_b3(p))
            self.assertEqual(len(pair_sums(p)),comb(n+1,2))

    def test_supersaturation_for_arbitrary_adversarial_subsets(self):
        p=[1,2,5,14]
        R=16
        G=difference_graph(p,range(1,R+1))
        n=len(p);q=len(pair_sums(p))
        for mask in range(1<<R):
            U=[i+1 for i in range(R) if mask>>i&1]
            m=len(U)
            lower=(m*m*q*q/(3*R)-m*q)/(2*n)
            self.assertGreaterEqual(edges_induced(G,U)+1e-9,lower)

    def test_fingerprint_is_injective_and_decodes_every_independent_set(self):
        p=[1,2,5,14]
        R=16
        G=difference_graph(p,range(1,R+1))
        # Use exact stronger delta here; for this small R the general
        # asymptotic profile bound is too weak to give an informative t.
        delta,s,t=density_params(p,R)
        seen={}
        for mask in range(1<<R):
            I=tuple(i+1 for i in range(R) if mask>>i&1)
            if any(v in G[u] for u,v in combinations(I,2)):
                continue
            code=encode_independent(G,I,s,t)
            self.assertNotIn(code,seen)
            seen[code]=I
            self.assertEqual(decode_fingerprint(G,code,s,t),I)
            self.assertLessEqual(len(code[0]),t)
            self.assertLessEqual(len(code[1]),s)
        self.assertGreater(len(seen),1)

    def test_container_count_agrees_with_all_exact_independent_sets(self):
        p=[1,2,5,14]
        R=16
        G=difference_graph(p,range(1,R+1))
        _,s,t=density_params(p,R)
        for k in range(0,5):
            independent=sum(
                all(v not in G[u] for u,v in combinations(T,2))
                for T in combinations(range(1,R+1),k)
            )
            ceiling=sum(comb(R,j)*comb(s,k-j)
                        for j in range(0,min(k,t)+1)
                        if 0<=k-j<=s)
            self.assertLessEqual(independent,ceiling)

    def test_arbitrary_future_interval_constraint_has_no_anchor(self):
        p=[1,2,5,14]
        for origin in (30,100,1000,10000):
            J=range(origin,origin+16)
            G=difference_graph(p,J)
            for T in combinations(J,2):
                if is_b3(p+list(T)):
                    self.assertNotIn(T[1],G[T[0]])
            self.assertEqual(edges_induced(G,J),
                             edges_induced(difference_graph(p,range(1,17)),
                                           range(1,17)))

    def test_forced_future_annulus_extraction_constants(self):
        c=.2
        C0=18**(1/3)
        lam=max(2,ceil((2*C0/c)**3))
        eta=C0/(lam-1)
        self.assertGreater(eta,0)
        self.assertGreaterEqual(c*lam**(1/3),2*C0-1e-10)
        # This is algebra for the conditional A(N)>=cN^(1/3)
        # hypothesis, not a fake infinite dense B3 witness.
        for R in (1000,1000000):
            lower=c*(lam*R)**(1/3)-C0*R**(1/3)
            self.assertGreaterEqual(lower+1e-9,eta*(lam-1)*R**(1/3))


if __name__=="__main__":
    unittest.main()
