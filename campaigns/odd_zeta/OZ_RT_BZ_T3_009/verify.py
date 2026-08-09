#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "OZ_RT_BZ_T3_002" / "target.py"
LOCK = HERE / "RECURRENCE_LOCK.json"
BASELINE = HERE / "BASELINE_RESULT.json"

spec = importlib.util.spec_from_file_location("t3_002_target_independent_for_t3_009", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected T3 target")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)


def a0(n): return 41218*n**3 + 198849*n**2 + 320790*n + 173057

def B8(n):
    return (3874492*n**8 + 59373972*n**7 + 394148190*n**6 + 1481084196*n**5
            + 3447878810*n**4 + 5095855458*n**3 + 4673546679*n**2
            + 2433871008*n + 551502039)

def B9(n):
    return (48802112*n**9 + 967468896*n**8 + 8488000862*n**7 + 43246197636*n**6
            + 140983768422*n**5 + 304912330849*n**4 + 437406946975*n**3
            + 401272692378*n**2 + 213593890911*n + 50257929339)

def cs(n):
    return ((n+1)**5*(n+2)*a0(n+1), -2*(n+2)*B8(n), -2*B9(n), 2*(n+3)**5*(2*n+5)*a0(n))

def p5(n):
    return sum((Q(t.T(n,k,l))*t.w5sym(n,k,l) for k in range(n+1) for l in range(n+1)), Q(0))

def w(n):
    return sum((Q(t.T(n,k,l))*t.W1(n,k,l) for k in range(n+1) for l in range(n+1)), Q(0))

def d(n): return w(n) + 2*p5(n)

def R(f,n): return sum((Q(c)*f(n+j) for j,c in enumerate(cs(n))), Q(0))


def main() -> int:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    if lock["order"] != 3 or lock["normalization_drift_allowed"]:
        raise AssertionError("operator lock drift")
    if lock["source"]["commit"] != "968477ed7e406df6542f8da6fbe1cd6ca7273c47":
        raise AssertionError("source pin drift")
    if not all(x > 0 for x in (41218,198849,320790,173057)):
        raise AssertionError("a0 coefficient positivity lost")
    for n in range(7):
        row = baseline["finite_component_baseline"][n]
        vals = (p5(n), w(n), d(n))
        exp = tuple(Q(*row[key]) for key in ("P5","W","D"))
        if vals != exp:
            raise AssertionError(f"source-normalized finite baseline drift at n={n}")
    if p5(1) != Q(87,4) or w(1) != Q(-87,2):
        raise AssertionError("nonvacuity witness drift")
    for n in range(4):
        if R(p5,n) != 0 or R(w,n) != 0 or R(d,n) != 0:
            raise AssertionError(f"finite operator residual drift at n={n}")
    for n in range(25):
        if cs(n)[3] <= 0:
            raise AssertionError("forward coefficient positivity failure")
    if baseline["proof_effect"] != "NONE" or baseline["promotion_effect"] != "NONE":
        raise AssertionError("finite evidence promoted")
    print("T3-009 independent locked-operator finite baseline replay: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
