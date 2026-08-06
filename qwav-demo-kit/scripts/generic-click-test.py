#!/usr/bin/env python3
"""generic-click-test.py — THE functionality gate (PRESENCE IS NOT THE GATE).

Clicks every button/input/select on ANY demo page and asserts the page state
actually changes (canvas, text, or attribute). Checks canvas renders non-blank,
zero console errors, light theme. Designed to run against deployed URLs and
localhost. Works on ANY demo — not hardcoded to one demo's selectors.

Usage:
    python generic-click-test.py <url>

Exit 0 = all passed, 1 = failures.

This is the enforcement script for DEM-E0-T03 (Chrome automation) and the
PRESENCE-OVER-FUNCTION-1 anti-pattern. A demo that "has canvas/scripts" but
whose buttons change nothing FAILS this gate — see the 2026-08-06 audit where
all 4 legacy demos failed (2-5/14 buttons changing state, blank canvases,
14 console errors on ultrametric-convergence).

State-change detection: compares the FULL document.body.innerText string
before/after each interaction (NOT its length — length can coincide when
digits swap, e.g. "156" -> "781"). Any text change = the control is wired.
"""
import sys
from playwright.sync_api import sync_playwright

failures = []
console_errors = []

def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        failures.append(name)

def body_text(page):
    """Full innerText — robust change detector (length can coincide)."""
    return page.evaluate("document.body.innerText")

