#!/usr/bin/env python3
"""Exact offline certificates for GCL EC-BULK-006 Erdős #871/#872.

No network, third-party packages, GitHub mutations, or claims of infinite proof.
Two independent game encodings are compared at every n in [2,30].
"""
import json
import hashlib
from functools import lru_cache
from itertools import combinations
from pathlib import Path


def representation_counts(A, n):
    ordered = sum(a+b == n for a in A for b in A)
    unordered = sum(a+b == n for a in A for b in A if a <= b)
    diagonal = int(n % 2 == 0 and n//2 in A)
    return ordered, unordered, diagonal


def incompatibility_masks(n):
    xs = list(range(2, n+1))
    masks = [sum(1<<j for j,y in enumerate(xs) if (x % y == 0 or y % x == 0)) for x in xs]
    return xs, masks


def game_chosen_state(n, prolonger_first):
    """Independent state: selected antichain, terminal value is |selected|."""
    xs, comp = incompatibility_masks(n)
    full = (1 << len(xs)) - 1
    @lru_cache(None)
    def V(chosen):
        blocked = 0
        for i in range(len(xs)):
            if chosen & (1 << i):
                blocked |= comp[i]
        available = full & ~blocked
        if not available:
            return chosen.bit_count()
        maximizing = ((chosen.bit_count() % 2 == 0) == prolonger_first)
        outcomes = []
        while available:
            bit = available & -available
            available -= bit
            outcomes.append(V(chosen | bit))
        return max(outcomes) if maximizing else min(outcomes)
    return V(0), V.cache_info().currsize


def game_remaining_state(n, prolonger_first):
    """Independent state: remaining legal moves; returns number of future moves."""
    xs, comp = incompatibility_masks(n)
    @lru_cache(None)
    def W(remaining, maximizing):
        if not remaining:
            return 0
        outcomes = []
        bits = remaining
        while bits:
            bit = bits & -bits
            bits -= bit
            i = bit.bit_length() - 1
            outcomes.append(1 + W(remaining & ~comp[i], not maximizing))
        return max(outcomes) if maximizing else min(outcomes)
    return W((1 << len(xs))-1, prolonger_first), W.cache_info().currsize


def prime_count(n):
    return sum(x >= 2 and all(x%d for d in range(2,int(x**.5)+1)) for x in range(2,n+1))


def min_maximal_antichain(n):
    """Independent exhaustive terminal-antichain enumeration; bounded n<=22."""
    xs, comp = incompatibility_masks(n)
    full = (1<<len(xs))-1
    best = n
    witness = None
    count = 0
    def visit(i, chosen, covered):
        nonlocal best, witness, count
        if i == len(xs):
            if covered == full:
                count += 1
                if chosen.bit_count() < best:
                    best = chosen.bit_count()
                    witness = [xs[j] for j in range(len(xs)) if chosen & (1<<j)]
            return
        visit(i+1,chosen,covered)
        if not (covered & (1<<i)):
            visit(i+1,chosen | (1<<i),covered | comp[i])
    visit(0,0,0)
    return {'minimum_size':best,'witness':witness,'maximal_antichains':count}


def run():
    checks = 0
    examples=[]
    for m in range(1,9):
        for chosen in combinations(range(1,9),m):
            A = set(chosen)
            for n in range(2,18):
                o,u,d = representation_counts(A,n)
                assert o == 2*u-d, (chosen,n,o,u,d)
                checks += 1
                if A=={1,2,3,5,8} and n in (6,8,10):
                    examples.append({'A':sorted(A),'n':n,'ordered':o,'unordered':u,'diagonal':d})
    table=[]
    for n in range(2,31):
        p1,c1=game_chosen_state(n,True)
        p2,c2=game_remaining_state(n,True)
        s1,d1=game_chosen_state(n,False)
        s2,d2=game_remaining_state(n,False)
        assert p1==p2 and s1==s2,(n,p1,p2,s1,s2)
        assert p1<= (n+1)//2 and s1 <= (n+1)//2
        row={'n':n,'prolonger_first':p1,'shortener_first':s1,'pi_n':prime_count(n),
             'selected_states':c1,'remaining_states':c2}
        if n<=22:
            a=min_maximal_antichain(n)
            row.update(a)
            assert a['minimum_size'] <= p1 and a['minimum_size'] <= s1
            assert a['minimum_size']==row['pi_n']
        table.append(row)
    assert next(r for r in table if r['n']==9)['prolonger_first']==5
    assert next(r for r in table if r['n']==9)['shortener_first']==4
    assert next(r for r in table if r['n']==25)['shortener_first']==10
    assert next(r for r in table if r['n']==25)['pi_n']==9
    assert next(r for r in table if r['n']==30)['prolonger_first']==13
    assert next(r for r in table if r['n']==30)['shortener_first']==11
    result={'scope':'Erdos 871-872 exact finite checks; not an asymptotic proof',
            '871':{'unordered_ordered_identity_tests':checks,
                   'identity':'R_ordered(n)=2*R_unordered(n)-1_{n even and n/2 in A}',
                   'examples':examples},
            '872':{'definition':'primitive antichain of [2,n], alternating perfect-play minimax, terminal size',
                   'first_player_conventions':'P maximizes; S minimizes',
                   'table':table,
                   'notable':{'first_player_difference_at_n':9,
                              'shortener_first_exceeds_pi_n_at_n':25,
                              'finite_values_are_not_asymptotic_claims':True}},
            'validation':{'two_independent_minimax_encodings':'PASS n=2..30',
                          'terminal_antichain_crosscheck':'PASS n=2..22',
                          'ordered_unordered_identity':'PASS all nonempty A subsets [1,8], n=2..17'}}
    return result

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
