# OZ-RT-BZ-T3-004

## Purpose

This packet executes the first parameter-dependent successor to T3-003. It keeps the normalized-Pochhammer deformation parameter `eta` and the auxiliary finite `t` coordinate inside an order-2 creative-telescoping system. It does not return to the exhausted undeformed-parent degree ladder.

The locked target remains

`sum_{k=0}^n sum_{l=0}^n T(n,k,l) * (W1(k,l)+2*w5_sym(n,k,l)) = 0`.

T3 is neither proved nor refuted.

## Auxiliary parents

For `r in {1,2}`, the retained parents are

`G_U = T(n,k,l) * t^(-r) * Q(t+l,0;eta)`

and

`G_ES = T(n,k,l) * t^(-r) * Q(t,0;eta)`,

where

`Q(length,offset;eta) = product_{i=1}^length (offset+i+eta)/(offset+i)`.

Logarithmic cumulants of `Q` at `eta=0` reconstruct `H_(t+l)^(m)` and `H_t^(m)` termwise. Summing over `t` therefore reconstructs the `U` and `ES` atoms used by the locked T3 weight.

This is a structural lift statement. Logarithmic cumulant extraction is nonlinear; a future positive parent identity would still need an explicit, independently verified mixed-jet differential-extraction bridge before it could have any T3 proof effect.

## Search class

The first fixture searches a common order-2 external-`k` telescoper across `U_R1`, `U_R2`, `ES_R1`, and `ES_R2`:

`sum_{j=0}^2 a_j(n,k,eta) G(n,k+j,l,t;eta) = Delta_l(G q_l) + Delta_t(G q_t)`.

The `a_j` are shared; the two certificates are component-specific. Parameter degree is at most one. Polynomial degree follows the declared ladder `d=0..4`.

Finite-edge cancellation is built into the numerator bases:

- `q_l` carries `l*(n+1-l)`;
- `q_t` carries `(t-1)*(k+1-t)`.

Certificate denominators are derived from the exact parent shift ratios.

## Exact result

| degree | equations | unknowns | rank | nullity |
|---:|---:|---:|---:|---:|
| 0 | 852 | 22 | 22 | 0 |
| 1 | 852 | 98 | 98 | 0 |
| 2 | 852 | 276 | 276 | 0 |
| 3 | 1860 | 620 | 620 | 0 |
| 4 | 3540 | 1210 | 1210 | 0 |

At degree 4, each component-specific certificate block has rank 280 and the induced shared-telescoper quotient system has rank 90. Thus the full 1210-column system has full rank.

All matrix entries are exact rationals. Their denominators are checked nonzero modulo `p=1000003`. Full rank modulo that prime exhibits a nonzero maximal minor; the corresponding rational minor is nonzero. The negative result is therefore exact over `Q`, not heuristic modular evidence.

Newly exhausted bounded class:

`PARAMETER_DEPENDENT_ORDER2_KSIDE_U_ES_TAUX_ETADEG_LE_1_POLYDEG_LE_4`.

## Coverage boundary

This fixture covers only the `k`-side rectangular auxiliary module. It does not yet cover:

- the mirror `U(l,k)/ES(l)` triangular-domain module;
- the complete one-body mixed-derivative jet module;
- the full weight-five differential extraction of the locked T3 summand.

Accordingly the result is not a refutation of T3 and has no theorem or promotion effect.

## Disposition

`OPEN_WITH_CHARACTERIZED_BLOCKER`

`proof_effect: NONE`

`promotion_effect: NONE`

Next distinct route:

`MIRROR_TRIANGULAR_AUXILIARY_MODULE_THEN_ONE_BODY_JET_COUPLING`.
