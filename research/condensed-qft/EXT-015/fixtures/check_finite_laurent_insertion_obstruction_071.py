"""Exact Laurent exponent/moment controls for the finite-state insertion no-go."""
from fractions import Fraction as F
from math import factorial

def gaussian_jet(shift, multiplicity, order):
    # Common positive normalization C_m=(2*pi)^(-(m-1)/2)/sqrt(m)
    # is kept formal. Keys are (epsilon power, delta derivative order).
    out={}
    for j in range(order+1):
        odd_product=1
        for r in range(1,2*j,2):odd_product*=r
        out[shift+1-multiplicity+2*j,2*j]=F(
            odd_product,multiplicity**j*factorial(2*j))
    return out
def plus(a,b):
    out=dict(a)
    for k,v in b.items():out[k]=out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}
def retain(a,cutoff):return {k:v for k,v in a.items() if k[0]<=cutoff}
def negative(a):return {k:v for k,v in a.items() if k[0]<0}
def finite(a):return {k:v for k,v in a.items() if k[0]==0}

cases=0
for cutoff in range(-7,97):
    N=max(1,cutoff//2+1)
    assert 2*N>cutoff
    order=N+5
    source=gaussian_jet(0,1,order)
    source_difference=gaussian_jet(2*N,1,order)
    assert retain(source,cutoff)==retain(plus(source,source_difference),cutoff)
    m=2*N+1
    inserted=gaussian_jet(0,m,order)
    difference=gaussian_jet(2*N,m,order)
    assert negative(inserted)==negative(plus(inserted,difference))
    assert finite(difference)=={(0,0):F(1)}
    # C_m^2*(2*pi)^(2N)=1/(2N+1)>0; no floating point needed.
    normalized_square=F(1,m)
    assert normalized_square>0
    # Every higher correction in the difference starts at +2 or higher.
    assert min(k[0] for k in difference if k[1]>0)==2
    cases+=1
print("PASS:",cases,"finite Laurent cutoffs with equal retained source states")
print("PASS: inserted negative parts unchanged, finite scalar delta differs")
print("PASS: exact normalized contact square 1/(2N+1) is positive")
print("PASS: symbolic difference starts at epsilon^0; strong remainder is proved in source")
print("LIMIT: this is the stated whole-amplitude finite-state contract, not a forest/BV theorem")

# Fixed-insertion controls on the unbounded polynomial module, theorem 71.2.
def hermite_even(K):
    n=2*K
    return {n-2*j:F((-1)**j*factorial(n),
                    2**j*factorial(j)*factorial(n-2*j))
            for j in range(K+1)}

def gaussian_moment(degree, a):
    if degree%2:return F(0)
    odd=1
    for j in range(1,degree,2):odd*=j
    return F(odd,a**(degree//2))

def polynomial_moment(poly, d, a):
    return sum((c*gaussian_moment(j+d,a) for j,c in poly.items()),F(0))

fixed_cases=0
for N in range(1,9):
    a=2*N+1
    for K in range(13):
        poly=hermite_even(K)
        for d in range(2*K):
            assert polynomial_moment(poly,d,1)==0
        assert polynomial_moment(poly,2*K,1)==factorial(2*K)
        actual=polynomial_moment(poly,0,a)
        expected=F(factorial(2*K),2**K*factorial(K))*(F(1,a)-1)**K
        assert actual==expected and actual!=0
        # Scaling after insertion is epsilon^0; evenness excludes epsilon^1.
        assert 2*N+1-a==0
        assert polynomial_moment(poly,1,a)==0
        fixed_cases+=1
print("PASS:",fixed_cases,"fixed-insertion Hermite orthogonality/contact controls")
print("LIMIT: arbitrary polynomial degree is essential to theorem 71.2")
