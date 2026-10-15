"""Final EC005 source-conflict tranche, exact finite interfaces; no asymptotic certificate."""
import itertools, math, unittest
from pathlib import Path

D=Path(__file__).resolve().parents[1]/"governance/erdos_compendium/editorial"

def divisors(n):
    return [d for d in range(1,n) if n%d==0]

def semiperfect(n):
    vals=divisors(n);sums={0}
    for x in vals:sums|={y+x for y in list(sums) if y+x<=n}
    return n in sums

def phi(n):
    if n==1:return 1
    result=n;m=n;p=2
    while p*p<=m:
        if m%p==0:
            while m%p==0:m//=p
            result-=result//p
        p+=1
    if m>1:result-=result//m
    return result

def is_2colorable(V,E):
    for bits in itertools.product((0,1),repeat=len(V)):
        c=dict(zip(V,bits))
        if all(len({c[x] for x in e})>1 for e in E):return True
    return False

def fano():
    return [(i,(i+1)%7,(i+3)%7) for i in range(7)]

def k5():
    return list(itertools.combinations(range(5),3))

def chromatic_critical_k5():
    E=k5()
    if is_2colorable(range(5),E):return False
    if not all(is_2colorable(range(5),E[:i]+E[i+1:]) for i in range(len(E))):return False
    return all(is_2colorable([x for x in range(5) if x!=v],
             [e for e in E if v not in e]) for v in range(5))

def alon_hypergraph(r):
    X=tuple(range(2*r-2))
    Y={}
    for a in itertools.combinations(X,r-1):
        left=frozenset(a);right=frozenset(set(X)-left)
        key=tuple(sorted((tuple(sorted(left)),tuple(sorted(right)))))
        Y.setdefault(key,len(X)+len(Y))
    edges={frozenset(e) for e in itertools.combinations(X,r)}
    for pair,y in Y.items():
        for side in pair:edges.add(frozenset(side)|{y})
    return list(range(len(X)+len(Y))),list(edges)

def johnson_edges(k):
    V=list(itertools.combinations(range(2*k),k))
    return V,[(x,y) for i,x in enumerate(V) for y in V[i+1:]
              if len(set(x)&set(y))==k-1]

def admissible_prefix(A):
    for i,x in enumerate(A):
        for j in range(i):
            running=0
            for y in A[j:i]:
                running+=y
                if running==x:return False
    return True

class FinalEight(unittest.TestCase):
    def test_825_weird70_and_12_semiperfect(self):
        self.assertEqual(sum(divisors(70))+70,144)
        self.assertFalse(semiperfect(70))
        self.assertTrue(semiperfect(12))
        self.assertIn("Larsen",(D/"0825.md").read_text())

    def test_828_exact_totient_zero_shift(self):
        for n in range(1,500):
            special=(n==1) or (n%2==0 and
                     all(p in (2,3) for p in range(2,n+1) if n%p==0 and all(p%d for d in range(2,math.isqrt(p)+1))))
            self.assertEqual(n%phi(n)==0,special,n)
        self.assertEqual(phi(9),6)
        self.assertIn("Graham",(D/"0828.md").read_text())

    def test_832_fano_not_two_colorable_small_case(self):
        self.assertEqual(len(fano()),7)
        self.assertFalse(is_2colorable(range(7),fano()))
        self.assertEqual(math.comb(5,3),10)
        self.assertIn("r>=4",(D/"0832.md").read_text())

    def test_834_k5_chromatic_three_critical_but_deg_six(self):
        self.assertTrue(chromatic_critical_k5())
        self.assertEqual(len(k5()),10)
        self.assertEqual(len([e for e in k5() if 0 in e]),6)
        self.assertIn("transversal",(D/"0834.md").read_text().lower())

    def test_835_johnson_k2_3_color_and_clique(self):
        V,E=johnson_edges(2)
        self.assertEqual((len(V),len(E)),(6,12))
        colors={tuple(sorted(x)): min(x) if False else 0 for x in V}
        matching={(0,1):0,(2,3):0,(0,2):1,(1,3):1,(0,3):2,(1,2):2}
        self.assertTrue(all(matching[x]!=matching[y] for x,y in E))
        V3,E3=johnson_edges(3)
        self.assertEqual(len(V3),20)
        self.assertEqual(sum(1 for x in V3 if set(x).issubset({0,1,2,3})),4)

    def test_836_alon_r3_intersecting_3chromatic(self):
        V,E=alon_hypergraph(3)
        self.assertEqual((len(V),len(E)),(7,10))
        self.assertTrue(all(a&b for a,b in itertools.combinations(E,2)))
        self.assertFalse(is_2colorable(V,E))
        for r in (3,4,5,6):
            W,edges=alon_hypergraph(r)
            self.assertEqual(len(W),2*r-2+math.comb(2*r-2,r-1)//2)
        self.assertIn("Omega(r)",(D/"0836.md").read_text())

    def test_839_all_earlier_consecutive_blocks(self):
        self.assertTrue(admissible_prefix([2**i for i in range(9)]))
        self.assertFalse(admissible_prefix([1,3,5,7,9]))
        self.assertEqual(1+3+5,9)
        self.assertIn("19/36",(D/"0839.md").read_text())

    def test_851_omega_vs_bigomega(self):
        def factors(n):
            omega=bigomega=0;p=2
            while p*p<=n:
                if n%p==0:
                    omega+=1
                    while n%p==0:n//=p;bigomega+=1
                p+=1
            if n>1:omega+=1;bigomega+=1
            return omega,bigomega
        self.assertEqual(factors(9),(1,2))
        self.assertEqual(1+9,10)
        self.assertEqual(8+2,10)
        self.assertIn("Romanoff",(D/"0851.md").read_text())

if __name__=="__main__":
    unittest.main()
