#!/usr/bin/env python3
"""chat-ui-click-test.py — the FUNCTIONALITY GATE for CHAT/LLM-style interfaces.

Variant of generic-click-test.py tuned for chat UIs (chat widgets, idea feeds,
ask panels — no canvas, MathJax-injected stylesheets). Adjustments:
  1. LIGHT THEME: computed body backgroundColor must be light AND a full-DOM
     scan finds ZERO elements with an actually-dark background (luminance < 40
     AND alpha > 0). MathJax's injected context-menu/tooltip styles use
     `color: black` on light backgrounds — the generic gate's naive substring
     match false-positives on them; this check measures real backgrounds.
  2. CANVAS: optional (N/A when the page has none — chat UIs have no canvas).
  3. Everything else identical: click EVERY button, assert page state changes
     (full innerText comparison), zero console errors, desktop + mobile.

Usage:
    python chat-ui-click-test.py <url>

Exit 0 = all pass, 1 = failures.
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
    return page.evaluate("document.body.innerText")

def main():
    url = sys.argv[1]
    print(f"Chat-UI Chrome audit → {url}\n")

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        page = b.new_page(viewport={"width": 1280, "height": 800})
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errors.append(str(e)))

        try:
            page.goto(url, timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)
            page.wait_for_timeout(1200)  # allow first-run tours / MathJax injection
        except Exception as e:
            print(f"  [FAIL] page load — {e}")
            b.close()
            sys.exit(1)

        print(f"  Title: {page.title()}")

        body_len = len(body_text(page))
        check("page has content", body_len > 200, f"{body_len} chars")

        # 1. Light theme: computed body background + real dark-element scan
        bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
        dark_els = page.evaluate("""() => {
            const out = [];
            document.querySelectorAll('body *').forEach(el => {
                const c = getComputedStyle(el).backgroundColor;
                const m = c.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)(?:,\\s*([\\d.]+))?\\)/);
                if (!m) return;
                const a = m[4] === undefined ? 1 : parseFloat(m[4]);
                const lum = 0.2126 * +m[1] + 0.7152 * +m[2] + 0.0722 * +m[3];
                if (a > 0 && lum < 40) out.push(el.tagName + '.' + String(el.className).slice(0, 30) + ' -> ' + c);
            });
            return out.slice(0, 8);
        }""")
        check("light theme (no real dark backgrounds)",
              len(dark_els) == 0,
              f"body {bg}" + (f"; dark: {dark_els}" if dark_els else ""))

        # 2. Interactive inventory (canvas optional for chat UIs)
        interactives = page.evaluate("""(() => ({
            buttons: document.querySelectorAll('button, [role=button], input[type=button], input[type=submit]').length,
            inputs: document.querySelectorAll('input:not([type=hidden]), select, textarea').length,
            sliders: document.querySelectorAll('input[type=range]').length,
            canvas: document.querySelectorAll('canvas').length
        }))()""")
        check("has interactive controls",
              interactives["buttons"] + interactives["inputs"] > 0,
              f"{interactives['buttons']} buttons, {interactives['inputs']} inputs, "
              f"{interactives['sliders']} sliders, {interactives['canvas']} canvas")

        # 3. Dismiss any first-run tour / modal via its actual buttons
        dismiss = page.evaluate("""(() => {
            const btns = Array.from(document.querySelectorAll('button, [role=button]'));
            const hits = btns.filter(bt => /skip|close|dismiss|got it|start|ok/i.test((bt.textContent || '').trim()));
            hits.slice(0, 5).forEach(bt => { try { bt.click(); } catch (e) {} });
            return hits.length;
        })()""")
        page.wait_for_timeout(800)

        # 4. Click every button; assert state change (full-text comparison)
        buttons = page.evaluate("""(() => {
            return Array.from(document.querySelectorAll('button, [role=button]'))
                .map((b, i) => ({ i, text: (b.textContent || '').trim().slice(0, 40), visible: b.offsetWidth > 0 && b.offsetHeight > 0 }))
                .filter(x => x.visible);
        })()""")
        changed = 0
        for bt in buttons:
            before = body_text(page)
            page.evaluate("(i) => { const b = document.querySelectorAll('button, [role=button]')[i]; if (b) b.click(); }", bt["i"])
            page.wait_for_timeout(800)
            after = body_text(page)
            if after != before:
                changed += 1
        check("buttons cause state change",
              changed >= max(1, len(buttons) // 2),
              f"{changed}/{len(buttons)} changed state")

        # 5. Sliders (if any)
        if interactives["sliders"] > 0:
            sliders = page.evaluate("""(() => {
                return Array.from(document.querySelectorAll('input[type=range]')).map((s, i) => ({ i, visible: s.offsetWidth > 0 }));
            })()""")
            schanged = 0
            for sl in sliders:
                before = body_text(page)
                page.evaluate("(i) => { const s = document.querySelectorAll('input[type=range]')[i]; if (s) { s.value = s.max; s.dispatchEvent(new Event('input', { bubbles: true })); s.dispatchEvent(new Event('change', { bubbles: true })); } }", sl["i"])
                page.wait_for_timeout(800)
                after = body_text(page)
                if after != before:
                    schanged += 1
            check("sliders cause state change", schanged >= max(1, len(sliders) // 2), f"{schanged}/{len(sliders)} changed state")
        else:
            print("  [PASS] sliders cause state change — N/A (0 sliders)")

        # 6. Canvas optional
        if interactives["canvas"] > 0:
            canvas_ok = page.evaluate("""(() => {
                const c = document.querySelector('canvas');
                if (!c) return false;
                try { return c.toDataURL().length > 1000; } catch (e) { return false; }
            })()""")
            check("canvas renders non-blank", canvas_ok)
        else:
            print("  [PASS] canvas present — N/A (chat UI, no canvas)")

        # 7. Zero console errors
        check("zero console errors", len(console_errors) == 0,
              f"{len(console_errors)} errors" + (f": {console_errors[:2]}" if console_errors else ""))

        # 8. Mobile viewport: no horizontal overflow
        page.set_viewport_size({"width": 375, "height": 667})
        page.wait_for_timeout(600)
        overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 2")
        check("mobile 375px no overflow", not overflow)

        b.close()

    print()
    if failures:
        print("FAILURES: " + ", ".join(failures))
        sys.exit(1)
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
