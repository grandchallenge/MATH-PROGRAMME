"""Finite exact Ruzsa separated-prime construction for disproved #537.

Bounded collisions do not establish positive natural density or
constitute an independently replayed external Lean certification.
"""
from collections import defaultdict
from itertools import combinations
from sympy import factorint, primerange, isprime


def separated_squarefree(n):
    f=factorint(n)
    if any(e!=1 for e in f.values()):return False
    q=sorted(f)
    return all(b>2*a for a,b in zip(q,q[1:]))


def upper_half(N):
    return tuple(a for a in range(N//2+1,N+1) if 2*a>N and separated_squarefree(a))


def representations(A,pmax):
    m=defaultdict(set)
    for a in A:
        for p in primerange(2,pmax+1):
            m[a*p].add((a,int(p)))
    return m


def independent_bad_triple(A,pmax):
    P=tuple(int(p) for p in primerange(2,pmax+1))
    # Direct search for a common product using pairwise equality
    # before checking whether a third distinct prime represents it.
    vals={a*p:(a,p) for a in A for p in P}
    from collections import Counter
    ct=Counter(a*p for a in A for p in P)
    return any(v>=3 for v in ct.values())


def test_537_squarefree_gap_examples_and_interval():
    assert separated_squarefree(1)
    assert separated_squarefree(10)
    assert not separated_squarefree(6)
    assert not separated_squarefree(4)
    assert separated_squarefree(2*7*17)
    assert not separated_squarefree(2*5*7)
    for N in (50,100,200,400):
        A=upper_half(N)
        assert A and all(N/2<a<=N for a in A)
        assert all(separated_squarefree(a) for a in A)


def test_537_no_three_prime_multiple_representations():
    for N in (50,100,200,400):
        A=upper_half(N)
        m=representations(A,500)
        assert m
        assert all(len(v)<=2 for v in m.values())
        assert not independent_bad_triple(A,500)


def test_537_ratio_obstruction_exact_cross_multiplication():
    for N in (50,100,200,400):
        A=upper_half(N)
        for a in A:
            ps=sorted(factorint(a))
            for p,q in combinations(ps,2):
                assert q>2*p
        # Distinct members a2,a3 both in (N/2,N] satisfy a2/a3<2.
        for a,b in combinations(A,2):
            assert max(a,b) < 2*min(a,b)
    # In any triple p_i*a_i=m, p2,p3|a1 and p3/p2=a2/a3,
    # forcing both >2 and <2, contradiction.


def test_537_prime_quotient_stronger_than_equal_lcm():
    # Three prime quotients from lcm produce one form of lcm triangle.
    A=(6,10,15)
    assert 30//6==5 and 30//10==3 and 30//15==2
    assert all(isprime(30//a) for a in A)
    # Equal pairwise LCM can have COMPOSITE quotient, so it does
    # not necessarily produce three distinct prime multiples.
    C=(12,20,15)
    from math import lcm
    assert lcm(C[0],C[1])==lcm(C[0],C[2])==lcm(C[1],C[2])==60
    assert {60//a for a in C}=={3,4,5}
    assert not all(isprime(60//a) for a in C)
