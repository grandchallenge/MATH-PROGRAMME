# Erdős #41: conditional extraction of disjoint populated lag families

**Boundary:** This is a theorem *conditional on persistent positive B3 lower density*. It neither constructs a positive-density infinite B3 set nor proves the conjecture. It shows that a future overlap argument cannot require positive overlap for **every** densely populated selection of geometric scales.

## Finite spectral separation

A B3 set has unique unordered sums of three elements, repetitions allowed. Let X_1,...,X_k be nonempty ordered, disjoint inner blocks and Y a common outer block, all subsets of one B3 set, with every X_i<Y. Put $P_i=\{a+b:a,b\in X_i\}$ (unordered positive pairs including diagonals), and

$$
f_i(d)=\#\{(p,z)\in P_i\times Y:p-2z=d\}.
$$

**Theorem A.** If every gap between consecutive inner blocks is larger than $\operatorname{diam}Y$, then $f_i$ and $f_j$ have disjoint lag supports for every $i\ne j$. In addition,

$$
\boxed{|\operatorname{supp}f_i|\ge |X_i||Y|.}\tag{A}
$$

**Proof.** Every lag of family i belongs to the interval

$$
I_i=[2\min X_i-2\max Y,\ 2\max X_i-2\min Y].
$$

Adjacent intervals are separated by
$2(\min X_{i+1}-\max X_i-\operatorname{diam}Y)>0$. Therefore the actual occupied lag sets are disjoint. This first conclusion needs no B3 assumption.

The family $X_iX_i|Y$ has $|X_i|^2|Y|$ *weighted* representations, assigning weight 2 to off-diagonal unordered positive pairs and 1 to diagonal pairs. All its lags are nonzero since $X_i<Y$. B3 positive-pair matching bounds the weight at any fixed nonzero lag by $|X_i|$. Therefore at least $|X_i||Y|$ distinct integer lags are occupied. This proves (A) while accounting for repeated representations.

## Persistent-density extraction

Suppose, hypothetically, an infinite B3 set A satisfies $A(t)\ge c t^{1/3}$ for all sufficiently large t, with $0<c\le1$. Finite three-sum counting gives $A(t)<3t^{1/3}$. Define

$$
R=(6/c)^3\ge216.
$$

For an integer $k\ge2$ and sufficiently large N, choose inner geometric shells

$$
X_j=A\cap(N/R^{2j+1},N/R^{2j}],\qquad 1\le j\le k.
$$

Each is populated, with

$$
\boxed{n_j=|X_j|\ge {c\over2R^{2j/3}}N^{1/3}.}\tag{B}
$$

Indeed, subtract the finite upper bound at $N/R^{2j+1}$ from the density lower bound at $N/R^{2j}$, and use $3R^{-1/3}=c/2$. Adjacent shells are separated in position by more than $\gamma_kN$, where

$$
\gamma_k=(R-1)R^{-2k}.
$$

Also $W=A\cap(N/R,N]$ has at least $(c/2)N^{1/3}$ members. Divide $(N/R,N]$ into

$$
B_k=\left\lceil 2/\gamma_k\right\rceil
$$

equal subintervals. Some subinterval contains a set $Y\subseteq W$ with

$$
\boxed{|Y|\ge {c\over2B_k}N^{1/3},
\qquad \operatorname{diam}Y\le N/B_k\le\gamma_kN/2.}\tag{C}
$$

Theorem A applies: all inner supports are pairwise disjoint, despite each containing at least

$$
\boxed{|\operatorname{supp}f_j|
\ge{c^2\over4B_kR^{2j/3}}N^{2/3}.}\tag{D}
$$

**Theorem B.** Under the hypothetical persistent-density assumption, for *every fixed* number of scales k, and all sufficiently large N, there are k populated inner shells with a populated outer block Y, each producing $\gg_{c,k}N^{2/3}$ distinct actual lags, yet **all pairwise cross-family overlap energies vanish exactly**.

## Logarithmically many scales

The constants can be made uniform as k grows. Let

$$
k(N)=\left\lfloor{\log_R N\over12}\right\rfloor.
$$

For sufficiently large N, $k(N)\ge2$, $R^{2k(N)}\le N^{1/6}$, and the smallest lower endpoint $N/R^{2k(N)+1}\ge N^{5/6}/R\to\infty$. Thus the density hypothesis applies simultaneously to all shell endpoints. Moreover,

$$
B_{k(N)}=\left\lceil{2R^{2k(N)}\over R-1}\right\rceil
\le2N^{1/6}
$$

for $R\ge216$ and $N\ge1$. Consequently for every $j\le k(N)$,

$$
|X_j|\ge(c/2)N^{5/18},\qquad
|Y|\ge(c/4)N^{1/6},
$$

$$
\boxed{|\operatorname{supp}f_j|\ge(c^2/8)N^{4/9},
\quad \operatorname{supp}f_i\cap\operatorname{supp}f_j=\varnothing\ (i\ne j).}\tag{E}
$$

**Theorem C.** Under hypothetical persistent positive B3 density, for every sufficiently large N one can select $k(N)\asymp_c\log N$ populated geometric inner blocks and a single outer block, such that all their centered-lag spectra are **pairwise disjoint** while every spectrum occupies at least $(c^2/8)N^{4/9}$ distinct integer positions.

This is a necessary conditional extraction property, **not an infinite B3 counterexample**. It does not contradict the possibility of *some other*, more comprehensive selection of blocks forcing overlap. In fact it rules out an overly strong proof strategy requiring overlap for every populated choice of geometric scales.

## Genuine finite-B3 test and remaining obligation

The previously validated 29-element B3 sequence contains

$$
X=\{1,2,5,14\},\quad Z=\{19144,24546,28974\},
\quad Y=\{37769,45864,50877\}.
$$

Here $\min Z-\max X=19130>13108=\operatorname{diam}Y$. The two actual centered-lag supports have respectively **30** and **18** distinct positions with **zero overlap** (Theorem A guarantees only 12 and 9).

The next obligation is **not** an overlap theorem for arbitrary selected families. It must control an essentially complete collection of all mixed-color pair sums and all center positions, or another selection-invariant correlation that cannot be made zero by narrowing Y. It must account for representation multiplicities and avoid summing the same cut-crossing representations more than once. No density contradiction, MATHCERT certification, novelty priority or resolution of Erdős #41 is claimed.