#!/usr/bin/env python3
"""Read-only browser attestation of the actual deployed Erdős #7 MkDocs page.

This does NOT accept the manuscript, count reviewed coverage, certify a theorem,
or change publication permissions. It records whether visible math rendered.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PUBLIC = "https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0007/"


def verify(browser, url: str = PUBLIC) -> dict:
    page = browser.new_page(viewport={"width": 1280, "height": 850},
                            device_scale_factor=1)
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    response = page.goto(url, wait_until="domcontentloaded", timeout=45000)
    if response is None or response.status != 200:
        raise RuntimeError(f"public page GET failed: status={response.status if response else None}")
    page.locator("main").wait_for(timeout=15000)
    page.wait_for_function(
        """() => window.MathJax && window.MathJax.startup
                  && document.querySelectorAll('.arithmatex mjx-container').length >= 7""",
        timeout=55000,
    )
    # Wait for MathJax processing to settle after the CHTML nodes appear.
    page.evaluate("async () => { await window.MathJax.startup.promise; }")
    observed = page.evaluate("""() => {
      const main = document.querySelector('main');
      const blocks = Array.from(main.querySelectorAll('.arithmatex'));
      const rendered = Array.from(main.querySelectorAll('.arithmatex mjx-container'));
      const prose = main.innerText;
      const missingAlt = main.querySelectorAll('img:not([alt])').length;
      const mathJS = Array.from(document.querySelectorAll('script[src]'))
        .some(s => /mathjax.*tex-mml-chtml|tex-mml-chtml/.test(s.src));
      return {
        title: document.title,
        draft: prose.includes('UNACCEPTED DRAFT'),
        provenance: prose.includes('Erdős Problem #7'),
        theorem: prose.includes('Theorem 1.4'),
        source: prose.includes('Balister'),
        covered: prose.includes('57 covered and 48 uncovered'),
        notCertified: prose.includes('NOT received separate GCL editorial acceptance'),
        mathInputs: blocks.length,
        mathOutputs: rendered.length,
        mathLoader: mathJS,
        missingAlt
      };
    }""")
    checks = {
        "draft_warning": observed["draft"] and observed["notCertified"],
        "problem_identity": observed["provenance"],
        "theorem_source": observed["theorem"] and observed["source"],
        "finite_example": observed["covered"],
        "mathjax_loaded": observed["mathLoader"],
        "mathjax_rendered": observed["mathOutputs"] >= 7
                            and observed["mathOutputs"] == observed["mathInputs"],
        "image_alt": observed["missingAlt"] == 0,
        "no_page_script_errors": not errors,
    }
    if not all(checks.values()):
        raise RuntimeError("public HTML failed guarded readback: " +
                           json.dumps({"checks": checks, "observed": observed, "js_errors": errors}))
    # Capture visible screenshot of at least one actual mathematical equation.
    first = page.locator(".arithmatex mjx-container").first
    first.screenshot(path="readback/first-rendered-math.png", timeout=20000)
    page.screenshot(path="readback/page-viewport.png", full_page=False)
    html_bytes = page.content().encode("utf-8")
    page.close()
    return {
        "record_type": "ERDOS_COMPENDIUM_PUBLIC_HTML_READBACK/1",
        "public_url": url,
        "status": "PASS",
        "checks": checks,
        "observed": observed,
        "dom_sha256": hashlib.sha256(html_bytes).hexdigest(),
        "identity_scope": "deployed_browser_dom_not_deep_theorem_proof",
        "editorial_accepted": False,
        "mathematical_certified": False,
    }


def main() -> None:
    args = argparse.ArgumentParser()
    args.add_argument("--url", default=PUBLIC)
    options = args.parse_args()
    if options.url != PUBLIC:
        raise SystemExit("Refusing unbound public URL")
    Path("readback").mkdir(exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        result = verify(browser)
        browser.close()
    Path("readback/readback.json").write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("ERDOS_COMPENDIUM_PUBLIC_HTML_READBACK/1", json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
