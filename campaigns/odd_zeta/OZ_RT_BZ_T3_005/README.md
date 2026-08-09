# OZ-RT-BZ-T3-005

Operation: `MIRROR_TRIANGULAR_AUXILIARY_MODULE_THEN_ONE_BODY_JET_COUPLING`.

This fixture is the governed successor to `OZ-RT-BZ-T3-004`. It closes two mathematical interface gaps without promoting T3.

## Stage A — mirror triangular auxiliary module

The mirror orientation retains an explicit finite auxiliary coordinate `s`:

- `U(l,k,r,m)`: `T(n,k,l) * s^(-r) * Q(s+k,0;eta)`;
- `ES(l,r,m)`: `T(n,k,l) * s^(-r) * Q(s,0;eta)`.

The common order-2 search shifts `l` and uses exact `k`/`s` divergences. The finite-flux basis contains the edge factors `k*(n+1-k)` and `(s-1)*(l+1-s)`. The retained degree ladder is `0..4`, with eta degree at most one and modular rank certification at `p=1000003`.

The strongest stage is full column rank: 3,540 equations, 1,210 unknowns, rank 1,210, nullity zero. Thus the exact bounded mirror class

`PARAMETER_DEPENDENT_ORDER2_LSIDE_U_ES_SAUX_ETADEG_LE_1_POLYDEG_LE_4`

is exhausted. This is not a refutation of T3.

## Stage B — linear one-body raw jet

To avoid applying nonlinear logarithmic cumulants to a telescoping identity, the fixture uses the power-sum isolator

`P_r(L,o;z) = prod_{i=1}^L (1 - (-z/(o+i))^r)`.

Its first nonzero raw derivative is

`d^r/dz^r P_r(L,o;z)|_0 = (-1)^(r+1) r! (H_(o+L)^(r) - H_o^(r))`.

Raw mixed derivatives are linear operators. Products and quotients of these isolators therefore encode the one-body harmonic letters needed by the locked T3 summand without using a nonlinear cumulant transform as a proof-producing step.

The generated coefficient map expands the locked `W1 + 2*w5_sym` target into 198 exact weight-five monomials. Of these, 158 are one-body-only and 40 contain exactly one nested `U/ES` atom. No weight-five monomial contains more than one nested atom. The map was checked against direct exact evaluation on 135 `(n,k,l)` samples, with 3,526 raw-jet atom checks.

## Stage C — orientation coupling

The extraction map records both nested orientations: protected k-side `U(k,l)/ES(k)` from T3-004 and mirror l-side `U(l,k)/ES(l)` from Stage A.

The coefficient map for the locked weight-five summand is complete, but there is not yet a common parameter-dependent parent telescoper for that full raw-jet module and therefore no differentiated finite-boundary T3 certificate.

Terminal disposition remains `OPEN_WITH_CHARACTERIZED_BLOCKER`, with `proof_effect: NONE` and `promotion_effect: NONE`.

Next route: `COUPLED_WEIGHT5_RAW_JET_ORDER2_SEARCH_001`.
