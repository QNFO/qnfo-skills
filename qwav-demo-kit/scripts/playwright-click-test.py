#!/usr/bin/env python3
"""playwright-click-test.py — extensive Chrome automated test suite (USER MANDATE).

Usage:
    python playwright-click-test.py <url>

Clicks every control, asserts state changes, captures screenshots,
fails on any console error. Run against BOTH the local dev server
and the deployed URL. Requires: pip install playwright && playwright install chromium

Exit code 0 = ALL PASS.
"""
import sys
from playwright.sync_api import sync_playwright

failures = []
console_errors = []


def check(name, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}")
    if not cond:
        failures.append(name)


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/index.html"
    print(f"Chrome test suite → {url}")

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        page = b.new_page(viewport={"width": 1280, "height": 800})
        page.on("console", lambda msg: console_errors.append(msg.text)
                if msg.type == "error" else None)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        page.goto(url)
        page.wait_for_load_state("networkidle")
        print(f"  Title: {page.title()}")

        # 1. Load sanity
        check("engine loaded",
              page.evaluate("typeof window._demo !== 'undefined' && window._demo.tree !== null"))

        # 2. Prime buttons
        for pval in ["2", "3", "5"]:
            page.click(f'[data-p="{pval}"]')
            check(f"prime={pval} rebuilds",
                  page.evaluate(f"window._demo.tree.p == {pval}"))

        # 3. Depth slider
        page.fill("#depthSlider", "4")
        page.dispatch_event("#depthSlider", "input")
        check("depth=4 rebuilds",
              page.evaluate("window._demo.tree.depth == 4"))
        check("stats update",
              page.evaluate("document.getElementById('statNodes').textContent") ==
              str(page.evaluate("window._demo.tree.nodeCount")))

        # 4-5. Tabs
        page.click('[data-view="curve"]')
        check("curve tab activates",
              page.evaluate("document.querySelector('[data-view=curve]').classList.contains('active')"))
        page.click('[data-view="tree"]')
        check("tree tab re-activates",
              page.evaluate("document.querySelector('[data-view=tree]').classList.contains('active')"))

        # 6. Compare toggle
        page.click("#btnCompare")
        check("compare toggles indicator",
              page.evaluate("!document.getElementById('cmpInd').classList.contains('off')"))
        page.click("#btnCompare")

        # 7-9. Error mode + canvas
        page.click("#btnError")
        check("error mode indicator on",
              page.evaluate("!document.getElementById('errInd').classList.contains('off')"))
        page.click("#mainCanvas", position={"x": 400, "y": 150})
        ovl = page.evaluate("document.getElementById('overlay').textContent")
        check("error mode updates overlay", len(ovl) > 0)

        # 10. Reset
        page.click("#btnReset")
        check("reset clears overlay",
              page.evaluate("document.getElementById('overlay').textContent") == "")

        # Screenshots
        page.screenshot(path="screenshots/view-tree.png")
        page.click('[data-view="curve"]')
        page.screenshot(path="screenshots/view-curve.png")
        print("  Screenshots: screenshots/view-tree.png, screenshots/view-curve.png")

        # Mobile viewport
        page.set_viewport_size({"width": 375, "height": 700})
        page.click('[data-view="tree"]')
        page.wait_for_timeout(300)
        overflow = page.evaluate(
            "document.documentElement.scrollWidth > document.documentElement.clientWidth")
        check("no horizontal overflow at 375px", not overflow)
        page.screenshot(path="screenshots/view-mobile.png")

        b.close()

    check("zero console errors", len(console_errors) == 0)
    if console_errors:
        for e in console_errors[:5]:
            print(f"    console error: {e}")

    print(f"\n{'ALL CHECKS PASSED' if not failures else 'FAILURES: ' + ', '.join(failures)}")
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
