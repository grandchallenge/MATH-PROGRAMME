"""Erdos 41: exact forward-shadow future-capacity regression.

Run: python -m unittest discover -s tests -p 'test_erdos41_forward_extension_capacity.py' -v
Tests are finite. Critical-density theorem is conditional; no infinite B3 set
at critical lower density or Erdős #41 solution is claimed.
"""
from itertools import combinations_with_replacement
import unittest

A = (1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
     3098,4048,5298,6704,7839,10987,12332,15465,19144,
     24546,28974,34406,37769,45864,50877)


def triple_sums(a):
    return [sum(t) for t in combinations_with_replacement(sorted(a),3)]


def is_b3(a):
    z=triple_sums(a)
    return len(z)==len(set(z))


def pair_sums(a):
    return {x+y for x,y in combinations_with_replacement(sorted(a),2)}


def shadow(a):
    return {x+y-z for x,y in combinations_with_replacement(sorted(a),2)
                     for z in a}


def forward_shadow(p,y):
    return {a+b-x for a,b in combinations_with_replacement(sorted(y),2)
                    for x in p}


def f(ell):
    return (ell**3-ell**2+2*ell)//2


def F(budget):
    if budget<0:
        return -1
    ell=0
    while f(ell+1)<=budget:
        ell+=1
    return ell


def capacity(p,J):
    """Exact branch-and-bound of true (not singleton) B3 extension capacity.

    Return one maximal-cardinality extension. All new triple sums added with
    each candidate z are explicitly enumerated, repetitions allowed.
    """
    p=tuple(sorted(p))
    base=set(triple_sums(p))
    assert len(base)==len(triple_sums(p))
    candidates=tuple(sorted(J))
    best=[]

    def recurse(i,chosen,sums):
        nonlocal best
        if len(chosen)>len(best):
            best=chosen[:]
        if i>=len(candidates) or len(chosen)+len(candidates)-i<=len(best):
            return
        z=candidates[i]
        old=p+tuple(chosen)
        new=[z+a+b for a,b in combinations_with_replacement(sorted(old),2)]
        new.extend([2*z+a for a in old])
        new.append(3*z)
        if len(new)==len(set(new)) and not set(new)&sums:
            recurse(i+1,chosen+[z],sums|set(new))
        recurse(i+1,chosen,sums)

    recurse(0,[],base)
    return best


def singleton_available(p,J):
    return {z for z in J if is_b3(list(p)+[z])}


def check_future_window(p,y,R):
    assert min(p)>=1 and max(p)<=R
    assert is_b3(p+y)
    a,b=min(y),max(y)
    assert a>2*R and b<2*a-R
    lo,hi=2*a-R,2*b-min(p)
    J=range(lo,hi+1)
    H=forward_shadow(p,y)
    assert H.issubset(set(J))
    assert lo>max(y) and lo>3*R
    return J,H


