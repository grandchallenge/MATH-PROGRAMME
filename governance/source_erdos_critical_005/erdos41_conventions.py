import itertools

def historical(a):
    z=[sum(x) for k in (1,2,3) for x in itertools.combinations(a,k)]
    return len(z)==len(set(z))
def old_finset(a):
    z=[sum(x) for x in itertools.combinations(a,3)]
    return len(z)==len(set(z))
def new_multiset(a):
    z=[sum(x) for x in itertools.combinations_with_replacement(a,3)]
    return len(z)==len(set(z))

def validate():
    assert (historical((1,2,4)),new_multiset((1,2,4)))==(True,False)
    assert (historical((1,4,5)),new_multiset((1,4,5)))==(False,True)
    assert (old_finset((1,2,3)),new_multiset((1,2,3)))==(True,False)
    n=0
    for k in range(1,5):
        for a in itertools.combinations(range(1,13),k):
            if historical(a) or new_multiset(a):
                assert old_finset(a)
            n+=1
    return n
if __name__=='__main__':print('B3_CONVENTION_CHECKS_PASS',validate())
