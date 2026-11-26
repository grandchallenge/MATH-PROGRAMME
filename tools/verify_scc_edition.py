#!/usr/bin/env python3
"""Bounded browser replay for the SCC chapter. Run after mkdocs build --strict."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import json
import threading
from playwright.sync_api import sync_playwright

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--site", default="site")
    p.add_argument("--screenshots", type=Path)
    args = p.parse_args()
    root = Path(args.site).resolve()
    assert (root / "scc/index.html").is_file(), "Build MkDocs first."
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=str(root)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    results = []
    try:
        with sync_playwright() as w:
            browser = w.chromium.launch(headless=True)
            for width, height, scheme in [(1440, 1000, "light"), (390, 844, "light"), (1440, 1000, "dark")]:
                page = browser.new_page(viewport={"width": width, "height": height},
                                        color_scheme=scheme, device_scale_factor=1)
                page.goto(base + "/scc/", wait_until="domcontentloaded", timeout=15000)
                page.wait_for_function("""Array.from(document.querySelectorAll('.scc-plate img')).length===8 &&
                    Array.from(document.querySelectorAll('.scc-plate img')).every(x=>x.complete && x.naturalWidth>0)""", timeout=10000)
                page.wait_for_function("""document.querySelectorAll('mjx-container').length >=
                    document.querySelectorAll('.arithmatex').length && document.querySelectorAll('.arithmatex').length>10""", timeout=15000)
                result = page.evaluate("""()=>({
                    width:innerWidth, scrollWidth:document.documentElement.scrollWidth,
                    plates:document.querySelectorAll('.scc-plate').length,
                    loaded:[...document.querySelectorAll('.scc-plate img')].filter(x=>x.naturalWidth>0).length,
                    captions:[...document.querySelectorAll('.scc-plate figcaption')].filter(x=>x.innerText.length>20).length,
                    alt:[...document.querySelectorAll('.scc-plate img')].filter(x=>x.alt.length>30).length,
                    fullSize:[...document.querySelectorAll('.scc-plate > a')].filter(x=>x.href.endsWith('.svg')).length,
                    math:document.querySelectorAll('mjx-container').length,
                    mathErrors:document.querySelectorAll('mjx-merror').length,
                    mathWrappers:document.querySelectorAll('.arithmatex').length,
                    nav:[...document.querySelectorAll('nav a')].some(x=>x.textContent.trim()==='Structural Capacity Calculus'),
                    currentResearch:[...document.querySelectorAll('nav a')].filter(x=>x.textContent.trim()==='Current Research').map(x=>new URL(x.href).pathname),
                    overflows:[...document.querySelectorAll('.scc-plate')].filter(x=>x.getBoundingClientRect().right>innerWidth+1).length,
                    heroY:Math.round(document.querySelector('.scc-plate').getBoundingClientRect().top)
                })""")
                result["scheme"] = scheme
                results.append(result)
                if args.screenshots:
                    page.screenshot(path=str(args.screenshots / f"page-{width}-{scheme}.png"))
                    if width == 1440 and scheme == "light":
                        page.locator(".scc-plate").nth(6).screenshot(path=str(args.screenshots / "spectators.png"))
                page.close()
            page = browser.new_page()
            page.goto(base + "/pnp_above/primer/", wait_until="domcontentloaded")
            assert page.locator("#structural-capacity-calculus-why-relationships-resist-compression").count() == 1
            assert page.locator("#scc-relations-between-relationships").count() == 1
            assert page.locator("article a[href='../../scc/']").count() >= 1
            assert page.locator("article a[href='../../scc/#iv-relations-between-relationships']").count() == 1
            browser.close()
        print(json.dumps(results, indent=2))
        for x in results:
            assert x["plates"] == x["loaded"] == x["alt"] == x["captions"] == x["fullSize"] == 8
            assert x["nav"] and x["currentResearch"] and all(y != "/scc/" for y in x["currentResearch"])
            assert x["overflows"] == x["mathErrors"] == 0 and x["scrollWidth"] <= x["width"] + 2
            assert x["math"] == x["mathWrappers"] and x["math"] > 10
        print("PASS: 8 plates, mathematical glyphs, navigation, anchors and responsive layout.")
    finally:
        server.shutdown()

if __name__ == "__main__":
    main()
