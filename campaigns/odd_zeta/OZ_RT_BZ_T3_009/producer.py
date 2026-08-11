#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "OZ_RT_BZ_T3_002" / "target.py"
OUT = HERE / "BASELINE_RESULT.json"

spec = importlib.util.spec_from_file_location("t3_002_target_for_t3_009", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected T3 target")
target = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target)


def a0(n: int) -> int:
    return 41218*n**3 + 198849*n**2 + 320790*n + 173057


def B8(n: int) -> int:
    return (3874492*n**8 + 59373972*n**7 + 394148190*n**6 + 1481084196*n**5
            + 3447878810*n**4 + 5095855458*n**3 + 4673546679*n**2
            + 2433871008*n + 551502039)


def B9(n: int) -> int:
    return (48802112*n**9 + 967468896*n**8 + 8488000862*n**7 + 43246197636*n**6
            + 140983768422*n**5 + 304912330849*n**4 + 437406946975*n**3
            + 401272692378*n**2 + 213593890911*n + 50257929339)


def coeffs(n: int) -> tuple[int, int, int, int]:
    return (
        (n+1)**5*(n+2)*a0(n+1),
        -2*(n+2)*B8(n),
        -2*B9(n),
        2*(n+3)**5*(2*n+5)*a0(n),
    )


def P5(n: int) -> Q:
    return sum((Q(target.T(n,k,l))*target.w5sym(n,k,l)
                for k in range(n+1) for l in range(n+1)), Q(0))


def W(n: int) -> Q:
    return sum((Q(target.T(n,k,l))*target.W1(n,k,l)
                for k in range(n+1) for l in range(n+1)), Q(0))


def D(n: int) -> Q:
    return W(n) + 2*P5(n)


def residual(seq, n: int) -> Q:
    return sum((Q(c)*seq(n+j) for j, c in enumerate(coeffs(n))), Q(0))


def pair(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def compute() -> dict:
    vals = []
    for n in range(7):
        vals.append({"n": n, "P5": pair(P5(n)), "W": pair(W(n)), "D": pair(D(n))})
    res = []
    for n in range(4):
        res.append({
            "n": n,
            "L_P5": pair(residual(P5,n)),
            "L_W": pair(residual(W,n)),
            "L_D": pair(residual(D,n)),
        })
    return {"finite_component_baseline": vals, "finite_residual_baseline": res}


def main() -> int:
    expected = json.loads(OUT.read_text(encoding="utf-8"))
    got = compute()
    if got["finite_component_baseline"] != expected["finite_component_baseline"]:
        raise AssertionError("finite component baseline drift")
    if got["finite_residual_baseline"] != expected["finite_residual_baseline"]:
        raise AssertionError("finite recurrence residual drift")
    if P5(1) == 0 or W(1) == 0:
        raise AssertionError("component route became vacuous")
    if any(D(n) != 0 for n in range(7)):
        raise AssertionError("protected finite T3 baseline drift")
    if any(residual(P5,n) != 0 or residual(W,n) != 0 for n in range(4)):
        raise AssertionError("locked finite component recurrence baseline drift")
    if any(c <= 0 for c in (a0(0), a0(1), a0(10))):
        raise AssertionError("a0 positivity sentinel drift")
    print(json.dumps(got, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
