from itertools import combinations,combinations_with_replacement

def distinct_upto_3(a):
    sums=[sum(x) for k in (1,2,3) for x in combinations(a,k)]
    return len(sums)==len(set(sums))
def repeated_exact_3(a):
    sums=[sum(x) for x in combinations_with_replacement(a,3)]
    return len(sums)==len(set(sums))

def run():
    for k in range(0,8):
        hist=sorted([1,2,4]+[10**i for i in range(1,k+1)])
        strong=sorted([1,4,5]+[100**i for i in range(1,k+1)])
        assert distinct_upto_3(hist)
        assert not repeated_exact_3(hist)
        assert repeated_exact_3(strong)
        assert not distinct_upto_3(strong)
    return {'family_check_tail_sizes':list(range(8)),
            'historical_not_strong':'{1,2,4} union {10^k : k>=1}',
            'strong_not_historical':'{1,4,5} union {100^k : k>=1}',
            'proven_for_all_finite_subsets':'SUPERINCREASING_DIGIT_ARGUMENT',
            'original_problem_41_settled':False}
if __name__=='__main__':print(run())
