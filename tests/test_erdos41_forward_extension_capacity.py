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


def shadow_arena(J):
    vals=tuple(J)
    assert vals
    j0,j1=min(vals),max(vals)
    return set(range(2*j0-j1,2*j1-j0+1))


def shadow_potential(p,J):
    arena=shadow_arena(J)
    return len(arena-shadow(p))


def reflected_signed_word_certificate(p, reflected):
    """Exact two-colour B3 word conditions, with/without middle anchor."""
    t=tuple(sorted(reflected))
    p=tuple(sorted(p))
    p_pairs=[a+b for a,b in combinations_with_replacement(p,2)]
    t_pairs=[a+b for a,b in combinations_with_replacement(t,2)]
    pp_minus_t=[s-x for s in p_pairs for x in t]
    p_minus_tt=[x-s for x in p for s in t_pairs]
    unanchored=(is_b3(t) and len(set(pp_minus_t))==len(pp_minus_t)
                and len(set(p_minus_tt))==len(p_minus_tt))
    anchored=(unanchored and not (set(t)&shadow(p))
              and not (set(p)&shadow(t)))
    return unanchored,anchored


def seven_layer_offsets(p, d, t):
    """Enumerate every unordered three-term word by its digit level."""
    result={j:[] for j in range(7)}
    for a,b,c in combinations_with_replacement(sorted(p),3):
        result[0].append(a+b+c)
    for a,b in combinations_with_replacement(sorted(p),2):
        for v in d:
            result[1].append(a+b+v)
    for v in p:
        for a,b in combinations_with_replacement(sorted(d),2):
            result[2].append(v+a+b)
    for a,b in combinations_with_replacement(sorted(p),2):
        for v in t:
            result[2].append(a+b-v)
    for a,b,c in combinations_with_replacement(sorted(d),3):
        result[3].append(a+b+c)
    for a in p:
        for b in d:
            for v in t:
                result[3].append(a+b-v)
    for a,b in combinations_with_replacement(sorted(d),2):
        for v in t:
            result[4].append(a+b-v)
    for v in p:
        for a,b in combinations_with_replacement(sorted(t),2):
            result[4].append(v-a-b)
    for v in d:
        for a,b in combinations_with_replacement(sorted(t),2):
            result[5].append(v-a-b)
    for a,b,c in combinations_with_replacement(sorted(t),3):
        result[6].append(-a-b-c)
    return result


def seven_layer_exact(p,d,t):
    offsets=seven_layer_offsets(p,d,t)
    return all(len(x)==len(set(x)) for x in offsets.values())


def seven_layer_cardinal_bounds(n,m,ell,R):
    from math import comb
    sizes=(comb(n+2,3),m*comb(n+1,2),
           n*comb(m+1,2)+ell*comb(n+1,2),
           comb(m+2,3)+n*m*ell,
           ell*comb(m+1,2)+n*comb(ell+1,2),
           m*comb(ell+1,2),comb(ell+2,3))
    limits=(3*R+1,3*R+1,4*R+1,4*R+1,
            4*R+1,3*R+1,3*R+1)
    return sizes,limits


