#!/usr/bin/env python3
"""Historical source-test: 1970 upper-third witness separates P conventions."""
import itertools
import json
from pathlib import Path

def source_upper_third(x: int) -> tuple[int, ...]:
    # The [x/3]+1 greatest positive integers not exceeding x.
    assert x >= 1
    return tuple(range(x - (x//3), x+1))

def weak_distinct(a: tuple[int, ...]) -> bool:
    return all((b+c)%small != 0
               for small in a for b,c in itertools.combinations(a,2)
               if small < b and small < c)

def strong_repeated(a: tuple[int, ...]) -> bool:
    return all((b+c)%small != 0
               for small in a
               for b,c in itertools.combinations_with_replacement(a,2)
               if small < b and small < c)

def audit():
    rows=[]
    for m in range(1,201):
        x=3*m
        s=source_upper_third(x)
        assert len(s)==m+1
        assert s[0]==2*m and s[-1]==3*m
        assert weak_distinct(s),m
        # One repeated larger term suffices to break the stricter variant.
        assert 2*m < 3*m and (3*m+3*m)%(2*m)==0
        assert not strong_repeated(s)
        rows.append({"x":x,"card":len(s),"weak_P":True,"strong_P":False})
    # Distinct-versus-equal repetition is a real mathematical distinction.
    assert weak_distinct((3,6))
    assert not strong_repeated((3,6))
    # A source counterexample to strict repeated-summand interpretation
    # must not be interpreted as a counterexample to any asymptotic conjecture.
    return {"schema":"GCL_ERDOS_012_PRIMARY_CONVENTION_FALSIFIER_V1",
            "checked_m":200,"all_weak":True,"all_strong":False,
            "primary_paper":"Erdos-Sarkozy, Proc. London Math. Soc. (3) 21 (1970), pp97-98",
            "primary_pdf_sha256":"4adba03f04de19ebb6ac9bddc6eaf43567619ca96c6cbe574e4c04be3595d0f3",
            "witness_m1":{"x":3,"A":[2,3],"repeat_collision":[2,3,3]},
            "witness_m2":{"x":6,"A":[4,5,6],"repeat_collision":[4,6,6]},
            "last_test":rows[-1],
            "historical_statement_solved":False,
            "external_i_ii_proofs_replayed":False}

if __name__=="__main__":
    result=audit()
    Path(__file__).with_name("property_p_1970_primary_regression_receipt.json").write_text(
        json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,sort_keys=True))
