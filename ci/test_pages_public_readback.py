#!/usr/bin/env python3
"""Hostile, deterministic tests for the served-Pages exact-byte gate."""
from __future__ import annotations

import hashlib
import unittest

from ci.pages_public_readback import examine, run


URL = "https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0001/"
BODY = ('<html><span class="arithmatex">$x$</span>'
        'Reviewed explanatory article — evidence qualified.'
        '<script src="../../../javascripts/mkdocs-math.js"></script></html>').encode()
HASH = hashlib.sha256(BODY).hexdigest()
HEAD = "a" * 40


class FakeResponse:
    status = 200
    headers = {"Content-Type": "text/html; charset=utf-8"}

    def __init__(self, payload=BODY, actual_url=URL):
        self.payload, self.actual_url = payload, actual_url

    def read(self):
        return self.payload

    def geturl(self):
        return self.actual_url

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class PagesReadbackTests(unittest.TestCase):
    def test_exact_html_acceptance_is_not_certification(self):
        result = examine(BODY, expected_sha256=HASH, url=URL, actual_url=URL,
                         status=200, content_type="text/html")
        self.assertTrue(result["qualified_editorial_badge"])
        self.assertTrue(result["arithmatex_present"])
        self.assertTrue(result["mathjax_configuration_present"])
        self.assertFalse(result["legacy_badge_present"])

    def test_changed_one_byte_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            examine(BODY+b"x", expected_sha256=HASH, url=URL, actual_url=URL,
                    status=200, content_type="text/html")

    def test_invalid_expected_digest_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid expected"):
            examine(BODY, expected_sha256="0"*63, url=URL, actual_url=URL,
                    status=200, content_type="text/html")

    def test_non_http_or_redirect_host_rejected(self):
        for actual in ("http://grandchallenge.github.io/evil", "https://example.org/"):
            with self.subTest(actual=actual), self.assertRaisesRegex(ValueError, "origin"):
                examine(BODY, expected_sha256=HASH, url=URL, actual_url=actual,
                        status=200, content_type="text/html")

    def test_not_html_rejected(self):
        with self.assertRaisesRegex(ValueError, "not text/html"):
            examine(BODY, expected_sha256=HASH, url=URL, actual_url=URL,
                    status=200, content_type="text/plain")

    def test_bad_status_rejected(self):
        with self.assertRaisesRegex(ValueError, "status"):
            examine(BODY, expected_sha256=HASH, url=URL, actual_url=URL,
                    status=404, content_type="text/html")

    def test_retry_then_success(self):
        calls, sleeps = [], []
        def opener(request, timeout):
            calls.append(timeout)
            return FakeResponse(BODY+b"X" if len(calls) == 1 else BODY)
        result = run(url=URL, expected_sha256=HASH, source_sha=HEAD,
                     attempts=3, interval=0, timeout=1, opener=opener,
                     sleep=lambda seconds: sleeps.append(seconds))
        self.assertEqual(result["html_sha256"], HASH)
        self.assertEqual(len(calls), 2)
        self.assertEqual(sleeps, [0])

    def test_bounded_exhaustion_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "SERVED_HTML_NOT_EQUAL"):
            run(url=URL, expected_sha256=HASH, source_sha=HEAD,
                attempts=2, interval=0, timeout=1,
                opener=lambda request, timeout: FakeResponse(BODY+b"BAD"),
                sleep=lambda _: None)

    def test_invalid_bounds_and_identity(self):
        with self.assertRaises(ValueError):
            run(url=URL, expected_sha256=HASH, source_sha=HEAD, attempts=31)
        with self.assertRaises(ValueError):
            run(url=URL, expected_sha256=HASH, source_sha="notasha", attempts=1)


if __name__ == "__main__":
    unittest.main()