def three_layer_interval_hall(p,d,t):
    """Exact integer range capacities for levels 2, 3, 4."""
    assert p and d and t
    pm,pM=min(p),max(p)
    dm,dM=min(d),max(d)
    tm,tM=min(t),max(t)
    windows=(
        ((pm+2*dm,pM+2*dM),(2*pm-tM,2*pM-tm)),
        ((3*dm,3*dM),(pm+dm-tM,pM+dM-tm)),
        ((2*dm-tM,2*dM-tm),(pm-2*tM,pM-2*tm)),
    )
    sizes=[]
    for (a,b),(c,e) in windows:
        sizes.append((b-a+1)+(e-c+1)-max(0,min(b,e)-max(a,c)+1))
    return tuple(sizes)


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


    def test_exact_shadow_potential_upper_bounds_true_batch(self):
        for prefix,J in (([1,2,5],range(23,28)),
                         ([1,2,5,14],range(23,28)),
                         ([1,2,5],range(25,34)),
                         ([1,2,5,14],range(25,34)),
                         ([1,2,5,14,33],range(61,73))):
            with self.subTest(prefix=prefix):
                phi=shadow_potential(prefix,J)
                x=capacity(prefix,J)
                self.assertLessEqual(f(len(x)),phi)
                self.assertLessEqual(len(x),F(phi))
                self.assertEqual(phi,len(shadow_arena(J)-shadow(prefix)))

    def test_exact_monotone_shadow_tax_telescopes_without_duplication(self):
        prefixes=([1,2,5], [1,2,5,14], [1,2,5,14,33],
                  [1,2,5,14,33,72])
        self.assertTrue(all(is_b3(p) for p in prefixes))
        J=range(160,301)
        phi=[shadow_potential(p,J) for p in prefixes]
        taxes=[phi[i]-phi[i+1] for i in range(len(phi)-1)]
        self.assertTrue(all(t>=0 for t in taxes))
        self.assertEqual(sum(taxes),phi[0]-phi[-1])
        arena=shadow_arena(J)
        new_sets=[(shadow(prefixes[i+1])-shadow(prefixes[i])) & arena
                  for i in range(len(prefixes)-1)]
        self.assertEqual(taxes,list(map(len,new_sets)))
        self.assertEqual(sum(map(len,new_sets)),
                         len(set().union(*new_sets)))
        for i in range(len(new_sets)):
            for j in range(i+1,len(new_sets)):
                self.assertFalse(new_sets[i]&new_sets[j])

    def test_forward_mixed_shadow_forces_potential_decrement(self):
        for p,y,R in (([1,2,5],[14],5),
                      ([1,2,5],[61,70,81],30)):
            with self.subTest(p=p,y=y):
                J,H=check_future_window(p,y,R)
                phi_before=shadow_potential(p,J)
                phi_after=shadow_potential(p+y,J)
                self.assertGreaterEqual(phi_before-phi_after,len(H))
                self.assertEqual(len(H),len(p)*len(y)*(len(y)+1)//2)
                self.assertTrue(H.issubset(shadow_arena(J)))
                self.assertFalse(H & shadow(p))
                self.assertTrue(H.issubset(shadow(p+y)))
                self.assertLessEqual(
                    len(capacity(p+y,J)) if len(J)<=12 else 0,
                    F(phi_after))


    def test_internal_shadow_contains_unique_median_triples(self):
        from math import comb
        for n in (3,4,5,8,12,17,29):
            p=A[:n]
            lo,hi=min(p),max(p)
            median={a+c-b for a,b,c in __import__("itertools").combinations(p,3)}
            with self.subTest(n=n):
                self.assertEqual(len(median),comb(n,3))
                self.assertFalse(median & set(p))
                self.assertTrue(median.issubset(set(range(lo,hi+1))))
                interior={v for v in shadow(p) if lo<=v<=hi}
                self.assertGreaterEqual(len(interior),n+comb(n,3))
                self.assertTrue(median.issubset(interior))

    def test_one_anchor_cubic_tax_and_exponential_raw_batch_bound(self):
        from math import comb, exp
        for p,y in (([1,2,5],14),
                    ([1,2,5,14],34),
                    (list(A[:5]),90),
                    (list(A[:8]),800)):
            if not is_b3(p+[y]):
                continue
            R=max(p); assert y>2*R
            j=range(2*y-R,2*y-min(p)+1)
            interior={v for v in shadow(p) if min(p)<=v<=max(p)}
            excluded={2*y-v for v in interior}
            before=singleton_available(p,j)
            after=singleton_available(p+[y],j)
            with self.subTest(n=len(p),y=y):
                self.assertEqual(before,set(j))
                self.assertTrue(excluded.issubset(set(j)-after))
                self.assertGreaterEqual(len(before)-len(after),len(interior))
                for size in (1,2,3):
                    remaining=len(j)-len(interior)
                    raw=comb(len(j),size) if size<=len(j) else 0
                    upper=comb(remaining,size) if size<=remaining else 0
                    self.assertLessEqual(upper,raw*exp(-len(interior)*size/len(j))+1e-10)

    def test_canonical_one_anchor_loss_without_true_batch_loss(self):
        p=[1,2,5,14];y=34;R=14
        self.assertTrue(is_b3(p+[y]))
        j=list(range(2*y-R,2*y-min(p)+1))
        self.assertEqual((j[0],j[-1]),(54,67))
        internal={v for v in shadow(p) if min(p)<=v<=max(p)}
        self.assertEqual(len(internal),12)
        self.assertEqual(len(singleton_available(p,j)),14)
        self.assertEqual(singleton_available(p+[y],j),{61})
        c0,c1=capacity(p,j),capacity(p+[y],j)
        self.assertEqual((len(c0),len(c1)),(1,1))
        self.assertTrue(is_b3(p+c0))
        self.assertTrue(is_b3(p+[y]+c1))

    def test_short_template_translations_blocked_within_canonical_window(self):
        p=[1,2,5,14];y=34;R=14
        j=list(range(2*y-R,2*y-min(p)+1))
        internal={v for v in shadow(p) if min(p)<=v<=max(p)}
        forbidden={2*y-v for v in internal}
        for template in ([0],[0,1],[0,1,4],[0,1,4,13]):
            if not is_b3(template):
                continue
            d=max(template)
            eligible=list(range(j[0],j[-1]-d+1))
            definitely_blocked=[t for t in eligible if t in forbidden]
            self.assertGreaterEqual(len(definitely_blocked),max(0,len(internal)-d))
            for t in definitely_blocked:
                self.assertFalse(is_b3(p+[y]+[t+v for v in template]))


    def test_reflected_signed_word_equivalence_all_small_future_sets(self):
        from itertools import combinations
        p=[1,2,5,14];R=max(p)
        for y in (100,101,250):
            self.assertGreater(y,6*R)
            self.assertTrue(is_b3(p+[y]))
            candidate=tuple(range(min(p),R+1))
            checked=0
            for k in range(0,len(candidate)+1):
                for t in combinations(candidate,k):
                    x=[2*y-v for v in t]
                    unanchored,anchored=reflected_signed_word_certificate(p,t)
                    with self.subTest(y=y,t=t):
                        self.assertEqual(is_b3(p+x),unanchored)
                        self.assertEqual(is_b3(p+[y]+x),anchored)
                    checked+=1
            self.assertEqual(checked,1<<len(candidate))

    def test_reflected_true_batch_optimum_is_anchor_invariant(self):
        p=[1,2,5,14]
        before=[]
        after=[]
        for y in (100,101,250):
            J=list(range(2*y-max(p),2*y-min(p)+1))
            cb,ca=capacity(p,J),capacity(p+[y],J)
            before.append(len(cb))
            after.append(len(ca))
        self.assertEqual(before,[1,1,1])
        self.assertEqual(after,[1,1,1])

    def test_reflection_conditions_are_not_naive_b3_of_color_union(self):
        # The reflected colour T may share literal integers with old P.
        # This is allowed before inserting y, but not afterward.
        p=[1,2,5]
        t=[1]
        unanchored,anchored=reflected_signed_word_certificate(p,t)
        self.assertTrue(unanchored)
        self.assertFalse(anchored)
        y=100
        self.assertTrue(is_b3(p+[2*y-1]))
        self.assertFalse(is_b3(p+[y,2*y-1]))


    def test_seven_layer_exact_equivalence_every_future_subset(self):
        from itertools import combinations
        p=[1,2,5]
        d=[0,11]
        R=14
        y=100
        self.assertTrue(is_b3(p+[y+x for x in d]))
        checks=0
        for k in range(R+1):
            for t in combinations(range(1,R+1),k):
                direct=is_b3(p+[y+x for x in d]+[2*y-x for x in t])
                layers=seven_layer_exact(p,d,t)
                self.assertEqual(direct,layers)
                if direct:
                    weights,budgets=seven_layer_cardinal_bounds(
                        len(p),len(d),len(t),R)
                    self.assertTrue(all(a<=b for a,b in zip(weights,budgets)))
                    offsets=seven_layer_offsets(p,d,t)
                    self.assertEqual(tuple(map(len, (offsets[i] for i in range(7)))),
                                     weights)
                checks+=1
        self.assertEqual(checks,1<<R)

    def test_three_colour_count_bound_captures_cross_type_collisions(self):
        p=[1,2,5]
        d=[0,11]
        y=100
        t=[1,2,3]
        assert is_b3(p+[y+x for x in d])
        offsets=seven_layer_offsets(p,d,t)
        self.assertEqual(len(offsets[3]),
                         len(d)*(len(d)+1)*(len(d)+2)//6+
                         len(p)*len(d)*len(t))
        self.assertTrue(any(len(v)!=len(set(v)) for v in offsets.values()))
        self.assertFalse(is_b3(p+[y+x for x in d]+[2*y-x for x in t]))

    def test_three_colour_degenerate_single_anchor_reconciles_reflection(self):
        p=[1,2,5,14]
        y=100
        for t in ((),(1,),(6,),(1,6),(8,10),(2,9,13)):
            three=seven_layer_exact(p,[0],t)
            _,anchored=reflected_signed_word_certificate(p,t)
            self.assertEqual(three,anchored)
            self.assertEqual(three,is_b3(p+[y]+[2*y-x for x in t]))


    def test_local_hall_word_intervals_contain_all_real_offsets(self):
        p=[1,2,5];d=[0,11];R=14;y=100
        from itertools import combinations
        for k in (1,2,3,4):
            for t in combinations(range(1,R+1),k):
                h=three_layer_interval_hall(p,d,t)
                offsets=seven_layer_offsets(p,d,t)
                sizes=tuple(len(offsets[j]) for j in (2,3,4))
                self.assertTrue(all(
                    h[j-2]>=len(set(offsets[j]))
                    for j in (2,3,4)))
                self.assertTrue(all(s<=4*R+1 for s in h))
                if seven_layer_exact(p,d,t):
                    self.assertTrue(all(a<=b for a,b in zip(sizes,h)))

    def test_local_hall_can_strictly_sharpen_global_range(self):
        p=[1,2,5];d=[0,11];t=[1,4]
        h=three_layer_interval_hall(p,d,t)
        self.assertTrue(all(x<=4*14+1 for x in h))
        self.assertTrue(any(x<4*14+1 for x in h))


if __name__=="__main__":
    unittest.main()
