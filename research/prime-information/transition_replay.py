"""TCU-001 finite tests: independently enumerate smooth integers and leave-one-prime influence.
Standard-library only; finite verification does NOT prove a transition asymptotic.
Run: python research/prime-information/transition_replay.py
"""
import bisect
import csv
import math
from collections import Counter
from itertools import product


def primes_up_to(y):
    return [p for p in range(2, y + 1) if all(p % q for q in range(2, math.isqrt(p) + 1))]


def smooth_values(x, primes):
    values = [1]
    for p in primes:
        nxt = []
        power = 1
        while power <= x:
            nxt.extend(a * power for a in values if a * power <= x)
            power *= p
        values = nxt
    return sorted(values)


def saddle(t, primes):
    def mean(s):
        return sum(math.log(p) / math.expm1(s * math.log(p)) for p in primes)
    lo, hi = 0.0, 1.0
    while mean(hi) > t:
        hi *= 2
    for _ in range(90):
        s = (lo + hi) / 2
        if mean(s) > t:
            lo = s
        else:
            hi = s
    return (lo + hi) / 2


def experiment(x, y):
    primes = primes_up_to(y)
    values = smooth_values(x, primes)
    n = len(values)
    t = math.log(x)
    s = saddle(t, primes)
    logz = -sum(math.log(-math.expm1(-s * math.log(p))) for p in primes)
    sigma2 = sum(math.log(p) ** 2 * math.exp(s * math.log(p)) /
                 math.expm1(s * math.log(p)) ** 2 for p in primes)
    meanlog = sum(math.log(a) for a in values) / n
    totalcorr, kldiv, chisq = -math.log(n), 0.0, 0.0
    max_local_residual = 0.0
    for p in primes:
        hist = Counter()
        for a in values:
            j = 0
            while a % p == 0:
                a //= p
                j += 1
            hist[j] += 1
        m = max(hist)
        marg = {j: v / n for j, v in hist.items()}
        totalcorr -= sum(v * math.log(v) for v in marg.values())
        r = p ** (-s)
        zminus = math.exp(logz) * (1 - r)
        excluded = smooth_values(x, [q for q in primes if q != p])
        local_d = 0.0
        local_chi = r ** (m + 1)
        for j in range(m + 1):
            qj = (1 - r) * (r ** j)
            pj = marg.get(j, 0.0)
            cnt = bisect.bisect_right(excluded, x // p ** j)
            fminus = s * math.exp(-s * (t - j * math.log(p))) * cnt / zminus
            fe = s * math.exp(-s * t) * n / math.exp(logz)
            local_p = qj * fminus / fe
            max_local_residual = max(max_local_residual, abs(local_p - pj))
            if pj:
                local_d += pj * math.log(pj / qj)
            local_chi += ((pj - qj) ** 2) / qj
        kldiv += local_d
        chisq += local_chi
    dglobal = logz + s * meanlog - math.log(n)
    residual = dglobal - kldiv - totalcorr
    prediction = math.log(s * math.sqrt(2 * math.pi * sigma2)) - 1
    assert abs(residual) < 2e-9, residual
    assert max_local_residual < 2e-9, max_local_residual
    assert kldiv <= chisq + 1e-10
    return dict(X=x, y=y, u=t / math.log(y), k=len(primes),
                smooth_count=n, alpha=s, alpha_sigma=s*math.sqrt(sigma2),
                T=totalcorr, alpha_slack=s * (t - meanlog), K=kldiv,
                K_chi_upper=chisq, predicted_T=prediction,
                actual_minus_predicted=totalcorr-prediction,
                exact_KL_residual=residual,
                leave_one_prime_max_residual=max_local_residual)


def main():
    cases = [(100, 2), (1000, 5), (10000, 7), (10000, 17),
             (100000, 13), (100000, 53), (1000000, 29)]
    rows = [experiment(x, y) for x, y in cases]
    with open("transition_replay_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(f"X={row['X']:>7}, y={row['y']:>2}, T={row['T']:.6f}, "
              f"alpha*slack={row['alpha_slack']:.6f}, K={row['K']:.6f}, "
              f"bridge_error={row['actual_minus_predicted']:+.6f}")
    print("PASS: exact marginal likelihood, KL decomposition and chi-square upper bound")


if __name__ == "__main__":
    main()
