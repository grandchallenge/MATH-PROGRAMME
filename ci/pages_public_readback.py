#!/usr/bin/env python3
"""Read back served GitHub Pages bytes against the exact validated build artifact.

This check does not confer mathematical, editorial, or MATHCERT authority.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import time
import urllib.parse
import urllib.request


def examine(body: bytes, *, expected_sha256: str, url: str, actual_url: str,
            status: int, content_type: str) -> dict[str, object]:
    """Fail when the served HTML is not the validated source byte-for-byte."""
    expected = expected_sha256.lower()
    if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
        raise ValueError("invalid expected SHA-256")
    original = urllib.parse.urlsplit(url)
    redirect = urllib.parse.urlsplit(actual_url)
    if original.scheme != "https" or redirect.scheme != "https" or original.netloc != redirect.netloc:
        raise ValueError(f"redirected away from authorized HTTPS Pages origin: {actual_url}")
    if status != 200:
        raise ValueError(f"served response status {status}, expected 200")
    if not content_type.lower().startswith("text/html"):
        raise ValueError(f"served response not text/html: {content_type!r}")
    observed = hashlib.sha256(body).hexdigest()
    if observed != expected:
        raise ValueError(f"served HTML digest mismatch: observed {observed}, expected {expected}")
    return {
        "html_sha256": observed,
        "bytes": len(body),
        "qualified_editorial_badge": "Reviewed explanatory article — evidence qualified.".encode() in body,
        "legacy_badge_present": b"Legacy authored exemplar" in body,
        "arithmatex_present": b"arithmatex" in body,
        "mathjax_configuration_present": b"mkdocs-math.js" in body,
    }


def run(*, url: str, expected_sha256: str, source_sha: str,
        attempts: int = 15, interval: float = 8, timeout: float = 10,
        opener=urllib.request.urlopen, sleep=time.sleep) -> dict[str, object]:
    if not (1 <= attempts <= 30) or not (0 <= interval <= 30) or not (1 <= timeout <= 30):
        raise ValueError("out-of-policy retry bounds")
    if len(source_sha) != 40 or any(c not in "0123456789abcdef" for c in source_sha.lower()):
        raise ValueError("invalid source commit SHA")
    last_failure = ""
    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(
            url, headers={
                "User-Agent": "GCL-Pages-Readback/1",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
        )
        try:
            with opener(request, timeout=timeout) as response:
                result = examine(
                    response.read(), expected_sha256=expected_sha256,
                    url=url, actual_url=response.geturl(), status=response.status,
                    content_type=response.headers.get("Content-Type", ""),
                )
            print("GCL_PAGES_PUBLIC_READBACK/1 "
                  f"source_sha={source_sha} url={url} "
                  f"html_sha256={result['html_sha256']} bytes={result['bytes']} "
                  f"qualified_badge={result['qualified_editorial_badge']} "
                  f"legacy_badge={result['legacy_badge_present']} "
                  f"arithmatex={result['arithmatex_present']} "
                  f"mathjax_config={result['mathjax_configuration_present']} "
                  f"attempt={attempt}", flush=True)
            return result
        except (ValueError, OSError) as exc:
            last_failure = str(exc)
            print(f"GCL_PAGES_PUBLIC_READBACK_RETRY/1 attempt={attempt}/{attempts} "
                  f"reason={last_failure}", file=sys.stderr, flush=True)
            if attempt < attempts:
                sleep(interval)
    raise RuntimeError(
        f"SERVED_HTML_NOT_EQUAL_TO_VALIDATED_ARTIFACT after {attempts} attempts: {last_failure}"
    )


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", required=True)
    p.add_argument("--expected-sha256", required=True)
    p.add_argument("--source-sha", required=True)
    p.add_argument("--attempts", type=int, default=15)
    p.add_argument("--interval", type=float, default=8)
    p.add_argument("--timeout", type=float, default=10)
    args = p.parse_args()
    run(url=args.url, expected_sha256=args.expected_sha256, source_sha=args.source_sha,
        attempts=args.attempts, interval=args.interval, timeout=args.timeout)


if __name__ == "__main__":
    main()