class ForwardShadowCapacityTests(unittest.TestCase):
    def test_actual_b3_fixture_and_shadow_formula(self):
        self.assertTrue(is_b3(A))
        for n in (1,2,3,4,5,8,12,17,29):
            with self.subTest(n=n):
                x=A[:n]
                self.assertEqual(len(shadow(x)),f(n))
                self.assertEqual(f(n), (n**3-n**2+2*n)//2)

    def test_mixed_shadow_exact_count_and_nonoverlap(self):
        for p,y in ((A[:3],A[3:5]),
                    (A[:6],A[6:9]),
                    (A[:10],A[10:14]),
                    (A[:12],A[12:17])):
            with self.subTest(np=len(p),ny=len(y)):
                self.assertTrue(is_b3(p+y))
                h=forward_shadow(p,y)
                self.assertEqual(len(h),len(p)*len(y)*(len(y)+1)//2)
                self.assertFalse(h & set(p+y))
                x=A[len(p)+len(y):len(p)+len(y)+3]
                self.assertTrue(is_b3(p+y+x))
                self.assertFalse(h & shadow(x))

    def test_canonical_future_window_loses_all_forward_shadow_sites(self):
        p=[1,2,5];y=[14]; R=5
        J,H=check_future_window(p,y,R)
        self.assertEqual((J.start,J.stop-1),(23,27))
        self.assertEqual(H,{23,26,27})
        self.assertEqual(singleton_available(p,J),set(J))
        self.assertTrue(H.isdisjoint(singleton_available(p+y,J)))
        self.assertGreaterEqual(
            len(singleton_available(p,J))-len(singleton_available(p+y,J)),
            len(H))
        self.assertEqual(len(shadow(p+y)),f(len(p+y)))
        c0,c1=capacity(p,J),capacity(p+y,J)
        self.assertEqual(len(c0),1)
        self.assertEqual(len(c1),0)
        L=J.stop-J.start-1
        self.assertLessEqual(f(len(c1))+len(H),3*L+1)
        self.assertLessEqual(len(c1),F(3*L+1-len(H)))

    def test_longer_genuine_critical_order_middle_block(self):
        # Geometry for n=3, m=3, R=30: 18 distinct newly blocked sites.
        p=[1,2,5]; y=[61,70,81]; R=30
        self.assertTrue(is_b3(p+y))
        J,H=check_future_window(p,y,R)
        self.assertEqual((J.start,J.stop-1),(92,161))
        self.assertEqual(len(J),70)
        self.assertEqual(len(H),18)
        self.assertEqual(singleton_available(p,J),set(J))
        self.assertTrue(H.isdisjoint(singleton_available(p+y,J)))
        self.assertGreaterEqual(
            len(J)-len(singleton_available(p+y,J)),len(H))
        for z in (92,110,130,150,161):
            if is_b3(p+y+[z]):
                self.assertFalse(H & shadow([z]))
        self.assertLessEqual(f(0)+len(H),3*(len(J)-1)+1)
        self.assertLessEqual(F(3*(len(J)-1)+1-len(H)),
                             F(3*(len(J)-1)+1))

    def test_singleton_tax_does_not_imply_true_batch_tax(self):
        p=[1,2,5]; y=[14]
        J=range(25,34)
        H=forward_shadow(p,y)
        self.assertEqual(H & set(J),{26,27})
        self.assertTrue({26,27}.issubset(singleton_available(p,J)))
        self.assertFalse({26,27} & singleton_available(p+y,J))
        c0,c1=capacity(p,J),capacity(p+y,J)
        self.assertEqual((len(c0),len(c1)),(1,1))
        self.assertEqual(c0,[25])
        self.assertEqual(c1,[33])

    def test_true_capacity_is_monotone_and_cubic_envelope_valid(self):
        p=[1,2,5]; y=[14]
        for j0,j1 in ((23,27),(25,33),(26,37),(30,40)):
            J=range(j0,j1+1)
            c0=capacity(p,J)
            c1=capacity(p+y,J)
            self.assertGreaterEqual(len(c0),len(c1))
            self.assertTrue(is_b3(p+c0))
            self.assertTrue(is_b3(p+y+c1))
            L=j1-j0
            self.assertLessEqual(f(len(c0)),3*L+1)
            if J.start<=23 and J.stop-1>=27:
                self.assertLessEqual(f(len(c1))+3,3*L+1)

    def test_shadow_tax_cannot_exceed_enclosing_integer_budget(self):
        for p,y,R in (([1,2,5],[14],5),([1,2,5],[61,70,81],30)):
            J,H=check_future_window(p,y,R)
            self.assertLessEqual(len(H),len(J))
            self.assertLessEqual(len(H),3*(len(J)-1)+1)

    def test_non_b3_hostile_invalidates_injectivity(self):
        p=[1,2,3];y=[4,5,6]
        self.assertFalse(is_b3(p+y))
        self.assertLess(len(forward_shadow(p,y)),
                        len(p)*len(y)*(len(y)+1)//2)


    def test_fixed_shape_blocked_translation_tax(self):
        for p,y in (([1,2,5],[14]),([1,2,5],[61,70,81])):
            H=forward_shadow(p,y)
            for template in ([0],[0,1],[0,1,4],[0,1,4,13]):
                with self.subTest(p=p,y=y,x=template):
                    self.assertTrue(is_b3(template))
                    shadow_template=shadow(template)
                    shifts={h-s for h in H for s in shadow_template}
                    bound=len(H)+f(len(template))-1
                    self.assertGreaterEqual(len(shifts),bound)
                    full_span=max(H)-min(H)+(
                        max(shadow_template)-min(shadow_template))+1
                    self.assertLessEqual(len(shifts),full_span)
                    # For every shift for which all three blocks are
                    # genuinely disjoint, the full union cannot be B3.
                    for t in sorted(shifts)[:15]:
                        x=[z+t for z in template]
                        if set(x).isdisjoint(set(p+y)):
                            self.assertFalse(is_b3(p+y+x))


if __name__=="__main__":
    unittest.main()
