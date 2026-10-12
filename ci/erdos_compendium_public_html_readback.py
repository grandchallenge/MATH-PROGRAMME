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


def protected_editorial_state(problem_id: int = 7) -> bool:
    """Read protected editorial authority; never infer it from the live page."""
    from erdos_compendium import load_batch_admissions, manuscript

    admitted = load_batch_admissions().get(problem_id)
    if admitted is None:
        return False
    source = manuscript(problem_id)
    if source is None:
        raise RuntimeError("accepted record has no manuscript")
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    if digest != admitted["source_sha256"]:
        raise RuntimeError("stale editorial admission source hash")
    return True


def publication_state_matches(observed: dict, admitted: bool) -> bool:
    """Fail closed on wrong public classification in either lifecycle state."""
    if admitted:
        return observed["reviewed"] and not observed["draft"] and not observed["notCertified"]
    return observed["draft"] and observed["notCertified"] and not observed["reviewed"]


def verify(browser, url: str = PUBLIC) -> dict:
    admitted = protected_editorial_state()
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
        reviewed: prose.includes('Reviewed explanatory article — evidence qualified'),
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
        "publication_state": publication_state_matches(observed, admitted),
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
        "editorial_accepted": admitted,
        "mathematical_certified": False,
    }


def verify_github(browser, sha: str) -> dict:
    """Independently inspect GitHub's visible rich-rendered Markdown.

    GitHub can use SVG, MathML or CommonHTML outputs. Count only physically
    visible rendered math nodes, not any unprocessed TeX/source text.
    Save a bounded public-page diagnostic even if rendering fails.
    """
    import re
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise RuntimeError("missing exact protected manuscript SHA")
    url = ("https://github.com/grandchallenge/MATH-PROGRAMME/blob/" + sha +
           "/governance/erdos_compendium/editorial/0007.md")
    page = browser.new_page(viewport={"width": 1280, "height": 850})
    errors: list[str] = []
    page.on("pageerror", lambda err: errors.append(str(err)[:300]))
    response = page.goto(url, wait_until="domcontentloaded", timeout=45000)
    if response is None or response.status != 200:
        raise RuntimeError(f"GitHub Markdown GET failed: {response.status if response else None}")

    selectors = {
        "mathjax_chtml": "mjx-container",
        "mathjax_svg": "mjx-container[jax='SVG'] svg",
        "katex": ".katex",
        "native_mathml": "math",
        "github_math_svg": "[data-math-style] svg",
        "github_render_svg": ".js-render-target svg",
        "math_role": "[role='math']",
    }
    def snapshot() -> dict:
        return page.evaluate("""selectors => {
            const root = document.querySelector('.markdown-body');
            const visible = e => {
                const r = e.getBoundingClientRect();
                const style = getComputedStyle(e);
                return r.width > 2 && r.height > 2
                    && style.display !== 'none' && style.visibility !== 'hidden';
            };
            const counts = {};
            for (const [name, css] of Object.entries(selectors)) {
                counts[name] = root
                  ? Array.from(root.querySelectorAll(css)).filter(visible).length : 0;
            }
            const body = root?.innerText || '';
            return {
                url: location.href, title: document.title,
                rootFound: !!root,
                rootChars: body.length, textStart: body.slice(0, 800),
                markers: {
                    theorem: body.includes('Theorem 1.4'),
                    source: body.includes('Hough'),
                    example: body.includes('48 uncovered')
                },
                counts,
                unprocessedMath: root
                  ? (body.match(/\\$\\$|\\\\equiv|\\\\operatorname/g) || []).length : null,
            };
        }""", selectors)
    try:
        page.wait_for_function("""selectors => {
           const root = document.querySelector('.markdown-body');
           if (!root || !root.innerText.includes('Theorem 1.4')) return false;
           const css = Object.values(selectors).join(',');
           return Array.from(root.querySelectorAll(css)).filter(el => {
              const r = el.getBoundingClientRect();
              return r.width > 2 && r.height > 2;
           }).length >= 7;
        }""", arg=selectors, timeout=25000)
    except PlaywrightTimeoutError:
        pass  # Evidence must still be written before failing closed.

    observed = snapshot()
    observed["scriptErrors"] = errors[:10]
    Path("readback/github-diagnostic.json").write_text(
        json.dumps(observed, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    page.screenshot(path="readback/github-page-viewport.png", full_page=False)
    counts = observed["counts"]
    math_count = max(counts.values(), default=0)
    valid = (observed["rootFound"] and math_count >= 7
             and all(observed["markers"].values())
             and observed["unprocessedMath"] == 0 and not errors)
    if not valid:
        page.close()
        raise RuntimeError("GitHub rich-rendered math UNVERIFIED; "
                           "bounded screenshot and DOM diagnostic preserved: " +
                           json.dumps(observed, sort_keys=True)[:2200])

    # The element must have nonzero layout and be on the rendered page.
    winner = max(selectors, key=lambda name: counts[name])
    page.locator(".markdown-body " + selectors[winner]).first.screenshot(
        path="readback/github-first-rendered-math.png", timeout=20000)
    dom_hash = hashlib.sha256(page.content().encode("utf-8")).hexdigest()
    page.close()
    return {"url": url, "status": "PASS", "observed": observed,
            "renderedMath": math_count, "renderer": winner,
            "dom_sha256": dom_hash}


def main() -> None:
    args = argparse.ArgumentParser()
    args.add_argument("--url", default=PUBLIC)
    options = args.parse_args()
    if options.url != PUBLIC:
        raise SystemExit("Refusing unbound public URL")
    Path("readback").mkdir(exist_ok=True)
    from playwright.sync_api import sync_playwright
    import os
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        result = verify(browser)
        # Durable site-only evidence is diagnostic, not an admission.
        provisional = dict(result, status="PARTIAL", github_render={"status": "UNVERIFIED"})
        Path("readback/mkdocs-only.json").write_text(
            json.dumps(provisional, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        result["github_render"] = verify_github(browser, os.environ["DEPLOYED_SHA"])
        browser.close()
    Path("readback/readback.json").write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("ERDOS_COMPENDIUM_PUBLIC_HTML_READBACK/1", json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
