"""Exact sixth-moment collision ledger and two-block reciprocal resonance.

Repetition-permitted B3 throughout. Integer enumeration is a bounded
regression against the separate mathematical proof, NOT certification.
"""
from collections import Counter
from itertools import combinations_with_replacement, product
import unittest


def is_b3(xs):
    sums=[sum(z) for z in combinations_with_replacement(sorted(xs),3)]
    return len(sums)==len(set(sums))


def energy(xs):
    r=Counter(sum(tr) for tr in product(xs,repeat=3))
    return sum(c*c for c in r.values())


def baseline(n):
    return 6*n**3-9*n*n+4*n


def defect(xs):
    return energy(xs)-baseline(len(xs))


def weight(tr):
    return len(set(__import__("itertools").permutations(tr)))


def collision_ledger(xs):
    tris=list(combinations_with_replacement(sorted(xs),3))
    ans=0
    for i in range(len(tris)):
        for j in range(i+1,len(tris)):
            if sum(tris[i])==sum(tris[j]):
                ans+=2*weight(tris[i])*weight(tris[j])
    return ans


def pair_sum_weights(xs):
    out={}
    for a,b in combinations_with_replacement(sorted(xs),2):
        assert a+b not in out, "Only defined for B2/B3 sets"
        out[a+b]=1 if a==b else 2
    return out


def H(xs):
    qw=pair_sum_weights(xs)
    result=Counter()
    for q,w in qw.items():
        for qq,ww in qw.items():
            if q>qq:
                result[q-qq]+=w*ww
    return result


def G(xs):
    out=Counter()
    for a in xs:
        for b in xs:
            if a>b:
                out[a-b]+=1
    return out


def resonance(p,t):
    hp=H(p)
    ht=H(t)
    gp=G(p)
    gt=G(t)
    a=sum(v*gt[d] for d,v in hp.items())
    b=sum(v*gp[d] for d,v in ht.items())
    return 18*(a+b)


def shadow(xs):
    return {a+b-c for a,b in combinations_with_replacement(sorted(xs),2) for c in xs}


def xi4(p,y):
    u={a-b for a in y for b in shadow(p)}
    v={b-a for b in shadow(y) for a in p}
    base={b-a for b in y for a in p}
    return len((u&v)-base)


def moment_code(p):
    B=3*p+1
    return [1+i+B*(i*i%p)+B*B*(i*i*i%p) for i in range(p)]


class SixthDefectResonanceTests(unittest.TestCase):
    def test_unordered_collision_ledger_equals_fourier_energy(self):
        for xs in ([1],[1,2],[1,2,3],[1,2,5,14],
                   [1,2,5,14,17],[1,2,5,14,33,72]):
            with self.subTest(xs=xs):
                self.assertEqual(defect(xs),collision_ledger(xs))
                self.assertGreaterEqual(defect(xs),0)
                self.assertEqual(defect(xs)==0,is_b3(xs))

    def test_ledger_is_monotone_under_element_addition(self):
        for xs in ([1,2,5],[1,2,3],[1,2,5,14],[1,2,5,14,33]):
            before=defect(xs)
            for y in (100,1000,10000):
                with self.subTest(xs=xs,y=y):
                    self.assertGreaterEqual(defect(xs+[y]),before)

    def test_exact_farfield_formula_with_two_intrinsically_b3_blocks(self):
        psets=[[1],[1,2],[1,2,5],[1,2,5,14],moment_code(7)[:5]]
        tsets=[[1],[1,3],[1,2,5,14],[1,2,6,20],
               [33,72,125,219],moment_code(7)[:4]]
        for p in psets:
            for t in tsets:
                if not is_b3(p) or not is_b3(t):
                    continue
                target=resonance(p,t)
                W=max(max(p),max(t))
                for L in (3*W+1,5*W+1):
                    with self.subTest(p=p,t=t,L=L):
                        self.assertTrue(set(p).isdisjoint({L+x for x in t}))
                        union=p+[L+x for x in t]
                        self.assertEqual(defect(union),target)
                        self.assertEqual(is_b3(union),target==0)

    def test_reciprocal_correlation_is_translation_invariant(self):
        p=[1,2,5,14]
        t=[1,2,5,14]
        self.assertTrue(is_b3(p) and is_b3(t))
        self.assertEqual(resonance(p,t),2592)
        self.assertEqual(
            sum(v*G(t)[d] for d,v in H(p).items()),72)
        self.assertEqual(
            sum(v*G(p)[d] for d,v in H(t).items()),72)
        for L in (100,1000,10000):
            self.assertEqual(defect(p+[L+x for x in t]),2592)

    def test_colortype_separation_is_essential_to_equality(self):
        p=[1,2,5,14]
        t=[33,72,125,219]
        self.assertTrue(is_b3(p))
        self.assertTrue(is_b3(t))
        self.assertEqual(resonance(p,t),0)
        self.assertEqual(defect(p+[100+x for x in t]),12)
        self.assertEqual(defect(p+[1000+x for x in t]),0)

    def test_any_separation_multiblock_lower_bound(self):
        base=[1,2,5,14]
        for starts in ((0,100,1000),(0,50,100,150)):
            blocks=[[a+s for a in base] for s in starts]
            self.assertTrue(all(is_b3(b) for b in blocks))
            total=sum(resonance(blocks[i],blocks[j])
                      for i in range(len(blocks))
                      for j in range(i+1,len(blocks)))
            merged=[a for block in blocks for a in block]
            self.assertEqual(len(merged),len(set(merged)))
            self.assertGreaterEqual(defect(merged),total)
            self.assertGreater(total,0)

    def test_real_b3_has_four_sum_overlap_but_zero_sixth_defect(self):
        p=[1,2,5,14]
        y=[1033,1072,1125,1219]
        self.assertTrue(is_b3(p+y))
        self.assertEqual(xi4(p,y),11)
        self.assertEqual(resonance(p,y),0)
        self.assertEqual(defect(p+y),0)

    def test_resonance_positive_for_two_element_difference_collision(self):
        p=[1,2,5,14]
        t=[1,3]
        self.assertTrue(is_b3(t))
        self.assertEqual(resonance(p,t),72)
        self.assertEqual(defect(p+[100+t0 for t0 in t]),72)

    def test_moment_code_disjoint_components_have_zero_inherited_resonance(self):
        code=moment_code(11)
        self.assertTrue(is_b3(code))
        blocks=[code[:3],code[3:7],code[7:]]
        self.assertEqual(sum(resonance(blocks[i],blocks[j])
                             for i in range(3) for j in range(i+1,3)),0)


if __name__=="__main__":
    unittest.main()
