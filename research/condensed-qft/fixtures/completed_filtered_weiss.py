#!/usr/bin/env python3
"""Exact finite regression for CF-001 completed filtered quantum Weiss theorem.

This checks grading, completed coproduct/cutoff logic, and Cauchy
multiplication; it is not a simulation of derived condensed modules.
"""
from fractions import Fraction as Q


def finite_terms(cutoff):
    """(r,k) indices in CG quotient /F^cutoff."""
    return {(r,k) for r in range(cutoff) for k in range(cutoff)
            if r + 2*k < cutoff}


def cg_formula_terms(cutoff):
    """Independent formula from F^N=prod_k hbar^k Sym^{>=N-2k}."""
    return {(r,k) for k in range(cutoff) for r in range(cutoff)
            if r < cutoff - 2*k}


def convolution(x,y,cutoff):
    out={}
    for i,a in x.items():
        for j,b in y.items():
            if i+j < cutoff:
                out[i+j]=out.get(i+j,Q(0))+a*b
    return {n:a for n,a in out.items() if a}


def quotient(x,cutoff):
    return {w:a for w,a in x.items() if w<cutoff}


def local_moment(stage,weight):
    # Normalized cocycle of weight j lives only in the jth interval.
    return Q(1) if 1 <= weight <= stage else Q(0)


def test():
    for N in range(1,24):
        assert finite_terms(N)==cg_formula_terms(N)
        # Finite weight cutoffs are invariant under d and hbar*Delta.
        for r,k in finite_terms(N):
            assert r+2*k < N
            if r>=2:
                assert (r-2)+2*(k+1)==r+2*k
                assert (r-2,k+1) in finite_terms(N)
        for j in range(1,N):
            assert local_moment(N-1,j)==Q(1)
        # The diagonal survives completion because a stage may depend on N.
        completed_tuple=tuple(local_moment(N-1,j) for j in range(1,N))
        assert completed_tuple==(Q(1),)*(N-1)
        # For every fixed stage k, sufficiently large N misses a coefficient.
        for k in range(0,N-1):
            assert local_moment(k,N-1)==Q(0)

    a={0:Q(2),1:Q(3),3:Q(4)}
    b={0:Q(5),2:Q(7),3:Q(8)}
    c={0:Q(1),1:Q(11),4:Q(1,3)}
    for N in range(1,15):
        assert convolution(convolution(a,b,N),c,N)==convolution(a,convolution(b,c,N),N)
        assert convolution(quotient(a,N),quotient(b,N),N)==convolution(a,b,N)
        for M in range(1,N+1):
            assert quotient(convolution(a,b,N),M)==convolution(a,b,M)
    # Completed sum differs from ordinary sum of already completed stages:
    # the diagonal has stage N-1 at quotient N but no common finite stage.
    for fixed_stage in range(1,8):
        assert local_moment(fixed_stage,fixed_stage+1)==Q(0)
    print('CF-001 finite quotient / completed Cauchy / Weiss controls: PASS')


if __name__=='__main__':
    test()
