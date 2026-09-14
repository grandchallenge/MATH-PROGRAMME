from __future__ import annotations

import hashlib
import re
import urllib.request

SOURCE_REPOSITORY = "rain-1/-odd-zeta-values-moremath"
SOURCE_COMMIT = "6cc0bf07137815ceeef0d9f340559f85352391e5"
SOURCE_BLOBS = {
    "work/z5la/o_scan.py": "bc6e9a59a48b15eddbab8e80ad4e5063972582d2",
    "work/z5la/o_scan_E1.log": "9085d23798074e9e86bc1c41faaf17a7e4b1386f",
    "work/z5la/o_zero.py": "2bfa58cb573b0d40646e85bdbed682d8344b594a",
    "work/z5la/o_zero1.log": "14dfe8cff588867ecbd478993dc318e78be8b232",
    "work/z5la/o_csweep.py": "b506b9d6fbd405e6ac36fc790aa354196df20938",
    "work/z5la/o_final.py": "e51582d64e664714524ccf566178c94fc30b202a",
    "work/z5la/o_final.log": "fdb111957380d1be0876982f706980eb074fc9ab",
    "work/z5la/o_zero3.log": "d7ee036184121def642470768a9c3a1a46c43fa4",
}


def _blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _fetch(path: str) -> bytes:
    url = f"https://raw.githubusercontent.com/{SOURCE_REPOSITORY}/{SOURCE_COMMIT}/{path}"
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    got = _blob_sha1(data)
    expected = SOURCE_BLOBS[path]
    if got != expected:
        raise AssertionError(f"source reconciliation lock drift for {path}: {got} != {expected}")
    return data


def verify() -> dict:
    locked = {path: _fetch(path).decode("utf-8") for path in SOURCE_BLOBS}

    scan = locked["work/z5la/o_scan.py"]
    if "force_k=0, force_l=0" not in scan:
        raise AssertionError("o_scan no longer declares the unforced exploratory ansatz")

    scan_log = locked["work/z5la/o_scan_E1.log"]
    slack18 = scan_log.split("===== E1 slack=18 =====", 1)
    if len(slack18) != 2:
        raise AssertionError("E1 slack-18 scan section missing")
    slack18 = slack18[1].split("===== E1 slack=26 =====", 1)[0]
    order7 = next(
        (line for line in slack18.splitlines() if "m= 7 E1 deg=(28,28) nc=1682" in line),
        None,
    )
    if order7 is None:
        raise AssertionError("unforced order-7 nc=1682 scan witness missing")
    if "rk1106" not in slack18:
        raise AssertionError("unforced order-7 rank-1106 scan witness missing")

    zero = locked["work/z5la/o_zero.py"]
    if zero.count("force_k=0, force_l=0") < 2:
        raise AssertionError("o_zero rank-producing route is no longer unforced")
    zero1 = locked["work/z5la/o_zero1.log"]
    rank_match = re.search(r"seven standalone blocks: rank=(\d+) nbad=(\d+)", zero1)
    if rank_match is None or tuple(map(int, rank_match.groups())) != (1106, 0):
        raise AssertionError("unforced o_zero rank witness drift")

    csweep = locked["work/z5la/o_csweep.py"]
    if "FORCE = (1, 1)" not in csweep:
        raise AssertionError("cofactor sweep no longer uses the boundary-forced ansatz")
    if "fastlin.solve(Mm[:nfit]" not in csweep:
        raise AssertionError("cofactor sweep scalar solve path drift")

    final_py = locked["work/z5la/o_final.py"]
    if "force=(1, 1)" not in final_py:
        raise AssertionError("end-to-end certificate route no longer uses boundary forcing")
    final_log = locked["work/z5la/o_final.log"]
    if final_log.count("7 standalone (nc=1624") < 4:
        raise AssertionError("boundary-forced nc=1624 end-to-end witnesses drift")
    if final_log.count("ALL SATISFIED") < 4 or final_log.count("(B-bot)") < 4:
        raise AssertionError("end-to-end modular fresh-point/boundary witnesses drift")

    zero3 = locked["work/z5la/o_zero3.log"]
    if "--- () ansatz Z3 slack 16 ---" not in zero3:
        raise AssertionError("constant-block Z3 slack-16 witness missing")
    z3_section = zero3.split("--- () ansatz Z3 slack 16 ---", 1)[1].split(
        "--- () ansatz Z3 slack 24 ---", 1
    )[0]
    if "nbad=0 *** SOLVED ***" not in z3_section or "300 unused points: 0 violations" not in z3_section:
        raise AssertionError("constant-block Z3 modular solution witness drift")

    unforced_columns = 1682
    unforced_rank = 1106
    boundary_forced_columns = 1624
    boundary_forced_reconstructed_rank = 1048
    if unforced_columns - unforced_rank != 576:
        raise AssertionError("unforced nullity arithmetic drift")
    if boundary_forced_columns - boundary_forced_reconstructed_rank != 576:
        raise AssertionError("boundary-forced nullity arithmetic drift")

    return {
        "source_commit": SOURCE_COMMIT,
        "source_locks_verified": True,
        "unforced_scan": {
            "force": [0, 0],
            "columns": unforced_columns,
            "rank": unforced_rank,
            "kernel_dimension": 576,
            "rank_witness_route": "o_zero.py + o_zero1.log",
        },
        "boundary_forced_certificate": {
            "force": [1, 1],
            "columns": boundary_forced_columns,
            "reconstructed_rank": boundary_forced_reconstructed_rank,
            "kernel_dimension": 576,
            "source_forced_rank_recorded": False,
        },
        "cross_regime_518_rejected": True,
        "cross_regime_518_reason": "1624 boundary-forced columns minus 1106 unforced rank mixes distinct ansatz regimes",
        "constant_block_modular_candidate": {
            "ansatz": "Z3",
            "slack": 16,
            "solved": True,
            "fresh_points": 300,
            "fresh_violations": 0,
            "authority": "SOURCE_MODULAR_CANDIDATE_ONLY",
        },
    }