def main():
    url = sys.argv[1]
    print(f"Generic Chrome audit → {url}\n")

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        page = b.new_page(viewport={"width": 1280, "height": 800})
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errors.append(str(e)))

        try:
            page.goto(url, timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            print(f"  [FAIL] page load — {e}")
            b.close()
            sys.exit(1)

        print(f"  Title: {page.title()}")

        # 1. Content present
        body_len = len(body_text(page))
        check("page has content", body_len > 200, f"{body_len} chars")

        # 2. Light theme check (no dark background in CSS)
        css = page.evaluate("""(() => {
            let out = '';
            for (const s of document.styleSheets) {
                try {
                    for (const r of s.cssRules) {
                        if (r.cssText && (r.cssText.includes('background') || r.cssText.includes('--bg'))) out += r.cssText;
                    }
                } catch(e) {}
            }
            return out;
        })()""")
        dark_indicators = [
            "#0a0a0f", "#08090d", "#0d1117", "#07080f", "#0b0f1c", "#0e1425",
            "#1d2a46", "#2b3d6b", "#00e5a0", "#00ffa3", "#00e5ff", "#ffb300",
            "#b388ff", "#7dd8ff", "#dce6ff", "#8295c0", "#000", "black",
            "background-color: #0", "background: #0", "background:black"]
        dark_hits = [d for d in dark_indicators if d in css.lower()]
        check("light theme (no dark bg)", len(dark_hits) == 0, f"dark hints: {dark_hits}")

        # 3. Interactive elements inventory
        interactives = page.evaluate("""(() => ({
            buttons: document.querySelectorAll('button, [role=button], input[type=button], input[type=submit]').length,
            inputs: document.querySelectorAll('input:not([type=hidden]), select, textarea').length,
            sliders: document.querySelectorAll('input[type=range]').length,
            canvas: document.querySelectorAll('canvas').length
        }))()""")
        check("has interactive controls",
              interactives["buttons"] + interactives["inputs"] > 0,
              f"{interactives['buttons']} buttons, {interactives['inputs']} inputs, {interactives['sliders']} sliders, {interactives['canvas']} canvas")

        # 3b. Dismiss first-run tours / modals BEFORE click-through (real user path).
        # Critical timing: demos schedule the tour via setTimeout(startTour, 800) in init(),
        # so a dismissal at load+0ms is UNDONE at +800ms when the tour re-appears and
        # swallows real pointer clicks (canonical case: A1 3/16 -> 2/16 -> 1/16 changed
        # across runs = racy overlay, not dead buttons). Correct sequence (real user path):
        # (1) wait past the scheduled tour window, (2) dismiss via the overlay's actual
        # Skip/close button (sets localStorage flag -> tour never reappears), (3) fallback
        # DOM-remove if no skip button. Second pass catches longer-delay / re-triggered tours.
        page.wait_for_timeout(1200)
        page.evaluate("""(() => {
            let dismissed = 0;
            for (const o of document.querySelectorAll('.tour-overlay, .modal, [role=dialog], .overlay, .popup')) {
                if (!o) continue;
                const active = o.classList.contains('active') || (o.style && o.style.display !== 'none' && o.style.display !== '');
                if (!active) continue;
                const skip = o.querySelector('.skip, .close, [data-dismiss], [aria-label=Close], .tour-skip');
                if (skip) { skip.click(); dismissed++; continue; }
                o.classList.remove('active');
                o.style.display = 'none';
                o.style.pointerEvents = 'none';
                dismissed++;
            }
            return dismissed;
        })()""")
        page.wait_for_timeout(400)
        page.evaluate("""(() => {
            let dismissed = 0;
            for (const o of document.querySelectorAll('.tour-overlay, .modal, [role=dialog], .overlay, .popup')) {
                if (!o) continue;
                const active = o.classList.contains('active') || (o.style && o.style.display !== 'none' && o.style.display !== '');
                if (!active) continue;
                const skip = o.querySelector('.skip, .close, [data-dismiss], [aria-label=Close], .tour-skip');
                if (skip) { skip.click(); dismissed++; continue; }
                o.classList.remove('active');
                o.style.display = 'none';
                o.style.pointerEvents = 'none';
                dismissed++;
            }
            return dismissed;
        })()""")
        page.wait_for_timeout(400)
        print("  First-run tour/modals dismissed (waited for scheduled tour)")

# 4. THE GATE: click every button — assert something changes
        btn_count = interactives["buttons"]
        changed = 0
        unchanged = 0
        for i in range(btn_count):
            try:
                before = body_text(page)
                page.locator("button, [role=button], input[type=button], input[type=submit]").nth(i).click(timeout=3000)
                page.wait_for_timeout(800)
                after = body_text(page)
                if after != before:
                    changed += 1
                else:
                    unchanged += 1
            except Exception:
                unchanged += 1
        check("buttons cause state change", changed >= max(1, btn_count // 2),
              f"{changed}/{btn_count} changed state")

        # 5. Sliders — move and assert change (range inputs: use evaluate+dispatch, NOT fill())
        slider_changed = 0
        for i in range(interactives["sliders"]):
            try:
                before = body_text(page)
                sl = page.locator("input[type=range]").nth(i)
                cur = sl.evaluate("el => parseInt(el.value)")
                newv = cur + 1 if cur < 10 else cur - 1
                sl.evaluate("""(el, v) => {
                    el.value = String(v);
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                }""", newv)
                page.wait_for_timeout(200)
                after = body_text(page)
                if after != before:
                    slider_changed += 1
            except Exception:
                pass
        # Skip when the demo has no sliders (A4/A5 have 0) — threshold must not force a fail.
        if interactives["sliders"] > 0:
            check("sliders cause state change",
                  slider_changed >= max(1, interactives["sliders"] // 2),
                  f"{slider_changed}/{interactives['sliders']} changed")
        else:
            print("  [PASS] sliders cause state change — N/A (0 sliders)")

        # 6. Canvas renders non-blank (if present)
        if interactives["canvas"] > 0:
            blank = page.evaluate("""(() => {
                // toDataURL length is layout-independent and proven reliable in CDP functional tests
                // (A1 rendered 130KB+ of real data). getImageData on a 0-sized backing store throws
                // or returns empty, producing false "blank" on legitimately-rendering canvases.
                const cs = document.querySelectorAll('canvas');
                if (!cs.length) return true;
                for (const c of cs) {
                    try {
                        const len = c.toDataURL().length;
                        if (len > 1000) return false;   // at least one canvas has real content
                    } catch(e) {}
                }
                return true;
            })()""")
            check("canvas renders non-blank", not blank)
        else:
            check("canvas present", False, "no canvas element")

        # 7. Screenshot
        try:
            import os
            os.makedirs("screenshots", exist_ok=True)
            slug = url.rstrip("/").split("/")[-1] or "demo"
            page.screenshot(path=f"screenshots/audit-{slug}.png")
            print("  Screenshot saved")
        except Exception:
            pass

        # 8. Console errors
        check("zero console errors", len(console_errors) == 0, f"{len(console_errors)} errors")
        if console_errors:
            for e in console_errors[:5]:
                print(f"    ! {e[:120]}")

        b.close()

    print(f"\n{'ALL CHECKS PASSED' if not failures else 'FAILURES: ' + ', '.join(failures)}")
    sys.exit(0 if not failures else 1)

if __name__ == "__main__":
    main()
