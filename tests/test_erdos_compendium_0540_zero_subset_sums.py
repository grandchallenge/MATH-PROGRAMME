"""Exact finite subset-sum semantics for PROVED Erdős #540.

These enumerations do not reproduce Szemerédi's 1970 proof or the
external Lean4.29.1 dependency/kernel closure.
"""
from itertools import combinations


def recursive_nonempty_sums(A,N):
    seen=set()
    for a in A:
        assert 0<=a<N
        seen |= {a} | {(s+a)%N for s in seen}
    return seen


def direct_nonempty_sums(A,N):
    return {sum(S)%N for k in range(1,len(A)+1)
            for S in combinations(A,k)}


def is_zero_free(A,N):
    return 0 not in recursive_nonempty_sums(A,N)


def max_zero_free_branchbound(N):
    candidates=range(1,N)
    best=0
    witness=()
    def visit(i,chosen,sums):
        nonlocal best,witness
        if len(chosen)+N-1-i<=best:return
        if i==N-1:
            if len(chosen)>best:
                best=len(chosen);witness=chosen
            return
        a=i+1
        shifted={(s+a)%N for s in sums}
        if a!=0 and 0 not in shifted:
            visit(i+1,chosen+(a,),sums|{a}|shifted)
        visit(i+1,chosen,sums)
    visit(0,(),set())
    return best,witness


def max_zero_free_mask(N):
    best=0
    for mask in range(1<<(N-1)):
        if mask.bit_count()<=best:continue
        A=tuple(a for a in range(1,N) if mask&(1<<(a-1)))
        if is_zero_free(A,N):
            best=len(A)
    return best


def k_prime_formula(p):
    k=0
    while (k+1)*(k+2)//2 < p:
        k+=1
    return k


def test_540_subset_sums_two_independent_oracles():
    for N in range(2,11):
        for A in combinations(range(N),min(3,N)):
            assert recursive_nonempty_sums(A,N)==direct_nonempty_sums(A,N)
    assert recursive_nonempty_sums((1,2,3),7)==set(range(1,7))
    assert 0 in recursive_nonempty_sums((0,),11)
    assert not is_zero_free((0,),11)


def test_540_exact_small_composite_and_prime_maxima():
    for N in range(2,13):
        best,witness=max_zero_free_branchbound(N)
        assert best==max_zero_free_mask(N)
        assert is_zero_free(witness,N)
        assert len(witness)==best
        assert all(0<a<N for a in witness)


def test_540_sharp_prime_threshold_independent_enumeration():
    for p in (2,3,5,7,11,13,17,19,23):
        k=k_prime_formula(p)
        assert k*(k+1)//2<p<=(k+1)*(k+2)//2
        assert is_zero_free(tuple(range(1,k+1)),p)
        if p<=17:
            best,witness=max_zero_free_branchbound(p)
            assert best==k and len(witness)==k
    # The general exact upper for p=19,23 is a proved Balandraud
    # theorem, not independently re-proved by this finite fixture.


def test_540_zero_residue_and_strict_triangular_boundary():
    for p in (2,3,5,7,11):
        assert not is_zero_free((0,),p)
        k=k_prime_formula(p)
        assert sum(range(1,k+1))<p
        assert 0 not in direct_nonempty_sums(range(1,k+1),p)
    assert not is_zero_free((1,2,4),7)  # 1+2+4=7
