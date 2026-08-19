from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "docs" / "operator" / "prvsr" / "app.js"


class PRVisualStatusOperatorLinkTests(unittest.TestCase):
    def test_browser_url_constructor_is_not_shadowed(self) -> None:
        source = APP.read_text(encoding="utf-8")

        self.assertIsNone(
            re.search(r"\bconst\s+URL\s*=", source),
            "dashboard code must not shadow the browser URL constructor",
        )
        self.assertIn("const MANIFEST_URL", source)
        self.assertIn("new window.URL(", source)
        self.assertIn("fetch(MANIFEST_URL", source)

    def test_link_sanitizer_keeps_explicit_host_allowlist(self) -> None:
        source = APP.read_text(encoding="utf-8")

        self.assertIn('"github.com"', source)
        self.assertIn('"raw.githubusercontent.com"', source)
        self.assertIn('u.protocol === "https:"', source)
        self.assertIn('ALLOWED_HOSTS.has(u.hostname)', source)


if __name__ == "__main__":
    unittest.main()
