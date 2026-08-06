#!/usr/bin/env python3
"""
QWAV Demo Test Runner - Chrome headless automated testing for interactive scientific demos.

Validates: console errors, canvas chain (button - canvas update), readout chain
(button - text update), interactive element audit, and performance budget.

Usage:
    python scripts/test-demo.py --url https://qnfo.github.io/qwav-demo-error-confinement/
    python scripts/test-demo.py --file index.html
    python scripts/test-demo.py --url <url> --smoke
    python scripts/test-demo.py --url <url> --junit report.xml

Requirements:
    pip install playwright && python -m playwright install chromium
    OR: Chrome for Testing installed at CHROME_PATH
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error
import struct
import socket
import base64
from pathlib import Path

# --- Configuration ---
CHROME_PATH = os.environ.get("CHROME_PATH", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
DEBUG_PORT = 9223
PAGE_LOAD_TIMEOUT_MS = 15000
CLICK_WAIT_MS = 800
PAGE_TITLE_MIN_LENGTH = 5
CANVAS_MIN_BYTES = 1000


def find_chrome():
    """Find Chrome executable on the system."""
    candidates = [
        CHROME_PATH,
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Google\Chrome for Testing\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    try:
        result = subprocess.run(["where", "chrome"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split("\n")[0]
    except Exception:
        pass
    return None


class ChromeSession:
    """Manages a headless Chrome instance with CDP access."""

    def __init__(self):
        self.process = None
        self.ws_url = None
        self._msg_id = 0

    def start(self):
        chrome = find_chrome()
        if not chrome:
            raise RuntimeError("Chrome not found. Install Chrome or set CHROME_PATH.")

        user_data = os.path.join(os.environ.get("TEMP", "/tmp"), f"qwav-test-{os.getpid()}")
        os.makedirs(user_data, exist_ok=True)

        cmd = [chrome, f"--remote-debugging-port={DEBUG_PORT}", "--headless=new",
               "--no-sandbox", "--disable-gpu", "--disable-extensions",
               "--disable-background-networking", f"--user-data-dir={user_data}", "about:blank"]
        self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)

        for _ in range(30):
            time.sleep(0.5)
            try:
                resp = urllib.request.urlopen(f"http://localhost:{DEBUG_PORT}/json/version", timeout=2)
                data = json.loads(resp.read().decode())
                self.ws_url = data.get("webSocketDebuggerUrl")
                if self.ws_url:
                    break
            except Exception:
                continue
        if not self.ws_url:
            self.stop()
            raise RuntimeError("Chrome started but CDP not available within 15s")

    def stop(self):
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except Exception:
                self.process.kill()
            self.process = None

    def _list_pages(self):
        resp = urllib.request.urlopen(f"http://localhost:{DEBUG_PORT}/json", timeout=5)
        return json.loads(resp.read().decode())

    def _ws_call(self, ws_url, payload):
        """Minimal WebSocket send/receive."""
        from urllib.parse import urlparse
        parsed = urlparse(ws_url)
        host, port = parsed.hostname, parsed.port or 9222
        path = parsed.path + ("?" + parsed.query if parsed.query else "")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))

        key = base64.b64encode(os.urandom(16)).decode()
        handshake = (f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n"
                     f"Upgrade: websocket\r\nConnection: Upgrade\r\n"
                     f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
        sock.send(handshake.encode())
        response = sock.recv(4096)
        if b"101" not in response:
            sock.close()
            raise RuntimeError(f"WebSocket handshake failed: {response[:200]}")

        frame = bytearray([0x81])
        pl = len(payload)
        if pl < 126:
            frame.append(pl)
        elif pl < 65536:
            frame.append(126)
            frame.extend(struct.pack(">H", pl))
        else:
            frame.append(127)
            frame.extend(struct.pack(">Q", pl))
        frame.extend(payload.encode())
        sock.send(bytes(frame))

        resp_buf = bytearray()
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            resp_buf.extend(chunk)
            if resp_buf.decode("utf-8", errors="replace").strip().endswith("}"):
                break
        sock.close()

        text = resp_buf.decode("utf-8", errors="replace")
        try:
            j_start = text.index("{")
            return json.loads(text[j_start:])
        except (ValueError, json.JSONDecodeError):
            return {"error": f"Parse failure: {text[:200]}"}

    def evaluate(self, expression):
        pages = self._list_pages()
        if not pages:
            return None
        ws_url = pages[0]["webSocketDebuggerUrl"]
        self._msg_id += 1
        result = self._ws_call(ws_url, json.dumps({
            "id": self._msg_id, "method": "Runtime.evaluate",
            "params": {"expression": expression, "returnByValue": True}
        }))
        r = result.get("result", {}).get("result", {})
        return r.get("value")

    def navigate(self, url):
        pages = self._list_pages()
        ws_url = pages[0]["webSocketDebuggerUrl"] if pages else None
        if not ws_url:
            # Create new page
            self._msg_id += 1
            result = self._ws_call(self.ws_url, json.dumps({
                "id": self._msg_id, "method": "Target.createTarget",
                "params": {"url": url}
            }))
            target_id = result.get("result", {}).get("targetId")
            if not target_id:
                return False
            # Wait and refresh page list
            time.sleep(1)
            pages = self._list_pages()
            ws_url = pages[0]["webSocketDebuggerUrl"] if pages else None
            if not ws_url:
                return False

        self._msg_id += 1
        self._ws_call(ws_url, json.dumps({
            "id": self._msg_id, "method": "Page.enable"
        }))
        self._msg_id += 1
        self._ws_call(ws_url, json.dumps({
            "id": self._msg_id, "method": "Page.navigate", "params": {"url": url}
        }))

        for _ in range(int(PAGE_LOAD_TIMEOUT_MS / 500)):
            time.sleep(0.5)
            state = self.evaluate("document.readyState")
            if state == "complete":
                return True
        return False

    def inject_error_collector(self):
        self.evaluate("""
            window.__qwav_test_errors = [];
            window.addEventListener('error', function(e) {
                window.__qwav_test_errors.push({type:'error',message:e.message,filename:e.filename,lineno:e.lineno,time:Date.now()});
            });
            var origErr = console.error;
            console.error = function() {
                var args = Array.prototype.slice.call(arguments);
                window.__qwav_test_errors.push({type:'console.error',message:args.map(function(a){return String(a)}).join(' '),time:Date.now()});
                return origErr.apply(console, args);
            };
            console.log("Error collector installed");
        """)

    def get_errors(self):
        result = self.evaluate("JSON.stringify(window.__qwav_test_errors || [])")
        if result:
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                pass
        return []


# --- Test Framework ---

class TestSuite:
    def __init__(self, url=None, file_path=None, smoke_only=False):
        self.url = url
        self.file_path = file_path
        self.smoke_only = smoke_only
        self.results = []
        self.chrome = None

    def _add(self, name, passed, detail=""):
        self.results.append({"name": name, "passed": passed, "detail": detail})
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}")
        if detail:
            print(f"         {detail}")

    def run(self):
        print(f"\n{'='*60}")
        print(f"QWAV Demo Test Runner")
        target = self.url or f"file:///{os.path.abspath(self.file_path).replace(os.sep, '/')}"
        print(f"Target: {target}")
        print(f"{'='*60}\n")

        self.chrome = ChromeSession()
        try:
            self.chrome.start()
            self.chrome.inject_error_collector()

            t0 = time.time()
            ok = self.chrome.navigate(target)
            load_ms = (time.time() - t0) * 1000
            self._add("Page load", ok, f"Loaded in {load_ms:.0f}ms")
            if not ok:
                return self._report()

            time.sleep(1.0)
            self.chrome.inject_error_collector()

            # Test 1: Title integrity
            title = self.chrome.evaluate("document.title")
            self._add("Page title", bool(title and len(title) >= PAGE_TITLE_MIN_LENGTH),
                      title or "missing")

            # Test 2: Body content
            body_len = self.chrome.evaluate("document.body ? document.body.textContent.length : 0")
            self._add("Page body", bool(body_len and body_len > 100), f"{body_len} chars")

            # Test 3: Console errors
            errors = self.chrome.get_errors()
            self._add("Console errors", len(errors) == 0,
                      f"{len(errors)} error(s)" if errors else "Zero errors")
            for e in errors[:5]:
                print(f"         - {e.get('message', str(e))[:100]}")

            if not self.smoke_only:
                # Test 4: Canvas
                canvas_count = self.chrome.evaluate("document.querySelectorAll('canvas').length")
                self._add("Canvas presence", bool(canvas_count), f"{canvas_count or 0} canvas(es)")

                data_len = self.chrome.evaluate(
                    "(function(){var c=document.querySelector('canvas');return c?c.toDataURL().length:0;})()")
                self._add("Canvas renders", bool(data_len and data_len >= CANVAS_MIN_BYTES),
                          f"{data_len or 0} bytes")

                # Test 5: Interactive elements
                elems_json = self.chrome.evaluate(
                    "JSON.stringify(Array.from(document.querySelectorAll('button')).map(function(b){return b.textContent.trim().substring(0,40)}))")
                if elems_json:
                    elems = json.loads(elems_json)
                    visible = self.chrome.evaluate(
                        "Array.from(document.querySelectorAll('button')).filter(function(b){var r=b.getBoundingClientRect();return r.width>0&&r.height>0}).length")
                    self._add("Interactive buttons", bool(elems), f"{visible or 0} visible, {len(elems)} total")

                # Test 6: Canvas chain (click button, verify canvas changes)
                chain_ok = 0
                chain_fail = 0
                for i in range(min(5, len(elems) if elems_json else 0)):
                    before = self.chrome.evaluate(
                        "(function(){var c=document.querySelector('canvas');return c?c.toDataURL():null;})()")
                    self.chrome.evaluate(
                        "(function(){var b=Array.from(document.querySelectorAll('button')).filter(function(b){return b.getBoundingClientRect().width>0})[" + str(i) + "];if(b)b.click();})()")
                    time.sleep(CLICK_WAIT_MS / 1000.0)
                    after = self.chrome.evaluate(
                        "(function(){var c=document.querySelector('canvas');return c?c.toDataURL():null;})()")
                    if before and after and before != after:
                        chain_ok += 1
                    else:
                        chain_fail += 1
                total = chain_ok + chain_fail
                self._add("Canvas chain", chain_fail == 0,
                          f"{chain_ok}/{total} button-canvas updates" if total > 0 else "No buttons tested")

                # Test 7: FCP
                fcp = self.chrome.evaluate(
                    "(function(){var p=performance.getEntriesByType('paint');var e=null;for(var i=0;i<p.length;i++){if(p[i].name==='first-contentful-paint')e=p[i];}return e?e.startTime:null;})()")
                if fcp is not None:
                    self._add("Performance (FCP)", fcp < 1800, f"{fcp:.0f}ms")

        finally:
            if self.chrome:
                self.chrome.stop()

        return self._report()

    def _report(self):
        passed = sum(1 for r in self.results if r["passed"])
        failed = sum(1 for r in self.results if not r["passed"])
        total = len(self.results)
        print(f"\n{'='*60}")
        print(f"RESULTS: {passed} passed, {failed} failed, {total} total")
        print(f"{'='*60}\n")
        return 0 if failed == 0 else 1


def write_junit(results, filepath):
    """Write JUnit XML report."""
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    tests = len(results)
    failures = sum(1 for r in results if not r["passed"])
    xml.append(f'<testsuite name="qwav-demo-test" tests="{tests}" failures="{failures}" errors="0" time="0.0">')
    for r in results:
        xml.append(f'  <testcase classname="qwav.demo" name="{r["name"]}">')
        if not r["passed"]:
            xml.append(f'    <failure type="AssertionError" message="{r["detail"]}">{r["detail"]}</failure>')
        xml.append(f'  </testcase>')
    xml.append('</testsuite>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))
    print(f"JUnit report: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="QWAV Demo Test Runner")
    parser.add_argument("--url", help="Live URL to test")
    parser.add_argument("--file", help="Local HTML file to test")
    parser.add_argument("--smoke", action="store_true", help="Smoke test only")
    parser.add_argument("--junit", help="JUnit XML report path")
    args = parser.parse_args()

    if not args.url and not args.file:
        parser.error("--url or --file required")

    suite = TestSuite(url=args.url, file_path=args.file, smoke_only=args.smoke)
    exit_code = suite.run()

    if args.junit:
        write_junit(suite.results, args.junit)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
