"""Exact regression for both half-open and positive-integer periodic counts."""
from fractions import Fraction
import hashlib
import json

def run():
    digest=hashlib.sha256()
    cases=0
    predicates=0
    for period in range(1,9):
        for mask in range(1<<period):
            predicates+=1
            q=lambda x: (mask>>(x%period))&1
            k=sum(q(x) for x in range(period))
            delta=Fraction(k,period)
            for n in sorted(set(range(1,3*period+2))|{11*period-1,11*period,11*period+1}):
                for start in (0,1):
                    count=sum(q(x) for x in range(start,start+n))
                    blocks,tail=divmod(n,period)
                    assert count==blocks*k+sum(q(x) for x in range(start,start+tail))
                    assert abs(Fraction(count,n)-delta)<=Fraction(period,n)
                    digest.update(f'{period},{mask},{start},{n},{count}\n'.encode())
                    cases+=1
    # Removing the tail term gives a wrong count for a partial block.
    assert sum(x%3==0 for x in range(4))!=4//3
    # Without periodicity the count of the first block need not repeat.
    assert sum(x<3 for x in range(6))!=2*sum(x<3 for x in range(3))
    result={'result':'PASS','predicates':predicates,'cases':cases,'hostile_controls':2,'digest':digest.hexdigest()}
    print(json.dumps(result,sort_keys=True))
    return result

if __name__=='__main__':
    run()
