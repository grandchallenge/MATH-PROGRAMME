# WP05 cancellation derivation

## Protected exact primitive

The independent MATHCERT C05 replay uses the exact edge list and constructs every oriented dual-edge increment as

[
delta_e=f(w_e),s_e,k_e,widetilde f(b_e),
]

where (w_e) is the white endpoint, (b_e) the black endpoint, (s_ein{pm1}) the Kasteleyn sign, and (k_e>0) the graph weight.

For an integer exponent vector (qinmathbb Z^{16}), define

[
D_q(delta)=prod_e delta_e^{q_e},qquad
K_q=prod_e (s_e k_e)^{q_e}.
]

Then, exactly,

[
D_q(delta)=K_q
prod_{w}f(w)^{sum_{e
i w}q_e}
prod_{b}widetilde f(b)^{sum_{e
i b}q_e}.
]

## Internal gauge lattice

Let (G) be the 8-by-16 unsigned incidence matrix restricted to the eight internal vertices. The internal-vertex weight gauge acts in logarithmic coordinates by

[
log kmapsto log k+G^	op h.
]

Therefore a weight monomial is gauge invariant exactly when

[
Gq=0.
]

Direct integer linear algebra gives

[
operatorname{rank}G=8,qquad
operatorname{rank}ker_{mathbb Z}G=8.
]

After multiplying the four white internal rows by (-1), (G) becomes the signed incidence matrix restricted to internal vertices. Hence the invariant lattice is a flow space with zero divergence at every internal vertex.

For the connected 14-vertex graph with 16 edges, the full closed-cycle rank is

[
16-14+1=3.
]

The remaining five invariant directions are boundary-to-boundary flows.

Thus the natural decomposition is

[
oxed{8=3 	ext{closed cycles}+5 	ext{boundary paths}.}
]

## Exact closed-cycle cancellation

If (q) is a closed-cycle flow, then it has zero divergence at every internal and boundary vertex. Every (f) and (widetilde f) exponent therefore vanishes. Consequently

[
oxed{D_q(delta)=K_q}
]

with no branch factor and no approximation.

The three retained fundamental cycles are:

[
C_1:
rac{delta_{F01|F02}delta_{F07|F04}}
{delta_{F01|F04}delta_{F07|F02}}
=
-rac{k_{F01|F02}k_{F07|F04}}
{k_{F01|F04}k_{F07|F02}}
=-rac67,
]

[
C_2:
rac{delta_{F03|F04}delta_{F05|F06}}
{delta_{F03|F06}delta_{F05|F04}}
=
-rac{k_{F03|F04}k_{F05|F06}}
{k_{F03|F06}k_{F05|F04}}
=-rac4{21},
]

and

[
C_3:
rac{delta_{F01|F02}delta_{F03|F04}delta_{F07|F08}}
{delta_{F01|F04}delta_{F07|F02}delta_{F03|F08}}
=
rac{k_{F01|F02}k_{F03|F04}k_{F07|F08}}
{k_{F01|F04}k_{F07|F02}k_{F03|F08}}
=rac{18}{175}.
]

The minus signs in (C_1,C_2) are the protected Kasteleyn signs, not discarded phases.

Because the pure closed-cycle lattice has rank three, no monomial cancellation argument using geometry increments alone can supply more than three independent quotient coordinates.

## Boundary-path obstruction

For a boundary-to-boundary flow (q), all internal factors still cancel, but endpoint boundary factors remain.

Write the one-based boundary factors as (eta_i), where the exact MATHCERT extension equations give

[
eta_1=widetildezeta_1,quad
eta_2=zeta_2,quad
eta_3=widetildezeta_3,quad
eta_4=-widetildezeta_4,quad
eta_5=-zeta_5,quad
eta_6=zeta_6.
]

Here

[
widetildezeta_i=rac{Delta_i}{zeta_i},
]

and the (zeta_i) are the branch-dependent boundary data from the algebraic witness.

Therefore every path invariant satisfies the exact identity

[
D_q(delta)
=
K_qprod_{i=1}^{6}eta_i^{q_{B_i}},
]

or equivalently

[
oxed{
K_q=
D_q(delta)Big/prod_ieta_i^{q_{B_i}}.
}
]

The five raw path products are consequently branch dependent. They become invariant only after the boundary calibration above.

## Quotient completeness with calibration

The five boundary paths together with the three cycles form a (mathbb Z)-basis of (ker_{mathbb Z}G). Their positive weight monomials (y) are related to the protected WP01 coordinates (x) by

[
log y=Alog x
]

with the integer matrix retained in `QUOTIENT_CHART.json`.

Its determinant is

[
det A=-1.
]

Hence the path+cycle basis is unimodularly equivalent to the WP01 chart: if all five boundary factors are available, the full eight-dimensional quotient is reconstructed exactly.

## What is and is not established

Established:

1. the internal gauge-invariant lattice has rank eight;
2. its natural graph decomposition is five boundary paths plus three cycles;
3. the three closed-cycle coordinates are exact geometry-only invariants;
4. all eight coordinates are exactly reconstructible from geometry increments **plus** the branch boundary factors;
5. the natural invariant basis and WP01 chart are related by an exact unimodular monomial transformation.

Not established:

- a geometry-only method for deriving the five branch boundary factors;
- a full geometry-only inverse (mathcal G	omathcal Q);
- any source-correspondence or physical claim.

This is therefore a partial reconstruction theorem, not a full reversal of WP04.
